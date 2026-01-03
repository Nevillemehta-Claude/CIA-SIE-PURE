"""
Tests for CIA-SIE Configuration Management
==========================================

Validates configuration loading and constitutional compliance.

GOVERNED BY: Governing Principle Law 4 (Explicit Precedes Implicit)
"""

import pytest
from pathlib import Path
from unittest.mock import patch
import os

from cia_sie.core.config import Settings, get_settings


class TestSettingsDefaults:
    """Tests for default configuration values."""

    def test_default_app_settings(self):
        """Test default application settings."""
        settings = Settings()
        assert settings.app_name == "CIA-SIE"
        assert settings.debug is False
        assert settings.environment == "development"

    def test_default_database_url(self):
        """Test default database URL is SQLite."""
        settings = Settings()
        assert "sqlite" in settings.database_url
        assert "aiosqlite" in settings.database_url

    def test_default_api_settings(self):
        """Test default API server settings."""
        settings = Settings()
        assert settings.api_host == "0.0.0.0"
        assert settings.api_port == 8000

    def test_default_ai_settings(self):
        """Test default AI provider settings."""
        settings = Settings()
        assert settings.anthropic_api_key is None  # Not set by default
        assert "claude" in settings.anthropic_model.lower()

    def test_default_budget_settings(self):
        """Test default budget settings."""
        settings = Settings()
        assert settings.ai_budget_limit == 50.0
        assert settings.ai_budget_alert_threshold == 80
        assert settings.ai_budget_alert_threshold >= 1
        assert settings.ai_budget_alert_threshold <= 100

    def test_default_rate_limit_settings(self):
        """Test default rate limit settings."""
        settings = Settings()
        assert settings.ai_rate_limit_requests_per_minute == 20
        assert settings.ai_rate_limit_tokens_per_minute == 100000

    def test_default_freshness_thresholds(self):
        """Test default freshness thresholds per SDD v4.0."""
        settings = Settings()
        assert settings.default_current_threshold_min == 2
        assert settings.default_recent_threshold_min == 10
        assert settings.default_stale_threshold_min == 30
        # Ensure proper ordering
        assert settings.default_current_threshold_min < settings.default_recent_threshold_min
        assert settings.default_recent_threshold_min < settings.default_stale_threshold_min

    def test_default_logging_settings(self):
        """Test default logging settings."""
        settings = Settings()
        assert settings.log_level == "INFO"
        assert settings.log_file is not None


class TestSettingsEnvironmentOverride:
    """Tests for environment variable overrides."""

    def test_environment_override(self):
        """Test that environment variables override defaults."""
        with patch.dict(os.environ, {"APP_NAME": "TEST-APP", "DEBUG": "true"}):
            settings = Settings()
            assert settings.app_name == "TEST-APP"
            assert settings.debug is True

    def test_database_url_override(self):
        """Test database URL can be overridden."""
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://localhost/test"}):
            settings = Settings()
            assert settings.database_url == "postgresql://localhost/test"

    def test_api_port_override(self):
        """Test API port can be overridden."""
        with patch.dict(os.environ, {"API_PORT": "9000"}):
            settings = Settings()
            assert settings.api_port == 9000


class TestSettingsProperties:
    """Tests for computed properties."""

    def test_data_dir_property(self):
        """Test data_dir property creates directory."""
        settings = Settings()
        data_dir = settings.data_dir
        assert isinstance(data_dir, Path)
        assert data_dir.name == "data"

    def test_logs_dir_property(self):
        """Test logs_dir property creates directory."""
        settings = Settings()
        logs_dir = settings.logs_dir
        assert isinstance(logs_dir, Path)
        assert logs_dir.name == "logs"

    def test_cors_origins_list_property(self):
        """Test CORS origins are parsed into list."""
        settings = Settings()
        origins = settings.cors_origins_list
        assert isinstance(origins, list)
        assert len(origins) >= 1
        # Check that splitting works
        assert all(isinstance(o, str) for o in origins)

    def test_cors_origins_list_with_spaces(self):
        """Test CORS origins handles whitespace."""
        with patch.dict(os.environ, {"CORS_ORIGINS": "http://a.com , http://b.com"}):
            settings = Settings()
            origins = settings.cors_origins_list
            # Should strip whitespace
            assert "http://a.com" in origins
            assert "http://b.com" in origins


class TestSettingsCaching:
    """Tests for settings caching."""

    def test_get_settings_returns_cached(self):
        """Test that get_settings returns cached instance."""
        # Clear cache first
        get_settings.cache_clear()

        settings1 = get_settings()
        settings2 = get_settings()

        # Should be the same instance
        assert settings1 is settings2

    def test_get_settings_cache_info(self):
        """Test that cache is being used."""
        get_settings.cache_clear()

        get_settings()
        get_settings()

        cache_info = get_settings.cache_info()
        assert cache_info.hits >= 1


class TestConstitutionalProhibitions:
    """
    Tests verifying PROHIBITED configuration options.

    CRITICAL: These tests ensure constitutional compliance.
    Per Section 0B of Gold Standard Specification.
    """

    def test_no_aggregation_weights_config(self):
        """
        CRITICAL: No aggregation_weights configuration allowed.

        Per Section 0B: Weights enable aggregation which is PROHIBITED.
        """
        settings = Settings()
        assert not hasattr(settings, "aggregation_weights")
        assert "aggregation_weights" not in Settings.model_fields

    def test_no_scoring_thresholds_config(self):
        """
        CRITICAL: No scoring_thresholds configuration allowed.

        Per Section 0B: Scoring is PROHIBITED.
        """
        settings = Settings()
        assert not hasattr(settings, "scoring_thresholds")
        assert "scoring_thresholds" not in Settings.model_fields

    def test_no_recommendation_rules_config(self):
        """
        CRITICAL: No recommendation_rules configuration allowed.

        Per Section 0B.5 P-04: Recommendations are PROHIBITED.
        """
        settings = Settings()
        assert not hasattr(settings, "recommendation_rules")
        assert "recommendation_rules" not in Settings.model_fields

    def test_no_signal_priority_config(self):
        """
        CRITICAL: No signal_priority_config allowed.

        Per Section 0B.5 P-02: Priority assignment implies weighting.
        """
        settings = Settings()
        assert not hasattr(settings, "signal_priority_config")
        assert "signal_priority_config" not in Settings.model_fields

    def test_no_confidence_calculation_params(self):
        """
        CRITICAL: No confidence_calculation_params allowed.

        Per Section 0B: Confidence scoring is PROHIBITED.
        """
        settings = Settings()
        assert not hasattr(settings, "confidence_calculation_params")
        assert "confidence_calculation_params" not in Settings.model_fields


class TestValidationConstraints:
    """Tests for field validation constraints."""

    def test_budget_alert_threshold_bounds(self):
        """Test budget alert threshold has valid bounds."""
        # Should accept valid values
        with patch.dict(os.environ, {"AI_BUDGET_ALERT_THRESHOLD": "50"}):
            settings = Settings()
            assert settings.ai_budget_alert_threshold == 50

    def test_freshness_threshold_positive(self):
        """Test freshness thresholds must be positive."""
        settings = Settings()
        assert settings.default_current_threshold_min >= 1
        assert settings.default_recent_threshold_min >= 1
        assert settings.default_stale_threshold_min >= 1
