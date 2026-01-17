"""
Tests for Mercury Error Classification
======================================

Tests for error types, classification, and severity.
"""

import pytest
from mercury.core.errors import (
    MercuryError,
    ErrorSeverity,
    ErrorCategory,
    ErrorContext,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    NetworkError,
    TimeoutError,
    ExternalAPIError,
    KiteAPIError,
    AIProviderError,
    ConfigurationError,
    ResourceExhaustedError,
    DataIntegrityError,
    ConversationError,
    CircuitOpenError,
    classify_exception,
)


class TestErrorSeverity:
    """Tests for ErrorSeverity enum."""
    
    def test_severity_values(self):
        """Should have expected severity levels."""
        assert ErrorSeverity.LOW.value == "low"
        assert ErrorSeverity.MEDIUM.value == "medium"
        assert ErrorSeverity.HIGH.value == "high"
        assert ErrorSeverity.CRITICAL.value == "critical"


class TestErrorCategory:
    """Tests for ErrorCategory enum."""
    
    def test_category_values(self):
        """Should have expected categories."""
        assert ErrorCategory.VALIDATION.value == "validation"
        assert ErrorCategory.EXTERNAL_API.value == "external_api"
        assert ErrorCategory.NETWORK.value == "network"


class TestMercuryError:
    """Tests for base MercuryError class."""
    
    def test_create_error(self):
        """Should create error with message."""
        error = MercuryError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.message == "Something went wrong"
    
    def test_error_with_details(self):
        """Should include details."""
        error = MercuryError(
            "Failed to process",
            details={"field": "price", "value": "invalid"}
        )
        assert error.details["field"] == "price"
    
    def test_error_with_cause(self):
        """Should chain exceptions."""
        cause = ValueError("original error")
        error = MercuryError("Wrapped error", cause=cause)
        assert error.cause is cause
    
    def test_error_with_context(self):
        """Should include context."""
        context = ErrorContext(
            component="chat",
            operation="process_query",
            correlation_id="abc123"
        )
        error = MercuryError("Failed", context=context)
        
        assert error.context.component == "chat"
        assert error.context.correlation_id == "abc123"
    
    def test_to_dict_basic(self):
        """Should convert to dictionary."""
        error = MercuryError("Test error")
        result = error.to_dict()
        
        assert "error" in result
        assert result["error"]["message"] == "Test error"
        assert result["error"]["code"] == "MERCURY_ERROR"
    
    def test_to_dict_with_internal(self):
        """Should include internal details when requested."""
        error = MercuryError(
            "Test error",
            details={"debug": "info"},
            context=ErrorContext(component="test")
        )
        result = error.to_dict(include_internal=True)
        
        assert "_internal" in result
        assert result["_internal"]["component"] == "test"
    
    def test_should_alert(self):
        """Should determine alert threshold."""
        low_error = ValidationError("Invalid input")
        assert low_error.should_alert() is False
        
        high_error = ConfigurationError("Config broken")
        assert high_error.should_alert() is True
    
    def test_should_retry(self):
        """Should determine retry eligibility."""
        network_error = NetworkError("Connection failed")
        assert network_error.should_retry() is True
        
        validation_error = ValidationError("Bad input")
        assert validation_error.should_retry() is False


class TestSpecificErrors:
    """Tests for specific error types."""
    
    def test_validation_error(self):
        """Should have correct properties."""
        error = ValidationError("Invalid symbol")
        
        assert error.code == "VALIDATION_ERROR"
        assert error.severity == ErrorSeverity.LOW
        assert error.category == ErrorCategory.VALIDATION
        assert error.http_status == 400
    
    def test_authentication_error(self):
        """Should have correct properties."""
        error = AuthenticationError("Invalid credentials")
        
        assert error.http_status == 401
        assert error.category == ErrorCategory.AUTHENTICATION
    
    def test_authorization_error(self):
        """Should have correct properties."""
        error = AuthorizationError("Permission denied")
        
        assert error.http_status == 403
        assert error.category == ErrorCategory.AUTHORIZATION
    
    def test_not_found_error(self):
        """Should have correct properties."""
        error = NotFoundError("Symbol not found")
        
        assert error.http_status == 404
    
    def test_rate_limit_error(self):
        """Should include retry_after."""
        error = RateLimitError(
            "Rate limit exceeded",
            retry_after_seconds=60
        )
        
        assert error.http_status == 429
        assert error.retry_after_seconds == 60
    
    def test_network_error(self):
        """Should have correct properties."""
        error = NetworkError("Connection failed")
        
        assert error.http_status == 503
        assert error.should_retry() is True
    
    def test_timeout_error(self):
        """Should have correct properties."""
        error = TimeoutError("Request timed out")
        
        assert error.http_status == 504
        assert error.should_retry() is True
    
    def test_external_api_error(self):
        """Should include service info."""
        error = ExternalAPIError(
            "API returned error",
            service="kite",
            status_code=500
        )
        
        assert error.service == "kite"
        assert error.external_status_code == 500
        assert error.details["service"] == "kite"
    
    def test_kite_api_error(self):
        """Should be properly configured."""
        error = KiteAPIError("Kite connection failed")
        
        assert error.code == "KITE_API_ERROR"
        assert error.service == "kite"
    
    def test_ai_provider_error(self):
        """Should be properly configured."""
        error = AIProviderError("Claude API error")
        
        assert error.code == "AI_PROVIDER_ERROR"
        assert error.service == "anthropic"
    
    def test_configuration_error(self):
        """Should be high severity."""
        error = ConfigurationError("Missing API key")
        
        assert error.severity == ErrorSeverity.HIGH
        assert error.should_alert() is True
    
    def test_resource_exhausted_error(self):
        """Should be high severity."""
        error = ResourceExhaustedError("Token limit reached")
        
        assert error.severity == ErrorSeverity.HIGH
    
    def test_data_integrity_error(self):
        """Should be critical severity."""
        error = DataIntegrityError("Data corruption detected")
        
        assert error.severity == ErrorSeverity.CRITICAL
    
    def test_circuit_open_error(self):
        """Should include service name."""
        error = CircuitOpenError(service="kite")
        
        assert "kite" in error.message
        assert error.service == "kite"


class TestClassifyException:
    """Tests for classify_exception function."""
    
    def test_classify_timeout(self):
        """Should classify timeout exceptions."""
        exc = Exception("Connection timed out")
        error = classify_exception(exc)
        
        assert isinstance(error, TimeoutError)
    
    def test_classify_network(self):
        """Should classify network exceptions."""
        exc = Exception("Connection refused")
        error = classify_exception(exc)
        
        assert isinstance(error, NetworkError)
    
    def test_classify_rate_limit(self):
        """Should classify rate limit exceptions."""
        exc = Exception("Rate limit exceeded")
        error = classify_exception(exc)
        
        assert isinstance(error, RateLimitError)
    
    def test_classify_auth(self):
        """Should classify auth exceptions."""
        exc = Exception("Authentication failed: unauthorized")
        error = classify_exception(exc)
        
        assert isinstance(error, AuthenticationError)
    
    def test_classify_validation(self):
        """Should classify validation exceptions."""
        exc = Exception("Validation failed: invalid format")
        error = classify_exception(exc)
        
        assert isinstance(error, ValidationError)
    
    def test_classify_unknown(self):
        """Should wrap unknown exceptions."""
        exc = Exception("Something strange happened")
        error = classify_exception(exc)
        
        assert isinstance(error, MercuryError)
        assert error.cause is exc
