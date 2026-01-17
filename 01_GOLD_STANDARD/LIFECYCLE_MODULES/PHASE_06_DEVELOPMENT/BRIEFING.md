# PHASE 06: DEVELOPMENT
## Briefing Document

**Phase Number:** 6
**Phase Name:** Development
**Purpose:** Build the components according to specification

---

## WHAT THIS PHASE IS

Development is the construction phase where specifications become working code. Every function, every component, every interface is built according to the detailed specifications created in Phase 5.

**Key Insight:** Development is NOT creative work. It is translation work. The creativity happened in Phases 1-5. Development translates those decisions into executable code.

---

## WHAT YOU'RE DOING

1. **Implementing components** per the Technical Specification
2. **Writing unit tests** for every function
3. **Writing contract tests** for every interface
4. **Conducting code reviews** for every merge
5. **Maintaining continuous integration** for every commit

---

## WHAT YOU'RE NOT DOING

- Making design decisions (that was Phase 4)
- Defining behaviors (that was Phase 5)
- Integrating components (that's Phase 7)
- Conducting system testing (that's Phase 8)

**If you find yourself making design decisions, STOP. Return to the appropriate phase.**

---

## GOVERNING DOCUMENTS

| Document | Location | Contains |
|----------|----------|----------|
| Technical Specification | Phase 5 output | What to build |
| API Specification | Phase 5 output | Interface contracts |
| Architecture Document | Phase 4 output | System structure |
| DEVELOPMENT Standards | BIBLE_MODULES/DEVELOPMENT/ | How to build |

---

## KEY PRINCIPLES FOR THIS PHASE

### From FIRST_PRINCIPLES

1. **Law 3: Validation Precedes Optimization**
   - Make it work first
   - Make it right second
   - Make it fast last

2. **Law 4: Explicit Precedes Implicit**
   - No magic
   - No hidden behavior
   - All dependencies declared

### From VERIFICATION_DOCTRINE

1. **Continuous Verification**
   - Unit test after every function
   - Static analysis on every commit
   - Regression suite on every merge

2. **Fix-Verify Cycle**
   - Failed test = STOP
   - Fix at the lowest layer
   - Re-verify before proceeding

---

## SUCCESS CRITERIA

| Criterion | Target |
|-----------|--------|
| Unit Test Coverage | >90% |
| Contract Tests | 100% of interfaces |
| Static Analysis | 0 critical issues |
| Code Review | 100% of merges |
| Specification Compliance | 100% |

---

## COMMON PITFALLS

### 1. Building Without Tests
**Problem:** "I'll write tests later"
**Reality:** Later never comes, or tests become afterthought
**Solution:** Write test BEFORE implementation (TDD) or IMMEDIATELY after

### 2. Making Design Decisions During Code
**Problem:** "This specification doesn't work, I'll design something better"
**Reality:** Creates specification drift, untracked decisions
**Solution:** Return to Phase 4 or 5, update specifications, then implement

### 3. Premature Optimization
**Problem:** "Let me make this faster before it even works"
**Reality:** Wastes time on code that might not be correct
**Solution:** Make it work, verify it works, THEN optimize

### 4. Skipping Code Review
**Problem:** "I know what I'm doing, no review needed"
**Reality:** Misses defects, reduces knowledge sharing
**Solution:** Every merge gets reviewed, no exceptions

---

## PHASE DURATION

This phase ends when:
- All components specified in Phase 5 are implemented
- All unit tests pass
- All contract tests pass
- All code reviews complete
- Ready for integration (Phase 7)

---

## NEXT STEPS

After completing this phase:
1. Verify all exit criteria in `VERIFICATION/EXIT_CRITERIA.md`
2. Proceed to Phase 7: Integration
3. Load `LIFECYCLE_MODULES/PHASE_07_INTEGRATION/`

---

*PHASE 06 BRIEFING v1.0 | LIFECYCLE_MODULES | Gold Standard System*
