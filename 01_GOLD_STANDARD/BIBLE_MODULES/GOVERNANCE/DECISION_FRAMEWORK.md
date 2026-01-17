# DECISION FRAMEWORK
## How to Make and Document Decisions

**Module:** GOVERNANCE
**Version:** 1.0

---

## CORE PRINCIPLE

> "Undocumented decisions are assumptions. Assumptions are the mother of all failures."

Every decision of consequence must be documented in a way that allows future understanding without access to the decision-maker.

---

## DECISION CATEGORIES

| Category | Examples | Documentation Level |
|----------|----------|---------------------|
| **Strategic** | Project direction, major technology | Formal ADR |
| **Architectural** | System structure, patterns | ADR |
| **Technical** | Implementation approach | ADR or Decision Log |
| **Operational** | Process, workflow | Decision Log |
| **Tactical** | Day-to-day choices | Code comments / commit messages |

---

## ARCHITECTURE DECISION RECORD (ADR)

### When to Use
- Technology selection
- Framework choices
- Architectural patterns
- Integration approaches
- Security architecture
- Any decision that would be hard to reverse

### ADR Template

```markdown
# ADR-[NUMBER]: [TITLE]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date
[YYYY-MM-DD]

## Decision Makers
- [Name] (Accountable)
- [Name] (Consulted)

## Context
[What is the situation that requires a decision?
What forces are at play?
What constraints exist?]

## Decision
[What is the decision?
State it clearly and unambiguously.]

## Rationale
[Why was this decision made?
What factors were most important?]

## Alternatives Considered

### Alternative 1: [Name]
- Description: [what it is]
- Pros: [benefits]
- Cons: [drawbacks]
- Why rejected: [reason]

### Alternative 2: [Name]
- Description: [what it is]
- Pros: [benefits]
- Cons: [drawbacks]
- Why rejected: [reason]

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [trade-off 1]
- [trade-off 2]

### Risks
- [risk and mitigation]

## Related Decisions
- [ADR-XXX: Related topic]

## Notes
[Any additional context]
```

---

## DECISION LOG

For decisions that don't warrant full ADR:

| Date | Decision | Rationale | Decided By | Affects |
|------|----------|-----------|------------|---------|
| 2026-01-14 | Use UTC for all timestamps | Consistency across timezones | Tech Lead | Data layer |
| 2026-01-14 | 2-week sprint cadence | Balance planning and delivery | PM | Process |

---

## DECISION-MAKING PROCESS

### Step 1: Frame the Decision

**Questions to answer:**
- What exactly needs to be decided?
- Why does this need a decision now?
- What are the constraints?
- Who is affected?
- What happens if we don't decide?

### Step 2: Identify Options

**Generate alternatives:**
- At least 2 options (including "do nothing" if applicable)
- Avoid false dichotomies
- Include unconventional options

### Step 3: Evaluate Options

**For each option:**
- What are the benefits?
- What are the costs/risks?
- What are the dependencies?
- Is it reversible?
- What's the timeline?

### Step 4: Decide

**Make the call:**
- One person is accountable
- Decision is explicit and clear
- Decision is communicated

### Step 5: Document

**Record the decision:**
- Use appropriate format (ADR or Log)
- Include rationale
- Note alternatives considered
- Identify consequences

### Step 6: Communicate

**Inform stakeholders:**
- Those affected by the decision
- Those who need to implement it
- Those who were consulted

---

## DECISION PRINCIPLES

### Principle 1: Decide at the Right Level

| Impact | Decision Level |
|--------|----------------|
| Affects entire project | Principal/Sponsor |
| Affects architecture | Technical Lead |
| Affects single component | Component Owner |
| Affects implementation detail | Developer |

### Principle 2: Reversibility Matters

| Reversibility | Approach |
|---------------|----------|
| **Easily reversible** | Decide quickly, adjust if needed |
| **Difficult to reverse** | Careful evaluation, more stakeholders |
| **Irreversible** | Maximum scrutiny, escalate to Principal |

### Principle 3: Information vs. Delay

- Don't delay decisions waiting for perfect information
- Decide with 70% information if reversible
- Require 90% information if irreversible
- "No decision" is a decision (usually bad)

### Principle 4: Document Why, Not Just What

- "We chose React" - Insufficient
- "We chose React because of team expertise and ecosystem" - Sufficient
- Future readers need to understand the context

---

## DECISION ANTI-PATTERNS

### 1. Analysis Paralysis
**Symptom:** Endless evaluation, no decision
**Fix:** Time-box decisions; set decision deadline

### 2. HiPPO (Highest Paid Person's Opinion)
**Symptom:** Decisions based on authority, not evidence
**Fix:** Require rationale for all decisions

### 3. Decision Amnesia
**Symptom:** Same decisions revisited repeatedly
**Fix:** Document decisions; reference when revisiting

### 4. Consensus Seeking
**Symptom:** Decisions delayed until everyone agrees
**Fix:** Accountable person decides after consultation

### 5. Implicit Decisions
**Symptom:** "We just ended up doing X"
**Fix:** Make decisions explicit and documented

---

## REVISITING DECISIONS

Decisions can be revisited when:
- Context has significantly changed
- New information invalidates assumptions
- Consequences are worse than anticipated

Revisiting requires:
1. Documenting what changed
2. Re-evaluating options
3. Making new decision (supersedes old)
4. Updating ADR status to "Superseded"

---

*DECISION_FRAMEWORK v1.0 | GOVERNANCE | BIBLE_MODULES*
