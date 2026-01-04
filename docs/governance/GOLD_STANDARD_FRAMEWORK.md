# GOLD STANDARD UNIFIED FRAMEWORK
## Universal Software Audit & Certification Standard
### Version 3.0

---

**Document ID:** GSUF-001
**Version:** 3.0.0
**Classification:** Universal Reference Framework
**Applicability:** All mission-critical software development
**Compliance Alignment:** IEEE 1028, ISO/IEC 25010, ISO 27001, OWASP ASVS, NASA-STD-8739.8, FDA 21 CFR Part 11, SOX, DO-178C, IEC 62304

---

# EXECUTIVE SUMMARY

This framework establishes the **definitive methodology** for software code audit, validation, and handoff certification. It consolidates proven practices from aerospace (NASA/DO-178C), medical devices (FDA/IEC 62304), financial services (SOX/PCI-DSS), and critical infrastructure into a single, universally applicable standard.

**Core Tenets:**

1. **100% Coverage Mandate** — Every file verified; no sampling, no assumptions
2. **Zero Tolerance for Error** — Binary compliance; no partial states
3. **Evidence-Based Verification** — Every finding traceable to exact file:line
4. **Bidirectional Traceability** — Requirements ↔ Implementation ↔ Tests fully mapped
5. **Living Documentation** — Specifications synchronised with implementation
6. **Defence-in-Depth** — Multiple independent verification layers

---

# TABLE OF CONTENTS

