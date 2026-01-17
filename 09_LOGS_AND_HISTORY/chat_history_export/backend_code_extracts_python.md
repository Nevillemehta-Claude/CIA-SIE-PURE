# Backend Python code extracts from chat chronicle

Source: `chat_history_export/CIA_SIE_COMPLETE_CHAT_CHRONICLE.html`

Python backend code blocks extracted: 38

## Block 1

```python
Example verification:
  File: src/cia_sie/api/routes/webhooks.py
  Import: from cia_sie.ingestion.webhook_handler import WebhookHandler
  
  Check: Does cia_sie/ingestion/webhook_handler.py exist?
  Check: Does it export WebhookHandler class?
  Check: Does WebhookHandler have process_webhook method?
```

## Block 2

```python
49:68:src/cia_sie/core/enums.py
class FreshnessStatus(str, Enum):
    """
    Data freshness classification.
    // ...
    NOTE: Freshness is purely DESCRIPTIVE - it does NOT invalidate
    or suppress data. All data is displayed regardless of freshness.
    (Section 0C - Automation Boundaries)
    """
```

## Block 3

```python
118:128:src/cia_sie/dal/models.py
class ChartDB(Base):
    """
    Charts Table.
    // ...
    CRITICAL: NO WEIGHT COLUMN
    Per ADR-003: Weights enable aggregation which is PROHIBITED.
    All charts have equal standing.
    """
    // ... fields ...
    # NOTE: Deliberately NO weight column - prohibited by Section 0B
```

## Block 4

```python
163:173:src/cia_sie/dal/models.py
class SignalDB(Base):
    """
    Signals Table.
    // ...
    CRITICAL: NO CONFIDENCE COLUMN
    Per ADR-003: Scores imply system judgment which is PROHIBITED.
    Raw direction and indicators preserved.
    """
    // ... fields ...
    # NOTE: Deliberately NO confidence or strength column - prohibited by Section 0B
```

## Block 5

```python
99:128:src/cia_sie/core/models.py
class Chart(CIASIEBaseModel):
    """
    CRITICAL: NO WEIGHT ATTRIBUTE
    Per ADR-003: Weights enable aggregation which is PROHIBITED.
    All charts have equal standing. User determines importance through interpretation.
    """
    // ... fields (NO weight, priority, or importance)
    # NOTE: Deliberately NO weight field - prohibited by Section 0B

class Signal(CIASIEBaseModel):
    """
    CRITICAL: NO CONFIDENCE/STRENGTH SCORES
    Per ADR-003: Scores imply system judgment which is PROHIBITED.
    Raw direction and indicators preserved. User interprets significance.
    """
    // ... fields (NO confidence, score, or strength)
    # NOTE: Deliberately NO confidence or strength field - prohibited by Section 0B
```

## Block 6

```python
109:124:src/cia_sie/core/enums.py
class ValidationStatus(str, Enum):
    """
    Status of AI response validation.

    Per Gold Standard Specification Section 14.4:
    All AI responses must be validated for constitutional compliance.

    - VALID: Response passed all validation checks
    - INVALID: Response contains prohibited content
    - REMEDIATED: Response was modified to achieve compliance
    """

    VALID = "VALID"
    INVALID = "INVALID"
    REMEDIATED = "REMEDIATED"
```

## Block 7

```python
438-461:src/cia_sie/ai/response_validator.py
    def _add_stricter_constraints(
        self,
        system_prompt: str,
        violations: list[str],
    ) -> str:
        """Add additional constraints based on specific violations."""
        additions = [
            "",
            "CRITICAL REMINDER - Previous response was REJECTED for these violations:",
        ]
        for v in violations:
            additions.append(f"  - {v}")
        additions.extend([
            "",
            "You MUST avoid these specific issues in your next response.",
            "Be EXTREMELY careful to use only DESCRIPTIVE language.",
            "Do NOT use any form of recommendation, suggestion, or advice.",
        ])
        return system_prompt + "\n".join(additions)
```

## Block 8

```python
python
# src/cia_sie/platforms/kite_intelligence.py

class KiteIntelligenceEngine:
    """
    Market intelligence layer that Claude can query via tool use.
    
    This is NOT a trading engine. It's a semantic query interface
    to market data that Claude orchestrates.
    """
    
    # REFERENCE DATA (cached, not real-time)
    async def get_index_constituents(self, index: str) -> list[Instrument]:
        """Get all instruments in NIFTY50, BANKNIFTY, etc."""
        
    async def get_sector_instruments(self, sector: str) -> list[Instrument]:
        """Get instruments by sector: IT, BANKING, AUTO, PHARMA, etc."""
    
    # REAL-TIME QUERIES
    async def get_quotes(self, symbols: list[str]) -> dict[str, Quote]:
        """Get current LTP, volume, OHLC for multiple instruments"""
    
    async def get_market_depth(self, symbol: str) -> MarketDepth:
        """Get order book depth (buy/sell pressure)"""
    
    # HISTORICAL ANALYSIS
    async def get_historical_ohlcv(
        self, 
        symbol: str, 
        from_date: date, 
        to_date: date,
        interval: str  # minute, 5minute, day, etc.
    ) -> list[OHLCV]:
        """Get historical candles for analysis"""
    
    async def calculate_volume_profile(
        self,
        symbol: str,
        lookback_days: int,
        time_window: tuple[time, time]  # e.g., (9:15, 10:15)
    ) -> VolumeProfile:
        """Calculate average volume for specific time windows"""
    
    # COMPUTED METRICS (Claude can request these)
    async def detect_volume_anomalies(
        self,
        symbols: list[str],
        threshold_multiplier: float = 1.5,
        baseline_days: int = 10
    ) -> list[VolumeAnomaly]:
        """Find instruments trading above normal volume"""
    
    async def get_top_movers(
        self,
        universe: str,  # NIFTY50, BANKNIFTY, ALL
        metric: str,    # volume, change_percent, range_percent
        limit: int = 10,
        direction: str = "top"  # top or bottom
    ) -> list[Mover]:
        """Get top/bottom performers by metric"""
    
    async def compare_instruments(
        self,
        symbols: list[str],
        metric: str,
        period_days: int
    ) -> ComparisonResult:
        """Compare multiple instruments over a period"""
```

## Block 9

