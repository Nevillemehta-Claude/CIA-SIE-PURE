# CHAPTER 03: INTEGRATION TEST PROTOCOL

**Document ID:** ASM-CH03-2026
**Classification:** VALIDATION PROCEDURES
**Predecessor:** 02_SIGNAL_FLOW_MATRIX.md
**Successor:** 04_FAILURE_MODE_ANALYSIS.md

---

## Purpose

Validation sequences for each junction point. Every connection between nodes verified with specific test procedures.

---

## 3.1 TEST COVERAGE MATRIX

### Complete System Test Registry

| System | Test Files | Test Cases | Junction Coverage |
|--------|-----------|------------|-------------------|
| CIA-SIE | 64 files | 200+ | 100% |
| Mercury | 10 files | 139+ | 100% |
| **TOTAL** | **74 files** | **339+** | **100%** |

---

## 3.2 CIA-SIE INTEGRATION TESTS

### 3.2.1 API Layer Junction Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    API LAYER INTEGRATION TESTS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: API → Service Layer                                              │
│  Test File: tests/integration/test_api_integration.py                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-API-001: Instrument CRUD Operations                            │   │
│  │  ─────────────────────────────────────                               │   │
│  │  Purpose: Verify API → Repository → Database chain                   │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. POST /api/instruments → Create instrument                        │   │
│  │  2. GET /api/instruments/{id} → Verify persisted                     │   │
│  │  3. PUT /api/instruments/{id} → Update instrument                    │   │
│  │  4. GET /api/instruments/{id} → Verify update                        │   │
│  │  5. DELETE /api/instruments/{id} → Remove                            │   │
│  │  6. GET /api/instruments/{id} → Verify 404                           │   │
│  │                                                                      │   │
│  │  Expected: All operations return correct status codes                │   │
│  │  Data persists correctly across operations                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-API-002: Signal Ingestion Chain                                │   │
│  │  ────────────────────────────────                                    │   │
│  │  Purpose: Verify Webhook → Normalizer → Detector → DB                │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. POST /webhook/tradingview/GOLD_01A with valid payload            │   │
│  │  2. Query signals table → Verify signal persisted                    │   │
│  │  3. Query contradictions → Verify detection ran                      │   │
│  │  4. Query confirmations → Verify detection ran                       │   │
│  │                                                                      │   │
│  │  Expected: Signal stored, detections executed                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-API-003: Health Endpoint                                       │   │
│  │  ─────────────────────────────                                       │   │
│  │  Purpose: Verify system health reporting                             │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. GET /health                                                      │   │
│  │  2. Verify response contains all subsystem statuses                  │   │
│  │  3. Verify database connectivity check                               │   │
│  │  4. Verify timestamp current                                         │   │
│  │                                                                      │   │
│  │  Expected: 200 OK with complete health data                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2.2 AI Layer Junction Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI LAYER INTEGRATION TESTS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: AI Layer → External API (Claude)                                 │
│  Test File: tests/integration/test_ai_integration.py                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-AI-001: Narrative Generation Chain                             │   │
│  │  ───────────────────────────────────                                 │   │
│  │  Purpose: Verify Prompt → Claude → Validation → Storage              │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Create test instrument with signals                              │   │
│  │  2. Call narrative generation endpoint                               │   │
│  │  3. Verify Claude API called with correct prompt                     │   │
│  │  4. Verify response validated against constitution                   │   │
│  │  5. Verify narrative persisted to database                           │   │
│  │                                                                      │   │
│  │  Expected: Valid narrative returned and stored                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-AI-002: Constitutional Violation Rejection                     │   │
│  │  ───────────────────────────────────────────                         │   │
│  │  Purpose: Verify CR-001/002/003 enforcement                          │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Mock Claude response with "you should buy"                       │   │
│  │  2. Call validation layer                                            │   │
│  │  3. Verify REJECTION due to CR-001 violation                         │   │
│  │  4. Mock response with "I recommend selling"                         │   │
│  │  5. Verify REJECTION due to CR-003 violation                         │   │
│  │                                                                      │   │
│  │  Expected: All violating responses rejected                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-AI-003: Model Selection Based on Budget                        │   │
│  │  ────────────────────────────────────────                            │   │
│  │  Purpose: Verify AI budget enforcement                               │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Set low AI budget                                                │   │
│  │  2. Request complex narrative                                        │   │
│  │  3. Verify cheaper model selected (haiku vs sonnet)                  │   │
│  │  4. Verify budget decremented after use                              │   │
│  │                                                                      │   │
│  │  Expected: Model selection respects budget constraints               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2.3 Exposure Layer Junction Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXPOSURE LAYER INTEGRATION TESTS                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: Exposure Engine → Data Layer                                     │
│  Test File: tests/integration/test_exposure_integration.py                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-EXP-001: Contradiction Detection                               │   │
│  │  ─────────────────────────────────                                   │   │
│  │  Purpose: Verify conflicting signals create contradictions           │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Create instrument                                                │   │
│  │  2. Create chart1 in silo_A with BULLISH signal                      │   │
│  │  3. Create chart2 in silo_B with BEARISH signal                      │   │
│  │  4. Trigger contradiction detection                                  │   │
│  │  5. Verify contradiction record created                              │   │
│  │  6. Verify both signals referenced                                   │   │
│  │                                                                      │   │
│  │  Expected: Contradiction exposed, NOT resolved                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-EXP-002: Confirmation Detection                                │   │
│  │  ────────────────────────────────                                    │   │
│  │  Purpose: Verify aligned signals create confirmations                │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Create instrument                                                │   │
│  │  2. Create chart1 in silo_A with BULLISH signal                      │   │
│  │  3. Create chart2 in silo_B with BULLISH signal                      │   │
│  │  4. Trigger confirmation detection                                   │   │
│  │  5. Verify confirmation record created                               │   │
│  │  6. Verify confidence_exposure calculated                            │   │
│  │                                                                      │   │
│  │  Expected: Confirmation with exposure metric                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-EXP-003: Relationship Summary Generation                       │   │
│  │  ─────────────────────────────────────────                           │   │
│  │  Purpose: Verify complete relationship exposure                      │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Create instrument with multiple signals                          │   │
│  │  2. Call GET /api/relationships/{instrument_id}                      │   │
│  │  3. Verify response contains all contradictions                      │   │
│  │  4. Verify response contains all confirmations                       │   │
│  │  5. Verify no "recommendation" or "should" in response               │   │
│  │                                                                      │   │
│  │  Expected: Pure exposure, no prescription                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2.4 Constitutional Compliance Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONSTITUTIONAL COMPLIANCE TESTS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: All Layers → Constitutional Rules                                │
│  Test File: tests/constitutional/test_constitutional_compliance.py          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-CONST-001: CR-001 Enforcement (No Decision-Making)             │   │
│  │  ───────────────────────────────────────────────────                 │   │
│  │  Purpose: Verify system never makes decisions for user               │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Scan all API responses for prohibited terms                      │   │
│  │     - "should", "must", "recommend", "advise", "suggest"             │   │
│  │  2. Scan all AI prompts for instruction patterns                     │   │
│  │  3. Scan all UI text for action directives                           │   │
│  │                                                                      │   │
│  │  Expected: ZERO matches for prohibited terms                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-CONST-002: CR-002 Enforcement (No Resolution)                  │   │
│  │  ──────────────────────────────────────────────                      │   │
│  │  Purpose: Verify contradictions exposed, never resolved              │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Create conflicting signals                                       │   │
│  │  2. Generate narrative                                               │   │
│  │  3. Verify narrative presents BOTH views                             │   │
│  │  4. Verify no "therefore" or "conclusion" statements                 │   │
│  │  5. Verify no prioritization of one view over another                │   │
│  │                                                                      │   │
│  │  Expected: Equal exposure of conflicting signals                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-CONST-003: CR-003 Enforcement (Descriptive Only)               │   │
│  │  ─────────────────────────────────────────────────                   │   │
│  │  Purpose: Verify all output is descriptive, not prescriptive         │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Generate narrative for any instrument                            │   │
│  │  2. Analyze language for imperative mood                             │   │
│  │  3. Check for future predictions with certainty                      │   │
│  │  4. Verify all statements are observations                           │   │
│  │                                                                      │   │
│  │  Expected: 100% descriptive language                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-CONST-004: Five-Layer Defense Verification                     │   │
│  │  ────────────────────────────────────────────                        │   │
│  │  Purpose: Verify all 5 defense layers active                         │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Layer 1 (Schema): Check DB has no weight/score columns           │   │
│  │  2. Layer 2 (Models): Check Pydantic has no prohibited fields        │   │
│  │  3. Layer 3 (Logic): Check validators for prohibited terms           │   │
│  │  4. Layer 4 (AI): Check response_validator.py exists and active      │   │
│  │  5. Layer 5 (UI): Check components have disclaimers                  │   │
│  │                                                                      │   │
│  │  Expected: All 5 layers verified operational                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3.3 MERCURY INTEGRATION TESTS

