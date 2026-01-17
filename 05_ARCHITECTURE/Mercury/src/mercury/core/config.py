"""
Mercury Configuration
=====================

Centralized configuration using Pydantic Settings.

CONSTITUTIONAL: MR-001 - Configuration supports data grounding
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Mercury application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Mercury")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)

    # Kite Connect
    kite_api_key: Optional[str] = Field(default=None)
    kite_api_secret: Optional[str] = Field(default=None)
    kite_access_token: Optional[str] = Field(default=None)
    kite_redirect_uri: str = Field(
        default="http://127.0.0.1:8000/callback"
    )

    # Claude/Anthropic
    anthropic_api_key: Optional[str] = Field(default=None)
    anthropic_model: str = Field(default="claude-sonnet-4-20250514")
    max_tokens: int = Field(default=2000)

    # Conversation
    conversation_limit: int = Field(
        default=20, 
        description="Max messages to include in context"
    )

    # Rate Limiting
    kite_rate_limit_per_second: int = Field(default=1)
    claude_rate_limit_per_minute: int = Field(default=60)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
