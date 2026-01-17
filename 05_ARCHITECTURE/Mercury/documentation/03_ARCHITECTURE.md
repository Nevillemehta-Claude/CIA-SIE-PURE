# PROJECT MERCURY: TECHNICAL ARCHITECTURE

**Document ID**: MERCURY-ARCH-001  
**Version**: 1.0.0  
**Classification**: FOUNDATION  
**Date**: 2026-01-13  

---

## STAGE III: ARCHITECTURE
> *"Structure precedes substance; design the skeleton before the flesh."*

---

## 1. SYSTEM OVERVIEW

### 1.1 Architecture Philosophy

Mercury follows a **minimal, efficient architecture** optimized for:
- **Speed**: Minimal layers between question and answer
- **Reliability**: Robust error handling at every integration point
- **Simplicity**: Only components necessary for the core use case

### 1.2 C4 Model: Level 1 - System Context

```
┌─────────────────────────────────────────────────────────────────┐
│                        SYSTEM CONTEXT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────┐         ┌──────────────┐        ┌──────────┐   │
│    │          │         │              │        │          │   │
│    │  TRADER  │◄───────►│   MERCURY    │◄──────►│   KITE   │   │
│    │  (User)  │         │   (System)   │        │   API    │   │
│    │          │         │              │        │          │   │
│    └──────────┘         └──────┬───────┘        └──────────┘   │
│                                │                                │
│                                │                                │
│                                ▼                                │
│                         ┌──────────┐                           │
│                         │          │                           │
│                         │  CLAUDE  │                           │
│                         │   API    │                           │
│                         │          │                           │
│                         └──────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 C4 Model: Level 2 - Container Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MERCURY SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐   │
│  │                 │     │                 │     │                 │   │
│  │   CLI / REPL    │────►│   CHAT ENGINE   │────►│  KITE ADAPTER   │   │
│  │   (Interface)   │     │   (Orchestrator)│     │  (Data Source)  │   │
│  │                 │     │                 │     │                 │   │
│  └─────────────────┘     └────────┬────────┘     └────────┬────────┘   │
│                                   │                        │            │
│                                   │                        │            │
│                                   ▼                        ▼            │
│                          ┌─────────────────┐     ┌─────────────────┐   │
│                          │                 │     │                 │   │
│                          │   AI ENGINE     │     │   KITE API      │   │
│                          │   (Claude)      │     │   (External)    │   │
│                          │                 │     │                 │   │
│                          └─────────────────┘     └─────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. LAYER ARCHITECTURE

### 2.1 Four-Layer Stack

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: INTERFACE                             │
│  ─────────────────                              │
│  • CLI/REPL for user input                      │
│  • Message formatting                           │
│  • Session management                           │
├─────────────────────────────────────────────────┤
│  LAYER 2: CHAT ENGINE (Orchestrator)            │
│  ────────────────────────────────               │
│  • Query interpretation                         │
│  • Data requirement identification              │
│  • Response assembly                            │
│  • Conversation state management                │
├─────────────────────────────────────────────────┤
│  LAYER 3: DATA LAYER                            │
│  ───────────────────                            │
│  • Kite API integration                         │
│  • Data fetching & caching                      │
│  • Error handling                               │
├─────────────────────────────────────────────────┤
│  LAYER 4: AI LAYER                              │
│  ─────────────────                              │
│  • Claude API integration                       │
│  • Prompt construction                          │
│  • Response generation                          │
│  • Context management                           │
└─────────────────────────────────────────────────┘
```

### 2.2 Dependency Rules

| Layer | May Depend On | May NOT Depend On |
|-------|---------------|-------------------|
| Interface | Chat Engine | Data Layer, AI Layer |
| Chat Engine | Data Layer, AI Layer | Interface |
| Data Layer | External (Kite API) | Chat Engine, Interface, AI Layer |
| AI Layer | External (Claude API) | Chat Engine, Interface, Data Layer |

### 2.3 Data Flow

```
User Query
    │
    ▼
┌─────────────────┐
│  CLI / REPL     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│              CHAT ENGINE                         │
│  ┌─────────────────────────────────────────┐   │
│  │  1. Parse query                          │   │
│  │  2. Identify data requirements           │   │
│  │  3. Fetch data from Kite                 │   │
│  │  4. Construct AI prompt with data        │   │
│  │  5. Get AI response                      │   │
│  │  6. Format and return                    │   │
│  └─────────────────────────────────────────┘   │
└────────┬──────────────────────┬─────────────────┘
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│  KITE ADAPTER   │    │   AI ENGINE     │
│                 │    │                 │
│  - get_quote()  │    │  - generate()   │
│  - get_ltp()    │    │  - with_context │
│  - get_ohlc()   │    │  - with_data    │
│  - get_positions│    │                 │
│  - get_holdings │    │                 │
└────────┬────────┘    └────────┬────────┘
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│   KITE API      │    │   CLAUDE API    │
│   (Zerodha)     │    │   (Anthropic)   │
└─────────────────┘    └─────────────────┘
```

---

## 3. COMPONENT SPECIFICATIONS

