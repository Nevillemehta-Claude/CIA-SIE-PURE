"""
CIA-SIE Kite (Zerodha) Platform Adapter
=======================================

Adapter for Zerodha Kite Connect integration.

GOVERNED BY: Section 8 (Platform-Agnostic Integration)

Kite Connect Integration Model:
- REST API for watchlist and instrument access
- OAuth 2.0 authentication flow
- Watchlist import supported
- Real-time market data available (but not signals)

CRITICAL NOTE:
Kite provides market data and watchlists, but NOT indicator values.
Indicators (RSI, MACD, etc.) must be computed separately or sourced
from TradingView/other charting platforms.

This adapter enables:
- Importing watchlists from Kite
- Fetching instrument metadata
- Creating CIA-SIE instruments from Kite watchlists

This adapter does NOT provide:
- Computed indicator values (user must configure TradingView alerts)
- Trading signals (only raw market data)
"""

import logging
from typing import Optional

import httpx

from cia_sie.platforms.base import (
    ConnectionStatus,
    PlatformAdapter,
    PlatformCredentials,
    PlatformInstrument,
    WatchlistInfo,
)

logger = logging.getLogger(__name__)


class KiteAdapter(PlatformAdapter):
    """
    Zerodha Kite Connect platform adapter.

    Per Gold Standard Specification Section 8.

    Kite Connect provides:
    - Watchlist API: Retrieve user's watchlists
    - Instruments API: Get instrument metadata
    - Market Data: Live quotes and historical data

    Kite Connect does NOT provide:
    - Indicator computations (RSI, MACD, etc.)
    - Trading signals or alerts
    - Chart configurations

    Integration Flow:
    1. User authenticates with Kite Connect OAuth
    2. User selects watchlist to import
    3. CIA-SIE creates instruments from watchlist
    4. User configures TradingView charts for these instruments
    5. TradingView sends signals to CIA-SIE via webhooks
    """

    # Kite Connect API endpoints
    KITE_API_BASE = "https://api.kite.trade"
    KITE_LOGIN_URL = "https://kite.zerodha.com/connect/login"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Kite adapter.

        Args:
            api_key: Kite Connect API key (from developer console)
        """
        super().__init__()
        self._api_key = api_key
        self._access_token: Optional[str] = None
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def platform_name(self) -> str:
        return "Kite"

    @property
    def platform_display_name(self) -> str:
        return "Zerodha Kite"

    @property
    def supports_watchlist_import(self) -> bool:
        return True

    @property
    def supports_real_time_signals(self) -> bool:
        # Kite provides market data, not trading signals
        return False

    @property
    def requires_authentication(self) -> bool:
        return True

    def get_login_url(self) -> str:
        """
        Get the Kite Connect OAuth login URL.

        Returns:
            URL to redirect user for authentication
        """
        if not self._api_key:
            raise ValueError("API key not configured")
        return f"{self.KITE_LOGIN_URL}?api_key={self._api_key}&v=3"

    async def connect(self, credentials: PlatformCredentials) -> bool:
        """
        Connect to Kite using OAuth access token.

        Args:
            credentials: Must contain access_token from OAuth flow

        Returns:
            True if connection successful
        """
        if not credentials.access_token:
            self._last_error = "Access token required"
            self._status = ConnectionStatus.ERROR
            return False

        self._access_token = credentials.access_token
        self._api_key = credentials.api_key or self._api_key

        if not self._api_key:
            self._last_error = "API key required"
            self._status = ConnectionStatus.ERROR
            return False

        self._credentials = credentials
        self._status = ConnectionStatus.CONNECTING

        try:
            self._client = httpx.AsyncClient(
                base_url=self.KITE_API_BASE,
                headers={
                    "Authorization": f"token {self._api_key}:{self._access_token}",
                    "X-Kite-Version": "3",
                },
            )

            # Verify connection with profile endpoint
            if await self.health_check():
                self._status = ConnectionStatus.CONNECTED
                logger.info("Kite adapter connected successfully")
                return True
            else:
                self._status = ConnectionStatus.ERROR
                return False

        except Exception as e:
            self._last_error = str(e)
            self._status = ConnectionStatus.ERROR
            logger.error(f"Kite connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Kite and cleanup."""
        if self._client:
            await self._client.aclose()
            self._client = None

        self._access_token = None
        self._status = ConnectionStatus.DISCONNECTED
        logger.info("Kite adapter disconnected")

    async def health_check(self) -> bool:
        """
        Verify Kite connectivity by fetching user profile.

        Returns:
            True if API is reachable and authenticated
        """
        if not self._client:
            return False

        try:
            response = await self._client.get("/user/profile")
            if response.status_code == 200:
                return True
            else:
                self._last_error = f"API error: {response.status_code}"
                return False
        except Exception as e:
            self._last_error = str(e)
            return False

    async def get_watchlists(self) -> list[WatchlistInfo]:
        """
        Retrieve user's watchlists from Kite.

        Returns:
            List of watchlist metadata
        """
        if not self._client or not self.is_connected:
            raise ConnectionError("Not connected to Kite")

        try:
            # Kite uses "marketwatch" for watchlists
            response = await self._client.get("/marketwatch")

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            data = response.json()
            watchlists = []

            for idx, mw in enumerate(data.get("data", [])):
                watchlists.append(
                    WatchlistInfo(
                        watchlist_id=str(idx),
                        name=f"Watchlist {idx + 1}",
                        instrument_count=len(mw),
                        platform=self.platform_name,
                        metadata={"raw": mw},
                    )
                )

            return watchlists

        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Failed to fetch watchlists: {e}")
            raise

    async def get_instruments(self, watchlist_id: str) -> list[PlatformInstrument]:
        """
        Retrieve instruments from a Kite watchlist.

        Args:
            watchlist_id: Index of the watchlist (0-based)

        Returns:
            List of instruments in the watchlist
        """
        if not self._client or not self.is_connected:
            raise ConnectionError("Not connected to Kite")

        try:
            response = await self._client.get("/marketwatch")

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            data = response.json()
            watchlists = data.get("data", [])

            idx = int(watchlist_id)
            if idx >= len(watchlists):
                raise ValueError(f"Watchlist {watchlist_id} not found")

            instruments = []
            for item in watchlists[idx]:
                instruments.append(
                    PlatformInstrument(
                        symbol=item.get("tradingsymbol", ""),
                        display_name=item.get("tradingsymbol", ""),
                        exchange=item.get("exchange", "NSE"),
                        instrument_type=self._map_instrument_type(
                            item.get("instrument_type", "EQ")
                        ),
                        platform=self.platform_name,
                        platform_symbol=str(item.get("instrument_token", "")),
                        metadata={
                            "instrument_token": item.get("instrument_token"),
                            "exchange": item.get("exchange"),
                            "segment": item.get("segment"),
                        },
                    )
                )

            return instruments

        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Failed to fetch instruments: {e}")
            raise

    def _map_instrument_type(self, kite_type: str) -> str:
        """Map Kite instrument type to standard type."""
        mapping = {
            "EQ": "EQUITY",
            "CE": "OPTION",
            "PE": "OPTION",
            "FUT": "FUTURE",
            "IDX": "INDEX",
        }
        return mapping.get(kite_type, "EQUITY")

    def get_setup_instructions(self) -> str:
        """
        Get setup instructions for Kite integration.

        Returns:
            Markdown-formatted setup instructions
        """
        return """
## Zerodha Kite Connect Setup

### Step 1: Create Kite Connect App
1. Go to https://developers.kite.trade
2. Create a new app
3. Note your API key and API secret

### Step 2: Configure OAuth Redirect
Set your redirect URL to:
```
http://your-domain/api/v1/platforms/kite/callback
```

### Step 3: Authenticate
1. Click "Connect to Kite" in CIA-SIE
2. Log in with your Zerodha credentials
3. Authorize the app

### Step 4: Import Watchlist
1. Select a watchlist from your Kite account
2. Choose instruments to import
3. Map to CIA-SIE silos

### Important Notes
- Kite provides WATCHLIST data only, not indicator values
- For signals with indicators (RSI, MACD), configure TradingView alerts
- TradingView webhooks will send signals to CIA-SIE
"""

    def to_dict(self) -> dict:
        """Convert adapter info to dictionary."""
        base = super().to_dict()
        base.update(
            {
                "login_url": self.get_login_url() if self._api_key else None,
                "integration_type": "api",
                "oauth_required": True,
            }
        )
        return base


# Register adapter on module load
def register():
    """Register Kite adapter with the global registry."""
    from cia_sie.platforms.registry import register_adapter

    register_adapter(KiteAdapter)
