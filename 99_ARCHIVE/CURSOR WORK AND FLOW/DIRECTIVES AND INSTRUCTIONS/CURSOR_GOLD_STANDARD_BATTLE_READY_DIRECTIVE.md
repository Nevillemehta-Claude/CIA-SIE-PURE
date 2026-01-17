# CURSOR GOLD STANDARD BATTLE-READY DIRECTIVE
## Strategic Validation & Completion Brief for CIA-SIE-PURE and MERCURY
**Issued:** January 15, 2026
**Authority:** Neville Mehta (Principal, Standards Authority)
**Classification:** COMMAND DIRECTIVE - MANDATORY EXECUTION

---

# EXECUTIVE SUMMARY

This directive instructs Cursor to apply the **Gold Standard Development Framework** to validate, complete, and certify both **CIA-SIE-PURE** (backend signals engine) and **MERCURY** (full-stack trading dashboard) as **BATTLE-READY** for production deployment.

**Objective:** Transform current codebase state into Gold Standard-compliant, production-grade software through systematic verification, gap remediation, and certification.

---

# PART 1: GOLD STANDARD FRAMEWORK TO APPLY

## 1.1 The 8 Gold Standard Principles (MANDATORY)

Every action taken must honor these principles:

| # | Principle | Application to This Task |
|---|-----------|--------------------------|
| 1 | **Accuracy First** | No shortcuts. Every fix must be correct, not quick. |
| 2 | **Complete Coverage** | Every feature specified must be implemented and working. |
| 3 | **Continuous Verification** | Test after every change. No untested code. |
| 4 | **Living Documentation** | Update docs as code changes. No stale documentation. |
| 5 | **Explicit Assumptions** | Document all assumptions. No hidden logic. |
| 6 | **Modularity** | Respect component boundaries. No cross-contamination. |
| 7 | **Traceability** | Every change traceable to requirement or issue. |
| 8 | **Progressive Refinement** | Make it work → Make it right → Make it fast. |

## 1.2 The 5 Immutable Laws (CANNOT BE VIOLATED)

| Law | Meaning | Enforcement |
|-----|---------|-------------|
| **Singular Truth** | One source of truth per artifact | No duplicate configs, no conflicting definitions |
| **Explicit Dependency** | All dependencies declared | No implicit imports, no magic connections |
| **Verification Gates** | Cannot proceed past failed tests | Fix before moving forward |
| **Reversibility** | Every change can be undone | Git commits, migrations reversible |
| **Audit Trail** | Every decision documented | Commit messages explain WHY |

## 1.3 The 10 Verification Layers (HIERARCHICAL - ALL MUST PASS)

```
LAYER 10: ACCEPTANCE ────── Does it meet business goals?
LAYER 9:  SECURITY ──────── Are there vulnerabilities?
LAYER 8:  PERFORMANCE ───── Is it within acceptable bounds?
LAYER 7:  END-TO-END ────── Do complete workflows work?
LAYER 6:  FUNCTIONAL ────── Do features work correctly?
LAYER 5:  REGRESSION ────── Did we break anything?
LAYER 4:  INTEGRATION ───── Do components connect properly?
LAYER 3:  CONTRACT ──────── Are API contracts honored?
LAYER 2:  UNIT ──────────── Do individual functions work?
LAYER 1:  SYNTAX ────────── Does the code compile/run?
```

**RULE:** Lower layers must pass before higher layers are tested.

---

# PART 2: CIA-SIE-PURE VALIDATION REQUIREMENTS

## 2.1 System Identity

| Attribute | Value |
|-----------|-------|
| **Name** | CIA-SIE-PURE |
| **Type** | Backend Signals Intelligence Engine |
| **Tech Stack** | Python, FastAPI, PostgreSQL, SQLAlchemy |
| **Purpose** | Generate, store, and serve trading signals |

## 2.2 Verification Checklist

### Layer 1: Syntax Verification
- [ ] All Python files pass `python -m py_compile`
- [ ] No syntax errors in any module
- [ ] All imports resolve correctly
- [ ] `pyproject.toml` / `requirements.txt` complete

### Layer 2: Unit Test Verification
- [ ] pytest discovers all test files
- [ ] All unit tests pass: `pytest tests/unit/`
- [ ] Coverage target: **>90%** on core logic
- [ ] No skipped tests without documented reason

### Layer 3: Contract Verification
- [ ] OpenAPI spec exists and is valid
- [ ] All endpoints match OpenAPI definitions
- [ ] Request/response schemas enforced
- [ ] Error responses follow standard format

### Layer 4: Integration Verification
- [ ] Database migrations run cleanly: `alembic upgrade head`
- [ ] Database connections establish successfully
- [ ] All repository methods work with real DB
- [ ] External service mocks available for testing

