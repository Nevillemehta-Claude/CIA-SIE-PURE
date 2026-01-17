# CIA-SIE Ecosystem

## Sovereign Project Domains — Post-Restructuring Architecture

---

## Overview

The CIA-SIE (Chart Intelligence Assistant - Signal Intelligence Engine) Ecosystem has been restructured into three sovereign, independently deployable project domains following CEAD v2.0 (Cursor Engagement Alignment Document) specifications.

This restructuring enables:
- **Clear architectural boundaries** between system components
- **Independent development, testing, and deployment** of each domain
- **Zero cross-contamination** between projects
- **Audit-ready, navigable documentation** structure

---

## Domain Structure

```
CIA-SIE-PURE/
├── CIA-SIE-Pure/           # Primary Domain — Backend Intelligence Engine
├── Mercury/                # Frontend Domain — Chat Interface
├── Command-Control/        # Operations Domain — CLI & Launchers
├── shared/                 # Cross-project resources (currently empty)
├── quarantine/             # Isolated items for review
└── migration-logs/         # Restructuring audit trail
```

---

## Domain Descriptions

### 🔷 CIA-SIE-Pure (Primary Domain)

The core backend intelligence engine providing:
- **FastAPI REST API** — Signal ingestion, basket management, AI narratives
- **SQLAlchemy ORM** — PostgreSQL/SQLite database access
- **Anthropic Claude Integration** — Intelligent response generation
- **Constitutional Compliance** — Regulatory safeguards

**Quick Start:**
```bash
cd CIA-SIE-Pure
pip install -e .
python -m cia_sie
```

**Key Directories:**
| Path | Purpose |
|------|---------|
| `/src/cia_sie/` | Core application code |
| `/tests/` | Unit, integration, constitutional tests |
| `/docs/` | Technical documentation |
| `/alembic/` | Database migrations |

---

### 🟠 Mercury (Frontend Domain)

The conversational frontend interface providing:
- **WebSocket Chat** — Real-time AI-powered conversations
- **Kite Connect Integration** — Market data access
- **Launch Readiness System** — API authentication verification
- **Terminal REPL** — Command-line interface alternative

**Quick Start:**
```bash
cd Mercury
pip install -e .
python -m mercury --web
```

**Key Directories:**
| Path | Purpose |
|------|---------|
| `/src/mercury/` | Core frontend code |
| `/tests/` | Frontend test suite |
| `/documentation/` | 12-chapter modular compendium |
| `/static/` | HTML/CSS assets |

---

### 🟢 Command-Control (Operations Domain)

Operational scripts and launchers providing:
- **Shell Scripts** — System ignition, shutdown, health checks
- **macOS Commands** — Double-click launch files
- **Configuration** — Environment setup

**Quick Start:**
```bash
# Double-click or:
./Command-Control/scripts/macos/start-cia-sie.command
```

**Key Directories:**
| Path | Purpose |
|------|---------|
| `/scripts/shell/` | Bash launcher scripts |
| `/scripts/macos/` | macOS .command files |

---

## System Launch

### Option 1: Composite Launch (Recommended)

From the repository root:
```bash
./Command-Control/scripts/macos/start-cia-sie.command
```

This will:
1. Start CIA-SIE-Pure backend (port 8000)
2. Start Mercury frontend (port 8001)
3. Perform health checks

### Option 2: Independent Domain Launch

**Backend Only:**
```bash
cd CIA-SIE-Pure && python -m cia_sie
```

**Frontend Only:**
```bash
cd Mercury && python -m mercury --web
```

---

## Documentation Structure

| Location | Content |
|----------|---------|
| `/CIA-SIE-Pure/docs/` | Backend technical documentation |
| `/Mercury/documentation/` | Frontend modular compendium |
| `/Command-Control/docs/` | Operations guides |
| `/migration-logs/` | CEAD v2.0 restructuring audit trail |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI, Uvicorn |
| Database | SQLAlchemy, Alembic |
| AI | Anthropic Claude |
| Market Data | Kite Connect |
| Frontend | HTML, WebSocket, REPL |
| Operations | Bash, macOS .command |

---

## Restructuring Reference

This repository was restructured on **January 13, 2026** following CEAD v2.0 specifications:

- **Phases Completed:** 9
- **Files Migrated:** 549
- **Hash Verification:** ✅ Zero data loss
- **Domain Isolation:** ✅ Confirmed

Full audit trail available in `/migration-logs/`:
- `phase-1-inventory.md` — File inventory with hashes
- `phase-2-classification.md` — Destination assignments
- `phase-3-structure.md` — Directory creation log
- `phase-4-migration.md` — File movement log
- `phase-5-path-resolution.md` — Import analysis
- `phase-6-validation.md` — Hash verification
- `CEAD-v2.0-*.md` — Original directive document

---

## License & Governance

Refer to `/CIA-SIE-Pure/docs/01_GOVERNANCE/` for:
- Constitutional requirements
- Regulatory compliance
- Operational governance

---

*Generated per CEAD v2.0 Phase 7 | January 13, 2026*
