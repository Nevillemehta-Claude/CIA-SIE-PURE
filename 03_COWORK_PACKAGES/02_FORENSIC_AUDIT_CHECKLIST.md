# BACKEND FORENSIC AUDIT CHECKLIST

**Classification:** OPERATIONAL DIRECTIVE
**Phase:** 1 - Forensic Audit
**Framework:** Gold Standard System v1.0

---

## SECTION A: FILE INVENTORY AUDIT

### A1. Source Code Files
Read and document every file in:

```
/src/cia_sie/
├── __init__.py                 [ ] Read  [ ] Documented
├── main.py                     [ ] Read  [ ] Documented
│
├── api/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── app.py                  [ ] Read  [ ] Documented
│   └── routes/
│       ├── __init__.py         [ ] Read  [ ] Documented
│       ├── signals.py          [ ] Read  [ ] Documented
│       ├── narratives.py       [ ] Read  [ ] Documented
│       ├── charts.py           [ ] Read  [ ] Documented
│       ├── platforms.py        [ ] Read  [ ] Documented
│       ├── silos.py            [ ] Read  [ ] Documented
│       ├── ai.py               [ ] Read  [ ] Documented
│       ├── strategy.py         [ ] Read  [ ] Documented
│       ├── instruments.py      [ ] Read  [ ] Documented
│       ├── chat.py             [ ] Read  [ ] Documented
│       ├── webhooks.py         [ ] Read  [ ] Documented
│       ├── baskets.py          [ ] Read  [ ] Documented
│       └── relationships.py    [ ] Read  [ ] Documented
│
├── core/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── enums.py                [ ] Read  [ ] Documented
│   ├── config.py               [ ] Read  [ ] Documented
│   ├── models.py               [ ] Read  [ ] Documented
│   ├── security.py             [ ] Read  [ ] Documented
│   └── exceptions.py           [ ] Read  [ ] Documented
│
├── dal/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── models.py               [ ] Read  [ ] Documented
│   ├── database.py             [ ] Read  [ ] Documented
│   └── repositories.py         [ ] Read  [ ] Documented
│
├── ai/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── claude_client.py        [ ] Read  [ ] Documented
│   ├── prompt_builder.py       [ ] Read  [ ] Documented
│   ├── narrative_generator.py  [ ] Read  [ ] Documented
│   ├── response_validator.py   [ ] Read  [ ] Documented
│   ├── usage_tracker.py        [ ] Read  [ ] Documented
│   └── model_registry.py       [ ] Read  [ ] Documented
│
├── exposure/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── contradiction_detector.py [ ] Read  [ ] Documented
│   ├── confirmation_detector.py  [ ] Read  [ ] Documented
│   └── relationship_exposer.py   [ ] Read  [ ] Documented
│
├── ingestion/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── webhook_handler.py      [ ] Read  [ ] Documented
│   ├── signal_normalizer.py    [ ] Read  [ ] Documented
│   └── freshness.py            [ ] Read  [ ] Documented
│
├── platforms/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   ├── base.py                 [ ] Read  [ ] Documented
│   ├── kite.py                 [ ] Read  [ ] Documented
│   ├── tradingview.py          [ ] Read  [ ] Documented
│   └── registry.py             [ ] Read  [ ] Documented
│
├── webhooks/
│   ├── __init__.py             [ ] Read  [ ] Documented
│   └── tradingview_receiver.py [ ] Read  [ ] Documented
│
└── bridge/
    └── __init__.py             [ ] Read  [ ] Documented
```

### A2. Test Files
Read and document every file in:

```
/tests/
├── conftest.py                 [ ] Read  [ ] Documented
├── unit/                       [ ] Read all files
├── integration/                [ ] Read all files
└── e2e/                        [ ] Read all files
```

### A3. Configuration Files
```
/
├── pyproject.toml              [ ] Read  [ ] Documented
├── alembic.ini                 [ ] Read  [ ] Documented
└── alembic/
    └── versions/               [ ] Read all migrations
```

---

## SECTION B: ARCHITECTURE DOCUMENT AUDIT

### B1. Existing Flowcharts (MUST READ)

| Document | Location | Status |
|----------|----------|--------|
| BACKEND_FLOWCHARTS.md | `/documentation/02_ARCHITECTURE/` | [ ] Read |
| FRONTEND_DATA_FLOW.md | `/documentation/02_ARCHITECTURE/` | [ ] Read |
| SIGNAL_FLOW_MATRIX.md | `/documentation/AEROSPACE_SYSTEMS_MANUAL/` | [ ] Read |
| OPERATIONAL_GUIDE_SIGNAL_FLOW.html | `/documentation/prototypes/` | [ ] Read |
| SYSTEM_ARCHITECTURE_VISUAL.html | `/documentation/06_AUDITS/` | [ ] Read |

