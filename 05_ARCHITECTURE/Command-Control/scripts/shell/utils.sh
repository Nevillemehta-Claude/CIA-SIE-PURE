#!/bin/zsh
#===============================================================================
#
#   CIA-SIE LAUNCHER UTILITIES
#   ═══════════════════════════
#
#   Document ID: IMPL-LAUNCHER-UTILS
#   Version: 1.0.0
#   Date: 12 January 2026
#
#   Purpose: Shared utility functions for display, logging, and process 
#            management
#
#   Usage: This file is sourced by other launcher scripts
#          source ./scripts/launcher/utils.sh
#
#   Dependencies: config.sh must be sourced first
#
#===============================================================================

#-------------------------------------------------------------------------------
# DISPLAY FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# print_header - Display major section header
#
# Arguments:
#   $1 - Header message
#
# Output:
#   Formatted header to stdout
#-------------------------------------------------------------------------------
print_header() {
    local message="$1"
    local emoji="${2:-🚀}"
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    printf "║   %s %-72s║\n" "${emoji}" "${message}"
    echo "║                                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    log_message "INFO" "HEADER" "${message}"
}

#-------------------------------------------------------------------------------
# print_step - Display step progress
#
# Arguments:
#   $1 - Step number
#   $2 - Total steps
#   $3 - Step message
#-------------------------------------------------------------------------------
print_step() {
    local step="$1"
    local total="$2"
    local message="$3"
    local timestamp
    
    timestamp=$(date "+%H:%M:%S")
    
    echo ""
    echo -e "[${timestamp}] ${COLOR_CYAN}STEP ${step}/${total}:${COLOR_RESET} ${message}"
}

#-------------------------------------------------------------------------------
# print_detail - Display detail line under a step
#
# Arguments:
#   $1 - Label
#   $2 - Value
#-------------------------------------------------------------------------------
print_detail() {
    local label="$1"
    local value="$2"
    
    echo -e "         ├── ${label}: ${value}"
}

#-------------------------------------------------------------------------------
# print_success - Display success message
#
# Arguments:
#   $1 - Success message
#-------------------------------------------------------------------------------
print_success() {
    local message="$1"
    echo -e "         └── ${COLOR_GREEN}${SYMBOL_SUCCESS} ${message}${COLOR_RESET}"
    log_message "INFO" "SUCCESS" "${message}"
}

#-------------------------------------------------------------------------------
# print_warning - Display warning message
#
# Arguments:
#   $1 - Warning message
#-------------------------------------------------------------------------------
print_warning() {
    local message="$1"
    echo -e "         └── ${COLOR_YELLOW}${SYMBOL_WARNING} ${message}${COLOR_RESET}"
    log_message "WARN" "WARNING" "${message}"
}

#-------------------------------------------------------------------------------
# print_error - Display error message
#
# Arguments:
#   $1 - Error message
#-------------------------------------------------------------------------------
print_error() {
    local message="$1"
    echo -e "         └── ${COLOR_RED}${SYMBOL_FAILURE} ${message}${COLOR_RESET}"
    log_message "ERROR" "ERROR" "${message}"
}

#-------------------------------------------------------------------------------
# print_info - Display info message (indented under step)
#
# Arguments:
#   $1 - Info message
#-------------------------------------------------------------------------------
print_info() {
    local message="$1"
    echo -e "             ${COLOR_BLUE}${SYMBOL_INFO} ${message}${COLOR_RESET}"
}

#-------------------------------------------------------------------------------
# print_status_box - Display final status summary after ignition
#-------------------------------------------------------------------------------
print_status_box() {
    local backend_status backend_url
    local ngrok_status ngrok_url
    local frontend_status frontend_url
    
    # Backend status
    if is_process_running "$(get_pid "backend")"; then
        backend_status="🟢 RUNNING"
        backend_url="${BACKEND_URL}"
    else
        backend_status="🔴 STOPPED"
        backend_url="(not running)"
    fi
    
    # ngrok status
    if [[ -n "${NGROK_PUBLIC_URL}" ]]; then
        ngrok_status="🟢 RUNNING"
        ngrok_url="${NGROK_PUBLIC_URL}"
    elif is_process_running "$(get_pid "ngrok")"; then
        ngrok_status="🟡 STARTING"
        ngrok_url="(waiting for URL)"
    else
        ngrok_status="⚪ NOT STARTED"
        ngrok_url="(disabled or failed)"
    fi
    
    # Frontend status
    if is_process_running "$(get_pid "frontend")"; then
        frontend_status="🟢 RUNNING"
        frontend_url="${FRONTEND_URL}"
    elif [[ ! -d "${FRONTEND_PATH}" ]]; then
        frontend_status="⚪ NOT BUILT"
        frontend_url="(frontend not yet created)"
    else
        frontend_status="🔴 STOPPED"
        frontend_url="(not running)"
    fi
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    echo "║   ✅ CIA-SIE SYSTEM IGNITION COMPLETE                                        ║"
    echo "║                                                                               ║"
    printf "║   Backend:   %-13s %-44s ║\n" "${backend_status}" "${backend_url}"
    printf "║   Tunnel:    %-13s %-44s ║\n" "${ngrok_status}" "${ngrok_url}"
    printf "║   Frontend:  %-13s %-44s ║\n" "${frontend_status}" "${frontend_url}"
    echo "║                                                                               ║"
    echo "║   Press Ctrl+C to stop all services, or use stop-cia-sie.command             ║"
    echo "║                                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
}

