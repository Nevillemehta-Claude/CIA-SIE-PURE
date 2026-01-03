# CURSOR VALIDATION INSTRUCTIONS
## CIA-SIE Gold Standard 15-Layer Validation Protocol

**Version:** 1.0
**Effective Date:** January 2026
**Predecessor:** CURSOR_REMEDIATION_INSTRUCTIONS.md (Phase 2)
**Successor:** CURSOR_ARCHITECTURE_GENERATION_DIRECTIVE.md (Phase 4)
**Source Framework:** GOLD_STANDARD_VALIDATION_PROTOCOL_v2.0_GENERIC.md

---

## EXECUTIVE SUMMARY

This document provides Cursor with complete, autonomous instructions to execute the 15-Layer Validation Protocol on the remediated CIA-SIE codebase. Upon successful completion, the codebase will receive certification at Bronze, Silver, Gold, or Platinum level, establishing it as a verified baseline for development.

---

## PART I: VALIDATION PHILOSOPHY

### 1.1 Purpose of Validation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VALIDATION vs AUDIT                                  │
│                                                                              │
│   AUDIT (Phase 1):   "What is wrong?"      → Identifies gaps                │
│   REMEDIATION (Phase 2): "Fix what's wrong" → Closes gaps                   │
│   VALIDATION (Phase 3): "Prove it's right"  → Certifies quality             │
│                                                                              │
│   Validation provides EVIDENCE that the system meets Gold Standard.         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Certification Levels

| Level | Requirements | Meaning |
|-------|--------------|---------|
| **PLATINUM** | 100% all layers | Exemplary - exceeds all standards |
| **GOLD** | 95%+ critical layers, 90%+ all layers | Full compliance - production ready |
| **SILVER** | 90%+ critical layers, 80%+ all layers | Substantial compliance - minor gaps |
| **BRONZE** | 80%+ critical layers, 70%+ all layers | Basic compliance - acceptable baseline |
| **FAILED** | Below Bronze thresholds | Not certified - return to Phase 2 |

### 1.3 Critical vs Standard Layers

**Critical Layers (must meet higher threshold):**
- Layer 4: Constitutional Compliance
- Layer 7: Security Validation
- Layer 10: Integration Integrity
- Layer 13: Error Handling

**Standard Layers (meet base threshold):**
- All other layers

### 1.4 Constitutional Override

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CONSTITUTIONAL VIOLATION = AUTOMATIC FAILURE                                 │
│                                                                              │
│ Regardless of scores on other layers, ANY constitutional violation          │
│ results in certification FAILURE. No exceptions. No waivers.                │
│                                                                              │
│ Constitutional Rules:                                                        │
│   1. Decision-Support ONLY (never decision-making)                          │
│   2. Expose Contradictions, NEVER Resolve                                   │
│   3. Descriptive AI, NOT Prescriptive                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PART II: THE 15 VALIDATION LAYERS

### Layer Map Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         15-LAYER VALIDATION PYRAMID                          │
│                                                                              │
│                            ┌─────────────┐                                  │
│                            │   LAYER 15  │  Certification                   │
│                            │  READINESS  │                                  │
│                            └──────┬──────┘                                  │
│                       ┌───────────┴───────────┐                             │
│                       │    LAYERS 13-14       │  Performance                │
│                       │  Error + Resilience   │                             │
│                       └───────────┬───────────┘                             │
│                  ┌────────────────┴────────────────┐                        │
│                  │       LAYERS 10-12              │  Integration           │
│                  │  Integrity + E2E + Contracts    │                        │
│                  └────────────────┬────────────────┘                        │
│             ┌─────────────────────┴─────────────────────┐                   │
│             │           LAYERS 7-9                      │  Security         │
│             │  Security + Auth + Data Protection        │                   │
│             └─────────────────────┬─────────────────────┘                   │
│        ┌──────────────────────────┴──────────────────────────┐              │
│        │               LAYERS 4-6                            │  Functional  │
│        │  Constitutional + Business Logic + API              │              │
│        └──────────────────────────┬──────────────────────────┘              │
│   ┌───────────────────────────────┴───────────────────────────────┐         │
│   │                    LAYERS 1-3                                 │ Struct  │
│   │  Repository Structure + Code Quality + Documentation         │         │
│   └───────────────────────────────────────────────────────────────┘         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PART III: LAYER SPECIFICATIONS

### LAYER 1: Repository Structure Validation

