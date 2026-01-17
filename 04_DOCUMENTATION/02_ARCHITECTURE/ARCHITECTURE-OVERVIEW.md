# CIA-SIE Ecosystem — Architecture Overview

## Post-Restructuring System Design

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CIA-SIE ECOSYSTEM                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐   │
│   │                     │     │                     │     │                     │   │
│   │    CIA-SIE-Pure     │     │       Mercury       │     │   Command-Control   │   │
│   │    (Backend)        │     │     (Frontend)      │     │    (Operations)     │   │
│   │                     │     │                     │     │                     │   │
│   │  ┌───────────────┐  │     │  ┌───────────────┐  │     │  ┌───────────────┐  │   │
│   │  │  FastAPI      │  │◄────┼──│  WebSocket    │  │     │  │  Shell        │  │   │
│   │  │  REST API     │  │HTTP │  │  Chat Client  │  │     │  │  Scripts      │  │   │
│   │  └───────────────┘  │     │  └───────────────┘  │     │  └───────────────┘  │   │
│   │         │           │     │         │           │     │         │           │   │
│   │  ┌───────────────┐  │     │  ┌───────────────┐  │     │  ┌───────────────┐  │   │
│   │  │  SQLAlchemy   │  │     │  │  AI Engine    │  │     │  │  .command     │  │   │
│   │  │  Database     │  │     │  │  Chat Logic   │  │     │  │  Launchers    │  │   │
│   │  └───────────────┘  │     │  └───────────────┘  │     │  └───────────────┘  │   │
│   │         │           │     │         │           │     │         │           │   │
│   │  ┌───────────────┐  │     │  ┌───────────────┐  │     │  ┌───────────────┐  │   │
│   │  │  Claude AI    │  │     │  │  Kite Connect │  │     │  │  Health       │  │   │
│   │  │  Integration  │  │     │  │  Market Data  │  │     │  │  Checks       │  │   │
│   │  └───────────────┘  │     │  └───────────────┘  │     │  └───────────────┘  │   │
│   │                     │     │                     │     │                     │   │
│   └─────────────────────┘     └─────────────────────┘     └─────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Domain Sovereignty

Each domain operates independently with no compile-time dependencies:

### Communication Patterns

| From | To | Method | Purpose |
|------|----|--------|---------|
| Mercury | CIA-SIE-Pure | HTTP REST | API calls, data retrieval |
| Mercury | CIA-SIE-Pure | WebSocket | Real-time updates |
| Command-Control | CIA-SIE-Pure | Process spawn | System launch |
| Command-Control | Mercury | Process spawn | Frontend launch |

**Key Principle:** No `import` statements cross domain boundaries. All inter-domain communication happens at runtime via network protocols or process management.

---

## CIA-SIE-Pure Architecture

### Module Structure

