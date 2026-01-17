# PHASE 08: VERIFICATION
## Standards

**Purpose:** Quality standards for comprehensive system verification

---

## THE TEN VERIFICATION LAWS

Reference: BIBLE_MODULES/VERIFICATION/PRINCIPLES.md

1. **Verification is continuous** - Not a phase, a practice
2. **Requirements drive tests** - Every requirement has a test
3. **Automation is mandatory** - Manual testing doesn't scale
4. **Evidence is required** - If it's not recorded, it didn't happen
5. **Independence matters** - Testers separate from developers
6. **Early is cheaper** - Find bugs before they compound
7. **Coverage is measured** - Know what you're testing
8. **Regression is prevented** - Tests run on every change
9. **Environments match** - Test where you deploy
10. **Failure is information** - Failed tests guide improvement

---

## TEST PYRAMID STANDARDS

Reference: BIBLE_MODULES/VERIFICATION/TEST_PYRAMID.md

### Distribution Targets

| Level | Target % | Execution | Scope |
|-------|----------|-----------|-------|
| Unit | 50% | Milliseconds | Single function/class |
| Contract | 20% | Seconds | API boundaries |
| Integration | 20% | Seconds-Minutes | Component interaction |
| E2E | 10% | Minutes | Full user journey |

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Ice Cream Cone | Too many E2E, few unit | Invert the pyramid |
| Hourglass | Missing integration layer | Add contract tests |
| No Pyramid | Random distribution | Define test strategy |

---

## TEST COVERAGE STANDARDS

### Minimum Coverage Requirements

| Code Type | Line Coverage | Branch Coverage |
|-----------|---------------|-----------------|
| Business Logic | 80% | 70% |
| API Handlers | 75% | 65% |
| Data Access | 70% | 60% |
| Utilities | 60% | 50% |
| Configuration | 50% | N/A |

### Coverage Exclusions

May exclude from coverage metrics:
- Generated code
- Third-party integrations (mock instead)
- Dead code (should be removed)
- Trivial getters/setters

### Coverage Enforcement

| Environment | Enforcement |
|-------------|-------------|
| Local | Warning on decrease |
| PR/MR | Block if below threshold |
| Main branch | Block if below threshold |

---

## TEST NAMING STANDARDS

### Unit Test Naming

Format: `[MethodName]_[Scenario]_[ExpectedResult]`

Examples:
- `calculateTotal_withValidItems_returnsSumOfPrices`
- `validateEmail_withInvalidFormat_throwsValidationError`
- `getUserById_whenNotFound_returnsNull`

### Integration Test Naming

Format: `[Feature]_[Scenario]_[ExpectedBehavior]`

Examples:
- `OrderCreation_withValidPayment_createsOrderAndSendsConfirmation`
- `UserRegistration_withDuplicateEmail_returns409Conflict`

### E2E Test Naming

Format: `[UserJourney]_[Variant]`

Examples:
- `CheckoutFlow_happyPath`
- `CheckoutFlow_paymentDeclined`
- `UserOnboarding_withSocialLogin`

---

## TEST DATA STANDARDS

### Test Data Principles

| Principle | Description |
|-----------|-------------|
| Isolation | Tests don't share mutable state |
| Reproducibility | Same data produces same results |
| Minimalism | Only data needed for test |
| Realism | Data resembles production (sanitized) |
| Documentation | Test data is documented |

### Test Data Sources

| Source | Use For | Caution |
|--------|---------|---------|
| Factories | Unit tests | Keep simple |
| Fixtures | Integration tests | Version control |
| Snapshots | Regression tests | Review changes |
| Synthetic | Load tests | Match production patterns |
| Sanitized Prod | E2E tests | Never real PII |

### Forbidden in Test Data

- Real customer names, emails, addresses
- Real payment information
- Real credentials or secrets
- Production database copies (unsanitized)

---

## TEST ENVIRONMENT STANDARDS

### Environment Requirements

| Requirement | Standard |
|-------------|----------|
| Isolation | Tests don't affect each other |
| Reset | Can return to known state |
| Speed | Fast setup and teardown |
| Parity | Matches production configuration |
| Availability | Always available for testing |

### Environment Tiers

| Tier | Purpose | Data | Refresh |
|------|---------|------|---------|
| Local | Developer testing | Synthetic | On demand |
| CI | Automated testing | Synthetic | Per build |
| Integration | Integration testing | Synthetic | Daily |
| Staging | Pre-prod verification | Sanitized prod | Weekly |

---

## TEST AUTOMATION STANDARDS

### Automation Requirements

| Test Type | Automation | Trigger |
|-----------|------------|---------|
| Unit | 100% automated | Every commit |
| Contract | 100% automated | Every commit |
| Integration | 100% automated | Every PR |
| E2E | 100% automated | Daily + pre-release |
| Performance | Automated | Weekly + pre-release |
| Security | Automated | Daily + pre-release |

### CI/CD Integration

| Stage | Tests Run | Gate |
|-------|-----------|------|
| Pre-commit | Unit (fast) | Pass to commit |
| PR Build | Unit + Contract | Pass to merge |
| Post-merge | Integration | Pass to deploy |
| Pre-deploy | E2E + Security | Pass to release |

### Test Execution SLAs

| Test Suite | Max Duration | Action if Exceeded |
|------------|--------------|-------------------|
| Unit | 5 minutes | Optimize or split |
| Contract | 10 minutes | Parallelize |
| Integration | 30 minutes | Selective execution |
| E2E | 60 minutes | Parallelize, prioritize |

---

## DEFECT MANAGEMENT STANDARDS

### Defect Severity

| Severity | Definition | Response |
|----------|------------|----------|
| Critical | System unusable, data loss | Immediate fix |
| High | Major feature broken | Fix before release |
| Medium | Feature impaired, workaround exists | Fix in next sprint |
| Low | Minor issue, cosmetic | Backlog |

### Defect Documentation

Every defect MUST include:

```markdown
## Defect: [ID]

**Summary:** [One-line description]
**Severity:** Critical | High | Medium | Low
**Status:** Open | In Progress | Fixed | Verified | Closed

### Environment
- Version: [Version]
- Environment: [Where found]
- Browser/Device: [If applicable]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Result
[What should happen]

### Actual Result
[What actually happens]

### Evidence
[Screenshots, logs, error messages]

### Root Cause (when known)
[Technical explanation]

### Fix
[How it was fixed]
```

---

## REGRESSION TESTING STANDARDS

### Regression Suite Requirements

| Requirement | Standard |
|-------------|----------|
| Coverage | All critical paths |
| Execution | Every release |
| Automation | 100% automated |
| Duration | < 4 hours |
| Stability | < 2% flaky rate |

### Regression Triggers

| Event | Regression Scope |
|-------|------------------|
| Bug fix | Affected area + related |
| Feature add | Full regression |
| Refactoring | Affected area + related |
| Dependency update | Full regression |
| Release | Full regression |

---

## TEST REPORTING STANDARDS

### Required Reports

| Report | Frequency | Audience |
|--------|-----------|----------|
| Test execution | Per run | Team |
| Coverage | Daily | Team |
| Defect summary | Weekly | Stakeholders |
| Quality metrics | Sprint | Leadership |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pass rate | > 98% | Passed / Total |
| Flaky rate | < 2% | Flaky / Total |
| Coverage | Per standard | Lines/Branches covered |
| Defect escape | < 5% | Prod bugs / Total bugs |
| MTTR (test fix) | < 4 hours | Time to fix failing test |

---

*STANDARDS v1.0 | PHASE 08 | Gold Standard System*
