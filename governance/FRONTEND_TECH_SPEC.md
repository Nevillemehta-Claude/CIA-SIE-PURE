# CIA-SIE Frontend Technology Specification

**Version:** 1.0  
**Date:** 2026-01-03  
**Classification:** Complete Implementation Specification  
**Purpose:** Enable developers unfamiliar with CIA-SIE to build the complete frontend from scratch

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Constitutional Framework](#2-constitutional-framework)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [TypeScript Types](#5-typescript-types)
6. [Component Architecture](#6-component-architecture)
7. [State Management](#7-state-management)
8. [Real-Time Data Flow](#8-real-time-data-flow)
9. [API Integration](#9-api-integration)
10. [UI State Machine](#10-ui-state-machine)
11. [Edge Case Handling](#11-edge-case-handling)
12. [Constitutional Enforcement at Presentation Layer](#12-constitutional-enforcement-at-presentation-layer)
13. [Performance & Optimization](#13-performance--optimization)
14. [Accessibility & Responsiveness](#14-accessibility--responsiveness)
15. [Testing Strategy](#15-testing-strategy)
16. [Design System](#16-design-system)

---

## 1. Executive Summary

CIA-SIE (Chart Intelligence Aggregator - Signal Intelligence Engine) is a **decision-support platform** for traders. The frontend displays trading signals from multiple TradingView charts, exposes contradictions and confirmations between signals, and provides AI-generated narrative descriptions.

### 1.1 Critical Understanding

**This is NOT a trading platform.** The system:
- **DISPLAYS** signals - never generates trading commands
- **EXPOSES** contradictions - never resolves them
- **DESCRIBES** data - never recommends actions

Every UI component, every data display, and every interaction must enforce these principles.

### 1.2 Core Functionality

| Feature | Purpose | Constitutional Constraint |
|---------|---------|---------------------------|
| Signal Dashboard | Display current chart signals | Read-only, no weighting |
| Contradiction Panel | Show conflicting signals side-by-side | Equal prominence, no resolution |
| Confirmation Panel | Show aligned signals | No confidence scoring |
| AI Narratives | Describe what data shows | Mandatory disclaimer |
| Freshness Indicators | Show data age | Descriptive only |

---

## 2. Constitutional Framework

### 2.1 The Three Inviolable Rules

These rules are **absolute constraints** that must be enforced in every frontend component, every API call, and every data display.

#### CR-001: Decision-Support ONLY

**Rule Statement:**
The system must NEVER make investment decisions or output actionable trading commands.

**Frontend Enforcement:**
- No "Buy Now" / "Sell Now" buttons
- No trading action forms
- No order placement UI
- No position management
- Mandatory disclaimer on all AI-generated content:
  > "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."

**Prohibited UI Elements:**
```
❌ <button>Buy</button>
❌ <button>Sell</button>
❌ <button>Execute Trade</button>
❌ <button>Enter Position</button>
❌ <form>Order Entry</form>
❌ Any trading action controls
```

**Required UI Elements:**
```
✅ Mandatory disclaimer on every AI response
✅ Clear "informational only" labeling
✅ No imperative language in UI text
```

#### CR-002: Never Resolve Contradictions

**Rule Statement:**
The system must NEVER pick sides, aggregate, weight, hide, or average conflicting signals.

**Frontend Enforcement:**
- No "overall direction" indicators
- No "net signal" displays
- No pie charts showing "bullish %" 
- No progress bars implying consensus
- Contradictions displayed with EQUAL visual prominence
- No visual hierarchy suggesting one signal is "more correct"

**Prohibited UI Patterns:**
```
❌ Overall Direction: BULLISH (confidence: 72%)
❌ Net Signal: +3 (6 bullish, 3 bearish)
❌ [=========>    ] 72% Bullish
❌ Color-coding that implies one side is "winning"
❌ Larger/more prominent display for any signal
❌ Aggregated scores or summaries
```

**Required UI Patterns:**
```
✅ Side-by-side contradiction display with equal sizing
✅ Equal visual weight for all signals
✅ "Chart A shows BULLISH" AND "Chart B shows BEARISH"
✅ No visual preference for either side
```

#### CR-003: Descriptive NOT Prescriptive

**Rule Statement:**
The system must NEVER use prescriptive language for investment actions.

**Frontend Enforcement:**
- No "should", "must", "recommend", "suggest", "advise" in UI text
- No "consider buying/selling" prompts
- AI responses must be validated before display
- All text is purely factual/descriptive

**Prohibited Language:**
```
❌ "You should consider..."
❌ "We recommend..."
❌ "Based on signals, you should buy..."
❌ "This suggests you should..."
❌ "Consider entering a position..."
```

**Required Language:**
```
✅ "Chart A shows bullish momentum"
✅ "The signal changed from BEARISH to BULLISH"
✅ "There is a contradiction between Chart A and Chart B"
✅ "The data was last updated 2 minutes ago"
```

### 2.2 Prohibited Data Patterns

The frontend must NEVER display or compute these values:

| Prohibited Field | Why Prohibited | Alternative Display |
|------------------|----------------|---------------------|
| `weight` | Enables aggregation | Display all charts equally |
| `score` | Implies judgment | Display raw direction only |
| `confidence` | Implies reliability ranking | Display signal type only |
| `recommendation` | Prescriptive action | Display description only |
| `priority` | Implies hierarchy | Display in creation order |
| `rank` | Implies superiority | Display alphabetically |
| `overall_direction` | Aggregates signals | Show each signal separately |
| `net_signal` | Resolves contradictions | Show contradictions explicitly |

### 2.3 Constitutional Validation Checklist

Before implementing any component, verify:

- [ ] Does this component display data without recommending action?
- [ ] Does this component show contradictions without resolving them?
- [ ] Does this component use descriptive language only?
- [ ] Does this component give equal prominence to all signals?
- [ ] Does this component include required disclaimers (if AI-generated)?
- [ ] Does this component avoid all prohibited fields?
- [ ] Does this component avoid all prohibited language patterns?

---

## 3. Technology Stack

### 3.1 Core Dependencies (LOCKED)

| Package | Version | Purpose |
|---------|---------|---------|
| React | 18.2.x | UI framework |
| TypeScript | 5.3.x | Type safety |
| Vite | 5.0.x | Build tool |
| Tailwind CSS | 3.4.x | Styling |
| React Query | 5.17.x | Server state management |
| React Router | 6.21.x | Client-side routing |
| Axios | 1.6.x | HTTP client |
| Lucide React | 0.303.x | Icon library |
| Vitest | 1.1.x | Testing framework |

### 3.2 package.json

```json
{
  "name": "cia-sie-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.303.0",
    "clsx": "^2.1.0",
    "date-fns": "^3.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "vitest": "^1.1.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "jsdom": "^23.0.0",
    "eslint": "^8.55.0",
    "@typescript-eslint/parser": "^6.15.0",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0"
  }
}
```

### 3.3 vite.config.ts

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@constants': path.resolve(__dirname, './src/constants'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

### 3.4 tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Signal direction colors (constitutional: equal visual weight)
        signal: {
          bullish: '#22c55e',    // green-500
          bearish: '#ef4444',    // red-500
          neutral: '#6b7280',    // gray-500
        },
        // Freshness status colors
        freshness: {
          current: '#22c55e',    // green-500
          recent: '#eab308',     // yellow-500
          stale: '#f97316',      // orange-500
          unavailable: '#6b7280', // gray-500
        },
        // UI theme colors
        surface: {
          primary: '#0f172a',    // slate-900
          secondary: '#1e293b',  // slate-800
          tertiary: '#334155',   // slate-700
        },
        accent: {
          primary: '#3b82f6',    // blue-500
          secondary: '#8b5cf6',  // violet-500
        },
      },
      fontFamily: {
        sans: ['JetBrains Mono', 'SF Mono', 'monospace'],
        display: ['Space Grotesk', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

### 3.5 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@services/*": ["src/services/*"],
      "@types/*": ["src/types/*"],
      "@utils/*": ["src/utils/*"],
      "@constants/*": ["src/constants/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

## 4. Project Structure

```
src/
├── main.tsx                          # Application entry point
├── App.tsx                           # Root component with routing
├── index.css                         # Global styles and Tailwind imports
│
├── types/                            # TypeScript type definitions
│   ├── index.ts                      # Re-exports all types
│   ├── models.ts                     # Domain model types
│   ├── api.ts                        # API request/response types
│   └── enums.ts                      # Enum definitions
│
├── constants/                        # Application constants
│   ├── index.ts                      # Re-exports
│   ├── constitutional.ts             # Constitutional rules & patterns
│   ├── api.ts                        # API endpoints
│   └── ui.ts                         # UI constants
│
├── services/                         # API layer
│   ├── api.ts                        # Axios instance configuration
│   ├── instruments.ts                # Instrument API calls
│   ├── silos.ts                      # Silo API calls
│   ├── charts.ts                     # Chart API calls
│   ├── signals.ts                    # Signal API calls
│   ├── relationships.ts              # Relationships API calls
│   ├── narratives.ts                 # Narratives API calls
│   ├── chat.ts                       # AI chat API calls
│   ├── ai.ts                         # AI configuration API calls
│   ├── baskets.ts                    # Basket API calls
│   └── platforms.ts                  # Platform API calls
│
├── hooks/                            # Custom React hooks
│   ├── useInstruments.ts             # Instrument data hooks
│   ├── useSilos.ts                   # Silo data hooks
│   ├── useCharts.ts                  # Chart data hooks
│   ├── useSignals.ts                 # Signal data hooks
│   ├── useRelationships.ts           # Relationship data hooks
│   ├── useNarratives.ts              # Narrative generation hooks
│   ├── useChat.ts                    # AI chat hooks
│   ├── useConstitutionalValidation.ts # Content validation hook
│   └── useFreshness.ts               # Freshness calculation hook
│
├── utils/                            # Utility functions
│   ├── constitutional.ts             # Constitutional validation utilities
│   ├── formatting.ts                 # Data formatting utilities
│   ├── freshness.ts                  # Freshness calculation
│   └── date.ts                       # Date utilities
│
├── components/                       # React components
│   ├── layout/                       # Layout components
│   │   ├── AppShell.tsx              # Main application shell
│   │   ├── Header.tsx                # Application header
│   │   ├── Sidebar.tsx               # Navigation sidebar
│   │   └── Footer.tsx                # Application footer
│   │
│   ├── common/                       # Shared/atomic components
│   │   ├── Button.tsx                # Button component
│   │   ├── Card.tsx                  # Card container
│   │   ├── Badge.tsx                 # Status badge
│   │   ├── Spinner.tsx               # Loading spinner
│   │   ├── ErrorBoundary.tsx         # Error boundary
│   │   ├── EmptyState.tsx            # Empty state display
│   │   ├── Skeleton.tsx              # Loading skeleton
│   │   └── Disclaimer.tsx            # Mandatory disclaimer component
│   │
│   ├── instruments/                  # Instrument feature
│   │   ├── InstrumentList.tsx        # Instrument list view
│   │   ├── InstrumentCard.tsx        # Single instrument card
│   │   ├── InstrumentSelector.tsx    # Instrument dropdown
│   │   └── InstrumentDetail.tsx      # Instrument detail view
│   │
│   ├── silos/                        # Silo feature
│   │   ├── SiloList.tsx              # Silo list view
│   │   ├── SiloCard.tsx              # Single silo card
│   │   └── SiloDetail.tsx            # Silo detail view
│   │
│   ├── charts/                       # Chart feature
│   │   ├── ChartList.tsx             # Chart list view
│   │   ├── ChartCard.tsx             # Single chart card
│   │   ├── ChartGrid.tsx             # Chart grid layout
│   │   └── ChartSignalDisplay.tsx    # Chart with signal
│   │
│   ├── signals/                      # Signal feature
│   │   ├── SignalDisplay.tsx         # Signal direction display
│   │   ├── SignalHistory.tsx         # Signal history list
│   │   ├── DirectionBadge.tsx        # Direction indicator
│   │   └── FreshnessBadge.tsx        # Freshness status
│   │
│   ├── relationships/                # Relationships feature
│   │   ├── RelationshipSummary.tsx   # Full relationship view
│   │   ├── ContradictionPanel.tsx    # Contradiction display
│   │   ├── ContradictionCard.tsx     # Single contradiction
│   │   ├── ConfirmationPanel.tsx     # Confirmation display
│   │   └── ConfirmationCard.tsx      # Single confirmation
│   │
│   ├── narratives/                   # AI narrative feature
│   │   ├── NarrativeDisplay.tsx      # Full narrative view
│   │   ├── NarrativeSection.tsx      # Single section
│   │   └── NarrativeLoading.tsx      # Loading state
│   │
│   ├── chat/                         # AI chat feature
│   │   ├── ChatInterface.tsx         # Chat container
│   │   ├── ChatMessage.tsx           # Single message
│   │   ├── ChatInput.tsx             # Message input
│   │   └── ChatHistory.tsx           # Conversation history
│   │
│   ├── baskets/                      # Basket feature
│   │   ├── BasketList.tsx            # Basket list view
│   │   ├── BasketCard.tsx            # Single basket
│   │   └── BasketEditor.tsx          # Basket management
│   │
│   ├── dashboard/                    # Dashboard views
│   │   ├── Dashboard.tsx             # Main dashboard
│   │   ├── InstrumentDashboard.tsx   # Per-instrument view
│   │   ├── SiloDashboard.tsx         # Per-silo view
│   │   └── OverviewPanel.tsx         # Quick overview
│   │
│   └── ai/                           # AI management
│       ├── AISettings.tsx            # AI configuration
│       ├── UsageDisplay.tsx          # Usage statistics
│       ├── ModelSelector.tsx         # Model picker
│       └── BudgetIndicator.tsx       # Budget status
│
├── pages/                            # Route pages
│   ├── HomePage.tsx                  # Landing/dashboard
│   ├── InstrumentsPage.tsx           # Instruments listing
│   ├── InstrumentDetailPage.tsx      # Single instrument
│   ├── SiloDetailPage.tsx            # Single silo
│   ├── ChatPage.tsx                  # AI chat interface
│   ├── SettingsPage.tsx              # Application settings
│   └── NotFoundPage.tsx              # 404 page
│
└── test/                             # Test files
    ├── setup.ts                      # Test setup
    ├── utils/                        # Test utilities
    └── components/                   # Component tests
```

---

## 5. TypeScript Types

### 5.1 Enum Definitions

```typescript
// src/types/enums.ts

/**
 * Signal directional bias.
 * NOTE: System does NOT resolve conflicts between directions.
 */
export enum Direction {
  BULLISH = 'BULLISH',
  BEARISH = 'BEARISH',
  NEUTRAL = 'NEUTRAL',
}

/**
 * Data freshness classification.
 * NOTE: Freshness is purely DESCRIPTIVE - it does NOT invalidate data.
 */
export enum FreshnessStatus {
  CURRENT = 'CURRENT',
  RECENT = 'RECENT',
  STALE = 'STALE',
  UNAVAILABLE = 'UNAVAILABLE',
}

/**
 * Classification of signal origin.
 */
export enum SignalType {
  HEARTBEAT = 'HEARTBEAT',
  STATE_CHANGE = 'STATE_CHANGE',
  BAR_CLOSE = 'BAR_CLOSE',
  MANUAL = 'MANUAL',
}

/**
 * Analytical basket classification.
 * CRITICAL: Baskets exist ONLY in the UI layer.
 */
export enum BasketType {
  LOGICAL = 'LOGICAL',
  HIERARCHICAL = 'HIERARCHICAL',
  CONTEXTUAL = 'CONTEXTUAL',
  CUSTOM = 'CUSTOM',
}

/**
 * Types of narrative sections generated by AI.
 * NOTE: All narrative types are DESCRIPTIVE, never PRESCRIPTIVE.
 */
export enum NarrativeSectionType {
  SIGNAL_SUMMARY = 'SIGNAL_SUMMARY',
  CONTRADICTION = 'CONTRADICTION',
  CONFIRMATION = 'CONFIRMATION',
  FRESHNESS = 'FRESHNESS',
}

/**
 * Status of AI response validation.
 */
export enum ValidationStatus {
  VALID = 'VALID',
  INVALID = 'INVALID',
  REMEDIATED = 'REMEDIATED',
}

/**
 * Claude model tiers for dynamic selection.
 */
export enum AIModelTier {
  HAIKU = 'HAIKU',
  SONNET = 'SONNET',
  OPUS = 'OPUS',
}

/**
 * Time periods for AI usage tracking.
 */
export enum UsagePeriod {
  DAILY = 'DAILY',
  WEEKLY = 'WEEKLY',
  MONTHLY = 'MONTHLY',
}

/**
 * Message roles in conversation.
 */
export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
}
```

### 5.2 Domain Model Types

```typescript
// src/types/models.ts

import type {
  Direction,
  FreshnessStatus,
  SignalType,
  BasketType,
  NarrativeSectionType,
  MessageRole,
} from './enums'

/**
 * A tradeable financial asset.
 */
export interface Instrument {
  instrument_id: string
  symbol: string
  display_name: string
  created_at: string
  updated_at: string
  is_active: boolean
  metadata?: Record<string, unknown>
}

/**
 * A logical container grouping charts for a single instrument.
 */
export interface Silo {
  silo_id: string
  instrument_id: string
  silo_name: string
  heartbeat_enabled: boolean
  heartbeat_frequency_min: number
  current_threshold_min: number
  recent_threshold_min: number
  stale_threshold_min: number
  created_at: string
  updated_at: string
  is_active: boolean
}

/**
 * A TradingView chart that emits signals via webhook.
 * 
 * CRITICAL: NO WEIGHT PROPERTY
 * Per ADR-003: Weights enable aggregation which is PROHIBITED.
 * All charts have equal standing.
 */
export interface Chart {
  chart_id: string
  silo_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  webhook_id: string
  created_at: string
  updated_at: string
  is_active: boolean
  // NOTE: Deliberately NO weight field - prohibited by Section 0B
}

/**
 * A point-in-time data emission from a chart.
 * 
 * CRITICAL: NO CONFIDENCE/STRENGTH SCORES
 * Per ADR-003: Scores imply system judgment which is PROHIBITED.
 */
export interface Signal {
  signal_id: string
  chart_id: string
  received_at: string
  signal_timestamp: string
  signal_type: SignalType
  direction: Direction
  indicators: Record<string, unknown>
  raw_payload: Record<string, unknown>
  // NOTE: Deliberately NO confidence or strength field - prohibited by Section 0B
}

/**
 * Current status of a chart including its latest signal and freshness.
 */
export interface ChartSignalStatus {
  chart_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  latest_signal: Signal | null
  freshness: FreshnessStatus
}

/**
 * Represents a detected contradiction between two charts.
 * 
 * PROHIBITED ACTIONS:
 * - Resolving which signal is "correct"
 * - Suggesting which to prioritize
 * - Hiding any contradiction
 */
export interface Contradiction {
  chart_a_id: string
  chart_a_name: string
  chart_a_direction: Direction
  chart_b_id: string
  chart_b_name: string
  chart_b_direction: Direction
  detected_at: string
}

/**
 * Represents detected alignment between two charts.
 * NOTE: Does NOT weight or prioritize confirmations.
 */
export interface Confirmation {
  chart_a_id: string
  chart_a_name: string
  chart_b_id: string
  chart_b_name: string
  aligned_direction: Direction
  detected_at: string
}

/**
 * Complete relationship summary for a silo.
 * 
 * - Returns ALL charts (none hidden)
 * - Returns ALL contradictions (none resolved)
 * - Returns ALL confirmations (none weighted)
 * - NO aggregation anywhere
 * - NO scores anywhere
 * - NO recommendations anywhere
 */
export interface RelationshipSummary {
  silo_id: string
  silo_name: string
  instrument_id: string
  instrument_symbol: string
  charts: ChartSignalStatus[]
  contradictions: Contradiction[]
  confirmations: Confirmation[]
  generated_at: string
}

/**
 * A section of the AI-generated narrative.
 * All sections are DESCRIPTIVE, never PRESCRIPTIVE.
 */
export interface NarrativeSection {
  section_type: NarrativeSectionType
  content: string
  referenced_chart_ids: string[]
}

/**
 * Complete AI-generated narrative.
 * 
 * REQUIRED CLOSING STATEMENT:
 * "This is a description of what your charts are showing.
 * The interpretation and any decision is entirely yours."
 */
export interface Narrative {
  narrative_id: string
  silo_id: string
  sections: NarrativeSection[]
  closing_statement: string
  generated_at: string
}

/**
 * A user-defined grouping of charts for comparison.
 * 
 * CRITICAL: Baskets are organizational/display constructs ONLY.
 * They have ZERO impact on signal processing.
 */
export interface AnalyticalBasket {
  basket_id: string
  basket_name: string
  basket_type: BasketType
  description?: string
  instrument_id?: string
  chart_ids: string[]
  created_at: string
  updated_at: string
  is_active: boolean
}

/**
 * AI conversation message.
 */
export interface ChatMessage {
  role: MessageRole
  content: string
  timestamp: string
}

/**
 * AI conversation with an instrument.
 */
export interface Conversation {
  conversation_id: string
  instrument_id: string
  messages: ChatMessage[]
  model_used: string
  total_tokens: number
  total_cost: number
  created_at: string
  updated_at: string
}

/**
 * AI model information.
 */
export interface AIModel {
  id: string
  display_name: string
  description: string
  cost_per_1k_input_tokens: number
  cost_per_1k_output_tokens: number
  max_tokens: number
  capabilities: string[]
  recommended_for: string[]
}

/**
 * AI usage statistics.
 */
export interface AIUsage {
  period: string
  period_start: string
  period_end: string
  tokens_used: {
    input: number
    output: number
    total: number
  }
  cost: {
    amount: number
    currency: string
  }
  budget: {
    limit: number
    used: number
    remaining: number
    percentage_used: number
  }
  requests_count: number
  average_tokens_per_request: number
  model_breakdown: Array<{
    model_id: string
    requests: number
    tokens: number
    cost: number
  }>
}

/**
 * Platform connection status.
 */
export interface Platform {
  platform_name: string
  display_name: string
  status: 'connected' | 'disconnected' | 'connecting'
  connected_at?: string
}

/**
 * Health check response.
 */
export interface HealthStatus {
  status: 'healthy' | 'unhealthy'
  version: string
  timestamp: string
}
```

### 5.3 API Request/Response Types

```typescript
// src/types/api.ts

import type {
  Direction,
  SignalType,
  BasketType,
} from './enums'
import type {
  Instrument,
  Silo,
  Chart,
  Signal,
  RelationshipSummary,
  Narrative,
  AnalyticalBasket,
  AIModel,
  AIUsage,
  ChatMessage,
} from './models'

// ============================================================================
// Request Types
// ============================================================================

export interface InstrumentCreateRequest {
  symbol: string
  display_name: string
  metadata?: Record<string, unknown>
}

export interface InstrumentUpdateRequest {
  display_name?: string
  is_active?: boolean
  metadata?: Record<string, unknown>
}

export interface SiloCreateRequest {
  instrument_id: string
  silo_name: string
  heartbeat_enabled?: boolean
  heartbeat_frequency_min?: number
  current_threshold_min?: number
  recent_threshold_min?: number
  stale_threshold_min?: number
}

export interface ChartCreateRequest {
  silo_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  webhook_id: string
}

export interface BasketCreateRequest {
  basket_name: string
  basket_type?: BasketType
  description?: string
  instrument_id?: string
  chart_ids?: string[]
}

export interface ChatRequest {
  message: string
  model?: string
  include_context?: boolean
  conversation_id?: string
}

export interface StrategyEvaluateRequest {
  scrip_id: string
  strategy_description: string
  model?: string
}

export interface WebhookPayload {
  webhook_id: string
  direction: Direction
  indicators?: Record<string, unknown>
}

// ============================================================================
// Response Types
// ============================================================================

export interface ChatResponse {
  conversation_id: string
  message: {
    role: 'assistant'
    content: string
  }
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
  disclaimer: string
}

export interface StrategyEvaluateResponse {
  analysis: {
    alignment_with_signals: string
    contradictions_noted: string[]
    confirmations_noted: string[]
    freshness_concerns: string[]
  }
  disclaimer: string
  usage: {
    input_tokens: number
    output_tokens: number
    cost: number
    model_used: string
  }
}

export interface WebhookResponse {
  status: 'accepted' | 'rejected'
  signal_id?: string
  chart_id?: string
  direction?: Direction
  received_at?: string
  error?: string
}

export interface NarrativeResponse extends Narrative {
  // Extends Narrative with no additional fields
}

export interface PlainNarrativeResponse {
  text: string
  generated_at: string
}

export interface AIModelsResponse {
  models: AIModel[]
  default_model: string
  budget_remaining: number
}

export interface AIBudgetResponse {
  limit: number
  used: number
  remaining: number
  percentage_used: number
  alert_threshold: number
  alert_triggered: boolean
}

export interface AIHealthResponse {
  status: 'healthy' | 'unhealthy'
  api_key_configured: boolean
  last_successful_call: string
  error_rate_24h: number
}

export interface ConversationHistoryResponse {
  scrip_id: string
  conversations: Array<{
    conversation_id: string
    messages: ChatMessage[]
    created_at: string
    total_tokens: number
    total_cost: number
  }>
}

export interface ContradictionsResponse {
  contradictions: Array<{
    chart_a_id: string
    chart_a_name: string
    chart_a_direction: Direction
    chart_b_id: string
    chart_b_name: string
    chart_b_direction: Direction
    detected_at: string
  }>
  count: number
}

export interface PlatformStatusResponse {
  platform_name: string
  status: 'healthy' | 'unhealthy'
  last_heartbeat?: string
  latency_ms?: number
}

export interface PlatformSetupResponse {
  platform_name: string
  display_name: string
  instructions: string[]
  documentation_url: string
}

export interface ErrorResponse {
  detail: string
}

// ============================================================================
// Query Parameter Types
// ============================================================================

export interface InstrumentListParams {
  active_only?: boolean
}

export interface SiloListParams {
  instrument_id?: string
  active_only?: boolean
}

export interface ChartListParams {
  silo_id?: string
  active_only?: boolean
}

export interface SignalListParams {
  limit?: number
}

export interface NarrativeParams {
  use_ai?: boolean
}

export interface UsageParams {
  period?: 'daily' | 'weekly' | 'monthly'
}

export interface HistoryParams {
  limit?: number
}
```

---

## 6. Component Architecture

### 6.1 Component Hierarchy

```
App (Root)
├── QueryClientProvider (React Query)
│   └── BrowserRouter (React Router)
│       └── AppShell (Layout)
│           ├── Header
│           │   ├── Logo
│           │   ├── Navigation
│           │   ├── InstrumentSelector
│           │   └── AIBudgetIndicator
│           │
│           ├── Sidebar
│           │   ├── NavigationLinks
│           │   ├── SiloList
│           │   └── QuickActions
│           │
│           └── MainContent (Outlet)
│               ├── Dashboard
│               │   ├── OverviewPanel
│               │   ├── ChartGrid
│               │   └── RelationshipSummary
│               │
│               ├── InstrumentDashboard
│               │   ├── InstrumentHeader
│               │   ├── SiloList
│               │   └── NarrativeDisplay
│               │
│               ├── SiloDashboard
│               │   ├── ChartList
│               │   ├── ContradictionPanel
│               │   ├── ConfirmationPanel
│               │   └── NarrativeDisplay
│               │
│               └── ChatInterface
│                   ├── MessageHistory
│                   ├── ChatInput
│                   └── ModelSelector
```

### 6.2 Root Container Component

```typescript
// src/App.tsx

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppShell } from '@components/layout/AppShell'
import { HomePage } from '@/pages/HomePage'
import { InstrumentsPage } from '@/pages/InstrumentsPage'
import { InstrumentDetailPage } from '@/pages/InstrumentDetailPage'
import { SiloDetailPage } from '@/pages/SiloDetailPage'
import { ChatPage } from '@/pages/ChatPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000, // 30 seconds
      gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
      retry: 2,
      refetchOnWindowFocus: true,
    },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppShell />}>
            <Route index element={<HomePage />} />
            <Route path="instruments" element={<InstrumentsPage />} />
            <Route path="instruments/:instrumentId" element={<InstrumentDetailPage />} />
            <Route path="silos/:siloId" element={<SiloDetailPage />} />
            <Route path="chat/:instrumentId?" element={<ChatPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
```

### 6.3 Layout Components

```typescript
// src/components/layout/AppShell.tsx

import { Outlet } from 'react-router-dom'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

export function AppShell() {
  return (
    <div className="min-h-screen bg-surface-primary text-white">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

```typescript
// src/components/layout/Header.tsx

import { Link } from 'react-router-dom'
import { Activity, Settings } from 'lucide-react'
import { InstrumentSelector } from '@components/instruments/InstrumentSelector'
import { BudgetIndicator } from '@components/ai/BudgetIndicator'

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-700 bg-surface-secondary/95 backdrop-blur">
      <div className="flex h-16 items-center justify-between px-4 lg:px-8">
        <Link to="/" className="flex items-center gap-2">
          <Activity className="h-6 w-6 text-accent-primary" />
          <span className="font-display text-xl font-bold">CIA-SIE</span>
        </Link>
        
        <div className="flex items-center gap-4">
          <InstrumentSelector />
          <BudgetIndicator />
          <Link to="/settings" className="rounded-lg p-2 hover:bg-surface-tertiary">
            <Settings className="h-5 w-5" />
          </Link>
        </div>
      </div>
    </header>
  )
}
```

### 6.4 Feature Module Components

#### Signal Display Components

```typescript
// src/components/signals/DirectionBadge.tsx

import { clsx } from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import type { Direction } from '@types/enums'

interface DirectionBadgeProps {
  direction: Direction
  showLabel?: boolean
  size?: 'sm' | 'md' | 'lg'
}

/**
 * Displays a signal direction with EQUAL visual prominence.
 * 
 * CONSTITUTIONAL: All directions have equal visual weight.
 * No direction is displayed as "more important" than another.
 */
export function DirectionBadge({ 
  direction, 
  showLabel = true,
  size = 'md' 
}: DirectionBadgeProps) {
  const config = {
    BULLISH: {
      icon: TrendingUp,
      label: 'Bullish',
      className: 'bg-signal-bullish/20 text-signal-bullish border-signal-bullish/40',
    },
    BEARISH: {
      icon: TrendingDown,
      label: 'Bearish',
      className: 'bg-signal-bearish/20 text-signal-bearish border-signal-bearish/40',
    },
    NEUTRAL: {
      icon: Minus,
      label: 'Neutral',
      className: 'bg-signal-neutral/20 text-signal-neutral border-signal-neutral/40',
    },
  }[direction]

  const Icon = config.icon
  
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-3 py-1 text-sm gap-1.5',
    lg: 'px-4 py-1.5 text-base gap-2',
  }[size]

  const iconSizes = {
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
    lg: 'h-5 w-5',
  }[size]

  return (
    <span className={clsx(
      'inline-flex items-center rounded-full border font-medium',
      config.className,
      sizeClasses
    )}>
      <Icon className={iconSizes} />
      {showLabel && config.label}
    </span>
  )
}
```

```typescript
// src/components/signals/FreshnessBadge.tsx

import { clsx } from 'clsx'
import { Clock, AlertCircle, AlertTriangle, HelpCircle } from 'lucide-react'
import type { FreshnessStatus } from '@types/enums'

interface FreshnessBadgeProps {
  status: FreshnessStatus
  showLabel?: boolean
}

/**
 * Displays data freshness status.
 * 
 * CONSTITUTIONAL: Freshness is purely DESCRIPTIVE.
 * It does NOT invalidate or suppress data.
 */
export function FreshnessBadge({ status, showLabel = true }: FreshnessBadgeProps) {
  const config = {
    CURRENT: {
      icon: Clock,
      label: 'Current',
      className: 'text-freshness-current',
    },
    RECENT: {
      icon: Clock,
      label: 'Recent',
      className: 'text-freshness-recent',
    },
    STALE: {
      icon: AlertTriangle,
      label: 'Stale',
      className: 'text-freshness-stale',
    },
    UNAVAILABLE: {
      icon: HelpCircle,
      label: 'No Data',
      className: 'text-freshness-unavailable',
    },
  }[status]

  const Icon = config.icon

  return (
    <span className={clsx('inline-flex items-center gap-1 text-sm', config.className)}>
      <Icon className="h-4 w-4" />
      {showLabel && config.label}
    </span>
  )
}
```

#### Contradiction Display (Constitutional Critical)

```typescript
// src/components/relationships/ContradictionPanel.tsx

import type { Contradiction } from '@types/models'
import { ContradictionCard } from './ContradictionCard'
import { AlertTriangle } from 'lucide-react'

interface ContradictionPanelProps {
  contradictions: Contradiction[]
}

/**
 * Displays ALL contradictions between chart signals.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * - Displays ALL contradictions (none hidden)
 * - EQUAL visual prominence for both sides
 * - NO resolution or "winner" indicated
 * - NO aggregation or summary score
 */
export function ContradictionPanel({ contradictions }: ContradictionPanelProps) {
  if (contradictions.length === 0) {
    return (
      <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
        <div className="flex items-center gap-2 text-slate-400">
          <AlertTriangle className="h-5 w-5" />
          <span>No contradictions detected</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-5 w-5 text-amber-500" />
        <h3 className="font-display text-lg font-semibold">
          Contradictions ({contradictions.length})
        </h3>
      </div>
      
      {/* 
        CONSTITUTIONAL: Each contradiction shown with EQUAL prominence.
        Grid layout ensures equal sizing.
      */}
      <div className="grid gap-4">
        {contradictions.map((contradiction) => (
          <ContradictionCard 
            key={`${contradiction.chart_a_id}-${contradiction.chart_b_id}`}
            contradiction={contradiction}
          />
        ))}
      </div>
    </div>
  )
}
```

```typescript
// src/components/relationships/ContradictionCard.tsx

import type { Contradiction } from '@types/models'
import { DirectionBadge } from '@components/signals/DirectionBadge'
import { ArrowLeftRight } from 'lucide-react'

interface ContradictionCardProps {
  contradiction: Contradiction
}

/**
 * Displays a single contradiction between two charts.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * - Both charts displayed with IDENTICAL styling
 * - No visual hierarchy suggesting one is "correct"
 * - Side-by-side layout with equal space allocation
 */
export function ContradictionCard({ contradiction }: ContradictionCardProps) {
  return (
    <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-4">
      <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">
        {/* Chart A - EQUAL SIZE */}
        <div className="rounded-lg bg-surface-secondary p-3 text-center">
          <div className="mb-2 text-sm text-slate-400">{contradiction.chart_a_name}</div>
          <DirectionBadge direction={contradiction.chart_a_direction} size="lg" />
        </div>
        
        {/* Separator - No bias indicator */}
        <div className="flex flex-col items-center gap-1">
          <ArrowLeftRight className="h-5 w-5 text-slate-500" />
          <span className="text-xs text-slate-500">vs</span>
        </div>
        
        {/* Chart B - EQUAL SIZE (identical to Chart A) */}
        <div className="rounded-lg bg-surface-secondary p-3 text-center">
          <div className="mb-2 text-sm text-slate-400">{contradiction.chart_b_name}</div>
          <DirectionBadge direction={contradiction.chart_b_direction} size="lg" />
        </div>
      </div>
    </div>
  )
}
```

#### Mandatory Disclaimer Component

```typescript
// src/components/common/Disclaimer.tsx

import { Info } from 'lucide-react'

interface DisclaimerProps {
  variant?: 'inline' | 'block'
}

/**
 * Mandatory disclaimer for AI-generated content.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-001):
 * This disclaimer MUST appear on ALL AI-generated content.
 */
export function Disclaimer({ variant = 'block' }: DisclaimerProps) {
  const text = "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."

  if (variant === 'inline') {
    return (
      <span className="text-sm italic text-slate-400">
        {text}
      </span>
    )
  }

  return (
    <div className="mt-4 rounded-lg border border-slate-600 bg-slate-800/50 p-4">
      <div className="flex items-start gap-3">
        <Info className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" />
        <p className="text-sm italic text-slate-300">
          {text}
        </p>
      </div>
    </div>
  )
}
```

#### AI Narrative Display

```typescript
// src/components/narratives/NarrativeDisplay.tsx

import type { Narrative } from '@types/models'
import { NarrativeSection } from './NarrativeSection'
import { Disclaimer } from '@components/common/Disclaimer'
import { FileText } from 'lucide-react'

interface NarrativeDisplayProps {
  narrative: Narrative
}

/**
 * Displays AI-generated narrative.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-001, CR-003):
 * - Content is DESCRIPTIVE only
 * - Mandatory disclaimer is ALWAYS displayed
 * - No prescriptive language
 */
export function NarrativeDisplay({ narrative }: NarrativeDisplayProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <FileText className="h-5 w-5 text-accent-primary" />
        <h3 className="font-display text-lg font-semibold">Signal Narrative</h3>
      </div>

      <div className="space-y-4 rounded-lg border border-slate-700 bg-surface-secondary p-4">
        {narrative.sections.map((section, index) => (
          <NarrativeSection key={index} section={section} />
        ))}
      </div>

      {/* MANDATORY: Disclaimer must always be displayed */}
      <Disclaimer />
    </div>
  )
}
```

### 6.5 Atomic Components

```typescript
// src/components/common/Button.tsx

import { clsx } from 'clsx'
import { Loader2 } from 'lucide-react'
import type { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  children: ReactNode
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled,
  className,
  children,
  ...props
}: ButtonProps) {
  const variantClasses = {
    primary: 'bg-accent-primary hover:bg-accent-primary/90 text-white',
    secondary: 'bg-surface-tertiary hover:bg-surface-tertiary/80 text-white',
    ghost: 'hover:bg-surface-tertiary text-slate-300',
  }[variant]

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }[size]

  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors',
        'disabled:cursor-not-allowed disabled:opacity-50',
        variantClasses,
        sizeClasses,
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" />}
      {children}
    </button>
  )
}
```

```typescript
// src/components/common/Card.tsx

import { clsx } from 'clsx'
import type { HTMLAttributes, ReactNode } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
  padding?: 'sm' | 'md' | 'lg'
}

export function Card({ 
  children, 
  padding = 'md',
  className,
  ...props 
}: CardProps) {
  const paddingClasses = {
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  }[padding]

  return (
    <div 
      className={clsx(
        'rounded-lg border border-slate-700 bg-surface-secondary',
        paddingClasses,
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}
```

```typescript
// src/components/common/Spinner.tsx

import { Loader2 } from 'lucide-react'
import { clsx } from 'clsx'

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function Spinner({ size = 'md', className }: SpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  }[size]

  return (
    <Loader2 className={clsx('animate-spin text-accent-primary', sizeClasses, className)} />
  )
}
```

```typescript
// src/components/common/EmptyState.tsx

import type { ReactNode } from 'react'
import { Inbox } from 'lucide-react'

interface EmptyStateProps {
  icon?: ReactNode
  title: string
  description?: string
  action?: ReactNode
}

export function EmptyState({ 
  icon, 
  title, 
  description, 
  action 
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="mb-4 text-slate-500">
        {icon ?? <Inbox className="h-12 w-12" />}
      </div>
      <h3 className="mb-2 font-display text-lg font-semibold text-slate-300">
        {title}
      </h3>
      {description && (
        <p className="mb-4 max-w-sm text-sm text-slate-400">
          {description}
        </p>
      )}
      {action}
    </div>
  )
}
```

---

## 7. State Management

### 7.1 State Categories

| Category | Solution | Use Case |
|----------|----------|----------|
| Server State | React Query | API data, caching, synchronization |
| Global UI State | React Context | Theme, active instrument, modals |
| Local UI State | useState | Form inputs, toggles, selections |
| URL State | React Router | Navigation, deep linking |

### 7.2 React Query Configuration

```typescript
// src/lib/queryClient.ts

import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Signal data should be considered stale quickly (30s)
      staleTime: 30 * 1000,
      // Keep in cache for 5 minutes
      gcTime: 5 * 60 * 1000,
      // Retry twice on failure
      retry: 2,
      // Refetch when window regains focus (important for signal freshness)
      refetchOnWindowFocus: true,
      // Don't refetch on mount if data is fresh
      refetchOnMount: false,
    },
    mutations: {
      retry: 1,
    },
  },
})
```

### 7.3 Query Key Factory

```typescript
// src/lib/queryKeys.ts

export const queryKeys = {
  // Health
  health: ['health'] as const,

  // Instruments
  instruments: {
    all: ['instruments'] as const,
    lists: () => [...queryKeys.instruments.all, 'list'] as const,
    list: (filters: { active_only?: boolean }) => 
      [...queryKeys.instruments.lists(), filters] as const,
    details: () => [...queryKeys.instruments.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.instruments.details(), id] as const,
    bySymbol: (symbol: string) => 
      [...queryKeys.instruments.all, 'symbol', symbol] as const,
  },

  // Silos
  silos: {
    all: ['silos'] as const,
    lists: () => [...queryKeys.silos.all, 'list'] as const,
    list: (filters: { instrument_id?: string; active_only?: boolean }) => 
      [...queryKeys.silos.lists(), filters] as const,
    details: () => [...queryKeys.silos.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.silos.details(), id] as const,
  },

  // Charts
  charts: {
    all: ['charts'] as const,
    lists: () => [...queryKeys.charts.all, 'list'] as const,
    list: (filters: { silo_id?: string; active_only?: boolean }) => 
      [...queryKeys.charts.lists(), filters] as const,
    details: () => [...queryKeys.charts.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.charts.details(), id] as const,
    byWebhook: (webhookId: string) => 
      [...queryKeys.charts.all, 'webhook', webhookId] as const,
  },

  // Signals
  signals: {
    all: ['signals'] as const,
    forChart: (chartId: string, limit?: number) => 
      [...queryKeys.signals.all, 'chart', chartId, { limit }] as const,
    latest: (chartId: string) => 
      [...queryKeys.signals.all, 'chart', chartId, 'latest'] as const,
    detail: (id: string) => [...queryKeys.signals.all, 'detail', id] as const,
  },

  // Relationships
  relationships: {
    all: ['relationships'] as const,
    forSilo: (siloId: string) => 
      [...queryKeys.relationships.all, 'silo', siloId] as const,
    forInstrument: (instrumentId: string) => 
      [...queryKeys.relationships.all, 'instrument', instrumentId] as const,
    contradictions: (siloId: string) => 
      [...queryKeys.relationships.all, 'contradictions', siloId] as const,
  },

  // Narratives
  narratives: {
    all: ['narratives'] as const,
    forSilo: (siloId: string, useAi?: boolean) => 
      [...queryKeys.narratives.all, 'silo', siloId, { useAi }] as const,
    plain: (siloId: string) => 
      [...queryKeys.narratives.all, 'silo', siloId, 'plain'] as const,
  },

  // AI
  ai: {
    all: ['ai'] as const,
    models: () => [...queryKeys.ai.all, 'models'] as const,
    usage: (period?: string) => [...queryKeys.ai.all, 'usage', period] as const,
    budget: () => [...queryKeys.ai.all, 'budget'] as const,
    health: () => [...queryKeys.ai.all, 'health'] as const,
  },

  // Chat
  chat: {
    all: ['chat'] as const,
    history: (instrumentId: string, limit?: number) => 
      [...queryKeys.chat.all, 'history', instrumentId, { limit }] as const,
  },

  // Baskets
  baskets: {
    all: ['baskets'] as const,
    lists: () => [...queryKeys.baskets.all, 'list'] as const,
    list: (filters: { instrument_id?: string; active_only?: boolean }) => 
      [...queryKeys.baskets.lists(), filters] as const,
    detail: (id: string) => [...queryKeys.baskets.all, 'detail', id] as const,
  },

  // Platforms
  platforms: {
    all: ['platforms'] as const,
    list: () => [...queryKeys.platforms.all, 'list'] as const,
    detail: (name: string) => [...queryKeys.platforms.all, 'detail', name] as const,
    health: (name: string) => [...queryKeys.platforms.all, 'health', name] as const,
    setup: (name: string) => [...queryKeys.platforms.all, 'setup', name] as const,
  },
} as const
```

### 7.4 Custom Hooks for Data Fetching

```typescript
// src/hooks/useRelationships.ts

import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { relationshipsApi } from '@services/relationships'
import type { RelationshipSummary } from '@types/models'

/**
 * Fetch relationship summary for a silo.
 * 
 * CONSTITUTIONAL: Returns ALL relationships without filtering or aggregation.
 * - All charts included
 * - All contradictions exposed
 * - All confirmations listed
 * - No scores or weights
 */
export function useRelationshipSummary(siloId: string) {
  return useQuery<RelationshipSummary>({
    queryKey: queryKeys.relationships.forSilo(siloId),
    queryFn: () => relationshipsApi.getForSilo(siloId),
    enabled: !!siloId,
    // Relationships change frequently with new signals
    staleTime: 15 * 1000, // 15 seconds
  })
}

/**
 * Fetch relationship summaries for all silos of an instrument.
 */
export function useInstrumentRelationships(instrumentId: string) {
  return useQuery<RelationshipSummary[]>({
    queryKey: queryKeys.relationships.forInstrument(instrumentId),
    queryFn: () => relationshipsApi.getForInstrument(instrumentId),
    enabled: !!instrumentId,
    staleTime: 15 * 1000,
  })
}
```

```typescript
// src/hooks/useNarratives.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { narrativesApi } from '@services/narratives'
import type { Narrative, NarrativeParams } from '@types/api'

/**
 * Fetch AI-generated narrative for a silo.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - Narrative content is validated server-side
 * - Always includes mandatory disclaimer
 * - Content is descriptive only
 */
export function useNarrative(siloId: string, params?: NarrativeParams) {
  return useQuery<Narrative>({
    queryKey: queryKeys.narratives.forSilo(siloId, params?.use_ai),
    queryFn: () => narrativesApi.generate(siloId, params),
    enabled: !!siloId,
    // AI narratives are computationally expensive - cache longer
    staleTime: 60 * 1000, // 1 minute
    gcTime: 10 * 60 * 1000, // 10 minutes
  })
}

/**
 * Generate a fresh narrative (mutation).
 */
export function useGenerateNarrative() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ siloId, params }: { siloId: string; params?: NarrativeParams }) =>
      narrativesApi.generate(siloId, params),
    onSuccess: (data, { siloId, params }) => {
      queryClient.setQueryData(
        queryKeys.narratives.forSilo(siloId, params?.use_ai),
        data
      )
    },
  })
}
```

### 7.5 Global UI Context

```typescript
// src/contexts/AppContext.tsx

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'
import type { Instrument } from '@types/models'