### Layer 5: Regression Verification
- [ ] Full test suite passes: `pytest`
- [ ] No previously passing tests now fail
- [ ] CI pipeline green

### Layer 6: Functional Verification
- [ ] Signal generation produces valid output
- [ ] Signal storage persists correctly
- [ ] Signal retrieval returns expected data
- [ ] All business logic behaves per specification

### Layer 7: End-to-End Verification
- [ ] API server starts: `uvicorn main:app`
- [ ] Health endpoint responds: `GET /health`
- [ ] Full signal flow works: Generate → Store → Retrieve
- [ ] Postman/curl tests pass

### Layer 8: Performance Verification
- [ ] API response time < 200ms for standard queries
- [ ] Database queries optimized (no N+1)
- [ ] Memory usage within bounds
- [ ] No blocking operations on main thread

### Layer 9: Security Verification
- [ ] No hardcoded credentials
- [ ] Environment variables for secrets
- [ ] SQL injection prevention (parameterized queries)
- [ ] Input validation on all endpoints
- [ ] CORS configured appropriately

### Layer 10: Acceptance Verification
- [ ] All specified features implemented
- [ ] API documentation complete
- [ ] Deployment instructions documented
- [ ] Principal sign-off obtained

## 2.3 Gap Identification Protocol

For each gap found, document:

```markdown
## GAP: [ID]
**Type:** Structural | Flow | Validation | Documentation
**Location:** [file/module]
**Description:** [what is missing or broken]
**Impact:** Critical | High | Medium | Low
**Remediation:** [specific fix required]
**Verification:** [how to confirm fix works]
```

## 2.4 Required Outputs

Upon completion, produce:

1. **CIA-SIE-PURE_VERIFICATION_REPORT.md** - All checklist items with status
2. **CIA-SIE-PURE_GAP_REMEDIATION_LOG.md** - All gaps found and fixed
3. **CIA-SIE-PURE_BATTLE_READY_CERTIFICATE.md** - Final certification

---

# PART 3: MERCURY VALIDATION REQUIREMENTS

## 3.1 System Identity

| Attribute | Value |
|-----------|-------|
| **Name** | MERCURY |
| **Type** | Full-Stack Trading Dashboard |
| **Backend Stack** | Python, FastAPI (or similar) |
| **Frontend Stack** | React/Next.js, TypeScript, TailwindCSS |
| **Purpose** | Visualize signals, manage portfolios, execute trades |

## 3.2 Backend Verification Checklist

### Layer 1: Syntax Verification
- [ ] All Python files compile without error
- [ ] All TypeScript files compile: `tsc --noEmit`
- [ ] No linting errors: `eslint` / `ruff`
- [ ] Dependencies install cleanly: `pip install` / `npm install`

### Layer 2: Unit Test Verification
- [ ] Backend unit tests pass: `pytest tests/unit/`
- [ ] Frontend unit tests pass: `npm test`
- [ ] Coverage target: **>85%** on business logic
- [ ] Component tests for critical UI elements

### Layer 3: Contract Verification
- [ ] Backend OpenAPI spec valid and complete
- [ ] Frontend API client matches backend spec
- [ ] Type definitions synchronized
- [ ] No type mismatches between layers

### Layer 4: Integration Verification
- [ ] Backend connects to database
- [ ] Backend connects to CIA-SIE-PURE (if applicable)
- [ ] Frontend connects to backend API
- [ ] WebSocket connections establish (if used)
- [ ] Authentication flow works end-to-end

### Layer 5: Regression Verification
- [ ] Full backend test suite passes
- [ ] Full frontend test suite passes
- [ ] No visual regressions (if snapshot tests exist)
- [ ] CI pipeline green

### Layer 6: Functional Verification
- [ ] Dashboard loads and displays data
- [ ] Charts render correctly
- [ ] Filters and sorting work
- [ ] CRUD operations function
- [ ] Real-time updates work (if applicable)

### Layer 7: End-to-End Verification
- [ ] Backend starts successfully
- [ ] Frontend builds: `npm run build`
- [ ] Frontend starts: `npm run dev` / `npm start`
- [ ] Complete user workflows function:
  - [ ] Login/Authentication
  - [ ] View dashboard
  - [ ] View signals
  - [ ] Apply filters
  - [ ] Export data (if applicable)

### Layer 8: Performance Verification
- [ ] Frontend bundle size acceptable (<500KB gzipped)
- [ ] Initial page load < 3 seconds
- [ ] API calls < 200ms response time
- [ ] No memory leaks on long sessions
- [ ] Smooth scrolling and interactions

