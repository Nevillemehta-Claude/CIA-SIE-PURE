# PHASE 04: ARCHITECTURE DESIGN
## Briefing Document

**Phase Number:** 4
**Phase Name:** Architecture Design
**Purpose:** Define the structural solution to meet requirements

---

## WHAT THIS PHASE IS

Architecture Design creates the blueprint for the system. It defines how components are organized, how they communicate, and how the system achieves its quality attributes. Architecture decisions made here constrain all subsequent design and implementation work.

**Key Insight:** Architecture is about the decisions that are expensive to change later. Get these right first, because reversing them costs orders of magnitude more than getting them right initially.

---

## WHAT YOU'RE DOING

1. **Defining system structure** - Components, layers, boundaries
2. **Designing communication patterns** - How components interact
3. **Selecting architectural styles** - Monolith, microservices, event-driven, etc.
4. **Addressing quality attributes** - Performance, scalability, security, maintainability
5. **Identifying architectural risks** - What could go wrong at scale
6. **Documenting architectural decisions** - ADRs for significant choices

---

## WHAT YOU'RE NOT DOING

- Detailed class design (that's Phase 5)
- Implementation details (that's Phase 6)
- Technology selection without justification
- Premature optimization

**This phase answers HOW (structurally), not WHAT (that was Phase 3).**

---

## ARCHITECTURE VIEWS

### The C4 Model

Architecture documentation uses the C4 model for consistent visualization:

| Level | View | Audience | Shows |
|-------|------|----------|-------|
| **L1** | Context | Everyone | System + external actors |
| **L2** | Container | Technical | Applications, data stores, services |
| **L3** | Component | Developers | Components within containers |
| **L4** | Code | Developers | Class/module structure |

**Phase 4 focuses on L1 (Context) and L2 (Container).** L3 and L4 are addressed in Phase 5.

---

## ARCHITECTURE DECISION RECORDS

Every significant architectural decision is documented in an ADR:

```markdown
# ADR-[NUMBER]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the situation? What forces are at play?]

## Decision
[What architectural decision was made?]

## Consequences
[What are the results? Both positive and negative.]

## Alternatives Considered
[What other options were evaluated?]
```

### Example ADR

```markdown
# ADR-001: Monolithic Architecture for MVP

## Status
Accepted

## Context
Building an MVP with a team of 2 developers. Need to ship in 8 weeks.
Requirements include user management, data processing, and reporting.
Team has strong experience with Django.

## Decision
Use monolithic Django architecture for the MVP release.

## Consequences
**Positive:**
- Faster development velocity
- Simpler deployment
- Easier debugging
- Team expertise leveraged

**Negative:**
- Scaling limits (acceptable for MVP)
- Larger deployment unit
- Potential for tight coupling

## Alternatives Considered
1. **Microservices** - Rejected due to operational overhead for small team
2. **Serverless** - Rejected due to cold start concerns and vendor lock-in
```

---

## ARCHITECTURAL PATTERNS

### Structural Patterns

| Pattern | Use When | Trade-offs |
|---------|----------|------------|
| **Layered** | Clear separation of concerns | Can become over-engineered |
| **Hexagonal** | High testability needed | More initial complexity |
| **Microservices** | Independent scaling/deployment | Operational overhead |
| **Event-Driven** | Loose coupling, async processing | Eventual consistency |
| **Monolith** | Small team, MVP, unclear boundaries | Scaling limits |

### Communication Patterns

| Pattern | Use When | Trade-offs |
|---------|----------|------------|
| **Synchronous REST** | Simple request/response | Coupling, latency chains |
| **Async Messaging** | Decoupled processing | Complexity, eventual consistency |
| **Event Sourcing** | Audit trail, replay capability | Storage, complexity |
| **CQRS** | Read/write scaling differs | Dual models to maintain |

---

## QUALITY ATTRIBUTE SCENARIOS

For each quality attribute, define testable scenarios:

```markdown
## Quality Attribute: [Name]

**Scenario:** [Stimulus] → [Response] under [Conditions]

**Stimulus:** [What triggers the scenario]
**Environment:** [System state when stimulus occurs]
**Response:** [What the system does]
**Measure:** [How we verify the response]
```

### Example

```markdown
## Quality Attribute: Performance

**Scenario:** 1000 concurrent users → <200ms response time under normal load

**Stimulus:** 1000 concurrent users request dashboard
**Environment:** Normal operation, all services healthy
**Response:** Dashboard data returned
**Measure:** 95th percentile response time < 200ms
```

---

## ARCHITECTURE DELIVERABLES

| Deliverable | Description |
|-------------|-------------|
| Context Diagram (C4 L1) | System in its environment |
| Container Diagram (C4 L2) | High-level technical architecture |
| Quality Attribute Scenarios | Testable quality requirements |
| ADRs | Documented architectural decisions |
| Risk Assessment | Identified architectural risks |
| Technology Selection | Justified technology choices |

---

## COMMON PITFALLS

### 1. Resume-Driven Architecture
**Problem:** Choosing technology because it looks good on a resume
**Fix:** Technology choices must be justified by requirements

### 2. Over-Engineering for Scale
**Problem:** Building for 1M users when you have 100
**Fix:** Design for current needs with evolution path documented

### 3. Under-Documented Decisions
**Problem:** "We just decided to use microservices"
**Fix:** Every significant decision has an ADR with rationale

### 4. Ignoring Quality Attributes
**Problem:** Focus only on functional requirements
**Fix:** Architecture addresses -ilities (scalability, maintainability, etc.)

### 5. Big Bang Architecture
**Problem:** Trying to design everything upfront
**Fix:** Architecture is iterative; document known decisions, defer others

---

## EXIT CRITERIA

Phase 4 is complete when:

- [ ] Context diagram (C4 L1) created
- [ ] Container diagram (C4 L2) created
- [ ] All significant decisions documented as ADRs
- [ ] Quality attribute scenarios defined
- [ ] Architectural risks identified
- [ ] Technology selections justified
- [ ] Architecture reviewed and approved

---

## NEXT STEPS

After completing this phase:
1. Architecture reviewed by technical stakeholders
2. ADRs approved
3. Proceed to Phase 5: Detailed Specification
4. Load `LIFECYCLE_MODULES/PHASE_05_SPECIFICATION/`

---

*PHASE 04 BRIEFING v1.0 | LIFECYCLE_MODULES | Gold Standard System*
