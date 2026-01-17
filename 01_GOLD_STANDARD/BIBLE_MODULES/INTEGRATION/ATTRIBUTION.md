# ATTRIBUTION FRAMEWORK
## Root Cause Determination for Integration Failures

**Module:** INTEGRATION
**Version:** 1.0

---

## PURPOSE

When integration failures occur, accountability must be established before remediation can proceed. This framework systematically identifies the source of failures.

---

## THE THREE RESPONSIBILITY DOMAINS

### 1. BACKEND / PROVIDER

**Responsibilities:**
- API design and implementation
- Data models and business logic
- External service integration
- Authentication and authorization
- Database operations

**Typical Failure Modes:**
- Undocumented schemas
- Missing error codes
- Async/sync mismatch
- Authentication gaps
- Unhandled edge cases

### 2. FRONTEND / CONSUMER

**Responsibilities:**
- UI components
- State management
- API client layer
- Error handling and user feedback
- Data binding and display

**Typical Failure Modes:**
- Calls to non-existent endpoints
- Incorrect payload structure
- Missing error handlers
- Type mismatches
- Stale state display

### 3. ORCHESTRATION / HANDOFF

**Responsibilities:**
- Contract definition
- Schema synchronization
- Integration testing
- Handoff documentation
- Deployment coordination

**Typical Failure Modes:**
- No formal contract exists
- Skipped integration testing
- Undocumented assumptions
- Version drift between components
- Miscommunication between teams

---

## CRITICAL INSIGHT

> In multi-agent or multi-team development, the **orchestration layer is statistically the most common failure point**. Each agent/team operates with correct internal logic but incompatible external assumptions.

---

## DIAGNOSTIC DECISION TREE

Ask these questions in order to isolate the failure domain:

```
1. Does a formal API contract exist?
   │
   ├── NO ──────────────────────► ORCHESTRATION FAILURE
   │                              (Create contract first)
   │
   └── YES
       │
       2. Does the backend implementation match the contract?
          │
          ├── NO ─────────────────► BACKEND FAILURE
          │                         (Fix implementation or update contract)
          │
          └── YES
              │
              3. Does the frontend implementation match the contract?
                 │
                 ├── NO ────────────► FRONTEND FAILURE
                 │                    (Fix implementation)
                 │
                 └── YES
                     │
                     4. Was integration testing performed?
                        │
                        ├── NO ─────► ORCHESTRATION FAILURE
                        │             (Run integration tests)
                        │
                        └── YES
                            │
                            5. Did a recent change break the contract?
                               │
                               ├── YES ─► Determine which side changed
                               │          without updating contract
                               │
                               └── NO ──► Investigate deeper
                                          (edge case, timing, state)
```

---

## ATTRIBUTION QUESTIONS

For any integration failure, answer these:

### Contract Questions
- Does an API contract exist for this endpoint? (OpenAPI spec?)
- Is the contract up to date?
- Are both sides aware of the contract?

### Backend Questions
- Does the backend implement the contract correctly?
- Are all error codes documented and returned correctly?
- Is authentication behaving as documented?

### Frontend Questions
- Does the frontend follow the contract correctly?
- Are all response types handled?
- Are all error codes handled?

### Orchestration Questions
- Was the contract shared with both teams?
- Were integration tests run?
- Was there a recent change that wasn't coordinated?

---

## ATTRIBUTION TEMPLATE

When documenting an integration failure:

```markdown
# Integration Failure Report

## Failure Description
[What happened? What was expected? What occurred instead?]

## Evidence
[Error messages, logs, screenshots]

## Contract Status
- Contract exists: [ ] YES  [ ] NO
- Contract location: _______________
- Contract last updated: _______________

## Diagnostic Results
1. Contract exists? _______________
2. Backend matches contract? _______________
3. Frontend matches contract? _______________
4. Integration tests run? _______________
5. Recent changes? _______________

## Attribution
**Primary Domain:** [ ] Backend  [ ] Frontend  [ ] Orchestration

**Root Cause:**
[Specific cause identified]

**Responsible Party:**
[Team or individual responsible for fix]

## Remediation
[Steps to fix]
```

---

## ESCALATION PATH

| Situation | Escalation |
|-----------|------------|
| Both sides claim they match contract | Review contract together, run contract tests |
| Contract doesn't exist | Orchestration must create it |
| Contract is ambiguous | Clarify and update contract |
| Disagreement on who should change | Architecture review |
| Repeated failures | Process review |

---

## PREVENTION

After each failure attribution:

1. **Identify** the root cause category
2. **Add** a check to the integration checklist
3. **Automate** detection if possible
4. **Document** in lessons learned

---

*ATTRIBUTION v1.0 | INTEGRATION | BIBLE_MODULES*
