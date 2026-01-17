#!/bin/zsh
#===============================================================================
#
#   CIA-SIE LAUNCHER SHUTDOWN SCRIPT
#   ═════════════════════════════════
#
#   Document ID: IMPL-LAUNCHER-SHUTDOWN
#   Version: 1.0.0
#   Date: 12 January 2026
#
#   Purpose: Orchestrate the complete system shutdown sequence
#
#   Usage: This file is sourced by stop-cia-sie.command
#          source ./scripts/launcher/shutdown.sh
#          main "$@"
#
#   Dependencies: config.sh and utils.sh must be sourced first
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

#-------------------------------------------------------------------------------
# SERVICE STOP FUNCTIONS
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# stop_service - Stop a service by name
#
# Arguments:
#   $1 - Service name (backend, ngrok, frontend)
#   $2 - Process pattern to match
#
# Returns:
#   0 on success (stopped or not running)
#-------------------------------------------------------------------------------
stop_service() {
    local name="$1"
    local pattern="$2"
    local pid
    local attempts=0
    local max_attempts="${PROCESS_STOP_TIMEOUT}"
    
    # Get PID from file
    pid=$(get_pid "${name}")
    
    # If no PID file, try to find by pattern
    if [[ -z "${pid}" ]] || ! is_process_running "${pid}"; then
        pid=$(find_process_by_pattern "${pattern}")
    fi
    
    # If still no PID, service is not running
    if [[ -z "${pid}" ]]; then
        print_detail "Status" "Not running"
        remove_pid "${name}"
        log_message "INFO" "SHUTDOWN" "${name} was not running"
        return 0
    fi
    
    print_detail "PID" "${pid}"
    log_message "INFO" "SHUTDOWN" "Stopping ${name} (PID: ${pid})"
    
    # Send SIGTERM for graceful shutdown
    kill -TERM "${pid}" 2>/dev/null
    
    # Wait for process to stop
    while [[ ${attempts} -lt ${max_attempts} ]]; do
        if ! is_process_running "${pid}"; then
            print_success "Stopped gracefully"
            remove_pid "${name}"
            log_message "INFO" "SHUTDOWN" "${name} stopped gracefully"
            return 0
        fi
        sleep 1
        ((attempts++))
        
        # Show progress
        if [[ $((attempts % 3)) -eq 0 ]]; then
            print_detail "Status" "Waiting... (${attempts}/${max_attempts}s)"
        fi
    done
    
    # Force kill if still running
    log_message "WARN" "SHUTDOWN" "${name} did not stop gracefully, sending SIGKILL"
    print_detail "Status" "Force killing..."
    
    kill -KILL "${pid}" 2>/dev/null
    sleep 1
    
    if ! is_process_running "${pid}"; then
        print_success "Stopped (forced)"
        remove_pid "${name}"
        log_message "INFO" "SHUTDOWN" "${name} force killed"
        return 0
    fi
    
    print_error "Failed to stop"
    log_message "ERROR" "SHUTDOWN" "Failed to stop ${name}"
    return 1
}

#-------------------------------------------------------------------------------
# stop_frontend - Stop the frontend server
#-------------------------------------------------------------------------------
stop_frontend() {
    stop_service "frontend" "${FRONTEND_PATTERN}"
}

#-------------------------------------------------------------------------------
# stop_ngrok - Stop the ngrok tunnel
#-------------------------------------------------------------------------------
stop_ngrok() {
    stop_service "ngrok" "${NGROK_PATTERN}"
}

#-------------------------------------------------------------------------------
# stop_backend - Stop the backend server
#-------------------------------------------------------------------------------
stop_backend() {
    stop_service "backend" "${BACKEND_PATTERN}"
}

#-------------------------------------------------------------------------------
# cleanup_all - Clean up all PID files and verify no orphans
#-------------------------------------------------------------------------------
cleanup_all() {
    local orphans
    
    # Remove any remaining PID files
    for service in backend ngrok frontend; do
        remove_pid "${service}"
    done
    
    # Check for orphan processes
    orphans=$(find_process_by_pattern "uvicorn.*cia_sie")
    if [[ -n "${orphans}" ]]; then
        log_message "WARN" "CLEANUP" "Found orphan uvicorn process: ${orphans}"
        print_warning "Found orphan backend process (PID: ${orphans})"
        print_info "Run: kill ${orphans}"
    fi
    
    orphans=$(find_process_by_pattern "ngrok http")
    if [[ -n "${orphans}" ]]; then
        log_message "WARN" "CLEANUP" "Found orphan ngrok process: ${orphans}"
        print_warning "Found orphan ngrok process (PID: ${orphans})"
        print_info "Run: kill ${orphans}"
    fi
    
    log_message "INFO" "CLEANUP" "Cleanup complete"
}

#-------------------------------------------------------------------------------
# MAIN ENTRY POINT
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# main - Main shutdown sequence
#
# Arguments:
#   $@ - Command line arguments (currently unused)
#
# Returns:
#   0 on success
#-------------------------------------------------------------------------------
main() {
    local total_steps=4
    local step=0
    local errors=0
    
    # Header
    print_header "CIA-SIE SYSTEM SHUTDOWN" "🛑"
    log_message "INFO" "SHUTDOWN" "Starting system shutdown"
    
    # Step 1: Stop frontend
    ((step++))
    print_step ${step} ${total_steps} "Stopping Frontend..."
    if ! stop_frontend; then
        ((errors++))
    fi
    
    # Step 2: Stop ngrok
    ((step++))
    print_step ${step} ${total_steps} "Stopping Tunnel..."
    if ! stop_ngrok; then
        ((errors++))
    fi
    
    # Step 3: Stop backend
    ((step++))
    print_step ${step} ${total_steps} "Stopping Backend..."
    if ! stop_backend; then
        ((errors++))
    fi
    
    # Step 4: Cleanup
    ((step++))
    print_step ${step} ${total_steps} "Cleaning up..."
    cleanup_all
    print_success "Cleanup complete"
    
    # Final status
    print_shutdown_complete
    
    if [[ ${errors} -gt 0 ]]; then
        log_message "WARN" "SHUTDOWN" "Shutdown completed with ${errors} warnings"
        return 1
    fi
    
    log_message "INFO" "SHUTDOWN" "System shutdown complete"
    return 0
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
