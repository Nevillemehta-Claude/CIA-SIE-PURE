# CIA-SIE-PURE GOLD STANDARD AUDIT INSTRUCTIONS
# ══════════════════════════════════════════════════════════════════════════════
#                    Zero-Tolerance Software Engineering Audit
#                              Based on Universal Code Audit Framework v2.0
#                              COMPLETE & UNDILUTED
# ══════════════════════════════════════════════════════════════════════════════

---

## DOCUMENT CONTROL

| Attribute | Value |
|-----------|-------|
| Document ID | CIA-SIE-PURE-AUDIT-001 |
| Version | 1.0 |
| Based On | Universal Code Audit & Application Development Framework v2.0 |
| Classification | Zero-Tolerance Audit Protocol |
| Target Repository | CIA-SIE-PURE |
| Date | 2026-01-03 |
| Status | AUTHORITATIVE |

---

## PROJECT CONTEXT

| Attribute | Value |
|-----------|-------|
| **Repository** | CIA-SIE-PURE |
| **Type** | Backend-Only (No Frontend) |
| **Language** | Python 3.11 |
| **Framework** | FastAPI + SQLAlchemy + Pydantic |
| **Purpose** | Financial Decision-Support System for Traders |
| **Database** | SQLite |
| **Test Framework** | pytest + pytest-asyncio |

---

# PART I: GOVERNING PRINCIPLES
# ══════════════════════════════════════════════════════════════════════════════

## 1. EIGHT GOLD STANDARD PRINCIPLES

### 1.1 Principle 1: NASA-Style Rigour

**Definition:** Exhaustive, systematic, evidence-based validation where every claim is verifiable and reproducible.

| Attribute | Requirement |
|-----------|-------------|
| No Assumptions | Every finding cites exact `file:line` reference |
| No Shortcuts | 100% coverage verification, never statistical sampling |
| No Ambiguity | Binary pass/fail determination only |
| Reproducibility | Any qualified auditor following protocol reaches identical conclusions |

---

### 1.2 Principle 2: Audit Before Build

**Axiom:** Validation must precede construction. Building upon unvalidated foundations propagates defects exponentially.

```
MANDATED SEQUENCE:
┌───────────────────────────────────────────────────────────────────────────┐
│  Phase 1: Audit existing codebase against specifications                   │
│  Phase 2: Document all discrepancies with evidence                         │
│  Phase 3: Remediate (correct code OR update specifications)                │
│  Phase 4: Construct new features upon validated baseline                   │
└───────────────────────────────────────────────────────────────────────────┘

PROHIBITED SEQUENCE:
┌───────────────────────────────────────────────────────────────────────────┐
│  ✗ Build new features on unvalidated code                                  │
│  ✗ Defer audit activities                                                  │
│  ✗ Discover foundational defects post-construction                         │
└───────────────────────────────────────────────────────────────────────────┘
```

---

### 1.3 Principle 3: Zero Drift Policy

**Axiom:** Specifications and implementation shall remain synchronised at all times. No divergence without documented justification.

| Scenario | Mandated Action |
|----------|-----------------|
| Implementation differs from specification; specification is correct | Correct the implementation |
| Implementation differs from specification; implementation is correct | Update the specification |
| Both require improvement | Correct both; document the change |
| Divergence without justification | **NON-COMPLIANT — Audit failure** |

---

### 1.4 Principle 4: Living Documentation

**Axiom:** Documentation is maintained contemporaneously, not retrospectively. Stale documentation is a compliance violation.

| Anti-Pattern | Gold Standard |
|--------------|---------------|
| "Documentation will be completed later" | Document as construction proceeds |
| Stale README files | README reflects current operational state |
| Orphaned specifications | Specifications updated synchronously with code changes |

**Validation Test:** Can a qualified engineer understand the complete system from documentation alone? If documentation is insufficient, drift has occurred.

---

### 1.5 Principle 5: Full Bidirectional Traceability

**Axiom:** Every line of code traces to a requirement; every requirement traces to implementation and verification.

```
┌──────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  REQUIREMENT │ ────►│  IMPLEMENTATION  │ ────►│  VERIFICATION   │
│              │      │                  │      │  (Test/Review)  │
└──────────────┘      └──────────────────┘      └─────────────────┘
       │                      │                         │
       └──────────────────────┴─────────────────────────┘
                    BIDIRECTIONAL TRACEABILITY
```

| Question | Must Be Answerable |
|----------|-------------------|
| Which requirement does this code implement? | Yes — with evidence |
| Where is this requirement implemented? | Yes — with file:line |
| What tests verify this implementation? | Yes — with test reference |
| Is there orphan code (no requirement)? | Must be zero |
| Is there unimplemented requirements? | Must be documented |

**Orphan Code Definition:** Any code that cannot be traced to a documented requirement. Orphan code is prohibited in zero-tolerance environments.

---

### 1.6 Principle 6: Evidence-Based Validation

**Axiom:** Assertions without evidence are invalid. Every compliance claim requires verifiable proof.

| Evidence Quality | Example | Acceptability |
|------------------|---------|---------------|
| **Weak (Unacceptable)** | "The module handles errors appropriately" | ✗ REJECTED |
| **Strong (Required)** | "Error handling verified at `src/cia_sie/core/exceptions.py:45-67`; implements custom exception classes per HANDOFF_04_TECHNICAL_STANDARDS.md#error-handling" | ✓ ACCEPTED |

---

### 1.7 Principle 7: Single Source of Truth

**Axiom:** For any category of information, exactly one authoritative source exists. All other references derive from it.

| Information Category | Single Source Location (CIA-SIE-PURE) |
|---------------------|--------------------------------------|
| Requirements | `AI_HANDOFF/HANDOFF_01_DESIGN_SPECIFICATION.md` |
| API Contracts | `AI_HANDOFF/HANDOFF_02_API_ENDPOINTS.md` |
| Data Models | `src/cia_sie/dal/models.py` |
| Business Logic | `AI_HANDOFF/HANDOFF_07_BUSINESS_LOGIC.md` |
| Configuration | `src/cia_sie/core/config.py` |
| Constitutional Rules | `AI_HANDOFF/HANDOFF_03_CONSTITUTIONAL_RULES.md` |
| Technical Standards | `AI_HANDOFF/HANDOFF_04_TECHNICAL_STANDARDS.md` |

---

### 1.8 Principle 8: Defensive Documentation

**Axiom:** Documentation anticipates failure modes and explicitly addresses edge cases.

**Defensive documentation includes:**
1. Known limitations and constraints
2. Failure modes and recovery procedures
3. Security considerations and threat mitigations
4. Performance boundaries and degradation behaviours

---

## 2. MATURITY LEVEL DIFFERENTIATION

### 2.1 CMMI Level Mapping