```python
python
# src/cia_sie/ai/kite_tools.py

KITE_TOOLS = [
    {
        "name": "get_quote",
        "description": "Get current market quote including last price, volume, OHLC, change percentage for one or more instruments",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of trading symbols (e.g., ['RELIANCE', 'TCS', 'HDFCBANK'])"
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["ltp", "volume", "ohlc", "change", "all"]},
                    "description": "Which data fields to return"
                }
            },
            "required": ["symbols"]
        }
    },
    {
        "name": "get_index_constituents",
        "description": "Get all instruments that are part of a major index",
        "input_schema": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "string",
                    "enum": ["NIFTY50", "NIFTY100", "NIFTYBANK", "NIFTYIT", "NIFTYPHARMA", "NIFTYAUTO"],
                    "description": "Index name"
                }
            },
            "required": ["index"]
        }
    },
    {
        "name": "get_top_movers",
        "description": "Get the top or bottom performing instruments by a specific metric within a universe",
        "input_schema": {
            "type": "object",
            "properties": {
                "universe": {
                    "type": "string",
                    "enum": ["NIFTY50", "NIFTY100", "NIFTYBANK", "ALL"],
                    "description": "Which universe to scan"
                },
                "metric": {
                    "type": "string",
                    "enum": ["volume", "change_percent", "range_percent", "value_traded"],
                    "description": "Metric to rank by"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 50,
                    "description": "Number of results to return"
                },
                "direction": {
                    "type": "string",
                    "enum": ["top", "bottom"],
                    "description": "Top performers or bottom performers"
                }
            },
            "required": ["universe", "metric"]
        }
    },
    {
        "name": "detect_volume_anomalies",
        "description": "Find instruments trading at unusual volume compared to their historical average",
        "input_schema": {
            "type": "object",
            "properties": {
                "universe": {"type": "string", "enum": ["NIFTY50", "NIFTY100", "WATCHLIST", "ALL"]},
                "threshold_multiplier": {
                    "type": "number",
                    "minimum": 1.0,
                    "maximum": 10.0,
                    "description": "Volume must be this many times the average to qualify (e.g., 1.5 = 50% above average)"
                },
                "baseline_days": {
                    "type": "integer",
                    "minimum": 5,
                    "maximum": 30,
                    "description": "Number of days to calculate baseline from"
                },
                "time_window": {
                    "type": "string",
                    "description": "Optional time window like '09:15-10:15' for intraday analysis"
                }
            },
            "required": ["universe"]
        }
    },
    {
        "name": "get_historical_data",
        "description": "Get historical OHLCV candles for technical analysis",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "from_date": {"type": "string", "format": "date"},
                "to_date": {"type": "string", "format": "date"},
                "interval": {
                    "type": "string",
                    "enum": ["minute", "5minute", "15minute", "30minute", "60minute", "day"]
                }
            },
            "required": ["symbol", "from_date", "to_date", "interval"]
        }
    },
    {
        "name": "compare_instruments",
        "description": "Compare multiple instruments across a metric over a time period",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}},
                "metric": {"type": "string", "enum": ["price_change", "volume_change", "volatility", "relative_strength"]},
                "period_days": {"type": "integer", "minimum": 1, "maximum": 365}
            },
            "required": ["symbols", "metric", "period_days"]
        }
    },
    {
        "name": "get_user_watchlist",
        "description": "Get instruments from the user's CIA-SIE watchlist or Kite watchlist",
        "input_schema": {
            "type": "object",
            "properties": {
                "watchlist_name": {"type": "string", "description": "Optional specific watchlist name"}
            }
        }
    },
    {
        "name": "calculate_technical_levels",
        "description": "Calculate support, resistance, and pivot levels for an instrument",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "method": {"type": "string", "enum": ["standard_pivot", "fibonacci", "camarilla"]}
            },
            "required": ["symbol"]
        }
    }
]
```

## Block 10

```python
python
# src/cia_sie/ai/market_agent.py

class MarketIntelligenceAgent:
    """
    Agentic layer that orchestrates Claude + Kite for natural language queries.
    
    This agent:
    1. Receives natural language query
    2. Uses Claude with tools to plan and execute
    3. Iteratively calls Kite APIs as needed
    4. Synthesizes results into descriptive response
    
    CONSTITUTIONAL CONSTRAINTS:
    - All outputs are DESCRIPTIVE only
    - No recommendations, predictions, or confidence scores
    - User context is injected but not stored beyond session
    """
    
    def __init__(
        self,
        claude_client: ClaudeClient,
        kite_engine: KiteIntelligenceEngine,
        user_context: Optional[UserContext] = None,
    ):
        self.claude = claude_client
        self.kite = kite_engine
        self.user_context = user_context
        self.tools = KITE_TOOLS
        self.execution_log = []  # Audit trail
    
    async def query(self, user_message: str) -> AgentResponse:
        """
        Process a natural language market query.
        
        Examples:
        - "What are the top 5 most traded stocks in Nifty 50 right now?"
        - "Show me banking stocks with unusual volume today"
        - "Compare HDFC vs ICICI performance this month"
        - "Which stocks in my watchlist are near 52-week highs?"
        """
        
        # Build system prompt with context
        system_prompt = self._build_system_prompt()
        
        # Initial Claude call with tools
        response = await self.claude.client.messages.create(
            model=self.claude.model,
            max_tokens=4000,
            system=system_prompt,
            tools=self.tools,
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Agentic loop: handle tool calls
        messages = [{"role": "user", "content": user_message}]
        
        while response.stop_reason == "tool_use":
            # Extract tool calls from response
            tool_calls = [block for block in response.content if block.type == "tool_use"]
            
            # Execute each tool call
            tool_results = []
            for tool_call in tool_calls:
                result = await self._execute_tool(tool_call.name, tool_call.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": json.dumps(result)
                })
                
                # Audit log
                self.execution_log.append({
                    "tool": tool_call.name,
                    "input": tool_call.input,
                    "result_summary": self._summarize_result(result),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Continue conversation with tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            
            response = await self.claude.client.messages.create(
                model=self.claude.model,
                max_tokens=4000,
                system=system_prompt,
                tools=self.tools,
                messages=messages
            )
        
        # Extract final text response
        final_text = self._extract_text(response.content)
        
        # Validate constitutional compliance
        validated_text = self._ensure_compliance(final_text)
        
        return AgentResponse(
            response=validated_text,
            tools_used=[log["tool"] for log in self.execution_log],
            execution_log=self.execution_log,
            disclaimer=MANDATORY_DISCLAIMER
        )
    
    async def _execute_tool(self, tool_name: str, tool_input: dict) -> Any:
        """Execute a tool call against Kite engine."""
        
        tool_handlers = {
            "get_quote": self.kite.get_quotes,
            "get_index_constituents": self.kite.get_index_constituents,
            "get_top_movers": self.kite.get_top_movers,
            "detect_volume_anomalies": self.kite.detect_volume_anomalies,
            "get_historical_data": self.kite.get_historical_ohlcv,
            "compare_instruments": self.kite.compare_instruments,
            "get_user_watchlist": self._get_watchlist,
            "calculate_technical_levels": self.kite.calculate_technical_levels,
        }
        
        handler = tool_handlers.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return await handler(**tool_input)
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with user context."""
        
        base = """You are a market data assistant for CIA-SIE.

You have access to tools that query the Kite (Zerodha) API for market data.

CRITICAL RULES:
1. You DESCRIBE market data. You NEVER recommend actions.
2. You present data factually without predictions or confidence scores.
3. When asked about multiple instruments, present each with equal weight.
4. Always explain what the data shows, not what the user should do.
5. Every response must end with: "This is market data for your review. The interpretation and any decision is entirely yours."

You may use tools in sequence to answer complex queries. Plan your approach before executing.

PROHIBITED:
- "You should buy/sell..."
- "This looks like a good entry..."
- "I recommend..."
- "The trend suggests..."
- Probability or confidence percentages
- Signal strength ratings
- Predictions about future price movement
"""

        if self.user_context:
            base += f"""

USER CONTEXT:
- Watchlist: {', '.join(self.user_context.watchlist)}
- Preferred sectors: {', '.join(self.user_context.preferred_sectors)}
- Focus indices: {', '.join(self.user_context.focus_indices)}
"""

        return base
```

