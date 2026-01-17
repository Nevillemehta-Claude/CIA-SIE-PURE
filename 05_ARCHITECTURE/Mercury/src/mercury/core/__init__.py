"""
Mercury Core Module
===================

Configuration, exceptions, logging, metrics, resilience, and health.
"""

# Configuration
from mercury.core.config import get_settings, Settings

# Original exceptions (for backwards compatibility)
from mercury.core.exceptions import (
    MercuryError as BaseMercuryError,
    KiteAPIError as BaseKiteAPIError,
    KiteAuthError,
    SymbolNotFoundError,
    AIEngineError,
    NetworkError as BaseNetworkError,
)

# Enhanced error classification
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

# Security
from mercury.core.security import (
    mask_sensitive_string,
    sanitize_text,
    sanitize_dict,
    sanitize_exception,
    is_sensitive_key,
)

# Logging
from mercury.core.logging import (
    get_logger,
    setup_logging,
    get_correlation_id,
    set_correlation_id,
    new_correlation_id,
    MercuryLogger,
)

# Validation
from mercury.core.validation import (
    validate_config,
    validate_and_report,
    require_valid_config,
    ValidationResult,
)

# Resilience
from mercury.core.resilience import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    CircuitOpenError as CircuitOpenException,
    get_circuit_breaker,
    get_all_circuit_health,
    kite_circuit,
    ai_circuit,
    retry_async,
    RetryConfig,
    GracefulDegradation,
    DegradationLevel,
    degradation,
)

# Health
from mercury.core.health import (
    HealthStatus,
    ComponentHealth,
    SystemHealth,
    get_system_health,
    run_startup_checks,
)

# Metrics
from mercury.core.metrics import (
    Counter,
    Gauge,
    Histogram,
    MetricsRegistry,
    get_registry,
    get_metrics,
    inc_queries,
    observe_query_duration,
    time_query,
)

# Feature Flags
from mercury.core.features import (
    Feature,
    FeatureState,
    FeatureManager,
    get_features,
    is_enabled,
)

# Startup & Initialization
from mercury.core.startup import (
    ServiceStatus,
    APIStatus,
    LaunchReadiness,
    verify_kite_api,
    verify_anthropic_api,
    perform_launch_readiness_check,
    initialize_system,
    sync_initialize_system,
)

__all__ = [
    # Configuration
    "get_settings",
    "Settings",
    
    # Error Classification
    "MercuryError",
    "ErrorSeverity",
    "ErrorCategory",
    "ErrorContext",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "RateLimitError",
    "NetworkError",
    "TimeoutError",
    "ExternalAPIError",
    "KiteAPIError",
    "AIProviderError",
    "ConfigurationError",
    "ResourceExhaustedError",
    "DataIntegrityError",
    "ConversationError",
    "CircuitOpenError",
    "classify_exception",
    
    # Legacy exceptions
    "KiteAuthError",
    "SymbolNotFoundError",
    "AIEngineError",
    
    # Security
    "mask_sensitive_string",
    "sanitize_text",
    "sanitize_dict",
    "sanitize_exception",
    "is_sensitive_key",
    
    # Logging
    "get_logger",
    "setup_logging",
    "get_correlation_id",
    "set_correlation_id",
    "new_correlation_id",
    "MercuryLogger",
    
    # Validation
    "validate_config",
    "validate_and_report",
    "require_valid_config",
    "ValidationResult",
    
    # Resilience
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitState",
    "get_circuit_breaker",
    "get_all_circuit_health",
    "kite_circuit",
    "ai_circuit",
    "retry_async",
    "RetryConfig",
    "GracefulDegradation",
    "DegradationLevel",
    "degradation",
    
    # Health
    "HealthStatus",
    "ComponentHealth",
    "SystemHealth",
    "get_system_health",
    "run_startup_checks",
    
    # Metrics
    "Counter",
    "Gauge",
    "Histogram",
    "MetricsRegistry",
    "get_registry",
    "get_metrics",
    "inc_queries",
    "observe_query_duration",
    "time_query",
    
    # Feature Flags
    "Feature",
    "FeatureState",
    "FeatureManager",
    "get_features",
    "is_enabled",
]
