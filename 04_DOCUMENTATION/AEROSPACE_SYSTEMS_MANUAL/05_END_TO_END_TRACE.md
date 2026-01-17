# CHAPTER 05: END-TO-END TRACE DOCUMENTATION

**Document ID:** ASM-CH05-2026
**Classification:** CIRCUIT TRAVERSAL DOCUMENTATION
**Predecessor:** 04_FAILURE_MODE_ANALYSIS.md
**Successor:** 06_LAUNCH_READINESS_CHECKLIST.md

---

## Purpose

Action A → Action B → ... → Circuit Complete. Complete circuit traversal from ignition to mission completion for every user journey.

---

## 5.1 CIRCUIT TRACE NOTATION

### Trace Element Key

| Symbol | Meaning |
|--------|---------|
| `[→]` | Direct flow (synchronous) |
| `[⇢]` | Async flow (non-blocking) |
| `[◆]` | Decision point |
| `[●]` | Terminal state |
| `[↺]` | Loop/retry |
| `[✓]` | Validation checkpoint |
| `[⚠]` | Potential failure point |
| `[📁]` | Database operation |
| `[🌐]` | External API call |

---

## 5.2 CIA-SIE COMPLETE CIRCUIT TRACES

### 5.2.1 TRACE-001: System Startup to Operational

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-001: CIA-SIE STARTUP CIRCUIT                                        │
│  Duration: ~5 seconds | Steps: 14 | Checkpoints: 6                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IGNITION                                                                   │
│  ════════                                                                   │
│                                                                             │
│  [USER] Double-clicks start-cia-sie.command                                 │
│     │                                                                       │
│     [→] STEP 01: Shell script executes                                      │
│         File: start-cia-sie.command                                         │
│         Action: Source ignite.sh                                            │
│     │                                                                       │
│     [→] STEP 02: Load configuration                                         │
│         File: scripts/launcher/config.sh                                    │
│         Action: Set PROJECT_ROOT, VENV_PATH, PORTS                          │
│         [✓] CHECKPOINT: Config loaded                                       │
│     │                                                                       │
│     [→] STEP 03: Load utilities                                             │
│         File: scripts/launcher/utils.sh                                     │
│         Action: Define log_*, pid_*, display_* functions                    │
│     │                                                                       │
│     [→] STEP 04: Verify prerequisites                                       │
│         File: scripts/launcher/ignite.sh                                    │
│         [⚠] Failure: Missing venv → EXIT with error                        │
│         [⚠] Failure: Missing source → EXIT with error                      │
│         [⚠] Failure: Port in use → EXIT with error                         │
│         [✓] CHECKPOINT: Prerequisites verified                              │
│     │                                                                       │
│     [→] STEP 05: Activate virtual environment                               │
│         Action: source venv/bin/activate                                    │
│         [✓] CHECKPOINT: Python environment active                           │
│     │                                                                       │
│     [→] STEP 06: Start backend server                                       │
│         Action: uvicorn cia_sie.api.app:app --port 8000                     │
│         [⇢] Background process started                                      │
│         PID stored in: pids/backend.pid                                     │
│     │                                                                       │
│     [→] STEP 07: Wait for backend health                                    │
│         File: scripts/launcher/health-check.sh                              │
│         Action: Poll GET /health every 1s, max 30 attempts                  │
│         [↺] Retry loop until 200 OK                                         │
│         [⚠] Failure after 30s → EXIT with error                            │
│         [✓] CHECKPOINT: Backend healthy                                     │
│     │                                                                       │
│     [→] STEP 08: Initialize database                                        │
│         File: src/cia_sie/dal/database.py                                   │
│         Action: SQLAlchemy engine.connect()                                 │
│         Action: Run pending Alembic migrations                              │
│         [📁] Database: data/cia_sie.db                                      │
│         [✓] CHECKPOINT: Database ready                                      │
│     │                                                                       │
│     [◆] STEP 09: Check ngrok enabled?                                       │
│         │                                                                   │
│         ├─[YES]→ STEP 10a: Start ngrok                                      │
│         │        Action: ngrok http 8000                                    │
│         │        PID stored in: pids/ngrok.pid                              │
│         │        Retrieve public URL                                        │
│         │                                                                   │
│         └─[NO]─→ STEP 10b: Skip ngrok                                       │
│     │                                                                       │
│     [◆] STEP 11: Check frontend enabled?                                    │
│         │                                                                   │
│         ├─[YES]→ STEP 12a: Start frontend                                   │
│         │        Action: npm run dev                                        │
│         │        PID stored in: pids/frontend.pid                           │
│         │                                                                   │
│         └─[NO]─→ STEP 12b: Skip frontend                                    │
│     │                                                                       │
│     [→] STEP 13: Display status                                             │
│         Action: Print service URLs, PIDs                                    │
│     │                                                                       │
│     [→] STEP 14: Open browser                                               │
│         Action: open http://localhost:8000/docs                             │
│     │                                                                       │
│     [●] OPERATIONAL STATE                                                   │
│         System running, all services active                                 │
│         Monitoring loop: wait for Ctrl+C                                    │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2.2 TRACE-002: Webhook Signal Ingestion

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-002: SIGNAL INGESTION CIRCUIT                                       │
│  Duration: ~200ms | Steps: 12 | Checkpoints: 5                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IGNITION                                                                   │
│  ════════                                                                   │
│                                                                             │
│  [EXTERNAL] TradingView alert fires                                         │
│     │                                                                       │
│     [🌐] STEP 01: HTTP POST to /webhook/tradingview/GOLD_01A                │
│         File: src/cia_sie/webhooks/tradingview_receiver.py                  │
│         Payload: {"chart_id": "GOLD_01A", "direction": "BULLISH", ...}      │
│     │                                                                       │
│     [→] STEP 02: Pydantic validation                                        │
│         Model: PrimarySignalPayload or HTFStructurePayload                  │
│         [⚠] Failure: ValidationError → Return 400                          │
│         [✓] CHECKPOINT: Payload valid                                       │
│     │                                                                       │
│     [→] STEP 03: Chart lookup                                               │
│         File: src/cia_sie/dal/repositories.py                               │
│         Action: SELECT chart WHERE chart_id = 'GOLD_01A'                    │
│         [📁] Database read                                                  │
│         [⚠] Failure: Chart not found → Return 404                          │
│     │                                                                       │
│     [→] STEP 04: Signal normalization                                       │
│         File: src/cia_sie/ingestion/signal_normalizer.py                    │
│         Action: Map payload fields to Signal model                          │
│         Action: Normalize direction enum                                    │
│         Action: Calculate derived fields                                    │
│         [✓] CHECKPOINT: Signal normalized                                   │
│     │                                                                       │
│     [→] STEP 05: Freshness calculation                                      │
│         File: src/cia_sie/ingestion/freshness.py                            │
│         Action: Compare timestamp to now()                                  │
│         Result: FRESH (< 1 hour old)                                        │
│     │                                                                       │
│     [→] STEP 06: Fetch existing signals                                     │
│         File: src/cia_sie/dal/repositories.py                               │
│         Action: SELECT signals WHERE instrument_id = X                      │
│         [📁] Database read                                                  │
│     │                                                                       │
│     [→] STEP 07: Contradiction detection                                    │
│         File: src/cia_sie/exposure/contradiction_detector.py                │
│         Action: Compare new signal direction with existing                  │
│         [◆] If conflict found:                                              │
│             Create Contradiction(signal_a, signal_b)                        │
│             [✓] CHECKPOINT: Contradiction EXPOSED (not resolved)            │
│     │                                                                       │
│     [→] STEP 08: Confirmation detection                                     │
│         File: src/cia_sie/exposure/confirmation_detector.py                 │
│         Action: Compare new signal direction with existing                  │
│         [◆] If alignment found:                                             │
│             Create Confirmation(signal_a, signal_b)                         │
│             Calculate confidence_exposure                                   │
│     │                                                                       │
│     [→] STEP 09: Begin transaction                                          │
│         File: src/cia_sie/dal/database.py                                   │
│         Action: session.begin()                                             │
│     │                                                                       │
│     [→] STEP 10: Persist signal                                             │
│         Action: INSERT INTO signals                                         │
│         [📁] Database write                                                 │
│     │                                                                       │
│     [→] STEP 11: Persist contradictions/confirmations                       │
│         Action: INSERT INTO contradictions (if any)                         │
│         Action: INSERT INTO confirmations (if any)                          │
│         [📁] Database write                                                 │
│     │                                                                       │
│     [→] STEP 12: Commit transaction                                         │
│         Action: session.commit()                                            │
│         [⚠] Failure: IntegrityError → ROLLBACK                             │
│         [✓] CHECKPOINT: Data persisted                                      │
│     │                                                                       │
│     [●] RETURN HTTP 200                                                     │
│         Response: {"status": "processed", "signal_id": 123}                 │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2.3 TRACE-003: Narrative Generation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-003: NARRATIVE GENERATION CIRCUIT                                    │
│  Duration: ~3-5 seconds | Steps: 16 | Checkpoints: 7                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IGNITION                                                                   │
│  ════════                                                                   │
│                                                                             │
│  [USER] Requests analysis for instrument                                    │
│     │                                                                       │
│     [→] STEP 01: HTTP GET /api/narratives/{instrument_id}                   │
│         File: src/cia_sie/api/routes/narratives.py                          │
│     │                                                                       │
│     [→] STEP 02: Authenticate request                                       │
│         [⚠] Failure: 401 Unauthorized                                      │
│         [✓] CHECKPOINT: Authenticated                                       │
│     │                                                                       │
│     [→] STEP 03: Fetch instrument                                           │
│         File: src/cia_sie/dal/repositories.py                               │
│         Action: SELECT instrument WHERE id = X                              │
│         [📁] Database read                                                  │
│         [⚠] Failure: 404 Not Found                                         │
│     │                                                                       │
│     [→] STEP 04: Fetch all signals                                          │
│         Action: SELECT signals WHERE instrument_id = X                      │
│         [📁] Database read                                                  │
│     │                                                                       │
│     [→] STEP 05: Fetch contradictions                                       │
│         Action: SELECT contradictions WHERE instrument_id = X               │
│         [📁] Database read                                                  │
│     │                                                                       │
│     [→] STEP 06: Fetch confirmations                                        │
│         Action: SELECT confirmations WHERE instrument_id = X                │
│         [📁] Database read                                                  │
│         [✓] CHECKPOINT: Data assembled                                      │
│     │                                                                       │
│     [→] STEP 07: Build system prompt                                        │
│         File: src/cia_sie/ai/prompt_builder.py                              │
│         Include: CR-001, CR-002, CR-003 (Constitutional Rules)              │
│         Include: Forbidden patterns list                                    │
│     │                                                                       │
│     [→] STEP 08: Build user prompt                                          │
│         Action: Format signals as markdown tables                           │
│         Action: Format contradictions as conflicts                          │
│         Action: Format confirmations as alignments                          │
│         [✓] CHECKPOINT: Prompts constructed                                 │
│     │                                                                       │
│     [→] STEP 09: Check AI budget                                            │
│         File: src/cia_sie/ai/model_registry.py                              │
│         Action: SELECT remaining_budget FROM ai_budget                      │
│         [📁] Database read                                                  │
│     │                                                                       │
│     [→] STEP 10: Select model                                               │
│         [◆] If budget high → claude-sonnet-4-20250514                                │
│         [◆] If budget low → claude-3-haiku                                  │
│         [⚠] If budget zero → Return cached narrative                       │
│         [✓] CHECKPOINT: Model selected                                      │
│     │                                                                       │
│     [🌐] STEP 11: Call Claude API                                           │
│         File: src/cia_sie/ai/claude_client.py                               │
│         Action: POST api.anthropic.com/v1/messages                          │
│         [⚠] Failure: Circuit breaker check                                 │
│         [↺] Retry: 3 attempts with exponential backoff                     │
│         [⚠] Failure after retries → Return error                           │
│     │                                                                       │
│     [→] STEP 12: Parse response                                             │
│         Action: Extract content from Claude response                        │
│         [✓] CHECKPOINT: Response received                                   │
│     │                                                                       │
│     [→] STEP 13: CONSTITUTIONAL VALIDATION                                  │
│         File: src/cia_sie/ai/response_validator.py                          │
│         *** CRITICAL GATE ***                                               │
│         │                                                                   │
│         ├── Check CR-001: No "should", "must", "recommend"                  │
│         ├── Check CR-002: Contradictions exposed, not resolved              │
│         └── Check CR-003: Descriptive only, not prescriptive                │
│         │                                                                   │
│         [◆] If VIOLATION detected:                                          │
│             Log violation details                                           │
│             [↺] Regenerate with stronger prompt (max 3x)                    │
│             [⚠] Still failing → Return error to user                       │
│         │                                                                   │
│         [✓] CHECKPOINT: Constitutional compliance verified                  │
│     │                                                                       │
│     [→] STEP 14: Track usage                                                │
│         File: src/cia_sie/ai/usage_tracker.py                               │
│         Action: INSERT INTO ai_usage (tokens, cost, model)                  │
│         Action: UPDATE ai_budget SET remaining = remaining - cost           │
│         [📁] Database write                                                 │
│     │                                                                       │
│     [→] STEP 15: Persist narrative                                          │
│         Action: INSERT INTO narratives                                      │
│         [📁] Database write                                                 │
│         [✓] CHECKPOINT: Narrative persisted                                 │
│     │                                                                       │
│     [→] STEP 16: Format response                                            │
│         Action: Convert markdown to HTML                                    │
│         Action: Add metadata (timestamp, model, tokens)                     │
│     │                                                                       │
│     [●] RETURN HTTP 200                                                     │
│         Response: {"narrative": "<html>...", "meta": {...}}                 │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2.4 TRACE-004: Dashboard Assembly

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-004: DASHBOARD ASSEMBLY CIRCUIT                                      │
│  Duration: ~500ms | Steps: 10 | Checkpoints: 4                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IGNITION                                                                   │
│  ════════                                                                   │
│                                                                             │
│  [USER] Opens dashboard in browser                                          │
│     │                                                                       │
│     [→] STEP 01: React app loads                                            │
│         Action: index.html → main.tsx → App.tsx                             │
│     │                                                                       │
│     [→] STEP 02: React Query cache check                                    │
│         [◆] If cache valid (< 5 min) → Use cached data                      │
│         [◆] If cache stale → Proceed to fetch                               │
│     │                                                                       │
│     [⇢] STEP 03: Parallel API calls (React Query)                           │
│         │                                                                   │
│         ├─[⇢] GET /api/instruments                                          │
│         ├─[⇢] GET /api/signals?fresh=true                                   │
│         ├─[⇢] GET /api/relationships                                        │
│         └─[⇢] GET /api/baskets                                              │
│         │                                                                   │
│         [✓] CHECKPOINT: All requests dispatched                             │
│     │                                                                       │
│     [→] STEP 04-07: Backend processes (parallel)                            │
│         │                                                                   │
│         ├── instruments.py → [📁] SELECT * FROM instruments                 │
│         ├── signals.py → [📁] SELECT * FROM signals WHERE fresh             │
│         ├── relationships.py → [📁] SELECT contradictions, confirms         │
│         └── baskets.py → [📁] SELECT baskets JOIN items                     │
│     │                                                                       │
│     [→] STEP 08: Responses received                                         │
│         Action: React Query caches all responses                            │
│         [✓] CHECKPOINT: Data fetched                                        │
│     │                                                                       │
│     [→] STEP 09: Component rendering                                        │
│         │                                                                   │
│         ├── <Dashboard>                                                     │
│         │   ├── <InstrumentList data={instruments}>                         │
│         │   ├── <SignalGrid data={signals}>                                 │
│         │   ├── <ContradictionPanel data={contradictions}>                  │
│         │   ├── <ConfirmationPanel data={confirmations}>                    │
│         │   └── <BasketSidebar data={baskets}>                              │
│         │                                                                   │
│         [✓] CHECKPOINT: Components rendered                                 │
│     │                                                                       │
│     [→] STEP 10: Interactive state                                          │
│         Action: User can click, filter, sort                                │
│         Action: Background polling every 30s for fresh data                 │
│     │                                                                       │
│     [●] DASHBOARD OPERATIONAL                                               │
│         All data displayed, updates streaming                               │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5.3 MERCURY COMPLETE CIRCUIT TRACES