### B2. Audit Reports (MUST READ)

| Document | Location | Status |
|----------|----------|--------|
| PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_2_BACKEND_CODE_AUDIT.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_4_DATA_LAYER_AUDIT.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_5_API_SPECIFICATION_AUDIT.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_6_TEST_COVERAGE_AUDIT.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_8_CONSTITUTIONAL_COMPLIANCE_AUDIT.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_9C_GAP_ANALYSIS.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |
| PHASE_9D_REMEDIATION_ROADMAP.md | `/documentation/06_AUDITS/handoff_audit/` | [ ] Read |

---

## SECTION C: API ENDPOINT INVENTORY

For each route file, extract and document:

### C1. Endpoint Template
```
ENDPOINT: [METHOD] [PATH]
├── Handler Function: [function name]
├── File Location: [file:line]
├── Request Model: [Pydantic model or None]
├── Response Model: [Pydantic model or None]
├── Dependencies: [list of dependencies]
├── Database Operations: [list of DB calls]
├── External Calls: [Kite/Claude/etc.]
├── Error Handling: [exception types caught]
├── Constitutional Compliance: [PASS/FAIL/NA]
└── Test Coverage: [test file:function or NONE]
```

### C2. Endpoints to Document

**signals.py:**
- [ ] POST /api/v1/signals/webhook/{webhook_id}
- [ ] GET /api/v1/signals/{signal_id}
- [ ] GET /api/v1/signals/chart/{chart_id}
- [ ] GET /api/v1/signals/latest/{chart_id}

**narratives.py:**
- [ ] GET /api/v1/narratives/silo/{silo_id}
- [ ] GET /api/v1/narratives/chart/{chart_id}

**charts.py:**
- [ ] GET /api/v1/charts
- [ ] POST /api/v1/charts
- [ ] GET /api/v1/charts/{chart_id}
- [ ] PUT /api/v1/charts/{chart_id}
- [ ] DELETE /api/v1/charts/{chart_id}

**silos.py:**
- [ ] GET /api/v1/silos
- [ ] POST /api/v1/silos
- [ ] GET /api/v1/silos/{silo_id}
- [ ] PUT /api/v1/silos/{silo_id}
- [ ] DELETE /api/v1/silos/{silo_id}

**instruments.py:**
- [ ] GET /api/v1/instruments
- [ ] POST /api/v1/instruments
- [ ] GET /api/v1/instruments/{instrument_id}

**platforms.py:**
- [ ] GET /api/v1/platforms
- [ ] GET /api/v1/platforms/{platform}/status
- [ ] GET /api/v1/platforms/kite/login
- [ ] GET /api/v1/platforms/kite/callback

**baskets.py:**
- [ ] GET /api/v1/baskets
- [ ] POST /api/v1/baskets
- [ ] GET /api/v1/baskets/{basket_id}
- [ ] PUT /api/v1/baskets/{basket_id}

**relationships.py:**
- [ ] GET /api/v1/relationships/silo/{silo_id}
- [ ] GET /api/v1/relationships/instrument/{instrument_id}

**ai.py:**
- [ ] GET /api/v1/ai/usage
- [ ] GET /api/v1/ai/models

**chat.py:**
- [ ] POST /api/v1/chat/{instrument_id}
- [ ] GET /api/v1/chat/{instrument_id}/history

---

## SECTION D: DATABASE SCHEMA AUDIT

### D1. Table Inventory
For each table in `dal/models.py`:

```
TABLE: [table_name]
├── Columns:
│   ├── [column_name]: [type] [constraints]
│   └── ...
├── Primary Key: [column(s)]
├── Foreign Keys: [relationships]
├── Indexes: [index definitions]
├── Prohibited Columns Check:
│   ├── weight: [EXISTS/ABSENT]
│   ├── score: [EXISTS/ABSENT]
│   ├── confidence: [EXISTS/ABSENT]
│   ├── recommendation: [EXISTS/ABSENT]
│   └── priority: [EXISTS/ABSENT]
└── Constitutional Status: [COMPLIANT/VIOLATION]
```

### D2. Tables to Audit
- [ ] instruments
- [ ] silos
- [ ] charts
- [ ] signals
- [ ] analytical_baskets
- [ ] basket_charts
- [ ] conversations
- [ ] ai_usage

### D3. Migration History
- [ ] Document all Alembic migrations in order
- [ ] Verify each migration has rollback capability

---

## SECTION E: CONSTITUTIONAL COMPLIANCE AUDIT

### E1. AI Response Validator Check
File: `ai/response_validator.py`

**Must verify these prohibited patterns are checked:**
- [ ] "you should"
- [ ] "I recommend"
- [ ] "consider buying/selling"
- [ ] "overall direction"
- [ ] "net signal"
- [ ] "consensus"
- [ ] "confidence: X%"
- [ ] "probability of"
- [ ] "stronger/weaker signal"

