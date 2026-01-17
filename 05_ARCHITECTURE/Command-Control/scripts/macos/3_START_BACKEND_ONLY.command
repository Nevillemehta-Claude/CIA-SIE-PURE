#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# NaSa-Core — BACKEND ONLY LAUNCHER
# ═══════════════════════════════════════════════════════════════════════════════
# Start only the backend API without the Mercury frontend
# Use this for:
#   - API development/testing
#   - Backend-only operations
#   - When you want to use a different frontend
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "           NaSa-Core — BACKEND ONLY MODE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "🚀 Starting NaSa-Core Backend on port 8000..."
echo ""
echo "   API Docs:  http://localhost:8000/docs"
echo "   Health:    http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Change to NaSa-Core directory (required for relative database path)
cd "$PROJECT_ROOT/NaSa-Core"

# Run backend in foreground
PYTHONPATH="$PROJECT_ROOT/NaSa-Core/src:$PYTHONPATH" python -m nasa
