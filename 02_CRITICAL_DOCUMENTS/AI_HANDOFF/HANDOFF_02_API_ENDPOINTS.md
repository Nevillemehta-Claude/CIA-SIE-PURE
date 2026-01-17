# HANDOFF_02: API ENDPOINTS

**Backend:** FastAPI running on `http://localhost:8000`
**API Version:** v1
**Base URL:** `/api/v1`

---

## API CONNECTION

### Existing API Service (KEEP THIS FILE)
```typescript
// frontend/src/services/api.ts - Already implemented correctly
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',  // Uses Vite proxy to localhost:8000
  headers: {
    'Content-Type': 'application/json',
  },
})
```

---

## ENDPOINT REFERENCE

### 1. HEALTH CHECK

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.3.0",
  "timestamp": "2025-12-30T10:00:00Z"
}
```

**Usage:** Check if backend is running before displaying data.

---

### 2. INSTRUMENTS

#### List All Instruments
```
GET /api/v1/instruments/
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| active_only | boolean | true | Filter to active instruments only |

**Response:**
```json
[
  {
    "instrument_id": "uuid-1234",
    "symbol": "SAMPLE_INST",
    "display_name": "Sample Asset",
    "created_at": "2025-12-27T00:00:00Z",
    "updated_at": "2025-12-27T00:00:00Z",
    "is_active": true,
    "metadata": {}
  }
]
```

#### Get Single Instrument
```
GET /api/v1/instruments/{instrument_id}
```

**Response:** Same as single item in list above.

#### Get Instrument by Symbol
```
GET /api/v1/instruments/symbol/{symbol}
```

**Example:** `GET /api/v1/instruments/symbol/SAMPLE_INST`

#### Create Instrument
```
POST /api/v1/instruments/
```

**Request Body:**
```json
{
  "symbol": "SAMPLE_INST",
  "display_name": "Sample Asset"
}
```

#### Update Instrument
```
PATCH /api/v1/instruments/{instrument_id}
```

**Request Body:**
```json
{
  "display_name": "Updated Display Name",
  "is_active": true
}
```

**Response:** Updated Instrument object.

#### Delete Instrument
```
DELETE /api/v1/instruments/{instrument_id}
```

---

### 3. SILOS

#### List All Silos
```
GET /api/v1/silos/
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| instrument_id | string | null | Filter by instrument |
| active_only | boolean | true | Filter to active silos only |

**Response:**
```json
[
  {
    "silo_id": "uuid-5678",
    "instrument_id": "uuid-1234",
    "silo_name": "SAMPLE_INST Primary",
    "heartbeat_enabled": true,
    "heartbeat_frequency_min": 5,
    "current_threshold_min": 2,
    "recent_threshold_min": 10,
    "stale_threshold_min": 30,
    "created_at": "2025-12-27T00:00:00Z",
    "updated_at": "2025-12-27T00:00:00Z",
    "is_active": true
  }
]
```

#### Get Single Silo
```
GET /api/v1/silos/{silo_id}
```

#### Create Silo
```
POST /api/v1/silos/
```

**Request Body:**
```json
{
  "instrument_id": "uuid-1234",
  "silo_name": "SAMPLE_INST Primary",
  "heartbeat_enabled": true,
  "heartbeat_frequency_min": 5,
  "current_threshold_min": 2,
  "recent_threshold_min": 10,
  "stale_threshold_min": 30
}
```

#### Delete Silo
```
DELETE /api/v1/silos/{silo_id}
```

---

### 4. CHARTS

#### List All Charts
```
GET /api/v1/charts/
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| silo_id | string | null | Filter by silo |
| active_only | boolean | true | Filter to active charts only |

**Response:**
```json
[
  {
    "chart_id": "uuid-9012",
    "silo_id": "uuid-5678",
    "chart_code": "01A",
    "chart_name": "Momentum Health",
    "timeframe": "Daily",
    "webhook_id": "SAMPLE_01A",
    "created_at": "2025-12-27T00:00:00Z",
    "updated_at": "2025-12-27T00:00:00Z",
    "is_active": true
  }
]
```