interface AppContextValue {
  activeInstrument: Instrument | null
  setActiveInstrument: (instrument: Instrument | null) => void
  sidebarOpen: boolean
  toggleSidebar: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
  const [activeInstrument, setActiveInstrument] = useState<Instrument | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const toggleSidebar = useCallback(() => {
    setSidebarOpen(prev => !prev)
  }, [])

  return (
    <AppContext.Provider 
      value={{ 
        activeInstrument, 
        setActiveInstrument, 
        sidebarOpen, 
        toggleSidebar 
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
```

---

## 8. Real-Time Data Flow

### 8.1 Data Freshness Management

Signal freshness is a core concept - the system must display how current each signal is.

```typescript
// src/utils/freshness.ts

import type { FreshnessStatus } from '@types/enums'
import type { Silo, Signal } from '@types/models'
import { differenceInMinutes } from 'date-fns'

interface FreshnessThresholds {
  current: number  // minutes
  recent: number   // minutes
  stale: number    // minutes
}

/**
 * Calculate freshness status for a signal based on silo thresholds.
 * 
 * CONSTITUTIONAL: Freshness is DESCRIPTIVE only.
 * It does not invalidate or suppress any data.
 */
export function calculateFreshness(
  signal: Signal | null,
  thresholds: FreshnessThresholds
): FreshnessStatus {
  if (!signal) {
    return 'UNAVAILABLE'
  }

  const signalTime = new Date(signal.signal_timestamp)
  const now = new Date()
  const ageMinutes = differenceInMinutes(now, signalTime)

  if (ageMinutes <= thresholds.current) {
    return 'CURRENT'
  }
  if (ageMinutes <= thresholds.recent) {
    return 'RECENT'
  }
  if (ageMinutes <= thresholds.stale) {
    return 'STALE'
  }
  return 'STALE' // Anything older is still stale (not hidden!)
}

/**
 * Extract thresholds from a silo.
 */
export function getSiloThresholds(silo: Silo): FreshnessThresholds {
  return {
    current: silo.current_threshold_min,
    recent: silo.recent_threshold_min,
    stale: silo.stale_threshold_min,
  }
}
```

### 8.2 Polling Strategy

```typescript
// src/hooks/useSignalPolling.ts

import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { signalsApi } from '@services/signals'
import type { Signal } from '@types/models'

/**
 * Poll for latest signal with automatic refresh.
 * 
 * Uses React Query's refetchInterval for efficient polling.
 */
export function useLatestSignal(chartId: string, pollInterval = 30000) {
  return useQuery<Signal | null>({
    queryKey: queryKeys.signals.latest(chartId),
    queryFn: () => signalsApi.getLatest(chartId),
    enabled: !!chartId,
    // Poll every 30 seconds by default
    refetchInterval: pollInterval,
    // Keep polling even when tab is in background
    refetchIntervalInBackground: false,
  })
}

/**
 * Poll relationship summary for a silo.
 */
export function useRelationshipPolling(siloId: string, pollInterval = 30000) {
  return useQuery({
    queryKey: queryKeys.relationships.forSilo(siloId),
    queryFn: () => relationshipsApi.getForSilo(siloId),
    enabled: !!siloId,
    refetchInterval: pollInterval,
    refetchIntervalInBackground: false,
    staleTime: pollInterval / 2,
  })
}
```

### 8.3 Optimistic Updates

```typescript
// src/hooks/useWebhookMutations.ts

import { useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { webhookApi } from '@services/webhook'
import type { WebhookPayload, Signal } from '@types/models'

/**
 * Submit a manual signal via webhook.
 * 
 * Uses optimistic updates to immediately reflect the new signal.
 */
export function useManualSignal() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: WebhookPayload) => webhookApi.submit(payload),
    
    // Optimistically update the cache
    onMutate: async (payload) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ 
        queryKey: queryKeys.signals.all 
      })

      // We could optimistically add the signal here, but for constitutional
      // compliance, we wait for server confirmation to ensure proper validation
    },

