#!/bin/bash
#===============================================================================
#
#   MERCURY LAUNCHER
#   ═════════════════
#
#   Start Mercury - LLM as Financial Market Cognitive Interface
#
#   Usage:
#       ./scripts/start_mercury.sh          # Terminal mode
#       ./scripts/start_mercury.sh --web    # Web interface
#       ./scripts/start_mercury.sh --check  # System check
#
#===============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
MERCURY_ROOT="${PROJECT_ROOT}"

# Check if we're in the mercury project or parent
if [[ -f "${PROJECT_ROOT}/src/mercury/__init__.py" ]]; then
    MERCURY_ROOT="${PROJECT_ROOT}"
elif [[ -f "${PROJECT_ROOT}/projects/mercury/src/mercury/__init__.py" ]]; then
    MERCURY_ROOT="${PROJECT_ROOT}/projects/mercury"
else
    echo -e "${RED}Error: Cannot find Mercury project${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}║   ☿ MERCURY LAUNCHER                                             ║${NC}"
echo -e "${CYAN}║   LLM as Financial Market Cognitive Interface                    ║${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Find virtual environment
VENV_PATH=""
if [[ -f "${MERCURY_ROOT}/venv/bin/activate" ]]; then
    VENV_PATH="${MERCURY_ROOT}/venv"
elif [[ -f "${MERCURY_ROOT}/../../venv/bin/activate" ]]; then
    VENV_PATH="${MERCURY_ROOT}/../../venv"
fi

if [[ -z "${VENV_PATH}" ]]; then
    echo -e "${RED}Error: Virtual environment not found${NC}"
    echo "Expected: ${MERCURY_ROOT}/venv or parent venv"
    exit 1
fi

echo -e "${GREEN}[1/3]${NC} Activating virtual environment..."
source "${VENV_PATH}/bin/activate"
echo "       Python: $(python --version)"

echo -e "${GREEN}[2/3]${NC} Checking environment..."

# Check for .env file
if [[ -f "${MERCURY_ROOT}/.env" ]]; then
    echo "       .env: Found"
    # Export variables
    set -a
    source "${MERCURY_ROOT}/.env"
    set +a
elif [[ -f "${MERCURY_ROOT}/../../.env" ]]; then
    echo "       .env: Found (parent directory)"
    set -a
    source "${MERCURY_ROOT}/../../.env"
    set +a
else
    echo -e "       .env: ${YELLOW}Not found - using defaults${NC}"
fi

# Check API keys
if [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    echo "       Anthropic API: Configured"
else
    echo -e "       Anthropic API: ${YELLOW}Not configured (mock mode)${NC}"
fi

if [[ -n "${KITE_API_KEY}" ]]; then
    echo "       Kite API: Configured"
else
    echo -e "       Kite API: ${YELLOW}Not configured (mock mode)${NC}"
fi

echo -e "${GREEN}[3/3]${NC} Starting Mercury..."
echo ""

# Change to Mercury directory
cd "${MERCURY_ROOT}"

# Add src to Python path
export PYTHONPATH="${MERCURY_ROOT}/src:${PYTHONPATH}"

# Run Mercury
python -m mercury.main "$@"
