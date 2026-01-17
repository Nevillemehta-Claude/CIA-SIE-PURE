# MASTER TEST EXECUTION PLAN v1.0
## CIA-SIE Comprehensive Testing Framework

**Document ID:** CIA-SIE-TEST-PLAN-001  
**Version:** 1.0  
**Date:** 2026-01-05  
**Author:** Claude Opus 4.5 (AI Testing Engineer)  
**Status:** PENDING APPROVAL  

---

## EXECUTIVE SUMMARY

This document defines the **exhaustive test execution plan** for the CIA-SIE application. Every component, every interaction, every data flow will be tested **multiple times** to ensure statistical confidence in reliability.

### Key Metrics

| Metric | Target |
|--------|--------|
| Total Test Cases | 1,500+ |
| Repetitions per Test | 10 runs minimum |
| Total Test Executions | 15,000+ |
| Required Pass Rate | 100% (all runs must pass) |
| Code Coverage Target | >90% |

---

## TESTING PHILOSOPHY

### The "10x Rule"

Every test will be executed **10 times minimum**. A test is only considered "PASSED" if it passes **all 10 runs**. This eliminates:
- Flaky tests (intermittent failures)
- Race conditions
- Timing-dependent bugs
- Random state corruption

### Complete Cycle Principle

Every test represents a **complete interaction cycle**:

```
KNOWN START STATE → ACTION → VERIFIED END STATE
```

No orphan tests. No partial verifications.

---

## PART 1: BACKEND TEST INVENTORY

### 1.1 API LAYER - INSTRUMENTS (`src/cia_sie/api/routes/instruments.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-INST-001 | Create instrument - valid data | 0 instruments | POST /instruments/ with valid JSON | 1 instrument exists, correct fields | 10 |
| API-INST-002 | Create instrument - missing symbol | 0 instruments | POST without symbol field | 422 error, 0 instruments | 10 |
| API-INST-003 | Create instrument - duplicate symbol | 1 instrument (RELIANCE) | POST with RELIANCE | 409 error, still 1 instrument | 10 |
| API-INST-004 | Create instrument - invalid exchange | 0 instruments | POST with exchange="INVALID" | 422 error, 0 instruments | 10 |
| API-INST-005 | Create instrument - empty symbol | 0 instruments | POST with symbol="" | 422 error, 0 instruments | 10 |
| API-INST-006 | Create instrument - symbol too long | 0 instruments | POST with symbol=100 chars | 422 error, 0 instruments | 10 |
| API-INST-007 | List instruments - empty database | 0 instruments | GET /instruments/ | Empty array [] | 10 |
| API-INST-008 | List instruments - with data | 5 instruments | GET /instruments/ | Array of 5 items | 10 |
| API-INST-009 | List instruments - pagination | 100 instruments | GET /instruments/?limit=10 | Array of 10 items | 10 |
| API-INST-010 | Get instrument by ID - exists | 1 instrument | GET /instruments/{id} | Correct instrument | 10 |
| API-INST-011 | Get instrument by ID - not found | 0 instruments | GET /instruments/{random-uuid} | 404 error | 10 |
| API-INST-012 | Get instrument by ID - invalid UUID | 0 instruments | GET /instruments/not-a-uuid | 422 error | 10 |
| API-INST-013 | Update instrument - valid | 1 instrument | PUT /instruments/{id} | Updated fields | 10 |
| API-INST-014 | Update instrument - not found | 0 instruments | PUT /instruments/{random-uuid} | 404 error | 10 |
| API-INST-015 | Delete instrument - exists | 1 instrument | DELETE /instruments/{id} | is_active=false | 10 |
| API-INST-016 | Delete instrument - not found | 0 instruments | DELETE /instruments/{random-uuid} | 404 error | 10 |
| API-INST-017 | Delete instrument - cascade check | 1 instrument with silos | DELETE /instruments/{id} | Silos also soft-deleted | 10 |
| API-INST-018 | Get instrument by symbol - exists | 1 instrument (RELIANCE) | GET /instruments/symbol/RELIANCE | Correct instrument | 10 |
| API-INST-019 | Get instrument by symbol - not found | 0 instruments | GET /instruments/symbol/UNKNOWN | 404 error | 10 |
| API-INST-020 | Create instrument - special chars in name | 0 instruments | POST with display_name="Test & Co." | Created successfully | 10 |

**Subtotal: 20 tests × 10 runs = 200 executions**

---

### 1.2 API LAYER - SILOS (`src/cia_sie/api/routes/silos.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-SILO-001 | Create silo - valid data | 1 instrument, 0 silos | POST /silos/ | 1 silo exists | 10 |
| API-SILO-002 | Create silo - missing instrument_id | 0 instruments | POST without instrument_id | 422 error | 10 |
| API-SILO-003 | Create silo - invalid instrument_id | 0 instruments | POST with random UUID | 404/422 error | 10 |
| API-SILO-004 | Create silo - duplicate name per instrument | 1 silo named "Daily" | POST with same name, same instrument | 409 error | 10 |
| API-SILO-005 | Create silo - same name different instrument | 1 silo named "Daily" | POST with same name, different instrument | Created (allowed) | 10 |
| API-SILO-006 | List silos - empty | 0 silos | GET /silos/ | Empty array | 10 |
| API-SILO-007 | List silos - with data | 5 silos | GET /silos/ | Array of 5 | 10 |
| API-SILO-008 | List silos - filter by instrument | 3 silos (2 for inst A, 1 for inst B) | GET /silos/?instrument_id=A | Array of 2 | 10 |
| API-SILO-009 | Get silo by ID - exists | 1 silo | GET /silos/{id} | Correct silo | 10 |
| API-SILO-010 | Get silo by ID - not found | 0 silos | GET /silos/{random-uuid} | 404 error | 10 |
| API-SILO-011 | Update silo - valid | 1 silo | PUT /silos/{id} | Updated fields | 10 |
| API-SILO-012 | Update silo - change thresholds | 1 silo | PUT with new threshold values | Thresholds updated | 10 |
| API-SILO-013 | Delete silo - exists | 1 silo | DELETE /silos/{id} | is_active=false | 10 |
| API-SILO-014 | Delete silo - with charts | 1 silo with 3 charts | DELETE /silos/{id} | Charts also soft-deleted | 10 |
| API-SILO-015 | Get silo with charts | 1 silo with 3 charts | GET /silos/{id}?include_charts=true | Silo with charts array | 10 |