    // On success, invalidate relevant queries
    onSuccess: (response) => {
      if (response.chart_id) {
        queryClient.invalidateQueries({ 
          queryKey: queryKeys.signals.forChart(response.chart_id) 
        })
        queryClient.invalidateQueries({ 
          queryKey: queryKeys.signals.latest(response.chart_id) 
        })
        // Also invalidate relationships as contradictions may have changed
        queryClient.invalidateQueries({ 
          queryKey: queryKeys.relationships.all 
        })
      }
    },
  })
}
```

### 8.4 WebSocket Integration (Future)

```typescript
// src/hooks/useWebSocketSignals.ts
// NOTE: Placeholder for future WebSocket implementation

import { useEffect, useRef, useCallback } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'

interface WebSocketMessage {
  type: 'signal' | 'relationship_update'
  payload: unknown
}

/**
 * WebSocket connection for real-time signal updates.
 * 
 * FUTURE IMPLEMENTATION:
 * When WebSocket support is added to the backend, this hook will:
 * - Maintain a persistent connection
 * - Receive signal updates in real-time
 * - Automatically invalidate React Query caches
 */
export function useWebSocketSignals(enabled = false) {
  const queryClient = useQueryClient()
  const wsRef = useRef<WebSocket | null>(null)

  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const message: WebSocketMessage = JSON.parse(event.data)

      if (message.type === 'signal') {
        // Invalidate signal queries
        queryClient.invalidateQueries({ queryKey: queryKeys.signals.all })
        queryClient.invalidateQueries({ queryKey: queryKeys.relationships.all })
      }
    } catch (error) {
      console.error('WebSocket message parse error:', error)
    }
  }, [queryClient])

  useEffect(() => {
    if (!enabled) return

    // WebSocket connection logic would go here
    // Currently not implemented in backend

    return () => {
      wsRef.current?.close()
    }
  }, [enabled, handleMessage])

  return {
    connected: false, // Will be dynamic when implemented
  }
}
```

---

## 9. API Integration

### 9.1 Axios Configuration

```typescript
// src/services/api.ts

