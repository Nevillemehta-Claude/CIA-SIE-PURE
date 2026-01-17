#!/bin/zsh
#===============================================================================
#
#   CIA-SIE SYSTEM STOP
#   ════════════════════
#
#   Double-click this file in Finder to stop the CIA-SIE platform.
#
#   This script will:
#   1. Stop the React frontend (if running)
#   2. Stop the ngrok webhook tunnel (if running)
#   3. Stop the FastAPI backend server
#   4. Clean up any orphan processes
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
source ./scripts/launcher/shutdown.sh

# Run main shutdown sequence
set +e  # Disable strict mode for main (has its own error handling)
main "$@"
exit_code=$?

# Always prompt before closing
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  Press Enter to close this window..."
echo "═══════════════════════════════════════════════════════════════════════════════"
read -r

exit ${exit_code}
