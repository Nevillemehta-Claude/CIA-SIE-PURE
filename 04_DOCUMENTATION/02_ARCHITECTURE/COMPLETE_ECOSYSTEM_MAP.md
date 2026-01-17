# ═══════════════════════════════════════════════════════════════════════════════
# CIA-SIE ECOSYSTEM — COMPLETE HIERARCHICAL MAP & NARRATIVE GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
# Post-CEAD v2.0 Restructuring | Generated: January 13, 2026
# ═══════════════════════════════════════════════════════════════════════════════

## EXECUTIVE OVERVIEW

The CIA-SIE (Chart Intelligence Assistant - Signal Intelligence Engine) Ecosystem 
has been restructured into **three sovereign domains** plus supporting infrastructure.

```
CIA-SIE-PURE/
├── 🔷 CIA-SIE-Pure/        ← PRIMARY DOMAIN: Backend Intelligence Engine
├── 🟠 Mercury/             ← FRONTEND DOMAIN: Chat Interface
├── 🟢 Command-Control/     ← OPERATIONS DOMAIN: CLI & Launchers
├── 📦 shared/              ← Cross-project resources (future use)
├── ⚠️ quarantine/          ← Isolated items pending review
├── 📋 migration-logs/      ← CEAD v2.0 audit trail
└── 📄 Root Documentation   ← System-wide guides
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                        🔷 CIA-SIE-PURE (PRIMARY DOMAIN)
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose
The **backend intelligence engine** — the brain of the system. Handles all data 
processing, AI integration, database operations, and exposes REST APIs.

## Directory Structure with Narratives

```
CIA-SIE-Pure/                           # 463 files total
│
├── 📄 alembic.ini                      # Database migration configuration
├── 📄 pyproject.toml                   # Python package definition & dependencies
├── 📄 .gitkeep                         # Git placeholder
│
├── 📁 alembic/                         # DATABASE MIGRATIONS
│   ├── env.py                          # Migration environment setup
│   ├── script.py.mako                  # Migration template
│   └── 📁 versions/                    # Migration history
│       ├── 20251230_0001_initial_schema.py        # Initial tables
│       └── 20251231_1004_..._add_ai_tables.py     # AI conversation tables
│
├── 📁 config/                          # CONFIGURATION (Future Use)
│   ├── 📁 api-keys/                    # API key storage
│   ├── 📁 environments/                # Environment configs
│   └── 📁 feature-flags/               # Feature toggles
│
├── 📁 data/                            # PERSISTENT DATA
│   └── cia_sie.db                      # SQLite database (167KB)
│                                       # Contains: instruments, signals, baskets,
│                                       # silos, relationships, AI conversations
│
├── 📁 src/                             # SOURCE CODE (51 Python files)
│   └── 📁 cia_sie/                     # Main Python package
│       │
│       ├── __init__.py                 # Package initialization
│       ├── main.py                     # 🚀 APPLICATION ENTRY POINT
│       │                               # Starts FastAPI server on port 8000
│       │
│       ├── 📁 api/                     # REST API LAYER
│       │   ├── __init__.py
│       │   ├── app.py                  # FastAPI application factory
│       │   │                           # CORS, middleware, route registration
│       │   └── 📁 routes/              # ENDPOINT HANDLERS
│       │       ├── __init__.py         # Route aggregator
│       │       ├── ai.py               # /api/ai/* — Claude AI endpoints
│       │       ├── baskets.py          # /api/baskets/* — Basket CRUD
│       │       ├── charts.py           # /api/charts/* — Chart data
│       │       ├── chat.py             # /api/chat/* — Chat interface
│       │       ├── instruments.py      # /api/instruments/* — Instrument CRUD
│       │       ├── narratives.py       # /api/narratives/* — AI narratives
│       │       ├── platforms.py        # /api/platforms/* — Platform registry
│       │       ├── relationships.py    # /api/relationships/* — Entity links
│       │       ├── signals.py          # /api/signals/* — Signal management
│       │       ├── silos.py            # /api/silos/* — Data silo CRUD
│       │       ├── strategy.py         # /api/strategy/* — Trading strategies
│       │       └── webhooks.py         # /api/webhooks/* — External webhooks
│       │
│       ├── 📁 ai/                      # AI INTEGRATION LAYER
│       │   ├── __init__.py             # AI module exports
│       │   ├── claude_client.py        # 🤖 Anthropic Claude API wrapper
│       │   │                           # Handles API calls, rate limiting
│       │   ├── model_registry.py       # AI model configurations
│       │   ├── narrative_generator.py  # Generates trading narratives
│       │   ├── prompt_builder.py       # Constructs AI prompts
│       │   ├── response_validator.py   # ⚖️ CONSTITUTIONAL COMPLIANCE
│       │   │                           # Enforces CR-001, CR-002, CR-003
│       │   └── usage_tracker.py        # API usage metrics
│       │
│       ├── 📁 core/                    # CORE UTILITIES
│       │   ├── __init__.py
│       │   ├── config.py               # ⚙️ SETTINGS MANAGEMENT
│       │   │                           # Environment variables, defaults
│       │   ├── enums.py                # Enumeration types
│       │   ├── exceptions.py           # Custom exception classes
│       │   ├── models.py               # Pydantic data models
│       │   └── security.py             # Security utilities
│       │
│       ├── 📁 dal/                     # DATA ACCESS LAYER
│       │   ├── __init__.py
│       │   ├── database.py             # 🗄️ SQLAlchemy engine & session
│       │   ├── models.py               # ORM entity definitions
│       │   │                           # Instrument, Signal, Basket, Silo, etc.
│       │   └── repositories.py         # Data access patterns
│       │
│       ├── 📁 exposure/                # RELATIONSHIP ANALYSIS
│       │   ├── __init__.py
│       │   ├── confirmation_detector.py # Finds confirming signals
│       │   ├── contradiction_detector.py # Finds conflicting signals
│       │   └── relationship_exposer.py  # Exposes entity relationships
│       │
│       ├── 📁 ingestion/               # SIGNAL INGESTION
│       │   ├── __init__.py
│       │   ├── freshness.py            # Data freshness tracking
│       │   ├── signal_normalizer.py    # Normalizes incoming signals
│       │   └── webhook_handler.py      # Processes webhook payloads
│       │
│       ├── 📁 platforms/               # PLATFORM ADAPTERS
│       │   ├── __init__.py
│       │   ├── base.py                 # Abstract platform interface
│       │   ├── kite.py                 # 📈 Kite Connect adapter
│       │   ├── registry.py             # Platform registry
│       │   └── tradingview.py          # 📊 TradingView adapter
│       │
│       └── 📁 webhooks/                # WEBHOOK RECEIVERS
│           ├── __init__.py
│           └── tradingview_receiver.py # TradingView alert receiver
│
├── 📁 tests/                           # TEST SUITE (64 Python files)
│   ├── __init__.py
│   ├── conftest.py                     # Shared fixtures
│   │
│   ├── 📁 backend/                     # API endpoint tests
│   │   └── test_api_*.py               # 11 test files
│   │
│   ├── 📁 chaos/                       # Chaos/stress tests
│   │   ├── test_concurrent_load.py
│   │   └── test_invalid_input.py
│   │
│   ├── 📁 constitutional/              # ⚖️ COMPLIANCE TESTS
│   │   ├── test_cr001_no_recommendations.py    # No investment advice
│   │   ├── test_cr002_equal_visual_weight.py   # Balanced presentation
│   │   └── test_cr003_mandatory_disclaimer.py  # Required disclaimers
│   │
│   ├── 📁 e2e/                         # End-to-end tests
│   │   ├── test_signal_flow.py
│   │   └── test_user_journeys.py
│   │
│   ├── 📁 integration/                 # Integration tests
│   │   ├── test_api.py
│   │   └── test_full_api.py
│   │
│   └── 📁 unit/                        # Unit tests (32 files)
│       └── test_*.py                   # Individual module tests
│
├── 📁 scripts/                         # UTILITY SCRIPTS
│   ├── execute_all_tests_autonomous.py # 🧪 Automated test runner
│   ├── extract_chat_history.py         # Chat export utility
│   ├── extract_docx.py                 # Document extraction
│   ├── generate_chronicle.py           # Chronicle generator
│   ├── gold_correlation_chart.py       # Gold analysis charting
│   ├── run_comprehensive_tests.py      # Full test suite
│   ├── run_quick_tests.py              # Quick smoke tests
│   └── seed_sample_data.py             # 🌱 Database seeding
│
└── 📁 docs/                            # DOCUMENTATION (209 files)
    │
    ├── 📁 01_GOVERNANCE/               # GOVERNANCE DOCUMENTS
    │   ├── CONSTITUTIONAL_RULES.md     # ⚖️ Trading compliance rules
    │   ├── FINANCIAL_SERVICES_ADAPTER.md
    │   ├── GOLD_STANDARD_FRAMEWORK.md
    │   ├── PROJECT_CONFIGURATION.md
    │   └── UNIVERSAL_CONTEXT_REHYDRATION_PROTOCOL.md
    │
    ├── 📁 02_ARCHITECTURE/             # ARCHITECTURE DOCUMENTS
    │   ├── BACKEND_ARCHITECTURE.md
    │   ├── CIA-SIE_MASTER_SYSTEM_ARCHITECTURE.md
    │   ├── CROSS_CUTTING_CONCERNS.md
    │   ├── DATA_TYPES_REFERENCE.md
    │   ├── INTEGRATION_ARCHITECTURE.md
    │   └── 📁 diagrams/                # PlantUML diagrams (14 files)
    │       ├── system_architecture.puml
    │       ├── signal_ingestion_flow.puml
    │       ├── ai_narrative_flow.puml
    │       └── ... (11 more)
    │
    ├── 📁 03_SPECIFICATIONS/           # TECHNICAL SPECS (10 files)
    │   ├── COMPREHENSIVE_COMPONENT_SPECIFICATIONS_v1.0.md
    │   ├── UI_UX_DESIGN_SYSTEM_v1.0.md
    │   └── 📁 MCC_SPECIFICATIONS/      # Mission Control specs
    │
    ├── 📁 04_AI_HANDOFF/               # AI AGENT HANDOFF DOCS
    │   ├── AUTONOMOUS_HANDOFF_COMPREHENSIVE.md
    │   ├── HANDOFF_00_README.md
    │   ├── HANDOFF_01-09_*.md          # 9 handoff chapters
    │   └── 📁 PROMPTS/                 # AI prompts
    │
    ├── 📁 05_DECISIONS/                # ARCHITECTURAL DECISIONS
    │   ├── ADR-001_Data_Repository_Model.md
    │   ├── ADR-002_Self_Contained_Workspace.md
    │   └── ADR-003_AI_Model_Selection.md
    │
    ├── 📁 06_AUDITS/                   # AUDIT REPORTS (14 files)
    │   ├── CIRCUIT_INTEGRITY_REPORT_v1.0.md
    │   ├── DESIGN_VALIDATION_REPORT_v1.0.md
    │   ├── PROJECT_MATURITY_AUDIT.md
    │   └── 📁 RECONCILIATION/          # Remediation docs
    │
    ├── 📁 07_MISSION_CONTROL/          # MCC DOCUMENTATION
    │   ├── CURSOR_HANDOFF_PROTOCOL.md
    │   ├── HITL_APPROVAL_GATES.md
    │   └── MCC_README.md
    │
    ├── 📁 07_TESTING/                  # TEST DOCUMENTATION (8 files)
    │   ├── MASTER_TEST_EXECUTION_PLAN_v1.0.md
    │   ├── LATEST_TEST_REPORT.md
    │   └── LAUNCHER_UAT_RESULTS_*.md
    │
    ├── 📁 08_OPERATIONS/               # OPERATIONAL GUIDES
    │   ├── DOCUMENTATION_INDEX.md
    │   ├── PROJECT_README.md
    │   └── TESTING.md
    │
    ├── 📁 AEROSPACE_SYSTEMS_MANUAL/    # 🚀 AEROSPACE-GRADE DOCS
    │   ├── 00_MASTER_INDEX.md
    │   ├── 01_SYSTEM_CIRCUIT_MAP.md
    │   ├── 02_SIGNAL_FLOW_MATRIX.md
    │   ├── 03_INTEGRATION_TEST_PROTOCOL.md
    │   ├── 04_FAILURE_MODE_ANALYSIS.md
    │   ├── 05_END_TO_END_TRACE.md
    │   └── 06_LAUNCH_READINESS_CHECKLIST.md
    │
    ├── 📁 CHART_01A_COMPLETE_PACKAGE/  # TradingView Chart Package
    │   ├── 01_UPGRADED_PRIMARY_SIGNAL.pine
    │   ├── 02_UPGRADED_MOM_HEALTH.pine
    │   └── README.md
    │
    ├── 📁 CHART_02_COMPLETE_PACKAGE/   # Second Chart Package
    │   ├── 01_UPGRADED_HTF_STRUCTURE.pine
    │   └── README.md
    │
    ├── 📁 LAUNCHER_SYSTEM_COMPLETE/    # Launcher documentation
    │   └── (22 files across 7 subdirectories)
    │
    ├── 📁 prototypes/                  # UI PROTOTYPES (15 HTML files)
    │   ├── 00_index.html               # Prototype index
    │   ├── 07_ai_chat.html             # AI chat prototype
    │   └── 05_mcc_dashboard.html       # MCC dashboard
    │
    ├── 📁 QA_KNOWLEDGE_BASE/           # QA session logs
    │   └── (7 files)
    │
    ├── 📁 chat_history_export/         # ARCHIVED CHAT HISTORY (37 files)
    │   ├── 00_INDEX.md
    │   ├── 001-032_*.md                # Individual chat sessions
    │   └── CIA_SIE_COMPLETE_CHAT_CHRONICLE.html
    │
    ├── USER_MANUAL.md                  # 📖 USER MANUAL
    │   │                               # Quick start, usage, troubleshooting
    │
    ├── PROJECT_TREE_COMPLETE.md        # Project tree visualization
    └── MASTER_TODO_TRACKER.md          # Task tracking
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                        🟠 MERCURY (FRONTEND DOMAIN)
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose
The **conversational frontend interface** — the face of the system. Provides 
WebSocket-based chat, Kite market data integration, and launch readiness checks.