import axios, { type AxiosError, type AxiosResponse } from 'axios'
import type { ErrorResponse } from '@types/api'

// Create axios instance with base configuration
export const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
})

// Request interceptor for logging/auth
api.interceptors.request.use(
  (config) => {
    // Could add auth headers here if needed
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError<ErrorResponse>) => {
    // Extract meaningful error message
    const message = error.response?.data?.detail ?? error.message ?? 'Unknown error'
    
    // Log for debugging
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message,
    })

    // Re-throw with structured error
    return Promise.reject(new Error(message))
  }
)
```

### 9.2 API Service Modules

```typescript
// src/services/instruments.ts

import { api } from './api'
import type { 
  Instrument, 
  InstrumentCreateRequest, 
  InstrumentUpdateRequest,
  InstrumentListParams 
} from '@types/api'

export const instrumentsApi = {
  list: async (params?: InstrumentListParams): Promise<Instrument[]> => {
    const response = await api.get('/instruments/', { params })
    return response.data
  },

  get: async (id: string): Promise<Instrument> => {
    const response = await api.get(`/instruments/${id}`)
    return response.data
  },

  getBySymbol: async (symbol: string): Promise<Instrument> => {
    const response = await api.get(`/instruments/symbol/${symbol}`)
    return response.data
  },

  create: async (data: InstrumentCreateRequest): Promise<Instrument> => {
    const response = await api.post('/instruments/', data)
    return response.data
  },

  update: async (id: string, data: InstrumentUpdateRequest): Promise<Instrument> => {
    const response = await api.patch(`/instruments/${id}`, data)
    return response.data
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/instruments/${id}`)
  },
}
```

```typescript
// src/services/relationships.ts

import { api } from './api'
import type { RelationshipSummary, ContradictionsResponse } from '@types/api'

export const relationshipsApi = {
  /**
   * Get relationship summary for a silo.
   * 
   * CONSTITUTIONAL: Returns ALL relationships without filtering.
   */
  getForSilo: async (siloId: string): Promise<RelationshipSummary> => {
    const response = await api.get(`/relationships/silo/${siloId}`)
    return response.data
  },

  /**
   * Get relationship summaries for all silos of an instrument.
   */
  getForInstrument: async (instrumentId: string): Promise<RelationshipSummary[]> => {
    const response = await api.get(`/relationships/instrument/${instrumentId}`)
    return response.data
  },

  /**
   * Get just contradictions for a silo.
   */
  getContradictions: async (siloId: string): Promise<ContradictionsResponse> => {
    const response = await api.get(`/relationships/contradictions/silo/${siloId}`)
    return response.data
  },
}
```

```typescript
// src/services/chat.ts

import { api } from './api'
import type { 
  ChatRequest, 
  ChatResponse, 
  ConversationHistoryResponse,
  HistoryParams 
} from '@types/api'

export const chatApi = {
  /**
   * Send a message to the AI for a specific instrument.
   * 
   * CONSTITUTIONAL: All responses are validated server-side for compliance.
   * Response will always include mandatory disclaimer.
   */
  sendMessage: async (instrumentId: string, request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post(`/chat/${instrumentId}`, request)
    return response.data
  },

  /**
   * Get conversation history for an instrument.
   */
  getHistory: async (
    instrumentId: string, 
    params?: HistoryParams
  ): Promise<ConversationHistoryResponse> => {
    const response = await api.get(`/chat/${instrumentId}/history`, { params })
    return response.data
  },
}
```

```typescript
// src/services/narratives.ts

import { api } from './api'
import type { Narrative, PlainNarrativeResponse, NarrativeParams } from '@types/api'

export const narrativesApi = {
  /**
   * Generate narrative for a silo.
   * 
   * CONSTITUTIONAL: Narrative is DESCRIPTIVE only.
   * Always includes mandatory disclaimer.
   */
  generate: async (siloId: string, params?: NarrativeParams): Promise<Narrative> => {
    const response = await api.get(`/narratives/silo/${siloId}`, { params })
    return response.data
  },

  /**
   * Get plain text narrative.
   */
  getPlain: async (siloId: string): Promise<PlainNarrativeResponse> => {
    const response = await api.get(`/narratives/silo/${siloId}/plain`)
    return response.data
  },
}
```

### 9.3 Request Cancellation

```typescript
// src/hooks/useCancelableQuery.ts

import { useQuery, type UseQueryOptions } from '@tanstack/react-query'
import { useRef, useEffect } from 'react'

/**
 * Query hook with automatic request cancellation.
 * 
 * Useful for expensive queries (like AI generation) that should be
 * cancelled if the user navigates away.
 */
export function useCancelableQuery<TData>(
  options: UseQueryOptions<TData> & {
    queryFn: (signal: AbortSignal) => Promise<TData>
  }
) {
  const abortControllerRef = useRef<AbortController | null>(null)

  useEffect(() => {
    return () => {
      // Cancel on unmount
      abortControllerRef.current?.abort()
    }
  }, [])

  return useQuery({
    ...options,
    queryFn: () => {
      abortControllerRef.current = new AbortController()
      return options.queryFn(abortControllerRef.current.signal)
    },
  })
}
```

---

## 10. UI State Machine

### 10.1 Standard View States

Every data-fetching component should handle these states:

| State | Trigger | Display |
|-------|---------|---------|
| IDLE | Initial mount | Nothing or placeholder |
| LOADING | Query in progress | Skeleton/spinner |
| SUCCESS | Data received | Rendered content |
| ERROR | Query failed | Error message + retry |
| EMPTY | Success but no data | Empty state message |

### 10.2 State Machine Hook

```typescript
// src/hooks/useViewState.ts

import type { UseQueryResult } from '@tanstack/react-query'

type ViewState = 'idle' | 'loading' | 'success' | 'error' | 'empty'

interface ViewStateResult<TData> {
  state: ViewState
  data: TData | undefined
  error: Error | null
  isLoading: boolean
  isEmpty: boolean
}

/**
 * Derive view state from React Query result.
 */
export function useViewState<TData>(
  query: UseQueryResult<TData, Error>,
  isEmptyFn?: (data: TData) => boolean
): ViewStateResult<TData> {
  const { data, error, isLoading, isFetching, isError, isSuccess } = query

  const isEmpty = isSuccess && data !== undefined && (isEmptyFn?.(data) ?? false)

  let state: ViewState = 'idle'
  if (isLoading) state = 'loading'
  else if (isError) state = 'error'
  else if (isEmpty) state = 'empty'
  else if (isSuccess) state = 'success'

  return {
    state,
    data,
    error: error ?? null,
    isLoading: isLoading || isFetching,
    isEmpty,
  }
}
```

### 10.3 State-Driven Components

```typescript
// src/components/common/QueryStateHandler.tsx

import type { ReactNode } from 'react'
import type { UseQueryResult } from '@tanstack/react-query'
import { useViewState } from '@hooks/useViewState'
import { Spinner } from './Spinner'
import { ErrorDisplay } from './ErrorDisplay'
import { EmptyState } from './EmptyState'

interface QueryStateHandlerProps<TData> {
  query: UseQueryResult<TData, Error>
  isEmptyFn?: (data: TData) => boolean
  children: (data: TData) => ReactNode
  loadingFallback?: ReactNode
  errorFallback?: ReactNode
  emptyFallback?: ReactNode
}

/**
 * Wrapper component that handles all query states.
 * 
 * Renders loading, error, and empty states automatically.
 * Only renders children when data is successfully loaded.
 */
export function QueryStateHandler<TData>({
  query,
  isEmptyFn,
  children,
  loadingFallback,
  errorFallback,
  emptyFallback,
}: QueryStateHandlerProps<TData>) {
  const { state, data, error } = useViewState(query, isEmptyFn)

  switch (state) {
    case 'loading':
      return loadingFallback ?? (
        <div className="flex items-center justify-center py-12">
          <Spinner size="lg" />
        </div>
      )

    case 'error':
      return errorFallback ?? (
        <ErrorDisplay 
          error={error} 
          onRetry={() => query.refetch()}
        />
      )

    case 'empty':
      return emptyFallback ?? (
        <EmptyState 
          title="No data available" 
          description="There is no data to display."
        />
      )

    case 'success':
      return <>{children(data!)}</>

    default:
      return null
  }
}
```

### 10.4 Loading States

```typescript
// src/components/common/Skeleton.tsx

import { clsx } from 'clsx'

interface SkeletonProps {
  className?: string
  variant?: 'text' | 'rectangular' | 'circular'
  width?: string | number
  height?: string | number
}

export function Skeleton({ 
  className, 
  variant = 'text',
  width,
  height,
}: SkeletonProps) {
  const baseClasses = 'animate-pulse bg-slate-700'
  
  const variantClasses = {
    text: 'h-4 rounded',
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
  }[variant]

  return (
    <div 
      className={clsx(baseClasses, variantClasses, className)}
      style={{ width, height }}
    />
  )
}

// Preset skeleton components
export function ChartCardSkeleton() {
  return (
    <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
      <Skeleton className="mb-2 h-5 w-1/3" />
      <Skeleton className="mb-4 h-4 w-2/3" />
      <Skeleton className="h-8 w-24" variant="rectangular" />
    </div>
  )
}

export function SignalListSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <ChartCardSkeleton key={i} />
      ))}
    </div>
  )
}
```

### 10.5 Error Display

```typescript
// src/components/common/ErrorDisplay.tsx

import { AlertCircle, RefreshCw } from 'lucide-react'
import { Button } from './Button'

interface ErrorDisplayProps {
  error: Error | null
  title?: string
  onRetry?: () => void
}

export function ErrorDisplay({ 
  error, 
  title = 'Something went wrong',
  onRetry 
}: ErrorDisplayProps) {
  return (
    <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-6">
      <div className="flex flex-col items-center text-center">
        <AlertCircle className="mb-4 h-12 w-12 text-red-400" />
        <h3 className="mb-2 font-display text-lg font-semibold text-red-300">
          {title}
        </h3>
        {error && (
          <p className="mb-4 text-sm text-red-300/80">
            {error.message}
          </p>
        )}
        {onRetry && (
          <Button variant="secondary" onClick={onRetry}>
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
        )}
      </div>
    </div>
  )
}
```

---

## 11. Edge Case Handling

### 11.1 Edge Case Matrix

| Scenario | Detection | Handling | User Feedback |
|----------|-----------|----------|---------------|
| API Timeout | Axios timeout | Retry with backoff | "Request timed out. Retrying..." |
| Network Offline | Navigator.onLine | Disable mutations, show banner | "You are offline" |
| Session Expired | 401 response | Redirect to login | "Session expired" |
| Rate Limited | 429 response | Exponential backoff | "Too many requests" |
| Stale Cache | Query stale | Background refetch | Subtle loading indicator |
| Partial Data | Missing fields | Fallback values | Graceful degradation |
| AI Service Down | 503 response | Show cached/template | "AI unavailable" |

### 11.2 Network Status Hook

```typescript
// src/hooks/useNetworkStatus.ts

import { useState, useEffect } from 'react'

interface NetworkStatus {
  online: boolean
  effectiveType?: 'slow-2g' | '2g' | '3g' | '4g'
}

export function useNetworkStatus(): NetworkStatus {
  const [status, setStatus] = useState<NetworkStatus>({
    online: typeof navigator !== 'undefined' ? navigator.onLine : true,
  })

  useEffect(() => {
    const handleOnline = () => setStatus(prev => ({ ...prev, online: true }))
    const handleOffline = () => setStatus(prev => ({ ...prev, online: false }))

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    // Check connection quality if available
    const connection = (navigator as any).connection
    if (connection) {
      setStatus(prev => ({ 
        ...prev, 
        effectiveType: connection.effectiveType 
      }))
    }

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  return status
}
```

### 11.3 Offline Banner

```typescript
// src/components/common/OfflineBanner.tsx

import { WifiOff } from 'lucide-react'
import { useNetworkStatus } from '@hooks/useNetworkStatus'

export function OfflineBanner() {
  const { online } = useNetworkStatus()

  if (online) return null

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-amber-600 px-4 py-2 text-center text-sm font-medium text-white">
      <WifiOff className="mr-2 inline-block h-4 w-4" />
      You are offline. Some features may be unavailable.
    </div>
  )
}
```

### 11.4 Retry Logic with Backoff

```typescript
// src/utils/retry.ts

interface RetryConfig {
  maxAttempts: number
  baseDelay: number
  maxDelay: number
}

const defaultConfig: RetryConfig = {
  maxAttempts: 3,
  baseDelay: 1000,
  maxDelay: 30000,
}

/**
 * Calculate exponential backoff delay.
 */
export function getBackoffDelay(attempt: number, config = defaultConfig): number {
  const delay = config.baseDelay * Math.pow(2, attempt)
  const jitter = Math.random() * 0.3 * delay // 30% jitter
  return Math.min(delay + jitter, config.maxDelay)
}

/**
 * Retry a function with exponential backoff.
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  config = defaultConfig
): Promise<T> {
  let lastError: Error | undefined

  for (let attempt = 0; attempt < config.maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      
      if (attempt < config.maxAttempts - 1) {
        const delay = getBackoffDelay(attempt, config)
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }

  throw lastError
}
```

### 11.5 Graceful Degradation for AI

```typescript
// src/hooks/useNarrativeWithFallback.ts

import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { narrativesApi } from '@services/narratives'
import type { Narrative } from '@types/models'

/**
 * Fetch narrative with fallback to template if AI is unavailable.
 * 
 * CONSTITUTIONAL: Both AI and template narratives are compliant.
 * Templates are pre-approved descriptive text.
 */
export function useNarrativeWithFallback(siloId: string) {
  // Try AI first
  const aiQuery = useQuery({
    queryKey: queryKeys.narratives.forSilo(siloId, true),
    queryFn: () => narrativesApi.generate(siloId, { use_ai: true }),
    enabled: !!siloId,
    retry: 1, // Only retry once for AI
  })

  // Fallback to template if AI fails
  const templateQuery = useQuery({
    queryKey: queryKeys.narratives.forSilo(siloId, false),
    queryFn: () => narrativesApi.generate(siloId, { use_ai: false }),
    enabled: !!siloId && aiQuery.isError,
  })

  return {
    data: aiQuery.data ?? templateQuery.data,
    isLoading: aiQuery.isLoading || templateQuery.isLoading,
    isError: aiQuery.isError && templateQuery.isError,
    error: templateQuery.error ?? aiQuery.error,
    isAiFallback: aiQuery.isError && templateQuery.isSuccess,
  }
}
```

---

## 12. Constitutional Enforcement at Presentation Layer

### 12.1 Response Validation Utility

```typescript
// src/utils/constitutional.ts

/**
 * CONSTITUTIONAL COMPLIANCE UTILITIES
 * 
 * These utilities enforce constitutional rules at the presentation layer.
 * They provide an additional layer of protection beyond backend validation.
 */

// Prohibited language patterns (matches backend validator)
const PROHIBITED_PATTERNS = [
  // Recommendation language
  /\byou should\b/i,
  /\bi recommend\b/i,
  /\bi suggest\b/i,
  /\bconsider (buying|selling)\b/i,
  /\bthe best action\b/i,
  /\byou must\b/i,
  /\byou need to\b/i,
  
  // Trading action language
  /\bbuy now\b/i,
  /\bsell now\b/i,
  /\benter (a )?position\b/i,
  /\bexit (the )?position\b/i,
  /\btake profit\b/i,
  /\bcut (your )?loss(es)?\b/i,
  
  // Aggregation language
  /\boverall direction\b/i,
  /\bnet signal\b/i,
  /\bconsensus\b/i,
  /\bmajority of signals\b/i,
  /\bon balance\b/i,
  
  // Confidence language
  /\bconfidence level\b/i,
  /\bprobability\b/i,
  /\blikely to (rise|fall)\b/i,
  /\bforecast\b/i,
  /\bprice target\b/i,
  /\b\d+%\s*(confidence|probability|chance)\b/i,
  
  // Ranking language
  /\bmore reliable\b/i,
  /\bstronger signal\b/i,
  /\bsignal strength\b/i,
  /\brisk score\b/i,
]

const MANDATORY_DISCLAIMER = 'The interpretation and any decision is entirely yours'

/**
 * Check if text contains prohibited patterns.
 * 
 * Returns array of violations found.
 */
export function findConstitutionalViolations(text: string): string[] {
  const violations: string[] = []
  
  for (const pattern of PROHIBITED_PATTERNS) {
    const match = text.match(pattern)
    if (match) {
      violations.push(match[0])
    }
  }
  
  return violations
}

/**
 * Check if text contains required disclaimer.
 */
export function hasRequiredDisclaimer(text: string): boolean {
  return text.toLowerCase().includes(MANDATORY_DISCLAIMER.toLowerCase())
}

/**
 * Validate AI response for constitutional compliance.
 */
export function validateAIResponse(text: string): {
  isValid: boolean
  violations: string[]
  hasDisclaimer: boolean
} {
  const violations = findConstitutionalViolations(text)
  const hasDisclaimer = hasRequiredDisclaimer(text)
  
  return {
    isValid: violations.length === 0 && hasDisclaimer,
    violations,
    hasDisclaimer,
  }
}

/**
 * Sanitize text by removing prohibited patterns.
 * 
 * NOTE: This is a fallback. Primary validation should happen on backend.
 */
export function sanitizeText(text: string): string {
  let sanitized = text
  
  for (const pattern of PROHIBITED_PATTERNS) {
    sanitized = sanitized.replace(pattern, '[REMOVED]')
  }
  
  return sanitized
}
```

### 12.2 Constitutional Validation Hook

```typescript
// src/hooks/useConstitutionalValidation.ts

import { useMemo } from 'react'
import { validateAIResponse, sanitizeText } from '@utils/constitutional'

interface ValidationResult {
  content: string
  isValid: boolean
  violations: string[]
  wasModified: boolean
}

/**
 * Hook to validate and optionally sanitize AI-generated content.
 * 
 * CONSTITUTIONAL: Provides client-side validation as defense-in-depth.
 * Primary validation occurs on the backend.
 */
export function useConstitutionalValidation(
  content: string | undefined,
  options?: {
    sanitize?: boolean
    logViolations?: boolean
  }
): ValidationResult | null {
  const { sanitize = false, logViolations = true } = options ?? {}

  return useMemo(() => {
    if (!content) return null

    const validation = validateAIResponse(content)

    if (!validation.isValid && logViolations) {
      console.warn('Constitutional validation failed:', {
        violations: validation.violations,
        hasDisclaimer: validation.hasDisclaimer,
      })
    }

    if (!validation.isValid && sanitize) {
      return {
        content: sanitizeText(content),
        isValid: false,
        violations: validation.violations,
        wasModified: true,
      }
    }

    return {
      content,
      isValid: validation.isValid,
      violations: validation.violations,
      wasModified: false,
    }
  }, [content, sanitize, logViolations])
}
```

### 12.3 Read-Only Signal Display Pattern

```typescript
// src/components/signals/SignalDisplay.tsx

import type { Signal } from '@types/models'
import { DirectionBadge } from './DirectionBadge'
import { FreshnessBadge } from './FreshnessBadge'
import { formatDistanceToNow } from 'date-fns'
import type { FreshnessStatus } from '@types/enums'

interface SignalDisplayProps {
  signal: Signal
  freshness: FreshnessStatus
}

/**
 * Display a signal in read-only format.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - No action buttons (buy/sell)
 * - No confidence/score display
 * - No weight/priority indicators
 * - Pure data display only
 */
export function SignalDisplay({ signal, freshness }: SignalDisplayProps) {
  return (
    <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
      {/* Direction - displayed without bias */}
      <div className="mb-3 flex items-center justify-between">
        <DirectionBadge direction={signal.direction} size="lg" />
        <FreshnessBadge status={freshness} />
      </div>

      {/* Signal metadata - purely informational */}
      <div className="space-y-1 text-sm text-slate-400">
        <div className="flex justify-between">
          <span>Type:</span>
          <span className="text-slate-300">{signal.signal_type}</span>
        </div>
        <div className="flex justify-between">
          <span>Received:</span>
          <span className="text-slate-300">
            {formatDistanceToNow(new Date(signal.received_at), { addSuffix: true })}
          </span>
        </div>
      </div>

      {/* Indicators - raw data only, no interpretation */}
      {Object.keys(signal.indicators).length > 0 && (
        <div className="mt-3 border-t border-slate-700 pt-3">
          <div className="text-xs font-medium uppercase text-slate-500">
            Indicators
          </div>
          <div className="mt-1 grid grid-cols-2 gap-2 text-sm">
            {Object.entries(signal.indicators).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="text-slate-400">{key}:</span>
                <span className="text-slate-300">{String(value)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 
        CONSTITUTIONAL: NO ACTION BUTTONS
        ❌ <Button>Buy</Button>
        ❌ <Button>Sell</Button>
        ❌ <Button>Execute</Button>
      */}
    </div>
  )
}
```

### 12.4 Equal Prominence Layout

```typescript
// src/components/relationships/EqualProminenceGrid.tsx

import type { ReactNode } from 'react'
import { clsx } from 'clsx'

interface EqualProminenceGridProps {
  items: ReactNode[]
  columns?: 1 | 2 | 3 | 4
  className?: string
}

/**
 * Grid layout that gives EQUAL visual prominence to all items.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * - All grid cells have identical size
 * - No item is visually prioritized
 * - Supports responsive layouts while maintaining equality
 */
export function EqualProminenceGrid({ 
  items, 
  columns = 2,
  className 
}: EqualProminenceGridProps) {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  }[columns]

  return (
    <div className={clsx('grid gap-4', gridCols, className)}>
      {items.map((item, index) => (
        <div key={index} className="min-h-0">
          {/* Each cell has equal constraint - no special sizing */}
          {item}
        </div>
      ))}
    </div>
  )
}
```

### 12.5 Audit Trail Display

```typescript
// src/components/common/AuditInfo.tsx

import { Clock, Database } from 'lucide-react'
import { format } from 'date-fns'

interface AuditInfoProps {
  createdAt?: string
  updatedAt?: string
  source?: string
}

/**
 * Display audit information for data provenance.
 * 
 * CONSTITUTIONAL: Provides transparency about data origin and timing.
 * Helps users make informed decisions.
 */
export function AuditInfo({ createdAt, updatedAt, source }: AuditInfoProps) {
  return (
    <div className="flex flex-wrap gap-4 text-xs text-slate-500">
      {createdAt && (
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          <span>
            Created: {format(new Date(createdAt), 'MMM d, yyyy HH:mm')}
          </span>
        </div>
      )}
      {updatedAt && (
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          <span>
            Updated: {format(new Date(updatedAt), 'MMM d, yyyy HH:mm')}
          </span>
        </div>
      )}
      {source && (
        <div className="flex items-center gap-1">
          <Database className="h-3 w-3" />
          <span>Source: {source}</span>
        </div>
      )}
    </div>
  )
}
```

### 12.6 Constitutional Compliance Testing

```typescript
// src/test/constitutional.test.ts

import { describe, it, expect } from 'vitest'
import { 
  findConstitutionalViolations, 
  hasRequiredDisclaimer,
  validateAIResponse 
} from '@utils/constitutional'

describe('Constitutional Validation', () => {
  describe('findConstitutionalViolations', () => {
    it('should detect recommendation language', () => {
      const violations = findConstitutionalViolations('You should buy now')
      expect(violations).toContain('You should')
      expect(violations).toContain('buy now')
    })

    it('should detect aggregation language', () => {
      const violations = findConstitutionalViolations('The overall direction is bullish')
      expect(violations).toContain('overall direction')
    })

    it('should detect confidence language', () => {
      const violations = findConstitutionalViolations('There is 85% confidence this will rise')
      expect(violations.length).toBeGreaterThan(0)
    })

    it('should pass clean descriptive text', () => {
      const violations = findConstitutionalViolations(
        'Chart A shows bullish momentum while Chart B shows bearish divergence.'
      )
      expect(violations).toHaveLength(0)
    })
  })

  describe('hasRequiredDisclaimer', () => {
    it('should detect presence of disclaimer', () => {
      const text = 'Some analysis. The interpretation and any decision is entirely yours.'
      expect(hasRequiredDisclaimer(text)).toBe(true)
    })

    it('should fail when disclaimer is missing', () => {
      const text = 'Some analysis without disclaimer.'
      expect(hasRequiredDisclaimer(text)).toBe(false)
    })
  })

  describe('validateAIResponse', () => {
    it('should validate compliant response', () => {
      const text = 
        'Chart A shows bullish signals. Chart B shows bearish signals. ' +
        'The interpretation and any decision is entirely yours.'
      
      const result = validateAIResponse(text)
      expect(result.isValid).toBe(true)
      expect(result.violations).toHaveLength(0)
      expect(result.hasDisclaimer).toBe(true)
    })

    it('should reject non-compliant response', () => {
      const text = 'You should buy now. 90% probability of success.'
      
      const result = validateAIResponse(text)
      expect(result.isValid).toBe(false)
      expect(result.violations.length).toBeGreaterThan(0)
    })
  })
})
```

---

## 13. Performance & Optimization

### 13.1 Virtual Scrolling for Large Lists

```typescript
// src/components/common/VirtualList.tsx

import { useRef, useState, useEffect, type ReactNode } from 'react'

interface VirtualListProps<T> {
  items: T[]
  itemHeight: number
  renderItem: (item: T, index: number) => ReactNode
  overscan?: number
  className?: string
}

/**
 * Virtualized list for efficient rendering of large datasets.
 * 
 * Used for:
 * - Signal history (potentially thousands)
 * - Chart lists (many per silo)
 * - Conversation history
 */
export function VirtualList<T>({
  items,
  itemHeight,
  renderItem,
  overscan = 5,
  className,
}: VirtualListProps<T>) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [scrollTop, setScrollTop] = useState(0)
  const [containerHeight, setContainerHeight] = useState(0)

  useEffect(() => {
    const container = containerRef.current
    if (!container) return

    const observer = new ResizeObserver(entries => {
      setContainerHeight(entries[0].contentRect.height)
    })
    observer.observe(container)

    return () => observer.disconnect()
  }, [])

  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan)
  const endIndex = Math.min(
    items.length,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan
  )

  const visibleItems = items.slice(startIndex, endIndex)
  const totalHeight = items.length * itemHeight
  const offsetY = startIndex * itemHeight

  return (
    <div
      ref={containerRef}
      className={className}
      style={{ overflow: 'auto', height: '100%' }}
      onScroll={e => setScrollTop(e.currentTarget.scrollTop)}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, index) => (
            <div key={startIndex + index} style={{ height: itemHeight }}>
              {renderItem(item, startIndex + index)}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

### 13.2 Memoization Patterns

```typescript
// src/components/charts/ChartGrid.tsx

import { memo, useMemo } from 'react'
import type { ChartSignalStatus } from '@types/models'
import { ChartSignalDisplay } from './ChartSignalDisplay'
import { EqualProminenceGrid } from '@components/relationships/EqualProminenceGrid'

interface ChartGridProps {
  charts: ChartSignalStatus[]
}

/**
 * Memoized chart grid for performance.
 * 
 * CONSTITUTIONAL: All charts displayed with equal prominence.
 */
export const ChartGrid = memo(function ChartGrid({ charts }: ChartGridProps) {
  // Memoize the rendered items
  const chartItems = useMemo(
    () => charts.map(chart => (
      <ChartSignalDisplay key={chart.chart_id} chart={chart} />
    )),
    [charts]
  )

  return <EqualProminenceGrid items={chartItems} columns={3} />
})
```

```typescript
// src/hooks/useMemoizedRelationships.ts

import { useMemo } from 'react'
import type { RelationshipSummary } from '@types/models'

/**
 * Memoize derived relationship data.
 */
export function useMemoizedRelationships(summary: RelationshipSummary | undefined) {
  return useMemo(() => {
    if (!summary) return null

    const chartsByDirection = {
      BULLISH: summary.charts.filter(
        c => c.latest_signal?.direction === 'BULLISH'
      ),
      BEARISH: summary.charts.filter(
        c => c.latest_signal?.direction === 'BEARISH'
      ),
      NEUTRAL: summary.charts.filter(
        c => c.latest_signal?.direction === 'NEUTRAL'
      ),
      NO_SIGNAL: summary.charts.filter(c => !c.latest_signal),
    }

    const chartsByFreshness = {
      CURRENT: summary.charts.filter(c => c.freshness === 'CURRENT'),
      RECENT: summary.charts.filter(c => c.freshness === 'RECENT'),
      STALE: summary.charts.filter(c => c.freshness === 'STALE'),
      UNAVAILABLE: summary.charts.filter(c => c.freshness === 'UNAVAILABLE'),
    }

    return {
      summary,
      chartsByDirection,
      chartsByFreshness,
      hasContradictions: summary.contradictions.length > 0,
      hasConfirmations: summary.confirmations.length > 0,
    }
  }, [summary])
}
```

### 13.3 Code Splitting

```typescript
// src/pages/routes.tsx

import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Spinner } from '@components/common/Spinner'
import { AppShell } from '@components/layout/AppShell'

// Lazy load pages for code splitting
const HomePage = lazy(() => import('./HomePage'))
const InstrumentsPage = lazy(() => import('./InstrumentsPage'))
const InstrumentDetailPage = lazy(() => import('./InstrumentDetailPage'))
const SiloDetailPage = lazy(() => import('./SiloDetailPage'))
const ChatPage = lazy(() => import('./ChatPage'))
const SettingsPage = lazy(() => import('./SettingsPage'))
const NotFoundPage = lazy(() => import('./NotFoundPage'))

function PageLoader() {
  return (
    <div className="flex min-h-[400px] items-center justify-center">
      <Spinner size="lg" />
    </div>
  )
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<AppShell />}>
        <Route
          index
          element={
            <Suspense fallback={<PageLoader />}>
              <HomePage />
            </Suspense>
          }
        />
        <Route
          path="instruments"
          element={
            <Suspense fallback={<PageLoader />}>
              <InstrumentsPage />
            </Suspense>
          }
        />
        {/* ... other routes ... */}
      </Route>
    </Routes>
  )
}
```

### 13.4 Bundle Optimization

```typescript
// vite.config.ts (extended)

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // Split vendor chunks for better caching
    rollupOptions: {
      output: {
        manualChunks: {
          // Core React vendor chunk
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          // Data fetching vendor chunk
          'vendor-query': ['@tanstack/react-query', 'axios'],
          // UI vendor chunk
          'vendor-ui': ['lucide-react', 'clsx', 'date-fns'],
        },
      },
    },
    // Target modern browsers
    target: 'es2020',
    // Minification settings
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
  },
})
```

---

## 14. Accessibility & Responsiveness

### 14.1 ARIA Implementation

```typescript
// src/components/signals/DirectionBadge.tsx (with ARIA)

