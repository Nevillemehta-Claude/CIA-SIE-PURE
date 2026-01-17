# PROJECT MERCURY: SPECIFICATION

**Document ID**: MERCURY-SPEC-001  
**Version**: 1.0.0  
**Classification**: SPECIFICATION  
**Date**: 2026-01-13  

---

## STAGE IV: SPECIFICATION
> *"Contracts define truth; ambiguity breeds failure."*

---

## 1. DATA MODELS

### 1.1 Core Models

```python
# Quote - Current market quote
@dataclass
class Quote:
    symbol: str
    exchange: str
    ltp: float              # Last traded price
    open: float
    high: float
    low: float
    close: float            # Previous close
    volume: int
    change: float           # Absolute change
    change_percent: float   # Percentage change
    timestamp: datetime

# OHLC - Historical candle
@dataclass
class OHLC:
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

# Position - Open trading position
@dataclass
class Position:
    symbol: str
    exchange: str
    product: str            # MIS, CNC, NRML
    quantity: int
    average_price: float
    ltp: float
    pnl: float
    pnl_percent: float

# Holding - Delivery holding
@dataclass
class Holding:
    symbol: str
    exchange: str
    quantity: int
    average_price: float
    ltp: float
    pnl: float
    pnl_percent: float

# Instrument - Tradeable instrument
@dataclass
class Instrument:
    instrument_token: int
    exchange_token: int
    symbol: str
    name: str
    exchange: str
    segment: str
    instrument_type: str
```

### 1.2 Conversation Models

```python
# Message - Single conversation message
@dataclass
class Message:
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime
    data_context: Optional[dict] = None

# Conversation - Full conversation
@dataclass
class Conversation:
    id: str
    messages: list[Message]
    created_at: datetime
    instrument_context: list[str] = field(default_factory=list)
```

### 1.3 Request/Response Models

```python
# QueryRequest - User query
@dataclass
class QueryRequest:
    query: str
    conversation_id: Optional[str] = None

# QueryResponse - System response
@dataclass
class QueryResponse:
    response: str
    conversation_id: str
    data_used: dict
    timestamp: datetime
```

---

## 2. INTERFACE CONTRACTS

### 2.1 KiteAdapter Interface

```python
class KiteAdapter:
    """Interface for Kite API access."""
    
    async def get_quote(self, symbol: str, exchange: str = "NSE") -> Quote:
        """
        Get current market quote for a symbol.
        
        Args:
            symbol: Trading symbol (e.g., "GOLDBEES")
            exchange: Exchange code (NSE, BSE, NFO, etc.)
            
        Returns:
            Quote object with current market data
            
        Raises:
            SymbolNotFoundError: If symbol doesn't exist
            KiteAPIError: If API call fails
        """
        
    async def get_ltp(self, symbols: list[str]) -> dict[str, float]:
        """
        Get last traded prices for multiple symbols.
        
        Args:
            symbols: List of symbols (format: "EXCHANGE:SYMBOL")
            
        Returns:
            Dict mapping symbol to LTP
        """
        
    async def get_ohlc(
        self, 
        symbol: str, 
        interval: str = "day",
        from_date: datetime = None,
        to_date: datetime = None
    ) -> list[OHLC]:
        """
        Get historical OHLC data.
        
        Args:
            symbol: Trading symbol
            interval: Candle interval (minute, day, week, month)
            from_date: Start date (default: 7 days ago)
            to_date: End date (default: today)
            
        Returns:
            List of OHLC candles
        """
        
    async def get_positions(self) -> list[Position]:
        """Get all open positions."""
        
    async def get_holdings(self) -> list[Holding]:
        """Get all holdings (delivery positions)."""
        
    async def search_instruments(self, query: str) -> list[Instrument]:
        """Search for instruments by name or symbol."""
        
    def is_authenticated(self) -> bool:
        """Check if Kite session is valid."""
```

### 2.2 AIEngine Interface