## Directory Structure with Narratives

```
Mercury/                                # 57 files total
│
├── 📄 README.md                        # Mercury overview
├── 📄 pyproject.toml                   # Package definition
├── 📄 requirements.txt                 # Dependencies
├── 📄 start-mercury.command            # 🖱️ DOUBLE-CLICK LAUNCHER (macOS)
│
├── 📁 src/                             # SOURCE CODE
│   └── 📁 mercury/                     # Main Python package
│       │
│       ├── __init__.py                 # Package initialization
│       ├── main.py                     # 🚀 APPLICATION ENTRY POINT
│       │                               # Modes: --web, --check, REPL
│       │
│       ├── 📁 api/                     # WEB API LAYER
│       │   ├── __init__.py
│       │   └── app.py                  # 🌐 FastAPI WebSocket server
│       │                               # Routes: /, /ws, /status, /health
│       │
│       ├── 📁 ai/                      # AI ENGINE
│       │   ├── __init__.py
│       │   ├── engine.py               # AI response generation
│       │   └── prompts.py              # Prompt templates
│       │
│       ├── 📁 chat/                    # CHAT LOGIC
│       │   ├── __init__.py
│       │   ├── conversation.py         # Conversation management
│       │   └── engine.py               # Chat processing engine
│       │
│       ├── 📁 core/                    # CORE SERVICES
│       │   ├── __init__.py             # Module exports (11 imports)
│       │   ├── config.py               # ⚙️ Settings management
│       │   ├── errors.py               # Error handling
│       │   ├── exceptions.py           # Custom exceptions
│       │   ├── features.py             # Feature flags
│       │   ├── health.py               # 💓 Health check system
│       │   ├── logging.py              # Logging configuration
│       │   ├── metrics.py              # Usage metrics
│       │   ├── resilience.py           # 🔄 Circuit breakers
│       │   ├── security.py             # Security utilities
│       │   ├── startup.py              # 🚦 API VERIFICATION
│       │   │                           # verify_kite_api(), verify_anthropic_api()
│       │   │                           # perform_launch_readiness_check()
│       │   └── validation.py           # Input validation
│       │
│       ├── 📁 interface/               # USER INTERFACES
│       │   ├── __init__.py
│       │   └── repl.py                 # 💻 Terminal REPL interface
│       │
│       └── 📁 kite/                    # MARKET DATA
│           ├── __init__.py
│           ├── adapter.py              # 📈 Kite Connect adapter
│           └── models.py               # Kite data models
│
├── 📁 tests/                           # TEST SUITE (10 files)
│   ├── __init__.py
│   ├── test_api.py                     # WebSocket/API tests
│   ├── test_chat_engine.py             # Chat logic tests
│   ├── test_conversation.py            # Conversation tests
│   ├── test_errors.py                  # Error handling tests
│   ├── test_health.py                  # Health check tests
│   ├── test_metrics.py                 # Metrics tests
│   ├── test_resilience.py              # Circuit breaker tests
│   ├── test_security.py                # Security tests
│   └── test_startup.py                 # Startup verification tests
│
├── 📁 scripts/                         # UTILITY SCRIPTS
│   ├── start_mercury.sh                # Shell launcher
│   └── verify_deployment.py            # Deployment verification
│
├── 📁 documentation/                   # 📚 MODULAR COMPENDIUM (12 chapters)
│   ├── 01_GENESIS.md                   # Origin & purpose
│   ├── 02_CONSTITUTION.md              # Operating principles
│   ├── 03_ARCHITECTURE.md              # Technical design
│   ├── 04_SPECIFICATION.md             # Detailed specs
│   ├── 05_INTEGRATION_VERIFICATION.md  # Integration tests
│   ├── 06_RECONCILIATION.md            # Issue resolution
│   ├── 07_CERTIFICATION.md             # Quality certification
│   ├── 08_OPERATION.md                 # Operational guide
│   ├── 09_MISSION_CRITICAL_STANDARDS.md
│   ├── 10_MISSION_CRITICAL_IMPLEMENTATION.md
│   ├── 11_DEPLOYMENT_CERTIFICATION.md
│   ├── 12_LAUNCH_READINESS_REPORT.md   # 🚀 Final readiness report
│   └── 📁 templates/
│       └── POSTMORTEM_TEMPLATE.md
│
├── 📁 static/                          # STATIC ASSETS
│   ├── 📁 css/                         # Stylesheets
│   ├── 📁 images/                      # Images
│   └── 📁 js/                          # JavaScript
│
└── 📁 docs/                            # ADDITIONAL DOCS
    ├── 📁 audit-logs/
    ├── 📁 component-library/
    ├── 📁 design-specs/
    ├── 📁 style-guide/
    └── 📁 user-flows/
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                     🟢 COMMAND-CONTROL (OPERATIONS DOMAIN)
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose
The **operational command center** — controls system lifecycle. Provides scripts 
for starting, stopping, and monitoring the entire ecosystem.

## Directory Structure with Narratives

```
Command-Control/                        # 7 files (excl. placeholders)
│
├── 📁 scripts/                         # OPERATIONAL SCRIPTS
│   │
│   ├── 📁 macos/                       # macOS LAUNCHERS
│   │   ├── start-cia-sie.command       # 🖱️ DOUBLE-CLICK TO START
│   │   │                               # Starts both CIA-SIE-Pure + Mercury
│   │   └── stop-cia-sie.command        # 🛑 DOUBLE-CLICK TO STOP
│   │                                   # Graceful shutdown of all services
│   │
│   └── 📁 shell/                       # BASH SCRIPTS
│       ├── config.sh                   # ⚙️ Configuration variables
│       │                               # Ports, paths, timeouts
│       ├── health-check.sh             # 💓 Service health verification
│       │                               # Checks port availability, responses
│       ├── ignite.sh                   # 🔥 MAIN STARTUP SEQUENCE
│       │                               # 1. Load config
│       │                               # 2. Activate venv
│       │                               # 3. Start backend (port 8000)
│       │                               # 4. Wait for health
│       │                               # 5. Start frontend (port 8001)
│       │                               # 6. Final health check
│       ├── shutdown.sh                 # 🛑 GRACEFUL SHUTDOWN
│       │                               # Sends SIGTERM, waits, force kills
│       └── utils.sh                    # 🛠️ Utility functions
│                                       # Logging, error handling, helpers
│
├── 📁 config/                          # CONFIGURATION (Future Use)
│   ├── 📁 cli-settings/
│   └── 📁 defaults/
│
├── 📁 docs/                            # DOCUMENTATION (Future Use)
│   ├── 📁 audit-logs/
│   ├── 📁 command-reference/
│   └── 📁 usage-guide/
│
├── 📁 src/                             # SOURCE CODE (Future Use)
│   ├── 📁 commands/                    # Command implementations
│   │   ├── health/
│   │   ├── restart/
│   │   ├── start/
│   │   ├── status/
│   │   └── stop/
│   ├── 📁 handlers/                    # Response handlers
│   ├── 📁 utils/                       # Utilities
│   └── 📁 validators/                  # Input validation
│
└── 📁 tests/                           # TESTS (Future Use)
    ├── 📁 command-validation/
    └── 📁 unit/
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                          📦 SHARED (CROSS-PROJECT)
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose
Reserved for truly shared resources between domains. Currently empty as domains 
communicate via APIs (HTTP/WebSocket), not shared code.

