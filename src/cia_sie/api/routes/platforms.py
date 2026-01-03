"""
CIA-SIE Platform Integration Routes
====================================

API endpoints for platform adapter management.

GOVERNED BY: Section 8 (Platform-Agnostic Integration)

These endpoints enable:
- Listing available platforms
- Platform connection management
- Watchlist retrieval
- Instrument import from platforms
"""

import hashlib
import logging
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

from cia_sie.core.config import get_settings
from cia_sie.platforms.base import ConnectionStatus, PlatformCredentials
from cia_sie.platforms.registry import get_registry

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# Request/Response Models
# ============================================================================


class PlatformInfo(BaseModel):
    """Platform information response."""

    platform_name: str
    display_name: str
    supports_watchlist_import: bool
    supports_real_time_signals: bool
    requires_authentication: bool
    status: str
    is_connected: bool


class PlatformConnectRequest(BaseModel):
    """Platform connection request."""

    platform: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    access_token: Optional[str] = None


class PlatformConnectResponse(BaseModel):
    """Platform connection response."""

    platform: str
    status: str
    is_connected: bool
    error: Optional[str] = None


class WatchlistResponse(BaseModel):
    """Watchlist information."""

    watchlist_id: str
    name: str
    instrument_count: int
    platform: str


class InstrumentResponse(BaseModel):
    """Instrument information from platform."""

    symbol: str
    display_name: str
    exchange: str
    instrument_type: str
    platform: str
    platform_symbol: str


class ImportInstrumentsRequest(BaseModel):
    """Request to import instruments from a platform."""

    platform: str
    watchlist_id: str
    instrument_symbols: list[str]
    default_silo_name: Optional[str] = "Default Analysis"


class SetupInstructionsResponse(BaseModel):
    """Setup instructions for a platform."""

    platform: str
    instructions: str
    webhook_url_template: Optional[str] = None
    alert_message_template: Optional[str] = None


# ============================================================================
# Endpoints
# ============================================================================


@router.get("/", response_model=list[PlatformInfo])
async def list_platforms():
    """
    List all available trading platform adapters.

    Returns information about each registered platform adapter,
    including capabilities and connection status.
    """
    registry = get_registry()

    # Register default adapters if not already registered
    _ensure_adapters_registered()

    return registry.list_all()


@router.get("/{platform_name}", response_model=PlatformInfo)
async def get_platform(platform_name: str):
    """
    Get information about a specific platform.

    Args:
        platform_name: Name of the platform (e.g., "TradingView", "Kite")
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(platform_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")

    return adapter.to_dict()


@router.post("/connect", response_model=PlatformConnectResponse)
async def connect_platform(request: PlatformConnectRequest):
    """
    Connect to a trading platform.

    For platforms like Kite that require authentication,
    provide the necessary credentials.

    For webhook-based platforms like TradingView,
    connection is automatic.
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(request.platform)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{request.platform}' not found")

    credentials = PlatformCredentials(
        platform=request.platform,
        api_key=request.api_key,
        api_secret=request.api_secret,
        access_token=request.access_token,
    )

    try:
        success = await adapter.connect(credentials)
        return PlatformConnectResponse(
            platform=request.platform,
            status=adapter.status.value,
            is_connected=success,
            error=adapter.last_error if not success else None,
        )
    except Exception as e:
        logger.error(f"Platform connection error: {e}")
        return PlatformConnectResponse(
            platform=request.platform,
            status=ConnectionStatus.ERROR.value,
            is_connected=False,
            error=str(e),
        )


