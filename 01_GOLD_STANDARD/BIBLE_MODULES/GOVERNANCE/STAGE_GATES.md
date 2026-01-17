# STAGE GATES
## Quality Checkpoints Throughout the Lifecycle

**Module:** GOVERNANCE
**Version:** 1.0

---

## WHAT ARE STAGE GATES?

Stage gates are formal checkpoints where work is reviewed against defined criteria before proceeding. They exist to:

1. **Prevent defect propagation** - Catch issues early
2. **Ensure alignment** - Verify work matches expectations
3. **Enable decisions** - Provide data for go/no-go choices
4. **Create accountability** - Force explicit approval

---

## THE FIVE STANDARD GATES

### GATE 1: DESIGN REVIEW

**When:** After Phase 4 (Architecture) / Before Phase 5 (Specification)

**Purpose:** Verify the design is sound before detailed specification

**Entry Criteria:**
- [ ] Requirements documented and approved
- [ ] Architecture designed
- [ ] ADRs created for key decisions

**Review Checklist:**
- [ ] Architecture addresses all requirements
- [ ] Non-functional requirements addressed (security, performance)
- [ ] Integration points identified
- [ ] Risks identified and mitigated
- [ ] No unresolved architectural questions

**Exit Criteria:**
- [ ] Architecture approved by technical authority
- [ ] All review comments addressed
- [ ] Ready for detailed specification

**Participants:**
- Technical Lead (presenter)
- Principal/Sponsor (approver)
- Security reviewer (if applicable)
- Architecture reviewer

---

### GATE 2: SPECIFICATION REVIEW

**When:** After Phase 5 (Specification) / Before Phase 6 (Development)

**Purpose:** Verify specifications are complete and unambiguous

**Entry Criteria:**
- [ ] Design review passed
- [ ] All components specified
- [ ] API contracts defined

**Review Checklist:**
- [ ] Every component has complete specification
- [ ] API specifications validated (OpenAPI)
- [ ] Data models defined
- [ ] Business logic documented
- [ ] Edge cases addressed
- [ ] Error handling specified

**Exit Criteria:**
- [ ] Specifications approved
- [ ] Development can begin without questions
- [ ] Test strategy defined

**Participants:**
- Technical Lead (presenter)
- Developers (reviewers)
- QA Lead (test strategy)

---

### GATE 3: CODE REVIEW

**When:** After Phase 6 (Development) / Before Phase 7 (Integration)

**Purpose:** Verify code quality before integration

**Entry Criteria:**
- [ ] Specification review passed
- [ ] Code complete
- [ ] Unit tests passing

**Review Checklist:**
- [ ] Code implements specification
- [ ] Unit tests cover all functions
- [ ] Coverage targets met (>90%)
- [ ] Static analysis clean
- [ ] No security vulnerabilities
- [ ] Documentation complete

**Exit Criteria:**
- [ ] All code reviewed and approved
- [ ] All tests passing
- [ ] Ready for integration

**Participants:**
- Developers (peer review)
- Technical Lead (approval)
- Security reviewer (if applicable)

---

### GATE 4: INTEGRATION REVIEW

**When:** After Phase 7 (Integration) / Before Phase 8 (Verification)

**Purpose:** Verify components integrate correctly

**Entry Criteria:**
- [ ] Code review passed
- [ ] All components ready
- [ ] Integration environment available

**Review Checklist:**
- [ ] All components integrated
- [ ] Integration tests passing
- [ ] No orphaned endpoints
- [ ] No phantom features
- [ ] Contract tests passing
- [ ] System runs end-to-end

**Exit Criteria:**
- [ ] Integration complete
- [ ] System ready for full verification
- [ ] RTM populated

**Participants:**
- Technical Lead (presenter)
- QA Lead (verification readiness)
- Integration specialists

---

### GATE 5: RELEASE REVIEW

**When:** After Phase 8 (Verification) / Before Phase 10 (Deployment)

**Purpose:** Final approval before production release

**Entry Criteria:**
- [ ] All verification complete
- [ ] UAT approved
- [ ] Documentation complete

**Review Checklist:**
- [ ] All tests passing
- [ ] Coverage targets met
- [ ] Performance targets met
- [ ] Security audit passed
- [ ] RTM complete
- [ ] UAT signed off
- [ ] Documentation accurate
- [ ] Rollback procedure verified
- [ ] Monitoring configured

**Exit Criteria:**
- [ ] Release approved
- [ ] Go-live date confirmed
- [ ] All stakeholders notified

**Participants:**
- Technical Lead (presenter)
- Principal/Sponsor (approver)
- Operations Lead (deployment readiness)
- QA Lead (verification attestation)

---

## GATE PROCESS

### Before the Gate

1. **Prepare materials** - All required documents ready
2. **Self-review** - Presenter verifies criteria met
3. **Schedule review** - All participants available

### During the Gate

1. **Present status** - Walk through checklist
2. **Review evidence** - Examine supporting materials
3. **Identify issues** - Note any deficiencies
4. **Decide outcome** - Pass / Conditional Pass / Fail

### Gate Outcomes

| Outcome | Definition | Action |
|---------|------------|--------|
| **PASS** | All criteria met | Proceed to next phase |
| **CONDITIONAL** | Minor issues, can proceed with plan | Document conditions, verify resolution |
| **FAIL** | Significant issues | Stop, remediate, re-present |

### After the Gate

1. **Document outcome** - Record decision and any conditions
2. **Communicate result** - Notify stakeholders
3. **Track conditions** - If conditional, ensure resolution
4. **Archive materials** - Preserve for audit trail

---

## GATE DOCUMENTATION

### Gate Record Template

```markdown
# Gate [N] Record: [Gate Name]

**Date:** [date]
**Project:** [project name]
**Presenter:** [name]
**Approvers:** [names]

## Checklist Results

| Item | Status | Notes |
|------|--------|-------|
| [item 1] | PASS/FAIL | [notes] |
| [item 2] | PASS/FAIL | [notes] |

## Outcome

**Decision:** [PASS / CONDITIONAL / FAIL]

**Conditions (if any):**
1. [condition]
2. [condition]

**Approvals:**
- [Name]: [Approved/Rejected]
- [Name]: [Approved/Rejected]

## Follow-up Actions

| Action | Owner | Due Date |
|--------|-------|----------|
| [action] | [name] | [date] |
```

---

## GATE ESCALATION

If gate reviewers disagree:

1. Document differing positions
2. Escalate to Principal/Sponsor
3. Principal makes final decision
4. Decision is documented
5. All parties notified

**Escalation is not failure** - It's the governance system working.

---

## GATE ANTI-PATTERNS

### 1. Rubber Stamp
**Symptom:** Gates always pass without real review
**Fix:** Enforce documented evidence for each item

### 2. Perpetual Conditional
**Symptom:** Conditions never cleared
**Fix:** Time-bound conditions with verification

### 3. Gate Avoidance
**Symptom:** Work proceeds without gate approval
**Fix:** Gates are blocking; work cannot proceed without pass

### 4. Scope Creep at Gate
**Symptom:** New requirements introduced during gate review
**Fix:** Gates verify against existing scope; new requirements go through change control

---

*STAGE_GATES v1.0 | GOVERNANCE | BIBLE_MODULES*
