# CIA-SIE LAUNCHER SYSTEM ARCHITECTURE

**Document ID:** ARCH-LAUNCHER-001  
**Version:** 1.0.0  
**Date:** 12 January 2026  
**Status:** DRAFT → PENDING APPROVAL  
**Related Specification:** SPEC-LAUNCHER-001 v1.0.0  

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Architectural Principles](#2-architectural-principles)
3. [System Context](#3-system-context)
4. [Component Architecture](#4-component-architecture)
5. [Data Flow](#5-data-flow)
6. [Sequence Diagrams](#6-sequence-diagrams)
7. [State Management](#7-state-management)
8. [Error Handling Architecture](#8-error-handling-architecture)
9. [Logging Architecture](#9-logging-architecture)
10. [Configuration Architecture](#10-configuration-architecture)
11. [Interface Specifications](#11-interface-specifications)
12. [Deployment Architecture](#12-deployment-architecture)
13. [Cross-Reference Matrix](#13-cross-reference-matrix)

---

## 1. OVERVIEW

### 1.1 Purpose

This document defines the architectural design of the CIA-SIE Launcher System, providing a blueprint for implementation that satisfies all requirements specified in SPEC-LAUNCHER-001.

### 1.2 Scope

The architecture covers:
- File structure and organization
- Component relationships
- Process control mechanisms
- Error handling strategies
- Logging and monitoring

### 1.3 Architectural Approach

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    LAYERED ARCHITECTURE                                 │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    USER INTERFACE LAYER                           │ │
│  │          start-cia-sie.command  │  stop-cia-sie.command          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                  │                                      │
│                                  ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    ORCHESTRATION LAYER                            │ │
│  │              ignite.sh          │       shutdown.sh               │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                  │                                      │
│                                  ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    UTILITY LAYER                                  │ │
│  │        health-check.sh    │    utils.sh    │    config.sh        │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                  │                                      │
│                                  ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    SYSTEM LAYER                                   │ │
│  │      Python/venv    │    uvicorn    │    ngrok    │    node      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. ARCHITECTURAL PRINCIPLES

### 2.1 Core Principles

| Principle | Description | Application |
|-----------|-------------|-------------|
| **Separation of Concerns** | Each script has a single responsibility | User scripts delegate to orchestration |
| **Fail-Safe Design** | System fails gracefully with informative messages | Every command wrapped in error handling |
| **Idempotent Operations** | Running start twice doesn't break system | Check state before acting |
| **Configuration over Code** | Variables externalized | All paths/ports in config.sh |
| **Observable Operations** | User can see what's happening | Verbose output with timestamps |

### 2.2 Design Decisions

| Decision | Rationale | Reference |
|----------|-----------|-----------|
| DD-001: Shell Scripts | Native to macOS, no dependencies | NFR-005 Compatibility |
| DD-002: .command Extension | Enables Finder double-click | FR-001, FR-002 |
| DD-003: Layered Structure | Separation of user/logic/utility | Maintainability |
| DD-004: Background Processes | Long-running services need detachment | FR-001 |
| DD-005: PID Files | Track running processes for shutdown | FR-002 |

---

## 3. SYSTEM CONTEXT

### 3.1 Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                         SYSTEM CONTEXT DIAGRAM                                  │
│                                                                                 │
│                                                                                 │
│          ┌───────────┐                                                          │
│          │           │                                                          │
│          │   USER    │                                                          │
│          │           │                                                          │
│          └─────┬─────┘                                                          │
│                │                                                                │
│                │ Double-click                                                   │
│                ▼                                                                │
│     ┌──────────────────────────────────────────────────────────────────┐       │
│     │                                                                  │       │
│     │                   CIA-SIE LAUNCHER SYSTEM                       │       │
│     │                                                                  │       │
│     │    ┌─────────────────────┐      ┌─────────────────────┐        │       │
│     │    │                     │      │                     │        │       │
│     │    │  start-cia-sie      │      │  stop-cia-sie       │        │       │
│     │    │     .command        │      │    .command         │        │       │
│     │    │                     │      │                     │        │       │
│     │    └──────────┬──────────┘      └──────────┬──────────┘        │       │
│     │               │                            │                    │       │
│     └───────────────┼────────────────────────────┼────────────────────┘       │
│                     │                            │                             │
│                     │ Manages                    │ Manages                     │
│                     ▼                            ▼                             │
│     ┌──────────────────────────────────────────────────────────────────┐       │
│     │                                                                  │       │
│     │                      CIA-SIE PLATFORM                            │       │
│     │                                                                  │       │
│     │    ┌────────────┐    ┌────────────┐    ┌────────────┐           │       │
│     │    │            │    │            │    │            │           │       │
│     │    │  Backend   │◄───│   ngrok    │    │  Frontend  │           │       │
│     │    │ (FastAPI)  │    │  (Tunnel)  │    │  (React)   │           │       │
│     │    │            │    │            │    │            │           │       │
│     │    └────────────┘    └────────────┘    └────────────┘           │       │
│     │         ▲                                                        │       │
│     │         │                                                        │       │
│     │    ┌────┴───────┐    ┌────────────┐    ┌────────────┐           │       │
│     │    │            │    │            │    │            │           │       │
│     │    │  Database  │    │    Logs    │    │   Config   │           │       │
│     │    │ (SQLite)   │    │            │    │            │           │       │
│     │    │            │    │            │    │            │           │       │
│     │    └────────────┘    └────────────┘    └────────────┘           │       │
│     │                                                                  │       │
│     └──────────────────────────────────────────────────────────────────┘       │
│                                                                                 │
│                                                                                 │
│     ┌──────────────────────────────────────────────────────────────────┐       │
│     │                      EXTERNAL SYSTEMS                            │       │
│     │                                                                  │       │
│     │    ┌────────────┐    ┌────────────┐    ┌────────────┐           │       │
│     │    │            │    │            │    │            │           │       │
│     │    │ Anthropic  │    │   Kite/    │    │ TradingView│           │       │
│     │    │  (Claude)  │    │  Zerodha   │    │ (Webhooks) │           │       │
│     │    │            │    │            │    │            │           │       │
│     │    └────────────┘    └────────────┘    └────────────┘           │       │
│     │                                                                  │       │
│     └──────────────────────────────────────────────────────────────────┘       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Boundary Definition

| Boundary | Inside | Outside |
|----------|--------|---------|
| Launcher System | Script files, config, PID management | Backend, Frontend, Database code |
| User Interface | Terminal output | GUI, system tray |
| Process Control | Start/stop, health check | Business logic |

---

## 4. COMPONENT ARCHITECTURE

### 4.1 Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                        COMPONENT ARCHITECTURE                                   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        USER INTERFACE LAYER                             │   │
│  │                                                                         │   │
│  │    ┌─────────────────────────┐      ┌─────────────────────────┐        │   │
│  │    │                         │      │                         │        │   │
│  │    │  start-cia-sie.command │      │  stop-cia-sie.command  │        │   │
│  │    │                         │      │                         │        │   │
│  │    │  • Opens Terminal       │      │  • Opens Terminal       │        │   │
│  │    │  • Sources config       │      │  • Sources config       │        │   │
│  │    │  • Calls ignite.sh      │      │  • Calls shutdown.sh    │        │   │
│  │    │                         │      │                         │        │   │
│  │    └────────────┬────────────┘      └────────────┬────────────┘        │   │
│  │                 │                                │                      │   │
│  └─────────────────┼────────────────────────────────┼──────────────────────┘   │
│                    │                                │                           │
│                    ▼                                ▼                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                       ORCHESTRATION LAYER                               │   │
│  │                                                                         │   │
│  │    ┌─────────────────────────┐      ┌─────────────────────────┐        │   │
│  │    │                         │      │                         │        │   │
│  │    │      ignite.sh          │      │     shutdown.sh         │        │   │
│  │    │                         │      │                         │        │   │
│  │    │  • Activate venv        │      │  • Find PIDs            │        │   │
│  │    │  • Start Backend        │      │  • Stop Frontend        │        │   │
│  │    │  • Start ngrok          │      │  • Stop ngrok           │        │   │
│  │    │  • Start Frontend       │      │  • Stop Backend         │        │   │
│  │    │  • Open Browser         │      │  • Clean PIDs           │        │   │
│  │    │  • Report Status        │      │  • Report Status        │        │   │
│  │    │                         │      │                         │        │   │
│  │    └────────────┬────────────┘      └────────────┬────────────┘        │   │
│  │                 │                                │                      │   │
│  └─────────────────┼────────────────────────────────┼──────────────────────┘   │
│                    │                                │                           │
│                    ▼                                ▼                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                          UTILITY LAYER                                  │   │
│  │                                                                         │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │   │
│  │  │                  │  │                  │  │                  │      │   │
│  │  │  health-check.sh │  │     utils.sh     │  │    config.sh     │      │   │
│  │  │                  │  │                  │  │                  │      │   │
│  │  │  • curl health   │  │  • print_header  │  │  • PROJECT_ROOT  │      │   │
│  │  │  • retry logic   │  │  • print_step    │  │  • PORTS         │      │   │
│  │  │  • timeout       │  │  • print_success │  │  • TIMEOUTS      │      │   │
│  │  │  • return status │  │  • print_error   │  │  • PATHS         │      │   │
│  │  │                  │  │  • log_message   │  │                  │      │   │
│  │  │                  │  │  • get_pid       │  │                  │      │   │
│  │  │                  │  │  • save_pid      │  │                  │      │   │
│  │  │                  │  │                  │  │                  │      │   │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘      │   │
│  │                                                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Component Specifications

#### 4.2.1 start-cia-sie.command

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/start-cia-sie.command` |
| **Type** | Executable shell script |
| **Responsibility** | Entry point for system start |
| **Dependencies** | config.sh, ignite.sh |
| **Inputs** | None (user double-click) |
| **Outputs** | Terminal with progress, running services |

**Pseudo-code:**
```bash
#!/bin/zsh
cd "$(dirname "$0")"
source ./scripts/launcher/config.sh
source ./scripts/launcher/ignite.sh
main "$@"
```

#### 4.2.2 stop-cia-sie.command

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/stop-cia-sie.command` |
| **Type** | Executable shell script |
| **Responsibility** | Entry point for system stop |
| **Dependencies** | config.sh, shutdown.sh |
| **Inputs** | None (user double-click) |
| **Outputs** | Terminal with progress, stopped services |

#### 4.2.3 ignite.sh

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/scripts/launcher/ignite.sh` |
| **Type** | Shell script library |
| **Responsibility** | Orchestrate service startup |
| **Dependencies** | config.sh, utils.sh, health-check.sh |

**Functions:**
| Function | Purpose |
|----------|---------|
| `main()` | Entry point, orchestrates all steps |
| `activate_venv()` | Activate Python virtual environment |
| `start_backend()` | Launch uvicorn in background |
| `start_ngrok()` | Launch ngrok tunnel |
| `start_frontend()` | Launch React dev server (if exists) |
| `open_browser()` | Open default browser to app URL |
| `report_status()` | Display final status summary |

#### 4.2.4 shutdown.sh

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/scripts/launcher/shutdown.sh` |
| **Type** | Shell script library |
| **Responsibility** | Orchestrate service shutdown |
| **Dependencies** | config.sh, utils.sh |

**Functions:**
| Function | Purpose |
|----------|---------|
| `main()` | Entry point, orchestrates all steps |
| `stop_frontend()` | Stop React dev server |
| `stop_ngrok()` | Stop ngrok tunnel |
| `stop_backend()` | Stop uvicorn |
| `cleanup_pids()` | Remove PID files |
| `report_status()` | Display final status summary |

#### 4.2.5 health-check.sh

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/scripts/launcher/health-check.sh` |
| **Type** | Shell script library |
| **Responsibility** | Verify service health |
| **Dependencies** | config.sh |

**Functions:**
| Function | Purpose |
|----------|---------|
| `check_backend_health()` | Poll /health endpoint |
| `wait_for_backend()` | Retry with timeout |
| `check_port()` | Verify port is listening |
| `check_process()` | Verify process is running |

#### 4.2.6 utils.sh

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/scripts/launcher/utils.sh` |
| **Type** | Shell script library |
| **Responsibility** | Shared utility functions |
| **Dependencies** | config.sh |

**Functions:**
| Function | Purpose |
|----------|---------|
| `print_header()` | Display section header |
| `print_step()` | Display step progress |
| `print_success()` | Display success message |
| `print_warning()` | Display warning message |
| `print_error()` | Display error message |
| `log_message()` | Write to log file |
| `get_timestamp()` | Get formatted timestamp |
| `save_pid()` | Save PID to file |
| `get_pid()` | Read PID from file |
| `remove_pid()` | Delete PID file |
| `is_process_running()` | Check if PID is active |

#### 4.2.7 config.sh

| Attribute | Value |
|-----------|-------|
| **File Location** | `${PROJECT_ROOT}/scripts/launcher/config.sh` |
| **Type** | Shell script configuration |
| **Responsibility** | Centralized configuration |
| **Dependencies** | None |

---

## 5. DATA FLOW

### 5.1 Ignition Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                        IGNITION DATA FLOW                                       │
│                                                                                 │
│  ┌──────────────┐                                                               │
│  │              │                                                               │
│  │     USER     │                                                               │
│  │              │                                                               │
│  └──────┬───────┘                                                               │
│         │                                                                        │
│         │ Double-click                                                           │
│         ▼                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                     start-cia-sie.command                                │   │
│  │                                                                          │   │
│  │  1. cd to project directory                                              │   │
│  │  2. source config.sh  ──────────────────────────────────────┐            │   │
│  │  3. source ignite.sh                                        │            │   │
│  │  4. call main()                                              │            │   │
│  │                                                              ▼            │   │
│  └──────────────────────────────────────────────────────┬──────────────────┘   │
│                                                          │                      │
│         ┌────────────────────────────────────────────────┘                      │
│         │                                                                        │
│         ▼                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                            ignite.sh                                    │    │
│  │                                                                         │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 1: activate_venv()                                          │  │    │
│  │  │                                                                  │  │    │
│  │  │  Input:  VENV_PATH from config                                   │  │    │
│  │  │  Action: source ${VENV_PATH}/bin/activate                        │  │    │
│  │  │  Output: Python environment activated                            │  │    │
│  │  │  Log:    "Virtual environment activated"                         │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 2: start_backend()                                          │  │    │
│  │  │                                                                  │  │    │
│  │  │  Input:  BACKEND_PORT, BACKEND_PATH from config                  │  │    │
│  │  │  Action: uvicorn src.cia_sie.main:app --port 8000 &              │  │    │
│  │  │  Output: PID saved to pids/backend.pid                           │  │    │
│  │  │  Call:   wait_for_backend() from health-check.sh                 │  │    │
│  │  │  Log:    "Backend started on port 8000"                          │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 3: start_ngrok()                                            │  │    │
│  │  │                                                                  │  │    │
│  │  │  Input:  BACKEND_PORT from config                                │  │    │
│  │  │  Action: ngrok http ${BACKEND_PORT} --log=stdout &               │  │    │
│  │  │  Output: PID saved to pids/ngrok.pid                             │  │    │
│  │  │          Public URL extracted from API                           │  │    │
│  │  │  Log:    "ngrok tunnel established: https://xxx.ngrok.io"        │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 4: start_frontend()                                         │  │    │
│  │  │                                                                  │  │    │
│  │  │  Input:  FRONTEND_PATH from config                               │  │    │
│  │  │  Check:  Does FRONTEND_PATH exist?                               │  │    │
│  │  │  If No:  print_warning("Frontend not built")                     │  │    │
│  │  │  If Yes: npm run dev &                                           │  │    │
│  │  │  Output: PID saved to pids/frontend.pid (if started)             │  │    │
│  │  │  Log:    "Frontend started" or "Frontend skipped"                │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 5: open_browser()                                           │  │    │
│  │  │                                                                  │  │    │
│  │  │  Input:  BROWSER_URL from config                                 │  │    │
│  │  │  Action: open "${BROWSER_URL}"                                   │  │    │
│  │  │  Output: Default browser opens                                   │  │    │
│  │  │  Log:    "Browser opened to http://localhost:8000/docs"          │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 6: report_status()                                          │  │    │
│  │  │                                                                  │  │    │
│  │  │  Input:  Status of each service                                  │  │    │
│  │  │  Action: Display summary box                                     │  │    │
│  │  │  Output: Terminal shows final status                             │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                         │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Shutdown Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                        SHUTDOWN DATA FLOW                                       │
│                                                                                 │
│  ┌──────────────┐                                                               │
│  │              │                                                               │
│  │     USER     │                                                               │
│  │              │                                                               │
│  └──────┬───────┘                                                               │
│         │                                                                        │
│         │ Double-click                                                           │
│         ▼                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                      stop-cia-sie.command                                │   │
│  │                                                                          │   │
│  │  1. cd to project directory                                              │   │
│  │  2. source config.sh                                                     │   │
│  │  3. source shutdown.sh                                                   │   │
│  │  4. call main()                                                          │   │
│  │                                                                          │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│         │                                                                        │
│         ▼                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                           shutdown.sh                                   │    │
│  │                                                                         │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 1: stop_frontend()                                          │  │    │
│  │  │                                                                  │  │    │
│  │  │  Check:  Is frontend running? (read pids/frontend.pid)           │  │    │
│  │  │  If No:  print_step("Frontend not running")                      │  │    │
│  │  │  If Yes: kill -TERM ${FRONTEND_PID}                              │  │    │
│  │  │          Wait for graceful shutdown                              │  │    │
│  │  │          If still running: kill -KILL ${FRONTEND_PID}            │  │    │
│  │  │  Output: Remove pids/frontend.pid                                │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 2: stop_ngrok()                                             │  │    │
│  │  │                                                                  │  │    │
│  │  │  Check:  Is ngrok running? (read pids/ngrok.pid or pgrep)        │  │    │
│  │  │  If No:  print_step("ngrok not running")                         │  │    │
│  │  │  If Yes: kill -TERM ${NGROK_PID}                                 │  │    │
│  │  │  Output: Remove pids/ngrok.pid                                   │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 3: stop_backend()                                           │  │    │
│  │  │                                                                  │  │    │
│  │  │  Check:  Is backend running? (read pids/backend.pid or pgrep)    │  │    │
│  │  │  If No:  print_step("Backend not running")                       │  │    │
│  │  │  If Yes: kill -TERM ${BACKEND_PID}                               │  │    │
│  │  │          Wait for graceful shutdown                              │  │    │
│  │  │          If still running: kill -KILL ${BACKEND_PID}             │  │    │
│  │  │  Output: Remove pids/backend.pid                                 │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 4: cleanup_pids()                                           │  │    │
│  │  │                                                                  │  │    │
│  │  │  Action: Remove any remaining PID files                          │  │    │
│  │  │  Action: Verify no orphan processes                              │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                              │                                          │    │
│  │                              ▼                                          │    │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │    │
│  │  │ STEP 5: report_status()                                          │  │    │
│  │  │                                                                  │  │    │
│  │  │  Action: Display shutdown summary                                │  │    │
│  │  │  Output: "All services stopped"                                  │  │    │
│  │  │                                                                  │  │    │
│  │  └──────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                         │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. SEQUENCE DIAGRAMS

### 6.1 Ignition Sequence

See: `/documentation/02_ARCHITECTURE/diagrams/launcher_ignition_sequence.puml`

### 6.2 Shutdown Sequence

See: `/documentation/02_ARCHITECTURE/diagrams/launcher_shutdown_sequence.puml`

### 6.3 Health Check Sequence

See: `/documentation/02_ARCHITECTURE/diagrams/launcher_health_check.puml`

---

## 7. STATE MANAGEMENT

### 7.1 Service States

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                         SERVICE STATE DIAGRAM                                   │
│                                                                                 │
│                                                                                 │
│                              ┌───────────┐                                      │
│                              │           │                                      │
│                              │  UNKNOWN  │◄────────────────────────┐            │
│                              │           │                         │            │
│                              └─────┬─────┘                         │            │
│                                    │                               │            │
│                                    │ discover                      │            │
│                                    ▼                               │            │
│                              ┌───────────┐                         │            │
│                              │           │                         │            │
│                              │  STOPPED  │◄────────────────────────┤            │
│                              │           │                         │            │
│                              └─────┬─────┘                         │            │
│                                    │                               │            │
│                                    │ start                         │            │
│                                    ▼                               │            │
│                              ┌───────────┐                         │            │
│                              │           │                         │            │
│                              │ STARTING  │                         │            │
│                              │           │                         │            │
│                              └─────┬─────┘                         │            │
│                                    │                               │            │
│                      ┌─────────────┼─────────────┐                 │            │
│                      │             │             │                 │            │
│                      ▼             ▼             │                 │            │
│              ┌───────────┐  ┌───────────┐        │                 │            │
│              │           │  │           │        │                 │            │
│              │  HEALTHY  │  │ UNHEALTHY │        │                 │            │
│              │           │  │           │        │ timeout         │            │
│              └─────┬─────┘  └─────┬─────┘        │                 │            │
│                    │              │              │                 │            │
│                    │              │ retry        │                 │            │
│                    │              └──────────────┘                 │            │
│                    │                                               │            │
│                    │ stop                                          │ crash      │
│                    ▼                                               │            │
│              ┌───────────┐                                         │            │
│              │           │                                         │            │
│              │ STOPPING  │─────────────────────────────────────────┘            │
│              │           │                                                      │
│              └───────────┘                                                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 PID File Management

| Service | PID File | Created | Deleted |
|---------|----------|---------|---------|
| Backend | `pids/backend.pid` | On start | On stop |
| ngrok | `pids/ngrok.pid` | On start | On stop |
| Frontend | `pids/frontend.pid` | On start | On stop |

### 7.3 State Recovery

If the launcher detects orphan processes (PID file exists but process not running), it will:

1. Log the inconsistency
2. Clean up the PID file
3. Attempt to find the process by name
4. Kill if found, proceed if not

---

## 8. ERROR HANDLING ARCHITECTURE

### 8.1 Error Categories

| Category | Examples | Handling Strategy |
|----------|----------|-------------------|
| **Configuration** | Missing config, invalid paths | Abort with clear message |
| **Prerequisite** | venv missing, port in use | Abort with actionable steps |
| **Runtime** | Process crash, timeout | Log, retry, or fail gracefully |
| **Resource** | Disk full, permission denied | Abort with system guidance |

### 8.2 Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                      ERROR HANDLING DECISION TREE                               │
│                                                                                 │
│                           ┌───────────────┐                                     │
│                           │    Error      │                                     │
│                           │   Occurred    │                                     │
│                           └───────┬───────┘                                     │
│                                   │                                             │
│                                   ▼                                             │
│                    ┌──────────────────────────────┐                             │
│                    │    Is it a critical error?   │                             │
│                    │    (Backend won't start)     │                             │
│                    └──────────────┬───────────────┘                             │
│                                   │                                             │
│                    ┌──────────────┴──────────────┐                              │
│                    │                             │                              │
│                YES ▼                             ▼ NO                           │
│            ┌───────────────┐            ┌───────────────┐                       │
│            │ Log error     │            │ Is it         │                       │
│            │ Display error │            │ recoverable?  │                       │
│            │ Suggest fix   │            │               │                       │
│            │ ABORT         │            └───────┬───────┘                       │
│            └───────────────┘                    │                               │
│                                  ┌──────────────┴──────────────┐                │
│                                  │                             │                │
│                              YES ▼                             ▼ NO             │
│                          ┌───────────────┐            ┌───────────────┐         │
│                          │ Retry up to   │            │ Log warning   │         │
│                          │ MAX_RETRIES   │            │ Display warn  │         │
│                          │               │            │ CONTINUE      │         │
│                          └───────┬───────┘            └───────────────┘         │
│                                  │                                              │
│                       ┌──────────┴──────────┐                                   │
│                       │                     │                                   │
│                SUCCESS▼                     ▼ EXHAUST                           │
│                ┌───────────────┐     ┌───────────────┐                          │
│                │ Log success   │     │ Log failure   │                          │
│                │ CONTINUE      │     │ ABORT or WARN │                          │
│                └───────────────┘     └───────────────┘                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 8.3 Error Message Format

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ❌ ERROR: [ERROR_CODE] - [SHORT_DESCRIPTION]                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

WHAT HAPPENED:
  [Detailed explanation in plain English]

DETAILS:
  • Component: [Service name]
  • Action: [What was being attempted]
  • Error: [Technical error if available]

SUGGESTED ACTIONS:
  1. [First thing to try]
  2. [Second thing to try]
  3. [Escalation path]

LOG LOCATION:
  /logs/launcher.log

TIMESTAMP: [ISO 8601 timestamp]
```

---

## 9. LOGGING ARCHITECTURE

### 9.1 Log File Structure

| Log File | Purpose | Rotation |
|----------|---------|----------|
| `/logs/launcher.log` | All launcher operations | Date-based |
| `/logs/backend.log` | Uvicorn/backend output | Size-based |

### 9.2 Log Entry Format

```
[TIMESTAMP] [LEVEL] [COMPONENT] [MESSAGE]

Examples:
[2026-01-12T10:30:15+0530] [INFO] [IGNITE] Starting system ignition
[2026-01-12T10:30:16+0530] [INFO] [VENV] Virtual environment activated
[2026-01-12T10:30:17+0530] [INFO] [BACKEND] Starting uvicorn on port 8000
[2026-01-12T10:30:22+0530] [INFO] [HEALTH] Backend healthy after 5 seconds
[2026-01-12T10:30:23+0530] [WARN] [FRONTEND] Frontend directory not found
[2026-01-12T10:30:25+0530] [INFO] [IGNITE] System ignition complete
```

### 9.3 Log Levels

| Level | Usage | Terminal |
|-------|-------|----------|
| DEBUG | Detailed troubleshooting | Not shown |
| INFO | Normal operations | Shown |
| WARN | Non-critical issues | Shown (yellow) |
| ERROR | Critical failures | Shown (red) |

---

## 10. CONFIGURATION ARCHITECTURE

### 10.1 Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                    CONFIGURATION HIERARCHY                                      │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                         │   │
│  │  LEVEL 1: DEFAULTS (config.sh)                                         │   │
│  │  ════════════════════════════════                                       │   │
│  │                                                                         │   │
│  │  • Hardcoded sensible defaults                                         │   │
│  │  • Used when no override exists                                        │   │
│  │                                                                         │   │
│  │  Example: BACKEND_PORT=8000                                            │   │
│  │                                                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                              │                                                  │
│                              │ overridden by                                    │
│                              ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                         │   │
│  │  LEVEL 2: ENVIRONMENT VARIABLES                                        │   │
│  │  ══════════════════════════════════                                     │   │
│  │                                                                         │   │
│  │  • Set in shell or .env file                                           │   │
│  │  • Takes precedence over defaults                                      │   │
│  │                                                                         │   │
│  │  Example: export CIA_SIE_BACKEND_PORT=9000                             │   │
│  │                                                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                              │                                                  │
│                              │ overridden by                                    │
│                              ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                         │   │
│  │  LEVEL 3: COMMAND-LINE ARGUMENTS                                       │   │
│  │  ═══════════════════════════════════                                    │   │
│  │                                                                         │   │
│  │  • Passed directly to script                                           │   │
│  │  • Highest precedence                                                  │   │
│  │                                                                         │   │
│  │  Example: ./start-cia-sie.command --port=9000                          │   │
│  │                                                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 Configuration Variables

| Variable | Default | Environment Override | Description |
|----------|---------|---------------------|-------------|
| `PROJECT_ROOT` | Script directory | `CIA_SIE_ROOT` | Project root path |
| `BACKEND_PORT` | 8000 | `CIA_SIE_BACKEND_PORT` | Backend server port |
| `FRONTEND_PORT` | 5173 | `CIA_SIE_FRONTEND_PORT` | Frontend dev port |
| `HEALTH_TIMEOUT` | 30 | `CIA_SIE_HEALTH_TIMEOUT` | Health check timeout |
| `OPEN_BROWSER` | true | `CIA_SIE_OPEN_BROWSER` | Auto-open browser |

---

## 11. INTERFACE SPECIFICATIONS

### 11.1 Script Interfaces

#### start-cia-sie.command

**Input Interface:**
- None (designed for double-click)

**Output Interface:**
- Terminal output (stdout)
- Exit code: 0 = success, 1 = failure

**Side Effects:**
- Starts processes (backend, ngrok, frontend)
- Creates PID files
- Creates log entries
- Opens browser

#### stop-cia-sie.command

**Input Interface:**
- None (designed for double-click)

**Output Interface:**
- Terminal output (stdout)
- Exit code: 0 = success, 1 = failure

**Side Effects:**
- Stops processes
- Removes PID files
- Creates log entries

### 11.2 Health Check Interface

**Endpoint:** `GET /health`

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-12T10:30:22Z"
}
```

**HTTP Status Codes:**
- 200: Healthy
- 503: Unhealthy

---

## 12. DEPLOYMENT ARCHITECTURE

### 12.1 File Deployment

```
CIA-SIE-PURE/
│
├── start-cia-sie.command          # chmod 755
├── stop-cia-sie.command           # chmod 755
│
├── scripts/
│   └── launcher/
│       ├── config.sh              # chmod 644
│       ├── ignite.sh              # chmod 755
│       ├── shutdown.sh            # chmod 755
│       ├── health-check.sh        # chmod 755
│       └── utils.sh               # chmod 644
│
├── pids/                          # Created at runtime
│   ├── backend.pid
│   ├── ngrok.pid
│   └── frontend.pid
│
└── logs/
    └── launcher.log               # Created at runtime
```

### 12.2 Permission Requirements

| File/Directory | Permission | Reason |
|----------------|------------|--------|
| `*.command` | 755 (rwxr-xr-x) | Must be executable |
| `ignite.sh`, `shutdown.sh`, `health-check.sh` | 755 | Must be executable |
| `config.sh`, `utils.sh` | 644 (rw-r--r--) | Sourced, not executed |
| `pids/` | 755 | Directory for PID files |
| `logs/` | 755 | Directory for log files |

---

## 13. CROSS-REFERENCE MATRIX

### 13.1 Requirements to Components

| Requirement | Component(s) |
|-------------|--------------|
| FR-001 (Start All) | start-cia-sie.command, ignite.sh |
| FR-002 (Stop All) | stop-cia-sie.command, shutdown.sh |
| FR-003 (Health) | health-check.sh |
| FR-004 (Visual) | utils.sh (print functions) |
| FR-005 (Errors) | utils.sh (error handling) |
| FR-006 (Graceful) | ignite.sh (conditional logic) |
| FR-007 (Logging) | utils.sh (log_message) |

### 13.2 Components to Files

| Component | File |
|-----------|------|
| User Interface (Start) | `start-cia-sie.command` |
| User Interface (Stop) | `stop-cia-sie.command` |
| Orchestration (Start) | `scripts/launcher/ignite.sh` |
| Orchestration (Stop) | `scripts/launcher/shutdown.sh` |
| Health Verification | `scripts/launcher/health-check.sh` |
| Utilities | `scripts/launcher/utils.sh` |
| Configuration | `scripts/launcher/config.sh` |

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
| 1.0.0 | 12 Jan 2026 | Claude | Initial architecture |

---

**END OF ARCHITECTURE DOCUMENT**
