# CIA-SIE PROJECT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
#                    Project-Specific Audit Configuration
#                              Version 1.0
# ══════════════════════════════════════════════════════════════════════════════

---

## DOCUMENT CONTROL

| Attribute | Value |
|-----------|-------|
| Document ID | CIA-SIE-CONFIG-001 |
| Version | 1.0 |
| Project | CIA-SIE (Chart Intelligence Auditor & Signal Intelligence Engine) |
| Framework Reference | UNIVERSAL_CODE_AUDIT_AND_APPLICATION_DEVELOPMENT_FRAMEWORK_v2.0_GENERIC.md |
| Date | 03 January 2026 |
| Status | AUTHORITATIVE |

---

## PURPOSE

This document provides the **project-specific configuration** for CIA-SIE that complements the Universal Code Audit Framework v2.0. It defines:

1. CIA-SIE's Constitutional Rules (inviolable constraints)
2. Audit Tier Assignments for all file categories
3. Prohibited Patterns specific to this domain
4. Project File Manifest with scope classifications
5. Output locations for audit deliverables

**Usage:** This document + the Universal Framework = Complete Audit Specification for CIA-SIE.

---

## SECTION 1: CONSTITUTIONAL RULES

CIA-SIE operates under **three inviolable constitutional rules**. A single violation of any rule renders the entire system non-compliant.

### RULE 1: Decision-Support, NOT Decision-Making

```
RULE 1: NO RECOMMENDATIONS

PROHIBITION:
- System shall NOT use language: "should", "recommend", "suggest", "consider"
- System shall NOT provide buy/sell/hold/action recommendations
- System shall NOT imply action through output framing
- System shall NOT include weight, score, or confidence attributes
- System shall NOT aggregate signals into overall direction

REQUIREMENT:
- Descriptive statements ONLY
- User retains ALL decision authority
- No action implication in outputs
- Equal presentation of all data points

DETECTION METHOD:
- Keyword search: should, recommend, suggest, consider, advise, ought
- Field search: weight, confidence, score, rating, ranking
- Method search: aggregate, combine, summarize, overall

VIOLATION SEVERITY: CRITICAL — Renders system non-compliant
```

### RULE 2: Expose Contradictions, NEVER Resolve Them

```
RULE 2: CONTRADICTIONS EXPOSED, NEVER RESOLVED

PROHIBITION:
- NO signal weighting or prioritisation
- NO aggregation of conflicting signals
- NO consensus calculations
- NO "overall" summaries that mask disagreement
- NO resolution logic that picks a "winner"
- NO confidence scoring on contradictions

REQUIREMENT:
- Display ALL contradictions explicitly
- Equal visual prominence for all signals
- No resolution logic anywhere in codebase
- User sees raw disagreement, not synthesised view

DETECTION METHOD:
- Keyword search: resolve, consensus, overall, aggregate, weight, priority
- Column search: resolution, winner, primary, dominant
- Logic search: if/else that picks between conflicting signals

VIOLATION SEVERITY: CRITICAL — Renders system non-compliant
```

### RULE 3: Descriptive AI, NOT Prescriptive AI

```
RULE 3: AI DISCLAIMERS ON ALL AI OUTPUT

PROHIBITION:
- AI shall NOT prescribe action
- AI shall NOT predict outcomes
- AI shall NOT make recommendations
- AI shall NOT express confidence in predictions
- AI shall NOT use directional language (bullish, bearish, positive, negative outlook)

REQUIREMENT:
- AI describes data ONLY
- Interpretation remains with user
- Mandatory disclaimer on ALL AI-generated content

MANDATORY DISCLAIMER:
"This is a description of what your data shows.
 The interpretation and any decision is entirely yours."

DETECTION METHOD:
- Output validation: Check all AI responses contain disclaimer
- Keyword search: predict, forecast, expect, likely, probably, bullish, bearish
- Pattern search: future tense predictions, outcome statements

VIOLATION SEVERITY: CRITICAL — Renders system non-compliant
```

