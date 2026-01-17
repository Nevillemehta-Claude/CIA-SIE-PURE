# FIRST PRINCIPLES
## Immutable Truths of Software Development

**Classification:** CORE_KERNEL (Immutable)
**Version:** 1.0
**Applicability:** Universal - All Projects, All Phases, All Time

---

## PREAMBLE

These principles are axiomatic. They do not change based on project, technology, timeline, or circumstance. They are the bedrock upon which all other standards, processes, and decisions rest.

When any standard, process, or decision conflicts with these principles, the principle prevails.

---

## THE EIGHT GOLD STANDARD PRINCIPLES

### PRINCIPLE 1: NASA-STYLE RIGOUR

**Axiom:** Exhaustive, systematic, evidence-based validation where every claim is verifiable and reproducible.

| Attribute | Requirement |
|-----------|-------------|
| No Assumptions | Every finding cites exact evidence |
| No Shortcuts | 100% coverage, never sampling |
| No Ambiguity | Binary pass/fail only |
| Reproducibility | Same process yields same result |

**Test:** Can another qualified person, following your documentation, reach the identical conclusion?

---

### PRINCIPLE 2: AUDIT BEFORE BUILD

**Axiom:** Validation must precede construction. Building upon unvalidated foundations propagates defects exponentially.

```
MANDATED SEQUENCE:
1. Audit existing artifacts against specifications
2. Document all discrepancies with evidence
3. Remediate (correct implementation OR update specification)
4. Construct new features upon validated baseline

PROHIBITED SEQUENCE:
- Build new features on unvalidated code
- Defer audit activities
- Discover foundational defects post-construction
```

**Rationale:** Technical debt compounds. Defects in foundational layers propagate to all dependent components, creating exponential remediation costs.

---

### PRINCIPLE 3: ZERO DRIFT POLICY

**Axiom:** Specifications and implementation shall remain synchronized at all times. No divergence without documented justification.

| Scenario | Mandated Action |
|----------|-----------------|
| Implementation differs from spec; spec is correct | Correct the implementation |
| Implementation differs from spec; implementation is correct | Update the specification |
| Both require improvement | Correct both; document the change |
| Divergence without justification | **NON-COMPLIANT** |

**Test:** Does the documentation accurately describe what the code does right now?

---

### PRINCIPLE 4: LIVING DOCUMENTATION

**Axiom:** Documentation is maintained contemporaneously, not retrospectively. Stale documentation is a compliance violation.

| Anti-Pattern | Gold Standard |
|--------------|---------------|
| "Documentation later" | Document as you build |
| Stale README | README reflects current state |
| Orphaned specifications | Specs updated with code |

**Test:** Can a qualified engineer understand the complete system from documentation alone?

---

### PRINCIPLE 5: FULL BIDIRECTIONAL TRACEABILITY

**Axiom:** Every line of code traces to a requirement; every requirement traces to implementation and verification.

```
REQUIREMENT <---> IMPLEMENTATION <---> VERIFICATION
     ^                   ^                   ^
     |___________________|___________________|
              BIDIRECTIONAL TRACEABILITY
```

| Question | Must Be Answerable |
|----------|-------------------|
| Which requirement does this code implement? | Yes |
| Where is this requirement implemented? | Yes |
| What tests verify this implementation? | Yes |
| Is there orphan code (no requirement)? | Must be zero |
| Are there unimplemented requirements? | Must be documented |

---

### PRINCIPLE 6: EVIDENCE-BASED VALIDATION

**Axiom:** Assertions without evidence are invalid. Every compliance claim requires verifiable proof.

| Evidence Quality | Example | Acceptability |
|------------------|---------|---------------|
| **Weak** | "The module handles errors appropriately" | REJECTED |
| **Strong** | "Error handling at file:line; implements pattern per SPEC#section" | ACCEPTED |

**Rule:** If you cannot point to the exact location, you have not verified it.

---

### PRINCIPLE 7: SINGLE SOURCE OF TRUTH

**Axiom:** For any category of information, exactly one authoritative source exists. All other references derive from it.

| Information Category | Single Source |
|---------------------|---------------|
| Requirements | Requirements Specification |
| API Contracts | OpenAPI Schema |
| Data Models | Database Schema / ORM |
| Business Logic | Authoritative Specification |
| Configuration | Configuration Repository |
| Test Expectations | Test Specification |

