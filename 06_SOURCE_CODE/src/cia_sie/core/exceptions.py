"""
CIA-SIE Custom Exceptions
=========================

Defines application-specific exceptions for error handling.
All exceptions are explicit and descriptive.
"""

from typing import Optional


class CIASIEError(Exception):
    """Base exception for all CIA-SIE errors."""

    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


# =============================================================================
# DOMAIN EXCEPTIONS
# =============================================================================


class InstrumentNotFoundError(CIASIEError):
    """Raised when an instrument cannot be found."""

    pass


class SiloNotFoundError(CIASIEError):
    """Raised when a silo cannot be found."""

    pass


class ChartNotFoundError(CIASIEError):
    """Raised when a chart cannot be found."""

    pass


class SignalNotFoundError(CIASIEError):
    """Raised when a signal cannot be found."""

    pass


class BasketNotFoundError(CIASIEError):
    """Raised when an analytical basket cannot be found."""

    pass


# =============================================================================
# VALIDATION EXCEPTIONS
# =============================================================================


class ValidationError(CIASIEError):
    """Raised when validation fails."""

    pass


class DuplicateError(CIASIEError):
    """Raised when attempting to create a duplicate entity."""

    pass


class InvalidWebhookPayloadError(CIASIEError):
    """Raised when webhook payload validation fails."""

    pass


class WebhookNotRegisteredError(CIASIEError):
    """Raised when webhook_id is not found in chart registry."""

    pass


# =============================================================================
# INFRASTRUCTURE EXCEPTIONS
# =============================================================================


class DatabaseError(CIASIEError):
    """Raised when database operations fail."""

    pass


class AIProviderError(CIASIEError):
    """Raised when AI provider (Claude) operations fail."""

    pass


class PlatformAdapterError(CIASIEError):
    """Raised when platform adapter operations fail."""

    pass


# =============================================================================
# CONSTITUTIONAL VIOLATION EXCEPTIONS
# =============================================================================


class ConstitutionalViolationError(CIASIEError):
    """
    Raised when code attempts to violate constitutional principles.

    This exception should NEVER occur in production if the code is
    properly implemented. Its presence indicates a severe design flaw.

    Per Section 0A: No loopholes, no exceptions.
    """

    pass


class AggregationAttemptError(ConstitutionalViolationError):
    """
    Raised when code attempts to aggregate signals.

    Per Section 0B.5 P-01: No system component shall reduce
    multiple chart outputs to a single score.
    """

    pass


class RecommendationAttemptError(ConstitutionalViolationError):
    """
    Raised when code attempts to generate recommendations.

    Per Section 0B.5 P-04: No system component shall recommend
    actions based on analytical outputs.
    """

    pass


class ContradictionResolutionAttemptError(ConstitutionalViolationError):
    """
    Raised when code attempts to resolve contradictions.

    Per Section 0B.5 P-03: No system component shall resolve
    contradictions between signals.
    """

    pass