| CMMI Level | Framework Application | Audit Depth |
|------------|----------------------|-------------|
| **Level 1: Initial** | Foundational controls; basic audit checklist | Sampling permitted (≥80%) |
| **Level 2: Managed** | Standardised processes; documented procedures | Representative coverage (≥90%) |
| **Level 3: Defined** | Organisation-wide standards; full traceability | Comprehensive coverage (≥95%) |
| **Level 4: Quantitatively Managed** | Metrics-driven; statistical process control | Full coverage (100%) with metrics |
| **Level 5: Optimising** | Continuous improvement; predictive capability | 100% + trend analysis + root cause |

**CIA-SIE-PURE Target Level:** Level 4 (100% coverage with metrics)

---

## 3. AUDIT TIER CLASSIFICATION

### 3.1 Five-Tier Audit Depth Model

| Tier | Name | Coverage | Evidence Standard | Applicable To |
|------|------|----------|-------------------|---------------|
| **Tier 1** | Cursory Review | Structure verification | File existence | Configuration files, assets |
| **Tier 2** | Standard Audit | Function-level review | Function signatures documented | Utility modules, helpers |
| **Tier 3** | Deep Audit | Line-by-line verification | Every function documented | Core business logic |
| **Tier 4** | Forensic Audit | Character-level analysis | Logic flow mapped | Security modules, cryptography |
| **Tier 5** | Exhaustive Verification | Mathematical proof | Formal verification artefacts | Safety-critical algorithms |

### 3.2 CIA-SIE-PURE Tier Assignment

| Artefact | Assigned Tier | Rationale |
|----------|---------------|-----------|
| `src/cia_sie/ai/` | Tier 4 | AI/LLM integration - constitutional compliance critical |
| `src/cia_sie/api/routes/` | Tier 3 | Business logic endpoints |
| `src/cia_sie/core/security.py` | Tier 4 | Security-critical |
| `src/cia_sie/dal/models.py` | Tier 4 | Constitutional columns prohibited |
| `src/cia_sie/dal/repositories.py` | Tier 3 | Data access patterns |
| `src/cia_sie/exposure/` | Tier 4 | Contradiction detection - Rule 2 critical |
| `src/cia_sie/ingestion/` | Tier 3 | Signal processing |
| `src/cia_sie/platforms/` | Tier 3 | External integrations |
| `tests/` | Tier 3 | Test completeness |
| `alembic/` | Tier 3 | Migration integrity |
| Configuration files | Tier 1 | Structure only |
| Documentation | Tier 2 | Accuracy verification |

### 3.3 Scope Classification

| Classification | Definition | Access Level |
|----------------|------------|--------------|
| **IN-SCOPE (Full Access)** | Subject to complete audit with read/write capability | Audit + Remediation |
| **IN-SCOPE (Read-Only)** | Subject to audit verification; modifications prohibited | Audit only |
| **REFERENCE-ONLY** | Used for cross-reference; not directly audited | Cross-reference |
| **OUT-OF-SCOPE** | Explicitly excluded; system-managed | No access |

**CIA-SIE-PURE Exclusions:**
- `.git/` — System-managed (OUT-OF-SCOPE)
- `__pycache__/` — Generated (OUT-OF-SCOPE)
- `.env` — Secrets file (OUT-OF-SCOPE, verify `.env.example` only)

---

# PART II: CONSTITUTIONAL FRAMEWORK
# ══════════════════════════════════════════════════════════════════════════════

## 4. INVIOLABLE RULES — CIA-SIE-PURE

Constitutional rules are **absolute constraints** that cannot be violated under any circumstances. A single violation renders the entire system non-compliant.

---

### RULE 1: Decision-Support ONLY

```
RULE 1: DECISION-SUPPORT ONLY

PROHIBITION:
- System must NEVER make investment decisions
- System must NEVER execute trades
- System must NEVER tell users what to buy/sell
- System must NEVER output actionable trading commands

REQUIREMENT:
- All outputs framed as informational/educational
- User retains 100% decision authority
- System provides data, human decides action

MANDATORY ARTEFACT:
- All AI-generated outputs MUST include disclaimer
- Disclaimer text: "This is decision-support information only, not investment advice"
- Disclaimer must appear in: narrative responses, API outputs, chat responses

DETECTION METHOD:
- Pattern search: `buy`, `sell`, `execute`, `trade`, `order` in action/command contexts
- Pattern search: imperative language directing investment action
- Review: prompt templates in `src/cia_sie/ai/prompt_builder.py`
- Review: narrative outputs in `src/cia_sie/ai/narrative_generator.py`
- Review: all API response schemas

VIOLATION SEVERITY: CRITICAL — Renders system non-compliant
```

---

### RULE 2: Never Resolve Contradictions

```
RULE 2: NEVER RESOLVE CONTRADICTIONS

PROHIBITION:
- System must NEVER pick sides when signals contradict
- System must NEVER aggregate signals into single recommendation
- System must NEVER weight signals by reliability/confidence
- System must NEVER hide, suppress, or deprioritise any signal
- System must NEVER average conflicting indicators

REQUIREMENT:
- Present ALL signals equally to user
- Contradictions are VALUABLE information, not errors to resolve
- Let human trader synthesise and decide
- Expose contradictions explicitly as useful data points

MANDATORY ARTEFACT:
- Contradiction detection module must EXPOSE not RESOLVE
- `src/cia_sie/exposure/contradiction_detector.py` must surface conflicts

DETECTION METHOD:
- Search database models for: `weight`, `score`, `confidence`, `priority`, `rank`
- Search codebase for: averaging logic, ranking logic, aggregation logic
- Search for: "best signal", "preferred", "most reliable", "highest confidence"
- Review: `src/cia_sie/exposure/` for resolution vs exposure patterns

VIOLATION SEVERITY: CRITICAL — Renders system non-compliant
```

---

### RULE 3: Descriptive NOT Prescriptive

```
RULE 3: DESCRIPTIVE NOT PRESCRIPTIVE

PROHIBITION:
- NEVER use prescriptive language for investment actions:
  - `should`, `must`, `recommend`, `suggest`, `advise`
  - `consider buying`, `consider selling`
  - `opportunity to`, `time to`
  - `you might want to`, `it would be wise to`
- NEVER frame outputs as advice or recommendations

REQUIREMENT:
- Only DESCRIBE what signals indicate
- Use neutral, factual language
- State observations, not directions

EXAMPLES:
✓ GOOD (Descriptive):
  - "Signal A indicates bullish momentum on the daily timeframe"
  - "Signal B shows bearish divergence on RSI"
  - "These two signals present contradicting views"

✗ BAD (Prescriptive):
  - "Based on signals, you should consider buying"
  - "We recommend taking a long position"
  - "This would be a good entry point"

DETECTION METHOD:
- Pattern search entire codebase for prescriptive terms
- Focus areas:
  - `src/cia_sie/ai/prompt_builder.py` — prompt templates
  - `src/cia_sie/ai/narrative_generator.py` — narrative outputs
  - `src/cia_sie/api/routes/` — API response messages
  - All string literals in business logic

VIOLATION SEVERITY: CRITICAL — Renders system non-compliant
```

