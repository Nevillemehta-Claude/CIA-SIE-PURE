"""
CIA-SIE AI Response Validator
=============================

Validates AI-generated responses for constitutional compliance.

GOVERNED BY: Section 14.4 (AI Narrative Validation)

This module implements runtime validation to ensure Claude's responses
adhere to the constitutional principles. Responses that violate the
constitution are rejected and regenerated.

CRITICAL: This is a DEFENSE-IN-DEPTH mechanism.
Even if Claude generates non-compliant content, this validator catches it.
"""

import logging
import re
from dataclasses import dataclass
from typing import Optional

from cia_sie.core.enums import ValidationStatus
from cia_sie.core.exceptions import ConstitutionalViolationError

logger = logging.getLogger(__name__)


# =============================================================================
# PROHIBITED PATTERNS (Constitutional Violations)
# =============================================================================

# Each tuple: (pattern, reason, severity)
# Severity: "CRITICAL" = always reject, "WARNING" = log but allow after remediation

PROHIBITED_PATTERNS: list[tuple[str, str, str]] = [
    # Recommendation language
    (r"\byou\s+should\b", "Contains 'you should' - implies recommendation", "CRITICAL"),
    (r"\bi\s+recommend\b", "Contains 'I recommend' - direct recommendation", "CRITICAL"),
    (r"\bi\s+suggest\b", "Contains 'I suggest' - implies recommendation", "CRITICAL"),
    (
        r"\bconsider\s+(buying|selling|entering|exiting)\b",
        "Contains trading action suggestion",
        "CRITICAL",
    ),
    (
        r"\byou\s+might\s+want\s+to\b",
        "Contains 'you might want to' - soft recommendation",
        "CRITICAL",
    ),
    (
        r"\bthe\s+best\s+(action|approach|strategy)\b",
        "Contains 'the best action' - implies recommendation",
        "CRITICAL",
    ),
    (
        r"\ba\s+prudent\s+approach\b",
        "Contains 'a prudent approach' - implies recommendation",
        "CRITICAL",
    ),
    # Trading action language
    (r"\b(buy|sell)\s+now\b", "Contains 'buy/sell now' - direct trading advice", "CRITICAL"),
    (r"\benter\s+(a\s+)?(long|short)\s+position\b", "Contains position entry advice", "CRITICAL"),
    (r"\bexit\s+(your\s+)?position\b", "Contains position exit advice", "CRITICAL"),
    (r"\btake\s+profits?\b", "Contains 'take profit' - trading advice", "CRITICAL"),
    (r"\bcut\s+(your\s+)?loss(es)?\b", "Contains 'cut losses' - trading advice", "CRITICAL"),
    # Aggregation language
    (
        r"\boverall\s+(direction|signal|trend)\s+(is|shows|indicates)\b",
        "Contains overall aggregation",
        "CRITICAL",
    ),
    (r"\bnet\s+(signal|direction|bias)\b", "Contains net aggregation", "CRITICAL"),
    (r"\bconsensus\s+(is|shows|indicates)\b", "Contains consensus aggregation", "CRITICAL"),
    (
        r"\bmajority\s+(of\s+)?(signals?|charts?)\s+(show|indicate|suggest)\b",
        "Contains majority aggregation",
        "CRITICAL",
    ),
    (r"\bon\s+balance\b", "Contains 'on balance' - implies aggregation", "WARNING"),
    # Confidence/probability language
    (r"\bconfidence\s*(level|score)?\s*[:\s]*\d+", "Contains confidence score", "CRITICAL"),
    (
        r"\b\d+\s*%\s*(confident|confidence|probability|chance|likelihood)\b",
        "Contains percentage confidence",
        "CRITICAL",
    ),
    (r"\bprobability\s*(of|that)\b", "Contains probability statement", "CRITICAL"),
    (
        r"\blikely\s+to\s+(rise|fall|increase|decrease|profit|lose)\b",
        "Contains likelihood prediction",
        "CRITICAL",
    ),
    (r"\b(high|low|strong|weak)\s+probability\b", "Contains probability qualifier", "CRITICAL"),
    # Prediction language
    (
        r"\bwill\s+(likely\s+)?(rise|fall|increase|decrease|go\s+up|go\s+down)\b",
        "Contains price prediction",
        "CRITICAL",
    ),
    (
        r"\bexpect(ed)?\s+to\s+(rise|fall|increase|decrease)\b",
        "Contains expectation prediction",
        "CRITICAL",
    ),
    (r"\bforecast\s*(is|shows|indicates)?\b", "Contains forecast", "CRITICAL"),
    (r"\bprice\s+target\b", "Contains price target", "CRITICAL"),
    # Ranking/weighting language
    (
        r"\bmore\s+(reliable|accurate|trustworthy)\s+(than|signal|chart)\b",
        "Contains reliability comparison",
        "CRITICAL",
    ),
    (r"\b(stronger|weaker)\s+signal\b", "Contains signal strength comparison", "CRITICAL"),
    (r"\bsignal\s+strength\s*(is|:)?\s*\d", "Contains signal strength score", "CRITICAL"),
    (r"\brisk\s+score\s*(is|:)?\s*\d", "Contains risk score", "CRITICAL"),
    (
        r"\b(rating|score|rank)\s*[:\s]*\d+\s*(out\s+of|\/)\s*\d+",
        "Contains numerical rating",
        "CRITICAL",
    ),
]


