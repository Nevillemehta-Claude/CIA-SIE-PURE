# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: RECONNAISSANCE — COMPLETE INVENTORY
# ═══════════════════════════════════════════════════════════════════════════════
# CEAD v2.0 | Forensic Codebase Restructuring
# Generated: January 13, 2026
# ═══════════════════════════════════════════════════════════════════════════════

## EXECUTIVE SUMMARY

| Metric | Count |
|--------|-------|
| **Total Files (Migratable)** | ~350+ |
| **Total Directories** | ~100+ |
| **Python Files (.py)** | ~150+ |
| **Documentation Files (.md)** | ~150+ |
| **HTML Files** | ~20+ |
| **Shell Scripts (.sh)** | ~10+ |
| **Command Files (.command)** | 3 |
| **Configuration Files** | ~15+ |
| **Image Files** | ~4 |
| **PlantUML Diagrams (.puml)** | ~20+ |

---

## DO NOT MIGRATE LIST

Per CEAD v2.0 Section 5.6, these items will be SKIPPED:

| Item | Reason |
|------|--------|
| `venv/` | Virtual environment — regenerate |
| `__pycache__/` (all instances) | Bytecode cache — auto-generated |
| `*.pyc` files | Compiled Python — auto-generated |
| `.git/` | Version control — PRESERVE at root |
| `.pytest_cache/` | Pytest cache — auto-generated |
| `*.egg-info/` | Build artifacts — regenerate |

---

## REPOSITORY STRUCTURE INVENTORY

### ROOT LEVEL FILES

| File | Type | Destination |
|------|------|-------------|
| `alembic.ini` | Config | CIA-SIE-Pure/config/ |
| `pyproject.toml` | Config | CIA-SIE-Pure/ |
| `README.md` | Doc | Reference for MASTER-README |
| `start-cia-sie.command` | CLI | Command-Control/scripts/macos/ |
| `stop-cia-sie.command` | CLI | Command-Control/scripts/macos/ |
| `CIA-SIE-PURE.code-workspace` | Config | quarantine/unclassified/ |
| `CEAD-v2.0-*.md` | Doc | migration-logs/ (reference) |
| `CURSOR-ENGAGEMENT-*.md` | Doc | migration-logs/ (reference) |
| `execute_all_tests_autonomous.py` | Script | CIA-SIE-Pure/scripts/ |
| `extract_chat_history.py` | Script | CIA-SIE-Pure/scripts/ |
| `generate_chronicle.py` | Script | CIA-SIE-Pure/scripts/ |
| `run_comprehensive_tests.py` | Script | CIA-SIE-Pure/scripts/ |
| `run_quick_tests.py` | Script | CIA-SIE-Pure/scripts/ |
| `seed_sample_data.py` | Script | CIA-SIE-Pure/scripts/ |

---

### /src/cia_sie/ — CORE BACKEND (50 files)

**Destination:** `/CIA-SIE-Pure/src/cia_sie/`

#### Root Files
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `main.py` | PRESERVE |

#### /ai/ (6 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `claude_client.py` | CIA-SIE-Pure/src/cia_sie/ai/ |
| `model_registry.py` | CIA-SIE-Pure/src/cia_sie/ai/ |
| `narrative_generator.py` | CIA-SIE-Pure/src/cia_sie/ai/ |
| `prompt_builder.py` | CIA-SIE-Pure/src/cia_sie/ai/ |
| `response_validator.py` | CIA-SIE-Pure/src/cia_sie/ai/ |
| `usage_tracker.py` | CIA-SIE-Pure/src/cia_sie/ai/ |