**Subtotal: 15 tests × 10 runs = 150 executions**

---

### 1.3 API LAYER - CHARTS (`src/cia_sie/api/routes/charts.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-CHART-001 | Create chart - valid data | 1 silo, 0 charts | POST /charts/ | 1 chart exists | 10 |
| API-CHART-002 | Create chart - missing silo_id | 0 silos | POST without silo_id | 422 error | 10 |
| API-CHART-003 | Create chart - invalid timeframe | 1 silo | POST with timeframe="INVALID" | 422 error | 10 |
| API-CHART-004 | Create chart - valid timeframes | 1 silo | POST with each: 1m,5m,15m,30m,1h,4h,D,W,M | All succeed | 10 |
| API-CHART-005 | Create chart - duplicate webhook_id | 1 chart with webhook "ABC" | POST with webhook_id="ABC" | 409 error | 10 |
| API-CHART-006 | Create chart - duplicate code per silo | 1 chart code "01A" | POST with same code, same silo | 409 error | 10 |
| API-CHART-007 | List charts - empty | 0 charts | GET /charts/ | Empty array | 10 |
| API-CHART-008 | List charts - filter by silo | 5 charts (3 in silo A) | GET /charts/?silo_id=A | Array of 3 | 10 |
| API-CHART-009 | Get chart by ID - exists | 1 chart | GET /charts/{id} | Correct chart | 10 |
| API-CHART-010 | Get chart by ID - not found | 0 charts | GET /charts/{random-uuid} | 404 error | 10 |
| API-CHART-011 | Get chart by webhook_id | 1 chart with webhook "TEST" | GET /charts/webhook/TEST | Correct chart | 10 |
| API-CHART-012 | Update chart - valid | 1 chart | PUT /charts/{id} | Updated fields | 10 |
| API-CHART-013 | Delete chart - exists | 1 chart | DELETE /charts/{id} | is_active=false | 10 |
| API-CHART-014 | Delete chart - with signals | 1 chart with 10 signals | DELETE /charts/{id} | Signals preserved (historical) | 10 |
| API-CHART-015 | Chart has NO weight field | 1 chart | GET /charts/{id} | Response has no "weight" key | 10 |

**Subtotal: 15 tests × 10 runs = 150 executions**

---

### 1.4 API LAYER - WEBHOOKS (`src/cia_sie/api/routes/webhooks.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-HOOK-001 | Receive webhook - valid TradingView | 1 chart | POST /webhook/ with valid payload | Signal created | 10 |
| API-HOOK-002 | Receive webhook - unknown webhook_id | 0 charts | POST with unknown webhook_id | 404 error | 10 |
| API-HOOK-003 | Receive webhook - missing direction | 1 chart | POST without direction | 422 error | 10 |
| API-HOOK-004 | Receive webhook - invalid direction | 1 chart | POST with direction="INVALID" | 422 error | 10 |
| API-HOOK-005 | Receive webhook - BULLISH direction | 1 chart | POST with direction="BULLISH" | Signal with BULLISH | 10 |
| API-HOOK-006 | Receive webhook - BEARISH direction | 1 chart | POST with direction="BEARISH" | Signal with BEARISH | 10 |
| API-HOOK-007 | Receive webhook - NEUTRAL direction | 1 chart | POST with direction="NEUTRAL" | Signal with NEUTRAL | 10 |
| API-HOOK-008 | Manual trigger - valid | 1 chart | POST /webhook/manual | Signal created | 10 |
| API-HOOK-009 | Webhook health check | N/A | GET /webhook/health | 200 OK | 10 |
| API-HOOK-010 | Webhook - signature validation (valid) | 1 chart, WEBHOOK_SECRET set | POST with valid HMAC | Signal created | 10 |
| API-HOOK-011 | Webhook - signature validation (invalid) | WEBHOOK_SECRET set | POST with wrong HMAC | 401 error | 10 |
| API-HOOK-012 | Webhook - signature validation (missing) | WEBHOOK_SECRET set, production mode | POST without signature | 401 error | 10 |
| API-HOOK-013 | Webhook - rapid fire (10 signals/sec) | 1 chart | POST 10 signals rapidly | All 10 created | 10 |
| API-HOOK-014 | Webhook - duplicate signal handling | 1 chart with signal | POST identical signal | Idempotent or new signal | 10 |
| API-HOOK-015 | Webhook - signal has NO confidence score | 1 chart | POST /webhook/ | Created signal has no confidence | 10 |
| API-HOOK-016 | Webhook - large message (10KB) | 1 chart | POST with 10KB message | 413 or truncated | 10 |
| API-HOOK-017 | Webhook - empty message | 1 chart | POST with message="" | Signal created (message optional) | 10 |
| API-HOOK-018 | Webhook - special chars in message | 1 chart | POST with emoji/unicode | Created successfully | 10 |

