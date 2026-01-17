"""
Mercury Error Classification
============================

Comprehensive error taxonomy with severity levels.

MISSION-CRITICAL STANDARD: Error Handling
- Clear error classification
- Severity levels for alerting
- Structured error information
- HTTP status code mapping
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class ErrorSeverity(Enum):
    """
    Error severity levels for alerting and response.
    
    LOW: Log only, no alerts
    MEDIUM: Log + metrics, on-call notification if repeated
    HIGH: Immediate on-call notification
    CRITICAL: Page everyone, potential data loss
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categories of errors for classification."""
    VALIDATION = "validation"        # Input validation failures
    AUTHENTICATION = "authentication"  # Auth failures
    AUTHORIZATION = "authorization"   # Permission failures
    RATE_LIMIT = "rate_limit"        # Rate limiting
    NETWORK = "network"              # Network/connectivity issues
    EXTERNAL_API = "external_api"    # External service failures
    INTERNAL = "internal"            # Internal logic errors
    CONFIGURATION = "configuration"  # Config errors
    RESOURCE = "resource"            # Resource exhaustion
    DATA = "data"                    # Data integrity issues
    TIMEOUT = "timeout"              # Operation timeouts
    UNKNOWN = "unknown"              # Unclassified errors


@dataclass
class ErrorContext:
    """Additional context for an error."""
    component: str = ""              # Component where error occurred
    operation: str = ""              # Operation being performed
    correlation_id: Optional[str] = None  # Request correlation ID
    user_context: dict = field(default_factory=dict)  # User-safe context
    internal_context: dict = field(default_factory=dict)  # Internal-only context
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MercuryError(Exception):
    """
    Base exception for all Mercury errors.
    
    Provides structured error information including:
    - Error code for programmatic handling
    - Severity for alerting
    - Category for classification
    - HTTP status code for API responses
    - User-safe message
    - Internal details for debugging
    """
    
    code: str = "MERCURY_ERROR"
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.UNKNOWN
    http_status: int = 500
    
    def __init__(
        self,
        message: str,
        details: Optional[dict] = None,
        cause: Optional[Exception] = None,
        context: Optional[ErrorContext] = None,
    ):
        self.message = message
        self.details = details or {}
        self.cause = cause
        self.context = context or ErrorContext()
        super().__init__(message)
    
    def to_dict(self, include_internal: bool = False) -> dict:
        """
        Convert to dictionary for API responses.
        
        Args:
            include_internal: Include internal details (for debugging only)
        """
        result = {
            "error": {
                "code": self.code,
                "message": self.message,
                "category": self.category.value,
            }
        }
        
        if self.context.correlation_id:
            result["error"]["correlation_id"] = self.context.correlation_id
        
        if self.context.user_context:
            result["error"]["context"] = self.context.user_context
        
        if include_internal:
            result["_internal"] = {
                "severity": self.severity.value,
                "component": self.context.component,
                "operation": self.context.operation,
                "details": self.details,
                "cause": str(self.cause) if self.cause else None,
                "internal_context": self.context.internal_context,
                "timestamp": self.context.timestamp.isoformat(),
            }
        
        return result
    
    def should_alert(self) -> bool:
        """Check if this error should trigger an alert."""
        return self.severity in (ErrorSeverity.HIGH, ErrorSeverity.CRITICAL)
    
    def should_retry(self) -> bool:
        """Check if this error is potentially retryable."""
        return self.category in (
            ErrorCategory.NETWORK,
            ErrorCategory.TIMEOUT,
            ErrorCategory.RATE_LIMIT,
            ErrorCategory.EXTERNAL_API,
        )


# Specific error types

class ValidationError(MercuryError):
    """Input validation failed."""
    code = "VALIDATION_ERROR"
    severity = ErrorSeverity.LOW
    category = ErrorCategory.VALIDATION
    http_status = 400


class AuthenticationError(MercuryError):
    """Authentication failed."""
    code = "AUTHENTICATION_ERROR"
    severity = ErrorSeverity.MEDIUM
    category = ErrorCategory.AUTHENTICATION
    http_status = 401


class AuthorizationError(MercuryError):
    """Authorization/permission denied."""
    code = "AUTHORIZATION_ERROR"
    severity = ErrorSeverity.MEDIUM
    category = ErrorCategory.AUTHORIZATION
    http_status = 403


class NotFoundError(MercuryError):
    """Resource not found."""
    code = "NOT_FOUND"
    severity = ErrorSeverity.LOW
    category = ErrorCategory.VALIDATION
    http_status = 404


class RateLimitError(MercuryError):
    """Rate limit exceeded."""
    code = "RATE_LIMIT_EXCEEDED"
    severity = ErrorSeverity.LOW
    category = ErrorCategory.RATE_LIMIT
    http_status = 429
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after_seconds: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.retry_after_seconds = retry_after_seconds


class NetworkError(MercuryError):
    """Network connectivity issue."""
    code = "NETWORK_ERROR"
    severity = ErrorSeverity.MEDIUM
    category = ErrorCategory.NETWORK
    http_status = 503


class TimeoutError(MercuryError):
    """Operation timed out."""
    code = "TIMEOUT"
    severity = ErrorSeverity.MEDIUM
    category = ErrorCategory.TIMEOUT
    http_status = 504


class ExternalAPIError(MercuryError):
    """External API call failed."""
    code = "EXTERNAL_API_ERROR"
    severity = ErrorSeverity.MEDIUM
    category = ErrorCategory.EXTERNAL_API
    http_status = 502
    
    def __init__(
        self,
        message: str,
        service: str,
        status_code: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.service = service
        self.external_status_code = status_code
        self.details["service"] = service
        if status_code:
            self.details["external_status_code"] = status_code


class KiteAPIError(ExternalAPIError):
    """Kite API specific error."""
    code = "KITE_API_ERROR"
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, service="kite", **kwargs)


class AIProviderError(ExternalAPIError):
    """AI provider (Anthropic) error."""
    code = "AI_PROVIDER_ERROR"
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, service="anthropic", **kwargs)


class ConfigurationError(MercuryError):
    """Configuration is invalid."""
    code = "CONFIGURATION_ERROR"
    severity = ErrorSeverity.HIGH
    category = ErrorCategory.CONFIGURATION
    http_status = 500


class ResourceExhaustedError(MercuryError):
    """Resource limit exceeded (memory, tokens, etc)."""
    code = "RESOURCE_EXHAUSTED"
    severity = ErrorSeverity.HIGH
    category = ErrorCategory.RESOURCE
    http_status = 503


class DataIntegrityError(MercuryError):
    """Data integrity violation."""
    code = "DATA_INTEGRITY_ERROR"
    severity = ErrorSeverity.CRITICAL
    category = ErrorCategory.DATA
    http_status = 500


class ConversationError(MercuryError):
    """Conversation processing error."""
    code = "CONVERSATION_ERROR"
    severity = ErrorSeverity.LOW
    category = ErrorCategory.INTERNAL
    http_status = 500


class CircuitOpenError(MercuryError):
    """Circuit breaker is open, request rejected."""
    code = "CIRCUIT_OPEN"
    severity = ErrorSeverity.MEDIUM
    category = ErrorCategory.EXTERNAL_API
    http_status = 503
    
    def __init__(self, service: str, **kwargs):
        message = f"Service '{service}' is temporarily unavailable"
        super().__init__(message, **kwargs)
        self.service = service
        self.details["service"] = service


# Error mapping for external exceptions

def classify_exception(exc: Exception) -> MercuryError:
    """
    Classify a generic exception into a Mercury error.
    
    Args:
        exc: Exception to classify
        
    Returns:
        Appropriate MercuryError subclass
    """
    exc_type = type(exc).__name__
    message = str(exc)
    
    # Network-related
    if "timeout" in message.lower() or "timed out" in message.lower():
        return TimeoutError(message, cause=exc)
    
    if "connection" in message.lower() or "network" in message.lower():
        return NetworkError(message, cause=exc)
    
    # Rate limiting
    if "rate limit" in message.lower() or "too many" in message.lower():
        return RateLimitError(message, cause=exc)
    
    # Auth
    if "unauthorized" in message.lower() or "authentication" in message.lower():
        return AuthenticationError(message, cause=exc)
    
    if "forbidden" in message.lower() or "permission" in message.lower():
        return AuthorizationError(message, cause=exc)
    
    # Validation
    if "validation" in message.lower() or "invalid" in message.lower():
        return ValidationError(message, cause=exc)
    
    # Default: wrap as internal error
    return MercuryError(
        f"Internal error: {message}",
        cause=exc,
    )
