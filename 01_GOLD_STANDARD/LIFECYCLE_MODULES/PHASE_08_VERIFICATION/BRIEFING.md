# PHASE 08: VERIFICATION
## Briefing Document

**Phase Number:** 8
**Phase Name:** Verification
**Purpose:** Prove the system works as specified

---

## WHAT THIS PHASE IS

Verification is the comprehensive validation phase where the integrated system is proven to work correctly, securely, and performantly. This is not "testing after development" - this is the systematic proof that requirements have been satisfied.

**Key Insight:** Verification is not about finding bugs. It's about generating evidence that the system meets its requirements.

---

## WHAT YOU'RE DOING

1. **Executing the full test pyramid** (unit → integration → E2E)
2. **Conducting performance testing** against defined benchmarks
3. **Conducting security testing** against known threats
4. **Verifying requirements traceability** (every requirement has implementation)
5. **Obtaining user acceptance** (stakeholder sign-off)
6. **Documenting all evidence** (test reports, coverage reports)

---

## WHAT YOU'RE NOT DOING

- Writing new features (that was Phase 6)
- Integrating components (that was Phase 7)
- Creating documentation (that's Phase 9)
- Deploying (that's Phase 10)

**If verification reveals issues, return to the appropriate phase to fix.**

---

## VERIFICATION LAYERS

From VERIFICATION_DOCTRINE:

| Layer | Question | Phase 8 Responsibility |
|-------|----------|------------------------|
| Unit | Does each function work? | Verify coverage |
| Contract | Do interfaces honor contracts? | Run contract tests |
| Integration | Do components work together? | Run integration suite |
| Functional | Do features work as specified? | Run functional tests |
| Performance | Does it meet speed requirements? | Run performance tests |
| Security | Is it secure against threats? | Run security tests |
| Acceptance | Does it satisfy the user need? | Conduct UAT |

---

## KEY DELIVERABLES

| Deliverable | Purpose |
|-------------|---------|
| Test Execution Report | Proof all tests pass |
| Coverage Report | Proof coverage targets met |
| Performance Test Results | Proof performance targets met |
| Security Audit Report | Proof security verified |
| Requirements Traceability Matrix | Proof all requirements implemented |
| UAT Sign-off | Stakeholder acceptance |

---

## COVERAGE TARGETS

| Test Type | Target |
|-----------|--------|
| Unit Test Coverage | >90% |
| Integration Test Coverage | >80% |
| E2E Critical Paths | 100% |
| Error Path Coverage | >80% |
| Security Test Coverage | All OWASP Top 10 |

---

## PERFORMANCE TARGETS

Verify against defined benchmarks:

| Metric | Typical Target |
|--------|----------------|
| API Response Time (p95) | < 200ms |
| API Response Time (p99) | < 500ms |
| Page Load Time | < 3s |
| Database Query Time | < 100ms |
| Error Rate | < 0.1% |

---

## SECURITY VERIFICATION

Minimum security verification:

- [ ] No critical/high vulnerabilities in dependency scan
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication bypass testing passed
- [ ] Authorization testing passed
- [ ] Secrets scan passed (no hardcoded credentials)

---

## COMMON PITFALLS

### 1. Verification as Afterthought
**Problem:** "We'll test what we can before release"
**Fix:** Verification has defined scope and targets; it's not optional

### 2. Only Happy Path Testing
**Problem:** Only testing when everything works
**Fix:** Test error paths, edge cases, failure modes

### 3. No Evidence Trail
**Problem:** "We tested it, trust us"
**Fix:** Generate reports, capture evidence

### 4. Skipping UAT
**Problem:** "It passes automated tests, ship it"
**Fix:** Stakeholder review is required for acceptance

---

## EXIT CRITERIA SUMMARY

- [ ] All tests passing
- [ ] Coverage targets met
- [ ] Performance targets met
- [ ] Security audit passed
- [ ] RTM complete (all requirements traced)
- [ ] UAT approved

---

## NEXT STEPS

After completing this phase:
1. Generate all reports and evidence
2. Obtain stakeholder sign-off
3. Proceed to Phase 9: Documentation
4. Load `LIFECYCLE_MODULES/PHASE_09_DOCUMENTATION/`

---

*PHASE 08 BRIEFING v1.0 | LIFECYCLE_MODULES | Gold Standard System*
