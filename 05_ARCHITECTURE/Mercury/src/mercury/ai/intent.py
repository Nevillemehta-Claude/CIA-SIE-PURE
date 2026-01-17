"""
Mercury Intent Resolution
=========================

Uses Claude to understand user intent and extract data requirements.

ARCHITECTURAL PRINCIPLE: Let the LLM handle natural language understanding.
Don't try to anticipate every possible phrasing with regex/keyword matching.

This is the "brain" that converts natural language to structured API calls.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from mercury.core.config import get_settings
from mercury.core.logging import get_logger

logger = get_logger("mercury.intent")


# Intent extraction prompt - designed for fast, accurate extraction
# NOTE: We use string concatenation to avoid issues with .format() and JSON braces
INTENT_EXTRACTION_PROMPT_TEMPLATE = '''You are a financial query intent parser. Extract structured data requirements from user queries.

AVAILABLE DATA SOURCES:
- quotes: Real-time price data for specific symbols
- positions: User's open intraday/F&O positions  
- holdings: User's long-term stock holdings
- historical: OHLC history for trend analysis

AVAILABLE EXCHANGES:
- NSE: National Stock Exchange (default for stocks)
- BSE: Bombay Stock Exchange  
- NFO: NSE Futures & Options

SYMBOL FORMATS:
- Indices: "NIFTY 50", "NIFTY BANK", "SENSEX"
- Stocks: "RELIANCE", "TCS", "INFY", "HDFCBANK"
- ETFs: "GOLDBEES", "SILVERBEES", "NIFTYBEES"

INSTRUCTIONS:
1. Identify what symbols/instruments the user is asking about
2. Determine what data types are needed
3. Output valid JSON only - no explanation

OUTPUT FORMAT (JSON):
symbols: list of trading symbols
data_types: list from [quotes, positions, holdings, historical]
intent_summary: brief description
confidence: 0.0-1.0

EXAMPLES:

User: "What's the market sentiment?"
Output: symbols=["NIFTY 50", "NIFTY BANK"], data_types=["quotes"], intent_summary="Market overview via major indices", confidence=0.95

User: "How is Reliance doing?"
Output: symbols=["RELIANCE"], data_types=["quotes"], intent_summary="Current price for Reliance", confidence=0.98

User: "Show me my portfolio"
Output: symbols=[], data_types=["holdings", "positions"], intent_summary="User portfolio overview", confidence=0.95

User: "Compare HDFC Bank and ICICI Bank performance this week"
Output: symbols=["HDFCBANK", "ICICIBANK"], data_types=["quotes", "historical"], intent_summary="Week performance comparison", confidence=0.92

User: "Gold price?"
Output: symbols=["GOLDBEES"], data_types=["quotes"], intent_summary="Gold ETF price", confidence=0.85

User: "What's happening in IT sector?"
Output: symbols=["NIFTY IT", "TCS", "INFY", "WIPRO", "HCLTECH"], data_types=["quotes"], intent_summary="IT sector overview", confidence=0.88

User: "P&L for today"
Output: symbols=[], data_types=["positions"], intent_summary="Today's trading P&L", confidence=0.95

User: "indices ka kya haal hai?"
Output: symbols=["NIFTY 50", "NIFTY BANK", "SENSEX"], data_types=["quotes"], intent_summary="Market indices status (Hindi)", confidence=0.90

IMPORTANT: Output ONLY valid JSON, no explanation. Example format:
{"symbols": ["NIFTY 50"], "data_types": ["quotes"], "intent_summary": "description", "confidence": 0.9}

Now parse this query:
User: "'''


def build_intent_prompt(query: str) -> str:
    """Build the intent extraction prompt safely."""
    return INTENT_EXTRACTION_PROMPT_TEMPLATE + query + '"'


@dataclass
class IntentResult:
    """Result of intent extraction."""
    symbols: list[str] = field(default_factory=list)
    data_types: list[str] = field(default_factory=lambda: ["quotes"])
    intent_summary: str = ""
    confidence: float = 0.0
    raw_response: Optional[str] = None
    
    @property
    def needs_quotes(self) -> bool:
        return "quotes" in self.data_types
    
    @property
    def needs_positions(self) -> bool:
        return "positions" in self.data_types
    
    @property
    def needs_holdings(self) -> bool:
        return "holdings" in self.data_types
    
    @property
    def needs_historical(self) -> bool:
        return "historical" in self.data_types


class IntentResolver:
    """
    Uses Claude to understand user intent and extract data requirements.
    
    ARCHITECTURAL PRINCIPLE:
    Instead of trying to anticipate every possible phrasing with hardcoded
    keyword matching, we use the LLM's natural language understanding to
    interpret what the user wants and map it to structured API calls.
    
    Benefits:
    - Handles novel phrasings automatically
    - Supports multiple languages (Hindi, Hinglish, etc.)
    - Understands context and nuance
    - No maintenance of keyword lists
    
    Trade-offs:
    - Additional API call (but using fast Haiku model)
    - Small latency increase (~200-500ms)
    - Slightly higher cost per query
    """
    
    def __init__(self, use_fast_model: bool = True):
        """
        Initialize intent resolver.
        
        Args:
            use_fast_model: Use Haiku for speed (True) or Sonnet for accuracy (False)
        """
        self.use_fast_model = use_fast_model
        self._client = None
    
    @property
    def client(self):
        """Lazy-initialize Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                settings = get_settings()
                self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            except ImportError:
                raise ImportError("anthropic package required for intent resolution")
        return self._client
    
    async def resolve(
        self,
        query: str,
        conversation_context: Optional[list[str]] = None,
    ) -> IntentResult:
        """
        Resolve user intent from a natural language query.
        
        Args:
            query: User's natural language query
            conversation_context: Optional recent messages for context
            
        Returns:
            IntentResult with extracted symbols and data requirements
        """
        try:
            # Build prompt safely (avoids .format() issues with JSON braces)
            prompt = build_intent_prompt(query)
            
            # Add conversation context if available
            if conversation_context:
                context_str = "\n".join(f"- {msg}" for msg in conversation_context[-3:])
                prompt += f"\n\nRecent conversation context:\n{context_str}"
            
            # Use Haiku for speed, Sonnet for accuracy
            model = "claude-sonnet-4-20250514"
            
            # Make the API call
            import asyncio
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=model,
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )
            
            # Parse response
            raw_text = response.content[0].text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            json_text = raw_text
            if "```" in json_text:
                # Extract from code block
                start = json_text.find("{")
                end = json_text.rfind("}") + 1
                if start >= 0 and end > start:
                    json_text = json_text[start:end]
            
            # Parse JSON
            data = json.loads(json_text)
            
            return IntentResult(
                symbols=data.get("symbols", []),
                data_types=data.get("data_types", ["quotes"]),
                intent_summary=data.get("intent_summary", ""),
                confidence=data.get("confidence", 0.5),
                raw_response=raw_text,
            )
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse intent JSON: {e}, raw: {raw_text[:200]}")
            # Fall back to basic extraction
            return self._fallback_extraction(query)
        except Exception as e:
            logger.error(f"Intent resolution failed: {e}")
            return self._fallback_extraction(query)
    
    def _fallback_extraction(self, query: str) -> IntentResult:
        """
        Fallback to basic keyword extraction if LLM fails.
        
        This is a safety net, not the primary mechanism.
        """
        query_lower = query.lower()
        symbols = []
        data_types = ["quotes"]
        
        # Basic keyword matching (fallback only)
        if any(word in query_lower for word in ["market", "sentiment", "indices", "index"]):
            symbols = ["NIFTY 50", "NIFTY BANK", "SENSEX"]
        
        if any(word in query_lower for word in ["position", "p&l", "pnl", "trade"]):
            data_types.append("positions")
        
        if any(word in query_lower for word in ["holding", "portfolio", "invested"]):
            data_types.append("holdings")
        
        if any(word in query_lower for word in ["history", "week", "month", "trend"]):
            data_types.append("historical")
        
        return IntentResult(
            symbols=symbols,
            data_types=data_types,
            intent_summary="Fallback extraction",
            confidence=0.3,
        )


# Singleton instance
_intent_resolver: Optional[IntentResolver] = None


def get_intent_resolver(use_fast_model: bool = True) -> IntentResolver:
    """Get or create the intent resolver."""
    global _intent_resolver
    if _intent_resolver is None:
        _intent_resolver = IntentResolver(use_fast_model=use_fast_model)
    return _intent_resolver