**CRITICAL:** Chart has NO `weight` property. All charts are equal.

#### Get Single Chart
```
GET /api/v1/charts/{chart_id}
```

**Response:** Single Chart object.

#### Get Chart by Webhook ID
```
GET /api/v1/charts/webhook/{webhook_id}
```

**Example:** `GET /api/v1/charts/webhook/SAMPLE_01A`

#### Create Chart
```
POST /api/v1/charts/
```

**Request Body:**
```json
{
  "silo_id": "uuid-5678",
  "chart_code": "01A",
  "chart_name": "Momentum Health",
  "timeframe": "Daily",
  "webhook_id": "SAMPLE_01A"
}
```

#### Delete Chart
```
DELETE /api/v1/charts/{chart_id}
```

---

### 5. SIGNALS

#### List Signals for Chart
```
GET /api/v1/signals/chart/{chart_id}
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 100 | Maximum signals to return |

**Response:**
```json
[
  {
    "signal_id": "uuid-3456",
    "chart_id": "uuid-9012",
    "received_at": "2025-12-30T10:00:00Z",
    "signal_timestamp": "2025-12-30T09:59:00Z",
    "signal_type": "STATE_CHANGE",
    "direction": "BULLISH",
    "indicators": {
      "rsi": 35,
      "macd": "crossing_up"
    },
    "raw_payload": {}
  }
]
```

**CRITICAL:** Signal has NO `confidence` score. Scores imply judgment.

**Direction Values:**
- `BULLISH` - Upward bias
- `BEARISH` - Downward bias
- `NEUTRAL` - No clear bias

**Signal Types:**
- `HEARTBEAT` - Periodic confirmation signal
- `STATE_CHANGE` - Direction changed
- `MANUAL` - Manually injected signal

#### Get Latest Signal for Chart
```
GET /api/v1/signals/chart/{chart_id}/latest
```

**Response:** Single signal object or `null` if no signals.

#### Get Single Signal
```
GET /api/v1/signals/{signal_id}
```

---

### 6. RELATIONSHIPS (Contradictions & Confirmations)

#### Get Relationship Summary for Silo
```
GET /api/v1/relationships/silo/{silo_id}
```

**Response:**
```json
{
  "silo_id": "uuid-5678",
  "silo_name": "SAMPLE_INST Primary",
  "instrument_id": "uuid-1234",
  "instrument_symbol": "SAMPLE_INST",
  "charts": [
    {
      "chart_id": "uuid-9012",
      "chart_code": "01A",
      "chart_name": "Momentum Health",
      "timeframe": "Daily",
      "latest_signal": { ... },
      "freshness": "CURRENT"
    }
  ],
  "contradictions": [
    {
      "chart_a_id": "uuid-9012",
      "chart_a_name": "Momentum Health",
      "chart_a_direction": "BULLISH",
      "chart_b_id": "uuid-9013",
      "chart_b_name": "HTF Structure",
      "chart_b_direction": "BEARISH",
      "detected_at": "2025-12-30T10:00:00Z"
    }
  ],
  "confirmations": [
    {
      "chart_a_id": "uuid-9012",
      "chart_a_name": "Momentum Health",
      "chart_b_id": "uuid-9014",
      "chart_b_name": "Primary Trend",
      "aligned_direction": "BULLISH",
      "detected_at": "2025-12-30T10:00:00Z"
    }
  ],
  "generated_at": "2025-12-30T10:00:00Z"
}
```

**CRITICAL:** Display contradictions without resolution. Never suggest which chart is "correct".

**Freshness Values:**
- `CURRENT` - Signal received within current_threshold_min (default 2 min)
- `RECENT` - Signal received within recent_threshold_min (default 10 min)
- `STALE` - Signal older than stale_threshold_min (default 30 min)
- `UNAVAILABLE` - No signal ever received for this chart

#### Get Contradictions for Silo
```
GET /api/v1/relationships/contradictions/silo/{silo_id}
```

**Response:**
```json
{
  "contradictions": [ ... ],
  "count": 2
}
```

#### Get Relationships for Instrument
```
GET /api/v1/relationships/instrument/{instrument_id}
```

**Response:** Array of RelationshipSummary objects (one per silo).

---

### 7. NARRATIVES (AI Descriptions)

#### Generate Narrative for Silo
```
GET /api/v1/narratives/silo/{silo_id}
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| use_ai | boolean | true | Use Claude AI for generation |

