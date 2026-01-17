# PHASE 11: OPERATIONS
## Briefing Document

**Phase Number:** 11
**Phase Name:** Operations
**Purpose:** Maintain and evolve the system in production

---

## WHAT THIS PHASE IS

Operations is the ongoing management of a live system. Unlike previous phases with clear end points, Operations is continuous. It encompasses monitoring, incident response, maintenance, and continuous improvement. This phase ensures the system continues to deliver value reliably.

**Key Insight:** Operations is not a phase that ends - it's a continuous cycle of monitoring, responding, improving, and evolving. The system is never "done."

---

## WHAT YOU'RE DOING

1. **Monitoring system health** - Continuous observation
2. **Responding to incidents** - Problem resolution
3. **Performing maintenance** - Updates, patches, optimization
4. **Managing capacity** - Scaling to meet demand
5. **Improving continuously** - Learning from operations
6. **Evolving the system** - New features through lifecycle

---

## WHAT YOU'RE NOT DOING

- Major feature development (goes through full lifecycle)
- Fundamental architecture changes (requires new lifecycle)
- Ad-hoc changes without process (all changes controlled)

**This phase answers "HOW DO WE KEEP IT RUNNING AND IMPROVING?"**

---

## OPERATIONAL PILLARS

### 1. Monitoring

Continuous observation of system health:

| Pillar | Purpose | Tools |
|--------|---------|-------|
| **Metrics** | Quantitative health | Prometheus, Datadog |
| **Logs** | Event records | ELK, Splunk |
| **Traces** | Request flows | Jaeger, Zipkin |
| **Alerts** | Proactive notification | PagerDuty, Opsgenie |

### 2. Incident Management

Structured response to problems:

```
Detection → Triage → Response → Resolution → Review
```

### 3. Change Management

Controlled system modifications:

```
Request → Review → Approve → Implement → Verify
```

### 4. Capacity Management

Ensuring adequate resources:

```
Monitor → Forecast → Plan → Provision → Verify
```

---

## SERVICE LEVEL MANAGEMENT

### Definitions

| Term | Definition | Example |
|------|------------|---------|
| **SLI** | Service Level Indicator | Request latency |
| **SLO** | Service Level Objective | p95 < 200ms |
| **SLA** | Service Level Agreement | 99.9% uptime |
| **Error Budget** | Allowable unreliability | 0.1% downtime |

### SLO Dashboard

```
Service: [Name]

Availability SLO: 99.9%
  Current: 99.95% ✓
  Budget remaining: 50%

Latency SLO: p95 < 200ms
  Current: 150ms ✓
  Trend: Stable

Error Rate SLO: < 0.1%
  Current: 0.05% ✓
  Trend: Improving
```

---

## INCIDENT MANAGEMENT

### Incident Severity Levels

| Severity | Definition | Response Time | Examples |
|----------|------------|---------------|----------|
| **SEV1** | Critical, widespread impact | 15 minutes | System down, data loss |
| **SEV2** | Major, significant impact | 30 minutes | Core feature broken |
| **SEV3** | Moderate, limited impact | 4 hours | Non-critical feature broken |
| **SEV4** | Minor, minimal impact | 24 hours | Cosmetic issue |

### Incident Response Process

```markdown
## Incident: INC-[NUMBER]

**Severity:** SEV[1-4]
**Status:** Investigating | Identified | Mitigated | Resolved

### Timeline
| Time | Action |
|------|--------|
| [Time] | Incident detected |
| [Time] | Response initiated |
| [Time] | Root cause identified |
| [Time] | Mitigation applied |
| [Time] | Incident resolved |

### Impact
[What was affected, who was affected]

### Root Cause
[Why did this happen]

### Resolution
[What fixed it]

### Follow-up Actions
- [ ] [Action item 1]
- [ ] [Action item 2]
```

---

## RUNBOOKS

### Runbook Structure

```markdown
# Runbook: [Name]

**Last Updated:** [Date]
**Owner:** [Team/Person]

## Purpose
[When to use this runbook]

## Prerequisites
- [Access needed]
- [Tools needed]

## Steps

### Step 1: [Title]
```
[Command or action]
```
**Expected outcome:** [What should happen]
**If this fails:** [What to do]

### Step 2: [Title]
...

## Verification
[How to confirm success]

## Rollback
[How to undo if needed]
```

