#!/bin/zsh
#===============================================================================
#
#   CIA-SIE LAUNCHER CONFIGURATION
#   ═══════════════════════════════
#
#   Document ID: IMPL-LAUNCHER-CONFIG
#   Version: 1.0.0
#   Date: 12 January 2026
#
#   Purpose: Centralized configuration with sensible defaults and 
#            environment variable overrides
#
#   Usage: This file is sourced by other launcher scripts
#          source ./scripts/launcher/config.sh
#
#===============================================================================

#-------------------------------------------------------------------------------
# PATH CONFIGURATION
#-------------------------------------------------------------------------------

# Project root (auto-detected or override with CIA_SIE_ROOT)
# When sourced from .command files, this resolves to project root
if [[ -z "${PROJECT_ROOT:-}" ]]; then
    if [[ -n "${CIA_SIE_ROOT:-}" ]]; then
        export PROJECT_ROOT="${CIA_SIE_ROOT}"
    else
        # Auto-detect: go up from scripts/launcher to project root
        export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-${0}}")/../.." 2>/dev/null && pwd)"
    fi
fi

# Derived paths
export VENV_PATH="${PROJECT_ROOT}/venv"
export BACKEND_PATH="${PROJECT_ROOT}/src"
export FRONTEND_PATH="${PROJECT_ROOT}/frontend"
export LOGS_PATH="${PROJECT_ROOT}/logs"
export PIDS_PATH="${PROJECT_ROOT}/pids"
export SCRIPTS_PATH="${PROJECT_ROOT}/scripts/launcher"
export DATA_PATH="${PROJECT_ROOT}/data"

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

# Set to "false" to disable
export OPEN_BROWSER="${CIA_SIE_OPEN_BROWSER:-true}"
export START_NGROK="${CIA_SIE_START_NGROK:-true}"
export START_FRONTEND="${CIA_SIE_START_FRONTEND:-true}"
export VERBOSE="${CIA_SIE_VERBOSE:-false}"

#-------------------------------------------------------------------------------
# PROCESS IDENTIFICATION PATTERNS
#-------------------------------------------------------------------------------

export BACKEND_PATTERN="uvicorn.*cia_sie.api.app"
export NGROK_PATTERN="ngrok http"
export FRONTEND_PATTERN="vite.*${FRONTEND_PORT}"

#-------------------------------------------------------------------------------
# LOG CONFIGURATION
#-------------------------------------------------------------------------------

export LOG_FILE="${LOGS_PATH}/launcher.log"
export BACKEND_LOG_FILE="${LOGS_PATH}/backend.log"
export NGROK_LOG_FILE="${LOGS_PATH}/ngrok.log"
export FRONTEND_LOG_FILE="${LOGS_PATH}/frontend.log"
export LOG_DATE_FORMAT="+%Y-%m-%dT%H:%M:%S%z"

#-------------------------------------------------------------------------------
# DISPLAY CONFIGURATION - Colors (ANSI escape codes)
#-------------------------------------------------------------------------------

export COLOR_RESET="\033[0m"
export COLOR_RED="\033[0;31m"
export COLOR_GREEN="\033[0;32m"
export COLOR_YELLOW="\033[0;33m"
export COLOR_BLUE="\033[0;34m"
export COLOR_MAGENTA="\033[0;35m"
export COLOR_CYAN="\033[0;36m"
export COLOR_WHITE="\033[0;37m"
export COLOR_BOLD="\033[1m"

#-------------------------------------------------------------------------------
# DISPLAY CONFIGURATION - Symbols
#-------------------------------------------------------------------------------

export SYMBOL_SUCCESS="✓"
export SYMBOL_FAILURE="✗"
export SYMBOL_WARNING="⚠"
export SYMBOL_INFO="ℹ"
export SYMBOL_PENDING="○"
export SYMBOL_RUNNING="●"

#-------------------------------------------------------------------------------
# GLOBAL STATE (set during runtime)
#-------------------------------------------------------------------------------

# Will be populated by ignite.sh if ngrok starts successfully
export NGROK_PUBLIC_URL=""

# Note: This file is meant to be sourced, not executed directly.
# When sourced, it sets environment variables silently.