---

## SECTION 2: PROHIBITED PATTERNS REGISTRY

### 2.1 Category A: Prescriptive Language (Domain-Specific)

| Pattern | Type | Detection |
|---------|------|-----------|
| `should` | Keyword | Case-insensitive search |
| `recommend` | Keyword | Case-insensitive search |
| `suggest` | Keyword | Case-insensitive search |
| `consider` | Keyword | Case-insensitive search |
| `advise` | Keyword | Case-insensitive search |
| `ought` | Keyword | Case-insensitive search |
| `you might want to` | Phrase | Case-insensitive search |
| `it would be wise` | Phrase | Case-insensitive search |

**Exceptions:** Allowed in docstrings describing what the system does NOT do, test assertions, and documentation explicitly prohibiting these patterns.

### 2.2 Category B: Aggregation Patterns (Domain-Specific)

| Pattern | Type | Detection |
|---------|------|-----------|
| `weight` | Field/Column | Schema and model search |
| `score` | Field/Column | Schema and model search |
| `confidence` | Field/Column | Schema and model search |
| `rating` | Field/Column | Schema and model search |
| `ranking` | Field/Column | Schema and model search |
| `aggregate` | Method | Function name search |
| `combine` | Method | Function name search |
| `overall` | Variable | Variable name search |
| `consensus` | Variable | Variable name search |
| `summary_score` | Variable | Variable name search |

### 2.3 Category C: Decision Logic (Domain-Specific)

| Pattern | Type | Detection |
|---------|------|-----------|
| Recommendation engines | Code structure | AST analysis |
| Decision trees outputting actions | Code structure | AST analysis |
| Signal prioritisation logic | Code structure | If/else analysis |
| Contradiction resolution logic | Code structure | Logic flow analysis |

### 2.4 Categories D & E: Universal Security/Safety Patterns

Per Universal Framework Section 5.1 — applies to all projects.

---

## SECTION 3: AUDIT TIER ASSIGNMENTS

### 3.1 File Category → Tier Mapping

| Category | Path Pattern | Tier | Rationale |
|----------|--------------|------|-----------|
| **AI Layer** | `src/cia_sie/ai/*.py` | **Tier 4** | Constitutional Rule 3 enforcement |
| **API Routes** | `src/cia_sie/api/routes/*.py` | **Tier 4** | Output to users, constitutional exposure |
| **Core Models** | `src/cia_sie/core/models.py` | **Tier 4** | Schema defines prohibited fields |
| **DAL Models** | `src/cia_sie/dal/models.py` | **Tier 4** | Database schema, prohibited columns |
| **Response Validator** | `src/cia_sie/ai/response_validator.py` | **Tier 5** | Constitutional enforcement logic |
| **Exposure Layer** | `src/cia_sie/exposure/*.py` | **Tier 4** | Contradiction handling |
| **Ingestion Layer** | `src/cia_sie/ingestion/*.py` | **Tier 3** | Data normalisation |
| **Platforms Layer** | `src/cia_sie/platforms/*.py` | **Tier 3** | External integrations |
| **Core Config** | `src/cia_sie/core/config.py` | **Tier 3** | Configuration management |
| **Core Enums** | `src/cia_sie/core/enums.py` | **Tier 2** | Enumeration definitions |
| **Core Exceptions** | `src/cia_sie/core/exceptions.py` | **Tier 3** | Constitutional exception types |
| **Security** | `src/cia_sie/core/security.py` | **Tier 4** | Security-critical |
| **Database Migrations** | `alembic/versions/*.py` | **Tier 4** | Schema changes, prohibited columns |
| **Frontend Types** | `frontend/src/types/*.ts` | **Tier 3** | Type definitions |
| **Frontend Services** | `frontend/src/services/*.ts` | **Tier 3** | API interactions |
| **Frontend Components** | `frontend/src/components/*.tsx` | **Tier 3** | UI components |
| **Test Files** | `tests/**/*.py` | **Tier 3** | Verification of compliance |
| **Constitutional Tests** | `tests/unit/test_constitutional_compliance.py` | **Tier 4** | Constitutional verification |
| **CI/CD Pipelines** | `.github/workflows/*.yml` | **Tier 2** | Deployment configuration |
| **Documentation** | `*.md` | **Tier 1** | Accuracy verification |
| **Configuration Files** | `*.toml`, `*.json`, `*.yaml` | **Tier 1** | Structure verification |

