# CIA-SIE AUDIT CONFIGURATION
## Project-Specific Implementation of Gold Standard Framework

---

**Document ID:** GSUF-TIER3-CIASIE-001
**Version:** 1.0.0
**Classification:** Project Configuration
**Project:** CIA-SIE (Confirmation, Invalidation, and Actionable Signal Intelligence Engine)
**Repository:** CIA-SIE-PURE (Backend Only)

---

## FRAMEWORK REFERENCES

| Tier | Document | Purpose |
|------|----------|---------|
| **TIER 1** | [GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0.md](./GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0.md) | Universal audit methodology |
| **TIER 2** | [ADAPTER_FINANCIAL_SERVICES.md](./ADAPTER_FINANCIAL_SERVICES.md) | Domain-specific constitutional rules |
| **TIER 3** | This document | CIA-SIE project configuration |

---

# 1. PROJECT METADATA

## 1.1 Repository Information

| Attribute | Value |
|-----------|-------|
| **Project Name** | CIA-SIE (Confirmation, Invalidation, and Actionable Signal Intelligence Engine) |
| **Repository** | CIA-SIE-PURE |
| **Repository Type** | Backend Only (clean room for audit) |
| **GitHub URL** | https://github.com/Nevillemehta-Claude/CIA-SIE-PURE |
| **Primary Branch** | main |
| **Domain Adapter** | ADAPTER_FINANCIAL_SERVICES.md |

## 1.2 Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Runtime** | Python | 3.11 |
| **Web Framework** | FastAPI | Latest |
| **ORM** | SQLAlchemy | 2.x |
| **Database** | SQLite | (Development) |
| **Validation** | Pydantic | 2.x |
| **Testing** | pytest | Latest |
| **AI Integration** | Anthropic Claude API | Latest |
| **Package Management** | pip / pyproject.toml | — |

## 1.3 Application Purpose

CIA-SIE is a **trading signal aggregation and analysis platform** that:

1. Ingests signals from multiple trading platforms (Kite, TradingView)
2. Normalises signals into a common format
3. Detects confirmations (multiple signals agreeing)
4. Detects contradictions (signals disagreeing)
5. Generates AI-powered narratives describing market conditions
6. Presents all information WITHOUT recommendations

**Critical Constraint:** CIA-SIE is a **decision-support tool**, NOT an advisory service. See TIER 2 Constitutional Rules.

---

# 2. DIRECTORY STRUCTURE

```
CIA-SIE-PURE/
├── .github/workflows/       # CI/CD pipelines
│   ├── ci.yml              # Main CI pipeline
│   └── codeql.yml          # Security scanning
├── AI_HANDOFF/             # AI handoff documentation
├── alembic/                # Database migrations
│   └── versions/           # Migration files
├── context/decisions/      # Architecture Decision Records
├── docs/                   # Documentation
│   └── diagrams/           # PlantUML diagrams
├── governance/             # Audit framework documents
├── handoff/                # Audit deliverables output
├── src/cia_sie/            # Main source code
│   ├── ai/                 # Claude AI integration
│   ├── api/                # FastAPI application
│   │   └── routes/         # API endpoints
│   ├── bridge/             # Platform bridges
│   ├── core/               # Core models, config, enums
│   ├── dal/                # Data Access Layer
│   ├── exposure/           # Confirmation/contradiction detection
│   ├── ingestion/          # Signal ingestion pipeline
│   └── platforms/          # Trading platform adapters
├── tests/                  # Test suite
│   ├── integration/        # Integration tests
│   └── unit/               # Unit tests
├── pyproject.toml          # Package configuration
└── README.md               # Project README
```

---

# 3. COMPONENT TIER ASSIGNMENTS

Per TIER 1 Section 4 (5-Tier Audit Depth Model), each component is assigned an audit tier based on criticality.

## 3.1 Tier 4: Forensic Audit (Security/API Critical)

These components handle external integrations, authentication, and API boundaries. Require character-level analysis.

| Component | Path | Rationale |
|-----------|------|-----------|
| **Kite Platform Adapter** | `src/cia_sie/platforms/kite.py` | External API, OAuth, financial data |
| **TradingView Adapter** | `src/cia_sie/platforms/tradingview.py` | External webhooks, signal ingestion |
| **Webhook Handler** | `src/cia_sie/ingestion/webhook_handler.py` | External input validation |
| **Security Module** | `src/cia_sie/core/security.py` | Authentication, authorization |
| **Claude Client** | `src/cia_sie/ai/claude_client.py` | External API, API key handling |
| **Database Models** | `src/cia_sie/dal/models.py` | Data integrity, prohibited columns check |