**Category:** Structural
**Weight:** Standard
**Pass Threshold:** 70%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L1.01 | Directory structure follows convention | Inspect tree | src/, tests/, docs/ present |
| L1.02 | No orphan files in root | List root files | Only config files in root |
| L1.03 | Test mirrors source structure | Compare paths | tests/unit/ mirrors src/ |
| L1.04 | Configuration files present | File exists | pyproject.toml, .gitignore exist |
| L1.05 | No build artifacts committed | Check .gitignore | __pycache__, .pyc excluded |
| L1.06 | CI/CD configuration valid | Parse YAML | .github/workflows/ valid |
| L1.07 | Environment template exists | File exists | .env.example present |
| L1.08 | README exists and non-empty | Read file | README.md > 100 chars |

#### Validation Commands:

```bash
# L1.01: Directory structure
ls -la src/ tests/ docs/

# L1.04: Config files
test -f pyproject.toml && test -f .gitignore && echo "PASS" || echo "FAIL"

# L1.06: CI validation
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
```

---

### LAYER 2: Code Quality Validation

**Category:** Structural
**Weight:** Standard
**Pass Threshold:** 70%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L2.01 | Linting passes | ruff check | Zero errors |
| L2.02 | Formatting consistent | ruff format --check | Zero changes needed |
| L2.03 | No unused imports | ruff check --select F401 | Zero unused imports |
| L2.04 | No unused variables | ruff check --select F841 | Zero unused variables |
| L2.05 | Type hints present | Spot check | >80% functions typed |
| L2.06 | No TODO/FIXME in production | grep | Zero in src/ |
| L2.07 | Complexity acceptable | radon cc | No function > 15 CC |
| L2.08 | Line length compliant | ruff | No lines > 120 chars |

#### Validation Commands:

```bash
# L2.01-L2.04: Linting
ruff check src/cia_sie --output-format=json

# L2.02: Formatting
ruff format --check src/cia_sie

# L2.06: No TODOs
grep -rn "TODO\|FIXME" src/cia_sie && echo "FAIL" || echo "PASS"
```

---

### LAYER 3: Documentation Validation

**Category:** Structural
**Weight:** Standard
**Pass Threshold:** 70%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L3.01 | Module docstrings present | AST parse | All modules have docstrings |
| L3.02 | Public function docstrings | AST parse | >80% public functions documented |
| L3.03 | API documentation exists | File check | docs/ contains API docs |
| L3.04 | README accurate | Content review | Matches current functionality |
| L3.05 | CHANGELOG maintained | File check | CHANGELOG.md exists and current |
| L3.06 | Configuration documented | Content review | All settings explained |
| L3.07 | Error codes documented | Content review | All exceptions listed |
| L3.08 | Architecture docs exist | File check | Flowcharts present |

---

### LAYER 4: Constitutional Compliance Validation (CRITICAL)

**Category:** Functional
**Weight:** CRITICAL
**Pass Threshold:** 100% (no tolerance)

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L4.01 | No trade execution logic | grep + AST | Zero execution functions |
| L4.02 | No order placement logic | grep + AST | Zero order functions |
| L4.03 | No contradiction resolution | grep + AST | Zero resolution logic |
| L4.04 | No signal aggregation | grep + AST | Zero aggregation functions |
| L4.05 | No weighted scoring | grep + AST | Zero weight calculations |
| L4.06 | No prescriptive language | grep AI outputs | Zero should/recommend/suggest |
| L4.07 | Disclaimers present | grep AI outputs | All outputs have disclaimer |
| L4.08 | Prohibited columns absent | grep models | Zero weight/score/confidence columns |
| L4.09 | Equal signal display | UI inspection | No visual bias |
| L4.10 | Contradiction exposure | Functional test | Contradictions shown, not resolved |

#### Validation Commands:

```bash
# L4.01-L4.02: No execution logic
grep -rn "execute_trade\|place_order\|submit_order" src/cia_sie
# Expected: No matches

# L4.03-L4.05: No resolution/aggregation
grep -rn "resolve_contradiction\|aggregate_signal\|weighted_average" src/cia_sie
# Expected: No matches

# L4.06: No prescriptive language
grep -rn '".*should.*"\|".*recommend.*"\|".*suggest.*"' src/cia_sie/ai/
# Expected: Only in filtering code

# L4.08: Prohibited columns
grep -rn "weight\s*=\|score\s*=\|confidence\s*=" src/cia_sie/dal/models.py
# Expected: No matches
```

#### Constitutional Test Suite:

