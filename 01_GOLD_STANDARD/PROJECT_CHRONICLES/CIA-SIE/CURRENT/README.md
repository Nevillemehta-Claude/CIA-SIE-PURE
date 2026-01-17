# PROJECT CHRONICLE: CIA-SIE
## Comprehensive Implementation Reference

**Project Name:** CIA-SIE (Chart Intelligence Aggregator - Signal Integration Engine)
**Chronicle Type:** PROJECT-SPECIFIC (Not part of Gold Standard Bible)
**Version:** 4.0.0
**Status:** Active Development
**Last Updated:** January 14, 2026

---

## IMPORTANT NOTICE

This is a **PROJECT CHRONICLE**, not part of the Gold Standard Bible.

- Bible = Universal principles (project-agnostic)
- Chronicle = Project-specific implementation details

When using AI assistants, provide:
1. `COMMAND_PROTOCOL/00_GENESIS.md` (operating framework)
2. Relevant `BIBLE_MODULES/` (universal standards)
3. This Chronicle (project-specific context)

---

## THE INTELLIGENCE TRIAD VISION

CIA-SIE is the first pillar of a **Contextual Market Intelligence Platform**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE INTELLIGENCE TRIAD                        │
├─────────────────────────────────────────────────────────────────┤
│    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐
│    │   CIA-SIE       │    │   KITE API      │    │   CLAUDE    │
│    │   SIGNALS       │    │   MARKET DATA   │    │   REASONING │
│    │                 │    │                 │    │             │
│    │ • TradingView   │    │ • Live quotes   │    │ • Intent    │
│    │ • Directions    │    │ • Historical    │    │   parsing   │
│    │ • Indicators    │    │ • Instruments   │    │ • Query     │
│    │ • Freshness     │    │ • Positions     │    │   planning  │
│    │ • Contra/Conf   │    │ • Volume        │    │ • Synthesis │
│    └────────┬────────┘    └────────┬────────┘    └──────┬──────┘
│             │                      │                    │       │
│             └──────────────────────┼────────────────────┘       │
│                                    ▼                            │
│                    CONTEXTUAL INTELLIGENCE                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## PROJECT OVERVIEW

### What CIA-SIE Is

CIA-SIE is a **Data Repository Platform** that aggregates trading chart signals into a single organized interface. It is explicitly NOT an intelligence engine - it provides information without interpretation.

### The Three Constitutional Rules

**These are INVIOLABLE and RUNTIME-ENFORCED:**

| Rule | Principle | Code Enforcement |
|------|-----------|------------------|
| **CR-001** | No Recommendations | 31 prohibited regex patterns in `response_validator.py` |
| **CR-002** | Never Resolve Contradictions | `ContradictionDetector` exposes, never resolves |
| **CR-003** | Mandatory Disclaimer | 5-layer enforcement pipeline |

---

## CONSTITUTIONAL RULE IMPLEMENTATIONS

### CR-001: 31 Prohibited Patterns

Implemented in `response_validator.py`:

