#!/bin/zsh
#===============================================================================
#
#   MERCURY START (macOS)
#   ═════════════════════
#
#   Double-click this file in Finder to start Mercury.
#
#   This will:
#   1. Activate the Python virtual environment
#   2. Verify API connections
#   3. Start the Mercury web interface
#   4. Open your browser
#
#===============================================================================

# Change to script directory
cd "$(dirname "$0")" || exit 1

# Run the launcher script with web mode
./scripts/start_mercury.sh --web

# Keep terminal open on error
if [[ $? -ne 0 ]]; then
    echo ""
    echo "Press Enter to close..."
    read -r
fi
