"""
CIA-SIE Platform Adapter Base Class
===================================

Abstract base class for platform integrations.

GOVERNED BY: Section 8.2 (Platform Adapter Interface)

This module defines the contract that all platform adapters must implement.
Each adapter (TradingView, Kite, etc.) provides platform-specific logic
while the core system remains platform-agnostic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class ConnectionStatus(str, Enum):
    """Platform connection status."""

    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    ERROR = "ERROR"


@dataclass
class PlatformCredentials:
    """
    Platform-specific credentials.

    Different platforms require different authentication methods:
    - API key/secret pairs
    - OAuth tokens
    - Session tokens

    Per Gold Standard Specification Section 8.2.
    """

    platform: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if credentials have expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at


@dataclass
class WatchlistInfo:
    """
    Watchlist metadata from a trading platform.

    Per Gold Standard Specification Section 8.3.
    """

    watchlist_id: str
    name: str
    instrument_count: int
    platform: str
    last_updated: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformInstrument:
    """
    Instrument information from a trading platform.

    Represents a tradeable asset that can be imported into CIA-SIE.
    Per Gold Standard Specification Section 8.3.
    """

    symbol: str
    display_name: str
    exchange: str
    instrument_type: str  # EQUITY, COMMODITY, CURRENCY, etc.
    platform: str
    platform_symbol: str  # Symbol as used by the platform
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_instrument_create(self) -> dict:
        """Convert to instrument creation format."""
        return {
            "symbol": self.symbol,
            "display_name": self.display_name,
            "metadata": {
                "exchange": self.exchange,
                "instrument_type": self.instrument_type,
                "platform": self.platform,
                "platform_symbol": self.platform_symbol,
                **self.metadata,
            },
        }


class PlatformAdapter(ABC):
    """
    Abstract base class for platform integrations.

    Per Gold Standard Specification Section 8.2.

    Each platform (TradingView, Kite, etc.) implements this interface.
    The core system is platform-agnostic - it works with any adapter
    that implements this contract.

    CRITICAL DESIGN CONSTRAINTS:
    - Adapters ONLY provide data access, not analysis
    - No scoring, weighting, or aggregation in adapters
    - All data exposed as-is for user interpretation
    """

    def __init__(self):
        self._status = ConnectionStatus.DISCONNECTED
        self._credentials: Optional[PlatformCredentials] = None
        self._last_error: Optional[str] = None

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """
        Return the platform identifier.

        This is used for routing and display purposes.
        Example: "TradingView", "Kite", "Zerodha"
        """
        pass

    @property
    @abstractmethod
    def platform_display_name(self) -> str:
        """
        Return the human-readable platform name.

        Example: "TradingView Charts", "Zerodha Kite"
        """
        pass

    @property
    @abstractmethod
    def supports_watchlist_import(self) -> bool:
        """
        Whether this platform supports watchlist import via API.

        TradingView: False (no public API)
        Kite: True (has REST API for watchlists)
        """
        pass

    @property
    @abstractmethod
    def supports_real_time_signals(self) -> bool:
        """
        Whether this platform can send real-time signals.

        TradingView: True (via webhooks)
        Kite: False (market data only, no signals)
        """
        pass

    @property
    @abstractmethod
    def requires_authentication(self) -> bool:
        """Whether this platform requires authentication."""
        pass

    @property
    def status(self) -> ConnectionStatus:
        """Current connection status."""
        return self._status

    @property
    def last_error(self) -> Optional[str]:
        """Last error message, if any."""
        return self._last_error

    @property
    def is_connected(self) -> bool:
        """Whether currently connected to the platform."""
        return self._status == ConnectionStatus.CONNECTED

    @abstractmethod
    async def connect(self, credentials: PlatformCredentials) -> bool:
        """
        Establish connection to platform.

        Args:
            credentials: Platform-specific credentials

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from platform and cleanup resources."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify platform connectivity.

        Returns:
            True if platform is reachable and authenticated
        """
        pass

    @abstractmethod
    async def get_watchlists(self) -> list[WatchlistInfo]:
        """
        Retrieve available watchlists from the platform.

        Returns:
            List of watchlist metadata

        Raises:
            NotImplementedError: If platform doesn't support watchlist import
        """
        pass

    @abstractmethod
    async def get_instruments(self, watchlist_id: str) -> list[PlatformInstrument]:
        """
        Retrieve instruments from a specific watchlist.

        Args:
            watchlist_id: Platform-specific watchlist identifier

        Returns:
            List of instruments in the watchlist

        Raises:
            NotImplementedError: If platform doesn't support watchlist import
        """
        pass

    def get_webhook_url_template(self) -> Optional[str]:
        """
        Get the webhook URL template for this platform.

        Returns:
            URL template with {webhook_id} placeholder, or None if not applicable
        """
        return None

    def get_alert_message_template(self) -> Optional[str]:
        """
        Get the alert message template for TradingView-style alerts.

        Returns:
            JSON template for alert messages, or None if not applicable
        """
        return None

    def to_dict(self) -> dict:
        """Convert adapter info to dictionary."""
        return {
            "platform_name": self.platform_name,
            "display_name": self.platform_display_name,
            "supports_watchlist_import": self.supports_watchlist_import,
            "supports_real_time_signals": self.supports_real_time_signals,
            "requires_authentication": self.requires_authentication,
            "status": self._status.value,
            "is_connected": self.is_connected,
        }
