# NaSa → NaSa RENAME EXECUTION PLAN
## 100-Step Autonomous Migration

**Generated:** January 13, 2026
**Scope:** Complete ecosystem rename from NaSa to NaSa
**Estimated Changes:** ~22,000+ text replacements across 321 files

---

## NAMING CONVENTION MAP

| Current | New | Context |
|---------|-----|---------|
| `NaSa` | `NaSa` | Root folder |
| `NaSa-Core` | `NaSa-Core` | Backend folder |
| `nasa` | `nasa` | Python package |
| `NaSa` | `NaSa` | Display name |
| `nasa` | `nasa` | Kebab-case |
| `NASA` | `NASA` | Constants |
| `nasa.db` | `nasa.db` | Database |
| `nasa.log` | `nasa.log` | Log files |
| `Chart Intelligence Assistant - Signal Intelligence Engine` | `NaSa - Narrative Signal Architecture` | Full name |

---

## PHASE 1: PRE-FLIGHT CHECKS (Steps 1-10)

### Step 1: Verify clean state
- Ensure no processes running on ports 8000, 8001
- Kill any lingering Python processes

### Step 2: Create backup manifest
- Generate file list with SHA256 hashes
- Store in `migration-logs/nasa-rename-backup-manifest.md`

### Step 3: Create rollback script
- Generate script to reverse all changes if needed

### Step 4: Verify git status
- Check for uncommitted changes
- Recommend commit before proceeding

### Step 5: Document current state
- Capture directory structure
- Count files by type

### Step 6: Verify disk space
- Ensure sufficient space for operations

### Step 7: Test Python environment
- Verify venv is functional
- Check package imports work

### Step 8: Backup database
- Copy `nasa.db` to `nasa.db.backup`

### Step 9: Backup configuration
- Copy `.env` to `.env.backup`

### Step 10: Create execution log
- Initialize `migration-logs/nasa-rename-execution.log`

---

## PHASE 2: PYTHON PACKAGE RENAME (Steps 11-35)

### Step 11: Update NaSa-Core/src/nasa/__init__.py
- Replace all `nasa` → `nasa`
- Replace all `NaSa` → `NaSa`

### Step 12: Update NaSa-Core/src/nasa/__main__.py
- Replace all imports and references

### Step 13: Update NaSa-Core/src/nasa/main.py
- Replace app name, imports, references

### Step 14: Update NaSa-Core/src/nasa/core/config.py
- Replace app_name default
- Replace database path
- Replace log file path

### Step 15: Update NaSa-Core/src/nasa/core/enums.py
### Step 16: Update NaSa-Core/src/nasa/core/exceptions.py
### Step 17: Update NaSa-Core/src/nasa/core/models.py
### Step 18: Update NaSa-Core/src/nasa/core/security.py
### Step 19: Update NaSa-Core/src/nasa/core/__init__.py

### Step 20: Update NaSa-Core/src/nasa/api/app.py
- Critical: Update uvicorn reference
- Update CORS, logging, app name

### Step 21: Update NaSa-Core/src/nasa/api/__init__.py
### Step 22: Update NaSa-Core/src/nasa/api/routes/__init__.py
### Step 23: Update NaSa-Core/src/nasa/api/routes/ai.py
### Step 24: Update NaSa-Core/src/nasa/api/routes/baskets.py
### Step 25: Update NaSa-Core/src/nasa/api/routes/charts.py
### Step 26: Update NaSa-Core/src/nasa/api/routes/chat.py
### Step 27: Update NaSa-Core/src/nasa/api/routes/instruments.py
### Step 28: Update NaSa-Core/src/nasa/api/routes/narratives.py
### Step 29: Update NaSa-Core/src/nasa/api/routes/platforms.py
### Step 30: Update NaSa-Core/src/nasa/api/routes/relationships.py
### Step 31: Update NaSa-Core/src/nasa/api/routes/signals.py
### Step 32: Update NaSa-Core/src/nasa/api/routes/silos.py
### Step 33: Update NaSa-Core/src/nasa/api/routes/strategy.py
### Step 34: Update NaSa-Core/src/nasa/api/routes/webhooks.py

