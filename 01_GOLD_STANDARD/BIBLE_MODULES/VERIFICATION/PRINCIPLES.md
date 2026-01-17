# VERIFICATION PRINCIPLES
## Universal Laws of Testing and Validation

**Module:** VERIFICATION
**Version:** 1.0

---

## THE VERIFICATION CREED

> "Testing is not a phase. It is a constant companion to every action."

Verification is not something you do at the end. It is something you do at every step. Every artifact produced must be verified before proceeding.

---

## THE TEN VERIFICATION LAWS

### LAW 1: COVERAGE IS NON-NEGOTIABLE

**Statement:** Every line of code that can be tested must be tested. Coverage targets are minimums, not goals.

| Criticality | Minimum Coverage |
|-------------|------------------|
| Safety-Critical | 100% + MC/DC |
| Business-Critical | >95% |
| Standard | >90% |
| Utility | >80% |

**Corollary:** Untested code is unverified code. Unverified code is a liability.

---

### LAW 2: LAYERS CANNOT BE SKIPPED

**Statement:** The verification pyramid must be climbed from bottom to top. Higher layers depend on lower layers.

```
                ACCEPTANCE
               /          \
          SYSTEM            \
         /      \            \
    INTEGRATION  \            \
       /          \            \
   COMPONENT       \            \
      /             \            \
   UNIT              FOUNDATION
```

**Corollary:** A passing integration test does not validate units. A passing system test does not validate integration.

---

### LAW 3: EVIDENCE BEATS ASSERTION

**Statement:** "It works" is not verification. Evidence is verification.

| Assertion (Unacceptable) | Evidence (Required) |
|--------------------------|---------------------|
| "We tested it" | Test report with pass/fail |
| "It handles errors" | Test covering each error path |
| "Performance is good" | Benchmark results with numbers |
| "It's secure" | Security scan report |

---

### LAW 4: REGRESSION IS MANDATORY

**Statement:** Every change must be verified against existing functionality. No change is too small for regression testing.

**Regression triggers:**
- Any code change
- Any configuration change
- Any dependency update
- Any environment change

---

### LAW 5: TESTS ARE FIRST-CLASS CODE

**Statement:** Tests deserve the same quality standards as production code. Tests are not second-class citizens.

**Test quality requirements:**
- Readable and maintainable
- No duplication
- Properly named
- Properly organized
- Reviewed like production code

---

### LAW 6: FAILURE IS INFORMATION

**Statement:** A failing test is not a problem. A failing test is a discovery. Ignoring or disabling failing tests is the problem.

**When a test fails:**
1. Investigate the cause
2. Fix the defect OR fix the test
3. NEVER skip or comment out
4. NEVER mark as "known failure"

---

### LAW 7: AUTOMATION IS MANDATORY

**Statement:** Any test that will be run more than once must be automated. Manual testing is for exploration, not regression.

| Testing Type | Automation Level |
|--------------|------------------|
| Unit | 100% automated |
| Integration | 100% automated |
| Regression | 100% automated |
| Performance | 100% automated |
| Exploratory | Manual (by design) |
| UAT | Supported by automation |

---

### LAW 8: INDEPENDENCE IS REQUIRED

**Statement:** Tests must be independent. No test should depend on another test. No test should affect another test.

**Independence requirements:**
- Tests run in any order
- Tests run in isolation
- Tests clean up after themselves
- Tests don't share mutable state

---

### LAW 9: DETERMINISM IS ESSENTIAL

**Statement:** The same test with the same inputs must produce the same result. Flaky tests are bugs.

**Flaky test causes:**
- Timing dependencies
- External service dependencies
- Shared mutable state
- Random data without seed

**Flaky test response:** Fix immediately. Do not tolerate.

---

### LAW 10: VERIFICATION IS CONTINUOUS

**Statement:** Verification runs on every change, not before release. Continuous verification catches issues early.

**Continuous verification points:**
- Pre-commit: Lint, type check, unit tests
- Post-push: Full unit suite
- Pull request: Integration tests, coverage
- Pre-merge: Full regression
- Post-deploy: Smoke tests, monitoring

---

## TEST DESIGN PRINCIPLES

### Test One Thing

Each test verifies ONE behavior. If a test fails, you know exactly what broke.

```
// BAD: Tests multiple things
it('should create user and send email and update stats')

// GOOD: Tests one thing
it('should create user with valid data')
it('should send welcome email after user creation')
it('should increment user count after creation')
```

### Arrange-Act-Assert

Every test follows the AAA pattern:

```
it('should calculate total with tax', () => {
  // Arrange
  const items = [{ price: 100 }, { price: 50 }]
  const taxRate = 0.1

  // Act
  const total = calculateTotal(items, taxRate)

  // Assert
  expect(total).toBe(165)
})
```

### Test Behavior, Not Implementation

Test what the code DOES, not HOW it does it.

```
// BAD: Tests implementation
it('should call database.save with user object')

// GOOD: Tests behavior
it('should persist user and return user ID')
```

### Use Descriptive Names

Test names should describe the scenario and expected outcome.

```
// BAD
it('test 1')

// GOOD
it('should return CURRENT status for timestamp within 2 minutes')
```

---

## ERROR PATH TESTING

Happy paths are easy. Error paths reveal quality.

**Test error scenarios:**
- Invalid inputs
- Null/undefined values
- Empty collections
- Boundary conditions
- Network failures
- Timeout conditions
- Concurrent access
- Resource exhaustion

---

## VERIFICATION METRICS

| Metric | What It Measures | Target |
|--------|------------------|--------|
| Code Coverage | Lines executed by tests | >90% |
| Branch Coverage | Decision paths tested | >80% |
| Mutation Score | Tests that catch changes | >80% |
| Test Pass Rate | Tests that pass | 100% |
| Test Stability | Tests without flakiness | 100% |
| Time to Feedback | How fast tests run | <5 min for unit |

---

*PRINCIPLES v1.0 | VERIFICATION | BIBLE_MODULES*