### 3.1 Component: CLI/REPL (`interface/repl.py`)

**Responsibility**: User interaction

**Interfaces**:
- IN: User text input
- OUT: Formatted AI response

**Key Functions**:
```python
def run_repl() -> None:
    """Main REPL loop - read, evaluate, print, loop"""
    
def format_response(response: str) -> str:
    """Format AI response for terminal display"""
    
def handle_special_commands(command: str) -> Optional[str]:
    """Handle /help, /clear, /quit, etc."""
```

### 3.2 Component: Chat Engine (`chat/engine.py`)

**Responsibility**: Query orchestration

**Interfaces**:
- IN: User query string, conversation history
- OUT: AI-generated response

**Key Functions**:
```python
async def process_query(
    query: str,
    conversation: Conversation,
    kite: KiteAdapter,
    ai: AIEngine
) -> str:
    """Main orchestration: query → data → AI → response"""

def identify_data_requirements(query: str) -> list[DataRequest]:
    """Parse query to determine what data is needed"""

def construct_prompt(
    query: str,
    data: dict,
    conversation: Conversation
) -> str:
    """Build the prompt for Claude with data context"""
```

### 3.3 Component: Kite Adapter (`kite/adapter.py`)

**Responsibility**: Market data access

**Interfaces**:
- IN: Data requests (symbol, type)
- OUT: Market data (prices, positions, etc.)

**Key Functions**:
```python
async def get_quote(symbol: str) -> Quote:
    """Get current quote for symbol"""
    
async def get_ltp(symbols: list[str]) -> dict[str, float]:
    """Get last traded prices for multiple symbols"""
    
async def get_ohlc(symbol: str, interval: str, days: int) -> list[OHLC]:
    """Get historical OHLC data"""
    
async def get_positions() -> list[Position]:
    """Get current positions"""
    
async def get_holdings() -> list[Holding]:
    """Get holdings (delivery positions)"""
    
async def get_instruments() -> list[Instrument]:
    """Get instrument master list"""
```

### 3.4 Component: AI Engine (`ai/engine.py`)

**Responsibility**: AI response generation

**Interfaces**:
- IN: Prompt with context and data
- OUT: AI-generated text response

**Key Functions**:
```python
async def generate(
    system_prompt: str,
    user_prompt: str,
    conversation_history: list[Message]
) -> str:
    """Generate response from Claude"""

def build_system_prompt() -> str:
    """Build the Mercury system prompt (unrestricted)"""
```

### 3.5 Component: Conversation Manager (`chat/conversation.py`)

**Responsibility**: Conversation state management

**Key Classes**:
```python
@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    data_context: Optional[dict]  # Market data used

@dataclass
class Conversation:
    id: str
    messages: list[Message]
    created_at: datetime
    
    def add_message(self, role: str, content: str, data: dict = None):
        """Add message to conversation"""
    
    def get_history(self, limit: int = 10) -> list[Message]:
        """Get recent conversation history"""
    
    def clear(self):
        """Clear conversation history"""
```

---

## 4. DIRECTORY STRUCTURE

```
projects/mercury/
├── documentation/
│   ├── 01_GENESIS.md
│   ├── 02_CONSTITUTION.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_SPECIFICATION.md
│   └── ...
│
├── src/
│   └── mercury/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       │
│       ├── interface/
│       │   ├── __init__.py
│       │   └── repl.py          # CLI/REPL
│       │
│       ├── chat/
│       │   ├── __init__.py
│       │   ├── engine.py        # Query orchestration
│       │   └── conversation.py  # State management
│       │
│       ├── kite/
│       │   ├── __init__.py
│       │   ├── adapter.py       # Kite API wrapper
│       │   ├── auth.py          # OAuth handling
│       │   └── models.py        # Data models
│       │
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── engine.py        # Claude integration
│       │   └── prompts.py       # Prompt templates
│       │
│       └── core/
│           ├── __init__.py
│           ├── config.py        # Configuration
│           └── exceptions.py    # Custom exceptions
│
├── tests/
│   ├── __init__.py
│   ├── test_chat_engine.py
│   ├── test_kite_adapter.py
│   ├── test_ai_engine.py
│   └── test_conversation.py
│
├── scripts/
│   ├── start_mercury.sh
│   └── authenticate_kite.py
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 5. EXTERNAL DEPENDENCIES

### 5.1 Kite Connect API

| Endpoint | Purpose | Rate Limit |
|----------|---------|------------|
| `/quote` | Current market quote | 1 req/sec |
| `/ltp` | Last traded price (batch) | 1 req/sec |
| `/ohlc` | Historical data | 3 req/sec |
| `/portfolio/positions` | Current positions | 10 req/min |
| `/portfolio/holdings` | Delivery holdings | 10 req/min |
| `/instruments` | Instrument master | 1 req/day |

### 5.2 Claude API (Anthropic)

| Model | Use Case | Cost |
|-------|----------|------|
| claude-3-5-sonnet | Standard queries | $3/$15 per 1M tokens |
| claude-3-haiku | Simple queries | $0.25/$1.25 per 1M tokens |

### 5.3 Python Dependencies

```
anthropic>=0.18.0      # Claude API client
kiteconnect>=5.0.0     # Kite Connect client
httpx>=0.27.0          # Async HTTP
pydantic>=2.0.0        # Data validation
python-dotenv>=1.0.0   # Environment management
rich>=13.0.0           # Terminal formatting
```

---

## 6. CONFIGURATION

### 6.1 Environment Variables

```bash
# Kite Connect
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
KITE_ACCESS_TOKEN=session_token  # After OAuth

