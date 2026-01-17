# PHASE 06: DEVELOPMENT
## Process Document

**Phase Number:** 6
**Purpose:** Step-by-step execution guide for development

---

## PRE-DEVELOPMENT CHECKLIST

Before writing any code, verify:

- [ ] Technical Specification is complete and approved (Phase 5)
- [ ] API Specification is complete and validated
- [ ] Development environment is configured
- [ ] Test framework is operational
- [ ] CI/CD pipeline is configured
- [ ] Branching strategy is defined

---

## THE DEVELOPMENT CYCLE

For EACH component in the specification:

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. READ SPECIFICATION                                     │
│     "What exactly must this component do?"                 │
│                                                            │
│  2. WRITE TESTS FIRST (TDD) or IMMEDIATELY AFTER          │
│     "How will I know this works?"                          │
│                                                            │
│  3. IMPLEMENT                                              │
│     "Build according to specification"                     │
│                                                            │
│  4. VERIFY                                                 │
│     "Do all tests pass?"                                   │
│                                                            │
│  5. REFACTOR (if needed)                                   │
│     "Can this be cleaner while still passing tests?"       │
│                                                            │
│  6. DOCUMENT                                               │
│     "Is this understandable to others?"                    │
│                                                            │
│  7. COMMIT                                                 │
│     "Save this verified state"                             │
│                                                            │
│  8. REVIEW                                                 │
│     "Get another pair of eyes"                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## STEP 1: READ SPECIFICATION

**Action:** Load the relevant section of the Technical Specification

**Questions to Answer:**
1. What is this component's responsibility?
2. What are its inputs?
3. What are its outputs?
4. What are the edge cases?
5. What errors can occur?
6. What are the constraints?

**Output:** Understanding of what to build

**Time Box:** Until you can explain it clearly

---

## STEP 2: WRITE TESTS

**Action:** Write tests that will verify the specification is met

### Unit Tests

For each function:
1. **Happy Path:** Normal input → expected output
2. **Edge Cases:** Boundary values, empty inputs
3. **Error Cases:** Invalid inputs, failure conditions

```typescript
describe('functionName', () => {
  // Happy path
  it('should return expected output for normal input', () => {
    expect(functionName(normalInput)).toEqual(expectedOutput)
  })

  // Edge case
  it('should handle empty input', () => {
    expect(functionName([])).toEqual([])
  })

  // Error case
  it('should throw for invalid input', () => {
    expect(() => functionName(null)).toThrow(ValidationError)
  })
})
```

### Contract Tests

For each interface:
1. **Request Schema:** Valid requests accepted
2. **Response Schema:** Responses match contract
3. **Error Responses:** Error formats correct

**Output:** Test suite that currently FAILS (nothing implemented yet)

---

## STEP 3: IMPLEMENT

**Action:** Write the code that makes the tests pass

### Implementation Order

1. **Type Definitions First**
   ```typescript
   interface ComponentInput {
     // Define structure
   }

   interface ComponentOutput {
     // Define structure
   }
   ```

2. **Function Skeleton**
   ```typescript
   function processInput(input: ComponentInput): ComponentOutput {
     // TODO: Implement
     throw new Error('Not implemented')
   }
   ```

3. **Core Logic**
   ```typescript
   function processInput(input: ComponentInput): ComponentOutput {
     // Validate input
     if (!isValid(input)) {
       throw new ValidationError('Invalid input')
     }

     // Process
     const result = transform(input)

     // Return
     return result
   }
   ```

4. **Error Handling**
   ```typescript
   function processInput(input: ComponentInput): ComponentOutput {
     try {
       // ... core logic
     } catch (error) {
       if (error instanceof KnownError) {
         // Handle known error
       }
       // Log and rethrow unexpected errors
       logger.error('Unexpected error', { error })
       throw error
     }
   }
   ```

**Output:** Code that makes tests pass

---

## STEP 4: VERIFY

**Action:** Run all tests, confirm they pass

