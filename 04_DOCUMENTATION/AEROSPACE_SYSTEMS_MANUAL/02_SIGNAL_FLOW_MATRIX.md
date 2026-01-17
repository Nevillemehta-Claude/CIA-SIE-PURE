# CHAPTER 02: SIGNAL FLOW MATRIX

**Document ID:** ASM-CH02-2026
**Classification:** DATA PATHWAY DOCUMENTATION
**Predecessor:** 01_SYSTEM_CIRCUIT_MAP.md
**Successor:** 03_INTEGRATION_TEST_PROTOCOL.md

---

## Purpose

Data/event pathways: origin → transformation → destination. Every signal traced from its point of entry to its final state.

---

## 2.1 SIGNAL TAXONOMY

### Signal Categories

| Category | Description | Origin | Count |
|----------|-------------|--------|-------|
| **USER** | User-initiated actions | Browser/Terminal | 15+ |
| **WEBHOOK** | External system callbacks | TradingView | 3 |
| **API** | HTTP requests | Network | 45+ |
| **INTERNAL** | Inter-module events | Application | 30+ |
| **DATABASE** | Persistence operations | ORM | 25+ |
| **EXTERNAL** | Third-party API calls | Kite/Claude | 12 |

---

## 2.2 CIA-SIE SIGNAL FLOWS

