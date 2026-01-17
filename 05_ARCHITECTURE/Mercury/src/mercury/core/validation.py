"""
Mercury Configuration Validation
=================================

Validates configuration at startup to fail fast on misconfigurations.

MISSION-CRITICAL STANDARD: Configuration Management
- Validate all configuration at startup
- Fail fast on invalid configuration
- Provide clear error messages
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from mercury.core.config import Settings


class ValidationSeverity(Enum):
    """Severity of validation issues."""
    ERROR = "error"      # Cannot proceed
    WARNING = "warning"  # Can proceed but degraded
    INFO = "info"        # Informational


@dataclass
class ValidationIssue:
    """A configuration validation issue."""
    field: str
    message: str
    severity: ValidationSeverity
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of configuration validation."""
    is_valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    
    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]
    
    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]
    
    def add_error(self, field: str, message: str, suggestion: str = None) -> None:
        self.issues.append(ValidationIssue(
            field=field,
            message=message,
            severity=ValidationSeverity.ERROR,
            suggestion=suggestion,
        ))
        self.is_valid = False
    
    def add_warning(self, field: str, message: str, suggestion: str = None) -> None:
        self.issues.append(ValidationIssue(
            field=field,
            message=message,
            severity=ValidationSeverity.WARNING,
            suggestion=suggestion,
        ))
    
    def add_info(self, field: str, message: str) -> None:
        self.issues.append(ValidationIssue(
            field=field,
            message=message,
            severity=ValidationSeverity.INFO,
        ))
    
    def format_report(self) -> str:
        """Format validation result as readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("CONFIGURATION VALIDATION REPORT")
        lines.append("=" * 60)
        
        if self.is_valid:
            lines.append("✅ Configuration is VALID")
        else:
            lines.append("❌ Configuration is INVALID")
        
        lines.append("")
        
        if self.errors:
            lines.append("ERRORS (must fix):")
            for issue in self.errors:
                lines.append(f"  ❌ {issue.field}: {issue.message}")
                if issue.suggestion:
                    lines.append(f"     → {issue.suggestion}")
        
        if self.warnings:
            lines.append("")
            lines.append("WARNINGS (should fix):")
            for issue in self.warnings:
                lines.append(f"  ⚠️  {issue.field}: {issue.message}")
                if issue.suggestion:
                    lines.append(f"     → {issue.suggestion}")
        
        info_issues = [i for i in self.issues if i.severity == ValidationSeverity.INFO]
        if info_issues:
            lines.append("")
            lines.append("INFO:")
            for issue in info_issues:
                lines.append(f"  ℹ️  {issue.field}: {issue.message}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def validate_config(settings: Optional[Settings] = None) -> ValidationResult:
    """
    Validate Mercury configuration.
    
    Checks:
    - Required settings are present
    - Settings have valid formats
    - API keys appear valid
    - Numeric ranges are sensible
    
    Args:
        settings: Settings to validate (uses default if None)
        
    Returns:
        ValidationResult with any issues found
    """
    if settings is None:
        from mercury.core.config import get_settings
        settings = get_settings()
    
    result = ValidationResult(is_valid=True)
    
    # Check Kite configuration
    if not settings.kite_api_key:
        result.add_warning(
            "KITE_API_KEY",
            "Not configured - Kite API will use mock mode",
            "Set KITE_API_KEY in .env for live market data"
        )
    elif len(settings.kite_api_key) < 8:
        result.add_error(
            "KITE_API_KEY",
            "Appears too short to be valid",
            "Check your Kite API key at developers.kite.trade"
        )
    
    if settings.kite_api_key and not settings.kite_api_secret:
        result.add_warning(
            "KITE_API_SECRET",
            "API key set but secret missing",
            "Set KITE_API_SECRET for full functionality"
        )
    
    if settings.kite_api_key and not settings.kite_access_token:
        result.add_info(
            "KITE_ACCESS_TOKEN",
            "Not set - will need to authenticate before using"
        )
    
    # Check Anthropic configuration
    if not settings.anthropic_api_key:
        result.add_warning(
            "ANTHROPIC_API_KEY",
            "Not configured - AI will use mock mode",
            "Set ANTHROPIC_API_KEY in .env for AI responses"
        )
    elif not settings.anthropic_api_key.startswith("sk-"):
        result.add_warning(
            "ANTHROPIC_API_KEY",
            "Does not start with 'sk-' - may be invalid",
            "Anthropic keys typically start with 'sk-ant-'"
        )
    
    # Check model configuration
    valid_models = [
        "claude-sonnet-4-20250514",
        "claude-opus-4-20250514",
    ]
    if settings.anthropic_model not in valid_models:
        result.add_warning(
            "MERCURY_MODEL",
            f"Model '{settings.anthropic_model}' not in known models",
            f"Known models: {', '.join(valid_models)}"
        )
    
    # Check numeric ranges
    if settings.max_tokens < 100:
        result.add_warning(
            "MERCURY_MAX_TOKENS",
            f"Value {settings.max_tokens} seems too low",
            "Recommended minimum is 500 tokens"
        )
    elif settings.max_tokens > 8000:
        result.add_warning(
            "MERCURY_MAX_TOKENS",
            f"Value {settings.max_tokens} is very high (cost warning)",
            "Consider 2000-4000 for most use cases"
        )
    
    if settings.conversation_limit < 5:
        result.add_warning(
            "MERCURY_CONVERSATION_LIMIT",
            f"Value {settings.conversation_limit} may lose context quickly",
            "Recommended minimum is 10 messages"
        )
    
    return result


def validate_and_report(settings: Optional[Settings] = None) -> bool:
    """
    Validate configuration and print report.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    result = validate_config(settings)
    print(result.format_report())
    return result.is_valid


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    
    def __init__(self, result: ValidationResult):
        self.result = result
        super().__init__(result.format_report())


def require_valid_config(settings: Optional[Settings] = None) -> Settings:
    """
    Validate configuration and raise if invalid.
    
    Use at startup to fail fast on bad configuration.
    
    Args:
        settings: Settings to validate
        
    Returns:
        Validated settings
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    if settings is None:
        from mercury.core.config import get_settings
        settings = get_settings()
    
    result = validate_config(settings)
    
    if not result.is_valid:
        raise ConfigurationError(result)
    
    return settings