```
CIA-SIE-Pure/src/cia_sie/
├── __init__.py              # Package initialization
├── main.py                  # Application entry point
│
├── api/                     # REST API Layer
│   ├── app.py               # FastAPI application
│   └── routes/              # Endpoint handlers
│       ├── ai.py            # AI/Claude endpoints
│       ├── baskets.py       # Basket management
│       ├── charts.py        # Chart data
│       ├── chat.py          # Chat interface
│       ├── instruments.py   # Financial instruments
│       ├── narratives.py    # AI narratives
│       ├── platforms.py     # Platform registry
│       ├── relationships.py # Entity relationships
│       ├── signals.py       # Signal management
│       ├── silos.py         # Data silos
│       ├── strategy.py      # Strategy endpoints
│       └── webhooks.py      # External webhooks
│
├── ai/                      # AI Integration Layer
│   ├── claude_client.py     # Anthropic API client
│   ├── model_registry.py    # AI model management
│   ├── narrative_generator.py # Narrative creation
│   ├── prompt_builder.py    # Prompt engineering
│   ├── response_validator.py # Constitutional validation
│   └── usage_tracker.py     # API usage metrics
│
├── core/                    # Core Utilities
│   ├── config.py            # Configuration management
│   ├── enums.py             # Enumeration types
│   ├── exceptions.py        # Custom exceptions
│   ├── models.py            # Pydantic models
│   └── security.py          # Security utilities
│
├── dal/                     # Data Access Layer
│   ├── database.py          # SQLAlchemy engine
│   ├── models.py            # ORM models
│   └── repositories.py      # Data repositories
│
├── exposure/                # Relationship Analysis
│   ├── confirmation_detector.py
│   ├── contradiction_detector.py
│   └── relationship_exposer.py
│
├── ingestion/               # Signal Ingestion
│   ├── freshness.py         # Data freshness tracking
│   ├── signal_normalizer.py # Signal normalization
│   └── webhook_handler.py   # Webhook processing
│
├── platforms/               # Platform Adapters
│   ├── base.py              # Abstract base
│   ├── kite.py              # Kite Connect
│   ├── registry.py          # Platform registry
│   └── tradingview.py       # TradingView
│
└── webhooks/                # Webhook Receivers
    └── tradingview_receiver.py
```

### Request Flow

```
User Request → FastAPI Router → Route Handler → Service Layer → DAL → Database
                                     ↓
                              AI Integration (optional)
                                     ↓
                              Response Builder → JSON Response
```

---

## Mercury Architecture

### Module Structure

```
Mercury/src/mercury/
├── __init__.py              # Package initialization
├── main.py                  # Application entry point
│
├── api/                     # Web API Layer
│   └── app.py               # FastAPI + WebSocket
│
├── ai/                      # AI Engine
│   ├── __init__.py
│   └── engine.py            # Claude integration
│
├── chat/                    # Chat Logic
│   ├── __init__.py
│   └── engine.py            # Conversation management
│
├── core/                    # Core Services
│   ├── __init__.py          # Module exports
│   ├── features.py          # Feature flags
│   ├── health.py            # Health checks
│   ├── logging.py           # Logging configuration
│   ├── metrics.py           # Usage metrics
│   ├── resilience.py        # Circuit breakers
│   ├── startup.py           # API verification
│   └── validation.py        # Input validation
│
├── interface/               # User Interfaces
│   ├── __init__.py
│   └── repl.py              # Terminal REPL
│
└── kite/                    # Market Data
    ├── __init__.py
    └── adapter.py           # Kite Connect adapter
```

### Launch Readiness Flow

```
Application Start
       ↓
┌──────────────────────────────────────────────────────────┐
│                    perform_launch_readiness_check()       │
├──────────────────────────────────────────────────────────┤
│  1. verify_kite_api()                                     │
│     ├── Check API key presence                            │
│     ├── Validate access token                             │
│     └── Test connection                                   │
│                                                           │
│  2. verify_anthropic_api()                                │
│     ├── Check API key presence                            │
│     ├── Validate key format                               │
│     └── Send test message                                 │
│                                                           │
│  3. Aggregate status → LaunchReadiness object             │
└──────────────────────────────────────────────────────────┘
       ↓
WebSocket Server Ready (port 8001)
```

---

## Command-Control Architecture

### Script Structure

```
Command-Control/scripts/
├── macos/
│   ├── start-cia-sie.command   # Double-click launcher
│   └── stop-cia-sie.command    # System shutdown
│
└── shell/
    ├── config.sh               # Configuration variables
    ├── health-check.sh         # Service health verification
    ├── ignite.sh               # System startup sequence
    ├── shutdown.sh             # Graceful shutdown
    └── utils.sh                # Utility functions
```

### Launch Sequence

