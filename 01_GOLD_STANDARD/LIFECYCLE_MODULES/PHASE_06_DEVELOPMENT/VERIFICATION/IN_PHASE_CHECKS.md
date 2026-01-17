# PHASE 06: DEVELOPMENT
## In-Phase Verification Checks

**Purpose:** Verification activities that MUST occur during development

---

## CONTINUOUS VERIFICATION CADENCE

| Trigger | Verification Required | Pass Criteria |
|---------|----------------------|---------------|
| File Save | Syntax check, linting | No errors |
| Function Complete | Unit test written and passing | Function works as specified |
| Module Complete | All module tests passing | Module ready for integration |
| Commit | Pre-commit hooks | Lint + type check + tests |
| Push | CI pipeline | Full test suite green |
| PR Created | Code review | Approval from reviewer |
| PR Merged | Regression suite | No regressions introduced |

---

## PER-FUNCTION CHECKLIST

After completing each function:

- [ ] Function implements specification
- [ ] Unit tests written
- [ ] Unit tests passing
- [ ] Edge cases tested
- [ ] Error cases tested
- [ ] JSDoc documentation added

---

## PER-COMPONENT CHECKLIST

After completing each component:

- [ ] All functions complete
- [ ] All unit tests passing
- [ ] Contract tests written (if interface)
- [ ] Contract tests passing
- [ ] Component documentation complete
- [ ] Ready for code review

---

## DAILY CHECKS

At end of each development session:

- [ ] All local tests passing
- [ ] No uncommitted work left
- [ ] CI pipeline green
- [ ] No blocking issues unaddressed

---

*IN-PHASE CHECKS v1.0 | PHASE 06 | Gold Standard System*
