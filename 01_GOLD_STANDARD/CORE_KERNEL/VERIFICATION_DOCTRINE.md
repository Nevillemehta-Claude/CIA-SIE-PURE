# VERIFICATION DOCTRINE
## The Architecture of Certainty

**Classification:** CORE_KERNEL (Immutable)
**Version:** 1.0
**Applicability:** Universal - All Development, All Phases

---

## FOUNDATIONAL TRUTH

> Testing is not a phase. It is a constant companion to every action.

Verification is not something you do at the end. It is something you do at every step. The absence of verification at any layer invalidates all layers above it.

---

## THE VERIFICATION PYRAMID

```
                         /\
                        /  \
                       / AC \         ACCEPTANCE
                      / CEP  \        Does it satisfy the need?
                     / TANCE  \
                    /──────────\
                   /            \
                  /  SYSTEM      \    SYSTEM
                 /  VERIFICATION  \   Does the whole work?
                /──────────────────\
               /                    \
              /    INTEGRATION       \    INTEGRATION
             /     VERIFICATION       \   Do parts work together?
            /──────────────────────────\
           /                            \
          /      COMPONENT               \    COMPONENT
         /      VERIFICATION              \   Does this unit work?
        /──────────────────────────────────\
       /                                    \
      /          UNIT VERIFICATION           \    UNIT
     /          (Functions, Methods)          \   Does this function work?
    /──────────────────────────────────────────\
   /                                            \
  /            SYNTAX VERIFICATION               \    SYNTAX
 /            (Compilation, Parsing)              \   Is it valid code?
/──────────────────────────────────────────────────\
```

**LAW:** You cannot claim a higher layer is verified if a lower layer is not.

---

## THE TEN VERIFICATION LAYERS

### LAYER 1: SYNTAX
**Question:** Does the code compile/parse without errors?
**When:** Every file save
**Method:** Compiler, linter, parser
**Failure Response:** Cannot proceed until syntax is valid

---

### LAYER 2: STATIC ANALYSIS
**Question:** Does the code follow quality rules?
**When:** Before commit
**Method:** Linters, static analyzers, type checkers
**Failure Response:** Fix violations before proceeding

---

### LAYER 3: UNIT
**Question:** Does this function do what it claims?
**When:** After every function is written
**Method:** Unit tests with assertions
**Failure Response:** Fix function or fix test; do not proceed

---

### LAYER 4: CONTRACT
**Question:** Does this component honor its interface?
**When:** After component boundary is defined
**Method:** Contract tests, interface validation
**Failure Response:** Interface or implementation must align

---

### LAYER 5: INTEGRATION
**Question:** Do connected components communicate correctly?
**When:** After connecting components
**Method:** Integration tests
**Failure Response:** Fix integration point before adding more connections

---

### LAYER 6: FUNCTIONAL
**Question:** Does the feature work as specified?
**When:** After feature is complete
**Method:** Feature tests against specification
**Failure Response:** Implementation or specification must be corrected

---

### LAYER 7: REGRESSION
**Question:** Did new code break old functionality?
**When:** After every change
**Method:** Full test suite execution
**Failure Response:** Fix regression before merging

---

### LAYER 8: PERFORMANCE
**Question:** Does it meet speed/resource requirements?
**When:** At system level, before deployment
**Method:** Load tests, profiling, benchmarks
**Failure Response:** Optimize or revise requirements

---

### LAYER 9: SECURITY
**Question:** Is the system secure against threats?
**When:** Before deployment, after changes
**Method:** Security scans, penetration tests, audits
**Failure Response:** Remediate vulnerabilities before release

---

### LAYER 10: ACCEPTANCE
**Question:** Does it satisfy the original need?
**When:** Before release to production
**Method:** User acceptance testing, stakeholder review
**Failure Response:** Revise until acceptance criteria met

---

## VERIFICATION BY PHASE

Each development phase has applicable verification layers:

| Phase | Applicable Layers |
|-------|-------------------|
| Ideation | None (conceptual) |
| Concept | Acceptance criteria defined |
| Requirements | Requirements verification |
| Architecture | Architecture review, security review |
| Specification | Specification completeness |
| Development | Syntax, Static, Unit, Contract |
| Integration | Integration, Functional |
| Testing | All layers validated |
| Documentation | Documentation accuracy |
| Deployment | Performance, Security, Acceptance |
| Operations | Continuous monitoring |

---

## THE ENTRY-EXIT GATE PATTERN

Every phase has verification gates:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ENTRY GATE                                         │
│  "What must be verified before I can start?"        │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │                                             │   │
│  │          PHASE EXECUTION                    │   │
│  │          (Work happens here)                │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  IN-PHASE VERIFICATION                              │
│  "What must I verify as I work?"                    │
│                                                     │
│  EXIT GATE                                          │
│  "What must be verified before I can leave?"        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Example: Development Phase

**ENTRY CRITERIA (must be GREEN):**
- [ ] Architecture design verified and approved
- [ ] Specifications complete and reviewed
- [ ] API contracts defined and validated
- [ ] Test strategy documented

**IN-PHASE VERIFICATION:**
| Action | Verification Required |
|--------|----------------------|
| Write function | Unit test before proceeding |
| Complete module | Run all module tests |
| Define interface | Contract test |
| Commit code | Full regression suite |

**EXIT CRITERIA (must be GREEN):**
- [ ] All unit tests passing (100%)
- [ ] Code coverage meets threshold
- [ ] Contract tests verified
- [ ] No regression failures
- [ ] Code review approved

---

## THE FIX-VERIFY CYCLE

When verification fails:

```
┌──────────────┐
│  VERIFY      │
└──────┬───────┘
       │
       ▼
   ┌───────┐
   │ PASS? │──── YES ──── PROCEED
   └───┬───┘
       │
       NO
       │
       ▼
┌──────────────┐
│  DIAGNOSE    │◄─────────────────┐
│  (Root cause)│                  │
└──────┬───────┘                  │
       │                          │
       ▼                          │
┌──────────────┐                  │
│    FIX       │                  │
│  (At lowest  │                  │
│   layer)     │                  │
└──────┬───────┘                  │
       │                          │
       ▼                          │
┌──────────────┐                  │
│  RE-VERIFY   │                  │
│  (Same layer │                  │
│   + all      │                  │
│   below)     ├──── FAIL ────────┘
└──────┬───────┘
       │
       PASS
       │
       ▼
   PROCEED
```

**CRITICAL:** Never proceed without re-verification after a fix.

---

## VERIFICATION EVIDENCE STANDARDS

### Evidence Hierarchy

| Level | Type | Example | Acceptable For |
|-------|------|---------|----------------|
| 1 | Assertion | "It works" | Never |
| 2 | Reference | "See test file" | Tier 1-2 only |
| 3 | Citation | "Tests pass at commit abc123" | Tier 3 |
| 4 | Verified | "Coverage report attached, 94%" | Tier 4 |
| 5 | Formal | "Formal proof document" | Tier 5 |

### Citation Format

```
VERIFICATION EVIDENCE
Layer: Unit Testing
Status: PASS
Evidence: tests/unit/test_module.py - 47 tests, 100% pass
Coverage: 94.2% (report: coverage/htmlcov/index.html)
Commit: abc123def456
Timestamp: 2026-01-14T10:30:00Z
```

---

## VERIFICATION TOOLS BY LAYER

| Layer | Tools | Purpose |
|-------|-------|---------|
| Syntax | Compiler, Parser | Valid code structure |
| Static | ESLint, Pylint, TypeScript | Code quality rules |
| Unit | pytest, Jest, JUnit | Function-level testing |
| Contract | Pact, Dredd, Schemathesis | API contract validation |
| Integration | pytest, Cypress | Component interaction |
| Functional | Selenium, Playwright | Feature verification |
| Regression | CI/CD test suites | Change impact detection |
| Performance | k6, JMeter, Locust | Load and speed testing |
| Security | OWASP ZAP, Snyk, Bandit | Vulnerability detection |
| Acceptance | Manual + automated UAT | User need satisfaction |

---

## CONTINUOUS VERIFICATION

Verification is not a gate you pass once. It runs continuously.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   DEVELOPMENT                                       │
│   │                                                 │
│   ├── Save file ────► Syntax check                  │
│   ├── Write function ─► Unit test                   │
│   ├── Commit ────────► Pre-commit hooks             │
│   │                    - Lint                       │
│   │                    - Type check                 │
│   │                    - Unit tests                 │
│   │                                                 │
│   CI/CD PIPELINE                                    │
│   │                                                 │
│   ├── Push ──────────► Full test suite              │
│   ├── PR ────────────► Integration tests            │
│   │                    - Coverage report            │
│   │                    - Security scan              │
│   ├── Merge ─────────► Deployment tests             │
│   │                                                 │
│   PRODUCTION                                        │
│   │                                                 │
│   └── Continuous ────► Monitoring                   │
│                        - Health checks              │
│                        - Performance metrics        │
│                        - Error rates                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## VERIFICATION COVERAGE TARGETS

| Criticality | Unit | Integration | E2E | Security |
|-------------|------|-------------|-----|----------|
| Safety-Critical | 100% + MC/DC | 100% | Critical paths | Full audit |
| Business-Critical | >95% | >80% | Critical paths | Automated scan |
| Standard | >80% | >60% | Happy paths | Automated scan |
| Utility | >70% | >40% | None | Basic scan |

---

## THE CERTAINTY EQUATION

```
CERTAINTY = f(
    Layer Coverage,        ← All layers verified
    Evidence Quality,      ← Strong, not weak evidence
    Continuous Execution,  ← Not just once, but always
    Failure Response       ← Fix-verify cycles complete
)
```

**Maximum certainty requires ALL four components.**

---

## FAILURE PROTOCOL

When any verification fails:

1. **STOP** - Do not proceed to next activity
2. **DIAGNOSE** - Identify root cause at lowest applicable layer
3. **FIX** - Correct at the layer where failure originates
4. **RE-VERIFY** - Run verification at that layer AND all layers below
5. **PROCEED** - Only when all applicable layers are GREEN

**NEVER:**
- Skip a failing test
- Comment out assertions
- Mark "known failures" as acceptable
- Proceed with broken lower layers

---

## INTEGRATION WITH BIBLE MODULES

Each BIBLE_MODULE has:
```
MODULE/
└── VERIFICATION/
    ├── ENTRY_CRITERIA.md    ← What must be GREEN before using this module
    ├── SELF_VERIFICATION.md ← How to verify this module is correct
    └── EXIT_CRITERIA.md     ← What must be GREEN after applying this module
```

Each LIFECYCLE_MODULE has:
```
PHASE/
└── VERIFICATION/
    ├── APPLICABLE_LAYERS.md  ← Which layers apply in this phase
    ├── ENTRY_CRITERIA.md     ← Gates to enter this phase
    ├── IN_PHASE_CHECKS.md    ← Verification during the phase
    ├── EXIT_CRITERIA.md      ← Gates to exit this phase
    └── FAILURE_PROTOCOL.md   ← What to do when verification fails
```

---

## THE ULTIMATE TEST

> "Would I bet my career that this works?"

If the answer is not an unequivocal YES based on verification evidence, you are not done verifying.

---

*VERIFICATION DOCTRINE v1.0 | CORE_KERNEL | Gold Standard System*
