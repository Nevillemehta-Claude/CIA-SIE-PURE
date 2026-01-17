# REMEDIATION PROTOCOL
## How to Fix Integration Gaps

**Module:** INTEGRATION
**Version:** 1.0

---

## IMMEDIATE ACTIONS (Before Any Further Development)

When integration gaps are discovered:

### 1. STOP
Halt all new feature development until gaps are documented.

### 2. INVENTORY
List all backend endpoints and all frontend API calls.

### 3. COMPARE
Identify mismatches between the two lists.

### 4. DOCUMENT
Create or update the OpenAPI specification.

### 5. SHARE
Ensure all agents/teams have access to the contract.

---

## SHORT-TERM ACTIONS (Current Sprint)

### 1. Generate Types
Create TypeScript types from OpenAPI specification.

```bash
# Example using openapi-typescript
npx openapi-typescript ./api-spec.yaml -o ./src/types/api.ts
```

### 2. Validate Contracts
Run contract tests to identify all schema drift.

```bash
# Example using Prism
prism mock ./api-spec.yaml
# Then run frontend against mock
```

### 3. Fix Gaps
Remediate all identified gaps, prioritizing critical user flows.

| Priority | Fix |
|----------|-----|
| 1 | Auth/session gaps (security) |
| 2 | Phantom features (user-facing) |
| 3 | Schema drift (runtime errors) |
| 4 | Error handling gaps (UX) |
| 5 | Orphaned endpoints (tech debt) |

### 4. Test End-to-End
Write and run end-to-end tests for critical paths.

### 5. Update RTM
Change status from VERIFY to PASS or FAIL.

---

## MEDIUM-TERM ACTIONS (Next Release)

### 1. Automate Contract Testing
Integrate contract testing into CI/CD pipeline.

```yaml
# Example CI step
- name: Contract Tests
  run: |
    npx dredd ./api-spec.yaml http://localhost:8000
```

### 2. Set Up Drift Detection
Configure alerts when contract changes without coordination.

### 3. Establish Living Documentation
Documentation that updates automatically with code.

### 4. Train Team
Ensure all team members understand the integration protocol.

---

## ONGOING DISCIPLINE

### Contract-First Development
Update spec before implementation. Never implement first.

```
1. Update OpenAPI spec
2. Review with other team
3. Generate types
4. Implement backend
5. Implement frontend
6. Run contract tests
7. Merge
```

### Breaking Change Protocol
For any breaking API change:

1. Major version bump (v1 → v2)
2. Migration guide written
3. Deprecation warning added to old endpoint
4. Both versions supported during transition
5. Old version removed after migration complete

### RTM Maintenance
Update traceability matrix on every requirement change.

### Regular Audits
Run full integration checklist before each release.

---

## REMEDIATION BY GAP TYPE

### Schema Drift

**Immediate:**
1. Identify which side is "correct" (usually contract)
2. Update the incorrect implementation
3. Regenerate types
4. Run contract tests

**Prevention:**
- Type generation from OpenAPI in CI
- Contract tests required to pass

### Orphaned Endpoint

**Immediate:**
1. Verify endpoint is truly unused (check analytics)
2. If unused, deprecate
3. Schedule removal

**Prevention:**
- RTM review before each release
- Dead code analysis

### Phantom Feature

**Immediate:**
1. Implement missing backend endpoint, OR
2. Remove frontend call if feature cancelled
3. Update RTM

**Prevention:**
- Contract-first development
- RTM forward trace before frontend work

### State Mismatch

**Immediate:**
1. Document correct state machine
2. Align both sides
3. Add state transition tests

**Prevention:**
- Event Storming for new features
- State machine documentation required

### Error Handling Gap

**Immediate:**
1. Enumerate all possible error codes
2. Add handling for each
3. Test error paths

**Prevention:**
- Error code coverage in contract tests
- Required error handling code review

### Auth/Session Gap

**Immediate:**
1. Align token lifetimes
2. Implement proper refresh
3. Security audit

**Prevention:**
- Auth flow documentation required
- Security testing in CI

### Timing Gap

**Immediate:**
1. Document async behavior
2. Implement appropriate handling (polling, callbacks)
3. Add loading states

**Prevention:**
- Async behavior must be in contract
- Sequence diagrams for complex flows

### Protocol Mismatch

**Immediate:**
1. Align on protocol
2. Implement missing protocol support
3. Update documentation

**Prevention:**
- C4 Container diagram shows protocols
- Protocol agreement in architecture phase

---

## REMEDIATION CHECKLIST

After fixing any integration gap:

- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Contract tests passing
- [ ] RTM updated
- [ ] Documentation updated
- [ ] Regression tests added
- [ ] Prevention measure identified
- [ ] Prevention measure implemented or scheduled

---

*REMEDIATION v1.0 | INTEGRATION | BIBLE_MODULES*
