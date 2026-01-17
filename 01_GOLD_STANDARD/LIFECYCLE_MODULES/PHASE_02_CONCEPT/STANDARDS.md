# PHASE 02: CONCEPT CRYSTALLIZATION
## Standards

**Purpose:** Quality standards and templates for concept phase artifacts

---

## DOCUMENT STANDARDS

### Concept Document Requirements

Every concept document MUST include:

| Section | Required | Description |
|---------|----------|-------------|
| Executive Summary | ✓ | 2-3 paragraphs max |
| Problem Statement | ✓ | Clear, specific, measurable |
| Proposed Solution | ✓ | High-level concept only |
| Scope Definition | ✓ | In/Out/Deferred |
| Constraints | ✓ | All known constraints |
| Success Criteria | ✓ | Measurable outcomes |
| Risks | ✓ | With mitigations |
| Sign-off | ✓ | Stakeholder approval |

### Writing Standards

**Problem Statements:**
- Use active voice
- Be specific (avoid "improve" without metrics)
- Include who is affected
- State the impact

**Good Example:**
> "Customer service representatives spend 45 minutes per case searching across 3 disconnected systems, resulting in 23% longer resolution times and $2.1M annual labor cost."

**Bad Example:**
> "The systems are slow and need improvement."

### Naming Conventions

| Artifact | Format | Example |
|----------|--------|---------|
| Concept Document | `CONCEPT_[PROJECT]_v[X.Y].md` | `CONCEPT_CIA-SIE_v1.0.md` |
| Decision Record | `DEC-[NNNN]_[Topic].md` | `DEC-0001_Database_Selection.md` |
| Meeting Notes | `MEETING_[DATE]_[Topic].md` | `MEETING_2025-01-14_Kickoff.md` |

---

## SCOPE DEFINITION STANDARDS

### In-Scope Items

Must be:
- Specific and bounded
- Achievable within constraints
- Agreed by stakeholders
- Traceable to problem statement

### Out-of-Scope Items

Must include:
- Clear reason for exclusion
- Owner if different team handles
- Reference to where it IS addressed (if anywhere)

### Deferred Items

Must include:
- Target phase or release
- Dependencies that must be met first
- Owner responsible for tracking

---

## CONSTRAINT DOCUMENTATION STANDARDS

### Required Constraint Categories

1. **Budget** - Financial limitations
2. **Timeline** - Schedule constraints
3. **Resources** - People, skills, tools
4. **Technology** - Platform, integration limits
5. **Regulatory** - Compliance requirements
6. **Organizational** - Policies, processes

### Constraint Template

```markdown
## Constraint: [Name]

**Category:** [Budget/Timeline/Resources/Technology/Regulatory/Organizational]
**Source:** [Where this constraint comes from]
**Flexibility:** [Fixed/Negotiable/Soft]

**Description:**
[Detailed description of the constraint]

**Impact:**
[How this affects the project]

**Validation:**
[How we verified this constraint is real]
```

---

## STAKEHOLDER STANDARDS

### Stakeholder Identification

Every project must identify:

| Role | Description | Engagement Level |
|------|-------------|------------------|
| Sponsor | Funding/authority | Approve |
| Owner | Accountable for outcome | Decide |
| Subject Matter Expert | Domain knowledge | Consult |
| User Representative | End-user perspective | Consult |
| Technical Lead | Technical feasibility | Consult |

### Stakeholder Communication

| Stakeholder Type | Frequency | Format |
|-----------------|-----------|--------|
| Sponsor | Weekly | Summary report |
| Owner | Daily/As needed | Direct communication |
| SME | As needed | Working sessions |
| User Rep | Per milestone | Review sessions |

---

## VALIDATION STANDARDS

### Concept Validation Criteria

A concept is validated when:

1. **Problem Validated**
   - [ ] Problem exists and is significant
   - [ ] Problem is clearly articulated
   - [ ] Stakeholders agree on problem definition

2. **Solution Validated**
   - [ ] Solution addresses the problem
   - [ ] Solution is technically feasible
   - [ ] Solution is economically viable

3. **Scope Validated**
   - [ ] Scope is achievable within constraints
   - [ ] Scope addresses core problem
   - [ ] Stakeholders agree on boundaries

### Validation Evidence

Document validation with:
- Meeting minutes
- Email confirmations
- Sign-off signatures
- Prototype feedback (if applicable)

---

## DECISION STANDARDS

### When to Create Decision Record

Create a formal decision record when:
- Multiple options were considered
- Decision affects scope, timeline, or budget
- Decision may be questioned later
- Decision sets precedent

### Decision Record Requirements

| Field | Required | Purpose |
|-------|----------|---------|
| Decision | ✓ | What was decided |
| Date | ✓ | When decided |
| Decision Maker | ✓ | Who has authority |
| Context | ✓ | Why decision needed |
| Options | ✓ | What was considered |
| Rationale | ✓ | Why this option |
| Implications | ✓ | What this affects |

---

## QUALITY METRICS

### Phase 2 Quality Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| Problem Clarity | 100% | Stakeholder understanding test |
| Scope Agreement | 100% | Stakeholder sign-off |
| Constraint Coverage | 100% | All categories addressed |
| Decision Documentation | 100% | All major decisions recorded |
| Stakeholder Engagement | >80% | Participation rate |

### Quality Review Checklist

Before exiting Phase 2:

- [ ] Concept document meets all required sections
- [ ] Problem statement passes clarity test
- [ ] Scope boundaries are unambiguous
- [ ] All constraints documented with sources
- [ ] All stakeholders have provided input
- [ ] All decisions formally recorded
- [ ] Validation evidence documented

---

*STANDARDS v1.0 | PHASE 02 | Gold Standard System*