```python
class AIEngine:
    """Interface for Claude AI access."""
    
    async def generate(
        self,
        user_query: str,
        market_data: dict,
        conversation_history: list[Message],
        max_tokens: int = 2000
    ) -> str:
        """
        Generate AI response grounded in market data.
        
        Args:
            user_query: The user's question
            market_data: Fetched market data to ground response
            conversation_history: Previous messages for context
            max_tokens: Maximum response length
            
        Returns:
            AI-generated response text
            
        Raises:
            AIEngineError: If generation fails
        """
        
    def build_prompt(
        self,
        query: str,
        data: dict,
        history: list[Message]
    ) -> tuple[str, str]:
        """
        Build system and user prompts.
        
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
```

### 2.3 ChatEngine Interface

```python
class ChatEngine:
    """Main orchestration interface."""
    
    def __init__(self, kite: KiteAdapter, ai: AIEngine):
        """Initialize with dependencies."""
        
    async def process(
        self,
        query: str,
        conversation: Conversation
    ) -> QueryResponse:
        """
        Process a user query end-to-end.
        
        Args:
            query: User's natural language query
            conversation: Current conversation context
            
        Returns:
            QueryResponse with AI-generated answer
        """
        
    def identify_instruments(self, query: str) -> list[str]:
        """Extract instrument references from query."""
        
    def identify_data_needs(self, query: str) -> list[str]:
        """Identify what data types are needed (quote, positions, etc.)."""
```

---

## 3. PROMPT SPECIFICATION

### 3.1 System Prompt

```
You are Mercury, an intelligent financial market assistant. You have direct 
access to live market data from Zerodha Kite.

YOUR CAPABILITIES:
- Access real-time prices, quotes, and market data
- View the user's positions and holdings
- Analyze historical price movements
- Provide synthesized market insights

YOUR COMMUNICATION STYLE:
- Be direct and clear - avoid hedging or excessive caveats
- Synthesize information rather than dumping data
- Express opinions when the data supports conclusions
- Acknowledge uncertainty honestly when data is limited
- Provide actionable insights, not just descriptions

GROUNDING RULES:
- Always base responses on the market data provided
- Include specific numbers (prices, percentages) when relevant
- Reference timestamps for time-sensitive information
- If data is unavailable, say so clearly

You are a sophisticated financial intelligence partner, not a cautious 
disclaimer-generating machine.
```

### 3.2 User Prompt Template

```
USER QUERY: {query}

AVAILABLE MARKET DATA:
{formatted_data}

CONVERSATION CONTEXT:
{recent_messages}

Please provide a helpful, grounded response to the user's query.
```

---

## 4. ERROR CODES

| Code | Name | Description | User Message |
|------|------|-------------|--------------|
| E001 | KITE_AUTH_FAILED | Kite authentication failed | "Kite session expired. Please re-authenticate." |
| E002 | KITE_RATE_LIMIT | Rate limit exceeded | "Too many requests. Please wait a moment." |
| E003 | SYMBOL_NOT_FOUND | Symbol doesn't exist | "I couldn't find that symbol. Check the name?" |
| E004 | NO_DATA_AVAILABLE | No data for query | "No data available for that request." |
| E005 | AI_GENERATION_FAILED | Claude API failed | "AI temporarily unavailable. Try again?" |
| E006 | NETWORK_ERROR | Network connectivity | "Network issue. Check your connection." |
| E007 | INVALID_QUERY | Cannot parse query | "I didn't understand that. Could you rephrase?" |

---

## 5. SPECIAL COMMANDS

| Command | Action |
|---------|--------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/positions` | Show current positions summary |
| `/holdings` | Show current holdings summary |
| `/auth` | Re-authenticate with Kite |
| `/quit` or `/exit` | Exit Mercury |

---

## 6. SPECIFICATION VALIDATION CHECKLIST

| Condition | Status |
|-----------|--------|
| All data types formally defined | ✅ |
| All interfaces have docstrings | ✅ |
| Error codes enumerated | ✅ |
| Prompt templates defined | ✅ |
| Special commands documented | ✅ |

---

**Stage IV: SPECIFICATION is COMPLETE.**

---

**Next Stage**: IMPLEMENTATION (Stage V)
