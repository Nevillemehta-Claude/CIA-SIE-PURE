#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# CIA-SIE ECOSYSTEM — FIRST TIME SETUP
# ═══════════════════════════════════════════════════════════════════════════════
# Run this ONCE before using the system for the first time
# This will:
#   1. Create/verify virtual environment
#   2. Install all dependencies
#   3. Verify configuration
#   4. Run system check
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "           CIA-SIE ECOSYSTEM — FIRST TIME SETUP"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo ""

cd "$PROJECT_ROOT"

# Step 1: Virtual Environment
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 1: Virtual Environment"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ -d "venv" ]; then
    echo "✅ Virtual environment already exists"
    source venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created"
        source venv/bin/activate
    else
        echo "❌ Failed to create virtual environment"
        echo "   Please ensure Python 3.8+ is installed"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 2: Install Dependencies"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo ""
echo "📦 Installing CIA-SIE-Pure dependencies..."
pip install -e "$PROJECT_ROOT/CIA-SIE-Pure"

echo ""
echo "📦 Installing Mercury dependencies..."
pip install -r "$PROJECT_ROOT/Mercury/requirements.txt"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 3: Configuration Check"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    if [ -f ".env.example" ]; then
        echo "⚠️  .env file not found, copying from .env.example..."
        cp .env.example .env
        echo "✅ Created .env from template"
        echo ""
        echo "⚠️  IMPORTANT: You need to configure your API keys in .env:"
        echo "   - ANTHROPIC_API_KEY: Your Anthropic/Claude API key"
        echo "   - KITE_API_KEY: Your Kite Connect API key (optional)"
        echo "   - KITE_API_SECRET: Your Kite Connect API secret (optional)"
    else
        echo "❌ No .env or .env.example found"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 4: Database Check"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ -f "CIA-SIE-Pure/data/cia_sie.db" ]; then
    echo "✅ Database exists: CIA-SIE-Pure/data/cia_sie.db"
    DB_SIZE=$(ls -lh "CIA-SIE-Pure/data/cia_sie.db" | awk '{print $5}')
    echo "   Size: $DB_SIZE"
else
    echo "⚠️  Database not found. It will be created on first run."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    STEP 5: Verify Installation"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

echo "Checking Python packages..."
echo ""

# Check critical packages
python -c "import fastapi; print('✅ FastAPI: ' + fastapi.__version__)" 2>/dev/null || echo "❌ FastAPI not installed"
python -c "import uvicorn; print('✅ Uvicorn installed')" 2>/dev/null || echo "❌ Uvicorn not installed"
python -c "import sqlalchemy; print('✅ SQLAlchemy: ' + sqlalchemy.__version__)" 2>/dev/null || echo "❌ SQLAlchemy not installed"
python -c "import anthropic; print('✅ Anthropic SDK installed')" 2>/dev/null || echo "⚠️  Anthropic SDK not installed (AI features may not work)"
python -c "import pydantic; print('✅ Pydantic: ' + pydantic.__version__)" 2>/dev/null || echo "❌ Pydantic not installed"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                    ✅ SETUP COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "  Next steps:"
echo ""
echo "  1. Configure your API keys in .env file (if not done)"
echo ""
echo "  2. Start the system:"
echo "     → Double-click: LAUNCH/1_START_COMPOSITE_SYSTEM.command"
echo ""
echo "  3. Access the system:"
echo "     → Backend API: http://localhost:8000"
echo "     → Frontend:    http://localhost:8001"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
read -p "Press Enter to close..."