```python
# tests/unit/test_constitutional_compliance.py

def test_no_execution_logic():
    """Verify no trade execution code exists."""
    # Scan all source files for prohibited patterns
    assert count_matches("execute_trade") == 0
    assert count_matches("place_order") == 0

def test_contradictions_not_resolved():
    """Verify contradictions are exposed, not resolved."""
    contradiction = create_test_contradiction()
    result = exposure_engine.process(contradiction)
    assert result.resolution is None
    assert result.signal_a is not None
    assert result.signal_b is not None

def test_ai_output_is_descriptive():
    """Verify AI outputs contain no prescriptive language."""
    narrative = generate_test_narrative()
    assert "should" not in narrative.lower()
    assert "recommend" not in narrative.lower()
    assert "suggest" not in narrative.lower()
    assert DISCLAIMER in narrative
```

---

### LAYER 5: Business Logic Validation

**Category:** Functional
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L5.01 | Signal ingestion works | Integration test | Webhook creates signal |
| L5.02 | Signal normalization correct | Unit test | Values normalized properly |
| L5.03 | Contradiction detection works | Unit test | Contradictions detected |
| L5.04 | Confirmation detection works | Unit test | Confirmations detected |
| L5.05 | Freshness calculation correct | Unit test | Status matches time delta |
| L5.06 | Narrative generation works | Integration test | Narrative returned |
| L5.07 | Kite OAuth flow works | Integration test | Token exchange succeeds |
| L5.08 | Instrument CRUD works | Integration test | All operations succeed |

---

### LAYER 6: API Contract Validation

**Category:** Functional
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L6.01 | OpenAPI spec valid | Schema validation | Spec parses correctly |
| L6.02 | Endpoints match spec | Compare | All routes in spec |
| L6.03 | Request schemas enforced | Test invalid input | 422 returned |
| L6.04 | Response schemas match | Compare responses | Match spec exactly |
| L6.05 | Error responses consistent | Test errors | Standard error format |
| L6.06 | Pagination implemented | Test list endpoints | Pagination works |
| L6.07 | Versioning correct | Check paths | /api/v1/ prefix |
| L6.08 | CORS configured | Check headers | Appropriate origins |

---

### LAYER 7: Security Validation (CRITICAL)

**Category:** Security
**Weight:** CRITICAL
**Pass Threshold:** 95%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L7.01 | No SQL injection | Bandit + manual | Zero SQLi vulnerabilities |
| L7.02 | No XSS vulnerabilities | Bandit + manual | Zero XSS vulnerabilities |
| L7.03 | No hardcoded secrets | grep + git-secrets | Zero secrets in code |
| L7.04 | Dependencies secure | pip-audit | Zero critical CVEs |
| L7.05 | Input validation present | Code review | All inputs validated |
| L7.06 | Output encoding correct | Code review | All outputs encoded |
| L7.07 | HTTPS enforced | Config review | HTTP redirects to HTTPS |
| L7.08 | Security headers present | Response check | All headers set |
| L7.09 | Rate limiting configured | Config review | Limits defined |
| L7.10 | Logging sanitized | Code review | No secrets logged |

#### Validation Commands:

```bash
# L7.01-L7.02: Security scan
bandit -r src/cia_sie -f json -o bandit-report.json
bandit -r src/cia_sie -ll  # Show only medium+ severity

# L7.03: Secret detection
grep -rn "password\s*=\|api_key\s*=\|secret\s*=" src/cia_sie
# Exclude: os.environ.get patterns

# L7.04: Dependency vulnerabilities
pip-audit --strict
```

---

### LAYER 8: Authentication Validation

**Category:** Security
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L8.01 | Auth required on protected routes | Test without token | 401 returned |
| L8.02 | Token validation works | Test invalid token | 401 returned |
| L8.03 | Token expiry enforced | Test expired token | 401 returned |
| L8.04 | Refresh flow works | Test refresh | New token issued |
| L8.05 | Logout invalidates token | Test after logout | 401 returned |
| L8.06 | OAuth state validated | Test wrong state | Auth rejected |
| L8.07 | Secure cookie settings | Check config | HttpOnly, Secure, SameSite |
| L8.08 | Session management correct | Test sessions | Proper lifecycle |

---

### LAYER 9: Data Protection Validation

**Category:** Security
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L9.01 | Sensitive data encrypted | Code review | Encryption at rest |
| L9.02 | PII handled correctly | Data audit | Minimal PII, protected |
| L9.03 | Backup procedures exist | Doc review | Backup strategy defined |
| L9.04 | Data retention defined | Doc review | Retention policy exists |
| L9.05 | Access logging enabled | Code review | Access events logged |
| L9.06 | Database secured | Config review | Auth required |
| L9.07 | Migrations reversible | Test rollback | Rollback succeeds |
| L9.08 | No data leakage | API review | No sensitive data in errors |

