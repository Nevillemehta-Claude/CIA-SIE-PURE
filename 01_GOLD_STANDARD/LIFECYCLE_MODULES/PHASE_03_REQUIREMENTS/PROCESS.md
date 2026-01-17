# PHASE 03: REQUIREMENTS ANALYSIS
## Process Guide

**Purpose:** Step-by-step process for eliciting, analyzing, and documenting requirements

---

## PROCESS OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 3 PROCESS FLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1          STEP 2          STEP 3          STEP 4    │
│  ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐    │
│  │Elicit│──────▶│Analyze│─────▶│Specify│──────▶│Validate│  │
│  │      │       │       │       │       │       │        │  │
│  └──────┘       └──────┘       └──────┘       └──────┘    │
│                                                             │
│  Methods:       Activities:    Outputs:       Reviews:     │
│  - Interviews   - Decompose    - REQ specs    - Walkthrough│
│  - Workshops    - Prioritize   - NFRs         - Sign-off   │
│  - Observation  - Categorize   - Acceptance   - Trace      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## STEP 1: ELICIT REQUIREMENTS

### 1.1 Preparation

Before elicitation:
- [ ] Review concept document from Phase 2
- [ ] Identify stakeholders to interview
- [ ] Prepare interview guides
- [ ] Schedule sessions
- [ ] Prepare recording method

### 1.2 Elicitation Techniques

**Interviews:**
```markdown
## Interview Record

**Interviewee:** [Name/Role]
**Date:** [Date]
**Interviewer:** [Name]

### Questions Asked
1. [Question 1]
   Response: [Summary]

2. [Question 2]
   Response: [Summary]

### Requirements Identified
- [REQ-XXX]: [Requirement statement]
- [REQ-XXX]: [Requirement statement]

### Follow-up Needed
- [ ] [Item 1]
```

**Workshops:**
```markdown
## Workshop Record

**Topic:** [Workshop focus]
**Date:** [Date]
**Participants:** [List]
**Facilitator:** [Name]

### Agenda
1. [Topic 1] - [Duration]
2. [Topic 2] - [Duration]

### Outputs
- Requirements identified: [Count]
- Decisions made: [List]
- Open items: [List]

### Artifacts Created
- [Artifact 1]
- [Artifact 2]
```

**Observation:**
- Shadow users in their environment
- Document current workflows
- Note pain points and workarounds
- Identify implicit requirements

### 1.3 Document Raw Requirements

Capture everything, filter later:

```markdown
## Raw Requirement

**Source:** [Interview/Workshop/Observation/Document]
**Date:** [Date]
**Captured By:** [Name]

**Raw Statement:**
"[Exact words from stakeholder]"

**Context:**
[Situation in which this was stated]

**Initial Category:** [Functional/Non-Functional/Constraint]
```

---

## STEP 2: ANALYZE REQUIREMENTS

### 2.1 Decomposition

Break complex requirements into atomic units:

**Before (Complex):**
> "The system should manage user accounts including registration, login, password reset, and profile management."

**After (Atomic):**
- REQ-001: User registration
- REQ-002: User login
- REQ-003: Password reset
- REQ-004: Profile management

### 2.2 Categorization

Categorize each requirement:

| Category | Description | Examples |
|----------|-------------|----------|
| Functional | What system does | Process order, Calculate total |
| Non-Functional | How system performs | Response time, Availability |
| Constraint | Limitations | Must use PostgreSQL, Budget $X |
| Interface | External connections | API format, File import |

### 2.3 Prioritization

Use MoSCoW method:

| Priority | Meaning | Criteria |
|----------|---------|----------|
| Must | Essential | System fails without it |
| Should | Important | Significant value, not critical |
| Could | Desirable | Nice to have if time permits |
| Won't | Excluded | Not this release |

### 2.4 Dependency Analysis

Map requirement dependencies:

```markdown
## Dependency Map

REQ-001: User Registration
├── Depends on: None (root requirement)
└── Depended by: REQ-002, REQ-003, REQ-004

REQ-002: User Login
├── Depends on: REQ-001
└── Depended by: REQ-005, REQ-006

REQ-003: Password Reset
├── Depends on: REQ-001, REQ-002
└── Depended by: None
```

---

## STEP 3: SPECIFY REQUIREMENTS

### 3.1 Functional Requirement Format

```markdown
## REQ-[NUMBER]: [Title]

**Type:** Functional
**Priority:** Must | Should | Could
**Source:** [Stakeholder/Document reference]
**Version:** [X.Y]

### Statement
The system shall [action] [object] [condition].

### Rationale
[Why this requirement exists]

### Acceptance Criteria
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

### Dependencies
- Depends on: [REQ-XXX]
- Required by: [REQ-XXX]

### Notes
[Additional context or clarifications]
```

### 3.2 Non-Functional Requirement Format

```markdown
## NFR-[NUMBER]: [Title]

**Category:** Performance | Security | Reliability | Usability | Scalability
**Priority:** Must | Should | Could
**Source:** [Stakeholder/Standard reference]

### Statement
The system shall [quality attribute] [measurable target] [conditions].

### Measurement
- Metric: [What to measure]
- Target: [Specific value]
- Method: [How to measure]

### Rationale
[Why this NFR matters]

### Verification
[How to verify compliance]
```

### 3.3 Create Requirements Traceability Matrix (RTM)

| REQ ID | Requirement | Source | Priority | Design | Test | Status |
|--------|-------------|--------|----------|--------|------|--------|
| REQ-001 | [Summary] | [Source] | Must | [Link] | [Link] | Draft |
| REQ-002 | [Summary] | [Source] | Should | [Link] | [Link] | Draft |

---

## STEP 4: VALIDATE REQUIREMENTS

### 4.1 Requirements Walkthrough

Conduct structured review:

```markdown
## Requirements Walkthrough

**Date:** [Date]
**Document Reviewed:** [Document name/version]
**Participants:** [List]

### Review Results

| REQ ID | Status | Comments |
|--------|--------|----------|
| REQ-001 | Approved | None |
| REQ-002 | Modified | Changed priority to Must |
| REQ-003 | Rejected | Out of scope |

### Issues Identified
1. [Issue 1] - Resolution: [How resolved]
2. [Issue 2] - Resolution: [How resolved]

### Sign-off
| Reviewer | Role | Signature | Date |
|----------|------|-----------|------|
| [Name] | [Role] | _________ | [Date] |
```

### 4.2 Quality Checks

Verify each requirement is:

- [ ] **Complete** - All necessary information included
- [ ] **Consistent** - No conflicts with other requirements
- [ ] **Correct** - Accurately represents stakeholder need
- [ ] **Unambiguous** - Only one interpretation possible
- [ ] **Verifiable** - Can be tested or measured
- [ ] **Traceable** - Source identified, forward links planned
- [ ] **Feasible** - Achievable within constraints
- [ ] **Necessary** - Adds value, not gold-plating

### 4.3 Stakeholder Sign-off

Obtain formal approval:

```markdown
## Requirements Sign-off

**Document:** Requirements Specification v[X.Y]
**Date:** [Date]

I have reviewed the requirements specification and confirm:
- [ ] Requirements accurately represent my needs
- [ ] Requirements are complete for this phase
- [ ] I approve proceeding to Phase 4 (Architecture)

| Stakeholder | Role | Signature | Date |
|-------------|------|-----------|------|
| [Name] | Product Owner | _________ | [Date] |
| [Name] | Technical Lead | _________ | [Date] |
| [Name] | Business Rep | _________ | [Date] |
```

---

## DELIVERABLES CHECKLIST

- [ ] Requirements Specification Document
- [ ] Requirements Traceability Matrix (initial)
- [ ] Non-Functional Requirements Document
- [ ] Glossary of Terms
- [ ] Stakeholder Sign-off Record

---

*PROCESS v1.0 | PHASE 03 | Gold Standard System*