**Test:** If this information changes, how many places must be updated? (Answer must be: ONE)

---

### PRINCIPLE 8: DEFENSIVE DOCUMENTATION

**Axiom:** Documentation anticipates failure modes and explicitly addresses edge cases.

**Defensive documentation includes:**
1. Known limitations and constraints
2. Failure modes and recovery procedures
3. Security considerations and threat mitigations
4. Performance boundaries and degradation behaviors

**Test:** Does the documentation tell me what to do when things go wrong?

---

## THE FIVE IMMUTABLE LAWS

### LAW 1: MEANING PRECEDES IMPLEMENTATION

```
WHAT before HOW
Requirements before code
Understanding before building
```

- No code without documented requirements
- Every function has defined purpose before implementation
- "Why are we building this?" answered before "How?"

---

### LAW 2: STRUCTURE PRECEDES INTELLIGENCE

```
Data structures before algorithms
Schema before logic
Foundation before features
```

- Database schema finalized before business logic
- Data models defined before service layer
- Type definitions exist before functions that use them

---

### LAW 3: VALIDATION PRECEDES OPTIMIZATION

```
Correct before fast
Working before elegant
Tested before deployed
```

- Functionally correct before performance optimization
- Unit tests pass before refactoring
- "Make it work, make it right, make it fast" - in that order

---

### LAW 4: EXPLICIT PRECEDES IMPLICIT

```
No magic
No hidden behavior
No undocumented side effects
```

- All dependencies explicitly declared
- All side effects documented
- No "convention over configuration" that hides behavior

---

### LAW 5: REVERSIBILITY PRECEDES COMMITMENT

```
Design for rollback
Every change undoable
Every deployment reversible
```

- Every migration has rollback script
- Every deployment reversible within 5 minutes
- No "one-way door" decisions without explicit approval

---

## THE SIX ARCHITECTURE PRINCIPLES

### 1. SINGLE SOURCE OF TRUTH (SSOT)
Each piece of data has ONE authoritative source. No duplication of business logic.

### 2. LOOSE COUPLING
Components interact through well-defined interfaces. Changes isolated to single component.

### 3. HIGH COHESION
Related functionality grouped together. Each module has single, clear purpose.

### 4. EXPLICIT CONTRACTS
API contracts documented and versioned. Breaking changes require version bump.

### 5. FAIL-SAFE DEFAULTS
System fails to safe state. Missing config = secure defaults. Unknown input = reject.

### 6. DETERMINISTIC BEHAVIOR
Same input = same output. No hidden state. Reproducible results.

---

## THE MODULARITY DOCTRINE

### Core Truth
> Every worthy system is composed of autonomous, self-contained units that can be developed, tested, verified, upgraded, and replaced independently.

### Module Properties

Every module must be:

| Property | Definition |
|----------|------------|
| **Self-Contained** | Has everything needed to function |
| **Independently Testable** | Can be verified in isolation |
| **Versioned** | Has explicit version and change history |
| **Documented** | Has MANIFEST describing what it is |
| **Interface-Defined** | Has explicit inputs and outputs |
| **Replaceable** | Can be swapped without rebuilding the whole |

### Integration Law
Modules connect through defined contracts, not assumptions. The interface between modules is explicit, documented, and versioned.

---

## THE VERIFICATION DOCTRINE

### Core Truth
> Testing is not a phase. It is a constant companion to every action.

### Verification Layers

| Layer | Question | When |
|-------|----------|------|
| SYNTAX | Does it compile/parse? | Every save |
| UNIT | Does this function work? | After every function |
| CONTRACT | Does this honor its interface? | After component complete |
| INTEGRATION | Do connected parts work together? | After connecting |
| FUNCTIONAL | Does the feature work as specified? | After feature complete |
| REGRESSION | Did new code break old functionality? | After every change |
| PERFORMANCE | Does it meet speed/resource requirements? | At system level |
| ACCEPTANCE | Does it satisfy the original need? | Before release |

### Verification Law
You cannot skip layers. A system that passes integration tests but has no unit tests is a house built on sand.

---

## APPLICATION

These principles apply to:
- Every project, regardless of domain
- Every phase, regardless of timeline
- Every decision, regardless of pressure
- Every artifact, regardless of size

When in doubt, return to these principles. They are the foundation.

---

*FIRST PRINCIPLES v1.0 | CORE_KERNEL | Gold Standard System*
