# CIA-SIE Backend → Frontend Data Architecture

> **Purpose**: Complete reference of all data structures flowing from backend to frontend.
> **Generated**: During Pre-GUI Verification Protocol

---

## Entity Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INSTRUMENT                                      │
│  (Top-level entity - a tradeable asset like NIFTY, BANKNIFTY)               │
├─────────────────────────────────────────────────────────────────────────────┤
│  instrument_id     : UUID (primary key)                                      │
│  symbol            : string ("NIFTY", "BANKNIFTY")                          │
│  display_name      : string ("Nifty 50 Index")                              │
│  is_active         : boolean                                                 │
│  metadata          : object | null                                           │
│  created_at        : ISO datetime                                            │
│  updated_at        : ISO datetime                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ has many
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 SILO                                         │
│  (Analysis container - groups charts for one instrument)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  silo_id               : UUID (primary key)                                  │
│  instrument_id         : UUID (foreign key → Instrument)                     │
│  silo_name             : string ("NIFTY Technical Analysis")                │
│  heartbeat_enabled     : boolean                                             │
│  heartbeat_frequency_min : number (minutes between heartbeats)              │
│  current_threshold_min : number (freshness: CURRENT if < this)              │
│  recent_threshold_min  : number (freshness: RECENT if < this)               │
│  stale_threshold_min   : number (freshness: STALE if < this)                │
│  is_active             : boolean                                             │
│  created_at            : ISO datetime                                        │
│  updated_at            : ISO datetime                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ has many
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 CHART                                        │
│  (A TradingView chart that emits signals via webhook)                        │
│  ⚠️ CONSTITUTIONAL: NO weight field - all charts have equal standing        │
├─────────────────────────────────────────────────────────────────────────────┤
│  chart_id          : UUID (primary key)                                      │
│  silo_id           : UUID (foreign key → Silo)                              │
│  chart_code        : string ("RSI15M", "MACD1H")                            │
│  chart_name        : string ("RSI 15-Minute", "MACD 1-Hour")                │
│  timeframe         : string (1m|5m|15m|30m|1h|4h|D|W|M)                     │
│  webhook_id        : string (unique identifier for webhook)                  │
│  is_active         : boolean                                                 │
│  created_at        : ISO datetime                                            │
│  updated_at        : ISO datetime                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ has many
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                SIGNAL                                        │
│  (Point-in-time data emission from a chart)                                  │
│  ⚠️ CONSTITUTIONAL: NO confidence/strength fields                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  signal_id         : UUID (primary key)                                      │
│  chart_id          : UUID (foreign key → Chart)                             │
│  received_at       : ISO datetime (when backend received it)                │
│  signal_timestamp  : ISO datetime (when signal was generated)               │
│  signal_type       : enum (HEARTBEAT|STATE_CHANGE|BAR_CLOSE|MANUAL)         │
│  direction         : enum (BULLISH|BEARISH|NEUTRAL)                         │
│  indicators        : object { rsi?: number, macd?: number, ... }            │
│  raw_payload       : object (original webhook payload preserved)            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Derived/Computed Data Structures

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RELATIONSHIP SUMMARY                                  │
│  (Computed when querying a Silo - exposes contradictions & confirmations)   │
├─────────────────────────────────────────────────────────────────────────────┤
│  silo_id           : UUID                                                    │
│  silo_name         : string                                                  │
│  instrument_id     : UUID                                                    │
│  instrument_symbol : string                                                  │
│  generated_at      : ISO datetime                                            │
│                                                                              │
│  charts: [                          ← All charts with current status        │
│    {                                                                         │
│      chart_id      : UUID                                                    │
│      chart_code    : string                                                  │
│      chart_name    : string                                                  │
│      timeframe     : string                                                  │
│      latest_signal : Signal | null                                           │
│      freshness     : enum (CURRENT|RECENT|STALE|UNAVAILABLE)                │
│    }                                                                         │
│  ]                                                                           │
│                                                                              │
│  contradictions: [                  ← Pairs of charts with opposing signals │
│    {                                ⚠️ NEVER resolved, only EXPOSED         │
│      chart_a_id        : UUID                                                │
│      chart_a_name      : string                                              │
│      chart_a_direction : enum (BULLISH|BEARISH|NEUTRAL)                     │
│      chart_b_id        : UUID                                                │
│      chart_b_name      : string                                              │
│      chart_b_direction : enum (BULLISH|BEARISH|NEUTRAL)                     │
│      detected_at       : ISO datetime                                        │
│    }                                                                         │
│  ]                                                                           │
│                                                                              │
│  confirmations: [                   ← Pairs of charts with aligned signals  │
│    {                                                                         │
│      chart_a_id        : UUID                                                │
│      chart_a_name      : string                                              │
│      chart_b_id        : UUID                                                │
│      chart_b_name      : string                                              │
│      aligned_direction : enum (BULLISH|BEARISH|NEUTRAL)                     │
│      detected_at       : ISO datetime                                        │
│    }                                                                         │
│  ]                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## AI-Generated Content

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NARRATIVE                                       │
│  (AI-generated DESCRIPTIVE text for a Silo)                                 │
│  ⚠️ CONSTITUTIONAL: DESCRIPTIVE only, NEVER prescriptive                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  narrative_id      : UUID                                                    │
│  silo_id           : UUID                                                    │
│  generated_at      : ISO datetime                                            │
│                                                                              │
│  sections: [                                                                 │
│    {                                                                         │
│      section_type        : enum (SIGNAL_SUMMARY|CONTRADICTION|              │
│                                  CONFIRMATION|FRESHNESS)                    │
│      content             : string (AI-generated description)                │
│      referenced_chart_ids : UUID[]                                          │
│    }                                                                         │
│  ]                                                                           │
│                                                                              │
│  closing_statement : string                                                  │
│  ⚠️ ALWAYS: "This is a description of what your charts are showing.        │
│              The interpretation and any decision is entirely yours."        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHAT MESSAGE                                       │
│  (Conversational AI about an instrument's signals)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  conversation_id   : UUID                                                    │
│  role              : enum (user|assistant)                                  │
│  content           : string                                                  │
│  timestamp         : ISO datetime                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHAT RESPONSE                                      │
│  (Response from AI chat endpoint)                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  conversation_id   : UUID                                                    │
│  message           : ChatMessage                                             │
│  context_used      : { signals_included, charts_referenced }                │
│  usage             : { input_tokens, output_tokens, cost, model_used }      │
│  disclaimer        : string (MANDATORY)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## AI Management Data

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             AI MODEL                                         │
│  (Available Claude models)                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  id                      : string ("claude-3-haiku-20240307")               │
│  display_name            : string ("Haiku")                                 │
│  description             : string                                            │
│  cost_per_1k_input_tokens  : number (e.g., 0.00025)                         │
│  cost_per_1k_output_tokens : number (e.g., 0.00125)                         │
│  max_tokens              : number                                            │
│  capabilities            : string[] (["quick_query", "simple_description"]) │
│  recommended_for         : string[] (["single_chart", "freshness_check"])   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            AI BUDGET                                         │
│  (Current budget status)                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  within_budget     : boolean                                                 │
│  percentage_used   : number (0-100)                                         │
│  remaining         : number (dollars remaining)                             │
│  alert_level       : string | null ("warning", "critical")                  │
│  message           : string | null                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            AI USAGE                                          │
│  (Usage statistics for a period)                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  period            : enum (daily|weekly|monthly)                            │
│  period_start      : ISO datetime                                            │
│  period_end        : ISO datetime                                            │
│  requests_count    : number                                                  │
│  tokens_used       : { input, output, total }                               │
│  cost              : { amount, currency }                                   │
│  budget            : { limit, used, remaining, percentage_used }            │
│  model_breakdown   : [ { model_id, requests, tokens, cost } ]               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Enumerations (Fixed Value Sets)

| Enum | Values |
|------|--------|
| **DIRECTION** | `BULLISH` \| `BEARISH` \| `NEUTRAL` |
| **SIGNAL_TYPE** | `HEARTBEAT` \| `STATE_CHANGE` \| `BAR_CLOSE` \| `MANUAL` |
| **FRESHNESS_STATUS** | `CURRENT` \| `RECENT` \| `STALE` \| `UNAVAILABLE` |
| **TIMEFRAME** | `1m` \| `5m` \| `15m` \| `30m` \| `1h` \| `4h` \| `D` \| `W` \| `M` |

---

## API Endpoint → Data Mapping

| Endpoint | HTTP Method | Returns | Data Structure |
|----------|-------------|---------|----------------|
| `/api/v1/instruments/` | GET | Array | `Instrument[]` |
| `/api/v1/instruments/{id}` | GET | Single | `Instrument` |
| `/api/v1/instruments/symbol/{symbol}` | GET | Single | `Instrument` |
| `/api/v1/silos/` | GET | Array | `Silo[]` |
| `/api/v1/silos/{id}` | GET | Single | `Silo` |
| `/api/v1/charts/` | GET | Array | `Chart[]` |
| `/api/v1/charts/{id}` | GET | Single | `Chart` |
| `/api/v1/signals/chart/{id}` | GET | Array | `Signal[]` |
| `/api/v1/signals/chart/{id}/latest` | GET | Single | `Signal \| null` |
| `/api/v1/relationships/silo/{id}` | GET | Computed | `RelationshipSummary` |
| `/api/v1/relationships/instrument/{id}` | GET | Array | `RelationshipSummary[]` |
| `/api/v1/narratives/silo/{id}` | GET | AI-Generated | `Narrative` |
| `/api/v1/narratives/silo/{id}/plain` | GET | Plain Text | `{ text, generated_at }` |
| `/api/v1/ai/models` | GET | Config | `{ models, default_model, budget_remaining }` |
| `/api/v1/ai/budget` | GET | Status | `AIBudget` |
| `/api/v1/ai/usage` | GET | Stats | `AIUsage` |
| `/api/v1/chat/{scrip_id}` | POST | AI Response | `ChatResponse` |
| `/api/v1/chat/{scrip_id}/history` | GET | History | `ChatHistoryResponse` |
| `/health` | GET | Status | `HealthResponse` |

---

## Visual Data Flow

```
                    ┌─────────────┐
                    │ TradingView │
                    │   Webhooks  │
                    └──────┬──────┘
                           │ POST /webhook
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         BACKEND (FastAPI)                            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│  │Instrument│───▶│  Silo   │───▶│  Chart  │───▶│ Signal  │           │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘           │
│       │              │              │              │                 │
│       │              │              └──────────────┴──────┐          │
│       │              │                                    ▼          │
│       │              │         ┌──────────────────────────────────┐  │
│       │              └────────▶│     Relationship Detector       │  │
│       │                        │  • Contradiction Detection      │  │
│       │                        │  • Confirmation Detection       │  │
│       │                        │  • Freshness Calculation        │  │
│       │                        └──────────────┬───────────────────┘  │
│       │                                       │                      │
│       │                                       ▼                      │
│       │                        ┌──────────────────────────────────┐  │
│       │                        │      AI Narrative Generator     │  │
│       │                        │  • Claude API                   │  │
│       │                        │  • Constitutional Validation    │  │
│       │                        └──────────────┬───────────────────┘  │
│       │                                       │                      │
└───────┼───────────────────────────────────────┼──────────────────────┘
        │                                       │
        ▼                                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                              │
│                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
│  │   Instruments  │  │     Silos      │  │     Charts     │         │
│  │      Page      │  │     Page       │  │      Page      │         │
│  └────────────────┘  └────────────────┘  └────────────────┘         │
│                              │                                       │
│                              ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Silo Detail View                           │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │  │
│  │  │   Charts    │ │Contradictions│ │Confirmations│              │  │
│  │  │   List      │ │   Panel      │ │   Panel     │              │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘              │  │
│  │  ┌────────────────────────────────────────────┐               │  │
│  │  │           Narrative Display                │               │  │
│  │  │  + MANDATORY Disclaimer                    │               │  │
│  │  └────────────────────────────────────────────┘               │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Constitutional Constraints on Data

| Constraint | Affected Data | Rule |
|------------|---------------|------|
| **CR-001** | All AI outputs | No recommendations, suggestions, or advice |
| **CR-002** | Contradictions | Must be EXPOSED, never RESOLVED |
| **CR-002** | Charts | No weight/priority field - all equal |
| **CR-003** | Signals | No confidence/strength scores |
| **CR-003** | Narratives | Must include mandatory disclaimer |

---

## Sample Data (From Live Backend)

### Instrument Example
```json
{
  "instrument_id": "574d6865-e36c-4d59-9930-18b52350f70b",
  "symbol": "NIFTY",
  "display_name": "Nifty 50 Index",
  "is_active": true,
  "metadata": null,
  "created_at": "2026-01-03T18:37:41.378371",
  "updated_at": "2026-01-03T18:37:41.378374"
}
```

### Signal Example
```json
{
  "signal_id": "ccb63db0-9775-4d5d-bfec-7d5bbc76ce7c",
  "chart_id": "e9f1d6f0-08a6-47a0-a5fa-73bf2be95467",
  "received_at": "2026-01-03T18:39:23.760527",
  "signal_timestamp": "2026-01-03T18:39:23.760649",
  "signal_type": "STATE_CHANGE",
  "direction": "BULLISH",
  "indicators": {
    "rsi": 72,
    "price": 24850.5
  },
  "raw_payload": { ... }
}
```

### Contradiction Example
```json
{
  "chart_a_id": "e9f1d6f0-08a6-47a0-a5fa-73bf2be95467",
  "chart_a_name": "RSI 15-Minute",
  "chart_a_direction": "BULLISH",
  "chart_b_id": "74f43e98-e832-43c8-bed5-01b1b206106b",
  "chart_b_name": "MACD 1-Hour",
  "chart_b_direction": "BEARISH",
  "detected_at": "2026-01-04T05:09:20.805609Z"
}
```

---

*Document generated as part of Pre-GUI Verification Protocol*