---

## 5. PROHIBITED PATTERNS REGISTRY

### 5.1 Prohibited Database Columns

| Column Name | Reason | Detection Location |
|-------------|--------|-------------------|
| `weight` | Implies signal prioritisation (violates Rule 2) | `src/cia_sie/dal/models.py` |
| `score` | Implies signal ranking (violates Rule 2) | `src/cia_sie/dal/models.py` |
| `confidence` | Implies reliability judgment (violates Rule 2) | `src/cia_sie/dal/models.py` |
| `recommendation` | Implies prescriptive output (violates Rule 3) | `src/cia_sie/dal/models.py` |
| `priority` | Implies signal ordering (violates Rule 2) | `src/cia_sie/dal/models.py` |
| `rank` | Implies signal ordering (violates Rule 2) | `src/cia_sie/dal/models.py` |

### 5.2 Prohibited Code Patterns

| Pattern Category | Prohibited Pattern | Detection Method |
|------------------|-------------------|------------------|
| Signal Aggregation | `sum(signals)`, `average(signals)`, `mean()` on signals | Code search |
| Signal Weighting | `signal * weight`, `weighted_average` | Code search |
| Signal Ranking | `sorted(signals, key=...)`, `max(signals)`, `best_signal` | Code search |
| Prescriptive Output | `"should"`, `"recommend"`, `"suggest"` in output strings | String search |
| Action Commands | `execute_trade()`, `place_order()`, `buy()`, `sell()` | Function search |

### 5.3 Security Anti-Patterns (Universal)

| Pattern | Detection | Severity |
|---------|-----------|----------|
| Hardcoded credentials | Search for `password=`, `secret=`, `api_key=` with literals | CRITICAL |
| SQL injection | Search for string concatenation in queries | CRITICAL |
| Command injection | Search for `os.system()`, `subprocess` with user input | CRITICAL |
| Eval usage | Search for `eval()`, `exec()` | HIGH |
| Insecure deserialization | Search for `pickle.loads()` with untrusted input | HIGH |

---

# PART III: MULTI-PHASE AUDIT METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════

## 6. PHASE ARCHITECTURE

### 6.1 Nine-Phase Protocol

| Phase | Name | Scope | Output Artefact |
|-------|------|-------|-----------------|
| 1 | Repository Structure | File manifest, directory hierarchy | `PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md` |
| 2 | Backend Code | All server-side source code | `PHASE_2_BACKEND_CODE_AUDIT.md` |
| 3 | Frontend Code | N/A for CIA-SIE-PURE | `PHASE_3_FRONTEND_CODE_AUDIT.md` (N/A notice) |
| 4 | Data Layer | Database schemas, migrations, ORM | `PHASE_4_DATA_LAYER_AUDIT.md` |
| 5 | API Specification | Endpoint contracts, request/response | `PHASE_5_API_SPECIFICATION_AUDIT.md` |
| 6 | Test Coverage | Unit, integration tests | `PHASE_6_TEST_COVERAGE_AUDIT.md` |
| 7 | Documentation Sync | Spec ↔ Implementation alignment | `PHASE_7_DOCUMENTATION_SYNC_AUDIT.md` |
| 8 | Constitutional Compliance | Inviolable rule verification | `PHASE_8_CONSTITUTIONAL_COMPLIANCE_AUDIT.md` |
| 9 | Final Certification | Aggregation, scoring, certification | 5 certification deliverables (9A-9E) |

### 6.2 Execution Protocol

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 1 → Create Report → Commit → Proceed immediately                      │
│  Phase 2 → Create Report → Commit → Proceed immediately                      │
│  Phase 3 → Create Report (N/A) → Commit → Proceed immediately               │
│  Phase 4 → Create Report → Commit → Proceed immediately                      │
│  Phase 5 → Create Report → Commit → Proceed immediately                      │
│  Phase 6 → Create Report → Commit → Proceed immediately                      │
│  Phase 7 → Create Report → Commit → Proceed immediately                      │
│  Phase 8 → Create Report → Commit → Proceed immediately                      │
│  Phase 9 → Create 5 Reports → Commit → "AUDIT CYCLE COMPLETE"               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. PHASE-SPECIFIC PROCEDURES

### 7.1 PHASE 1: Repository Structure Audit

**Objective:** Establish complete file manifest with line counts and categorisation.

**Actions:**
1. Enumerate ALL files in repository (exclude `.git/`, `__pycache__/`)
2. Categorise by type:
   - Backend Source (`src/`)
   - Test Files (`tests/`)
   - Configuration (`.env.example`, `pyproject.toml`, `alembic.ini`)
   - Documentation (`*.md`, `docs/`)
   - Migrations (`alembic/`)
3. Calculate line counts per file
4. Verify directory structure against expected architecture
5. Identify any orphaned or unexpected files

**Output Format:**
```markdown
# PHASE 1: Repository Structure Audit

| Attribute | Value |
|-----------|-------|
| Phase | 1 |
| Date | [date] |
| Auditor | Cursor AI |
| Status | COMPLETE |

## Summary

| Category | Files | Lines |
|----------|-------|-------|
| Backend Source | X | Y |
| Test Files | X | Y |
| Configuration | X | Y |
| Documentation | X | Y |
| Migrations | X | Y |
| **TOTAL** | **X** | **Y** |

## Complete File Manifest

### Backend Source (`src/cia_sie/`)
| File | Lines | Tier |
|------|-------|------|
| [path] | [count] | [tier] |

### Test Files (`tests/`)
[...]

### Configuration
[...]

### Documentation
[...]

### Migrations (`alembic/`)
[...]

## Findings
[Any anomalies, orphaned files, unexpected items]
```

**Output Location:** `handoff/PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md`

**Commit Message:** `Phase 1 Complete: Repository Structure Audit [X files, Y lines enumerated]`

---

### 7.2 PHASE 2: Backend Code Audit

**Objective:** Verify every backend source file at assigned tier depth.

**Scope — Audit EVERY file:**