### Essential Runbooks

| Runbook | Purpose |
|---------|---------|
| Service restart | Restart services safely |
| Database failover | Switch to replica |
| Cache clear | Clear application caches |
| Log investigation | Find issues in logs |
| Scaling | Add/remove capacity |
| Rollback | Revert to previous version |

---

## ON-CALL PRACTICES

### On-Call Responsibilities

- Acknowledge alerts within response time
- Investigate and resolve or escalate
- Document actions taken
- Update status pages
- Hand off to next on-call

### On-Call Handoff

```markdown
## On-Call Handoff

**From:** [Name]
**To:** [Name]
**Date:** [Date]

### Active Issues
- [Issue 1: Status, next steps]
- [Issue 2: Status, next steps]

### Recent Incidents
- [INC-XXX: Summary]

### Upcoming Changes
- [Scheduled change 1]

### Notes
[Anything else the next person should know]
```

---

## CHANGE MANAGEMENT

### Change Categories

| Category | Risk | Approval | Example |
|----------|------|----------|---------|
| **Standard** | Low | Pre-approved | Config change |
| **Normal** | Medium | CAB review | Feature release |
| **Emergency** | Variable | Fast-track | Critical fix |

### Change Request

```markdown
## Change Request: CHG-[NUMBER]

**Category:** Standard | Normal | Emergency
**Status:** Requested | Approved | Implemented | Closed

### Description
[What change is being made]

### Justification
[Why this change is needed]

### Impact
[What will be affected]

### Implementation Plan
1. [Step 1]
2. [Step 2]

### Rollback Plan
1. [Step 1]
2. [Step 2]

### Verification
[How to confirm success]

### Approvals
- [ ] Technical: [Name]
- [ ] Operations: [Name]
```

---

## CONTINUOUS IMPROVEMENT

### Improvement Sources

| Source | Action |
|--------|--------|
| Incident postmortems | Action items from reviews |
| On-call feedback | Pain points from responders |
| Monitoring gaps | Missing visibility |
| Toil identification | Manual work to automate |
| User feedback | Reliability concerns |

### Postmortem Template

```markdown
# Postmortem: INC-[NUMBER]

**Date:** [Date]
**Author:** [Name]

## Summary
[Brief description of what happened]

## Impact
- Duration: [Time]
- Users affected: [Number]
- Revenue impact: [If applicable]

## Timeline
| Time | Event |
|------|-------|
| [Time] | [Event] |

## Root Cause
[Deep analysis of why this happened]

## What Went Well
- [Item 1]
- [Item 2]

## What Went Poorly
- [Item 1]
- [Item 2]

## Action Items
| Item | Owner | Due Date |
|------|-------|----------|
| [Action] | [Name] | [Date] |

## Lessons Learned
[Key takeaways]
```

---

## OPERATIONAL METRICS

### Key Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Availability | 99.9% | < 99.5% |
| Error rate | < 0.1% | > 1% |
| Latency (p95) | < 200ms | > 500ms |
| MTTR | < 1 hour | > 4 hours |
| Deployment frequency | Weekly | N/A |
| Change failure rate | < 5% | > 15% |

---

## OPERATIONAL READINESS CHECKLIST

For any system in operations:

- [ ] **Monitoring**
  - Dashboards configured
  - Key metrics tracked
  - Alerts defined and tested

- [ ] **Documentation**
  - Runbooks written
  - Architecture documented
  - Contact information current

- [ ] **Processes**
  - On-call rotation established
  - Incident process defined
  - Change management in place

- [ ] **Testing**
  - Disaster recovery tested
  - Failover verified
  - Rollback procedures tested

---

## LIFECYCLE CONTINUATION

Operations connects back to the lifecycle:

- **Bug fixes:** Minor cycle through Phases 6-10
- **Enhancements:** Full cycle from Phase 1
- **Major changes:** New lifecycle iteration

```
Operations ──► New Feature Request ──► Phase 1 (Ideation)
     │
     ├──► Bug Fix ──► Phase 6 (Development) ──► Phase 10 (Deploy)
     │
     └──► Continuous Improvement ──► Operational Excellence
```

---

*PHASE 11 BRIEFING v1.0 | LIFECYCLE_MODULES | Gold Standard System*
