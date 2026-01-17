# CIA-SIE LAUNCHER SYSTEM - DETAILED DESIGN

**Document ID:** DESIGN-LAUNCHER-001  
**Version:** 1.0.0  
**Date:** 12 January 2026  
**Status:** DRAFT → PENDING APPROVAL  
**Related Specification:** SPEC-LAUNCHER-001 v1.0.0  
**Related Architecture:** ARCH-LAUNCHER-001 v1.0.0  

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [File Structure](#2-file-structure)
3. [Script Detailed Design](#3-script-detailed-design)
4. [Function Specifications](#4-function-specifications)
5. [Error Handling Design](#5-error-handling-design)
6. [Logging Design](#6-logging-design)
7. [Visual Output Design](#7-visual-output-design)
8. [Configuration Design](#8-configuration-design)
9. [Process Management Design](#9-process-management-design)
10. [Testing Interface Design](#10-testing-interface-design)
11. [Deployment Checklist](#11-deployment-checklist)

---

## 1. OVERVIEW

### 1.1 Purpose

This document provides the detailed design specifications required to implement the CIA-SIE Launcher System. It serves as the definitive reference for developers implementing the scripts.

### 1.2 Design Philosophy

| Principle | Application |
|-----------|-------------|
| **Explicit over Implicit** | Every action is logged and reported |
| **Defensive Programming** | Check before act, verify after |
| **User-First Messaging** | Technical details in logs, plain English on screen |
| **Atomic Operations** | Each step completes or rolls back cleanly |

---

## 2. FILE STRUCTURE

### 2.1 Complete File Tree

```
CIA-SIE-PURE/
│
├── start-cia-sie.command              # Entry point: START
│   └── Size: ~50 lines
│   └── Permissions: 755 (rwxr-xr-x)
│
├── stop-cia-sie.command               # Entry point: STOP
│   └── Size: ~40 lines
│   └── Permissions: 755 (rwxr-xr-x)
│
├── scripts/
│   └── launcher/
│       ├── config.sh                  # Configuration variables
│       │   └── Size: ~80 lines
│       │   └── Permissions: 644 (rw-r--r--)
│       │
│       ├── ignite.sh                  # Start orchestration
│       │   └── Size: ~250 lines
│       │   └── Permissions: 755 (rwxr-xr-x)
│       │
│       ├── shutdown.sh                # Stop orchestration
│       │   └── Size: ~180 lines
│       │   └── Permissions: 755 (rwxr-xr-x)
│       │
│       ├── health-check.sh            # Health verification
│       │   └── Size: ~100 lines
│       │   └── Permissions: 755 (rwxr-xr-x)
│       │
│       └── utils.sh                   # Shared utilities
│           └── Size: ~200 lines
│           └── Permissions: 644 (rw-r--r--)
│
├── pids/                              # Runtime PID storage
│   ├── .gitkeep                       # Preserve empty directory
│   ├── backend.pid                    # Created at runtime
│   ├── ngrok.pid                      # Created at runtime
│   └── frontend.pid                   # Created at runtime
│
└── logs/
    └── launcher.log                   # Launcher operations log
```

### 2.2 File Dependencies

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  start-cia-sie.command                                                     │
│      │                                                                     │
│      ├── sources ─► config.sh                                              │
│      ├── sources ─► utils.sh ─────────► sources ─► config.sh               │
│      ├── sources ─► ignite.sh ────────► sources ─► utils.sh                │
│      │                                    │                                │
│      │                                    └────► sources ─► health-check.sh │
│      │                                                                     │
│  stop-cia-sie.command                                                      │
│      │                                                                     │
│      ├── sources ─► config.sh                                              │
│      ├── sources ─► utils.sh ─────────► sources ─► config.sh               │
│      └── sources ─► shutdown.sh ──────► sources ─► utils.sh                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. SCRIPT DETAILED DESIGN

### 3.1 start-cia-sie.command

#### 3.1.1 Purpose
Entry point for system startup. Designed for Finder double-click execution.

#### 3.1.2 Pseudo-code
```bash
#!/bin/zsh
#===============================================================================
# CIA-SIE System Start
# Double-click this file to start the CIA-SIE platform
#===============================================================================

# Change to script directory (project root)
cd "$(dirname "$0")" || exit 1

# Source dependencies
source ./scripts/launcher/config.sh
source ./scripts/launcher/utils.sh
source ./scripts/launcher/ignite.sh

# Run main ignition sequence
main "$@"

# Keep terminal open on error
if [[ $? -ne 0 ]]; then
    echo ""
    echo "Press Enter to close this window..."
    read -r
fi
```

#### 3.1.3 Behavior
| Scenario | Behavior |
|----------|----------|
| Normal execution | Runs ignite.sh main(), terminal stays open |
| Error occurs | Shows error, prompts to press Enter |
| User closes terminal | Processes continue in background |

---

### 3.2 stop-cia-sie.command

#### 3.2.1 Purpose
Entry point for system shutdown. Designed for Finder double-click execution.

#### 3.2.2 Pseudo-code
```bash
#!/bin/zsh
#===============================================================================
# CIA-SIE System Stop
# Double-click this file to stop the CIA-SIE platform
#===============================================================================

# Change to script directory (project root)
cd "$(dirname "$0")" || exit 1

# Source dependencies
source ./scripts/launcher/config.sh
source ./scripts/launcher/utils.sh
source ./scripts/launcher/shutdown.sh

# Run main shutdown sequence
main "$@"

# Always prompt before closing
echo ""
echo "Press Enter to close this window..."
read -r
```

---

### 3.3 config.sh

#### 3.3.1 Purpose
Centralized configuration with sensible defaults and environment overrides.

#### 3.3.2 Variables

```bash
#!/bin/zsh
#===============================================================================
# CIA-SIE Launcher Configuration
# All configurable values in one place
#===============================================================================

#-------------------------------------------------------------------------------
# PATH CONFIGURATION
#-------------------------------------------------------------------------------

# Project root (auto-detected or override with CIA_SIE_ROOT)
export PROJECT_ROOT="${CIA_SIE_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

# Derived paths
export VENV_PATH="${PROJECT_ROOT}/venv"
export BACKEND_PATH="${PROJECT_ROOT}/src"
export FRONTEND_PATH="${PROJECT_ROOT}/frontend"
export LOGS_PATH="${PROJECT_ROOT}/logs"
export PIDS_PATH="${PROJECT_ROOT}/pids"
export SCRIPTS_PATH="${PROJECT_ROOT}/scripts/launcher"

#-------------------------------------------------------------------------------
# PORT CONFIGURATION
#-------------------------------------------------------------------------------

export BACKEND_PORT="${CIA_SIE_BACKEND_PORT:-8000}"
export FRONTEND_PORT="${CIA_SIE_FRONTEND_PORT:-5173}"
export NGROK_API_PORT="${CIA_SIE_NGROK_API_PORT:-4040}"

#-------------------------------------------------------------------------------
# TIMEOUT CONFIGURATION (in seconds)
#-------------------------------------------------------------------------------

export HEALTH_CHECK_TIMEOUT="${CIA_SIE_HEALTH_TIMEOUT:-30}"
export HEALTH_CHECK_INTERVAL="${CIA_SIE_HEALTH_INTERVAL:-2}"
export HEALTH_CHECK_RETRIES="${CIA_SIE_HEALTH_RETRIES:-15}"
export PROCESS_STOP_TIMEOUT="${CIA_SIE_STOP_TIMEOUT:-10}"
export NGROK_START_TIMEOUT="${CIA_SIE_NGROK_TIMEOUT:-15}"

#-------------------------------------------------------------------------------
# URL CONFIGURATION
#-------------------------------------------------------------------------------

export BACKEND_URL="http://localhost:${BACKEND_PORT}"
export FRONTEND_URL="http://localhost:${FRONTEND_PORT}"
export HEALTH_ENDPOINT="${BACKEND_URL}/health"
export DOCS_ENDPOINT="${BACKEND_URL}/docs"
export NGROK_API_URL="http://localhost:${NGROK_API_PORT}/api/tunnels"

#-------------------------------------------------------------------------------
# BEHAVIOR CONFIGURATION
#-------------------------------------------------------------------------------

export OPEN_BROWSER="${CIA_SIE_OPEN_BROWSER:-true}"
export START_NGROK="${CIA_SIE_START_NGROK:-true}"
export START_FRONTEND="${CIA_SIE_START_FRONTEND:-true}"
export VERBOSE="${CIA_SIE_VERBOSE:-false}"

#-------------------------------------------------------------------------------
# PROCESS IDENTIFICATION PATTERNS
#-------------------------------------------------------------------------------

export BACKEND_PATTERN="uvicorn.*cia_sie"
export NGROK_PATTERN="ngrok http"
export FRONTEND_PATTERN="vite.*${FRONTEND_PORT}"

#-------------------------------------------------------------------------------
# LOG CONFIGURATION
#-------------------------------------------------------------------------------

export LOG_FILE="${LOGS_PATH}/launcher.log"
export LOG_DATE_FORMAT="+%Y-%m-%dT%H:%M:%S%z"

#-------------------------------------------------------------------------------
# DISPLAY CONFIGURATION
#-------------------------------------------------------------------------------

# Colors (ANSI escape codes)
export COLOR_RESET="\033[0m"
export COLOR_RED="\033[0;31m"
export COLOR_GREEN="\033[0;32m"
export COLOR_YELLOW="\033[0;33m"
export COLOR_BLUE="\033[0;34m"
export COLOR_MAGENTA="\033[0;35m"
export COLOR_CYAN="\033[0;36m"
export COLOR_WHITE="\033[0;37m"
export COLOR_BOLD="\033[1m"

# Symbols
export SYMBOL_SUCCESS="✓"
export SYMBOL_FAILURE="✗"
export SYMBOL_WARNING="⚠"
export SYMBOL_INFO="ℹ"
export SYMBOL_PENDING="○"
export SYMBOL_RUNNING="●"
```

---

### 3.4 utils.sh

#### 3.4.1 Purpose
Shared utility functions for display, logging, and process management.

#### 3.4.2 Functions

| Function | Purpose | Parameters |
|----------|---------|------------|
| `print_header` | Display major section header | message |
| `print_step` | Display step with spinner | step_number, total_steps, message |
| `print_success` | Display success message | message |
| `print_warning` | Display warning message | message |
| `print_error` | Display error message | message |
| `print_info` | Display info message | message |
| `print_status_box` | Display final status summary | (reads global state) |
| `log_message` | Write to log file | level, component, message |
| `get_timestamp` | Get formatted timestamp | (none) |
| `save_pid` | Save PID to file | service_name, pid |
| `get_pid` | Read PID from file | service_name |
| `remove_pid` | Delete PID file | service_name |
| `is_process_running` | Check if PID is alive | pid |
| `find_process_by_pattern` | Find PID by grep pattern | pattern |
| `ensure_directory` | Create directory if needed | path |
| `check_port_available` | Check if port is free | port |
| `wait_for_port` | Wait until port is listening | port, timeout |

---

### 3.5 ignite.sh

#### 3.5.1 Purpose
Orchestrate the complete system startup sequence.

#### 3.5.2 Main Function Flow

```bash
main() {
    local exit_code=0
    
    # Initialize
    print_header "CIA-SIE SYSTEM IGNITION"
    log_message "INFO" "IGNITE" "Starting system ignition"
    ensure_directory "${PIDS_PATH}"
    ensure_directory "${LOGS_PATH}"
    
    # Step 1: Verify prerequisites
    print_step 1 6 "Verifying prerequisites..."
    if ! verify_prerequisites; then
        print_error "Prerequisites check failed"
        return 1
    fi
    print_success "Prerequisites verified"
    
    # Step 2: Activate virtual environment
    print_step 2 6 "Activating Python environment..."
    if ! activate_venv; then
        print_error "Failed to activate virtual environment"
        return 1
    fi
    print_success "Python environment activated"
    
    # Step 3: Start backend
    print_step 3 6 "Starting Backend server..."
    if ! start_backend; then
        print_error "Failed to start backend"
        return 1
    fi
    print_success "Backend running on port ${BACKEND_PORT}"
    
    # Step 4: Start ngrok (if enabled)
    if [[ "${START_NGROK}" == "true" ]]; then
        print_step 4 6 "Starting webhook tunnel..."
        if ! start_ngrok; then
            print_warning "Failed to start ngrok (non-critical)"
        else
            print_success "Tunnel established: ${NGROK_PUBLIC_URL}"
        fi
    else
        print_step 4 6 "Webhook tunnel..."
        print_info "Skipped (disabled in config)"
    fi
    
    # Step 5: Start frontend (if exists)
    print_step 5 6 "Starting Frontend server..."
    if [[ -d "${FRONTEND_PATH}" ]]; then
        if ! start_frontend; then
            print_warning "Failed to start frontend (non-critical)"
        else
            print_success "Frontend running on port ${FRONTEND_PORT}"
        fi
    else
        print_warning "Frontend not built yet"
        print_info "Backend and API are fully operational"
    fi
    
    # Step 6: Open browser (if enabled)
    if [[ "${OPEN_BROWSER}" == "true" ]]; then
        print_step 6 6 "Opening browser..."
        open_browser
        print_success "Browser opened"
    fi
    
    # Final status
    print_status_box
    
    log_message "INFO" "IGNITE" "System ignition complete"
    
    # Keep script running to maintain context
    echo ""
    echo "Press Ctrl+C to stop all services, or run stop-cia-sie.command"
    
    # Wait indefinitely (allows Ctrl+C to trigger cleanup)
    trap 'shutdown_all; exit 0' INT TERM
    while true; do
        sleep 60
    done
}
```

#### 3.5.3 Service Start Functions

##### activate_venv()
```bash
activate_venv() {
    local venv_activate="${VENV_PATH}/bin/activate"
    
    if [[ ! -f "${venv_activate}" ]]; then
        log_message "ERROR" "VENV" "Virtual environment not found: ${VENV_PATH}"
        return 1
    fi
    
    # shellcheck source=/dev/null
    source "${venv_activate}"
    
    log_message "INFO" "VENV" "Virtual environment activated"
    return 0
}
```

##### start_backend()
```bash
start_backend() {
    local pid
    
    # Check if already running
    if pid=$(find_process_by_pattern "${BACKEND_PATTERN}"); then
        log_message "WARN" "BACKEND" "Backend already running (PID: ${pid})"
        save_pid "backend" "${pid}"
        return 0
    fi
    
    # Check port availability
    if ! check_port_available "${BACKEND_PORT}"; then
        log_message "ERROR" "BACKEND" "Port ${BACKEND_PORT} is already in use"
        return 1
    fi
    
    # Start uvicorn in background
    cd "${PROJECT_ROOT}" || return 1
    
    nohup uvicorn src.cia_sie.main:app \
        --host 0.0.0.0 \
        --port "${BACKEND_PORT}" \
        --log-level info \
        >> "${LOGS_PATH}/backend.log" 2>&1 &
    
    pid=$!
    save_pid "backend" "${pid}"
    
    log_message "INFO" "BACKEND" "Started uvicorn (PID: ${pid})"
    
    # Wait for health
    if ! wait_for_backend; then
        log_message "ERROR" "BACKEND" "Health check failed"
        kill "${pid}" 2>/dev/null
        remove_pid "backend"
        return 1
    fi
    
    log_message "INFO" "BACKEND" "Backend healthy"
    return 0
}
```

##### start_ngrok()
```bash
start_ngrok() {
    local pid
    local public_url
    local attempt=0
    local max_attempts=10
    
    # Check if already running
    if pid=$(find_process_by_pattern "${NGROK_PATTERN}"); then
        log_message "WARN" "NGROK" "ngrok already running (PID: ${pid})"
        save_pid "ngrok" "${pid}"
        # Get existing URL
        NGROK_PUBLIC_URL=$(get_ngrok_url)
        return 0
    fi
    
    # Start ngrok in background
    nohup ngrok http "${BACKEND_PORT}" \
        --log=stdout \
        >> "${LOGS_PATH}/ngrok.log" 2>&1 &
    
    pid=$!
    save_pid "ngrok" "${pid}"
    
    log_message "INFO" "NGROK" "Started ngrok (PID: ${pid})"
    
    # Wait for API to be ready and get URL
    while [[ ${attempt} -lt ${max_attempts} ]]; do
        sleep 2
        public_url=$(get_ngrok_url)
        if [[ -n "${public_url}" ]]; then
            NGROK_PUBLIC_URL="${public_url}"
            log_message "INFO" "NGROK" "Tunnel established: ${public_url}"
            return 0
        fi
        ((attempt++))
    done
    
    log_message "ERROR" "NGROK" "Failed to get tunnel URL"
    return 1
}

get_ngrok_url() {
    curl -s "${NGROK_API_URL}" 2>/dev/null \
        | grep -o '"public_url":"[^"]*"' \
        | head -1 \
        | cut -d'"' -f4
}
```

##### start_frontend()
```bash
start_frontend() {
    local pid
    
    # Check if directory exists
    if [[ ! -d "${FRONTEND_PATH}" ]]; then
        log_message "WARN" "FRONTEND" "Frontend directory not found"
        return 1
    fi
    
    # Check if package.json exists
    if [[ ! -f "${FRONTEND_PATH}/package.json" ]]; then
        log_message "WARN" "FRONTEND" "No package.json found"
        return 1
    fi
    
    # Check if node_modules exists
    if [[ ! -d "${FRONTEND_PATH}/node_modules" ]]; then
        log_message "WARN" "FRONTEND" "node_modules not found, run npm install"
        return 1
    fi
    
    # Check if already running
    if pid=$(find_process_by_pattern "${FRONTEND_PATTERN}"); then
        log_message "WARN" "FRONTEND" "Frontend already running (PID: ${pid})"
        save_pid "frontend" "${pid}"
        return 0
    fi
    
    # Start dev server
    cd "${FRONTEND_PATH}" || return 1
    
    nohup npm run dev \
        >> "${LOGS_PATH}/frontend.log" 2>&1 &
    
    pid=$!
    save_pid "frontend" "${pid}"
    
    log_message "INFO" "FRONTEND" "Started frontend (PID: ${pid})"
    
    # Wait for port
    if ! wait_for_port "${FRONTEND_PORT}" 30; then
        log_message "ERROR" "FRONTEND" "Frontend failed to start"
        kill "${pid}" 2>/dev/null
        remove_pid "frontend"
        return 1
    fi
    
    return 0
}
```

---

### 3.6 shutdown.sh

#### 3.6.1 Main Function Flow

```bash
main() {
    print_header "CIA-SIE SYSTEM SHUTDOWN"
    log_message "INFO" "SHUTDOWN" "Starting system shutdown"
    
    # Step 1: Stop frontend
    print_step 1 4 "Stopping Frontend..."
    stop_service "frontend" "${FRONTEND_PATTERN}"
    
    # Step 2: Stop ngrok
    print_step 2 4 "Stopping Tunnel..."
    stop_service "ngrok" "${NGROK_PATTERN}"
    
    # Step 3: Stop backend
    print_step 3 4 "Stopping Backend..."
    stop_service "backend" "${BACKEND_PATTERN}"
    
    # Step 4: Cleanup
    print_step 4 4 "Cleaning up..."
    cleanup_all
    print_success "Cleanup complete"
    
    # Final status
    print_shutdown_complete
    
    log_message "INFO" "SHUTDOWN" "System shutdown complete"
    return 0
}
```

#### 3.6.2 Service Stop Function

```bash
stop_service() {
    local name="$1"
    local pattern="$2"
    local pid
    local attempts=0
    local max_attempts=$((PROCESS_STOP_TIMEOUT))
    
    # Get PID from file or find by pattern
    pid=$(get_pid "${name}")
    if [[ -z "${pid}" ]] || ! is_process_running "${pid}"; then
        pid=$(find_process_by_pattern "${pattern}")
    fi
    
    if [[ -z "${pid}" ]]; then
        print_info "Not running"
        remove_pid "${name}"
        return 0
    fi
    
    log_message "INFO" "SHUTDOWN" "Stopping ${name} (PID: ${pid})"
    
    # Send SIGTERM for graceful shutdown
    kill -TERM "${pid}" 2>/dev/null
    
    # Wait for process to stop
    while [[ ${attempts} -lt ${max_attempts} ]]; do
        if ! is_process_running "${pid}"; then
            print_success "Stopped"
            remove_pid "${name}"
            log_message "INFO" "SHUTDOWN" "${name} stopped gracefully"
            return 0
        fi
        sleep 1
        ((attempts++))
    done
    
    # Force kill if still running
    log_message "WARN" "SHUTDOWN" "${name} did not stop gracefully, sending SIGKILL"
    kill -KILL "${pid}" 2>/dev/null
    sleep 1
    
    if ! is_process_running "${pid}"; then
        print_success "Stopped (forced)"
        remove_pid "${name}"
        return 0
    fi
    
    print_error "Failed to stop"
    log_message "ERROR" "SHUTDOWN" "Failed to stop ${name}"
    return 1
}
```

---

### 3.7 health-check.sh

#### 3.7.1 Wait for Backend Function

```bash
wait_for_backend() {
    local attempt=0
    local max_attempts="${HEALTH_CHECK_RETRIES}"
    local interval="${HEALTH_CHECK_INTERVAL}"
    local start_time
    local elapsed
    
    start_time=$(date +%s)
    
    while [[ ${attempt} -lt ${max_attempts} ]]; do
        if check_backend_health; then
            elapsed=$(($(date +%s) - start_time))
            log_message "INFO" "HEALTH" "Backend healthy after ${elapsed}s"
            return 0
        fi
        
        ((attempt++))
        log_message "DEBUG" "HEALTH" "Attempt ${attempt}/${max_attempts} failed"
        sleep "${interval}"
    done
    
    elapsed=$(($(date +%s) - start_time))
    log_message "ERROR" "HEALTH" "Backend unhealthy after ${elapsed}s"
    return 1
}

check_backend_health() {
    local response
    local status_code
    
    # Get HTTP status code
    status_code=$(curl -s -o /dev/null -w "%{http_code}" \
        --connect-timeout 5 \
        "${HEALTH_ENDPOINT}" 2>/dev/null)
    
    if [[ "${status_code}" == "200" ]]; then
        return 0
    fi
    
    return 1
}
```

---

## 4. FUNCTION SPECIFICATIONS

### 4.1 utils.sh Function Details

#### 4.1.1 print_header

```bash
#-------------------------------------------------------------------------------
# print_header - Display major section header
#
# Arguments:
#   $1 - Header message
#
# Output:
#   Formatted header to stdout
#
# Example:
#   print_header "CIA-SIE SYSTEM IGNITION"
#-------------------------------------------------------------------------------
print_header() {
    local message="$1"
    local width=79
    local padding
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    printf "║%*s%s%*s║\n" $(((width-${#message})/2)) "" "$message" $(((width-${#message}+1)/2)) ""
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    log_message "INFO" "DISPLAY" "Header: ${message}"
}
```

#### 4.1.2 print_step

```bash
#-------------------------------------------------------------------------------
# print_step - Display step progress
#
# Arguments:
#   $1 - Step number
#   $2 - Total steps
#   $3 - Step message
#
# Output:
#   Formatted step indicator to stdout
#
# Example:
#   print_step 1 5 "Activating virtual environment..."
#-------------------------------------------------------------------------------
print_step() {
    local step="$1"
    local total="$2"
    local message="$3"
    
    echo ""
    echo -e "${COLOR_CYAN}STEP ${step}/${total}:${COLOR_RESET} ${message}"
}
```

#### 4.1.3 print_success / print_warning / print_error

```bash
print_success() {
    local message="$1"
    echo -e "         └── ${COLOR_GREEN}${SYMBOL_SUCCESS} ${message}${COLOR_RESET}"
    log_message "INFO" "STATUS" "${message}"
}

print_warning() {
    local message="$1"
    echo -e "         └── ${COLOR_YELLOW}${SYMBOL_WARNING} ${message}${COLOR_RESET}"
    log_message "WARN" "STATUS" "${message}"
}

print_error() {
    local message="$1"
    echo -e "         └── ${COLOR_RED}${SYMBOL_FAILURE} ${message}${COLOR_RESET}"
    log_message "ERROR" "STATUS" "${message}"
}

print_info() {
    local message="$1"
    echo -e "             ${COLOR_BLUE}${SYMBOL_INFO} ${message}${COLOR_RESET}"
}
```

#### 4.1.4 log_message

```bash
#-------------------------------------------------------------------------------
# log_message - Write entry to log file
#
# Arguments:
#   $1 - Log level (DEBUG, INFO, WARN, ERROR)
#   $2 - Component name
#   $3 - Message
#
# Output:
#   Appends formatted line to LOG_FILE
#
# Example:
#   log_message "INFO" "BACKEND" "Started on port 8000"
#-------------------------------------------------------------------------------
log_message() {
    local level="$1"
    local component="$2"
    local message="$3"
    local timestamp
    
    timestamp=$(date "${LOG_DATE_FORMAT}")
    
    # Create log directory if needed
    [[ -d "${LOGS_PATH}" ]] || mkdir -p "${LOGS_PATH}"
    
    echo "[${timestamp}] [${level}] [${component}] ${message}" >> "${LOG_FILE}"
    
    # Also output to stderr if verbose
    if [[ "${VERBOSE}" == "true" ]]; then
        echo "[${level}] [${component}] ${message}" >&2
    fi
}
```

#### 4.1.5 PID Management Functions

```bash
save_pid() {
    local name="$1"
    local pid="$2"
    local pid_file="${PIDS_PATH}/${name}.pid"
    
    [[ -d "${PIDS_PATH}" ]] || mkdir -p "${PIDS_PATH}"
    echo "${pid}" > "${pid_file}"
    log_message "DEBUG" "PID" "Saved ${name} PID: ${pid}"
}

get_pid() {
    local name="$1"
    local pid_file="${PIDS_PATH}/${name}.pid"
    
    if [[ -f "${pid_file}" ]]; then
        cat "${pid_file}"
    fi
}

remove_pid() {
    local name="$1"
    local pid_file="${PIDS_PATH}/${name}.pid"
    
    if [[ -f "${pid_file}" ]]; then
        rm -f "${pid_file}"
        log_message "DEBUG" "PID" "Removed ${name} PID file"
    fi
}

is_process_running() {
    local pid="$1"
    
    if [[ -z "${pid}" ]]; then
        return 1
    fi
    
    kill -0 "${pid}" 2>/dev/null
}

find_process_by_pattern() {
    local pattern="$1"
    
    pgrep -f "${pattern}" 2>/dev/null | head -1
}
```

#### 4.1.6 Port Functions

```bash
check_port_available() {
    local port="$1"
    
    ! lsof -i ":${port}" -sTCP:LISTEN >/dev/null 2>&1
}

wait_for_port() {
    local port="$1"
    local timeout="${2:-30}"
    local elapsed=0
    
    while [[ ${elapsed} -lt ${timeout} ]]; do
        if lsof -i ":${port}" -sTCP:LISTEN >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
        ((elapsed++))
    done
    
    return 1
}
```

---

## 5. ERROR HANDLING DESIGN

### 5.1 Error Categories and Codes

| Code | Category | Description | Recovery |
|------|----------|-------------|----------|
| E001 | Configuration | Missing or invalid config | Abort with guidance |
| E002 | Prerequisite | Missing dependency | Abort with install steps |
| E003 | Port Conflict | Port already in use | Abort with lsof guidance |
| E004 | Process Start | Service failed to start | Abort with log location |
| E005 | Health Check | Service unhealthy | Abort with diagnostic steps |
| E006 | Permission | File/directory access | Abort with chmod guidance |
| W001 | Optional Skip | Optional service unavailable | Warn and continue |
| W002 | Already Running | Service already active | Warn and continue |

### 5.2 Error Display Format

```bash
display_error() {
    local code="$1"
    local title="$2"
    local details="$3"
    local suggestions="$4"
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    echo -e "║   ${COLOR_RED}❌ ERROR: ${code} - ${title}${COLOR_RESET}"
    echo "║                                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "WHAT HAPPENED:"
    echo "  ${details}"
    echo ""
    echo "SUGGESTED ACTIONS:"
    echo "${suggestions}"
    echo ""
    echo "LOG LOCATION:"
    echo "  ${LOG_FILE}"
    echo ""
    echo "TIMESTAMP: $(date "${LOG_DATE_FORMAT}")"
}
```

---

## 6. LOGGING DESIGN

### 6.1 Log Format

```
[TIMESTAMP] [LEVEL] [COMPONENT] MESSAGE
```

Example:
```
[2026-01-12T10:30:15+0530] [INFO] [IGNITE] Starting system ignition
[2026-01-12T10:30:16+0530] [INFO] [VENV] Virtual environment activated
[2026-01-12T10:30:17+0530] [INFO] [BACKEND] Started uvicorn (PID: 12345)
[2026-01-12T10:30:22+0530] [INFO] [HEALTH] Backend healthy after 5s
[2026-01-12T10:30:23+0530] [WARN] [FRONTEND] Frontend directory not found
[2026-01-12T10:30:25+0530] [INFO] [IGNITE] System ignition complete
```

### 6.2 Component Names

| Component | Used By | Purpose |
|-----------|---------|---------|
| IGNITE | ignite.sh | Startup orchestration |
| SHUTDOWN | shutdown.sh | Shutdown orchestration |
| BACKEND | ignite.sh, shutdown.sh | Backend server |
| NGROK | ignite.sh, shutdown.sh | ngrok tunnel |
| FRONTEND | ignite.sh, shutdown.sh | Frontend server |
| HEALTH | health-check.sh | Health verification |
| VENV | ignite.sh | Virtual environment |
| PID | utils.sh | PID file management |
| CONFIG | config.sh | Configuration |
| STATUS | utils.sh | Status messages |
| DISPLAY | utils.sh | Display output |

---

## 7. VISUAL OUTPUT DESIGN

### 7.1 Terminal Width

All output designed for 80-character terminal width (standard default).

### 7.2 Status Box Design

```bash
print_status_box() {
    local backend_status frontend_status ngrok_status
    local backend_url frontend_url ngrok_url
    
    # Determine status for each service
    backend_status="🟢 RUNNING"
    backend_url="${BACKEND_URL}"
    
    if [[ -n "${NGROK_PUBLIC_URL}" ]]; then
        ngrok_status="🟢 RUNNING"
        ngrok_url="${NGROK_PUBLIC_URL}"
    else
        ngrok_status="⚪ NOT STARTED"
        ngrok_url="(disabled or failed)"
    fi
    
    if [[ -f "${PIDS_PATH}/frontend.pid" ]]; then
        frontend_status="🟢 RUNNING"
        frontend_url="${FRONTEND_URL}"
    else
        frontend_status="⚪ NOT BUILT"
        frontend_url="(run frontend build when ready)"
    fi
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    echo "║   ✅ CIA-SIE SYSTEM IGNITION COMPLETE                                        ║"
    echo "║                                                                               ║"
    printf "║   Backend:   %-12s %-45s ║\n" "${backend_status}" "${backend_url}"
    printf "║   Tunnel:    %-12s %-45s ║\n" "${ngrok_status}" "${ngrok_url}"
    printf "║   Frontend:  %-12s %-45s ║\n" "${frontend_status}" "${frontend_url}"
    echo "║                                                                               ║"
    echo "║   Press Ctrl+C to stop all services, or use stop-cia-sie.command             ║"
    echo "║                                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
}
```

---

## 8. CONFIGURATION DESIGN

### 8.1 Override Hierarchy

1. **Hardcoded defaults** (in config.sh)
2. **Environment variables** (CIA_SIE_* prefix)
3. **Command-line arguments** (--port=XXXX)

### 8.2 Environment Variable Naming

All environment variables use prefix `CIA_SIE_` for namespacing.

| Variable | Default | Description |
|----------|---------|-------------|
| `CIA_SIE_ROOT` | Auto-detect | Project root path |
| `CIA_SIE_BACKEND_PORT` | 8000 | Backend port |
| `CIA_SIE_FRONTEND_PORT` | 5173 | Frontend port |
| `CIA_SIE_HEALTH_TIMEOUT` | 30 | Health check timeout |
| `CIA_SIE_OPEN_BROWSER` | true | Auto-open browser |
| `CIA_SIE_START_NGROK` | true | Start ngrok tunnel |
| `CIA_SIE_VERBOSE` | false | Verbose output |

---

## 9. PROCESS MANAGEMENT DESIGN

### 9.1 Background Process Handling

All services run as background processes using `nohup ... &` pattern:

```bash
nohup <command> >> <logfile> 2>&1 &
pid=$!
```

### 9.2 Signal Handling

```bash
# Trap signals for clean shutdown
trap 'shutdown_all; exit 0' INT TERM

shutdown_all() {
    echo ""
    echo "Received shutdown signal..."
    source "${SCRIPTS_PATH}/shutdown.sh"
    main
}
```

### 9.3 Process Identification

| Service | Primary ID | Fallback ID |
|---------|-----------|-------------|
| Backend | PID file | `pgrep -f "uvicorn.*cia_sie"` |
| ngrok | PID file | `pgrep -f "ngrok http"` |
| Frontend | PID file | `pgrep -f "vite.*5173"` |

---

## 10. TESTING INTERFACE DESIGN

### 10.1 Testable Functions

All functions designed to be callable in isolation for testing:

```bash
# Example test
source ./scripts/launcher/config.sh
source ./scripts/launcher/utils.sh
source ./scripts/launcher/health-check.sh

# Test health check against mock server
HEALTH_ENDPOINT="http://localhost:9999/health"
check_backend_health
echo "Exit code: $?"
```

### 10.2 Mock-Friendly Design

- All external calls (curl, kill, pgrep) through wrapper functions
- Configuration injectable via environment variables
- No hardcoded paths (all derived from PROJECT_ROOT)

---

## 11. DEPLOYMENT CHECKLIST

### 11.1 Pre-Deployment

| Step | Command | Expected Result |
|------|---------|-----------------|
| 1. Create directories | `mkdir -p scripts/launcher pids logs` | Directories exist |
| 2. Create files | (implementation phase) | Files exist |
| 3. Set permissions | `chmod 755 *.command scripts/launcher/*.sh` | Executable |
| 4. Verify venv | `test -d venv/bin/activate` | Returns 0 |
| 5. Verify backend | `python -c "import cia_sie"` | No error |

### 11.2 Post-Deployment Verification

| Test | Method | Expected |
|------|--------|----------|
| Start script runs | Double-click | Terminal opens, services start |
| Stop script runs | Double-click | Services stop, terminal shows complete |
| Health check works | `curl localhost:8000/health` | 200 OK |
| Logs created | `ls logs/launcher.log` | File exists |
| PIDs created | `ls pids/` | PID files present |

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
| 1.0.0 | 12 Jan 2026 | Claude | Initial detailed design |

---

**END OF DETAILED DESIGN DOCUMENT**
