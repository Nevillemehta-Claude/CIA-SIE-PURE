"""
CIA-SIE Configuration Management
================================

Centralized configuration using Pydantic Settings.
All configuration is explicit - no magic values.

GOVERNED BY: Governing Principle Law 4 (Explicit Precedes Implicit)
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Configuration follows 12-Factor App methodology.
    All values have sensible defaults but can be overridden via environment.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =========================================================================
    # APPLICATION
    # =========================================================================
    app_name: str = Field(default="CIA-SIE")
    app_version: str = Field(default="2.3.0")
    debug: bool = Field(default=False)
    environment: str = Field(
        default="development", description="Environment: development, staging, production"
    )

    # =========================================================================
    # DATABASE
    # =========================================================================
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/cia_sie.db", description="Database connection URL"
    )

    # =========================================================================
    # API SERVER
    # =========================================================================
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)

    # =========================================================================
    # AI PROVIDER (Claude)
    # =========================================================================
    anthropic_api_key: Optional[str] = Field(
        default=None, description="Anthropic API key for Claude"
    )
    anthropic_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Claude model to use for narrative generation",
    )

    # =========================================================================
    # AI BUDGET & USAGE
    # =========================================================================
    ai_budget_limit: float = Field(default=50.0, description="Monthly budget limit in USD")
    ai_budget_alert_threshold: int = Field(
        default=80, ge=1, le=100, description="Percentage at which to alert user about budget"
    )
    ai_rate_limit_requests_per_minute: int = Field(
        default=20, description="Maximum AI requests per minute"
    )
    ai_rate_limit_tokens_per_minute: int = Field(
        default=100000, description="Maximum tokens per minute"
    )
    ai_fallback_model: str = Field(
        default="claude-3-haiku-20240307", description="Fallback model when budget is low"
    )

    # =========================================================================
    # WEBHOOK
    # =========================================================================
    webhook_secret: Optional[str] = Field(default=None, description="Secret for webhook validation")

    # =========================================================================
    # KITE CONNECT (Zerodha)
    # =========================================================================
    kite_api_key: Optional[str] = Field(default=None, description="Kite Connect API key")
    kite_api_secret: Optional[str] = Field(default=None, description="Kite Connect API secret")
    kite_redirect_uri: str = Field(
        default="http://127.0.0.1:8000/api/v1/platforms/kite/callback",
        description="Kite OAuth redirect URI",
    )

    # =========================================================================
    # FRESHNESS DEFAULTS (can be overridden per silo)
    # =========================================================================
    default_current_threshold_min: int = Field(
        default=2, ge=1, description="Default minutes for CURRENT freshness"
    )
    default_recent_threshold_min: int = Field(
        default=10, ge=1, description="Default minutes for RECENT freshness"
    )
    default_stale_threshold_min: int = Field(
        default=30, ge=1, description="Default minutes for STALE freshness"
    )

    # =========================================================================
    # LOGGING
    # =========================================================================
    log_level: str = Field(default="INFO")
    log_file: Optional[str] = Field(default="logs/cia_sie.log")

    # =========================================================================
    # CORS
    # =========================================================================
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed origins",
    )

    # =========================================================================
    # PATHS
    # =========================================================================
    @property
    def data_dir(self) -> Path:
        """Data directory path."""
        path = Path("data")
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def logs_dir(self) -> Path:
        """Logs directory path."""
        path = Path("logs")
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def cors_origins_list(self) -> list[str]:
        """CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # =========================================================================
    # NOTE: PROHIBITED CONFIGURATION
    # =========================================================================
    # The following configuration options are CONSTITUTIONALLY PROHIBITED
    # per Section 0B of the Gold Standard Specification:
    #
    # - aggregation_weights: Weights enable aggregation (PROHIBITED)
    # - scoring_thresholds: Scoring is prohibited
    # - recommendation_rules: Recommendations are prohibited
    # - signal_priority_config: Priority assignment is prohibited
    # - confidence_calculation_params: Confidence scoring is prohibited
    #
    # These features will NEVER be added to this configuration.
    # =========================================================================


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Using lru_cache ensures settings are only loaded once.
    """
    return Settings()