### Layer 9: Security Verification
- [ ] Authentication implemented and working
- [ ] Authorization enforced (role-based if applicable)
- [ ] No XSS vulnerabilities
- [ ] No CSRF vulnerabilities
- [ ] Secure cookie handling
- [ ] HTTPS enforced
- [ ] No sensitive data in frontend bundle

### Layer 10: Acceptance Verification
- [ ] All dashboard features functional
- [ ] UI matches design specifications
- [ ] Responsive design works (mobile/tablet/desktop)
- [ ] Accessibility basics (keyboard nav, contrast)
- [ ] User documentation complete
- [ ] Deployment guide documented
- [ ] Principal sign-off obtained

## 3.3 Frontend-Specific Verification

### Component Verification
- [ ] All components render without errors
- [ ] Props validation (TypeScript types)
- [ ] Error boundaries in place
- [ ] Loading states implemented
- [ ] Empty states handled

### State Management Verification
- [ ] State updates correctly on user actions
- [ ] No stale state issues
- [ ] Proper cleanup on unmount
- [ ] Optimistic updates work (if used)

### API Integration Verification
- [ ] All API calls have error handling
- [ ] Loading indicators during fetches
- [ ] Retry logic for failed requests
- [ ] Proper caching strategy

## 3.4 Required Outputs

Upon completion, produce:

1. **MERCURY_BACKEND_VERIFICATION_REPORT.md** - Backend checklist with status
2. **MERCURY_FRONTEND_VERIFICATION_REPORT.md** - Frontend checklist with status
3. **MERCURY_GAP_REMEDIATION_LOG.md** - All gaps found and fixed
4. **MERCURY_BATTLE_READY_CERTIFICATE.md** - Final certification

---

# PART 4: EXECUTION PROTOCOL

## 4.1 Phase Sequence

Execute in this order:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  PHASE A: ENVIRONMENT SETUP                                     │
│  ─────────────────────────────                                  │
│  1. Clone/access both repositories                              │
│  2. Install all dependencies                                    │
│  3. Configure environment variables                             │
│  4. Verify development environment works                        │
│                                                                 │
│  PHASE B: CIA-SIE-PURE VALIDATION                              │
│  ─────────────────────────────────                              │
│  1. Execute Layer 1-10 verification                             │
│  2. Document all gaps found                                     │
│  3. Remediate gaps (fix issues)                                 │
│  4. Re-verify after each fix                                    │
│  5. Produce verification report                                 │
│  6. Produce battle-ready certificate                            │
│                                                                 │
│  PHASE C: MERCURY BACKEND VALIDATION                            │
│  ─────────────────────────────────────                          │
│  1. Execute Layer 1-10 verification for backend                 │
│  2. Document all gaps found                                     │
│  3. Remediate gaps                                              │
│  4. Re-verify after each fix                                    │
│  5. Produce backend verification report                         │
│                                                                 │
│  PHASE D: MERCURY FRONTEND VALIDATION                           │
│  ──────────────────────────────────────                         │
│  1. Execute Layer 1-10 verification for frontend                │
│  2. Execute component-specific verification                     │
│  3. Document all gaps found                                     │
│  4. Remediate gaps                                              │
│  5. Re-verify after each fix                                    │
│  6. Produce frontend verification report                        │
│                                                                 │
│  PHASE E: INTEGRATION VALIDATION                                │
│  ─────────────────────────────────                              │
│  1. Verify CIA-SIE-PURE ↔ MERCURY connection (if applicable)   │
│  2. Verify end-to-end data flow                                 │
│  3. Document any integration gaps                               │
│  4. Remediate and re-verify                                     │
│                                                                 │
│  PHASE F: CERTIFICATION                                         │
│  ───────────────────────                                        │
│  1. Compile all verification reports                            │
│  2. Confirm all checklists complete                             │
│  3. Produce battle-ready certificates                           │
│  4. Submit for Principal approval                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 4.2 Fix-Verify Cycle (MANDATORY)

For every issue found:

```
DETECT ──► DOCUMENT ──► FIX ──► VERIFY ──► CONFIRM
                         │         │
                         └─────────┘
                        (loop until pass)
```

**CRITICAL RULE:** Never mark an issue as fixed until verification passes.

## 4.3 Communication Protocol

### When Starting Each Phase
```
"Beginning Phase [X]: [Name]
Target: [what will be verified]
Approach: [methodology]"
```

### When Gap Found
```
"GAP IDENTIFIED: [ID]
Type: [Structural/Flow/Validation/Documentation]
Severity: [Critical/High/Medium/Low]
Location: [file:line or module]
Issue: [description]
Proposed Fix: [solution]"
```

### When Gap Fixed
```
"GAP REMEDIATED: [ID]
Fix Applied: [description]
Verification: [test run/result]
Status: CONFIRMED FIXED"
```

