# CIA-SIE Frontend Build Specification
## Interface Control Document (ICD)

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         DOCUMENT CONTROL                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Document ID:       CIA-SIE-ICD-001                                          ║
║  Version:           1.0.0                                                     ║
║  Classification:    IMPLEMENTATION DIRECTIVE                                  ║
║  Authority:         Gold Standard Specification v2.0.0                        ║
║  Generated:         2026-01-04                                                ║
║  Target System:     CIA-SIE Frontend (React/TypeScript)                       ║
║  Backend Version:   2.3.0 (Audited)                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## PURPOSE

This document provides **complete, unambiguous specifications** for building the CIA-SIE frontend. Every requirement has:

- **Unique ID** for traceability
- **Backend source** (exact endpoint, exact response)
- **Frontend target** (exact component, exact props, exact behavior)
- **Verification criteria** (how to confirm implementation is correct)

**An AI agent (Cursor) should be able to implement the entire frontend from this document alone.**

---

## TABLE OF CONTENTS

1. [Constitutional Framework](#1-constitutional-framework)
2. [Technology Stack Requirements](#2-technology-stack-requirements)
3. [Project Structure](#3-project-structure)
4. [Interface Control Specifications](#4-interface-control-specifications)
5. [Component Build Specifications](#5-component-build-specifications)
6. [TypeScript Type Definitions](#6-typescript-type-definitions)
7. [API Service Layer](#7-api-service-layer)
8. [React Query Hooks](#8-react-query-hooks)
9. [Page Specifications](#9-page-specifications)
10. [State Management](#10-state-management)
11. [Verification Matrix](#11-verification-matrix)

---

# 1. CONSTITUTIONAL FRAMEWORK

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INVIOLABLE CONSTITUTIONAL RULES                           │
│                                                                              │
│  These rules CANNOT be violated under ANY circumstances.                    │
│  Any implementation that violates these rules is REJECTED.                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## CR-001: DECISION-SUPPORT ONLY

| Requirement ID | CR-001 |
|----------------|--------|
| **Statement** | System provides INFORMATION, never recommendations |
| **Frontend Enforcement** | |
| FE-CR-001-A | NO buttons labeled "Buy", "Sell", "Enter", "Exit" |
| FE-CR-001-B | NO text containing "should", "recommend", "suggest", "consider" |
| FE-CR-001-C | NO action prompts implying trading decisions |
| FE-CR-001-D | All AI content displays mandatory disclaimer |

## CR-002: NEVER RESOLVE CONTRADICTIONS

| Requirement ID | CR-002 |
|----------------|--------|
| **Statement** | When charts disagree, show BOTH with EQUAL prominence |
| **Frontend Enforcement** | |
| FE-CR-002-A | Contradiction display uses IDENTICAL styling for both sides |
| FE-CR-002-B | NO visual hierarchy suggesting one side is "correct" |
| FE-CR-002-C | NO aggregation, weighting, or "net" calculations displayed |
| FE-CR-002-D | NO "overall direction" or "consensus" indicators |

## CR-003: DESCRIPTIVE NOT PRESCRIPTIVE

| Requirement ID | CR-003 |
|----------------|--------|
| **Statement** | AI describes what data shows, never what to do |
| **Frontend Enforcement** | |
| FE-CR-003-A | Disclaimer component MUST appear on ALL AI content |
| FE-CR-003-B | Disclaimer text is EXACTLY: "This is a description of what your charts are showing. The interpretation and any decision is entirely yours." |
| FE-CR-003-C | Disclaimer is NOT dismissible, collapsible, or hideable |

---

# 2. TECHNOLOGY STACK REQUIREMENTS

## REQ-TECH: Required Dependencies

| Requirement ID | Package | Version | Purpose |
|----------------|---------|---------|---------|
| REQ-TECH-001 | `react` | ^18.2.0 | UI framework |
| REQ-TECH-002 | `react-dom` | ^18.2.0 | DOM rendering |
| REQ-TECH-003 | `typescript` | ^5.3.0 | Type safety |
| REQ-TECH-004 | `vite` | ^5.0.0 | Build tool |
| REQ-TECH-005 | `tailwindcss` | ^3.4.0 | Styling |
| REQ-TECH-006 | `@tanstack/react-query` | ^5.0.0 | Server state |
| REQ-TECH-007 | `react-router-dom` | ^6.20.0 | Routing |
| REQ-TECH-008 | `axios` | ^1.6.0 | HTTP client |
| REQ-TECH-009 | `clsx` | ^2.0.0 | Class utilities |
| REQ-TECH-010 | `lucide-react` | ^0.300.0 | Icons |

## REQ-TECH-011: package.json

```json
{
  "name": "cia-sie-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.6.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.300.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

## REQ-TECH-012: vite.config.ts

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
      '@pages': path.resolve(__dirname, './src/pages'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@lib': path.resolve(__dirname, './src/lib'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## REQ-TECH-013: tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Surface colors
        'surface-primary': '#0f172a',
        'surface-secondary': '#1e293b',
        'surface-tertiary': '#334155',
        // Accent
        'accent-primary': '#3b82f6',
        'accent-secondary': '#8b5cf6',
        // Signal colors (EQUAL visual weight)
        'signal-bullish': '#22c55e',
        'signal-bearish': '#ef4444',
        'signal-neutral': '#94a3b8',
        // Freshness colors (descriptive only)
        'freshness-current': '#22c55e',
        'freshness-recent': '#f59e0b',
        'freshness-stale': '#ef4444',
        'freshness-unavailable': '#64748b',
      },
      fontFamily: {
        display: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
```

---

# 3. PROJECT STRUCTURE

## REQ-STRUCT-001: Directory Layout

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── postcss.config.js
│
└── src/
    ├── main.tsx                      # Application entry
    ├── App.tsx                       # Root component with providers
    ├── index.css                     # Global styles + Tailwind
    │
    ├── types/                        # TypeScript definitions
    │   ├── index.ts                  # Re-exports
    │   ├── enums.ts                  # All enumerations
    │   ├── models.ts                 # Domain models
    │   └── api.ts                    # API response types
    │
    ├── services/                     # API service layer
    │   ├── index.ts                  # Re-exports
    │   ├── client.ts                 # Axios instance
    │   ├── instruments.ts            # Instrument API
    │   ├── silos.ts                  # Silo API
    │   ├── charts.ts                 # Chart API
    │   ├── signals.ts                # Signal API
    │   ├── relationships.ts          # Relationship API
    │   ├── narratives.ts             # Narrative API
    │   ├── ai.ts                     # AI API
    │   └── chat.ts                   # Chat API
    │
    ├── hooks/                        # React Query hooks
    │   ├── index.ts                  # Re-exports
    │   ├── useInstruments.ts
    │   ├── useSilos.ts
    │   ├── useCharts.ts
    │   ├── useSignals.ts
    │   ├── useRelationships.ts
    │   ├── useNarratives.ts
    │   ├── useAI.ts
    │   └── useChat.ts
    │
    ├── lib/                          # Utilities
    │   ├── queryClient.ts            # React Query config
    │   ├── queryKeys.ts              # Query key factory
    │   └── utils.ts                  # Helper functions
    │
    ├── components/                   # UI components
    │   ├── layout/                   # Layout components
    │   │   ├── AppShell.tsx
    │   │   ├── Header.tsx
    │   │   ├── Sidebar.tsx
    │   │   └── PageHeader.tsx
    │   │
    │   ├── common/                   # Shared components
    │   │   ├── Button.tsx
    │   │   ├── Card.tsx
    │   │   ├── Spinner.tsx
    │   │   ├── EmptyState.tsx
    │   │   ├── ErrorState.tsx
    │   │   └── Disclaimer.tsx        # CONSTITUTIONAL: Mandatory
    │   │
    │   ├── signals/                  # Signal display
    │   │   ├── DirectionBadge.tsx
    │   │   ├── FreshnessBadge.tsx
    │   │   ├── SignalCard.tsx
    │   │   └── SignalList.tsx
    │   │
    │   ├── relationships/            # Contradiction/Confirmation
    │   │   ├── ContradictionPanel.tsx
    │   │   ├── ContradictionCard.tsx
    │   │   ├── ConfirmationPanel.tsx
    │   │   └── ConfirmationCard.tsx
    │   │
    │   ├── narratives/               # AI narratives
    │   │   ├── NarrativeDisplay.tsx
    │   │   └── NarrativeSection.tsx
    │   │
    │   ├── instruments/              # Instrument UI
    │   │   ├── InstrumentCard.tsx
    │   │   ├── InstrumentList.tsx
    │   │   └── InstrumentSelector.tsx
    │   │
    │   ├── silos/                    # Silo UI
    │   │   ├── SiloCard.tsx
    │   │   └── SiloList.tsx
    │   │
    │   ├── charts/                   # Chart UI
    │   │   ├── ChartCard.tsx
    │   │   └── ChartList.tsx
    │   │
    │   └── ai/                       # AI UI
    │       ├── BudgetIndicator.tsx
    │       ├── ChatInterface.tsx
    │       └── ModelSelector.tsx
    │
    └── pages/                        # Route pages
        ├── HomePage.tsx
        ├── InstrumentsPage.tsx
        ├── InstrumentDetailPage.tsx
        ├── SiloDetailPage.tsx
        ├── ChartDetailPage.tsx
        ├── ChatPage.tsx
        ├── SettingsPage.tsx
        └── NotFoundPage.tsx
```

---

# 4. INTERFACE CONTROL SPECIFICATIONS

Each specification maps a backend endpoint to its frontend consumer with complete precision.

---

## ICS-001: Health Check

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Health Check                                                      │
│ ID: ICS-001                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /health                                                    │
│ Auth:         None                                                           │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "status": "healthy",                                                       │
│   "app": "CIA-SIE",                                                          │
│   "version": "2.3.0",                                                        │
│   "environment": "development"                                               │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/client.ts                                         │
│ Hook:         None (used internally)                                         │
│ Component:    Header.tsx (status indicator)                                  │
│                                                                              │
│ Display:                                                                     │
│ - Green dot when status === "healthy"                                        │
│ - Red dot otherwise                                                          │
│ - Tooltip shows version                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-001-A: Backend running → Green status indicator visible                    │
│ V-001-B: Backend stopped → Red status indicator visible                      │
│ V-001-C: Hover tooltip shows "CIA-SIE v2.3.0"                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-002: List Instruments

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: List Instruments                                                  │
│ ID: ICS-002                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/instruments/                                       │
│ Auth:         None                                                           │
│ Query Params: active_only?: boolean                                          │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema (Array):                                                     │
│ [                                                                            │
│   {                                                                          │
│     "instrument_id": "uuid",                                                 │
│     "symbol": "GOLDBEES",                                                    │
│     "display_name": "Gold BEES ETF",                                         │
│     "created_at": "2026-01-01T00:00:00Z",                                    │
│     "updated_at": "2026-01-04T10:00:00Z",                                    │
│     "is_active": true,                                                       │
│     "metadata_json": {}                                                      │
│   }                                                                          │
│ ]                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/instruments.ts → getInstruments()                 │
│ Hook:         src/hooks/useInstruments.ts → useInstruments()                 │
│ Components:                                                                  │
│   - InstrumentsPage.tsx (full list view)                                     │
│   - InstrumentList.tsx (list component)                                      │
│   - InstrumentCard.tsx (individual card)                                     │
│   - InstrumentSelector.tsx (dropdown in header)                              │
│   - Sidebar.tsx (navigation list)                                            │
│                                                                              │
│ Display per Instrument:                                                      │
│   - symbol (large, bold)                                                     │
│   - display_name (subtitle)                                                  │
│   - Active badge if is_active === true                                       │
│   - Click → Navigate to /instruments/{instrument_id}                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-002-A: InstrumentsPage shows all instruments from API                      │
│ V-002-B: Each card shows symbol and display_name                             │
│ V-002-C: Clicking card navigates to detail page                              │
│ V-002-D: Loading spinner shown while fetching                                │
│ V-002-E: Empty state shown when no instruments                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-003: Get Instrument by ID

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Instrument by ID                                              │
│ ID: ICS-003                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/instruments/{instrument_id}                        │
│ Path Param:   instrument_id (UUID)                                           │
│ Response:     200 OK | 404 Not Found                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "instrument_id": "uuid",                                                   │
│   "symbol": "GOLDBEES",                                                      │
│   "display_name": "Gold BEES ETF",                                           │
│   "created_at": "2026-01-01T00:00:00Z",                                      │
│   "updated_at": "2026-01-04T10:00:00Z",                                      │
│   "is_active": true,                                                         │
│   "metadata_json": {}                                                        │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/instruments.ts → getInstrument(id)                │
│ Hook:         src/hooks/useInstruments.ts → useInstrument(id)                │
│ Component:    InstrumentDetailPage.tsx                                       │
│                                                                              │
│ Route:        /instruments/:instrumentId                                     │
│ URL Param:    instrumentId → passed to useInstrument()                       │
│                                                                              │
│ Display:                                                                     │
│   - Page header with symbol and display_name                                 │
│   - List of silos for this instrument (ICS-004)                              │
│   - AI narrative for instrument (ICS-014)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-003-A: Navigate to /instruments/{id} shows instrument header               │
│ V-003-B: Invalid ID shows error state                                        │
│ V-003-C: Loading state shown while fetching                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-004: List Silos by Instrument

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: List Silos by Instrument                                          │
│ ID: ICS-004                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/silos/                                             │
│ Query Params: instrument_id: string (required for filtering)                 │
│               active_only?: boolean                                          │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema (Array):                                                     │
│ [                                                                            │
│   {                                                                          │
│     "silo_id": "uuid",                                                       │
│     "instrument_id": "uuid",                                                 │
│     "silo_name": "Gold BEES Primary",                                        │
│     "heartbeat_enabled": true,                                               │
│     "heartbeat_frequency_min": 15,                                           │
│     "current_threshold_min": 5,                                              │
│     "recent_threshold_min": 30,                                              │
│     "stale_threshold_min": 60,                                               │
│     "created_at": "2026-01-01T00:00:00Z",                                    │
│     "updated_at": "2026-01-04T10:00:00Z",                                    │
│     "is_active": true                                                        │
│   }                                                                          │
│ ]                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/silos.ts → getSilos({ instrument_id })            │
│ Hook:         src/hooks/useSilos.ts → useSilos(instrumentId)                 │
│ Components:                                                                  │
│   - InstrumentDetailPage.tsx (parent)                                        │
│   - SiloList.tsx (list component)                                            │
│   - SiloCard.tsx (individual card)                                           │
│                                                                              │
│ Display per Silo:                                                            │
│   - silo_name (bold)                                                         │
│   - Heartbeat indicator (if heartbeat_enabled)                               │
│   - Chart count (from ICS-005)                                               │
│   - Click → Navigate to /silos/{silo_id}                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-004-A: InstrumentDetailPage shows silos for that instrument                │
│ V-004-B: Each silo card shows silo_name                                      │
│ V-004-C: Clicking card navigates to silo detail                              │
│ V-004-D: Empty state shown when no silos                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-005: List Charts by Silo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: List Charts by Silo                                               │
│ ID: ICS-005                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/charts/                                            │
│ Query Params: silo_id: string (required for filtering)                       │
│               active_only?: boolean                                          │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema (Array):                                                     │
│ [                                                                            │
│   {                                                                          │
│     "chart_id": "uuid",                                                      │
│     "silo_id": "uuid",                                                       │
│     "chart_code": "01A",                                                     │
│     "chart_name": "4H Momentum",                                             │
│     "timeframe": "4H",                                                       │
│     "webhook_id": "unique-webhook-id",                                       │
│     "created_at": "2026-01-01T00:00:00Z",                                    │
│     "updated_at": "2026-01-04T10:00:00Z",                                    │
│     "is_active": true                                                        │
│   }                                                                          │
│ ]                                                                            │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: NO weight field exists. All charts are EQUAL.             │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/charts.ts → getCharts({ silo_id })                │
│ Hook:         src/hooks/useCharts.ts → useCharts(siloId)                     │
│ Components:                                                                  │
│   - SiloDetailPage.tsx (parent)                                              │
│   - ChartList.tsx (list component)                                           │
│   - ChartCard.tsx (individual card)                                          │
│                                                                              │
│ Display per Chart:                                                           │
│   - chart_code (e.g., "01A")                                                 │
│   - chart_name (e.g., "4H Momentum")                                         │
│   - timeframe badge                                                          │
│   - Latest signal direction (from ICS-007)                                   │
│   - Freshness indicator (from ICS-007)                                       │
│   - Click → Navigate to /charts/{chart_id}                                   │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: All charts displayed with EQUAL visual prominence.        │
│    NO size differences. NO ordering by "importance".                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-005-A: SiloDetailPage shows all charts for that silo                       │
│ V-005-B: Each chart card shows code, name, timeframe                         │
│ V-005-C: All chart cards are IDENTICAL size                                  │
│ V-005-D: NO chart is visually emphasized over another                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-006: Get Chart by ID

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Chart by ID                                                   │
│ ID: ICS-006                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/charts/{chart_id}                                  │
│ Path Param:   chart_id (UUID)                                                │
│ Response:     200 OK | 404 Not Found                                         │
│                                                                              │
│ Response Schema: Same as ICS-005 single item                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/charts.ts → getChart(id)                          │
│ Hook:         src/hooks/useCharts.ts → useChart(id)                          │
│ Component:    ChartDetailPage.tsx                                            │
│                                                                              │
│ Route:        /charts/:chartId                                               │
│                                                                              │
│ Display:                                                                     │
│   - Chart header (code, name, timeframe)                                     │
│   - Signal history (ICS-007)                                                 │
│   - Webhook ID for reference                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-006-A: Navigate to /charts/{id} shows chart detail                         │
│ V-006-B: Signal history loads for this chart                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-007: Get Signals by Chart

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Signals by Chart                                              │
│ ID: ICS-007                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/signals/chart/{chart_id}                           │
│ Path Param:   chart_id (UUID)                                                │
│ Query Params: limit?: number (default: 20)                                   │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema (Array):                                                     │
│ [                                                                            │
│   {                                                                          │
│     "signal_id": "uuid",                                                     │
│     "chart_id": "uuid",                                                      │
│     "received_at": "2026-01-04T10:00:00Z",                                   │
│     "signal_timestamp": "2026-01-04T09:59:00Z",                              │
│     "signal_type": "BAR_CLOSE",                                              │
│     "direction": "BULLISH",                                                  │
│     "indicators": { "rsi": 65.5, "macd": 0.5 },                              │
│     "raw_payload": {}                                                        │
│   }                                                                          │
│ ]                                                                            │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: NO confidence or strength field exists.                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/signals.ts → getSignalsByChart(chartId, params)   │
│ Hook:         src/hooks/useSignals.ts → useSignals(chartId)                  │
│ Components:                                                                  │
│   - ChartDetailPage.tsx (parent)                                             │
│   - SignalList.tsx (list component)                                          │
│   - SignalCard.tsx (individual signal)                                       │
│   - DirectionBadge.tsx (direction display)                                   │
│                                                                              │
│ Display per Signal:                                                          │
│   - direction → DirectionBadge component                                     │
│   - signal_type → Badge (HEARTBEAT, STATE_CHANGE, BAR_CLOSE, MANUAL)         │
│   - received_at → Formatted timestamp                                        │
│   - indicators → Expandable JSON view                                        │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: NO visual emphasis on any signal direction.               │
│    Bullish and Bearish have EQUAL visual weight.                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-007-A: ChartDetailPage shows signal history                                │
│ V-007-B: Each signal shows direction, type, timestamp                        │
│ V-007-C: DirectionBadge uses EQUAL visual weight for all directions          │
│ V-007-D: BULLISH uses green, BEARISH uses red, NEUTRAL uses gray             │
│ V-007-E: All direction badges are SAME SIZE                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-008: Get Latest Signal

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Latest Signal for Chart                                       │
│ ID: ICS-008                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/signals/chart/{chart_id}/latest                    │
│ Path Param:   chart_id (UUID)                                                │
│ Response:     200 OK | 404 Not Found (no signals)                            │
│                                                                              │
│ Response Schema: Same as single signal in ICS-007                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/signals.ts → getLatestSignal(chartId)             │
│ Hook:         src/hooks/useSignals.ts → useLatestSignal(chartId)             │
│ Component:    ChartCard.tsx (shows latest signal inline)                     │
│                                                                              │
│ Display:                                                                     │
│   - DirectionBadge with current direction                                    │
│   - FreshnessBadge (calculated from received_at)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-008-A: ChartCard shows latest signal direction                             │
│ V-008-B: FreshnessBadge shows CURRENT/RECENT/STALE correctly                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-009: Webhook Ingestion

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Webhook Signal Ingestion                                          │
│ ID: ICS-009                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     POST /api/v1/webhook                                           │
│ Auth:         Optional (WEBHOOK_SECRET env var)                              │
│ Request Body:                                                                │
│ {                                                                            │
│   "webhook_id": "unique-id",                                                 │
│   "direction": "BULLISH",                                                    │
│   "signal_type": "BAR_CLOSE",                                                │
│   "indicators": { "rsi": 65 }                                                │
│ }                                                                            │
│ Response:     201 Created | 404 Chart Not Found                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ This endpoint is called by TradingView, NOT by the frontend.                 │
│                                                                              │
│ Frontend behavior:                                                           │
│   - React Query will refetch signals automatically (staleTime: 30s)          │
│   - User can manually refresh via refetch button                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-009-A: After webhook POST, frontend shows new signal on refresh            │
│ V-009-B: Manual refresh button triggers refetch                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-010: Get Silo Relationships (Contradictions + Confirmations)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Silo Relationships                                            │
│ ID: ICS-010                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-002                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/relationships/silo/{silo_id}                       │
│ Path Param:   silo_id (UUID)                                                 │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "silo_id": "uuid",                                                         │
│   "contradictions": [                                                        │
│     {                                                                        │
│       "chart_a_id": "uuid",                                                  │
│       "chart_a_name": "4H Momentum",                                         │
│       "chart_a_direction": "BULLISH",                                        │
│       "chart_b_id": "uuid",                                                  │
│       "chart_b_name": "1D Trend",                                            │
│       "chart_b_direction": "BEARISH",                                        │
│       "detected_at": "2026-01-04T10:00:00Z"                                  │
│     }                                                                        │
│   ],                                                                         │
│   "confirmations": [                                                         │
│     {                                                                        │
│       "direction": "BULLISH",                                                │
│       "charts": [                                                            │
│         { "chart_id": "uuid", "chart_name": "4H RSI" },                      │
│         { "chart_id": "uuid", "chart_name": "4H MACD" }                      │
│       ],                                                                     │
│       "count": 2                                                             │
│     }                                                                        │
│   ]                                                                          │
│ }                                                                            │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: Backend EXPOSES contradictions, NEVER resolves them.      │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/relationships.ts → getRelationships(siloId)       │
│ Hook:         src/hooks/useRelationships.ts → useRelationships(siloId)       │
│ Components:                                                                  │
│   - SiloDetailPage.tsx (parent)                                              │
│   - ContradictionPanel.tsx (container)                                       │
│   - ContradictionCard.tsx (single contradiction)                             │
│   - ConfirmationPanel.tsx (container)                                        │
│   - ConfirmationCard.tsx (single confirmation)                               │
│                                                                              │
│ ⚠️ CONSTITUTIONAL DISPLAY REQUIREMENTS:                                      │
│                                                                              │
│ ContradictionCard Layout:                                                    │
│ ┌───────────────────────────────────────────────────────────────┐           │
│ │  ┌─────────────┐      vs      ┌─────────────┐                │           │
│ │  │  Chart A    │              │  Chart B    │                │           │
│ │  │  4H Momentum│              │  1D Trend   │                │           │
│ │  │  [BULLISH]  │              │  [BEARISH]  │                │           │
│ │  └─────────────┘              └─────────────┘                │           │
│ │       ↑ EQUAL SIZE ↑               ↑ EQUAL SIZE ↑            │           │
│ └───────────────────────────────────────────────────────────────┘           │
│                                                                              │
│ MANDATORY:                                                                   │
│   - Both sides use IDENTICAL CSS classes                                     │
│   - Both sides have IDENTICAL dimensions                                     │
│   - NO visual indicator of "which is correct"                                │
│   - NO "winner" or "majority" indication                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-010-A: SiloDetailPage shows ContradictionPanel                             │
│ V-010-B: Each contradiction shows BOTH charts side-by-side                   │
│ V-010-C: Both sides of contradiction are PIXEL-IDENTICAL in size             │
│ V-010-D: NO text like "net direction" or "overall"                           │
│ V-010-E: Confirmations show grouped charts with same direction               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-011: Get Contradictions Only

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Contradictions for Silo                                       │
│ ID: ICS-011                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/relationships/contradictions/silo/{silo_id}        │
│ Path Param:   silo_id (UUID)                                                 │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "contradictions": [...],  // Same as ICS-010                               │
│   "count": 2                                                                 │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/relationships.ts → getContradictions(siloId)      │
│ Hook:         src/hooks/useRelationships.ts → useContradictions(siloId)      │
│ Component:    ContradictionPanel.tsx (can use this for focused view)         │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-011-A: Hook returns only contradictions                                    │
│ V-011-B: Count matches array length                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-012: Get Instrument Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Instrument Relationships                                      │
│ ID: ICS-012                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/relationships/instrument/{instrument_id}           │
│ Path Param:   instrument_id (UUID)                                           │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "instrument_id": "uuid",                                                   │
│   "silos": [                                                                 │
│     {                                                                        │
│       "silo_id": "uuid",                                                     │
│       "silo_name": "Primary",                                                │
│       "contradictions": [...],                                               │
│       "confirmations": [...]                                                 │
│     }                                                                        │
│   ]                                                                          │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      relationships.ts → getInstrumentRelationships(instrumentId)    │
│ Hook:         useRelationships.ts → useInstrumentRelationships(instrumentId) │
│ Component:    InstrumentDetailPage.tsx (overview of all silos' relationships)│
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-012-A: InstrumentDetailPage can show cross-silo relationship summary       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-013: Generate Silo Narrative

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Generate AI Narrative for Silo                                    │
│ ID: ICS-013                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-001, CR-003                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/narratives/silo/{silo_id}                          │
│ Path Param:   silo_id (UUID)                                                 │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "silo_id": "uuid",                                                         │
│   "narrative": "Description of current signal states...",                    │
│   "generated_at": "2026-01-04T10:00:00Z",                                    │
│   "model_used": "claude-3-5-haiku-latest",                                   │
│   "disclaimer": "This is a description of what your charts are showing..."   │
│ }                                                                            │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: Response is VALIDATED by ResponseValidator.               │
│    Contains NO prescriptive language. Includes MANDATORY disclaimer.         │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/narratives.ts → getNarrative(siloId)              │
│ Hook:         src/hooks/useNarratives.ts → useNarrative(siloId)              │
│ Components:                                                                  │
│   - SiloDetailPage.tsx (parent)                                              │
│   - NarrativeDisplay.tsx (narrative container)                               │
│   - Disclaimer.tsx (MANDATORY disclaimer display)                            │
│                                                                              │
│ Display:                                                                     │
│ ┌───────────────────────────────────────────────────────────────┐           │
│ │  📄 Signal Narrative                                          │           │
│ │  ───────────────────────────────────────────────────         │           │
│ │  [AI-generated narrative text here...]                        │           │
│ │                                                               │           │
│ │  ┌─────────────────────────────────────────────────────────┐ │           │
│ │  │ ℹ️ This is a description of what your charts are        │ │           │
│ │  │    showing. The interpretation and any decision is      │ │           │
│ │  │    entirely yours.                                      │ │           │
│ │  └─────────────────────────────────────────────────────────┘ │           │
│ └───────────────────────────────────────────────────────────────┘           │
│                                                                              │
│ ⚠️ MANDATORY: Disclaimer component MUST be rendered.                         │
│    Disclaimer is NOT dismissible, collapsible, or hideable.                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-013-A: SiloDetailPage shows NarrativeDisplay                               │
│ V-013-B: Disclaimer component is ALWAYS visible                              │
│ V-013-C: Disclaimer text is EXACTLY as specified                             │
│ V-013-D: NO close button on disclaimer                                       │
│ V-013-E: NO collapse/expand on disclaimer                                    │
│ V-013-F: Narrative text does NOT contain "should", "recommend", "suggest"    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-014: Get Plain Text Narrative

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Plain Text Narrative                                          │
│ ID: ICS-014                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/narratives/silo/{silo_id}/plain                    │
│ Path Param:   silo_id (UUID)                                                 │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "text": "Plain text narrative...",                                         │
│   "generated_at": "2026-01-04T10:00:00Z"                                     │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/narratives.ts → getPlainNarrative(siloId)         │
│ Hook:         src/hooks/useNarratives.ts → usePlainNarrative(siloId)         │
│ Component:    Used for copy-to-clipboard functionality                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-014-A: Copy button copies plain text version                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-015: Get AI Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Available AI Models                                           │
│ ID: ICS-015                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/ai/models                                          │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "models": [                                                                │
│     {                                                                        │
│       "tier": "HAIKU",                                                       │
│       "model_id": "claude-3-5-haiku-latest",                                 │
│       "display_name": "Claude 3.5 Haiku",                                    │
│       "input_cost_per_1k": 0.00025,                                          │
│       "output_cost_per_1k": 0.00125                                          │
│     },                                                                       │
│     ...                                                                      │
│   ],                                                                         │
│   "default_model": "claude-3-5-haiku-latest",                                │
│   "budget_remaining": 45.50                                                  │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/ai.ts → getModels()                               │
│ Hook:         src/hooks/useAI.ts → useModels()                               │
│ Components:                                                                  │
│   - ModelSelector.tsx (dropdown for chat)                                    │
│   - SettingsPage.tsx (model configuration)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-015-A: ModelSelector shows all available models                            │
│ V-015-B: Default model is pre-selected                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-016: Get AI Usage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get AI Usage Statistics                                           │
│ ID: ICS-016                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/ai/usage                                           │
│ Query Params: period?: "daily" | "weekly" | "monthly"                        │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "period": "daily",                                                         │
│   "input_tokens": 12500,                                                     │
│   "output_tokens": 8500,                                                     │
│   "total_cost": 2.35,                                                        │
│   "requests_count": 45,                                                      │
│   "model_breakdown": {                                                       │
│     "HAIKU": { "requests": 40, "cost": 1.85 },                               │
│     "SONNET": { "requests": 5, "cost": 0.50 }                                │
│   }                                                                          │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/ai.ts → getUsage(period)                          │
│ Hook:         src/hooks/useAI.ts → useUsage(period)                          │
│ Component:    SettingsPage.tsx (usage dashboard)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-016-A: SettingsPage shows usage statistics                                 │
│ V-016-B: Period selector changes displayed data                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-017: Get AI Budget

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get AI Budget Status                                              │
│ ID: ICS-017                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/ai/budget                                          │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "limit": 50.00,                                                            │
│   "used": 4.50,                                                              │
│   "remaining": 45.50,                                                        │
│   "percentage_used": 9.0,                                                    │
│   "alert_threshold": 80,                                                     │
│   "alert_triggered": false                                                   │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/ai.ts → getBudget()                               │
│ Hook:         src/hooks/useAI.ts → useBudget()                               │
│ Components:                                                                  │
│   - BudgetIndicator.tsx (header indicator)                                   │
│   - SettingsPage.tsx (detailed view)                                         │
│                                                                              │
│ Display:                                                                     │
│   - Progress bar showing percentage_used                                     │
│   - Color: green (<50%), yellow (50-80%), red (>80%)                         │
│   - Warning banner if alert_triggered === true                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-017-A: Header shows BudgetIndicator                                        │
│ V-017-B: Progress bar reflects percentage_used                               │
│ V-017-C: Color changes based on threshold                                    │
│ V-017-D: Warning shown when alert_triggered                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-018: Chat with AI

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Chat with AI                                                      │
│ ID: ICS-018                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-001, CR-003                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     POST /api/v1/chat/{scrip_id}                                   │
│ Path Param:   scrip_id (instrument symbol, e.g., "GOLDBEES")                 │
│ Request Body:                                                                │
│ {                                                                            │
│   "message": "What does the current RSI indicate?",                          │
│   "model": "claude-3-5-haiku-latest"                                         │
│ }                                                                            │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "response": "The RSI is currently at 65, which is above the...",           │
│   "conversation_id": "uuid",                                                 │
│   "model_used": "claude-3-5-haiku-latest",                                   │
│   "tokens_used": 450,                                                        │
│   "cost": 0.015                                                              │
│ }                                                                            │
│                                                                              │
│ ⚠️ CONSTITUTIONAL: Response is VALIDATED. No prescriptive language.          │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/chat.ts → sendMessage(scripId, message, model)    │
│ Hook:         src/hooks/useChat.ts → useSendMessage()                        │
│ Components:                                                                  │
│   - ChatPage.tsx (parent)                                                    │
│   - ChatInterface.tsx (main chat UI)                                         │
│   - Disclaimer.tsx (MANDATORY on all AI responses)                           │
│                                                                              │
│ Display:                                                                     │
│ ┌───────────────────────────────────────────────────────────────┐           │
│ │  User: What does the current RSI indicate?                    │           │
│ │                                                               │           │
│ │  AI: The RSI is currently at 65...                            │           │
│ │  ┌─────────────────────────────────────────────────────────┐ │           │
│ │  │ ℹ️ This is a description... [MANDATORY DISCLAIMER]      │ │           │
│ │  └─────────────────────────────────────────────────────────┘ │           │
│ │                                                               │           │
│ │  [Type your message...]                          [Send]       │           │
│ └───────────────────────────────────────────────────────────────┘           │
│                                                                              │
│ ⚠️ MANDATORY: Disclaimer appears after EVERY AI response.                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-018-A: ChatPage shows ChatInterface                                        │
│ V-018-B: User message appears in chat                                        │
│ V-018-C: AI response appears with disclaimer                                 │
│ V-018-D: Disclaimer is NOT dismissible                                       │
│ V-018-E: Response does NOT contain "should", "recommend", "suggest"          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICS-019: Get Chat History

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INTERFACE: Get Chat History                                                  │
│ ID: ICS-019                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BACKEND                                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Endpoint:     GET /api/v1/chat/{scrip_id}/history                            │
│ Path Param:   scrip_id (instrument symbol)                                   │
│ Query Params: limit?: number                                                 │
│ Response:     200 OK                                                         │
│                                                                              │
│ Response Schema:                                                             │
│ {                                                                            │
│   "scrip_id": "GOLDBEES",                                                    │
│   "conversations": [                                                         │
│     {                                                                        │
│       "conversation_id": "uuid",                                             │
│       "messages": [                                                          │
│         { "role": "user", "content": "..." },                                │
│         { "role": "assistant", "content": "..." }                            │
│       ],                                                                     │
│       "created_at": "2026-01-04T10:00:00Z",                                  │
│       "total_tokens": 850,                                                   │
│       "total_cost": 0.03                                                     │
│     }                                                                        │
│   ]                                                                          │
│ }                                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ FRONTEND                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service:      src/services/chat.ts → getHistory(scripId, limit)              │
│ Hook:         src/hooks/useChat.ts → useHistory(scripId)                     │
│ Component:    ChatInterface.tsx (loads previous conversations)               │
├─────────────────────────────────────────────────────────────────────────────┤
│ VERIFICATION                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ V-019-A: ChatInterface loads previous messages on mount                      │
│ V-019-B: Older conversations are scrollable                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 5. COMPONENT BUILD SPECIFICATIONS

---

## CBS-001: DirectionBadge

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT: DirectionBadge                                                    │
│ ID: CBS-001                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-002 (Equal Visual Weight)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ FILE: src/components/signals/DirectionBadge.tsx                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ PROPS:                                                                       │
│   direction: Direction (required)                                            │
│   showLabel?: boolean (default: true)                                        │
│   size?: 'sm' | 'md' | 'lg' (default: 'md')                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BEHAVIOR:                                                                    │
│   - Displays direction with icon and optional label                          │
│   - BULLISH: TrendingUp icon, green color                                    │
│   - BEARISH: TrendingDown icon, red color                                    │
│   - NEUTRAL: Minus icon, gray color                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ CONSTITUTIONAL REQUIREMENTS:                                                 │
│   ✓ All three directions use IDENTICAL layout structure                      │
│   ✓ All three directions use SAME font size                                  │
│   ✓ All three directions use SAME padding                                    │
│   ✓ All three directions use SAME icon size                                  │
│   ✓ Color is the ONLY differentiator (semantic, not hierarchical)            │
├─────────────────────────────────────────────────────────────────────────────┤
│ IMPLEMENTATION:                                                              │
├─────────────────────────────────────────────────────────────────────────────┘

```typescript
import { clsx } from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import type { Direction } from '@/types/enums'

interface DirectionBadgeProps {
  direction: Direction
  showLabel?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const CONFIG = {
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
} as const

const SIZE_CLASSES = {
  sm: { badge: 'px-2 py-0.5 text-xs gap-1', icon: 'h-3 w-3' },
  md: { badge: 'px-3 py-1 text-sm gap-1.5', icon: 'h-4 w-4' },
  lg: { badge: 'px-4 py-1.5 text-base gap-2', icon: 'h-5 w-5' },
} as const

export function DirectionBadge({
  direction,
  showLabel = true,
  size = 'md',
}: DirectionBadgeProps) {
  const config = CONFIG[direction]
  const sizeConfig = SIZE_CLASSES[size]
  const Icon = config.icon

  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full border font-medium',
        config.className,
        sizeConfig.badge
      )}
    >
      <Icon className={sizeConfig.icon} />
      {showLabel && config.label}
    </span>
  )
}
```

---

## CBS-002: FreshnessBadge

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT: FreshnessBadge                                                    │
│ ID: CBS-002                                                                  │
│ CONSTITUTIONAL NOTE: Freshness is DESCRIPTIVE only                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ FILE: src/components/signals/FreshnessBadge.tsx                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ PROPS:                                                                       │
│   status: FreshnessStatus (required)                                         │
│   showLabel?: boolean (default: true)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ BEHAVIOR:                                                                    │
│   - CURRENT: Clock icon, green                                               │
│   - RECENT: Clock icon, yellow                                               │
│   - STALE: AlertTriangle icon, red                                           │
│   - UNAVAILABLE: HelpCircle icon, gray                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ CONSTITUTIONAL REQUIREMENTS:                                                 │
│   ✓ Freshness does NOT suppress or invalidate data                           │
│   ✓ Freshness is informational only                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ IMPLEMENTATION:                                                              │
├─────────────────────────────────────────────────────────────────────────────┘

```typescript
import { clsx } from 'clsx'
import { Clock, AlertTriangle, HelpCircle } from 'lucide-react'
import type { FreshnessStatus } from '@/types/enums'

interface FreshnessBadgeProps {
  status: FreshnessStatus
  showLabel?: boolean
}

const CONFIG = {
  CURRENT: { icon: Clock, label: 'Current', className: 'text-freshness-current' },
  RECENT: { icon: Clock, label: 'Recent', className: 'text-freshness-recent' },
  STALE: { icon: AlertTriangle, label: 'Stale', className: 'text-freshness-stale' },
  UNAVAILABLE: { icon: HelpCircle, label: 'No Data', className: 'text-freshness-unavailable' },
} as const

export function FreshnessBadge({ status, showLabel = true }: FreshnessBadgeProps) {
  const config = CONFIG[status]
  const Icon = config.icon

  return (
    <span className={clsx('inline-flex items-center gap-1 text-sm', config.className)}>
      <Icon className="h-4 w-4" />
      {showLabel && config.label}
    </span>
  )
}
```

---

## CBS-003: Disclaimer (CONSTITUTIONAL CRITICAL)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT: Disclaimer                                                        │
│ ID: CBS-003                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-001, CR-003                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ FILE: src/components/common/Disclaimer.tsx                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ PROPS:                                                                       │
│   variant?: 'inline' | 'block' (default: 'block')                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ BEHAVIOR:                                                                    │
│   - Displays MANDATORY disclaimer text                                       │
│   - Text is HARDCODED (not configurable)                                     │
│   - NO dismiss button                                                        │
│   - NO collapse/expand                                                       │
│   - NO hide functionality                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ MANDATORY TEXT (EXACT):                                                      │
│   "This is a description of what your charts are showing.                    │
│    The interpretation and any decision is entirely yours."                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ CONSTITUTIONAL REQUIREMENTS:                                                 │
│   ✓ Text is NOT editable at runtime                                          │
│   ✓ Component has NO close/dismiss props                                     │
│   ✓ Component has NO collapse props                                          │
│   ✓ Must be used on ALL AI-generated content                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ IMPLEMENTATION:                                                              │
├─────────────────────────────────────────────────────────────────────────────┘

```typescript
import { Info } from 'lucide-react'

interface DisclaimerProps {
  variant?: 'inline' | 'block'
}

// CONSTITUTIONAL: This text is HARDCODED and CANNOT be changed
const DISCLAIMER_TEXT =
  'This is a description of what your charts are showing. The interpretation and any decision is entirely yours.'

export function Disclaimer({ variant = 'block' }: DisclaimerProps) {
  if (variant === 'inline') {
    return <span className="text-sm italic text-slate-400">{DISCLAIMER_TEXT}</span>
  }

  return (
    <div className="mt-4 rounded-lg border border-slate-600 bg-slate-800/50 p-4">
      <div className="flex items-start gap-3">
        <Info className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" />
        <p className="text-sm italic text-slate-300">{DISCLAIMER_TEXT}</p>
      </div>
    </div>
  )
}
```

---

## CBS-004: ContradictionCard (CONSTITUTIONAL CRITICAL)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT: ContradictionCard                                                 │
│ ID: CBS-004                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-002 (Never Resolve Contradictions)               │
├─────────────────────────────────────────────────────────────────────────────┤
│ FILE: src/components/relationships/ContradictionCard.tsx                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ PROPS:                                                                       │
│   contradiction: Contradiction (required)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYOUT:                                                                      │
│   - CSS Grid with 3 columns: [1fr, auto, 1fr]                                │
│   - Left: Chart A (EQUAL SIZE)                                               │
│   - Center: "vs" separator (neutral)                                         │
│   - Right: Chart B (EQUAL SIZE)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ CONSTITUTIONAL REQUIREMENTS:                                                 │
│   ✓ Grid columns MUST be [1fr, auto, 1fr] (equal sizing)                     │
│   ✓ Chart A and Chart B use IDENTICAL CSS classes                            │
│   ✓ NO visual indicator of "winner" or "correct" side                        │
│   ✓ Center separator is NEUTRAL (no directional indicator)                   │
│   ✓ NO aggregation or resolution text                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ IMPLEMENTATION:                                                              │
├─────────────────────────────────────────────────────────────────────────────┘

```typescript
import type { Contradiction } from '@/types/models'
import { DirectionBadge } from '@/components/signals/DirectionBadge'
import { ArrowLeftRight } from 'lucide-react'

interface ContradictionCardProps {
  contradiction: Contradiction
}

export function ContradictionCard({ contradiction }: ContradictionCardProps) {
  // CONSTITUTIONAL: Both sides use IDENTICAL styling
  const sideClassName = 'rounded-lg bg-surface-secondary p-3 text-center'

  return (
    <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-4">
      {/* CONSTITUTIONAL: Grid ensures EQUAL sizing */}
      <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">
        {/* Chart A */}
        <div className={sideClassName}>
          <div className="mb-2 text-sm text-slate-400">{contradiction.chart_a_name}</div>
          <DirectionBadge direction={contradiction.chart_a_direction} size="lg" />
        </div>

        {/* Neutral Separator */}
        <div className="flex flex-col items-center gap-1">
          <ArrowLeftRight className="h-5 w-5 text-slate-500" />
          <span className="text-xs text-slate-500">vs</span>
        </div>

        {/* Chart B - IDENTICAL to Chart A */}
        <div className={sideClassName}>
          <div className="mb-2 text-sm text-slate-400">{contradiction.chart_b_name}</div>
          <DirectionBadge direction={contradiction.chart_b_direction} size="lg" />
        </div>
      </div>
    </div>
  )
}
```

---

## CBS-005: ContradictionPanel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT: ContradictionPanel                                                │
│ ID: CBS-005                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ FILE: src/components/relationships/ContradictionPanel.tsx                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ PROPS:                                                                       │
│   contradictions: Contradiction[] (required)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ IMPLEMENTATION:                                                              │
├─────────────────────────────────────────────────────────────────────────────┘

```typescript
import type { Contradiction } from '@/types/models'
import { ContradictionCard } from './ContradictionCard'
import { AlertTriangle } from 'lucide-react'

interface ContradictionPanelProps {
  contradictions: Contradiction[]
}

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

      <div className="grid gap-4">
        {contradictions.map((c) => (
          <ContradictionCard
            key={`${c.chart_a_id}-${c.chart_b_id}`}
            contradiction={c}
          />
        ))}
      </div>
    </div>
  )
}
```

---

## CBS-006: NarrativeDisplay

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPONENT: NarrativeDisplay                                                  │
│ ID: CBS-006                                                                  │
│ CONSTITUTIONAL CRITICAL: CR-001, CR-003                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ FILE: src/components/narratives/NarrativeDisplay.tsx                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ PROPS:                                                                       │
│   narrative: NarrativeResponse (required)                                    │
│   isLoading?: boolean                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ CONSTITUTIONAL REQUIREMENTS:                                                 │
│   ✓ Disclaimer component MUST be rendered                                    │
│   ✓ Disclaimer is ALWAYS visible (not conditional)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ IMPLEMENTATION:                                                              │
├─────────────────────────────────────────────────────────────────────────────┘

```typescript
import type { NarrativeResponse } from '@/types/api'
import { Disclaimer } from '@/components/common/Disclaimer'
import { Spinner } from '@/components/common/Spinner'
import { FileText } from 'lucide-react'

interface NarrativeDisplayProps {
  narrative?: NarrativeResponse
  isLoading?: boolean
}

export function NarrativeDisplay({ narrative, isLoading }: NarrativeDisplayProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!narrative) {
    return null
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <FileText className="h-5 w-5 text-accent-primary" />
        <h3 className="font-display text-lg font-semibold">Signal Narrative</h3>
      </div>

      <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
        <p className="whitespace-pre-wrap text-slate-300">{narrative.narrative}</p>
      </div>

      {/* CONSTITUTIONAL: Disclaimer is MANDATORY and ALWAYS rendered */}
      <Disclaimer />
    </div>
  )
}
```

---

# 6. TYPESCRIPT TYPE DEFINITIONS

## File: src/types/enums.ts

```typescript
// ============================================================================
// ENUMERATIONS
// ============================================================================

export type Direction = 'BULLISH' | 'BEARISH' | 'NEUTRAL'

export type SignalType = 'HEARTBEAT' | 'STATE_CHANGE' | 'BAR_CLOSE' | 'MANUAL'

export type FreshnessStatus = 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'

export type BasketType = 'LOGICAL' | 'HIERARCHICAL' | 'CONTEXTUAL' | 'CUSTOM'

export type ModelTier = 'HAIKU' | 'SONNET' | 'OPUS'

export type ValidationStatus = 'VALID' | 'INVALID' | 'REMEDIATED'
```

## File: src/types/models.ts

```typescript
import type { Direction, SignalType, FreshnessStatus, BasketType } from './enums'

// ============================================================================
// DOMAIN MODELS
// ============================================================================

export interface Instrument {
  instrument_id: string
  symbol: string
  display_name: string
  created_at: string
  updated_at: string
  is_active: boolean
  metadata_json: Record<string, unknown>
}

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
  // CONSTITUTIONAL: NO weight field
}

export interface Signal {
  signal_id: string
  chart_id: string
  received_at: string
  signal_timestamp: string
  signal_type: SignalType
  direction: Direction
  indicators: Record<string, number | string>
  raw_payload: Record<string, unknown>
  // CONSTITUTIONAL: NO confidence field
  // CONSTITUTIONAL: NO strength field
}

export interface Contradiction {
  chart_a_id: string
  chart_a_name: string
  chart_a_direction: Direction
  chart_b_id: string
  chart_b_name: string
  chart_b_direction: Direction
  detected_at: string
}

export interface Confirmation {
  direction: Direction
  charts: Array<{ chart_id: string; chart_name: string }>
  count: number
}

export interface RelationshipSummary {
  silo_id: string
  contradictions: Contradiction[]
  confirmations: Confirmation[]
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface AIModel {
  tier: string
  model_id: string
  display_name: string
  input_cost_per_1k: number
  output_cost_per_1k: number
}
```

## File: src/types/api.ts

```typescript
import type {
  Instrument,
  Silo,
  Chart,
  Signal,
  Contradiction,
  Confirmation,
  ChatMessage,
  AIModel,
} from './models'

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export interface HealthResponse {
  status: 'healthy' | 'unhealthy'
  app: string
  version: string
  environment: string
}

export interface NarrativeResponse {
  silo_id: string
  narrative: string
  generated_at: string
  model_used: string
  disclaimer: string
}

export interface PlainNarrativeResponse {
  text: string
  generated_at: string
}

export interface RelationshipResponse {
  silo_id: string
  contradictions: Contradiction[]
  confirmations: Confirmation[]
}

export interface ContradictionsResponse {
  contradictions: Contradiction[]
  count: number
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

export interface AIUsageResponse {
  period: 'daily' | 'weekly' | 'monthly'
  input_tokens: number
  output_tokens: number
  total_cost: number
  requests_count: number
  model_breakdown: Record<string, { requests: number; cost: number }>
}

export interface ChatResponse {
  response: string
  conversation_id: string
  model_used: string
  tokens_used: number
  cost: number
}

export interface ChatHistoryResponse {
  scrip_id: string
  conversations: Array<{
    conversation_id: string
    messages: ChatMessage[]
    created_at: string
    total_tokens: number
    total_cost: number
  }>
}

// ============================================================================
// QUERY PARAMETER TYPES
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

export interface UsageParams {
  period?: 'daily' | 'weekly' | 'monthly'
}
```

---

# 7. API SERVICE LAYER

## File: src/services/client.ts

```typescript
import axios from 'axios'

export const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Helper to extract data from response
export async function apiRequest<T>(promise: Promise<{ data: T }>): Promise<T> {
  const response = await promise
  return response.data
}
```

## File: src/services/instruments.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { Instrument } from '@/types/models'
import type { InstrumentListParams } from '@/types/api'

const PATH = '/instruments'

export async function getInstruments(params?: InstrumentListParams): Promise<Instrument[]> {
  return apiRequest(apiClient.get(`${PATH}/`, { params }))
}

export async function getInstrument(id: string): Promise<Instrument> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}

export async function getInstrumentBySymbol(symbol: string): Promise<Instrument> {
  return apiRequest(apiClient.get(`${PATH}/symbol/${symbol}`))
}
```

## File: src/services/silos.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { Silo } from '@/types/models'
import type { SiloListParams } from '@/types/api'

const PATH = '/silos'

export async function getSilos(params?: SiloListParams): Promise<Silo[]> {
  return apiRequest(apiClient.get(`${PATH}/`, { params }))
}

export async function getSilo(id: string): Promise<Silo> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}
```

## File: src/services/charts.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { Chart } from '@/types/models'
import type { ChartListParams } from '@/types/api'

const PATH = '/charts'

export async function getCharts(params?: ChartListParams): Promise<Chart[]> {
  return apiRequest(apiClient.get(`${PATH}/`, { params }))
}

export async function getChart(id: string): Promise<Chart> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}
```

## File: src/services/signals.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { Signal } from '@/types/models'
import type { SignalListParams } from '@/types/api'

const PATH = '/signals'

export async function getSignalsByChart(
  chartId: string,
  params?: SignalListParams
): Promise<Signal[]> {
  return apiRequest(apiClient.get(`${PATH}/chart/${chartId}`, { params }))
}

export async function getLatestSignal(chartId: string): Promise<Signal> {
  return apiRequest(apiClient.get(`${PATH}/chart/${chartId}/latest`))
}
```

## File: src/services/relationships.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { RelationshipResponse, ContradictionsResponse } from '@/types/api'

const PATH = '/relationships'

export async function getRelationships(siloId: string): Promise<RelationshipResponse> {
  return apiRequest(apiClient.get(`${PATH}/silo/${siloId}`))
}

export async function getContradictions(siloId: string): Promise<ContradictionsResponse> {
  return apiRequest(apiClient.get(`${PATH}/contradictions/silo/${siloId}`))
}

export async function getInstrumentRelationships(
  instrumentId: string
): Promise<RelationshipResponse> {
  return apiRequest(apiClient.get(`${PATH}/instrument/${instrumentId}`))
}
```

## File: src/services/narratives.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { NarrativeResponse, PlainNarrativeResponse } from '@/types/api'

const PATH = '/narratives'

export async function getNarrative(siloId: string): Promise<NarrativeResponse> {
  return apiRequest(apiClient.get(`${PATH}/silo/${siloId}`))
}

export async function getPlainNarrative(siloId: string): Promise<PlainNarrativeResponse> {
  return apiRequest(apiClient.get(`${PATH}/silo/${siloId}/plain`))
}
```

## File: src/services/ai.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { AIModelsResponse, AIBudgetResponse, AIUsageResponse, UsageParams } from '@/types/api'

const PATH = '/ai'

export async function getModels(): Promise<AIModelsResponse> {
  return apiRequest(apiClient.get(`${PATH}/models`))
}

export async function getBudget(): Promise<AIBudgetResponse> {
  return apiRequest(apiClient.get(`${PATH}/budget`))
}

export async function getUsage(params?: UsageParams): Promise<AIUsageResponse> {
  return apiRequest(apiClient.get(`${PATH}/usage`, { params }))
}
```

## File: src/services/chat.ts

```typescript
import { apiClient, apiRequest } from './client'
import type { ChatResponse, ChatHistoryResponse } from '@/types/api'

const PATH = '/chat'

export async function sendMessage(
  scripId: string,
  message: string,
  model?: string
): Promise<ChatResponse> {
  return apiRequest(apiClient.post(`${PATH}/${scripId}`, { message, model }))
}

export async function getHistory(
  scripId: string,
  limit?: number
): Promise<ChatHistoryResponse> {
  return apiRequest(apiClient.get(`${PATH}/${scripId}/history`, { params: { limit } }))
}
```

---

# 8. REACT QUERY HOOKS

## File: src/lib/queryKeys.ts

```typescript
export const queryKeys = {
  instruments: {
    all: ['instruments'] as const,
    list: (params?: { active_only?: boolean }) => [...queryKeys.instruments.all, 'list', params] as const,
    detail: (id: string) => [...queryKeys.instruments.all, 'detail', id] as const,
  },
  silos: {
    all: ['silos'] as const,
    list: (instrumentId?: string) => [...queryKeys.silos.all, 'list', instrumentId] as const,
    detail: (id: string) => [...queryKeys.silos.all, 'detail', id] as const,
  },
  charts: {
    all: ['charts'] as const,
    list: (siloId?: string) => [...queryKeys.charts.all, 'list', siloId] as const,
    detail: (id: string) => [...queryKeys.charts.all, 'detail', id] as const,
  },
  signals: {
    all: ['signals'] as const,
    byChart: (chartId: string) => [...queryKeys.signals.all, 'chart', chartId] as const,
    latest: (chartId: string) => [...queryKeys.signals.all, 'latest', chartId] as const,
  },
  relationships: {
    all: ['relationships'] as const,
    bySilo: (siloId: string) => [...queryKeys.relationships.all, 'silo', siloId] as const,
    byInstrument: (instrumentId: string) => [...queryKeys.relationships.all, 'instrument', instrumentId] as const,
  },
  narratives: {
    all: ['narratives'] as const,
    bySilo: (siloId: string) => [...queryKeys.narratives.all, 'silo', siloId] as const,
  },
  ai: {
    models: ['ai', 'models'] as const,
    budget: ['ai', 'budget'] as const,
    usage: (period?: string) => ['ai', 'usage', period] as const,
  },
  chat: {
    history: (scripId: string) => ['chat', 'history', scripId] as const,
  },
}
```

## File: src/hooks/useInstruments.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getInstruments, getInstrument } from '@/services/instruments'
import type { InstrumentListParams } from '@/types/api'

export function useInstruments(params?: InstrumentListParams) {
  return useQuery({
    queryKey: queryKeys.instruments.list(params),
    queryFn: () => getInstruments(params),
  })
}

export function useInstrument(id: string) {
  return useQuery({
    queryKey: queryKeys.instruments.detail(id),
    queryFn: () => getInstrument(id),
    enabled: !!id,
  })
}
```

## File: src/hooks/useSilos.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getSilos, getSilo } from '@/services/silos'

export function useSilos(instrumentId?: string) {
  return useQuery({
    queryKey: queryKeys.silos.list(instrumentId),
    queryFn: () => getSilos({ instrument_id: instrumentId }),
    enabled: !!instrumentId,
  })
}

export function useSilo(id: string) {
  return useQuery({
    queryKey: queryKeys.silos.detail(id),
    queryFn: () => getSilo(id),
    enabled: !!id,
  })
}
```

## File: src/hooks/useCharts.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getCharts, getChart } from '@/services/charts'

export function useCharts(siloId?: string) {
  return useQuery({
    queryKey: queryKeys.charts.list(siloId),
    queryFn: () => getCharts({ silo_id: siloId }),
    enabled: !!siloId,
  })
}

export function useChart(id: string) {
  return useQuery({
    queryKey: queryKeys.charts.detail(id),
    queryFn: () => getChart(id),
    enabled: !!id,
  })
}
```

## File: src/hooks/useSignals.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getSignalsByChart, getLatestSignal } from '@/services/signals'

export function useSignals(chartId: string, limit?: number) {
  return useQuery({
    queryKey: queryKeys.signals.byChart(chartId),
    queryFn: () => getSignalsByChart(chartId, { limit }),
    enabled: !!chartId,
  })
}

export function useLatestSignal(chartId: string) {
  return useQuery({
    queryKey: queryKeys.signals.latest(chartId),
    queryFn: () => getLatestSignal(chartId),
    enabled: !!chartId,
    staleTime: 30 * 1000, // 30 seconds
  })
}
```

## File: src/hooks/useRelationships.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getRelationships, getInstrumentRelationships } from '@/services/relationships'

export function useRelationships(siloId: string) {
  return useQuery({
    queryKey: queryKeys.relationships.bySilo(siloId),
    queryFn: () => getRelationships(siloId),
    enabled: !!siloId,
  })
}

export function useInstrumentRelationships(instrumentId: string) {
  return useQuery({
    queryKey: queryKeys.relationships.byInstrument(instrumentId),
    queryFn: () => getInstrumentRelationships(instrumentId),
    enabled: !!instrumentId,
  })
}
```

## File: src/hooks/useNarratives.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getNarrative } from '@/services/narratives'

export function useNarrative(siloId: string) {
  return useQuery({
    queryKey: queryKeys.narratives.bySilo(siloId),
    queryFn: () => getNarrative(siloId),
    enabled: !!siloId,
    staleTime: 60 * 1000, // 1 minute
  })
}
```

## File: src/hooks/useAI.ts

```typescript
import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getModels, getBudget, getUsage } from '@/services/ai'

export function useModels() {
  return useQuery({
    queryKey: queryKeys.ai.models,
    queryFn: getModels,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useBudget() {
  return useQuery({
    queryKey: queryKeys.ai.budget,
    queryFn: getBudget,
    refetchInterval: 60 * 1000, // Refetch every minute
  })
}

export function useUsage(period?: 'daily' | 'weekly' | 'monthly') {
  return useQuery({
    queryKey: queryKeys.ai.usage(period),
    queryFn: () => getUsage({ period }),
  })
}
```

## File: src/hooks/useChat.ts

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { sendMessage, getHistory } from '@/services/chat'

export function useHistory(scripId: string) {
  return useQuery({
    queryKey: queryKeys.chat.history(scripId),
    queryFn: () => getHistory(scripId),
    enabled: !!scripId,
  })
}

export function useSendMessage(scripId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ message, model }: { message: string; model?: string }) =>
      sendMessage(scripId, message, model),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.chat.history(scripId) })
      queryClient.invalidateQueries({ queryKey: queryKeys.ai.budget })
    },
  })
}
```

---

# 9. PAGE SPECIFICATIONS

## Page: HomePage.tsx

```typescript
import { Link } from 'react-router-dom'
import { useInstruments } from '@/hooks/useInstruments'
import { InstrumentCard } from '@/components/instruments/InstrumentCard'
import { Spinner } from '@/components/common/Spinner'
import { EmptyState } from '@/components/common/EmptyState'
import { Activity } from 'lucide-react'

