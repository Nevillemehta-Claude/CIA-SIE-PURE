# CIA-SIE LAUNCHER SYSTEM SPECIFICATION

**Document ID:** SPEC-LAUNCHER-001  
**Version:** 1.0.0  
**Date:** 12 January 2026  
**Status:** DRAFT → PENDING APPROVAL  
**Author:** Claude (AI Assistant)  
**Reviewed By:** Neville Mehta (Project Principal)  

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Purpose and Scope](#2-purpose-and-scope)
3. [Definitions and Acronyms](#3-definitions-and-acronyms)
4. [System Overview](#4-system-overview)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Technical Constraints](#7-technical-constraints)
8. [Dependencies](#8-dependencies)
9. [User Interface Requirements](#9-user-interface-requirements)
10. [Success Criteria](#10-success-criteria)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [Risk Assessment](#12-risk-assessment)
13. [Appendices](#13-appendices)

---

## 1. EXECUTIVE SUMMARY

### 1.1 Problem Statement

The CIA-SIE platform currently requires manual execution of multiple terminal commands in a specific sequence to start and stop the system. This process:

- Requires technical knowledge of command-line operations
- Is error-prone due to sequence dependencies
- Does not provide visual feedback on system status
- Creates a barrier for non-technical users

### 1.2 Proposed Solution

Create a **Launcher System** consisting of two executable files that:

- **START**: Ignites all system components in the correct dependency order
- **STOP**: Gracefully shuts down all components in reverse order

### 1.3 Success Definition

The Launcher System is successful when a non-technical user can:

1. Double-click `start-cia-sie.command` to start the entire system
2. Double-click `stop-cia-sie.command` to stop the entire system
3. Observe clear visual feedback during start/stop operations
4. Have the system reach a fully operational state without manual intervention

---

## 2. PURPOSE AND SCOPE

### 2.1 Purpose

To provide a simple, reliable, one-click mechanism for starting and stopping the CIA-SIE platform, abstracting away all technical complexity from the end user.

### 2.2 In Scope

| Item | Description |
|------|-------------|
| Start Script | Executable that starts all services in order |
| Stop Script | Executable that stops all services in order |
| Health Verification | Automated checks to confirm service readiness |
| Visual Feedback | Terminal output showing progress and status |
| Error Handling | Graceful handling of failure scenarios |
| Logging | Record of start/stop operations |

### 2.3 Out of Scope

| Item | Reason |
|------|--------|
| GUI Application | Deferred to MCC (Mission Control Console) phase |
| System Tray Icon | Deferred to MCC phase |
| Auto-restart on Failure | Deferred to future enhancement |
| Remote Management | Not required for local development |
| Windows/Linux Support | macOS only per project requirements |

### 2.4 Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Neville Mehta | Project Principal | Primary user; requires simplicity |
| Development Team | Future developers | Maintenance and extension |
| System | Backend/Frontend | Must be started/stopped correctly |

---

## 3. DEFINITIONS AND ACRONYMS

| Term | Definition |
|------|------------|
| **Ignition** | The process of starting a component or the entire system |
| **Shutdown** | The process of gracefully stopping a component or the entire system |
| **Health Check** | Verification that a component is running and responsive |
| **Dependency Order** | The sequence in which components must start (determined by their dependencies) |
| **Reverse Order** | The opposite of dependency order (used for shutdown) |
| **venv** | Python Virtual Environment containing project dependencies |
| **uvicorn** | ASGI server that runs the FastAPI backend |
| **ngrok** | Tunnel service that exposes localhost to the internet |
| **PID** | Process Identifier; unique number assigned to each running process |

---

## 4. SYSTEM OVERVIEW

### 4.1 Component Inventory

The CIA-SIE platform consists of the following components that must be managed:

| Component | Type | Port | Dependency |
|-----------|------|------|------------|
| Python Virtual Environment | Environment | N/A | None (base) |
| Backend Server (FastAPI) | Service | 8000 | venv |
| ngrok Tunnel | Service | N/A | Backend |
| Frontend Server (React) | Service | 5173 | Backend |
| Browser | Application | N/A | Frontend |

### 4.2 Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   IGNITION ORDER (Start from bottom, move up)                  │
│                                                                 │
│                         ┌──────────┐                            │
│                         │ BROWSER  │  ◄── Step 5: Open browser │
│                         └────┬─────┘                            │
│                              │                                  │
│                         ┌────▼─────┐                            │
│                         │ FRONTEND │  ◄── Step 4: Start React  │
│                         └────┬─────┘                            │
│                              │                                  │
│                         ┌────▼─────┐                            │
│                         │  NGROK   │  ◄── Step 3: Start tunnel │
│                         └────┬─────┘                            │
│                              │                                  │
│                         ┌────▼─────┐                            │
│                         │ BACKEND  │  ◄── Step 2: Start API    │
│                         └────┬─────┘                            │
│                              │                                  │
│                         ┌────▼─────┐                            │
│                         │   VENV   │  ◄── Step 1: Activate     │
│                         └──────────┘                            │
│                                                                 │
│   SHUTDOWN ORDER (Start from top, move down)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Current State Assumption

Per the forensic analysis and Technical Memorandum (CIA-SIE-TM-2026-001-FRONTEND-INIT):

| Component | Current State | Notes |
|-----------|---------------|-------|
| Backend | ✅ Ready to start | All code exists |
| ngrok | ✅ Ready to start | Installed and configured |
| Frontend | ❌ Does not exist | Will be skipped with notification |
| Browser | ✅ Available | System application |

---

## 5. FUNCTIONAL REQUIREMENTS

### 5.1 FR-001: Start All Services

**Description:** The system shall provide a mechanism to start all services with a single action.

**Priority:** CRITICAL

**Details:**
- User double-clicks `start-cia-sie.command`
- Script activates Python virtual environment
- Script starts Backend server
- Script waits for Backend health confirmation
- Script starts ngrok tunnel
- Script attempts to start Frontend (graceful skip if not exists)
- Script opens browser to application URL
- Script displays final status summary

**Acceptance Criteria:**
- AC-001-1: Backend reaches healthy state within 30 seconds
- AC-001-2: ngrok tunnel establishes within 15 seconds
- AC-001-3: User sees clear status messages for each step
- AC-001-4: Browser opens automatically upon success

### 5.2 FR-002: Stop All Services

**Description:** The system shall provide a mechanism to stop all services with a single action.

**Priority:** CRITICAL

**Details:**
- User double-clicks `stop-cia-sie.command`
- Script identifies running CIA-SIE processes
- Script stops Frontend server (if running)
- Script stops ngrok tunnel (if running)
- Script stops Backend server (if running)
- Script confirms all processes terminated
- Script displays final status summary

**Acceptance Criteria:**
- AC-002-1: All CIA-SIE processes terminate within 30 seconds
- AC-002-2: No orphan processes remain
- AC-002-3: User sees confirmation of each service stopping
- AC-002-4: Script exits cleanly

### 5.3 FR-003: Health Verification

**Description:** The system shall verify each service is healthy before proceeding to the next.

**Priority:** HIGH

**Details:**
- After starting Backend, call `/health` endpoint
- Retry up to 10 times with 2-second intervals
- Only proceed to ngrok after Backend is confirmed healthy
- Log health check results

**Acceptance Criteria:**
- AC-003-1: Backend health verified via HTTP request
- AC-003-2: Timeout after 20 seconds if unhealthy
- AC-003-3: Clear error message if health check fails

### 5.4 FR-004: Visual Feedback

**Description:** The system shall provide clear visual feedback during operations.

**Priority:** HIGH

**Details:**
- Display step-by-step progress
- Use visual indicators (✓, ✗, ⏳) for status
- Show elapsed time for each step
- Display final summary with all service states

**Acceptance Criteria:**
- AC-004-1: Each step clearly labeled
- AC-004-2: Success/failure visually distinct
- AC-004-3: Summary shows all service states

### 5.5 FR-005: Error Handling

**Description:** The system shall handle errors gracefully without crashing.

**Priority:** HIGH

**Details:**
- Catch and report process start failures
- Provide actionable error messages
- Offer recovery suggestions
- Log errors for debugging

**Acceptance Criteria:**
- AC-005-1: Script never exits without explanation
- AC-005-2: Error messages are human-readable
- AC-005-3: Logs capture technical details

### 5.6 FR-006: Graceful Degradation

**Description:** The system shall continue operation even if optional components fail.

**Priority:** MEDIUM

**Details:**
- If Frontend doesn't exist, notify user and continue
- If ngrok fails, offer to continue without tunnel
- Core functionality (Backend) failure is fatal

**Acceptance Criteria:**
- AC-006-1: Missing Frontend shows warning, not error
- AC-006-2: Optional component failures don't stop ignition
- AC-006-3: Critical failures abort with clear message

### 5.7 FR-007: Logging

**Description:** The system shall log all operations for troubleshooting.

**Priority:** MEDIUM

**Details:**
- Log to `/logs/launcher.log`
- Include timestamps
- Log start/stop events
- Log errors with stack traces

**Acceptance Criteria:**
- AC-007-1: Log file created in logs directory
- AC-007-2: All events timestamped
- AC-007-3: Errors include context

---

## 6. NON-FUNCTIONAL REQUIREMENTS

### 6.1 NFR-001: Performance

| Metric | Requirement |
|--------|-------------|
| Total start time | < 60 seconds |
| Total stop time | < 30 seconds |
| Health check latency | < 5 seconds per check |

### 6.2 NFR-002: Reliability

| Metric | Requirement |
|--------|-------------|
| Start success rate | > 99% (given all prerequisites met) |
| Stop success rate | 100% |
| Crash recovery | Script never hangs indefinitely |

### 6.3 NFR-003: Usability

| Metric | Requirement |
|--------|-------------|
| User actions required | 1 (double-click) |
| Technical knowledge required | None |
| Error message clarity | Understandable by non-technical user |

### 6.4 NFR-004: Maintainability

| Metric | Requirement |
|--------|-------------|
| Code documentation | Inline comments for each section |
| Configuration separation | Variables in config file |
| Extensibility | Easy to add new services |

### 6.5 NFR-005: Compatibility

| Metric | Requirement |
|--------|-------------|
| Operating System | macOS 13+ (Ventura and later) |
| Shell | /bin/zsh (default on macOS) |
| Terminal | Native Terminal.app |

---

## 7. TECHNICAL CONSTRAINTS

### 7.1 Environment Constraints

| Constraint | Description |
|------------|-------------|
| TC-001 | Must use existing Python virtual environment at `/venv/` |
| TC-002 | Must use existing project structure |
| TC-003 | Backend must be started with uvicorn |
| TC-004 | Ports 8000 (backend) and 5173 (frontend) must be available |

### 7.2 Security Constraints

| Constraint | Description |
|------------|-------------|
| TC-005 | No hardcoded API keys in scripts |
| TC-006 | API keys must be read from environment or config |
| TC-007 | Scripts must not require sudo/root |

### 7.3 Operational Constraints

| Constraint | Description |
|------------|-------------|
| TC-008 | Must work without internet (except ngrok) |
| TC-009 | Must handle missing Frontend gracefully |
| TC-010 | Must not modify project source code |

---

## 8. DEPENDENCIES

### 8.1 Software Dependencies

| Dependency | Version | Purpose | Verification |
|------------|---------|---------|--------------|
| macOS | 13+ | Operating system | `sw_vers` |
| Python | 3.11+ | Backend runtime | `python3 --version` |
| Node.js | 18+ | Frontend runtime (when exists) | `node --version` |
| ngrok | 3.x | Webhook tunnel | `ngrok version` |
| curl | Any | Health checks | `which curl` |

### 8.2 Project Dependencies

| Dependency | Location | Purpose |
|------------|----------|---------|
| Virtual Environment | `/venv/` | Python packages |
| Backend Code | `/src/cia_sie/` | API server |
| Database | `/data/cia_sie.db` | Data storage |
| Logs Directory | `/logs/` | Log output |

### 8.3 Environment Variables

| Variable | Required | Purpose | Default |
|----------|----------|---------|---------|
| `ANTHROPIC_API_KEY` | For AI features | Claude API access | None |
| `KITE_API_KEY` | For Kite features | Zerodha integration | None |
| `KITE_API_SECRET` | For Kite features | Zerodha integration | None |

---

## 9. USER INTERFACE REQUIREMENTS

### 9.1 File Naming

| File | Purpose | User Action |
|------|---------|-------------|
| `start-cia-sie.command` | Start all services | Double-click |
| `stop-cia-sie.command` | Stop all services | Double-click |

**Note:** The `.command` extension is macOS-specific and allows double-click execution.

### 9.2 Terminal Output: Start Sequence

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🚀 CIA-SIE SYSTEM IGNITION                                                  ║
║   ══════════════════════════                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

[12:00:00] Starting CIA-SIE Platform...

STEP 1/5: Activating Python Environment
         ├── Location: /Users/.../CIA-SIE-PURE/venv
         └── Status: ✓ ACTIVATED

STEP 2/5: Starting Backend Server
         ├── Command: uvicorn src.cia_sie.main:app --port 8000
         ├── Port: 8000
         ├── Waiting for health check...
         └── Status: ✓ RUNNING (healthy)

STEP 3/5: Starting Webhook Tunnel
         ├── Command: ngrok http 8000
         ├── Public URL: https://abc123.ngrok.io
         └── Status: ✓ RUNNING

STEP 4/5: Starting Frontend Server
         ├── Location: /Users/.../CIA-SIE-PURE/frontend
         └── Status: ⚠ SKIPPED (directory not found)
                     Frontend has not been built yet.
                     Backend and API are fully operational.

STEP 5/5: Opening Browser
         ├── URL: http://localhost:8000/docs
         └── Status: ✓ OPENED

╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ✅ CIA-SIE SYSTEM IGNITION COMPLETE                                        ║
║                                                                               ║
║   Backend:   🟢 RUNNING    http://localhost:8000                              ║
║   Tunnel:    🟢 RUNNING    https://abc123.ngrok.io                            ║
║   Frontend:  ⚪ NOT BUILT  (run frontend build when ready)                    ║
║                                                                               ║
║   Press Ctrl+C to stop all services, or use stop-cia-sie.command             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 9.3 Terminal Output: Stop Sequence

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🛑 CIA-SIE SYSTEM SHUTDOWN                                                  ║
║   ══════════════════════════                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

[12:30:00] Stopping CIA-SIE Platform...

STEP 1/3: Stopping Frontend Server
         ├── Process: Not running
         └── Status: ✓ SKIPPED

STEP 2/3: Stopping Webhook Tunnel
         ├── Process: ngrok (PID 12346)
         └── Status: ✓ STOPPED

STEP 3/3: Stopping Backend Server
         ├── Process: uvicorn (PID 12345)
         └── Status: ✓ STOPPED

╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ✅ CIA-SIE SYSTEM SHUTDOWN COMPLETE                                        ║
║                                                                               ║
║   All services have been stopped.                                             ║
║   It is now safe to close this terminal.                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 9.4 Error Output Example

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ❌ IGNITION FAILED                                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

ERROR: Backend server failed to start

Details:
  • Port 8000 is already in use
  • Another process may be running

Suggested Actions:
  1. Run: lsof -i :8000  (to see what's using the port)
  2. Run: stop-cia-sie.command  (to stop any existing CIA-SIE processes)
  3. Try starting again

For technical support, see: /logs/launcher.log
```

---

## 10. SUCCESS CRITERIA

### 10.1 Primary Success Criteria

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| SC-01 | User can start system with single double-click | Manual test |
| SC-02 | User can stop system with single double-click | Manual test |
| SC-03 | Backend reaches healthy state automatically | Health check response |
| SC-04 | ngrok tunnel establishes automatically | URL displayed |
| SC-05 | Browser opens to application | Visual confirmation |

### 10.2 Secondary Success Criteria

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| SC-06 | Clear progress feedback during start | Terminal output review |
| SC-07 | Clear progress feedback during stop | Terminal output review |
| SC-08 | Graceful handling of missing Frontend | Warning displayed |
| SC-09 | All processes terminate on stop | PID verification |
| SC-10 | Logs written to launcher.log | File existence check |

---

## 11. ACCEPTANCE CRITERIA

### 11.1 User Acceptance Tests

| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| UAT-01 | Fresh start | Double-click start-cia-sie.command | All services start, browser opens |
| UAT-02 | Clean stop | Double-click stop-cia-sie.command | All services stop, no orphans |
| UAT-03 | Repeat start/stop | Start, stop, start again | System works on second start |
| UAT-04 | Port conflict | Start with port 8000 in use | Clear error message shown |
| UAT-05 | Missing Frontend | Start without frontend directory | Warning shown, backend still works |

### 11.2 Technical Acceptance Tests

| Test ID | Description | Verification |
|---------|-------------|--------------|
| TAT-01 | Backend health | `curl localhost:8000/health` returns 200 |
| TAT-02 | ngrok active | ngrok process running, URL accessible |
| TAT-03 | Process cleanup | `pgrep -f uvicorn` returns nothing after stop |
| TAT-04 | Log creation | launcher.log exists with entries |
| TAT-05 | No root required | Script runs without sudo |

---

## 12. RISK ASSESSMENT

### 12.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Port already in use | Medium | High | Check port, provide clear error |
| ngrok auth expired | Low | Medium | Verify auth on start, guide user |
| venv corrupted | Low | High | Verify venv before activation |
| Script permissions | Medium | Low | Set executable on creation |

### 12.2 User Experience Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Confusing error messages | Medium | High | Use plain English, provide next steps |
| Terminal closes too fast | Medium | Medium | Keep terminal open on error |
| User doesn't see output | Low | Medium | Clear visual formatting |

---

## 13. APPENDICES

### Appendix A: File Structure

```
CIA-SIE-PURE/
├── start-cia-sie.command       # User-facing start script
├── stop-cia-sie.command        # User-facing stop script
├── scripts/
│   └── launcher/
│       ├── config.sh           # Configuration variables
│       ├── ignite.sh           # Core start logic
│       ├── shutdown.sh         # Core stop logic
│       ├── health-check.sh     # Health verification
│       └── utils.sh            # Shared utilities
└── logs/
    └── launcher.log            # Operations log
```

### Appendix B: Configuration Variables

```bash
# config.sh

# Project paths
PROJECT_ROOT="/Users/nevillemehta/Downloads/CIA-SIE-PURE"
VENV_PATH="${PROJECT_ROOT}/venv"
BACKEND_PATH="${PROJECT_ROOT}/src"
FRONTEND_PATH="${PROJECT_ROOT}/frontend"
LOG_PATH="${PROJECT_ROOT}/logs"

# Ports
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Timeouts (seconds)
BACKEND_HEALTH_TIMEOUT=30
NGROK_START_TIMEOUT=15
PROCESS_STOP_TIMEOUT=10

# Health check
HEALTH_ENDPOINT="http://localhost:${BACKEND_PORT}/health"
HEALTH_CHECK_INTERVAL=2
HEALTH_CHECK_RETRIES=10
```

### Appendix C: Process Identification

| Service | Process Name | Identification Method |
|---------|--------------|----------------------|
| Backend | uvicorn | `pgrep -f "uvicorn.*cia_sie"` |
| ngrok | ngrok | `pgrep -f "ngrok http"` |
| Frontend | node/vite | `pgrep -f "vite.*5173"` |

---

## DOCUMENT APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | Claude (AI Assistant) | — | 12 Jan 2026 |
| Technical Review | Pending | | |
| Project Principal | Neville Mehta | | |

---

## REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 12 Jan 2026 | Claude | Initial specification |

---

**END OF SPECIFICATION**