**Subtotal: 18 tests × 10 runs = 180 executions**

---

### 1.5 API LAYER - RELATIONSHIPS (`src/cia_sie/api/routes/relationships.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-REL-001 | Get silo relationships - no signals | 1 silo, 2 charts, 0 signals | GET /relationships/silo/{id} | Empty contradictions/confirmations | 10 |
| API-REL-002 | Get silo relationships - contradiction | 2 charts (BULLISH, BEARISH) | GET /relationships/silo/{id} | 1 contradiction | 10 |
| API-REL-003 | Get silo relationships - confirmation | 2 charts (BULLISH, BULLISH) | GET /relationships/silo/{id} | 1 confirmation | 10 |
| API-REL-004 | Get silo relationships - mixed | 3 charts (B, B, BEAR) | GET /relationships/silo/{id} | 1 confirm, 2 contradictions | 10 |
| API-REL-005 | Contradiction - NO resolution field | 2 charts contradicting | GET /relationships/silo/{id} | No "resolution" in response | 10 |
| API-REL-006 | Contradiction - NO priority field | 2 charts contradicting | GET /relationships/silo/{id} | No "priority" in response | 10 |
| API-REL-007 | Confirmation - NO aggregation | 2 charts confirming | GET /relationships/silo/{id} | No "combined_strength" field | 10 |
| API-REL-008 | Get instrument relationships | 1 instrument, 2 silos | GET /relationships/instrument/{id} | All relationships across silos | 10 |
| API-REL-009 | Get contradictions only | 2 charts contradicting | GET /relationships/silo/{id}/contradictions | Only contradictions | 10 |
| API-REL-010 | Relationship - NEUTRAL ignored | 3 charts (BULL, NEUTRAL, BEAR) | GET /relationships/silo/{id} | Only BULL vs BEAR counted | 10 |
| API-REL-011 | All charts returned (CR-001) | 5 charts in silo | GET /relationships/silo/{id} | All 5 charts in response | 10 |
| API-REL-012 | No scores in response (CR-001) | 2 charts | GET /relationships/silo/{id} | No "score" field anywhere | 10 |

**Subtotal: 12 tests × 10 runs = 120 executions**

---

### 1.6 API LAYER - NARRATIVES (`src/cia_sie/api/routes/narratives.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-NAR-001 | Generate narrative - valid silo | 1 silo with signals | GET /narratives/silo/{id} | Narrative text returned | 10 |
| API-NAR-002 | Generate narrative - empty silo | 1 silo, 0 signals | GET /narratives/silo/{id} | Graceful empty message | 10 |
| API-NAR-003 | Generate narrative - silo not found | 0 silos | GET /narratives/silo/{random-uuid} | 404 error | 10 |
| API-NAR-004 | Narrative contains disclaimer (CR-003) | 1 silo with signals | GET /narratives/silo/{id} | Disclaimer present | 10 |
| API-NAR-005 | Narrative NO recommendations (CR-001) | 1 silo with signals | GET /narratives/silo/{id} | No "you should" text | 10 |
| API-NAR-006 | Narrative NO buy/sell (CR-001) | 1 silo with signals | GET /narratives/silo/{id} | No "buy"/"sell" text | 10 |
| API-NAR-007 | Narrative plain text format | 1 silo with signals | GET /narratives/silo/{id}/plain | Plain text, no markdown | 10 |
| API-NAR-008 | Narrative - Claude API failure | Mock Claude error | GET /narratives/silo/{id} | Fallback message with disclaimer | 10 |

**Subtotal: 8 tests × 10 runs = 80 executions**

---

### 1.7 API LAYER - BASKETS (`src/cia_sie/api/routes/baskets.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-BASK-001 | Create basket - valid | 0 baskets | POST /baskets/ | 1 basket exists | 10 |
| API-BASK-002 | Create basket - all types | 0 baskets | POST each type (LOGICAL, HIERARCHICAL, CONTEXTUAL, CUSTOM) | All 4 created | 10 |
| API-BASK-003 | Add chart to basket | 1 basket, 1 chart | POST /baskets/{id}/charts/{chart_id} | Chart in basket | 10 |
| API-BASK-004 | Add chart to multiple baskets | 2 baskets, 1 chart | Add same chart to both | Chart in both baskets | 10 |
| API-BASK-005 | Remove chart from basket | 1 basket with 1 chart | DELETE /baskets/{id}/charts/{chart_id} | Chart removed | 10 |
| API-BASK-006 | List baskets | 5 baskets | GET /baskets/ | Array of 5 | 10 |
| API-BASK-007 | Get basket with charts | 1 basket with 3 charts | GET /baskets/{id} | Basket with chart_ids | 10 |
| API-BASK-008 | Delete basket - soft delete | 1 basket | DELETE /baskets/{id} | is_active=false | 10 |
| API-BASK-009 | Delete basket - charts unaffected | 1 basket with charts | DELETE /baskets/{id} | Charts still exist | 10 |
| API-BASK-010 | Basket has NO processing effect (CR) | 1 basket with charts | Send signals to charts | Signals unaffected by basket | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

