# CHAPTER 04: FAILURE MODE ANALYSIS

**Document ID:** ASM-CH04-2026
**Classification:** FAULT TOLERANCE DOCUMENTATION
**Predecessor:** 03_INTEGRATION_TEST_PROTOCOL.md
**Successor:** 05_END_TO_END_TRACE.md

---

## Purpose

Every break point mapped with failover routing. Like avionics systems, if one node fails, the entire chain is visible for diagnosis and recovery paths are pre-defined.

---

## 4.1 FAILURE MODE TAXONOMY

### Severity Classification

| Level | Name | Description | Response Time | Example |
|-------|------|-------------|---------------|---------|
| **SEV-1** | CRITICAL | System inoperable | Immediate | Database down |
| **SEV-2** | MAJOR | Core feature unavailable | <1 hour | AI API unavailable |
| **SEV-3** | MINOR | Degraded functionality | <4 hours | Stale data |
| **SEV-4** | COSMETIC | No operational impact | <24 hours | UI glitch |

### Failure Categories

| Category | Code | Description |
|----------|------|-------------|
| **NETWORK** | NET | Network connectivity failures |
| **AUTH** | AUTH | Authentication/authorization failures |
| **DATA** | DATA | Data integrity/availability failures |
| **API** | API | External API failures |
| **SYSTEM** | SYS | Internal system failures |
| **CONFIG** | CFG | Configuration failures |

---

## 4.2 CIA-SIE FAILURE MODES

