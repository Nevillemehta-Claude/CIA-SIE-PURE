# LIFECYCLE DEFINITION
## The Complete Development Pathway

**Classification:** COMMAND_PROTOCOL
**Version:** 1.0
**Applicability:** All Software Development Projects

---

## OVERVIEW

This document defines the complete lifecycle from initial idea to operational system. Each phase is a self-contained module with defined entry criteria, activities, verification requirements, and exit criteria.

**Pathway Structure:**
```
IDEA ──► Phase 1-3: CONCEPTION ──► Phase 4-5: DESIGN ──► Phase 6-7: CONSTRUCTION ──► Phase 8-10: DELIVERY ──► Phase 11: OPERATION
```

---

## THE ELEVEN PHASES

| # | Phase | Purpose | Key Outcome |
|---|-------|---------|-------------|
| 1 | IDEATION | Capture the initial concept | Idea Statement |
| 2 | CONCEPT CRYSTALLIZATION | Refine idea into definite shape | Concept Document |
| 3 | REQUIREMENTS ANALYSIS | Define what must be built | Requirements Specification |
| 4 | ARCHITECTURE DESIGN | Define how it will be structured | Architecture Document |
| 5 | SPECIFICATION | Define precise behaviors | Technical Specification |
| 6 | DEVELOPMENT | Build the components | Working Code |
| 7 | INTEGRATION | Connect the components | Integrated System |
| 8 | VERIFICATION | Prove it works | Test Reports |
| 9 | DOCUMENTATION | Record what was built | Complete Documentation |
| 10 | DEPLOYMENT | Release to production | Deployed System |
| 11 | OPERATIONS | Maintain and evolve | Operational Excellence |

---

## PHASE DEPENDENCIES

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   CONCEPTION STREAM                                                     │
│   ┌──────────┐    ┌──────────────┐    ┌─────────────┐                  │
│   │ Phase 1  │───►│   Phase 2    │───►│   Phase 3   │                  │
│   │ Ideation │    │   Concept    │    │Requirements │                  │
│   └──────────┘    └──────────────┘    └──────┬──────┘                  │
│                                              │                          │
│   DESIGN STREAM                              │                          │
│                                              ▼                          │
│                              ┌──────────────────────────┐               │
│                              │       Phase 4            │               │
│                              │   Architecture Design    │               │
│                              └────────────┬─────────────┘               │
│                                           │                             │
│                                           ▼                             │
│                              ┌──────────────────────────┐               │
│                              │       Phase 5            │               │
│                              │    Specification         │               │
│                              └────────────┬─────────────┘               │
│                                           │                             │
│   CONSTRUCTION STREAM                     │                             │
│                                           ▼                             │
│                              ┌──────────────────────────┐               │
│                              │       Phase 6            │               │
│                              │     Development          │               │
│                              └────────────┬─────────────┘               │
│                                           │                             │
│                                           ▼                             │
│                              ┌──────────────────────────┐               │
│                              │       Phase 7            │               │
│                              │     Integration          │               │
│                              └────────────┬─────────────┘               │
│                                           │                             │
│   DELIVERY STREAM                         │                             │
│                                           ▼                             │
│            ┌──────────────────────────────────────────────────┐         │
│            │                    Phase 8                        │         │
│            │                 Verification                      │         │
│            └────────────────────────┬─────────────────────────┘         │
│                                     │                                   │
│            ┌────────────────────────┼────────────────────────┐          │
│            ▼                        ▼                        ▼          │
│   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐        │
│   │    Phase 9     │    │   Phase 10     │    │   Phase 11     │        │
│   │ Documentation  │    │  Deployment    │───►│  Operations    │        │
│   └────────────────┘    └────────────────┘    └────────────────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: IDEATION

**Purpose:** Capture the initial spark of an idea

### Entry Criteria
- A need or opportunity has been identified
- Principal is ready to articulate the concept

### Activities
1. Express the core idea in plain language
2. Identify the problem being solved
3. Describe the desired outcome
4. Note any initial constraints

### Deliverables
- Idea Statement (1-2 paragraphs)
- Problem Statement
- Success Criteria (high-level)

### Exit Criteria
- [ ] Idea clearly articulated
- [ ] Problem identified
- [ ] Value proposition stated
- [ ] Principal confirms: "This is what I want to explore"

### Playbook Location
`LIFECYCLE_MODULES/PHASE_01_IDEATION/`

---

## PHASE 2: CONCEPT CRYSTALLIZATION

**Purpose:** Transform the idea into a defined concept

### Entry Criteria
- Phase 1 complete
- Idea Statement approved

### Activities
1. Expand idea into detailed concept
2. Define scope (what's in, what's out)
3. Identify major components
4. Identify risks and dependencies
5. Refine success criteria

### Deliverables
- Concept Document
- Scope Definition
- Risk Register (initial)
- Success Criteria (refined)