**Response:**
```json
{
  "narrative_id": "uuid-7890",
  "silo_id": "uuid-5678",
  "sections": [
    {
      "section_type": "SIGNAL_SUMMARY",
      "content": "Currently, 8 of 12 charts have current signals...",
      "referenced_chart_ids": ["uuid-9012", "uuid-9013"]
    },
    {
      "section_type": "CONTRADICTION",
      "content": "There is a contradiction between Chart 01A and Chart 02...",
      "referenced_chart_ids": ["uuid-9012", "uuid-9013"]
    },
    {
      "section_type": "CONFIRMATION",
      "content": "Charts 01A, 07, and 08 all show bullish alignment...",
      "referenced_chart_ids": ["uuid-9012", "uuid-9014", "uuid-9015"]
    },
    {
      "section_type": "FRESHNESS",
      "content": "3 charts have stale data older than 30 minutes...",
      "referenced_chart_ids": ["uuid-9016", "uuid-9017", "uuid-9018"]
    }
  ],
  "closing_statement": "This is a description of what your charts are showing. The interpretation and any decision is entirely yours.",
  "generated_at": "2025-12-30T10:00:00Z"
}
```

**CRITICAL:** Every narrative MUST end with the closing statement disclaiming any recommendation.

#### Get Plain Text Narrative
```
GET /api/v1/narratives/silo/{silo_id}/plain
```

**Response:**
```json
{
  "text": "Currently, 8 of 12 charts have current signals...\n\nThis is a description of what your charts are showing. The interpretation and any decision is entirely yours.",
  "generated_at": "2025-12-30T10:00:00Z"
}
```

---

### 8. WEBHOOKS

#### Receive Webhook from TradingView
```
POST /api/v1/webhook/
```

**Request Body:**
```json
{
  "webhook_id": "SAMPLE_01A",
  "direction": "BULLISH",
  "indicators": {
    "rsi": 35,
    "macd": "crossing_up"
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "signal_id": "uuid-new",
  "chart_id": "uuid-9012",
  "direction": "BULLISH",
  "received_at": "2025-12-30T10:00:00Z"
}
```

#### Manual Signal Injection
```
POST /api/v1/webhook/manual
```

#### Webhook Health Check
```
GET /api/v1/webhook/health
```

---

### 9. BASKETS (Analytical Groupings)