| Directory | Files to Audit | Tier |
|-----------|---------------|------|
| `src/cia_sie/` | `__init__.py`, `main.py` | 2 |
| `src/cia_sie/ai/` | `__init__.py`, `claude_client.py`, `model_registry.py`, `narrative_generator.py`, `prompt_builder.py`, `response_validator.py`, `usage_tracker.py` | 4 |
| `src/cia_sie/api/` | `__init__.py`, `app.py` | 3 |
| `src/cia_sie/api/routes/` | `__init__.py`, `ai.py`, `baskets.py`, `charts.py`, `chat.py`, `instruments.py`, `narratives.py`, `platforms.py`, `relationships.py`, `signals.py`, `silos.py`, `strategy.py`, `webhooks.py` | 3 |
| `src/cia_sie/core/` | `__init__.py`, `config.py`, `enums.py`, `exceptions.py`, `models.py`, `security.py` | 3-4 |
| `src/cia_sie/dal/` | `__init__.py`, `database.py`, `models.py`, `repositories.py` | 4 |
| `src/cia_sie/exposure/` | `__init__.py`, `confirmation_detector.py`, `contradiction_detector.py`, `relationship_exposer.py` | 4 |
| `src/cia_sie/ingestion/` | `__init__.py`, `freshness.py`, `signal_normalizer.py`, `webhook_handler.py` | 3 |
| `src/cia_sie/platforms/` | `__init__.py`, `base.py`, `kite.py`, `registry.py`, `tradingview.py` | 3 |

**Actions per file:**
1. Read ENTIRE file content
2. Document ALL classes with line numbers
3. Document ALL functions/methods with line numbers and signatures
4. Verify constitutional compliance (all 3 rules)
5. Check for prohibited patterns
6. Note any security concerns
7. Mark verification status with evidence

**Per-File Audit Template:**
```markdown
## File: `[full/path/to/file.py]`

### Metadata
- **Lines:** [count]
- **Audit Tier:** [1-5]
- **Status:** [ ] PENDING / [X] VERIFIED / [!] ISSUES FOUND

### Contents Enumeration

#### Classes
| Class | Lines | Purpose |
|-------|-------|---------|
| ClassName | 10-50 | [brief description] |

#### Functions/Methods
| Function | Lines | Signature | Purpose |
|----------|-------|-----------|---------|
| function_name | 52-67 | `def function_name(arg1: Type) -> ReturnType` | [description] |

### Constitutional Compliance
| Rule | Status | Evidence |
|------|--------|----------|
| Rule 1 (Decision-Support) | PASS/FAIL | [file:line reference or "No violations found"] |
| Rule 2 (No Contradiction Resolution) | PASS/FAIL | [file:line reference or "No violations found"] |
| Rule 3 (Descriptive Only) | PASS/FAIL | [file:line reference or "No violations found"] |

### Prohibited Pattern Check
| Pattern | Status | Location |
|---------|--------|----------|
| Hardcoded credentials | ABSENT/PRESENT | [file:line or N/A] |
| SQL injection risk | ABSENT/PRESENT | [file:line or N/A] |
| Prescriptive language | ABSENT/PRESENT | [file:line or N/A] |

### Cross-References
- **Implements Requirement:** [requirement ID from HANDOFF docs]
- **Tested By:** [test file reference]
- **Documented In:** [spec reference]

### Findings
[Any issues, concerns, or notes]
```

**Output Location:** `handoff/PHASE_2_BACKEND_CODE_AUDIT.md`

**Commit Message:** `Phase 2 Complete: Backend Code Audit [X files, Y lines verified]`

---

### 7.3 PHASE 3: Frontend Code Audit

**Status:** NOT APPLICABLE

**Reason:** CIA-SIE-PURE is a backend-only repository. No frontend directory exists.

**Output:**
```markdown
# PHASE 3: Frontend Code Audit

| Attribute | Value |
|-----------|-------|
| Phase | 3 |
| Date | [date] |
| Auditor | Cursor AI |
| Status | N/A |

## Determination

**Status:** NOT APPLICABLE

**Reason:** CIA-SIE-PURE is a backend-only repository created specifically for backend code audit and study. No frontend directory exists.

**Verification:**
- Checked for `frontend/` directory: NOT FOUND
- Checked for frontend file extensions (`.tsx`, `.jsx`, `.vue`, `.svelte`): NONE FOUND
- Checked for `package.json`: NOT FOUND (except in root if any)

**Conclusion:** Phase 3 is not applicable to this repository. Proceeding to Phase 4.
```

**Output Location:** `handoff/PHASE_3_FRONTEND_CODE_AUDIT.md`

**Commit Message:** `Phase 3 Complete: Frontend Audit N/A (Backend-only repository)`

---

### 7.4 PHASE 4: Data Layer Audit

**Objective:** Verify database schema integrity, constitutional compliance, and migration chain.

**Scope:**
- `src/cia_sie/dal/models.py` — ORM models (Tier 4)
- `src/cia_sie/dal/database.py` — Database connection (Tier 3)
- `src/cia_sie/dal/repositories.py` — Data access layer (Tier 3)
- `alembic/versions/*.py` — All migration files (Tier 3)
- `alembic/env.py` — Migration configuration (Tier 2)

**Actions:**

**4.1 ORM Models Audit (`models.py`):**
1. Read ENTIRE file
2. Document ALL tables/models
3. Document ALL columns with types and constraints
4. Document ALL relationships
5. **CRITICAL:** Verify NO prohibited columns:
   - `weight` — MUST BE ABSENT
   - `score` — MUST BE ABSENT
   - `confidence` — MUST BE ABSENT
   - `recommendation` — MUST BE ABSENT
   - `priority` — MUST BE ABSENT
   - `rank` — MUST BE ABSENT

**4.2 Database Connection Audit (`database.py`):**
1. Verify connection configuration
2. Check for hardcoded credentials (MUST BE ABSENT)
3. Verify session management

**4.3 Repository Audit (`repositories.py`):**
1. Document all repository classes
2. Verify no signal aggregation/weighting logic
3. Verify no SQL injection vulnerabilities

**4.4 Migration Chain Audit:**
1. List ALL migrations in chronological order
2. Verify migration chain integrity (no gaps)
3. Verify each migration is reversible
4. Cross-reference migrations with current models

**Output Format:**
```markdown
# PHASE 4: Data Layer Audit

## 4.1 Database Models

### Model: [ModelName]
| Column | Type | Constraints | Constitutional Check |
|--------|------|-------------|---------------------|
| id | Integer | PK | N/A |
| name | String | NOT NULL | N/A |
| [column] | [type] | [constraints] | [PASS/FAIL] |

### Prohibited Column Verification
| Prohibited Column | Status | Evidence |
|-------------------|--------|----------|
| weight | ABSENT ✓ / PRESENT ✗ | [line number if present] |
| score | ABSENT ✓ / PRESENT ✗ | [line number if present] |
| confidence | ABSENT ✓ / PRESENT ✗ | [line number if present] |
| recommendation | ABSENT ✓ / PRESENT ✗ | [line number if present] |
| priority | ABSENT ✓ / PRESENT ✗ | [line number if present] |
| rank | ABSENT ✓ / PRESENT ✗ | [line number if present] |

## 4.2 Migration Chain

| # | Migration File | Date | Description | Status |
|---|---------------|------|-------------|--------|
| 1 | [filename] | [date] | [description] | VERIFIED |

## 4.3 Findings
[Any issues or concerns]
```