#-------------------------------------------------------------------------------
# print_shutdown_complete - Display shutdown complete message
#-------------------------------------------------------------------------------
print_shutdown_complete() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    echo "║   ✅ CIA-SIE SYSTEM SHUTDOWN COMPLETE                                        ║"
    echo "║                                                                               ║"
    echo "║   All services have been stopped.                                             ║"
    echo "║   It is now safe to close this terminal.                                      ║"
    echo "║                                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
}

#-------------------------------------------------------------------------------
# display_error - Display formatted error box
#
# Arguments:
#   $1 - Error code
#   $2 - Error title
#   $3 - Error details
#   $4 - Suggested actions (multi-line string)
#-------------------------------------------------------------------------------
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
    
    log_message "ERROR" "DISPLAY" "Error ${code}: ${title}"
}

#-------------------------------------------------------------------------------
# LOGGING FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# log_message - Write entry to log file
#
# Arguments:
#   $1 - Log level (DEBUG, INFO, WARN, ERROR)
#   $2 - Component name
#   $3 - Message
#-------------------------------------------------------------------------------
log_message() {
    local level="$1"
    local component="$2"
    local message="$3"
    local timestamp
    
    timestamp=$(date "${LOG_DATE_FORMAT}")
    
    # Create log directory if needed
    ensure_directory "${LOGS_PATH}"
    
    # Write to log file
    echo "[${timestamp}] [${level}] [${component}] ${message}" >> "${LOG_FILE}"
    
    # Also output to stderr if verbose mode
    if [[ "${VERBOSE}" == "true" ]]; then
        echo "[${level}] [${component}] ${message}" >&2
    fi
}

#-------------------------------------------------------------------------------
# get_timestamp - Get formatted timestamp
#
# Output:
#   ISO 8601 formatted timestamp
#-------------------------------------------------------------------------------
get_timestamp() {
    date "${LOG_DATE_FORMAT}"
}

#-------------------------------------------------------------------------------
# DIRECTORY FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# ensure_directory - Create directory if it doesn't exist
#
# Arguments:
#   $1 - Directory path
#-------------------------------------------------------------------------------
ensure_directory() {
    local dir="$1"
    
    if [[ ! -d "${dir}" ]]; then
        mkdir -p "${dir}"
        log_message "DEBUG" "UTIL" "Created directory: ${dir}"
    fi
}

#-------------------------------------------------------------------------------
# PID MANAGEMENT FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# save_pid - Save process ID to file
#
# Arguments:
#   $1 - Service name (backend, ngrok, frontend)
#   $2 - PID value
#-------------------------------------------------------------------------------
save_pid() {
    local name="$1"
    local pid="$2"
    local pid_file="${PIDS_PATH}/${name}.pid"
    
    ensure_directory "${PIDS_PATH}"
    echo "${pid}" > "${pid_file}"
    log_message "DEBUG" "PID" "Saved ${name} PID: ${pid} to ${pid_file}"
}

#-------------------------------------------------------------------------------
# get_pid - Read process ID from file
#
# Arguments:
#   $1 - Service name
#
# Output:
#   PID value if file exists, empty string otherwise
#-------------------------------------------------------------------------------
get_pid() {
    local name="$1"
    local pid_file="${PIDS_PATH}/${name}.pid"
    
    if [[ -f "${pid_file}" ]]; then
        cat "${pid_file}"
    fi
}

#-------------------------------------------------------------------------------
# remove_pid - Delete PID file
#
# Arguments:
#   $1 - Service name
#-------------------------------------------------------------------------------
remove_pid() {
    local name="$1"
    local pid_file="${PIDS_PATH}/${name}.pid"
    
    if [[ -f "${pid_file}" ]]; then
        rm -f "${pid_file}"
        log_message "DEBUG" "PID" "Removed ${name} PID file"
    fi
}

#-------------------------------------------------------------------------------
# is_process_running - Check if a process is running
#
# Arguments:
#   $1 - PID to check
#
# Returns:
#   0 if running, 1 if not
#-------------------------------------------------------------------------------
is_process_running() {
    local pid="$1"
    
    # Empty PID means not running
    if [[ -z "${pid}" ]]; then
        return 1
    fi
    
    # Check if process exists
    kill -0 "${pid}" 2>/dev/null
}

#-------------------------------------------------------------------------------
# find_process_by_pattern - Find PID by process pattern
#
# Arguments:
#   $1 - Pattern to match
#
# Output:
#   PID of first matching process, empty if none
#-------------------------------------------------------------------------------
find_process_by_pattern() {
    local pattern="$1"
    
    pgrep -f "${pattern}" 2>/dev/null | head -1
}

#-------------------------------------------------------------------------------
# PORT FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# check_port_available - Check if a port is available
#
# Arguments:
#   $1 - Port number
#
# Returns:
#   0 if available, 1 if in use
#-------------------------------------------------------------------------------
check_port_available() {
    local port="$1"
    
    ! lsof -i ":${port}" -sTCP:LISTEN >/dev/null 2>&1
}

#-------------------------------------------------------------------------------
# wait_for_port - Wait until a port is listening
#
# Arguments:
#   $1 - Port number
#   $2 - Timeout in seconds (default 30)
#
# Returns:
#   0 if port becomes available, 1 if timeout
#-------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
# get_port_process - Get the process using a port
#
# Arguments:
#   $1 - Port number
#
# Output:
#   Process information or empty
#-------------------------------------------------------------------------------
get_port_process() {
    local port="$1"
    
    lsof -i ":${port}" -sTCP:LISTEN 2>/dev/null | tail -1
}