### 1.8 API LAYER - AI (`src/cia_sie/api/routes/ai.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-AI-001 | Get budget status | Fresh state | GET /ai/budget | Budget info returned | 10 |
| API-AI-002 | Get available models | N/A | GET /ai/models | List of models | 10 |
| API-AI-003 | Budget under limit | $0 used of $50 | GET /ai/budget | within_budget=true | 10 |
| API-AI-004 | Budget at threshold | $40 used of $50 (80%) | GET /ai/budget | alert_level present | 10 |
| API-AI-005 | Budget exceeded | $51 used of $50 | GET /ai/budget | within_budget=false | 10 |
| API-AI-006 | Set active model | N/A | PUT /ai/model | Model updated | 10 |
| API-AI-007 | Set invalid model | N/A | PUT /ai/model with "invalid-model" | 400 error | 10 |
| API-AI-008 | Usage tracking | 0 usage | Make AI request | Usage incremented | 10 |
| API-AI-009 | All AI is DESCRIPTIVE (CR-001) | N/A | GET /ai/models | No "prescriptive" capability | 10 |
| API-AI-010 | Rate limit - under limit | 0 requests this minute | Make 5 requests | All succeed | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

### 1.9 API LAYER - CHAT (`src/cia_sie/api/routes/chat.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-CHAT-001 | Send chat message | 1 instrument | POST /chat/ with question | Response returned | 10 |
| API-CHAT-002 | Chat - empty message | 1 instrument | POST with message="" | 422 error | 10 |
| API-CHAT-003 | Chat - instrument not found | 0 instruments | POST with random instrument_id | 404 error | 10 |
| API-CHAT-004 | Chat response has disclaimer (CR-003) | 1 instrument | POST /chat/ | Disclaimer in response | 10 |
| API-CHAT-005 | Chat NO recommendations (CR-001) | 1 instrument | Ask "should I buy?" | Response avoids prescription | 10 |
| API-CHAT-006 | Chat history - new conversation | 0 conversations | POST /chat/ | Conversation created | 10 |
| API-CHAT-007 | Chat history - continue conversation | 1 conversation | POST /chat/ with conversation_id | Added to history | 10 |
| API-CHAT-008 | Chat - very long message | 1 instrument | POST with 5000 char message | Handled gracefully | 10 |

**Subtotal: 8 tests × 10 runs = 80 executions**

---

### 1.10 API LAYER - PLATFORMS (`src/cia_sie/api/routes/platforms.py`)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| API-PLAT-001 | List platforms | N/A | GET /platforms/ | Kite in list | 10 |
| API-PLAT-002 | Get platform status - Kite | Kite not connected | GET /platforms/kite | is_connected=false | 10 |
| API-PLAT-003 | Connect platform - missing API key | No KITE_API_KEY | POST /platforms/kite/connect | Error about missing key | 10 |
| API-PLAT-004 | Connect platform - with API key | KITE_API_KEY set | POST /platforms/kite/connect | OAuth URL returned | 10 |
| API-PLAT-005 | Get setup instructions | N/A | GET /platforms/kite/setup | Instructions returned | 10 |
| API-PLAT-006 | OAuth callback - valid | Valid request_token | GET /platforms/kite/callback?token=X | Access token stored | 10 |
| API-PLAT-007 | OAuth callback - invalid token | Invalid request_token | GET /platforms/kite/callback?token=BAD | Error returned | 10 |
| API-PLAT-008 | Disconnect platform | Kite connected | POST /platforms/kite/disconnect | is_connected=false | 10 |
| API-PLAT-009 | Get watchlists - not connected | Kite not connected | GET /platforms/kite/watchlists | Error: not connected | 10 |
| API-PLAT-010 | Import instruments - not connected | Kite not connected | POST /platforms/kite/import | Error: not connected | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

### 1.11 CORE LAYER - CONSTITUTIONAL COMPLIANCE

| Test ID | Test Name | Component | Verification | Repetitions |
|---------|-----------|-----------|--------------|-------------|
| CONST-001 | No "you should" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-002 | No "I recommend" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-003 | No "buy" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-004 | No "sell" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-005 | No "trade" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-006 | No "invest" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-007 | No "profitable" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-008 | No "guaranteed" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-009 | No "strong signal" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-010 | No "weak signal" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-011 | No "overall direction" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-012 | No "net bullish" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-013 | No "net bearish" in AI output | response_validator.py | Regex pattern match | 10 |
| CONST-014 | Disclaimer text is exact match | constants | String comparison | 10 |
| CONST-015 | Disclaimer present in all AI responses | narrative_generator.py | Check every response | 10 |
| CONST-016 | Chart model has NO weight field | models.py | Field inspection | 10 |
| CONST-017 | Signal model has NO confidence field | models.py | Field inspection | 10 |
| CONST-018 | No aggregation config exists | config.py | Settings inspection | 10 |
| CONST-019 | No scoring config exists | config.py | Settings inspection | 10 |
| CONST-020 | No recommendation config exists | config.py | Settings inspection | 10 |
| CONST-021 | ConstitutionalViolationError exists | exceptions.py | Class exists | 10 |
| CONST-022 | Contradiction has no resolution field | models.py | Field inspection | 10 |
| CONST-023 | Confirmation has no weight field | models.py | Field inspection | 10 |
| CONST-024 | Validator retries on violation | response_validator.py | Retry logic | 10 |
| CONST-025 | Fallback message has disclaimer | narrative_generator.py | Fallback inspection | 10 |

**Subtotal: 25 tests × 10 runs = 250 executions**

---