#### List Baskets
```
GET /api/v1/baskets/
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| instrument_id | string | null | Filter by instrument |
| active_only | boolean | true | Filter to active baskets only |

**Response:**
```json
[
  {
    "basket_id": "uuid-basket-1",
    "basket_name": "Momentum Indicators",
    "basket_type": "LOGICAL",
    "description": "Charts focused on momentum analysis",
    "instrument_id": "uuid-1234",
    "chart_ids": ["uuid-9012", "uuid-9013"],
    "created_at": "2025-12-27T00:00:00Z",
    "updated_at": "2025-12-27T00:00:00Z",
    "is_active": true
  }
]
```

**Basket Types:**
- `LOGICAL` - Grouped by analysis type
- `HIERARCHICAL` - Grouped by timeframe hierarchy
- `CONTEXTUAL` - Grouped by market context
- `CUSTOM` - User-defined grouping

#### Get Single Basket
```
GET /api/v1/baskets/{basket_id}
```

**Response:** Single Basket object.

#### Create Basket
```
POST /api/v1/baskets/
```

#### Add Chart to Basket
```
POST /api/v1/baskets/{basket_id}/charts/{chart_id}
```

#### Remove Chart from Basket
```
DELETE /api/v1/baskets/{basket_id}/charts/{chart_id}
```

#### Delete Basket
```
DELETE /api/v1/baskets/{basket_id}
```

---

### 10. PLATFORMS (Kite Integration)

#### List Connected Platforms
```
GET /api/v1/platforms/
```

**Response:**
```json
[
  {
    "platform_name": "kite",
    "display_name": "Zerodha Kite",
    "status": "connected",
    "connected_at": "2025-12-30T09:00:00Z"
  }
]
```

#### Get Platform Status
```
GET /api/v1/platforms/{platform_name}
```

#### Connect to Platform
```
POST /api/v1/platforms/connect
```

**Request Body:**
```json
{
  "platform_name": "kite",
  "credentials": {
    "api_key": "xxx",
    "api_secret": "xxx"
  }
}
```

**Response:**
```json
{
  "status": "connecting",
  "platform_name": "kite",
  "message": "Connection initiated"
}
```

#### Disconnect Platform
```
POST /api/v1/platforms/{platform_name}/disconnect
```

**Response:**
```json
{
  "status": "disconnected",
  "platform_name": "kite"
}
```

#### Platform Health Check
```
GET /api/v1/platforms/{platform_name}/health
```

**Response:**
```json
{
  "platform_name": "kite",
  "status": "healthy",
  "last_heartbeat": "2025-12-30T10:00:00Z",
  "latency_ms": 45
}
```

#### Get Setup Instructions
```
GET /api/v1/platforms/{platform_name}/setup
```

**Response:**
```json
{
  "platform_name": "kite",
  "display_name": "Zerodha Kite",
  "instructions": [
    "1. Log in to kite.zerodha.com",
    "2. Go to API settings",
    "3. Generate API key"
  ],
  "documentation_url": "https://kite.trade/docs/connect/v3/"
}
```

#### Kite Login (OAuth)
```
GET /api/v1/platforms/kite/login
```

**Response:** Redirects to Zerodha login page.

#### Kite OAuth Callback
```
GET /api/v1/platforms/kite/callback?request_token=xxx&status=success
```

**Note:** This is called by Zerodha after user authenticates.

#### Kite Connection Status
```
GET /api/v1/platforms/kite/status
```

**Response:**
```json
{
  "connected": true,
  "user_id": "AB1234",
  "user_name": "Neville Mehta",
  "connected_at": "2025-12-30T09:00:00Z"
}
```

#### Get Watchlists
```
GET /api/v1/platforms/{platform_name}/watchlists
```

---

## API USAGE IN REACT

### Example: Fetching Instrument Data
```typescript
import { instrumentsApi } from '../services/api'

const InstrumentList = () => {
  const [instruments, setInstruments] = useState<Instrument[]>([])

  useEffect(() => {
    instrumentsApi.list(true).then(setInstruments)
  }, [])

  return (
    <div>
      {instruments.map(inst => (
        <InstrumentCard key={inst.instrument_id} instrument={inst} />
      ))}
    </div>
  )
}
```

### Example: Fetching Relationships with Contradictions
```typescript
import { relationshipsApi } from '../services/api'

