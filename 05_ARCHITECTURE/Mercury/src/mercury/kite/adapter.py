"""
Mercury Kite Adapter
====================

Wrapper around Kite Connect API for market data access.

CONSTITUTIONAL: MR-001 - All market data comes through this adapter.

AUTONOMOUS ENHANCEMENTS:
- Integrated OAuth manager for automatic token handling
- Rate limiting to prevent API bans
- Circuit breaker integration for resilience
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Callable, TypeVar, Awaitable
from functools import wraps

from mercury.core.config import get_settings
from mercury.core.exceptions import (
    KiteAPIError,
    KiteAuthError,
    KiteRateLimitError,
    SymbolNotFoundError,
)
from mercury.core.rate_limiter import get_kite_limiter, RateLimitExceeded
from mercury.core.resilience import kite_circuit, CircuitOpenError
from mercury.kite.models import (
    Quote,
    OHLC,
    Position,
    Holding,
    Instrument,
    MarketDataBundle,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


def rate_limited(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """Decorator to apply rate limiting to Kite API calls."""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        limiter = get_kite_limiter()
        try:
            await limiter.acquire()
            return await func(*args, **kwargs)
        except RateLimitExceeded as e:
            raise KiteRateLimitError(f"Rate limit exceeded: {e}")
    return wrapper


def circuit_protected(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """Decorator to apply circuit breaker protection to Kite API calls."""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        if not kite_circuit.allow_request():
            raise KiteAPIError(
                "Kite API circuit breaker is open - service temporarily unavailable"
            )
        try:
            result = await func(*args, **kwargs)
            kite_circuit.record_success()
            return result
        except (KiteAuthError, SymbolNotFoundError):
            # Don't count auth errors or symbol not found as circuit failures
            raise
        except Exception as e:
            kite_circuit.record_failure(e)
            raise
    return wrapper


class KiteAdapter:
    """
    Adapter for Kite Connect API.
    
    CONSTITUTIONAL: MR-001 - This is the sole source of market data.
    All data-grounded responses must come through this adapter.
    
    AUTONOMOUS FEATURES:
    - Rate limiting (1 request/second with burst of 3)
    - Circuit breaker protection (fails fast when API is down)
    - OAuth manager integration (automatic token handling)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        use_oauth_manager: bool = True,
    ):
        """
        Initialize Kite adapter.
        
        Args:
            api_key: Kite API key (defaults to settings)
            access_token: Session access token (defaults to settings)
            use_oauth_manager: Whether to use OAuth manager for token handling
        """
        settings = get_settings()
        self.api_key = api_key or settings.kite_api_key
        self.access_token = access_token or settings.kite_access_token
        self._kite = None
        self._instruments_cache: dict[str, Instrument] = {}
        self._use_oauth_manager = use_oauth_manager
        self._oauth_manager = None
        
    @property
    def oauth_manager(self):
        """Get the OAuth manager (lazy initialization)."""
        if self._oauth_manager is None and self._use_oauth_manager:
            from mercury.kite.oauth_manager import get_oauth_manager
            self._oauth_manager = get_oauth_manager()
        return self._oauth_manager
    
    @property
    def kite(self):
        """Get or create Kite Connect client."""
        if self._kite is None:
            try:
                from kiteconnect import KiteConnect
                self._kite = KiteConnect(api_key=self.api_key)
                if self.access_token:
                    self._kite.set_access_token(self.access_token)
            except ImportError:
                logger.warning("kiteconnect not installed, using mock mode")
                self._kite = MockKite()
            except Exception as e:
                raise KiteAPIError(f"Failed to initialize Kite: {e}")
        return self._kite
    
    def is_authenticated(self) -> bool:
        """Check if we have a valid session."""
        return self.access_token is not None
    
    def set_access_token(self, token: str) -> None:
        """Set access token after OAuth."""
        self.access_token = token
        if self._kite:
            self._kite.set_access_token(token)
    
    async def _handle_token_error(self, error: Exception) -> None:
        """Handle token-related errors by notifying OAuth manager."""
        if self.oauth_manager:
            await self.oauth_manager.handle_token_exception(error)
    
    @rate_limited
    @circuit_protected
    async def get_quote(self, symbol: str, exchange: str = "NSE") -> Quote:
        """
        Get current market quote for a symbol.
        
        Args:
            symbol: Trading symbol (any valid symbol on the exchange)
            exchange: Exchange code (NSE, BSE, NFO)
            
        Returns:
            Quote object with current market data
            
        Raises:
            SymbolNotFoundError: If symbol doesn't exist
            KiteAPIError: If API call fails
        """
        try:
            instrument_key = f"{exchange}:{symbol}"
            data = self.kite.quote([instrument_key])
            
            if instrument_key not in data:
                raise SymbolNotFoundError(symbol)
            
            q = data[instrument_key]
            
            return Quote(
                symbol=symbol,
                exchange=exchange,
                ltp=q.get("last_price", 0),
                open=q.get("ohlc", {}).get("open", 0),
                high=q.get("ohlc", {}).get("high", 0),
                low=q.get("ohlc", {}).get("low", 0),
                close=q.get("ohlc", {}).get("close", 0),
                volume=q.get("volume", 0),
                change=q.get("net_change", 0),
                change_percent=q.get("change", 0),
                timestamp=datetime.now(),
                bid=q.get("depth", {}).get("buy", [{}])[0].get("price"),
                ask=q.get("depth", {}).get("sell", [{}])[0].get("price"),
            )
            
        except SymbolNotFoundError:
            raise
        except Exception as e:
            if "TokenException" in str(type(e).__name__):
                await self._handle_token_error(e)
                raise KiteAuthError("Session expired")
            if "NetworkException" in str(type(e).__name__):
                raise KiteAPIError(f"Network error: {e}")
            if "DataException" in str(type(e).__name__):
                raise SymbolNotFoundError(symbol)
            raise KiteAPIError(f"Quote fetch failed: {e}")
    
    @rate_limited
    @circuit_protected
    async def get_ltp(self, symbols: list[str]) -> dict[str, float]:
        """
        Get last traded prices for multiple symbols.
        
        Args:
            symbols: List of symbols (format: "EXCHANGE:SYMBOL")
            
        Returns:
            Dict mapping symbol to LTP
        """
        try:
            data = self.kite.ltp(symbols)
            return {
                key: val.get("last_price", 0)
                for key, val in data.items()
            }
        except Exception as e:
            if "TokenException" in str(type(e).__name__):
                await self._handle_token_error(e)
                raise KiteAuthError("Session expired")
            raise KiteAPIError(f"LTP fetch failed: {e}")
    
    @rate_limited
    @circuit_protected
    async def get_ohlc(
        self,
        symbol: str,
        exchange: str = "NSE",
        interval: str = "day",
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> list[OHLC]:
        """
        Get historical OHLC data.
        
        Args:
            symbol: Trading symbol
            exchange: Exchange code
            interval: Candle interval (minute, day, week, month)
            from_date: Start date (default: 30 days ago)
            to_date: End date (default: today)
            
        Returns:
            List of OHLC candles
        """
        try:
            if to_date is None:
                to_date = datetime.now()
            if from_date is None:
                from_date = to_date - timedelta(days=30)
            
            # Get instrument token
            instrument_key = f"{exchange}:{symbol}"
            instruments = await self.search_instruments(symbol)
            
            token = None
            for inst in instruments:
                if inst.exchange == exchange and inst.symbol == symbol:
                    token = inst.instrument_token
                    break
            
            if token is None:
                raise SymbolNotFoundError(symbol)
            
            data = self.kite.historical_data(
                instrument_token=token,
                from_date=from_date,
                to_date=to_date,
                interval=interval,
            )
            
            return [
                OHLC(
                    date=candle["date"],
                    open=candle["open"],
                    high=candle["high"],
                    low=candle["low"],
                    close=candle["close"],
                    volume=candle.get("volume", 0),
                )
                for candle in data
            ]
            
        except SymbolNotFoundError:
            raise
        except Exception as e:
            raise KiteAPIError(f"OHLC fetch failed: {e}")
    
    @rate_limited
    @circuit_protected
    async def get_positions(self) -> list[Position]:
        """Get all open positions."""
        try:
            data = self.kite.positions()
            net_positions = data.get("net", [])
            
            positions = []
            for p in net_positions:
                if p.get("quantity", 0) != 0:
                    qty = p.get("quantity", 0)
                    avg = p.get("average_price", 0)
                    ltp = p.get("last_price", 0)
                    pnl = (ltp - avg) * qty
                    pnl_pct = ((ltp - avg) / avg * 100) if avg != 0 else 0
                    
                    positions.append(Position(
                        symbol=p.get("tradingsymbol", ""),
                        exchange=p.get("exchange", ""),
                        product=p.get("product", ""),
                        quantity=qty,
                        average_price=avg,
                        ltp=ltp,
                        pnl=pnl,
                        pnl_percent=pnl_pct,
                        buy_quantity=p.get("buy_quantity", 0),
                        sell_quantity=p.get("sell_quantity", 0),
                    ))
            
            return positions
            
        except Exception as e:
            if "TokenException" in str(type(e).__name__):
                await self._handle_token_error(e)
                raise KiteAuthError("Session expired")
            raise KiteAPIError(f"Positions fetch failed: {e}")
    
    @rate_limited
    @circuit_protected
    async def get_holdings(self) -> list[Holding]:
        """Get all holdings (delivery positions)."""
        try:
            data = self.kite.holdings()
            
            holdings = []
            for h in data:
                qty = h.get("quantity", 0)
                avg = h.get("average_price", 0)
                ltp = h.get("last_price", 0)
                pnl = (ltp - avg) * qty
                pnl_pct = ((ltp - avg) / avg * 100) if avg != 0 else 0
                
                holdings.append(Holding(
                    symbol=h.get("tradingsymbol", ""),
                    exchange=h.get("exchange", ""),
                    quantity=qty,
                    average_price=avg,
                    ltp=ltp,
                    pnl=pnl,
                    pnl_percent=pnl_pct,
                    isin=h.get("isin", ""),
                    collateral_quantity=h.get("collateral_quantity", 0),
                    t1_quantity=h.get("t1_quantity", 0),
                ))
            
            return holdings
            
        except Exception as e:
            if "TokenException" in str(type(e).__name__):
                await self._handle_token_error(e)
                raise KiteAuthError("Session expired")
            raise KiteAPIError(f"Holdings fetch failed: {e}")
    
    @rate_limited
    @circuit_protected
    async def search_instruments(self, query: str) -> list[Instrument]:
        """Search for instruments by name or symbol."""
        try:
            # Cache instruments on first call
            if not self._instruments_cache:
                all_instruments = self.kite.instruments()
                for i in all_instruments:
                    key = f"{i['exchange']}:{i['tradingsymbol']}"
                    self._instruments_cache[key] = Instrument(
                        instrument_token=i["instrument_token"],
                        exchange_token=i["exchange_token"],
                        symbol=i["tradingsymbol"],
                        name=i.get("name", ""),
                        exchange=i["exchange"],
                        segment=i.get("segment", ""),
                        instrument_type=i.get("instrument_type", ""),
                        lot_size=i.get("lot_size", 1),
                        tick_size=i.get("tick_size", 0.05),
                    )
            
            # Search
            query_lower = query.lower()
            results = []
            for inst in self._instruments_cache.values():
                if (query_lower in inst.symbol.lower() or 
                    query_lower in inst.name.lower()):
                    results.append(inst)
                    if len(results) >= 20:  # Limit results
                        break
            
            return results
            
        except Exception as e:
            raise KiteAPIError(f"Instrument search failed: {e}")
    
    async def get_data_bundle(
        self,
        symbols: list[str],
        include_positions: bool = True,
        include_holdings: bool = True,
        include_history: bool = False,
    ) -> MarketDataBundle:
        """
        Get a bundle of market data for AI context.
        
        Args:
            symbols: List of symbols to fetch quotes for
            include_positions: Include user's positions
            include_holdings: Include user's holdings
            include_history: Include historical data for symbols
            
        Returns:
            MarketDataBundle with all requested data
        """
        bundle = MarketDataBundle()
        
        # Fetch quotes
        for symbol in symbols:
            try:
                # Parse "EXCHANGE:SYMBOL" format or default to NSE
                if ":" in symbol:
                    exchange, sym = symbol.split(":", 1)
                else:
                    exchange, sym = "NSE", symbol
                
                quote = await self.get_quote(sym, exchange)
                bundle.quotes[symbol] = quote
            except Exception as e:
                logger.warning(f"Failed to fetch quote for {symbol}: {e}")
        
        # Fetch positions
        if include_positions:
            try:
                bundle.positions = await self.get_positions()
            except Exception as e:
                logger.warning(f"Failed to fetch positions: {e}")
        
        # Fetch holdings
        if include_holdings:
            try:
                bundle.holdings = await self.get_holdings()
            except Exception as e:
                logger.warning(f"Failed to fetch holdings: {e}")
        
        # Fetch historical data
        if include_history:
            for symbol in symbols:
                try:
                    if ":" in symbol:
                        exchange, sym = symbol.split(":", 1)
                    else:
                        exchange, sym = "NSE", symbol
                    
                    history = await self.get_ohlc(sym, exchange)
                    bundle.historical[symbol] = history
                except Exception as e:
                    logger.warning(f"Failed to fetch history for {symbol}: {e}")
        
        bundle.timestamp = datetime.now()
        return bundle


class MockKite:
    """Mock Kite client for development without API access."""
    
    def quote(self, instruments: list[str]) -> dict:
        """Return mock quote data."""
        import random
        result = {}
        for inst in instruments:
            base_price = random.uniform(50, 5000)
            change = random.uniform(-2, 2)
            result[inst] = {
                "last_price": base_price,
                "ohlc": {
                    "open": base_price * 0.99,
                    "high": base_price * 1.02,
                    "low": base_price * 0.98,
                    "close": base_price * (1 - change/100),
                },
                "volume": random.randint(10000, 1000000),
                "net_change": base_price * change / 100,
                "change": change,
            }
        return result
    
    def ltp(self, instruments: list[str]) -> dict:
        """Return mock LTP data."""
        import random
        return {inst: {"last_price": random.uniform(50, 5000)} for inst in instruments}
    
    def positions(self) -> dict:
        """Return mock positions."""
        return {"net": [], "day": []}
    
    def holdings(self) -> list:
        """Return mock holdings."""
        return []
    
    def instruments(self) -> list:
        """
        Return mock instruments.
        
        NOTE: This is MOCK MODE - returns empty list.
        In production with real Kite API, this fetches the full instrument master.
        The system is fully instrument-agnostic.
        """
        # Return empty in mock mode - no hardcoded instruments
        # Real Kite API will return the full instrument master
        return []
    
    def historical_data(self, **kwargs) -> list:
        """Return mock historical data."""
        import random
        from datetime import datetime, timedelta
        
        data = []
        base = random.uniform(50, 5000)
        for i in range(30):
            date = datetime.now() - timedelta(days=30-i)
            data.append({
                "date": date,
                "open": base,
                "high": base * 1.02,
                "low": base * 0.98,
                "close": base * random.uniform(0.98, 1.02),
                "volume": random.randint(10000, 1000000),
            })
            base = data[-1]["close"]
        return data
    
    def set_access_token(self, token: str) -> None:
        """Set access token (no-op for mock)."""
        pass