### 1.12 DATA ACCESS LAYER - REPOSITORIES

| Test ID | Test Name | Repository | Operation | Repetitions |
|---------|-----------|------------|-----------|-------------|
| DAL-001 | Create instrument | InstrumentRepository | create() | 10 |
| DAL-002 | Get instrument by ID | InstrumentRepository | get_by_id() | 10 |
| DAL-003 | Get instrument by symbol | InstrumentRepository | get_by_symbol() | 10 |
| DAL-004 | List all instruments | InstrumentRepository | get_all() | 10 |
| DAL-005 | Update instrument | InstrumentRepository | update() | 10 |
| DAL-006 | Soft delete instrument | InstrumentRepository | delete() | 10 |
| DAL-007 | Create silo | SiloRepository | create() | 10 |
| DAL-008 | Get silos by instrument | SiloRepository | get_by_instrument() | 10 |
| DAL-009 | Create chart | ChartRepository | create() | 10 |
| DAL-010 | Get chart by webhook_id | ChartRepository | get_by_webhook_id() | 10 |
| DAL-011 | Get charts by silo | ChartRepository | get_by_silo() | 10 |
| DAL-012 | Create signal | SignalRepository | create() | 10 |
| DAL-013 | Get latest signal by chart | SignalRepository | get_latest_by_chart() | 10 |
| DAL-014 | Get signals in time range | SignalRepository | get_by_time_range() | 10 |
| DAL-015 | Create basket | BasketRepository | create() | 10 |
| DAL-016 | Add chart to basket | BasketRepository | add_chart() | 10 |
| DAL-017 | Remove chart from basket | BasketRepository | remove_chart() | 10 |
| DAL-018 | Get basket with charts | BasketRepository | get_with_charts() | 10 |
| DAL-019 | Create conversation | ConversationRepository | create() | 10 |
| DAL-020 | Get conversation history | ConversationRepository | get_history() | 10 |
| DAL-021 | Track AI usage | AIUsageRepository | track_usage() | 10 |
| DAL-022 | Get usage by period | AIUsageRepository | get_by_period() | 10 |
| DAL-023 | Transaction rollback on error | All repositories | Rollback test | 10 |
| DAL-024 | Concurrent writes | SignalRepository | Race condition test | 10 |
| DAL-025 | Connection pool exhaustion | Database | Many connections | 10 |

**Subtotal: 25 tests × 10 runs = 250 executions**

---

## PART 2: FRONTEND TEST INVENTORY

### 2.1 UI COMPONENTS - BUTTON

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-BTN-001 | Render primary variant | - | Render Button variant="primary" | Teal background | 10 |
| UI-BTN-002 | Render secondary variant | - | Render Button variant="secondary" | Gray background | 10 |
| UI-BTN-003 | Render danger variant | - | Render Button variant="danger" | Red background | 10 |
| UI-BTN-004 | Render disabled state | - | Render Button disabled={true} | Opacity reduced, not clickable | 10 |
| UI-BTN-005 | Render loading state | - | Render Button isLoading={true} | Spinner visible | 10 |
| UI-BTN-006 | Click handler fires | - | Click button | onClick called once | 10 |
| UI-BTN-007 | Click disabled - no fire | disabled={true} | Click button | onClick NOT called | 10 |
| UI-BTN-008 | Click loading - no fire | isLoading={true} | Click button | onClick NOT called | 10 |
| UI-BTN-009 | Keyboard Enter activates | Button focused | Press Enter | onClick called | 10 |
| UI-BTN-010 | Keyboard Space activates | Button focused | Press Space | onClick called | 10 |
| UI-BTN-011 | Icon renders left | - | Render with leftIcon | Icon before text | 10 |
| UI-BTN-012 | Accessibility - role | - | Render Button | role="button" | 10 |
| UI-BTN-013 | Accessibility - aria-disabled | disabled={true} | Render | aria-disabled="true" | 10 |
| UI-BTN-014 | Double-click protection | - | Click twice rapidly | onClick called once (if debounced) | 10 |
| UI-BTN-015 | Size variants | - | Render sm, default, lg | Different sizes | 10 |

**Subtotal: 15 tests × 10 runs = 150 executions**

---

### 2.2 UI COMPONENTS - BADGE (CR-002 CRITICAL)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-BADGE-001 | Bullish variant renders | - | Render variant="bullish" | Green color | 10 |
| UI-BADGE-002 | Bearish variant renders | - | Render variant="bearish" | Red color | 10 |
| UI-BADGE-003 | CR-002: Bullish same size as Bearish | - | Render both | Same dimensions | 10 |
| UI-BADGE-004 | CR-002: Same font size | - | Render both | Same font-size | 10 |
| UI-BADGE-005 | CR-002: Same font weight | - | Render both | Same font-weight | 10 |
| UI-BADGE-006 | CR-002: Same padding | - | Render both | Same padding | 10 |
| UI-BADGE-007 | CR-002: Same border-radius | - | Render both | Same border-radius | 10 |
| UI-BADGE-008 | Neutral variant renders | - | Render variant="neutral" | Gray color | 10 |
| UI-BADGE-009 | Freshness variants | - | Render current/recent/stale/unavailable | Correct colors | 10 |
| UI-BADGE-010 | Basket type variants | - | Render logical/hierarchical/contextual/custom | Correct colors | 10 |
| UI-BADGE-011 | Accessibility - no aria-hidden | - | Render | Text accessible | 10 |
| UI-BADGE-012 | No "stronger" text | - | Inspect component | No such text | 10 |