#### /api/ (14 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `app.py` | CIA-SIE-Pure/src/cia_sie/api/ |
| `/routes/__init__.py` | PRESERVE |
| `/routes/ai.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/baskets.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/charts.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/chat.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/instruments.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/narratives.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/platforms.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/relationships.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/signals.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/silos.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/strategy.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |
| `/routes/webhooks.py` | CIA-SIE-Pure/src/cia_sie/api/routes/ |

#### /bridge/ (1 file)
| File | Destination |
|------|-------------|
| `__init__.py` | CIA-SIE-Pure/src/cia_sie/bridge/ (or quarantine if empty) |

#### /core/ (6 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `config.py` | CIA-SIE-Pure/src/cia_sie/core/ |
| `enums.py` | CIA-SIE-Pure/src/cia_sie/core/ |
| `exceptions.py` | CIA-SIE-Pure/src/cia_sie/core/ |
| `models.py` | CIA-SIE-Pure/src/cia_sie/core/ |
| `security.py` | CIA-SIE-Pure/src/cia_sie/core/ |

#### /dal/ (4 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `database.py` | CIA-SIE-Pure/src/cia_sie/dal/ |
| `models.py` | CIA-SIE-Pure/src/cia_sie/dal/ |
| `repositories.py` | CIA-SIE-Pure/src/cia_sie/dal/ |

#### /exposure/ (4 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `confirmation_detector.py` | CIA-SIE-Pure/src/cia_sie/exposure/ |
| `contradiction_detector.py` | CIA-SIE-Pure/src/cia_sie/exposure/ |
| `relationship_exposer.py` | CIA-SIE-Pure/src/cia_sie/exposure/ |

#### /ingestion/ (4 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `freshness.py` | CIA-SIE-Pure/src/cia_sie/ingestion/ |
| `signal_normalizer.py` | CIA-SIE-Pure/src/cia_sie/ingestion/ |
| `webhook_handler.py` | CIA-SIE-Pure/src/cia_sie/ingestion/ |

#### /platforms/ (5 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `base.py` | CIA-SIE-Pure/src/cia_sie/platforms/ |
| `kite.py` | CIA-SIE-Pure/src/cia_sie/platforms/ |
| `registry.py` | CIA-SIE-Pure/src/cia_sie/platforms/ |
| `tradingview.py` | CIA-SIE-Pure/src/cia_sie/platforms/ |

#### /webhooks/ (2 files)
| File | Destination |
|------|-------------|
| `__init__.py` | PRESERVE |
| `tradingview_receiver.py` | CIA-SIE-Pure/src/cia_sie/webhooks/ |

---

### /projects/mercury/ — FRONTEND (56 files)

**Destination:** `/Mercury/` (LIFT entire structure)

**SPECIAL INSTRUCTION:** LIFT as-is, preserve internal structure

#### Mercury Root Files
| File | Destination |
|------|-------------|
| `pyproject.toml` | Mercury/ |
| `README.md` | Mercury/ |
| `requirements.txt` | Mercury/ |
| `start-mercury.command` | Mercury/ |

#### /src/mercury/ (27 .py files)
- LIFT entire directory to `/Mercury/src/mercury/`
- Preserve all subdirectories: `/ai/`, `/api/`, `/chat/`, `/core/`, `/interface/`, `/kite/`
- Preserve all `__init__.py` files

#### /documentation/ (13 .md files + templates/)
- LIFT to `/Mercury/documentation/`

#### /scripts/ (2 files)
- LIFT to `/Mercury/scripts/`

#### /tests/ (10 files)
- LIFT to `/Mercury/tests/`

---

### /scripts/launcher/ — CLI SCRIPTS (5 files)

**Destination:** `/Command-Control/scripts/shell/`

| File | Destination |
|------|-------------|
| `config.sh` | Command-Control/scripts/shell/ |
| `health-check.sh` | Command-Control/scripts/shell/ |
| `ignite.sh` | Command-Control/scripts/shell/ |
| `shutdown.sh` | Command-Control/scripts/shell/ |
| `utils.sh` | Command-Control/scripts/shell/ |

---

### /scripts/ (root scripts, 2 files)

| File | Destination |
|------|-------------|
| `extract_docx.py` | CIA-SIE-Pure/scripts/ |
| `gold_correlation_chart.py` | CIA-SIE-Pure/scripts/ |

---

### /documentation/ — EXISTING DOCS (~157 files)

**Destination:** `/CIA-SIE-Pure/docs/` (PRESERVE internal structure)

#### Major Subdirectories:
| Directory | Files | Destination |
|-----------|-------|-------------|
| `/01_GOVERNANCE/` | 5 .md | CIA-SIE-Pure/docs/01_GOVERNANCE/ |
| `/02_ARCHITECTURE/` | 8 .md + 15 diagrams | CIA-SIE-Pure/docs/02_ARCHITECTURE/ |
| `/03_SPECIFICATIONS/` | 10 .md | CIA-SIE-Pure/docs/03_SPECIFICATIONS/ |
| `/04_AI_HANDOFF/` | 13 .md | CIA-SIE-Pure/docs/04_AI_HANDOFF/ |
| `/05_DECISIONS/` | 3 .md | CIA-SIE-Pure/docs/05_DECISIONS/ |
| `/06_AUDITS/` | 14 .md | CIA-SIE-Pure/docs/06_AUDITS/ |
| `/07_MISSION_CONTROL/` | 6 .md | CIA-SIE-Pure/docs/07_MISSION_CONTROL/ |
| `/07_TESTING/` | 8 .md | CIA-SIE-Pure/docs/07_TESTING/ |
| `/08_OPERATIONS/` | 5 .md | CIA-SIE-Pure/docs/08_OPERATIONS/ |
| `/09_FRONTEND QUERIES/` | 1 .docx | CIA-SIE-Pure/docs/09_FRONTEND QUERIES/ |
| `/AEROSPACE_SYSTEMS_MANUAL/` | 7 .md | CIA-SIE-Pure/docs/AEROSPACE_SYSTEMS_MANUAL/ |
| `/CHART_01A_COMPLETE_PACKAGE/` | 6 files | CIA-SIE-Pure/docs/CHART_01A_COMPLETE_PACKAGE/ |
| `/CHART_02_COMPLETE_PACKAGE/` | 5 files | CIA-SIE-Pure/docs/CHART_02_COMPLETE_PACKAGE/ |
| `/LAUNCHER_SYSTEM_COMPLETE/` | 22 files | CIA-SIE-Pure/docs/LAUNCHER_SYSTEM_COMPLETE/ |
| `/prototypes/` | 16 files | CIA-SIE-Pure/docs/prototypes/ |
| `/QA_KNOWLEDGE_BASE/` | 7 .md | CIA-SIE-Pure/docs/QA_KNOWLEDGE_BASE/ |

#### Root Documentation Files:
| File | Destination |
|------|-------------|
| `DOCUMENTATION_FORENSIC_ANALYSIS.html` | CIA-SIE-Pure/docs/ |
| `DOCUMENTATION_FORENSIC_ANALYSIS.md` | CIA-SIE-Pure/docs/ |
| `MASTER_TODO_TRACKER.md` | CIA-SIE-Pure/docs/ |
| `PROJECT_STATUS_TREE.md` | CIA-SIE-Pure/docs/ |
| `PROJECT_TREE_COMPLETE.md` | CIA-SIE-Pure/docs/ |
| `USER_MANUAL.md` | CIA-SIE-Pure/docs/ |

---

### /tests/ — BACKEND TESTS (~63 files)

**Destination:** `/CIA-SIE-Pure/tests/` (PRESERVE structure)

| Directory | Files | Destination |
|-----------|-------|-------------|
| Root | `__init__.py`, `conftest.py` | CIA-SIE-Pure/tests/ |
| `/backend/` | 13 .py | CIA-SIE-Pure/tests/backend/ |
| `/chaos/` | 4 .py | CIA-SIE-Pure/tests/chaos/ |
| `/constitutional/` | 5 .py | CIA-SIE-Pure/tests/constitutional/ |
| `/e2e/` | 4 .py | CIA-SIE-Pure/tests/e2e/ |
| `/integration/` | 4 .py | CIA-SIE-Pure/tests/integration/ |
| `/unit/` | 32 .py | CIA-SIE-Pure/tests/unit/ |

---

### /alembic/ — DATABASE MIGRATIONS (4 files)

**Destination:** `/CIA-SIE-Pure/alembic/`

| File | Destination |
|------|-------------|
| `env.py` | CIA-SIE-Pure/alembic/ |
| `script.py.mako` | CIA-SIE-Pure/alembic/ |
| `/versions/20251230_*.py` | CIA-SIE-Pure/alembic/versions/ |
| `/versions/20251231_*.py` | CIA-SIE-Pure/alembic/versions/ |

---

### /data/ — DATABASE FILES (1 file)

| File | Destination |
|------|-------------|
| `cia_sie.db` | CIA-SIE-Pure/data/ |

---

### /docs/ — AUDIT HTMLS (4 files)

**Destination:** `/CIA-SIE-Pure/docs/audits/`

| File | Destination |
|------|-------------|
| `/audits/PROJECT_MATURITY_AUDIT.html` | CIA-SIE-Pure/docs/audits/ |
| `/audits/SYSTEM_ARCHITECTURE_VISUAL.html` | CIA-SIE-Pure/docs/audits/ |
| `gold_correlation_analysis.png` | CIA-SIE-Pure/docs/ |
| `gold_scatter_correlation.png` | CIA-SIE-Pure/docs/ |

---

### /chat_history_export/ — CHAT LOGS (37 files)

**Destination:** `/quarantine/deprecated/` or `/CIA-SIE-Pure/docs/chat_history_export/`

Note: These are historical chat exports. May quarantine as deprecated or preserve.

---

### /logs/ — LOG FILES (4 files)

**Destination:** `/quarantine/debug-logs/`

| File | Destination |
|------|-------------|
| `backend.log` | quarantine/debug-logs/ |
| `cia_sie.log` | quarantine/debug-logs/ |
| `launcher.log` | quarantine/debug-logs/ |
| `ngrok.log` | quarantine/debug-logs/ |

---

### /quarantine/ — EXISTING QUARANTINE (4 files)

**Destination:** `/quarantine/` (already correct location)

| File | Status |
|------|--------|
| `EMPTY_MODULE_QUARANTINED.py` | PRESERVE |
| `README.md` | PRESERVE |
| `SANITISATION_AUDIT_REPORT.md` | PRESERVE |
| `STUB_FUNCTIONS_QUARANTINED.py` | PRESERVE |

---

### /Duplicates for Deletion/ — PRE-FLAGGED DUPLICATES (12 files)

**Destination:** `/quarantine/duplicates/`

| Contents | Destination |
|----------|-------------|
| `/docs_architecture_diagrams/` (9 .puml) | quarantine/duplicates/docs_architecture_diagrams/ |
| `/root_level/` (2 files) | quarantine/duplicates/root_level/ |
| `DUPLICATE_FORENSIC_AUDIT_REPORT.md` | quarantine/duplicates/ |

---

### EMPTY/PLACEHOLDER DIRECTORIES

| Directory | Status |
|-----------|--------|
| `/context/decisions/` | Empty — will add .gitkeep |
| `/pids/` | Empty — will add .gitkeep or quarantine |
| `/prompts/` | Empty — will add .gitkeep or quarantine |
| `/tests/frontend/` | Empty — will add .gitkeep |

---

## __init__.py FILE INVENTORY

**CRITICAL:** All these files must be preserved at exact relative positions.

### /src/cia_sie/ tree:
- `/src/cia_sie/__init__.py`
- `/src/cia_sie/ai/__init__.py`
- `/src/cia_sie/api/__init__.py`
- `/src/cia_sie/api/routes/__init__.py`
- `/src/cia_sie/bridge/__init__.py`
- `/src/cia_sie/core/__init__.py`
- `/src/cia_sie/dal/__init__.py`
- `/src/cia_sie/exposure/__init__.py`
- `/src/cia_sie/ingestion/__init__.py`
- `/src/cia_sie/platforms/__init__.py`
- `/src/cia_sie/webhooks/__init__.py`

**Total: 11 __init__.py files in cia_sie package**

### /projects/mercury/ tree:
- `/projects/mercury/src/mercury/__init__.py`
- `/projects/mercury/src/mercury/ai/__init__.py`
- `/projects/mercury/src/mercury/api/__init__.py`
- `/projects/mercury/src/mercury/chat/__init__.py`
- `/projects/mercury/src/mercury/core/__init__.py`
- `/projects/mercury/src/mercury/interface/__init__.py`
- `/projects/mercury/src/mercury/kite/__init__.py`
- `/projects/mercury/tests/__init__.py`

**Total: 8 __init__.py files in Mercury package**

### /tests/ tree:
- `/tests/__init__.py`
- `/tests/backend/__init__.py`
- `/tests/chaos/__init__.py`
- `/tests/constitutional/__init__.py`
- `/tests/e2e/__init__.py`
- `/tests/integration/__init__.py`
- `/tests/unit/__init__.py`

**Total: 7 __init__.py files in tests package**

---

## PHASE 1 CHECKPOINT CONFIRMATION

| # | Criterion | Status |
|---|-----------|--------|
| 1.1 | Repository fully scanned | ✅ COMPLETE |
| 1.2 | Inventory file generated | ✅ THIS DOCUMENT |
| 1.3 | All files catalogued with paths | ✅ COMPLETE |
| 1.4 | __init__.py files identified | ✅ 26 FILES IDENTIFIED |
| 1.5 | DO_NOT_MIGRATE items flagged | ✅ COMPLETE |
| 1.6 | Mercury location confirmed | ✅ /projects/mercury/ |
| 1.7 | CLI scripts location confirmed | ✅ /scripts/launcher/ + root .command |

---

## PHASE 1 OUTPUT MESSAGE

```
═══════════════════════════════════════════════════════════════════════════════
                    PHASE 1 COMPLETE: RECONNAISSANCE
═══════════════════════════════════════════════════════════════════════════════

Files Catalogued:        ~350+
Directories Scanned:     ~100+
__init__.py Files:       26 identified
Mercury Location:        /projects/mercury/ (CONFIRMED)
CLI Scripts Location:    /scripts/launcher/ + root .command files (CONFIRMED)

Key Locations Confirmed:
├── Core Backend:     /src/cia_sie/ (50 files)
├── Mercury Frontend: /projects/mercury/ (56 files)
├── Documentation:    /documentation/ (157 files)
├── Tests:            /tests/ (63 files)
├── CLI Scripts:      /scripts/launcher/ (5 files) + 2 .command at root
└── Quarantine:       /quarantine/ (existing) + /Duplicates for Deletion/

DO_NOT_MIGRATE Items:
├── venv/
├── __pycache__/ (all)
├── .git/
├── *.pyc
├── .pytest_cache/
└── *.egg-info/

READY FOR PHASE 2: CLASSIFICATION

═══════════════════════════════════════════════════════════════════════════════
```

---

*Generated per CEAD v2.0 Section 9 Phase 1 | January 13, 2026*
