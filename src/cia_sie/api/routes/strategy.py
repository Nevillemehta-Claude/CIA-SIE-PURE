"""
CIA-SIE Strategy Evaluation Routes
==================================

Endpoint for describing how a stated strategy aligns with current signals.

GOVERNED BY: Section 14 (AI Narrative Engine)

CRITICAL PROHIBITION:
- This endpoint MUST NEVER return recommendations
- This endpoint MUST NEVER return probability of success
- This endpoint MUST NEVER return risk scores
- This endpoint MUST NEVER use "you should" statements

This endpoint DESCRIBES alignment, it does NOT ADVISE.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.ai.claude_client import ClaudeClient
from cia_sie.ai.model_registry import estimate_cost, get_default_model, get_model_info
from cia_sie.ai.response_validator import ensure_disclaimer, validate_ai_response
from cia_sie.ai.usage_tracker import UsageTracker
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.repositories import (
    ChartRepository,
    InstrumentRepository,
    SignalRepository,
    SiloRepository,
)
from cia_sie.exposure.relationship_exposer import RelationshipExposer

logger = logging.getLogger(__name__)

router = APIRouter()

# Mandatory disclaimer for strategy evaluation
STRATEGY_DISCLAIMER = (
    "This analysis describes how your stated strategy aligns with current chart signals. "
    "It is NOT a recommendation to proceed or not proceed. The decision is entirely yours."
)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class StrategyEvaluationRequest(BaseModel):
    """Request to evaluate strategy alignment."""

    scrip_id: str = Field(..., description="Instrument ID")
    strategy_description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="User's stated strategy (e.g., 'I am considering entering a long position')",
    )
    model: Optional[str] = None


class StrategyAnalysis(BaseModel):
    """Analysis of strategy alignment with signals."""

    alignment_with_signals: str
    contradictions_noted: list[str]
    confirmations_noted: list[str]
    freshness_concerns: list[str]


class UsageInfo(BaseModel):
    """Token and cost usage info."""

    input_tokens: int
    output_tokens: int
    cost: float
    model_used: str


class StrategyEvaluationResponse(BaseModel):
    """Response for strategy evaluation."""

    analysis: StrategyAnalysis
    disclaimer: str = STRATEGY_DISCLAIMER
    usage: UsageInfo


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


async def get_signal_context(
    instrument_id: str,
    session: AsyncSession,
) -> dict:
    """
    Get current signal context for an instrument.

    Returns:
        Dict with signals, contradictions, confirmations, freshness issues
    """
    exposer = RelationshipExposer(
        silo_repository=SiloRepository(session),
        chart_repository=ChartRepository(session),
        signal_repository=SignalRepository(session),
    )

    silo_repo = SiloRepository(session)
    silos = await silo_repo.get_by_instrument(instrument_id)

    signals = []
    contradictions = []
    confirmations = []
    freshness_issues = []

    for silo in silos:
        try:
            summary = await exposer.expose_for_silo(str(silo.silo_id))

            for chart in summary.get("charts", []):
                chart_name = chart.get("chart_name", "Unknown")
                freshness = chart.get("freshness", "UNAVAILABLE")

                if chart.get("latest_signal"):
                    signal = chart["latest_signal"]
                    direction = signal.get("direction", "NEUTRAL")
                    signals.append(
                        {
                            "chart": chart_name,
                            "direction": direction,
                            "freshness": freshness,
                        }
                    )

                    if freshness in ["STALE", "UNAVAILABLE"]:
                        freshness_issues.append(f"{chart_name} signal is {freshness}")
                else:
                    signals.append(
                        {
                            "chart": chart_name,
                            "direction": None,
                            "freshness": "UNAVAILABLE",
                        }
                    )
                    freshness_issues.append(f"{chart_name} has no signal")

            for c in summary.get("contradictions", []):
                contradictions.append(
                    f"{c['chart_a_name']} ({c['chart_a_direction']}) "
                    f"contradicts {c['chart_b_name']} ({c['chart_b_direction']})"
                )

            for c in summary.get("confirmations", []):
                confirmations.append(
                    f"{c['chart_a_name']} and {c['chart_b_name']} "
                    f"both show {c['aligned_direction']}"
                )

        except Exception as e:
            logger.warning(f"Error getting silo context: {e}")
            continue

    return {
        "signals": signals,
        "contradictions": contradictions,
        "confirmations": confirmations,
        "freshness_issues": freshness_issues,
    }


def build_strategy_prompt(strategy: str, context: dict) -> tuple[str, str]:
    """
    Build prompts for strategy evaluation.

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    system_prompt = """You are a DESCRIPTIVE analyst for CIA-SIE. Your task is to describe how a user's stated strategy aligns with current chart signals.

CRITICAL RULES - ABSOLUTE PROHIBITIONS:
1. You MUST NEVER recommend whether to proceed or not proceed.
2. You MUST NEVER provide probability of success.
3. You MUST NEVER assign risk scores.
4. You MUST NEVER use words like "should", "recommend", "suggest", "advise".
5. You MUST NEVER say things like "this looks favorable" or "this looks risky".
6. You MUST NEVER imply one direction is "better" or "safer".

Your ONLY job is to DESCRIBE:
- Which signals align with the stated strategy direction
- Which signals contradict the stated strategy direction
- Any contradictions between charts
- Any freshness concerns

You are a MIRROR reflecting data, not an ADVISOR giving opinions.

End every response with: "This analysis describes how your stated strategy aligns with current chart signals. It is NOT a recommendation to proceed or not proceed. The decision is entirely yours."
"""

    # Format signals for prompt
    signal_lines = []
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0
    no_signal_count = 0

    for s in context.get("signals", []):
        direction = s.get("direction")
        if direction == "BULLISH":
            bullish_count += 1
        elif direction == "BEARISH":
            bearish_count += 1
        elif direction == "NEUTRAL":
            neutral_count += 1
        else:
            no_signal_count += 1

        signal_lines.append(
            f"- {s['chart']}: {direction or 'No signal'} (Freshness: {s['freshness']})"
        )

    user_prompt = f"""The user has stated the following strategy:
"{strategy}"

CURRENT CHART SIGNALS:
{chr(10).join(signal_lines)}

Signal Summary (factual only):
- BULLISH signals: {bullish_count}
- BEARISH signals: {bearish_count}
- NEUTRAL signals: {neutral_count}
- No signal: {no_signal_count}

CONTRADICTIONS DETECTED:
{chr(10).join("- " + c for c in context.get("contradictions", [])) or "None detected"}

CONFIRMATIONS DETECTED:
{chr(10).join("- " + c for c in context.get("confirmations", [])) or "None detected"}

FRESHNESS CONCERNS:
{chr(10).join("- " + f for f in context.get("freshness_issues", [])) or "None"}

DESCRIBE (without recommending) how the stated strategy aligns or conflicts with these signals."""

    return system_prompt, user_prompt


