# PHASE 03: REQUIREMENTS ANALYSIS
## Standards

**Purpose:** Quality standards for requirements documentation and management

---

## REQUIREMENT WRITING STANDARDS

### The Golden Rule

Every requirement SHALL be:
- **S**pecific - Clear and precise
- **M**easurable - Quantifiable when possible
- **A**chievable - Realistic within constraints
- **R**elevant - Tied to project goals
- **T**raceable - Source and destination known

### Language Standards

**Use:**
- "SHALL" for mandatory requirements
- "SHOULD" for recommended requirements
- "MAY" for optional requirements

**Avoid:**
- Ambiguous terms (some, few, many, adequate)
- Subjective terms (user-friendly, fast, easy)
- Compound requirements (use atomic statements)

### Good vs Bad Examples

| Bad | Good |
|-----|------|
| "The system should be fast" | "The system SHALL respond within 200ms for 95% of requests" |
| "Users can manage their data" | "The system SHALL allow users to create, read, update, and delete their profile data" |
| "The system must be secure" | "The system SHALL encrypt all data at rest using AES-256" |
| "Should support many users" | "The system SHALL support 10,000 concurrent users" |

---

## REQUIREMENT ID STANDARDS

### Functional Requirements

Format: `REQ-[Category]-[Number]`

| Category | Code | Example |
|----------|------|---------|
| User Management | UM | REQ-UM-001 |
| Data Processing | DP | REQ-DP-001 |
| Reporting | RP | REQ-RP-001 |
| Integration | IN | REQ-IN-001 |
| Workflow | WF | REQ-WF-001 |

### Non-Functional Requirements

Format: `NFR-[Category]-[Number]`

| Category | Code | Example |
|----------|------|---------|
| Performance | PF | NFR-PF-001 |
| Security | SC | NFR-SC-001 |
| Reliability | RL | NFR-RL-001 |
| Usability | US | NFR-US-001 |
| Scalability | SL | NFR-SL-001 |
| Maintainability | MT | NFR-MT-001 |

---

## ACCEPTANCE CRITERIA STANDARDS

### Format: Given-When-Then

```
Given [precondition/context]
When [action/trigger]
Then [expected outcome]
```

### Example

```markdown
## REQ-UM-001: User Login

### Acceptance Criteria

**AC-1:** Successful login
Given a registered user with valid credentials
When the user submits username and password
Then the system shall authenticate the user and redirect to dashboard

**AC-2:** Invalid credentials
Given a user with invalid credentials
When the user submits incorrect username or password
Then the system shall display "Invalid credentials" message
And the system shall not authenticate the user

**AC-3:** Account locked
Given a user who has failed login 5 times
When the user attempts another login
Then the system shall display "Account locked" message
And the system shall not allow further attempts for 30 minutes
```

---

## TRACEABILITY STANDARDS

### Forward Traceability

Every requirement MUST trace forward to:
- Design component(s)
- Test case(s)
- Implementation artifact(s)

### Backward Traceability

Every requirement MUST trace backward to:
- Source (stakeholder, regulation, standard)
- Business objective
- Concept document reference

### RTM Requirements

The Requirements Traceability Matrix MUST include:

| Column | Required | Description |
|--------|----------|-------------|
| REQ ID | ✓ | Unique identifier |
| Title | ✓ | Brief description |
| Source | ✓ | Where requirement came from |
| Priority | ✓ | MoSCoW classification |
| Status | ✓ | Draft/Review/Approved/Implemented |
| Design Ref | ✓ | Link to design artifact |
| Test Ref | ✓ | Link to test case |
| Owner | ✓ | Responsible party |

---

## PRIORITIZATION STANDARDS

### MoSCoW Definitions

| Priority | Definition | Criteria | % of Scope |
|----------|------------|----------|------------|
| Must | Essential | System cannot function without | 60% max |
| Should | Important | High value but workarounds exist | 20% |
| Could | Desirable | Enhances system but not critical | 10% |
| Won't | Not now | Explicitly excluded this release | 10% |

### Prioritization Rules

1. No more than 60% of requirements can be "Must"
2. "Must" requirements define MVP
3. "Won't" items must be documented (not deleted)
4. Priority can only change through change control

---

## VERSION CONTROL STANDARDS

### Versioning Scheme

`[Major].[Minor]`

- **Major**: Significant scope changes
- **Minor**: Clarifications, corrections

### Change Tracking

Every change must record:

```markdown
## Change Record

**REQ ID:** [ID]
**Version:** [From] → [To]
**Date:** [Date]
**Changed By:** [Name]

**Previous:**
[Previous text]

**Current:**
[New text]

**Reason:**
[Why changed]

**Impact:**
[What else is affected]
```

---

## REVIEW STANDARDS

### Review Checklist

Each requirement must pass:

- [ ] Unique ID assigned
- [ ] Source documented
- [ ] Priority assigned
- [ ] Acceptance criteria defined
- [ ] No ambiguous language
- [ ] No compound statements
- [ ] Testable/verifiable
- [ ] No conflicts with other requirements
- [ ] Within scope boundaries
- [ ] Feasible within constraints

### Review Roles

| Role | Responsibility |
|------|----------------|
| Author | Write requirements, address comments |
| Reviewer | Check quality, identify issues |
| Approver | Final sign-off authority |

### Review Meeting Rules

1. Maximum 2 hours per session
2. Maximum 20 requirements per session
3. All issues documented
4. Follow-up required within 48 hours

---

## NON-FUNCTIONAL REQUIREMENTS STANDARDS

### Performance Requirements

MUST specify:
- Response time (with percentile: p50, p95, p99)
- Throughput (transactions per second)
- Concurrent users
- Data volume

### Security Requirements

MUST reference:
- OWASP Top 10 coverage
- Authentication requirements
- Authorization model
- Encryption standards
- Audit logging requirements

### Reliability Requirements

MUST specify:
- Availability target (e.g., 99.9%)
- Recovery Time Objective (RTO)
- Recovery Point Objective (RPO)
- Mean Time Between Failures (MTBF)

---

## GLOSSARY STANDARDS

Every requirements document MUST include glossary with:

```markdown
## Glossary

| Term | Definition | Source |
|------|------------|--------|
| [Term] | [Clear definition] | [Authority] |
```

- All domain terms defined
- All acronyms expanded
- All technical terms explained

---

*STANDARDS v1.0 | PHASE 03 | Gold Standard System*
