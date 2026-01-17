#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# Mercury — FRONTEND ONLY LAUNCHER
# ═══════════════════════════════════════════════════════════════════════════════
# Start only the Mercury frontend without the NaSa-Core backend
# 
# ⚠️  NOTE: Mercury can run INDEPENDENTLY but some features require the backend:
#     - Market data from Kite Connect: Works independently
#     - AI chat with Claude: Works independently  
#     - Backend API calls: Requires backend running
#
# Use this for:
#   - Testing Mercury in isolation
#   - When backend is running elsewhere
#   - Frontend development
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "           Mercury — FRONTEND ONLY MODE"
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

echo "🚀 Starting Mercury Frontend on port 8001..."
echo ""
echo "   Chat Interface: http://localhost:8001"
echo "   Health Check:   http://localhost:8001/health"
echo ""
echo "⚠️  Backend status: $(curl -s http://localhost:8000/health >/dev/null 2>&1 && echo "✅ RUNNING" || echo "❌ NOT RUNNING")"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run frontend in foreground (port 8001, no auto-browser)
PYTHONPATH="$PROJECT_ROOT/Mercury/src:$PYTHONPATH" python -m mercury --web --port 8001 --no-browser