```
start-cia-sie.command
       ↓
    ignite.sh
       ↓
┌──────────────────────────────────────────────────────────┐
│  1. Load config.sh                                        │
│  2. Activate virtual environment                          │
│  3. Start CIA-SIE-Pure backend (port 8000)                │
│  4. Wait for backend health                               │
│  5. Start Mercury frontend (port 8001)                    │
│  6. Run health-check.sh                                   │
│  7. Report status                                         │
└──────────────────────────────────────────────────────────┘
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   External Sources                                                          │
│   ┌─────────────┐     ┌─────────────┐                                       │
│   │ TradingView │     │    Kite     │                                       │
│   │  Webhooks   │     │   Connect   │                                       │
│   └──────┬──────┘     └──────┬──────┘                                       │
│          │                   │                                              │
│          ▼                   ▼                                              │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │                      CIA-SIE-Pure                               │       │
│   │  ┌────────────┐    ┌────────────┐    ┌────────────┐             │       │
│   │  │  Webhook   │───▶│  Signal    │───▶│  Database  │             │       │
│   │  │  Handler   │    │ Normalizer │    │    (DAL)   │             │       │
│   │  └────────────┘    └────────────┘    └────────────┘             │       │
│   │                           │                │                     │       │
│   │                           ▼                ▼                     │       │
│   │                    ┌────────────┐    ┌────────────┐             │       │
│   │                    │  Exposure  │    │    API     │◄────────┐   │       │
│   │                    │  Engine    │    │  Endpoints │         │   │       │
│   │                    └────────────┘    └────────────┘         │   │       │
│   └─────────────────────────────────────────────┬───────────────┘   │       │
│                                                 │                   │       │
│                                                 │ HTTP/WS           │       │
│                                                 ▼                   │       │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │                         Mercury                                 │       │
│   │  ┌────────────┐    ┌────────────┐    ┌────────────┐             │       │
│   │  │  WebSocket │◄───│    Chat    │◄───│     AI     │             │       │
│   │  │   Server   │    │   Engine   │    │   Engine   │             │       │
│   │  └────────────┘    └────────────┘    └────────────┘             │       │
│   │        │                                    │                   │       │
│   └────────┼────────────────────────────────────┼───────────────────┘       │
│            │                                    │                           │
│            ▼                                    ▼                           │
│   ┌─────────────┐                      ┌─────────────┐                      │
│   │    User     │                      │   Claude    │                      │
│   │  Interface  │                      │     API     │                      │
│   └─────────────┘                      └─────────────┘                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Constitutional Compliance Layer

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CONSTITUTIONAL COMPLIANCE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   CR-001: No Investment Recommendations                                     │
│   ├── response_validator.py enforces                                        │
│   └── Tests: test_cr001_no_recommendations.py                               │
│                                                                             │
│   CR-002: Equal Visual Weight                                               │
│   ├── Balanced presentation required                                        │
│   └── Tests: test_cr002_equal_visual_weight.py                              │
│                                                                             │
│   CR-003: Mandatory Disclaimer                                              │
│   ├── All responses include disclaimer                                      │
│   └── Tests: test_cr003_mandatory_disclaimer.py                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Port Allocation

| Service | Port | Domain |
|---------|------|--------|
| CIA-SIE-Pure Backend | 8000 | CIA-SIE-Pure |
| Mercury Frontend | 8001 | Mercury |
| PostgreSQL (if used) | 5432 | External |

---

## Technology Stack Summary

| Component | Technology | Location |
|-----------|------------|----------|
| Backend API | FastAPI 0.100+ | CIA-SIE-Pure |
| ORM | SQLAlchemy 2.0+ | CIA-SIE-Pure |
| Migrations | Alembic | CIA-SIE-Pure |
| AI | Anthropic Claude | CIA-SIE-Pure, Mercury |
| Market Data | Kite Connect | CIA-SIE-Pure, Mercury |
| Frontend Server | Uvicorn | Mercury |
| WebSocket | FastAPI WebSocket | Mercury |
| CLI | REPL | Mercury |
| Operations | Bash, .command | Command-Control |

---

*Generated per CEAD v2.0 Phase 7 | January 13, 2026*
