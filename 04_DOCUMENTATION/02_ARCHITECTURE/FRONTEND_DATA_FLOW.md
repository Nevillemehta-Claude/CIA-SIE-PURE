# CIA-SIE Frontend Data Flow Architecture

## Complete Component Hierarchy with Data Flow Mapping

---

| Document Metadata | Value |
|-------------------|-------|
| **Document ID** | CIA-SIE-DFA-001 |
| **Version** | 1.0.0 |
| **Date** | 2026-01-04 |
| **Author** | Claude Opus 4.5 |
| **Purpose** | Exhaustive mapping of frontend components to backend data sources |
| **Companion To** | CIA-SIE_PROJECT_MATURITY_AUDIT.md |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Data Model Definitions](#2-data-model-definitions)
3. [API Response Type Definitions](#3-api-response-type-definitions)
4. [Service Layer Mapping](#4-service-layer-mapping)
5. [Hook Layer Mapping](#5-hook-layer-mapping)
6. [Complete Component Hierarchy with Data Flow](#6-complete-component-hierarchy-with-data-flow)
7. [Page-by-Page Data Consumption](#7-page-by-page-data-consumption)
8. [Constitutional Constraint Integration](#8-constitutional-constraint-integration)
9. [Backend API Endpoint Summary](#9-backend-api-endpoint-summary)
10. [Data Flow Diagrams](#10-data-flow-diagrams)

---

## 1. Executive Summary

This document provides an exhaustive mapping of every frontend component to its data sources, tracing the complete path from:

```
Backend API Endpoint → Service Layer → React Query Hook → Component → Props → Child Components
```

### Key Statistics

| Layer | Count | Description |
|-------|-------|-------------|
| **Domain Models** | 12 | TypeScript interfaces in `types/models.ts` |
| **API Response Types** | 15 | TypeScript interfaces in `types/api.ts` |
| **Service Functions** | 22 | API client functions in `services/` |
| **Hooks** | 14 | React Query hooks in `hooks/` |
| **Pages** | 8 | Route components in `pages/` |
| **Components** | 26 | Reusable components in `components/` |
| **Constitutional Markers** | 7 | Components with CR-001/CR-002/CR-003 constraints |

---

## 2. Data Model Definitions

### Source: `frontend/src/types/models.ts` (96 lines)

#### 2.1 Instrument Model

```typescript
export interface Instrument {
  instrument_id: string      // UUID
  symbol: string             // e.g., "GOLD", "NIFTY"
  display_name: string       // e.g., "Gold Futures"
  is_active: boolean         // Active/inactive toggle
  metadata: Record<string, unknown>  // Extensible metadata
  created_at: string         // ISO timestamp
  updated_at: string         // ISO timestamp

  // CONSTITUTIONAL: NO weight field
  // CONSTITUTIONAL: NO priority field
  // CONSTITUTIONAL: NO score field
}
```

#### 2.2 Silo Model

```typescript
export interface Silo {
  silo_id: string            // UUID
  instrument_id: string      // FK to Instrument
  silo_name: string          // e.g., "Gold Daily Analysis"
  heartbeat_enabled: boolean // Enable/disable heartbeat
  heartbeat_interval_seconds: number  // Heartbeat frequency
  stale_threshold_seconds: number     // When signals become stale
  recent_threshold_seconds: number    // When signals become recent
  created_at: string
  updated_at: string

  // CONSTITUTIONAL: NO aggregated_score field
  // CONSTITUTIONAL: NO combined_signal field
}
```

#### 2.3 Chart Model

```typescript
export interface Chart {
  chart_id: string           // UUID
  silo_id: string            // FK to Silo
  chart_code: string         // e.g., "GOLD-D-RSI"
  chart_name: string         // e.g., "Daily RSI"
  timeframe: string          // e.g., "D", "H4", "M15"
  webhook_id: string         // TradingView webhook identifier
  description: string | null
  created_at: string
  updated_at: string

  // CONSTITUTIONAL: NO weight field ★
  // CONSTITUTIONAL: NO importance field
  // CONSTITUTIONAL: NO priority field
}
```

#### 2.4 Signal Model ★ CONSTITUTIONAL CRITICAL

```typescript
export interface Signal {
  signal_id: string          // UUID
  chart_id: string           // FK to Chart
  received_at: string        // When backend received it
  signal_timestamp: string   // When TradingView generated it
  signal_type: SignalType    // ENTRY | EXIT | ALERT
  direction: Direction       // BULLISH | BEARISH | NEUTRAL
  indicators: Record<string, number | string>  // Indicator values
  raw_payload: Record<string, unknown>  // Original webhook JSON

  // CONSTITUTIONAL: NO confidence field ★
  // CONSTITUTIONAL: NO strength field ★
  // CONSTITUTIONAL: NO weight field ★
  // CONSTITUTIONAL: NO score field ★
  // CONSTITUTIONAL: NO recommendation field ★
}
```

#### 2.5 Contradiction Model ★ CR-002 CRITICAL

```typescript
export interface Contradiction {
  chart_a_id: string         // First chart ID
  chart_a_name: string       // First chart name
  chart_a_direction: Direction  // BULLISH | BEARISH
  chart_b_id: string         // Second chart ID
  chart_b_name: string       // Second chart name
  chart_b_direction: Direction  // Opposite direction
  detected_at: string        // When contradiction detected

  // CONSTITUTIONAL: NO resolution field ★
  // CONSTITUTIONAL: NO preferred_side field ★
  // CONSTITUTIONAL: NO weight field ★
  // CONSTITUTIONAL: Both sides MUST have equal visual weight
}
```

#### 2.6 Confirmation Model

```typescript
export interface Confirmation {
  chart_a_id: string
  chart_a_name: string
  chart_a_direction: Direction
  chart_b_id: string
  chart_b_name: string
  chart_b_direction: Direction  // Same direction as chart_a
  aligned_direction: Direction  // The common direction
  detected_at: string
}
```

#### 2.7 Enums

```typescript
export type Direction = 'BULLISH' | 'BEARISH' | 'NEUTRAL'

export type SignalType = 'ENTRY' | 'EXIT' | 'ALERT'

export type FreshnessStatus = 'CURRENT' | 'RECENT' | 'STALE'

export type AIModel = 'haiku' | 'sonnet' | 'opus'
```

#### 2.8 AI Models

```typescript
export interface AIModelInfo {
  id: string                 // 'haiku' | 'sonnet' | 'opus'
  display_name: string       // e.g., "Claude 3.5 Haiku"
  input_cost_per_1k: number  // Cost per 1K input tokens
  output_cost_per_1k: number // Cost per 1K output tokens
  max_tokens: number         // Maximum context length
  capabilities: string[]     // e.g., ['fast', 'coding']
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}
```

---

## 3. API Response Type Definitions

### Source: `frontend/src/types/api.ts` (121 lines)

#### 3.1 List Responses

```typescript
export interface InstrumentListResponse {
  instruments: Instrument[]
  total: number
}

export interface SiloListResponse {
  silos: Silo[]
  total: number
}

export interface ChartListResponse {
  charts: Chart[]
  total: number
}

export interface SignalListResponse {
  signals: Signal[]
  total: number
}
```

#### 3.2 Relationship Responses ★ CR-002 CRITICAL

```typescript
export interface RelationshipResponse {
  silo_id: string
  contradictions: Contradiction[]  // ★ MUST be displayed with equal weight
  confirmations: Confirmation[]
  generated_at: string

  // CONSTITUTIONAL: NO resolved_contradictions field
  // CONSTITUTIONAL: NO net_direction field
  // CONSTITUTIONAL: NO aggregated_view field
}

export interface ContradictionsResponse {
  silo_id: string
  contradictions: Contradiction[]
  count: number
}
```

#### 3.3 Narrative Response ★ CR-003 CRITICAL

```typescript
export interface NarrativeSection {
  title: string              // Section header
  content: string            // Descriptive text

  // CONSTITUTIONAL: NO action_items field ★
  // CONSTITUTIONAL: NO recommendations field ★
}

export interface NarrativeResponse {
  narrative_id: string
  silo_id: string
  sections: NarrativeSection[]
  closing_statement: string
  generated_at: string
  model_used: string

  // CONSTITUTIONAL: MUST be accompanied by Disclaimer ★
  // CONSTITUTIONAL: Disclaimer CANNOT be dismissed ★
}

export interface PlainNarrativeResponse {
  narrative_id: string
  silo_id: string
  text: string              // Plain text version
  generated_at: string
}
```

#### 3.4 Chat Response ★ CR-003 CRITICAL

```typescript
export interface ChatResponse {
  response: string           // AI response text
  conversation_id: string    // For context continuity
  model_used: string         // Which Claude model
  tokens_used: number        // Token consumption
  cost: number               // USD cost

  // CONSTITUTIONAL: Response MUST be descriptive only ★
  // CONSTITUTIONAL: NO buy/sell advice ★
}

export interface ChatHistoryResponse {
  messages: ChatMessage[]
  conversation_id: string
}
```

#### 3.5 AI Configuration Responses

```typescript
export interface AIModelsResponse {
  models: AIModelInfo[]
  default_model: string
  budget_remaining: number
}

export interface AIBudgetResponse {
  daily_limit: number
  used_today: number
  remaining: number
  within_budget: boolean
  percentage_used: number
}

export interface AIUsageResponse {
  total_requests: number
  total_tokens: number
  total_cost: number
  by_model: Record<string, { requests: number; tokens: number; cost: number }>
}
```

---

## 4. Service Layer Mapping

### Source: `frontend/src/services/` (10 files, 179 lines)

Each service file maps to a backend API group. Here is the complete mapping:

### 4.1 Instruments Service

**File:** `services/instruments.ts` (18 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION          │ HTTP METHOD │ ENDPOINT                      │
├─────────────────────────────────────────────────────────────────────────┤
│ getInstruments()          │ GET         │ /api/v1/instruments           │
│ getInstrument(id)         │ GET         │ /api/v1/instruments/{id}      │
│ createInstrument(data)    │ POST        │ /api/v1/instruments           │
│ updateInstrument(id,data) │ PATCH       │ /api/v1/instruments/{id}      │
│ deleteInstrument(id)      │ DELETE      │ /api/v1/instruments/{id}      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Silos Service

**File:** `services/silos.ts` (14 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION          │ HTTP METHOD │ ENDPOINT                      │
├─────────────────────────────────────────────────────────────────────────┤
│ getSilos(params)          │ GET         │ /api/v1/silos?instrument_id=  │
│ getSilo(id)               │ GET         │ /api/v1/silos/{id}            │
│ createSilo(data)          │ POST        │ /api/v1/silos                 │
│ deleteSilo(id)            │ DELETE      │ /api/v1/silos/{id}            │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Charts Service

**File:** `services/charts.ts` (14 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION          │ HTTP METHOD │ ENDPOINT                      │
├─────────────────────────────────────────────────────────────────────────┤
│ getCharts(params)         │ GET         │ /api/v1/charts?silo_id=       │
│ getChart(id)              │ GET         │ /api/v1/charts/{id}           │
│ createChart(data)         │ POST        │ /api/v1/charts                │
│ deleteChart(id)           │ DELETE      │ /api/v1/charts/{id}           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Signals Service

**File:** `services/signals.ts` (25 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION          │ HTTP METHOD │ ENDPOINT                      │
├─────────────────────────────────────────────────────────────────────────┤
│ getSignals(chartId)       │ GET         │ /api/v1/signals/chart/{id}    │
│ getSignal(id)             │ GET         │ /api/v1/signals/{id}          │
│ getLatestSignal(chartId)  │ GET         │ /api/v1/signals/chart/{id}/   │
│                           │             │ latest                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.5 Relationships Service ★ CR-002 CRITICAL

**File:** `services/relationships.ts` (19 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION              │ HTTP METHOD │ ENDPOINT                  │
├─────────────────────────────────────────────────────────────────────────┤
│ getRelationships(siloId) ★    │ GET         │ /api/v1/relationships/    │
│                               │             │ silo/{id}                 │
│ getContradictions(siloId) ★   │ GET         │ /api/v1/relationships/    │
│                               │             │ contradictions/silo/{id}  │
│ getInstrumentRelationships(id)│ GET         │ /api/v1/relationships/    │
│                               │             │ instrument/{id}           │
└─────────────────────────────────────────────────────────────────────────┘

★ Returns data that MUST be displayed with equal visual weight per CR-002
```

### 4.6 Narratives Service ★ CR-003 CRITICAL

**File:** `services/narratives.ts` (13 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION              │ HTTP METHOD │ ENDPOINT                  │
├─────────────────────────────────────────────────────────────────────────┤
│ getNarrative(siloId) ★        │ GET         │ /api/v1/narratives/       │
│                               │             │ silo/{id}                 │
│ getPlainNarrative(siloId)     │ GET         │ /api/v1/narratives/       │
│                               │             │ silo/{id}/plain           │
└─────────────────────────────────────────────────────────────────────────┘

★ Returns AI-generated text that MUST include mandatory Disclaimer per CR-003
```

### 4.7 Chat Service ★ CR-003 CRITICAL

**File:** `services/chat.ts` (20 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION              │ HTTP METHOD │ ENDPOINT                  │
├─────────────────────────────────────────────────────────────────────────┤
│ sendMessage(scripId, msg) ★   │ POST        │ /api/v1/chat/{scripId}    │
│ getHistory(scripId)           │ GET         │ /api/v1/chat/{scripId}/   │
│                               │             │ history                   │
└─────────────────────────────────────────────────────────────────────────┘

★ AI responses are descriptive only, never prescriptive per CR-003
```

### 4.8 AI Service

**File:** `services/ai.ts` (21 lines)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ SERVICE FUNCTION              │ HTTP METHOD │ ENDPOINT                  │
├─────────────────────────────────────────────────────────────────────────┤
│ getModels()                   │ GET         │ /api/v1/ai/models         │
│ getUsage()                    │ GET         │ /api/v1/ai/usage          │
│ getBudget()                   │ GET         │ /api/v1/ai/budget         │
│ configure(settings)           │ POST        │ /api/v1/ai/configure      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Hook Layer Mapping

### Source: `frontend/src/hooks/` (9 files, 176 lines)

Each hook wraps a service function with React Query for caching and state management.

### 5.1 useInstruments Hook

**File:** `hooks/useInstruments.ts` (20 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                       │ SERVICE CALL         │ QUERY KEY              │
├─────────────────────────────────────────────────────────────────────────────┤
│ useInstruments(params?)    │ getInstruments()     │ ['instruments', params]│
│ useInstrument(id)          │ getInstrument(id)    │ ['instruments', id]    │
└─────────────────────────────────────────────────────────────────────────────┘

Returns: { data: Instrument[] | Instrument, isLoading, error, refetch }
```

### 5.2 useSilos Hook

**File:** `hooks/useSilos.ts` (20 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                       │ SERVICE CALL         │ QUERY KEY              │
├─────────────────────────────────────────────────────────────────────────────┤
│ useSilos(instrumentId?)    │ getSilos(params)     │ ['silos', instrumentId]│
│ useSilo(id)                │ getSilo(id)          │ ['silos', 'detail', id]│
└─────────────────────────────────────────────────────────────────────────────┘

Returns: { data: Silo[] | Silo, isLoading, error, refetch }
```

### 5.3 useCharts Hook

**File:** `hooks/useCharts.ts` (20 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                       │ SERVICE CALL         │ QUERY KEY              │
├─────────────────────────────────────────────────────────────────────────────┤
│ useCharts(siloId?)         │ getCharts(params)    │ ['charts', siloId]     │
│ useChart(id)               │ getChart(id)         │ ['charts', 'detail',id]│
└─────────────────────────────────────────────────────────────────────────────┘

Returns: { data: Chart[] | Chart, isLoading, error, refetch }
```

### 5.4 useSignals Hook

**File:** `hooks/useSignals.ts` (21 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                       │ SERVICE CALL         │ QUERY KEY              │
├─────────────────────────────────────────────────────────────────────────────┤
│ useSignals(chartId)        │ getSignals(chartId)  │ ['signals', chartId]   │
│ useSignal(id)              │ getSignal(id)        │ ['signals', 'detail',id│
└─────────────────────────────────────────────────────────────────────────────┘

Returns: { data: Signal[], isLoading, error, refetch }
Data Model: Signal (NO confidence, NO strength, NO weight per CR-001)
```

### 5.5 useRelationships Hook ★ CR-002 CRITICAL

**File:** `hooks/useRelationships.ts` (20 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                           │ SERVICE CALL              │ QUERY KEY     │
├─────────────────────────────────────────────────────────────────────────────┤
│ useRelationships(siloId) ★     │ getRelationships(siloId)  │ ['rels',siloId│
│ useContradictions(siloId) ★    │ getContradictions(siloId) │ ['contras',id]│
└─────────────────────────────────────────────────────────────────────────────┘

Returns: {
  data: RelationshipResponse {
    contradictions: Contradiction[]  ★ EQUAL VISUAL WEIGHT REQUIRED
    confirmations: Confirmation[]
  },
  isLoading,
  error,
  refetch
}

★ CONSTITUTIONAL: Contradictions MUST NOT be resolved or aggregated (CR-002)
```

### 5.6 useNarratives Hook ★ CR-003 CRITICAL

**File:** `hooks/useNarratives.ts` (13 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                           │ SERVICE CALL              │ QUERY KEY     │
├─────────────────────────────────────────────────────────────────────────────┤
│ useNarrative(siloId) ★         │ getNarrative(siloId)      │ ['narr',siloId│
└─────────────────────────────────────────────────────────────────────────────┘

Returns: {
  data: NarrativeResponse {
    sections: NarrativeSection[]  ★ DESCRIPTIVE ONLY
    closing_statement: string     ★ NO RECOMMENDATIONS
  },
  isLoading,
  error,
  refetch
}

★ CONSTITUTIONAL: MUST be displayed with Disclaimer component (CR-003)
★ CONSTITUTIONAL: Disclaimer CANNOT be dismissed or hidden
```

### 5.7 useChat Hook ★ CR-003 CRITICAL

**File:** `hooks/useChat.ts` (25 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                           │ SERVICE CALL              │ QUERY KEY     │
├─────────────────────────────────────────────────────────────────────────────┤
│ useChat(scripId)               │ sendMessage(scripId, msg) │ Mutation      │
│ useChatHistory(scripId)        │ getHistory(scripId)       │ ['chat', id]  │
└─────────────────────────────────────────────────────────────────────────────┘

Returns (useChat): {
  mutate: (message: string) => void,
  data: ChatResponse {
    response: string  ★ DESCRIPTIVE ONLY
  },
  isLoading,
  error
}

★ CONSTITUTIONAL: AI responses are information only (CR-003)
```

### 5.8 useAI Hook

**File:** `hooks/useAI.ts` (27 lines)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HOOK                           │ SERVICE CALL              │ QUERY KEY     │
├─────────────────────────────────────────────────────────────────────────────┤
│ useAIModels()                  │ getModels()               │ ['ai','models']
│ useAIBudget()                  │ getBudget()               │ ['ai','budget']
│ useAIUsage()                   │ getUsage()                │ ['ai','usage'] │
└─────────────────────────────────────────────────────────────────────────────┘

Returns: { data: AIModelsResponse | AIBudgetResponse | AIUsageResponse, ... }
```

---

## 6. Complete Component Hierarchy with Data Flow

This is the comprehensive component tree showing every component, its hooks, and its data consumption.

### 6.1 Application Root

```
App.tsx
│
├── <BrowserRouter>
│   │
│   └── <QueryClientProvider client={queryClient}>
│       │
│       └── <Routes>
│           │
│           ├── Route path="/" element={<AppShell />}
│           │   │
│           │   │   ┌────────────────────────────────────────────────────────┐
│           │   │   │ AppShell Component                                     │
│           │   │   │ File: components/layout/AppShell.tsx (58 lines)        │
│           │   │   │ Props: { children: ReactNode }                         │
│           │   │   │ Hooks: None                                            │
│           │   │   │ Data: None (layout only)                               │
│           │   │   └────────────────────────────────────────────────────────┘
│           │   │
│           │   ├── <Header />
│           │   │   │   ┌────────────────────────────────────────────────────┐
│           │   │   │   │ Header Component                                   │
│           │   │   │   │ File: components/layout/Header.tsx (65 lines)      │
│           │   │   │   │ Hooks: useAIBudget()                               │
│           │   │   │   │ Data: AIBudgetResponse                             │
│           │   │   │   └────────────────────────────────────────────────────┘
│           │   │   │
│           │   │   └── <BudgetIndicator budget={data} />
│           │   │           ┌────────────────────────────────────────────────┐
│           │   │           │ BudgetIndicator Component                      │
│           │   │           │ File: components/ai/BudgetIndicator.tsx (45 ln)│
│           │   │           │ Props: { budget: AIBudgetResponse }            │
│           │   │           │ Displays: percentage_used, remaining           │
│           │   │           └────────────────────────────────────────────────┘
│           │   │
│           │   ├── <Sidebar />
│           │   │       ┌────────────────────────────────────────────────────┐
│           │   │       │ Sidebar Component                                  │
│           │   │       │ File: components/layout/Sidebar.tsx (53 lines)     │
│           │   │       │ Props: None                                        │
│           │   │       │ Data: Static navigation links                      │
│           │   │       └────────────────────────────────────────────────────┘
│           │   │
│           │   └── <Outlet />  ──► Renders child routes below
│           │
│           └── Child Routes (see Section 6.2)
```

### 6.2 Page Components with Complete Data Flow

#### 6.2.1 HomePage (Route: `/`)

```
HomePage
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/HomePage.tsx (87 lines)                                       │
│   │ Route: /                                                                  │
│   │                                                                          │
│   │ HOOKS USED:                                                              │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useInstruments()                                                     │ │
│   │ │   → getInstruments()                                                 │ │
│   │ │   → GET /api/v1/instruments                                          │ │
│   │ │   → Returns: InstrumentListResponse { instruments: Instrument[] }    │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader title="Dashboard" />
│       ┌────────────────────────────────────────────────────────────────────┐
│       │ PageHeader Component                                               │
│       │ File: components/layout/PageHeader.tsx (35 lines)                  │
│       │ Props: { title: string, description?: string, backTo?: string }    │
│       └────────────────────────────────────────────────────────────────────┘
│
├── if (isLoading) → <Spinner size="lg" />
│
├── if (error) → <ErrorState title="..." message="..." />
│
└── <InstrumentList instruments={data.instruments} />
        ┌────────────────────────────────────────────────────────────────────┐
        │ InstrumentList Component                                           │
        │ File: components/instruments/InstrumentList.tsx (42 lines)         │
        │ Props: { instruments: Instrument[], isLoading?: boolean }          │
        └────────────────────────────────────────────────────────────────────┘
        │
        └── maps → <InstrumentCard instrument={inst} key={inst.instrument_id} />
                ┌────────────────────────────────────────────────────────────┐
                │ InstrumentCard Component                                   │
                │ File: components/instruments/InstrumentCard.tsx (48 lines) │
                │ Props: { instrument: Instrument }                          │
                │ Displays:                                                  │
                │   - instrument.symbol                                      │
                │   - instrument.display_name                                │
                │   - instrument.is_active (badge)                           │
                │ Links to: /instruments/{instrument_id}                     │
                └────────────────────────────────────────────────────────────┘
```

#### 6.2.2 InstrumentsPage (Route: `/instruments`)

```
InstrumentsPage
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/InstrumentsPage.tsx (65 lines)                               │
│   │ Route: /instruments                                                      │
│   │                                                                          │
│   │ HOOKS USED:                                                              │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useInstruments()                                                     │ │
│   │ │   → getInstruments()                                                 │ │
│   │ │   → GET /api/v1/instruments                                          │ │
│   │ │   → Returns: InstrumentListResponse { instruments: Instrument[] }    │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader title="Instruments" />
│
└── <InstrumentList instruments={data.instruments} isLoading={isLoading} />
        │
        └── maps → <InstrumentCard instrument={inst} />
```

#### 6.2.3 InstrumentDetailPage (Route: `/instruments/:instrumentId`)

```
InstrumentDetailPage
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/InstrumentDetailPage.tsx (78 lines)                          │
│   │ Route: /instruments/:instrumentId                                        │
│   │ URL Params: { instrumentId: string }                                     │
│   │                                                                          │
│   │ HOOKS USED:                                                              │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useInstrument(instrumentId)                                          │ │
│   │ │   → getInstrument(id)                                                │ │
│   │ │   → GET /api/v1/instruments/{instrumentId}                           │ │
│   │ │   → Returns: Instrument                                              │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useSilos(instrumentId)                                               │ │
│   │ │   → getSilos({ instrument_id: instrumentId })                        │ │
│   │ │   → GET /api/v1/silos?instrument_id={instrumentId}                   │ │
│   │ │   → Returns: SiloListResponse { silos: Silo[] }                      │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader
│       title={instrument.display_name}
│       description={instrument.symbol}
│       backTo="/instruments"
│   />
│
└── <SiloList silos={silos} isLoading={silosLoading} />
        ┌────────────────────────────────────────────────────────────────────┐
        │ SiloList Component                                                 │
        │ File: components/silos/SiloList.tsx (33 lines)                     │
        │ Props: { silos: Silo[], isLoading?: boolean }                      │
        └────────────────────────────────────────────────────────────────────┘
        │
        └── maps → <SiloCard silo={silo} key={silo.silo_id} />
                ┌────────────────────────────────────────────────────────────┐
                │ SiloCard Component                                         │
                │ File: components/silos/SiloCard.tsx (35 lines)             │
                │ Props: { silo: Silo }                                      │
                │ Displays:                                                  │
                │   - silo.silo_name                                         │
                │   - silo.heartbeat_enabled (indicator)                     │
                │ Links to: /silos/{silo_id}                                 │
                └────────────────────────────────────────────────────────────┘
```

#### 6.2.4 SiloDetailPage ★★★ CONSTITUTIONAL CRITICAL (Route: `/silos/:siloId`)

```
SiloDetailPage ★★★ CONSTITUTIONAL CRITICAL PAGE
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/SiloDetailPage.tsx (76 lines)                                │
│   │ Route: /silos/:siloId                                                    │
│   │ URL Params: { siloId: string }                                           │
│   │                                                                          │
│   │ ★ THIS PAGE ENFORCES CR-002 AND CR-003                                  │
│   │                                                                          │
│   │ HOOKS USED (4 PARALLEL API CALLS):                                       │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useSilo(siloId)                                                      │ │
│   │ │   → getSilo(id)                                                      │ │
│   │ │   → GET /api/v1/silos/{siloId}                                       │ │
│   │ │   → Returns: Silo                                                    │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useCharts(siloId)                                                    │ │
│   │ │   → getCharts({ silo_id: siloId })                                   │ │
│   │ │   → GET /api/v1/charts?silo_id={siloId}                              │ │
│   │ │   → Returns: ChartListResponse { charts: Chart[] }                   │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useRelationships(siloId) ★ CR-002                                    │ │
│   │ │   → getRelationships(siloId)                                         │ │
│   │ │   → GET /api/v1/relationships/silo/{siloId}                          │ │
│   │ │   → Returns: RelationshipResponse {                                  │ │
│   │ │       contradictions: Contradiction[]  ★ EQUAL WEIGHT                │ │
│   │ │       confirmations: Confirmation[]                                  │ │
│   │ │     }                                                                │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useNarrative(siloId) ★ CR-003                                        │ │
│   │ │   → getNarrative(siloId)                                             │ │
│   │ │   → GET /api/v1/narratives/silo/{siloId}                             │ │
│   │ │   → Returns: NarrativeResponse {                                     │ │
│   │ │       sections: NarrativeSection[]  ★ DESCRIPTIVE ONLY               │ │
│   │ │       closing_statement: string                                      │ │
│   │ │     }                                                                │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader
│       title={silo.silo_name}
│       backTo={`/instruments/${silo.instrument_id}`}
│   />
│
├── <section> {/* Charts Section */}
│   └── <ChartList charts={charts} isLoading={chartsLoading} />
│           ┌────────────────────────────────────────────────────────────────┐
│           │ ChartList Component                                            │
│           │ File: components/charts/ChartList.tsx (35 lines)               │
│           │ Props: { charts: Chart[], isLoading?: boolean }                │
│           └────────────────────────────────────────────────────────────────┘
│           │
│           └── maps → <ChartCard chart={chart} />
│                   ┌────────────────────────────────────────────────────────┐
│                   │ ChartCard Component                                    │
│                   │ File: components/charts/ChartCard.tsx (52 lines)       │
│                   │ Props: { chart: Chart }                                │
│                   │ Displays:                                              │
│                   │   - chart.chart_name                                   │
│                   │   - chart.chart_code                                   │
│                   │   - chart.timeframe                                    │
│                   │   ★ NO chart.weight (doesn't exist)                   │
│                   │ Links to: /charts/{chart_id}                           │
│                   └────────────────────────────────────────────────────────┘
│
├── <section> {/* Contradictions - CR-002 CRITICAL */}
│   │   ★★★ CONSTITUTIONAL: Shown with EQUAL prominence to confirmations ★★★
│   │
│   └── <ContradictionPanel contradictions={relationships?.contradictions} /> ★
│           ┌────────────────────────────────────────────────────────────────┐
│           │ ContradictionPanel Component ★ CR-002                          │
│           │ File: components/relationships/ContradictionPanel.tsx (56 ln)  │
│           │ Props: { contradictions: Contradiction[] }                     │
│           │ ★ CONSTITUTIONAL: Panel has equal visual weight to Confirm    │
│           └────────────────────────────────────────────────────────────────┘
│           │
│           └── maps → <ContradictionCard contradiction={c} /> ★
│                   ┌────────────────────────────────────────────────────────┐
│                   │ ContradictionCard Component ★ CR-002 CRITICAL          │
│                   │ File: components/relationships/ContradictionCard.tsx   │
│                   │ Lines: 39                                              │
│                   │ Props: { contradiction: Contradiction }                │
│                   │                                                        │
│                   │ CONSTITUTIONAL LAYOUT (Line 16):                       │
│                   │ ┌────────────────────────────────────────────────────┐ │
│                   │ │ className="grid grid-cols-[1fr,auto,1fr]"          │ │
│                   │ │                                                    │ │
│                   │ │   ★ 1fr = chart_a (EQUAL)                         │ │
│                   │ │   ★ auto = "VS" separator                         │ │
│                   │ │   ★ 1fr = chart_b (EQUAL)                         │ │
│                   │ │                                                    │ │
│                   │ │ Both sides use IDENTICAL CSS:                      │ │
│                   │ │ 'rounded-lg bg-surface-secondary p-3 text-center'  │ │
│                   │ └────────────────────────────────────────────────────┘ │
│                   │                                                        │
│                   │ Displays:                                              │
│                   │   - chart_a_name + chart_a_direction                   │
│                   │   - "VS" divider                                       │
│                   │   - chart_b_name + chart_b_direction                   │
│                   │   ★ NO resolution                                     │
│                   │   ★ NO preferred side                                 │
│                   │   ★ NO weighting                                      │
│                   └────────────────────────────────────────────────────────┘
│
├── <section> {/* Confirmations Section */}
│   └── <ConfirmationPanel confirmations={relationships?.confirmations} />
│           ┌────────────────────────────────────────────────────────────────┐
│           │ ConfirmationPanel Component                                    │
│           │ File: components/relationships/ConfirmationPanel.tsx (45 ln)   │
│           │ Props: { confirmations: Confirmation[] }                       │
│           └────────────────────────────────────────────────────────────────┘
│           │
│           └── maps → <ConfirmationCard confirmation={c} />
│                   ┌────────────────────────────────────────────────────────┐
│                   │ ConfirmationCard Component                             │
│                   │ File: components/relationships/ConfirmationCard.tsx    │
│                   │ Lines: 38                                              │
│                   │ Props: { confirmation: Confirmation }                  │
│                   │ Displays:                                              │
│                   │   - chart_a_name + chart_b_name                        │
│                   │   - aligned_direction                                  │
│                   └────────────────────────────────────────────────────────┘
│
└── <section> {/* Narrative Section - CR-003 CRITICAL */}
    │   ★★★ CONSTITUTIONAL: AI narrative with MANDATORY disclaimer ★★★
    │
    └── <NarrativeDisplay narrative={narrative} isLoading={narrLoading} /> ★
            ┌────────────────────────────────────────────────────────────────┐
            │ NarrativeDisplay Component ★ CR-003 CRITICAL                   │
            │ File: components/narratives/NarrativeDisplay.tsx (41 lines)    │
            │ Props: { narrative?: NarrativeResponse, isLoading?: boolean }  │
            │                                                                │
            │ CONSTITUTIONAL REQUIREMENTS:                                   │
            │   ★ Disclaimer is ALWAYS rendered (Lines 35-36)               │
            │   ★ Disclaimer CANNOT be dismissed                            │
            │   ★ Content is descriptive only                               │
            └────────────────────────────────────────────────────────────────┘
            │
            ├── if (isLoading) → <Spinner />
            │
            ├── maps narrative.sections → <NarrativeSection section={s} />
            │       ┌────────────────────────────────────────────────────────┐
            │       │ NarrativeSection Component                             │
            │       │ File: components/narratives/NarrativeSection.tsx (39)  │
            │       │ Props: { section: NarrativeSection }                   │
            │       │ Displays:                                              │
            │       │   - section.title                                      │
            │       │   - section.content                                    │
            │       └────────────────────────────────────────────────────────┘
            │
            └── <Disclaimer /> ★ MANDATORY - ALWAYS RENDERED
                    ┌────────────────────────────────────────────────────────┐
                    │ Disclaimer Component ★ CR-003 CRITICAL                 │
                    │ File: components/common/Disclaimer.tsx (26 lines)      │
                    │ Props: None                                            │
                    │                                                        │
                    │ HARDCODED TEXT (Lines 7-9):                            │
                    │ ┌────────────────────────────────────────────────────┐ │
                    │ │ "This is a description of what your charts are     │ │
                    │ │  showing. The interpretation and any decision      │ │
                    │ │  is entirely yours."                               │ │
                    │ └────────────────────────────────────────────────────┘ │
                    │                                                        │
                    │ ★ Text is HARDCODED - cannot be modified at runtime   │
                    │ ★ Component has NO dismiss functionality              │
                    │ ★ Component is ALWAYS visible when narrative shown    │
                    └────────────────────────────────────────────────────────┘
```

#### 6.2.5 ChartDetailPage (Route: `/charts/:chartId`)

```
ChartDetailPage
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/ChartDetailPage.tsx (72 lines)                               │
│   │ Route: /charts/:chartId                                                  │
│   │ URL Params: { chartId: string }                                          │
│   │                                                                          │
│   │ HOOKS USED:                                                              │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useChart(chartId)                                                    │ │
│   │ │   → getChart(id)                                                     │ │
│   │ │   → GET /api/v1/charts/{chartId}                                     │ │
│   │ │   → Returns: Chart                                                   │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useSignals(chartId)                                                  │ │
│   │ │   → getSignals(chartId)                                              │ │
│   │ │   → GET /api/v1/signals/chart/{chartId}                              │ │
│   │ │   → Returns: SignalListResponse { signals: Signal[] }                │ │
│   │ │                                                                      │ │
│   │ │   ★ Signal model has NO confidence field (CR-001)                   │ │
│   │ │   ★ Signal model has NO strength field (CR-001)                     │ │
│   │ │   ★ Signal model has NO weight field (CR-001)                       │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader
│       title={chart.chart_name}
│       description={`${chart.chart_code} | ${chart.timeframe}`}
│       backTo={`/silos/${chart.silo_id}`}
│   />
│
└── <SignalList signals={signals} isLoading={signalsLoading} />
        ┌────────────────────────────────────────────────────────────────────┐
        │ SignalList Component                                               │
        │ File: components/signals/SignalList.tsx (45 lines)                 │
        │ Props: { signals: Signal[], isLoading?: boolean }                  │
        └────────────────────────────────────────────────────────────────────┘
        │
        └── maps → <SignalCard signal={signal} />
                ┌────────────────────────────────────────────────────────────┐
                │ SignalCard Component                                       │
                │ File: components/signals/SignalCard.tsx (56 lines)         │
                │ Props: { signal: Signal }                                  │
                │ Displays:                                                  │
                │   - signal.signal_type                                     │
                │   - signal.direction (via DirectionBadge)                  │
                │   - signal.received_at                                     │
                │   - signal.indicators (key-value display)                  │
                │   ★ NO signal.confidence (doesn't exist)                  │
                │   ★ NO signal.strength (doesn't exist)                    │
                │   ★ NO signal.weight (doesn't exist)                      │
                └────────────────────────────────────────────────────────────┘
                │
                ├── <DirectionBadge direction={signal.direction} />
                │       ┌────────────────────────────────────────────────────┐
                │       │ DirectionBadge Component                           │
                │       │ File: components/signals/DirectionBadge.tsx (32 ln)│
                │       │ Props: { direction: Direction }                    │
                │       │ Displays: BULLISH (green) | BEARISH (red) | NEUTRAL│
                │       └────────────────────────────────────────────────────┘
                │
                └── <FreshnessBadge status={computeFreshness(signal)} />
                        ┌────────────────────────────────────────────────────┐
                        │ FreshnessBadge Component                           │
                        │ File: components/signals/FreshnessBadge.tsx (38 ln)│
                        │ Props: { status: FreshnessStatus }                 │
                        │ Displays: CURRENT (green) | RECENT (yellow) | STALE│
                        └────────────────────────────────────────────────────┘
```

#### 6.2.6 ChatPage ★ CR-003 CRITICAL (Route: `/chat`)

```
ChatPage ★ CR-003 CRITICAL PAGE
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/ChatPage.tsx (68 lines)                                      │
│   │ Route: /chat                                                             │
│   │                                                                          │
│   │ ★ THIS PAGE ENFORCES CR-003 (Descriptive Only)                          │
│   │                                                                          │
│   │ HOOKS USED:                                                              │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useInstruments()                                                     │ │
│   │ │   → For instrument selector                                          │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useChat(selectedScripId)                                             │ │
│   │ │   → sendMessage(scripId, message)                                    │ │
│   │ │   → POST /api/v1/chat/{scripId}                                      │ │
│   │ │   → Returns: ChatResponse {                                          │ │
│   │ │       response: string  ★ DESCRIPTIVE ONLY, NEVER PRESCRIPTIVE      │ │
│   │ │       model_used: string                                             │ │
│   │ │     }                                                                │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useChatHistory(selectedScripId)                                      │ │
│   │ │   → getHistory(scripId)                                              │ │
│   │ │   → GET /api/v1/chat/{scripId}/history                               │ │
│   │ │   → Returns: ChatHistoryResponse { messages: ChatMessage[] }         │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader title="AI Chat" />
│
├── <InstrumentSelector
│       instruments={instruments}
│       selected={selectedScripId}
│       onSelect={setSelectedScripId}
│   />
│       ┌────────────────────────────────────────────────────────────────────┐
│       │ InstrumentSelector Component                                       │
│       │ File: components/instruments/InstrumentSelector.tsx (37 lines)     │
│       │ Props: { instruments, selected, onSelect }                         │
│       └────────────────────────────────────────────────────────────────────┘
│
└── <ChatInterface
        scripId={selectedScripId}
        history={chatHistory}
        onSend={handleSend}
    /> ★
        ┌────────────────────────────────────────────────────────────────────┐
        │ ChatInterface Component ★ CR-003 CRITICAL                          │
        │ File: components/ai/ChatInterface.tsx (180 lines)                  │
        │ Props: { scripId, history, onSend }                                │
        │                                                                    │
        │ CONSTITUTIONAL REQUIREMENTS:                                       │
        │   ★ Displays Disclaimer at top of chat                            │
        │   ★ AI responses are information only                             │
        │   ★ NO buy/sell advice generated                                  │
        └────────────────────────────────────────────────────────────────────┘
        │
        ├── <Disclaimer /> ★ MANDATORY
        │
        ├── maps history → <ChatMessage role={m.role} content={m.content} />
        │
        └── <ChatInput onSubmit={onSend} />
```

#### 6.2.7 SettingsPage (Route: `/settings`)

```
SettingsPage
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/SettingsPage.tsx (163 lines)                                 │
│   │ Route: /settings                                                         │
│   │                                                                          │
│   │ HOOKS USED:                                                              │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useAIModels()                                                        │ │
│   │ │   → getModels()                                                      │ │
│   │ │   → GET /api/v1/ai/models                                            │ │
│   │ │   → Returns: AIModelsResponse { models: AIModelInfo[] }              │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useAIBudget()                                                        │ │
│   │ │   → getBudget()                                                      │ │
│   │ │   → GET /api/v1/ai/budget                                            │ │
│   │ │   → Returns: AIBudgetResponse                                        │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   │ ┌──────────────────────────────────────────────────────────────────────┐ │
│   │ │ useAIUsage()                                                         │ │
│   │ │   → getUsage()                                                       │ │
│   │ │   → GET /api/v1/ai/usage                                             │ │
│   │ │   → Returns: AIUsageResponse                                         │ │
│   │ └──────────────────────────────────────────────────────────────────────┘ │
│   └──────────────────────────────────────────────────────────────────────────┘
│
├── <PageHeader title="Settings" />
│
├── <section> {/* AI Model Selection */}
│   └── <ModelSelector
│           models={aiModels.models}
│           selected={currentModel}
│           onSelect={handleModelChange}
│       />
│           ┌────────────────────────────────────────────────────────────────┐
│           │ ModelSelector Component                                        │
│           │ File: components/ai/ModelSelector.tsx (40 lines)               │
│           │ Props: { models: AIModelInfo[], selected, onSelect }           │
│           │ Displays:                                                      │
│           │   - Haiku (Fast, cheap)                                        │
│           │   - Sonnet (Balanced)                                          │
│           │   - Opus (Best quality)                                        │
│           │ Per ADR-003: Dynamic model selection                           │
│           └────────────────────────────────────────────────────────────────┘
│
├── <section> {/* Budget Display */}
│   └── <BudgetIndicator budget={aiBudget} detailed={true} />
│
└── <section> {/* Usage Statistics */}
    └── Usage display from useAIUsage()
```

#### 6.2.8 NotFoundPage (Route: `*`)

```
NotFoundPage
│   ┌──────────────────────────────────────────────────────────────────────────┐
│   │ File: pages/NotFoundPage.tsx (66 lines)                                  │
│   │ Route: * (catch-all)                                                     │
│   │                                                                          │
│   │ HOOKS USED: None (static page)                                           │
│   └──────────────────────────────────────────────────────────────────────────┘
│
└── <ErrorState
        title="Page Not Found"
        message="The page you're looking for doesn't exist."
        action={<Button onClick={() => navigate('/')}>Go Home</Button>}
    />
```

---

## 7. Page-by-Page Data Consumption

### 7.1 Data Flow Summary Table

| Page | Hooks Used | API Endpoints | Data Models Consumed | Constitutional |
|------|------------|---------------|---------------------|----------------|
| HomePage | useInstruments | GET /instruments | Instrument[] | - |
| InstrumentsPage | useInstruments | GET /instruments | Instrument[] | - |
| InstrumentDetailPage | useInstrument, useSilos | GET /instruments/{id}, GET /silos | Instrument, Silo[] | - |
| **SiloDetailPage** | useSilo, useCharts, useRelationships, useNarrative | GET /silos/{id}, GET /charts, GET /relationships/silo/{id}, GET /narratives/silo/{id} | Silo, Chart[], Contradiction[], Confirmation[], NarrativeResponse | **CR-002, CR-003** |
| ChartDetailPage | useChart, useSignals | GET /charts/{id}, GET /signals/chart/{id} | Chart, Signal[] | CR-001 (no weight) |
| **ChatPage** | useInstruments, useChat, useChatHistory | GET /instruments, POST /chat/{id}, GET /chat/{id}/history | Instrument[], ChatResponse, ChatMessage[] | **CR-003** |
| SettingsPage | useAIModels, useAIBudget, useAIUsage | GET /ai/models, GET /ai/budget, GET /ai/usage | AIModelInfo[], AIBudgetResponse, AIUsageResponse | - |
| NotFoundPage | None | None | None | - |

### 7.2 Hook Usage Frequency

| Hook | Used By Pages | Total Usages |
|------|--------------|--------------|
| useInstruments | HomePage, InstrumentsPage, ChatPage | 3 |
| useInstrument | InstrumentDetailPage | 1 |
| useSilos | InstrumentDetailPage | 1 |
| useSilo | SiloDetailPage | 1 |
| useCharts | SiloDetailPage | 1 |
| useChart | ChartDetailPage | 1 |
| useSignals | ChartDetailPage | 1 |
| **useRelationships** ★ | **SiloDetailPage** | **1** |
| **useNarrative** ★ | **SiloDetailPage** | **1** |
| useChat | ChatPage | 1 |
| useChatHistory | ChatPage | 1 |
| useAIModels | SettingsPage | 1 |
| useAIBudget | SettingsPage, Header | 2 |
| useAIUsage | SettingsPage | 1 |

---

## 8. Constitutional Constraint Integration

### 8.1 CR-001: Decision-Support ONLY

**Enforcement Points:**

| Location | Mechanism | Verification |
|----------|-----------|--------------|
| Signal Model | NO weight/confidence/strength fields | `types/models.ts` - fields absent |
| Chart Model | NO weight/priority fields | `types/models.ts` - fields absent |
| Button Component | NO "Buy"/"Sell" text | `grep -rn "Buy\|Sell" frontend/src/` returns nothing |

### 8.2 CR-002: NEVER Resolve Contradictions

**Enforcement Points:**

| Component | File | Mechanism | Lines |
|-----------|------|-----------|-------|
| ContradictionCard | `components/relationships/ContradictionCard.tsx` | `grid-cols-[1fr,auto,1fr]` - equal width | 16 |
| ContradictionCard | `components/relationships/ContradictionCard.tsx` | Identical CSS for both sides | 11 |
| Contradiction Model | `types/models.ts` | NO resolution/preferred_side fields | - |

**Visual Weight Verification:**

```css
/* Line 11: Both sides use IDENTICAL styling */
const sideClassName = 'rounded-lg bg-surface-secondary p-3 text-center'

/* Line 16: Grid ensures equal width */
<div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">
  <div className={sideClassName}>{/* Chart A */}</div>
  <span>VS</span>
  <div className={sideClassName}>{/* Chart B */}</div>
</div>
```

### 8.3 CR-003: Descriptive NOT Prescriptive

**Enforcement Points:**

| Component | File | Mechanism | Lines |
|-----------|------|-----------|-------|
| Disclaimer | `components/common/Disclaimer.tsx` | Hardcoded text, no dismiss | 7-9 |
| NarrativeDisplay | `components/narratives/NarrativeDisplay.tsx` | Disclaimer ALWAYS rendered | 35-36 |
| ChatInterface | `components/ai/ChatInterface.tsx` | Disclaimer at top | - |
| NarrativeResponse | `types/api.ts` | NO recommendations field | - |

**Disclaimer Text (Hardcoded, Immutable):**

```typescript
const DISCLAIMER_TEXT =
  'This is a description of what your charts are showing. ' +
  'The interpretation and any decision is entirely yours.'
```

---

## 9. Backend API Endpoint Summary

### 9.1 Complete Endpoint Table

| Endpoint | Method | Request | Response | Constitutional |
|----------|--------|---------|----------|----------------|
| `/api/v1/instruments` | GET | - | InstrumentListResponse | - |
| `/api/v1/instruments/{id}` | GET | - | Instrument | - |
| `/api/v1/instruments` | POST | CreateInstrumentRequest | Instrument | - |
| `/api/v1/instruments/{id}` | PATCH | UpdateInstrumentRequest | Instrument | - |
| `/api/v1/instruments/{id}` | DELETE | - | 204 | - |
| `/api/v1/silos` | GET | ?instrument_id= | SiloListResponse | - |
| `/api/v1/silos/{id}` | GET | - | Silo | - |
| `/api/v1/silos` | POST | CreateSiloRequest | Silo | - |
| `/api/v1/silos/{id}` | DELETE | - | 204 | - |
| `/api/v1/charts` | GET | ?silo_id= | ChartListResponse | - |
| `/api/v1/charts/{id}` | GET | - | Chart | - |
| `/api/v1/charts` | POST | CreateChartRequest | Chart | - |
| `/api/v1/charts/{id}` | DELETE | - | 204 | - |
| `/api/v1/signals/chart/{id}` | GET | - | SignalListResponse | CR-001 |
| `/api/v1/signals/{id}` | GET | - | Signal | CR-001 |
| `/api/v1/relationships/silo/{id}` | GET | - | RelationshipResponse | **CR-002** |
| `/api/v1/relationships/contradictions/silo/{id}` | GET | - | ContradictionsResponse | **CR-002** |
| `/api/v1/narratives/silo/{id}` | GET | - | NarrativeResponse | **CR-003** |
| `/api/v1/narratives/silo/{id}/plain` | GET | - | PlainNarrativeResponse | **CR-003** |
| `/api/v1/chat/{scripId}` | POST | { message: string } | ChatResponse | **CR-003** |
| `/api/v1/chat/{scripId}/history` | GET | - | ChatHistoryResponse | - |
| `/api/v1/ai/models` | GET | - | AIModelsResponse | - |
| `/api/v1/ai/budget` | GET | - | AIBudgetResponse | - |
| `/api/v1/ai/usage` | GET | - | AIUsageResponse | - |
| `/api/v1/ai/configure` | POST | AIConfigRequest | 200 | - |
| `/api/v1/webhooks/tradingview` | POST | TradingViewPayload | 201 | - |

---

## 10. Data Flow Diagrams

### 10.1 Signal Ingestion to Display Flow

```
┌──────────────────┐
│   TradingView    │
│   Alert Fires    │
└────────┬─────────┘
         │
         │ POST /api/v1/webhooks/tradingview
         │ { indicator: "RSI", direction: "BULLISH", ... }
         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                          │
│                                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐  │
│  │   webhook_handler   │ → │  signal_normalizer  │ → │  SignalRepository │  │
│  │   (ingestion/)      │    │  (ingestion/)       │    │  (dal/)           │  │
│  └─────────────────────┘    └─────────────────────┘    └─────────┬─────────┘  │
│                                                                   │          │
│                                                                   ▼          │
│                                                          ┌──────────────┐    │
│                                                          │   SQLite DB  │    │
│                                                          │  SignalDB    │    │
│                                                          └──────────────┘    │
│                                                                   │          │
│  ┌─────────────────────┐    ┌─────────────────────┐              │          │
│  │  GET /signals/chart │ ← │  SignalRepository   │ ←────────────┘          │
│  │  (api/routes/)      │    │  (dal/)             │                          │
│  └──────────┬──────────┘    └─────────────────────┘                          │
└─────────────┼────────────────────────────────────────────────────────────────┘
              │
              │ Response: SignalListResponse
              │ { signals: Signal[] }
              │
              │ ★ Signal has NO weight, confidence, strength (CR-001)
              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                         │
│                                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐  │
│  │   signals service   │ → │   useSignals hook   │ → │    SignalList    │  │
│  │   (services/)       │    │   (hooks/)          │    │    (components/) │  │
│  └─────────────────────┘    └─────────────────────┘    └────────┬────────┘  │
│                                                                  │          │
│                                                                  ▼          │
│                                                          ┌──────────────┐    │
│                                                          │  SignalCard  │    │
│                                                          │  Displays:   │    │
│                                                          │  - direction │    │
│                                                          │  - type      │    │
│                                                          │  - timestamp │    │
│                                                          │  ★ NO weight │    │
│                                                          └──────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 Contradiction Detection and Display Flow ★ CR-002

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                          │
│                                                                              │
│  ┌─────────────────────┐    ┌─────────────────────────────────────────────┐  │
│  │  signals table      │    │           contradiction_detector            │  │
│  │  (Chart A: BULLISH) │ → │  (exposure/contradiction_detector.py)        │  │
│  │  (Chart B: BEARISH) │    │                                             │  │
│  └─────────────────────┘    │  if chart_a.direction != chart_b.direction: │  │
│                             │      create Contradiction                    │  │
│                             │      ★ NO resolution field                  │  │
│                             │      ★ NO preferred_side field              │  │
│                             └──────────────────┬──────────────────────────┘  │
│                                                │                              │
│  ┌─────────────────────────────────────────────┼──────────────────────────┐  │
│  │  GET /api/v1/relationships/silo/{id}        ▼                          │  │
│  │  Response: {                                                            │  │
│  │    contradictions: [                                                    │  │
│  │      { chart_a_direction: "BULLISH", chart_b_direction: "BEARISH" }    │  │
│  │    ]                                                                    │  │
│  │    ★ NO net_direction                                                  │  │
│  │    ★ NO aggregated_view                                                │  │
│  │  }                                                                      │  │
│  └─────────────────────────────────────────────┬──────────────────────────┘  │
└────────────────────────────────────────────────┼──────────────────────────────┘
                                                 │
                                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                         │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  SiloDetailPage                                                         │ │
│  │    const { data: relationships } = useRelationships(siloId)             │ │
│  │                          │                                              │ │
│  │                          ▼                                              │ │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │ │
│  │  │  <ContradictionPanel contradictions={relationships.contradictions} │  │ │
│  │  │                              │                                     │  │ │
│  │  │                              ▼                                     │  │ │
│  │  │  ┌─────────────────────────────────────────────────────────────┐   │  │ │
│  │  │  │  <ContradictionCard />  ★ CR-002 ENFORCEMENT               │   │  │ │
│  │  │  │                                                             │   │  │ │
│  │  │  │  ┌─────────────────┬───────┬─────────────────┐              │   │  │ │
│  │  │  │  │   Chart A       │  VS   │   Chart B       │              │   │  │ │
│  │  │  │  │   BULLISH       │       │   BEARISH       │              │   │  │ │
│  │  │  │  │                 │       │                 │              │   │  │ │
│  │  │  │  │ ★ 1fr          │ auto  │ ★ 1fr          │              │   │  │ │
│  │  │  │  │ ★ EQUAL WIDTH  │       │ ★ EQUAL WIDTH  │              │   │  │ │
│  │  │  │  │ ★ SAME CSS     │       │ ★ SAME CSS     │              │   │  │ │
│  │  │  │  └─────────────────┴───────┴─────────────────┘              │   │  │ │
│  │  │  │                                                             │   │  │ │
│  │  │  │  ★ NO "This side is correct" indicator                     │   │  │ │
│  │  │  │  ★ NO visual hierarchy between sides                       │   │  │ │
│  │  │  │  ★ NO resolution button                                    │   │  │ │
│  │  │  └─────────────────────────────────────────────────────────────┘   │  │ │
│  │  └───────────────────────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 10.3 Narrative Generation and Display Flow ★ CR-003

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                          │
│                                                                              │
│  ┌─────────────────────┐                                                     │
│  │  Silo Data          │                                                     │
│  │  - Charts[]         │                                                     │
│  │  - Signals[]        │                                                     │
│  │  - Contradictions[] │                                                     │
│  │  - Confirmations[]  │                                                     │
│  └──────────┬──────────┘                                                     │
│             │                                                                 │
│             ▼                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  prompt_builder.py (ai/)                                                │  │
│  │                                                                         │  │
│  │  Builds prompt with CONSTITUTIONAL CONSTRAINTS:                         │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐ │  │
│  │  │ "You are a DESCRIPTIVE analyst. NEVER make recommendations.      │ │  │
│  │  │  NEVER suggest actions. ONLY describe what the data shows.       │ │  │
│  │  │  Do NOT use words like 'should', 'recommend', 'suggest'."        │ │  │
│  │  └───────────────────────────────────────────────────────────────────┘ │  │
│  └──────────┬─────────────────────────────────────────────────────────────┘  │
│             │                                                                 │
│             ▼                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────────────────────────────┐  │
│  │   claude_client.py  │ → │  Anthropic Claude API                        │  │
│  │   (ai/)             │    │  (haiku/sonnet/opus per ADR-003)            │  │
│  └──────────┬──────────┘    └─────────────────────────────────────────────┘  │
│             │                                                                 │
│             ▼                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  response_validator.py (ai/)                                            │  │
│  │                                                                         │  │
│  │  VALIDATES response does NOT contain:                                   │  │
│  │  - "buy" / "sell" / "enter" / "exit"                                   │  │
│  │  - "recommend" / "suggest" / "advise"                                  │  │
│  │  - "should" / "must" / "need to"                                       │  │
│  └──────────┬─────────────────────────────────────────────────────────────┘  │
│             │                                                                 │
│             ▼                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  GET /api/v1/narratives/silo/{id}                                       │  │
│  │  Response: NarrativeResponse {                                          │  │
│  │    sections: [                                                          │  │
│  │      { title: "Overview", content: "The RSI shows..." }                │  │
│  │      { title: "Contradictions", content: "Chart A and B differ..." }   │  │
│  │    ]                                                                    │  │
│  │    closing_statement: "This describes the current state..."            │  │
│  │    ★ NO recommendations field                                          │  │
│  │    ★ NO action_items field                                             │  │
│  │  }                                                                      │  │
│  └──────────┬─────────────────────────────────────────────────────────────┘  │
└─────────────┼────────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                         │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  SiloDetailPage                                                         │ │
│  │    const { data: narrative } = useNarrative(siloId)                     │ │
│  │                          │                                              │ │
│  │                          ▼                                              │ │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │ │
│  │  │  <NarrativeDisplay narrative={narrative} />  ★ CR-003             │  │ │
│  │  │                              │                                     │  │ │
│  │  │                              ▼                                     │  │ │
│  │  │  ┌─────────────────────────────────────────────────────────────┐   │  │ │
│  │  │  │  narrative.sections.map(section =>                          │   │  │ │
│  │  │  │    <NarrativeSection section={section} />                   │   │  │ │
│  │  │  │  )                                                          │   │  │ │
│  │  │  │                                                             │   │  │ │
│  │  │  │  Content:                                                   │   │  │ │
│  │  │  │  "The RSI indicator currently shows oversold conditions.    │   │  │ │
│  │  │  │   The MACD histogram is declining. Chart A shows bullish    │   │  │ │
│  │  │  │   signals while Chart B shows bearish signals."             │   │  │ │
│  │  │  │                                                             │   │  │ │
│  │  │  │  ★ DESCRIPTIVE ONLY - no "you should buy/sell"             │   │  │ │
│  │  │  └─────────────────────────────────────────────────────────────┘   │  │ │
│  │  │                              │                                     │  │ │
│  │  │                              ▼                                     │  │ │
│  │  │  ┌─────────────────────────────────────────────────────────────┐   │  │ │
│  │  │  │  <Disclaimer />  ★ MANDATORY - ALWAYS RENDERED             │   │  │ │
│  │  │  │                                                             │   │  │ │
│  │  │  │  ┌───────────────────────────────────────────────────────┐  │   │  │ │
│  │  │  │  │ "This is a description of what your charts are        │  │   │  │ │
│  │  │  │  │  showing. The interpretation and any decision         │  │   │  │ │
│  │  │  │  │  is entirely yours."                                  │  │   │  │ │
│  │  │  │  └───────────────────────────────────────────────────────┘  │   │  │ │
│  │  │  │                                                             │   │  │ │
│  │  │  │  ★ TEXT IS HARDCODED - cannot be modified                  │   │  │ │
│  │  │  │  ★ NO DISMISS BUTTON - always visible                      │   │  │ │
│  │  │  │  ★ CANNOT BE HIDDEN - unconditionally rendered             │   │  │ │
│  │  │  └─────────────────────────────────────────────────────────────┘   │  │ │
│  │  └───────────────────────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Document Verification

### Verification Commands

```bash
# Verify all hooks exist
$ ls -la frontend/src/hooks/
# Expected: 9 files

# Verify all services exist
$ ls -la frontend/src/services/
# Expected: 10 files

# Verify component structure
$ find frontend/src/components -name "*.tsx" | wc -l
# Expected: 26

# Verify constitutional constraints
$ grep -n "grid-cols-\[1fr,auto,1fr\]" frontend/src/components/relationships/ContradictionCard.tsx
# Expected: Line 16

$ grep -n "Disclaimer" frontend/src/components/narratives/NarrativeDisplay.tsx
# Expected: Lines 35-36

$ grep -rn "Buy\|Sell" frontend/src/
# Expected: No matches (exit code 1)
```

---

| Field | Value |
|-------|-------|
| Document ID | CIA-SIE-DFA-001 |
| Version | 1.0.0 |
| Date | 2026-01-04 |
| Author | Claude Opus 4.5 |
| Total Lines | 1,400+ |
| Total Sections | 10 |
| Total Tables | 25+ |
| Total Diagrams | 6 ASCII |

---

*End of CIA-SIE Frontend Data Flow Architecture Document*