### Verification Checklist

```bash
# Run unit tests
npm run test

# Run with coverage
npm run test:coverage

# Check coverage threshold
# Must be >90% for new code

# Run static analysis
npm run lint

# Run type check
npm run typecheck
```

**Pass Criteria:**
- [ ] All unit tests GREEN
- [ ] Coverage >90% for new code
- [ ] No lint errors
- [ ] No type errors

**If ANY fail:** Return to Step 3, fix, re-verify

---

## STEP 5: REFACTOR

**Action:** Improve code quality while maintaining passing tests

**When to Refactor:**
- Code duplication detected
- Function too long (>50 lines)
- Complexity too high (cyclomatic >10)
- Names unclear
- Magic numbers present

**Refactoring Rules:**
1. Tests must pass BEFORE refactoring
2. Make small changes
3. Run tests after EACH change
4. If tests fail, revert immediately

**Output:** Cleaner code, still passing tests

---

## STEP 6: DOCUMENT

**Action:** Add documentation where needed

### What to Document

| Element | Documentation Required |
|---------|----------------------|
| Public functions | JSDoc with @param, @returns, @example |
| Complex logic | Inline comments explaining "why" |
| Exported types | JSDoc describing purpose |
| Constants | Comment if purpose not obvious |

### What NOT to Document

| Element | Why |
|---------|-----|
| Self-explanatory code | `const name = user.name` needs no comment |
| Implementation details | Tests document behavior |
| Temporary workarounds | Should be fixed, not documented |

**Output:** Code understandable by others

---

## STEP 7: COMMIT

**Action:** Save verified state to version control

### Pre-Commit Checks

```bash
# Automated by pre-commit hooks:
- Lint
- Type check
- Unit tests
- Commit message format
```

### Commit Message

```
<type>(<scope>): <subject>

- What was done
- Why it was done

Implements: REQ-XXX (traceability to requirement)
```

**Output:** Atomic commit of verified code

---

## STEP 8: REVIEW

**Action:** Request code review from qualified reviewer

### Create Pull Request

```markdown
## Summary
Brief description of what this implements

## Changes
- List of specific changes
- Component added/modified

## Testing
- [ ] Unit tests added
- [ ] Integration tests added (if applicable)
- [ ] Manual testing completed

## Specification Reference
Links to relevant specification sections

## Checklist
- [ ] Follows coding standards
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No security issues
```

### Review Response

1. **Address all comments**
2. **Re-verify after changes**
3. **Request re-review if significant changes**
4. **Merge only after approval**

**Output:** Approved, merged code

---

## ITERATION

Repeat Steps 1-8 for each component until:
- All components in specification are implemented
- All tests pass
- All code reviewed and merged

---

## HANDLING BLOCKERS

### Specification Unclear

```
1. Document the ambiguity
2. Propose interpretation
3. Seek clarification from Principal
4. If answer changes specification, update Phase 5 output
5. Then proceed with implementation
```

### Technical Obstacle

```
1. Document the obstacle
2. Research solutions
3. Propose alternatives with trade-offs
4. Seek decision from Principal
5. Document decision as ADR
6. Implement chosen solution
```

### Test Cannot Pass

```
1. Verify test is correct (matches specification)
2. If test is wrong, fix test
3. If implementation is wrong, fix implementation
4. If specification is wrong, return to Phase 5
5. NEVER skip or comment out failing tests
```

---

## END OF PHASE

Phase 6 is complete when:

- [ ] ALL components in specification are implemented
- [ ] ALL unit tests pass
- [ ] ALL contract tests pass
- [ ] Coverage targets met (>90%)
- [ ] ALL code reviewed and approved
- [ ] ALL commits merged to main branch
- [ ] No pending TODOs in codebase (or tracked as issues)

**Next:** Proceed to Phase 7 (Integration)

---

*PHASE 06 PROCESS v1.0 | LIFECYCLE_MODULES | Gold Standard System*