**Output Location:** `handoff/PHASE_4_DATA_LAYER_AUDIT.md`

**Commit Message:** `Phase 4 Complete: Data Layer Audit [X tables, Y migrations, prohibited columns verified ABSENT]`

---

### 7.5 PHASE 5: API Specification Audit

**Objective:** Verify API implementation matches specification exactly.

**Scope:**
- `src/cia_sie/api/app.py` — Main FastAPI application
- `src/cia_sie/api/routes/*.py` — All route files
- `AI_HANDOFF/HANDOFF_02_API_ENDPOINTS.md` — API specification (reference)

**Actions:**
1. Read API specification document completely
2. For EACH documented endpoint:
   - Verify route exists in code (cite file:line)
   - Verify HTTP method matches
   - Verify URL path matches
   - Verify request schema/parameters match
   - Verify response schema matches
   - Document status: **Implemented** / **Partial** / **Missing**
3. Identify any UNDOCUMENTED endpoints (code exists, spec missing)
4. Verify constitutional compliance in all response schemas

**Output Format:**
```markdown
# PHASE 5: API Specification Audit

## Endpoint Verification Matrix

| Endpoint | Method | Spec Reference | Implementation | Status |
|----------|--------|---------------|----------------|--------|
| `/api/v1/instruments` | GET | HANDOFF_02#instruments | `routes/instruments.py:15` | ✓ Implemented |
| `/api/v1/signals` | POST | HANDOFF_02#signals | `routes/signals.py:42` | ✓ Implemented |
| [endpoint] | [method] | [spec ref] | [file:line] | [status] |

## Detailed Endpoint Audit

### Endpoint: `[METHOD] [path]`
| Attribute | Specification | Implementation | Match |
|-----------|--------------|----------------|-------|
| Method | [spec] | [code] | ✓/✗ |
| Path | [spec] | [code] | ✓/✗ |
| Request Body | [spec schema] | [code schema] | ✓/✗ |
| Response | [spec schema] | [code schema] | ✓/✗ |
| Auth Required | [spec] | [code] | ✓/✗ |

## Undocumented Endpoints
[Any endpoints in code but not in specification]

## Missing Endpoints
[Any endpoints in specification but not in code]

## Constitutional Compliance in APIs
[Verify no prescriptive language in response messages]
```

**Output Location:** `handoff/PHASE_5_API_SPECIFICATION_AUDIT.md`

**Commit Message:** `Phase 5 Complete: API Specification Audit [X endpoints verified, Y implemented, Z missing]`

---

### 7.6 PHASE 6: Test Coverage Audit

**Objective:** Verify test suite completeness and constitutional test coverage.

**Scope:**
- `tests/unit/*.py` — All unit test files
- `tests/integration/*.py` — All integration test files
- `tests/conftest.py` — Test configuration

**Actions:**
1. Read EVERY test file completely
2. Document all test classes and functions
3. Map tests to source modules they cover
4. Identify untested modules/functions
5. **CRITICAL:** Verify constitutional compliance tests exist:
   - Tests for Rule 1 (Decision-Support)
   - Tests for Rule 2 (No Contradiction Resolution)
   - Tests for Rule 3 (Descriptive Only)
   - Tests for prohibited column absence
6. Calculate/estimate coverage percentage

**Coverage Thresholds:**
| Category | Minimum Required |
|----------|------------------|
| Overall | ≥80% |
| Constitutional Tests | 100% (all rules must have tests) |
| Security-Critical Code | ≥95% |
| Core Business Logic | ≥90% |

**Output Format:**
```markdown
# PHASE 6: Test Coverage Audit

## Test File Inventory

| Test File | Test Count | Covers Module |
|-----------|------------|---------------|
| `test_models.py` | X | `dal/models.py` |
| [file] | [count] | [module] |

## Coverage Matrix

| Source Module | Test File | Coverage | Status |
|---------------|-----------|----------|--------|
| `src/cia_sie/ai/claude_client.py` | `test_claude_client.py` | X% | ✓/✗ |
| [module] | [test] | [%] | [status] |

## Constitutional Compliance Tests

| Rule | Test Exists | Test Location | Status |
|------|-------------|---------------|--------|
| Rule 1 (Decision-Support) | YES/NO | [file:line] | ✓/✗ |
| Rule 2 (No Contradiction Resolution) | YES/NO | [file:line] | ✓/✗ |
| Rule 3 (Descriptive Only) | YES/NO | [file:line] | ✓/✗ |
| Prohibited Columns | YES/NO | [file:line] | ✓/✗ |

## Untested Code
[List of modules/functions without test coverage]

## Findings
[Coverage gaps, missing tests, recommendations]
```

**Output Location:** `handoff/PHASE_6_TEST_COVERAGE_AUDIT.md`

**Commit Message:** `Phase 6 Complete: Test Coverage Audit [X test files, Y% coverage, constitutional tests verified]`

---

### 7.7 PHASE 7: Documentation Synchronisation Audit

**Objective:** Verify all documentation matches implementation (Zero Drift).

**Scope:**
- `AI_HANDOFF/HANDOFF_00_README.md`
- `AI_HANDOFF/HANDOFF_01_DESIGN_SPECIFICATION.md`
- `AI_HANDOFF/HANDOFF_02_API_ENDPOINTS.md`
- `AI_HANDOFF/HANDOFF_03_CONSTITUTIONAL_RULES.md`
- `AI_HANDOFF/HANDOFF_04_TECHNICAL_STANDARDS.md`
- `AI_HANDOFF/HANDOFF_05_COMPONENT_REQUIREMENTS.md`
- `AI_HANDOFF/HANDOFF_06_CSS_DESIGN_SYSTEM.md` (N/A - no frontend)
- `AI_HANDOFF/HANDOFF_07_BUSINESS_LOGIC.md`
- `AI_HANDOFF/HANDOFF_08_IMPLEMENTATION_STATUS.md`
- `README.md`
- `PROJECT_CONFIGURATION.md`
- `TESTING.md`
- `docs/` — All documentation files
- `context/decisions/` — Architecture Decision Records

**Actions:**
1. Read each documentation file
2. For each specification claim, verify against code
3. Document ALL discrepancies
4. Classify each discrepancy:
   - **Code Error:** Code doesn't match correct spec
   - **Spec Drift:** Spec doesn't match correct code
   - **Both:** Both need correction
5. Verify diagrams match implementation