### 3.3.1 Chat Layer Junction Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MERCURY CHAT LAYER TESTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: Interface → Chat → AI → Kite                                     │
│  Test File: tests/test_chat_engine.py                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MCHAT-001: Query Processing Pipeline                           │   │
│  │  ─────────────────────────────────────                               │   │
│  │  Purpose: Verify complete query → response chain                     │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Submit query "What is current price of RELIANCE?"                │   │
│  │  2. Verify query parsed correctly (symbol extracted)                 │   │
│  │  3. Verify Kite adapter called for quote                             │   │
│  │  4. Verify AI engine called with market data                         │   │
│  │  5. Verify response contains price information                       │   │
│  │                                                                      │   │
│  │  Expected: Complete response with real data                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MCHAT-002: Conversation Continuity                             │   │
│  │  ───────────────────────────────────                                 │   │
│  │  Purpose: Verify multi-turn conversation context                     │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Submit "What is RELIANCE trading at?"                            │   │
│  │  2. Submit follow-up "What about its 52-week high?"                  │   │
│  │  3. Verify second query understands context (RELIANCE)               │   │
│  │  4. Submit "Compare it to INFY"                                      │   │
│  │  5. Verify comparison includes RELIANCE context                      │   │
│  │                                                                      │   │
│  │  Expected: Context preserved across turns                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MCHAT-003: Unrestricted Response Verification                  │   │
│  │  ──────────────────────────────────────────                          │   │
│  │  Purpose: Verify Mercury constitution allows recommendations         │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Ask "Should I buy RELIANCE at current levels?"                   │   │
│  │  2. Verify response contains opinion/recommendation                  │   │
│  │  3. Verify response NOT rejected for CR-001 violation                │   │
│  │  4. Verify confidence score may be included                          │   │
│  │                                                                      │   │
│  │  Expected: Unrestricted, helpful response                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3.2 Startup & Health Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MERCURY STARTUP & HEALTH TESTS                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: Startup → Core → External APIs                                   │
│  Test File: tests/test_startup.py, tests/test_health.py                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MSTART-001: API Verification Sequence                          │   │
│  │  ──────────────────────────────────────                              │   │
│  │  Purpose: Verify both APIs checked at startup                        │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Call perform_launch_readiness_check()                            │   │
│  │  2. Verify Kite API verification called                              │   │
│  │  3. Verify Anthropic API verification called                         │   │
│  │  4. Verify status report generated                                   │   │
│  │  5. Verify readiness determined correctly                            │   │
│  │                                                                      │   │
│  │  Expected: Complete verification with accurate status                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MSTART-002: Failed API Handling                                │   │
│  │  ────────────────────────────────                                    │   │
│  │  Purpose: Verify graceful handling of API failures                   │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Mock Kite API to fail                                            │   │
│  │  2. Call verification                                                │   │
│  │  3. Verify FAILED status returned                                    │   │
│  │  4. Verify error message descriptive                                 │   │
│  │  5. Verify system does not crash                                     │   │
│  │                                                                      │   │
│  │  Expected: Graceful degradation with clear messaging                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MHEALTH-001: Health Check Endpoints                            │   │
│  │  ────────────────────────────────────                                │   │
│  │  Purpose: Verify health endpoints return accurate status             │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. GET /health → Verify basic health response                       │   │
│  │  2. GET /status → Verify detailed status response                    │   │
│  │  3. Verify Kite status included                                      │   │
│  │  4. Verify Anthropic status included                                 │   │
│  │  5. Verify uptime tracking accurate                                  │   │
│  │                                                                      │   │
│  │  Expected: Comprehensive health information                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3.3 Resilience Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MERCURY RESILIENCE TESTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: Core Resilience → External APIs                                  │
│  Test File: tests/test_resilience.py                                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MRES-001: Circuit Breaker Activation                           │   │
│  │  ─────────────────────────────────────                               │   │
│  │  Purpose: Verify circuit breaker opens after failures                │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Configure circuit breaker (threshold=5)                          │   │
│  │  2. Simulate 5 consecutive failures                                  │   │
│  │  3. Verify circuit breaker state = OPEN                              │   │
│  │  4. Attempt call → Verify fast-fail                                  │   │
│  │  5. Wait recovery_timeout                                            │   │
│  │  6. Verify circuit breaker state = HALF_OPEN                         │   │
│  │                                                                      │   │
│  │  Expected: Circuit breaker prevents cascade failure                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MRES-002: Retry Mechanism                                      │   │
│  │  ──────────────────────────                                          │   │
│  │  Purpose: Verify exponential backoff retry                           │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Configure retry (max_attempts=3, base_delay=100ms)               │   │
│  │  2. Mock API to fail twice, succeed third time                       │   │
│  │  3. Call with retry wrapper                                          │   │
│  │  4. Verify 3 attempts made                                           │   │
│  │  5. Verify delays were 100ms, 200ms                                  │   │
│  │  6. Verify final success returned                                    │   │
│  │                                                                      │   │
│  │  Expected: Transient failures recovered                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MRES-003: Graceful Degradation                                 │   │
│  │  ───────────────────────────────                                     │   │
│  │  Purpose: Verify degraded mode when API unavailable                  │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Mock Kite API completely unavailable                             │   │
│  │  2. Submit query requiring market data                               │   │
│  │  3. Verify system does not crash                                     │   │
│  │  4. Verify user receives helpful error message                       │   │
│  │  5. Verify system remains operational for non-market queries         │   │
│  │                                                                      │   │
│  │  Expected: Degraded but functional state                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3.4 Security Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MERCURY SECURITY TESTS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUNCTION: Core Security → All Layers                                       │
│  Test File: tests/test_security.py                                          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MSEC-001: API Key Masking                                      │   │
│  │  ──────────────────────────                                          │   │
│  │  Purpose: Verify API keys never logged in plain text                 │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Set API key "sk-ant-api03-1234567890abcdef"                      │   │
│  │  2. Call mask_sensitive_data()                                       │   │
│  │  3. Verify output is "sk-ant-***...***cdef"                          │   │
│  │  4. Search all log outputs for full key                              │   │
│  │  5. Verify ZERO matches                                              │   │
│  │                                                                      │   │
│  │  Expected: Keys always masked in logs                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MSEC-002: Token Sanitization                                   │   │
│  │  ─────────────────────────────                                       │   │
│  │  Purpose: Verify access tokens sanitized in logs                     │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Create log entry with access_token                               │   │
│  │  2. Apply sanitization                                               │   │
│  │  3. Verify token replaced with [REDACTED]                            │   │
│  │  4. Verify original data unchanged                                   │   │
│  │                                                                      │   │
│  │  Expected: Tokens never exposed in logs                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TEST-MSEC-003: Configuration Validation                             │   │
│  │  ───────────────────────────────────                                 │   │
│  │  Purpose: Verify invalid configs rejected at startup                 │   │
│  │                                                                      │   │
│  │  Procedure:                                                          │   │
│  │  1. Provide malformed API key                                        │   │
│  │  2. Call validation                                                  │   │
│  │  3. Verify validation error returned                                 │   │
│  │  4. Verify system does not start with invalid config                 │   │
│  │                                                                      │   │
│  │  Expected: Fail-fast on invalid configuration                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3.4 END-TO-END TEST SCENARIOS