### 5.3.1 TRACE-M001: Mercury Startup

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-M001: MERCURY STARTUP CIRCUIT                                        │
│  Duration: ~3 seconds | Steps: 12 | Checkpoints: 6                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IGNITION                                                                   │
│  ════════                                                                   │
│                                                                             │
│  [USER] Executes: python -m mercury --web                                   │
│     │                                                                       │
│     [→] STEP 01: Main entry point                                           │
│         File: src/mercury/main.py                                           │
│         Action: Parse CLI arguments (--web, --check, default=REPL)          │
│     │                                                                       │
│     [→] STEP 02: Load configuration                                         │
│         File: src/mercury/core/config.py                                    │
│         Action: Load .env file                                              │
│         Action: Create MercurySettings from env vars                        │
│         [⚠] Failure: Missing required vars → EXIT with error               │
│         [✓] CHECKPOINT: Configuration loaded                                │
│     │                                                                       │
│     [→] STEP 03: Validate configuration                                     │
│         File: src/mercury/core/validation.py                                │
│         Action: Check API key formats                                       │
│         Action: Check endpoint validity                                     │
│         [⚠] Failure: Invalid format → EXIT with error                      │
│         [✓] CHECKPOINT: Configuration valid                                 │
│     │                                                                       │
│     [→] STEP 04: Initialize structured logging                              │
│         File: src/mercury/core/logging.py                                   │
│         Action: Configure JSON logger with correlation IDs                  │
│     │                                                                       │
│     [→] STEP 05: Perform launch readiness check                             │
│         File: src/mercury/core/startup.py                                   │
│         │                                                                   │
│         ├─[→] STEP 05a: Verify Kite API                                     │
│         │     [◆] Mock mode? → Return MOCK_MODE status                      │
│         │     [🌐] Call Kite API test endpoint                              │
│         │     [⚠] Failure: Return FAILED status                            │
│         │     [✓] Success: Return AUTHENTICATED status                      │
│         │                                                                   │
│         └─[→] STEP 05b: Verify Anthropic API                                │
│               [🌐] Send test message to Claude                              │
│               [⚠] Failure: Return FAILED status                            │
│               [✓] Success: Return AUTHENTICATED status                      │
│         │                                                                   │
│         [✓] CHECKPOINT: API verification complete                           │
│     │                                                                       │
│     [→] STEP 06: Display status report                                      │
│         Action: Print formatted status table                                │
│         │                                                                   │
│         ┌─────────────────────────────────────────────────────────┐        │
│         │  ═══════════════════════════════════════════════════    │        │
│         │   MERCURY LAUNCH READINESS CHECK                        │        │
│         │  ═══════════════════════════════════════════════════    │        │
│         │                                                         │        │
│         │   Kite Connect     ✅ AUTHENTICATED (234ms)             │        │
│         │   Anthropic Claude ✅ AUTHENTICATED (567ms)             │        │
│         │                                                         │        │
│         │   Status: READY FOR LAUNCH                              │        │
│         │  ═══════════════════════════════════════════════════    │        │
│         └─────────────────────────────────────────────────────────┘        │
│     │                                                                       │
│     [→] STEP 07: Determine readiness                                        │
│         [◆] If any FAILED → Set ready=False, add to errors                  │
│         [◆] If any NOT_CONFIGURED → Add to warnings                         │
│         [◆] If all OK → Set ready=True                                      │
│         [✓] CHECKPOINT: Readiness determined                                │
│     │                                                                       │
│     [◆] STEP 08: Launch decision                                            │
│         │                                                                   │
│         ├─[NOT READY]→ STEP 09a: Exit with error                            │
│         │              Display errors, suggest fixes                        │
│         │              [●] EXIT CODE 1                                      │
│         │                                                                   │
│         └─[READY]────→ STEP 09b: Continue to server start                   │
│     │                                                                       │
│     [→] STEP 10: Initialize components                                      │
│         Action: Create ChatEngine instance                                  │
│         Action: Create KiteAdapter instance                                 │
│         Action: Create AIEngine instance                                    │
│         [✓] CHECKPOINT: Components initialized                              │
│     │                                                                       │
│     [→] STEP 11: Start FastAPI server                                       │
│         File: src/mercury/api/app.py                                        │
│         Action: uvicorn.run(app, host="0.0.0.0", port=8888)                 │
│     │                                                                       │
│     [→] STEP 12: Open browser (if web mode)                                 │
│         Action: open http://localhost:8888                                  │
│     │                                                                       │
│     [●] OPERATIONAL STATE                                                   │
│         Mercury web interface running                                       │
│         Ready to receive chat queries                                       │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3.2 TRACE-M002: Chat Query Processing

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-M002: CHAT QUERY PROCESSING CIRCUIT                                  │
│  Duration: ~2-4 seconds | Steps: 14 | Checkpoints: 6                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IGNITION                                                                   │
│  ════════                                                                   │
│                                                                             │
│  [USER] Types: "What is RELIANCE trading at?"                               │
│     │                                                                       │
│     [→] STEP 01: WebSocket message received                                 │
│         File: src/mercury/api/app.py                                        │
│         Route: /ws/chat                                                     │
│         Payload: {"type": "message", "content": "What is..."}               │
│     │                                                                       │
│     [→] STEP 02: Parse query                                                │
│         File: src/mercury/chat/engine.py                                    │
│         Function: _parse_query()                                            │
│         │                                                                   │
│         ├── Extract symbols: ["RELIANCE"]                                   │
│         ├── Identify intent: "price_check"                                  │
│         └── Validate symbols                                                │
│         │                                                                   │
│         [✓] CHECKPOINT: Query parsed                                        │
│     │                                                                       │
│     [→] STEP 03: Check circuit breaker (Kite)                               │
│         File: src/mercury/core/resilience.py                                │
│         [◆] If OPEN → Skip to degraded response                             │
│         [◆] If CLOSED → Proceed to fetch                                    │
│     │                                                                       │
│     [🌐] STEP 04: Fetch market data                                         │
│         File: src/mercury/kite/adapter.py                                   │
│         Action: kite.get_quote("NSE:RELIANCE")                              │
│         [⚠] Failure: Record failure, check breaker                         │
│         [↺] Retry with exponential backoff                                 │
│         │                                                                   │
│         [✓] CHECKPOINT: Market data fetched                                 │
│         Result: Quote(last_price=2450.50, change=+1.2%, ...)                │
│     │                                                                       │
│     [→] STEP 05: Get conversation context                                   │
│         File: src/mercury/chat/conversation.py                              │
│         Function: get_context()                                             │
│         Action: Retrieve last N messages                                    │
│         Action: Format for AI consumption                                   │
│     │                                                                       │
│     [→] STEP 06: Build system prompt                                        │
│         File: src/mercury/ai/prompts.py                                     │
│         Constant: SYSTEM_PROMPT                                             │
│         │                                                                   │
│         *** MERCURY CONSTITUTION (UNRESTRICTED) ***                         │
│         - MR-001: May provide opinions                                      │
│         - MR-002: May include recommendations                               │
│         - MR-003: May synthesize and conclude                               │
│         - MR-004: Maintains conversation context                            │
│         - MR-005: Expresses uncertainty honestly                            │
│     │                                                                       │
│     [→] STEP 07: Build user prompt                                          │
│         File: src/mercury/ai/prompts.py                                     │
│         Function: build_user_prompt()                                       │
│         │                                                                   │
│         Include:                                                            │
│         - User query                                                        │
│         - Market data bundle (formatted)                                    │
│         - Conversation history                                              │
│         │                                                                   │
│         [✓] CHECKPOINT: Prompts constructed                                 │
│     │                                                                       │
│     [→] STEP 08: Check circuit breaker (Anthropic)                          │
│         File: src/mercury/core/resilience.py                                │
│         [◆] If OPEN → Return error message                                  │
│         [◆] If CLOSED → Proceed to generate                                 │
│     │                                                                       │
│     [🌐] STEP 09: Call Claude API                                           │
│         File: src/mercury/ai/engine.py                                      │
│         Action: anthropic.messages.create()                                 │
│         Model: claude-sonnet-4-20250514                                              │
│         [⚠] Failure: Record failure, check breaker                         │
│         [↺] Retry with exponential backoff                                 │
│         │                                                                   │
│         [✓] CHECKPOINT: AI response received                                │
│     │                                                                       │
│     [→] STEP 10: NO constitutional validation                               │
│         *** MERCURY BYPASS ***                                              │
│         Response passed through directly                                    │
│         No CR-001/002/003 checks applied                                    │
│     │                                                                       │
│     [→] STEP 11: Update conversation                                        │
│         File: src/mercury/chat/conversation.py                              │
│         Function: add_message()                                             │
│         Action: Append user message                                         │
│         Action: Append AI response                                          │
│         │                                                                   │
│         [✓] CHECKPOINT: Conversation updated                                │
│     │                                                                       │
│     [→] STEP 12: Record metrics                                             │
│         File: src/mercury/core/metrics.py                                   │
│         Action: Increment queries_total                                     │
│         Action: Record latency histogram                                    │
│     │                                                                       │
│     [→] STEP 13: Format response                                            │
│         Create ChatResponse:                                                │
│         - message: AI response text                                         │
│         - data_used: list of symbols fetched                                │
│         - confidence: (if AI included)                                      │
│     │                                                                       │
│     [→] STEP 14: Send via WebSocket                                         │
│         Action: websocket.send_json(response)                               │
│     │                                                                       │
│     [●] USER SEES RESPONSE                                                  │
│         "RELIANCE is currently trading at ₹2,450.50, up 1.2%..."            │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3.3 TRACE-M003: Multi-Turn Conversation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-M003: MULTI-TURN CONVERSATION CIRCUIT                                │
│  Duration: ~10 seconds total | Steps: 8 per turn | Checkpoints: 3          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TURN 1                                                                     │
│  ══════                                                                     │
│                                                                             │
│  [USER] "What is RELIANCE trading at?"                                      │
│     │                                                                       │
│     [→] Process query (TRACE-M002 abbreviated)                              │
│         Symbols: ["RELIANCE"]                                               │
│         Kite: Fetch quote                                                   │
│         AI: Generate response                                               │
│     │                                                                       │
│     [→] Store in conversation                                               │
│         history = [                                                         │
│           {role: "user", content: "What is RELIANCE..."},                   │
│           {role: "assistant", content: "RELIANCE is at ₹2450..."}           │
│         ]                                                                   │
│     │                                                                       │
│     [●] RESPONSE: "RELIANCE is currently at ₹2,450.50..."                   │
│                                                                             │
│  TURN 2                                                                     │
│  ══════                                                                     │
│                                                                             │
│  [USER] "What about its 52-week high?"                                      │
│     │                                                                       │
│     [→] Parse query                                                         │
│         Direct symbol: None                                                 │
│         Context reference: "its" → RELIANCE (from history)                  │
│         [✓] CHECKPOINT: Context preserved                                   │
│     │                                                                       │
│     [→] Get conversation context                                            │
│         Previous exchange included in prompt                                │
│     │                                                                       │
│     [🌐] Kite: Fetch OHLC with 52-week range                                │
│     │                                                                       │
│     [🌐] AI: Generate with context                                          │
│         AI knows "it" = RELIANCE from history                               │
│     │                                                                       │
│     [→] Store in conversation                                               │
│         history = [                                                         │
│           {role: "user", content: "What is RELIANCE..."},                   │
│           {role: "assistant", content: "RELIANCE is at ₹2450..."},          │
│           {role: "user", content: "What about its 52-week high?"},          │
│           {role: "assistant", content: "RELIANCE's 52-week high..."}        │
│         ]                                                                   │
│     │                                                                       │
│     [●] RESPONSE: "RELIANCE's 52-week high is ₹2,850..."                    │
│                                                                             │
│  TURN 3                                                                     │
│  ══════                                                                     │
│                                                                             │
│  [USER] "Compare it to INFY"                                                │
│     │                                                                       │
│     [→] Parse query                                                         │
│         New symbol: ["INFY"]                                                │
│         Context reference: "it" → RELIANCE                                  │
│         [✓] CHECKPOINT: Multi-symbol context                                │
│     │                                                                       │
│     [🌐] Kite: Fetch quotes for RELIANCE and INFY                           │
│     │                                                                       │
│     [🌐] AI: Generate comparison                                            │
│         Full conversation context provided                                  │
│         AI understands comparison request                                   │
│     │                                                                       │
│     [●] RESPONSE: "Comparing RELIANCE (₹2,450) to INFY (₹1,650)..."         │
│                                                                             │
│  CIRCUIT COMPLETE ✓                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5.4 CROSS-SYSTEM TRACE

