# CIA-SIE Master Data Reference

> **Document ID:** CIA-SIE-MDR-001
> **Version:** 1.0.0
> **Date:** 2026-01-04
> **Status:** Verified against live backend API
> **Purpose:** Single source of truth for all data structures, flows, and component mappings

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Entity Hierarchy](#2-entity-hierarchy)
3. [Verified Data Models](#3-verified-data-models)
4. [API Endpoint Reference](#4-api-endpoint-reference)
5. [Frontend Component Data Flow](#5-frontend-component-data-flow)
6. [Constitutional Constraints](#6-constitutional-constraints)
7. [Backend Architecture Context](#7-backend-architecture-context)
8. [Verification Evidence](#8-verification-evidence)

---

## 1. Executive Summary

This master document consolidates:
- **Verified data types** from live API testing
- **Component-level data flow** from frontend architecture
- **Backend context** from code audit

### Key Statistics

| Category | Count |
|----------|-------|
| Domain Models | 8 |
| API Endpoints | 25+ |
| Frontend Components | 26 |
| React Query Hooks | 14 |
| Constitutional Markers | 11 |

---

## 2. Entity Hierarchy

```
INSTRUMENT (Top-level tradeable asset)
    │
    ├── SILO (Analysis container)
    │       │
    │       ├── CHART (TradingView chart)
    │       │       │
    │       │       └── SIGNAL (Point-in-time data)
    │       │
    │       ├── CONTRADICTION (Detected conflict)
    │       │
    │       └── CONFIRMATION (Detected alignment)
    │
    └── CONVERSATION (AI chat history)

ANALYTICAL_BASKET (UI-only grouping - no processing impact)
    │
    └── BASKET_CHARTS (Many-to-many with Chart)

AI_USAGE (Token/cost tracking)
```

---

## 3. Verified Data Models

> ⚠️ These types have been verified against live API responses on 2026-01-04

### 3.1 Instrument

```typescript
interface Instrument {
  instrument_id: string          // UUID
  symbol: string                 // "NIFTY", "BANKNIFTY"
  display_name: string           // "Nifty 50 Index"
  is_active: boolean
  metadata: Record<string, unknown> | null  // ✓ Verified: 'metadata' not 'metadata_json'
  created_at: string             // ISO datetime
  updated_at: string             // ISO datetime
}
```

### 3.2 Silo

```typescript
interface Silo {
  silo_id: string
  instrument_id: string          // FK to Instrument
  silo_name: string
  heartbeat_enabled: boolean
  heartbeat_frequency_min: number
  current_threshold_min: number  // Freshness: CURRENT if < this
  recent_threshold_min: number   // Freshness: RECENT if < this
  stale_threshold_min: number    // Freshness: STALE if < this
  created_at: string
  updated_at: string
  is_active: boolean
}
```

### 3.3 Chart ★ CONSTITUTIONAL

```typescript
interface Chart {
  chart_id: string
  silo_id: string                // FK to Silo
  chart_code: string             // "RSI15M", "MACD1H"
  chart_name: string             // "RSI 15-Minute"
  timeframe: string              // "1m"|"5m"|"15m"|"30m"|"1h"|"4h"|"D"|"W"|"M"
  webhook_id: string             // Unique webhook identifier
  created_at: string
  updated_at: string
  is_active: boolean

  // ★ CONSTITUTIONAL: NO weight field
  // ★ CONSTITUTIONAL: NO priority field
  // ★ CONSTITUTIONAL: NO importance field
}
```

### 3.4 Signal ★ CONSTITUTIONAL

```typescript
interface Signal {
  signal_id: string
  chart_id: string               // FK to Chart
  received_at: string            // When backend received it
  signal_timestamp: string       // When TradingView generated it
  signal_type: 'HEARTBEAT' | 'STATE_CHANGE' | 'BAR_CLOSE' | 'MANUAL'
  direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
  indicators: Record<string, number | string>
  raw_payload: Record<string, unknown>

  // ★ CONSTITUTIONAL: NO confidence field
  // ★ CONSTITUTIONAL: NO strength field
  // ★ CONSTITUTIONAL: NO weight field
  // ★ CONSTITUTIONAL: NO score field
}
```

### 3.5 Contradiction ★ CONSTITUTIONAL CR-002

```typescript
interface Contradiction {
  chart_a_id: string
  chart_a_name: string
  chart_a_direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
  chart_b_id: string
  chart_b_name: string
  chart_b_direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
  detected_at: string            // ISO datetime

  // ★ CONSTITUTIONAL: NO resolution field
  // ★ CONSTITUTIONAL: NO preferred_side field
  // ★ CONSTITUTIONAL: Both sides MUST have equal visual weight
}
```

### 3.6 Confirmation

```typescript
interface Confirmation {
  chart_a_id: string
  chart_a_name: string
  chart_b_id: string
  chart_b_name: string
  aligned_direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
  detected_at: string
}
```

### 3.7 RelationshipSummary

```typescript
interface ChartSignalStatus {
  chart_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  latest_signal: Signal | null
  freshness: 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'
}

interface RelationshipSummary {
  silo_id: string
  silo_name: string
  instrument_id: string
  instrument_symbol: string
  charts: ChartSignalStatus[]
  contradictions: Contradiction[]
  confirmations: Confirmation[]
  generated_at: string
}
```

### 3.8 Narrative ★ CONSTITUTIONAL CR-003

```typescript
interface NarrativeSection {
  section_type: 'SIGNAL_SUMMARY' | 'CONTRADICTION' | 'CONFIRMATION' | 'FRESHNESS'
  content: string                // ✓ Verified: 'section_type' not 'title'
  referenced_chart_ids: string[]
}

interface NarrativeResponse {
  narrative_id: string
  silo_id: string
  sections: NarrativeSection[]
  closing_statement: string      // ★ MANDATORY disclaimer
  generated_at: string

  // ★ CONSTITUTIONAL: MUST be accompanied by Disclaimer component
}
```

### 3.9 AI Model ✓ CORRECTED

```typescript
interface AIModel {
  id: string                           // ✓ Verified: 'id' not 'model_id'
  display_name: string                 // "Haiku", "Sonnet", "Opus"
  description: string
  cost_per_1k_input_tokens: number     // ✓ Verified field name
  cost_per_1k_output_tokens: number    // ✓ Verified field name
  max_tokens: number
  capabilities: string[]
  recommended_for: string[]
}
```

### 3.10 AI Budget ✓ CORRECTED

```typescript
interface AIBudgetResponse {
  within_budget: boolean          // ✓ Verified: not 'daily_limit'
  percentage_used: number         // ✓ Verified: not 'used_today'
  remaining: number
  alert_level: string | null      // "warning" | "critical" | null
  message: string | null
}
```

### 3.11 Chat

```typescript
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

interface ChatResponse {
  conversation_id: string
  message: ChatMessage
  context_used: {
    signals_included: number
    charts_referenced: string[]
  }
  usage: {
    input_tokens: number
    output_tokens: number
    cost: number
    model_used: string
  }
  disclaimer: string             // ★ MANDATORY
}
```

---

## 4. API Endpoint Reference

### 4.1 Complete Endpoint Table

| Endpoint | Method | Returns | Constitutional |
|----------|--------|---------|----------------|
| `/api/v1/instruments/` | GET | `Instrument[]` | - |
| `/api/v1/instruments/{id}` | GET | `Instrument` | - |
| `/api/v1/instruments/symbol/{symbol}` | GET | `Instrument` | - |
| `/api/v1/silos/` | GET | `Silo[]` | - |
| `/api/v1/silos/{id}` | GET | `Silo` | - |
| `/api/v1/charts/` | GET | `Chart[]` | CR-001 (no weight) |
| `/api/v1/charts/{id}` | GET | `Chart` | CR-001 |
| `/api/v1/signals/chart/{id}` | GET | `Signal[]` | CR-001 (no confidence) |
| `/api/v1/signals/chart/{id}/latest` | GET | `Signal \| null` | CR-001 |
| `/api/v1/relationships/silo/{id}` | GET | `RelationshipSummary` | **CR-002** |
| `/api/v1/relationships/instrument/{id}` | GET | `RelationshipSummary[]` | **CR-002** |
| `/api/v1/relationships/contradictions/silo/{id}` | GET | `Contradiction[]` | **CR-002** |
| `/api/v1/narratives/silo/{id}` | GET | `NarrativeResponse` | **CR-003** |
| `/api/v1/narratives/silo/{id}/plain` | GET | `{ text, generated_at }` | **CR-003** |
| `/api/v1/ai/models` | GET | `{ models, default_model, budget_remaining }` | - |
| `/api/v1/ai/budget` | GET | `AIBudgetResponse` | - |
| `/api/v1/ai/usage` | GET | `AIUsageResponse` | - |
| `/api/v1/chat/{scrip_id}` | POST | `ChatResponse` | **CR-003** |
| `/api/v1/chat/{scrip_id}/history` | GET | `ChatHistoryResponse` | - |
| `/api/v1/webhook/` | POST | `{ signal_id }` | - |
| `/health` | GET | `HealthResponse` | - |

---

## 5. Frontend Component Data Flow

### 5.1 Page → Hook → Service → API Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PAGE COMPONENTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  HomePage                                                                   │
│  ├── useInstruments() → getInstruments() → GET /api/v1/instruments/        │
│  └── Renders: InstrumentList → InstrumentCard[]                            │
│                                                                             │
│  InstrumentDetailPage                                                       │
│  ├── useInstrument(id) → getInstrument() → GET /api/v1/instruments/{id}    │
│  ├── useSilos(instrumentId) → getSilos() → GET /api/v1/silos/              │
│  └── Renders: SiloList → SiloCard[]                                        │
│                                                                             │
│  SiloDetailPage ★★★ CONSTITUTIONAL CRITICAL ★★★                            │
│  ├── useSilo(id) → getSilo() → GET /api/v1/silos/{id}                      │
│  ├── useCharts(siloId) → getCharts() → GET /api/v1/charts/                 │
│  ├── useRelationships(siloId) → GET /api/v1/relationships/silo/{id} ★CR-002│
│  ├── useNarrative(siloId) → GET /api/v1/narratives/silo/{id} ★CR-003       │
│  └── Renders:                                                               │
│      ├── ChartList → ChartCard[]                                           │
│      ├── ContradictionPanel → ContradictionCard[] ★ EQUAL WEIGHT           │
│      ├── ConfirmationPanel → ConfirmationCard[]                            │
│      └── NarrativeDisplay + Disclaimer ★ MANDATORY                         │
│                                                                             │
│  ChartDetailPage                                                            │
│  ├── useChart(id) → getChart() → GET /api/v1/charts/{id}                   │
│  ├── useSignals(chartId) → getSignals() → GET /api/v1/signals/chart/{id}   │
│  └── Renders: SignalList → SignalCard[] (NO confidence/strength)           │
│                                                                             │
│  ChatPage ★ CR-003                                                          │
│  ├── useInstruments() → instrument selector                                 │
│  ├── useSendMessage() → POST /api/v1/chat/{scrip_id} ★ DESCRIPTIVE ONLY    │
│  ├── useHistory() → GET /api/v1/chat/{scrip_id}/history                    │
│  └── Renders: ChatInterface + Disclaimer ★ MANDATORY                       │
│                                                                             │
│  SettingsPage                                                               │
│  ├── useModels() → getModels() → GET /api/v1/ai/models                     │
│  ├── useBudget() → getBudget() → GET /api/v1/ai/budget                     │
│  ├── useUsage() → getUsage() → GET /api/v1/ai/usage                        │
│  └── Renders: ModelSelector, BudgetIndicator, UsageStats                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Constitutional Component Specifications

| Component | Spec ID | Requirement |
|-----------|---------|-------------|
| DirectionBadge | CBS-001 | Identical size for all directions, only color differs |
| FreshnessBadge | CBS-002 | Correct status thresholds and icons |
| Disclaimer | CBS-003 | Hardcoded text, non-dismissible, non-collapsible |
| ContradictionCard | CBS-004 | `grid-cols-[1fr,auto,1fr]` - equal sides |
| ContradictionPanel | CBS-005 | "No contradictions detected" empty state |
| NarrativeDisplay | CBS-006 | Always renders Disclaimer component |

---

## 6. Constitutional Constraints

### 6.1 CR-001: Decision-Support ONLY

| Enforcement | Location |
|-------------|----------|
| No weight field on Chart | `types/models.ts`, `dal/models.py` |
| No confidence/strength on Signal | `types/models.ts`, `dal/models.py` |
| No "Buy"/"Sell" buttons | All components |
| Forbidden words scan | AI response validation |

### 6.2 CR-002: NEVER Resolve Contradictions

| Enforcement | Location |
|-------------|----------|
| Equal grid layout | `ContradictionCard.tsx` line 16 |
| Identical CSS both sides | `ContradictionCard.tsx` line 11 |
| No resolution field | `Contradiction` type |
| No preferred_side field | `Contradiction` type |

### 6.3 CR-003: Descriptive NOT Prescriptive

| Enforcement | Location |
|-------------|----------|
| Hardcoded disclaimer text | `Disclaimer.tsx` lines 7-9 |
| Always render Disclaimer | `NarrativeDisplay.tsx` lines 35-36 |
| No dismiss functionality | `Disclaimer.tsx` |
| AI response validation | `response_validator.py` |

---

## 7. Backend Architecture Context

### 7.1 Module Structure

```
src/cia_sie/
├── api/routes/          # 12 route modules
├── ai/                  # 6 AI integration modules
├── core/                # 5 core definitions
├── dal/                 # 3 data access modules
├── exposure/            # 3 relationship detection modules
├── ingestion/           # 3 signal ingestion modules
└── platforms/           # 4 platform adapter modules
```

### 7.2 Signal Flow

```
TradingView → POST /webhook → WebhookHandler → SignalNormalizer → SignalRepository → Database
```

### 7.3 Narrative Flow

```
GET /narratives → NarrativeGenerator → PromptBuilder → ClaudeClient → ResponseValidator → NarrativeResponse
```

---

## 8. Verification Evidence

### 8.1 Live API Samples (2026-01-04)

**Instrument Response:**
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

**Signal Response:**
```json
{
  "signal_id": "ccb63db0-9775-4d5d-bfec-7d5bbc76ce7c",
  "chart_id": "e9f1d6f0-08a6-47a0-a5fa-73bf2be95467",
  "received_at": "2026-01-03T18:39:23.760527",
  "signal_timestamp": "2026-01-03T18:39:23.760649",
  "signal_type": "STATE_CHANGE",
  "direction": "BULLISH",
  "indicators": { "rsi": 72, "price": 24850.5 },
  "raw_payload": { ... }
}
```

**Contradiction Response:**
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

**AI Budget Response:**
```json
{
  "within_budget": true,
  "percentage_used": 0.0,
  "remaining": 50.0,
  "alert_level": null,
  "message": null
}
```

### 8.2 Verification Commands

```bash
# Verify constitutional markers
grep -rn "CONSTITUTIONAL" frontend/src/
# Expected: 11+ matches

# Verify ContradictionCard grid
grep -n "grid-cols-\[1fr,auto,1fr\]" frontend/src/components/relationships/ContradictionCard.tsx
# Expected: Line 16

# Verify Disclaimer in NarrativeDisplay
grep -n "Disclaimer" frontend/src/components/narratives/NarrativeDisplay.tsx
# Expected: Lines 2, 35-36

# Verify no Buy/Sell text
grep -rn "Buy\|Sell" frontend/src/
# Expected: No matches
```

---

## Document Lineage

| Source Document | Contribution |
|-----------------|--------------|
| `DATA_ARCHITECTURE.md` (newly created) | Verified data types, API samples |
| `CIA-SIE_FRONTEND_DATA_FLOW_ARCHITECTURE.md` | Component hierarchy, hook mapping |
| `CIA-SIE_BACKEND_ARCHITECTURE_ACCURATE.md` | Backend module structure, flows |

---

| Metadata | Value |
|----------|-------|
| Document ID | CIA-SIE-MDR-001 |
| Version | 1.0.0 |
| Created | 2026-01-04 |
| Verified Against | Live Backend API |
| Total Sections | 8 |

---

*End of CIA-SIE Master Data Reference*

