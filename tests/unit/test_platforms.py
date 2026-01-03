"""
Tests for CIA-SIE Platform Adapters
===================================

Validates platform adapter base classes and implementations.

GOVERNED BY: Section 8.2 (Platform Adapter Interface)
"""

import pytest
from datetime import datetime, timedelta

from cia_sie.platforms.base import (
    ConnectionStatus,
    PlatformCredentials,
    WatchlistInfo,
    PlatformInstrument,
    PlatformAdapter,
)


class TestConnectionStatus:
    """Tests for ConnectionStatus enum."""

    def test_all_status_values_exist(self):
        """Test all required status values exist."""
        assert hasattr(ConnectionStatus, 'DISCONNECTED')
        assert hasattr(ConnectionStatus, 'CONNECTING')
        assert hasattr(ConnectionStatus, 'CONNECTED')
        assert hasattr(ConnectionStatus, 'ERROR')

    def test_status_values_are_strings(self):
        """Test status values are string-based."""
        assert ConnectionStatus.DISCONNECTED.value == "DISCONNECTED"
        assert ConnectionStatus.CONNECTED.value == "CONNECTED"


class TestPlatformCredentials:
    """Tests for PlatformCredentials dataclass."""

    def test_credentials_creation(self):
        """Test creating platform credentials."""
        creds = PlatformCredentials(
            platform="TradingView",
            api_key="test_key",
            api_secret="test_secret",
        )
        assert creds.platform == "TradingView"
        assert creds.api_key == "test_key"
        assert creds.api_secret == "test_secret"

    def test_credentials_with_oauth(self):
        """Test credentials with OAuth tokens."""
        expires = datetime.utcnow() + timedelta(hours=1)
        creds = PlatformCredentials(
            platform="Kite",
            access_token="access_123",
            refresh_token="refresh_456",
            expires_at=expires,
        )
        assert creds.access_token == "access_123"
        assert creds.refresh_token == "refresh_456"
        assert creds.expires_at == expires

    def test_is_expired_when_expired(self):
        """Test is_expired returns True when expired."""
        expired_time = datetime.utcnow() - timedelta(hours=1)
        creds = PlatformCredentials(
            platform="Test",
            expires_at=expired_time,
        )
        assert creds.is_expired() is True

    def test_is_expired_when_valid(self):
        """Test is_expired returns False when valid."""
        future_time = datetime.utcnow() + timedelta(hours=1)
        creds = PlatformCredentials(
            platform="Test",
            expires_at=future_time,
        )
        assert creds.is_expired() is False

    def test_is_expired_when_no_expiry(self):
        """Test is_expired returns False when no expiry set."""
        creds = PlatformCredentials(platform="Test")
        assert creds.is_expired() is False

    def test_credentials_metadata(self):
        """Test credentials with metadata."""
        creds = PlatformCredentials(
            platform="Test",
            metadata={"region": "us-east-1"},
        )
        assert creds.metadata == {"region": "us-east-1"}


class TestWatchlistInfo:
    """Tests for WatchlistInfo dataclass."""

    def test_watchlist_creation(self):
        """Test creating watchlist info."""
        watchlist = WatchlistInfo(
            watchlist_id="wl_123",
            name="My Watchlist",
            instrument_count=10,
            platform="Kite",
        )
        assert watchlist.watchlist_id == "wl_123"
        assert watchlist.name == "My Watchlist"
        assert watchlist.instrument_count == 10
        assert watchlist.platform == "Kite"

    def test_watchlist_with_metadata(self):
        """Test watchlist with optional metadata."""
        watchlist = WatchlistInfo(
            watchlist_id="wl_456",
            name="Tech Stocks",
            instrument_count=25,
            platform="Kite",
            last_updated=datetime.utcnow(),
            metadata={"category": "technology"},
        )
        assert watchlist.metadata == {"category": "technology"}
        assert watchlist.last_updated is not None