# =============================================================================
# REQUIRED ELEMENTS
# =============================================================================

MANDATORY_DISCLAIMER = (
    "This is a description of what your charts are showing. "
    "The interpretation and any decision is entirely yours."
)

# Alternative acceptable disclaimers (partial matches)
ACCEPTABLE_DISCLAIMER_PATTERNS = [
    r"interpretation.*decision.*yours",
    r"decision.*entirely\s+yours",
    r"interpretation.*yours",
]


# =============================================================================
# VALIDATION RESULT
# =============================================================================


@dataclass
class ValidationResult:
    """Result of validating an AI response."""

    is_valid: bool
    status: ValidationStatus
    violations: list[str]
    remediated_text: Optional[str] = None

    def __str__(self) -> str:
        if self.is_valid:
            return "ValidationResult(VALID)"
        return f"ValidationResult(INVALID, violations={self.violations})"


# =============================================================================
# VALIDATOR CLASS
# =============================================================================


class AIResponseValidator:
    """
    Validates AI responses for constitutional compliance.

    Per Gold Standard Specification Section 14.4:
    - All AI output must be DESCRIPTIVE, never PRESCRIPTIVE
    - No recommendations, predictions, or aggregations
    - Mandatory disclaimer must be present

    This validator implements:
    1. Regex pattern matching against prohibited phrases
    2. Mandatory disclaimer verification
    3. Optional remediation (phrase replacement)
    4. Logging of all violations for audit
    """

    def __init__(
        self,
        strict_mode: bool = True,
        allow_remediation: bool = True,
        log_violations: bool = True,
    ):
        """
        Initialize the validator.

        Args:
            strict_mode: If True, CRITICAL violations cannot be remediated
            allow_remediation: If True, attempt to fix WARNING violations
            log_violations: If True, log all violations for audit
        """
        self.strict_mode = strict_mode
        self.allow_remediation = allow_remediation
        self.log_violations = log_violations

        # Compile patterns for performance
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), reason, severity)
            for pattern, reason, severity in PROHIBITED_PATTERNS
        ]

        self._disclaimer_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in ACCEPTABLE_DISCLAIMER_PATTERNS
        ]

    def validate(self, response: str) -> ValidationResult:
        """
        Validate an AI response for constitutional compliance.

        Args:
            response: The AI-generated text to validate

        Returns:
            ValidationResult with validation status and any violations
        """
        violations: list[str] = []
        critical_violations: list[str] = []
        warning_violations: list[str] = []

        # Check for prohibited patterns
        for compiled_pattern, reason, severity in self._compiled_patterns:
            if compiled_pattern.search(response):
                violations.append(reason)
                if severity == "CRITICAL":
                    critical_violations.append(reason)
                else:
                    warning_violations.append(reason)

                if self.log_violations:
                    logger.warning(
                        f"Constitutional violation detected: {reason} (severity={severity})"
                    )

        # Check for mandatory disclaimer
        has_disclaimer = self._check_disclaimer(response)
        if not has_disclaimer:
            violations.append("Missing mandatory disclaimer")
            critical_violations.append("Missing mandatory disclaimer")
            if self.log_violations:
                logger.warning("Constitutional violation: Missing mandatory disclaimer")

        # Determine result
        if not violations:
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.VALID,
                violations=[],
            )

        # If strict mode, reject on any critical violation
        if self.strict_mode and critical_violations:
            return ValidationResult(
                is_valid=False,
                status=ValidationStatus.INVALID,
                violations=violations,
            )

        # Attempt remediation if allowed
        if self.allow_remediation and not critical_violations:
            remediated = self._remediate(response, warning_violations)
            return ValidationResult(
                is_valid=True,
                status=ValidationStatus.REMEDIATED,
                violations=warning_violations,
                remediated_text=remediated,
            )

        return ValidationResult(
            is_valid=False,
            status=ValidationStatus.INVALID,
            violations=violations,
        )

    def validate_or_raise(self, response: str) -> str:
        """
        Validate response and raise exception if invalid.

        Args:
            response: The AI-generated text to validate

        Returns:
            The validated (possibly remediated) response

        Raises:
            ConstitutionalViolationError: If response is non-compliant
        """
        result = self.validate(response)

        if result.is_valid:
            return result.remediated_text or response

        raise ConstitutionalViolationError(
            message="AI response violates constitutional principles",
            details={
                "violations": result.violations,
                "response_preview": response[:200] + "..." if len(response) > 200 else response,
            },
        )

    def _check_disclaimer(self, response: str) -> bool:
        """Check if response contains an acceptable disclaimer."""
        # Check for exact match first
        if MANDATORY_DISCLAIMER in response:
            return True

        # Check for acceptable variations
        for pattern in self._disclaimer_patterns:
            if pattern.search(response):
                return True

        return False

    def _remediate(self, response: str, violations: list[str]) -> str:
        """
        Attempt to remediate a response by replacing problematic phrases.

        Only called for WARNING-level violations.
        """
        result = response

        # Replace known problematic phrases with neutral alternatives
        replacements = [
            (r"\bon\s+balance\b", "considering all signals"),
            (r"\boverall\b", "across the charts"),
        ]

        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # Ensure disclaimer is present
        if not self._check_disclaimer(result):
            result = result.rstrip() + "\n\n" + MANDATORY_DISCLAIMER

        return result


