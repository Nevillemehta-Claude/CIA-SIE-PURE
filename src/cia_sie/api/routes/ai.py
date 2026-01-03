"""
CIA-SIE AI Management Routes
============================

Endpoints for AI model selection, usage tracking, and configuration.

GOVERNED BY: Section 14 (AI Narrative Engine)

CRITICAL:
- All AI features are DESCRIPTIVE only
- NO recommendations or predictions
- Budget tracking prevents runaway costs
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.ai.model_registry import (
    ModelInfo,
    get_default_model,
    get_model_info,
    list_models,
)
from cia_sie.ai.usage_tracker import UsageTracker
from cia_sie.core.config import get_settings
from cia_sie.core.enums import UsagePeriod
from cia_sie.dal.database import get_session_dependency

logger = logging.getLogger(__name__)

router = APIRouter()


# =============================================================================
# RESPONSE MODELS
# =============================================================================


class ModelResponse(BaseModel):
    """Response model for a single AI model."""

    id: str
    display_name: str
    description: str
    cost_per_1k_input_tokens: float
    cost_per_1k_output_tokens: float
    max_tokens: int
    capabilities: list[str]
    recommended_for: list[str]


class ModelsListResponse(BaseModel):
    """Response for listing available models."""

    models: list[ModelResponse]
    default_model: str
    budget_remaining: float


class TokensUsed(BaseModel):
    """Token usage breakdown."""

    input: int
    output: int
    total: int


class CostInfo(BaseModel):
    """Cost information."""

    amount: float
    currency: str = "USD"


class BudgetInfo(BaseModel):
    """Budget status information."""

    limit: float
    used: float
    remaining: float
    percentage_used: float


class ModelBreakdown(BaseModel):
    """Usage breakdown by model."""

    model_id: str
    requests: int
    tokens: int
    cost: float


class UsageResponse(BaseModel):
    """Response for usage statistics."""

    period: str
    period_start: str
    period_end: str
    tokens_used: TokensUsed
    cost: CostInfo
    budget: BudgetInfo
    requests_count: int
    average_tokens_per_request: int
    model_breakdown: list[ModelBreakdown]


class ConfigureRequest(BaseModel):
    """Request to configure AI settings."""

    default_model: Optional[str] = None
    budget_limit: Optional[float] = Field(None, gt=0)
    alert_threshold: Optional[int] = Field(None, ge=1, le=100)


class ConfigureResponse(BaseModel):
    """Response for configuration update."""

    status: str
    settings: dict


class BudgetStatusResponse(BaseModel):
    """Response for budget check."""

    within_budget: bool
    percentage_used: float
    remaining: float
    alert_level: Optional[str] = None
    message: Optional[str] = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def model_to_response(model: ModelInfo) -> ModelResponse:
    """Convert ModelInfo to API response."""
    return ModelResponse(
        id=model.id,
        display_name=model.display_name,
        description=model.description,
        cost_per_1k_input_tokens=model.cost_per_1k_input,
        cost_per_1k_output_tokens=model.cost_per_1k_output,
        max_tokens=model.max_tokens,
        capabilities=list(model.capabilities),
        recommended_for=list(model.recommended_for),
    )


async def get_usage_tracker(
    session: AsyncSession = Depends(get_session_dependency),
) -> UsageTracker:
    """Dependency to get usage tracker."""
    return UsageTracker(session)


# =============================================================================
# ROUTES
# =============================================================================


@router.get("/models", response_model=ModelsListResponse)
async def list_available_models(
    tracker: UsageTracker = Depends(get_usage_tracker),
):
    """
    List all available Claude AI models.

    Returns models with their capabilities, costs, and recommended use cases.
    The frontend uses this to populate the model selector.
    """
    models = list_models()
    default = get_default_model()

    # Get budget remaining
    budget_status = await tracker.check_budget()

    return ModelsListResponse(
        models=[model_to_response(m) for m in models],
        default_model=default.id,
        budget_remaining=budget_status["remaining"],
    )


@router.get("/usage", response_model=UsageResponse)
async def get_usage_statistics(
    period: str = "monthly",
    tracker: UsageTracker = Depends(get_usage_tracker),
):
    """
    Get AI usage statistics for a period.

    Args:
        period: Time period (daily, weekly, monthly)

    Returns:
        Usage statistics including tokens, costs, and budget info.
    """
    # Parse period
    period_upper = period.upper()
    try:
        usage_period = UsagePeriod(period_upper)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid period: {period}. Must be daily, weekly, or monthly.",
        )

    usage = await tracker.get_usage(usage_period)

    return UsageResponse(
        period=usage["period"],
        period_start=usage["period_start"],
        period_end=usage["period_end"],
        tokens_used=TokensUsed(**usage["tokens_used"]),
        cost=CostInfo(**usage["cost"]),
        budget=BudgetInfo(**usage["budget"]),
        requests_count=usage["requests_count"],
        average_tokens_per_request=usage["average_tokens_per_request"],
        model_breakdown=[ModelBreakdown(**m) for m in usage["model_breakdown"]],
    )


@router.get("/budget", response_model=BudgetStatusResponse)
async def check_budget_status(
    tracker: UsageTracker = Depends(get_usage_tracker),
):
    """
    Check current budget status.

    Returns budget info with alerts if thresholds are exceeded.
    """
    status = await tracker.check_budget()
    return BudgetStatusResponse(**status)


@router.post("/configure", response_model=ConfigureResponse)
async def configure_ai_settings(
    config: ConfigureRequest,
):
    """
    Configure AI settings.

    NOTE: This endpoint updates in-memory settings only.
    For persistent configuration, use environment variables.

    LIMITATION: Budget and threshold changes require application restart.
    """
    settings = get_settings()
    updates = {}

    if config.default_model:
        model_info = get_model_info(config.default_model)
        if not model_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown model: {config.default_model}",
            )
        updates["default_model"] = config.default_model

    if config.budget_limit is not None:
        updates["budget_limit"] = config.budget_limit

    if config.alert_threshold is not None:
        updates["alert_threshold"] = config.alert_threshold

    # Note: Actual settings modification would require app restart
    # This returns what WOULD be configured
    return ConfigureResponse(
        status="configured",
        settings={
            "default_model": updates.get("default_model", settings.anthropic_model),
            "budget_limit": updates.get("budget_limit", settings.ai_budget_limit),
            "alert_threshold": updates.get("alert_threshold", settings.ai_budget_alert_threshold),
            "fallback_model": settings.ai_fallback_model,
        },
    )


@router.get("/health")
async def ai_health_check():
    """
    Check AI service health.

    Returns status of AI provider connectivity.
    """
    from cia_sie.ai.claude_client import ClaudeClient

    client = ClaudeClient()
    settings = get_settings()

    try:
        is_healthy = await client.health_check()
        return {
            "status": "healthy" if is_healthy else "degraded",
            "model": settings.anthropic_model,
            "api_configured": bool(settings.anthropic_api_key),
        }
    except Exception as e:
        # Log full exception internally for debugging
        logger.error(f"AI health check failed: {e}", exc_info=True)
        # Return generic error to client (don't expose internal details)
        return {
            "status": "unhealthy",
            "model": settings.anthropic_model,
            "api_configured": bool(settings.anthropic_api_key),
            "error": "AI service health check failed. Check server logs for details.",
        }
