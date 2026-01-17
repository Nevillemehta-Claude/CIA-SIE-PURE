# CIA-SIE-PURE + MERCURY
## COMPLETE INTEGRATED PROJECT TREE

**Generated:** January 2026
**Purpose:** Hierarchical visualization of the complete composite application

---

## LEGEND

| Symbol | Meaning |
|--------|---------|
| 📖 | **USER MANUAL** - Start here for usage instructions |
| 🚀 | **START COMMAND** - Double-click to launch system |
| 🛑 | **STOP COMMAND** - Double-click to stop system |
| 📁 | Directory |
| 📄 | File |
| ⚙️ | Configuration file |
| 🐍 | Python source file |
| 📝 | Documentation/Markdown |
| 🧪 | Test file |
| 🔧 | Shell script |

---

## COMPLETE PROJECT TREE

```
CIA-SIE-PURE/
│
├── 🚀 start-cia-sie.command ─────────────── DOUBLE-CLICK TO START CIA-SIE
├── 🛑 stop-cia-sie.command ──────────────── DOUBLE-CLICK TO STOP CIA-SIE
│
├── 📄 README.md
├── ⚙️ pyproject.toml
├── ⚙️ alembic.ini
│
│
├── 📁 documentation/ ────────────────────── ALL DOCUMENTATION
│   │
│   ├── 📖 USER_MANUAL.md ────────────────── ★★★ START HERE FOR USAGE ★★★
│   │
│   ├── 📁 AEROSPACE_SYSTEMS_MANUAL/ ─────── Technical Architecture Docs
│   │   ├── 📝 00_MASTER_INDEX.md
│   │   ├── 📝 01_SYSTEM_CIRCUIT_MAP.md
│   │   ├── 📝 02_SIGNAL_FLOW_MATRIX.md
│   │   ├── 📝 03_INTEGRATION_TEST_PROTOCOL.md
│   │   ├── 📝 04_FAILURE_MODE_ANALYSIS.md
│   │   ├── 📝 05_END_TO_END_TRACE.md
│   │   └── 📝 06_LAUNCH_READINESS_CHECKLIST.md
│   │
│   ├── 📁 01_GOVERNANCE/
│   │   ├── 📝 CONSTITUTIONAL_RULES.md ───── CR-001, CR-002, CR-003
│   │   ├── 📝 FINANCIAL_SERVICES_ADAPTER.md
│   │   ├── 📝 GOLD_STANDARD_FRAMEWORK.md
│   │   ├── 📝 PROJECT_CONFIGURATION.md
│   │   └── 📝 UNIVERSAL_CONTEXT_REHYDRATION_PROTOCOL.md
│   │
│   ├── 📁 02_ARCHITECTURE/
│   │   ├── 📝 BACKEND_ARCHITECTURE.md
│   │   ├── 📝 BACKEND_FLOWCHARTS.md
│   │   ├── 📝 CIA-SIE_MASTER_SYSTEM_ARCHITECTURE.md
│   │   ├── 📝 CROSS_CUTTING_CONCERNS.md
│   │   ├── 📝 DATA_TYPES_REFERENCE.md
│   │   ├── 📝 INTEGRATION_ARCHITECTURE.md
│   │   ├── 📝 LAUNCHER_SYSTEM_ARCHITECTURE.md
│   │   ├── 📝 MASTER_DATA_REFERENCE.md
│   │   └── 📁 diagrams/ (14 PlantUML files)
│   │
│   ├── 📁 03_SPECIFICATIONS/ (10 files)
│   ├── 📁 04_AI_HANDOFF/ (13 files)
│   ├── 📁 05_DECISIONS/ (3 ADR files)
│   ├── 📁 06_AUDITS/ (14 files)
│   ├── 📁 07_MISSION_CONTROL/ (6 files)
│   ├── 📁 07_TESTING/ (8 files)
│   ├── 📁 08_OPERATIONS/ (5 files)
│   │
│   ├── 📁 CHART_01A_COMPLETE_PACKAGE/ ──── TradingView Pine Scripts
│   ├── 📁 CHART_02_COMPLETE_PACKAGE/
│   ├── 📁 LAUNCHER_SYSTEM_COMPLETE/
│   ├── 📁 prototypes/ (15 HTML prototypes)
│   └── 📁 QA_KNOWLEDGE_BASE/
│
│
├── 📁 src/cia_sie/ ──────────────────────── CIA-SIE SOURCE CODE
│   │
│   ├── 🐍 __init__.py
│   ├── 🐍 main.py
│   │
│   ├── 📁 api/ ──────────────────────────── FastAPI Application
│   │   ├── 🐍 app.py ────────────────────── Main API entry point
│   │   └── 📁 routes/
│   │       ├── 🐍 ai.py
│   │       ├── 🐍 baskets.py
│   │       ├── 🐍 charts.py
│   │       ├── 🐍 chat.py
│   │       ├── 🐍 instruments.py
│   │       ├── 🐍 narratives.py
│   │       ├── 🐍 platforms.py
│   │       ├── 🐍 relationships.py
│   │       ├── 🐍 signals.py
│   │       ├── 🐍 silos.py
│   │       ├── 🐍 strategy.py
│   │       └── 🐍 webhooks.py
│   │
│   ├── 📁 ai/ ───────────────────────────── AI/Claude Integration
│   │   ├── 🐍 claude_client.py
│   │   ├── 🐍 model_registry.py
│   │   ├── 🐍 narrative_generator.py
│   │   ├── 🐍 prompt_builder.py
│   │   ├── 🐍 response_validator.py ─────── Constitutional Enforcement
│   │   └── 🐍 usage_tracker.py
│   │
│   ├── 📁 core/ ─────────────────────────── Core Utilities
│   │   ├── 🐍 config.py
│   │   ├── 🐍 enums.py
│   │   ├── 🐍 exceptions.py
│   │   ├── 🐍 models.py
│   │   └── 🐍 security.py
│   │
│   ├── 📁 dal/ ──────────────────────────── Data Access Layer
│   │   ├── 🐍 database.py
│   │   ├── 🐍 models.py ─────────────────── ORM Models
│   │   └── 🐍 repositories.py
│   │
│   ├── 📁 exposure/ ─────────────────────── Signal Analysis
│   │   ├── 🐍 confirmation_detector.py
│   │   ├── 🐍 contradiction_detector.py
│   │   └── 🐍 relationship_exposer.py
│   │
│   ├── 📁 ingestion/ ────────────────────── Data Ingestion
│   │   ├── 🐍 freshness.py
│   │   ├── 🐍 signal_normalizer.py
│   │   └── 🐍 webhook_handler.py
│   │
│   ├── 📁 platforms/ ────────────────────── External Platforms
│   │   ├── 🐍 base.py
│   │   ├── 🐍 kite.py
│   │   ├── 🐍 registry.py
│   │   └── 🐍 tradingview.py
│   │
│   ├── 📁 webhooks/
│   │   └── 🐍 tradingview_receiver.py
│   │
│   └── 📁 bridge/
│
│
├── 📁 projects/ ─────────────────────────── SUB-PROJECTS
│   │
│   └── 📁 mercury/ ──────────────────────── MERCURY AI CHAT SYSTEM
│       │
│       ├── 🚀 start-mercury.command ─────── DOUBLE-CLICK TO START MERCURY
│       │
│       ├── 📝 README.md
│       ├── ⚙️ pyproject.toml
│       ├── ⚙️ requirements.txt
│       │
│       ├── 📁 documentation/ ────────────── Mercury Documentation
│       │   ├── 📝 01_GENESIS.md
│       │   ├── 📝 02_CONSTITUTION.md ────── MR-001 to MR-005 (Unrestricted)
│       │   ├── 📝 03_ARCHITECTURE.md
│       │   ├── 📝 04_SPECIFICATION.md
│       │   ├── 📝 05_INTEGRATION_VERIFICATION.md
│       │   ├── 📝 06_RECONCILIATION.md
│       │   ├── 📝 07_CERTIFICATION.md
│       │   ├── 📝 08_OPERATION.md
│       │   ├── 📝 09_MISSION_CRITICAL_STANDARDS.md
│       │   ├── 📝 10_MISSION_CRITICAL_IMPLEMENTATION.md
│       │   ├── 📝 11_DEPLOYMENT_CERTIFICATION.md
│       │   ├── 📝 12_LAUNCH_READINESS_REPORT.md
│       │   └── 📁 templates/
│       │       └── 📝 POSTMORTEM_TEMPLATE.md
│       │
│       ├── 📁 scripts/
│       │   ├── 🔧 start_mercury.sh
│       │   └── 🐍 verify_deployment.py
│       │
│       ├── 📁 src/mercury/ ──────────────── Mercury Source Code
│       │   │
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 main.py ───────────────── Entry Point (--web, --check)
│       │   │
│       │   ├── 📁 api/
│       │   │   └── 🐍 app.py ────────────── Web Frontend (port 8888)
│       │   │
│       │   ├── 📁 ai/
│       │   │   ├── 🐍 engine.py ─────────── Claude Integration
│       │   │   └── 🐍 prompts.py ────────── Unrestricted Prompts
│       │   │
│       │   ├── 📁 chat/
│       │   │   ├── 🐍 engine.py ─────────── Query Processing
│       │   │   └── 🐍 conversation.py ───── Context Management
│       │   │
│       │   ├── 📁 kite/
│       │   │   ├── 🐍 adapter.py ────────── Kite API Integration
│       │   │   └── 🐍 models.py ─────────── Data Models
│       │   │
│       │   ├── 📁 core/
│       │   │   ├── 🐍 config.py ─────────── Configuration
│       │   │   ├── 🐍 startup.py ────────── Launch Readiness Check
│       │   │   ├── 🐍 security.py ───────── Key Masking
│       │   │   ├── 🐍 logging.py ────────── Structured Logging
│       │   │   ├── 🐍 validation.py ─────── Config Validation
│       │   │   ├── 🐍 resilience.py ─────── Circuit Breakers
│       │   │   ├── 🐍 health.py ─────────── Health Checks
│       │   │   ├── 🐍 metrics.py ────────── Observability
│       │   │   ├── 🐍 errors.py ─────────── Error Taxonomy
│       │   │   ├── 🐍 features.py ───────── Feature Flags
│       │   │   └── 🐍 exceptions.py
│       │   │
│       │   └── 📁 interface/
│       │       └── 🐍 repl.py ───────────── Terminal Interface
│       │
│       └── 📁 tests/ ────────────────────── Mercury Tests (10 files)
│           ├── 🧪 test_api.py
│           ├── 🧪 test_chat_engine.py
│           ├── 🧪 test_conversation.py
│           ├── 🧪 test_errors.py
│           ├── 🧪 test_health.py
│           ├── 🧪 test_metrics.py
│           ├── 🧪 test_resilience.py
│           ├── 🧪 test_security.py
│           └── 🧪 test_startup.py
│
│
├── 📁 tests/ ────────────────────────────── CIA-SIE TESTS (64 files)
│   ├── 📁 backend/ (12 test files)
│   ├── 📁 chaos/ (2 test files)
│   ├── 📁 constitutional/ (3 test files)
│   ├── 📁 e2e/ (2 test files)
│   ├── 📁 integration/ (2 test files)
│   └── 📁 unit/ (32 test files)
│
│
├── 📁 scripts/ ──────────────────────────── UTILITY SCRIPTS
│   │
│   ├── 📁 launcher/ ─────────────────────── Launcher System
│   │   ├── 🔧 config.sh ─────────────────── Configuration
│   │   ├── 🔧 ignite.sh ─────────────────── Startup Logic
│   │   ├── 🔧 shutdown.sh ───────────────── Shutdown Logic
│   │   ├── 🔧 health-check.sh ───────────── Health Verification
│   │   └── 🔧 utils.sh ──────────────────── Utility Functions
│   │
│   ├── 🐍 extract_docx.py
│   └── 🐍 gold_correlation_chart.py
│
│
├── 📁 alembic/ ──────────────────────────── DATABASE MIGRATIONS
│   ├── 🐍 env.py
│   ├── 📄 script.py.mako
│   └── 📁 versions/
│       ├── 🐍 20251230_0001_initial_schema.py
│       └── 🐍 20251231_1004_d06c96f6b20c_add_ai_tables.py
│
│
├── 📁 data/ ─────────────────────────────── DATA STORAGE
│   └── 📄 cia_sie.db ────────────────────── SQLite Database
│
│
├── 📁 logs/ ─────────────────────────────── LOG FILES
│   ├── 📄 backend.log
│   ├── 📄 cia_sie.log
│   ├── 📄 launcher.log
│   └── 📄 ngrok.log
│
│
├── 📁 pids/ ─────────────────────────────── PROCESS ID FILES
│
│
├── 📁 docs/audits/ ──────────────────────── AUDIT REPORTS
│   ├── 📄 PROJECT_MATURITY_AUDIT.html
│   └── 📄 SYSTEM_ARCHITECTURE_VISUAL.html
│
│
├── 📁 chat_history_export/ ──────────────── CHAT HISTORY ARCHIVE
│
│
└── 📁 venv/ ─────────────────────────────── PYTHON VIRTUAL ENVIRONMENT
```

