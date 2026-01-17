#!/bin/zsh
#===============================================================================
#
#   CIA-SIE LAUNCHER IGNITION SCRIPT
#   ═════════════════════════════════
#
#   Document ID: IMPL-LAUNCHER-IGNITE
#   Version: 1.0.0
#   Date: 12 January 2026
#
#   Purpose: Orchestrate the complete system startup sequence
#
#   Usage: This file is sourced by start-cia-sie.command
#          source ./scripts/launcher/ignite.sh
#          main "$@"
#
#   Dependencies: config.sh, utils.sh, health-check.sh must be sourced first
#
#===============================================================================

#-------------------------------------------------------------------------------
# Source dependencies if not already loaded
#-------------------------------------------------------------------------------
SCRIPT_DIR="${SCRIPTS_PATH:-$(cd "$(dirname "${BASH_SOURCE[0]:-${0}}")" && pwd)}"

if [[ -z "${PROJECT_ROOT:-}" ]]; then
    source "${SCRIPT_DIR}/config.sh"
fi

if ! type log_message &>/dev/null; then
    source "${SCRIPT_DIR}/utils.sh"
fi

if ! type wait_for_backend &>/dev/null; then
    source "${SCRIPT_DIR}/health-check.sh"
fi

#-------------------------------------------------------------------------------
# PREREQUISITE VERIFICATION
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# verify_prerequisites - Check all required dependencies
#
# Returns:
#   0 if all prerequisites met, 1 otherwise
#-------------------------------------------------------------------------------
verify_prerequisites() {
    local errors=0
    
    log_message "INFO" "PREREQ" "Verifying prerequisites"
    
    # Check Python virtual environment
    if [[ ! -f "${VENV_PATH}/bin/activate" ]]; then
        print_detail "Virtual Environment" "${COLOR_RED}NOT FOUND${COLOR_RESET}"
        log_message "ERROR" "PREREQ" "Virtual environment not found at ${VENV_PATH}"
        ((errors++))
    else
        print_detail "Virtual Environment" "${VENV_PATH}"
    fi
    
    # Check if backend source exists
    if [[ ! -f "${BACKEND_PATH}/cia_sie/main.py" ]]; then
        print_detail "Backend Source" "${COLOR_RED}NOT FOUND${COLOR_RESET}"
        log_message "ERROR" "PREREQ" "Backend source not found"
        ((errors++))
    else
        print_detail "Backend Source" "${BACKEND_PATH}"
    fi
    
    # Check if database directory exists
    if [[ ! -d "${DATA_PATH}" ]]; then
        print_detail "Data Directory" "${COLOR_YELLOW}Creating...${COLOR_RESET}"
        mkdir -p "${DATA_PATH}"
    fi
    
    # Check if port is available
    if ! check_port_available "${BACKEND_PORT}"; then
        local process_info
        process_info=$(get_port_process "${BACKEND_PORT}")
        print_detail "Port ${BACKEND_PORT}" "${COLOR_RED}IN USE${COLOR_RESET}"
        print_info "Process using port: ${process_info}"
        log_message "ERROR" "PREREQ" "Port ${BACKEND_PORT} already in use"
        ((errors++))
    else
        print_detail "Port ${BACKEND_PORT}" "Available"
    fi
    
    # Check ngrok if enabled
    if [[ "${START_NGROK}" == "true" ]]; then
        if ! command -v ngrok &>/dev/null; then
            print_detail "ngrok" "${COLOR_YELLOW}NOT INSTALLED${COLOR_RESET}"
            log_message "WARN" "PREREQ" "ngrok not installed, tunnel will be skipped"
        else
            print_detail "ngrok" "$(ngrok version 2>/dev/null | head -1)"
        fi
    fi
    
    if [[ ${errors} -gt 0 ]]; then
        log_message "ERROR" "PREREQ" "Prerequisites check failed with ${errors} errors"
        return 1
    fi
    
    log_message "INFO" "PREREQ" "All prerequisites verified"
    return 0
}

#-------------------------------------------------------------------------------
# SERVICE START FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# activate_venv - Activate Python virtual environment
#
# Returns:
#   0 if activated, 1 on error
#-------------------------------------------------------------------------------
activate_venv() {
    local venv_activate="${VENV_PATH}/bin/activate"
    
    if [[ ! -f "${venv_activate}" ]]; then
        log_message "ERROR" "VENV" "Virtual environment not found: ${VENV_PATH}"
        return 1
    fi
    
    # shellcheck source=/dev/null
    source "${venv_activate}"
    
    print_detail "Python" "$(python3 --version 2>&1)"
    log_message "INFO" "VENV" "Virtual environment activated"
    return 0
}

