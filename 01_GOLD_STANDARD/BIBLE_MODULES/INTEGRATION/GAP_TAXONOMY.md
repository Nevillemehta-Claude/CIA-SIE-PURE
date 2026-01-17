# INTEGRATION GAP TAXONOMY
## Classification of Integration Failures

**Module:** INTEGRATION
**Version:** 1.0

---

## OVERVIEW

Integration failures manifest in predictable patterns. This taxonomy classifies gaps by type, enabling systematic detection and remediation.

---

## GAP TYPES

### 1. SCHEMA DRIFT

**Definition:** Consumer expects different data structure than provider delivers.

**Symptoms:**
- Runtime errors
- Undefined values
- Type errors

**Detection Methods:**
- Contract testing
- TypeScript compilation
- Schema validation

**Example:**
```
Frontend expects: { user_name: string }
Backend returns:  { userName: string }
```

**Root Cause:** Naming convention mismatch, outdated types, missing regeneration

---

### 2. ORPHANED ENDPOINT

**Definition:** Backend exposes API that no frontend consumes.

**Symptoms:**
- Dead code
- Wasted resources
- Maintenance burden

**Detection Methods:**
- RTM backward trace
- API usage analytics
- Code coverage for endpoints

**Example:**
```
Backend: GET /api/v1/legacy-reports
Frontend: Never calls this endpoint
```

**Root Cause:** Feature removed from frontend but not backend, speculative implementation

---

### 3. PHANTOM FEATURE

**Definition:** Frontend calls endpoint that doesn't exist.

**Symptoms:**
- 404 errors
- Broken features
- User-facing failures

**Detection Methods:**
- RTM forward trace
- Runtime monitoring
- Integration tests

**Example:**
```
Frontend: calls GET /api/v1/notifications
Backend: Endpoint not implemented
```

**Root Cause:** Frontend built ahead of backend, miscommunication, typos in URLs

---

### 4. STATE MISMATCH

**Definition:** Different understanding of entity lifecycle between components.

**Symptoms:**
- Inconsistent UI
- Stale data display
- Race conditions

**Detection Methods:**
- Event Storming
- State machine validation
- Integration testing

**Example:**
```
Frontend: Assumes order can be cancelled anytime
Backend: Order cannot be cancelled after shipping
```

**Root Cause:** Incomplete state machine documentation, missing state transitions

---

### 5. ERROR HANDLING GAP

**Definition:** Consumer doesn't handle all provider error codes.

**Symptoms:**
- Unhandled exceptions
- Poor user experience
- Silent failures

**Detection Methods:**
- Error code coverage analysis
- Contract testing
- Exception monitoring

**Example:**
```
Backend returns: 429 Too Many Requests
Frontend handles: Only 200, 400, 500
```

**Root Cause:** Incomplete error enumeration, added errors not communicated

---

### 6. AUTH/SESSION GAP

**Definition:** Token handling inconsistencies between frontend and backend.

**Symptoms:**
- Authentication failures
- Security vulnerabilities
- Session drops

**Detection Methods:**
- Security testing
- Auth flow audit
- Token lifecycle testing

**Example:**
```
Frontend: Expects token refresh at 15 min
Backend: Token expires at 10 min
```

**Root Cause:** Misaligned token lifetimes, refresh logic errors

---

### 7. TIMING GAP

**Definition:** Sync assumption when behavior is async, or vice versa.

**Symptoms:**
- Missing data on display
- UI glitches
- Race conditions

**Detection Methods:**
- Sequence diagrams
- Async audit
- Load testing

**Example:**
```
Frontend: Expects immediate response
Backend: Returns 202 Accepted, processes async
```

**Root Cause:** Async behavior undocumented, polling not implemented

---

### 8. PROTOCOL MISMATCH

**Definition:** Different expectations about communication protocol.

**Symptoms:**
- Connection failures
- Data format errors
- Timeout issues

**Detection Methods:**
- Architecture review
- C4 Container diagram
- Protocol testing

**Example:**
```
Frontend: Expects WebSocket for real-time
Backend: Implements REST polling only
```

**Root Cause:** Architecture decisions not communicated, technology assumptions

---

## GAP SEVERITY CLASSIFICATION

| Severity | Definition | Response |
|----------|------------|----------|
| **CRITICAL** | System unusable, data loss possible | Immediate fix, block release |
| **HIGH** | Major feature broken | Fix before release |
| **MEDIUM** | Feature degraded but usable | Fix in current sprint |
| **LOW** | Minor inconvenience | Schedule for future |

### Severity by Gap Type

| Gap Type | Typical Severity | Notes |
|----------|------------------|-------|
| Schema Drift | HIGH-CRITICAL | Depends on data criticality |
| Orphaned Endpoint | LOW | Technical debt |
| Phantom Feature | HIGH | User-facing failure |
| State Mismatch | HIGH | Data integrity risk |
| Error Handling Gap | MEDIUM | UX degradation |
| Auth/Session Gap | CRITICAL | Security risk |
| Timing Gap | MEDIUM-HIGH | Depends on feature |
| Protocol Mismatch | HIGH | Complete feature failure |

---

## DETECTION MATRIX

| Gap Type | Contract Test | RTM Check | C4 Review | Event Storm | Runtime Monitor |
|----------|:-------------:|:---------:|:---------:|:-----------:|:---------------:|
| Schema Drift | PRIMARY | - | - | - | SECONDARY |
| Orphaned Endpoint | - | PRIMARY | SECONDARY | - | - |
| Phantom Feature | - | PRIMARY | SECONDARY | - | SECONDARY |
| State Mismatch | SECONDARY | - | - | PRIMARY | - |
| Error Handling Gap | PRIMARY | - | - | - | SECONDARY |
| Auth/Session Gap | SECONDARY | - | - | - | PRIMARY |
| Timing Gap | - | - | SECONDARY | PRIMARY | SECONDARY |
| Protocol Mismatch | - | - | PRIMARY | - | SECONDARY |

---

## PREVENTION STRATEGIES

### Contract-First Development
Define API contract before implementation. Both sides implement to same contract.

### Continuous Contract Testing
Run contract tests in CI/CD. Catch drift before merge.

### RTM Maintenance
Update traceability matrix with every change. Review for gaps regularly.

### Event Storming Sessions
Conduct before major features. Resolve all red hotspots.

### Integration Testing
Test full flows, not just units. Verify actual communication.

---

*GAP_TAXONOMY v1.0 | INTEGRATION | BIBLE_MODULES*