### Exit Criteria
- [ ] Concept fully described
- [ ] Boundaries clearly defined
- [ ] Major components identified
- [ ] Principal confirms: "This is the shape of what we're building"

### Playbook Location
`LIFECYCLE_MODULES/PHASE_02_CONCEPT/`

---

## PHASE 3: REQUIREMENTS ANALYSIS

**Purpose:** Define exactly what the system must do

### Entry Criteria
- Phase 2 complete
- Concept Document approved

### Activities
1. Elicit all requirements (functional, non-functional)
2. Document each requirement with unique ID
3. Prioritize requirements (must/should/could)
4. Validate requirements with stakeholders
5. Establish traceability baseline

### Deliverables
- Requirements Specification
- Requirements Traceability Matrix (initial)
- Acceptance Criteria per requirement

### Exit Criteria
- [ ] All requirements documented with IDs
- [ ] Each requirement has acceptance criteria
- [ ] Requirements reviewed and approved
- [ ] Traceability matrix established

### Playbook Location
`LIFECYCLE_MODULES/PHASE_03_REQUIREMENTS/`

---

## PHASE 4: ARCHITECTURE DESIGN

**Purpose:** Define how the system will be structured

### Entry Criteria
- Phase 3 complete
- Requirements Specification approved

### Activities
1. Define system boundaries (C4 Context)
2. Identify containers (C4 Container)
3. Design components (C4 Component)
4. Define integration points and contracts
5. Address non-functional requirements (security, performance, scalability)
6. Document architectural decisions (ADRs)

### Deliverables
- Architecture Document
- C4 Diagrams (Context, Container, Component)
- Integration Contracts
- Architectural Decision Records
- Security Architecture

### Exit Criteria
- [ ] System structure fully defined
- [ ] All containers and components identified
- [ ] Integration points specified
- [ ] Security architecture addressed
- [ ] Architecture reviewed and approved

### Playbook Location
`LIFECYCLE_MODULES/PHASE_04_ARCHITECTURE/`

---

## PHASE 5: SPECIFICATION

**Purpose:** Define precise behaviors for every component

### Entry Criteria
- Phase 4 complete
- Architecture Document approved

### Activities
1. Write detailed specifications for each component
2. Define API contracts (OpenAPI)
3. Define data models and schemas
4. Document business logic algorithms
5. Specify error handling and edge cases
6. Create interface control documents

### Deliverables
- Technical Specification
- API Specification (OpenAPI)
- Data Model Specification
- Business Logic Specification
- Interface Control Documents

### Exit Criteria
- [ ] Every component fully specified
- [ ] API contracts complete and validated
- [ ] Data models defined
- [ ] Business logic documented
- [ ] Specifications reviewed and approved

### Playbook Location
`LIFECYCLE_MODULES/PHASE_05_SPECIFICATION/`

---

## PHASE 6: DEVELOPMENT

**Purpose:** Build the components according to specification

### Entry Criteria
- Phase 5 complete
- Technical Specification approved
- Development environment ready
- Test strategy defined

### Activities
1. Implement components per specification
2. Write unit tests for each function
3. Write contract tests for each interface
4. Conduct code reviews
5. Maintain continuous integration

### Deliverables
- Source Code
- Unit Tests
- Contract Tests
- Code Review Records
- CI/CD Pipeline

### Verification Layers (Active)
- Syntax (every save)
- Static Analysis (every commit)
- Unit (every function)
- Contract (every interface)
- Regression (every merge)

### Exit Criteria
- [ ] All components implemented
- [ ] Unit tests passing (>90% coverage)
- [ ] Contract tests passing
- [ ] Code reviews complete
- [ ] No critical/high static analysis issues

### Playbook Location
`LIFECYCLE_MODULES/PHASE_06_DEVELOPMENT/`

---

## PHASE 7: INTEGRATION

**Purpose:** Connect components into a working system

### Entry Criteria
- Phase 6 complete for components being integrated
- Component-level tests passing

### Activities
1. Connect components via defined interfaces
2. Verify integration contracts
3. Test component interactions
4. Resolve integration conflicts
5. Conduct integration testing

### Deliverables
- Integrated System
- Integration Test Suite
- Integration Test Reports
- Resolved Conflict Log

### Verification Layers (Active)
- Contract (interfaces)
- Integration (component interaction)
- Functional (features)
- Regression (full suite)

### Exit Criteria
- [ ] All components integrated
- [ ] Integration tests passing
- [ ] No orphaned endpoints
- [ ] No phantom features
- [ ] System runs end-to-end

### Playbook Location
`LIFECYCLE_MODULES/PHASE_07_INTEGRATION/`

---

## PHASE 8: VERIFICATION

**Purpose:** Prove the system works as specified

### Entry Criteria
- Phase 7 complete
- Integrated system running
- Test environment ready

### Activities
1. Execute full test pyramid
2. Conduct performance testing
3. Conduct security testing
4. Verify requirements traceability
5. Conduct user acceptance testing
6. Document all test results

