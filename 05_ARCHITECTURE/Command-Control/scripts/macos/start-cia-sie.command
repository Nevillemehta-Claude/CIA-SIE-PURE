#!/bin/zsh
#===============================================================================
#
#   CIA-SIE SYSTEM START
#   ═════════════════════
#
#   Double-click this file in Finder to start the CIA-SIE platform.
#
#   This script will:
#   1. Activate the Python virtual environment
#   2. Start the FastAPI backend server
#   3. Start the ngrok webhook tunnel
#   4. Start the React frontend (if built)
#   5. Open your browser to the application
#
#   To stop the system, use stop-cia-sie.command or press Ctrl+C
#
#===============================================================================

# Enable strict mode
set -e

# Change to script directory (project root)
cd "$(dirname "$0")" || {
    echo "Error: Could not change to project directory"
    exit 1
}

# Store project root
export PROJECT_ROOT="$(pwd)"

# Source launcher scripts
source ./scripts/launcher/config.sh
source ./scripts/launcher/utils.sh
source ./scripts/launcher/health-check.sh
source ./scripts/launcher/ignite.sh

# Run main ignition sequence
set +e  # Disable strict mode for main (has its own error handling)
main "$@"
exit_code=$?

# If there was an error, keep the terminal open
if [[ ${exit_code} -ne 0 ]]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  An error occurred during startup. Review the messages above."
    echo "  Check the log file for details: ${LOG_FILE}"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Press Enter to close this window..."
    read -r
    exit ${exit_code}
fi

# Main function keeps running (for Ctrl+C handling)
# This line is only reached if main exits normally
exit 0