**Must verify mandatory disclaimer check:**
- [ ] Response must end with user authority reminder

### E2. Prompt Builder Check
File: `ai/prompt_builder.py`

**Must verify constraints are injected:**
- [ ] "DESCRIBE signals, do not PRESCRIBE"
- [ ] "EXPOSE contradictions, do not RESOLVE"
- [ ] "NEVER compute aggregate scores"
- [ ] "ALWAYS present ALL signals with equal weight"

### E3. Exposure Module Check
Files: `exposure/*.py`

**ContradictionDetector:**
- [ ] Detects opposing signals between charts
- [ ] Does NOT resolve or prioritize
- [ ] Returns list without ranking

**ConfirmationDetector:**
- [ ] Detects aligned signals
- [ ] Does NOT strengthen or weight
- [ ] Returns list without aggregation

### E4. Database Schema Check
File: `dal/models.py`

**PROHIBITED columns (must be ABSENT):**
- [ ] `weight` on any table
- [ ] `score` on any table
- [ ] `confidence` on any table
- [ ] `recommendation` on any table
- [ ] `priority` on signals
- [ ] `rank` on signals

---

## SECTION F: INTEGRATION AUDIT

### F1. Kite Integration
File: `platforms/kite.py`

- [ ] OAuth flow implemented correctly
- [ ] Token storage (memory-only, not persisted)
- [ ] Session management (daily expiry)
- [ ] Error handling for API failures
- [ ] Rate limit handling

### F2. Claude AI Integration
Files: `ai/claude_client.py`, `ai/narrative_generator.py`

- [ ] API key configuration
- [ ] Model selection logic
- [ ] Token tracking implementation
- [ ] Fallback handling when AI unavailable
- [ ] Retry logic with temperature reduction

### F3. TradingView Webhook Integration
Files: `ingestion/webhook_handler.py`, `webhooks/tradingview_receiver.py`

- [ ] Webhook signature validation
- [ ] Payload normalization
- [ ] Chart lookup by webhook_id
- [ ] Signal storage
- [ ] Error responses

---

## SECTION G: GAP ANALYSIS TEMPLATE

### G1. Gap Types to Identify

| Gap Type | Definition | Severity |
|----------|------------|----------|
| Schema Drift | DB differs from documented schema | HIGH |
| Orphaned Endpoint | API route with no matching spec | MEDIUM |
| Phantom Feature | Documented but not implemented | HIGH |
| Stale Documentation | Docs don't match current code | MEDIUM |
| Missing Test | Implemented but no test coverage | MEDIUM |
| Constitutional Violation | Section 0B non-compliance | CRITICAL |
| Broken Integration | External system not working | HIGH |
| Dead Code | Code that is never executed | LOW |

### G2. Gap Documentation Format
```
GAP-[ID]:
├── Type: [gap type from above]
├── Severity: [CRITICAL/HIGH/MEDIUM/LOW]
├── Location: [file:line or document]
├── Description: [what is wrong]
├── Evidence: [how discovered]
├── Remediation: [fix code | update spec | remove]
└── Effort: [hours estimate]
```

---

## SECTION H: DELIVERABLE TEMPLATES

### H1. FORENSIC_AUDIT_INVENTORY.md
```markdown
# Forensic Audit Inventory

## Source Files
[List all files with line counts, last modified, purpose]

## API Endpoints
[Table of all endpoints with coverage status]

## Database Tables
[Schema documentation]

## Integration Points
[External system connections]
```

### H2. GAP_ANALYSIS_REPORT.md
```markdown
# Gap Analysis Report

## Summary Statistics
- Total gaps: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Gap Registry
[All gaps documented per template]

## Remediation Priority
[Ordered list by severity and effort]
```

### H3. CONSTITUTIONAL_COMPLIANCE_MATRIX.md
```markdown
# Constitutional Compliance Matrix

## Section 0B Requirements

| Requirement | Location | Status | Evidence |
|-------------|----------|--------|----------|
| No weight columns | dal/models.py | PASS | Grep shows 0 matches |
| No score calculations | exposure/*.py | PASS | Code review |
| ...

## Violations Found
[List of any violations with remediation plan]

## Certification
[ ] Backend is fully Section 0B compliant
```

---

## AUDIT EXECUTION ORDER

1. **Read all architecture flowcharts** (Section B1)
2. **Read all existing audit reports** (Section B2)
3. **Inventory all source files** (Section A)
4. **Document all API endpoints** (Section C)
5. **Audit database schema** (Section D)
6. **Constitutional compliance check** (Section E)
7. **Integration audit** (Section F)
8. **Compile gap analysis** (Section G)
9. **Generate deliverables** (Section H)

---

**END OF CHECKLIST**

*Use this checklist systematically. Do not skip sections.*