import { clsx } from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import type { Direction } from '@types/enums'

interface DirectionBadgeProps {
  direction: Direction
  showLabel?: boolean
  size?: 'sm' | 'md' | 'lg'
}

export function DirectionBadge({ 
  direction, 
  showLabel = true,
  size = 'md' 
}: DirectionBadgeProps) {
  const config = {
    BULLISH: {
      icon: TrendingUp,
      label: 'Bullish',
      className: 'bg-signal-bullish/20 text-signal-bullish border-signal-bullish/40',
      ariaDescription: 'Signal indicates bullish or upward direction',
    },
    BEARISH: {
      icon: TrendingDown,
      label: 'Bearish',
      className: 'bg-signal-bearish/20 text-signal-bearish border-signal-bearish/40',
      ariaDescription: 'Signal indicates bearish or downward direction',
    },
    NEUTRAL: {
      icon: Minus,
      label: 'Neutral',
      className: 'bg-signal-neutral/20 text-signal-neutral border-signal-neutral/40',
      ariaDescription: 'Signal indicates neutral or no clear direction',
    },
  }[direction]

  const Icon = config.icon

  return (
    <span 
      className={clsx(
        'inline-flex items-center rounded-full border font-medium',
        config.className,
        // ... size classes
      )}
      role="status"
      aria-label={`Direction: ${config.label}`}
      aria-description={config.ariaDescription}
    >
      <Icon className="h-4 w-4" aria-hidden="true" />
      {showLabel && config.label}
    </span>
  )
}
```

### 14.2 Keyboard Navigation

```typescript
// src/hooks/useKeyboardNavigation.ts