### 3.2 Tier Escalation Triggers

| Trigger | Escalation |
|---------|------------|
| File contains AI output logic | → Tier 4 minimum |
| File contains user-facing output | → Tier 4 minimum |
| File contains database schema | → Tier 4 minimum |
| File contains constitutional enforcement | → Tier 5 |
| File contains security logic | → Tier 4 minimum |

---

## SECTION 4: SCOPE CLASSIFICATION

### 4.1 IN-SCOPE (Full Access)

| Path | Category | Access |
|------|----------|--------|
| `src/cia_sie/` | Backend Application | Audit + Remediation |
| `frontend/src/` | Frontend Application | Audit + Remediation |
| `tests/` | Test Suites | Audit + Remediation |
| `alembic/` | Database Migrations | Audit + Remediation |
| `.github/workflows/` | CI/CD Pipelines | Audit + Remediation |
| `AI_HANDOFF/` | Handoff Documentation | Audit + Remediation |
| `specifications/` | Design Specifications | Audit + Remediation |

### 4.2 REFERENCE-ONLY

| Path | Category | Access |
|------|----------|--------|
| `context/decisions/` | Architecture Decision Records | Cross-reference |
| `assets/` | Flowcharts and Diagrams | Cross-reference |

### 4.3 OUT-OF-SCOPE

| Path | Category | Reason |
|------|----------|--------|
| `.git/` | Version Control Internals | System-managed |
| `venv/` | Virtual Environment | Third-party packages |
| `frontend/node_modules/` | Node Modules | Third-party packages |
| `__pycache__/` | Python Cache | Build artefacts |
| `.pytest_cache/` | Pytest Cache | Build artefacts |

---

## SECTION 5: FILE MANIFEST

### 5.1 Summary

| Category | Files | Lines | Tier Range |
|----------|-------|-------|------------|
| Backend Source | 48 | 9,668 | Tier 2-5 |
| Frontend Source | 6 | 707 | Tier 3 |
| Test Files | 38 | 13,098 | Tier 3-4 |
| Database Migrations | 2 | ~200 | Tier 4 |
| Documentation | 32 | ~16,618 | Tier 1 |
| **TOTAL** | **126** | **~40,291** | — |

### 5.2 Backend Source (48 files)

#### API Layer (14 files) — Tier 4
```
src/cia_sie/api/app.py                       227 lines
src/cia_sie/api/__init__.py                   22 lines
src/cia_sie/api/routes/__init__.py            38 lines
src/cia_sie/api/routes/ai.py                 313 lines
src/cia_sie/api/routes/baskets.py            187 lines
src/cia_sie/api/routes/charts.py             146 lines
src/cia_sie/api/routes/chat.py               445 lines
src/cia_sie/api/routes/instruments.py        163 lines
src/cia_sie/api/routes/narratives.py         161 lines
src/cia_sie/api/routes/platforms.py          500 lines
src/cia_sie/api/routes/relationships.py      144 lines
src/cia_sie/api/routes/signals.py             98 lines
src/cia_sie/api/routes/silos.py              128 lines
src/cia_sie/api/routes/strategy.py           365 lines
src/cia_sie/api/routes/webhooks.py           275 lines
```