### 3.4.1 Complete User Journey Tests

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    END-TO-END JOURNEY TESTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  E2E-001: CIA-SIE Signal to Narrative Journey                        │   │
│  │  ────────────────────────────────────────────                        │   │
│  │                                                                      │   │
│  │  Complete Flow:                                                      │   │
│  │  1. TradingView sends webhook with BULLISH signal                    │   │
│  │  2. Backend receives and normalizes signal                           │   │
│  │  3. Contradiction detection runs (finds existing BEARISH)            │   │
│  │  4. Contradiction record created                                     │   │
│  │  5. User requests narrative for instrument                           │   │
│  │  6. AI generates response acknowledging contradiction                │   │
│  │  7. Response validated for constitutional compliance                 │   │
│  │  8. Narrative displayed to user                                      │   │
│  │  9. Verify NO recommendation in output                               │   │
│  │                                                                      │   │
│  │  Duration: ~5 seconds                                                │   │
│  │  Validation Points: 9                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  E2E-002: Mercury Chat Session Journey                               │   │
│  │  ─────────────────────────────────────                               │   │
│  │                                                                      │   │
│  │  Complete Flow:                                                      │   │
│  │  1. User opens Mercury web interface                                 │   │
│  │  2. WebSocket connection established                                 │   │
│  │  3. User asks "Analyze NIFTY for me"                                 │   │
│  │  4. Query parsed, symbols extracted                                  │   │
│  │  5. Kite API called for market data                                  │   │
│  │  6. Context assembled with data                                      │   │
│  │  7. AI generates comprehensive analysis                              │   │
│  │  8. Response streamed to user                                        │   │
│  │  9. User asks follow-up question                                     │   │
│  │  10. Context includes previous exchange                              │   │
│  │  11. Coherent follow-up response generated                           │   │
│  │                                                                      │   │
│  │  Duration: ~8 seconds                                                │   │
│  │  Validation Points: 11                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  E2E-003: System Startup to Operational Journey                      │   │
│  │  ──────────────────────────────────────────────                      │   │
│  │                                                                      │   │
│  │  Complete Flow:                                                      │   │
│  │  1. User double-clicks start-mercury.command                         │   │
│  │  2. Configuration loaded from .env                                   │   │
│  │  3. Configuration validated                                          │   │
│  │  4. Kite API verification attempted                                  │   │
│  │  5. Anthropic API verification attempted                             │   │
│  │  6. Launch readiness determined                                      │   │
│  │  7. Status report displayed                                          │   │
│  │  8. FastAPI server started                                           │   │
│  │  9. Browser opens to interface                                       │   │
│  │  10. User begins interaction                                         │   │
│  │                                                                      │   │
│  │  Duration: ~3 seconds                                                │   │
│  │  Validation Points: 10                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3.5 TEST EXECUTION COMMANDS

