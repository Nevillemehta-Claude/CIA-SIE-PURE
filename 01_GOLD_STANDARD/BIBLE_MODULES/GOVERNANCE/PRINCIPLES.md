# GOVERNANCE PRINCIPLES
## Universal Laws of Project Governance

**Module:** GOVERNANCE
**Version:** 1.0

---

## THE SEVEN GOVERNANCE PRINCIPLES

### PRINCIPLE 1: ACCOUNTABILITY IS SINGULAR

**Definition:** For any decision, exactly ONE person is accountable. Accountability cannot be shared or delegated.

| Role | Definition |
|------|------------|
| **Accountable** | The ONE person who answers for the outcome |
| **Responsible** | Those who do the work |
| **Consulted** | Those whose input is sought |
| **Informed** | Those who are kept updated |

**Application:**
- Every decision has a named accountable party
- "The team decided" is not acceptable
- Accountability can be escalated but not split

**Test:** "Who answers if this goes wrong?" Must have ONE name.

---

### PRINCIPLE 2: DECISIONS ARE DOCUMENTED

**Definition:** Undocumented decisions are not decisions. They are assumptions waiting to cause problems.

**Every decision record includes:**
1. What was decided
2. Why it was decided (rationale)
3. What alternatives were considered
4. Who made the decision
5. When it was made
6. What it supersedes (if anything)

**Application:**
- ADRs (Architecture Decision Records) for technical decisions
- Meeting minutes for operational decisions
- Change requests for scope decisions

**Test:** "Can someone understand this decision in 6 months without asking the decision-maker?"

---

### PRINCIPLE 3: CHANGES ARE CONTROLLED

**Definition:** Uncontrolled change is the primary source of project failure. All changes go through defined process.

**Change control applies to:**
- Requirements changes
- Scope changes
- Technical approach changes
- Resource changes
- Timeline changes

**Change control does NOT mean:**
- No changes allowed
- Bureaucratic delays
- Innovation prevention

**Change control DOES mean:**
- Changes are visible
- Impact is assessed
- Decision is documented
- Affected parties are notified

---

### PRINCIPLE 4: GATES ARE NON-NEGOTIABLE

**Definition:** Quality gates exist to prevent defects from propagating. Bypassing gates creates compounding problems.

**Gate characteristics:**
- Defined entry criteria
- Defined exit criteria
- Binary pass/fail
- No "conditional pass"
- No "we'll fix it later"

**If gate not passed:**
1. STOP
2. Identify deficiency
3. Remediate
4. Re-verify
5. Then proceed

**The cost of gate enforcement < The cost of defect propagation**

---

### PRINCIPLE 5: RISKS ARE MANAGED, NOT IGNORED

**Definition:** Every project has risks. Mature governance identifies, assesses, and mitigates them proactively.

**Risk management cycle:**
1. **Identify** - What could go wrong?
2. **Assess** - How likely? How severe?
3. **Plan** - What's the mitigation?
4. **Monitor** - Is it changing?
5. **Respond** - If it occurs, what then?

**Risk categories:**
- Technical risks (technology doesn't work)
- Resource risks (people unavailable)
- Schedule risks (timeline slips)
- Scope risks (requirements change)
- External risks (dependencies fail)

---

### PRINCIPLE 6: STAKEHOLDERS ARE ENGAGED

**Definition:** Projects fail when stakeholders are surprised. Regular, structured engagement prevents misalignment.

**Engagement frequency:**
| Stakeholder Type | Engagement |
|------------------|------------|
| Sponsors | Weekly status, milestone reviews |
| Users | Requirements validation, UAT |
| Technical leads | Daily/weekly syncs |
| External parties | Per contract/agreement |

**Engagement principles:**
- No surprises
- Bad news travels fast
- Feedback is actively sought
- Decisions are communicated

---

### PRINCIPLE 7: AUTHORITY MATCHES RESPONSIBILITY

**Definition:** People cannot be responsible for outcomes they cannot control. Authority and responsibility must align.

**Misalignment symptoms:**
- "I'm responsible but can't make decisions"
- "I made the decision but others are blamed"
- "Nobody knows who can approve this"

**Alignment requirements:**
- Decision rights are explicit
- Escalation paths are defined
- Authority is documented
- Responsibility is matched to authority

---

## GOVERNANCE ANTI-PATTERNS

### 1. GOVERNANCE THEATER
**Symptom:** Lots of process, no actual control
**Fix:** Ensure governance activities have teeth (can stop work)

### 2. DIFFUSED ACCOUNTABILITY
**Symptom:** "The team" or "we all" are accountable
**Fix:** Name ONE person for each decision

### 3. SHADOW DECISIONS
**Symptom:** Real decisions made in hallways, not documented
**Fix:** If it's not documented, it's not decided

### 4. GATE BYPASS
**Symptom:** "We'll get sign-off later"
**Fix:** Gates are blocking; no bypass without escalation

### 5. RISK BLINDNESS
**Symptom:** "We don't have any risks"
**Fix:** Every project has risks; find them

### 6. STAKEHOLDER SURPRISE
**Symptom:** Stakeholders learn bad news late
**Fix:** Proactive, regular communication

---

## GOVERNANCE MATURITY LEVELS

| Level | Characteristics |
|-------|-----------------|
| **Level 1: Ad Hoc** | No defined process, decisions are reactive |
| **Level 2: Defined** | Processes exist but inconsistently applied |
| **Level 3: Managed** | Processes consistently applied, metrics tracked |
| **Level 4: Optimizing** | Continuous improvement, predictive capability |

**Target:** Level 3 minimum for any serious project.

---

## GOVERNANCE DOCUMENTS

Every project should have:

| Document | Purpose |
|----------|---------|
| Project Charter | Authority, scope, stakeholders |
| Governance Plan | How decisions are made |
| RACI Matrix | Who does what |
| Risk Register | Known risks and mitigations |
| Change Log | Record of changes |
| Decision Log | Record of decisions |

---

*PRINCIPLES v1.0 | GOVERNANCE | BIBLE_MODULES*