# =============================================================================
# VALIDATED GENERATION WITH RETRY
# =============================================================================


class ValidatedResponseGenerator:
    """
    Generates AI responses with validation and retry logic.

    This class wraps the Claude client and validator to provide
    automatic retry on constitutional violations.
    """

    def __init__(
        self,
        claude_client,
        validator: Optional[AIResponseValidator] = None,
        max_retries: int = 3,
    ):
        """
        Initialize the validated generator.

        Args:
            claude_client: The ClaudeClient instance
            validator: The validator to use (creates default if None)
            max_retries: Maximum retry attempts on validation failure
        """
        self.claude = claude_client
        self.validator = validator or AIResponseValidator()
        self.max_retries = max_retries

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate a validated response with retry logic.

        Args:
            system_prompt: System instructions for Claude
            user_prompt: User message/request
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            Validated response text

        Raises:
            ConstitutionalViolationError: If all retries fail
        """
        last_violations: list[str] = []

        for attempt in range(self.max_retries):
            # Generate response
            response = await self.claude.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Validate
            result = self.validator.validate(response)

            if result.is_valid:
                if result.status == ValidationStatus.REMEDIATED:
                    logger.info(
                        f"Response remediated on attempt {attempt + 1}: {result.violations}"
                    )
                    return result.remediated_text
                return response

            # Log failure and prepare stricter prompt for retry
            last_violations = result.violations
            logger.warning(
                f"Validation failed on attempt {attempt + 1}/{self.max_retries}: "
                f"{result.violations}"
            )

            # Add stricter constraints for retry
            system_prompt = self._add_stricter_constraints(system_prompt, result.violations)

            # Reduce temperature for more focused output
            temperature = max(0.1, temperature - 0.1)

        # All retries failed - raise exception
        raise ConstitutionalViolationError(
            message=f"AI response failed validation after {self.max_retries} attempts",
            details={
                "violations": last_violations,
                "attempts": self.max_retries,
            },
        )

    def _add_stricter_constraints(
        self,
        system_prompt: str,
        violations: list[str],
    ) -> str:
        """Add additional constraints based on specific violations."""
        additions = [
            "",
            "CRITICAL REMINDER - Previous response was REJECTED for these violations:",
        ]

        for v in violations:
            additions.append(f"  - {v}")

        additions.extend(
            [
                "",
                "You MUST avoid these specific issues in your next response.",
                "Be EXTREMELY careful to use only DESCRIPTIVE language.",
                "Do NOT use any form of recommendation, suggestion, or advice.",
            ]
        )

        return system_prompt + "\n".join(additions)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def validate_ai_response(response: str) -> ValidationResult:
    """
    Convenience function to validate an AI response.

    Args:
        response: The AI-generated text

    Returns:
        ValidationResult with is_valid, status, violations, and optional remediated_text
    """
    validator = AIResponseValidator()
    return validator.validate(response)


def ensure_disclaimer(response: str) -> str:
    """
    Ensure response has the mandatory disclaimer.

    Args:
        response: The AI-generated text

    Returns:
        Response with disclaimer appended if missing
    """
    validator = AIResponseValidator()
    if validator._check_disclaimer(response):
        return response

    return response.rstrip() + "\n\n" + MANDATORY_DISCLAIMER