### 2.2.1 Signal Ingestion Flow (FLOW-001)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLOW-001: SIGNAL INGESTION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORIGIN: TradingView Webhook                                                │
│  ════════════════════════                                                   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: WEBHOOK RECEIPT                                             │   │
│  │  ──────────────────────                                              │   │
│  │  Location: src/cia_sie/webhooks/tradingview_receiver.py              │   │
│  │  Endpoint: POST /webhook/tradingview/{chart_id}                      │   │
│  │                                                                      │   │
│  │  Input:  { chart_id, timestamp, close, direction, macro, ... }       │   │
│  │  Output: Validated webhook payload                                   │   │
│  │  Transform: JSON parse → Pydantic validation                         │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 2: SIGNAL NORMALIZATION                                        │   │
│  │  ────────────────────────────                                        │   │
│  │  Location: src/cia_sie/ingestion/signal_normalizer.py                │   │
│  │                                                                      │   │
│  │  Input:  Raw webhook payload                                         │   │
│  │  Output: Normalized Signal object                                    │   │
│  │  Transform:                                                          │   │
│  │    - Map chart_id → chart FK                                         │   │
│  │    - Normalize direction enum                                        │   │
│  │    - Calculate derived values                                        │   │
│  │    - Validate constitutional compliance (no prescriptive terms)      │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 3: FRESHNESS CALCULATION                                       │   │
│  │  ─────────────────────────────                                       │   │
│  │  Location: src/cia_sie/ingestion/freshness.py                        │   │
│  │                                                                      │   │
│  │  Input:  Signal with timestamp                                       │   │
│  │  Output: Signal with freshness_status                                │   │
│  │  Transform:                                                          │   │
│  │    - age < 1h  → FRESH                                               │   │
│  │    - age < 24h → AGING                                               │   │
│  │    - age ≥ 24h → STALE                                               │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 4: CONTRADICTION DETECTION                                     │   │
│  │  ────────────────────────────────                                    │   │
│  │  Location: src/cia_sie/exposure/contradiction_detector.py            │   │
│  │                                                                      │   │
│  │  Input:  New signal + existing signals for same instrument           │   │
│  │  Output: List of Contradiction objects (if any)                      │   │
│  │  Transform:                                                          │   │
│  │    - Compare direction with other silos                              │   │
│  │    - Identify conflicts (BULLISH vs BEARISH on same instrument)      │   │
│  │    - Create Contradiction record (EXPOSED, never resolved)           │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 5: CONFIRMATION DETECTION                                      │   │
│  │  ───────────────────────────────                                     │   │
│  │  Location: src/cia_sie/exposure/confirmation_detector.py             │   │
│  │                                                                      │   │
│  │  Input:  New signal + existing signals for same instrument           │   │
│  │  Output: List of Confirmation objects (if any)                       │   │
│  │  Transform:                                                          │   │
│  │    - Compare direction across silos                                  │   │
│  │    - Identify alignments (BULLISH + BULLISH on same instrument)      │   │
│  │    - Create Confirmation record with confidence_exposure             │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 6: DATABASE PERSISTENCE                                        │   │
│  │  ────────────────────────────                                        │   │
│  │  Location: src/cia_sie/dal/repositories.py                           │   │
│  │                                                                      │   │
│  │  Input:  Signal, Contradictions[], Confirmations[]                   │   │
│  │  Output: Persisted records with IDs                                  │   │
│  │  Transform:                                                          │   │
│  │    - signals table INSERT                                            │   │
│  │    - contradictions table INSERT (if any)                            │   │
│  │    - confirmations table INSERT (if any)                             │   │
│  │    - Transaction commit                                              │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  DESTINATION: Database (signals, contradictions, confirmations tables)     │
│  ══════════════════════════════════════════════════════════════════════    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2.2 Narrative Generation Flow (FLOW-002)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLOW-002: NARRATIVE GENERATION                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORIGIN: User request for instrument analysis                               │
│  ═══════════════════════════════════════════                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: API REQUEST                                                 │   │
│  │  ───────────────────                                                 │   │
│  │  Location: src/cia_sie/api/routes/narratives.py                      │   │
│  │  Endpoint: GET /api/narratives/{instrument_id}                       │   │
│  │                                                                      │   │
│  │  Input:  instrument_id, include_contradictions, include_confirms     │   │
│  │  Output: Request validated and parsed                                │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 2: DATA ASSEMBLY                                               │   │
│  │  ─────────────────────                                               │   │
│  │  Location: src/cia_sie/dal/repositories.py                           │   │
│  │                                                                      │   │
│  │  Input:  instrument_id                                               │   │
│  │  Output: Complete data bundle                                        │   │
│  │  Transform:                                                          │   │
│  │    - Fetch instrument details                                        │   │
│  │    - Fetch all signals (grouped by silo)                             │   │
│  │    - Fetch all contradictions                                        │   │
│  │    - Fetch all confirmations                                         │   │
│  │    - Fetch chart configurations                                      │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 3: PROMPT CONSTRUCTION                                         │   │
│  │  ───────────────────────────                                         │   │
│  │  Location: src/cia_sie/ai/prompt_builder.py                          │   │
│  │                                                                      │   │
│  │  Input:  Data bundle                                                 │   │
│  │  Output: System prompt + User prompt                                 │   │
│  │  Transform:                                                          │   │
│  │    - Include constitutional rules (CR-001, CR-002, CR-003)           │   │
│  │    - Structure signal data as markdown tables                        │   │
│  │    - Format contradictions as explicit conflicts                     │   │
│  │    - Format confirmations as aligned signals                         │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 4: MODEL SELECTION                                             │   │
│  │  ───────────────────────                                             │   │
│  │  Location: src/cia_sie/ai/model_registry.py                          │   │
│  │                                                                      │   │
│  │  Input:  Request complexity, budget remaining                        │   │
│  │  Output: Selected model (claude-sonnet-4-20250514, haiku, etc.)               │   │
│  │  Transform:                                                          │   │
│  │    - Check AI budget table                                           │   │
│  │    - Assess request complexity                                       │   │
│  │    - Return appropriate tier                                         │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 5: CLAUDE API CALL                                             │   │
│  │  ───────────────────────                                             │   │
│  │  Location: src/cia_sie/ai/claude_client.py                           │   │
│  │  External: EXT-002 (Anthropic API)                                   │   │
│  │                                                                      │   │
│  │  Input:  System prompt, User prompt, Model ID                        │   │
│  │  Output: Raw AI response                                             │   │
│  │  Transform:                                                          │   │
│  │    - HTTP POST to api.anthropic.com/v1/messages                      │   │
│  │    - Handle rate limits, retries                                     │   │
│  │    - Track token usage                                               │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 6: CONSTITUTIONAL VALIDATION                                   │   │
│  │  ─────────────────────────────────                                   │   │
│  │  Location: src/cia_sie/ai/response_validator.py                      │   │
│  │  *** CRITICAL COMPLIANCE GATE ***                                    │   │
│  │                                                                      │   │
│  │  Input:  Raw AI response                                             │   │
│  │  Output: Validated response OR ValidationError                       │   │
│  │  Transform:                                                          │   │
│  │    - CHECK CR-001: No "should", "must", "recommend"                  │   │
│  │    - CHECK CR-002: Contradictions exposed, not resolved              │   │
│  │    - CHECK CR-003: Descriptive language only                         │   │
│  │    - REJECT if violations found                                      │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 7: NARRATIVE PERSISTENCE                                       │   │
│  │  ─────────────────────────────                                       │   │
│  │  Location: src/cia_sie/dal/repositories.py                           │   │
│  │                                                                      │   │
│  │  Input:  Validated narrative, usage stats                            │   │
│  │  Output: Persisted narrative with ID                                 │   │
│  │  Transform:                                                          │   │
│  │    - narratives table INSERT                                         │   │
│  │    - ai_usage table INSERT (tokens, model, cost)                     │   │
│  │    - Transaction commit                                              │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 8: RESPONSE FORMATTING                                         │   │
│  │  ───────────────────────────                                         │   │
│  │  Location: src/cia_sie/api/routes/narratives.py                      │   │
│  │                                                                      │   │
│  │  Input:  Narrative object                                            │   │
│  │  Output: JSON response with HTML-formatted narrative                 │   │
│  │  Transform:                                                          │   │
│  │    - Markdown → HTML conversion                                      │   │
│  │    - Add metadata (timestamp, model, tokens)                         │   │
│  │    - Return HTTP 200 with body                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  DESTINATION: Client (Browser/API consumer)                                 │
│  ══════════════════════════════════════════                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2.3 Dashboard Assembly Flow (FLOW-003)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLOW-003: DASHBOARD ASSEMBLY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORIGIN: User opens dashboard in browser                                    │
│  ═══════════════════════════════════════                                    │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐     │
│  │  PARALLEL API CALLS (React Query)                                  │     │
│  │                                                                    │     │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │     │
│  │  │GET /instru- │ │GET /signals │ │GET /relatio-│ │GET /baskets │ │     │
│  │  │ments        │ │?fresh=true  │ │nships       │ │             │ │     │
│  │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ │     │
│  │         │               │               │               │        │     │
│  └─────────┼───────────────┼───────────────┼───────────────┼────────┘     │
│            │               │               │               │              │
│            ▼               ▼               ▼               ▼              │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  BACKEND PROCESSING                                                  │  │
│  │                                                                      │  │
│  │  instruments.py    signals.py      relationships.py   baskets.py    │  │
│  │       │                │                  │               │          │  │
│  │       ▼                ▼                  ▼               ▼          │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                    repositories.py                            │   │  │
│  │  │                                                               │   │  │
│  │  │  SELECT * FROM instruments                                    │   │  │
│  │  │  SELECT * FROM signals WHERE freshness != 'STALE'             │   │  │
│  │  │  SELECT * FROM contradictions                                 │   │  │
│  │  │  SELECT * FROM confirmations                                  │   │  │
│  │  │  SELECT * FROM baskets JOIN basket_items                      │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │       │                │                  │               │          │  │
│  └───────┼────────────────┼──────────────────┼───────────────┼──────────┘  │
│          │                │                  │               │             │
│          ▼                ▼                  ▼               ▼             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  FRONTEND STATE ASSEMBLY                                             │  │
│  │                                                                      │  │
│  │  React Query Cache:                                                  │  │
│  │  ┌─────────────────────────────────────────────────────────────┐    │  │
│  │  │ instruments: [...], signals: [...], contradictions: [...],  │    │  │
│  │  │ confirmations: [...], baskets: [...]                        │    │  │
│  │  └─────────────────────────────────────────────────────────────┘    │  │
│  │                                                                      │  │
│  │  Component Tree:                                                     │  │
│  │  Dashboard                                                           │  │
│  │  ├── InstrumentList → instruments data                               │  │
│  │  ├── SignalGrid → signals data                                       │  │
│  │  ├── ContradictionPanel → contradictions data                        │  │
│  │  ├── ConfirmationPanel → confirmations data                          │  │
│  │  └── BasketSidebar → baskets data                                    │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  DESTINATION: Rendered UI with complete dashboard                          │
│  ═════════════════════════════════════════════════                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2.3 MERCURY SIGNAL FLOWS