#### AI Layer (7 files) — Tier 4-5
```
src/cia_sie/ai/__init__.py                    50 lines   [Tier 4]
src/cia_sie/ai/claude_client.py              122 lines   [Tier 4]
src/cia_sie/ai/model_registry.py             143 lines   [Tier 4]
src/cia_sie/ai/narrative_generator.py        390 lines   [Tier 4]
src/cia_sie/ai/prompt_builder.py             274 lines   [Tier 4]
src/cia_sie/ai/response_validator.py         497 lines   [Tier 5]
src/cia_sie/ai/usage_tracker.py              261 lines   [Tier 4]
```

#### Core Layer (6 files) — Tier 2-4
```
src/cia_sie/core/__init__.py                  49 lines   [Tier 2]
src/cia_sie/core/config.py                   172 lines   [Tier 3]
src/cia_sie/core/enums.py                    156 lines   [Tier 2]
src/cia_sie/core/exceptions.py               156 lines   [Tier 3]
src/cia_sie/core/models.py                   367 lines   [Tier 4]
src/cia_sie/core/security.py                 446 lines   [Tier 4]
```

#### Data Access Layer (4 files) — Tier 3-4
```
src/cia_sie/dal/__init__.py                   33 lines   [Tier 3]
src/cia_sie/dal/database.py                  101 lines   [Tier 3]
src/cia_sie/dal/models.py                    335 lines   [Tier 4]
src/cia_sie/dal/repositories.py              471 lines   [Tier 3]
```

#### Exposure Layer (4 files) — Tier 4
```
src/cia_sie/exposure/__init__.py              27 lines
src/cia_sie/exposure/confirmation_detector.py 180 lines
src/cia_sie/exposure/contradiction_detector.py 195 lines
src/cia_sie/exposure/relationship_exposer.py  220 lines
```

#### Ingestion Layer (4 files) — Tier 3
```
src/cia_sie/ingestion/__init__.py             25 lines
src/cia_sie/ingestion/freshness.py           145 lines
src/cia_sie/ingestion/signal_normalizer.py   165 lines
src/cia_sie/ingestion/webhook_handler.py     190 lines
```

#### Platforms Layer (4 files) — Tier 3
```
src/cia_sie/platforms/__init__.py             30 lines
src/cia_sie/platforms/base.py                120 lines
src/cia_sie/platforms/tradingview.py         180 lines
src/cia_sie/platforms/metatrader.py          175 lines
```

### 5.3 Frontend Source (6 files) — Tier 3

```
frontend/src/types/index.ts                  287 lines
frontend/src/services/api.ts                 282 lines
frontend/src/hooks/useInstruments.ts          44 lines
frontend/src/hooks/useRelationships.ts        41 lines
frontend/src/App.tsx                          28 lines
frontend/src/main.tsx                         25 lines
```

### 5.4 Test Files (38 files) — Tier 3-4

```
tests/unit/test_constitutional_compliance.py  450 lines  [Tier 4]
tests/unit/test_response_validator.py         380 lines  [Tier 4]
tests/unit/test_models.py                     320 lines  [Tier 3]
tests/integration/test_api_*.py              ~2000 lines [Tier 3]
[... additional test files ...]
```

---

## SECTION 6: AUDIT OUTPUT CONFIGURATION

### 6.1 Output Location

```
/Users/nevillemehta/Downloads/CIA-SIE/audit/
```

### 6.2 Deliverables Naming Convention

