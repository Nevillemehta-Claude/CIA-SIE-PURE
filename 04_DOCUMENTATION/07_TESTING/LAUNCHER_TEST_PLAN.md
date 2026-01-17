# CIA-SIE LAUNCHER SYSTEM - TEST PLAN

**Document ID:** TEST-LAUNCHER-001  
**Version:** 1.0.0  
**Date:** 12 January 2026  
**Status:** DRAFT → PENDING EXECUTION  
**Related Specification:** SPEC-LAUNCHER-001 v1.0.0  
**Related Design:** DESIGN-LAUNCHER-001 v1.0.0  

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Test Scope](#2-test-scope)
3. [Test Environment](#3-test-environment)
4. [Test Categories](#4-test-categories)
5. [Unit Tests](#5-unit-tests)
6. [Integration Tests](#6-integration-tests)
7. [User Acceptance Tests](#7-user-acceptance-tests)
8. [Regression Tests](#8-regression-tests)
9. [Test Execution Schedule](#9-test-execution-schedule)
10. [Test Results Template](#10-test-results-template)

---

## 1. OVERVIEW

### 1.1 Purpose

This document defines the test plan for verifying the CIA-SIE Launcher System meets all requirements specified in SPEC-LAUNCHER-001.

### 1.2 Test Objectives

| Objective | Priority |
|-----------|----------|
| Verify all functional requirements are met | CRITICAL |
| Verify non-functional requirements (performance, reliability) | HIGH |
| Verify error handling works correctly | HIGH |
| Verify user experience is intuitive | MEDIUM |

### 1.3 Success Criteria

The Launcher System passes testing when:

1. ✅ All CRITICAL tests pass
2. ✅ All HIGH priority tests pass
3. ✅ No blocking defects remain
4. ⚠️ Any MEDIUM priority failures are documented with mitigation

---

## 2. TEST SCOPE

### 2.1 In Scope

| Component | Test Type |
|-----------|-----------|
| `start-cia-sie.command` | Functional, UAT |
| `stop-cia-sie.command` | Functional, UAT |
| `ignite.sh` | Unit, Integration |
| `shutdown.sh` | Unit, Integration |
| `health-check.sh` | Unit, Integration |
| `utils.sh` | Unit |
| `config.sh` | Unit |

### 2.2 Out of Scope

| Item | Reason |
|------|--------|
| Backend functionality | Covered by separate test suite |
| Frontend functionality | Not yet built |
| External APIs | Mocked for testing |

---

## 3. TEST ENVIRONMENT

### 3.1 Required Environment

| Component | Requirement |
|-----------|-------------|
| OS | macOS 13+ (Ventura or later) |
| Shell | zsh (default) |
| Python | 3.11+ with virtual environment |
| ngrok | 3.x installed and configured |
| Ports | 8000, 5173, 4040 available |

### 3.2 Pre-Test Setup

```bash
# 1. Ensure no services are running
pkill -f "uvicorn.*cia_sie" 2>/dev/null
pkill -f "ngrok http" 2>/dev/null

# 2. Clean PID files
rm -f pids/*.pid

# 3. Verify virtual environment
test -f venv/bin/activate && echo "venv OK" || echo "venv MISSING"

# 4. Verify ports available
lsof -i :8000 -sTCP:LISTEN || echo "Port 8000 OK"
lsof -i :5173 -sTCP:LISTEN || echo "Port 5173 OK"
```

---

## 4. TEST CATEGORIES

### 4.1 Test Priority Levels

| Priority | Description | Failure Impact |
|----------|-------------|----------------|
| **P0 - CRITICAL** | Core functionality | Blocks release |
| **P1 - HIGH** | Important features | Significant degradation |
| **P2 - MEDIUM** | Nice-to-have features | Minor inconvenience |
| **P3 - LOW** | Edge cases | Cosmetic issues |

### 4.2 Test Types

| Type | Description |
|------|-------------|
| **Unit** | Individual function testing |
| **Integration** | Component interaction testing |
| **UAT** | User acceptance testing |
| **Regression** | Ensure changes don't break existing |

---

## 5. UNIT TESTS

### 5.1 config.sh Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| UT-CFG-001 | Default values set | Source config.sh, check BACKEND_PORT | 8000 | P0 |
| UT-CFG-002 | Environment override works | Set CIA_SIE_BACKEND_PORT=9000, source config.sh | BACKEND_PORT=9000 | P1 |
| UT-CFG-003 | PROJECT_ROOT auto-detection | Source from different directory | Correct path resolved | P0 |
| UT-CFG-004 | Paths derived correctly | Check VENV_PATH, LOGS_PATH | Paths relative to PROJECT_ROOT | P1 |

### 5.2 utils.sh Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| UT-UTL-001 | print_header displays correctly | Call print_header "TEST" | Formatted box output | P2 |
| UT-UTL-002 | log_message writes to file | Call log_message "INFO" "TEST" "message" | Entry in launcher.log | P1 |
| UT-UTL-003 | save_pid creates file | Call save_pid "test" "12345" | pids/test.pid contains 12345 | P0 |
| UT-UTL-004 | get_pid reads file | Create PID file, call get_pid | Returns correct PID | P0 |
| UT-UTL-005 | remove_pid deletes file | Create PID file, call remove_pid | File removed | P0 |
| UT-UTL-006 | is_process_running true | Get current shell PID, test | Returns 0 | P0 |
| UT-UTL-007 | is_process_running false | Test with non-existent PID | Returns 1 | P0 |
| UT-UTL-008 | check_port_available true | Test unused port | Returns 0 | P0 |
| UT-UTL-009 | check_port_available false | Start listener, test | Returns 1 | P0 |
| UT-UTL-010 | ensure_directory creates | Call on non-existent path | Directory created | P1 |

### 5.3 health-check.sh Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| UT-HLT-001 | check_backend_health when running | Start backend, call function | Returns 0 | P0 |
| UT-HLT-002 | check_backend_health when stopped | Stop backend, call function | Returns 1 | P0 |
| UT-HLT-003 | wait_for_backend succeeds | Start backend, call function | Returns 0 within timeout | P0 |
| UT-HLT-004 | wait_for_backend times out | No backend, call function | Returns 1 after retries | P0 |

---

## 6. INTEGRATION TESTS

### 6.1 Ignition Sequence Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| IT-IGN-001 | Full ignition success | Run start-cia-sie.command | All services start, status shown | P0 |
| IT-IGN-002 | Backend starts and healthy | Run ignite, check health endpoint | curl localhost:8000/health → 200 | P0 |
| IT-IGN-003 | ngrok tunnel establishes | Run ignite with ngrok enabled | Public URL displayed | P1 |
| IT-IGN-004 | Frontend graceful skip | Run ignite without frontend dir | Warning shown, continues | P0 |
| IT-IGN-005 | Browser opens | Run ignite with OPEN_BROWSER=true | Browser opens | P2 |
| IT-IGN-006 | PID files created | Run ignite, check pids/ | backend.pid exists | P0 |
| IT-IGN-007 | Log file created | Run ignite, check logs/ | launcher.log has entries | P1 |

### 6.2 Shutdown Sequence Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| IT-SHT-001 | Full shutdown success | Run stop-cia-sie.command | All services stop | P0 |
| IT-SHT-002 | Backend stops | Run shutdown, check process | No uvicorn process | P0 |
| IT-SHT-003 | ngrok stops | Run shutdown, check process | No ngrok process | P1 |
| IT-SHT-004 | PID files cleaned | Run shutdown, check pids/ | No PID files remain | P0 |
| IT-SHT-005 | Graceful when not running | Run shutdown with nothing running | Completes without error | P0 |

### 6.3 Error Handling Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| IT-ERR-001 | Port conflict detected | Occupy port 8000, run ignite | Error E003 displayed | P0 |
| IT-ERR-002 | Missing venv detected | Rename venv, run ignite | Error E002 displayed | P0 |
| IT-ERR-003 | Health check timeout | Start broken backend, run ignite | Error E005 after timeout | P1 |
| IT-ERR-004 | Recovery after failed start | Fix issue, run ignite again | Starts successfully | P0 |

### 6.4 Signal Handling Tests

| Test ID | Description | Steps | Expected | Priority |
|---------|-------------|-------|----------|----------|
| IT-SIG-001 | Ctrl+C triggers shutdown | Start system, press Ctrl+C | Clean shutdown executed | P0 |
| IT-SIG-002 | SIGTERM triggers shutdown | Start system, send SIGTERM | Clean shutdown executed | P1 |

---

## 7. USER ACCEPTANCE TESTS

### 7.1 Start System (UAT-01)

**Objective:** Verify a user can start the system with a single action

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate `start-cia-sie.command` in Finder | File visible in project root |
| 2 | Double-click the file | Terminal window opens |
| 3 | Observe output | Step-by-step progress displayed |
| 4 | Wait for completion | Status box shows all services |
| 5 | Verify browser | Browser opens to /docs |
| 6 | Test API | curl localhost:8000/health returns 200 |

**Pass Criteria:** All steps complete without manual intervention

---

### 7.2 Stop System (UAT-02)

**Objective:** Verify a user can stop the system with a single action

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Locate `stop-cia-sie.command` in Finder | File visible in project root |
| 2 | Double-click the file | Terminal window opens |
| 3 | Observe output | Step-by-step progress displayed |
| 4 | Wait for completion | "SHUTDOWN COMPLETE" shown |
| 5 | Verify services | No CIA-SIE processes running |
| 6 | Press Enter | Terminal window closes |

**Pass Criteria:** All services stop, terminal prompts before closing

---

### 7.3 Start-Stop-Start Cycle (UAT-03)

**Objective:** Verify system can be restarted

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Start system | All services running |
| 2 | Stop system | All services stopped |
| 3 | Start system again | All services running again |
| 4 | Verify API | Health check passes |

**Pass Criteria:** System restarts cleanly without issues

---

### 7.4 Error Feedback (UAT-04)

**Objective:** Verify user receives clear error messages

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Occupy port 8000 (e.g., nc -l 8000) | Port in use |
| 2 | Run start-cia-sie.command | Error displayed |
| 3 | Observe error message | Plain English, suggests lsof |
| 4 | Release port 8000 | Port available |
| 5 | Run start again | System starts successfully |

**Pass Criteria:** Error message is understandable, actionable

---

### 7.5 Missing Frontend Warning (UAT-05)

**Objective:** Verify system works without frontend

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify no frontend/ directory | Directory absent |
| 2 | Run start-cia-sie.command | System starts |
| 3 | Observe frontend step | Warning shown (not error) |
| 4 | Verify backend | Backend operational |
| 5 | Verify API | curl localhost:8000/docs works |

**Pass Criteria:** Backend works, warning is informative

---

## 8. REGRESSION TESTS

### 8.1 After Code Changes

Run these tests after any modification to launcher scripts:

| Test ID | Test | Command |
|---------|------|---------|
| REG-001 | Config loads | `source scripts/launcher/config.sh && echo $PROJECT_ROOT` |
| REG-002 | Utils functions exist | `source scripts/launcher/utils.sh && type print_header` |
| REG-003 | Start succeeds | `./start-cia-sie.command` (manual) |
| REG-004 | Stop succeeds | `./stop-cia-sie.command` (manual) |
| REG-005 | Health check works | `curl -s localhost:8000/health` |

---

## 9. TEST EXECUTION SCHEDULE

### 9.1 Execution Plan

| Phase | Tests | Timing |
|-------|-------|--------|
| 1. Unit Tests | UT-* | Immediately after implementation |
| 2. Integration Tests | IT-* | After unit tests pass |
| 3. User Acceptance Tests | UAT-* | After integration tests pass |
| 4. Regression Tests | REG-* | Before final approval |

### 9.2 Test Execution Checklist

```
□ Pre-test setup completed
□ Unit tests executed
□ Unit test results documented
□ Integration tests executed
□ Integration test results documented
□ UAT executed
□ UAT results documented
□ All P0 tests pass
□ All P1 tests pass
□ Test results reviewed
□ Sign-off obtained
```

---

## 10. TEST RESULTS TEMPLATE

### 10.1 Individual Test Result

```markdown
## Test ID: [TEST-ID]

**Date:** [YYYY-MM-DD]
**Tester:** [Name]
**Environment:** [macOS version, shell, etc.]

### Execution

| Step | Action | Actual Result |
|------|--------|---------------|
| 1 | ... | ... |

### Result

- [ ] PASS
- [ ] FAIL
- [ ] BLOCKED

### Notes

[Any observations, deviations, or issues]

### Evidence

[Screenshots, log excerpts, command outputs]
```

### 10.2 Summary Template

```markdown
## Test Execution Summary

**Date:** [YYYY-MM-DD]
**Executor:** [Name]

### Results

| Category | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| Unit | XX | XX | XX | XX |
| Integration | XX | XX | XX | XX |
| UAT | XX | XX | XX | XX |

### Critical Issues

1. [Issue description, test ID]

### Recommendations

1. [Recommendation]

### Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Tester | | | |
| Reviewer | | | |
```

---

## DOCUMENT APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | Claude (AI Assistant) | — | 12 Jan 2026 |
| Technical Review | Pending | | |
| Project Principal | Neville Mehta | | |

---

**END OF TEST PLAN**