**PART I: FOUNDATIONAL PRINCIPLES**
- [1. Eight Gold Standard Principles](#1-eight-gold-standard-principles)
- [2. Protocol Application Guide](#2-protocol-application-guide)

**PART II: VALIDATION ARCHITECTURE**
- [3. 15-Layer Validation Framework](#3-15-layer-validation-framework)
- [4. 5-Tier Audit Depth Model](#4-5-tier-audit-depth-model)
- [5. Maturity Level Alignment](#5-maturity-level-alignment)

**PART III: EXECUTION METHODOLOGY**
- [6. Nine-Phase Audit Protocol](#6-nine-phase-audit-protocol)
- [7. Phase-Specific Procedures](#7-phase-specific-procedures)
- [8. Autonomous Execution Directives](#8-autonomous-execution-directives)

**PART IV: EVIDENCE & VERIFICATION**
- [9. Evidence Standards](#9-evidence-standards)
- [10. Per-Artefact Audit Template](#10-per-artefact-audit-template)

**PART V: CERTIFICATION & DELIVERABLES**
- [11. Certification Criteria](#11-certification-criteria)
- [12. Deliverables Specification](#12-deliverables-specification)
- [13. Handoff Package Structure](#13-handoff-package-structure)

**PART VI: IMPLEMENTATION SUPPORT**
- [14. Automated Tooling](#14-automated-tooling)
- [15. CI/CD Integration](#15-cicd-integration)
- [16. Quick Reference Checklists](#16-quick-reference-checklists)

**APPENDICES**
- [Appendix A: Regulatory Cross-Reference Matrix](#appendix-a-regulatory-cross-reference-matrix)
- [Appendix B: Audit Report Templates](#appendix-b-audit-report-templates)
- [Appendix C: SDLC Phase Coverage Matrix](#appendix-c-sdlc-phase-coverage-matrix)

---

# PART I: FOUNDATIONAL PRINCIPLES

## 1. EIGHT GOLD STANDARD PRINCIPLES

### Principle 1: NASA-Style Rigour

Exhaustive, systematic, evidence-based validation where every claim is verifiable and reproducible.

| Attribute | Requirement |
|-----------|-------------|
| No Assumptions | Every finding cites exact `file:line` reference |
| No Shortcuts | 100% coverage verification, never statistical sampling |
| No Ambiguity | Binary PASS/FAIL determination only |
| Reproducibility | Any auditor following protocol reaches identical conclusions |

---

### Principle 2: Audit Before Build

Validation must precede construction. Building upon unvalidated foundations propagates defects exponentially.

```
MANDATED SEQUENCE:
┌───────────────────────────────────────────────────────────────────────────┐
│  1. Audit existing codebase against specifications                        │
│  2. Document all discrepancies with evidence                              │
│  3. Remediate (correct code OR update specifications)                     │
│  4. Construct new features upon validated baseline                        │
└───────────────────────────────────────────────────────────────────────────┘

PROHIBITED:
  ✗ Build new features on unvalidated code
  ✗ Defer audit activities
  ✗ Discover foundational defects post-construction
```

**Rationale:** Technical debt compounds. Defects in foundational layers propagate to all dependent components.

---

### Principle 3: Zero Drift Policy

Specifications and implementation shall remain synchronised at all times.

| Scenario | Mandated Action |
|----------|-----------------|
| Implementation differs; specification is correct | Correct the implementation |
| Implementation differs; implementation is correct | Update the specification |
| Both require improvement | Correct both; document the change |
| Divergence without justification | **AUDIT FAILURE** |

---

### Principle 4: Living Documentation

Documentation is maintained contemporaneously, not retrospectively. Stale documentation is a compliance violation.

| Anti-Pattern | Gold Standard |
|--------------|---------------|
| "Documentation will be completed later" | Document as construction proceeds |
| Stale README files | README reflects current operational state |
| Orphaned specifications | Specifications updated synchronously with code |

**Validation Test:** Can a qualified engineer understand the complete system from documentation alone?

---

### Principle 5: Full Bidirectional Traceability

Every line of code traces to a requirement; every requirement traces to implementation and verification.

```
┌──────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  REQUIREMENT │ ────►│  IMPLEMENTATION  │ ────►│  VERIFICATION   │
│              │◄─────│                  │◄─────│  (Test/Review)  │
└──────────────┘      └──────────────────┘      └─────────────────┘
                 BIDIRECTIONAL TRACEABILITY
```

| Question | Must Be Answerable |
|----------|-------------------|
| Which requirement does this code implement? | Yes — with evidence |
| Where is this requirement implemented? | Yes — with file:line |
| What tests verify this implementation? | Yes — with test reference |
| Is there orphan code (no requirement)? | Must be zero |

**Orphan Code:** Any code that cannot be traced to a documented requirement. Prohibited in zero-tolerance environments.

---

### Principle 6: Evidence-Based Validation

Assertions without evidence are invalid. Every compliance claim requires verifiable proof.

| Evidence Quality | Example | Acceptability |
|------------------|---------|---------------|
| **Weak** | "The module handles errors appropriately" | ✗ REJECTED |
| **Strong** | "Error handling at `handler.py:45-67`; implements try-except for DatabaseError per `SPEC.md#errors`; tested by `test_errors.py:test_db_error`" | ✓ ACCEPTED |

---

### Principle 7: Single Source of Truth

For any category of information, exactly one authoritative source exists.

| Information Category | Single Source |
|---------------------|---------------|
| Requirements | Requirements Specification Document |
| API Contracts | OpenAPI Schema / API Specification |
| Data Models | Database Schema / ORM Models |
| Business Logic | Authoritative Specification Document |
| Configuration | Environment Configuration Repository |

---

### Principle 8: Defence in Depth

Multiple validation layers catch different issue classes. No single layer provides complete coverage.

- Automate all repeatable checks
- Reserve manual review for architectural and semantic validation
- Layer automated tools with human verification

---

## 2. PROTOCOL APPLICATION GUIDE

### 2.1 When to Apply This Protocol

| Scenario | Protocol Application |
|----------|---------------------|
| **Project Handoff** | Full validation (all 15 layers, all 9 phases) |
| **Major Release (vX.0.0)** | Full validation |
| **Minor Release (vX.Y.0)** | Layers 1-8 + 12-13 |
| **Patch Release (vX.Y.Z)** | Layers 1-3 + 12 |
| **Pre-Audit Preparation** | Full validation |
| **Third-Party Code Review** | Layers 2-8 + 10-12 |

### 2.2 What This Protocol Guarantees

| Certification Area | Guarantee |
|--------------------|-----------|
| Code Quality | Meets maintainability standards, technical debt < 5% |
| Security Posture | OWASP Top 10 compliant, no critical vulnerabilities |
| Test Coverage | Follows testing pyramid, >80% overall, >95% critical paths |
| Documentation | Complete, accurate, and synchronized with code |
| CI/CD Pipeline | All checks passing, deployment-ready |
| API Integrity | Documented, validated, specification-compliant |
| Constitutional Compliance | Business rules enforced in code |
| Type Safety | Complete type coverage (where applicable) |

### 2.3 Pre-Validation Requirements

Before beginning validation, ensure these prerequisites are met:

**Repository Requirements:**
```
□ Version control initialized (Git)
□ Main/master branch protected
□ All work committed (no uncommitted changes)
□ Clean working directory
□ Remote repository accessible
□ README.md exists at root
□ .gitignore properly configured
□ No secrets in git history
```

**Environment Requirements:**
```
□ Development environment reproducible
□ All dependencies installable without errors
□ Application starts without errors
□ Database migrations apply to fresh database
□ Environment variables documented
```

**Documentation Requirements:**
```
□ Primary specification document exists
□ API documentation exists
□ Deployment instructions exist
□ Architecture overview exists
```

---

# PART II: VALIDATION ARCHITECTURE

## 3. 15-LAYER VALIDATION FRAMEWORK

### 3.1 Framework Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      15-LAYER VALIDATION FRAMEWORK                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ GOVERNANCE LAYERS (L1-L3)                                                   │
│   L1   Constitutional/Business Rules Compliance                             │
│   L2   Specification-to-Code Reconciliation                                 │
│   L3   Architecture Diagram-to-Code Trace                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ CODE QUALITY LAYERS (L4-L7)                                                 │
│   L4   Static Code Analysis                                                 │
│   L5   Technical Debt Assessment                                            │
│   L6   Code Complexity & Maintainability                                    │
│   L7   Dead Code & Unused Dependency Detection                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ DATA INTEGRITY LAYERS (L8-L9)                                               │
│   L8   Data Model Hierarchy Validation                                      │
│   L9   Database Schema & Migration Audit                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ INTERFACE LAYERS (L10-L11)                                                  │
│   L10  API Endpoint Reconciliation                                          │
│   L11  Frontend-Backend Type Synchronization                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ SECURITY LAYERS (L12-L13)                                                   │
│   L12  OWASP Top 10 Security Audit                                          │
│   L13  Automated Security Scanning (SAST/DAST)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ QUALITY ASSURANCE LAYERS (L14-L15)                                          │
│   L14  Test Coverage & Quality Analysis                                     │
│   L15  CI/CD Pipeline Validation                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Layer Criticality Matrix

| Layer | Name | Criticality | Blocking? | Automation Level |
|-------|------|-------------|-----------|------------------|
| L1 | Constitutional Compliance | **CRITICAL** | YES | Manual + Grep |
| L2 | Spec-to-Code Reconciliation | **CRITICAL** | YES | Manual |
| L3 | Architecture Trace | HIGH | YES | Manual |
| L4 | Static Code Analysis | HIGH | YES | Automated |
| L5 | Technical Debt | MEDIUM | NO | Automated |
| L6 | Complexity/Maintainability | MEDIUM | NO | Automated |
| L7 | Dead Code Detection | LOW | NO | Automated |
| L8 | Data Model Hierarchy | HIGH | YES | Manual |
| L9 | Database Schema Audit | HIGH | YES | Semi-Automated |
| L10 | API Reconciliation | **CRITICAL** | YES | Semi-Automated |
| L11 | Type Synchronization | HIGH | YES | Automated |
| L12 | OWASP Security Audit | **CRITICAL** | YES | Manual |
| L13 | Automated Security Scanning | **CRITICAL** | YES | Automated |
| L14 | Test Coverage | HIGH | YES | Automated |
| L15 | CI/CD Validation | **CRITICAL** | YES | Automated |

### 3.3 Layer-to-Phase Mapping

| Layer | Maps to Audit Phase |
|-------|---------------------|
| L1 | Phase 8 |
| L2, L3 | Phase 7 |
| L4, L5, L6, L7 | Phase 2, 3 |
| L8, L9 | Phase 4 |
| L10, L11 | Phase 5 |
| L12, L13 | Phase 8 |
| L14 | Phase 6 |
| L15 | Phase 1, 9 |

---

## 4. 5-TIER AUDIT DEPTH MODEL

### 4.1 Tier Definitions

| Tier | Name | Coverage | Evidence Standard | Apply To |
|------|------|----------|-------------------|----------|
| **Tier 1** | Cursory Review | Structure verification | File existence confirmed | Config files, static assets |
| **Tier 2** | Standard Audit | Function-level review | Function signatures documented | Utility modules, helpers |
| **Tier 3** | Deep Audit | Line-by-line verification | Every function documented with purpose | Core business logic |
| **Tier 4** | Forensic Audit | Character-level analysis | Logic flow mapped completely | Security modules, API handlers |
| **Tier 5** | Exhaustive Verification | Mathematical proof level | Formal verification artefacts | Cryptographic operations, safety-critical |

### 4.2 Tier Assignment Matrix

| Artefact Category | Default Tier | Elevation Triggers |
|-------------------|--------------|-------------------|
| Source Code — Business Logic | Tier 3 | Security implications → Tier 4 |
| Source Code — Security/Auth | Tier 4 | Cryptographic operations → Tier 5 |
| Source Code — Utility | Tier 2 | Shared across critical paths → Tier 3 |
| Test Files | Tier 3 | Coverage of Tier 4+ code → Tier 4 |
| Database Migrations | Tier 3 | Schema affecting critical data → Tier 4 |
| Configuration Files | Tier 1 | Security parameters → Tier 3 |
| CI/CD Pipelines | Tier 2 | Deployment to production → Tier 3 |
| Specifications | Tier 2 | Cross-reference verification only |
| Documentation | Tier 1 | Accuracy verification only |

### 4.3 Scope Classification

| Classification | Definition | Access Level |
|----------------|------------|--------------|
| **IN-SCOPE (Full Access)** | Subject to complete audit with read/write | Audit + Remediation |
| **IN-SCOPE (Read-Only)** | Subject to audit; modifications prohibited | Audit only |
| **REFERENCE-ONLY** | Used for cross-reference; not directly audited | Cross-reference |
| **OUT-OF-SCOPE** | Explicitly excluded; system-managed | No access |

**Standard Exclusions:**
- `.git/` — Version control internals
- `node_modules/` — Dependency artifacts
- `__pycache__/` — Python bytecode
- `venv/`, `.venv/` — Virtual environments

---

## 5. MATURITY LEVEL ALIGNMENT

### 5.1 CMMI Level Mapping

| CMMI Level | Framework Application | Audit Depth |
|------------|----------------------|-------------|
| **Level 1: Initial** | Foundational controls | Sampling permitted (≥80%) |
| **Level 2: Managed** | Standardised processes | Representative coverage (≥90%) |
| **Level 3: Defined** | Organisation-wide standards | Comprehensive coverage (≥95%) |
| **Level 4: Quantitatively Managed** | Metrics-driven | Full coverage (100%) with metrics |
| **Level 5: Optimising** | Continuous improvement | 100% + trend analysis + root cause |

### 5.2 Regulatory Compliance Mapping

| Regulatory Framework | Minimum CMMI Level | Coverage Requirement |
|---------------------|-------------------|---------------------|
| FDA 21 CFR Part 11 | Level 3 | 100% for Class III devices |
| DO-178C Level A | Level 4 | 100% + MC/DC coverage |
| SOX Section 404 | Level 3 | 100% for in-scope controls |
| ISO 27001 | Level 2 | Risk-based coverage |
| PCI-DSS | Level 3 | 100% for cardholder data paths |
| IEC 62304 Class C | Level 4 | 100% + safety analysis |

---

# PART III: EXECUTION METHODOLOGY

## 6. NINE-PHASE AUDIT PROTOCOL

### 6.1 Phase Architecture

| Phase | Name | Scope | Output Artefact |
|-------|------|-------|-----------------|
| 1 | Repository Structure | File manifest, hierarchy | `PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md` |
| 2 | Backend Code | Server-side source code | `PHASE_2_BACKEND_CODE_AUDIT.md` |
| 3 | Frontend Code | Client-side source code | `PHASE_3_FRONTEND_CODE_AUDIT.md` |
| 4 | Data Layer | Schemas, migrations, ORM | `PHASE_4_DATA_LAYER_AUDIT.md` |
| 5 | API Specification | Endpoint contracts | `PHASE_5_API_SPECIFICATION_AUDIT.md` |
| 6 | Test Coverage | Unit, integration, E2E | `PHASE_6_TEST_COVERAGE_AUDIT.md` |
| 7 | Documentation Sync | Spec ↔ Implementation | `PHASE_7_DOCUMENTATION_SYNC_AUDIT.md` |
| 8 | Security & Constitutional | Rules verification | `PHASE_8_SECURITY_CONSTITUTIONAL_AUDIT.md` |
| 9 | Final Certification | Aggregation, scoring | 5 certification deliverables |

### 6.2 Phase 9 Sub-Deliverables

| Deliverable | Purpose |
|-------------|---------|
| `PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md` | Requirement → Implementation → Test mapping |
| `PHASE_9B_COMPLIANCE_SCORECARD.md` | Percentage compliance per category |
| `PHASE_9C_GAP_ANALYSIS.md` | All gaps classified by severity |
| `PHASE_9D_REMEDIATION_ROADMAP.md` | Prioritised remediation plan |
| `PHASE_9E_AUDIT_CERTIFICATION.md` | Formal certification statement |

### 6.3 Execution Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. Acknowledge: "GOLD STANDARD AUDIT INITIATED"                            │
│  2. Verify Pre-Validation Requirements — STOP if any fail                   │
│  3. Phase 1 → Commit → Proceed immediately                                  │
│  4. Phase 2 → Commit → Proceed immediately                                  │
│  5. Phase 3 → Commit → Proceed immediately                                  │
│  6. Phase 4 → Commit → Proceed immediately                                  │
│  7. Phase 5 → Commit → Proceed immediately                                  │
│  8. Phase 6 → Commit → Proceed immediately                                  │
│  9. Phase 7 → Commit → Proceed immediately                                  │
│  10. Phase 8 → Commit → Proceed immediately                                 │
│  11. Phase 9 (all sub-phases) → Commit                                      │
│  12. Announce: "AUDIT CYCLE COMPLETE — 13 REPORTS GENERATED"                │
└─────────────────────────────────────────────────────────────────────────────┘

DO NOT pause for human intervention between phases.
DO NOT skip phases.
DO NOT proceed to staging until all phases complete.
```

### 6.4 Standardised Commit Messages

| Phase | Commit Message Template |
|-------|------------------------|
| 1 | `Phase 1 Complete: Repository Structure Audit [X files enumerated, Y total lines]` |
| 2 | `Phase 2 Complete: Backend Code Audit [X files, Y lines verified, Z issues]` |
| 3 | `Phase 3 Complete: Frontend Code Audit [X files, Y components verified]` |
| 4 | `Phase 4 Complete: Data Layer Audit [schema verified, X migrations validated]` |
| 5 | `Phase 5 Complete: API Specification Audit [X endpoints verified, Y discrepancies]` |
| 6 | `Phase 6 Complete: Test Coverage Audit [X% coverage, Y test files verified]` |
| 7 | `Phase 7 Complete: Documentation Sync Audit [X documents verified, Y discrepancies]` |
| 8 | `Phase 8 Complete: Security & Constitutional Audit [OWASP: X/10, Y rules verified]` |
| 9 | `Phase 9 Complete: Final Certification [Overall: X% compliance, Status: LEVEL]` |

---

## 7. PHASE-SPECIFIC PROCEDURES

### Phase 1: Repository Structure Audit

**Objective:** Establish complete file manifest with categorisation.

**Actions:**
1. Enumerate ALL files in repository
2. Categorise: Backend Source | Frontend Source | Test | Config | Documentation | Assets
3. Calculate line counts per file
4. Verify directory structure matches architecture
5. Identify orphaned or untracked files
6. Verify CI/CD configuration exists

**Output Format:**
```markdown
# PHASE 1: Repository Structure Audit
**Status:** COMPLETE

## Summary Statistics
| Category | Files | Lines | % of Total |
|----------|-------|-------|------------|
| Backend Source | X | Y | Z% |
| Frontend Source | X | Y | Z% |
| Test Files | X | Y | Z% |
| Configuration | X | Y | Z% |
| Documentation | X | Y | Z% |
| **TOTAL** | **X** | **Y** | **100%** |

## Complete File Manifest
[Categorised listing with line counts and tier assignments]
```

---

### Phase 2: Backend Code Audit

**Objective:** Verify every backend source file at assigned Tier depth.

**Actions per file:**
1. Read entire file — no skipping
2. Document all classes and functions with line ranges
3. Run linter with strict rules
4. Check for prohibited patterns
5. Verify constitutional compliance
6. Assess complexity metrics

**Layers Covered:** L4, L5, L6, L7

**Metrics to Capture:**

| Metric | Target |
|--------|--------|
| Cyclomatic Complexity | < 10 per function |
| Function Length | < 50 lines |
| File Length | < 500 lines |
| Nesting Depth | < 4 levels |
| Technical Debt Ratio | < 5% |

---

### Phase 3: Frontend Code Audit

**Objective:** Verify every frontend source file.

**Actions per file:**
1. Read entire file
2. Document components and functions
3. Run linters (ESLint, TypeScript)
4. Compare against component specification
5. Verify type safety (no implicit `any`)
6. Check accessibility compliance (WCAG 2.1 AA)

**Layers Covered:** L4, L5, L6, L7, L11

---

### Phase 4: Data Layer Audit

**Objective:** Verify database schema integrity and migration chain.

**Actions:**
1. Read all ORM/model definitions completely
2. Verify NO prohibited columns exist (per constitutional rules)
3. Read all migration files
4. Apply migrations to fresh database — verify no errors
5. Test rollback capability
6. Document all tables, columns, relationships, constraints
7. Run EXPLAIN on critical queries

**Layers Covered:** L8, L9

**Pass Criteria:**
- All specified entities exist
- All relationships correctly implemented
- No prohibited fields present
- All migrations apply without error
- Critical queries use indexes

---

### Phase 5: API Specification Audit

**Objective:** Verify API implementation matches specification exactly.

**Actions:**
1. Read API specification document
2. For EACH documented endpoint:
   - Verify route exists in code
   - Verify HTTP method matches
   - Verify request schema matches
   - Verify response schema matches
   - Document: IMPLEMENTED | PARTIAL | MISSING
3. Reverse trace: Find undocumented endpoints
4. Validate OpenAPI spec (if applicable)
5. Test each endpoint

**Layers Covered:** L10, L11

---

### Phase 6: Test Coverage Audit

**Objective:** Verify test suite completeness following testing pyramid.

**Testing Pyramid Standards:**
```
┌─────────────────────────────────────┐
│           E2E Tests (10%)           │
│         ┌───────────────┐           │
│         │      E2E      │           │
│         └───────────────┘           │
│      Integration Tests (20%)        │
│     ┌─────────────────────┐         │
│     │    Integration      │         │
│     └─────────────────────┘         │
│         Unit Tests (70%)            │
│  ┌───────────────────────────────┐  │
│  │        Unit Tests             │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Coverage Thresholds:**

| Criticality Level | Minimum Coverage |
|-------------------|------------------|
| Safety-Critical (Tier 5) | 100% + MC/DC |
| Security-Critical (Tier 4) | 100% statement |
| Business-Critical (Tier 3) | ≥95% statement |
| Standard (Tier 2) | ≥80% statement |
| Constitutional Rules | **100%** — non-negotiable |
| Overall | >80% |

**Layers Covered:** L14

---

### Phase 7: Documentation Synchronisation Audit

**Objective:** Verify all documentation matches implementation.

**Actions:**
1. Inventory all specification documents
2. Trace each specification claim to code
3. Reverse trace code to specifications
4. Verify architecture diagrams match code
5. Document all discrepancies
6. Classify: Code Error | Spec Drift | Both

**Layers Covered:** L2, L3

---

### Phase 8: Security & Constitutional Compliance Audit

**Objective:** Exhaustive verification of security and constitutional rules.

**OWASP Top 10 (2021) Checklist:**

| # | Risk | Validation Method |
|---|------|-------------------|
| A01 | Broken Access Control | Review auth middleware |
| A02 | Cryptographic Failures | Review encryption, key management |
| A03 | Injection | Verify parameterized queries |
| A04 | Insecure Design | Review architecture patterns |
| A05 | Security Misconfiguration | Review configs, headers |
| A06 | Vulnerable Components | Dependency vulnerability scan |
| A07 | Auth/Session Failures | Review auth flows |
| A08 | Data Integrity Failures | Review signatures |
| A09 | Logging Failures | Verify no sensitive data logged |
| A10 | SSRF | Review URL handling |

**Constitutional Compliance Actions:**
1. For each constitutional rule:
   - Search ENTIRE codebase for prohibited patterns
   - Document EVERY occurrence with file:line
   - Verify mandatory artefacts exist
2. Generate compliance matrix

**Layers Covered:** L1, L12, L13

---

### Phase 9: Final Certification

**9A: Requirements Traceability Matrix**
- Map EVERY requirement to implementation
- Document file:line for each
- Status: Implemented | Partial | Missing | N/A

**9B: Compliance Scorecard**
- Calculate compliance percentage per category
- Overall compliance percentage
- Pass/Fail determination per layer

**9C: Gap Analysis**
- List ALL gaps found across all phases
- Classify: CRITICAL | HIGH | MEDIUM | LOW
- Impact assessment for each

**9D: Remediation Roadmap**
- Priority 1: Must-fix before staging (blocking)
- Priority 2: Should-fix before production
- Priority 3: Track for future
- Effort estimates and dependencies

**9E: Audit Certification**
- Formal certification statement
- Scope summary
- Finding summary
- Certification status

---

## 8. AUTONOMOUS EXECUTION DIRECTIVES

### 8.1 Initiation Protocol

When this framework is invoked:

1. Acknowledge: `"GOLD STANDARD AUDIT INITIATED"`
2. Verify Pre-Validation Requirements
3. Execute all 9 phases sequentially
4. Commit after each phase completion
5. Do NOT pause for human intervention between phases
6. Upon completion: `"AUDIT CYCLE COMPLETE — 13 REPORTS GENERATED"`

### 8.2 Quality Gate

| Criterion | Requirement |
|-----------|-------------|
| Coverage | 100% of enumerated files |
| Evidence | Every finding cites file:line |
| Completeness | Every function/class documented |
| Constitutional | Every rule verified |
| Layers | All 15 layers validated |
| Phases | All 9 phases complete |

### 8.3 Abort Conditions

Autonomous execution may ONLY abort for:
1. Pre-Validation Requirements failure
2. Repository access failure
3. Critical system error
4. Discovery of active security breach (immediate escalation required)

---

# PART IV: EVIDENCE & VERIFICATION

## 9. EVIDENCE STANDARDS

### 9.1 Evidence Hierarchy

| Level | Evidence Type | Strength | Acceptable For |
|-------|--------------|----------|----------------|
| 1 | Assertion | Weak | **NEVER acceptable alone** |
| 2 | Reference | Moderate | Tier 1-2 audits |
| 3 | Citation | Strong | Tier 3 audits |
| 4 | Verified Citation | Very Strong | Tier 4 audits |
| 5 | Formally Verified | Maximum | Tier 5 audits |

### 9.2 Citation Format Standards

| Format | Example | Use Case |
|--------|---------|----------|
| File reference | `handler.py` | General file reference |
| Path reference | `src/api/handler.py` | Specific file |
| Line reference | `handler.py:45` | Specific line |
| Range reference | `handler.py:45-67` | Line range |
| Function reference | `handler.py:process()` | Function citation |
| Class reference | `handler.py:Handler` | Class citation |
| Method reference | `handler.py:Handler.process()` | Method citation |
| Spec section | `SPEC.md#validation` | Specification section |

### 9.3 Evidence Sufficiency Matrix

| Claim Type | Minimum Evidence Required |
|------------|---------------------------|
| "File exists" | File path |
| "Function implemented" | Function reference + signature |
| "Logic correct" | Line range + explanation |
| "Compliant with spec" | Code reference + spec reference |
| "No violations" | Search methodology + null result evidence |
| "Test covers feature" | Test file:function + assertion description |

---

## 10. PER-ARTEFACT AUDIT TEMPLATE

For EACH file audited:

```markdown
## File: [full/path/to/file.ext]

### Metadata
- **Lines:** [count]
- **Audit Tier:** [1-5]
- **Status:** [ ] PENDING / [X] VERIFIED / [!] ISSUES FOUND

### Contents Enumeration
| Type | Name | Lines | Purpose |
|------|------|-------|---------|
| Class | ClassName | 10-50 | [description] |
| Function | func_name | 52-67 | [description] |

### Prohibited Pattern Check
| Pattern | Status | Location |
|---------|--------|----------|
| [pattern] | ABSENT ✓ | — |

### Complexity Metrics
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Cyclomatic Complexity | X | ≤10 | PASS/FAIL |
| Function Length | X | ≤50 | PASS/FAIL |
| Nesting Depth | X | ≤4 | PASS/FAIL |

### Cross-References
- Implements: [requirement ID]
- Tested by: [test file reference]
- Documented in: [spec reference]

### Findings
[List issues with file:line references]
```

---

# PART V: CERTIFICATION & DELIVERABLES

## 11. CERTIFICATION CRITERIA

### 11.1 Certification Levels

| Level | Requirements | Use Case |
|-------|--------------|----------|
| **PLATINUM** | GOLD + external audit verified | Compliance-critical, enterprise |
| **GOLD** | All layers PASS, 0 critical, 0 high, ≥98% overall | Production release, handoff |
| **SILVER** | All CRITICAL layers PASS, 0 critical, ≤3 high, ≥95% overall | Production with observations |
| **BRONZE** | All CRITICAL layers PASS, 0 critical, ≤5 high, ≥90% overall | Internal handoff, staging |
| **NOT CERTIFIED** | Any CRITICAL layer FAIL, OR >0 critical, OR >5 high | Remediation required |

### 11.2 Pass/Fail Determination

```
LAYER RESULT:
- PASS: All criteria met
- PASS WITH EXCEPTIONS: Criteria met with documented exceptions
- FAIL: Criteria not met

OVERALL CERTIFICATION:
- All CRITICAL layers (L1, L2, L10, L12, L13, L15) must PASS
- HIGH layers: Maximum 2 with documented exceptions
- MEDIUM/LOW layers: May have documented exceptions
```

### 11.3 Certification Statement Template

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AUDIT CERTIFICATION STATEMENT                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  Project: [Project Name]                                                    │
│  Audit Date: [DATE]                                                         │
│  Auditor: [Identification]                                                  │
│  Protocol: Gold Standard Unified Framework v3.0                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  SCOPE                                                                      │
│  • Files Audited: [X]                                                       │
│  • Lines Verified: [Y]                                                      │
│  • Coverage: 100%                                                           │
│  • Layers Validated: 15/15                                                  │
│  • Phases Completed: 9/9                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  FINDINGS SUMMARY                                                           │
│  • Critical: [0]                                                            │
│  • High: [X]                                                                │
│  • Medium: [Y]                                                              │
│  • Low: [Z]                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  CERTIFICATION STATUS: [PLATINUM / GOLD / SILVER / BRONZE / NOT CERTIFIED] │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGING AUTHORISATION: [AUTHORISED / NOT AUTHORISED]                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. DELIVERABLES SPECIFICATION

### 12.1 Complete Deliverables List (13 Total)

| # | Deliverable | Phase | Purpose |
|---|-------------|-------|---------|
| 1 | Repository Structure Audit | 1 | File manifest |
| 2 | Backend Code Audit | 2 | Server-side verification |
| 3 | Frontend Code Audit | 3 | Client-side verification |
| 4 | Data Layer Audit | 4 | Schema verification |
| 5 | API Specification Audit | 5 | Contract verification |
| 6 | Test Coverage Audit | 6 | Test completeness |
| 7 | Documentation Sync Audit | 7 | Specification alignment |
| 8 | Security & Constitutional Audit | 8 | Compliance verification |
| 9 | Requirements Traceability Matrix | 9A | Bidirectional traceability |
| 10 | Compliance Scorecard | 9B | Quantitative metrics |
| 11 | Gap Analysis | 9C | Deficiency enumeration |
| 12 | Remediation Roadmap | 9D | Corrective action plan |
| 13 | Audit Certification | 9E | Formal certification |

### 12.2 Deliverable Quality Standards

| Criterion | Requirement |
|-----------|-------------|
| Completeness | Every in-scope artefact addressed |
| Evidence | Every finding cites specific file:line |
| Objectivity | Binary determinations; no subjective language |
| Traceability | Cross-references to specifications |
| Actionability | Findings enable remediation |

---

## 13. HANDOFF PACKAGE STRUCTURE

### 13.1 Required Deliverables Checklist

```
DOCUMENTATION
□ README.md with quick start instructions
□ Architecture overview document
□ API documentation (OpenAPI spec or equivalent)
□ Data model documentation
□ Deployment guide
□ Configuration reference
□ Troubleshooting guide
□ KNOWN_ISSUES.md

CODE ARTIFACTS
□ Clean, passing CI/CD pipeline
□ All tests passing
□ No uncommitted changes
□ Tagged release (vX.Y.Z)
□ CHANGELOG.md updated

VALIDATION ARTIFACTS
□ All 13 audit reports (Phases 1-9)
□ Certification report (Phase 9E)
□ Security scan reports
□ Coverage reports
□ Lint/analysis reports

ACCESS & CREDENTIALS
□ Repository access documented
□ CI/CD access documented
□ Deployment credentials documented
□ Third-party service credentials documented
```

### 13.2 Directory Structure

```
project/
├── README.md
├── CHANGELOG.md
├── KNOWN_ISSUES.md
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── data-model/
│   └── deployment/
├── handoff/
│   ├── PHASE_1_REPOSITORY_STRUCTURE_AUDIT.md
│   ├── PHASE_2_BACKEND_CODE_AUDIT.md
│   ├── PHASE_3_FRONTEND_CODE_AUDIT.md
│   ├── PHASE_4_DATA_LAYER_AUDIT.md
│   ├── PHASE_5_API_SPECIFICATION_AUDIT.md
│   ├── PHASE_6_TEST_COVERAGE_AUDIT.md
│   ├── PHASE_7_DOCUMENTATION_SYNC_AUDIT.md
│   ├── PHASE_8_SECURITY_CONSTITUTIONAL_AUDIT.md
│   ├── PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md
│   ├── PHASE_9B_COMPLIANCE_SCORECARD.md
│   ├── PHASE_9C_GAP_ANALYSIS.md
│   ├── PHASE_9D_REMEDIATION_ROADMAP.md
│   ├── PHASE_9E_AUDIT_CERTIFICATION.md
│   ├── VALIDATION_EXECUTION_LOG.md
│   └── reports/
│       ├── coverage/
│       ├── security/
│       └── quality/
├── src/
└── tests/
```

### 13.3 Handoff Validation KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| Environment Setup Time | < 4 hours | Time from clone to running |
| First PR Time | < 1 week | Time to first merged PR |
| Support Requests | < 5 in first month | Questions to original team |
| Critical Bug Discovery | **0** | Bugs found not in KNOWN_ISSUES.md |

---

# PART VI: IMPLEMENTATION SUPPORT

## 14. AUTOMATED TOOLING

### 14.1 Code Quality Tools

| Purpose | Tool | Command |
|---------|------|---------|
| Python Linting | pylint + flake8 | `pylint src/ && flake8 src/` |
| Python Types | mypy | `mypy src/ --strict` |
| Python Complexity | radon | `radon cc src/ -a` |
| Python Dead Code | vulture | `vulture src/` |
| JS/TS Linting | ESLint | `eslint . --ext ts,tsx` |
| JS/TS Types | TypeScript | `tsc --noEmit` |
| General Quality | SonarQube | `sonar-scanner` |

### 14.2 Security Tools

| Purpose | Tool | Command |
|---------|------|---------|
| SAST | Semgrep | `semgrep --config auto src/` |
| Python Security | Bandit | `bandit -r src/` |
| SCA (Python) | pip-audit | `pip-audit` |
| SCA (Node) | npm audit | `npm audit --production` |
| Secrets | git-secrets | `git secrets --scan` |
| Secrets | truffleHog | `trufflehog git file://. --only-verified` |

### 14.3 Testing Tools

| Purpose | Tool | Command |
|---------|------|---------|
| Python Tests | pytest | `pytest --cov=src tests/` |
| JS/TS Tests | vitest/jest | `npm test -- --coverage` |
| E2E | Playwright | `npx playwright test` |
| API Testing | Postman/Newman | `newman run collection.json` |

### 14.4 Documentation Tools

| Purpose | Tool | Command |
|---------|------|---------|
| OpenAPI Validation | openapi-spec-validator | `openapi-spec-validator spec.yaml` |
| Markdown Lint | markdownlint | `markdownlint '**/*.md'` |
| Link Checker | lychee | `lychee docs/` |

---

## 15. CI/CD INTEGRATION

### 15.1 Reference Implementation

```yaml
# .github/workflows/gold-standard-validation.yml
name: Gold Standard Validation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # L4: Static Code Analysis
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Python Lint
        run: |
          pip install pylint flake8
          pylint src/ --exit-zero
          flake8 src/
      - name: TypeScript Lint
        run: |
          npm ci
          npm run lint

  # L6: Type Check
  types:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Python Types
        run: |
          pip install mypy
          mypy src/ --ignore-missing-imports
      - name: TypeScript Types
        run: |
          npm ci
          npm run build

  # L13: Security Scan
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Python Security
        run: |
          pip install bandit pip-audit
          bandit -r src/
          pip-audit
      - name: Node Security
        run: npm audit --production
      - name: Secret Scan
        run: |
          pip install trufflehog
          trufflehog git file://. --only-verified --fail

  # L14: Test Coverage
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Backend Tests
        run: |
          pip install -r requirements.txt
          pytest --cov=src --cov-report=xml --cov-fail-under=80 tests/
      - name: Frontend Tests
        run: |
          npm ci
          npm test -- --coverage
      - name: Upload Coverage
        uses: codecov/codecov-action@v3

  # L15: Build Verification
  build:
    runs-on: ubuntu-latest
    needs: [lint, types, security, test]
    steps:
      - uses: actions/checkout@v4
      - name: Build Backend
        run: |
          pip install -r requirements.txt
          python -m compileall src/
      - name: Build Frontend
        run: |
          npm ci
          npm run build
```

---

## 16. QUICK REFERENCE CHECKLISTS

### 16.1 Pre-Validation Quick Check

```
□ Git status clean (no uncommitted changes)
□ Main branch up to date
□ All dependencies installable
□ Application starts without errors
□ Database migrations apply
□ README.md exists and current
□ Specification documents accessible
```

### 16.2 Pre-Staging Quick Check

```
□ All 9 phases completed with committed reports
□ All CI jobs green
□ Main branch clean
□ Version tagged (vX.Y.Z)
□ CHANGELOG.md updated
□ No critical security alerts
□ No failing tests
□ Coverage meets thresholds (>80% overall, >95% critical)
□ Documentation synchronised
□ Certification report generated
□ Priority 1 remediation complete
□ KNOWN_ISSUES.md complete
```

### 16.3 Security Quick Check

```
□ No secrets in code or git history
□ Dependencies updated (no critical CVEs)
□ Security headers configured
□ Authentication working
□ Authorization enforced
□ Input validation present
□ Output encoding present
□ HTTPS enforced (production)
□ Logging configured (no sensitive data logged)
□ Error messages generic (no stack traces to client)
□ Rate limiting implemented
□ CORS properly configured
```

### 16.4 Code Quality Quick Check

```
□ Linter passes (zero errors)
□ Type checker passes (strict mode)
□ No TODO/FIXME in critical paths
□ No commented-out code blocks > 10 lines
□ Functions < 50 lines
□ Files < 500 lines
□ Cyclomatic complexity < 10 (per function)
□ No code duplication > 10 lines
□ All public APIs documented
□ Consistent naming conventions
□ Technical Debt Ratio < 5%
```

### 16.5 Documentation Quick Check

```
□ README.md exists and current
□ Architecture documented
□ API endpoints documented
□ Data model documented
□ Deployment documented
□ Configuration documented
□ Troubleshooting guide exists
□ Known issues documented
□ Environment setup documented
```

---

# APPENDICES

## APPENDIX A: REGULATORY CROSS-REFERENCE MATRIX

| Framework | Key Requirements | Framework Sections |
|-----------|------------------|-------------------|
| **IEEE 1028** | Software Reviews & Audits | 6, 7, 9, 11 |
| **ISO/IEC 25010** | Software Product Quality | 3, 4, 14 |
| **ISO 27001** | Information Security | 7.8, 8, 16.3 |
| **OWASP ASVS** | Application Security | 7.8, 14 |
| **NASA-STD-8739.8** | Software Assurance | 1, 6, 9 |
| **FDA 21 CFR Part 11** | Electronic Records | 5, 8, 11 |
| **SOX Section 404** | Internal Controls | 7, 9, 11, 12 |
| **DO-178C** | Airborne Software | 4, 6, 9, 11 |
| **IEC 62304** | Medical Device Software | All |
| **ISO 26262** | Automotive Safety | 4, 6, 8 |
| **PCI-DSS** | Payment Card Industry | 7.8, 8, 14 |

---

## APPENDIX B: AUDIT REPORT TEMPLATES

### B.1 Phase Report Header

```markdown
# [PHASE NAME] AUDIT REPORT

| Attribute | Value |
|-----------|-------|
| Phase | [number] |
| Date | [date] |
| Auditor | [identification] |
| Scope | [description] |
| Status | COMPLETE / IN PROGRESS |
```

### B.2 Finding Template

```markdown
## Finding: [FINDING-XXX]

| Attribute | Value |
|-----------|-------|
| Severity | CRITICAL / HIGH / MEDIUM / LOW |
| Category | [category] |
| Location | [file:line] |
| Specification Reference | [spec reference] |

### Description
[Detailed description]

### Evidence
[Specific evidence]

### Recommendation
[Recommended corrective action]
```

### B.3 Validation Execution Log Template

```markdown
# VALIDATION EXECUTION LOG

**Project:** ___________________
**Date:** ___________________
**Auditor:** ___________________
**Protocol:** Gold Standard Unified Framework v3.0

## Phase Execution

| Phase | Start | End | Result | Files | Issues |
|-------|-------|-----|--------|-------|--------|
| 1 | | | PASS/FAIL | | |
| 2 | | | PASS/FAIL | | |
| ... | | | | | |

## Summary

| Metric | Value |
|--------|-------|
| Total Phases | 9 |
| Passed | ___ |
| Failed | ___ |
| Total Files Audited | ___ |
| Total Lines Verified | ___ |
| Reports Generated | 13 |

## Certification Recommendation

[ ] PLATINUM
[ ] GOLD
[ ] SILVER
[ ] BRONZE
[ ] NOT CERTIFIED — requires remediation
```

---

## APPENDIX C: SDLC PHASE COVERAGE MATRIX

| SDLC Phase | Audit Phase(s) | Layers | Coverage |
|------------|----------------|--------|----------|
| Requirements | 7, 9A | L2 | Specification verification |
| Design | 7 | L3 | Architecture documentation |
| Implementation | 2, 3, 4, 5 | L4-L11 | Code verification |
| Testing | 6 | L14 | Test coverage |
| Deployment | 1, 9 | L15 | Configuration verification |
| Maintenance | 8, 9 | L1, L12, L13 | Compliance and security |

---

# DOCUMENT METADATA

```yaml
document_id: GSUF-001
version: 3.0.0
status: AUTHORITATIVE
classification: Universal Reference Framework
applicability: All mission-critical software development

consolidates:
  - GOLD_STANDARD_VALIDATION_PROTOCOL_v2.0_GENERIC.md
  - UNIVERSAL_CODE_AUDIT_AND_APPLICATION_DEVELOPMENT_FRAMEWORK_v2.0_GENERIC.md

compliance_alignment:
  - IEEE 1028-2008 (Software Reviews & Audits)
  - ISO/IEC 25010:2011 (Software Product Quality)
  - ISO/IEC 27001 (Information Security)
  - OWASP ASVS v4.0 (Application Security)
  - NASA-STD-8739.8 (Software Assurance)
  - FDA 21 CFR Part 11 (Electronic Records)
  - SOX Section 404 (Internal Controls)
  - DO-178C (Airborne Software)
  - IEC 62304 (Medical Device Software)
  - ISO 26262 (Automotive Safety)
  - PCI-DSS (Payment Card Industry)

key_components:
  - Eight Gold Standard Principles
  - 15-Layer Validation Framework
  - 5-Tier Audit Depth Model
  - Nine-Phase Audit Methodology
  - Evidence-Based Verification Standards
  - Certification Criteria (Platinum/Gold/Silver/Bronze)
  - 13 Deliverables Specification
  - Regulatory Cross-Reference Matrix

usage:
  This framework is project-agnostic. To apply to a specific project:
  1. Create PROJECT_CONSTITUTIONAL_RULES.md (Tier 2 Domain Adapter)
  2. Create PROJECT_AUDIT_CONFIGURATION.md (Tier 3 Project Config)
  3. Reference this framework in audit execution
```

---

**END OF DOCUMENT**

*Gold Standard Unified Framework v3.0*
*Universal Software Audit & Certification Standard*
*Consolidation of GOLD_STANDARD_VALIDATION_PROTOCOL + UNIVERSAL_CODE_AUDIT_FRAMEWORK*