| Phase | Filename |
|-------|----------|
| 1 | `PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md` |
| 2 | `PHASE_2_BACKEND_CODE_AUDIT.md` |
| 3 | `PHASE_3_FRONTEND_CODE_AUDIT.md` |
| 4 | `PHASE_4_DATABASE_MIGRATIONS_AUDIT.md` |
| 5 | `PHASE_5_API_SPECIFICATION_AUDIT.md` |
| 6 | `PHASE_6_TEST_COVERAGE_AUDIT.md` |
| 7 | `PHASE_7_DOCUMENTATION_SYNC_AUDIT.md` |
| 8 | `PHASE_8_CONSTITUTIONAL_COMPLIANCE_AUDIT.md` |
| 9A | `REPORT_01_TRACEABILITY_MATRIX.md` |
| 9B | `REPORT_02_COMPLIANCE_SCORECARD.md` |
| 9C | `REPORT_03_GAP_ANALYSIS.md` |
| 9D | `REPORT_04_REMEDIATION_ROADMAP.md` |
| 9E | `REPORT_05_AUDIT_CERTIFICATION.md` |

---

## SECTION 7: CURSOR INITIATION PROMPT

When initiating a new audit cycle, use this prompt:

```
You are operating under the UNIVERSAL CODE AUDIT FRAMEWORK v2.0 with
CIA-SIE PROJECT CONFIGURATION v1.0.

FRAMEWORK: /Users/nevillemehta/Downloads/Gold Audit Standards/
           UNIVERSAL_CODE_AUDIT_AND_APPLICATION_DEVELOPMENT_FRAMEWORK_v2.0_GENERIC.md

PROJECT CONFIG: /Users/nevillemehta/Downloads/CIA-SIE/PROJECT_CONFIGURATION.md

TARGET: /Users/nevillemehta/Downloads/CIA-SIE/

OUTPUT: /Users/nevillemehta/Downloads/CIA-SIE/audit/

CONSTITUTIONAL RULES: 3 (defined in PROJECT_CONFIGURATION.md Section 1)

EXECUTE: 9-Phase Gold Standard Audit with 100% coverage.
Proceed autonomously through all phases.
Commit after each phase.
Report "AUDIT CYCLE COMPLETE" when finished.

BEGIN.
```

---

## SECTION 8: REFERENCE DOCUMENTS

| Document | Location | Purpose |
|----------|----------|---------|
| Universal Framework v2.0 | `/Gold Audit Standards/UNIVERSAL_CODE_AUDIT_AND_APPLICATION_DEVELOPMENT_FRAMEWORK_v2.0_GENERIC.md` | Methodology, templates, standards |
| Gold Standard Specification | `/CIA-SIE/specifications/architecture/00_GOLD_STANDARD_SPECIFICATION.md` | System architecture |
| Constitutional Rules | `/CIA-SIE/AI_HANDOFF/HANDOFF_03_CONSTITUTIONAL_RULES.md` | Detailed rule documentation |
| API Specification | `/CIA-SIE/AI_HANDOFF/HANDOFF_02_API_ENDPOINTS.md` | API contract |
| Component Requirements | `/CIA-SIE/AI_HANDOFF/HANDOFF_05_COMPONENT_REQUIREMENTS.md` | Frontend specification |

---

## DOCUMENT CERTIFICATION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  CIA-SIE PROJECT CONFIGURATION                                              │
│  Version 1.0                                                                │
│                                                                             │
│  This document provides the project-specific configuration that             │
│  complements the Universal Code Audit Framework v2.0.                       │
│                                                                             │
│  Contents:                                                                  │
│  - 3 Constitutional Rules (inviolable)                                      │
│  - Prohibited Patterns Registry (domain-specific)                           │
│  - Audit Tier Assignments (48 backend, 6 frontend, 38 test files)           │
│  - Scope Classifications (IN-SCOPE, REFERENCE, OUT-OF-SCOPE)                │
│  - File Manifest (126 files, ~40,291 lines)                                 │
│  - Output Configuration                                                     │
│  - Cursor Initiation Prompt                                                 │
│                                                                             │
│  Usage:                                                                     │
│  This document + Universal Framework v2.0 = Complete CIA-SIE Audit Spec     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*CIA-SIE Project Configuration v1.0*
*Companion to Universal Code Audit Framework v2.0*
*Date: 03 January 2026*