# =============================================================================
# ROUTES
# =============================================================================


@router.post("/evaluate", response_model=StrategyEvaluationResponse)
async def evaluate_strategy_alignment(
    request: StrategyEvaluationRequest,
    session: AsyncSession = Depends(get_session_dependency),
):
    """
    Evaluate how a stated strategy aligns with current signals.

    THIS IS NOT A RECOMMENDATION.

    This endpoint describes which signals align with the stated strategy
    and which contradict it. It does NOT advise whether to proceed.

    Args:
        request: Strategy description and instrument ID

    Returns:
        Descriptive analysis of signal alignment (NOT a recommendation)
    """
    # Verify instrument exists
    instrument_repo = InstrumentRepository(session)
    instrument = await instrument_repo.get_by_id(request.scrip_id)
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instrument not found: {request.scrip_id}",
        )

    # Check budget
    tracker = UsageTracker(session)
    budget_status = await tracker.check_budget()
    if not budget_status["within_budget"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI budget exhausted. AI features are temporarily disabled.",
        )

    # Select model
    model_id = request.model
    if not model_id:
        model_info = get_default_model()
        model_id = model_info.id
    else:
        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown model: {model_id}",
            )

    # Get signal context
    context = await get_signal_context(request.scrip_id, session)

    # Build prompts
    system_prompt, user_prompt = build_strategy_prompt(request.strategy_description, context)

    # Generate response
    client = ClaudeClient(model=model_id)
    try:
        response_text = await client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=1500,
            temperature=0.2,  # Lower temperature for more factual responses
        )
    except Exception as e:
        logger.error(f"AI generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable.",
        )

    # Validate response
    validation = validate_ai_response(response_text)
    if not validation.is_valid:
        logger.warning(f"Strategy evaluation validation failed: {validation.violations}")
        # Remediate
        response_text = ensure_disclaimer(response_text)

    # Estimate tokens
    input_tokens = (len(system_prompt.split()) + len(user_prompt.split())) * 4
    output_tokens = len(response_text.split()) * 4

    # Calculate cost
    cost = estimate_cost(model_id, input_tokens, output_tokens)

    # Record usage
    await tracker.record_usage(model_id, input_tokens, output_tokens)

    # Build structured response from context (not from AI response)
    # The AI response is just additional descriptive text
    alignment_text = response_text

    return StrategyEvaluationResponse(
        analysis=StrategyAnalysis(
            alignment_with_signals=alignment_text,
            contradictions_noted=context.get("contradictions", []),
            confirmations_noted=context.get("confirmations", []),
            freshness_concerns=context.get("freshness_issues", []),
        ),
        disclaimer=STRATEGY_DISCLAIMER,
        usage=UsageInfo(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            model_used=model_id,
        ),
    )