```
shared/                                 # 0 files (prepared for future)
├── 📁 constants/                       # Shared constants
├── 📁 enums/                           # Shared enumerations
├── 📁 interfaces/                      # Shared interfaces
└── 📁 types/                           # Shared type definitions
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                          ⚠️ QUARANTINE (ISOLATED ITEMS)
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose
Contains isolated items pending human review before permanent deletion.
Items here are NOT part of the active codebase.

```
quarantine/                             # 22 files
│
├── README.md                           # Quarantine overview
├── SANITISATION_AUDIT_REPORT.md        # Audit findings
├── EMPTY_MODULE_QUARANTINED.py         # Empty module backup
├── STUB_FUNCTIONS_QUARANTINED.py       # Stub function backup
│
├── 📁 debug-logs/                      # ARCHIVED LOGS
│   ├── backend.log                     # Backend runtime logs
│   ├── cia_sie.log                     # Application logs
│   ├── launcher.log                    # Launcher logs
│   └── ngrok.log                       # ngrok tunnel logs
│
├── 📁 duplicates/                      # PRE-FLAGGED DUPLICATES
│   ├── DUPLICATE_FORENSIC_AUDIT_REPORT.md
│   ├── 📁 docs_architecture_diagrams/  # 9 duplicate .puml files
│   └── 📁 root_level/                  # 2 duplicate analysis files
│
├── 📁 orphans/                         # ORPHANED ITEMS
│   └── empty_dirs.txt                  # Log of empty directories
│
├── 📁 unclassified/                    # UNCLASSIFIED ITEMS
│   └── code-workspace-copy.json        # VS Code workspace config
│
├── 📁 dead-code/                       # (empty, prepared)
├── 📁 deprecated/                      # (empty, prepared)
└── 📁 empty-files/                     # (empty, prepared)
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                        📋 MIGRATION-LOGS (AUDIT TRAIL)
# ═══════════════════════════════════════════════════════════════════════════════