#-------------------------------------------------------------------------------
# start_backend - Start the FastAPI backend server
#
# Returns:
#   0 if started and healthy, 1 on error
#-------------------------------------------------------------------------------
start_backend() {
    local pid
    
    # Check if already running
    pid=$(find_process_by_pattern "${BACKEND_PATTERN}")
    if [[ -n "${pid}" ]]; then
        log_message "WARN" "BACKEND" "Backend already running (PID: ${pid})"
        save_pid "backend" "${pid}"
        print_detail "Status" "Already running (PID: ${pid})"
        
        # Verify it's actually healthy
        if check_backend_health; then
            return 0
        else
            print_warning "Backend process exists but not responding"
            log_message "WARN" "BACKEND" "Existing process not responding, attempting restart"
            kill -TERM "${pid}" 2>/dev/null
            sleep 2
        fi
    fi
    
    # Check port availability
    if ! check_port_available "${BACKEND_PORT}"; then
        log_message "ERROR" "BACKEND" "Port ${BACKEND_PORT} is already in use"
        display_error "E003" "Port Conflict" \
            "Port ${BACKEND_PORT} is already in use by another process." \
            "  1. Run: lsof -i :${BACKEND_PORT}
  2. Stop the conflicting process
  3. Run start-cia-sie.command again"
        return 1
    fi
    
    # Ensure logs directory exists
    ensure_directory "${LOGS_PATH}"
    
    # Change to project root for module resolution
    cd "${PROJECT_ROOT}" || return 1
    
    print_detail "Command" "uvicorn cia_sie.api.app:app --port ${BACKEND_PORT}"
    print_detail "Logs" "${BACKEND_LOG_FILE}"
    
    # Start uvicorn in background
    # The FastAPI app is defined in src/cia_sie/api/app.py
    nohup python -m uvicorn cia_sie.api.app:app \
        --host 0.0.0.0 \
        --port "${BACKEND_PORT}" \
        --log-level info \
        >> "${BACKEND_LOG_FILE}" 2>&1 &
    
    pid=$!
    save_pid "backend" "${pid}"
    
    log_message "INFO" "BACKEND" "Started uvicorn (PID: ${pid})"
    print_detail "PID" "${pid}"
    print_detail "Status" "Waiting for health check..."
    
    # Wait for health
    if ! wait_for_backend; then
        log_message "ERROR" "BACKEND" "Health check failed"
        kill "${pid}" 2>/dev/null
        remove_pid "backend"
        display_error "E005" "Health Check Failed" \
            "The backend server started but did not become healthy." \
            "  1. Check logs: tail -50 ${BACKEND_LOG_FILE}
  2. Look for Python errors or missing dependencies
  3. Verify the database exists at ${DATA_PATH}/cia_sie.db"
        return 1
    fi
    
    return 0
}

#-------------------------------------------------------------------------------
# start_ngrok - Start ngrok tunnel for webhooks
#
# Returns:
#   0 if started, 1 on error (non-fatal)
#-------------------------------------------------------------------------------
start_ngrok() {
    local pid
    local attempt=0
    local max_attempts=10
    
    # Check if ngrok is installed
    if ! command -v ngrok &>/dev/null; then
        log_message "WARN" "NGROK" "ngrok not installed"
        print_warning "ngrok not installed, skipping tunnel"
        return 1
    fi
    
    # Check if already running
    pid=$(find_process_by_pattern "${NGROK_PATTERN}")
    if [[ -n "${pid}" ]]; then
        log_message "WARN" "NGROK" "ngrok already running (PID: ${pid})"
        save_pid "ngrok" "${pid}"
        print_detail "Status" "Already running (PID: ${pid})"
        
        # Try to get existing URL
        NGROK_PUBLIC_URL=$(get_ngrok_url)
        if [[ -n "${NGROK_PUBLIC_URL}" ]]; then
            print_detail "URL" "${NGROK_PUBLIC_URL}"
            return 0
        fi
        return 0
    fi
    
    # Ensure logs directory exists
    ensure_directory "${LOGS_PATH}"
    
    print_detail "Command" "ngrok http ${BACKEND_PORT}"
    print_detail "Logs" "${NGROK_LOG_FILE}"
    
    # Start ngrok in background
    nohup ngrok http "${BACKEND_PORT}" \
        --log=stdout \
        >> "${NGROK_LOG_FILE}" 2>&1 &
    
    pid=$!
    save_pid "ngrok" "${pid}"
    
    log_message "INFO" "NGROK" "Started ngrok (PID: ${pid})"
    print_detail "PID" "${pid}"
    print_detail "Status" "Waiting for tunnel..."
    
    # Wait for API to be ready and get URL
    while [[ ${attempt} -lt ${max_attempts} ]]; do
        sleep 2
        NGROK_PUBLIC_URL=$(get_ngrok_url)
        if [[ -n "${NGROK_PUBLIC_URL}" ]]; then
            log_message "INFO" "NGROK" "Tunnel established: ${NGROK_PUBLIC_URL}"
            return 0
        fi
        ((attempt++))
    done
    
    log_message "WARN" "NGROK" "Could not retrieve tunnel URL"
    print_warning "Tunnel started but URL not available yet"
    return 0  # Non-fatal, ngrok may still be establishing
}