```python
PROHIBITED_PATTERNS = [
    # Category 1: Recommendation Language (7 patterns)
    (r"\byou\s+should\b", "implies recommendation", "CRITICAL"),
    (r"\bi\s+recommend\b", "direct recommendation", "CRITICAL"),
    (r"\bconsider\s+\w+ing\b", "suggests action", "CRITICAL"),
    (r"\bit\s+would\s+be\s+wise\b", "advisory language", "CRITICAL"),
    (r"\byou\s+might\s+want\b", "suggestion pattern", "CRITICAL"),
    (r"\bi\s+suggest\b", "direct suggestion", "CRITICAL"),
    (r"\bi\s+advise\b", "advisory language", "CRITICAL"),

    # Category 2: Trading Action Language (5 patterns)
    (r"\bbuy\s+now\b", "trading directive", "CRITICAL"),
    (r"\benter\s+long\b", "position directive", "CRITICAL"),
    (r"\benter\s+short\b", "position directive", "CRITICAL"),
    (r"\btake\s+profit\b", "trading directive", "CRITICAL"),
    (r"\bstop\s+loss\s+at\b", "trading directive", "CRITICAL"),

    # Category 3: Aggregation Language (5 patterns)
    (r"\boverall\s+direction\b", "aggregation", "MODERATE"),
    (r"\bconsensus\b", "aggregation", "MODERATE"),
    (r"\bnet\s+signal\b", "aggregation", "MODERATE"),
    (r"\bcombined\s+view\b", "aggregation", "MODERATE"),
    (r"\bbalance\s+of\s+signals\b", "aggregation", "MODERATE"),

    # Category 4: Confidence/Probability (5 patterns)
    (r"confidence:\s*\d+%", "confidence score", "CRITICAL"),
    (r"\blikely\s+to\s+rise\b", "prediction", "CRITICAL"),
    (r"\bprobably\s+will\b", "probability statement", "CRITICAL"),
    (r"\b\d+%\s+chance\b", "probability", "CRITICAL"),
    (r"\bhigh\s+probability\b", "probability assessment", "CRITICAL"),

    # Category 5: Prediction Language (4 patterns)
    (r"\bwill\s+rise\b", "prediction", "CRITICAL"),
    (r"\bwill\s+fall\b", "prediction", "CRITICAL"),
    (r"\bforecast\b", "prediction language", "MODERATE"),
    (r"\bexpect\s+to\s+see\b", "prediction", "MODERATE"),

    # Category 6: Ranking/Weighting (5 patterns)
    (r"\bmore\s+reliable\b", "signal ranking", "CRITICAL"),
    (r"\bmost\s+important\s+signal\b", "signal ranking", "CRITICAL"),
    (r"signal\s+strength:\s*\d", "strength scoring", "CRITICAL"),
    (r"\bprimary\s+indicator\b", "ranking language", "MODERATE"),
    (r"\bweighted\s+average\b", "aggregation", "MODERATE"),
]
```

### CR-003: 5-Layer Disclaimer Enforcement

```
Layer 1: Claude instructed to include disclaimer
    ↓
Layer 2: Validator checks for disclaimer presence
    ↓
Layer 3: Generator appends if missing
    ↓
Layer 4: Route ensures disclaimer present
    ↓
Layer 5: Model defaults to disclaimer
```

**Mandatory Disclaimer Text:**
```
"This is a description of what your charts are showing.
The interpretation and any decision is entirely yours."
```

---

## DATABASE SCHEMA CONSTRAINTS

**Constitutionally Prohibited Columns:**

| Entity | Prohibited Column | Rationale |
|--------|-------------------|-----------|
| `ChartDB` | `weight` | Would imply chart priority/ranking |
| `SignalDB` | `confidence` | Would imply signal reliability |
| `SignalDB` | `strength` | Would imply signal quality |
| `ContradictionDB` | `preferred` | Would resolve contradictions |

---

## ARCHITECTURE

### 12-Route API Architecture

| # | Router | Prefix | Purpose |
|---|--------|--------|---------|
| 1 | `instruments_router` | `/instruments` | CRUD for tradable assets |
| 2 | `silos_router` | `/silos` | CRUD for analysis categories |
| 3 | `charts_router` | `/charts` | CRUD for signal receivers |
| 4 | `signals_router` | `/signals` | Signal data access |
| 5 | `webhooks_router` | `/webhook` | TradingView ingestion |
| 6 | `relationships_router` | `/relationships` | Contradictions & confirmations |
| 7 | `narratives_router` | `/narratives` | AI-generated descriptions |
| 8 | `baskets_router` | `/baskets` | Analytical basket management |
| 9 | `platforms_router` | `/platforms` | External platform integration |
| 10 | `ai_router` | `/ai` | AI model management |
| 11 | `chat_router` | `/chat` | Conversational AI |
| 12 | `strategy_router` | `/strategy` | Strategy alignment |

### Entity Hierarchy