## 3.2 Tier 3: Deep Audit (Business Logic)

Core business logic requiring line-by-line verification.

| Component | Path | Rationale |
|-----------|------|-----------|
| **Confirmation Detector** | `src/cia_sie/exposure/confirmation_detector.py` | Core business logic |
| **Contradiction Detector** | `src/cia_sie/exposure/contradiction_detector.py` | Core business logic, CR-002 critical |
| **Relationship Exposer** | `src/cia_sie/exposure/relationship_exposer.py` | Signal relationship analysis |
| **Signal Normalizer** | `src/cia_sie/ingestion/signal_normalizer.py` | Data transformation |
| **Narrative Generator** | `src/cia_sie/ai/narrative_generator.py` | AI output, CR-003 critical |
| **Response Validator** | `src/cia_sie/ai/response_validator.py` | Output validation |
| **Prompt Builder** | `src/cia_sie/ai/prompt_builder.py` | AI prompts, constitutional compliance |
| **Repositories** | `src/cia_sie/dal/repositories.py` | Data access patterns |
| **All API Routes** | `src/cia_sie/api/routes/*.py` | API contracts |
| **App Configuration** | `src/cia_sie/api/app.py` | Application setup |
| **Core Models** | `src/cia_sie/core/models.py` | Domain models |

## 3.3 Tier 2: Standard Audit (Utilities)

Supporting modules requiring function-level review.

| Component | Path | Rationale |
|-----------|------|-----------|
| **Configuration** | `src/cia_sie/core/config.py` | Settings management |
| **Enums** | `src/cia_sie/core/enums.py` | Type definitions |
| **Exceptions** | `src/cia_sie/core/exceptions.py` | Error handling |
| **Freshness Tracker** | `src/cia_sie/ingestion/freshness.py` | Signal age tracking |
| **Usage Tracker** | `src/cia_sie/ai/usage_tracker.py` | API usage monitoring |
| **Model Registry** | `src/cia_sie/ai/model_registry.py` | AI model configuration |
| **Platform Registry** | `src/cia_sie/platforms/registry.py` | Platform management |
| **Platform Base** | `src/cia_sie/platforms/base.py` | Abstract base class |
| **Database Setup** | `src/cia_sie/dal/database.py` | Connection management |
| **Main Entry** | `src/cia_sie/main.py` | Application entry point |

## 3.4 Tier 1: Cursory Review (Configuration/Init)

Structure verification only.

| Component | Path | Rationale |
|-----------|------|-----------|
| **Package Init Files** | `src/cia_sie/*/__init__.py` | Package structure |
| **Alembic Config** | `alembic.ini` | Migration configuration |
| **Alembic Env** | `alembic/env.py` | Migration environment |
| **pyproject.toml** | `pyproject.toml` | Package metadata |
| **CI Workflows** | `.github/workflows/*.yml` | CI/CD configuration |

## 3.5 Tier Assignment Summary

| Tier | Files | Coverage Focus |
|------|-------|----------------|
| **Tier 4** | 6 | Character-level, security focus |
| **Tier 3** | 15+ | Line-by-line, business logic |
| **Tier 2** | 10 | Function-level, utilities |
| **Tier 1** | 10+ | Structure verification |

---

# 4. CONSTITUTIONAL RULES INSTANTIATION

CIA-SIE inherits all constitutional rules from **TIER 2: ADAPTER_FINANCIAL_SERVICES.md**.

## 4.1 Rule Application

| Rule | TIER 2 Reference | CIA-SIE Application |
|------|------------------|---------------------|
| **CR-001** | Decision-Support Only | CIA-SIE displays signals; user executes trades via Kite |
| **CR-002** | Never Resolve Contradictions | Contradiction detector EXPOSES conflicts, never resolves |
| **CR-003** | Descriptive Not Prescriptive | Narrative generator uses descriptive language only |

## 4.2 CIA-SIE Specific Verification Points

### CR-001 Verification

```bash
# Verify no trade execution code exists
grep -rn "execute.*trade\|place.*order\|submit.*order" src/cia_sie/
# Expected: 0 results

# Verify Kite adapter is read-only (no order methods)
grep -rn "def.*order\|def.*trade\|def.*buy\|def.*sell" src/cia_sie/platforms/kite.py
# Expected: 0 results
```

### CR-002 Verification

