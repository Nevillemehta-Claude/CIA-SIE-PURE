"""
CIA-SIE Kite Intelligence Engine
=================================

Market intelligence layer powered by Kite Connect API.

This engine provides:
- Real-time market data (quotes, depth)
- Historical data analysis
- Reference data (index constituents, sectors)
- Computed metrics (volume anomalies, top movers)

CONSTITUTIONAL COMPLIANCE:
- All methods return FACTUAL DATA only
- No predictions, recommendations, or confidence scores
- Data is exposed for user interpretation

GOVERNED BY: Section 8 (Platform Integration) and Constitutional Rules
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, time
from decimal import Decimal
from enum import Enum
from typing import Optional

from cia_sie.platforms.kite import KiteAdapter


class KiteInterval(str, Enum):
    """Kite historical data intervals."""
    MINUTE = "minute"
    FIVE_MINUTE = "5minute"
    FIFTEEN_MINUTE = "15minute"
    THIRTY_MINUTE = "30minute"
    HOUR = "60minute"
    DAY = "day"


@dataclass
class Quote:
    """Real-time market quote."""
    symbol: str
    ltp: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    change: Decimal
    change_percent: Decimal
    timestamp: datetime


@dataclass
class OHLCV:
    """Historical candle data."""
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


@dataclass
class VolumeProfile:
    """Volume analysis for a specific time window."""
    symbol: str
    current_volume: int
    average_volume: float
    volume_ratio: float  # current / average
    time_window: tuple[time, time]
    baseline_days: int


@dataclass
class InstrumentInfo:
    """Comprehensive instrument information."""
    symbol: str
    trading_symbol: str
    exchange: str
    instrument_token: int
    instrument_type: str
    segment: str
    lot_size: int
    tick_size: Decimal


@dataclass
class TopMover:
    """Top mover result."""
    symbol: str
    ltp: Decimal
    metric_value: float  # The value of the metric used for ranking
    metric_name: str
    rank: int


class KiteIntelligenceEngine:
    """
    Market intelligence layer powered by Kite Connect API.
    
    This engine provides:
    - Real-time market data (quotes, depth)
    - Historical data analysis
    - Reference data (index constituents, sectors)
    - Computed metrics (volume anomalies, top movers)
    
    CONSTITUTIONAL COMPLIANCE:
    - All methods return FACTUAL DATA only
    - No predictions, recommendations, or confidence scores
    - Data is exposed for user interpretation
    """
    
    # Index constituent mappings (cached on startup)
    # These should be loaded from Kite instruments API
    INDEX_CONSTITUENTS = {
        "NIFTY50": [],  # Load from Kite instruments
        "NIFTYBANK": [],
        "NIFTYIT": [],
        # etc.
    }
    
    SECTOR_MAPPINGS = {
        "BANKING": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK", "AXISBANK"],
        "IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM"],
        "AUTO": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO"],
        # etc.
    }

    def __init__(self, kite_adapter: KiteAdapter):
        self.adapter = kite_adapter
        self._instruments_cache: dict[str, InstrumentInfo] = {}
        self._last_cache_refresh: Optional[datetime] = None
    
    # =========================================================================
    # REAL-TIME DATA
    # =========================================================================
    
    async def get_quotes(self, symbols: list[str]) -> dict[str, Quote]:
        """
        Get real-time quotes for multiple instruments.
        
        Args:
            symbols: List of trading symbols
            
        Returns:
            Dict mapping symbol to Quote
        """
        if not self.adapter.is_connected:
            raise ConnectionError("Kite adapter not connected")
        
        # Convert symbols to instrument tokens
        tokens = [self._get_token(s) for s in symbols]
        
        response = await self.adapter._client.get(
            "/quote",
            params={"i": [f"NSE:{s}" for s in symbols]}
        )
        
        if response.status_code != 200:
            raise Exception(f"Quote API error: {response.status_code}")
        
        data = response.json().get("data", {})
        
        return {
            symbol: Quote(
                symbol=symbol,
                ltp=Decimal(str(d["last_price"])),
                open=Decimal(str(d["ohlc"]["open"])),
                high=Decimal(str(d["ohlc"]["high"])),
                low=Decimal(str(d["ohlc"]["low"])),
                close=Decimal(str(d["ohlc"]["close"])),
                volume=d["volume"],
                change=Decimal(str(d["change"])),
                change_percent=Decimal(str(d.get("change_percent", 0))),
                timestamp=datetime.now()
            )
            for symbol, d in self._parse_quote_response(data, symbols).items()
        }
    
    async def get_market_depth(self, symbol: str) -> dict:
        """Get order book depth showing buy/sell pressure."""
        response = await self.adapter._client.get(
            "/quote",
            params={"i": f"NSE:{symbol}", "depth": True}
        )
        return response.json().get("data", {}).get(f"NSE:{symbol}", {}).get("depth", {})
    
    # =========================================================================
    # HISTORICAL DATA
    # =========================================================================
    
    async def get_historical_ohlcv(
        self,
        symbol: str,
        from_date: date,
        to_date: date,
        interval: str | KiteInterval = KiteInterval.DAY
    ) -> list[OHLCV]:
        """
        Get historical OHLCV data for analysis.
        
        Args:
            symbol: Trading symbol
            from_date: Start date
            to_date: End date
            interval: Candle interval (string or KiteInterval enum)
            
        Returns:
            List of OHLCV candles
        """
        # Convert string to enum if needed
        if isinstance(interval, str):
            try:
                interval = KiteInterval(interval)
            except ValueError:
                raise ValueError(f"Invalid interval: {interval}. Must be one of {[e.value for e in KiteInterval]}")
        
        token = self._get_token(symbol)
        
        response = await self.adapter._client.get(
            f"/instruments/historical/{token}/{interval.value}",
            params={
                "from": from_date.isoformat(),
                "to": to_date.isoformat()
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Historical API error: {response.status_code}")
        
        candles = response.json().get("data", {}).get("candles", [])
        
        return [
            OHLCV(
                timestamp=datetime.fromisoformat(c[0].replace("T", " ").split("+")[0]),
                open=Decimal(str(c[1])),
                high=Decimal(str(c[2])),
                low=Decimal(str(c[3])),
                close=Decimal(str(c[4])),
                volume=c[5]
            )
            for c in candles
        ]
    
    # =========================================================================
    # REFERENCE DATA
    # =========================================================================
    
    async def get_index_constituents(self, index: str) -> list[str]:
        """Get all symbols in a major index."""
        if index not in self.INDEX_CONSTITUENTS:
            raise ValueError(f"Unknown index: {index}")
        return self.INDEX_CONSTITUENTS[index]
    
    async def get_sector_instruments(self, sector: str) -> list[str]:
        """Get all symbols in a sector."""
        sector_upper = sector.upper()
        if sector_upper not in self.SECTOR_MAPPINGS:
            raise ValueError(f"Unknown sector: {sector}")
        return self.SECTOR_MAPPINGS[sector_upper]
    
    async def refresh_instruments_cache(self) -> None:
        """Refresh the instruments master list from Kite."""
        response = await self.adapter._client.get("/instruments")
        if response.status_code == 200:
            # Parse CSV response and populate cache
            self._parse_instruments_csv(response.text)
            self._last_cache_refresh = datetime.now()
    
    # =========================================================================
    # COMPUTED METRICS
    # =========================================================================
    
    async def get_top_movers(
        self,
        universe: str,
        metric: str,
        limit: int = 10,
        direction: str = "top"
    ) -> list[TopMover]:
        """
        Get top/bottom performers by a specific metric.
        
        Args:
            universe: NIFTY50, NIFTYBANK, ALL, or WATCHLIST
            metric: volume, change_percent, range_percent, value_traded
            limit: Number of results
            direction: "top" or "bottom"
            
        Returns:
            List of TopMover results
        """
        # Get universe symbols
        if universe == "ALL":
            symbols = list(self._instruments_cache.keys())[:200]  # Limit for API
        elif universe == "WATCHLIST":
            symbols = await self._get_user_watchlist_symbols()
        else:
            symbols = await self.get_index_constituents(universe)
        
        # Fetch quotes
        quotes = await self.get_quotes(symbols)
        
        # Calculate metric for each
        ranked = []
        for symbol, quote in quotes.items():
            if metric == "volume":
                value = quote.volume
            elif metric == "change_percent":
                value = float(quote.change_percent)
            elif metric == "range_percent":
                value = float((quote.high - quote.low) / quote.open * 100) if quote.open > 0 else 0
            elif metric == "value_traded":
                value = float(quote.ltp) * quote.volume
            else:
                continue
            
            ranked.append((symbol, value, quote.ltp))
        
        # Sort
        ranked.sort(key=lambda x: x[1], reverse=(direction == "top"))
        
        return [
            TopMover(
                symbol=r[0],
                ltp=Decimal(str(r[2])),
                metric_value=r[1],
                metric_name=metric,
                rank=i + 1
            )
            for i, r in enumerate(ranked[:limit])
        ]
    
    async def detect_volume_anomalies(
        self,
        universe: str,
        threshold_multiplier: float = 1.5,
        baseline_days: int = 10,
        time_window: Optional[tuple[time, time]] = None
    ) -> list[VolumeProfile]:
        """
        Find instruments trading at unusual volume.
        
        Args:
            universe: Symbol universe to scan
            threshold_multiplier: Volume must be >= this × average
            baseline_days: Days for baseline calculation
            time_window: Optional intraday window (e.g., 9:15-10:15)
            
        Returns:
            List of instruments with unusual volume
        """
        # Get universe symbols
        if universe == "WATCHLIST":
            symbols = await self._get_user_watchlist_symbols()
        else:
            symbols = await self.get_index_constituents(universe)
        
        anomalies = []
        
        for symbol in symbols:
            try:
                profile = await self._calculate_volume_profile(
                    symbol, baseline_days, time_window
                )
                if profile.volume_ratio >= threshold_multiplier:
                    anomalies.append(profile)
            except Exception:
                continue  # Skip symbols with missing data
        
        # Sort by volume ratio descending
        anomalies.sort(key=lambda x: x.volume_ratio, reverse=True)
        
        return anomalies
    
    async def calculate_technical_levels(
        self,
        symbol: str,
        method: str = "standard_pivot"
    ) -> dict:
        """
        Calculate support, resistance, and pivot levels.
        
        CONSTITUTIONAL NOTE: These are mathematical calculations,
        not predictions. The user interprets their significance.
        
        Args:
            symbol: Trading symbol
            method: Calculation method (standard_pivot, fibonacci, camarilla)
            
        Returns:
            Dict with pivot, support, and resistance levels
        """
        # Get previous day's OHLC
        from_date = date.today() - timedelta(days=7)
        to_date = date.today() - timedelta(days=1)
        
        candles = await self.get_historical_ohlcv(
            symbol, from_date, to_date, KiteInterval.DAY
        )
        
        if not candles:
            raise ValueError(f"No historical data for {symbol}")
        
        prev = candles[-1]  # Previous day
        high, low, close = float(prev.high), float(prev.low), float(prev.close)
        
        if method == "standard_pivot":
            pivot = (high + low + close) / 3
            return {
                "method": "standard_pivot",
                "pivot": round(pivot, 2),
                "r1": round(2 * pivot - low, 2),
                "r2": round(pivot + (high - low), 2),
                "r3": round(high + 2 * (pivot - low), 2),
                "s1": round(2 * pivot - high, 2),
                "s2": round(pivot - (high - low), 2),
                "s3": round(low - 2 * (high - pivot), 2),
            }
        elif method == "fibonacci":
            pivot = (high + low + close) / 3
            range_ = high - low
            return {
                "method": "fibonacci",
                "pivot": round(pivot, 2),
                "r1": round(pivot + 0.382 * range_, 2),
                "r2": round(pivot + 0.618 * range_, 2),
                "r3": round(pivot + 1.0 * range_, 2),
                "s1": round(pivot - 0.382 * range_, 2),
                "s2": round(pivot - 0.618 * range_, 2),
                "s3": round(pivot - 1.0 * range_, 2),
            }
        elif method == "camarilla":
            range_ = high - low
            return {
                "method": "camarilla",
                "r1": round(close + range_ * 1.1 / 12, 2),
                "r2": round(close + range_ * 1.1 / 6, 2),
                "r3": round(close + range_ * 1.1 / 4, 2),
                "r4": round(close + range_ * 1.1 / 2, 2),
                "s1": round(close - range_ * 1.1 / 12, 2),
                "s2": round(close - range_ * 1.1 / 6, 2),
                "s3": round(close - range_ * 1.1 / 4, 2),
                "s4": round(close - range_ * 1.1 / 2, 2),
            }
        else:
            raise ValueError(f"Unknown method: {method}")
    
    async def compare_instruments(
        self,
        symbols: list[str],
        metric: str,
        period_days: int
    ) -> dict:
        """
        Compare multiple instruments across a metric.
        
        Args:
            symbols: List of symbols to compare
            metric: Comparison metric (price_change, volume_change, volatility)
            period_days: Lookback period
            
        Returns:
            Comparison results for all instruments
        """
        from_date = date.today() - timedelta(days=period_days)
        to_date = date.today()
        
        results = {}
        
        for symbol in symbols:
            candles = await self.get_historical_ohlcv(
                symbol, from_date, to_date, KiteInterval.DAY
            )
            
            if len(candles) < 2:
                continue
            
            if metric == "price_change":
                start_price = float(candles[0].close)
                end_price = float(candles[-1].close)
                change = ((end_price - start_price) / start_price) * 100
                results[symbol] = {"change_percent": round(change, 2)}
                
            elif metric == "volume_change":
                first_half = sum(c.volume for c in candles[:len(candles)//2])
                second_half = sum(c.volume for c in candles[len(candles)//2:])
                change = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
                results[symbol] = {"volume_change_percent": round(change, 2)}
                
            elif metric == "volatility":
                returns = []
                for i in range(1, len(candles)):
                    daily_return = (float(candles[i].close) - float(candles[i-1].close)) / float(candles[i-1].close)
                    returns.append(daily_return)
                
                import statistics
                if returns:
                    volatility = statistics.stdev(returns) * 100 * (252 ** 0.5)  # Annualized
                    results[symbol] = {"volatility_percent": round(volatility, 2)}
        
        return {
            "metric": metric,
            "period_days": period_days,
            "instruments": results
        }
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _get_token(self, symbol: str) -> int:
        """Get instrument token for a symbol."""
        if symbol in self._instruments_cache:
            return self._instruments_cache[symbol].instrument_token
        raise ValueError(f"Unknown symbol: {symbol}")
    
    async def _calculate_volume_profile(
        self,
        symbol: str,
        baseline_days: int,
        time_window: Optional[tuple[time, time]]
    ) -> VolumeProfile:
        """Calculate volume profile for an instrument."""
        # Get current quote
        quotes = await self.get_quotes([symbol])
        current_volume = quotes[symbol].volume
        
        # Get historical data
        from_date = date.today() - timedelta(days=baseline_days + 5)
        to_date = date.today() - timedelta(days=1)
        
        candles = await self.get_historical_ohlcv(
            symbol, from_date, to_date, KiteInterval.DAY
        )
        
        if not candles:
            raise ValueError(f"No historical data for {symbol}")
        
        # Calculate average volume
        avg_volume = sum(c.volume for c in candles[-baseline_days:]) / baseline_days
        
        return VolumeProfile(
            symbol=symbol,
            current_volume=current_volume,
            average_volume=avg_volume,
            volume_ratio=current_volume / avg_volume if avg_volume > 0 else 0,
            time_window=time_window or (time(9, 15), time(15, 30)),
            baseline_days=baseline_days
        )
    
    async def _get_user_watchlist_symbols(self) -> list[str]:
        """Get symbols from user's watchlist."""
        # This should integrate with CIA-SIE instruments
        # For now, return empty list
        return []
    
    def _parse_quote_response(self, data: dict, symbols: list[str]) -> dict:
        """Parse Kite quote API response."""
        result = {}
        for symbol in symbols:
            key = f"NSE:{symbol}"
            if key in data:
                result[symbol] = data[key]
        return result
    
    def _parse_instruments_csv(self, csv_text: str) -> None:
        """Parse Kite instruments CSV and populate cache."""
        # Implementation would parse CSV and populate _instruments_cache
        # For now, placeholder
        pass