export function HomePage() {
  const { data: instruments, isLoading } = useInstruments({ active_only: true })

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!instruments?.length) {
    return (
      <EmptyState
        title="No Instruments"
        description="No active instruments found. Create one to get started."
      />
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Activity className="h-8 w-8 text-accent-primary" />
        <h1 className="font-display text-2xl font-bold">Dashboard</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {instruments.map((instrument) => (
          <Link key={instrument.instrument_id} to={`/instruments/${instrument.instrument_id}`}>
            <InstrumentCard instrument={instrument} />
          </Link>
        ))}
      </div>
    </div>
  )
}
```

## Page: SiloDetailPage.tsx (CONSTITUTIONAL CRITICAL)

```typescript
import { useParams } from 'react-router-dom'
import { useSilo } from '@/hooks/useSilos'
import { useCharts } from '@/hooks/useCharts'
import { useRelationships } from '@/hooks/useRelationships'
import { useNarrative } from '@/hooks/useNarratives'
import { ChartList } from '@/components/charts/ChartList'
import { ContradictionPanel } from '@/components/relationships/ContradictionPanel'
import { ConfirmationPanel } from '@/components/relationships/ConfirmationPanel'
import { NarrativeDisplay } from '@/components/narratives/NarrativeDisplay'
import { PageHeader } from '@/components/layout/PageHeader'
import { Spinner } from '@/components/common/Spinner'

