# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: CLASSIFICATION — COMPLETE FILE ASSIGNMENT MAP
# ═══════════════════════════════════════════════════════════════════════════════
# CEAD v2.0 | Forensic Codebase Restructuring
# Generated: January 13, 2026
# ═══════════════════════════════════════════════════════════════════════════════

## CLASSIFICATION SUMMARY

| Destination | File Count | Status |
|-------------|------------|--------|
| **CIA-SIE-Pure** | ~270 | CLASSIFIED |
| **Mercury** | ~56 | LIFT OPERATION |
| **Command-Control** | ~10 | CLASSIFIED |
| **shared** | 0 | (none identified) |
| **quarantine** | ~20+ | CLASSIFIED |

---

## CIA-SIE-PURE DESTINATIONS

### Source: /src/cia_sie/ → Destination: /CIA-SIE-Pure/src/cia_sie/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/__init__.py` | C-029 |
| `/src/cia_sie/main.py` | `/CIA-SIE-Pure/src/cia_sie/main.py` | C-010 |

#### /src/cia_sie/ai/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/ai/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/ai/__init__.py` | C-029 |
| `/src/cia_sie/ai/claude_client.py` | `/CIA-SIE-Pure/src/cia_sie/ai/claude_client.py` | C-010 |
| `/src/cia_sie/ai/model_registry.py` | `/CIA-SIE-Pure/src/cia_sie/ai/model_registry.py` | C-010 |
| `/src/cia_sie/ai/narrative_generator.py` | `/CIA-SIE-Pure/src/cia_sie/ai/narrative_generator.py` | C-010 |
| `/src/cia_sie/ai/prompt_builder.py` | `/CIA-SIE-Pure/src/cia_sie/ai/prompt_builder.py` | C-010 |
| `/src/cia_sie/ai/response_validator.py` | `/CIA-SIE-Pure/src/cia_sie/ai/response_validator.py` | C-010 |
| `/src/cia_sie/ai/usage_tracker.py` | `/CIA-SIE-Pure/src/cia_sie/ai/usage_tracker.py` | C-010 |

#### /src/cia_sie/api/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/api/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/api/__init__.py` | C-029 |
| `/src/cia_sie/api/app.py` | `/CIA-SIE-Pure/src/cia_sie/api/app.py` | C-030 |
| `/src/cia_sie/api/routes/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/__init__.py` | C-029 |
| `/src/cia_sie/api/routes/ai.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/ai.py` | C-030 |
| `/src/cia_sie/api/routes/baskets.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/baskets.py` | C-030 |
| `/src/cia_sie/api/routes/charts.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/charts.py` | C-030 |
| `/src/cia_sie/api/routes/chat.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/chat.py` | C-030 |
| `/src/cia_sie/api/routes/instruments.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/instruments.py` | C-030 |
| `/src/cia_sie/api/routes/narratives.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/narratives.py` | C-030 |
| `/src/cia_sie/api/routes/platforms.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/platforms.py` | C-030 |
| `/src/cia_sie/api/routes/relationships.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/relationships.py` | C-030 |
| `/src/cia_sie/api/routes/signals.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/signals.py` | C-030 |
| `/src/cia_sie/api/routes/silos.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/silos.py` | C-030 |
| `/src/cia_sie/api/routes/strategy.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/strategy.py` | C-030 |
| `/src/cia_sie/api/routes/webhooks.py` | `/CIA-SIE-Pure/src/cia_sie/api/routes/webhooks.py` | C-030 |

#### /src/cia_sie/bridge/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/bridge/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/bridge/__init__.py` | C-029 |

#### /src/cia_sie/core/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/core/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/core/__init__.py` | C-029 |
| `/src/cia_sie/core/config.py` | `/CIA-SIE-Pure/src/cia_sie/core/config.py` | C-010 |
| `/src/cia_sie/core/enums.py` | `/CIA-SIE-Pure/src/cia_sie/core/enums.py` | C-012 |
| `/src/cia_sie/core/exceptions.py` | `/CIA-SIE-Pure/src/cia_sie/core/exceptions.py` | C-010 |
| `/src/cia_sie/core/models.py` | `/CIA-SIE-Pure/src/cia_sie/core/models.py` | C-008 |
| `/src/cia_sie/core/security.py` | `/CIA-SIE-Pure/src/cia_sie/core/security.py` | C-010 |

