# CIA-SIE MASTER FOUNDATIONAL DOCUMENT
## Chart Intelligence Auditor & Signal Intelligence Engine
### Comprehensive Backend Reconstruction Blueprint

---

**Document Version:** 1.0.0
**Generated:** 2026-01-15
**Source:** HTML-Forensic-Audit by Cursor (77 HTML files analyzed)
**Purpose:** Complete specification for backend reconstruction

---

## TABLE OF CONTENTS

1. [Constitutional Principles (INVIOLABLE)](#1-constitutional-principles-inviolable)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Data Model Specification](#3-data-model-specification)
4. [API Endpoint Reference](#4-api-endpoint-reference)
5. [Webhook Processing Pipeline](#5-webhook-processing-pipeline)
6. [AI Narrative Generation System](#6-ai-narrative-generation-system)
7. [Relationship Detection (Contradiction/Confirmation)](#7-relationship-detection)
8. [Technology Stack](#8-technology-stack)
9. [Current Backend Gap Analysis](#9-current-backend-gap-analysis)
10. [Reconstruction Priority Matrix](#10-reconstruction-priority-matrix)

---

## 1. CONSTITUTIONAL PRINCIPLES (INVIOLABLE)

These rules CANNOT be violated under any circumstances. They are the foundational philosophy of CIA-SIE.

### CR-001: Decision-Support, NOT Decision-Making
- System provides information, NEVER recommendations
- No buy/sell/hold suggestions
- No aggregated scores or weights
- No confidence percentages
- **Implementation:** AI prompts explicitly forbid prescriptive language

### CR-002: Expose Contradictions, NEVER Resolve Them
- When signals conflict, display both with EQUAL visual weight
- Never prioritize one signal over another
- No "more reliable" or "stronger signal" language
- Contradiction cards must be identical in size/styling
- **Implementation:** UI renders contradiction pairs with neutral separator

### CR-003: Descriptive AI, NOT Prescriptive AI
- AI narratives DESCRIBE what indicators show
- MANDATORY disclaimer on every AI response
- Disclaimer cannot be dismissed or hidden
- **Implementation:** System prompt constraints + post-response filtering

### Constitutional Enforcement Points
| Rule | Screen | Element | How Enforced |
|------|--------|---------|--------------|
| CR-001 | Silo Detail | Confirmation Note | "NOT stronger signal" warning |
| CR-001 | Chart Detail | CR-001 Notice | "No weight" reminder box |
| CR-001 | Basket List | Info Banner | "UI-only, no effect" message |
| CR-001 | Basket Detail | Warning Note | "Counts are not aggregation" |
| CR-002 | Silo Detail | Charts Grid | Equal sizing, 4-column grid |
| CR-002 | Silo Detail | Contradiction Card | Equal boxes, neutral separator |
| CR-003 | All Pages | Disclaimer Banner | Non-dismissible, immutable |
| CR-003 | AI Chat | Every AI Message | Inline disclaimer |

---

## 2. SYSTEM ARCHITECTURE OVERVIEW

### High-Level Data Flow
```
TradingView Alert → ngrok Tunnel → FastAPI Webhook → Signal Storage → Frontend Display
                                                           ↓
                                                    AI Narrative ← Claude API
```

### Component Layers
```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React/TypeScript)                  │
│  CommandCenter | InstrumentDetail | SiloDetail | ChartDetail    │
│  BasketsPage | AIChat | NarrativePanel | ContradictionBanner    │
├─────────────────────────────────────────────────────────────────┤
│                        API LAYER (FastAPI)                       │
│  12 Routers: instruments, silos, charts, signals, webhooks,     │
│  relationships, narratives, baskets, platforms, ai, chat,       │
│  strategy, market-intelligence                                   │
├─────────────────────────────────────────────────────────────────┤
│                      BUSINESS LOGIC LAYER                        │
│  webhook_handler | signal_normalizer | contradiction_detector   │
│  confirmation_detector | narrative_generator | prompt_builder   │
├─────────────────────────────────────────────────────────────────┤
│                     DATA ACCESS LAYER (DAL)                      │
│  SQLAlchemy ORM | Repository Pattern | Pydantic Schemas         │
├─────────────────────────────────────────────────────────────────┤
│                    DATABASE (SQLite/PostgreSQL)                  │
│  instruments | silos | charts | signals | analytical_baskets    │
│  basket_charts | conversations | ai_usage                        │
└─────────────────────────────────────────────────────────────────┘
```

### Backend Directory Structure (Required)
```
src/cia_sie/
├── __init__.py
├── main.py                      # Application entry point
├── api/
│   ├── __init__.py
│   ├── app.py                   # FastAPI application factory
│   └── routes/
│       ├── __init__.py          # Router aggregation
│       ├── instruments.py       # CRUD for instruments
│       ├── silos.py             # CRUD for silos
│       ├── charts.py            # CRUD for charts
│       ├── signals.py           # Signal queries
│       ├── webhooks.py          # TradingView webhook receiver
│       ├── relationships.py     # Contradiction/confirmation exposure
│       ├── narratives.py        # AI narrative generation
│       ├── baskets.py           # Analytical baskets
│       ├── platforms.py         # Platform integration
│       ├── ai.py                # AI model management
│       ├── chat.py              # Conversational AI
│       └── strategy.py          # Strategy analysis
├── ai/
│   ├── __init__.py
│   ├── claude_client.py         # Anthropic API wrapper
│   ├── model_registry.py        # Available models
│   ├── narrative_generator.py   # Narrative service
│   ├── prompt_builder.py        # Constitutional prompt construction
│   ├── response_validator.py    # Filter prohibited content
│   └── usage_tracker.py         # API usage tracking
├── core/
│   ├── __init__.py
│   ├── config.py                # Settings management
│   ├── enums.py                 # Direction, SignalType, FreshnessLevel
│   ├── exceptions.py            # Custom exceptions
│   ├── models.py                # Pydantic schemas
│   └── security.py              # Rate limiting, headers
├── dal/
│   ├── __init__.py
│   ├── database.py              # Database connection
│   ├── models.py                # SQLAlchemy ORM models
│   └── repositories.py          # Data access patterns
├── exposure/
│   ├── __init__.py
│   ├── confirmation_detector.py # Same-direction signal detection
│   ├── contradiction_detector.py # Opposite-direction signal detection
│   └── relationship_exposer.py  # Combined exposure service
├── ingestion/
│   ├── __init__.py
│   ├── freshness.py             # Signal age calculation
│   ├── signal_normalizer.py     # Payload normalization
│   └── webhook_handler.py       # Webhook processing logic
└── platforms/
    ├── __init__.py
    ├── base.py                  # Platform adapter interface
    ├── kite.py                  # Zerodha Kite adapter
    ├── registry.py              # Platform registry
    └── tradingview.py           # TradingView adapter
```

---

## 3. DATA MODEL SPECIFICATION

### Entity Hierarchy
```
INSTRUMENT (Root)
    └── SILO (1:N)
        └── CHART (1:N)
            └── SIGNAL (1:N)

BASKET ←→ CHART (M:N via basket_charts junction table)
```

### Database Tables

#### instruments
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| symbol | VARCHAR(50) | UNIQUE, NOT NULL | Trading symbol |
| name | VARCHAR(200) | NOT NULL | Display name |
| exchange | VARCHAR(50) | | Exchange code |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | | Last update |

#### silos
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| instrument_id | UUID | FK→instruments.id | Parent instrument |
| name | VARCHAR(200) | NOT NULL | Silo name |
| description | TEXT | | Analysis context |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

#### charts
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| silo_id | UUID | FK→silos.id | Parent silo |
| name | VARCHAR(200) | NOT NULL | Chart name |
| webhook_id | VARCHAR(100) | UNIQUE, NOT NULL | TradingView identifier |
| description | TEXT | | Chart description |
| tradingview_url | TEXT | | Link to TradingView |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

#### signals
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| chart_id | UUID | FK→charts.id | Parent chart |
| direction | ENUM | BULLISH/BEARISH/NEUTRAL | Signal direction |
| signal_type | ENUM | STATE_CHANGE/BAR_CLOSE/HEARTBEAT/MANUAL | Type |
| timestamp | TIMESTAMP | NOT NULL | Signal timestamp |
| metadata | JSON | | Additional data |
| created_at | TIMESTAMP | DEFAULT NOW() | Ingestion timestamp |

#### analytical_baskets
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Basket name |
| description | TEXT | | Purpose description |
| basket_type | ENUM | SECTOR/STRATEGY/CORRELATION/CUSTOM | Type |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

#### basket_charts (Junction Table)
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| basket_id | UUID | FK→analytical_baskets.id | Basket reference |
| chart_id | UUID | FK→charts.id | Chart reference |
| added_at | TIMESTAMP | DEFAULT NOW() | Association timestamp |
| PRIMARY KEY | | (basket_id, chart_id) | Composite key |

#### conversations
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| instrument_id | UUID | FK→instruments.id | Context instrument |
| title | VARCHAR(200) | | Conversation title |
| model_id | VARCHAR(100) | | AI model used |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

#### ai_usage
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| conversation_id | UUID | FK→conversations.id | Parent conversation |
| input_tokens | INTEGER | | Tokens in prompt |
| output_tokens | INTEGER | | Tokens in response |
| cost_usd | DECIMAL(10,6) | | Calculated cost |
| model_id | VARCHAR(100) | | Model used |
| created_at | TIMESTAMP | DEFAULT NOW() | Usage timestamp |

### Enumerations

```python
class Direction(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

class SignalType(str, Enum):
    STATE_CHANGE = "STATE_CHANGE"
    BAR_CLOSE = "BAR_CLOSE"
    HEARTBEAT = "HEARTBEAT"
    MANUAL = "MANUAL"

class FreshnessLevel(str, Enum):
    CURRENT = "CURRENT"    # < 1 hour
    RECENT = "RECENT"      # 1-24 hours
    STALE = "STALE"        # > 24 hours

class BasketType(str, Enum):
    SECTOR = "SECTOR"
    STRATEGY = "STRATEGY"
    CORRELATION = "CORRELATION"
    CUSTOM = "CUSTOM"
```

---

## 4. API ENDPOINT REFERENCE

### Base URL: `/api/v1`

### Instruments API
| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/instruments/` | List all instruments | - | InstrumentRead[] |
| POST | `/instruments/` | Create instrument | InstrumentCreate | InstrumentRead (201) |
| GET | `/instruments/{id}` | Get by ID | - | InstrumentRead |
| PUT | `/instruments/{id}` | Update instrument | InstrumentUpdate | InstrumentRead |
| DELETE | `/instruments/{id}` | Delete instrument | - | 204 No Content |

### Silos API
| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/silos/` | List all silos | - | SiloRead[] |
| POST | `/silos/` | Create silo | SiloCreate | SiloRead (201) |
| GET | `/silos/{id}` | Get with charts & signals | - | SiloReadWithCharts |
| PUT | `/silos/{id}` | Update silo | SiloUpdate | SiloRead |
| DELETE | `/silos/{id}` | Delete silo (cascades) | - | 204 No Content |
| GET | `/silos/{id}/signals` | Get all silo signals | - | SignalRead[] |
| POST | `/silos/{id}/narrative` | Generate AI narrative | - | NarrativeResponse |

### Charts API
| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/charts/` | List all charts | - | ChartRead[] |
| POST | `/charts/` | Create chart | ChartCreate | ChartRead (201) |
| GET | `/charts/{id}` | Get by ID | - | ChartRead |
| PUT | `/charts/{id}` | Update chart | ChartUpdate | ChartRead |
| DELETE | `/charts/{id}` | Delete chart (cascades) | - | 204 No Content |
| GET | `/charts/{id}/signals` | Get chart signals | - | SignalRead[] |

### Webhook API
| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| POST | `/webhook/` | Receive TradingView alert | WebhookPayload | WebhookResponse |

### Baskets API
| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/baskets/` | List all baskets | - | BasketRead[] |
| POST | `/baskets/` | Create basket | BasketCreate | BasketRead (201) |
| GET | `/baskets/{id}` | Get with charts | - | BasketReadWithCharts |
| PUT | `/baskets/{id}` | Update basket | BasketUpdate | BasketRead |
| DELETE | `/baskets/{id}` | Delete basket | - | 204 No Content |

### Relationships API
| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/relationships/contradictions` | Get all contradictions | ContradictionPair[] |
| GET | `/relationships/confirmations` | Get all confirmations | ConfirmationGroup[] |
| GET | `/relationships/silo/{id}/contradictions` | Silo contradictions | ContradictionPair[] |
| GET | `/relationships/silo/{id}/confirmations` | Silo confirmations | ConfirmationGroup[] |

### AI Management API
| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/ai/models` | List available models | AIModel[] |
| GET | `/ai/usage` | Get usage statistics | UsageStats |
| PUT | `/ai/settings` | Update AI settings | AISettings |

### Chat API
| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/chat/conversations` | List conversations | - | Conversation[] |
| POST | `/chat/conversations` | Create conversation | CreateConversation | Conversation |
| GET | `/chat/conversations/{id}` | Get conversation | - | ConversationWithMessages |
| POST | `/chat/conversations/{id}/messages` | Send message | ChatMessage | AIResponse |

### Health API
| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/health` | Health check | HealthStatus |

---

## 5. WEBHOOK PROCESSING PIPELINE

### Flow Diagram
```
TradingView Alert Fires
        ↓
ngrok Tunnel Receives
        ↓
FastAPI Endpoint: POST /api/v1/webhook/
        ↓
Parse JSON Body ─── Invalid JSON → 400 Bad Request
        ↓
Validate Against Schema ─── Missing fields → 422 Validation Error
        ↓
Normalize Payload
        ↓
Lookup Chart by webhook_id ─── Not found → 404 Not Found
        ↓
Create Signal Record
        ↓
Store in Database
        ↓
Return 200 + Signal ID
```

### Webhook Payload Schema
```json
{
  "webhook_id": "GOLDBEES_01A_PRIMARY",    // Required: Unique chart identifier
  "direction": "BULLISH",                   // Required: BULLISH | BEARISH | NEUTRAL
  "signal_type": "STATE_CHANGE",            // Required: STATE_CHANGE | BAR_CLOSE | HEARTBEAT
  "timestamp": "2024-01-15T10:30:00Z",      // Optional: ISO 8601, defaults to now
  "metadata": {                              // Optional: Additional context
    "indicator": "RSI",
    "value": 72.5,
    "timeframe": "1D"
  }
}
```

### Field Validation Rules
| Field | Type | Required | Validation | Error if Invalid |
|-------|------|----------|------------|------------------|
| webhook_id | string | Yes | Must match existing chart.webhook_id | 404 Not Found |
| direction | enum | Yes | BULLISH \| BEARISH \| NEUTRAL | 422 Validation Error |
| signal_type | enum | Yes | STATE_CHANGE \| BAR_CLOSE \| HEARTBEAT \| MANUAL | 422 Validation Error |
| timestamp | datetime | No | Valid ISO 8601 format | 422 if malformed |
| metadata | object | No | Any valid JSON object | N/A |

### Response Codes
| Status | Meaning | Response Body |
|--------|---------|---------------|
| 200 OK | Signal accepted and stored | `{"status": "accepted", "signal_id": "uuid", "direction": "BULLISH"}` |
| 400 Bad Request | Malformed JSON | `{"detail": "Invalid JSON"}` |
| 404 Not Found | No chart with matching webhook_id | `{"detail": "Chart not found for webhook_id: X"}` |
| 422 Validation Error | Schema validation failed | `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}` |
| 500 Server Error | Database or internal error | `{"detail": "Internal server error"}` |

---

## 6. AI NARRATIVE GENERATION SYSTEM

### Constitutional AI Constraints
The AI narrative service is bound by CIA-SIE's constitutional principles:

**PROHIBITED:**
- Recommending buy/sell/hold actions
- Providing price targets or predictions
- Expressing confidence percentages
- Prioritizing one signal over another
- Resolving contradictions between signals

### System Prompt
```
You are a technical analysis narrator for CIA-SIE (Chart Intelligence Auditor & Signal Intelligence Engine).

Your role is to DESCRIBE what technical indicators and signals show. You are an educator and narrator, NOT an advisor.

CONSTITUTIONAL CONSTRAINTS - YOU MUST FOLLOW THESE:

1. DESCRIBE, NEVER PRESCRIBE
   - Explain what indicators show
   - Do NOT recommend actions

2. EXPOSE CONTRADICTIONS, NEVER RESOLVE THEM
   - If signals conflict, describe both perspectives
   - Do NOT say which signal is "more reliable"

3. NO PREDICTIONS OR TARGETS
   - Do NOT provide price targets
   - Do NOT express probability or confidence

4. NO TRADING ADVICE
   - Do NOT use words like "buy", "sell", "hold", "enter", "exit"
   - Do NOT suggest timing of any actions

5. EDUCATIONAL CONTEXT ONLY
   - Explain what patterns historically represent
   - Let the human operator draw conclusions

You MUST include this disclaimer at the end:
"This narrative describes technical indicator readings and is for informational purposes only.
It does not constitute financial advice. Trading decisions are the sole responsibility of the user."
```

### API Configuration
| Parameter | Value | Purpose |
|-----------|-------|---------|
| model | claude-3-sonnet-20240229 | Fast, capable model |
| max_tokens | 1024 | Limit response length |
| temperature | 0.3 | Low creativity for consistency |
| system | SYSTEM_PROMPT | Constitutional constraints |

### Response Validation - Prohibited Patterns
- "you should"
- "recommend"
- "buy" / "sell"
- "target price"
- "% confidence"

### Narrative Response Schema
```json
{
  "silo_id": "uuid",
  "instrument": {
    "symbol": "GOLDBEES",
    "name": "Nippon India ETF Gold BeES"
  },
  "narrative": "The RSI indicator shows a reading of 65...",
  "generated_at": "2024-01-15T10:30:00Z",
  "signal_count": 3,
  "freshness_summary": {
    "current": 2,
    "recent": 1,
    "stale": 0
  },
  "disclaimer": "This narrative describes technical indicator readings...",
  "cached": false,
  "filtered": false
}
```

---

## 7. RELATIONSHIP DETECTION

### Contradiction Detection
Contradictions occur when charts within the same silo show OPPOSITE directions.

**Detection Logic:**
```python
def detect_contradictions(silo_id: UUID) -> List[ContradictionPair]:
    # Get all charts in silo
    charts = get_charts_for_silo(silo_id)

    contradictions = []

    # Compare each pair of charts
    for i, chart_a in enumerate(charts):
        for chart_b in charts[i+1:]:
            signal_a = get_latest_signal(chart_a.id)
            signal_b = get_latest_signal(chart_b.id)

            # Check for opposite directions
            if is_contradiction(signal_a.direction, signal_b.direction):
                contradictions.append(ContradictionPair(
                    chart_a=chart_a,
                    signal_a=signal_a,
                    chart_b=chart_b,
                    signal_b=signal_b
                ))

    return contradictions

def is_contradiction(dir_a: Direction, dir_b: Direction) -> bool:
    return (
        (dir_a == Direction.BULLISH and dir_b == Direction.BEARISH) or
        (dir_a == Direction.BEARISH and dir_b == Direction.BULLISH)
    )
```

### Confirmation Detection
Confirmations occur when charts within the same silo show the SAME direction.

**Detection Logic:**
```python
def detect_confirmations(silo_id: UUID) -> List[ConfirmationGroup]:
    # Get all charts in silo
    charts = get_charts_for_silo(silo_id)

    # Group by direction
    bullish = []
    bearish = []
    neutral = []

    for chart in charts:
        signal = get_latest_signal(chart.id)
        if signal.direction == Direction.BULLISH:
            bullish.append((chart, signal))
        elif signal.direction == Direction.BEARISH:
            bearish.append((chart, signal))
        else:
            neutral.append((chart, signal))

    confirmations = []

    # Create confirmation groups (2+ charts in same direction)
    if len(bullish) >= 2:
        confirmations.append(ConfirmationGroup(
            direction=Direction.BULLISH,
            charts=[c for c, s in bullish],
            signals=[s for c, s in bullish]
        ))
    if len(bearish) >= 2:
        confirmations.append(ConfirmationGroup(
            direction=Direction.BEARISH,
            charts=[c for c, s in bearish],
            signals=[s for c, s in bearish]
        ))

    return confirmations
```

### Freshness Calculation
```python
def calculate_freshness(signal_timestamp: datetime) -> FreshnessLevel:
    age = datetime.utcnow() - signal_timestamp

    if age < timedelta(hours=1):
        return FreshnessLevel.CURRENT
    elif age < timedelta(hours=24):
        return FreshnessLevel.RECENT
    else:
        return FreshnessLevel.STALE
```

---

## 8. TECHNOLOGY STACK

### Backend
| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | 0.100+ |
| Language | Python | 3.11+ |
| ORM | SQLAlchemy | 2.0+ |
| Validation | Pydantic | 2.0+ |
| Database | SQLite (dev) / PostgreSQL (prod) | - |
| AI Provider | Anthropic | Claude 3 |
| Migrations | Alembic | - |
| HTTP Server | Uvicorn | - |

### Frontend
| Component | Technology | Version |
|-----------|------------|---------|
| Framework | React | 18+ |
| Language | TypeScript | 5+ |
| Build Tool | Vite | - |
| Styling | TailwindCSS | 3.4+ |
| Data Fetching | React Query | 5+ |
| Routing | React Router | 6+ |

### Infrastructure
| Component | Technology | Purpose |
|-----------|------------|---------|
| Tunnel | ngrok | Expose local webhook endpoint |
| VCS | Git | Version control |
| CI/CD | GitHub Actions | Automated testing |

---

## 9. CURRENT BACKEND GAP ANALYSIS

### Comparison: Specification vs Implementation

Based on analysis of `/Users/nevillemehta/Downloads/CIA-SIE-PURE/src/cia_sie/`:

#### API Routes (Current State)
| Router | Spec Status | Implementation Status | Notes |
|--------|-------------|----------------------|-------|
| instruments | Required | EXISTS | Verify CRUD completeness |
| silos | Required | EXISTS | Verify CRUD completeness |
| charts | Required | EXISTS | Verify CRUD completeness |
| signals | Required | EXISTS | Verify query patterns |
| webhooks | Required | EXISTS | Verify payload handling |
| relationships | Required | EXISTS | Verify contradiction/confirmation logic |
| narratives | Required | EXISTS | Verify AI integration |
| baskets | Required | EXISTS | Verify UI-only constraint |
| platforms | Optional | EXISTS | Kite integration |
| ai | Required | EXISTS | Verify model management |
| chat | Required | EXISTS | Verify conversation handling |
| strategy | Optional | EXISTS | Extended feature |
| market_intelligence | Optional | EXISTS | Extended feature |

#### Core Modules Status
| Module | Required | Status | Gap |
|--------|----------|--------|-----|
| ai/claude_client.py | Yes | VERIFY | Need to check API integration |
| ai/narrative_generator.py | Yes | VERIFY | Need to check constitutional prompts |
| ai/prompt_builder.py | Yes | VERIFY | Need to check system prompt |
| ai/response_validator.py | Yes | VERIFY | Need to check filtering |
| core/config.py | Yes | EXISTS | Basic settings |
| core/enums.py | Yes | VERIFY | Need Direction, SignalType, FreshnessLevel |
| dal/models.py | Yes | EXISTS | SQLAlchemy models |
| dal/repositories.py | Yes | EXISTS | Data access patterns |
| exposure/contradiction_detector.py | Yes | EXISTS | Need to verify logic |
| exposure/confirmation_detector.py | Yes | EXISTS | Need to verify logic |
| ingestion/webhook_handler.py | Yes | VERIFY | Need to check processing |
| ingestion/freshness.py | Yes | VERIFY | Need to check calculation |

### Key Areas Requiring Verification

1. **Constitutional Compliance**
   - Are AI prompts correctly constrained?
   - Is response filtering implemented?
   - Are disclaimers mandatory?

2. **Data Model Integrity**
   - Is the hierarchy enforced (Instrument → Silo → Chart → Signal)?
   - Are cascade deletes working?
   - Is webhook_id uniqueness enforced?

3. **Relationship Detection**
   - Is contradiction detection accurate?
   - Is confirmation detection accurate?
   - Are freshness levels calculated correctly?

4. **Webhook Processing**
   - Is payload validation complete?
   - Is signal normalization working?
   - Are error responses correct?

---

## 10. RECONSTRUCTION PRIORITY MATRIX

### Priority 1: CRITICAL (Must Have)
| Component | Reason | Estimated Effort |
|-----------|--------|------------------|
| Webhook Processing | Core data ingestion | Medium |
| Data Model (4 entities) | Foundation | High |
| Constitutional Prompts | Compliance | Low |
| Contradiction Detection | Core feature | Medium |

### Priority 2: HIGH (Should Have)
| Component | Reason | Estimated Effort |
|-----------|--------|------------------|
| AI Narrative Generation | User value | Medium |
| Freshness Calculation | Signal context | Low |
| Confirmation Detection | User value | Medium |
| Basket Management | UI organization | Low |

### Priority 3: MEDIUM (Nice to Have)
| Component | Reason | Estimated Effort |
|-----------|--------|------------------|
| Chat Interface | Extended AI | Medium |
| Usage Tracking | Cost management | Low |
| Response Filtering | Safety | Medium |

### Priority 4: LOW (Future)
| Component | Reason | Estimated Effort |
|-----------|--------|------------------|
| Kite Integration | Platform extension | High |
| Real-time WebSockets | Enhancement | High |
| Advanced Analytics | Extended features | High |

---

## APPENDIX A: File Sources

This document was generated from analysis of 77 HTML files in:
`/Users/nevillemehta/Downloads/HTML-Forensic-Audit by Cursor - 2026-01-15/`

**Key Source Documents:**
- SYSTEM_ARCHITECTURE_VISUAL.html (1434 lines)
- UI_FUNCTIONAL_SPECIFICATION_COMPLETE.html
- Feature_Specification_Matrix.html
- 01_Webhook_Processing_Flow.html
- 04_API_CRUD_Flow.html
- 05_Data_Hierarchy_Flow.html
- 03_AI_Narrative_Generation_Flow.html
- 06_AI_Narrative_Flow.html
- software_development_mermaid_flowchart.html

---

## APPENDIX B: Current Backend Files Reference

Located at: `/Users/nevillemehta/Downloads/CIA-SIE-PURE/`

**API Routes (13 routers):**
- src/cia_sie/api/routes/__init__.py
- src/cia_sie/api/routes/instruments.py
- src/cia_sie/api/routes/silos.py
- src/cia_sie/api/routes/charts.py
- src/cia_sie/api/routes/signals.py
- src/cia_sie/api/routes/webhooks.py
- src/cia_sie/api/routes/relationships.py
- src/cia_sie/api/routes/narratives.py
- src/cia_sie/api/routes/baskets.py
- src/cia_sie/api/routes/platforms.py
- src/cia_sie/api/routes/ai.py
- src/cia_sie/api/routes/chat.py
- src/cia_sie/api/routes/strategy.py
- src/cia_sie/api/routes/market_intelligence.py

---

**END OF MASTER FOUNDATIONAL DOCUMENT**

*This document serves as the authoritative specification for CIA-SIE backend reconstruction.*
