"""
Tests for CIA-SIE Kite Platform Adapter
=======================================

Validates Kite (Zerodha) platform adapter implementation.

GOVERNED BY: Section 8 (Platform-Agnostic Integration)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta

from cia_sie.platforms.kite import KiteAdapter
from cia_sie.platforms.base import (
    ConnectionStatus,
    PlatformCredentials,
    WatchlistInfo,
    PlatformInstrument,
)


class TestKiteAdapterProperties:
    """Tests for KiteAdapter property values."""

    @pytest.fixture
    def adapter(self):
        """Create KiteAdapter instance."""
        return KiteAdapter(api_key="test_api_key")

    def test_platform_name(self, adapter):
        """Test platform name is Kite."""
        assert adapter.platform_name == "Kite"

    def test_platform_display_name(self, adapter):
        """Test display name is Zerodha Kite."""
        assert adapter.platform_display_name == "Zerodha Kite"

    def test_supports_watchlist_import(self, adapter):
        """Test watchlist import is supported."""
        assert adapter.supports_watchlist_import is True

    def test_supports_real_time_signals(self, adapter):
        """Test real-time signals is NOT supported (Kite provides market data, not signals)."""
        assert adapter.supports_real_time_signals is False

    def test_requires_authentication(self, adapter):
        """Test authentication is required."""
        assert adapter.requires_authentication is True

    def test_initial_status(self, adapter):
        """Test initial status is disconnected."""
        assert adapter.status == ConnectionStatus.DISCONNECTED
        assert adapter.is_connected is False


class TestKiteAdapterLoginUrl:
    """Tests for KiteAdapter OAuth login URL."""

    def test_get_login_url_with_api_key(self):
        """Test login URL generation with API key."""
        adapter = KiteAdapter(api_key="test_api_key")
        login_url = adapter.get_login_url()

        assert "kite.zerodha.com" in login_url
        assert "api_key=test_api_key" in login_url

    def test_get_login_url_without_api_key(self):
        """Test login URL raises without API key."""
        adapter = KiteAdapter()

        with pytest.raises(ValueError, match="API key not configured"):
            adapter.get_login_url()


class TestKiteAdapterConnection:
    """Tests for KiteAdapter connection management."""

    @pytest.fixture
    def adapter(self):
        """Create KiteAdapter instance."""
        return KiteAdapter(api_key="test_api_key")

    @pytest.mark.asyncio
    async def test_connect_without_access_token(self, adapter):
        """Test connection fails without access token."""
        creds = PlatformCredentials(
            platform="Kite",
            api_key="just_api_key",
        )

        result = await adapter.connect(creds)

        assert result is False
        assert adapter.status == ConnectionStatus.ERROR

    @pytest.mark.asyncio
    async def test_connect_without_api_key(self):
        """Test connection fails without API key."""
        adapter = KiteAdapter()  # No API key
        creds = PlatformCredentials(
            platform="Kite",
            access_token="token_but_no_key",
        )

        result = await adapter.connect(creds)

        assert result is False
        assert adapter.status == ConnectionStatus.ERROR

    @pytest.mark.asyncio
    async def test_disconnect(self, adapter):
        """Test disconnection clears state."""
        # Set up as if connected
        adapter._access_token = "test_token"
        adapter._status = ConnectionStatus.CONNECTED

        await adapter.disconnect()

        assert adapter.status == ConnectionStatus.DISCONNECTED
        assert adapter._access_token is None


class TestKiteAdapterHealthCheck:
    """Tests for KiteAdapter health check."""

    @pytest.mark.asyncio
    async def test_health_check_when_no_client(self):
        """Test health check returns False when no client."""
        adapter = KiteAdapter(api_key="test_api_key")
        # _client is None by default
        result = await adapter.health_check()
        assert result is False


class TestKiteAdapterWatchlists:
    """Tests for KiteAdapter watchlist operations."""

    @pytest.mark.asyncio
    async def test_get_watchlists_when_disconnected(self):
        """Test get_watchlists raises when disconnected."""
        adapter = KiteAdapter(api_key="test_api_key")
        with pytest.raises(ConnectionError, match="Not connected"):
            await adapter.get_watchlists()


class TestKiteAdapterInstruments:
    """Tests for KiteAdapter instrument operations."""

    @pytest.mark.asyncio
    async def test_get_instruments_when_disconnected(self):
        """Test get_instruments raises when disconnected."""
        adapter = KiteAdapter(api_key="test_api_key")
        with pytest.raises(ConnectionError, match="Not connected"):
            await adapter.get_instruments("watchlist1")


class TestKiteAdapterConstitutionalCompliance:
    """Constitutional compliance tests for KiteAdapter."""

    @pytest.mark.constitutional
    def test_adapter_has_no_scoring_methods(self):
        """CRITICAL: Adapter must not have scoring methods."""
        prohibited_methods = [
            'score', 'weight', 'rank', 'prioritize',
            'aggregate', 'recommend', 'advise', 'confidence',
        ]

        for method in prohibited_methods:
            assert not hasattr(KiteAdapter, method), \
                f"CONSTITUTIONAL VIOLATION: KiteAdapter has {method}"

    @pytest.mark.constitutional
    def test_instruments_have_no_weights(self):
        """CRITICAL: Retrieved instruments must have no weights."""
        # Verify the instrument class doesn't add weights
        from cia_sie.platforms.base import PlatformInstrument

        inst = PlatformInstrument(
            symbol="TEST",
            display_name="Test",
            exchange="NSE",
            instrument_type="EQUITY",
            platform="Kite",
            platform_symbol="NSE:TEST",
        )

        assert not hasattr(inst, 'weight')
        assert not hasattr(inst, 'score')
        assert not hasattr(inst, 'priority')

    @pytest.mark.constitutional
    def test_no_trading_signal_generation(self):
        """CRITICAL: Kite adapter must not generate trading signals."""
        adapter = KiteAdapter(api_key="test")

        # Verify explicitly that real-time signals are not supported
        assert adapter.supports_real_time_signals is False

        # Verify no signal generation methods exist
        prohibited_signal_methods = [
            'generate_signal', 'create_signal', 'emit_signal',
            'get_trading_signal', 'compute_signal',
        ]

        for method in prohibited_signal_methods:
            assert not hasattr(adapter, method), \
                f"CONSTITUTIONAL VIOLATION: KiteAdapter has {method}"