**Subtotal: 12 tests × 10 runs = 120 executions**

---

### 2.3 UI COMPONENTS - CARD

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-CARD-001 | Render default variant | - | Render Card | White background, shadow | 10 |
| UI-CARD-002 | Render flat variant | - | Render variant="flat" | No shadow | 10 |
| UI-CARD-003 | Render elevated variant | - | Render variant="elevated" | Stronger shadow | 10 |
| UI-CARD-004 | CardHeader renders | - | Render with CardHeader | Header visible | 10 |
| UI-CARD-005 | CardContent renders | - | Render with CardContent | Content visible | 10 |
| UI-CARD-006 | CardFooter renders | - | Render with CardFooter | Footer visible | 10 |
| UI-CARD-007 | Children rendered | - | Render with children | Children visible | 10 |
| UI-CARD-008 | Click handler (if interactive) | - | Click card | Handler fires | 10 |

**Subtotal: 8 tests × 10 runs = 80 executions**

---

### 2.4 COMPONENTS - DISCLAIMER (CR-003 CRITICAL)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-DISC-001 | Disclaimer renders | - | Render Disclaimer | Text visible | 10 |
| UI-DISC-002 | CR-003: Exact text match | - | Render | Text equals constant | 10 |
| UI-DISC-003 | CR-003: No close button | - | Inspect | No dismiss element | 10 |
| UI-DISC-004 | CR-003: No collapse button | - | Inspect | No collapse element | 10 |
| UI-DISC-005 | CR-003: Always visible | - | Check CSS | display:block, visibility:visible | 10 |
| UI-DISC-006 | CR-003: Not opacity 0 | - | Check CSS | opacity != 0 | 10 |
| UI-DISC-007 | Accessibility - role="note" | - | Render | Has role="note" | 10 |
| UI-DISC-008 | Accessibility - aria-label | - | Render | Has descriptive aria-label | 10 |
| UI-DISC-009 | Block variant styling | - | Render variant="block" | Full width | 10 |
| UI-DISC-010 | Inline variant styling | - | Render variant="inline" | Inline display | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

### 2.5 PAGES - HOMEPAGE

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-HOME-001 | Page renders | Backend running | Navigate to / | Page loads | 10 |
| UI-HOME-002 | Constitutional banner visible | - | Render | 3 principles visible | 10 |
| UI-HOME-003 | Instruments section loads | 2 instruments | Render | 2 instrument cards | 10 |
| UI-HOME-004 | Empty state when no data | 0 instruments | Render | Empty state message | 10 |
| UI-HOME-005 | Click instrument card | 1 instrument | Click card | Navigate to detail | 10 |
| UI-HOME-006 | Loading state shows | Data loading | Render | Spinner visible | 10 |
| UI-HOME-007 | Error state shows | API error | Render | Error message | 10 |
| UI-HOME-008 | Quick stats visible | With data | Render | Stats cards visible | 10 |

**Subtotal: 8 tests × 10 runs = 80 executions**

---

### 2.6 PAGES - SILO DETAIL (CR-002/CR-003 CRITICAL)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-SILO-001 | Page renders | 1 silo | Navigate to /silos/{id} | Page loads | 10 |
| UI-SILO-002 | Charts list visible | 3 charts | Render | 3 chart cards | 10 |
| UI-SILO-003 | Contradiction panel visible | 2 contradicting charts | Render | Contradiction shown | 10 |
| UI-SILO-004 | CR-002: Both sides equal size | Contradiction | Inspect | Same dimensions | 10 |
| UI-SILO-005 | CR-002: Neutral separator | Contradiction | Inspect | "vs" not "but" | 10 |
| UI-SILO-006 | Confirmation panel visible | 2 confirming charts | Render | Confirmation shown | 10 |
| UI-SILO-007 | Narrative section visible | With signals | Render | Narrative text | 10 |
| UI-SILO-008 | CR-003: Disclaimer with narrative | With narrative | Render | Disclaimer present | 10 |
| UI-SILO-009 | Generate narrative button | No narrative | Click | Narrative generated | 10 |
| UI-SILO-010 | Freshness badges correct | Mixed freshness | Render | Correct colors | 10 |
| UI-SILO-011 | Click chart navigates | 1 chart | Click | Navigate to chart | 10 |
| UI-SILO-012 | Breadcrumb correct | - | Render | Shows path | 10 |

**Subtotal: 12 tests × 10 runs = 120 executions**

---

### 2.7 PAGES - AI CHAT (CR-001/CR-003 CRITICAL)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-CHAT-001 | Page renders | - | Navigate to /chat | Page loads | 10 |
| UI-CHAT-002 | Instrument selector works | 2 instruments | Select instrument | Selected state | 10 |
| UI-CHAT-003 | Message input works | - | Type message | Text appears | 10 |
| UI-CHAT-004 | Send message - Enter key | Message typed | Press Enter | Message sent | 10 |
| UI-CHAT-005 | Send message - button click | Message typed | Click send | Message sent | 10 |
| UI-CHAT-006 | Empty message blocked | Empty input | Click send | No send, warning | 10 |
| UI-CHAT-007 | Response displays | Message sent | Wait | Response visible | 10 |
| UI-CHAT-008 | CR-003: Disclaimer with every response | Response | Inspect | Disclaimer present | 10 |
| UI-CHAT-009 | Loading state during response | Waiting | Inspect | Spinner/typing indicator | 10 |
| UI-CHAT-010 | Conversation history shows | Multiple messages | Scroll | All messages visible | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