const SiloDashboard = ({ siloId }: { siloId: string }) => {
  const [data, setData] = useState<RelationshipSummary | null>(null)

  useEffect(() => {
    relationshipsApi.getForSilo(siloId).then(setData)
  }, [siloId])

  return (
    <div>
      {data?.contradictions.map(c => (
        <ContradictionAlert key={`${c.chart_a_id}-${c.chart_b_id}`} contradiction={c} />
      ))}
    </div>
  )
}
```

---

---

### 11. CLAUDE AI INTEGRATION

#### List Available AI Models
```
GET /api/v1/ai/models
```

**Response:**
```json
{
  "models": [
    {
      "id": "claude-3-haiku",
      "display_name": "Haiku",
      "description": "Fast responses for simple queries",
      "cost_per_1k_input_tokens": 0.00025,
      "cost_per_1k_output_tokens": 0.00125,
      "max_tokens": 4096,
      "capabilities": ["quick_query", "simple_description"],
      "recommended_for": ["single_chart", "freshness_check"]
    },
    {
      "id": "claude-3-sonnet",
      "display_name": "Sonnet",
      "description": "Balanced performance for standard analysis",
      "cost_per_1k_input_tokens": 0.003,
      "cost_per_1k_output_tokens": 0.015,
      "max_tokens": 4096,
      "capabilities": ["narrative", "multi_chart", "contradiction_description"],
      "recommended_for": ["silo_narrative", "relationship_analysis"]
    },
    {
      "id": "claude-opus-4",
      "display_name": "Opus",
      "description": "Most capable model for complex analysis",
      "cost_per_1k_input_tokens": 0.015,
      "cost_per_1k_output_tokens": 0.075,
      "max_tokens": 4096,
      "capabilities": ["complex_analysis", "multi_silo", "comprehensive_narrative"],
      "recommended_for": ["instrument_overview", "complex_patterns"]
    }
  ],
  "default_model": "claude-3-sonnet",
  "budget_remaining": 47.50
}
```

**Usage:** Populate model selector dropdown/tabs in UI.

#### Get AI Usage Statistics
```
GET /api/v1/ai/usage
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| period | string | "monthly" | Period type: daily, weekly, monthly |

**Response:**
```json
{
  "period": "monthly",
  "period_start": "2025-12-01T00:00:00Z",
  "period_end": "2025-12-31T23:59:59Z",
  "tokens_used": {
    "input": 125000,
    "output": 45000,
    "total": 170000
  },
  "cost": {
    "amount": 2.50,
    "currency": "USD"
  },
  "budget": {
    "limit": 50.00,
    "used": 2.50,
    "remaining": 47.50,
    "percentage_used": 5.0
  },
  "requests_count": 150,
  "average_tokens_per_request": 1133,
  "model_breakdown": [
    {
      "model_id": "claude-3-haiku",
      "requests": 100,
      "tokens": 50000,
      "cost": 0.25
    },
    {
      "model_id": "claude-3-sonnet",
      "requests": 45,
      "tokens": 110000,
      "cost": 2.00
    },
    {
      "model_id": "claude-opus-4",
      "requests": 5,
      "tokens": 10000,
      "cost": 0.25
    }
  ]
}
```

**Usage:** Display usage dashboard, budget warnings.

#### Get Budget Status
```
GET /api/v1/ai/budget
```

**Response:**
```json
{
  "limit": 50.00,
  "used": 2.50,
  "remaining": 47.50,
  "percentage_used": 5.0,
  "alert_threshold": 80,
  "alert_triggered": false
}
```

**Usage:** Quick budget check without full usage details.

#### AI Health Check
```
GET /api/v1/ai/health
```