### Step 35: Update remaining src/nasa modules
- ai/*.py (6 files)
- dal/*.py (4 files)
- exposure/*.py (4 files)
- ingestion/*.py (4 files)
- platforms/*.py (5 files)
- webhooks/*.py (2 files)
- bridge/*.py (1 file)

---

## PHASE 3: CONFIGURATION & DATA FILES (Steps 36-50)

### Step 36: Update NaSa-Core/pyproject.toml
- Replace package name
- Replace all references

### Step 37: Update NaSa-Core/alembic.ini
- Replace database path
- Replace script location

### Step 38: Update NaSa-Core/alembic/env.py
- Replace all imports

### Step 39: Update NaSa-Core/alembic/script.py.mako
### Step 40: Update NaSa-Core/alembic/versions/*.py (2 files)

### Step 41: Update all test files (32 files in tests/unit/)
### Step 42: Update tests/conftest.py
### Step 43: Update tests/constitutional/*.py (3 files)
### Step 44: Update tests/integration/*.py (4 files)
### Step 45: Update tests/backend/*.py
### Step 46: Update tests/e2e/*.py
### Step 47: Update tests/chaos/*.py

### Step 48: Update NaSa-Core/scripts/*.py (8 files)
### Step 49: Rename database file: nasa.db → nasa.db
### Step 50: Rename log files: nasa.log → nasa.log

---

## PHASE 4: SHELL SCRIPTS & LAUNCHERS (Steps 51-65)

### Step 51: Update LAUNCH/0_FIRST_TIME_SETUP.command
### Step 52: Update LAUNCH/1_START_COMPOSITE_SYSTEM.command
### Step 53: Update LAUNCH/2_STOP_COMPOSITE_SYSTEM.command
### Step 54: Update LAUNCH/3_START_BACKEND_ONLY.command
### Step 55: Update LAUNCH/4_START_FRONTEND_ONLY.command
### Step 56: Update LAUNCH/5_SYSTEM_STATUS_CHECK.command
### Step 57: Update LAUNCH/README.md

### Step 58: Update Command-Control/scripts/shell/config.sh
### Step 59: Update Command-Control/scripts/shell/ignite.sh
### Step 60: Update Command-Control/scripts/shell/shutdown.sh
### Step 61: Update Command-Control/scripts/shell/health-check.sh
### Step 62: Update Command-Control/scripts/shell/utils.sh

### Step 63: Update Command-Control/scripts/macos/start-nasa.command
- Also rename file to start-nasa.command

### Step 64: Update Command-Control/scripts/macos/stop-nasa.command
- Also rename file to stop-nasa.command

### Step 65: Update NaSa-Core/docs/LAUNCHER_SYSTEM_COMPLETE/03_IMPLEMENTATION/*.sh and *.command

---

## PHASE 5: DOCUMENTATION UPDATES (Steps 66-85)

### Step 66: Update MASTER-README.md
### Step 67: Update ARCHITECTURE-OVERVIEW.md
### Step 68: Update COMPLETE_ECOSYSTEM_MAP.md
### Step 69: Update MIGRATION-REPORT.md

### Step 70: Update NaSa-Core/docs/01_GOVERNANCE/*.md (5 files)
### Step 71: Update NaSa-Core/docs/02_ARCHITECTURE/*.md (9 files)
### Step 72: Update NaSa-Core/docs/02_ARCHITECTURE/diagrams/*.puml (14 files)
### Step 73: Update NaSa-Core/docs/03_SPECIFICATIONS/*.md (10 files)
### Step 74: Update NaSa-Core/docs/04_AI_HANDOFF/*.md (13 files)
### Step 75: Update NaSa-Core/docs/05_DECISIONS/*.md (3 files)
### Step 76: Update NaSa-Core/docs/06_AUDITS/*.md (14 files)
### Step 77: Update NaSa-Core/docs/07_MISSION_CONTROL/*.md (6 files)
### Step 78: Update NaSa-Core/docs/07_TESTING/*.md (8 files)
### Step 79: Update NaSa-Core/docs/08_OPERATIONS/*.md (5 files)
### Step 80: Update NaSa-Core/docs/AEROSPACE_SYSTEMS_MANUAL/*.md (7 files)
### Step 81: Update NaSa-Core/docs/LAUNCHER_SYSTEM_COMPLETE/**/*.md (10 files)
### Step 82: Update NaSa-Core/docs/prototypes/*.html (15 files)
### Step 83: Update NaSa-Core/docs/USER_MANUAL.md
### Step 84: Update NaSa-Core/docs/QA_KNOWLEDGE_BASE/*.md (7 files)