## Block 11

```python
python
# src/cia_sie/dal/models.py (additions)

class SavedQueryDB(Base):
    """
    Saved market intelligence queries.
    
    Users can save complex multi-step queries as named operations.
    Example: "My momentum scan" → volume anomaly + sector strength + breakout detection
    """
    
    __tablename__ = "saved_queries"
    
    query_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    query_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # The natural language query template
    query_template: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Variables that can be substituted
    # e.g., {"universe": "NIFTY50", "threshold": 1.5}
    default_parameters: Mapped[str] = mapped_column(JSON, nullable=False, default="{}")
    
    # Execution history (for learning common patterns)
    last_executed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    execution_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
```

## Block 12

```python
python
# src/cia_sie/platforms/kite_intelligence.py

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Optional

import httpx

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
    INDEX_CONSTITUENTS = {
        "NIFTY50": [...],  # Load from Kite instruments
        "NIFTYBANK": [...],
        "NIFTYIT": [...],
        # etc.
    }
    
    SECTOR_MAPPINGS = {
        "BANKING": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK", "AXISBANK", ...],
        "IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM", ...],
        "AUTO": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", ...],
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
        interval: KiteInterval = KiteInterval.DAY
    ) -> list[OHLCV]:
        """
        Get historical OHLCV data for analysis.
        
        Args:
            symbol: Trading symbol
            from_date: Start date
            to_date: End date
            interval: Candle interval
            
        Returns:
            List of OHLCV candles
        """
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
```

## Block 13

