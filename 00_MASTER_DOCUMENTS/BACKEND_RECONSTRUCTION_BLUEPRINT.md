# CIA-SIE BACKEND RECONSTRUCTION BLUEPRINT
## Actionable Technical Specification for Backend Verification & Repair

---

**Document Version:** 1.0.0
**Generated:** 2026-01-15
**Companion To:** MASTER_FOUNDATIONAL_DOCUMENT.md
**Purpose:** Step-by-step verification and reconstruction guide

---

## EXECUTIVE SUMMARY

This blueprint provides an **actionable verification checklist** for the CIA-SIE backend. Based on forensic analysis of 77 HTML specification files and comparison with the current implementation at `/Users/nevillemehta/Downloads/CIA-SIE-PURE/`, this document identifies:

1. **VERIFIED COMPLIANT** - Components meeting specification
2. **REQUIRES VERIFICATION** - Components needing testing
3. **GAP IDENTIFIED** - Missing or incorrect implementations
4. **RECONSTRUCTION TASKS** - Specific fixes required

---

## TABLE OF CONTENTS

1. [Current Implementation Assessment](#1-current-implementation-assessment)
2. [Constitutional Compliance Audit](#2-constitutional-compliance-audit)
3. [Data Layer Verification](#3-data-layer-verification)
4. [API Layer Verification](#4-api-layer-verification)
5. [Business Logic Verification](#5-business-logic-verification)
6. [AI Integration Verification](#6-ai-integration-verification)
7. [Reconstruction Task List](#7-reconstruction-task-list)
8. [Testing Protocol](#8-testing-protocol)
9. [Deployment Checklist](#9-deployment-checklist)

---

## 1. CURRENT IMPLEMENTATION ASSESSMENT

### 1.1 File Structure Analysis

**VERIFIED: Directory structure matches specification**

```
src/cia_sie/
├── __init__.py                      ✅ EXISTS
├── main.py                          ✅ EXISTS (61 lines)
├── api/
│   ├── __init__.py                  ✅ EXISTS
│   ├── app.py                       ✅ EXISTS (220 lines) - FastAPI factory
│   └── routes/
│       ├── __init__.py              ✅ EXISTS - 13 routers registered
│       ├── instruments.py           ✅ EXISTS
│       ├── silos.py                 ✅ EXISTS
│       ├── charts.py                ✅ EXISTS
│       ├── signals.py               ✅ EXISTS
│       ├── webhooks.py              ✅ EXISTS
│       ├── relationships.py         ✅ EXISTS
│       ├── narratives.py            ✅ EXISTS
│       ├── baskets.py               ✅ EXISTS
│       ├── platforms.py             ✅ EXISTS
│       ├── ai.py                    ✅ EXISTS
│       ├── chat.py                  ✅ EXISTS
│       ├── strategy.py              ✅ EXISTS
│       └── market_intelligence.py   ✅ EXISTS (extension)
├── ai/
│   ├── __init__.py                  ✅ EXISTS
│   ├── claude_client.py             ✅ EXISTS
│   ├── model_registry.py            ✅ EXISTS
│   ├── narrative_generator.py       ✅ EXISTS
│   ├── prompt_builder.py            ✅ EXISTS (275 lines) - VERIFIED COMPLIANT
│   ├── response_validator.py        ✅ EXISTS (498 lines) - VERIFIED COMPLIANT
│   ├── usage_tracker.py             ✅ EXISTS
│   └── market_intelligence_agent.py ✅ EXISTS (extension)
├── core/
│   ├── __init__.py                  ✅ EXISTS
│   ├── config.py                    ✅ EXISTS
│   ├── enums.py                     ✅ EXISTS (159 lines) - VERIFIED COMPLIANT
│   ├── exceptions.py                ✅ EXISTS
│   ├── models.py                    ✅ EXISTS
│   └── security.py                  ✅ EXISTS
├── dal/
│   ├── __init__.py                  ✅ EXISTS
│   ├── database.py                  ✅ EXISTS
│   ├── models.py                    ✅ EXISTS (363 lines) - VERIFIED COMPLIANT
│   └── repositories.py              ✅ EXISTS (476 lines) - VERIFIED COMPLIANT
├── exposure/
│   ├── __init__.py                  ✅ EXISTS
│   ├── confirmation_detector.py     ✅ EXISTS
│   ├── contradiction_detector.py    ✅ EXISTS (166 lines) - VERIFIED COMPLIANT
│   └── relationship_exposer.py      ✅ EXISTS
├── ingestion/
│   ├── __init__.py                  ✅ EXISTS
│   ├── freshness.py                 ✅ EXISTS
│   ├── signal_normalizer.py         ✅ EXISTS
│   └── webhook_handler.py           ✅ EXISTS (260 lines) - VERIFIED COMPLIANT
├── platforms/
│   ├── __init__.py                  ✅ EXISTS
│   ├── base.py                      ✅ EXISTS
│   ├── kite.py                      ✅ EXISTS
│   ├── kite_intelligence.py         ✅ EXISTS (extension)
│   ├── registry.py                  ✅ EXISTS
│   └── tradingview.py               ✅ EXISTS
├── webhooks/
│   ├── __init__.py                  ✅ EXISTS
│   └── tradingview_receiver.py      ✅ EXISTS
└── bridge/
    └── __init__.py                  ✅ EXISTS
```

### 1.2 Module Count Summary

| Category | Required | Implemented | Status |
|----------|----------|-------------|--------|
| API Routes | 12 | 13 | ✅ EXCEEDS (includes market_intelligence) |
| AI Modules | 6 | 7 | ✅ EXCEEDS (includes market_intelligence_agent) |
| Core Modules | 5 | 5 | ✅ MATCHES |
| DAL Modules | 3 | 3 | ✅ MATCHES |
| Exposure Modules | 3 | 3 | ✅ MATCHES |
| Ingestion Modules | 3 | 3 | ✅ MATCHES |
| Platform Modules | 4 | 5 | ✅ EXCEEDS (includes kite_intelligence) |

---

## 2. CONSTITUTIONAL COMPLIANCE AUDIT

### 2.1 CR-001: Decision-Support, NOT Decision-Making

**VERIFICATION STATUS: ✅ COMPLIANT**

Evidence from `src/cia_sie/ai/prompt_builder.py`:

```python
# Lines 64-69: Explicit prohibition
5. NEVER use these phrases:
   - "you should"
   - "I recommend"
   - "the best action"
   - "you might want to"
   - "consider buying/selling"
```

```python
# Lines 70-76: Prohibits computation of aggregates
6. NEVER compute:
   - Overall direction from multiple signals
   - Confidence scores or percentages
   - Rankings of which signals are "better"
   - Net position or summary bias
```

**TEST REQUIRED:** Verify AI responses never contain prohibited phrases.

---

### 2.2 CR-002: Expose Contradictions, NEVER Resolve Them

**VERIFICATION STATUS: ✅ COMPLIANT**

Evidence from `src/cia_sie/exposure/contradiction_detector.py`:

```python
# Lines 8-18: Docstring explicitly states purpose
"""
DOES:
- Identify BULLISH vs BEARISH conflicts
- Return list of all contradictions found

DOES NOT:
- Resolve contradictions
- Suggest which is "right"
- Weight or prioritize signals
- Hide any contradiction
"""
```

```python
# Lines 138-154: Implementation matches spec
def _is_contradiction(self, direction_a: Direction, direction_b: Direction) -> bool:
    """
    A contradiction exists when:
    - One is BULLISH and the other is BEARISH
    """
    return (direction_a == Direction.BULLISH and direction_b == Direction.BEARISH) or (
        direction_a == Direction.BEARISH and direction_b == Direction.BULLISH
    )
```

**TEST REQUIRED:** Confirm all contradiction pairs are returned, none filtered.

---

### 2.3 CR-003: Descriptive AI, NOT Prescriptive AI

**VERIFICATION STATUS: ✅ COMPLIANT**

Evidence from `src/cia_sie/ai/response_validator.py`:

```python
# Lines 35-121: 30+ prohibited patterns defined
PROHIBITED_PATTERNS: list[tuple[str, str, str]] = [
    (r"\byou\s+should\b", "Contains 'you should' - implies recommendation", "CRITICAL"),
    (r"\bi\s+recommend\b", "Contains 'I recommend' - direct recommendation", "CRITICAL"),
    # ... 28 more patterns
]
```

```python
# Lines 128-138: Mandatory disclaimer requirement
MANDATORY_DISCLAIMER = (
    "This is a description of what your charts are showing. "
    "The interpretation and any decision is entirely yours."
)
```

**TEST REQUIRED:** Run AI responses through validator, verify all pass.

---

## 3. DATA LAYER VERIFICATION

### 3.1 Database Models

**VERIFICATION STATUS: ✅ COMPLIANT**

| Model | Required Columns | Implementation Status | Constitutional Compliance |
|-------|------------------|----------------------|---------------------------|
| InstrumentDB | instrument_id, symbol, display_name, created_at, is_active | ✅ VERIFIED (line 50-76) | ✅ No prohibited columns |
| SiloDB | silo_id, instrument_id, silo_name, heartbeat settings | ✅ VERIFIED (line 79-115) | ✅ No prohibited columns |
| ChartDB | chart_id, silo_id, chart_code, webhook_id | ✅ VERIFIED (line 118-160) | ✅ **NO WEIGHT COLUMN** (per ADR-003) |
| SignalDB | signal_id, chart_id, direction, signal_type, indicators | ✅ VERIFIED (line 163-195) | ✅ **NO CONFIDENCE COLUMN** (per ADR-003) |
| AnalyticalBasketDB | basket_id, basket_name, basket_type | ✅ VERIFIED (line 198-232) | ✅ UI-layer only |
| BasketChartDB | basket_id, chart_id (M:N junction) | ✅ VERIFIED (line 235-263) | ✅ Junction table only |
| ConversationDB | conversation_id, instrument_id, messages | ✅ VERIFIED (line 271-305) | ✅ No learning/training |
| AIUsageDB | id, period_type, tokens, cost | ✅ VERIFIED (line 308-335) | ✅ Usage tracking only |
| SavedQueryDB | query_id, query_name, template | ✅ VERIFIED (line 338-362) | ✅ Extension feature |

### 3.2 Repository Layer

**VERIFICATION STATUS: ✅ COMPLIANT**

| Repository | Key Methods | Status |
|------------|-------------|--------|
| InstrumentRepository | get_by_id, get_by_symbol, get_all, create, update, delete | ✅ VERIFIED |
| SiloRepository | get_by_id, get_by_instrument, get_with_charts, create, delete | ✅ VERIFIED |
| ChartRepository | get_by_id, get_by_webhook_id, get_by_silo, create, delete | ✅ VERIFIED |
| SignalRepository | get_by_id, get_by_chart, get_latest_by_chart, get_latest_by_charts, create | ✅ VERIFIED |
| BasketRepository | get_by_id, get_with_charts, add_chart_to_basket, remove_chart_from_basket | ✅ VERIFIED |

### 3.3 Enumeration Types

**VERIFICATION STATUS: ✅ COMPLIANT**

| Enum | Values | Source Line |
|------|--------|-------------|
| SignalType | HEARTBEAT, STATE_CHANGE, BAR_CLOSE, MANUAL, TREND | Lines 14-31 |
| Direction | BULLISH, BEARISH, NEUTRAL | Lines 34-48 |
| FreshnessStatus | CURRENT, RECENT, STALE, UNAVAILABLE | Lines 51-69 |
| BasketType | LOGICAL, HIERARCHICAL, CONTEXTUAL, CUSTOM | Lines 72-89 |
| ValidationStatus | VALID, INVALID, REMEDIATED | Lines 111-125 |
| AIModelTier | HAIKU, SONNET, OPUS | Lines 128-139 |

---

## 4. API LAYER VERIFICATION

### 4.1 Router Registration

**VERIFICATION STATUS: ✅ COMPLIANT**

From `src/cia_sie/api/routes/__init__.py` (lines 28-40):

| Router | Prefix | Status |
|--------|--------|--------|
| instruments_router | /instruments | ✅ REGISTERED |
| silos_router | /silos | ✅ REGISTERED |
| charts_router | /charts | ✅ REGISTERED |
| signals_router | /signals | ✅ REGISTERED |
| webhooks_router | /webhook | ✅ REGISTERED |
| relationships_router | /relationships | ✅ REGISTERED |
| narratives_router | /narratives | ✅ REGISTERED |
| baskets_router | /baskets | ✅ REGISTERED |
| platforms_router | /platforms | ✅ REGISTERED |
| ai_router | /ai | ✅ REGISTERED |
| chat_router | /chat | ✅ REGISTERED |
| strategy_router | /strategy | ✅ REGISTERED |
| market_intelligence_router | /market-intelligence | ✅ REGISTERED (extension) |

### 4.2 Application Factory

**VERIFICATION STATUS: ✅ COMPLIANT**

From `src/cia_sie/api/app.py`:

| Feature | Spec Requirement | Implementation | Status |
|---------|------------------|----------------|--------|
| CORS Middleware | Environment-based | Lines 127-155 | ✅ |
| Security Headers | OWASP recommended | Lines 118-121 | ✅ |
| Rate Limiting | Per-endpoint | Lines 123-124 | ✅ |
| Health Endpoint | /health | Lines 165-183 | ✅ |
| API Versioning | /api/v1 prefix | Line 162 | ✅ |
| Docs Disabled in Prod | docs_url=None | Lines 108-109 | ✅ |

### 4.3 Endpoint Verification Checklist

**REQUIRES MANUAL TESTING**

| Endpoint | Method | Expected Behavior | Test Status |
|----------|--------|-------------------|-------------|
| POST /api/v1/webhook/ | POST | Accept TradingView payload, store signal | ⏳ PENDING |
| GET /api/v1/instruments/ | GET | Return all instruments | ⏳ PENDING |
| POST /api/v1/instruments/ | POST | Create new instrument | ⏳ PENDING |
| GET /api/v1/silos/{id} | GET | Return silo with charts | ⏳ PENDING |
| GET /api/v1/relationships/contradictions | GET | Return all contradictions | ⏳ PENDING |
| POST /api/v1/narratives/silo/{id} | POST | Generate AI narrative | ⏳ PENDING |
| GET /api/v1/baskets/ | GET | Return all baskets | ⏳ PENDING |
| GET /health | GET | Return health status | ⏳ PENDING |

---

## 5. BUSINESS LOGIC VERIFICATION

### 5.1 Webhook Handler

**VERIFICATION STATUS: ✅ COMPLIANT**

From `src/cia_sie/ingestion/webhook_handler.py`:

| Requirement | Implementation | Lines | Status |
|-------------|----------------|-------|--------|
| Validate webhook_id exists | `await self.chart_repo.get_by_webhook_id()` | 86-91 | ✅ |
| Parse direction enum | `Direction(direction_str)` | 168-175 | ✅ |
| Parse signal_type enum | `SignalType(signal_type_str)` | 178-184 | ✅ |
| Handle timestamp parsing | ISO 8601 + Unix epoch support | 187-195 | ✅ |
| Extract indicators | Filter reserved fields | 198-199 | ✅ |
| Store raw_payload | `raw_payload=payload` | 119 | ✅ |
| Return Signal object | Domain model conversion | 132-141 | ✅ |

### 5.2 Contradiction Detector

**VERIFICATION STATUS: ✅ COMPLIANT**

| Requirement | Implementation | Lines | Status |
|-------------|----------------|-------|--------|
| Detect BULLISH vs BEARISH | `_is_contradiction()` | 138-154 | ✅ |
| Skip NEUTRAL signals | `if cs.latest_signal.direction != Direction.NEUTRAL` | 72-73 | ✅ |
| Compare all pairs | Nested loop | 76-94 | ✅ |
| Return ALL contradictions | `contradictions.append()` for each | 85-94 | ✅ |
| No resolution logic | N/A - intentionally absent | ✅ | ✅ |

### 5.3 Response Validator

**VERIFICATION STATUS: ✅ COMPLIANT**

| Requirement | Implementation | Lines | Status |
|-------------|----------------|-------|--------|
| 30+ prohibited patterns | `PROHIBITED_PATTERNS` list | 35-121 | ✅ |
| Mandatory disclaimer check | `_check_disclaimer()` | 304-315 | ✅ |
| Severity levels | CRITICAL vs WARNING | 33-34 | ✅ |
| Retry with stricter prompt | `_add_stricter_constraints()` | 438-461 | ✅ |
| Remediation support | `_remediate()` | 317-338 | ✅ |

---

## 6. AI INTEGRATION VERIFICATION

### 6.1 Prompt Builder

**VERIFICATION STATUS: ✅ COMPLIANT**

From `src/cia_sie/ai/prompt_builder.py`:

| System Prompt Element | Lines | Status |
|----------------------|-------|--------|
| "DESCRIBE signals, do not PRESCRIBE actions" | 46-48 | ✅ |
| "EXPOSE contradictions, do not RESOLVE them" | 50-52 | ✅ |
| "Every response must end with user authority reminder" | 57-58 | ✅ |
| NEVER phrases list (7 items) | 64-69 | ✅ |
| NEVER compute list (4 items) | 70-76 | ✅ |
| "ALWAYS present ALL signals with equal weight" | 77-79 | ✅ |

### 6.2 Narrative Generation Flow

**REQUIRES TESTING**

```
User Requests Narrative
        ↓
NarrativePromptBuilder.build_silo_narrative_prompt()
        ↓
ClaudeClient.generate() with NARRATIVE_SYSTEM_PROMPT
        ↓
AIResponseValidator.validate() checks 30+ patterns
        ↓
If INVALID → Retry with stricter constraints (up to 3 times)
        ↓
If still INVALID → Raise ConstitutionalViolationError
        ↓
Return validated narrative with mandatory disclaimer
```

---

## 7. RECONSTRUCTION TASK LIST

### 7.1 HIGH PRIORITY (Must Fix)

| # | Task | File | Issue | Action |
|---|------|------|-------|--------|
| 1 | **NONE IDENTIFIED** | - | Backend appears specification-compliant | Continue testing |

### 7.2 MEDIUM PRIORITY (Should Verify)

| # | Task | File | Status |
|---|------|------|--------|
| 1 | Run full test suite | tests/ | ⏳ PENDING |
| 2 | Verify all API endpoints return correct schemas | api/routes/*.py | ⏳ PENDING |
| 3 | Test webhook with live TradingView payload | ingestion/webhook_handler.py | ⏳ PENDING |
| 4 | Test AI narrative generation end-to-end | ai/narrative_generator.py | ⏳ PENDING |
| 5 | Verify database migrations are current | alembic/ | ⏳ PENDING |

### 7.3 LOW PRIORITY (Nice to Have)

| # | Task | Rationale |
|---|------|-----------|
| 1 | Add API rate limit configuration to settings | Currently hardcoded |
| 2 | Add prometheus metrics endpoint | Observability |
| 3 | Add OpenAPI schema export | Documentation |

---

## 8. TESTING PROTOCOL

### 8.1 Unit Test Commands

```bash
# Run all tests
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE
python -m pytest tests/ -v

# Run constitutional tests specifically
python -m pytest tests/constitutional/ -v

# Run API tests
python -m pytest tests/backend/ -v

# Run with coverage
python -m pytest tests/ --cov=src/cia_sie --cov-report=html
```

### 8.2 Integration Test Scenarios

**Scenario 1: Webhook Ingestion**
```bash
curl -X POST http://localhost:8000/api/v1/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_id": "GOLDBEES_01A_PRIMARY",
    "direction": "BULLISH",
    "signal_type": "STATE_CHANGE",
    "timestamp": "2026-01-15T10:30:00Z",
    "RSI": 72.5,
    "MACD": "bullish_cross"
  }'
```

**Expected Response:**
```json
{
  "status": "accepted",
  "signal_id": "uuid-here",
  "chart_id": "uuid-here",
  "direction": "BULLISH"
}
```

**Scenario 2: Contradiction Detection**
```bash
curl http://localhost:8000/api/v1/relationships/silo/{silo_id}/contradictions
```

**Expected Response:**
```json
{
  "contradictions": [
    {
      "chart_a_id": "uuid",
      "chart_a_name": "01A Primary",
      "chart_a_direction": "BULLISH",
      "chart_b_id": "uuid",
      "chart_b_name": "02 HTF Structure",
      "chart_b_direction": "BEARISH",
      "detected_at": "2026-01-15T10:35:00Z"
    }
  ]
}
```

**Scenario 3: AI Narrative**
```bash
curl -X POST http://localhost:8000/api/v1/narratives/silo/{silo_id}
```

**Expected Response:**
```json
{
  "silo_id": "uuid",
  "narrative": "Chart 01A shows a BULLISH direction with RSI at 72.5...",
  "disclaimer": "This is a description of what your charts are showing. The interpretation and any decision is entirely yours.",
  "generated_at": "2026-01-15T10:35:00Z"
}
```

### 8.3 Constitutional Compliance Tests

**Test CR-001 (No Recommendations):**
```python
def test_narrative_has_no_recommendations():
    response = generate_narrative(silo_id)
    assert "you should" not in response.lower()
    assert "recommend" not in response.lower()
    assert "consider buying" not in response.lower()
```

**Test CR-002 (Expose All Contradictions):**
```python
def test_all_contradictions_exposed():
    # Create 3 charts: 2 BULLISH, 1 BEARISH
    # Expected: 2 contradictions (BULLISH1 vs BEARISH, BULLISH2 vs BEARISH)
    contradictions = detect_contradictions(silo_id)
    assert len(contradictions) == 2
```

**Test CR-003 (Mandatory Disclaimer):**
```python
def test_disclaimer_present():
    response = generate_narrative(silo_id)
    assert "interpretation" in response.lower()
    assert "decision" in response.lower()
    assert "yours" in response.lower()
```

---

## 9. DEPLOYMENT CHECKLIST

### 9.1 Pre-Deployment

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Constitutional compliance tests pass
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] CORS origins set for production
- [ ] Webhook secret configured
- [ ] AI API key configured (ANTHROPIC_API_KEY)

### 9.2 Environment Variables

```env
# Required
DATABASE_URL=postgresql://user:pass@localhost/cia_sie
ANTHROPIC_API_KEY=sk-ant-...
WEBHOOK_SECRET=your-secret-here

# Optional
ENVIRONMENT=production
CORS_ORIGINS=https://yourfrontend.com
LOG_LEVEL=INFO
```

### 9.3 Startup Command

```bash
# Development
uvicorn cia_sie.api.app:app --reload --port 8000

# Production
uvicorn cia_sie.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 9.4 Health Check Verification

```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "app": "CIA-SIE",
  "version": "1.0.0",
  "security": {
    "webhook_auth_enabled": true,
    "cors_restricted": true,
    "rate_limiting": "enabled",
    "security_headers": "enabled"
  }
}
```

---

## CONCLUSION

### Assessment Summary

| Area | Status | Notes |
|------|--------|-------|
| **File Structure** | ✅ COMPLIANT | All required modules present |
| **Constitutional Rules** | ✅ COMPLIANT | CR-001, CR-002, CR-003 implemented |
| **Data Layer** | ✅ COMPLIANT | No prohibited columns, proper relationships |
| **API Layer** | ✅ COMPLIANT | All routers registered, proper middleware |
| **Business Logic** | ✅ COMPLIANT | Webhook, detection, validation correct |
| **AI Integration** | ✅ COMPLIANT | Prompts and validation meet spec |

### Recommendation

**The current backend implementation appears to be specification-compliant based on code review.**

The next steps should be:
1. Run the full test suite to verify runtime behavior
2. Perform live integration testing with actual TradingView webhooks
3. Test AI narrative generation with real Claude API calls
4. Verify frontend integration points

### Critical Files Reference

| Purpose | File Path |
|---------|-----------|
| Main Entry | `src/cia_sie/main.py` |
| App Factory | `src/cia_sie/api/app.py` |
| Router Registry | `src/cia_sie/api/routes/__init__.py` |
| Database Models | `src/cia_sie/dal/models.py` |
| Repositories | `src/cia_sie/dal/repositories.py` |
| Enums | `src/cia_sie/core/enums.py` |
| Webhook Handler | `src/cia_sie/ingestion/webhook_handler.py` |
| Contradiction Detector | `src/cia_sie/exposure/contradiction_detector.py` |
| AI Prompt Builder | `src/cia_sie/ai/prompt_builder.py` |
| Response Validator | `src/cia_sie/ai/response_validator.py` |

---

**END OF BACKEND RECONSTRUCTION BLUEPRINT**

*This document should be used in conjunction with MASTER_FOUNDATIONAL_DOCUMENT.md for complete system understanding.*