import { useEffect, useCallback } from 'react'

interface KeyboardNavigationOptions {
  onNext?: () => void
  onPrevious?: () => void
  onSelect?: () => void
  onCancel?: () => void
  enabled?: boolean
}

/**
 * Hook for keyboard navigation in lists and grids.
 */
export function useKeyboardNavigation({
  onNext,
  onPrevious,
  onSelect,
  onCancel,
  enabled = true,
}: KeyboardNavigationOptions) {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    if (!enabled) return

    switch (event.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        event.preventDefault()
        onNext?.()
        break
      case 'ArrowUp':
      case 'ArrowLeft':
        event.preventDefault()
        onPrevious?.()
        break
      case 'Enter':
      case ' ':
        event.preventDefault()
        onSelect?.()
        break
      case 'Escape':
        event.preventDefault()
        onCancel?.()
        break
    }
  }, [enabled, onNext, onPrevious, onSelect, onCancel])

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])
}
```

### 14.3 Responsive Design Breakpoints

```css
/* src/index.css */

@tailwind base;
@tailwind components;
@tailwind utilities;

/* Breakpoint reference:
 * sm:  640px  - Mobile landscape
 * md:  768px  - Tablet portrait
 * lg:  1024px - Tablet landscape / Small desktop
 * xl:  1280px - Desktop
 * 2xl: 1536px - Large desktop
 */

