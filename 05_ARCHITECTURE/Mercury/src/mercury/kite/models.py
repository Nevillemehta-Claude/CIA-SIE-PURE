"""
Mercury Kite Data Models
========================

Data models for Kite API responses.

CONSTITUTIONAL: MR-001 - These models represent grounded market data.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


def _utc_now() -> datetime:
    """Return current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


@dataclass
class Quote:
    """Current market quote for an instrument."""
    
    symbol: str
    exchange: str
    ltp: float  # Last traded price
    open: float
    high: float
    low: float
    close: float  # Previous close
    volume: int
    change: float  # Absolute change from previous close
    change_percent: float
    timestamp: datetime
    
    # Optional extended data
    bid: Optional[float] = None
    ask: Optional[float] = None
    bid_qty: Optional[int] = None
    ask_qty: Optional[int] = None
    
    def format_summary(self) -> str:
        """Format quote as readable summary."""
        direction = "▲" if self.change >= 0 else "▼"
        sign = "+" if self.change >= 0 else ""
        return (
            f"{self.symbol} ({self.exchange}): ₹{self.ltp:,.2f} "
            f"{direction} {sign}{self.change_percent:.2f}% "
            f"(Vol: {self.volume:,})"
        )


@dataclass
class OHLC:
    """Historical OHLC candle."""
    
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    
    @property
    def change(self) -> float:
        """Intraday change."""
        return self.close - self.open
    
    @property
    def change_percent(self) -> float:
        """Intraday change percentage."""
        if self.open == 0:
            return 0.0
        return ((self.close - self.open) / self.open) * 100


@dataclass
class Position:
    """Open trading position."""
    
    symbol: str
    exchange: str
    product: str  # MIS, CNC, NRML
    quantity: int
    average_price: float
    ltp: float
    pnl: float
    pnl_percent: float
    
    # Optional
    buy_quantity: int = 0
    sell_quantity: int = 0
    buy_value: float = 0.0
    sell_value: float = 0.0
    
    @property
    def is_long(self) -> bool:
        """Is this a long position?"""
        return self.quantity > 0
    
    @property
    def is_profitable(self) -> bool:
        """Is position in profit?"""
        return self.pnl > 0
    
    def format_summary(self) -> str:
        """Format position as readable summary."""
        direction = "LONG" if self.is_long else "SHORT"
        pnl_sign = "+" if self.pnl >= 0 else ""
        return (
            f"{self.symbol}: {direction} {abs(self.quantity)} @ ₹{self.average_price:.2f} | "
            f"LTP: ₹{self.ltp:.2f} | P&L: {pnl_sign}₹{self.pnl:,.2f} ({pnl_sign}{self.pnl_percent:.2f}%)"
        )


@dataclass
class Holding:
    """Delivery holding (CNC positions)."""
    
    symbol: str
    exchange: str
    quantity: int
    average_price: float
    ltp: float
    pnl: float
    pnl_percent: float
    
    # Optional
    isin: str = ""
    collateral_quantity: int = 0
    t1_quantity: int = 0
    
    @property
    def current_value(self) -> float:
        """Current market value of holding."""
        return self.quantity * self.ltp
    
    @property
    def invested_value(self) -> float:
        """Original invested value."""
        return self.quantity * self.average_price
    
    def format_summary(self) -> str:
        """Format holding as readable summary."""
        pnl_sign = "+" if self.pnl >= 0 else ""
        return (
            f"{self.symbol}: {self.quantity} units @ ₹{self.average_price:.2f} | "
            f"LTP: ₹{self.ltp:.2f} | P&L: {pnl_sign}₹{self.pnl:,.2f} ({pnl_sign}{self.pnl_percent:.2f}%)"
        )


@dataclass
class Instrument:
    """Tradeable instrument from master list."""
    
    instrument_token: int
    exchange_token: int
    symbol: str
    name: str
    exchange: str
    segment: str
    instrument_type: str
    
    # Optional
    lot_size: int = 1
    tick_size: float = 0.05
    expiry: Optional[datetime] = None
    strike: Optional[float] = None
    
    @property
    def tradingsymbol(self) -> str:
        """Full trading symbol with exchange."""
        return f"{self.exchange}:{self.symbol}"


@dataclass
class MarketDataBundle:
    """Bundle of market data for AI context."""
    
    quotes: dict[str, Quote] = field(default_factory=dict)
    positions: list[Position] = field(default_factory=list)
    holdings: list[Holding] = field(default_factory=list)
    historical: dict[str, list[OHLC]] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=_utc_now)
    
    def to_context_dict(self) -> dict:
        """Convert to dictionary for AI context."""
        context = {
            "timestamp": self.timestamp.isoformat(),
            "quotes": {},
            "positions": [],
            "holdings": [],
            "historical": {},
        }
        
        for symbol, quote in self.quotes.items():
            context["quotes"][symbol] = {
                "ltp": quote.ltp,
                "change": quote.change,
                "change_percent": quote.change_percent,
                "volume": quote.volume,
                "high": quote.high,
                "low": quote.low,
            }
        
        for pos in self.positions:
            context["positions"].append({
                "symbol": pos.symbol,
                "quantity": pos.quantity,
                "avg_price": pos.average_price,
                "ltp": pos.ltp,
                "pnl": pos.pnl,
                "pnl_percent": pos.pnl_percent,
            })
        
        for hold in self.holdings:
            context["holdings"].append({
                "symbol": hold.symbol,
                "quantity": hold.quantity,
                "avg_price": hold.average_price,
                "ltp": hold.ltp,
                "pnl": hold.pnl,
                "pnl_percent": hold.pnl_percent,
            })
        
        for symbol, candles in self.historical.items():
            context["historical"][symbol] = [
                {
                    "date": c.date.isoformat(),
                    "open": c.open,
                    "high": c.high,
                    "low": c.low,
                    "close": c.close,
                    "volume": c.volume,
                }
                for c in candles[-10:]  # Last 10 candles
            ]
        
        return context