#### /src/cia_sie/dal/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/dal/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/dal/__init__.py` | C-029 |
| `/src/cia_sie/dal/database.py` | `/CIA-SIE-Pure/src/cia_sie/dal/database.py` | C-014 |
| `/src/cia_sie/dal/models.py` | `/CIA-SIE-Pure/src/cia_sie/dal/models.py` | C-008 |
| `/src/cia_sie/dal/repositories.py` | `/CIA-SIE-Pure/src/cia_sie/dal/repositories.py` | C-014 |

#### /src/cia_sie/exposure/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/exposure/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/exposure/__init__.py` | C-029 |
| `/src/cia_sie/exposure/confirmation_detector.py` | `/CIA-SIE-Pure/src/cia_sie/exposure/confirmation_detector.py` | C-010 |
| `/src/cia_sie/exposure/contradiction_detector.py` | `/CIA-SIE-Pure/src/cia_sie/exposure/contradiction_detector.py` | C-010 |
| `/src/cia_sie/exposure/relationship_exposer.py` | `/CIA-SIE-Pure/src/cia_sie/exposure/relationship_exposer.py` | C-010 |

#### /src/cia_sie/ingestion/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/ingestion/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/ingestion/__init__.py` | C-029 |
| `/src/cia_sie/ingestion/freshness.py` | `/CIA-SIE-Pure/src/cia_sie/ingestion/freshness.py` | C-010 |
| `/src/cia_sie/ingestion/signal_normalizer.py` | `/CIA-SIE-Pure/src/cia_sie/ingestion/signal_normalizer.py` | C-010 |
| `/src/cia_sie/ingestion/webhook_handler.py` | `/CIA-SIE-Pure/src/cia_sie/ingestion/webhook_handler.py` | C-010 |

#### /src/cia_sie/platforms/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/platforms/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/platforms/__init__.py` | C-029 |
| `/src/cia_sie/platforms/base.py` | `/CIA-SIE-Pure/src/cia_sie/platforms/base.py` | C-001 |
| `/src/cia_sie/platforms/kite.py` | `/CIA-SIE-Pure/src/cia_sie/platforms/kite.py` | C-001 |
| `/src/cia_sie/platforms/registry.py` | `/CIA-SIE-Pure/src/cia_sie/platforms/registry.py` | C-003 |
| `/src/cia_sie/platforms/tradingview.py` | `/CIA-SIE-Pure/src/cia_sie/platforms/tradingview.py` | C-002 |

#### /src/cia_sie/webhooks/
| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/src/cia_sie/webhooks/__init__.py` | `/CIA-SIE-Pure/src/cia_sie/webhooks/__init__.py` | C-029 |
| `/src/cia_sie/webhooks/tradingview_receiver.py` | `/CIA-SIE-Pure/src/cia_sie/webhooks/tradingview_receiver.py` | C-002 |

---

### Source: /tests/ → Destination: /CIA-SIE-Pure/tests/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/tests/__init__.py` | `/CIA-SIE-Pure/tests/__init__.py` | C-018 |
| `/tests/conftest.py` | `/CIA-SIE-Pure/tests/conftest.py` | C-018 |
| `/tests/backend/*` | `/CIA-SIE-Pure/tests/backend/*` | C-018 |
| `/tests/chaos/*` | `/CIA-SIE-Pure/tests/chaos/*` | C-018 |
| `/tests/constitutional/*` | `/CIA-SIE-Pure/tests/constitutional/*` | C-018 |
| `/tests/e2e/*` | `/CIA-SIE-Pure/tests/e2e/*` | C-018 |
| `/tests/integration/*` | `/CIA-SIE-Pure/tests/integration/*` | C-018 |
| `/tests/unit/*` | `/CIA-SIE-Pure/tests/unit/*` | C-018 |

**Total: ~63 test files**

---

### Source: /documentation/ → Destination: /CIA-SIE-Pure/docs/