### Step 85: Update Mercury references
- Mercury/src/mercury/*.py
- Mercury/documentation/*.md
- Mercury/README.md

---

## PHASE 6: FOLDER & FILE RENAMES (Steps 86-95)

### Step 86: Rename Python package directory
- `NaSa-Core/src/nasa` → `NaSa-Core/src/nasa`

### Step 87: Delete egg-info directory
- `NaSa-Core/src/nasa.egg-info` (will regenerate)

### Step 88: Rename database file
- `NaSa-Core/data/nasa.db` → `NaSa-Core/data/nasa.db`

### Step 89: Rename log files
- All `nasa.log` → `nasa.log`

### Step 90: Rename launcher script files
- `start-nasa.command` → `start-nasa.command`
- `stop-nasa.command` → `stop-nasa.command`

### Step 91: Rename documentation files with NaSa in name
- `NaSa_MASTER_SYSTEM_ARCHITECTURE.md` → `NaSa_MASTER_SYSTEM_ARCHITECTURE.md`
- `NASA_COMPLETE_CHAT_CHRONICLE.html` → `NaSa_COMPLETE_CHAT_CHRONICLE.html`

### Step 92: Rename backend folder
- `NaSa-Core` → `NaSa-Core`

### Step 93: Update all paths in scripts after folder rename

### Step 94: Rename root folder (optional - user decision)
- `NaSa` → `NaSa`

### Step 95: Clean up __pycache__ directories

---

## PHASE 7: VERIFICATION & TESTING (Steps 96-100)

### Step 96: Verify Python imports
- Run: `python -c "from nasa.main import main; print('OK')"`
- Verify no import errors

### Step 97: Test backend startup
- Run backend on port 8000
- Verify health endpoint responds
- Check app name in response

### Step 98: Test frontend startup
- Run Mercury on port 8001
- Verify health endpoint responds

### Step 99: Generate verification report
- Hash all modified files
- Compare with pre-migration hashes
- Document all changes

### Step 100: Create completion audit
- Generate `migration-logs/nasa-rename-completion-audit.md`
- Document success/failure of each step
- Provide rollback instructions if needed

---

## EXCLUDED FROM AUTOMATIC RENAME (Preserved for Audit Trail)

The following are **intentionally excluded** to preserve historical accuracy:

1. `NaSa-Core/docs/chat_history_export/*.md` (33 files)
2. `NaSa-Core/docs/chat_history_export/*.json` (2 files)
3. `NaSa-Core/docs/chat_history_export/*.html` (2 files)
4. `migration-logs/*.md` (11 files) - Historical migration records
5. `quarantine/*` - Archived items

---

## EXECUTION COMMAND

To execute this plan autonomously, run:
```bash
# The plan will be executed step-by-step with verification at each phase
```

---

## ROLLBACK PROCEDURE

If issues occur:
1. Restore from backup manifest
2. Run `git checkout .` if changes were staged
3. Restore database backup: `cp nasa.db.backup nasa.db`
4. Restore config backup: `cp .env.backup .env`

---

*Generated by Cursor AI Agent | January 13, 2026*
*Methodology: Aerospace-Grade Precision [[memory:12958409]]*