### 4.2.1 External API Failures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-API-001                                 │
│                    Claude API Unavailable                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: API                                                              │
│  Severity: SEV-2 (MAJOR)                                                    │
│  Component: AI Layer (AI-001)                                               │
│  Detection: HTTP 500/502/503 from api.anthropic.com                         │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • FLOW-002: Narrative Generation → BLOCKED                         │   │
│  │  • API-008: Narrative endpoint → Returns error                       │   │
│  │  • API-010: AI endpoints → Returns error                             │   │
│  │  • API-011: Chat interface → Returns error                           │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • FLOW-001: Signal Ingestion → CONTINUES                            │   │
│  │  • FLOW-003: Dashboard Assembly → PARTIAL (no narratives)            │   │
│  │  • All CRUD operations → CONTINUE                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  PRIMARY RESPONSE:                                                   │   │
│  │  1. Circuit breaker OPEN after 5 consecutive failures               │   │
│  │  2. Return cached narrative if available (< 24 hours old)            │   │
│  │  3. Display: "AI analysis temporarily unavailable"                   │   │
│  │                                                                      │   │
│  │  SECONDARY RESPONSE:                                                 │   │
│  │  4. Fall back to cheaper model (sonnet → haiku)                      │   │
│  │  5. Retry with exponential backoff (1s, 2s, 4s, 8s)                  │   │
│  │                                                                      │   │
│  │  TERTIARY RESPONSE:                                                  │   │
│  │  6. Queue request for later processing                               │   │
│  │  7. Notify user when narrative becomes available                     │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Circuit breaker HALF-OPEN after 60 seconds                        │   │
│  │  • Test request sent                                                 │   │
│  │  • On success: Circuit CLOSED, normal operation resumes              │   │
│  │  • On failure: Circuit OPEN, wait another 60 seconds                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  MONITORING                                                                 │
│  ══════════                                                                 │
│  • Alert: ai_api_error_rate > 10% for 5 minutes                            │
│  • Log: ERROR level with full context                                       │
│  • Metric: anthropic_api_failures_total                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-API-002                                 │
│                    TradingView Webhook Failure                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: API                                                              │
│  Severity: SEV-3 (MINOR)                                                    │
│  Component: Webhook Receiver (ING-002)                                      │
│  Detection: Malformed JSON, missing fields, invalid chart_id               │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • FLOW-001: Signal Ingestion → PARTIAL (one signal missed)          │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • All other flows continue normally                                 │   │
│  │  • Existing signals remain valid                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. Return HTTP 400 with descriptive error message                   │   │
│  │  2. Log full webhook payload for debugging                           │   │
│  │  3. Alert on webhook_error_rate > 5% for 10 minutes                  │   │
│  │  4. Continue processing other webhooks normally                      │   │
│  │  5. Retry not applicable (TradingView does not retry)                │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Manual review of failed webhooks from logs                        │   │
│  │  • Fix TradingView alert configuration if pattern detected           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2.2 Database Failures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-DATA-001                                │
│                    Database Connection Lost                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: DATA                                                             │
│  Severity: SEV-1 (CRITICAL)                                                 │
│  Component: Data Access Layer (DAL-001)                                     │
│  Detection: SQLAlchemy connection exception, timeout                        │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • ALL FLOWS → BLOCKED                                               │   │
│  │  • No reads, no writes possible                                      │   │
│  │  • System effectively inoperable                                     │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • Health endpoint (returns UNHEALTHY status)                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  IMMEDIATE:                                                          │   │
│  │  1. Log CRITICAL error with full stack trace                         │   │
│  │  2. Return HTTP 503 for all data-dependent endpoints                 │   │
│  │  3. Health endpoint returns degraded status                          │   │
│  │                                                                      │   │
│  │  RECOVERY ATTEMPT:                                                   │   │
│  │  4. Connection pool automatic reconnect (3 attempts)                 │   │
│  │  5. If SQLite: Check file permissions, disk space                    │   │
│  │  6. If still failing: Manual intervention required                   │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Check cia_sie.db file exists                                      │   │
│  │  • Check disk space (df -h)                                          │   │
│  │  • Restart application                                               │   │
│  │  • If corrupt: Restore from backup                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  MONITORING                                                                 │
│  ══════════                                                                 │
│  • Alert: IMMEDIATE on database connection failure                         │
│  • Log: CRITICAL level                                                      │
│  • Metric: database_connection_errors_total                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-DATA-002                                │
│                    Data Integrity Violation                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: DATA                                                             │
│  Severity: SEV-2 (MAJOR)                                                    │
│  Component: ORM Models (DAL-002)                                            │
│  Detection: Foreign key violation, unique constraint violation              │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • Specific write operation → BLOCKED                                │   │
│  │  • Related entity chain may be affected                              │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • Read operations continue                                          │   │
│  │  • Other write operations unaffected                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. Transaction ROLLBACK                                             │   │
│  │  2. Return HTTP 409 Conflict with details                            │   │
│  │  3. Log full constraint violation details                            │   │
│  │  4. User shown actionable error message                              │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Review data model relationships                                   │   │
│  │  • Fix data inconsistency at source                                  │   │
│  │  • Retry operation after fix                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2.3 Constitutional Failures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-CONST-001                               │
│                    AI Response Constitutional Violation                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: SYSTEM                                                           │
│  Severity: SEV-1 (CRITICAL)                                                 │
│  Component: Response Validator (AI-003)                                     │
│  Detection: CR-001/002/003 violation detected in AI response                │
│                                                                             │
│  *** THIS IS NOT A BUG - THIS IS THE SYSTEM WORKING CORRECTLY ***          │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • Current narrative request → BLOCKED (correct behavior)            │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • All other flows continue                                          │   │
│  │  • System integrity maintained                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AUTOMATIC RESPONSE:                                                 │   │
│  │  1. REJECT response completely                                       │   │
│  │  2. Log violation with full details (for prompt tuning)              │   │
│  │  3. Regenerate with adjusted prompt (up to 3 attempts)               │   │
│  │  4. If still violating: Return error to user                         │   │
│  │                                                                      │   │
│  │  USER MESSAGE:                                                       │   │
│  │  "Unable to generate compliant analysis. Please try again."          │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Review prompt templates                                           │   │
│  │  • Strengthen constitutional instructions in system prompt           │   │
│  │  • Consider model change if pattern persists                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  MONITORING                                                                 │
│  ══════════                                                                 │
│  • Alert: constitutional_violations > 5 in 1 hour                          │
│  • Log: WARNING level with violation details                                │
│  • Metric: constitutional_violations_total{rule="CR-001|002|003"}           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4.3 MERCURY FAILURE MODES