#-------------------------------------------------------------------------------
# get_ngrok_url - Get the public URL from ngrok API
#
# Output:
#   Public URL or empty string
#-------------------------------------------------------------------------------
get_ngrok_url() {
    local response
    local url
    
    response=$(curl -s "${NGROK_API_URL}" 2>/dev/null)
    
    if [[ -n "${response}" ]]; then
        # Extract HTTPS URL
        url=$(echo "${response}" | grep -o '"public_url":"https://[^"]*"' | head -1 | cut -d'"' -f4)
        if [[ -n "${url}" ]]; then
            echo "${url}"
            return
        fi
        # Fall back to any URL
        url=$(echo "${response}" | grep -o '"public_url":"[^"]*"' | head -1 | cut -d'"' -f4)
        echo "${url}"
    fi
}

#-------------------------------------------------------------------------------
# start_frontend - Start the React frontend dev server
#
# Returns:
#   0 if started or not applicable, 1 on error (non-fatal)
#-------------------------------------------------------------------------------
start_frontend() {
    local pid
    
    # Check if directory exists
    if [[ ! -d "${FRONTEND_PATH}" ]]; then
        log_message "WARN" "FRONTEND" "Frontend directory not found: ${FRONTEND_PATH}"
        return 1
    fi
    
    # Check if package.json exists
    if [[ ! -f "${FRONTEND_PATH}/package.json" ]]; then
        log_message "WARN" "FRONTEND" "No package.json found"
        print_warning "No package.json found in frontend directory"
        return 1
    fi
    
    # Check if node_modules exists
    if [[ ! -d "${FRONTEND_PATH}/node_modules" ]]; then
        log_message "WARN" "FRONTEND" "node_modules not found, run npm install"
        print_warning "node_modules not found - run 'npm install' in frontend directory"
        return 1
    fi
    
    # Check if already running
    pid=$(find_process_by_pattern "${FRONTEND_PATTERN}")
    if [[ -n "${pid}" ]]; then
        log_message "WARN" "FRONTEND" "Frontend already running (PID: ${pid})"
        save_pid "frontend" "${pid}"
        print_detail "Status" "Already running (PID: ${pid})"
        return 0
    fi
    
    # Ensure logs directory exists
    ensure_directory "${LOGS_PATH}"
    
    print_detail "Command" "npm run dev"
    print_detail "Logs" "${FRONTEND_LOG_FILE}"
    
    # Change to frontend directory
    cd "${FRONTEND_PATH}" || return 1
    
    # Start dev server in background
    nohup npm run dev \
        >> "${FRONTEND_LOG_FILE}" 2>&1 &
    
    pid=$!
    save_pid "frontend" "${pid}"
    
    log_message "INFO" "FRONTEND" "Started frontend (PID: ${pid})"
    print_detail "PID" "${pid}"
    
    # Return to project root
    cd "${PROJECT_ROOT}" || return 1
    
    # Wait for port
    if ! wait_for_port "${FRONTEND_PORT}" 30; then
        log_message "WARN" "FRONTEND" "Frontend may not have started correctly"
        print_warning "Frontend starting slowly, check logs if issues persist"
    fi
    
    return 0
}

#-------------------------------------------------------------------------------
# open_browser - Open browser to application
#-------------------------------------------------------------------------------
open_browser() {
    local url
    
    # Prefer frontend URL if running, otherwise API docs
    if is_process_running "$(get_pid "frontend")"; then
        url="${FRONTEND_URL}"
    else
        url="${DOCS_ENDPOINT}"
    fi
    
    print_detail "URL" "${url}"
    
    # macOS open command
    if command -v open &>/dev/null; then
        open "${url}" &>/dev/null
        log_message "INFO" "BROWSER" "Opened browser to ${url}"
    else
        log_message "WARN" "BROWSER" "Could not open browser (open command not found)"
        print_info "Open this URL in your browser: ${url}"
    fi
}

#-------------------------------------------------------------------------------
# shutdown_all - Stop all services (called on Ctrl+C)
#-------------------------------------------------------------------------------
shutdown_all() {
    echo ""
    echo ""
    log_message "INFO" "IGNITE" "Received shutdown signal"
    
    # Source shutdown script and run
    source "${SCRIPT_DIR}/shutdown.sh"
    main
}