---

### LAYER 10: Integration Integrity Validation (CRITICAL)

**Category:** Integration
**Weight:** CRITICAL
**Pass Threshold:** 95%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L10.01 | Database connection works | Integration test | Connection succeeds |
| L10.02 | Migrations apply cleanly | Run migrations | Zero errors |
| L10.03 | Claude API integration works | Integration test | Response received |
| L10.04 | Kite API integration works | Integration test | Auth succeeds |
| L10.05 | Webhook ingestion works | End-to-end test | Signal created |
| L10.06 | Component boundaries respected | Code review | Clean interfaces |
| L10.07 | Async operations correct | Code review | Proper await usage |
| L10.08 | Resource cleanup works | Test + review | No leaks |

---

### LAYER 11: End-to-End Validation

**Category:** Integration
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L11.01 | Full user journey works | E2E test | Complete flow succeeds |
| L11.02 | Signal → Display flow | E2E test | Signal visible in UI |
| L11.03 | Contradiction → Alert flow | E2E test | Alert shown |
| L11.04 | Narrative generation flow | E2E test | Narrative displayed |
| L11.05 | Kite import flow | E2E test | Instruments imported |
| L11.06 | Settings persistence | E2E test | Settings saved |
| L11.07 | Error recovery flow | E2E test | Graceful recovery |
| L11.08 | Multi-user isolation | E2E test | Data isolated |

---

### LAYER 12: Contract Testing Validation

**Category:** Integration
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L12.01 | API contracts honored | Contract tests | All contracts pass |
| L12.02 | External API mocks valid | Mock validation | Mocks match reality |
| L12.03 | Schema evolution safe | Compare schemas | Backward compatible |
| L12.04 | Version compatibility | Version tests | Supported versions work |
| L12.05 | Feature flags work | Flag tests | Flags toggle correctly |
| L12.06 | Deprecation warnings | API review | Deprecated items marked |
| L12.07 | Breaking changes documented | Doc review | Changes listed |
| L12.08 | Client compatibility | Compatibility tests | Clients still work |

---

### LAYER 13: Error Handling Validation (CRITICAL)

**Category:** Performance
**Weight:** CRITICAL
**Pass Threshold:** 95%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L13.01 | All errors caught | Code review | No unhandled exceptions |
| L13.02 | Error logging complete | Log review | All errors logged |
| L13.03 | Error responses correct | Test errors | Standard format returned |
| L13.04 | Graceful degradation works | Chaos test | System stays up |
| L13.05 | Circuit breakers work | Load test | Breakers trip correctly |
| L13.06 | Retry logic correct | Failure test | Retries with backoff |
| L13.07 | Timeout handling works | Timeout test | Timeouts handled |
| L13.08 | Resource exhaustion handled | Stress test | OOM prevented |
| L13.09 | Error recovery works | Recovery test | System recovers |
| L13.10 | Error notifications work | Alert test | Alerts sent |

---

### LAYER 14: Resilience Validation

**Category:** Performance
**Weight:** Standard
**Pass Threshold:** 80%

#### Validation Checks:

| Check ID | Description | Method | Pass Criteria |
|----------|-------------|--------|---------------|
| L14.01 | Load test passes | Load test | Handles expected load |
| L14.02 | Stress test passes | Stress test | Degrades gracefully |
| L14.03 | Spike test passes | Spike test | Handles traffic spikes |
| L14.04 | Soak test passes | Soak test | Stable over time |
| L14.05 | Database performance | Query analysis | Queries optimized |
| L14.06 | API response time | Benchmark | P95 < threshold |
| L14.07 | Memory usage stable | Monitor | No memory leaks |
| L14.08 | CPU usage acceptable | Monitor | CPU not saturated |

---

### LAYER 15: Certification Readiness

**Category:** Certification
**Weight:** Final Gate
**Pass Threshold:** Based on overall scores

#### Certification Calculation:

