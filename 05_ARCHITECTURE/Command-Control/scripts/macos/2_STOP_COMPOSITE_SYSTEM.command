#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# CIA-SIE ECOSYSTEM — COMPOSITE SYSTEM SHUTDOWN
# ═══════════════════════════════════════════════════════════════════════════════
# Double-click this file to STOP all running services
# ═══════════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "           CIA-SIE ECOSYSTEM — GRACEFUL SHUTDOWN"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Find and kill backend processes
echo "🔍 Finding CIA-SIE-Pure backend processes..."
BACKEND_PIDS=$(pgrep -f "python.*cia_sie" 2>/dev/null)
if [ -n "$BACKEND_PIDS" ]; then
    echo "   Found backend PIDs: $BACKEND_PIDS"
    kill $BACKEND_PIDS 2>/dev/null
    echo "✅ Backend shutdown signal sent"
else
    echo "   No backend processes found"
fi

# Find and kill frontend processes
echo ""
echo "🔍 Finding Mercury frontend processes..."
FRONTEND_PIDS=$(pgrep -f "python.*mercury" 2>/dev/null)
if [ -n "$FRONTEND_PIDS" ]; then
    echo "   Found frontend PIDs: $FRONTEND_PIDS"
    kill $FRONTEND_PIDS 2>/dev/null
    echo "✅ Frontend shutdown signal sent"
else
    echo "   No frontend processes found"
fi

# Find and kill uvicorn processes on our ports
echo ""
echo "🔍 Finding uvicorn processes on ports 8000/8001..."
UVICORN_PIDS=$(lsof -ti:8000,8001 2>/dev/null)
if [ -n "$UVICORN_PIDS" ]; then
    echo "   Found uvicorn PIDs: $UVICORN_PIDS"
    kill $UVICORN_PIDS 2>/dev/null
    echo "✅ Uvicorn processes stopped"
else
    echo "   No uvicorn processes found on these ports"
fi

# Wait a moment for graceful shutdown
sleep 2

# Force kill if still running
echo ""
echo "🔍 Verifying shutdown..."
REMAINING=$(lsof -ti:8000,8001 2>/dev/null)
if [ -n "$REMAINING" ]; then
    echo "⚠️  Force killing remaining processes..."
    kill -9 $REMAINING 2>/dev/null
    echo "✅ Force killed"
else
    echo "✅ All processes stopped cleanly"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    🛑 SYSTEM STOPPED"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "  Port 8000: $(lsof -ti:8000 >/dev/null 2>&1 && echo "⚠️ STILL IN USE" || echo "✅ FREE")"
echo "  Port 8001: $(lsof -ti:8001 >/dev/null 2>&1 && echo "⚠️ STILL IN USE" || echo "✅ FREE")"
echo ""
read -p "Press Enter to close..."