---

## QUICK ACCESS REFERENCE

### 📖 USER MANUAL
```
/Users/nevillemehta/Downloads/CIA-SIE-PURE/documentation/USER_MANUAL.md
```
**Open in any Markdown viewer or text editor to read usage instructions.**

---

### 🚀 START COMMANDS

| System | Location | Action |
|--------|----------|--------|
| **CIA-SIE** | `/Users/nevillemehta/Downloads/CIA-SIE-PURE/start-cia-sie.command` | Double-click in Finder |
| **Mercury** | `/Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury/start-mercury.command` | Double-click in Finder |

**Alternative (Terminal):**
```bash
# Start Mercury
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury
source ../../venv/bin/activate
python -m mercury --web

# Start CIA-SIE
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE
./start-cia-sie.command
```

---

### 🛑 STOP COMMANDS

| System | Location | Action |
|--------|----------|--------|
| **CIA-SIE** | `/Users/nevillemehta/Downloads/CIA-SIE-PURE/stop-cia-sie.command` | Double-click in Finder |
| **Mercury** | Terminal where it's running | Press `Ctrl+C` |

---

## FILE COUNTS SUMMARY

| Category | Count |
|----------|-------|
| **CIA-SIE Python Source** | 50 files |
| **Mercury Python Source** | 27 files |
| **CIA-SIE Tests** | 64 files |
| **Mercury Tests** | 10 files |
| **Documentation Files** | 160+ files |
| **Shell Scripts** | 7 files |
| **Configuration Files** | 5 files |
| **TOTAL** | 320+ files |