```python
def calculate_certification(layer_scores: dict) -> str:
    """Calculate certification level based on layer scores."""

    critical_layers = [4, 7, 10, 13]
    standard_layers = [1, 2, 3, 5, 6, 8, 9, 11, 12, 14]

    # Constitutional check - automatic fail
    if layer_scores[4] < 100:
        return "FAILED - Constitutional violation"

    critical_avg = sum(layer_scores[l] for l in critical_layers) / len(critical_layers)
    all_avg = sum(layer_scores.values()) / len(layer_scores)

    if critical_avg >= 100 and all_avg >= 100:
        return "PLATINUM"
    elif critical_avg >= 95 and all_avg >= 90:
        return "GOLD"
    elif critical_avg >= 90 and all_avg >= 80:
        return "SILVER"
    elif critical_avg >= 80 and all_avg >= 70:
        return "BRONZE"
    else:
        return "FAILED"
```

---

## PART IV: VALIDATION EXECUTION PROTOCOL

### 4.1 Initialization

Upon receiving this document, Cursor shall:

```
1. Output: "GOLD STANDARD VALIDATION INITIATED"

2. Verify prerequisites:
   - PHASE_9C gaps: Zero CRITICAL/HIGH remaining
   - REMEDIATION_LOG.md: Complete
   - Tests: All passing

3. Create validation report file:
   handoff/VALIDATION_REPORT.md

4. Begin layer-by-layer validation
```

### 4.2 Per-Layer Execution