### 2.3.1 Chat Query Flow (MFLOW-001)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MFLOW-001: MERCURY CHAT QUERY                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORIGIN: User types question in chat interface                              │
│  ═════════════════════════════════════════════                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: USER INPUT CAPTURE                                          │   │
│  │  ──────────────────────────                                          │   │
│  │  Location: src/mercury/api/app.py (WebSocket) OR                     │   │
│  │            src/mercury/interface/repl.py (Terminal)                  │   │
│  │                                                                      │   │
│  │  Input:  "What is the current price of RELIANCE?"                    │   │
│  │  Output: Query string + connection context                           │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 2: QUERY PARSING                                               │   │
│  │  ─────────────────────                                               │   │
│  │  Location: src/mercury/chat/engine.py                                │   │
│  │  Function: _parse_query()                                            │   │
│  │                                                                      │   │
│  │  Input:  Raw query string                                            │   │
│  │  Output: ParsedQuery(symbols=["RELIANCE"], intent="price_check")     │   │
│  │  Transform:                                                          │   │
│  │    - Extract instrument symbols using patterns                       │   │
│  │    - Identify query intent (price, analysis, portfolio)              │   │
│  │    - Validate symbols against allowed list                           │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 3: MARKET DATA FETCH                                           │   │
│  │  ─────────────────────────                                           │   │
│  │  Location: src/mercury/kite/adapter.py                               │   │
│  │  External: EXT-001 (Kite Connect API)                                │   │
│  │                                                                      │   │
│  │  Input:  List of symbols ["RELIANCE"]                                │   │
│  │  Output: MarketDataBundle with quotes, positions, holdings           │   │
│  │  Transform:                                                          │   │
│  │    - get_quote("NSE:RELIANCE")                                       │   │
│  │    - get_positions() if portfolio context needed                     │   │
│  │    - get_holdings() if holdings context needed                       │   │
│  │    - Apply circuit breaker if API failing                            │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 4: CONTEXT ASSEMBLY                                            │   │
│  │  ────────────────────────                                            │   │
│  │  Location: src/mercury/chat/conversation.py                          │   │
│  │  Function: get_context()                                             │   │
│  │                                                                      │   │
│  │  Input:  Current query + conversation history                        │   │
│  │  Output: Full context for AI                                         │   │
│  │  Transform:                                                          │   │
│  │    - Add last N messages for continuity                              │   │
│  │    - Include market data bundle                                      │   │
│  │    - Format as structured context                                    │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 5: PROMPT CONSTRUCTION                                         │   │
│  │  ───────────────────────────                                         │   │
│  │  Location: src/mercury/ai/prompts.py                                 │   │
│  │                                                                      │   │
│  │  Input:  Context bundle                                              │   │
│  │  Output: System prompt + User prompt                                 │   │
│  │  Transform:                                                          │   │
│  │    - SYSTEM_PROMPT (Mercury constitution - UNRESTRICTED)             │   │
│  │    - build_user_prompt() with market data                            │   │
│  │    - Include conversation history                                    │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 6: AI GENERATION                                               │   │
│  │  ─────────────────────                                               │   │
│  │  Location: src/mercury/ai/engine.py                                  │   │
│  │  External: EXT-002 (Anthropic Claude API)                            │   │
│  │                                                                      │   │
│  │  Input:  System prompt, User prompt                                  │   │
│  │  Output: AI-generated response                                       │   │
│  │  Transform:                                                          │   │
│  │    - POST to api.anthropic.com/v1/messages                           │   │
│  │    - Model: claude-sonnet-4-20250514 (default)                                │   │
│  │    - Apply circuit breaker if failing                                │   │
│  │    - NO constitutional validation (Mercury is unrestricted)          │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 7: CONVERSATION UPDATE                                         │   │
│  │  ───────────────────────────                                         │   │
│  │  Location: src/mercury/chat/conversation.py                          │   │
│  │  Function: add_message()                                             │   │
│  │                                                                      │   │
│  │  Input:  User query + AI response                                    │   │
│  │  Output: Updated conversation state                                  │   │
│  │  Transform:                                                          │   │
│  │    - Append user message to history                                  │   │
│  │    - Append AI response to history                                   │   │
│  │    - Trim if exceeding max_history                                   │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 8: RESPONSE DELIVERY                                           │   │
│  │  ─────────────────────────                                           │   │
│  │  Location: src/mercury/api/app.py OR src/mercury/interface/repl.py  │   │
│  │                                                                      │   │
│  │  Input:  ChatResponse object                                         │   │
│  │  Output: Formatted response to user                                  │   │
│  │  Transform:                                                          │   │
│  │    - WebSocket: JSON message with HTML content                       │   │
│  │    - REPL: Rich console formatted output                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  DESTINATION: User sees AI response in chat                                 │
│  ═══════════════════════════════════════════                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.3.2 Startup Initialization Flow (MFLOW-002)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MFLOW-002: MERCURY STARTUP                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORIGIN: python -m mercury --web                                            │
│  ═══════════════════════════════                                            │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: CONFIGURATION LOAD                                          │   │
│  │  ──────────────────────────                                          │   │
│  │  Location: src/mercury/core/config.py                                │   │
│  │                                                                      │   │
│  │  Input:  Environment variables, .env file                            │   │
│  │  Output: MercurySettings singleton                                   │   │
│  │  Transform:                                                          │   │
│  │    - Load ANTHROPIC_API_KEY                                          │   │
│  │    - Load KITE_API_KEY, KITE_API_SECRET                              │   │
│  │    - Load KITE_ACCESS_TOKEN (if available)                           │   │
│  │    - Validate required settings                                      │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 2: CONFIGURATION VALIDATION                                    │   │
│  │  ────────────────────────────────                                    │   │
│  │  Location: src/mercury/core/validation.py                            │   │
│  │                                                                      │   │
│  │  Input:  MercurySettings                                             │   │
│  │  Output: ValidationResult (errors, warnings)                         │   │
│  │  Transform:                                                          │   │
│  │    - Check API key formats                                           │   │
│  │    - Validate endpoint URLs                                          │   │
│  │    - Check feature flag consistency                                  │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 3: KITE API VERIFICATION                                       │   │
│  │  ─────────────────────────────                                       │   │
│  │  Location: src/mercury/core/startup.py                               │   │
│  │  Function: verify_kite_api()                                         │   │
│  │                                                                      │   │
│  │  Input:  Kite credentials                                            │   │
│  │  Output: APIStatus (status, authenticated, latency)                  │   │
│  │  Transform:                                                          │   │
│  │    - Check if KITE_MOCK_MODE enabled → return MOCK_MODE              │   │
│  │    - Check if KITE_ACCESS_TOKEN present                              │   │
│  │    - Attempt API call to validate token                              │   │
│  │    - Return AUTHENTICATED, FAILED, or NOT_CONFIGURED                 │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 4: ANTHROPIC API VERIFICATION                                  │   │
│  │  ──────────────────────────────────                                  │   │
│  │  Location: src/mercury/core/startup.py                               │   │
│  │  Function: verify_anthropic_api()                                    │   │
│  │                                                                      │   │
│  │  Input:  Anthropic API key                                           │   │
│  │  Output: APIStatus (status, authenticated, latency)                  │   │
│  │  Transform:                                                          │   │
│  │    - Check if mock mode → return MOCK_MODE                           │   │
│  │    - Send test message to Claude                                     │   │
│  │    - Validate response received                                      │   │
│  │    - Return AUTHENTICATED or FAILED                                  │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 5: READINESS DETERMINATION                                     │   │
│  │  ───────────────────────────────                                     │   │
│  │  Location: src/mercury/core/startup.py                               │   │
│  │  Function: perform_launch_readiness_check()                          │   │
│  │                                                                      │   │
│  │  Input:  Kite status + Anthropic status                              │   │
│  │  Output: LaunchReadiness (ready, errors, warnings)                   │   │
│  │  Transform:                                                          │   │
│  │    - Both AUTHENTICATED → ready = True                               │   │
│  │    - Any FAILED → ready = False, add to errors                       │   │
│  │    - Any NOT_CONFIGURED → add to warnings                            │   │
│  │    - Display formatted status report                                 │   │
│  └──────────────────────────────────┬──────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 6: SERVER START (if ready)                                     │   │
│  │  ───────────────────────────────                                     │   │
│  │  Location: src/mercury/main.py                                       │   │
│  │                                                                      │   │
│  │  Input:  Readiness result                                            │   │
│  │  Output: Running FastAPI server                                      │   │
│  │  Transform:                                                          │   │
│  │    - If ready: uvicorn.run(app, host, port)                          │   │
│  │    - If not ready: Exit with status report                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  DESTINATION: System operational at http://localhost:8888                   │
│  ═══════════════════════════════════════════════════════                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2.4 CROSS-SYSTEM SIGNAL FLOWS

