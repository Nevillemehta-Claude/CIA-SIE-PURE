#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# CIA-SIE ECOSYSTEM — SYSTEM STATUS CHECK
# ═══════════════════════════════════════════════════════════════════════════════
# Check the status of all system components
# ═══════════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "           CIA-SIE ECOSYSTEM — SYSTEM STATUS"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Checking system components..."
echo ""

echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│                          SERVICE STATUS                                     │"
echo "├─────────────────────────────────────────────────────────────────────────────┤"

# Check Backend
echo -n "│  CIA-SIE-Pure Backend (port 8000):  "
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ RUNNING                          │"
else
    if lsof -ti:8000 >/dev/null 2>&1; then
        echo "⚠️  PORT IN USE (not responding)    │"
    else
        echo "❌ NOT RUNNING                      │"
    fi
fi

# Check Frontend
echo -n "│  Mercury Frontend (port 8001):     "
if curl -s http://localhost:8001/health >/dev/null 2>&1; then
    echo "✅ RUNNING                          │"
else
    if lsof -ti:8001 >/dev/null 2>&1; then
        echo "⚠️  PORT IN USE (not responding)    │"
    else
        echo "❌ NOT RUNNING                      │"
    fi
fi

echo "├─────────────────────────────────────────────────────────────────────────────┤"
echo "│                          PROCESS INFO                                       │"
echo "├─────────────────────────────────────────────────────────────────────────────┤"

# Show processes
BACKEND_PIDS=$(pgrep -f "python.*cia_sie" 2>/dev/null)
if [ -n "$BACKEND_PIDS" ]; then
    echo "│  Backend PIDs: $BACKEND_PIDS"
else
    echo "│  Backend PIDs: (none)                                                    │"
fi

FRONTEND_PIDS=$(pgrep -f "python.*mercury" 2>/dev/null)
if [ -n "$FRONTEND_PIDS" ]; then
    echo "│  Frontend PIDs: $FRONTEND_PIDS"
else
    echo "│  Frontend PIDs: (none)                                                   │"
fi

echo "├─────────────────────────────────────────────────────────────────────────────┤"
echo "│                          PORT USAGE                                         │"
echo "├─────────────────────────────────────────────────────────────────────────────┤"

# Port 8000
PORT_8000=$(lsof -i:8000 2>/dev/null | grep LISTEN | head -1)
if [ -n "$PORT_8000" ]; then
    echo "│  Port 8000: IN USE                                                       │"
else
    echo "│  Port 8000: FREE                                                         │"
fi

# Port 8001
PORT_8001=$(lsof -i:8001 2>/dev/null | grep LISTEN | head -1)
if [ -n "$PORT_8001" ]; then
    echo "│  Port 8001: IN USE                                                       │"
else
    echo "│  Port 8001: FREE                                                         │"
fi

echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""

# API Key Status
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│                          CONFIGURATION STATUS                               │"
echo "├─────────────────────────────────────────────────────────────────────────────┤"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "│  .env file: ✅ EXISTS                                                    │"
    
    # Check for API keys (without exposing them)
    if grep -q "ANTHROPIC_API_KEY" "$PROJECT_ROOT/.env" 2>/dev/null; then
        if grep "ANTHROPIC_API_KEY" "$PROJECT_ROOT/.env" | grep -v "^#" | grep -q "sk-"; then
            echo "│  Anthropic API Key: ✅ CONFIGURED                                      │"
        else
            echo "│  Anthropic API Key: ⚠️  NOT SET                                         │"
        fi
    else
        echo "│  Anthropic API Key: ❌ MISSING                                          │"
    fi
    
    if grep -q "KITE_API_KEY" "$PROJECT_ROOT/.env" 2>/dev/null; then
        if grep "KITE_API_KEY" "$PROJECT_ROOT/.env" | grep -v "^#" | grep -qv "=$"; then
            echo "│  Kite API Key: ✅ CONFIGURED                                           │"
        else
            echo "│  Kite API Key: ⚠️  NOT SET                                              │"
        fi
    else
        echo "│  Kite API Key: ❌ MISSING                                               │"
    fi
else
    echo "│  .env file: ❌ MISSING                                                   │"
    echo "│  Please copy .env.example to .env and configure                          │"
fi

echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""
read -p "Press Enter to close..."
