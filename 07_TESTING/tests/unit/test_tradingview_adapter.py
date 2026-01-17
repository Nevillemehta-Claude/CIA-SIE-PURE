"""
Tests for CIA-SIE TradingView Platform Adapter
==============================================

Validates TradingView platform adapter implementation.

GOVERNED BY: Section 8 (Platform-Agnostic Integration)
"""

import pytest
from unittest.mock import Mock, AsyncMock

from cia_sie.platforms.tradingview import TradingViewAdapter
from cia_sie.platforms.base import (
    ConnectionStatus,
    PlatformCredentials,
)


class TestTradingViewAdapterProperties:
    """Tests for TradingViewAdapter property values."""

    @pytest.fixture
    def adapter(self):
        """Create TradingViewAdapter instance."""
        return TradingViewAdapter()

    def test_platform_name(self, adapter):
        """Test platform name is TradingView."""
        assert adapter.platform_name == "TradingView"

    def test_platform_display_name(self, adapter):
        """Test display name is TradingView Charts."""
        assert adapter.platform_display_name == "TradingView Charts"

    def test_supports_watchlist_import(self, adapter):
        """Test watchlist import is NOT supported (no public API)."""
        assert adapter.supports_watchlist_import is False

    def test_supports_real_time_signals(self, adapter):
        """Test real-time signals IS supported (via webhooks)."""
        assert adapter.supports_real_time_signals is True

    def test_requires_authentication(self, adapter):
        """Test authentication is NOT required (webhook-based)."""
        assert adapter.requires_authentication is False

    def test_initial_status_connected(self, adapter):
        """Test initial status is connected (always ready for webhooks)."""
        assert adapter.status == ConnectionStatus.CONNECTED
        assert adapter.is_connected is True


class TestTradingViewAdapterConnection:
    """Tests for TradingViewAdapter connection management."""

    @pytest.fixture
    def adapter(self):
        """Create TradingViewAdapter instance."""
        return TradingViewAdapter()

    @pytest.mark.asyncio
    async def test_connect_always_succeeds(self, adapter):
        """Test connection always succeeds (webhook-based)."""
        creds = PlatformCredentials(platform="TradingView")
        result = await adapter.connect(creds)

        assert result is True
        assert adapter.status == ConnectionStatus.CONNECTED

    @pytest.mark.asyncio
    async def test_disconnect_sets_disconnected(self, adapter):
        """Test disconnect sets status to disconnected."""
        await adapter.disconnect()

        assert adapter.status == ConnectionStatus.DISCONNECTED

    @pytest.mark.asyncio
    async def test_health_check_always_true(self, adapter):
        """Test health check always returns True."""
        result = await adapter.health_check()
        assert result is True


class TestTradingViewAdapterWatchlists:
    """Tests for TradingViewAdapter watchlist operations."""

    @pytest.fixture
    def adapter(self):
        """Create TradingViewAdapter instance."""
        return TradingViewAdapter()

    @pytest.mark.asyncio
    async def test_get_watchlists_not_implemented(self, adapter):
        """Test get_watchlists raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            await adapter.get_watchlists()

    @pytest.mark.asyncio
    async def test_get_instruments_not_implemented(self, adapter):
        """Test get_instruments raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            await adapter.get_instruments("any_watchlist")


