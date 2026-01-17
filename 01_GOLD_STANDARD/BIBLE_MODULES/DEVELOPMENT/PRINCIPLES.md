# DEVELOPMENT PRINCIPLES
## Universal Laws of Software Construction

**Module:** DEVELOPMENT
**Version:** 1.0

---

## THE FIVE IMMUTABLE LAWS

### LAW 1: MEANING PRECEDES IMPLEMENTATION

```
WHAT before HOW
Requirements before code
Understanding before building
```

**Application:**
- Never write code without understanding the requirement
- Ask "what problem does this solve?" before "how do I code this?"
- If the requirement is unclear, stop and clarify

---

### LAW 2: STRUCTURE PRECEDES INTELLIGENCE

```
Data structures before algorithms
Schema before logic
Foundation before features
```

**Application:**
- Define types and interfaces first
- Establish data models before business logic
- Build skeleton, then fill in details

---

### LAW 3: VALIDATION PRECEDES OPTIMIZATION

```
Correct before fast
Working before elegant
Tested before deployed
```

**Application:**
- Make it work first
- Verify it works with tests
- Only then optimize for performance

---

### LAW 4: EXPLICIT PRECEDES IMPLICIT

```
No magic
No hidden behavior
No undocumented side effects
```

**Application:**
- Declare all dependencies
- Document all side effects
- Prefer configuration over convention

---

### LAW 5: REVERSIBILITY PRECEDES COMMITMENT

```
Design for rollback
Every change undoable
Every deployment reversible
```

**Application:**
- Write migrations with rollback scripts
- Use feature flags for risky changes
- Keep ability to revert at all times

---

## DEVELOPMENT MANTRAS

### "Make It Work, Make It Right, Make It Fast"

1. **Make It Work:** Get basic functionality working
2. **Make It Right:** Refactor for clarity and correctness
3. **Make It Fast:** Optimize only when needed and measured

---

### "Test Early, Test Often, Test Automatically"

- Write tests alongside code (not after)
- Run tests on every change
- Automate all repeatable tests

---

### "Code Is Read More Than Written"

- Optimize for readability
- Future you is a stranger
- Comments explain "why", code shows "what"

---

### "The Best Code Is No Code"

- Don't build what you don't need
- Leverage existing solutions
- Complexity is a liability

---

## QUALITY HEURISTICS

### Single Responsibility
Each function does ONE thing. If you need "and" to describe it, split it.

### DRY (Don't Repeat Yourself)
Every piece of knowledge has a single source. If you copy-paste, extract.

### KISS (Keep It Simple, Stupid)
The simplest solution that works is often the best. Resist over-engineering.

### YAGNI (You Ain't Gonna Need It)
Don't build features for imagined future needs. Build what's needed now.

---

## ERROR PHILOSOPHY

### Fail Fast
Detect problems early. Validate inputs immediately.

### Fail Loud
Make errors visible. Never silently swallow exceptions.

### Fail Safe
When failure occurs, fail to a safe state. Never leave data corrupted.

---

*PRINCIPLES v1.0 | DEVELOPMENT | BIBLE_MODULES*