```python
python
# src/cia_sie/ai/market_intelligence_agent.py

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from anthropic import AsyncAnthropic

from cia_sie.ai.response_validator import ensure_disclaimer, validate_ai_response
from cia_sie.dal.repositories import InstrumentRepository, SignalRepository
from cia_sie.exposure.relationship_exposer import RelationshipExposer
from cia_sie.platforms.kite_intelligence import KiteIntelligenceEngine

logger = logging.getLogger(__name__)


@dataclass
class ExecutionLogEntry:
    """Audit trail entry for tool execution."""
    tool_name: str
    tool_input: dict
    result_summary: str
    execution_time_ms: int
    timestamp: str


@dataclass
class AgentResponse:
    """Response from the market intelligence agent."""
    response: str
    tools_used: list[str]
    execution_log: list[ExecutionLogEntry]
    data_sources: list[str]  # e.g., ["kite_quotes", "cia_sie_signals"]
    disclaimer: str


# Tool definitions for Claude
MARKET_INTELLIGENCE_TOOLS = [
    {
        "name": "get_quote",
        "description": "Get current market quotes including last price, volume, OHLC, and change percentage for one or more instruments. Use this when the user asks about current prices, how something is trading, or what's happening with a stock right now.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of trading symbols (e.g., ['RELIANCE', 'TCS', 'HDFCBANK'])"
                }
            },
            "required": ["symbols"]
        }
    },
    {
        "name": "get_top_movers",
        "description": "Get the top or bottom performing instruments by a specific metric. Use this when the user asks about gainers, losers, most active, highest volume, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "universe": {
                    "type": "string",
                    "enum": ["NIFTY50", "NIFTY100", "NIFTYBANK", "NIFTYIT", "WATCHLIST"],
                    "description": "Which universe of stocks to scan"
                },
                "metric": {
                    "type": "string",
                    "enum": ["volume", "change_percent", "range_percent", "value_traded"],
                    "description": "Metric to rank by: volume (trading volume), change_percent (price change %), range_percent (day's range %), value_traded (volume × price)"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 20,
                    "default": 5,
                    "description": "Number of results to return"
                },
                "direction": {
                    "type": "string",
                    "enum": ["top", "bottom"],
                    "default": "top",
                    "description": "Top performers or bottom performers"
                }
            },
            "required": ["universe", "metric"]
        }
    },
    {
        "name": "detect_volume_anomalies",
        "description": "Find instruments trading at unusual volume compared to their historical average. Use this when the user asks about unusual activity, volume spikes, or abnormal trading.",
        "input_schema": {
            "type": "object",
            "properties": {
                "universe": {
                    "type": "string",
                    "enum": ["NIFTY50", "NIFTY100", "NIFTYBANK", "NIFTYIT", "WATCHLIST"],
                    "description": "Universe to scan for volume anomalies"
                },
                "threshold_multiplier": {
                    "type": "number",
                    "minimum": 1.0,
                    "maximum": 5.0,
                    "default": 1.5,
                    "description": "Volume must be at least this many times the average (1.5 = 50% above average)"
                },
                "baseline_days": {
                    "type": "integer",
                    "minimum": 5,
                    "maximum": 30,
                    "default": 10,
                    "description": "Number of days to calculate baseline average from"
                }
            },
            "required": ["universe"]
        }
    },
    {
        "name": "get_historical_data",
        "description": "Get historical OHLCV (open, high, low, close, volume) candles for an instrument. Use this for historical analysis, trend identification, or when comparing current levels to past data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Trading symbol"},
                "from_date": {"type": "string", "format": "date", "description": "Start date (YYYY-MM-DD)"},
                "to_date": {"type": "string", "format": "date", "description": "End date (YYYY-MM-DD)"},
                "interval": {
                    "type": "string",
                    "enum": ["minute", "5minute", "15minute", "60minute", "day"],
                    "default": "day",
                    "description": "Candle interval"
                }
            },
            "required": ["symbol", "from_date", "to_date"]
        }
    },
    {
        "name": "compare_instruments",
        "description": "Compare multiple instruments across a specific metric over a time period. Use this when the user wants to compare stocks or analyze relative performance.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of symbols to compare"
                },
                "metric": {
                    "type": "string",
                    "enum": ["price_change", "volume_change", "volatility"],
                    "description": "Comparison metric"
                },
                "period_days": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 365,
                    "default": 30,
                    "description": "Lookback period in days"
                }
            },
            "required": ["symbols", "metric"]
        }
    },
    {
        "name": "calculate_technical_levels",
        "description": "Calculate pivot points, support, and resistance levels for an instrument. These are mathematical calculations based on previous day's price action.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Trading symbol"},
                "method": {
                    "type": "string",
                    "enum": ["standard_pivot", "fibonacci", "camarilla"],
                    "default": "standard_pivot",
                    "description": "Calculation method"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_index_constituents",
        "description": "Get all instruments that are part of a major index. Use this to understand what stocks make up an index.",
        "input_schema": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "string",
                    "enum": ["NIFTY50", "NIFTY100", "NIFTYBANK", "NIFTYIT", "NIFTYPHARMA", "NIFTYAUTO"],
                    "description": "Index name"
                }
            },
            "required": ["index"]
        }
    },
    {
        "name": "get_sector_instruments",
        "description": "Get all instruments in a specific sector. Use this when the user asks about a particular sector.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sector": {
                    "type": "string",
                    "enum": ["BANKING", "IT", "AUTO", "PHARMA", "FMCG", "METALS", "ENERGY", "REALTY"],
                    "description": "Sector name"
                }
            },
            "required": ["sector"]
        }
    },
    {
        "name": "get_cia_sie_signals",
        "description": "Get current signal state from CIA-SIE TradingView charts for an instrument. This returns signals from the user's configured TradingView charts including direction (BULLISH/BEARISH/NEUTRAL), freshness, and any contradictions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Instrument symbol to get signals for"
                },
                "include_contradictions": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to include contradiction details"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_user_watchlist",
        "description": "Get the user's watchlist with current data. Use this when the user refers to 'my stocks', 'my watchlist', or their tracked instruments.",
        "input_schema": {
            "type": "object",
            "properties": {
                "include_quotes": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to include current market quotes"
                },
                "include_signals": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to include CIA-SIE signals if available"
                }
            }
        }
    }
]


SYSTEM_PROMPT = """You are a market data assistant for CIA-SIE (Chart Intelligence Auditor & Signal Intelligence Engine).

You have access to:
1. Real-time market data from Kite (Zerodha) API
2. Signal data from the user's TradingView charts via CIA-SIE

CONSTITUTIONAL RULES - YOU MUST FOLLOW THESE:

1. You DESCRIBE market data and signals. You NEVER recommend actions.
   ✓ "RELIANCE is up 2.3% with volume at 1.5x average"
   ✗ "You should buy RELIANCE" or "This looks like a good entry"

2. You present all data with EQUAL WEIGHT. Do not emphasize one signal or metric over another.
   ✓ "Chart 01A shows BULLISH, Chart 02 shows BEARISH"
   ✗ "The stronger signal from Chart 01A suggests..."

3. You EXPOSE contradictions, you NEVER resolve them.
   ✓ "There is a contradiction: daily chart is bullish, weekly chart is bearish"
   ✗ "Despite the bearish weekly signal, the daily is more relevant"

4. You NEVER provide:
   - Predictions about future price movement
   - Probability or confidence percentages
   - Signal strength ratings
   - Recommendations to buy, sell, hold, enter, or exit

5. Every response MUST end with:
   "This is market data for your review. The interpretation and any decision is entirely yours."

You may use multiple tools in sequence to answer complex queries. Think step by step about which data you need, then gather it systematically.

When presenting data:
- Use clear, organized formatting
- Include relevant numbers (prices, volumes, percentages)
- Note data freshness where relevant
- Present contradictory information side by side, not hierarchically
"""


class MarketIntelligenceAgent:
    """
    Agentic AI layer that orchestrates Claude + Kite + CIA-SIE.
    
    This agent:
    1. Receives natural language queries
    2. Uses Claude with tool definitions to plan and execute
    3. Calls Kite API and CIA-SIE data as needed
    4. Synthesizes results into constitutional-compliant responses
    5. Maintains full audit trail of all tool calls
    """
    
    MANDATORY_DISCLAIMER = (
        "This is market data for your review. "
        "The interpretation and any decision is entirely yours."
    )
    
    def __init__(
        self,
        anthropic_client: AsyncAnthropic,
        kite_engine: KiteIntelligenceEngine,
        relationship_exposer: RelationshipExposer,
        instrument_repository: InstrumentRepository,
        model: str = "claude-sonnet-4-20250514",
    ):
        self.client = anthropic_client
        self.kite = kite_engine
        self.exposer = relationship_exposer
        self.instruments = instrument_repository
        self.model = model
        
        self.execution_log: list[ExecutionLogEntry] = []
        self.data_sources_used: set[str] = set()
    
    async def query(
        self,
        user_message: str,
        user_context: Optional[dict] = None,
        max_iterations: int = 10,
    ) -> AgentResponse:
        """
        Process a natural language market query.
        
        Args:
            user_message: The user's question in natural language
            user_context: Optional context (watchlist, preferences)
            max_iterations: Maximum tool call iterations
            
        Returns:
            AgentResponse with synthesized answer and audit trail
        """
        self.execution_log = []
        self.data_sources_used = set()
        
        # Build system prompt with optional user context
        system = self._build_system_prompt(user_context)
        
        # Initial message
        messages = [{"role": "user", "content": user_message}]
        
        # Agentic loop
        for iteration in range(max_iterations):
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system,
                tools=MARKET_INTELLIGENCE_TOOLS,
                messages=messages
            )
            
            # Check if we're done
            if response.stop_reason == "end_turn":
                break
            
            # Handle tool calls
            if response.stop_reason == "tool_use":
                # Add assistant's response to message history
                messages.append({"role": "assistant", "content": response.content})
                
                # Execute tool calls and collect results
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = await self._execute_tool(
                            block.name,
                            block.input
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, default=str)
                        })
                
                # Add tool results to messages
                messages.append({"role": "user", "content": tool_results})
        
        # Extract final text response
        final_text = self._extract_text(response.content)
        
        # Validate constitutional compliance
        validation = validate_ai_response(final_text)
        if not validation.is_valid:
            logger.warning(f"Response validation issues: {validation.violations}")
            final_text = ensure_disclaimer(final_text)
        
        # Ensure disclaimer is present
        if self.MANDATORY_DISCLAIMER not in final_text:
            final_text = f"{final_text}\n\n{self.MANDATORY_DISCLAIMER}"
        
        return AgentResponse(
            response=final_text,
            tools_used=[log.tool_name for log in self.execution_log],
            execution_log=self.execution_log,
            data_sources=list(self.data_sources_used),
            disclaimer=self.MANDATORY_DISCLAIMER
        )
    
    async def _execute_tool(self, tool_name: str, tool_input: dict) -> Any:
        """Execute a tool call and log it."""
        start_time = datetime.now()
        
        try:
            if tool_name == "get_quote":
                self.data_sources_used.add("kite_quotes")
                result = await self.kite.get_quotes(tool_input["symbols"])
                result = {k: self._quote_to_dict(v) for k, v in result.items()}
                
            elif tool_name == "get_top_movers":
                self.data_sources_used.add("kite_quotes")
                movers = await self.kite.get_top_movers(
                    universe=tool_input["universe"],
                    metric=tool_input["metric"],
                    limit=tool_input.get("limit", 5),
                    direction=tool_input.get("direction", "top")
                )
                result = [self._mover_to_dict(m) for m in movers]
                
            elif tool_name == "detect_volume_anomalies":
                self.data_sources_used.add("kite_historical")
                anomalies = await self.kite.detect_volume_anomalies(
                    universe=tool_input["universe"],
                    threshold_multiplier=tool_input.get("threshold_multiplier", 1.5),
                    baseline_days=tool_input.get("baseline_days", 10)
                )
                result = [self._volume_profile_to_dict(v) for v in anomalies]
                
            elif tool_name == "get_historical_data":
                self.data_sources_used.add("kite_historical")
                from datetime import date
                candles = await self.kite.get_historical_ohlcv(
                    symbol=tool_input["symbol"],
                    from_date=date.fromisoformat(tool_input["from_date"]),
                    to_date=date.fromisoformat(tool_input["to_date"]),
                    interval=tool_input.get("interval", "day")
                )
                result = [self._ohlcv_to_dict(c) for c in candles]
                
            elif tool_name == "compare_instruments":
                self.data_sources_used.add("kite_historical")
                result = await self.kite.compare_instruments(
                    symbols=tool_input["symbols"],
                    metric=tool_input["metric"],
                    period_days=tool_input.get("period_days", 30)
                )
                
            elif tool_name == "calculate_technical_levels":
                self.data_sources_used.add("kite_historical")
                result = await self.kite.calculate_technical_levels(
                    symbol=tool_input["symbol"],
                    method=tool_input.get("method", "standard_pivot")
                )
                
            elif tool_name == "get_index_constituents":
                result = await self.kite.get_index_constituents(tool_input["index"])
                
            elif tool_name == "get_sector_instruments":
                result = await self.kite.get_sector_instruments(tool_input["sector"])
                
            elif tool_name == "get_cia_sie_signals":
                self.data_sources_used.add("cia_sie_signals")
                result = await self._get_signals_for_symbol(
                    tool_input["symbol"],
                    tool_input.get("include_contradictions", True)
                )
                
            elif tool_name == "get_user_watchlist":
                result = await self._get_user_watchlist(
                    include_quotes=tool_input.get("include_quotes", True),
                    include_signals=tool_input.get("include_signals", True)
                )
                
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
        
        except Exception as e:
            logger.error(f"Tool execution error: {tool_name} - {e}")
            result = {"error": str(e)}
        
        # Log execution
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        self.execution_log.append(ExecutionLogEntry(
            tool_name=tool_name,
            tool_input=tool_input,
            result_summary=self._summarize_result(result),
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now().isoformat()
        ))
        
        return result
    
    async def _get_signals_for_symbol(
        self,
        symbol: str,
        include_contradictions: bool
    ) -> dict:
        """Get CIA-SIE signals for an instrument."""
        # Find instrument by symbol
        instrument = await self.instruments.get_by_symbol(symbol)
        if not instrument:
            return {"error": f"Instrument {symbol} not found in CIA-SIE"}
        
        # Get relationship summary
        summaries = await self.exposer.expose_for_instrument(instrument.instrument_id)
        
        if not summaries:
            return {"symbol": symbol, "signals": [], "message": "No silos configured"}
        
        result = {
            "symbol": symbol,
            "silos": []
        }
        
        for summary in summaries:
            silo_data = {
                "silo_name": summary.silo_name,
                "charts": []
            }
            
            for chart in summary.charts:
                chart_data = {
                    "chart_code": chart.chart_code,
                    "chart_name": chart.chart_name,
                    "timeframe": chart.timeframe,
                    "freshness": chart.freshness,
                    "direction": chart.latest_signal.direction if chart.latest_signal else "NO_SIGNAL",
                    "signal_type": chart.latest_signal.signal_type if chart.latest_signal else None,
                    "indicators": chart.latest_signal.indicators if chart.latest_signal else {}
                }
                silo_data["charts"].append(chart_data)
            
            if include_contradictions and summary.contradictions:
                silo_data["contradictions"] = [
                    {
                        "chart_a": c.chart_a_name,
                        "direction_a": c.chart_a_direction,
                        "chart_b": c.chart_b_name,
                        "direction_b": c.chart_b_direction
                    }
                    for c in summary.contradictions
                ]
            
            if summary.confirmations:
                silo_data["confirmations"] = [
                    {
                        "chart_a": c.chart_a_name,
                        "chart_b": c.chart_b_name,
                        "direction": c.aligned_direction
                    }
                    for c in summary.confirmations
                ]
            
            result["silos"].append(silo_data)
        
        return result
    
    async def _get_user_watchlist(
        self,
        include_quotes: bool,
        include_signals: bool
    ) -> dict:
        """Get user's watchlist with optional enrichment."""
        # Get all active instruments
        instruments = await self.instruments.get_all_active()
        
        watchlist = {
            "instruments": [],
            "count": len(instruments)
        }
        
        symbols = [i.symbol for i in instruments]
        
        # Get quotes if requested
        quotes = {}
        if include_quotes and symbols:
            try:
                quotes = await self.kite.get_quotes(symbols)
                self.data_sources_used.add("kite_quotes")
            except Exception as e:
                logger.warning(f"Failed to get quotes for watchlist: {e}")
        
        for instrument in instruments:
            item = {
                "symbol": instrument.symbol,
                "display_name": instrument.display_name
            }
            
            if include_quotes and instrument.symbol in quotes:
                q = quotes[instrument.symbol]
                item["quote"] = {
                    "ltp": float(q.ltp),
                    "change_percent": float(q.change_percent),
                    "volume": q.volume
                }
            
            if include_signals:
                try:
                    signals = await self._get_signals_for_symbol(
                        instrument.symbol,
                        include_contradictions=False
                    )
                    item["signals"] = signals.get("silos", [])
                    self.data_sources_used.add("cia_sie_signals")
                except Exception:
                    pass
            
            watchlist["instruments"].append(item)
        
        return watchlist
    
    def _build_system_prompt(self, user_context: Optional[dict]) -> str:
        """Build system prompt with optional user context."""
        prompt = SYSTEM_PROMPT
        
        if user_context:
            context_parts = []
            
            if user_context.get("watchlist"):
                context_parts.append(f"User's watchlist: {', '.join(user_context['watchlist'])}")
            
            if user_context.get("preferred_sectors"):
                context_parts.append(f"Preferred sectors: {', '.join(user_context['preferred_sectors'])}")
            
            if user_context.get("trading_style"):
                context_parts.append(f"Trading style: {user_context['trading_style']}")
            
            if context_parts:
                prompt += "\n\nUSER CONTEXT:\n" + "\n".join(context_parts)
        
        return prompt
    
    def _extract_text(self, content: list) -> str:
        """Extract text from response content blocks."""
        return "".join(
            block.text for block in content if hasattr(block, "text")
        )
    
    def _summarize_result(self, result: Any) -> str:
        """Create a brief summary of tool result for logging."""
        if isinstance(result, dict):
            if "error" in result:
                return f"Error: {result['error']}"
            return f"Dict with {len(result)} keys"
        elif isinstance(result, list):
            return f"List with {len(result)} items"
        else:
            return str(result)[:100]
    
    # Serialization helpers
    def _quote_to_dict(self, q) -> dict:
        return {
            "symbol": q.symbol,
            "ltp": float(q.ltp),
            "open": float(q.open),
            "high": float(q.high),
            "low": float(q.low),
            "close": float(q.close),
            "volume": q.volume,
            "change": float(q.change),
            "change_percent": float(q.change_percent)
        }
    
    def _mover_to_dict(self, m) -> dict:
        return {
            "symbol": m.symbol,
            "ltp": float(m.ltp),
            "metric_value": m.metric_value,
            "metric_name": m.metric_name,
            "rank": m.rank
        }
    
    def _volume_profile_to_dict(self, v) -> dict:
        return {
            "symbol": v.symbol,
            "current_volume": v.current_volume,
            "average_volume": v.average_volume,
            "volume_ratio": round(v.volume_ratio, 2),
            "baseline_days": v.baseline_days
        }
    
    def _ohlcv_to_dict(self, c) -> dict:
        return {
            "timestamp": c.timestamp.isoformat(),
            "open": float(c.open),
            "high": float(c.high),
            "low": float(c.low),
            "close": float(c.close),
            "volume": c.volume
        }
```