class TestTradingViewAdapterWebhookTemplates:
    """Tests for TradingViewAdapter webhook templates."""

    @pytest.fixture
    def adapter(self):
        """Create TradingViewAdapter with webhook URL."""
        return TradingViewAdapter(webhook_base_url="https://api.example.com/webhook")

    def test_get_webhook_url_template(self, adapter):
        """Test webhook URL template generation."""
        template = adapter.get_webhook_url_template()

        assert template is not None
        assert "https://api.example.com/webhook" in template
        assert "{webhook_id}" in template

    def test_get_webhook_url_with_default_base(self):
        """Test webhook URL with default base URL."""
        adapter = TradingViewAdapter()
        template = adapter.get_webhook_url_template()

        assert template is not None
        assert "localhost" in template

    def test_get_webhook_url_for_specific_chart(self, adapter):
        """Test getting webhook URL for a specific chart."""
        webhook_url = adapter.get_webhook_url("my_chart_id")

        assert webhook_url == "https://api.example.com/webhook/my_chart_id"

    def test_get_alert_message_template(self, adapter):
        """Test alert message template generation."""
        template = adapter.get_alert_message_template()

        assert template is not None
        # Should include webhook_id
        assert "webhook_id" in template
        # Should include direction
        assert "direction" in template
        # Should include signal_type
        assert "signal_type" in template

    def test_get_alert_message_template_simple(self, adapter):
        """Test simple alert message template."""
        template = adapter.get_alert_message_template_simple()

        assert template is not None
        assert "webhook_id" in template
        assert "direction" in template


class TestTradingViewAdapterConfiguration:
    """Tests for TradingViewAdapter configuration guidance."""

    @pytest.fixture
    def adapter(self):
        """Create TradingViewAdapter instance."""
        return TradingViewAdapter()

    def test_get_setup_instructions(self, adapter):
        """Test setup instructions include key information."""
        instructions = adapter.get_setup_instructions()

        assert instructions is not None
        # Should mention TradingView
        assert "TradingView" in instructions
        # Should mention webhook
        assert "webhook" in instructions.lower() or "Webhook" in instructions
        # Should mention alert
        assert "alert" in instructions.lower() or "Alert" in instructions


class TestTradingViewAdapterToDict:
    """Tests for TradingViewAdapter serialization."""

    @pytest.fixture
    def adapter(self):
        """Create TradingViewAdapter instance."""
        return TradingViewAdapter(webhook_base_url="https://api.example.com")

    def test_to_dict_includes_all_fields(self, adapter):
        """Test to_dict includes all required fields."""
        info = adapter.to_dict()

        assert info["platform_name"] == "TradingView"
        assert info["display_name"] == "TradingView Charts"
        assert info["supports_watchlist_import"] is False
        assert info["supports_real_time_signals"] is True
        assert info["requires_authentication"] is False
        assert info["status"] == "CONNECTED"
        assert info["is_connected"] is True


class TestTradingViewAdapterConstitutionalCompliance:
    """Constitutional compliance tests for TradingViewAdapter."""

    @pytest.mark.constitutional
    def test_adapter_has_no_scoring_methods(self):
        """CRITICAL: Adapter must not have scoring methods."""
        prohibited_methods = [
            'score', 'weight', 'rank', 'prioritize',
            'aggregate', 'recommend', 'advise', 'confidence',
        ]

        for method in prohibited_methods:
            assert not hasattr(TradingViewAdapter, method), \
                f"CONSTITUTIONAL VIOLATION: TradingViewAdapter has {method}"

    @pytest.mark.constitutional
    def test_no_signal_processing(self):
        """CRITICAL: TradingView adapter must not process signals."""
        adapter = TradingViewAdapter()

        # Verify no signal processing methods
        prohibited_signal_methods = [
            'process_signal', 'analyze_signal', 'evaluate_signal',
            'score_signal', 'weight_signal',
        ]

        for method in prohibited_signal_methods:
            assert not hasattr(adapter, method), \
                f"CONSTITUTIONAL VIOLATION: TradingViewAdapter has {method}"

    @pytest.mark.constitutional
    def test_no_recommendation_generation(self):
        """CRITICAL: Adapter must not generate recommendations."""
        adapter = TradingViewAdapter()

        prohibited_recommendation_methods = [
            'recommend', 'suggest', 'advise', 'should_buy', 'should_sell',
        ]

        for method in prohibited_recommendation_methods:
            assert not hasattr(adapter, method), \
                f"CONSTITUTIONAL VIOLATION: TradingViewAdapter has {method}"