For EACH layer (1-15):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: ANNOUNCE                                                             │
│ Output: "Validating Layer N: [Layer Name]"                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: EXECUTE CHECKS                                                       │
│ Run all checks for this layer (L#.01 through L#.XX)                         │
│ Record PASS/FAIL for each check                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: CALCULATE SCORE                                                      │
│ Score = (Passed Checks / Total Checks) × 100                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: RECORD RESULTS                                                       │
│ Log to VALIDATION_REPORT.md                                                 │
│ Output: "Layer N: [PASS/FAIL] - Score: XX%"                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: GATE CHECK (Critical Layers Only)                                    │
│ IF critical layer < threshold:                                              │
│   Output: "CRITICAL LAYER FAILED - Validation cannot continue"              │
│   Abort validation                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Layer 4 Special Handling

Layer 4 (Constitutional Compliance) requires additional checks:

```
IF Layer 4 score < 100%:
    1. IMMEDIATELY STOP validation
    2. Output: "CONSTITUTIONAL VIOLATION DETECTED"
    3. List all failing checks
    4. Output: "VALIDATION FAILED - Return to Phase 2 Remediation"
    5. Create CONSTITUTIONAL_VIOLATION_REPORT.md
    6. EXIT with failure status
```

---

## PART V: VALIDATION REPORT FORMAT

### 5.1 Report Structure

Create `handoff/VALIDATION_REPORT.md`:

```markdown
# CIA-SIE VALIDATION REPORT
## Gold Standard 15-Layer Validation

**Validation Date:** [timestamp]
**Validator:** Cursor (Automated)
**Codebase Version:** [git commit hash]
**Previous Phase:** Remediation (Phase 2)

---

## CERTIFICATION RESULT

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    CERTIFICATION: [LEVEL]                     ║
║                                                               ║
║   Critical Layer Average: XX%                                 ║
║   Overall Average: XX%                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## LAYER SUMMARY

| Layer | Name | Category | Weight | Score | Status |
|-------|------|----------|--------|-------|--------|
| 1 | Repository Structure | Structural | Standard | XX% | PASS/FAIL |
| 2 | Code Quality | Structural | Standard | XX% | PASS/FAIL |
| 3 | Documentation | Structural | Standard | XX% | PASS/FAIL |
| 4 | Constitutional Compliance | Functional | CRITICAL | XX% | PASS/FAIL |
| 5 | Business Logic | Functional | Standard | XX% | PASS/FAIL |
| 6 | API Contract | Functional | Standard | XX% | PASS/FAIL |
| 7 | Security | Security | CRITICAL | XX% | PASS/FAIL |
| 8 | Authentication | Security | Standard | XX% | PASS/FAIL |
| 9 | Data Protection | Security | Standard | XX% | PASS/FAIL |
| 10 | Integration Integrity | Integration | CRITICAL | XX% | PASS/FAIL |
| 11 | End-to-End | Integration | Standard | XX% | PASS/FAIL |
| 12 | Contract Testing | Integration | Standard | XX% | PASS/FAIL |
| 13 | Error Handling | Performance | CRITICAL | XX% | PASS/FAIL |
| 14 | Resilience | Performance | Standard | XX% | PASS/FAIL |
| 15 | Certification Readiness | Certification | Final | XX% | PASS/FAIL |

---

## DETAILED RESULTS

### Layer 1: Repository Structure

| Check | Description | Result | Evidence |
|-------|-------------|--------|----------|
| L1.01 | Directory structure | PASS | src/, tests/, docs/ present |
| L1.02 | No orphan files | PASS | Only config in root |
| ... | ... | ... | ... |

**Layer Score:** XX% (X/Y checks passed)

---

[Repeat for all 15 layers]

---

## ISSUES FOUND

### Critical Issues (Block Certification)
[List any issues that block certification]

### Warnings (Do Not Block)
[List any warnings that should be addressed]

---

## RECOMMENDATIONS

1. [Recommendation 1]
2. [Recommendation 2]
...

---

## NEXT STEPS

Based on certification level:
- PLATINUM/GOLD: Proceed to Phase 4 (Architecture Generation)
- SILVER: Proceed with caution, address warnings
- BRONZE: Proceed but prioritize improvements
- FAILED: Return to Phase 2 (Remediation)
```

---

## PART VI: AUTONOMOUS EXECUTION DIRECTIVE

### 6.1 Execution Command

Upon receiving this document, Cursor shall:

```
1. Output: "GOLD STANDARD VALIDATION INITIATED"
   Output: "Protocol: 15-Layer Validation"
   Output: "Target: CIA-SIE Codebase"

2. Verify prerequisites:
   □ REMEDIATION_LOG.md exists and shows all CRITICAL/HIGH fixed
   □ All tests passing
   □ No uncommitted changes

3. Create handoff/VALIDATION_REPORT.md with header

4. Execute Layer 1 validation
   - Run all L1.XX checks
   - Calculate score
   - Log results
   - Output: "Layer 1: Repository Structure - XX%"

5. Execute Layer 2 validation
   [repeat pattern]

6. SPECIAL: Layer 4 (Constitutional)
   - Run all L4.XX checks
   - IF any check fails:
     - STOP immediately
     - Output: "CONSTITUTIONAL VIOLATION - VALIDATION FAILED"
     - Exit with failure
   - ELSE continue

7. Execute Layers 5-15
   [repeat pattern]

8. Calculate certification level

9. Complete VALIDATION_REPORT.md

10. Output:
    "═══════════════════════════════════════"
    "VALIDATION COMPLETE"
    "Certification Level: [LEVEL]"
    "Critical Average: XX%"
    "Overall Average: XX%"
    "═══════════════════════════════════════"

11. IF certification >= BRONZE:
    Output: "Proceed to Phase 4: Architecture Generation"
    ELSE:
    Output: "FAILED - Return to Phase 2: Remediation"

12. Commit: "Complete Phase 3 validation - [LEVEL] certified"
```

### 6.2 Conditional Flows

```
IF Layer 4 < 100%:
    ABORT with constitutional failure
    DO NOT continue to other layers

IF any CRITICAL layer < threshold:
    COMPLETE all layers for documentation
    BUT certification = FAILED

IF overall < BRONZE:
    Document all findings
    Recommend specific remediations
    Return to Phase 2
```

---

## PART VII: COMPLETION CHECKLIST

Before declaring Phase 3 complete:

```
□ All 15 layers validated
□ Layer 4 (Constitutional): 100%
□ All CRITICAL layers: >= threshold for target level
□ VALIDATION_REPORT.md: Complete
□ Certification level: >= BRONZE
□ Commit: Pushed with certification level
□ Ready for: Phase 4 (Architecture Generation)
```

---

## APPENDIX: VALIDATION TEST COMMANDS

### Quick Validation Script

```bash
#!/bin/bash
# quick_validate.sh

echo "=== Layer 2: Code Quality ==="
ruff check src/cia_sie
ruff format --check src/cia_sie

echo "=== Layer 4: Constitutional ==="
echo "Checking for prohibited columns..."
grep -rn "weight\s*=\|score\s*=\|confidence\s*=" src/cia_sie/dal/models.py && echo "FAIL" || echo "PASS"

echo "Checking for prescriptive language..."
grep -rn '".*should.*"\|".*recommend.*"' src/cia_sie/ai/ && echo "FAIL" || echo "PASS"

echo "=== Layer 7: Security ==="
bandit -r src/cia_sie -ll

echo "=== Layer 10: Integration ==="
python -m pytest tests/integration/ -v

echo "=== Overall ==="
python -m pytest tests/ --cov=src/cia_sie --cov-report=term-missing
```

---

**END OF CURSOR_VALIDATION_INSTRUCTIONS.md**

*This document governs Phase 3 of the CIA-SIE Gold Standard Development Lifecycle.*