```
Instrument (e.g., EURUSD, GOLD)
└── Silo (e.g., "Technical", "Fundamental")
    └── Chart (e.g., "Chart 01A", "Chart 02")
        └── Signal (BULLISH | BEARISH | NEUTRAL + timestamp)
```

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      CIA-SIE SYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FRONTEND (React + TypeScript)                              │
│  ├── Dashboard (signal overview)                            │
│  ├── Instrument Management                                  │
│  ├── Silo Management                                        │
│  ├── Chart Management                                       │
│  ├── Signal Display                                         │
│  └── AI Chat Panel (with constitutional constraints)        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BACKEND (Python FastAPI)                                   │
│  ├── REST API (12 route modules)                            │
│  ├── AI Integration (Claude API)                            │
│  ├── Response Validator (31 prohibited patterns)            │
│  ├── Data Layer (PostgreSQL + SQLAlchemy)                   │
│  └── Business Logic (freshness, contradictions)             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DATABASE (PostgreSQL)                                      │
│  └── Instruments → Silos → Charts → Signals                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## FRESHNESS LOGIC

Implemented in `freshness.py`:

```python
class FreshnessCalculator:
    """
    Per Gold Standard Specification Section 7.3:
    - Freshness is purely descriptive
    - Does NOT invalidate or suppress data
    - All signals displayed regardless of freshness

    IMPORTANT: This is NOT a data validation mechanism.
    Stale data is still VALID data and must be displayed.
    """
```

| Status | Age | Color | Meaning |
|--------|-----|-------|---------|
| CURRENT | ≤2 min | Green | Signal recently received |
| RECENT | ≤10 min | Yellow | Signal within acceptable window |
| STALE | >30 min | Red | Signal older than threshold |
| UNAVAILABLE | Never received | Gray | No signal data available |

**Critical:** We NEVER return UNAVAILABLE based on age. UNAVAILABLE is only for retrieval failures.

---

## TECHNICAL STACK (LOCKED)

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend Framework | React | 18.2 |
| Type System | TypeScript | 5.3 |
| Build Tool | Vite | 5.0 |
| CSS Framework | Tailwind CSS | 3.4 |
| Data Fetching | React Query | 5.17 |
| Routing | React Router | 6.21 |
| HTTP Client | Axios | 1.6 |
| Icons | Lucide React | 0.303 |
| Testing | Vitest | 1.1 |
| Backend | Python + FastAPI | 3.11 / 0.109 |
| Database | PostgreSQL | 15+ |
| ORM | SQLAlchemy | 2.0 |
| AI | Claude API (Anthropic) | - |

---

## CODE METRICS (Verified)

| Metric | Value |
|--------|-------|
| Python Files | 50+ |
| Lines of Code | 10,263 |
| Test Cases | 834 |
| Test Coverage | 80% |
| Unit Tests | 781 passing |
| Integration Tests | 53 passing |

---

## CHART INTEGRATION

### Chart 01A: Daily Intelligence Hub

- PRIMARY_SIGNAL indicator with 31+ JSON payload fields
- MOM_HEALTH indicator with divergence detection
- Webhook-ready alerts with full state data

### Chart 02: Weekly HTF Structure

- HTF_STRUCTURE indicator
- SMA 50/100/200 alignment
- 52-week range positioning
- Swing structure detection (HH_HL, LH_LL)

### Webhook Payload Structure

```json
{
  "chart_id": "GOLD_01A",
  "timestamp": "...",
  "direction": "BULLISH|BEARISH|NEUTRAL",
  "macro": "STRONGLY_BULLISH|...",
  "trend": "BULLISH|BEARISH|MIXED",
  "strength": "WEAK|MODERATE|STRONG",
  "invalidation": 2345.67,
  "ema20": 2400.00,
  "ema50": 2380.00,
  "ema200": 2350.00
}
```

---

## KITE INTELLIGENCE ENGINE (Future Integration)

### 10 Planned Tools