### Standard Test Execution

```bash
# CIA-SIE Full Test Suite
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE
source venv/bin/activate
pytest tests/ -v --tb=short

# CIA-SIE Constitutional Tests Only
pytest tests/constitutional/ -v

# CIA-SIE Integration Tests Only
pytest tests/integration/ -v

# Mercury Full Test Suite
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury
pytest tests/ -v --tb=short

# Mercury with Coverage
pytest tests/ --cov=src/mercury --cov-report=html

# Both Systems - Complete Validation
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE
pytest tests/ projects/mercury/tests/ -v --tb=short
```

### Test Categories

| Category | Command | Purpose |
|----------|---------|---------|
| Unit | `pytest tests/unit/` | Individual function tests |
| Integration | `pytest tests/integration/` | Cross-module tests |
| Constitutional | `pytest tests/constitutional/` | CR compliance tests |
| E2E | `pytest tests/e2e/` | Full journey tests |
| Chaos | `pytest tests/chaos/` | Failure mode tests |
| Security | `pytest tests/test_security.py` | Security validation |
| Health | `pytest tests/test_health.py` | Health check tests |
| Resilience | `pytest tests/test_resilience.py` | Fault tolerance tests |

---

## 3.6 CHAPTER HANDOFF

**This chapter established:**
- Complete test registry (339+ test cases)
- Detailed test procedures for all junctions
- End-to-end test scenarios
- Test execution commands

**Next chapter will detail:**
- Failure mode analysis
- Every break point identified
- Failover routing for each failure

---

**Predecessor:** [02_SIGNAL_FLOW_MATRIX.md](./02_SIGNAL_FLOW_MATRIX.md)
**Successor:** [04_FAILURE_MODE_ANALYSIS.md](./04_FAILURE_MODE_ANALYSIS.md)

---

*"Validation sequences for each junction point."*