class TestPlatformInstrument:
    """Tests for PlatformInstrument dataclass."""

    def test_instrument_creation(self):
        """Test creating platform instrument."""
        instrument = PlatformInstrument(
            symbol="NIFTY50",
            display_name="Nifty 50 Index",
            exchange="NSE",
            instrument_type="INDEX",
            platform="Kite",
            platform_symbol="NSE:NIFTY50",
        )
        assert instrument.symbol == "NIFTY50"
        assert instrument.display_name == "Nifty 50 Index"
        assert instrument.exchange == "NSE"
        assert instrument.instrument_type == "INDEX"

    def test_to_instrument_create(self):
        """Test converting to instrument creation format."""
        instrument = PlatformInstrument(
            symbol="RELIANCE",
            display_name="Reliance Industries",
            exchange="NSE",
            instrument_type="EQUITY",
            platform="Kite",
            platform_symbol="NSE:RELIANCE",
            metadata={"sector": "Energy"},
        )
        create_data = instrument.to_instrument_create()

        assert create_data["symbol"] == "RELIANCE"
        assert create_data["display_name"] == "Reliance Industries"
        assert create_data["metadata"]["exchange"] == "NSE"
        assert create_data["metadata"]["instrument_type"] == "EQUITY"
        assert create_data["metadata"]["platform"] == "Kite"
        assert create_data["metadata"]["sector"] == "Energy"

    @pytest.mark.constitutional
    def test_instrument_has_no_weight(self):
        """CRITICAL: PlatformInstrument must have no weight."""
        instrument = PlatformInstrument(
            symbol="TEST",
            display_name="Test",
            exchange="NSE",
            instrument_type="EQUITY",
            platform="Kite",
            platform_symbol="NSE:TEST",
        )
        assert not hasattr(instrument, 'weight')
        assert not hasattr(instrument, 'priority')
        assert not hasattr(instrument, 'score')


class TestPlatformAdapterContract:
    """Tests for PlatformAdapter abstract base class."""

    def test_adapter_is_abstract(self):
        """Test that PlatformAdapter is abstract."""
        with pytest.raises(TypeError):
            PlatformAdapter()

    def test_adapter_has_required_abstract_methods(self):
        """Test adapter defines all required abstract methods."""
        required_methods = [
            'platform_name',
            'platform_display_name',
            'supports_watchlist_import',
            'supports_real_time_signals',
            'requires_authentication',
            'connect',
            'disconnect',
            'health_check',
            'get_watchlists',
            'get_instruments',
        ]

        for method in required_methods:
            assert hasattr(PlatformAdapter, method), \
                f"PlatformAdapter missing required method: {method}"

    @pytest.mark.constitutional
    def test_adapter_has_no_scoring_methods(self):
        """CRITICAL: Adapter must not have scoring methods."""
        prohibited_methods = [
            'score', 'weight', 'rank', 'prioritize',
            'aggregate', 'recommend', 'advise',
        ]

        for method in prohibited_methods:
            assert not hasattr(PlatformAdapter, method), \
                f"CONSTITUTIONAL VIOLATION: PlatformAdapter has {method}"


class TestMockPlatformAdapter:
    """Tests using a mock platform adapter implementation."""

    @pytest.fixture
    def mock_adapter(self):
        """Create a mock adapter implementation."""

        class MockAdapter(PlatformAdapter):
            @property
            def platform_name(self):
                return "MockPlatform"

            @property
            def platform_display_name(self):
                return "Mock Platform"

            @property
            def supports_watchlist_import(self):
                return True

            @property
            def supports_real_time_signals(self):
                return True

            @property
            def requires_authentication(self):
                return True

            async def connect(self, credentials):
                self._status = ConnectionStatus.CONNECTED
                return True

            async def disconnect(self):
                self._status = ConnectionStatus.DISCONNECTED

            async def health_check(self):
                return self._status == ConnectionStatus.CONNECTED

            async def get_watchlists(self):
                return []

            async def get_instruments(self, watchlist_id):
                return []

        return MockAdapter()

    def test_initial_status_disconnected(self, mock_adapter):
        """Test adapter starts disconnected."""
        assert mock_adapter.status == ConnectionStatus.DISCONNECTED
        assert mock_adapter.is_connected is False

    @pytest.mark.asyncio
    async def test_connect_updates_status(self, mock_adapter):
        """Test connect updates status."""
        creds = PlatformCredentials(platform="Mock")
        result = await mock_adapter.connect(creds)

        assert result is True
        assert mock_adapter.status == ConnectionStatus.CONNECTED
        assert mock_adapter.is_connected is True

    @pytest.mark.asyncio
    async def test_disconnect_updates_status(self, mock_adapter):
        """Test disconnect updates status."""
        creds = PlatformCredentials(platform="Mock")
        await mock_adapter.connect(creds)
        await mock_adapter.disconnect()

        assert mock_adapter.status == ConnectionStatus.DISCONNECTED
        assert mock_adapter.is_connected is False

    def test_to_dict(self, mock_adapter):
        """Test to_dict method."""
        info = mock_adapter.to_dict()

        assert info["platform_name"] == "MockPlatform"
        assert info["display_name"] == "Mock Platform"
        assert info["supports_watchlist_import"] is True
        assert info["supports_real_time_signals"] is True
        assert info["requires_authentication"] is True
        assert info["status"] == "DISCONNECTED"
        assert info["is_connected"] is False

    def test_get_webhook_url_template_default(self, mock_adapter):
        """Test default webhook URL template is None."""
        assert mock_adapter.get_webhook_url_template() is None

    def test_get_alert_message_template_default(self, mock_adapter):
        """Test default alert message template is None."""
        assert mock_adapter.get_alert_message_template() is None