### 5.4.1 TRACE-X001: Shared External API Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TRACE-X001: EXTERNAL API SHARED FLOW                                       │
│  Shows how both systems interact with external APIs                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                         ┌─────────────────┐            │
│  │    CIA-SIE      │                         │    MERCURY      │            │
│  └────────┬────────┘                         └────────┬────────┘            │
│           │                                           │                     │
│           │  KITE API (EXT-001)                       │                     │
│           │  ══════════════════                       │                     │
│           │                                           │                     │
│           │   CIA-SIE Usage:                         │   Mercury Usage:     │
│           │   - platforms/kite.py                    │   - kite/adapter.py  │
│           │   - Signal enrichment                    │   - Live quotes      │
│           │   - Price validation                     │   - Positions        │
│           │   - OAuth via web flow                   │   - Holdings         │
│           │                                           │   - Historical       │
│           │                                           │                     │
│           └──────────────┬───────────────────────────┘                     │
│                          │                                                  │
│                          ▼                                                  │
│           ┌──────────────────────────────┐                                 │
│           │     ZERODHA KITE API         │                                 │
│           │     api.kite.trade           │                                 │
│           │                              │                                 │
│           │  Endpoints Used:             │                                 │
│           │  - /quote                    │                                 │
│           │  - /ltp                      │                                 │
│           │  - /ohlc                     │                                 │
│           │  - /positions                │                                 │
│           │  - /holdings                 │                                 │
│           │  - /instruments              │                                 │
│           └──────────────────────────────┘                                 │
│                                                                             │
│           │                                           │                     │
│           │  ANTHROPIC API (EXT-002)                  │                     │
│           │  ════════════════════════                 │                     │
│           │                                           │                     │
│           │   CIA-SIE Usage:                         │   Mercury Usage:     │
│           │   - ai/claude_client.py                  │   - ai/engine.py     │
│           │   - Narrative generation                 │   - Chat responses   │
│           │   - VALIDATED (CR-001/002/003)           │   - UNRESTRICTED     │
│           │   - Budget-controlled                    │   - Direct pass      │
│           │                                           │                     │
│           └──────────────┬───────────────────────────┘                     │
│                          │                                                  │
│                          ▼                                                  │
│           ┌──────────────────────────────┐                                 │
│           │     ANTHROPIC CLAUDE API     │                                 │
│           │   api.anthropic.com          │                                 │
│           │                              │                                 │
│           │  Endpoint Used:              │                                 │
│           │  - /v1/messages              │                                 │
│           │                              │                                 │
│           │  Models:                     │                                 │
│           │  - claude-sonnet-4-20250514 (primary)    │                                 │
│           │  - claude-3-haiku (fallback) │                                 │
│           └──────────────────────────────┘                                 │
│                                                                             │
│  KEY DIFFERENCE:                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  CIA-SIE: AI response → CONSTITUTIONAL VALIDATION → If pass → User  │   │
│  │  MERCURY: AI response → DIRECT DELIVERY → User                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5.5 CIRCUIT COMPLETION VERIFICATION

