# CIA-SIE-PURE BACKEND RECONSTRUCTION BRIEF

**Classification:** MISSION CRITICAL
**Authority:** Principal Neville Mehta
**Orchestration:** Central Command (COWORK Moderator Session)
**Date:** January 15, 2026

---

## MISSION STATEMENT

Execute a complete forensic audit and architectural reconstruction of the CIA-SIE-PURE backend system. The objective is to study the present state comprehensively, synthesize a master flowchart representing how the backend SHOULD be, and prepare actionable directives for Cursor to rebuild/audit the backend to Gold Standard compliance.

---

## GOLD STANDARD FRAMEWORK CONTEXT

### The 8 Immutable Principles
1. **NASA-Style Rigour** - Exhaustive, evidence-based validation
2. **Audit Before Build** - Validation precedes construction
3. **Zero Drift Policy** - Specs and implementation synchronized
4. **Living Documentation** - Documentation maintained contemporaneously
5. **Full Bidirectional Traceability** - Requirement ↔ Implementation ↔ Verification
6. **Evidence-Based Validation** - No assertions without proof
7. **Single Source of Truth** - One authoritative source per information category
8. **Defensive Documentation** - Anticipate failure modes

### The 5 Immutable Laws
1. **Meaning Precedes Implementation** - WHAT before HOW
2. **Structure Precedes Intelligence** - Data before algorithms
3. **Validation Precedes Optimization** - Correct before fast
4. **Explicit Precedes Implicit** - No magic, no hidden behavior
5. **Reversibility Precedes Commitment** - Design for rollback

### The 3 Absolutes (CIA-SIE Constitutional)
1. **Decision-Support ONLY** - Never prescribe, only describe
2. **Never Resolve Contradictions** - Expose, don't determine
3. **Descriptive, Not Prescriptive** - No recommendations

### The 10 Verification Layers
1. Syntax
2. Static Analysis
3. Unit Testing
4. Contract Testing
5. Integration Testing
6. Functional Testing
7. Regression Testing
8. Performance Testing
9. Security Testing
10. Acceptance Testing

---

## PHASE 1 OBJECTIVES: FORENSIC AUDIT

### 1.1 What Must Be Discovered
- Complete inventory of all backend source files
- All API endpoints and their implementations
- All database models and relationships
- All external integrations (Kite, Claude AI, TradingView)
- All flowcharts and architecture diagrams
- All test files and their coverage
- Constitutional compliance status (Section 0B)

### 1.2 What Must Be Assessed
- Gap between documentation and implementation
- Orphaned code (implementation without requirement)
- Phantom features (documented but not implemented)
- Schema drift (database vs. models discrepancy)
- API contract violations
- Constitutional violations in AI layer

### 1.3 Deliverables
- **FORENSIC_AUDIT_INVENTORY.md** - Complete file inventory
- **GAP_ANALYSIS_REPORT.md** - Documented vs. implemented
- **CONSTITUTIONAL_COMPLIANCE_MATRIX.md** - Section 0B verification
- **INTEGRATION_STATUS_REPORT.md** - External system connections

---

## PHASE 2 OBJECTIVES: FLOWCHART SYNTHESIS

### 2.1 Input Flowcharts to Analyze
Located in: `/documentation/02_ARCHITECTURE/BACKEND_FLOWCHARTS.md`

Key flowcharts present:
- Section 1: Kite API Integration (OAuth, Sessions, REST)
- Section 2: Data Ingestion Pipeline (Webhooks, Normalization, Storage)
- Section 3: Claude API Two-Stage Orchestration
- Section 4: State Management & Persistence
- Section 5: Error Propagation & Recovery
- Section 6: Constitutional Compliance Enforcement

### 2.2 Additional Architecture Documents
- `/documentation/02_ARCHITECTURE/FRONTEND_DATA_FLOW.md`
- `/documentation/AEROSPACE_SYSTEMS_MANUAL/02_SIGNAL_FLOW_MATRIX.md`
- `/documentation/prototypes/OPERATIONAL_GUIDE_SIGNAL_FLOW.html`
- All `/documentation/06_AUDITS/` reports

### 2.3 Synthesis Objective
Create a **MASTER_BACKEND_FLOWCHART** that:
- Consolidates all existing flowcharts
- Fills gaps discovered in forensic audit
- Represents the IDEAL state (not current state)
- Is mermaid.js compatible for rendering
- Covers ALL backend operations end-to-end

---

## PHASE 3 OBJECTIVES: RETROFIT PLAN

