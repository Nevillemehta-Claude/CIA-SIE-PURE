# PHASE 03: REQUIREMENTS ANALYSIS
## Briefing Document

**Phase Number:** 3
**Phase Name:** Requirements Analysis
**Purpose:** Define exactly what the system must do

---

## WHAT THIS PHASE IS

Requirements Analysis transforms the concept into specific, testable requirements. Every capability identified in Phase 2 becomes one or more requirements with clear acceptance criteria. This phase creates the contract between stakeholders and development.

**Key Insight:** Requirements are the foundation of traceability. If it's not a requirement, it shouldn't be built. If it can't be tested, it's not a requirement.

---

## WHAT YOU'RE DOING

1. **Eliciting requirements** from stakeholders and concept document
2. **Documenting requirements** with unique identifiers
3. **Classifying requirements** (functional, non-functional)
4. **Prioritizing requirements** (must/should/could)
5. **Defining acceptance criteria** for each requirement
6. **Establishing traceability baseline**

---

## WHAT YOU'RE NOT DOING

- Designing solutions (that's Phase 4)
- Specifying implementation details (that's Phase 5)
- Making technology choices
- Writing code

**This phase answers WHAT (precisely), not HOW.**

---

## REQUIREMENT CHARACTERISTICS

Every good requirement is:

| Characteristic | Definition |
|----------------|------------|
| **Necessary** | Stakeholders need it |
| **Unambiguous** | One interpretation only |
| **Testable** | Can be verified |
| **Traceable** | Unique ID, linked to source |
| **Achievable** | Technically feasible |
| **Consistent** | No conflicts with other requirements |

---

## REQUIREMENT TYPES

### Functional Requirements
What the system DOES.
- "The system shall allow users to register with email and password"
- "The system shall display signal freshness status"

### Non-Functional Requirements
HOW WELL the system does it.
- Performance: "Page load time shall be under 3 seconds"
- Security: "Passwords shall be hashed using bcrypt"
- Availability: "System uptime shall be 99.9%"
- Usability: "Interface shall meet WCAG 2.1 AA"

### Constraints
Boundaries on solution space.
- "System shall run on Linux servers"
- "Frontend shall support Chrome, Firefox, Safari"

---

## REQUIREMENT FORMAT

```markdown
## REQ-[NUMBER]: [Title]

**Type:** Functional | Non-Functional | Constraint
**Priority:** Must | Should | Could
**Source:** [Where this requirement came from]

**Statement:**
The system shall [action] [object] [condition].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Dependencies:**
- [Related requirements]

**Notes:**
[Any clarifications]
```

### Example

```markdown
## REQ-001: User Registration

**Type:** Functional
**Priority:** Must
**Source:** Concept Document Section 3.1

**Statement:**
The system shall allow new users to register with email and password.

**Acceptance Criteria:**
- [ ] User can enter email address
- [ ] User can enter password
- [ ] Password must be at least 8 characters
- [ ] Email must be unique (not already registered)
- [ ] User receives confirmation email
- [ ] User cannot login until email confirmed

**Dependencies:**
- REQ-002 (Email service integration)

**Notes:**
Social login is out of scope for v1.
```

---

## REQUIREMENTS TRACEABILITY MATRIX

Initialize the RTM in this phase:

| REQ ID | Requirement | Source | Priority | Implementation | Test |
|--------|-------------|--------|----------|----------------|------|
| REQ-001 | User Registration | Concept 3.1 | Must | TBD | TBD |
| REQ-002 | Email Service | REQ-001 | Must | TBD | TBD |

**Implementation and Test columns completed in later phases.**

---

## PRIORITIZATION

### MoSCoW Method

| Priority | Definition | Treatment |
|----------|------------|-----------|
| **Must** | Essential, no workaround | Required for go-live |
| **Should** | Important, has workaround | Target for go-live |
| **Could** | Nice to have | If time permits |
| **Won't** | Out of scope for this release | Document for future |

---

## COMMON PITFALLS

### 1. Solution Masquerading as Requirement
**Problem:** "System shall use PostgreSQL database"
**Fix:** That's a design decision, not a requirement. Requirement: "System shall persist user data"

### 2. Untestable Requirement
**Problem:** "System shall be user-friendly"
**Fix:** "System shall complete common tasks in under 3 clicks"

### 3. Ambiguous Language
**Problem:** "System shall quickly process requests"
**Fix:** "System shall process requests in under 200ms (p95)"

### 4. Missing Acceptance Criteria
**Problem:** Requirement with no way to verify
**Fix:** Every requirement has specific acceptance criteria

---

## EXIT CRITERIA

Phase 3 is complete when:

- [ ] All requirements documented with unique IDs
- [ ] Each requirement has acceptance criteria
- [ ] Requirements are prioritized
- [ ] RTM established
- [ ] Requirements reviewed and approved
- [ ] No TBD or ambiguous requirements

---

## NEXT STEPS

After completing this phase:
1. Requirements reviewed by all stakeholders
2. Sign-off obtained
3. Proceed to Phase 4: Architecture Design
4. Load `LIFECYCLE_MODULES/PHASE_04_ARCHITECTURE/`

---

*PHASE 03 BRIEFING v1.0 | LIFECYCLE_MODULES | Gold Standard System*