### Deliverables
- Test Execution Reports
- Performance Test Results
- Security Audit Report
- Requirements Traceability Matrix (complete)
- UAT Sign-off

### Verification Layers (All Active)
- All layers verified
- Coverage targets met
- Performance targets met
- Security audit passed

### Exit Criteria
- [ ] All tests passing
- [ ] Coverage targets met
- [ ] Performance within bounds
- [ ] Security vulnerabilities remediated
- [ ] UAT approved

### Playbook Location
`LIFECYCLE_MODULES/PHASE_08_VERIFICATION/`

---

## PHASE 9: DOCUMENTATION

**Purpose:** Ensure complete, accurate documentation

### Entry Criteria
- Phase 8 complete
- System verified

### Activities
1. Finalize technical documentation
2. Create user documentation
3. Create operational runbooks
4. Update API documentation
5. Verify documentation accuracy against implementation

### Deliverables
- Technical Documentation
- User Guide
- Operational Runbooks
- API Documentation
- Troubleshooting Guide

### Verification
- Documentation matches implementation
- All public interfaces documented
- Runbooks tested by operations team

### Exit Criteria
- [ ] Documentation complete
- [ ] Documentation accurate
- [ ] Runbooks validated
- [ ] Documentation reviewed and approved

### Playbook Location
`LIFECYCLE_MODULES/PHASE_09_DOCUMENTATION/`

---

## PHASE 10: DEPLOYMENT

**Purpose:** Release the system to production

### Entry Criteria
- Phase 8 and 9 complete
- Deployment environment ready
- Rollback procedure defined

### Activities
1. Prepare deployment package
2. Execute deployment procedure
3. Verify deployment success
4. Conduct smoke tests
5. Monitor initial operation
6. Confirm rollback readiness

### Deliverables
- Deployed System
- Deployment Log
- Smoke Test Results
- Go-Live Confirmation

### Verification
- Deployment successful
- Smoke tests pass
- Monitoring active
- Rollback procedure tested

### Exit Criteria
- [ ] System deployed successfully
- [ ] Smoke tests passing
- [ ] Monitoring configured
- [ ] Stakeholders notified
- [ ] Production sign-off received

### Playbook Location
`LIFECYCLE_MODULES/PHASE_10_DEPLOYMENT/`

---

## PHASE 11: OPERATIONS

**Purpose:** Maintain and continuously improve the system

### Entry Criteria
- Phase 10 complete
- System in production

### Activities
1. Monitor system health
2. Respond to incidents
3. Apply patches and updates
4. Conduct periodic reviews
5. Plan improvements
6. Return to Phase 1 for new features

### Deliverables
- Operational Metrics
- Incident Reports
- Change Records
- Improvement Plans

### Ongoing Verification
- Health monitoring
- Performance tracking
- Security scanning
- Audit logging

### Transition Criteria
- New feature → Return to Phase 1
- Major change → Return to Phase 3 or 4
- Bug fix → Return to Phase 6

### Playbook Location
`LIFECYCLE_MODULES/PHASE_11_OPERATIONS/`

---

## ITERATION AND FEEDBACK

The lifecycle is not strictly linear. Feedback loops exist:

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  During any phase, discovery may require returning       │
│  to an earlier phase:                                    │
│                                                          │
│  • Requirements gap found → Return to Phase 3            │
│  • Architecture flaw found → Return to Phase 4           │
│  • Specification ambiguity → Return to Phase 5           │
│  • Integration failure → Return to Phase 6               │
│                                                          │
│  The rule: Return to the EARLIEST affected phase         │
│  and proceed forward again.                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## USING THE LIFECYCLE

### Starting a New Project
1. Read GENESIS.md
2. Begin at Phase 1
3. Load Phase 1 playbook
4. Execute phase activities
5. Satisfy exit criteria
6. Proceed to Phase 2
7. Repeat until Phase 11

### Resuming Work
1. Identify current phase
2. Load relevant playbook
3. Review entry criteria (were they met?)
4. Continue phase activities
5. Satisfy exit criteria
6. Proceed to next phase

### Handling Setbacks
1. Identify the root cause
2. Determine which phase is affected
3. Return to that phase
4. Re-execute from that point
5. Proceed forward again

---

## QUICK REFERENCE

| Current Activity | You're In |
|-----------------|-----------|
| Discussing what to build | Phase 1-2 |
| Defining what it must do | Phase 3 |
| Designing how it's structured | Phase 4 |
| Specifying precise behaviors | Phase 5 |
| Writing code | Phase 6 |
| Connecting components | Phase 7 |
| Testing everything | Phase 8 |
| Finalizing documentation | Phase 9 |
| Releasing to production | Phase 10 |
| Running in production | Phase 11 |

---

*LIFECYCLE DEFINITION v1.0 | COMMAND_PROTOCOL | Gold Standard System*