### When Phase Complete
```
"Phase [X] Complete
Gaps Found: [count]
Gaps Fixed: [count]
Remaining Issues: [count or NONE]
Verification Status: PASS/FAIL"
```

## 4.4 Escalation Protocol

If a blocker is encountered that cannot be resolved:

```
"BLOCKER ENCOUNTERED
Phase: [current phase]
Issue: [description]
Attempted Solutions: [what was tried]
Recommendation: [suggested path forward]
Decision Required: [specific question for Principal]"
```

---

# PART 5: DELIVERABLES CHECKLIST

## 5.1 Required Reports

| Report | Purpose | When Produced |
|--------|---------|---------------|
| CIA-SIE-PURE_VERIFICATION_REPORT.md | Full Layer 1-10 checklist results | After Phase B |
| CIA-SIE-PURE_GAP_REMEDIATION_LOG.md | All gaps and fixes | During Phase B |
| CIA-SIE-PURE_BATTLE_READY_CERTIFICATE.md | Certification document | End of Phase B |
| MERCURY_BACKEND_VERIFICATION_REPORT.md | Backend checklist results | After Phase C |
| MERCURY_FRONTEND_VERIFICATION_REPORT.md | Frontend checklist results | After Phase D |
| MERCURY_GAP_REMEDIATION_LOG.md | All gaps and fixes | During Phases C-D |
| MERCURY_BATTLE_READY_CERTIFICATE.md | Certification document | End of Phase D |
| INTEGRATION_VERIFICATION_REPORT.md | Cross-system validation | After Phase E |
| FINAL_BATTLE_READY_SUMMARY.md | Executive summary | End of Phase F |

## 5.2 Battle-Ready Certificate Template

```markdown
# BATTLE-READY CERTIFICATE

## System: [CIA-SIE-PURE / MERCURY]
## Date: [YYYY-MM-DD]
## Certified By: Cursor (Gold Standard Validation)
## Approved By: Neville Mehta (Principal)

---

## VERIFICATION SUMMARY

| Layer | Status | Notes |
|-------|--------|-------|
| 1. Syntax | ✅ PASS | |
| 2. Unit | ✅ PASS | Coverage: XX% |
| 3. Contract | ✅ PASS | |
| 4. Integration | ✅ PASS | |
| 5. Regression | ✅ PASS | |
| 6. Functional | ✅ PASS | |
| 7. End-to-End | ✅ PASS | |
| 8. Performance | ✅ PASS | |
| 9. Security | ✅ PASS | |
| 10. Acceptance | ✅ PASS | |

## GAPS REMEDIATED

- Total Gaps Found: [X]
- Total Gaps Fixed: [X]
- Remaining Issues: NONE

## CERTIFICATION

This system has been validated against the Gold Standard Development Framework
and is hereby certified as BATTLE-READY for production deployment.

---

Signature: ________________________
Date: ________________________
```

---

# PART 6: CRITICAL REMINDERS

## DO's

✅ Follow the verification layers in order (1→10)
✅ Document every gap before fixing
✅ Verify every fix before moving on
✅ Update documentation as code changes
✅ Commit frequently with meaningful messages
✅ Ask for clarification when uncertain
✅ Produce all required reports

## DON'Ts

❌ Skip verification layers
❌ Mark issues fixed without testing
❌ Proceed past failed gates
❌ Make undocumented changes
❌ Ignore "minor" issues
❌ Assume something works without verifying
❌ Leave gaps unresolved

## The Three Absolutes (NEVER VIOLATE)

1. **ACCURACY OVER SPEED** - Take time to do it right
2. **MODULARITY IS LAW** - Respect boundaries
3. **VERIFICATION IS CONTINUOUS** - Test everything

---

# PART 7: AUTHORIZATION

## Directive Authority

This directive is issued under the authority of the Gold Standard Development Framework as established and maintained by the Principal.

## Scope of Authority

Cursor is authorized to:
- Access and modify code in CIA-SIE-PURE and MERCURY repositories
- Install dependencies as needed
- Run tests and verification tools
- Create and modify documentation
- Make code changes to remediate gaps
- Produce certification reports

## Constraints

Cursor must NOT:
- Deploy to production without explicit approval
- Delete critical data or configurations
- Disable security features
- Skip mandatory verification steps
- Certify systems that have failed verification

---

# EXECUTION BEGINS

**Cursor: You are hereby directed to execute this Gold Standard Battle-Ready Validation for CIA-SIE-PURE and MERCURY.**

**Begin with Phase A: Environment Setup.**

**Report back when Phase A is complete, then await confirmation to proceed.**

---

*CURSOR GOLD STANDARD BATTLE-READY DIRECTIVE v1.0*
*Issued: January 15, 2026*
*Authority: Gold Standard Development Framework*
*Principal: Neville Mehta*
