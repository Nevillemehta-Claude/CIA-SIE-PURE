#!/bin/zsh
#===============================================================================
#
#   CIA-SIE LAUNCHER HEALTH CHECK
#   ═══════════════════════════════
#
#   Document ID: IMPL-LAUNCHER-HEALTH
#   Version: 1.0.0
#   Date: 12 January 2026
#
#   Purpose: Health verification functions for backend and services
#
#   Usage: This file is sourced by ignite.sh
#          source ./scripts/launcher/health-check.sh
#
#   Dependencies: config.sh and utils.sh must be sourced first
#
#===============================================================================

#-------------------------------------------------------------------------------
# check_backend_health - Single health check attempt
#
# Returns:
#   0 if healthy (HTTP 200), 1 otherwise
#-------------------------------------------------------------------------------
check_backend_health() {
    local status_code
    
    # Get HTTP status code with timeout
    status_code=$(curl -s -o /dev/null -w "%{http_code}" \
        --connect-timeout 5 \
        --max-time 10 \
        "${HEALTH_ENDPOINT}" 2>/dev/null)
    
    if [[ "${status_code}" == "200" ]]; then
        return 0
    fi
    
    return 1
}

#-------------------------------------------------------------------------------
# wait_for_backend - Wait for backend to become healthy
#
# Uses configuration:
#   HEALTH_CHECK_RETRIES - Maximum number of attempts
#   HEALTH_CHECK_INTERVAL - Seconds between attempts
#
# Returns:
#   0 if backend becomes healthy, 1 if timeout
#-------------------------------------------------------------------------------
wait_for_backend() {
    local attempt=0
    local max_attempts="${HEALTH_CHECK_RETRIES}"
    local interval="${HEALTH_CHECK_INTERVAL}"
    local start_time
    local elapsed
    
    start_time=$(date +%s)
    
    log_message "INFO" "HEALTH" "Waiting for backend health (max ${max_attempts} attempts, ${interval}s interval)"
    
    while [[ ${attempt} -lt ${max_attempts} ]]; do
        ((attempt++))
        
        if check_backend_health; then
            elapsed=$(($(date +%s) - start_time))
            log_message "INFO" "HEALTH" "Backend healthy after ${elapsed}s (attempt ${attempt})"
            return 0
        fi
        
        log_message "DEBUG" "HEALTH" "Attempt ${attempt}/${max_attempts}: not ready"
        
        # Show progress to user
        if [[ $((attempt % 3)) -eq 0 ]]; then
            echo -e "         ├── Waiting for backend... (attempt ${attempt}/${max_attempts})"
        fi
        
        sleep "${interval}"
    done
    
    elapsed=$(($(date +%s) - start_time))
    log_message "ERROR" "HEALTH" "Backend failed to become healthy after ${elapsed}s"
    return 1
}

#-------------------------------------------------------------------------------
# get_backend_health_details - Get detailed health information
#
# Output:
#   JSON response from health endpoint or error message
#-------------------------------------------------------------------------------
get_backend_health_details() {
    local response
    
    response=$(curl -s --connect-timeout 5 --max-time 10 "${HEALTH_ENDPOINT}" 2>/dev/null)
    
    if [[ -n "${response}" ]]; then
        echo "${response}"
    else
        echo '{"status": "unreachable"}'
    fi
}

#-------------------------------------------------------------------------------
# check_service_health - Generic service health check
#
# Arguments:
#   $1 - Service name
#   $2 - Health check command
#
# Returns:
#   0 if healthy, 1 otherwise
#-------------------------------------------------------------------------------
check_service_health() {
    local name="$1"
    local check_cmd="$2"
    
    log_message "DEBUG" "HEALTH" "Checking ${name} health"
    
    if eval "${check_cmd}"; then
        log_message "INFO" "HEALTH" "${name} is healthy"
        return 0
    else
        log_message "WARN" "HEALTH" "${name} health check failed"
        return 1
    fi
}

#-------------------------------------------------------------------------------
# verify_all_services - Check health of all running services
#
# Returns:
#   0 if all healthy, 1 if any unhealthy
#-------------------------------------------------------------------------------
verify_all_services() {
    local all_healthy=0
    
    echo ""
    echo "Service Health Check"
    echo "═══════════════════"
    echo ""
    
    # Check backend
    if is_process_running "$(get_pid "backend")"; then
        if check_backend_health; then
            echo "  Backend:  ✓ Healthy"
        else
            echo "  Backend:  ✗ Unhealthy"
            all_healthy=1
        fi
    else
        echo "  Backend:  ○ Not running"
    fi
    
    # Check ngrok
    if is_process_running "$(get_pid "ngrok")"; then
        if [[ -n "${NGROK_PUBLIC_URL}" ]]; then
            echo "  ngrok:    ✓ Healthy (${NGROK_PUBLIC_URL})"
        else
            echo "  ngrok:    ○ Running (no URL)"
        fi
    else
        echo "  ngrok:    ○ Not running"
    fi
    
    # Check frontend
    if is_process_running "$(get_pid "frontend")"; then
        if wait_for_port "${FRONTEND_PORT}" 1; then
            echo "  Frontend: ✓ Healthy"
        else
            echo "  Frontend: ✗ Unhealthy"
            all_healthy=1
        fi
    else
        echo "  Frontend: ○ Not running"
    fi
    
    echo ""
    
    return ${all_healthy}
}