### 2.8 PAGES - BASKETS

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-BASK-001 | Page renders | - | Navigate to /baskets | Page loads | 10 |
| UI-BASK-002 | Empty state | 0 baskets | Render | Empty message | 10 |
| UI-BASK-003 | Basket list renders | 3 baskets | Render | 3 cards | 10 |
| UI-BASK-004 | Add basket - open modal | - | Click "Add" | Modal opens | 10 |
| UI-BASK-005 | Add basket - complete cycle | Modal open | Fill form, submit | Basket created, list updated | 10 |
| UI-BASK-006 | Add basket - cancel | Modal open | Click cancel | Modal closes, no change | 10 |
| UI-BASK-007 | Add basket - validation | Modal open | Submit empty | Error shown | 10 |
| UI-BASK-008 | Click basket navigates | 1 basket | Click | Navigate to detail | 10 |
| UI-BASK-009 | Delete basket - complete | 1 basket | Click delete, confirm | Basket removed | 10 |
| UI-BASK-010 | Type badges correct | 4 baskets (each type) | Render | Correct type colors | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

### 2.9 PAGES - PLATFORMS (KITE)

| Test ID | Test Name | Start State | Action | End State | Repetitions |
|---------|-----------|-------------|--------|-----------|-------------|
| UI-PLAT-001 | Page renders | - | Navigate to /platforms | Page loads | 10 |
| UI-PLAT-002 | Kite platform visible | - | Render | Zerodha Kite in list | 10 |
| UI-PLAT-003 | Not connected state | Not connected | Render | "Not Connected" badge | 10 |
| UI-PLAT-004 | Connect button visible | Not connected | Render | "Connect" button | 10 |
| UI-PLAT-005 | Click platform shows setup | - | Click Kite card | Setup instructions | 10 |
| UI-PLAT-006 | Setup instructions correct | - | View setup | Contains webhook URL | 10 |
| UI-PLAT-007 | Copy webhook URL | - | Click copy | Copied to clipboard | 10 |
| UI-PLAT-008 | Connect initiates OAuth | KITE_API_KEY set | Click Connect | Redirect to Kite | 10 |
| UI-PLAT-009 | Disconnect button | Connected | Render | "Disconnect" visible | 10 |
| UI-PLAT-010 | Disconnect complete | Connected | Click Disconnect | Status changes | 10 |

**Subtotal: 10 tests × 10 runs = 100 executions**

---

## PART 3: END-TO-END FLOW TESTS

### 3.1 SIGNAL INGESTION FLOW

| Test ID | Test Name | Flow | Repetitions |
|---------|-----------|------|-------------|
| E2E-SIG-001 | Complete signal flow | Create instrument → Create silo → Create chart → Send webhook → Signal stored | 10 |
| E2E-SIG-002 | Multiple signals same chart | Create chart → Send 10 signals → All 10 stored | 10 |
| E2E-SIG-003 | Signals to multiple charts | 3 charts → Send signal to each → All 3 stored | 10 |
| E2E-SIG-004 | Signal triggers freshness update | Send signal → Check freshness = CURRENT | 10 |
| E2E-SIG-005 | Signal updates latest | 2 signals to same chart → Get latest → Returns newest | 10 |

**Subtotal: 5 tests × 10 runs = 50 executions**

---

### 3.2 RELATIONSHIP DETECTION FLOW

| Test ID | Test Name | Flow | Repetitions |
|---------|-----------|------|-------------|
| E2E-REL-001 | Contradiction detection flow | 2 charts → BULLISH + BEARISH → API returns contradiction | 10 |
| E2E-REL-002 | Confirmation detection flow | 2 charts → BULLISH + BULLISH → API returns confirmation | 10 |
| E2E-REL-003 | Mixed relationships | 3 charts → B, B, BEAR → 1 confirm, 2 contradictions | 10 |
| E2E-REL-004 | Relationship persists after new signal | Contradiction exists → Send new signal → Still detected | 10 |
| E2E-REL-005 | Relationship changes with signal | BULL vs BEAR → Change one to BULL → Now confirmation | 10 |

**Subtotal: 5 tests × 10 runs = 50 executions**

---

### 3.3 NARRATIVE GENERATION FLOW

| Test ID | Test Name | Flow | Repetitions |
|---------|-----------|------|-------------|
| E2E-NAR-001 | Complete narrative flow | Setup data → Request narrative → Narrative returned with disclaimer | 10 |
| E2E-NAR-002 | Narrative describes contradiction | Contradiction exists → Generate → Mentions both directions | 10 |
| E2E-NAR-003 | Narrative describes confirmation | Confirmation exists → Generate → Mentions alignment | 10 |
| E2E-NAR-004 | Narrative NO recommendation | Any data → Generate → No prescriptive language | 10 |
| E2E-NAR-005 | Narrative fallback | Mock Claude error → Generate → Fallback with disclaimer | 10 |

**Subtotal: 5 tests × 10 runs = 50 executions**

---

### 3.4 USER JOURNEY TESTS

| Test ID | Test Name | Flow | Repetitions |
|---------|-----------|------|-------------|
| E2E-USR-001 | New user complete journey | Open app → See dashboard → Click instrument → See silo → See narrative | 10 |
| E2E-USR-002 | Create basket journey | Dashboard → Baskets → Add basket → Add charts → View basket | 10 |
| E2E-USR-003 | AI chat journey | Dashboard → AI Chat → Select instrument → Ask question → Get answer | 10 |
| E2E-USR-004 | Platform connect journey | Dashboard → Platforms → Select Kite → View setup → Connect | 10 |
| E2E-USR-005 | Settings journey | Dashboard → Settings → AI Settings → View budget → Change model | 10 |