**Output Format:**
```markdown
# PHASE 7: Documentation Synchronisation Audit

## Document Verification Matrix

| Document | Sections | Verified | Discrepancies |
|----------|----------|----------|---------------|
| HANDOFF_01_DESIGN_SPECIFICATION.md | X | Y | Z |
| [document] | [sections] | [verified] | [discrepancies] |

## Discrepancy Log

### Discrepancy #1
| Attribute | Value |
|-----------|-------|
| Document | [document name] |
| Section | [section reference] |
| Specification Says | [what spec claims] |
| Code Shows | [what code does] |
| Evidence | [file:line] |
| Classification | Code Error / Spec Drift / Both |
| Severity | Critical / High / Medium / Low |

## Synchronisation Status
| Category | Status |
|----------|--------|
| API Documentation | IN SYNC / DRIFT DETECTED |
| Data Model Documentation | IN SYNC / DRIFT DETECTED |
| Business Logic Documentation | IN SYNC / DRIFT DETECTED |
| Constitutional Rules Documentation | IN SYNC / DRIFT DETECTED |
```

**Output Location:** `handoff/PHASE_7_DOCUMENTATION_SYNC_AUDIT.md`

**Commit Message:** `Phase 7 Complete: Documentation Sync Audit [X documents verified, Y discrepancies found]`

---

### 7.8 PHASE 8: Constitutional Compliance Audit

**Objective:** Exhaustive verification of all 3 constitutional rules across entire codebase.

**Actions:**

**8.1 Rule 1 Verification (Decision-Support ONLY):**
```
Search ENTIRE codebase for:
- "buy" (in action context)
- "sell" (in action context)
- "execute" (trade context)
- "trade" (action context)
- "order" (trading context)
- "execute_trade"
- "place_order"

For each occurrence:
- Document file:line
- Assess context (violation or acceptable use)
- Mark PASS/FAIL

Verify disclaimer exists in:
- AI prompt templates
- Narrative outputs
- API responses
```

**8.2 Rule 2 Verification (Never Resolve Contradictions):**
```
Search ENTIRE codebase for:
- "weight" (variable/column)
- "score" (variable/column)
- "confidence" (variable/column)
- "priority" (signal context)
- "rank" (signal context)
- "aggregate" (signal context)
- "average" (signal context)
- "best_signal"
- "preferred"
- "most reliable"
- "weighted"

Search for logic patterns:
- Signal averaging
- Signal ranking
- Conflict resolution

For each occurrence:
- Document file:line
- Assess context
- Mark PASS/FAIL
```

**8.3 Rule 3 Verification (Descriptive NOT Prescriptive):**
```
Search ENTIRE codebase for:
- "should"
- "must" (in advice context)
- "recommend"
- "suggest"
- "advise"
- "consider buying"
- "consider selling"
- "opportunity"
- "you might want"
- "it would be wise"

Focus on:
- String literals
- Prompt templates
- Response messages
- Comments that might leak to output

For each occurrence:
- Document file:line
- Assess if in output path
- Mark PASS/FAIL
```

**8.4 Prohibited Column Verification:**
```
Search src/cia_sie/dal/models.py for:
- weight =
- score =
- confidence =
- recommendation =
- priority =
- rank =

Required result: ZERO occurrences
```

**Output Format:**
```markdown
# PHASE 8: Constitutional Compliance Audit

## Rule 1: Decision-Support ONLY

### Prohibited Pattern Search Results
| Pattern | Occurrences | Status |
|---------|-------------|--------|
| "buy" (action context) | X | PASS/FAIL |
| "sell" (action context) | X | PASS/FAIL |
| [pattern] | [count] | [status] |

### Violation Details (if any)
| # | File:Line | Pattern | Context | Severity |
|---|-----------|---------|---------|----------|
| 1 | [location] | [pattern] | [context] | CRITICAL |

### Disclaimer Verification
| Location | Disclaimer Present | Status |
|----------|-------------------|--------|
| Narrative Generator | YES/NO | PASS/FAIL |
| API Responses | YES/NO | PASS/FAIL |
| Chat Responses | YES/NO | PASS/FAIL |

### Rule 1 Status: **PASS / FAIL**

---

## Rule 2: Never Resolve Contradictions

### Prohibited Pattern Search Results
| Pattern | Occurrences | Status |
|---------|-------------|--------|
| "weight" | X | PASS/FAIL |
| "score" | X | PASS/FAIL |
| "confidence" | X | PASS/FAIL |
| [pattern] | [count] | [status] |

### Prohibited Column Check
| Column | In models.py | Status |
|--------|--------------|--------|
| weight | ABSENT/PRESENT | PASS/FAIL |
| score | ABSENT/PRESENT | PASS/FAIL |
| confidence | ABSENT/PRESENT | PASS/FAIL |
| recommendation | ABSENT/PRESENT | PASS/FAIL |

### Rule 2 Status: **PASS / FAIL**

---

## Rule 3: Descriptive NOT Prescriptive

### Prohibited Pattern Search Results
| Pattern | Occurrences | In Output Path | Status |
|---------|-------------|----------------|--------|
| "should" | X | YES/NO | PASS/FAIL |
| "recommend" | X | YES/NO | PASS/FAIL |
| [pattern] | [count] | [output path] | [status] |

### Rule 3 Status: **PASS / FAIL**

---

## Overall Constitutional Compliance

| Rule | Status | Violations |
|------|--------|------------|
| Rule 1: Decision-Support ONLY | PASS/FAIL | X |
| Rule 2: Never Resolve Contradictions | PASS/FAIL | X |
| Rule 3: Descriptive NOT Prescriptive | PASS/FAIL | X |

### CONSTITUTIONAL COMPLIANCE STATUS: **COMPLIANT / NON-COMPLIANT**
```

**Output Location:** `handoff/PHASE_8_CONSTITUTIONAL_COMPLIANCE_AUDIT.md`

**Commit Message:** `Phase 8 Complete: Constitutional Compliance Audit [3 rules verified, X total violations, Status: COMPLIANT/NON-COMPLIANT]`

---

### 7.9 PHASE 9: Final Certification

**Objective:** Produce complete audit certification package with 5 deliverables.

---

#### 9A: Requirements Traceability Matrix

**Objective:** Map EVERY requirement to implementation and test.

**Source:** `AI_HANDOFF/HANDOFF_01_DESIGN_SPECIFICATION.md` and other HANDOFF documents

**Output Format:**
```markdown
# PHASE 9A: Requirements Traceability Matrix

## Traceability Matrix

| Req ID | Requirement Description | Implementation | Test | Status |
|--------|------------------------|----------------|------|--------|
| REQ-001 | [description] | `[file:line]` | `[test file:line]` | ✓ Implemented |
| REQ-002 | [description] | `[file:line]` | `[test file:line]` | ◐ Partial |
| REQ-003 | [description] | — | — | ✗ Not Implemented |

## Status Legend
| Symbol | Status | Definition |
|--------|--------|------------|
| ✓ | Implemented | Requirement fully implemented and tested |
| ◐ | Partial | Requirement partially implemented |
| ✗ | Not Implemented | Requirement not implemented |
| N/A | Not Applicable | Requirement not applicable (e.g., frontend) |
| ⚠ | Deviation | Implementation deviates from specification |

## Summary
| Status | Count | Percentage |
|--------|-------|------------|
| ✓ Implemented | X | Y% |
| ◐ Partial | X | Y% |
| ✗ Not Implemented | X | Y% |
| N/A | X | Y% |
```

