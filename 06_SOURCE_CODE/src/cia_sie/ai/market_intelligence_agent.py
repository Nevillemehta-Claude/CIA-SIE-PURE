"""
CIA-SIE Market Intelligence Agent
==================================

Agentic AI layer that orchestrates Claude + Kite + CIA-SIE.

This agent:
1. Receives natural language queries
2. Uses Claude with tool definitions to plan and execute
3. Calls Kite API and CIA-SIE data as needed
4. Synthesizes results into constitutional-compliant responses
5. Maintains full audit trail of all tool calls

GOVERNED BY: Constitutional Rules (CR-001, CR-002, CR-003)
"""

import json
import logging
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Optional

from anthropic import AsyncAnthropic

from cia_sie.ai.response_validator import ensure_disclaimer, validate_ai_response
from cia_sie.dal.repositories import InstrumentRepository
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
        response = None
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
        
        if response is None:
            raise RuntimeError("No response generated")
        
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
                from cia_sie.platforms.kite_intelligence import KiteInterval
                interval_str = tool_input.get("interval", "day")
                # Convert string to KiteInterval enum
                try:
                    interval = KiteInterval(interval_str)
                except ValueError:
                    interval = KiteInterval.DAY  # Default fallback
                candles = await self.kite.get_historical_ohlcv(
                    symbol=tool_input["symbol"],
                    from_date=date.fromisoformat(tool_input["from_date"]),
                    to_date=date.fromisoformat(tool_input["to_date"]),
                    interval=interval
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