```bash
# Verify contradiction detector does not resolve
grep -rn "resolve\|reconcile\|average\|aggregate" src/cia_sie/exposure/contradiction_detector.py
# Expected: 0 results (or only in comments)

# Verify no weighting in signal handling
grep -rn "weight\s*=\|score\s*=\|confidence\s*=" src/cia_sie/
# Expected: 0 results in models
```

### CR-003 Verification

```bash
# Verify narrative generator uses descriptive language
grep -rn "should\|recommend\|suggest\|advise" src/cia_sie/ai/narrative_generator.py
# Expected: 0 results

# Verify prompt builder enforces descriptive output
grep -rn "descriptive\|do not recommend\|no advice" src/cia_sie/ai/prompt_builder.py
# Expected: Presence of enforcement language
```

## 4.3 Prohibited Columns Check

Per TIER 2 Section 4, verify `src/cia_sie/dal/models.py` contains NONE of:

| Column | Status Required |
|--------|-----------------|
| `weight` | **ABSENT** |
| `score` | **ABSENT** |
| `confidence` | **ABSENT** |
| `priority` | **ABSENT** |
| `rank` | **ABSENT** |
| `recommendation` | **ABSENT** |

---

# 5. AUDIT EXECUTION PARAMETERS

## 5.1 Cursor AI Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Model** | Claude Opus 4.5 | Complex analysis capability |
| **Model Multiplier** | 2× | Enhanced reasoning |
| **Cycle Count** | 50 | Sufficient for comprehensive audit |
| **Agent Mode** | Enabled | Autonomous execution |

## 5.2 Audit Invocation Prompt

```
Read governance/GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0.md
Read governance/ADAPTER_FINANCIAL_SERVICES.md
Read governance/CIA-SIE_AUDIT_CONFIGURATION.md

Execute the 9-Phase Audit Protocol per TIER 1 Section 6.
Apply constitutional rules per TIER 2.
Use tier assignments per this document (TIER 3) Section 3.

This is a backend-only repository. Skip Phase 3 (Frontend Code Audit).
Create all deliverables in the handoff/ directory.

Begin with Phase 1: Repository Structure Audit.
```

## 5.3 Expected Deliverables

All deliverables created in `handoff/` directory:

| # | Deliverable | Phase |
|---|-------------|-------|
| 1 | `PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md` | 1 |
| 2 | `PHASE_2_BACKEND_CODE_AUDIT.md` | 2 |
| 3 | `PHASE_3_FRONTEND_CODE_AUDIT.md` | 3 (N/A - backend only) |
| 4 | `PHASE_4_DATA_LAYER_AUDIT.md` | 4 |
| 5 | `PHASE_5_API_SPECIFICATION_AUDIT.md` | 5 |
| 6 | `PHASE_6_TEST_COVERAGE_AUDIT.md` | 6 |
| 7 | `PHASE_7_DOCUMENTATION_SYNC_AUDIT.md` | 7 |
| 8 | `PHASE_8_SECURITY_CONSTITUTIONAL_AUDIT.md` | 8 |
| 9 | `PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md` | 9A |
| 10 | `PHASE_9B_COMPLIANCE_SCORECARD.md` | 9B |
| 11 | `PHASE_9C_GAP_ANALYSIS.md` | 9C |
| 12 | `PHASE_9D_REMEDIATION_ROADMAP.md` | 9D |
| 13 | `PHASE_9E_AUDIT_CERTIFICATION.md` | 9E |

---

# 6. CI/CD INTEGRATION

## 6.1 Existing Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| **CI** | `.github/workflows/ci.yml` | Tests, security, quality |
| **CodeQL** | `.github/workflows/codeql.yml` | Security analysis |

## 6.2 Constitutional Compliance Job

The CI pipeline includes a `constitutional-tests` job that:

1. Runs constitutional compliance tests
2. Greps for prohibited columns in models
3. Fails build if violations found

**Location:** `.github/workflows/ci.yml` lines 163-205

## 6.3 Coverage Thresholds

| Metric | Current Threshold | Target |
|--------|-------------------|--------|
| Overall Coverage | 30% | 80% |
| Constitutional Tests | 100% | 100% |

---

# 7. TEST REQUIREMENTS

## 7.1 Required Test Files

| Test Category | File | Coverage Target |
|---------------|------|-----------------|
| Constitutional Compliance | `tests/unit/test_constitutional_compliance.py` | 100% |
| Models | `tests/unit/test_models.py` | 100% |
| Confirmation Detector | `tests/unit/test_confirmation_detector.py` | 95% |
| Contradiction Detector | `tests/unit/test_contradiction_detector.py` | 95% |
| Claude Client | `tests/unit/test_claude_client.py` | 90% |
| Narrative Generator | `tests/unit/test_narrative_generator.py` | 90% |
| API Routes | `tests/unit/test_api_routes*.py` | 80% |
| Integration | `tests/integration/test_*.py` | 80% |