## Block 14

```python
python
# src/cia_sie/api/routes/market_intelligence.py

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from anthropic import AsyncAnthropic

from cia_sie.ai.market_intelligence_agent import AgentResponse, MarketIntelligenceAgent
from cia_sie.ai.usage_tracker import UsageTracker
from cia_sie.core.config import get_settings
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.repositories import InstrumentRepository, SiloRepository, ChartRepository, SignalRepository
from cia_sie.exposure.relationship_exposer import RelationshipExposer
from cia_sie.platforms.kite_intelligence import KiteIntelligenceEngine
from cia_sie.platforms.registry import get_adapter

router = APIRouter()


class MarketQueryRequest(BaseModel):
    """Request for market intelligence query."""
    query: str = Field(..., min_length=1, max_length=2000)
    user_context: Optional[dict] = None


class ExecutionLogResponse(BaseModel):
    """Execution log entry in response."""
    tool: str
    input_summary: str
    execution_time_ms: int
    timestamp: str


class MarketQueryResponse(BaseModel):
    """Response from market intelligence query."""
    response: str
    tools_used: list[str]
    execution_log: list[ExecutionLogResponse]
    data_sources: list[str]
    disclaimer: str
    query_time_ms: int


@router.post("/query", response_model=MarketQueryResponse)
async def query_market_intelligence(
    request: MarketQueryRequest,
    session: AsyncSession = Depends(get_session_dependency),
):
    """
    Execute a natural language market intelligence query.
    
    This endpoint combines:
    - Kite API market data (quotes, historical, instruments)
    - CIA-SIE signal data (TradingView chart signals)
    - Claude's reasoning and synthesis
    
    All responses are DESCRIPTIVE only, per constitutional rules.
    
    Example queries:
    - "What are the top 5 gainers in Nifty 50 today?"
    - "Show me unusual volume in banking stocks"
    - "Compare HDFC vs ICICI over the last month"
    - "What are my charts showing for RELIANCE?"
    """
    start_time = datetime.now()
    
    settings = get_settings()
    
    # Check budget
    tracker = UsageTracker(session)
    budget_status = await tracker.check_budget()
    if not budget_status["within_budget"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI budget exhausted. Market intelligence is temporarily disabled."
        )
    
    # Initialize components
    try:
        kite_adapter = get_adapter("Kite")
        if not kite_adapter.is_connected:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Kite connection not available. Please connect to Zerodha first."
            )
        
        kite_engine = KiteIntelligenceEngine(kite_adapter)
        
        anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        
        exposer = RelationshipExposer(
            silo_repository=SiloRepository(session),
            chart_repository=ChartRepository(session),
            signal_repository=SignalRepository(session),
        )
        
        instrument_repo = InstrumentRepository(session)
        
        agent = MarketIntelligenceAgent(
            anthropic_client=anthropic_client,
            kite_engine=kite_engine,
            relationship_exposer=exposer,
            instrument_repository=instrument_repo,
            model=settings.anthropic_model
        )
        
        result = await agent.query(
            user_message=request.query,
            user_context=request.user_context
        )
        
        # Record usage (estimate tokens)
        input_tokens = len(request.query.split()) * 4
        output_tokens = len(result.response.split()) * 4
        await tracker.record_usage(settings.anthropic_model, input_tokens, output_tokens)
        
        query_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return MarketQueryResponse(
            response=result.response,
            tools_used=result.tools_used,
            execution_log=[
                ExecutionLogResponse(
                    tool=log.tool_name,
                    input_summary=str(log.tool_input)[:200],
                    execution_time_ms=log.execution_time_ms,
                    timestamp=log.timestamp
                )
                for log in result.execution_log
            ],
            data_sources=result.data_sources,
            disclaimer=result.disclaimer,
            query_time_ms=query_time_ms
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Market intelligence query failed: {str(e)}"
        )
```