## Purpose
Complete audit trail of the CEAD v2.0 Forensic Codebase Restructuring.
Provides full traceability for every decision and action.

```
migration-logs/                         # 11 files
│
├── CEAD-v2.0-CIA-SIE-ECOSYSTEM-FORENSIC-RESTRUCTURING.md
│   │                                   # 📜 ORIGINAL DIRECTIVE
│   │                                   # 2,628 lines of specifications
│   │
├── CURSOR-ENGAGEMENT-ALIGNMENT-DOCUMENT-*.md
│   │                                   # 📜 ENGAGEMENT PROTOCOL
│   │
├── phase-1-inventory.md                # File inventory + hashes
├── phase-2-classification.md           # Destination assignments
├── phase-3-structure.md                # Directory creation log
├── phase-4-migration.md                # File movement log
├── phase-5-path-resolution.md          # Import analysis
├── phase-6-validation.md               # Hash verification
├── phase-7-documentation.md            # Documentation generation
├── phase-8-confirmation.md             # Success criteria check
└── phase-9-sanitisation.md             # Legacy cleanup log
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                          📄 ROOT DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

## Files at Repository Root

```
CIA-SIE-PURE/
│
├── MASTER-README.md                    # 📖 PRIMARY README
│   │                                   # Domain overview, quick starts
│   │
├── ARCHITECTURE-OVERVIEW.md            # 🏗️ TECHNICAL ARCHITECTURE
│   │                                   # System design, data flows
│   │
├── MIGRATION-REPORT.md                 # 📊 MIGRATION AUDIT
│   │                                   # Phase summaries, verification
│   │
├── COMPLETE_ECOSYSTEM_MAP.md           # 🗺️ THIS DOCUMENT
│   │                                   # Full hierarchical map
│   │
├── .env                                # Environment variables
├── .env.example                        # Environment template
├── .gitignore                          # Git ignore rules
└── .github/                            # GitHub configuration
```

---

# ═══════════════════════════════════════════════════════════════════════════════
#                            QUICK REFERENCE TABLE
# ═══════════════════════════════════════════════════════════════════════════════

## What Goes Where?

| Need To... | Go To... |
|------------|----------|
| **Start the system** | `Command-Control/scripts/macos/start-cia-sie.command` |
| **Stop the system** | `Command-Control/scripts/macos/stop-cia-sie.command` |
| **Edit backend code** | `CIA-SIE-Pure/src/cia_sie/` |
| **Edit frontend code** | `Mercury/src/mercury/` |
| **Run tests** | `CIA-SIE-Pure/tests/` or `Mercury/tests/` |
| **Read user manual** | `CIA-SIE-Pure/docs/USER_MANUAL.md` |
| **Check architecture** | `ARCHITECTURE-OVERVIEW.md` |
| **View API routes** | `CIA-SIE-Pure/src/cia_sie/api/routes/` |
| **Configure environment** | `.env` (root level) |
| **Check database** | `CIA-SIE-Pure/data/cia_sie.db` |
| **View chat prototypes** | `CIA-SIE-Pure/docs/prototypes/07_ai_chat.html` |
| **Review audit trail** | `migration-logs/` |

---

## File Counts by Domain

| Domain | Files | Purpose |
|--------|-------|---------|
| **CIA-SIE-Pure** | 463 | Backend engine |
| **Mercury** | 57 | Frontend interface |
| **Command-Control** | 7 | Operations CLI |
| **quarantine** | 22 | Isolated items |
| **migration-logs** | 11 | Audit trail |
| **shared** | 0 | Cross-project (future) |
| **Root** | 6 | Documentation |
| **TOTAL** | ~566 | Complete ecosystem |

---

*Generated per CEAD v2.0 Phase 7 | January 13, 2026*
*Aerospace-Grade Documentation Standards*