export function SiloDetailPage() {
  const { siloId } = useParams<{ siloId: string }>()
  const { data: silo, isLoading: siloLoading } = useSilo(siloId!)
  const { data: charts, isLoading: chartsLoading } = useCharts(siloId)
  const { data: relationships, isLoading: relLoading } = useRelationships(siloId!)
  const { data: narrative, isLoading: narrLoading } = useNarrative(siloId!)

  if (siloLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!silo) {
    return <div>Silo not found</div>
  }

  return (
    <div className="space-y-8">
      <PageHeader title={silo.silo_name} />

      {/* Charts Section */}
      <section>
        <h2 className="mb-4 font-display text-lg font-semibold">Charts</h2>
        <ChartList charts={charts ?? []} isLoading={chartsLoading} />
      </section>

      {/* CONSTITUTIONAL: Contradictions shown with EQUAL prominence */}
      <section>
        <ContradictionPanel
          contradictions={relationships?.contradictions ?? []}
        />
      </section>

      {/* Confirmations Section */}
      <section>
        <ConfirmationPanel
          confirmations={relationships?.confirmations ?? []}
        />
      </section>

      {/* CONSTITUTIONAL: Narrative with MANDATORY disclaimer */}
      <section>
        <NarrativeDisplay
          narrative={narrative}
          isLoading={narrLoading}
        />
      </section>
    </div>
  )
}
```

---

# 10. STATE MANAGEMENT

## File: src/lib/queryClient.ts

```typescript
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000, // 30 seconds
      gcTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: true,
    },
    mutations: {
      retry: 1,
    },
  },
})
```

## File: src/App.tsx

```typescript
import { QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { queryClient } from '@/lib/queryClient'
import { AppShell } from '@/components/layout/AppShell'
import { HomePage } from '@/pages/HomePage'
import { InstrumentsPage } from '@/pages/InstrumentsPage'
import { InstrumentDetailPage } from '@/pages/InstrumentDetailPage'
import { SiloDetailPage } from '@/pages/SiloDetailPage'
import { ChartDetailPage } from '@/pages/ChartDetailPage'
import { ChatPage } from '@/pages/ChatPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

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
            <Route path="charts/:chartId" element={<ChartDetailPage />} />
            <Route path="chat/:scripId?" element={<ChatPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
```

---

# 11. VERIFICATION MATRIX

| ID | Requirement | Component | Test Criteria | Pass/Fail |
|----|-------------|-----------|---------------|-----------|
| V-CR-001-A | No buy/sell buttons | All pages | Grep for "Buy", "Sell", "Enter", "Exit" buttons → 0 results | |
| V-CR-001-B | No prescriptive text | NarrativeDisplay | AI content does not contain "should", "recommend", "suggest" | |
| V-CR-002-A | Equal contradiction sides | ContradictionCard | Both sides use identical CSS classes | |
| V-CR-002-B | Equal sizing | ContradictionCard | Grid columns are [1fr, auto, 1fr] | |
| V-CR-003-A | Disclaimer present | NarrativeDisplay | Disclaimer component is rendered | |
| V-CR-003-B | Disclaimer not dismissible | Disclaimer | No close button, no collapse | |
| V-CR-003-C | Exact disclaimer text | Disclaimer | Text matches specification exactly | |
| V-ICS-002 | Instruments list | InstrumentsPage | Shows all instruments from API | |
| V-ICS-005 | Charts equal size | ChartList | All ChartCards are identical dimensions | |
| V-ICS-007 | Direction badges equal | DirectionBadge | BULLISH, BEARISH, NEUTRAL same size | |
| V-ICS-010 | Contradictions displayed | SiloDetailPage | Shows ContradictionPanel with data | |
| V-ICS-013 | Narrative with disclaimer | SiloDetailPage | NarrativeDisplay includes Disclaimer | |
| V-ICS-017 | Budget indicator | Header | BudgetIndicator shows remaining budget | |
| V-ICS-018 | Chat disclaimer | ChatInterface | Each AI response has Disclaimer | |

---

# IMPLEMENTATION DIRECTIVE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         FOR CURSOR AI AGENT                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  1. Read this document in its entirety before starting                        ║
║  2. Create the project structure exactly as specified in Section 3            ║
║  3. Implement TypeScript types exactly as specified in Section 6              ║
║  4. Implement API services exactly as specified in Section 7                  ║
║  5. Implement React Query hooks exactly as specified in Section 8             ║
║  6. Implement components exactly as specified in Section 5                    ║
║  7. Implement pages exactly as specified in Section 9                         ║
║  8. Run verification matrix (Section 11) to confirm compliance                ║
║                                                                               ║
║  CONSTITUTIONAL RULES ARE NON-NEGOTIABLE.                                     ║
║  Any implementation that violates CR-001, CR-002, or CR-003 is REJECTED.      ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

*Document ID: CIA-SIE-ICD-001 | Version 1.0.0 | Generated 2026-01-04*