## Block 15

```python
python
# src/cia_sie/dal/models.py (additions)

class SavedQueryDB(Base):
    """User-saved market intelligence queries."""
    __tablename__ = "saved_queries"
    
    query_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    query_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    query_template: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_parameters: Mapped[str] = mapped_column(JSON, default="{}")
    execution_count: Mapped[int] = mapped_column(Integer, default=0)
    last_executed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
```

## Block 16

```python
Your decision:
═══════════════════════════════════════════════════════════════════
56:82:src/cia_sie/api/routes/charts.py
@router.post("/", response_model=Chart, status_code=status.HTTP_201_CREATED)
async def create_chart(
```

## Block 17

```python
🤖 ASSISTANT

                    The app is at `src/cia_sie/api/app.py` and the `app` instance is exported. The issue is that the orchestrator needs to run uvicorn from the `src` directory or use the proper Python path. Let me check if the package is installed:
```

## Block 18

```python
| **Prohibition: "buy/sell now"** | Regex pattern `r"\b(buy|sell)\s+now\b"` | `src/cia_sie/ai/response_validator.py:61` | ✅ ENFORCED |
| **Prohibition: position entry advice** | Regex pattern `r"\benter\s+(a\s+)?(long|short)\s+position\b"` | `src/cia_sie/ai/response_validator.py:62` | ✅ ENFORCED |
| **Prohibition: "take profit"** | Regex pattern `r"\btake\s+profits?\b"` | `src/cia_sie/ai/response_validator.py:64` | ✅ ENFORCED |
| **Prohibition: "cut losses"** | Regex pattern `r"\bcut\s+(your\s+)?loss(es)?\b"` | `src/cia_sie/ai/response_validator.py:65` | ✅ ENFORCED |
| **Exception: RecommendationAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:137-145` | ✅ EXISTS |
```

## Block 19

```python
| **Prohibition: position entry advice** | Regex pattern `r"\benter\s+(a\s+)?(long|short)\s+position\b"` | `src/cia_sie/ai/response_validator.py:62` | ✅ ENFORCED |
| **Prohibition: "take profit"** | Regex pattern `r"\btake\s+profits?\b"` | `src/cia_sie/ai/response_validator.py:64` | ✅ ENFORCED |
| **Prohibition: "cut losses"** | Regex pattern `r"\bcut\s+(your\s+)?loss(es)?\b"` | `src/cia_sie/ai/response_validator.py:65` | ✅ ENFORCED |
| **Exception: RecommendationAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:137-145` | ✅ EXISTS |
```