#-------------------------------------------------------------------------------
# MAIN ENTRY POINT
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# main - Main ignition sequence
#
# Arguments:
#   $@ - Command line arguments (currently unused)
#
# Returns:
#   0 on success, 1 on critical failure
#-------------------------------------------------------------------------------
main() {
    local total_steps=6
    local step=0
    
    # Initialize
    print_header "CIA-SIE SYSTEM IGNITION" "🚀"
    log_message "INFO" "IGNITE" "Starting system ignition"
    log_message "INFO" "IGNITE" "Project root: ${PROJECT_ROOT}"
    
    # Ensure runtime directories exist
    ensure_directory "${PIDS_PATH}"
    ensure_directory "${LOGS_PATH}"
    
    # Step 1: Verify prerequisites
    ((step++))
    print_step ${step} ${total_steps} "Verifying prerequisites..."
    if ! verify_prerequisites; then
        print_error "Prerequisites check failed"
        display_error "E002" "Prerequisites Not Met" \
            "One or more required components are missing or misconfigured." \
            "  1. Ensure Python virtual environment exists: python3 -m venv venv
  2. Install dependencies: pip install -e .
  3. Verify backend source exists in src/cia_sie/"
        return 1
    fi
    print_success "Prerequisites verified"
    
    # Step 2: Activate virtual environment
    ((step++))
    print_step ${step} ${total_steps} "Activating Python environment..."
    if ! activate_venv; then
        print_error "Failed to activate virtual environment"
        return 1
    fi
    print_success "Python environment activated"
    
    # Step 3: Start backend
    ((step++))
    print_step ${step} ${total_steps} "Starting Backend server..."
    if ! start_backend; then
        print_error "Failed to start backend"
        return 1
    fi
    print_success "Backend running on port ${BACKEND_PORT}"
    
    # Step 4: Start ngrok (if enabled)
    ((step++))
    if [[ "${START_NGROK}" == "true" ]]; then
        print_step ${step} ${total_steps} "Starting webhook tunnel..."
        if start_ngrok; then
            if [[ -n "${NGROK_PUBLIC_URL}" ]]; then
                print_success "Tunnel established: ${NGROK_PUBLIC_URL}"
            else
                print_success "Tunnel starting..."
            fi
        else
            print_warning "Tunnel not started (non-critical)"
        fi
    else
        print_step ${step} ${total_steps} "Webhook tunnel..."
        print_info "Skipped (disabled in config)"
    fi
    
    # Step 5: Start frontend (if exists)
    ((step++))
    print_step ${step} ${total_steps} "Starting Frontend server..."
    if [[ -d "${FRONTEND_PATH}" ]]; then
        if start_frontend; then
            print_success "Frontend running on port ${FRONTEND_PORT}"
        else
            print_warning "Frontend not started (non-critical)"
        fi
    else
        print_warning "Frontend not built yet"
        print_info "Backend and API are fully operational"
        print_info "Frontend will be built in a future phase"
    fi
    
    # Step 6: Open browser (if enabled)
    ((step++))
    if [[ "${OPEN_BROWSER}" == "true" ]]; then
        print_step ${step} ${total_steps} "Opening browser..."
        open_browser
        print_success "Browser opened"
    else
        print_step ${step} ${total_steps} "Browser..."
        print_info "Auto-open disabled in config"
    fi
    
    # Final status
    print_status_box
    
    log_message "INFO" "IGNITE" "System ignition complete"
    
    # Set up signal handler for clean shutdown
    trap 'shutdown_all; exit 0' INT TERM
    
    # Keep script running (allows Ctrl+C to trigger cleanup)
    # This is necessary because background processes would otherwise be orphaned
    echo ""
    echo "Services are running. This terminal will remain open."
    echo "Press Ctrl+C to stop all services gracefully."
    echo ""
    
    while true; do
        sleep 60
        # Periodic health check (silent)
        if ! is_process_running "$(get_pid "backend")"; then
            echo ""
            print_warning "Backend process has stopped unexpectedly"
            log_message "ERROR" "MONITOR" "Backend process stopped unexpectedly"
        fi
    done
}

# If run directly (not sourced), execute main
# In zsh, check if the script was sourced using ZSH_EVAL_CONTEXT
if [[ -n "${ZSH_VERSION:-}" ]]; then
    # In zsh, ZSH_EVAL_CONTEXT contains 'file' when sourced
    if [[ ! "${ZSH_EVAL_CONTEXT:-}" =~ ":file$" ]] && [[ ! "${ZSH_EVAL_CONTEXT:-}" =~ ":file:" ]]; then
        main "$@"
    fi
elif [[ "${BASH_SOURCE[0]:-${0}}" == "${0}" ]]; then
    main "$@"
fi