| # | Tool | Purpose |
|---|------|---------|
| 1 | `get_quote` | Current market quotes |
| 2 | `get_top_movers` | Top/bottom performers |
| 3 | `detect_volume_anomalies` | Unusual volume detection |
| 4 | `get_historical_data` | OHLCV candles |
| 5 | `compare_instruments` | Multi-instrument comparison |
| 6 | `calculate_technical_levels` | Pivot/S/R levels |
| 7 | `get_index_constituents` | Index composition |
| 8 | `get_sector_instruments` | Sector composition |
| 9 | `get_cia_sie_signals` | TradingView signals |
| 10 | `get_user_watchlist` | User's tracked instruments |

### Constitutional Compliance in Tools

```python
# Tools return FACTS, not opinions
{
    "symbol": "RELIANCE",
    "ltp": 2456.50,
    "volume": 12500000,
    "volume_vs_average": 1.82,  # Factual comparison
    # NO "signal_strength", NO "confidence", NO "recommendation"
}
```

---

## PROJECT-SPECIFIC RULES

### Forbidden Patterns

```
FORBIDDEN (Constitutional Violations):
❌ "Based on the signals, you should consider buying"
❌ "The bullish consensus suggests a long position"
❌ "This is a good entry point"
❌ "You might want to wait for confirmation"
❌ Any form of "should", "recommend", "suggest", "consider"
❌ Signal scores or confidence values
❌ Chart weights or priorities
❌ Aggregation (counts, percentages, consensus)
❌ Predictions or forecasts
```

### Required Patterns

```
REQUIRED (Constitutional Compliance):
✅ "Chart 01A shows BULLISH, Chart 02 shows BEARISH"
✅ "3 of 12 charts currently display bullish signals"
✅ "The interpretation and any decision is entirely yours"
✅ CONTRADICTION DETECTED alerts
✅ Freshness indicators on all signals
✅ Constitutional banner on dashboard
✅ AI disclaimer on every narrative
```

---

## PROJECT DOCUMENTATION INDEX

### Handoff Documents (in AI_HANDOFF/)

| Document | Purpose |
|----------|---------|
| HANDOFF_00_README | Package overview |
| HANDOFF_01_DESIGN_SPECIFICATION | Visual design requirements |
| HANDOFF_02_API_ENDPOINTS | Complete API documentation |
| HANDOFF_03_CONSTITUTIONAL_RULES | Inviolable rules |
| HANDOFF_04_TECHNICAL_STANDARDS | Engineering standards |
| HANDOFF_05_COMPONENT_REQUIREMENTS | Component specifications |
| HANDOFF_06_CSS_DESIGN_SYSTEM | Styling system |
| HANDOFF_07_BUSINESS_LOGIC | Core algorithms |
| HANDOFF_08_IMPLEMENTATION_STATUS | Gap analysis |

### Source Locations (Canonical)

| Content | Location |
|---------|----------|
| Backend Code | `src/` |
| Frontend Code | `frontend/src/` |
| Documentation | `documentation/` |
| Tests | `tests/` |
| Migrations | `alembic/` |

---

## RELATIONSHIP TO GOLD STANDARD

| CIA-SIE Element | Derived From |
|-----------------|--------------|
| Technical Standards | BIBLE_MODULES/DEVELOPMENT |
| Architecture Principles | BIBLE_MODULES/ARCHITECTURE |
| Verification Approach | BIBLE_MODULES/VERIFICATION |
| Integration Method | BIBLE_MODULES/INTEGRATION |

The Gold Standard Bible provides the universal HOW.
This Chronicle provides the project-specific WHAT.

---

## PRIMARY SOURCE ATTRIBUTION

This Chronicle is derived from:
- **180,891 lines** of original development conversations
- **76 conversations** spanning January 2-14, 2026
- Comprehensive synthesis in `PRIMARY_SOURCE_ANALYSIS_REPORT.md`

---

*PROJECT CHRONICLE: CIA-SIE v4.0.0 | PROJECT_CHRONICLES*
*Updated from primary source review - January 14, 2026*