@layer base {
  html {
    @apply antialiased;
  }
  
  body {
    @apply bg-surface-primary text-white;
  }

  /* Focus visible styles for accessibility */
  :focus-visible {
    @apply outline-2 outline-offset-2 outline-accent-primary;
  }

  /* Reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
}

@layer components {
  /* Responsive container */
  .container-responsive {
    @apply mx-auto w-full px-4 sm:px-6 lg:px-8;
    max-width: min(100%, 1440px);
  }

  /* Card with consistent styling */
  .card {
    @apply rounded-lg border border-slate-700 bg-surface-secondary p-4;
  }

  /* Focus ring utility */
  .focus-ring {
    @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-primary focus-visible:ring-offset-2 focus-visible:ring-offset-surface-primary;
  }
}
```

### 14.4 Responsive Component Example

```typescript
// src/components/dashboard/Dashboard.tsx

import { useMediaQuery } from '@hooks/useMediaQuery'
import { ChartGrid } from '@components/charts/ChartGrid'
import { RelationshipSummary } from '@components/relationships/RelationshipSummary'

export function Dashboard() {
  const isDesktop = useMediaQuery('(min-width: 1024px)')
  const isTablet = useMediaQuery('(min-width: 768px)')

  return (
    <div className="space-y-6">
      {/* Responsive layout: stack on mobile, side-by-side on desktop */}
      <div className={clsx(
        'gap-6',
        isDesktop ? 'grid grid-cols-3' : isTablet ? 'grid grid-cols-2' : 'space-y-6'
      )}>
        <div className={isDesktop ? 'col-span-2' : ''}>
          <ChartGrid charts={charts} />
        </div>
        <div>
          <RelationshipSummary siloId={siloId} />
        </div>
      </div>
    </div>
  )
}
```

```typescript
// src/hooks/useMediaQuery.ts