### 2.4.1 External API Integration Points

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL API SIGNAL MATRIX                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  KITE API (EXT-001)                                                         │
│  ══════════════════                                                         │
│                                                                             │
│  ┌──────────────────┬────────────────────┬──────────────────────────────┐  │
│  │ Endpoint         │ Called By          │ Response Handling            │  │
│  ├──────────────────┼────────────────────┼──────────────────────────────┤  │
│  │ /quote           │ MKITE-001, PLAT-001│ → Quote model → Chat/UI      │  │
│  │ /ltp             │ MKITE-001          │ → Price dict → Chat          │  │
│  │ /ohlc            │ MKITE-001          │ → OHLC model → Analysis      │  │
│  │ /positions       │ MKITE-001          │ → Position[] → Portfolio     │  │
│  │ /holdings        │ MKITE-001          │ → Holding[] → Portfolio      │  │
│  │ /instruments     │ MKITE-001          │ → Instrument[] → Search      │  │
│  │ /historical      │ MKITE-001          │ → OHLC[] → Charts           │  │
│  └──────────────────┴────────────────────┴──────────────────────────────┘  │
│                                                                             │
│  Error Handling:                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ KiteAPIError      → Circuit breaker → Graceful degradation message  │   │
│  │ KiteAuthError     → Token refresh prompt → User re-auth required    │   │
│  │ SymbolNotFoundError → Return not found → User feedback              │   │
│  │ RateLimitError    → Retry with backoff → Eventually succeed/fail    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ANTHROPIC API (EXT-002)                                                    │
│  ═══════════════════════                                                    │
│                                                                             │
│  ┌──────────────────┬────────────────────┬──────────────────────────────┐  │
│  │ Endpoint         │ Called By          │ Response Handling            │  │
│  ├──────────────────┼────────────────────┼──────────────────────────────┤  │
│  │ /v1/messages     │ AI-001 (CIA-SIE)   │ → Validate → Narrative       │  │
│  │ /v1/messages     │ MAI-001 (Mercury)  │ → Direct → Chat response     │  │
│  └──────────────────┴────────────────────┴──────────────────────────────┘  │
│                                                                             │
│  Error Handling:                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ AuthenticationError → Check API key → User configuration prompt     │   │
│  │ RateLimitError      → Retry with backoff → Model fallback           │   │
│  │ APIError            → Circuit breaker → Error message to user       │   │
│  │ ValidationError     → REJECT response → Regenerate (CIA-SIE only)   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TRADINGVIEW WEBHOOKS (EXT-003)                                             │
│  ═══════════════════════════════                                            │
│                                                                             │
│  ┌──────────────────┬────────────────────┬──────────────────────────────┐  │
│  │ Event            │ Received By        │ Processing                   │  │
│  ├──────────────────┼────────────────────┼──────────────────────────────┤  │
│  │ PRIMARY_SIGNAL   │ PLAT-002           │ → Normalize → Signal table   │  │
│  │ HTF_STRUCTURE    │ PLAT-002           │ → Normalize → Signal table   │  │
│  │ MOM_HEALTH       │ PLAT-002           │ → Normalize → Signal table   │  │
│  └──────────────────┴────────────────────┴──────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2.5 SIGNAL TRANSFORMATION REGISTRY

