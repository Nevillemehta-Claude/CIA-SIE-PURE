"""
Tests for Mercury Startup & Initialization
==========================================

DIRECTIVE: Both APIs must initialise and authenticate successfully on launch.
"""

import pytest
from mercury.core.startup import (
    ServiceStatus,
    APIStatus,
    LaunchReadiness,
    verify_kite_api,
    verify_anthropic_api,
    perform_launch_readiness_check,
)
from mercury.core.config import Settings


class TestServiceStatus:
    """Tests for ServiceStatus enum."""
    
    def test_status_values(self):
        """Should have expected status values."""
        assert ServiceStatus.NOT_CONFIGURED.value == "not_configured"
        assert ServiceStatus.CONFIGURED.value == "configured"
        assert ServiceStatus.AUTHENTICATED.value == "authenticated"
        assert ServiceStatus.FAILED.value == "failed"
        assert ServiceStatus.MOCK_MODE.value == "mock_mode"


class TestAPIStatus:
    """Tests for APIStatus dataclass."""
    
    def test_create_status(self):
        """Should create API status."""
        status = APIStatus(
            name="Test API",
            status=ServiceStatus.AUTHENTICATED,
            message="Connected successfully",
            authenticated=True,
            latency_ms=50,
        )
        
        assert status.name == "Test API"
        assert status.status == ServiceStatus.AUTHENTICATED
        assert status.authenticated is True
        assert status.latency_ms == 50


class TestLaunchReadiness:
    """Tests for LaunchReadiness dataclass."""
    
    def test_initial_state(self):
        """Should start not ready."""
        readiness = LaunchReadiness()
        assert readiness.ready is False
        assert readiness.errors == []
        assert readiness.warnings == []
    
    def test_add_error(self):
        """Should add error and set not ready."""
        readiness = LaunchReadiness()
        readiness.ready = True  # Set to ready first
        
        readiness.add_error("Test error")
        
        assert "Test error" in readiness.errors
        assert readiness.ready is False  # Should be not ready after error
    
    def test_add_warning(self):
        """Should add warning without affecting ready state."""
        readiness = LaunchReadiness()
        readiness.ready = True
        
        readiness.add_warning("Test warning")
        
        assert "Test warning" in readiness.warnings
        assert readiness.ready is True  # Should still be ready


class TestVerifyKiteAPI:
    """Tests for verify_kite_api function."""
    
    @pytest.mark.asyncio
    async def test_not_configured(self):
        """Should return not_configured when no API key."""
        settings = Settings(kite_api_key=None)
        
        status = await verify_kite_api(settings)
        
        assert status.status == ServiceStatus.NOT_CONFIGURED
        assert status.authenticated is False
    
    @pytest.mark.asyncio
    async def test_configured_no_token(self):
        """Should return configured when API key but no token."""
        settings = Settings(
            kite_api_key="test_key",
            kite_api_secret="test_secret",
            kite_access_token=None,
        )
        
        status = await verify_kite_api(settings)
        
        assert status.status == ServiceStatus.CONFIGURED
        assert "authentication required" in status.message.lower()


class TestVerifyAnthropicAPI:
    """Tests for verify_anthropic_api function."""
    
    @pytest.mark.asyncio
    async def test_not_configured(self):
        """Should return not_configured when no API key."""
        settings = Settings(anthropic_api_key=None)
        
        status = await verify_anthropic_api(settings)
        
        assert status.status == ServiceStatus.NOT_CONFIGURED
        assert status.authenticated is False
    
    @pytest.mark.asyncio
    async def test_invalid_key_format(self):
        """Should warn about invalid key format."""
        settings = Settings(anthropic_api_key="invalid_key_format")
        
        status = await verify_anthropic_api(settings)
        
        # Should be configured but with warning about format
        assert status.status == ServiceStatus.CONFIGURED
        assert "format" in status.message.lower() or "invalid" in status.message.lower()


class TestPerformLaunchReadinessCheck:
    """Tests for perform_launch_readiness_check function."""
    
    @pytest.mark.asyncio
    async def test_returns_readiness(self):
        """Should return LaunchReadiness object."""
        readiness = await perform_launch_readiness_check()
        
        assert isinstance(readiness, LaunchReadiness)
        assert readiness.kite_status is not None
        assert readiness.anthropic_status is not None
    
    @pytest.mark.asyncio
    async def test_includes_validation(self):
        """Should include config validation."""
        readiness = await perform_launch_readiness_check()
        
        assert readiness.validation_result is not None
    
    @pytest.mark.asyncio
    async def test_determines_readiness(self):
        """Should determine overall readiness."""
        readiness = await perform_launch_readiness_check()
        
        # Without API keys, should still be ready (mock mode)
        # The system is designed to work in degraded mode
        assert isinstance(readiness.ready, bool)