### All Circuits Verified

| Trace ID | System | Circuit | Steps | Complete |
|----------|--------|---------|-------|----------|
| TRACE-001 | CIA-SIE | Startup | 14 | ✅ |
| TRACE-002 | CIA-SIE | Signal Ingestion | 12 | ✅ |
| TRACE-003 | CIA-SIE | Narrative Gen | 16 | ✅ |
| TRACE-004 | CIA-SIE | Dashboard | 10 | ✅ |
| TRACE-M001 | Mercury | Startup | 12 | ✅ |
| TRACE-M002 | Mercury | Chat Query | 14 | ✅ |
| TRACE-M003 | Mercury | Multi-Turn | 8/turn | ✅ |
| TRACE-X001 | Both | External API | - | ✅ |

**TOTAL: 8 COMPLETE CIRCUITS DOCUMENTED**

---

## 5.6 CHAPTER HANDOFF

**This chapter established:**
- 8 complete end-to-end circuit traces
- Every action from ignition to completion
- All checkpoints and failure points marked
- Cross-system integration documented

**Next chapter will detail:**
- Pre-flight validation checklist
- Launch readiness verification
- Final approval gates

---

**Predecessor:** [04_FAILURE_MODE_ANALYSIS.md](./04_FAILURE_MODE_ANALYSIS.md)
**Successor:** [06_LAUNCH_READINESS_CHECKLIST.md](./06_LAUNCH_READINESS_CHECKLIST.md)

---

*"Action A → Action B → ... → Circuit Complete."*
