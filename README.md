# CIA-SIE: Chart Intelligence Auditor & Signal Intelligence Engine

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CIA-SIE Platform                                                            ║
║   Version: 2.3.0                                                              ║
║   Status: Active Development                                                  ║
║                                                                               ║
║   A Data Repository for Trading Signal Intelligence                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## Overview

CIA-SIE (Chart Intelligence Auditor & Signal Intelligence Engine) is a **Data Repository Platform** designed to store, organize, and describe trading signals from multiple sources without aggregation, scoring, or automated recommendations.

### Core Philosophy

> **"The system shall NEVER aggregate, weight, score, or combine signals to produce composite indicators, recommendations, or trade directions."**
> — Gold Standard Specification, Section 0C

CIA-SIE follows a strict **Data Repository Model** where:
- All signals are stored with full fidelity
- Contradictions are exposed, not resolved
- AI provides descriptive narratives only
- Users retain complete decision-making authority

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   THE FUNDAMENTAL PRINCIPLE                                                 │
│                                                                             │
│   • Decision-support, NOT decision-making                                   │
│   • Expose contradictions, NEVER resolve them                               │
│   • Descriptive AI, NOT prescriptive AI                                     │
│   • Data Repository model, NOT Intelligence Engine                          │
│   • No aggregation, scoring, weighting, or recommendations                  │
│   • User retains ALL judgment and decision authority                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Features

### Implemented (v2.3.0)

| Feature | Description |
|---------|-------------|
| **Signal Ingestion** | Webhook-based signal reception from TradingView |
| **Instrument Management** | Full CRUD for instruments, silos, charts |
| **Contradiction Detection** | Automatic identification of conflicting signals |
| **Confirmation Detection** | Automatic identification of aligned signals |
| **Freshness Calculation** | CURRENT / RECENT / STALE signal aging |
| **AI Narratives** | Claude-powered descriptive analysis |
| **Analytical Baskets** | UI-layer grouping for organization |
| **Command Center** | React/TypeScript dashboard |
| **Model Selection** | Choose between Haiku, Sonnet, or Opus |

### In Development

| Feature | Priority | Status |
|---------|----------|--------|
| Platform Adapter System | HIGH | Planned |
| TradingView Watchlist Import | HIGH | Planned |
| Kite Connect Integration | MEDIUM | Planned |

## Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend (React)                           │
│  TypeScript │ Vite │ TailwindCSS │ React Query                 │
├─────────────────────────────────────────────────────────────────┤
│                      Backend (FastAPI)                          │
│  Python 3.11 │ SQLAlchemy │ Pydantic │ Uvicorn                 │
├─────────────────────────────────────────────────────────────────┤
│                      Database (SQLite)                          │
│  Self-contained │ Portable │ Backup-friendly                   │
├─────────────────────────────────────────────────────────────────┤
│                      AI Integration                             │
│  Anthropic Claude │ Haiku/Sonnet/Opus │ Descriptive Only       │
├─────────────────────────────────────────────────────────────────┤
│                      External Access                            │
│  ngrok Tunnel │ Webhook Reception │ HTTPS                      │
└─────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
CIA-SIE/
├── src/                    # Backend source code
│   └── cia_sie/
│       ├── api/            # FastAPI routes
│       ├── core/           # Domain models, enums, config
│       ├── dal/            # Data access layer (SQLAlchemy)
│       ├── ingestion/      # Webhook handling, signal normalization
│       ├── exposure/       # Contradiction/Confirmation detection
│       ├── ai/             # Claude integration
│       └── services/       # Business logic
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API client
│   │   └── types/          # TypeScript types
│   └── node_modules/       # Dependencies
├── venv/                   # Python virtual environment
├── data/                   # SQLite database
├── logs/                   # Application logs
├── specifications/         # Architecture documents
├── context/                # Development context
│   ├── decisions/          # ADRs
│   └── sessions/           # Session summaries
└── assets/                 # GUI mockups
```

## Quick Start

### Prerequisites

- macOS (tested on Darwin 23.4.0)
- Python 3.11+
- Node.js 18+
- Anthropic API Key

### Starting the Platform

```bash
# 1. Activate Python virtual environment
source .venv/bin/activate