### 4.3.1 Kite API Failures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-MKITE-001                               │
│                    Kite API Authentication Failure                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: AUTH                                                             │
│  Severity: SEV-2 (MAJOR)                                                    │
│  Component: Kite Adapter (MKITE-001)                                        │
│  Detection: HTTP 403/401, TokenException                                    │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • MFLOW-001: Chat queries requiring market data → DEGRADED          │   │
│  │  • get_quote(), get_positions(), get_holdings() → BLOCKED            │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • General conversation without market data → CONTINUES              │   │
│  │  • AI responses using cached/mock data → CONTINUES                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  IMMEDIATE:                                                          │   │
│  │  1. Circuit breaker OPEN for Kite API                                │   │
│  │  2. Mark Kite status as FAILED in health                             │   │
│  │  3. Log AUTH error with request details                              │   │
│  │                                                                      │   │
│  │  GRACEFUL DEGRADATION:                                               │   │
│  │  4. AI responds: "Unable to fetch live market data"                  │   │
│  │  5. Offer to continue with general analysis                          │   │
│  │  6. Prompt user to re-authenticate with Kite                         │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • User completes Kite OAuth flow                                    │   │
│  │  • New access_token obtained                                         │   │
│  │  • Circuit breaker resets on successful call                         │   │
│  │                                                                      │   │
│  │  USER MESSAGE:                                                       │   │
│  │  "Your Kite session has expired. Please re-authenticate to           │   │
│  │   access live market data. I can still help with general             │   │
│  │   questions about trading strategies and concepts."                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-MKITE-002                               │
│                    Symbol Not Found                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: DATA                                                             │
│  Severity: SEV-4 (COSMETIC)                                                 │
│  Component: Kite Adapter (MKITE-001)                                        │
│  Detection: SymbolNotFoundError                                             │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • Single symbol query → PARTIAL (that symbol missing)               │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • Other symbols in same query → CONTINUE                            │   │
│  │  • All other system functions → CONTINUE                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │   │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. Log warning with attempted symbol                                │   │
│  │  2. Search for similar symbols (fuzzy match)                         │   │
│  │  3. AI responds with clarification request                           │   │
│  │                                                                      │   │
│  │  USER MESSAGE:                                                       │   │
│  │  "I couldn't find '[SYMBOL]'. Did you mean one of these:             │   │
│  │   RELIANCE, RELIANCEINF, RELIANCENF? Please clarify."                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-MKITE-003                               │
│                    Kite API Rate Limit                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: API                                                              │
│  Severity: SEV-3 (MINOR)                                                    │
│  Component: Kite Adapter (MKITE-001)                                        │
│  Detection: HTTP 429 Too Many Requests                                      │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. Extract Retry-After header                                       │   │
│  │  2. Queue request with delay                                         │   │
│  │  3. Apply exponential backoff (1s, 2s, 4s...)                        │   │
│  │  4. If persistent: Reduce request frequency                          │   │
│  │                                                                      │   │
│  │  USER MESSAGE:                                                       │   │
│  │  "Market data temporarily throttled. Response may be slightly        │   │
│  │   delayed. Please wait a moment..."                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3.2 AI Engine Failures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-MAI-001                                 │
│                    Anthropic API Unavailable                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: API                                                              │
│  Severity: SEV-1 (CRITICAL - for Mercury)                                   │
│  Component: AI Engine (MAI-001)                                             │
│  Detection: HTTP 500/502/503, connection timeout                            │
│                                                                             │
│  IMPACT ANALYSIS                                                            │
│  ═══════════════                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AFFECTED FLOWS:                                                     │   │
│  │  • ALL chat responses → BLOCKED                                      │   │
│  │  • Mercury core function unavailable                                 │   │
│  │                                                                      │   │
│  │  UNAFFECTED FLOWS:                                                   │   │
│  │  • Health endpoints → CONTINUE                                       │   │
│  │  • Status display → CONTINUE (shows FAILED)                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  IMMEDIATE:                                                          │   │
│  │  1. Circuit breaker OPEN                                             │   │
│  │  2. Return error with clear messaging                                │   │
│  │  3. Log with full context                                            │   │
│  │                                                                      │   │
│  │  RETRY SEQUENCE:                                                     │   │
│  │  4. Retry 3 times with exponential backoff                           │   │
│  │  5. If still failing: Circuit stays OPEN                             │   │
│  │                                                                      │   │
│  │  USER MESSAGE:                                                       │   │
│  │  "AI service temporarily unavailable. Please try again in a          │   │
│  │   few moments. If the issue persists, the service may be             │   │
│  │   experiencing high demand."                                         │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Circuit breaker tests after 60 seconds                            │   │
│  │  • On success: Resume normal operation                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-MAI-002                                 │
│                    Invalid API Key                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: AUTH                                                             │
│  Severity: SEV-1 (CRITICAL)                                                 │
│  Component: AI Engine (MAI-001)                                             │
│  Detection: HTTP 401 Unauthorized                                           │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. FAIL startup if detected during initialization                   │   │
│  │  2. Do NOT retry (wrong key won't become right)                      │   │
│  │  3. Display configuration error message                              │   │
│  │                                                                      │   │
│  │  STARTUP MESSAGE:                                                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │  ❌ LAUNCH READINESS CHECK FAILED                            │    │   │
│  │  │                                                              │    │   │
│  │  │  Anthropic: FAILED                                           │    │   │
│  │  │  Message: API key invalid or authentication failed           │    │   │
│  │  │                                                              │    │   │
│  │  │  Please verify your ANTHROPIC_API_KEY in .env file           │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • User obtains valid API key from console.anthropic.com            │   │
│  │  • Update .env file                                                  │   │
│  │  • Restart application                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3.3 Startup Failures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE: FM-MSTART-001                              │
│                    Configuration Validation Failure                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IDENTIFICATION                                                             │
│  ══════════════                                                             │
│  Category: CONFIG                                                           │
│  Severity: SEV-1 (CRITICAL)                                                 │
│  Component: Core Config (MCORE-001)                                         │
│  Detection: Pydantic ValidationError                                        │
│                                                                             │
│  FAILOVER ROUTING                                                           │
│  ════════════════                                                           │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. FAIL FAST - Do not start with invalid config                     │   │
│  │  2. Display all validation errors                                    │   │
│  │  3. Suggest corrections                                              │   │
│  │                                                                      │   │
│  │  EXAMPLE OUTPUT:                                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │  Configuration Validation Failed:                            │    │   │
│  │  │                                                              │    │   │
│  │  │  1. ANTHROPIC_API_KEY: Field required                        │    │   │
│  │  │  2. KITE_API_KEY: Invalid format (expected 'api_key_xxxx')   │    │   │
│  │  │                                                              │    │   │
│  │  │  Please update your .env file and restart.                   │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                      │   │
│  │  RECOVERY:                                                           │   │
│  │  • Review .env.example for correct format                            │   │
│  │  • Update .env with valid values                                     │   │
│  │  • Restart application                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4.4 FAILURE MODE SUMMARY MATRIX

### Complete Failure Registry

| ID | Component | Failure | Severity | Detection | Recovery |
|----|-----------|---------|----------|-----------|----------|
| FM-API-001 | AI-001 | Claude API Down | SEV-2 | HTTP 5xx | Circuit breaker, cache |
| FM-API-002 | ING-002 | Bad Webhook | SEV-3 | Validation | Log, return 400 |
| FM-DATA-001 | DAL-001 | DB Connection Lost | SEV-1 | Exception | Reconnect, manual |
| FM-DATA-002 | DAL-002 | Constraint Violation | SEV-2 | IntegrityError | Rollback, fix data |
| FM-CONST-001 | AI-003 | CR Violation | SEV-1 | Validator | Reject, regenerate |
| FM-MKITE-001 | MKITE-001 | Kite Auth Fail | SEV-2 | HTTP 401/403 | Re-auth prompt |
| FM-MKITE-002 | MKITE-001 | Symbol Not Found | SEV-4 | Exception | Fuzzy match |
| FM-MKITE-003 | MKITE-001 | Rate Limited | SEV-3 | HTTP 429 | Backoff, queue |
| FM-MAI-001 | MAI-001 | Anthropic Down | SEV-1 | HTTP 5xx | Circuit breaker |
| FM-MAI-002 | MAI-001 | Invalid API Key | SEV-1 | HTTP 401 | Config fix |
| FM-MSTART-001 | MCORE-001 | Bad Config | SEV-1 | Validation | Fix .env |

### Failure Mode Coverage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAILURE MODE COVERAGE                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CATEGORIES COVERED:                                                        │
│  ├── NETWORK (NET)         ✅ Via API failures                              │
│  ├── AUTHENTICATION (AUTH) ✅ Kite, Anthropic                               │
│  ├── DATA (DATA)           ✅ DB, integrity                                 │
│  ├── EXTERNAL API (API)    ✅ All external systems                          │
│  ├── SYSTEM (SYS)          ✅ Constitutional                                │
│  └── CONFIGURATION (CFG)   ✅ Startup validation                            │
│                                                                             │
│  SEVERITY DISTRIBUTION:                                                     │
│  ├── SEV-1 (CRITICAL): 5 failure modes                                      │
│  ├── SEV-2 (MAJOR): 3 failure modes                                         │
│  ├── SEV-3 (MINOR): 2 failure modes                                         │
│  └── SEV-4 (COSMETIC): 1 failure mode                                       │
│                                                                             │
│  RECOVERY PATTERNS:                                                         │
│  ├── Circuit Breaker: 4 failure modes                                       │
│  ├── Retry/Backoff: 3 failure modes                                         │
│  ├── Graceful Degradation: 6 failure modes                                  │
│  ├── Fail Fast: 2 failure modes                                             │
│  └── Manual Intervention: 2 failure modes                                   │
│                                                                             │
│  COVERAGE STATUS: ✅ 100% - ALL BREAK POINTS MAPPED                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4.5 CHAPTER HANDOFF

**This chapter established:**
- Complete failure mode taxonomy
- 11 detailed failure mode analyses
- Failover routing for every break point
- Recovery procedures for each failure

**Next chapter will detail:**
- Complete end-to-end circuit traces
- Action A → Action B → ... → Circuit Complete
- Full journey documentation

---

**Predecessor:** [03_INTEGRATION_TEST_PROTOCOL.md](./03_INTEGRATION_TEST_PROTOCOL.md)
**Successor:** [05_END_TO_END_TRACE.md](./05_END_TO_END_TRACE.md)

---

*"Every break point mapped with failover routing."*
