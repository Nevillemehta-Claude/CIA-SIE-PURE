# PHASE 04: ARCHITECTURE DESIGN
## Standards

**Purpose:** Quality standards for architecture documentation and design decisions

---

## C4 MODEL STANDARDS

### Level 1: Context Diagram Requirements

MUST include:
- [ ] System boundary clearly marked
- [ ] All user types/roles identified
- [ ] All external systems shown
- [ ] Relationship descriptions on arrows
- [ ] Legend explaining notation

MUST NOT include:
- Internal system details
- Technology choices
- Database details

### Level 2: Container Diagram Requirements

MUST include:
- [ ] All containers within system boundary
- [ ] Technology/platform for each container
- [ ] Communication protocols between containers
- [ ] Data flow direction
- [ ] External system connections

Container naming:
- Use descriptive names (not "Service A")
- Include technology in parentheses
- Example: "API Gateway (Kong)"

### Level 3: Component Diagram (When Needed)

Used when:
- Container is complex
- Multiple teams work on same container
- Detailed design review needed

---

## DIAGRAM STANDARDS

### General Rules

| Rule | Standard |
|------|----------|
| Direction | Top-to-bottom or left-to-right |
| Crossing Lines | Minimize; use bridges if unavoidable |
| Spacing | Consistent spacing between elements |
| Font | Readable at 100% zoom |
| Colors | Consistent meaning across diagrams |

### Color Coding Standard

| Color | Meaning |
|-------|---------|
| Blue | Internal system/container |
| Gray | External system |
| Green | Database/storage |
| Orange | Message queue/async |
| Purple | User/actor |

### Arrow Standards

| Arrow Type | Meaning |
|------------|---------|
| Solid → | Synchronous call |
| Dashed --> | Asynchronous call |
| Double ⟷ | Bidirectional |

Label format: `[Protocol]: [Description]`
Example: `HTTPS: Submit order`

---

## ADR (ARCHITECTURE DECISION RECORD) STANDARDS

### When to Create ADR

Create an ADR when:
- [ ] Technology selection made
- [ ] Architecture pattern chosen
- [ ] Significant trade-off accepted
- [ ] Standard/convention established
- [ ] Previous decision reversed

### ADR Numbering

Format: `ADR-[NNNN]`
- Sequential numbering
- Never reuse numbers
- Mark superseded ADRs (don't delete)

### Required Sections

| Section | Required | Purpose |
|---------|----------|---------|
| Status | ✓ | Current state |
| Date | ✓ | When decided |
| Context | ✓ | Why needed |
| Decision | ✓ | What chosen |
| Consequences | ✓ | Impact |
| Alternatives | ✓ | What rejected |

### Status Values

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion |
| Accepted | Approved, in effect |
| Deprecated | No longer recommended |
| Superseded | Replaced by newer ADR |

---

## TECHNOLOGY SELECTION STANDARDS

### Evaluation Criteria (Mandatory)

Every technology selection MUST evaluate:

| Criterion | Description |
|-----------|-------------|
| Functional Fit | Does it meet requirements? |
| Performance | Does it meet NFRs? |
| Scalability | Can it grow with us? |
| Security | Are there vulnerabilities? |
| Team Skills | Can team use it effectively? |
| Community | Is there support/ecosystem? |
| License | Are terms acceptable? |
| Cost | TCO acceptable? |

### Scoring Standard

| Score | Meaning |
|-------|---------|
| 5 | Excellent - exceeds needs |
| 4 | Good - meets all needs |
| 3 | Adequate - meets most needs |
| 2 | Poor - significant gaps |
| 1 | Unacceptable - fails needs |

### Documentation Requirements

Every technology selection MUST document:
- Options considered (minimum 2)
- Evaluation matrix with scores
- Final recommendation with rationale
- Dissenting opinions (if any)

---

## CONTAINER SPECIFICATION STANDARDS

### Container Definition Template

```markdown
## Container: [Name]

**ID:** CTN-[NNN]
**Type:** [Web App | API | Database | Queue | Storage]
**Technology:** [Specific tech with version]

### Purpose
[Single paragraph describing what this container does]

### Responsibilities
1. [Responsibility 1]
2. [Responsibility 2]

### Does NOT Handle
1. [What this container does NOT do]

### Interfaces

#### Inbound
| Interface | Protocol | Port | Authentication |
|-----------|----------|------|----------------|
| [Name] | [Protocol] | [Port] | [Auth method] |

#### Outbound
| Target | Protocol | Purpose |
|--------|----------|---------|
| [Container/System] | [Protocol] | [What for] |

### Data
| Data Type | Storage | Retention |
|-----------|---------|-----------|
| [Type] | [Where] | [How long] |

### Scaling
- Horizontal: [Yes/No] - [How]
- Vertical: [Limits]

### Health Check
- Endpoint: [Path]
- Expected: [Response]
```

---

## CROSS-CUTTING CONCERNS STANDARDS

Every architecture MUST address:

### Security
- [ ] Authentication mechanism defined
- [ ] Authorization model documented
- [ ] Data encryption (at rest, in transit)
- [ ] Secrets management approach
- [ ] Security logging requirements

### Observability
- [ ] Logging strategy (what, where, format)
- [ ] Metrics to collect
- [ ] Distributed tracing approach
- [ ] Alerting strategy

### Error Handling
- [ ] Error response format
- [ ] Error categorization
- [ ] Retry strategies
- [ ] Circuit breaker patterns

### Configuration
- [ ] Configuration management approach
- [ ] Environment-specific config
- [ ] Feature flags (if used)
- [ ] Secrets injection

---

## ARCHITECTURE REVIEW STANDARDS

### Review Checklist

| Category | Check |
|----------|-------|
| Completeness | All requirements have design |
| Consistency | Patterns applied uniformly |
| Clarity | Diagrams understandable |
| Decisions | All major decisions recorded |
| Risks | Risks identified and mitigated |
| Feasibility | Design is implementable |
| Testability | Design supports testing |

### Review Roles

| Role | Responsibility |
|------|----------------|
| Architect | Present and defend design |
| Senior Developer | Validate implementability |
| Security | Review security aspects |
| Operations | Review operational concerns |

### Review Outcomes

| Outcome | Next Step |
|---------|-----------|
| Approved | Proceed to Phase 5 |
| Approved with changes | Address changes, re-review |
| Major revision | Redesign, full re-review |
| Rejected | Return to Phase 3 |

---

## VERSION CONTROL

### Architecture Document Versioning

- Major: Significant structural changes
- Minor: Clarifications, additions

### Change Tracking

All changes must record:
- What changed
- Why it changed
- Who approved
- Impact on other artifacts

---

*STANDARDS v1.0 | PHASE 04 | Gold Standard System*