**Output Location:** `handoff/PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md`

---

#### 9B: Compliance Scorecard

**Objective:** Calculate compliance percentage per category.

**Output Format:**
```markdown
# PHASE 9B: Compliance Scorecard

## Phase Compliance Scores

| Phase | Category | Items Checked | Passed | Failed | Score |
|-------|----------|---------------|--------|--------|-------|
| 1 | Repository Structure | X | Y | Z | XX% |
| 2 | Backend Code | X | Y | Z | XX% |
| 3 | Frontend Code | N/A | N/A | N/A | N/A |
| 4 | Data Layer | X | Y | Z | XX% |
| 5 | API Specification | X | Y | Z | XX% |
| 6 | Test Coverage | X | Y | Z | XX% |
| 7 | Documentation Sync | X | Y | Z | XX% |
| 8 | Constitutional Compliance | X | Y | Z | XX% |

## Constitutional Compliance Scores

| Rule | Status | Score |
|------|--------|-------|
| Rule 1: Decision-Support ONLY | PASS/FAIL | 100%/0% |
| Rule 2: Never Resolve Contradictions | PASS/FAIL | 100%/0% |
| Rule 3: Descriptive NOT Prescriptive | PASS/FAIL | 100%/0% |

## Overall Scores

| Metric | Value |
|--------|-------|
| **Overall Compliance** | XX% |
| **Constitutional Compliance** | XX% |
| **Code Coverage** | XX% |
| **Documentation Sync** | XX% |

## Pass/Fail Determination

| Criterion | Threshold | Actual | Status |
|-----------|-----------|--------|--------|
| Overall Compliance | ≥95% | XX% | PASS/FAIL |
| Constitutional Compliance | 100% | XX% | PASS/FAIL |
| Critical Findings | 0 | X | PASS/FAIL |
| High Findings | ≤5 | X | PASS/FAIL |
```

**Output Location:** `handoff/PHASE_9B_COMPLIANCE_SCORECARD.md`

---

#### 9C: Gap Analysis

**Objective:** List ALL gaps found across all phases with severity classification.

**Output Format:**
```markdown
# PHASE 9C: Gap Analysis

## Gap Summary

| Severity | Count |
|----------|-------|
| CRITICAL | X |
| HIGH | X |
| MEDIUM | X |
| LOW | X |
| **TOTAL** | **X** |

## Critical Gaps

### GAP-001: [Title]
| Attribute | Value |
|-----------|-------|
| Severity | CRITICAL |
| Phase Found | X |
| Category | [Constitutional / Code / Test / Doc] |
| Description | [detailed description] |
| Location | [file:line] |
| Impact | [impact assessment] |
| Remediation | [recommended fix] |

## High Gaps
[Same format as Critical]

## Medium Gaps
[Same format]

## Low Gaps
[Same format]
```

**Output Location:** `handoff/PHASE_9C_GAP_ANALYSIS.md`

---

#### 9D: Remediation Roadmap

**Objective:** Prioritised fix list with dependencies.

**Output Format:**
```markdown
# PHASE 9D: Remediation Roadmap

## Prioritised Remediation Plan

### Priority 1: Critical (Must Fix Immediately)
| # | Gap ID | Description | Effort | Dependencies |
|---|--------|-------------|--------|--------------|
| 1 | GAP-XXX | [description] | [S/M/L] | None |
| 2 | GAP-XXX | [description] | [S/M/L] | GAP-XXX |

### Priority 2: High (Fix Before Production)
[Same format]

### Priority 3: Medium (Fix in Next Sprint)
[Same format]

### Priority 4: Low (Backlog)
[Same format]

## Dependency Graph
[Visual or textual representation of fix dependencies]

## Effort Legend
| Code | Meaning |
|------|---------|
| S | Small (< 1 hour) |
| M | Medium (1-4 hours) |
| L | Large (> 4 hours) |
```

**Output Location:** `handoff/PHASE_9D_REMEDIATION_ROADMAP.md`

---

#### 9E: Audit Certification

**Objective:** Formal certification statement.

**Output Format:**
```markdown
# PHASE 9E: Audit Certification

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      AUDIT CERTIFICATION STATEMENT                          │
│                                                                             │
│  Project: CIA-SIE-PURE                                                      │
│  Audit Date: [date]                                                         │
│  Auditor: Cursor AI                                                         │
│  Framework: Universal Code Audit Framework v2.0                             │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  SCOPE                                                                      │
│  ─────                                                                      │
│  • Repository: CIA-SIE-PURE (Backend-Only)                                  │
│  • Files Audited: [count]                                                   │
│  • Lines Verified: [count]                                                  │
│  • Coverage: [percentage]%                                                  │
│                                                                             │
│  FINDINGS SUMMARY                                                           │
│  ────────────────                                                           │
│  • Critical: [count]                                                        │
│  • High: [count]                                                            │
│  • Medium: [count]                                                          │
│  • Low: [count]                                                             │
│  • Total: [count]                                                           │
│                                                                             │
│  CONSTITUTIONAL COMPLIANCE                                                  │
│  ─────────────────────────                                                  │
│  • Rule 1 (Decision-Support ONLY): [PASS/FAIL]                              │
│  • Rule 2 (Never Resolve Contradictions): [PASS/FAIL]                       │
│  • Rule 3 (Descriptive NOT Prescriptive): [PASS/FAIL]                       │
│  • Prohibited Columns: [ABSENT/PRESENT]                                     │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  CERTIFICATION STATUS                                                       │
│  ════════════════════                                                       │
│                                                                             │
│      [ ] CERTIFIED                                                          │
│          100% coverage, 0 critical, 0 high findings                         │
│                                                                             │
│      [ ] CERTIFIED WITH OBSERVATIONS                                        │
│          100% coverage, 0 critical, ≤5 high with remediation plan           │
│                                                                             │
│      [ ] NOT CERTIFIED                                                      │
│          <100% coverage OR ≥1 critical OR >5 high findings                  │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  CERTIFICATION: [CERTIFIED / CERTIFIED WITH OBSERVATIONS / NOT CERTIFIED]  │
│                                                                             │
│  CONDITIONS/OBSERVATIONS (if applicable):                                   │
│  [List any conditions or observations]                                      │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  This certification is based on the Universal Code Audit &                  │
│  Application Development Framework v2.0 (Zero-Tolerance Standard)          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Output Location:** `handoff/PHASE_9E_AUDIT_CERTIFICATION.md`

**Final Commit Message:** `Phase 9 Complete: Final Certification [Overall: XX% compliance, Status: CERTIFIED/CERTIFIED WITH OBSERVATIONS/NOT CERTIFIED]`

---

# PART IV: EVIDENCE AND VERIFICATION STANDARDS
# ══════════════════════════════════════════════════════════════════════════════

## 9. EVIDENCE REQUIREMENTS

### 9.1 Evidence Hierarchy

| Level | Evidence Type | Strength | Acceptable For |
|-------|--------------|----------|----------------|
| 1 | Assertion | Weak | Never acceptable alone |
| 2 | Reference | Moderate | Tier 1-2 audits |
| 3 | Citation | Strong | Tier 3 audits |
| 4 | Verified Citation | Very Strong | Tier 4 audits |
| 5 | Formally Verified | Maximum | Tier 5 audits |

### 9.2 Citation Format Standards

| Format | Example | Use Case |
|--------|---------|----------|
| File reference | `handler.py` | General file reference |
| Path reference | `src/cia_sie/api/handler.py` | Specific file in hierarchy |
| Line reference | `handler.py:45` | Specific line |
| Range reference | `handler.py:45-67` | Line range |
| Function reference | `handler.py:process()` | Function citation |
| Class reference | `handler.py:Handler` | Class citation |
| Method reference | `handler.py:Handler.process()` | Method citation |
| Document section | `HANDOFF_02.md#validation` | Specification section |