**Response:**
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "last_successful_call": "2025-12-30T10:00:00Z",
  "error_rate_24h": 0.02
}
```

**Usage:** Verify AI service is operational before making requests.

#### Configure AI Settings
```
POST /api/v1/ai/configure
```

**Request Body:**
```json
{
  "default_model": "claude-3-sonnet",
  "budget_limit": 50.00,
  "alert_threshold": 80,
  "rate_limit": {
    "requests_per_minute": 20,
    "tokens_per_minute": 100000
  },
  "fallback_model": "claude-3-haiku"
}
```

**Response:**
```json
{
  "status": "configured",
  "settings": {
    "default_model": "claude-3-sonnet",
    "budget_limit": 50.00,
    "alert_threshold": 80,
    "fallback_model": "claude-3-haiku"
  }
}
```

#### Per-Instrument Chat
```
POST /api/v1/chat/{scrip_id}
```

**Request Body:**
```json
{
  "message": "What are the current signals showing for this instrument?",
  "model": "claude-3-sonnet",
  "include_context": true,
  "conversation_id": "conv-uuid-optional"
}
```

**Response:**
```json
{
  "conversation_id": "conv-uuid-1234",
  "message": {
    "role": "assistant",
    "content": "Currently, 8 of 12 charts are displaying signals. Chart 01A shows BULLISH, while Chart 02 shows BEARISH, indicating a contradiction between momentum and structure timeframes...\n\nThis is a description of what your charts are showing. The interpretation and any decision is entirely yours."
  },
  "context_used": {
    "signals_included": 8,
    "charts_referenced": ["01A", "02", "04A", "05A", "06", "07", "08", "09"]
  },
  "usage": {
    "input_tokens": 1250,
    "output_tokens": 350,
    "cost": 0.009,
    "model_used": "claude-3-sonnet"
  },
  "disclaimer": "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."
}
```

**CRITICAL:** AI response MUST contain only descriptions, NEVER recommendations. The mandatory disclaimer MUST always appear.

#### Evaluate Strategy (Descriptive Only)
```
POST /api/v1/strategy/evaluate
```

**Request Body:**
```json
{
  "scrip_id": "uuid-1234",
  "strategy_description": "I am considering entering a long position based on the daily momentum signals",
  "model": "claude-3-sonnet"
}
```

**Response:**
```json
{
  "analysis": {
    "alignment_with_signals": "Currently, 5 charts show BULLISH signals which would align with a long position consideration. 2 charts show BEARISH signals which would contradict this direction. 5 charts have no current signal.",
    "contradictions_noted": [
      "Chart 01A (BULLISH) contradicts Chart 02 (BEARISH)",
      "Chart 05A (BULLISH) contradicts Chart 04B (BEARISH)"
    ],
    "confirmations_noted": [
      "Charts 01A, 07, and 08 all show BULLISH alignment",
      "Charts 05A and 05B both show BULLISH alignment"
    ],
    "freshness_concerns": [
      "Chart 06 signal is STALE (last updated 48 hours ago)",
      "Chart 09 has no signal (UNAVAILABLE)"
    ]
  },
  "disclaimer": "This analysis describes how your stated strategy aligns with current chart signals. It is NOT a recommendation to proceed or not proceed. The decision is entirely yours.",
  "usage": {
    "input_tokens": 1500,
    "output_tokens": 400,
    "cost": 0.011,
    "model_used": "claude-3-sonnet"
  }
}
```

**CRITICAL PROHIBITION:** This endpoint MUST NEVER return:
- Probability of success
- Risk scores
- "You should" statements
- Any form of recommendation

#### Get Conversation History
```
GET /api/v1/chat/{scrip_id}/history
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 50 | Maximum messages to return |

**Response:**
```json
{
  "scrip_id": "uuid-1234",
  "conversations": [
    {
      "conversation_id": "conv-uuid-1234",
      "messages": [
        {"role": "user", "content": "What signals are current?", "timestamp": "..."},
        {"role": "assistant", "content": "Currently...", "timestamp": "..."}
      ],
      "created_at": "2025-12-30T10:00:00Z",
      "total_tokens": 1600,
      "total_cost": 0.009
    }
  ]
}
```

---

### 12. DYNAMIC MODEL SELECTION ALGORITHM

The backend automatically selects the appropriate Claude model unless user overrides:

```
Selection Logic:
┌─────────────────────────────────────────────────────┐
│  User specified model?  ──YES──► Use specified      │
│          │                                          │
│          NO                                         │
│          ▼                                          │
│  Token estimate < 500?  ──YES──► Use HAIKU          │
│          │                                          │
│          NO                                         │
│          ▼                                          │
│  Charts involved > 6?   ──YES──► Use OPUS           │
│          │                                          │
│          NO                                         │
│          ▼                                          │
│  Complexity = complex?  ──YES──► Use OPUS           │
│          │                                          │
│          NO                                         │
│          ▼                                          │
│  Default: Use SONNET                                │
└─────────────────────────────────────────────────────┘
```

---

### 13. AI SAFETY VALIDATION

Every AI response is validated before returning to user:

**Prohibited Patterns (Auto-Rejected):**
- `\bshould\b` - "you should buy"
- `\brecommend\b` - "I recommend"
- `\bsuggest\b` - "I suggest"
- `\bconsider\b` - "consider selling"
- `\bconfidence\b.*\d+%` - "72% confidence"
- `\bprobability\b` - "probability of success"