@router.post("/{platform_name}/disconnect")
async def disconnect_platform(platform_name: str):
    """
    Disconnect from a platform.
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(platform_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")

    await adapter.disconnect()
    return {"platform": platform_name, "status": "disconnected"}


@router.get("/{platform_name}/health")
async def check_platform_health(platform_name: str):
    """
    Check platform connectivity health.
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(platform_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")

    is_healthy = await adapter.health_check()
    return {
        "platform": platform_name,
        "healthy": is_healthy,
        "status": adapter.status.value,
    }


@router.get("/{platform_name}/watchlists", response_model=list[WatchlistResponse])
async def get_watchlists(platform_name: str):
    """
    Get watchlists from a platform.

    Only available for platforms that support watchlist import
    (e.g., Kite). Will raise an error for webhook-only platforms
    like TradingView.
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(platform_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")

    if not adapter.supports_watchlist_import:
        raise HTTPException(
            status_code=400,
            detail=f"Platform '{platform_name}' does not support watchlist import. "
            f"Please configure instruments manually.",
        )

    if not adapter.is_connected:
        raise HTTPException(
            status_code=400, detail=f"Not connected to '{platform_name}'. Please connect first."
        )

    try:
        watchlists = await adapter.get_watchlists()
        return [
            WatchlistResponse(
                watchlist_id=wl.watchlist_id,
                name=wl.name,
                instrument_count=wl.instrument_count,
                platform=wl.platform,
            )
            for wl in watchlists
        ]
    except NotImplementedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to fetch watchlists: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{platform_name}/watchlists/{watchlist_id}/instruments",
    response_model=list[InstrumentResponse],
)
async def get_watchlist_instruments(platform_name: str, watchlist_id: str):
    """
    Get instruments from a specific watchlist.
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(platform_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")

    if not adapter.supports_watchlist_import:
        raise HTTPException(
            status_code=400, detail=f"Platform '{platform_name}' does not support watchlist import"
        )

    if not adapter.is_connected:
        raise HTTPException(
            status_code=400, detail=f"Not connected to '{platform_name}'. Please connect first."
        )

    try:
        instruments = await adapter.get_instruments(watchlist_id)
        return [
            InstrumentResponse(
                symbol=inst.symbol,
                display_name=inst.display_name,
                exchange=inst.exchange,
                instrument_type=inst.instrument_type,
                platform=inst.platform,
                platform_symbol=inst.platform_symbol,
            )
            for inst in instruments
        ]
    except NotImplementedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to fetch instruments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{platform_name}/setup", response_model=SetupInstructionsResponse)
async def get_setup_instructions(platform_name: str):
    """
    Get setup instructions for a platform.

    Returns markdown-formatted instructions for configuring
    the platform integration.
    """
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get(platform_name)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")

    instructions = ""
    webhook_template = None
    alert_template = None

    if hasattr(adapter, "get_setup_instructions"):
        instructions = adapter.get_setup_instructions()

    if hasattr(adapter, "get_webhook_url_template"):
        webhook_template = adapter.get_webhook_url_template()

    if hasattr(adapter, "get_alert_message_template"):
        alert_template = adapter.get_alert_message_template()

    return SetupInstructionsResponse(
        platform=platform_name,
        instructions=instructions,
        webhook_url_template=webhook_template,
        alert_message_template=alert_template,
    )


# ============================================================================
# Kite OAuth Endpoints
# ============================================================================


@router.get("/kite/login")
async def kite_login():
    """
    Redirect user to Kite login page for OAuth authentication.

    This initiates the Kite Connect OAuth flow.
    After login, Kite will redirect to /api/v1/platforms/kite/callback
    """
    settings = get_settings()

    if not settings.kite_api_key:
        raise HTTPException(
            status_code=500, detail="Kite API key not configured. Please set KITE_API_KEY in .env"
        )

    login_url = f"https://kite.zerodha.com/connect/login?api_key={settings.kite_api_key}&v=3"
    return RedirectResponse(url=login_url)


@router.get("/kite/callback")
async def kite_oauth_callback(
    request_token: str = Query(..., description="Request token from Kite OAuth"),
    status: str = Query(None, description="OAuth status"),
):
    """
    Handle Kite OAuth callback.

    This endpoint receives the request_token from Kite after user login,
    exchanges it for an access_token, and connects the Kite adapter.
    """
    settings = get_settings()

    if not settings.kite_api_key or not settings.kite_api_secret:
        raise HTTPException(status_code=500, detail="Kite API credentials not configured")

    # Generate checksum: SHA256(api_key + request_token + api_secret)
    checksum_string = settings.kite_api_key + request_token + settings.kite_api_secret
    checksum = hashlib.sha256(checksum_string.encode()).hexdigest()

    # Exchange request_token for access_token
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.kite.trade/session/token",
                data={
                    "api_key": settings.kite_api_key,
                    "request_token": request_token,
                    "checksum": checksum,
                },
            )

            if response.status_code != 200:
                logger.error(f"Kite token exchange failed: {response.text}")
                return HTMLResponse(
                    content=f"""
                    <html>
                    <head><title>Kite Connection Failed</title></head>
                    <body style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
                        <h1 style="color: #e53935;">Connection Failed</h1>
                        <p>Failed to connect to Kite: {response.json().get("message", "Unknown error")}</p>
                        <p><a href="/api/v1/platforms/kite/login">Try Again</a></p>
                    </body>
                    </html>
                    """,
                    status_code=400,
                )

            data = response.json()
            access_token = data.get("data", {}).get("access_token")

            if not access_token:
                raise HTTPException(status_code=500, detail="No access token received")

            # Connect the Kite adapter with the access token
            registry = get_registry()
            _ensure_adapters_registered()

            adapter = registry.get("Kite")
            if adapter:
                credentials = PlatformCredentials(
                    platform="Kite",
                    api_key=settings.kite_api_key,
                    access_token=access_token,
                )
                await adapter.connect(credentials)

            # Return success page
            return HTMLResponse(
                content=f"""
                <html>
                <head><title>Kite Connected Successfully</title></head>
                <body style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
                    <h1 style="color: #43a047;">Connected to Kite!</h1>
                    <p>Your Zerodha Kite account is now connected to CIA-SIE.</p>
                    <p>User: {data.get("data", {}).get("user_name", "Unknown")}</p>
                    <p>You can now import watchlists and instruments.</p>
                    <br>
                    <p><a href="http://localhost:3000" style="padding: 10px 20px; background: #2962ff; color: white; text-decoration: none; border-radius: 4px;">Go to CIA-SIE Dashboard</a></p>
                </body>
                </html>
                """
            )

    except httpx.RequestError as e:
        logger.error(f"Kite API request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to Kite API: {str(e)}")


@router.get("/kite/status")
async def kite_connection_status():
    """
    Check Kite connection status.
    """
    settings = get_settings()
    registry = get_registry()
    _ensure_adapters_registered()

    adapter = registry.get("Kite")

    return {
        "configured": bool(settings.kite_api_key and settings.kite_api_secret),
        "connected": adapter.is_connected if adapter else False,
        "status": adapter.status.value if adapter else "not_initialized",
        "login_url": "/api/v1/platforms/kite/login" if settings.kite_api_key else None,
    }


# ============================================================================
# Helper Functions
# ============================================================================


def _ensure_adapters_registered():
    """Ensure default adapters are registered."""
    registry = get_registry()

    if not registry.is_registered("TradingView"):
        from cia_sie.platforms.tradingview import TradingViewAdapter

        registry.register(TradingViewAdapter)

    if not registry.is_registered("Kite"):
        from cia_sie.platforms.kite import KiteAdapter

        registry.register(KiteAdapter)
