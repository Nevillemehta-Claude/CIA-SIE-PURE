"""
Tests for CIA-SIE Custom Exceptions
===================================

Validates exception hierarchy and behavior.
"""

import pytest
from cia_sie.core.exceptions import (
    CIASIEError,
    InstrumentNotFoundError,
    SiloNotFoundError,
    ChartNotFoundError,
    SignalNotFoundError,
    BasketNotFoundError,
    ValidationError,
    DuplicateError,
    InvalidWebhookPayloadError,
    WebhookNotRegisteredError,
    DatabaseError,
    AIProviderError,
    PlatformAdapterError,
    ConstitutionalViolationError,
    AggregationAttemptError,
    RecommendationAttemptError,
    ContradictionResolutionAttemptError,
)


class TestBaseException:
    """Tests for CIASIEError base exception."""

    def test_base_exception_with_message(self):
        """Test exception with message only."""
        error = CIASIEError("Test error message")
        assert error.message == "Test error message"
        assert error.details == {}
        assert str(error) == "Test error message"

    def test_base_exception_with_details(self):
        """Test exception with message and details."""
        details = {"key": "value", "code": 123}
        error = CIASIEError("Test error", details=details)
        assert error.message == "Test error"
        assert error.details == details
        assert error.details["key"] == "value"
        assert error.details["code"] == 123


class TestDomainExceptions:
    """Tests for domain-specific exceptions."""

    def test_instrument_not_found_error(self):
        """Test InstrumentNotFoundError."""
        error = InstrumentNotFoundError(
            "Instrument not found",
            {"instrument_id": "123"}
        )
        assert isinstance(error, CIASIEError)
        assert error.details["instrument_id"] == "123"

    def test_silo_not_found_error(self):
        """Test SiloNotFoundError."""
        error = SiloNotFoundError("Silo not found")
        assert isinstance(error, CIASIEError)

    def test_chart_not_found_error(self):
        """Test ChartNotFoundError."""
        error = ChartNotFoundError("Chart not found")
        assert isinstance(error, CIASIEError)

    def test_signal_not_found_error(self):
        """Test SignalNotFoundError."""
        error = SignalNotFoundError("Signal not found")
        assert isinstance(error, CIASIEError)

    def test_basket_not_found_error(self):
        """Test BasketNotFoundError."""
        error = BasketNotFoundError("Basket not found")
        assert isinstance(error, CIASIEError)


class TestValidationExceptions:
    """Tests for validation exceptions."""

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError(
            "Validation failed",
            {"field": "symbol", "reason": "too short"}
        )
        assert isinstance(error, CIASIEError)
        assert error.details["field"] == "symbol"

    def test_duplicate_error(self):
        """Test DuplicateError."""
        error = DuplicateError("Entity already exists")
        assert isinstance(error, CIASIEError)

    def test_invalid_webhook_payload_error(self):
        """Test InvalidWebhookPayloadError."""
        error = InvalidWebhookPayloadError(
            "Invalid payload",
            {"missing_field": "direction"}
        )
        assert isinstance(error, CIASIEError)

    def test_webhook_not_registered_error(self):
        """Test WebhookNotRegisteredError."""
        error = WebhookNotRegisteredError(
            "Webhook not registered",
            {"webhook_id": "UNKNOWN"}
        )
        assert isinstance(error, CIASIEError)


class TestInfrastructureExceptions:
    """Tests for infrastructure exceptions."""

    def test_database_error(self):
        """Test DatabaseError."""
        error = DatabaseError("Database connection failed")
        assert isinstance(error, CIASIEError)

    def test_ai_provider_error(self):
        """Test AIProviderError."""
        error = AIProviderError(
            "Claude API error",
            {"status_code": 500}
        )
        assert isinstance(error, CIASIEError)

    def test_platform_adapter_error(self):
        """Test PlatformAdapterError."""
        error = PlatformAdapterError("Platform connection failed")
        assert isinstance(error, CIASIEError)


class TestConstitutionalViolationExceptions:
    """
    Tests for constitutional violation exceptions.

    CRITICAL: These exceptions should NEVER occur in production.
    Their presence indicates severe design flaws.
    """

    def test_constitutional_violation_error(self):
        """Test ConstitutionalViolationError."""
        error = ConstitutionalViolationError(
            "Constitutional violation detected",
            {"violation_type": "aggregation"}
        )
        assert isinstance(error, CIASIEError)

    def test_aggregation_attempt_error(self):
        """
        Test AggregationAttemptError.

        Per Section 0B.5 P-01: No aggregation allowed.
        """
        error = AggregationAttemptError(
            "Attempted to aggregate signals",
            {"attempted_operation": "compute_net_direction"}
        )
        assert isinstance(error, ConstitutionalViolationError)
        assert isinstance(error, CIASIEError)

    def test_recommendation_attempt_error(self):
        """
        Test RecommendationAttemptError.

        Per Section 0B.5 P-04: No recommendations allowed.
        """
        error = RecommendationAttemptError(
            "Attempted to generate recommendation"
        )
        assert isinstance(error, ConstitutionalViolationError)

    def test_contradiction_resolution_attempt_error(self):
        """
        Test ContradictionResolutionAttemptError.

        Per Section 0B.5 P-03: No contradiction resolution allowed.
        """
        error = ContradictionResolutionAttemptError(
            "Attempted to resolve contradiction",
            {"chart_a": "01A", "chart_b": "02"}
        )
        assert isinstance(error, ConstitutionalViolationError)


class TestExceptionHierarchy:
    """Tests for exception inheritance hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """All custom exceptions should inherit from CIASIEError."""
        exception_classes = [
            InstrumentNotFoundError,
            SiloNotFoundError,
            ChartNotFoundError,
            SignalNotFoundError,
            BasketNotFoundError,
            ValidationError,
            DuplicateError,
            InvalidWebhookPayloadError,
            WebhookNotRegisteredError,
            DatabaseError,
            AIProviderError,
            PlatformAdapterError,
            ConstitutionalViolationError,
            AggregationAttemptError,
            RecommendationAttemptError,
            ContradictionResolutionAttemptError,
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, CIASIEError)
            assert issubclass(exc_class, Exception)

    def test_constitutional_exceptions_inherit_correctly(self):
        """Constitutional violations should inherit from ConstitutionalViolationError."""
        assert issubclass(AggregationAttemptError, ConstitutionalViolationError)
        assert issubclass(RecommendationAttemptError, ConstitutionalViolationError)
        assert issubclass(ContradictionResolutionAttemptError, ConstitutionalViolationError)
