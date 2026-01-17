# PHASE 11: OPERATIONS
## Exit Criteria

**Purpose:** Conditions for operational readiness and ongoing operational health

---

## NOTE ON PHASE 11

Unlike other phases, Phase 11 (Operations) does not have a traditional "exit" - it is continuous. Instead, this document defines:

1. **Entry criteria** - What must be true to begin operations
2. **Ongoing health criteria** - What must remain true during operations
3. **Transition criteria** - When changes flow to/from other phases

---

## OPERATIONAL ENTRY CRITERIA

Before a system enters full operations:

- [ ] **Phase 10 Complete**
  - Deployment successful
  - Smoke tests passing
  - Initial stability confirmed

- [ ] **Monitoring Operational**
  - Dashboards configured
  - Alerts active and tested
  - Log aggregation working

- [ ] **Documentation Complete**
  - Runbooks written
  - Architecture documented
  - Contact information current

- [ ] **Processes Established**
  - On-call rotation defined
  - Incident process documented
  - Change management in place

- [ ] **Team Readiness**
  - Operations team briefed
  - On-call trained
  - Escalation paths clear

---

## ONGOING HEALTH CRITERIA

During operations, these must remain true:

### Service Level Objectives

- [ ] Availability meets SLO (target: 99.9%)
- [ ] Latency within SLO (target: p95 < 200ms)
- [ ] Error rate within SLO (target: < 0.1%)
- [ ] Error budget remaining adequate

### Operational Health

- [ ] On-call rotation staffed
- [ ] Runbooks current and tested
- [ ] Monitoring coverage adequate
- [ ] Alerts actionable (low noise)

### Process Health

- [ ] Incidents resolved within targets
- [ ] Postmortems completed
- [ ] Action items tracked
- [ ] Changes following process

---

## OPERATIONAL REVIEW CADENCE

### Weekly Review

```markdown
## Weekly Ops Review

**Week of:** [Date]

### SLO Status
  Availability: ____%
  Latency (p95): _____ms
  Error rate: ____%

### Incidents
  Total: _____
  SEV1: _____ SEV2: _____ SEV3: _____ SEV4: _____

### On-Call Health
  Pages: _____
  Actionable: _____
  False positives: _____

### Changes Deployed
  Total: _____
  Success rate: ____%

### Action Items
  [ ] [Item 1]
  [ ] [Item 2]
```

### Monthly Review

```markdown
## Monthly Ops Review

**Month:** [Month/Year]

### SLO Trends
  [Graph or summary of trends]

### Incident Analysis
  Most common causes: [List]
  Repeat incidents: [List]
  Improvement areas: [List]

### Capacity Review
  Current utilization: ____%
  Projected growth: ____%
  Action needed: [Yes/No]

### Toil Analysis
  Manual tasks identified: [List]
  Automation opportunities: [List]

### Improvement Actions
  [ ] [Item 1]
  [ ] [Item 2]
```

---

## TRANSITION CRITERIA

### To Bug Fix Cycle (Phases 6-10)

When an issue requires code change:

- [ ] Issue documented
- [ ] Severity assessed
- [ ] Entered into tracking
- [ ] Assigned for resolution
- [ ] Follows mini-lifecycle through deployment

### To Full Lifecycle (Phases 1-11)

When enhancement or new feature needed:

- [ ] Request documented
- [ ] Business case made
- [ ] Entered into backlog
- [ ] Prioritized for lifecycle
- [ ] Full phase progression required

### From Other Phases (Entry to Operations)

When new release enters operations:

- [ ] Phase 10 exit criteria met
- [ ] Operational entry criteria verified
- [ ] Team briefed on changes
- [ ] Monitoring updated if needed
- [ ] Runbooks updated if needed

---

## OPERATIONAL MATURITY ASSESSMENT

Periodic assessment of operational maturity:

```
OPERATIONAL MATURITY

Date: _______________
Assessor: _______________

Monitoring:
  [ ] Basic (metrics only)
  [ ] Intermediate (metrics + logs)
  [ ] Advanced (metrics + logs + traces)
  [ ] Excellent (full observability)

Incident Response:
  [ ] Basic (ad-hoc)
  [ ] Intermediate (defined process)
  [ ] Advanced (measured MTTR)
  [ ] Excellent (proactive prevention)

Change Management:
  [ ] Basic (manual, infrequent)
  [ ] Intermediate (automated, regular)
  [ ] Advanced (CI/CD, frequent)
  [ ] Excellent (continuous, safe)

Documentation:
  [ ] Basic (exists)
  [ ] Intermediate (current)
  [ ] Advanced (tested)
  [ ] Excellent (living)

Automation:
  [ ] Basic (manual operations)
  [ ] Intermediate (some automation)
  [ ] Advanced (mostly automated)
  [ ] Excellent (self-healing)

Overall Maturity Level: _____/5
```

---

## DECOMMISSIONING CRITERIA

When a system is retired:

- [ ] Replacement system operational (if applicable)
- [ ] Data migrated or archived
- [ ] Dependencies updated
- [ ] Users notified
- [ ] Resources deprovisioned
- [ ] Documentation archived
- [ ] Monitoring removed
- [ ] On-call updated

---

*EXIT CRITERIA v1.0 | PHASE 11 | Gold Standard System*