---

## VISUAL MAP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                         CIA-SIE-PURE ROOT                                   │
│                                                                             │
│   ┌───────────────────────┐          ┌───────────────────────┐             │
│   │                       │          │                       │             │
│   │  🚀 start-cia-sie    │          │  📖 documentation/    │             │
│   │     .command          │          │     USER_MANUAL.md    │             │
│   │                       │          │                       │             │
│   │  🛑 stop-cia-sie     │          │  ★ READ THIS FIRST ★  │             │
│   │     .command          │          │                       │             │
│   │                       │          └───────────────────────┘             │
│   └───────────────────────┘                                                │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                                                                      │ │
│   │   📁 projects/mercury/                                               │ │
│   │                                                                      │ │
│   │   ┌─────────────────────────────────────────────────────────────┐   │ │
│   │   │                                                             │   │ │
│   │   │  🚀 start-mercury.command ─── DOUBLE-CLICK TO START CHAT   │   │ │
│   │   │                                                             │   │ │
│   │   │  When running, access at: http://localhost:8888             │   │ │
│   │   │                                                             │   │ │
│   │   └─────────────────────────────────────────────────────────────┘   │ │
│   │                                                                      │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## GETTING STARTED FLOWCHART

```
                    ┌─────────────────────┐
                    │                     │
                    │  Open Finder        │
                    │                     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │                     │
                    │  Navigate to:       │
                    │  CIA-SIE-PURE/      │
                    │                     │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
   ┌─────────────────────┐           ┌─────────────────────┐
   │                     │           │                     │
   │  Read First:        │           │  Or Jump Straight   │
   │  documentation/     │           │  To Launch:         │
   │  USER_MANUAL.md     │           │                     │
   │                     │           │  projects/mercury/  │
   │  📖                 │           │  start-mercury      │
   │                     │           │  .command           │
   └─────────────────────┘           │                     │
                                     │  🚀                 │
                                     └──────────┬──────────┘
                                                │
                                                ▼
                                     ┌─────────────────────┐
                                     │                     │
                                     │  Browser Opens:     │
                                     │  localhost:8888     │
                                     │                     │
                                     │  Start Chatting!    │
                                     │                     │
                                     └─────────────────────┘
```

---

**Document Version:** 1.0.0
**Last Updated:** January 2026