## 7.2 Constitutional Test Cases

Per TIER 2 Section 7, the following tests MUST exist:

```python
# tests/unit/test_constitutional_compliance.py

def test_no_recommendation_language_in_responses():
    """CR-001/CR-003: No advisory language in API responses."""
    pass

def test_signals_have_no_weight_or_score():
    """CR-002: No weighting fields in signal objects."""
    pass

def test_contradictions_displayed_equally():
    """CR-002: Contradictory signals shown with equal prominence."""
    pass

def test_narrative_uses_descriptive_language():
    """CR-003: AI narratives are descriptive, not prescriptive."""
    pass

def test_no_prohibited_columns_in_models():
    """CR-002: Database models have no prohibited columns."""
    pass
```

---

# 8. SPECIFICATION DOCUMENTS

## 8.1 Primary Specifications

| Document | Location | Purpose |
|----------|----------|---------|
| Design Specification | `AI_HANDOFF/HANDOFF_01_DESIGN_SPECIFICATION.md` | System design |
| API Endpoints | `AI_HANDOFF/HANDOFF_02_API_ENDPOINTS.md` | API contract |
| Constitutional Rules | `AI_HANDOFF/HANDOFF_03_CONSTITUTIONAL_RULES.md` | Business rules |
| Technical Standards | `AI_HANDOFF/HANDOFF_04_TECHNICAL_STANDARDS.md` | Tech requirements |
| Component Requirements | `AI_HANDOFF/HANDOFF_05_COMPONENT_REQUIREMENTS.md` | Component specs |
| Business Logic | `AI_HANDOFF/HANDOFF_07_BUSINESS_LOGIC.md` | Logic specification |

## 8.2 Architecture Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Architecture Flowcharts | `docs/CIA-SIE_ARCHITECTURE_FLOWCHARTS.md` | System architecture |
| PlantUML Diagrams | `docs/diagrams/*.puml` | Visual diagrams |
| ADRs | `context/decisions/ADR-*.md` | Architecture decisions |

---

# 9. KNOWN CONSTRAINTS

## 9.1 Backend-Only Repository

This repository contains **backend code only**. Frontend code is in the separate `CIA-SIE` repository.

**Implications:**
- Phase 3 (Frontend Code Audit) = N/A
- Layer L11 (Frontend-Backend Type Sync) = N/A
- No React/TypeScript code to audit

## 9.2 Development Database

SQLite is used for development. Production deployment may use PostgreSQL.

**Implications:**
- Migration compatibility should be verified for production database
- Performance testing should use production-equivalent database

## 9.3 External Dependencies

| Dependency | Type | Audit Consideration |
|------------|------|---------------------|
| Kite Connect API | External | API key security, rate limiting |
| TradingView Webhooks | External | Input validation, webhook security |
| Anthropic Claude API | External | API key security, response validation |

---

# 10. AUDIT HISTORY

| Date | Auditor | Result | Certification |
|------|---------|--------|---------------|
| 2026-01-03 | Cursor (Claude) | 100% Compliance | CERTIFIED |

**Latest Audit Deliverables:** `handoff/PHASE_*.md`

---

# DOCUMENT METADATA

```yaml
document_id: GSUF-TIER3-CIASIE-001
version: 1.0.0
type: Project Configuration
project: CIA-SIE
repository: CIA-SIE-PURE

framework_references:
  tier_1: GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0.md
  tier_2: ADAPTER_FINANCIAL_SERVICES.md

technology_stack:
  runtime: Python 3.11
  framework: FastAPI
  orm: SQLAlchemy
  database: SQLite (dev) / PostgreSQL (prod)
  ai: Anthropic Claude API

component_tiers:
  tier_4: 6 components (security/API critical)
  tier_3: 15+ components (business logic)
  tier_2: 10 components (utilities)
  tier_1: 10+ components (configuration)

constitutional_rules:
  source: ADAPTER_FINANCIAL_SERVICES.md
  rules:
    - CR-001: Decision-Support Only
    - CR-002: Never Resolve Contradictions
    - CR-003: Descriptive Not Prescriptive

audit_parameters:
  model: Claude Opus 4.5
  multiplier: 2x
  cycles: 50
  mode: Agent
```

---

**END OF DOCUMENT**

*CIA-SIE Audit Configuration v1.0*
*Project-Specific Implementation of Gold Standard Framework*
*TIER 3: Project Configuration*
