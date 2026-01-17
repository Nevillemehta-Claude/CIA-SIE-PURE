"""
CIA-SIE AI Layer
================

AI-powered narrative generation using Claude.

GOVERNED BY: Section 14 (AI Narrative Engine)

CRITICAL CONSTRAINTS:
- All narratives are DESCRIPTIVE, never PRESCRIPTIVE
- NO recommendations, scores, rankings, or confidence levels
- Every narrative must remind user they retain decision authority

VALIDATION:
- All AI responses are validated against constitutional patterns
- Responses failing validation are retried up to 3 times
- Non-compliant responses trigger fallback to template generation
"""

from cia_sie.ai.claude_client import ClaudeClient
from cia_sie.ai.narrative_generator import NarrativeGenerator
from cia_sie.ai.prompt_builder import NarrativePromptBuilder
from cia_sie.ai.response_validator import (
    MANDATORY_DISCLAIMER,
    PROHIBITED_PATTERNS,
    AIResponseValidator,
    ValidatedResponseGenerator,
    ValidationResult,
    ensure_disclaimer,
    validate_ai_response,
)
from cia_sie.core.enums import ValidationStatus

__all__ = [
    # Generators
    "NarrativeGenerator",
    "NarrativePromptBuilder",
    "ClaudeClient",
    # Validators
    "AIResponseValidator",
    "ValidatedResponseGenerator",
    "ValidationResult",
    "ValidationStatus",
    # Convenience functions
    "validate_ai_response",
    "ensure_disclaimer",
    # Constants
    "MANDATORY_DISCLAIMER",
    "PROHIBITED_PATTERNS",
]