# 2. Start the backend (port 8000)
cd src && uvicorn cia_sie.main:app --reload --port 8000 &

# 3. Start the frontend (port 3000)
cd frontend && npm run dev &

# 4. (Optional) Start ngrok tunnel for webhook reception
ngrok http 8000
```

### Stopping the Platform

```bash
# Stop frontend and backend
pkill -f "uvicorn"
pkill -f "vite"

# Or use Ctrl+C in the respective terminal windows
```

### Checking Status

```bash
# Check if backend is running
curl -s http://localhost:8000/health

# Check if frontend is running
curl -s http://localhost:3000
```

## Configuration

### Environment Variables

Create `.env` in the project root:

```env
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
NGROK_AUTHTOKEN=your_ngrok_token
DATABASE_URL=sqlite:///./data/cia_sie.db
```

### AI Model Selection

| Model | Use Case | Cost (per 1M tokens) |
|-------|----------|---------------------|
| Haiku | Simple queries | $0.25 input / $1.25 output |
| Sonnet | Balanced analysis | $3.00 input / $15.00 output |
| Opus | Complex analysis | $15.00 input / $75.00 output |

## API Endpoints

### Health Check
```
GET /health
```

### Signals
```
POST /api/v1/webhook/           # Receive signal (TradingView format)
GET  /api/v1/signals            # List signals
```

### Instruments
```
GET    /api/v1/instruments/     # List instruments
POST   /api/v1/instruments/     # Create instrument
GET    /api/v1/instruments/{id} # Get instrument
PUT    /api/v1/instruments/{id} # Update instrument
DELETE /api/v1/instruments/{id} # Delete instrument
```

### Relationships
```
GET /api/v1/relationships/silo/{id}  # Get silo relationships
```

### AI Narratives
```
GET /api/v1/narratives/silo/{id}     # Generate AI narrative
```

### Baskets
```
GET /api/v1/baskets/                 # List analytical baskets
```

## Signal Format

TradingView alerts should send JSON in this format:

```json
{
  "webhook_id": "SAMPLE_01A",
  "direction": "BULLISH",
  "rsi": 28.5,
  "macd": 0.12,
  "ema9": 52.30,
  "ema21": 51.80,
  "message": "RSI oversold condition detected"
}
```

## Development

### Running Tests

```bash
# Backend tests
cd src && pytest

# With coverage
pytest --cov=cia_sie

# Frontend tests
cd frontend && npm test
```

### Code Style

- Backend: Black, isort, mypy
- Frontend: ESLint, Prettier

## Constitutional Principles

The system operates under strict constitutional constraints defined in the Gold Standard Specification:

### Prohibited (PR-xx)

- PR-01: No automated buy/sell/hold recommendations
- PR-02: No proprietary signal weighting
- PR-03: No "confidence scores"
- PR-04: No signal aggregation
- PR-05: No predictive scoring
- PR-06: No trade direction inference

### Mandated (MN-xx)

- MN-01: Full signal exposure
- MN-02: Contradiction visibility
- MN-03: Freshness display
- MN-04: Descriptive AI only
- MN-05: User authority preservation

## Key Design Decisions

1. **ADR-001**: Data Repository Model (not Intelligence Engine)
2. **ADR-002**: Self-Contained Workspace Architecture
3. **ADR-003**: Dynamic AI Model Selection

See `context/decisions/` for detailed Architecture Decision Records.

## Documentation

| Document | Location |
|----------|----------|
| Gold Standard Specification | specifications/architecture/ |
| Implementation Roadmap | specifications/architecture/ |
| Architecture Decision Records | context/decisions/ |
| Session Summaries | context/sessions/ |
| GUI Mockup | assets/mockups/ |

## License

Proprietary - All Rights Reserved

## Author

**Neville Mehta** - Project Principal

---

**IMPORTANT**: This system provides decision support, not recommendations. All trading decisions are entirely yours.

*Built with Claude Opus 4.5 | December 2025*