import { useState, useEffect } from 'react'

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia(query)
    setMatches(mediaQuery.matches)

    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches)
    }

    mediaQuery.addEventListener('change', handler)
    return () => mediaQuery.removeEventListener('change', handler)
  }, [query])

  return matches
}
```

---

## 15. Testing Strategy

### 15.1 Testing Pyramid

| Level | Tools | Coverage Target | Focus |
|-------|-------|-----------------|-------|
| Unit | Vitest | 80%+ | Utilities, hooks, isolated components |
| Integration | Vitest + Testing Library | 70%+ | Component interactions |
| E2E | Playwright (future) | Critical paths | User journeys |

### 15.2 Test Setup

```typescript
// src/test/setup.ts

import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeAll, vi } from 'vitest'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock window.matchMedia
beforeAll(() => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  })
})

// Mock ResizeObserver
class ResizeObserverMock {
  observe = vi.fn()
  unobserve = vi.fn()
  disconnect = vi.fn()
}
window.ResizeObserver = ResizeObserverMock
```

### 15.3 Test Utilities

```typescript
// src/test/utils.tsx

import { render, type RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import type { ReactElement, ReactNode } from 'react'

// Create a fresh QueryClient for each test
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: Infinity,
      },
    },
  })
}

interface WrapperProps {
  children: ReactNode
}

function AllProviders({ children }: WrapperProps) {
  const queryClient = createTestQueryClient()
  
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  )
}

function customRender(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options })
}

export * from '@testing-library/react'
export { customRender as render }
```

### 15.4 Component Test Example

```typescript
// src/components/signals/DirectionBadge.test.tsx

import { describe, it, expect } from 'vitest'
import { render, screen } from '@test/utils'
import { DirectionBadge } from './DirectionBadge'

describe('DirectionBadge', () => {
  it('renders bullish direction correctly', () => {
    render(<DirectionBadge direction="BULLISH" />)
    
    expect(screen.getByText('Bullish')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveAttribute(
      'aria-label', 
      'Direction: Bullish'
    )
  })

  it('renders bearish direction correctly', () => {
    render(<DirectionBadge direction="BEARISH" />)
    
    expect(screen.getByText('Bearish')).toBeInTheDocument()
  })

  it('renders neutral direction correctly', () => {
    render(<DirectionBadge direction="NEUTRAL" />)
    
    expect(screen.getByText('Neutral')).toBeInTheDocument()
  })

  it('hides label when showLabel is false', () => {
    render(<DirectionBadge direction="BULLISH" showLabel={false} />)
    
    expect(screen.queryByText('Bullish')).not.toBeInTheDocument()
  })

  /**
   * CONSTITUTIONAL COMPLIANCE TEST
   * Verify that all directions have equal visual treatment.
   */
  it('gives equal visual prominence to all directions', () => {
    const { rerender } = render(<DirectionBadge direction="BULLISH" />)
    const bullishElement = screen.getByRole('status')
    const bullishClasses = bullishElement.className

    rerender(<DirectionBadge direction="BEARISH" />)
    const bearishElement = screen.getByRole('status')
    const bearishClasses = bearishElement.className

    // Both should have similar structural classes (padding, font, border-radius)
    // Only color classes should differ
    expect(bullishClasses).toContain('rounded-full')
    expect(bearishClasses).toContain('rounded-full')
    expect(bullishClasses).toContain('border')
    expect(bearishClasses).toContain('border')
  })
})
```

### 15.5 Hook Test Example

```typescript
// src/hooks/useConstitutionalValidation.test.ts

import { describe, it, expect } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useConstitutionalValidation } from './useConstitutionalValidation'

describe('useConstitutionalValidation', () => {
  it('returns null for undefined content', () => {
    const { result } = renderHook(() => 
      useConstitutionalValidation(undefined)
    )
    
    expect(result.current).toBeNull()
  })

  it('validates compliant content', () => {
    const content = 
      'Chart shows bullish momentum. ' +
      'The interpretation and any decision is entirely yours.'
    
    const { result } = renderHook(() => 
      useConstitutionalValidation(content)
    )
    
    expect(result.current?.isValid).toBe(true)
    expect(result.current?.violations).toHaveLength(0)
  })

  it('detects violations in non-compliant content', () => {
    const content = 'You should buy this stock immediately.'
    
    const { result } = renderHook(() => 
      useConstitutionalValidation(content)
    )
    
    expect(result.current?.isValid).toBe(false)
    expect(result.current?.violations.length).toBeGreaterThan(0)
  })

  it('sanitizes content when option enabled', () => {
    const content = 'I recommend you buy now.'
    
    const { result } = renderHook(() => 
      useConstitutionalValidation(content, { sanitize: true })
    )
    
    expect(result.current?.wasModified).toBe(true)
    expect(result.current?.content).toContain('[REMOVED]')
  })
})
```

---

## 16. Design System

### 16.1 Color Tokens

```css
/* CSS Variables for theming */
:root {
  /* Signal Colors - CONSTITUTIONAL: Equal visual weight */
  --color-signal-bullish: 34 197 94;    /* green-500 */
  --color-signal-bearish: 239 68 68;    /* red-500 */
  --color-signal-neutral: 107 114 128;  /* gray-500 */

  /* Freshness Colors */
  --color-freshness-current: 34 197 94;
  --color-freshness-recent: 234 179 8;
  --color-freshness-stale: 249 115 22;
  --color-freshness-unavailable: 107 114 128;

  /* Surface Colors */
  --color-surface-primary: 15 23 42;    /* slate-900 */
  --color-surface-secondary: 30 41 59;  /* slate-800 */
  --color-surface-tertiary: 51 65 85;   /* slate-700 */

  /* Accent Colors */
  --color-accent-primary: 59 130 246;   /* blue-500 */
  --color-accent-secondary: 139 92 246; /* violet-500 */

  /* Text Colors */
  --color-text-primary: 255 255 255;
  --color-text-secondary: 203 213 225;  /* slate-300 */
  --color-text-tertiary: 148 163 184;   /* slate-400 */
  --color-text-muted: 100 116 139;      /* slate-500 */
}
```

### 16.2 Typography Scale

```css
/* Typography tokens */
:root {
  /* Font Families */
  --font-sans: 'JetBrains Mono', 'SF Mono', ui-monospace, monospace;
  --font-display: 'Space Grotesk', system-ui, sans-serif;

  /* Font Sizes */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

### 16.3 Spacing Scale

```css
/* Spacing tokens (4px base) */
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

### 16.4 Component Variants

```typescript
// src/constants/ui.ts

/**
 * UI Constants following design system.
 */

export const CARD_VARIANTS = {
  default: 'rounded-lg border border-slate-700 bg-surface-secondary',
  elevated: 'rounded-lg border border-slate-600 bg-surface-secondary shadow-lg',
  outlined: 'rounded-lg border-2 border-slate-600 bg-transparent',
} as const

export const BUTTON_VARIANTS = {
  primary: 'bg-accent-primary hover:bg-accent-primary/90 text-white',
  secondary: 'bg-surface-tertiary hover:bg-surface-tertiary/80 text-white',
  ghost: 'hover:bg-surface-tertiary text-slate-300',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
} as const

export const TEXT_VARIANTS = {
  heading: 'font-display font-semibold text-white',
  body: 'font-sans text-slate-300',
  caption: 'font-sans text-sm text-slate-400',
  muted: 'font-sans text-slate-500',
} as const

/**
 * CONSTITUTIONAL: Signal colors have EQUAL visual weight.
 * Saturation and brightness are matched across all directions.
 */
export const SIGNAL_COLORS = {
  BULLISH: {
    bg: 'bg-signal-bullish/20',
    text: 'text-signal-bullish',
    border: 'border-signal-bullish/40',
  },
  BEARISH: {
    bg: 'bg-signal-bearish/20',
    text: 'text-signal-bearish',
    border: 'border-signal-bearish/40',
  },
  NEUTRAL: {
    bg: 'bg-signal-neutral/20',
    text: 'text-signal-neutral',
    border: 'border-signal-neutral/40',
  },
} as const
```

---

## Appendix A: Quick Reference

### A.1 Constitutional Rules Summary

| Rule | ID | Enforcement |
|------|-----|-------------|
| Decision-Support ONLY | CR-001 | No trading buttons, mandatory disclaimer |
| Never Resolve Contradictions | CR-002 | Equal prominence display, no aggregation |
| Descriptive NOT Prescriptive | CR-003 | Language validation, no "should/recommend" |

### A.2 Key File Locations

| Purpose | Path |
|---------|------|
| Types | `src/types/` |
| API Services | `src/services/` |
| Hooks | `src/hooks/` |
| Components | `src/components/` |
| Pages | `src/pages/` |
| Utils | `src/utils/` |
| Tests | `src/test/` |

### A.3 API Base URL

- Development: `http://localhost:8000/api/v1`
- Via Vite Proxy: `/api/v1`

### A.4 Prohibited Patterns Checklist

Before submitting any component:

- [ ] No `<button>Buy</button>` or similar trading actions
- [ ] No `weight`, `score`, `confidence`, `rank` fields displayed
- [ ] No "overall direction" or "net signal" aggregation
- [ ] No "you should", "recommend", "suggest" in UI text
- [ ] Equal visual prominence for all signals
- [ ] Mandatory disclaimer on AI content
- [ ] All contradictions displayed (none hidden)
- [ ] All confirmations displayed (none weighted)

---

**END OF FRONTEND TECHNOLOGY SPECIFICATION**

---

*Document Version: 1.0*  
*Created: 2026-01-03*  
*Classification: Complete Implementation Specification*  
*Compliance: Constitutional Rules CR-001, CR-002, CR-003*