**PRESERVE INTERNAL STRUCTURE**

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/documentation/01_GOVERNANCE/*` | `/CIA-SIE-Pure/docs/01_GOVERNANCE/*` | C-024 |
| `/documentation/02_ARCHITECTURE/*` | `/CIA-SIE-Pure/docs/02_ARCHITECTURE/*` | C-024 |
| `/documentation/03_SPECIFICATIONS/*` | `/CIA-SIE-Pure/docs/03_SPECIFICATIONS/*` | C-024 |
| `/documentation/04_AI_HANDOFF/*` | `/CIA-SIE-Pure/docs/04_AI_HANDOFF/*` | C-024 |
| `/documentation/05_DECISIONS/*` | `/CIA-SIE-Pure/docs/05_DECISIONS/*` | C-024 |
| `/documentation/06_AUDITS/*` | `/CIA-SIE-Pure/docs/06_AUDITS/*` | C-024 |
| `/documentation/07_MISSION_CONTROL/*` | `/CIA-SIE-Pure/docs/07_MISSION_CONTROL/*` | C-024 |
| `/documentation/07_TESTING/*` | `/CIA-SIE-Pure/docs/07_TESTING/*` | C-024 |
| `/documentation/08_OPERATIONS/*` | `/CIA-SIE-Pure/docs/08_OPERATIONS/*` | C-024 |
| `/documentation/09_FRONTEND QUERIES/*` | `/CIA-SIE-Pure/docs/09_FRONTEND QUERIES/*` | C-024 |
| `/documentation/AEROSPACE_SYSTEMS_MANUAL/*` | `/CIA-SIE-Pure/docs/AEROSPACE_SYSTEMS_MANUAL/*` | C-023 |
| `/documentation/CHART_01A_COMPLETE_PACKAGE/*` | `/CIA-SIE-Pure/docs/CHART_01A_COMPLETE_PACKAGE/*` | C-024 |
| `/documentation/CHART_02_COMPLETE_PACKAGE/*` | `/CIA-SIE-Pure/docs/CHART_02_COMPLETE_PACKAGE/*` | C-024 |
| `/documentation/LAUNCHER_SYSTEM_COMPLETE/*` | `/CIA-SIE-Pure/docs/LAUNCHER_SYSTEM_COMPLETE/*` | C-024 |
| `/documentation/prototypes/*` | `/CIA-SIE-Pure/docs/prototypes/*` | C-024 |
| `/documentation/QA_KNOWLEDGE_BASE/*` | `/CIA-SIE-Pure/docs/QA_KNOWLEDGE_BASE/*` | C-024 |
| `/documentation/*.md` | `/CIA-SIE-Pure/docs/*.md` | C-024 |
| `/documentation/*.html` | `/CIA-SIE-Pure/docs/*.html` | C-024 |

**Total: ~157 documentation files**

---

### Source: /alembic/ → Destination: /CIA-SIE-Pure/alembic/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/alembic/env.py` | `/CIA-SIE-Pure/alembic/env.py` | C-010 |
| `/alembic/script.py.mako` | `/CIA-SIE-Pure/alembic/script.py.mako` | C-010 |
| `/alembic/versions/*.py` | `/CIA-SIE-Pure/alembic/versions/*.py` | C-010 |

---

### Source: /scripts/ (non-launcher) → Destination: /CIA-SIE-Pure/scripts/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/scripts/extract_docx.py` | `/CIA-SIE-Pure/scripts/extract_docx.py` | C-025 |
| `/scripts/gold_correlation_chart.py` | `/CIA-SIE-Pure/scripts/gold_correlation_chart.py` | C-025 |

---

### Source: Root Scripts → Destination: /CIA-SIE-Pure/scripts/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/execute_all_tests_autonomous.py` | `/CIA-SIE-Pure/scripts/execute_all_tests_autonomous.py` | C-025 |
| `/extract_chat_history.py` | `/CIA-SIE-Pure/scripts/extract_chat_history.py` | C-025 |
| `/generate_chronicle.py` | `/CIA-SIE-Pure/scripts/generate_chronicle.py` | C-025 |
| `/run_comprehensive_tests.py` | `/CIA-SIE-Pure/scripts/run_comprehensive_tests.py` | C-025 |
| `/run_quick_tests.py` | `/CIA-SIE-Pure/scripts/run_quick_tests.py` | C-025 |
| `/seed_sample_data.py` | `/CIA-SIE-Pure/scripts/seed_sample_data.py` | C-025 |

---

### Source: Root Config → Destination: /CIA-SIE-Pure/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/alembic.ini` | `/CIA-SIE-Pure/alembic.ini` | C-027 |
| `/pyproject.toml` | `/CIA-SIE-Pure/pyproject.toml` | C-027 |

---

### Source: /data/ → Destination: /CIA-SIE-Pure/data/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/data/cia_sie.db` | `/CIA-SIE-Pure/data/cia_sie.db` | C-010 |

---

### Source: /docs/ → Destination: /CIA-SIE-Pure/docs/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/docs/audits/*.html` | `/CIA-SIE-Pure/docs/audits/*.html` | C-024 |
| `/docs/*.png` | `/CIA-SIE-Pure/docs/*.png` | C-024 |

---

### Source: /chat_history_export/ → Destination: /CIA-SIE-Pure/docs/chat_history_export/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/chat_history_export/*` | `/CIA-SIE-Pure/docs/chat_history_export/*` | C-024 |

**Total: 37 files — historical chat logs preserved as documentation**

---

## MERCURY DESTINATIONS (LIFT OPERATION)

**SPECIAL INSTRUCTION:** Per CEAD v2.0 Section 3.2, LIFT entire `/projects/mercury/` to `/Mercury/`

### Mercury LIFT Strategy

```
/projects/mercury/  →  /Mercury/

PRESERVE ALL INTERNAL STRUCTURE:
├── /src/mercury/       → /Mercury/src/mercury/
├── /tests/             → /Mercury/tests/
├── /documentation/     → /Mercury/documentation/
├── /scripts/           → /Mercury/scripts/
├── pyproject.toml      → /Mercury/pyproject.toml
├── README.md           → /Mercury/README.md
├── requirements.txt    → /Mercury/requirements.txt
└── start-mercury.command → /Mercury/start-mercury.command
```

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/projects/mercury/*` | `/Mercury/*` | M-021 |

**Total: 56 files — LIFT operation**

---

## COMMAND-CONTROL DESTINATIONS

### Source: /scripts/launcher/ → Destination: /Command-Control/scripts/shell/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/scripts/launcher/config.sh` | `/Command-Control/scripts/shell/config.sh` | CC-004 |
| `/scripts/launcher/health-check.sh` | `/Command-Control/scripts/shell/health-check.sh` | CC-009 |
| `/scripts/launcher/ignite.sh` | `/Command-Control/scripts/shell/ignite.sh` | CC-004 |
| `/scripts/launcher/shutdown.sh` | `/Command-Control/scripts/shell/shutdown.sh` | CC-005 |
| `/scripts/launcher/utils.sh` | `/Command-Control/scripts/shell/utils.sh` | CC-004 |

### Source: Root .command files → Destination: /Command-Control/scripts/macos/

| Source Path | Destination Path | Rule |
|-------------|------------------|------|
| `/start-cia-sie.command` | `/Command-Control/scripts/macos/start-cia-sie.command` | CC-001 |
| `/stop-cia-sie.command` | `/Command-Control/scripts/macos/stop-cia-sie.command` | CC-002 |

**Total: 7 CLI files**

---

## QUARANTINE DESTINATIONS

### Source: /logs/ → Destination: /quarantine/debug-logs/

| Source Path | Destination Path | Reason |
|-------------|------------------|--------|
| `/logs/backend.log` | `/quarantine/debug-logs/backend.log` | Q-011 |
| `/logs/cia_sie.log` | `/quarantine/debug-logs/cia_sie.log` | Q-011 |
| `/logs/launcher.log` | `/quarantine/debug-logs/launcher.log` | Q-011 |
| `/logs/ngrok.log` | `/quarantine/debug-logs/ngrok.log` | Q-011 |

### Source: /Duplicates for Deletion/ → Destination: /quarantine/duplicates/

| Source Path | Destination Path | Reason |
|-------------|------------------|--------|
| `/Duplicates for Deletion/*` | `/quarantine/duplicates/*` | Q-004 |

**Note:** This includes 9 .puml files, 2 root_level files, and 1 .md file

### Source: Workspace/Config → Destination: /quarantine/unclassified/

| Source Path | Destination Path | Reason |
|-------------|------------------|--------|
| `/CIA-SIE-PURE.code-workspace` | `/quarantine/unclassified/CIA-SIE-PURE.code-workspace` | Q-006 |

### Existing Quarantine (PRESERVE)

| Source Path | Status |
|-------------|--------|
| `/quarantine/EMPTY_MODULE_QUARANTINED.py` | PRESERVE |
| `/quarantine/README.md` | PRESERVE |
| `/quarantine/SANITISATION_AUDIT_REPORT.md` | PRESERVE |
| `/quarantine/STUB_FUNCTIONS_QUARANTINED.py` | PRESERVE |

---

## ROOT FILES — POST-MIGRATION

These files will be at repository root after migration:

| File | Source | Status |
|------|--------|--------|
| `MASTER-README.md` | GENERATE | Phase 7 |
| `ARCHITECTURE-OVERVIEW.md` | GENERATE | Phase 7 |
| `MIGRATION-REPORT.md` | GENERATE | Phase 7 |
| `.gitignore` | PRESERVE | Already at root |
| `.git/` | PRESERVE | DO NOT TOUCH |
| `CEAD-v2.0-*.md` | `/migration-logs/` | Reference doc |
| `CURSOR-ENGAGEMENT-*.md` | `/migration-logs/` | Reference doc |

---

## SHARED RESOURCES

**Assessment:** No files identified as genuinely shared between multiple projects.

All cross-references are:
- Mercury calling CIA-SIE-Pure APIs (via HTTP, not shared code)
- Command-Control launching both systems (via shell, not shared code)

**Result:** `/shared/` will be created but empty initially.

---

## EMPTY DIRECTORIES — SPECIAL HANDLING

| Directory | Action |
|-----------|--------|
| `/context/decisions/` | Quarantine as empty (Q-007) or add .gitkeep |
| `/pids/` | Quarantine as empty (Q-007) — runtime artifact |
| `/prompts/` | Quarantine as empty (Q-007) — placeholder |
| `/tests/frontend/` | Add .gitkeep — future test location |

---

## PHASE 2 CHECKPOINT CONFIRMATION

| # | Criterion | Status |
|---|-----------|--------|
| 2.1 | Every file analysed | ✅ COMPLETE |
| 2.2 | Every file assigned destination | ✅ COMPLETE |
| 2.3 | Classification map generated | ✅ THIS DOCUMENT |
| 2.4 | Mercury LIFT strategy confirmed | ✅ LIFT /projects/mercury/ → /Mercury/ |
| 2.5 | Quarantine items identified with reasons | ✅ ~20 items |

---

## PHASE 2 OUTPUT MESSAGE

```
═══════════════════════════════════════════════════════════════════════════════
                    PHASE 2 COMPLETE: CLASSIFICATION
═══════════════════════════════════════════════════════════════════════════════

Files Classified: ~350+

DESTINATION BREAKDOWN:
├── CIA-SIE-Pure:    ~270 files
│   ├── /src/cia_sie/: 50 files
│   ├── /tests/:       63 files
│   ├── /docs/:        157+ files
│   ├── /alembic/:     4 files
│   └── /scripts/:     8 files
│
├── Mercury:         ~56 files (LIFT OPERATION)
│   └── Entire /projects/mercury/ lifted intact
│
├── Command-Control: ~10 files
│   ├── /scripts/shell/: 5 files
│   └── /scripts/macos/: 2 files + README
│
├── shared:          0 files (none identified)
│
└── quarantine:      ~20 files
    ├── /debug-logs/: 4 log files
    ├── /duplicates/: 12 pre-flagged
    ├── /unclassified/: 1 workspace file
    └── /empty-files/: 3 empty dirs

Mercury LIFT Strategy: CONFIRMED
├── Source: /projects/mercury/
├── Destination: /Mercury/
└── Method: LIFT entire directory tree

READY FOR PHASE 3: STRUCTURE CREATION

═══════════════════════════════════════════════════════════════════════════════
```

---

*Generated per CEAD v2.0 Section 9 Phase 2 | January 13, 2026*