# Claude/Anthropic
ANTHROPIC_API_KEY=your_api_key

# Mercury Configuration
MERCURY_MODEL=claude-3-5-sonnet-20241022
MERCURY_MAX_TOKENS=2000
MERCURY_CONVERSATION_LIMIT=20  # Max messages in context
```

### 6.2 Configuration Hierarchy

```
1. Environment variables (highest priority)
2. .env file
3. Default values in code
```

---

## 7. ERROR HANDLING STRATEGY

### 7.1 Error Categories

| Category | Example | Handling |
|----------|---------|----------|
| **Kite API Error** | Rate limit, auth failure | Surface to user, suggest retry |
| **Claude API Error** | Token limit, rate limit | Fallback to simpler response |
| **Network Error** | Timeout, DNS failure | Retry with backoff |
| **Data Error** | Invalid symbol, no data | Inform user, suggest alternatives |

### 7.2 Error Flow

```
Error Occurs
    │
    ▼
┌─────────────────┐
│ Catch & Classify │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
Recoverable  Fatal
    │         │
    ▼         ▼
Retry/       Inform User
Fallback     Exit Gracefully
```

---

## 8. SEQUENCE DIAGRAMS

### 8.1 Basic Query Flow

```
User          REPL      ChatEngine    KiteAdapter    AIEngine      Kite API    Claude API
 │             │             │             │             │             │            │
 │─"GOLDBEES?"─►             │             │             │             │            │
 │             │─process()──►│             │             │             │            │
 │             │             │─get_quote()─►             │             │            │
 │             │             │             │─────────────────────────►│            │
 │             │             │             │◄────quote data───────────│            │
 │             │             │◄─quote data─│             │             │            │
 │             │             │─────────────generate()───►│             │            │
 │             │             │             │             │─────────────────────────►│
 │             │             │             │             │◄────response─────────────│
 │             │             │◄────────────response──────│             │            │
 │             │◄─response───│             │             │             │            │
 │◄─formatted──│             │             │             │             │            │
 │             │             │             │             │             │            │
```

### 8.2 Multi-Turn Conversation

```
Turn 1: "What's the price of GOLDBEES?"
    → Fetch quote → Generate response → Add to history

Turn 2: "How has it performed this week?"
    → Context: knows "it" = GOLDBEES
    → Fetch OHLC → Generate with context → Add to history

Turn 3: "Compare it with SILVERBEES"
    → Context: knows comparison is for this week
    → Fetch both → Generate comparison → Add to history
```

---

## 9. ARCHITECTURE DECISION RECORDS

### ADR-M001: Minimal Layer Architecture

**Decision**: Use 4 layers instead of CIA-SIE's 7 layers.

**Rationale**: Mercury is a focused tool. Fewer layers = less latency, less complexity.

**Consequences**: Some patterns (like repository pattern) are not used. Direct API calls instead.

---

### ADR-M002: REPL Over Web Interface

**Decision**: Start with CLI/REPL instead of web UI.

**Rationale**: Fastest path to working system. Web UI can be added later.

**Consequences**: Limited to terminal users initially.

---

### ADR-M003: No Response Validation

**Decision**: Do not validate AI responses against prohibited patterns.

**Rationale**: Mercury's constitution (MR-002) explicitly allows direct communication.

**Consequences**: AI may produce responses that would fail CIA-SIE validation. This is intentional.

---

### ADR-M004: Conversation in Memory Only

**Decision**: Store conversation history in memory, not database.

**Rationale**: Simplicity. No persistence needed for personal tool.

**Consequences**: Conversation lost on restart. Acceptable for v1.

---

## 10. ARCHITECTURE VALIDATION CHECKLIST

| Condition | Status | Evidence |
|-----------|--------|----------|
| Layer boundaries explicit | ✅ | Section 2 |
| Data flow documented | ✅ | Section 2.3 |
| External dependencies catalogued | ✅ | Section 5 |
| ADRs exist for major decisions | ✅ | Section 9 (4 ADRs) |
| C4 diagrams at Context & Container level | ✅ | Section 1.2, 1.3 |
| No circular dependencies | ✅ | Section 2.2 dependency rules |

---

## 11. ARCHITECTURE SIGN-OFF

**Stage III: ARCHITECTURE is COMPLETE.**

Mercury's architecture is defined: 4 layers, minimal dependencies, clear data flow, focused on speed and simplicity.

---

**Prepared by**: AI Development Assistant  
**Date**: 2026-01-13  
**Next Stage**: SPECIFICATION (Stage IV)