## Block 20

```python
| **Prohibition: "take profit"** | Regex pattern `r"\btake\s+profits?\b"` | `src/cia_sie/ai/response_validator.py:64` | ✅ ENFORCED |
| **Prohibition: "cut losses"** | Regex pattern `r"\bcut\s+(your\s+)?loss(es)?\b"` | `src/cia_sie/ai/response_validator.py:65` | ✅ ENFORCED |
| **Exception: RecommendationAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:137-145` | ✅ EXISTS |

**Prompt-Level Enforcement:**
```

## Block 21

```python
| Documentation Reference | Code Implementation | File:Line | Status |
|------------------------|---------------------|-----------|--------|
| **Contradiction Detection** | `ContradictionDetector` class | `src/cia_sie/exposure/contradiction_detector.py:32-44` | ✅ IMPLEMENTED |
| **DOES NOT resolve** | Docstring prohibition | `src/cia_sie/exposure/contradiction_detector.py:13-18` | ✅ DOCUMENTED |
| **Returns ALL contradictions** | Method returns complete list | `src/cia_sie/exposure/contradiction_detector.py:46-96` | ✅ IMPLEMENTED |
```

## Block 22

```python
|------------------------|---------------------|-----------|--------|
| **Contradiction Detection** | `ContradictionDetector` class | `src/cia_sie/exposure/contradiction_detector.py:32-44` | ✅ IMPLEMENTED |
| **DOES NOT resolve** | Docstring prohibition | `src/cia_sie/exposure/contradiction_detector.py:13-18` | ✅ DOCUMENTED |
| **Returns ALL contradictions** | Method returns complete list | `src/cia_sie/exposure/contradiction_detector.py:46-96` | ✅ IMPLEMENTED |
| **Prohibition: overall aggregation** | Regex pattern `r"\boverall\s+(direction|signal|trend)\s+(is|shows|indicates)\b"` | `src/cia_sie/ai/response_validator.py:66-70` | ✅ ENFORCED |
```

## Block 23

```python
| **Contradiction Detection** | `ContradictionDetector` class | `src/cia_sie/exposure/contradiction_detector.py:32-44` | ✅ IMPLEMENTED |
| **DOES NOT resolve** | Docstring prohibition | `src/cia_sie/exposure/contradiction_detector.py:13-18` | ✅ DOCUMENTED |
| **Returns ALL contradictions** | Method returns complete list | `src/cia_sie/exposure/contradiction_detector.py:46-96` | ✅ IMPLEMENTED |
| **Prohibition: overall aggregation** | Regex pattern `r"\boverall\s+(direction|signal|trend)\s+(is|shows|indicates)\b"` | `src/cia_sie/ai/response_validator.py:66-70` | ✅ ENFORCED |
| **Prohibition: net aggregation** | Regex pattern `r"\bnet\s+(signal|direction|bias)\b"` | `src/cia_sie/ai/response_validator.py:72` | ✅ ENFORCED |
```

## Block 24

```python
| **Prohibition: overall aggregation** | Regex pattern `r"\boverall\s+(direction|signal|trend)\s+(is|shows|indicates)\b"` | `src/cia_sie/ai/response_validator.py:66-70` | ✅ ENFORCED |
| **Prohibition: net aggregation** | Regex pattern `r"\bnet\s+(signal|direction|bias)\b"` | `src/cia_sie/ai/response_validator.py:72` | ✅ ENFORCED |
| **Prohibition: consensus** | Regex pattern `r"\bconsensus\s+(is|shows|indicates)\b"` | `src/cia_sie/ai/response_validator.py:73` | ✅ ENFORCED |
| **Prohibition: majority aggregation** | Regex pattern `r"\bmajority\s+(of\s+)?(signals?|charts?)\s+(show|indicate|suggest)\b"` | `src/cia_sie/ai/response_validator.py:74-78` | ✅ ENFORCED |
| **Exception: ContradictionResolutionAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:148-156` | ✅ EXISTS |
```

## Block 25

```python
| **Prohibition: net aggregation** | Regex pattern `r"\bnet\s+(signal|direction|bias)\b"` | `src/cia_sie/ai/response_validator.py:72` | ✅ ENFORCED |
| **Prohibition: consensus** | Regex pattern `r"\bconsensus\s+(is|shows|indicates)\b"` | `src/cia_sie/ai/response_validator.py:73` | ✅ ENFORCED |
| **Prohibition: majority aggregation** | Regex pattern `r"\bmajority\s+(of\s+)?(signals?|charts?)\s+(show|indicate|suggest)\b"` | `src/cia_sie/ai/response_validator.py:74-78` | ✅ ENFORCED |
| **Exception: ContradictionResolutionAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:148-156` | ✅ EXISTS |
| **Contradiction model (equal weight)** | `Contradiction` Pydantic model | `src/cia_sie/core/models.py:190-210` | ✅ IMPLEMENTED |
```

## Block 26

```python
| **Prohibition: consensus** | Regex pattern `r"\bconsensus\s+(is|shows|indicates)\b"` | `src/cia_sie/ai/response_validator.py:73` | ✅ ENFORCED |
| **Prohibition: majority aggregation** | Regex pattern `r"\bmajority\s+(of\s+)?(signals?|charts?)\s+(show|indicate|suggest)\b"` | `src/cia_sie/ai/response_validator.py:74-78` | ✅ ENFORCED |
| **Exception: ContradictionResolutionAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:148-156` | ✅ EXISTS |
| **Contradiction model (equal weight)** | `Contradiction` Pydantic model | `src/cia_sie/core/models.py:190-210` | ✅ IMPLEMENTED |
```

