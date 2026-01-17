#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# NaSa ECOSYSTEM — COMPOSITE SYSTEM LAUNCHER
# ═══════════════════════════════════════════════════════════════════════════════
# Double-click this file to start the COMPLETE system:
#   1. NaSa-Core Backend (port 8000)
#   2. Mercury Frontend (port 8001)
# ═══════════════════════════════════════════════════════════════════════════════

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "           NaSa ECOSYSTEM — COMPOSITE SYSTEM STARTUP"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please create it first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r NaSa-Core/pyproject.toml"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. System may not function correctly."
    echo "   Please copy .env.example to .env and configure API keys."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 1: Starting NaSa-Core Backend"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Start backend in background (from NaSa-Core directory for database path)
cd "$PROJECT_ROOT/NaSa-Core"
PYTHONPATH="$PROJECT_ROOT/NaSa-Core/src:$PYTHONPATH" python -m nasa &
BACKEND_PID=$!
echo "✅ Backend starting... (PID: $BACKEND_PID)"

# Wait for backend to be ready
echo "⏳ Waiting for backend to initialize (port 8000)..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is READY on http://localhost:8000"
else
    echo "⚠️  Backend health check pending... continuing anyway"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 2: Starting Mercury Frontend"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Start Mercury in background (port 8001, no auto-browser)
cd "$PROJECT_ROOT"
PYTHONPATH="$PROJECT_ROOT/Mercury/src:$PYTHONPATH" python -m mercury --web --port 8001 --no-browser &
FRONTEND_PID=$!
echo "✅ Frontend starting... (PID: $FRONTEND_PID)"

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to initialize (port 8001)..."
sleep 5

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    🚀 SYSTEM READY"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "  📊 Backend API:    http://localhost:8000"
echo "  💬 Frontend Chat:  http://localhost:8001"
echo ""
echo "  Backend PID:  $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "  To stop the system, use: LAUNCH/2_STOP_COMPOSITE_SYSTEM.command"
echo "  Or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Press Ctrl+C or close this terminal to stop monitoring."
echo "(The services will continue running in background)"
echo ""

# Keep terminal open and show logs
wait