**Subtotal: 5 tests × 10 runs = 50 executions**

---

## PART 4: STRESS/CHAOS TESTS

### 4.1 INVALID INPUT HANDLING

| Test ID | Test Name | Input | Expected | Repetitions |
|---------|-----------|-------|----------|-------------|
| CHAOS-001 | SQL injection attempt | symbol="'; DROP TABLE--" | Safely rejected | 10 |
| CHAOS-002 | XSS attempt | display_name="<script>alert()</script>" | Sanitized | 10 |
| CHAOS-003 | Oversized JSON | 1MB payload | 413 error | 10 |
| CHAOS-004 | Deeply nested JSON | 100 levels deep | Rejected | 10 |
| CHAOS-005 | Unicode extremes | emoji, RTL, zero-width | Handled | 10 |
| CHAOS-006 | Null bytes | Contains \x00 | Rejected | 10 |
| CHAOS-007 | Path traversal | webhook_id="../../../etc/passwd" | Rejected | 10 |

**Subtotal: 7 tests × 10 runs = 70 executions**

---

### 4.2 CONCURRENT LOAD

| Test ID | Test Name | Load | Expected | Repetitions |
|---------|-----------|------|----------|-------------|
| CHAOS-008 | 100 concurrent webhooks | 100 parallel POSTs | All succeed or rate-limited | 10 |
| CHAOS-009 | 50 concurrent reads | 50 parallel GETs | All succeed | 10 |
| CHAOS-010 | Mixed read/write | 25 GETs + 25 POSTs | No race conditions | 10 |
| CHAOS-011 | Database connection pool | 100 connections | Pooling works | 10 |

**Subtotal: 4 tests × 10 runs = 40 executions**

---

## EXECUTION SUMMARY

| Category | Tests | Runs per Test | Total Executions |
|----------|-------|---------------|------------------|
| API - Instruments | 20 | 10 | 200 |
| API - Silos | 15 | 10 | 150 |
| API - Charts | 15 | 10 | 150 |
| API - Webhooks | 18 | 10 | 180 |
| API - Relationships | 12 | 10 | 120 |
| API - Narratives | 8 | 10 | 80 |
| API - Baskets | 10 | 10 | 100 |
| API - AI | 10 | 10 | 100 |
| API - Chat | 8 | 10 | 80 |
| API - Platforms | 10 | 10 | 100 |
| Constitutional Compliance | 25 | 10 | 250 |
| Data Access Layer | 25 | 10 | 250 |
| UI - Button | 15 | 10 | 150 |
| UI - Badge | 12 | 10 | 120 |
| UI - Card | 8 | 10 | 80 |
| UI - Disclaimer | 10 | 10 | 100 |
| UI - HomePage | 8 | 10 | 80 |
| UI - SiloDetail | 12 | 10 | 120 |
| UI - AIChat | 10 | 10 | 100 |
| UI - Baskets | 10 | 10 | 100 |
| UI - Platforms | 10 | 10 | 100 |
| E2E - Signal Flow | 5 | 10 | 50 |
| E2E - Relationships | 5 | 10 | 50 |
| E2E - Narratives | 5 | 10 | 50 |
| E2E - User Journeys | 5 | 10 | 50 |
| Chaos - Invalid Input | 7 | 10 | 70 |
| Chaos - Concurrent Load | 4 | 10 | 40 |
| **TOTAL** | **292** | **10** | **2,920** |

---

## EXECUTION PHASES

### Phase 1: Backend Unit Tests
- Duration: ~20 minutes
- Tests: 141 (1,410 executions)
- Output: `tests/backend/` results

### Phase 2: Constitutional Compliance Tests
- Duration: ~10 minutes
- Tests: 25 (250 executions)
- Output: `tests/constitutional/` results

### Phase 3: Data Access Layer Tests
- Duration: ~10 minutes
- Tests: 25 (250 executions)
- Output: `tests/dal/` results

### Phase 4: Frontend Component Tests
- Duration: ~15 minutes
- Tests: 55 (550 executions)
- Output: `tests/frontend/` results

### Phase 5: Frontend Page Tests
- Duration: ~15 minutes
- Tests: 50 (500 executions)
- Output: `tests/frontend/pages/` results

### Phase 6: End-to-End Flow Tests
- Duration: ~15 minutes
- Tests: 20 (200 executions)
- Output: `tests/e2e/` results

### Phase 7: Chaos/Stress Tests
- Duration: ~10 minutes
- Tests: 11 (110 executions)
- Output: `tests/chaos/` results

### Total Estimated Duration: ~95 minutes

---

## SUCCESS CRITERIA

| Criterion | Requirement |
|-----------|-------------|
| All tests pass | 292/292 |
| All executions pass | 2,920/2,920 |
| Zero constitutional violations | 0 |
| Code coverage | >90% |
| No flaky tests | 100% consistency across 10 runs |

---

## APPROVAL GATE

**This document requires your approval before execution begins.**

Upon approval, I will:
1. Implement all test code
2. Execute all tests autonomously
3. Capture all results
4. Generate comprehensive report
5. Remediate any failures
6. Re-run until all pass

---

**Document Status:** AWAITING APPROVAL

**Approver:** [User]

**Date:** _______________

**Signature:** _______________