## Block 27

```python
| **Prohibition: majority aggregation** | Regex pattern `r"\bmajority\s+(of\s+)?(signals?|charts?)\s+(show|indicate|suggest)\b"` | `src/cia_sie/ai/response_validator.py:74-78` | ✅ ENFORCED |
| **Exception: ContradictionResolutionAttemptError** | Exception class definition | `src/cia_sie/core/exceptions.py:148-156` | ✅ EXISTS |
| **Contradiction model (equal weight)** | `Contradiction` Pydantic model | `src/cia_sie/core/models.py:190-210` | ✅ IMPLEMENTED |

**Key Enforcement Code:**
```

## Block 28

```python
| Component | Purpose | File |
|-----------|---------|------|
| **AIResponseValidator** | Main validation class | `src/cia_sie/ai/response_validator.py:166-276` |
| **ValidationResult** | Structured result object | `src/cia_sie/ai/response_validator.py:146-158` |
| **ValidatedResponseGenerator** | Retry on violations | `src/cia_sie/ai/response_validator.py:346-461` |
```

## Block 29

```python
|-----------|---------|------|
| **AIResponseValidator** | Main validation class | `src/cia_sie/ai/response_validator.py:166-276` |
| **ValidationResult** | Structured result object | `src/cia_sie/ai/response_validator.py:146-158` |
| **ValidatedResponseGenerator** | Retry on violations | `src/cia_sie/ai/response_validator.py:346-461` |
| **validate_ai_response()** | Convenience function | `src/cia_sie/ai/response_validator.py:469-480` |
```

## Block 30

```python
| **AIResponseValidator** | Main validation class | `src/cia_sie/ai/response_validator.py:166-276` |
| **ValidationResult** | Structured result object | `src/cia_sie/ai/response_validator.py:146-158` |
| **ValidatedResponseGenerator** | Retry on violations | `src/cia_sie/ai/response_validator.py:346-461` |
| **validate_ai_response()** | Convenience function | `src/cia_sie/ai/response_validator.py:469-480` |
| **ensure_disclaimer()** | Disclaimer enforcement | `src/cia_sie/ai/response_validator.py:483-497` |
```

## Block 31

```python
| Component | File | Lines | Purpose |
|-----------|------|-------|---------|
| **PROHIBITED_PATTERNS** | `src/cia_sie/ai/response_validator.py` | 35-121 | 31 regex patterns for detection |
| **AIResponseValidator** | `src/cia_sie/ai/response_validator.py` | 166-276 | Main validation class |
| **validate()** | `src/cia_sie/ai/response_validator.py` | 210-276 | Core validation method |
```

## Block 32

```python
|-----------|------|-------|---------|
| **PROHIBITED_PATTERNS** | `src/cia_sie/ai/response_validator.py` | 35-121 | 31 regex patterns for detection |
| **AIResponseValidator** | `src/cia_sie/ai/response_validator.py` | 166-276 | Main validation class |
| **validate()** | `src/cia_sie/ai/response_validator.py` | 210-276 | Core validation method |
| **validate_or_raise()** | `src/cia_sie/ai/response_validator.py` | 278-302 | Validation with exception |
```

## Block 33

```python
| **PROHIBITED_PATTERNS** | `src/cia_sie/ai/response_validator.py` | 35-121 | 31 regex patterns for detection |
| **AIResponseValidator** | `src/cia_sie/ai/response_validator.py` | 166-276 | Main validation class |
| **validate()** | `src/cia_sie/ai/response_validator.py` | 210-276 | Core validation method |
| **validate_or_raise()** | `src/cia_sie/ai/response_validator.py` | 278-302 | Validation with exception |
| **NARRATIVE_SYSTEM_PROMPT** | `src/cia_sie/ai/prompt_builder.py` | 40-82 | Prompt constraints |
```

## Block 34

```python
| **AIResponseValidator** | `src/cia_sie/ai/response_validator.py` | 166-276 | Main validation class |
| **validate()** | `src/cia_sie/ai/response_validator.py` | 210-276 | Core validation method |
| **validate_or_raise()** | `src/cia_sie/ai/response_validator.py` | 278-302 | Validation with exception |
| **NARRATIVE_SYSTEM_PROMPT** | `src/cia_sie/ai/prompt_builder.py` | 40-82 | Prompt constraints |
| **Chart (no weight)** | `src/cia_sie/core/models.py` | 99-128 | Model constraint |
```

## Block 35

```python
| Component | File | Lines | Purpose |
|-----------|------|-------|---------|
| **ContradictionDetector** | `src/cia_sie/exposure/contradiction_detector.py` | 32-166 | Detection class |
| **detect()** | `src/cia_sie/exposure/contradiction_detector.py` | 46-96 | Main detection method |
| **_is_contradiction()** | `src/cia_sie/exposure/contradiction_detector.py` | 138-154 | Contradiction logic |
```

## Block 36

```python
|-----------|------|-------|---------|
| **ContradictionDetector** | `src/cia_sie/exposure/contradiction_detector.py` | 32-166 | Detection class |
| **detect()** | `src/cia_sie/exposure/contradiction_detector.py` | 46-96 | Main detection method |
| **_is_contradiction()** | `src/cia_sie/exposure/contradiction_detector.py` | 138-154 | Contradiction logic |
| **Contradiction** | `src/cia_sie/core/models.py` | 190-210 | Model (no resolution fields) |
```

## Block 37

```python
| **ContradictionDetector** | `src/cia_sie/exposure/contradiction_detector.py` | 32-166 | Detection class |
| **detect()** | `src/cia_sie/exposure/contradiction_detector.py` | 46-96 | Main detection method |
| **_is_contradiction()** | `src/cia_sie/exposure/contradiction_detector.py` | 138-154 | Contradiction logic |
| **Contradiction** | `src/cia_sie/core/models.py` | 190-210 | Model (no resolution fields) |
| **Confirmation** | `src/cia_sie/core/models.py` | 213-228 | Model (no weight fields) |
```

## Block 38

```python
- `/CIA-SIE-Pure/src/cia_sie/ai/claude_client.py`
- `/CIA-SIE-Pure/src/cia_sie/dal/database.py`
- `/CIA-SIE-Pure/src/cia_sie/platforms/kite.py`

These are **backend Python files** that would be in the `NaSa` folder cloned from GitHub, NOT in the Cursor cache recovery.
```