### Complete Transformation Catalog

| Signal Origin | Transformation | Destination | Validation |
|---------------|----------------|-------------|------------|
| Webhook JSON | Pydantic parse | Signal model | Schema validation |
| Signal model | Freshness calc | Signal.freshness | Time-based |
| Signal model | Contradiction detect | Contradiction[] | Direction comparison |
| Signal model | Confirmation detect | Confirmation[] | Direction alignment |
| User query | Parse intent | ParsedQuery | Regex/NLP |
| ParsedQuery | Kite API call | MarketDataBundle | Response validation |
| MarketDataBundle | Prompt build | AI prompt | Template formatting |
| AI prompt | Claude API | Raw response | API contract |
| Raw response (CIA-SIE) | Constitutional validate | Narrative | CR-001/002/003 |
| Raw response (Mercury) | Direct pass | ChatResponse | None (unrestricted) |
| Narrative | HTML format | API response | Schema |
| ChatResponse | WebSocket send | UI update | JSON serialization |

---

## 2.6 CHAPTER HANDOFF

**This chapter established:**
- Complete signal taxonomy (6 categories)
- 6 detailed flow diagrams with step-by-step transformations
- External API integration points
- Signal transformation registry

**Next chapter will detail:**
- Integration test protocols for each junction
- Validation sequences
- Test data requirements

---

**Predecessor:** [01_SYSTEM_CIRCUIT_MAP.md](./01_SYSTEM_CIRCUIT_MAP.md)
**Successor:** [03_INTEGRATION_TEST_PROTOCOL.md](./03_INTEGRATION_TEST_PROTOCOL.md)

---

*"Every signal traced from its point of entry to its final state."*
