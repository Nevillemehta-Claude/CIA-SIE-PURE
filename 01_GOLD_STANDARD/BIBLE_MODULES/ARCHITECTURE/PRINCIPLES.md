# ARCHITECTURE PRINCIPLES
## Universal Laws of System Design

**Module:** ARCHITECTURE
**Version:** 1.0

---

## THE SIX ARCHITECTURE PRINCIPLES

### PRINCIPLE 1: SINGLE SOURCE OF TRUTH (SSOT)

**Definition:** Each piece of data has ONE authoritative source. All other references derive from it.

**Application:**
| Information | Single Source |
|-------------|---------------|
| Requirements | Requirements Specification |
| API Contracts | OpenAPI Schema |
| Data Models | Database Schema |
| Business Logic | Specification Document |
| Configuration | Configuration Repository |

**Anti-Pattern:** Same information in multiple places that can get out of sync.

**Test:** "If this changes, how many places must I update?" Answer must be: ONE.

---

### PRINCIPLE 2: LOOSE COUPLING

**Definition:** Components interact through well-defined interfaces. Changes in one component do not cascade to others.

**Application:**
- Components communicate via APIs, not shared internals
- No direct database access from presentation layer
- Dependencies are on interfaces, not implementations

**Anti-Pattern:** Component A directly accesses Component B's database.

**Test:** "Can I change the internals of Component A without changing Component B?" Answer must be: YES.

---

### PRINCIPLE 3: HIGH COHESION

**Definition:** Related functionality is grouped together. Each module has a single, clear purpose.

**Application:**
- One module handles authentication (not split across modules)
- One service handles user management (not scattered)
- Functions that change together live together

**Anti-Pattern:** User validation in 5 different files.

**Test:** "Does this module have a clear, single purpose?" Answer must be: YES.

---

### PRINCIPLE 4: EXPLICIT CONTRACTS

**Definition:** Interfaces are documented, versioned, and enforced. Breaking changes require version bump.

**Application:**
- OpenAPI specification for REST APIs
- TypeScript interfaces for data structures
- Semantic versioning for changes
- Contract tests to enforce compliance

**Anti-Pattern:** Undocumented API that changes without notice.

**Test:** "Is there a contract that defines exactly what this interface accepts and returns?" Answer must be: YES.

---

### PRINCIPLE 5: FAIL-SAFE DEFAULTS

**Definition:** When things go wrong, the system fails to a safe state. Missing config uses secure defaults. Unknown input is rejected.

**Application:**
- Authentication fails → deny access (not allow)
- Config missing → use secure default (not crash or allow)
- Unknown input → return 400 Bad Request (not process)
- Feature flag missing → disable feature (not enable)

**Anti-Pattern:** System allows access when auth service is unavailable.

**Test:** "What happens if [component] fails or [data] is missing?" Answer must be: SAFE STATE.

---

### PRINCIPLE 6: DETERMINISTIC BEHAVIOR

**Definition:** Same input produces same output. No hidden state. Results are reproducible.

**Application:**
- Pure functions where possible
- Idempotent API operations
- No reliance on global mutable state
- Time-dependent behavior uses injected clock

**Anti-Pattern:** Function returns different results on repeated calls with same input.

**Test:** "If I call this function twice with the same input, do I get the same output?" Answer must be: YES (or documented exception).

---

## ARCHITECTURAL DECISION MAKING

### Decision Record (ADR) Template

```markdown
# ADR-XXX: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[What is the situation requiring a decision?]

## Decision
[What is the decision?]

## Consequences
[What are the positive and negative consequences?]

## Alternatives Considered
[What other options were evaluated?]
```

### Decision Criteria

When choosing between alternatives:

| Priority | Criterion |
|----------|-----------|
| 1 | Correctness - Does it satisfy requirements? |
| 2 | Security - Is it safe? |
| 3 | Maintainability - Can it be understood and changed? |
| 4 | Performance - Is it fast enough? |
| 5 | Cost - Is it economical? |

---

## LAYERED ARCHITECTURE

Standard layers, from top to bottom:

```
┌─────────────────────────────────────┐
│         PRESENTATION LAYER          │
│   (UI, API Endpoints, Controllers)  │
├─────────────────────────────────────┤
│          APPLICATION LAYER          │
│   (Use Cases, Business Workflows)   │
├─────────────────────────────────────┤
│           DOMAIN LAYER              │
│   (Business Logic, Entities)        │
├─────────────────────────────────────┤
│       INFRASTRUCTURE LAYER          │
│   (Database, External Services)     │
└─────────────────────────────────────┘
```

**Dependency Rule:** Outer layers may depend on inner layers. Inner layers MUST NOT depend on outer layers.

---

## COMPONENT DESIGN

### Interface Segregation
Clients should not depend on interfaces they don't use.
Split large interfaces into focused ones.

### Dependency Inversion
High-level modules should not depend on low-level modules.
Both should depend on abstractions.

### Open-Closed Principle
Software entities should be open for extension, closed for modification.
Add new behavior without changing existing code.

---

*PRINCIPLES v1.0 | ARCHITECTURE | BIBLE_MODULES*
