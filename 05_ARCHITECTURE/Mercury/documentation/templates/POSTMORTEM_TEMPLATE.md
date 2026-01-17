# Incident Postmortem

**Incident ID:** INC-YYYY-MM-DD-###
**Status:** [DRAFT | FINAL]
**Author(s):** 
**Date:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

---

## Executive Summary

*A brief (2-3 sentence) summary of the incident, its impact, and resolution.*

---

## Incident Timeline

| Time (UTC) | Event |
|------------|-------|
| HH:MM | First alert triggered |
| HH:MM | Incident acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Service restored |
| HH:MM | All-clear declared |

---

## Impact

### User Impact
- **Duration:** X hours Y minutes
- **Users Affected:** N users / X% of traffic
- **Severity:** [P0 | P1 | P2 | P3]

### Business Impact
- *Describe any business/financial impact*

### Data Impact
- *Describe any data loss or corruption*
- **Data Loss:** [None | Partial | Complete]

---

## Root Cause

### What Happened?
*Detailed technical explanation of the root cause.*

### Why Did It Happen?
*5 Whys Analysis*

1. **Why?** 
2. **Why?** 
3. **Why?** 
4. **Why?** 
5. **Why?** (Root Cause)

---

## Detection

### How Was It Detected?
- [ ] Automated monitoring
- [ ] Customer report
- [ ] Internal user
- [ ] Automated test

### Detection Gap
*What could have detected this earlier?*

---

## Response

### What Went Well
1. 
2. 
3. 

### What Could Be Improved
1. 
2. 
3. 

### Where We Got Lucky
1. 

---

## Resolution

### Immediate Fix
*What was done to restore service?*

### Permanent Fix
*What will prevent recurrence?*

---

## Action Items

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| 1 | | | | [ ] TODO |
| 2 | | | | [ ] TODO |
| 3 | | | | [ ] TODO |

### Categorized Actions

**Prevention** (Stop it happening)
- [ ] 

**Detection** (Find it faster)
- [ ] 

**Response** (Fix it faster)
- [ ] 

**Recovery** (Recover faster)
- [ ] 

---

## Lessons Learned

### Technical Lessons
1. 

### Process Lessons
1. 

### Cultural Lessons
1. 

---

## Related Incidents

- *Link to related incidents if any*

---

## Appendix

### Graphs/Metrics

*Include relevant monitoring graphs*

### Logs

```
# Relevant log snippets
```

### Configuration Changes

```diff
# Before
- old_value: X

# After
+ new_value: Y
```

---

## Sign-Off

| Role | Name | Date | Approved |
|------|------|------|----------|
| Author | | | [ ] |
| Reviewer | | | [ ] |
| Engineering Lead | | | [ ] |

---

## Blameless Culture Reminder

> This postmortem is a learning document, not a blame assignment. 
> We focus on systemic improvements, not individual failures.
> Our goal is to make systems more resilient, not to punish humans.

---

*Template Version: 1.0.0 | Last Updated: 2026-01-13*
