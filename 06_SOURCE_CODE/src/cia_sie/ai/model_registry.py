"""
CIA-SIE AI Model Registry
=========================

Defines available Claude models and their characteristics.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

from dataclasses import dataclass
from typing import Optional

from cia_sie.core.enums import AIModelTier


@dataclass(frozen=True)
class ModelInfo:
    """
    Information about a Claude model.

    Attributes:
        id: Model identifier for API calls
        display_name: Human-friendly name
        tier: Model tier (HAIKU/SONNET/OPUS)
        description: Brief description
        cost_per_1k_input: Cost per 1K input tokens (USD)
        cost_per_1k_output: Cost per 1K output tokens (USD)
        max_tokens: Maximum tokens in response
        capabilities: List of capabilities
        recommended_for: Recommended use cases
    """

    id: str
    display_name: str
    tier: AIModelTier
    description: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_tokens: int
    capabilities: tuple[str, ...]
    recommended_for: tuple[str, ...]


# Available Claude models
CLAUDE_MODELS: dict[str, ModelInfo] = {
    "claude-3-haiku-20240307": ModelInfo(
        id="claude-3-haiku-20240307",
        display_name="Haiku",
        tier=AIModelTier.HAIKU,
        description="Fast responses for simple queries",
        cost_per_1k_input=0.00025,
        cost_per_1k_output=0.00125,
        max_tokens=4096,
        capabilities=("quick_query", "simple_description"),
        recommended_for=("single_chart", "freshness_check"),
    ),
    "claude-3-5-sonnet-20241022": ModelInfo(
        id="claude-3-5-sonnet-20241022",
        display_name="Sonnet",
        tier=AIModelTier.SONNET,
        description="Balanced performance for standard analysis",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_tokens=4096,
        capabilities=("narrative", "multi_chart", "contradiction_description"),
        recommended_for=("silo_narrative", "relationship_analysis"),
    ),
    "claude-sonnet-4-20250514": ModelInfo(
        id="claude-sonnet-4-20250514",
        display_name="Sonnet 4",
        tier=AIModelTier.SONNET,
        description="Latest Sonnet with improved capabilities",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        max_tokens=8192,
        capabilities=("narrative", "multi_chart", "contradiction_description", "complex_analysis"),
        recommended_for=("silo_narrative", "relationship_analysis", "instrument_overview"),
    ),
    "claude-opus-4-20250514": ModelInfo(
        id="claude-opus-4-20250514",
        display_name="Opus 4",
        tier=AIModelTier.OPUS,
        description="Most capable model for complex analysis",
        cost_per_1k_input=0.015,
        cost_per_1k_output=0.075,
        max_tokens=8192,
        capabilities=("complex_analysis", "multi_silo", "comprehensive_narrative"),
        recommended_for=("instrument_overview", "complex_patterns"),
    ),
}

# Default model
DEFAULT_MODEL_ID = "claude-3-5-sonnet-20241022"

# Fallback model (cheap option)
FALLBACK_MODEL_ID = "claude-3-haiku-20240307"


def get_model_info(model_id: str) -> Optional[ModelInfo]:
    """Get model info by ID."""
    return CLAUDE_MODELS.get(model_id)


def get_default_model() -> ModelInfo:
    """Get the default model."""
    return CLAUDE_MODELS[DEFAULT_MODEL_ID]


def get_fallback_model() -> ModelInfo:
    """Get the fallback model."""
    return CLAUDE_MODELS[FALLBACK_MODEL_ID]


def list_models() -> list[ModelInfo]:
    """List all available models."""
    return list(CLAUDE_MODELS.values())


def get_models_by_tier(tier: AIModelTier) -> list[ModelInfo]:
    """Get all models of a specific tier."""
    return [m for m in CLAUDE_MODELS.values() if m.tier == tier]


def estimate_cost(model_id: str, input_tokens: int, output_tokens: int) -> float:
    """
    Estimate cost for a request.

    Args:
        model_id: Model identifier
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in USD
    """
    model = get_model_info(model_id)
    if not model:
        model = get_default_model()

    input_cost = (input_tokens / 1000) * model.cost_per_1k_input
    output_cost = (output_tokens / 1000) * model.cost_per_1k_output

    return round(input_cost + output_cost, 6)