### 3.1 Gap Remediation
For each gap identified:
- Document the discrepancy
- Determine remediation path (fix code OR update spec)
- Estimate effort
- Prioritize by criticality

### 3.2 Retrofit Sequence
1. Constitutional violations (HIGHEST PRIORITY)
2. Data integrity issues
3. API contract alignment
4. Missing verification layers
5. Documentation synchronization

### 3.3 Deliverable
- **RETROFIT_REMEDIATION_ROADMAP.md** - Ordered list of fixes

---

## PHASE 4 OBJECTIVES: CURSOR DIRECTIVE

### 4.1 Cursor Handoff Requirements
- Clear, actionable instructions
- File paths and line references
- Expected outcomes per task
- Verification steps per task
- Gold Standard compliance checklist

### 4.2 Directive Structure
```
CURSOR_BACKEND_RECONSTRUCTION_DIRECTIVE.md
├── SECTION 0: Context & Authority
├── SECTION 1: Pre-Flight Checklist
├── SECTION 2: Task Registry (ordered)
├── SECTION 3: Verification Protocol per Task
├── SECTION 4: Constitutional Compliance Checks
├── SECTION 5: Post-Reconstruction Certification
```

---

## BACKEND SOURCE STRUCTURE

### Core Module: `/src/cia_sie/`
```
cia_sie/
├── __init__.py
├── main.py                    # Application entry
├── api/
│   ├── app.py                 # FastAPI application
│   └── routes/                # API endpoints
│       ├── signals.py
│       ├── narratives.py
│       ├── charts.py
│       ├── platforms.py
│       ├── silos.py
│       ├── ai.py
│       ├── strategy.py
│       ├── instruments.py
│       ├── chat.py
│       ├── webhooks.py
│       ├── baskets.py
│       └── relationships.py
├── core/
│   ├── enums.py               # Enumerations
│   ├── config.py              # Configuration
│   ├── models.py              # Pydantic models
│   ├── security.py            # Security utilities
│   └── exceptions.py          # Custom exceptions
├── dal/
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # DB connection
│   └── repositories.py        # Data access layer
├── ai/
│   ├── claude_client.py       # Anthropic API
│   ├── prompt_builder.py      # Prompt construction
│   ├── narrative_generator.py # Story generation
│   ├── response_validator.py  # Constitutional checks
│   ├── usage_tracker.py       # Token tracking
│   └── model_registry.py      # Model config
├── exposure/
│   ├── contradiction_detector.py
│   ├── confirmation_detector.py
│   └── relationship_exposer.py
├── ingestion/
│   ├── webhook_handler.py
│   ├── signal_normalizer.py
│   └── freshness.py
├── platforms/
│   ├── base.py
│   ├── kite.py
│   ├── tradingview.py
│   └── registry.py
├── webhooks/
│   └── tradingview_receiver.py
└── bridge/
    └── __init__.py
```

---

## CRITICAL CONSTITUTIONAL REQUIREMENTS

### Section 0B: What Backend MUST NOT Do
1. **No weight columns** in database
2. **No score calculations** anywhere
3. **No confidence metrics** computed
4. **No aggregation functions** that combine signals
5. **No recommendation language** in AI responses
6. **No contradiction resolution** - only exposure

### Constitutional Enforcement Points
| Location | Enforcement |
|----------|-------------|
| `dal/models.py` | No weight/score columns |
| `core/models.py` | No confidence fields |
| `ai/response_validator.py` | Prohibited pattern check |
| `ai/prompt_builder.py` | Constraint injection |
| `exposure/*.py` | Expose, never resolve |

---

## SUCCESS CRITERIA

This COWORK session succeeds when:

1. **Complete Inventory** - Every backend file catalogued
2. **Gap Analysis Complete** - All discrepancies documented
3. **Constitutional Audit Complete** - Section 0B verified
4. **Master Flowchart Created** - IDEAL state documented
5. **Retrofit Plan Ready** - Prioritized remediation list
6. **Cursor Directive Ready** - Actionable reconstruction guide

---

## HANDOFF PROTOCOL

Upon completion of this COWORK session:

1. Return to **Central Command** (moderator conversation)
2. Present all deliverables for review
3. Receive improvised enhancements if needed
4. Obtain **CURSOR Handoff Directive** for Phase 2
5. Execute in Cursor with verification checkpoints

---

**END OF BRIEF**

*Authority: Principal Neville Mehta*
*Framework: Gold Standard Development System v1.0*