**Required Elements:**
- Mandatory disclaimer must be present
- Response must be purely descriptive

---

## ERROR RESPONSES

All errors follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `204` - No Content (successful delete)
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error
- `503` - Service Unavailable (AI service down)

---

## DATA DICTIONARY

### Core Entities

#### Instrument
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| instrument_id | UUID | Primary key | Auto-generated |
| symbol | string | Trading symbol | Unique, max 20 chars |
| display_name | string | Human-readable name | Max 100 chars |
| is_active | boolean | Active status | Default: true |
| metadata | JSON | Additional data | Optional |
| created_at | datetime | Creation timestamp | Auto-generated |
| updated_at | datetime | Last update | Auto-updated |

#### Silo
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| silo_id | UUID | Primary key | Auto-generated |
| instrument_id | UUID | Parent instrument | Foreign key |
| silo_name | string | Silo name | Max 100 chars |
| heartbeat_enabled | boolean | Enable heartbeat | Default: true |
| heartbeat_frequency_min | integer | Heartbeat interval | Default: 5 |
| current_threshold_min | integer | CURRENT threshold | Default: 2 |
| recent_threshold_min | integer | RECENT threshold | Default: 10 |
| stale_threshold_min | integer | STALE threshold | Default: 30 |
| is_active | boolean | Active status | Default: true |

#### Chart
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| chart_id | UUID | Primary key | Auto-generated |
| silo_id | UUID | Parent silo | Foreign key |
| chart_code | string | Chart code | e.g., "01A", "02" |
| chart_name | string | Chart name | Max 100 chars |
| timeframe | string | Chart timeframe | e.g., "Daily", "3H" |
| webhook_id | string | Webhook identifier | Unique per instrument |
| is_active | boolean | Active status | Default: true |

**CRITICAL:** Chart has NO weight field. All charts are equal.

#### Signal
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| signal_id | UUID | Primary key | Auto-generated |
| chart_id | UUID | Parent chart | Foreign key |
| received_at | datetime | When received | Auto-generated |
| signal_timestamp | datetime | Signal time | From source |
| signal_type | enum | Type | HEARTBEAT, STATE_CHANGE, MANUAL |
| direction | enum | Direction | BULLISH, BEARISH, NEUTRAL |
| indicators | JSON | Indicator data | Optional |
| raw_payload | JSON | Original payload | For debugging |

**CRITICAL:** Signal has NO confidence field. Confidence implies judgment.

#### Conversation
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| conversation_id | UUID | Primary key | Auto-generated |
| scrip_id | UUID | Parent instrument | Foreign key |
| messages | JSON[] | Message history | Array of {role, content, timestamp} |
| model_used | string | Claude model | e.g., "claude-3-sonnet" |
| total_tokens | integer | Cumulative tokens | Running total |
| total_cost | decimal | Cumulative cost | USD |
| created_at | datetime | Creation time | Auto-generated |
| updated_at | datetime | Last message | Auto-updated |

#### AIUsage
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | UUID | Primary key | Auto-generated |
| period_type | enum | Period type | DAILY, WEEKLY, MONTHLY |
| period_start | date | Period start | Required |
| period_end | date | Period end | Required |
| input_tokens | integer | Input tokens | Default: 0 |
| output_tokens | integer | Output tokens | Default: 0 |
| total_cost | decimal | Total cost USD | Default: 0 |
| requests_count | integer | Request count | Default: 0 |
| model_breakdown | JSON | Per-model stats | Optional |

### Enums

#### Direction
```typescript
type Direction = 'BULLISH' | 'BEARISH' | 'NEUTRAL'
```

#### FreshnessStatus
```typescript
type FreshnessStatus = 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'
```

#### SignalType
```typescript
type SignalType = 'HEARTBEAT' | 'STATE_CHANGE' | 'MANUAL'
```

#### RelationshipType
```typescript
type RelationshipType = 'CONTRADICTION' | 'CONFIRMATION'
```