### 9.3 Evidence Sufficiency Matrix

| Claim Type | Minimum Evidence |
|------------|------------------|
| "File exists" | File path |
| "Function implemented" | Function reference + signature |
| "Logic correct" | Line range + explanation |
| "Compliant with spec" | Code reference + spec reference |
| "No violations" | Search methodology + null result documentation |

---

# PART V: AUTONOMOUS EXECUTION DIRECTIVES
# ══════════════════════════════════════════════════════════════════════════════

## 10. EXECUTION MANDATE

### 10.1 Initiation Protocol

Upon receiving this document, Cursor shall:

1. **Acknowledge initiation:** Output exactly:
   ```
   GOLD STANDARD AUDIT INITIATED
   Repository: CIA-SIE-PURE
   Framework: Universal Code Audit Framework v2.0
   Phases: 9
   Deliverables: 13
   Commencing Phase 1...
   ```

2. **Execute ALL phases sequentially** (1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9)

3. **Create report file** after each phase in `handoff/` directory

4. **Commit after EACH phase** with specified commit message

5. **Do NOT pause** for human intervention between phases

6. **Upon completion:** Output exactly:
   ```
   ══════════════════════════════════════════════════════════════════════
   AUDIT CYCLE COMPLETE

   Reports Generated: 13
   Location: handoff/

   Deliverables:
   ✓ PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md
   ✓ PHASE_2_BACKEND_CODE_AUDIT.md
   ✓ PHASE_3_FRONTEND_CODE_AUDIT.md (N/A)
   ✓ PHASE_4_DATA_LAYER_AUDIT.md
   ✓ PHASE_5_API_SPECIFICATION_AUDIT.md
   ✓ PHASE_6_TEST_COVERAGE_AUDIT.md
   ✓ PHASE_7_DOCUMENTATION_SYNC_AUDIT.md
   ✓ PHASE_8_CONSTITUTIONAL_COMPLIANCE_AUDIT.md
   ✓ PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md
   ✓ PHASE_9B_COMPLIANCE_SCORECARD.md
   ✓ PHASE_9C_GAP_ANALYSIS.md
   ✓ PHASE_9D_REMEDIATION_ROADMAP.md
   ✓ PHASE_9E_AUDIT_CERTIFICATION.md

   Overall Compliance: XX%
   Constitutional Status: COMPLIANT/NON-COMPLIANT
   Certification: CERTIFIED/CERTIFIED WITH OBSERVATIONS/NOT CERTIFIED
   ══════════════════════════════════════════════════════════════════════
   ```

### 10.2 Quality Gates

| Criterion | Requirement |
|-----------|-------------|
| Coverage | 100% of enumerated files audited |
| Evidence | Every finding cites file:line |
| Completeness | Every function/class documented |
| Constitutional | All 3 rules verified with evidence |
| Traceability | Every requirement mapped |

### 10.3 Abort Conditions

Autonomous execution may be aborted ONLY for:
1. Repository access failure
2. Critical system error
3. Discovery of active security breach (immediate escalation required)

**Do NOT abort for:**
- Findings or violations (document and continue)
- Missing files referenced in specs (document as gap)
- Test failures (document in coverage audit)

---

## 11. OUTPUT LOCATION

All audit reports shall be created in:

```
CIA-SIE-PURE/
└── handoff/
    ├── PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md
    ├── PHASE_2_BACKEND_CODE_AUDIT.md
    ├── PHASE_3_FRONTEND_CODE_AUDIT.md
    ├── PHASE_4_DATA_LAYER_AUDIT.md
    ├── PHASE_5_API_SPECIFICATION_AUDIT.md
    ├── PHASE_6_TEST_COVERAGE_AUDIT.md
    ├── PHASE_7_DOCUMENTATION_SYNC_AUDIT.md
    ├── PHASE_8_CONSTITUTIONAL_COMPLIANCE_AUDIT.md
    ├── PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md
    ├── PHASE_9B_COMPLIANCE_SCORECARD.md
    ├── PHASE_9C_GAP_ANALYSIS.md
    ├── PHASE_9D_REMEDIATION_ROADMAP.md
    └── PHASE_9E_AUDIT_CERTIFICATION.md
```

---

# BEGIN AUDIT
# ══════════════════════════════════════════════════════════════════════════════

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        INSTRUCTION TO CURSOR                                │
│                                                                             │
│  1. Read this ENTIRE document thoroughly                                    │
│                                                                             │
│  2. Acknowledge with:                                                       │
│     "GOLD STANDARD AUDIT INITIATED"                                         │
│                                                                             │
│  3. Proceed IMMEDIATELY with Phase 1                                        │
│                                                                             │
│  4. Execute ALL 9 phases AUTONOMOUSLY                                       │
│                                                                             │
│  5. Create report file after each phase                                     │
│                                                                             │
│  6. Commit after each phase completion                                      │
│                                                                             │
│  7. Do NOT stop until ALL 13 deliverables are complete                      │
│                                                                             │
│  8. Do NOT ask for permission between phases                                │
│                                                                             │
│  9. Document ALL findings with file:line evidence                           │
│                                                                             │
│  10. Upon completion, output "AUDIT CYCLE COMPLETE"                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Based on Universal Code Audit & Application Development Framework v2.0*
*Zero-Tolerance Software Engineering Standard*
*Complete & Undiluted*
