# AUTONOMOUS HANDOFF: CIA-SIE FRONTEND IMPLEMENTATION

**Version:** 1.0.0
**Generated:** January 3, 2026
**Purpose:** Enable fully autonomous frontend implementation by any AI coding assistant
**Validation Framework:** Gold Standard Validation Protocol v2.0
**Governance:** Constitutional Rules (INVIOLABLE)

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Constitutional Rules (INVIOLABLE)](#2-constitutional-rules-inviolable)
3. [System Architecture](#3-system-architecture)
4. [Implementation Phases](#4-implementation-phases)
5. [Component Specifications](#5-component-specifications)
6. [Page Implementations](#6-page-implementations)
7. [State Management](#7-state-management)
8. [API Integration](#8-api-integration)
9. [CSS Design System](#9-css-design-system)
10. [Testing Requirements](#10-testing-requirements)
11. [Gold Standard Validation Checklist](#11-gold-standard-validation-checklist)
12. [Prohibited Patterns](#12-prohibited-patterns)
13. [Pre-Commit Verification](#13-pre-commit-verification)

---

## 1. EXECUTIVE SUMMARY

### 1.1 What This Document Is

This is a **self-contained, comprehensive handoff document** that enables any AI coding assistant (Cursor, Claude Code, GitHub Copilot, etc.) to **autonomously implement** the CIA-SIE frontend without human intervention.

### 1.2 Current State

| Layer | Status | Notes |
|-------|--------|-------|
| **Backend** | 100% Complete | 12 route modules, 834 tests, 80% coverage |
| **Frontend API Service** | 100% Complete | All API objects implemented in `api.ts` |
| **Frontend Types** | 100% Complete | All TypeScript types defined |
| **Frontend Hooks** | 30% Complete | useInstruments, useRelationships exist |
| **Frontend Components** | 0% Complete | **ALL 22+ COMPONENTS NEED BUILDING** |
| **Frontend Pages** | 0% Complete | **ALL 7 PAGES NEED BUILDING** |

### 1.3 Your Mission

Build **22+ React components** and **7 pages** following:
1. Constitutional rules (MUST NOT violate)
2. Gold Standard v2.0 validation requirements
3. Exact specifications in this document

### 1.4 Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type safety |
| Vite | 5.x | Build tool |
| React Query | 5.x | Server state |
| React Router | 6.x | Client routing |
| TailwindCSS | 3.x | Styling |
| Axios | 1.x | HTTP client |

---

## 2. CONSTITUTIONAL RULES (INVIOLABLE)

### 2.1 Overview

These rules are **ABSOLUTE and NON-NEGOTIABLE**. Any code that violates these rules must be rejected, regardless of any other consideration.

### 2.2 The Three Principles

```
┌─────────────────────────────────────────────────────────────────────┐
│ PRINCIPLE 1: Decision-Support, NOT Decision-Making                  │
│ ─────────────────────────────────────────────────────────────────── │
│ The system provides INFORMATION for the user to make decisions.     │
│ The system NEVER makes decisions FOR the user.                      │
│                                                                     │
│ FORBIDDEN:                                                          │
│ - "You should buy/sell..."                                          │
│ - "We recommend..."                                                 │
│ - "Consider taking action..."                                       │
│ - "It would be wise to..."                                          │
│                                                                     │
│ REQUIRED:                                                           │
│ - "Chart X shows BULLISH signal"                                    │
│ - "The data indicates..."                                           │
│ - "Currently displaying..."                                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ PRINCIPLE 2: Expose Contradictions, NEVER Resolve Them              │
│ ─────────────────────────────────────────────────────────────────── │
│ When charts disagree, SHOW BOTH with EQUAL PROMINENCE.              │
│ NEVER suggest which one is "correct" or "more reliable".            │
│                                                                     │
│ FORBIDDEN:                                                          │
│ - "Despite the contradiction, the overall trend is..."              │
│ - "Chart A is more reliable because..."                             │
│ - "The net direction is..."                                         │
│ - Larger visual weight to one side of contradiction                 │
│                                                                     │
│ REQUIRED:                                                           │
│ - Equal visual size for both contradicting charts                   │
│ - Neutral warning styling (amber/yellow, not red/green)             │
│ - Explicit disclaimer: "System does NOT resolve conflicts"          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ PRINCIPLE 3: Descriptive AI, NOT Prescriptive AI                    │
│ ─────────────────────────────────────────────────────────────────── │
│ AI output DESCRIBES what charts show.                               │
│ AI output NEVER PRESCRIBES what user should do.                     │
│                                                                     │
│ MANDATORY DISCLAIMER (must appear on ALL AI output):                │
│ "This is a description of what your charts are showing.             │
│  The interpretation and any decision is entirely yours."            │
│                                                                     │
│ This disclaimer is NON-NEGOTIABLE and CANNOT be abbreviated.        │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.3 Prohibited Features (PR-01 to PR-06)

| Code | Prohibited Feature | Reason |
|------|-------------------|--------|
| PR-01 | Buy/Sell buttons | Implies decision-making |
| PR-02 | Signal strength scores | Implies judgment |
| PR-03 | Chart weights | Implies hierarchy |
| PR-04 | Confidence percentages | Implies prediction |
| PR-05 | "Overall direction" | Implies aggregation |
| PR-06 | Price predictions | Implies forecasting |

### 2.4 Mandated Features (MN-01 to MN-05)

| Code | Mandated Feature | Implementation |
|------|-----------------|----------------|
| MN-01 | Constitutional Banner | On every dashboard view |
| MN-02 | Mandatory AI Disclaimer | On every AI response |
| MN-03 | Equal Visual Weight | For all contradiction displays |
| MN-04 | Freshness Indicators | On every signal display |
| MN-05 | Response Validation | Before displaying AI content |

---

## 3. SYSTEM ARCHITECTURE

### 3.1 Directory Structure

```
frontend/
├── src/
│   ├── App.tsx                    # Root component with routing
│   ├── main.tsx                   # Entry point
│   ├── index.css                  # Global styles
│   │
│   ├── components/                # Reusable components
│   │   ├── layout/
│   │   │   ├── Layout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── PageHeader.tsx
│   │   │
│   │   ├── constitutional/        # CRITICAL - Constitutional compliance
│   │   │   ├── ConstitutionalBanner.tsx
│   │   │   ├── ContradictionAlert.tsx
│   │   │   ├── ContradictionPanel.tsx
│   │   │   └── NarrativePanel.tsx
│   │   │
│   │   ├── signals/               # Signal display
│   │   │   ├── SignalGrid.tsx
│   │   │   ├── ChartSignalCard.tsx
│   │   │   ├── DirectionBadge.tsx
│   │   │   └── FreshnessIndicator.tsx
│   │   │
│   │   ├── ai/                    # AI-related components
│   │   │   ├── ModelSelector.tsx
│   │   │   ├── TokenDisplay.tsx
│   │   │   ├── CostDisplay.tsx
│   │   │   ├── BudgetAlert.tsx
│   │   │   ├── AIUsagePanel.tsx
│   │   │   └── ChatPanel.tsx
│   │   │
│   │   └── shared/                # Generic components
│   │       ├── Card.tsx
│   │       ├── Badge.tsx
│   │       ├── Accordion.tsx
│   │       ├── Tabs.tsx
│   │       ├── InfoBox.tsx
│   │       ├── CommandBox.tsx
│   │       ├── Table.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── ErrorMessage.tsx
│   │
│   ├── pages/                     # Page components
│   │   ├── Dashboard.tsx
│   │   ├── InstrumentList.tsx
│   │   ├── InstrumentDetail.tsx
│   │   ├── SiloDetail.tsx
│   │   ├── ChartsReference.tsx
│   │   ├── Settings.tsx
│   │   └── Troubleshooting.tsx
│   │
│   ├── hooks/                     # React Query hooks
│   │   ├── useInstruments.ts      # EXISTS
│   │   ├── useRelationships.ts    # EXISTS
│   │   ├── useAI.ts               # TO CREATE
│   │   ├── useChat.ts             # TO CREATE
│   │   └── useNarrative.ts        # TO CREATE
│   │
│   ├── services/
│   │   └── api.ts                 # EXISTS - Complete
│   │
│   ├── types/
│   │   └── index.ts               # EXISTS - Complete
│   │
│   └── constants/
│       └── sampleCharts.ts        # TO CREATE
```

### 3.2 Component Hierarchy

```
App
├── BrowserRouter
│   └── Routes
│       ├── "/" → Dashboard
│       │   └── Layout
│       │       ├── Sidebar
│       │       └── MainContent
│       │           ├── PageHeader
│       │           ├── ConstitutionalBanner    [CRITICAL]
│       │           ├── InstrumentSelector
│       │           ├── SignalGrid
│       │           │   └── ChartSignalCard (×N)
│       │           │       ├── DirectionBadge
│       │           │       └── FreshnessIndicator
│       │           ├── ContradictionPanel      [CRITICAL]
│       │           │   └── ContradictionAlert (×N)
│       │           ├── ConfirmationPanel
│       │           └── NarrativePanel          [CRITICAL]
│       │
│       ├── "/instruments" → InstrumentList
│       ├── "/instruments/:id" → InstrumentDetail
│       ├── "/silos/:id" → SiloDetail
│       ├── "/charts" → ChartsReference
│       ├── "/settings" → Settings
│       └── "/troubleshooting" → Troubleshooting
```

---

## 4. IMPLEMENTATION PHASES

### Phase 1: Foundation Layer (Day 1)

| Order | Component | File | Priority |
|-------|-----------|------|----------|
| 1.1 | Layout | `components/layout/Layout.tsx` | CRITICAL |
| 1.2 | Sidebar | `components/layout/Sidebar.tsx` | CRITICAL |
| 1.3 | PageHeader | `components/layout/PageHeader.tsx` | HIGH |
| 1.4 | Card | `components/shared/Card.tsx` | HIGH |
| 1.5 | Badge | `components/shared/Badge.tsx` | HIGH |
| 1.6 | LoadingSpinner | `components/shared/LoadingSpinner.tsx` | MEDIUM |
| 1.7 | ErrorMessage | `components/shared/ErrorMessage.tsx` | MEDIUM |

### Phase 2: Core Display (Day 2)

| Order | Component | File | Priority |
|-------|-----------|------|----------|
| 2.1 | DirectionBadge | `components/signals/DirectionBadge.tsx` | HIGH |
| 2.2 | FreshnessIndicator | `components/signals/FreshnessIndicator.tsx` | HIGH |
| 2.3 | ChartSignalCard | `components/signals/ChartSignalCard.tsx` | HIGH |
| 2.4 | SignalGrid | `components/signals/SignalGrid.tsx` | HIGH |

### Phase 3: Constitutional Components (Day 3) - CRITICAL

| Order | Component | File | Priority |
|-------|-----------|------|----------|
| 3.1 | ConstitutionalBanner | `components/constitutional/ConstitutionalBanner.tsx` | **CRITICAL** |
| 3.2 | ContradictionAlert | `components/constitutional/ContradictionAlert.tsx` | **CRITICAL** |
| 3.3 | ContradictionPanel | `components/constitutional/ContradictionPanel.tsx` | **CRITICAL** |
| 3.4 | ConfirmationPanel | `components/constitutional/ConfirmationPanel.tsx` | HIGH |
| 3.5 | NarrativePanel | `components/constitutional/NarrativePanel.tsx` | **CRITICAL** |

### Phase 4: AI Components (Day 4)

| Order | Component | File | Priority |
|-------|-----------|------|----------|
| 4.1 | ModelSelector | `components/ai/ModelSelector.tsx` | HIGH |
| 4.2 | TokenDisplay | `components/ai/TokenDisplay.tsx` | MEDIUM |
| 4.3 | CostDisplay | `components/ai/CostDisplay.tsx` | MEDIUM |
| 4.4 | BudgetAlert | `components/ai/BudgetAlert.tsx` | HIGH |
| 4.5 | AIUsagePanel | `components/ai/AIUsagePanel.tsx` | MEDIUM |
| 4.6 | ChatPanel | `components/ai/ChatPanel.tsx` | HIGH |

### Phase 5: Utility Components (Day 5)

| Order | Component | File | Priority |
|-------|-----------|------|----------|
| 5.1 | Accordion | `components/shared/Accordion.tsx` | MEDIUM |
| 5.2 | Tabs | `components/shared/Tabs.tsx` | MEDIUM |
| 5.3 | InfoBox | `components/shared/InfoBox.tsx` | MEDIUM |
| 5.4 | CommandBox | `components/shared/CommandBox.tsx` | LOW |
| 5.5 | Table | `components/shared/Table.tsx` | MEDIUM |
| 5.6 | InstrumentSelector | `components/signals/InstrumentSelector.tsx` | HIGH |

### Phase 6: Pages (Day 6-7)

| Order | Page | File | Priority |
|-------|------|------|----------|
| 6.1 | Dashboard | `pages/Dashboard.tsx` | **CRITICAL** |
| 6.2 | InstrumentList | `pages/InstrumentList.tsx` | HIGH |
| 6.3 | InstrumentDetail | `pages/InstrumentDetail.tsx` | HIGH |
| 6.4 | SiloDetail | `pages/SiloDetail.tsx` | HIGH |
| 6.5 | ChartsReference | `pages/ChartsReference.tsx` | MEDIUM |
| 6.6 | Settings | `pages/Settings.tsx` | MEDIUM |
| 6.7 | Troubleshooting | `pages/Troubleshooting.tsx` | LOW |

### Phase 7: Hooks & Routing (Day 7)

| Order | Task | File | Priority |
|-------|------|------|----------|
| 7.1 | useAI hook | `hooks/useAI.ts` | HIGH |
| 7.2 | useChat hook | `hooks/useChat.ts` | HIGH |
| 7.3 | useNarrative hook | `hooks/useNarrative.ts` | HIGH |
| 7.4 | App routing | `App.tsx` | **CRITICAL** |
| 7.5 | Sample charts constant | `constants/sampleCharts.ts` | MEDIUM |

---

## 5. COMPONENT SPECIFICATIONS

### 5.1 ConstitutionalBanner (CRITICAL)

**File:** `components/constitutional/ConstitutionalBanner.tsx`

**Purpose:** Display the three constitutional principles prominently on the dashboard.

**EXACT Implementation:**

```tsx
import React from 'react'

/**
 * ConstitutionalBanner Component
 *
 * Displays the three inviolable constitutional principles.
 * This component MUST appear on every dashboard view.
 * The text is EXACT and CANNOT be modified.
 *
 * @constitutional MN-01
 */
export function ConstitutionalBanner(): React.ReactElement {
  const principles = [
    {
      number: 1,
      text: 'Decision-Support NOT Decision-Making',
      bgColor: 'bg-amber-100',
    },
    {
      number: 2,
      text: 'Expose Contradictions, NEVER Resolve Them',
      bgColor: 'bg-amber-100',
    },
    {
      number: 3,
      text: 'Descriptive AI, NOT Prescriptive AI',
      bgColor: 'bg-amber-100',
    },
  ]

  return (
    <div className="bg-gradient-to-r from-amber-50 to-yellow-50 border-2 border-amber-400 rounded-xl p-6 mb-8">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">⚠️</span>
        <h2 className="text-lg font-semibold text-amber-800">
          Constitutional Principles
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {principles.map((principle) => (
          <div
            key={principle.number}
            className="bg-white rounded-lg p-4 shadow-sm flex items-center gap-3"
          >
            <span className="w-7 h-7 rounded-full bg-amber-500 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
              {principle.number}
            </span>
            <span className="text-sm text-amber-900 font-medium">
              {principle.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Validation Checklist:**
- [ ] Exact text matches constitutional principles
- [ ] Uses warning color scheme (amber/yellow)
- [ ] Three items displayed with equal prominence
- [ ] No modifications to principle text

---

### 5.2 ContradictionAlert (CRITICAL)

**File:** `components/constitutional/ContradictionAlert.tsx`

**Purpose:** Display a single contradiction between two charts with EQUAL prominence.

**EXACT Implementation:**

```tsx
import React from 'react'
import type { Contradiction } from '../../types'
import { DirectionBadge } from '../signals/DirectionBadge'

/**
 * ContradictionAlert Component
 *
 * Displays a contradiction between two charts.
 *
 * CRITICAL REQUIREMENTS:
 * 1. Both charts MUST have EQUAL visual prominence
 * 2. No visual suggestion of which is "correct"
 * 3. Warning color scheme (amber/yellow)
 * 4. Clear disclaimer that system does NOT resolve conflicts
 *
 * @constitutional PRINCIPLE-2
 */
interface ContradictionAlertProps {
  contradiction: Contradiction
}

export function ContradictionAlert({ contradiction }: ContradictionAlertProps): React.ReactElement {
  return (
    <div className="bg-amber-50 border-2 border-amber-300 rounded-xl p-5 mb-4">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xl">⚠️</span>
        <span className="font-semibold text-amber-800">CONTRADICTION DETECTED</span>
      </div>

      {/* Two charts with EQUAL visual weight */}
      <div className="flex items-center justify-center gap-4">
        {/* Chart A - EQUAL SIZE */}
        <div className="flex-1 max-w-[200px] bg-white rounded-lg p-4 text-center border border-amber-200">
          <div className="text-lg font-bold text-slate-700">
            {contradiction.chart_a_name}
          </div>
          <div className="mt-2">
            <DirectionBadge direction={contradiction.chart_a_direction} size="lg" />
          </div>
        </div>

        {/* Bi-directional arrow - NEUTRAL */}
        <div className="text-3xl text-amber-500 flex-shrink-0">⇄</div>

        {/* Chart B - EQUAL SIZE (MUST match Chart A exactly) */}
        <div className="flex-1 max-w-[200px] bg-white rounded-lg p-4 text-center border border-amber-200">
          <div className="text-lg font-bold text-slate-700">
            {contradiction.chart_b_name}
          </div>
          <div className="mt-2">
            <DirectionBadge direction={contradiction.chart_b_direction} size="lg" />
          </div>
        </div>
      </div>

      {/* MANDATORY disclaimer */}
      <p className="mt-4 text-sm text-amber-700 text-center italic">
        This contradiction is shown for your awareness. The system does NOT resolve this conflict.
      </p>
    </div>
  )
}
```

**Validation Checklist:**
- [ ] Both chart displays have IDENTICAL dimensions
- [ ] No larger font, border, or highlighting on either side
- [ ] Neutral bi-directional arrow (not pointing to "winner")
- [ ] Disclaimer present stating system does NOT resolve
- [ ] Uses amber/yellow color scheme (not red/green)

---

### 5.3 NarrativePanel (CRITICAL)

**File:** `components/constitutional/NarrativePanel.tsx`

**Purpose:** Display AI-generated narrative with MANDATORY disclaimer.

**EXACT Implementation:**

```tsx
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { narrativesApi } from '../../services/api'
import { LoadingSpinner } from '../shared/LoadingSpinner'
import { ErrorMessage } from '../shared/ErrorMessage'

/**
 * NarrativePanel Component
 *
 * Displays AI-generated narrative about silo signals.
 *
 * CRITICAL: The disclaimer is MANDATORY and CANNOT be removed or abbreviated.
 *
 * @constitutional MN-02, PRINCIPLE-3
 */
interface NarrativePanelProps {
  siloId: string
  useAi?: boolean
}

const MANDATORY_DISCLAIMER = `This is a description of what your charts are showing. The interpretation and any decision is entirely yours.`

export function NarrativePanel({ siloId, useAi = true }: NarrativePanelProps): React.ReactElement {
  const { data: narrative, isLoading, error, refetch } = useQuery({
    queryKey: ['narrative', siloId, useAi],
    queryFn: () => narrativesApi.generateForSilo(siloId, useAi),
    enabled: !!siloId,
    staleTime: 5 * 60 * 1000, // 5 minutes (expensive AI call)
  })

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-semibold mb-4">AI Narrative</h3>
        <LoadingSpinner label="Generating narrative..." />
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-semibold mb-4">AI Narrative</h3>
        <ErrorMessage
          message="Failed to generate narrative"
          onRetry={() => refetch()}
        />
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h3 className="text-lg font-semibold mb-4">AI Narrative</h3>

      {/* Narrative sections */}
      <div className="space-y-4 mb-6">
        {narrative?.sections.map((section, index) => (
          <div key={index} className="text-slate-700">
            {section.section_type === 'SIGNAL_SUMMARY' && (
              <p className="font-medium">{section.content}</p>
            )}
            {section.section_type === 'CONTRADICTION' && (
              <p className="text-amber-700 bg-amber-50 p-3 rounded-lg">
                ⚠️ {section.content}
              </p>
            )}
            {section.section_type === 'CONFIRMATION' && (
              <p className="text-emerald-700 bg-emerald-50 p-3 rounded-lg">
                ✓ {section.content}
              </p>
            )}
            {section.section_type === 'FRESHNESS' && (
              <p className="text-slate-500 text-sm">{section.content}</p>
            )}
          </div>
        ))}
      </div>

      {/* MANDATORY DISCLAIMER - CANNOT BE REMOVED OR MODIFIED */}
      <div className="border-t pt-4 mt-4">
        <p className="text-sm text-slate-500 italic bg-slate-50 p-4 rounded-lg border-l-4 border-slate-300">
          {narrative?.closing_statement || MANDATORY_DISCLAIMER}
        </p>
      </div>
    </div>
  )
}
```

**Validation Checklist:**
- [ ] Disclaimer is ALWAYS displayed
- [ ] Disclaimer text is EXACT (not paraphrased)
- [ ] Disclaimer cannot be dismissed or hidden
- [ ] Visually distinct styling for disclaimer

---

### 5.4 DirectionBadge

**File:** `components/signals/DirectionBadge.tsx`

```tsx
import React from 'react'
import type { Direction } from '../../types'

interface DirectionBadgeProps {
  direction: Direction | null
  size?: 'sm' | 'md' | 'lg'
}

const DIRECTION_CONFIG = {
  BULLISH: {
    arrow: '↑',
    label: 'BULLISH',
    bgColor: 'bg-emerald-100',
    textColor: 'text-emerald-700',
    borderColor: 'border-emerald-300',
  },
  BEARISH: {
    arrow: '↓',
    label: 'BEARISH',
    bgColor: 'bg-red-100',
    textColor: 'text-red-700',
    borderColor: 'border-red-300',
  },
  NEUTRAL: {
    arrow: '→',
    label: 'NEUTRAL',
    bgColor: 'bg-slate-100',
    textColor: 'text-slate-600',
    borderColor: 'border-slate-300',
  },
}

const SIZE_CLASSES = {
  sm: 'text-xs px-2 py-1',
  md: 'text-sm px-3 py-1.5',
  lg: 'text-base px-4 py-2',
}

export function DirectionBadge({ direction, size = 'md' }: DirectionBadgeProps): React.ReactElement {
  if (!direction) {
    return (
      <span className={`inline-flex items-center gap-1 rounded-full bg-slate-100 text-slate-500 border border-slate-200 ${SIZE_CLASSES[size]}`}>
        <span>—</span>
        <span>NO SIGNAL</span>
      </span>
    )
  }

  const config = DIRECTION_CONFIG[direction]

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${config.bgColor} ${config.textColor} ${config.borderColor} ${SIZE_CLASSES[size]} font-medium`}>
      <span className="text-lg">{config.arrow}</span>
      <span>{config.label}</span>
    </span>
  )
}
```

---

### 5.5 FreshnessIndicator

**File:** `components/signals/FreshnessIndicator.tsx`

```tsx
import React from 'react'
import type { FreshnessStatus } from '../../types'

interface FreshnessIndicatorProps {
  status: FreshnessStatus
  showLabel?: boolean
}

const FRESHNESS_CONFIG = {
  CURRENT: {
    icon: '🟢',
    label: 'Current',
    color: 'text-emerald-600',
  },
  RECENT: {
    icon: '🟡',
    label: 'Recent',
    color: 'text-amber-600',
  },
  STALE: {
    icon: '🔴',
    label: 'Stale',
    color: 'text-red-600',
  },
  UNAVAILABLE: {
    icon: '⚫',
    label: 'Unavailable',
    color: 'text-slate-400',
  },
}

export function FreshnessIndicator({ status, showLabel = true }: FreshnessIndicatorProps): React.ReactElement {
  const config = FRESHNESS_CONFIG[status]

  return (
    <span className={`inline-flex items-center gap-1.5 text-sm ${config.color}`}>
      <span>{config.icon}</span>
      {showLabel && <span>{config.label}</span>}
    </span>
  )
}
```

---

### 5.6 ChartSignalCard

**File:** `components/signals/ChartSignalCard.tsx`

```tsx
import React from 'react'
import type { Direction, FreshnessStatus } from '../../types'
import { DirectionBadge } from './DirectionBadge'
import { FreshnessIndicator } from './FreshnessIndicator'

/**
 * ChartSignalCard Component
 *
 * Displays a single chart with its current signal status.
 *
 * CRITICAL: NO weight or score displays (prohibited by PR-02, PR-03)
 */
interface ChartSignalCardProps {
  chartCode: string
  chartName: string
  timeframe: string
  direction: Direction | null
  freshness: FreshnessStatus
  onClick?: () => void
}

export function ChartSignalCard({
  chartCode,
  chartName,
  timeframe,
  direction,
  freshness,
  onClick,
}: ChartSignalCardProps): React.ReactElement {
  return (
    <div
      className="bg-white border border-slate-200 rounded-lg p-4 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer"
      onClick={onClick}
    >
      {/* Chart Code - Primary identifier */}
      <div className="text-xl font-bold text-blue-600 mb-1">{chartCode}</div>

      {/* Chart Name */}
      <div className="text-sm text-slate-600 mb-2">{chartName}</div>

      {/* Timeframe Badge */}
      <div className="mb-3">
        <span className="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">
          {timeframe}
        </span>
      </div>

      {/* Direction - NO weight or score */}
      <div className="mb-2">
        <DirectionBadge direction={direction} size="sm" />
      </div>

      {/* Freshness Status */}
      <div className="text-right">
        <FreshnessIndicator status={freshness} showLabel={true} />
      </div>

      {/* NOTE: Deliberately NO weight, score, or confidence display */}
    </div>
  )
}
```

**Validation Checklist:**
- [ ] NO weight property displayed
- [ ] NO confidence score displayed
- [ ] NO strength indicator
- [ ] Freshness indicator present

---

### 5.7 SignalGrid

**File:** `components/signals/SignalGrid.tsx`

```tsx
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { relationshipsApi } from '../../services/api'
import { ChartSignalCard } from './ChartSignalCard'
import { LoadingSpinner } from '../shared/LoadingSpinner'
import { ErrorMessage } from '../shared/ErrorMessage'

interface SignalGridProps {
  siloId: string
}

export function SignalGrid({ siloId }: SignalGridProps): React.ReactElement {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['relationships', siloId],
    queryFn: () => relationshipsApi.getForSilo(siloId),
    enabled: !!siloId,
    refetchInterval: 60000, // Refresh every minute
  })

  if (isLoading) {
    return <LoadingSpinner label="Loading signals..." />
  }

  if (error) {
    return <ErrorMessage message="Failed to load signals" onRetry={() => refetch()} />
  }

  if (!data || data.charts.length === 0) {
    return (
      <div className="text-center text-slate-500 py-8">
        No charts configured for this silo.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      {data.charts.map((chart) => (
        <ChartSignalCard
          key={chart.chart_id}
          chartCode={chart.chart_code}
          chartName={chart.chart_name}
          timeframe={chart.timeframe}
          direction={chart.latest_signal?.direction ?? null}
          freshness={chart.freshness}
        />
      ))}
    </div>
  )
}
```

---

### 5.8 Layout

**File:** `components/layout/Layout.tsx`

```tsx
import React, { useState } from 'react'
import { Sidebar } from './Sidebar'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps): React.ReactElement {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <main className="flex-1 ml-0 md:ml-[280px] min-h-screen">
        {children}
      </main>

      {/* Mobile Toggle */}
      <button
        className="fixed bottom-5 right-5 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center md:hidden z-50"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        ☰
      </button>
    </div>
  )
}
```

---

### 5.9 Sidebar

**File:** `components/layout/Sidebar.tsx`

```tsx
import React from 'react'
import { NavLink } from 'react-router-dom'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const NAV_SECTIONS = [
  {
    title: 'Dashboard',
    items: [
      { to: '/', label: 'Command Center', icon: '📊' },
    ],
  },
  {
    title: 'Data',
    items: [
      { to: '/instruments', label: 'Instruments', icon: '📈' },
      { to: '/charts', label: '12 Sample Charts', icon: '📋' },
    ],
  },
  {
    title: 'System',
    items: [
      { to: '/settings', label: 'Settings', icon: '⚙️' },
      { to: '/troubleshooting', label: 'Troubleshooting', icon: '🔧' },
    ],
  },
]

export function Sidebar({ isOpen, onClose }: SidebarProps): React.ReactElement {
  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full w-[280px] bg-slate-900 text-white z-50 transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } md:translate-x-0`}
      >
        {/* Logo */}
        <div className="p-6 border-b border-white/10">
          <h1 className="text-2xl font-bold">CIA-SIE</h1>
          <p className="text-xs text-slate-400 mt-1">
            Chart Intelligence Auditor
          </p>
        </div>

        {/* Navigation */}
        <nav className="p-4">
          {NAV_SECTIONS.map((section) => (
            <div key={section.title} className="mb-6">
              <h2 className="text-xs uppercase tracking-wider text-slate-400 px-3 mb-2">
                {section.title}
              </h2>
              <ul className="space-y-1">
                {section.items.map((item) => (
                  <li key={item.to}>
                    <NavLink
                      to={item.to}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                          isActive
                            ? 'bg-blue-600 text-white'
                            : 'text-slate-300 hover:bg-white/10 hover:text-white'
                        }`
                      }
                    >
                      <span>{item.icon}</span>
                      <span className="text-sm">{item.label}</span>
                    </NavLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </aside>
    </>
  )
}
```

---

### 5.10 PageHeader

**File:** `components/layout/PageHeader.tsx`

```tsx
import React from 'react'

interface PageHeaderProps {
  badge: string
  title: string
  description: string
}

export function PageHeader({ badge, title, description }: PageHeaderProps): React.ReactElement {
  return (
    <header className="bg-gradient-to-r from-slate-900 to-blue-900 text-white px-10 py-16">
      <div className="max-w-5xl">
        {/* Badge */}
        <span className="inline-block bg-white/15 border border-white/20 px-3.5 py-1.5 rounded-full text-xs mb-4">
          {badge}
        </span>

        {/* Title */}
        <h1 className="text-4xl font-bold mb-3">{title}</h1>

        {/* Description */}
        <p className="text-lg text-white/80 max-w-xl">{description}</p>
      </div>
    </header>
  )
}
```

---

### 5.11 ModelSelector

**File:** `components/ai/ModelSelector.tsx`

```tsx
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { aiApi } from '../../services/api'

interface ModelSelectorProps {
  selectedModel: string
  onModelChange: (modelId: string) => void
  disabled?: boolean
}

export function ModelSelector({
  selectedModel,
  onModelChange,
  disabled = false,
}: ModelSelectorProps): React.ReactElement {
  const { data, isLoading } = useQuery({
    queryKey: ['ai-models'],
    queryFn: () => aiApi.listModels(),
    staleTime: 5 * 60 * 1000,
  })

  if (isLoading) {
    return <div className="animate-pulse h-12 bg-slate-200 rounded-lg" />
  }

  return (
    <div className="flex gap-2">
      {data?.models.map((model) => (
        <button
          key={model.id}
          onClick={() => onModelChange(model.id)}
          disabled={disabled}
          className={`flex-1 px-4 py-3 rounded-lg border-2 transition-all ${
            selectedModel === model.id
              ? 'border-blue-500 bg-blue-50 text-blue-700'
              : 'border-slate-200 hover:border-slate-300'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <div className="font-semibold">{model.display_name}</div>
          <div className="text-xs text-slate-500 mt-1">
            ${model.cost_per_1k_input_tokens}/1K tokens
          </div>
        </button>
      ))}
    </div>
  )
}
```

---

### 5.12 BudgetAlert

**File:** `components/ai/BudgetAlert.tsx`

```tsx
import React from 'react'

interface BudgetAlertProps {
  percentageUsed: number
  budgetRemaining: number
  onDismiss?: () => void
}

export function BudgetAlert({
  percentageUsed,
  budgetRemaining,
  onDismiss,
}: BudgetAlertProps): React.ReactElement | null {
  // No alert needed if under 80%
  if (percentageUsed < 80) {
    return null
  }

  // Determine alert level
  const isBlocked = percentageUsed >= 100
  const isCritical = percentageUsed >= 90
  const isWarning = percentageUsed >= 80

  const alertConfig = isBlocked
    ? {
        bg: 'bg-red-100 border-red-400',
        icon: '🚫',
        title: 'BUDGET EXHAUSTED',
        message: 'Your monthly AI budget has been exhausted. AI features are disabled until next billing period.',
        dismissible: false,
      }
    : isCritical
    ? {
        bg: 'bg-orange-100 border-orange-400',
        icon: '🔴',
        title: 'BUDGET CRITICAL',
        message: `You have used ${percentageUsed.toFixed(0)}% of your monthly AI budget. Remaining: $${budgetRemaining.toFixed(2)}`,
        dismissible: false,
      }
    : {
        bg: 'bg-amber-100 border-amber-400',
        icon: '⚠️',
        title: 'BUDGET WARNING',
        message: `You have used ${percentageUsed.toFixed(0)}% of your monthly AI budget. Remaining: $${budgetRemaining.toFixed(2)}`,
        dismissible: true,
      }

  return (
    <div className={`rounded-lg border-2 p-4 ${alertConfig.bg}`}>
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl">{alertConfig.icon}</span>
          <span className="font-bold">{alertConfig.title}</span>
        </div>
        {alertConfig.dismissible && onDismiss && (
          <button onClick={onDismiss} className="text-slate-500 hover:text-slate-700">
            ×
          </button>
        )}
      </div>
      <p className="mt-2 text-sm">{alertConfig.message}</p>
    </div>
  )
}
```

---

### 5.13 ChatPanel

**File:** `components/ai/ChatPanel.tsx`

```tsx
import React, { useState, useRef, useEffect } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { chatApi } from '../../services/api'
import type { ChatMessage } from '../../types'
import { ModelSelector } from './ModelSelector'
import { LoadingSpinner } from '../shared/LoadingSpinner'

/**
 * ChatPanel Component
 *
 * Per-instrument conversation interface.
 *
 * CRITICAL: AI responses MUST be descriptive only.
 * The mandatory disclaimer MUST always be displayed.
 *
 * @constitutional PRINCIPLE-3, MN-02
 */
interface ChatPanelProps {
  instrumentId: string
  defaultModel?: string
}

export function ChatPanel({ instrumentId, defaultModel = 'claude-3-sonnet' }: ChatPanelProps): React.ReactElement {
  const [input, setInput] = useState('')
  const [selectedModel, setSelectedModel] = useState(defaultModel)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const queryClient = useQueryClient()

  // Fetch conversation history
  const { data: history } = useQuery({
    queryKey: ['chat-history', instrumentId],
    queryFn: () => chatApi.getHistory(instrumentId),
    enabled: !!instrumentId,
  })

  // Send message mutation
  const sendMessage = useMutation({
    mutationFn: (message: string) =>
      chatApi.sendMessage(instrumentId, {
        message,
        model: selectedModel,
        include_context: true,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-history', instrumentId] })
      setInput('')
    },
  })

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [history])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !sendMessage.isPending) {
      sendMessage.mutate(input.trim())
    }
  }

  // Flatten messages from all conversations
  const allMessages: ChatMessage[] = history?.conversations.flatMap((c) => c.messages) ?? []

  return (
    <div className="bg-white rounded-xl shadow flex flex-col h-[500px]">
      {/* Header with Model Selector */}
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold mb-3">Chat with AI</h3>
        <ModelSelector
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
          disabled={sendMessage.isPending}
        />
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {allMessages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-100 text-slate-800'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
              {msg.role === 'assistant' && (
                <p className="mt-3 pt-2 border-t border-slate-300 text-xs text-slate-500 italic">
                  This is a description of what your charts are showing. The interpretation and any decision is entirely yours.
                </p>
              )}
            </div>
          </div>
        ))}

        {sendMessage.isPending && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-lg p-3">
              <LoadingSpinner size="sm" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..."
            className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={sendMessage.isPending}
          />
          <button
            type="submit"
            disabled={!input.trim() || sendMessage.isPending}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  )
}
```

**Validation Checklist:**
- [ ] Disclaimer appears on EVERY assistant message
- [ ] Model selector allows choosing Haiku/Sonnet/Opus
- [ ] No recommendations or prescriptive language in UI

---

### 5.14-5.20 Shared Components

**File:** `components/shared/Card.tsx`
```tsx
import React from 'react'

interface CardProps {
  title?: string
  children: React.ReactNode
  className?: string
}

export function Card({ title, children, className = '' }: CardProps): React.ReactElement {
  return (
    <div className={`bg-white rounded-xl shadow overflow-hidden ${className}`}>
      {title && (
        <div className="px-6 py-4 border-b border-slate-200">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  )
}
```

**File:** `components/shared/Badge.tsx`
```tsx
import React from 'react'

type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info'

interface BadgeProps {
  variant?: BadgeVariant
  children: React.ReactNode
}

const VARIANT_CLASSES: Record<BadgeVariant, string> = {
  default: 'bg-slate-100 text-slate-700',
  success: 'bg-emerald-100 text-emerald-700',
  warning: 'bg-amber-100 text-amber-700',
  danger: 'bg-red-100 text-red-700',
  info: 'bg-blue-100 text-blue-700',
}

export function Badge({ variant = 'default', children }: BadgeProps): React.ReactElement {
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${VARIANT_CLASSES[variant]}`}>
      {children}
    </span>
  )
}
```

**File:** `components/shared/LoadingSpinner.tsx`
```tsx
import React from 'react'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  label?: string
}

const SIZE_CLASSES = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
}

export function LoadingSpinner({ size = 'md', label }: LoadingSpinnerProps): React.ReactElement {
  return (
    <div className="flex flex-col items-center justify-center gap-2">
      <div className={`${SIZE_CLASSES[size]} border-2 border-slate-200 border-t-blue-600 rounded-full animate-spin`} />
      {label && <span className="text-sm text-slate-500">{label}</span>}
    </div>
  )
}
```

**File:** `components/shared/ErrorMessage.tsx`
```tsx
import React from 'react'

interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}

export function ErrorMessage({ message, onRetry }: ErrorMessageProps): React.ReactElement {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
      <p className="text-red-700 mb-2">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-sm text-red-600 hover:text-red-800 underline"
        >
          Try again
        </button>
      )}
    </div>
  )
}
```

**File:** `components/shared/InfoBox.tsx`
```tsx
import React from 'react'

type InfoBoxVariant = 'success' | 'warning' | 'danger' | 'info'

interface InfoBoxProps {
  variant: InfoBoxVariant
  title?: string
  children: React.ReactNode
}

const VARIANT_CLASSES: Record<InfoBoxVariant, { bg: string; border: string; title: string }> = {
  success: { bg: 'bg-emerald-50', border: 'border-emerald-500', title: 'text-emerald-800' },
  warning: { bg: 'bg-amber-50', border: 'border-amber-500', title: 'text-amber-800' },
  danger: { bg: 'bg-red-50', border: 'border-red-500', title: 'text-red-800' },
  info: { bg: 'bg-blue-50', border: 'border-blue-500', title: 'text-blue-800' },
}

export function InfoBox({ variant, title, children }: InfoBoxProps): React.ReactElement {
  const classes = VARIANT_CLASSES[variant]
  return (
    <div className={`${classes.bg} border-l-4 ${classes.border} rounded-lg p-5 mb-4`}>
      {title && <h4 className={`font-semibold mb-2 ${classes.title}`}>{title}</h4>}
      <div className="text-slate-700">{children}</div>
    </div>
  )
}
```

---

## 6. PAGE IMPLEMENTATIONS

### 6.1 Dashboard Page (CRITICAL)

**File:** `pages/Dashboard.tsx`

```tsx
import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Layout } from '../components/layout/Layout'
import { PageHeader } from '../components/layout/PageHeader'
import { ConstitutionalBanner } from '../components/constitutional/ConstitutionalBanner'
import { SignalGrid } from '../components/signals/SignalGrid'
import { ContradictionPanel } from '../components/constitutional/ContradictionPanel'
import { ConfirmationPanel } from '../components/constitutional/ConfirmationPanel'
import { NarrativePanel } from '../components/constitutional/NarrativePanel'
import { InstrumentSelector } from '../components/signals/InstrumentSelector'
import { instrumentsApi, silosApi } from '../services/api'
import { LoadingSpinner } from '../components/shared/LoadingSpinner'

/**
 * Dashboard Page (Command Center)
 *
 * The main dashboard displaying signal overview, contradictions,
 * confirmations, and AI narrative.
 *
 * CRITICAL: ConstitutionalBanner MUST be displayed.
 *
 * @constitutional MN-01
 */
export function Dashboard(): React.ReactElement {
  const [selectedInstrumentId, setSelectedInstrumentId] = useState<string | null>(null)
  const [selectedSiloId, setSelectedSiloId] = useState<string | null>(null)

  // Fetch instruments
  const { data: instruments, isLoading: instrumentsLoading } = useQuery({
    queryKey: ['instruments', true],
    queryFn: () => instrumentsApi.list(true),
  })

  // Fetch silos for selected instrument
  const { data: silos } = useQuery({
    queryKey: ['silos', selectedInstrumentId],
    queryFn: () => silosApi.list(selectedInstrumentId ?? undefined, true),
    enabled: !!selectedInstrumentId,
  })

  // Auto-select first instrument and silo
  React.useEffect(() => {
    if (instruments?.length && !selectedInstrumentId) {
      setSelectedInstrumentId(instruments[0].instrument_id)
    }
  }, [instruments, selectedInstrumentId])

  React.useEffect(() => {
    if (silos?.length && !selectedSiloId) {
      setSelectedSiloId(silos[0].silo_id)
    }
  }, [silos, selectedSiloId])

  return (
    <Layout>
      <PageHeader
        badge="Dashboard"
        title="CIA-SIE Command Center"
        description="Chart Intelligence Auditor & Signal Intelligence Engine"
      />

      <div className="p-10 max-w-6xl">
        {/* CONSTITUTIONAL BANNER - MANDATORY */}
        <ConstitutionalBanner />

        {instrumentsLoading ? (
          <LoadingSpinner label="Loading instruments..." />
        ) : (
          <>
            {/* Instrument & Silo Selection */}
            <section className="mb-8">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="w-1 h-7 bg-blue-600 rounded"></span>
                Select Instrument
              </h2>
              <InstrumentSelector
                selectedId={selectedInstrumentId}
                onSelect={setSelectedInstrumentId}
              />

              {silos && silos.length > 1 && (
                <div className="mt-4">
                  <label className="block text-sm text-slate-600 mb-2">Silo</label>
                  <select
                    value={selectedSiloId ?? ''}
                    onChange={(e) => setSelectedSiloId(e.target.value)}
                    className="px-4 py-2 border border-slate-300 rounded-lg"
                  >
                    {silos.map((silo) => (
                      <option key={silo.silo_id} value={silo.silo_id}>
                        {silo.silo_name}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </section>

            {selectedSiloId && (
              <>
                {/* Signal Grid */}
                <section className="mb-8">
                  <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <span className="w-1 h-7 bg-blue-600 rounded"></span>
                    Signal Overview
                  </h2>
                  <SignalGrid siloId={selectedSiloId} />
                </section>

                {/* Relationships */}
                <section className="mb-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <ContradictionPanel siloId={selectedSiloId} />
                  <ConfirmationPanel siloId={selectedSiloId} />
                </section>

                {/* AI Narrative */}
                <section className="mb-8">
                  <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <span className="w-1 h-7 bg-blue-600 rounded"></span>
                    AI Narrative
                  </h2>
                  <NarrativePanel siloId={selectedSiloId} />
                </section>
              </>
            )}
          </>
        )}
      </div>
    </Layout>
  )
}
```

---

### 6.2 Other Pages (Condensed)

**File:** `pages/InstrumentList.tsx`
```tsx
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Layout } from '../components/layout/Layout'
import { PageHeader } from '../components/layout/PageHeader'
import { instrumentsApi } from '../services/api'
import { Badge } from '../components/shared/Badge'
import { LoadingSpinner } from '../components/shared/LoadingSpinner'

export function InstrumentList(): React.ReactElement {
  const navigate = useNavigate()
  const { data: instruments, isLoading } = useQuery({
    queryKey: ['instruments', false],
    queryFn: () => instrumentsApi.list(false),
  })

  return (
    <Layout>
      <PageHeader
        badge="Instruments"
        title="All Instruments"
        description="Manage your trading instruments"
      />
      <div className="p-10 max-w-4xl">
        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-600">Symbol</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-600">Name</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-600">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {instruments?.map((inst) => (
                  <tr
                    key={inst.instrument_id}
                    onClick={() => navigate(`/instruments/${inst.instrument_id}`)}
                    className="hover:bg-slate-50 cursor-pointer"
                  >
                    <td className="px-6 py-4 font-medium">{inst.symbol}</td>
                    <td className="px-6 py-4 text-slate-600">{inst.display_name}</td>
                    <td className="px-6 py-4">
                      <Badge variant={inst.is_active ? 'success' : 'danger'}>
                        {inst.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  )
}
```

---

## 7. STATE MANAGEMENT

### 7.1 Server State (React Query)

| State Type | Solution | Stale Time |
|------------|----------|------------|
| Instruments | `useQuery(['instruments'])` | 5 minutes |
| Silos | `useQuery(['silos', instrumentId])` | 5 minutes |
| Signals | `useQuery(['signals', chartId])` | 1 minute |
| Relationships | `useQuery(['relationships', siloId])` | 1 minute |
| Narratives | `useQuery(['narrative', siloId])` | 5 minutes |
| AI Models | `useQuery(['ai-models'])` | 10 minutes |
| AI Usage | `useQuery(['ai-usage', period])` | 1 minute |
| Chat History | `useQuery(['chat-history', instrumentId])` | Real-time |

### 7.2 Client State (React useState)

| State | Component | Purpose |
|-------|-----------|---------|
| `selectedInstrumentId` | Dashboard | Currently selected instrument |
| `selectedSiloId` | Dashboard | Currently selected silo |
| `sidebarOpen` | Layout | Mobile sidebar visibility |
| `selectedModel` | ChatPanel | AI model selection |

### 7.3 URL State (React Router)

| URL Pattern | Page | Params |
|-------------|------|--------|
| `/` | Dashboard | - |
| `/instruments` | InstrumentList | - |
| `/instruments/:id` | InstrumentDetail | `id: instrumentId` |
| `/silos/:id` | SiloDetail | `id: siloId` |
| `/charts` | ChartsReference | - |
| `/settings` | Settings | - |

---

## 8. API INTEGRATION

### 8.1 API Service Reference

The API service is fully implemented in `frontend/src/services/api.ts`. Use these objects:

| API Object | Methods |
|------------|---------|
| `instrumentsApi` | `list()`, `get()`, `getBySymbol()`, `create()`, `delete()` |
| `silosApi` | `list()`, `get()`, `create()`, `delete()` |
| `chartsApi` | `list()`, `get()`, `getByWebhook()`, `create()`, `delete()` |
| `signalsApi` | `listForChart()`, `getLatest()`, `get()` |
| `relationshipsApi` | `getForSilo()`, `getForInstrument()`, `getContradictions()` |
| `narrativesApi` | `generateForSilo()`, `getPlainText()` |
| `basketsApi` | `list()`, `get()`, `create()`, `addChart()`, `removeChart()`, `delete()` |
| `aiApi` | `listModels()`, `getUsage()`, `checkBudget()`, `configure()`, `healthCheck()` |
| `chatApi` | `sendMessage()`, `getHistory()` |
| `strategyApi` | `evaluate()` |

### 8.2 Hooks to Create

**File:** `hooks/useAI.ts`
```tsx
import { useQuery } from '@tanstack/react-query'
import { aiApi } from '../services/api'
import type { UsagePeriod } from '../types'

export function useAIModels() {
  return useQuery({
    queryKey: ['ai-models'],
    queryFn: () => aiApi.listModels(),
    staleTime: 10 * 60 * 1000,
  })
}

export function useAIUsage(period: UsagePeriod = 'monthly') {
  return useQuery({
    queryKey: ['ai-usage', period],
    queryFn: () => aiApi.getUsage(period),
    refetchInterval: 60000,
  })
}

export function useAIBudget() {
  return useQuery({
    queryKey: ['ai-budget'],
    queryFn: () => aiApi.checkBudget(),
    refetchInterval: 60000,
  })
}
```

**File:** `hooks/useChat.ts`
```tsx
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { chatApi } from '../services/api'
import type { ChatRequest } from '../types'

export function useChat(instrumentId: string) {
  const queryClient = useQueryClient()

  const history = useQuery({
    queryKey: ['chat-history', instrumentId],
    queryFn: () => chatApi.getHistory(instrumentId),
    enabled: !!instrumentId,
  })

  const sendMessage = useMutation({
    mutationFn: (request: ChatRequest) => chatApi.sendMessage(instrumentId, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-history', instrumentId] })
    },
  })

  return { history, sendMessage }
}
```

**File:** `hooks/useNarrative.ts`
```tsx
import { useQuery } from '@tanstack/react-query'
import { narrativesApi } from '../services/api'

export function useNarrative(siloId: string, useAi = true) {
  return useQuery({
    queryKey: ['narrative', siloId, useAi],
    queryFn: () => narrativesApi.generateForSilo(siloId, useAi),
    enabled: !!siloId,
    staleTime: 5 * 60 * 1000,
  })
}
```

---

## 9. CSS DESIGN SYSTEM

### 9.1 Color Palette (TailwindCSS)

| Variable | TailwindCSS | Hex |
|----------|-------------|-----|
| Primary | `blue-600` | #2563eb |
| Primary Dark | `blue-700` | #1d4ed8 |
| Background | `slate-50` | #f8fafc |
| Card | `white` | #ffffff |
| Text Primary | `slate-900` | #0f172a |
| Text Secondary | `slate-600` | #475569 |
| Text Muted | `slate-400` | #94a3b8 |
| Success | `emerald-500` | #10b981 |
| Warning | `amber-500` | #f59e0b |
| Danger | `red-500` | #ef4444 |
| Border | `slate-200` | #e2e8f0 |

### 9.2 Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| xs | 4px | `p-1` |
| sm | 8px | `p-2` |
| md | 16px | `p-4` |
| lg | 24px | `p-6` |
| xl | 40px | `p-10` |

### 9.3 Border Radius

| Name | Value | Class |
|------|-------|-------|
| Standard | 12px | `rounded-xl` |
| Small | 8px | `rounded-lg` |

### 9.4 Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| Mobile | < 768px | Default styles |
| Tablet | ≥ 768px | `md:` prefix |
| Desktop | ≥ 1024px | `lg:` prefix |

---

## 10. TESTING REQUIREMENTS

### 10.1 Unit Tests Required

| Component | Test File | Minimum Coverage |
|-----------|-----------|------------------|
| ConstitutionalBanner | `ConstitutionalBanner.test.tsx` | 100% |
| ContradictionAlert | `ContradictionAlert.test.tsx` | 100% |
| NarrativePanel | `NarrativePanel.test.tsx` | 100% |
| DirectionBadge | `DirectionBadge.test.tsx` | 100% |
| FreshnessIndicator | `FreshnessIndicator.test.tsx` | 100% |

### 10.2 Constitutional Compliance Tests

```tsx
// Example: ContradictionAlert.test.tsx
import { render, screen } from '@testing-library/react'
import { ContradictionAlert } from './ContradictionAlert'

describe('ContradictionAlert Constitutional Compliance', () => {
  const mockContradiction = {
    chart_a_id: '1',
    chart_a_name: 'Chart 01A',
    chart_a_direction: 'BULLISH' as const,
    chart_b_id: '2',
    chart_b_name: 'Chart 02',
    chart_b_direction: 'BEARISH' as const,
    detected_at: new Date().toISOString(),
  }

  it('displays both charts with equal visual size', () => {
    render(<ContradictionAlert contradiction={mockContradiction} />)

    const chartA = screen.getByText('Chart 01A').closest('div')
    const chartB = screen.getByText('Chart 02').closest('div')

    expect(chartA?.className).toContain('max-w-[200px]')
    expect(chartB?.className).toContain('max-w-[200px]')
  })

  it('displays mandatory disclaimer', () => {
    render(<ContradictionAlert contradiction={mockContradiction} />)

    expect(screen.getByText(/system does NOT resolve/i)).toBeInTheDocument()
  })

  it('uses neutral warning colors (amber/yellow)', () => {
    render(<ContradictionAlert contradiction={mockContradiction} />)

    const container = screen.getByText('CONTRADICTION DETECTED').closest('div')
    expect(container?.className).toContain('bg-amber')
  })
})
```

---

## 11. GOLD STANDARD VALIDATION CHECKLIST

### L1: Constitutional Compliance (MANDATORY - ALL MUST PASS)

- [ ] **CC-01**: No buy/sell buttons exist
- [ ] **CC-02**: No signal strength scores displayed
- [ ] **CC-03**: No chart weights displayed
- [ ] **CC-04**: No confidence percentages displayed
- [ ] **CC-05**: No "overall direction" aggregations
- [ ] **CC-06**: No price predictions
- [ ] **CC-07**: ConstitutionalBanner appears on Dashboard
- [ ] **CC-08**: Mandatory disclaimer on ALL AI output
- [ ] **CC-09**: Contradictions shown with equal visual weight
- [ ] **CC-10**: Freshness indicators on all signal displays

### L2: Component Implementation

- [ ] **CI-01**: All 22+ components implemented
- [ ] **CI-02**: All components have TypeScript types
- [ ] **CI-03**: All components handle loading states
- [ ] **CI-04**: All components handle error states
- [ ] **CI-05**: No console errors in development

### L3: API Integration

- [ ] **AI-01**: All hooks properly query-keyed
- [ ] **AI-02**: Error boundaries implemented
- [ ] **AI-03**: Loading spinners on async operations
- [ ] **AI-04**: Proper cache invalidation

### L4: UI/UX

- [ ] **UX-01**: Mobile responsive (< 900px)
- [ ] **UX-02**: Sidebar collapses on mobile
- [ ] **UX-03**: All interactive elements focusable
- [ ] **UX-04**: Consistent color scheme

### L5: Testing

- [ ] **TS-01**: Constitutional components 100% covered
- [ ] **TS-02**: All unit tests pass
- [ ] **TS-03**: No TypeScript errors
- [ ] **TS-04**: ESLint passes

---

## 12. PROHIBITED PATTERNS

### 12.1 Text Patterns (NEVER USE)

```
FORBIDDEN WORDS/PHRASES:
- "should" (implies recommendation)
- "recommend" (direct recommendation)
- "suggest" (implies recommendation)
- "consider" (implies recommendation)
- "buy now" / "sell now" (trading advice)
- "confidence: X%" (judgment)
- "probability" (prediction)
- "likely to profit" (prediction)
- "risk score" (judgment)
- "rating: X/10" (judgment)
- "overall direction" (aggregation)
- "net sentiment" (aggregation)
- "consensus view" (aggregation)
```

### 12.2 UI Patterns (NEVER IMPLEMENT)

```
FORBIDDEN UI ELEMENTS:
- Buy/Sell buttons
- Trade execution forms
- Signal strength meters
- Confidence bars
- Overall direction indicators
- Pie charts showing "bullish vs bearish"
- Any aggregation visualization
- "Take action" buttons
- Strategy recommendation cards
```

### 12.3 Data Patterns (NEVER DISPLAY)

```
FORBIDDEN DATA DISPLAYS:
- Chart.weight (doesn't exist, NEVER add)
- Signal.confidence (doesn't exist, NEVER add)
- Signal.strength (doesn't exist, NEVER add)
- Any "score" property
- Any "rating" property
- Any aggregated direction
```

---

## 13. PRE-COMMIT VERIFICATION

Before committing ANY code, run these checks:

```bash
# 1. TypeScript compilation
npm run tsc --noEmit

# 2. ESLint
npm run lint

# 3. Unit tests
npm test

# 4. Build
npm run build

# 5. Manual constitutional check
grep -r "should\|recommend\|suggest\|consider\|confidence\|probability" src/
# ↑ This should return ZERO matches in component code
```

### Automated Constitutional Check

Create this script: `scripts/constitutional-check.ts`

```typescript
import * as fs from 'fs'
import * as path from 'path'

const PROHIBITED_PATTERNS = [
  /\bshould\b/i,
  /\brecommend\b/i,
  /\bsuggest\b/i,
  /\bconsider\b/i,
  /\bbuy\s*now\b/i,
  /\bsell\s*now\b/i,
  /confidence:\s*\d+%/i,
  /\bprobability\b/i,
  /\brisk\s*score\b/i,
  /\brating:\s*\d+/i,
  /overall\s*direction/i,
  /net\s*sentiment/i,
]

function checkFile(filePath: string): boolean {
  const content = fs.readFileSync(filePath, 'utf-8')
  let hasViolation = false

  for (const pattern of PROHIBITED_PATTERNS) {
    if (pattern.test(content)) {
      console.error(`VIOLATION in ${filePath}: Found "${pattern}"`)
      hasViolation = true
    }
  }

  return !hasViolation
}

// Check all TSX files
const srcDir = path.join(__dirname, '../src')
// ... recursively check files
```

---

## APPENDIX A: 12 SAMPLE CHARTS REFERENCE

**File:** `constants/sampleCharts.ts`

```typescript
export const SAMPLE_CHARTS = [
  { code: '01A', name: 'Momentum Health', timeframe: 'Daily', webhookId: 'SAMPLE_01A' },
  { code: '02', name: 'HTF Structure', timeframe: 'Weekly', webhookId: 'SAMPLE_02' },
  { code: '04A', name: 'Risk Extension', timeframe: '3H', webhookId: 'SAMPLE_04A' },
  { code: '04B', name: 'Support/Resistance', timeframe: '3H', webhookId: 'SAMPLE_04B' },
  { code: '05A', name: 'VWAP Execution', timeframe: 'Daily', webhookId: 'SAMPLE_05A' },
  { code: '05B', name: 'Momentum Exhaustion', timeframe: 'Daily', webhookId: 'SAMPLE_05B' },
  { code: '05C', name: 'Extension Risk', timeframe: 'Daily', webhookId: 'SAMPLE_05C' },
  { code: '05D', name: 'VWAP Deviation', timeframe: 'Daily', webhookId: 'SAMPLE_05D' },
  { code: '06', name: 'Macro Correlation', timeframe: 'Daily', webhookId: 'SAMPLE_06' },
  { code: '07', name: 'Primary Trend', timeframe: 'Daily', webhookId: 'SAMPLE_07' },
  { code: '08', name: 'Volume Analysis', timeframe: 'Daily', webhookId: 'SAMPLE_08' },
  { code: '09', name: 'Order Flow', timeframe: 'Daily', webhookId: 'SAMPLE_09' },
] as const

export type SampleChart = typeof SAMPLE_CHARTS[number]
```

---

## APPENDIX B: QUICK REFERENCE COMMANDS

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Type check
npm run tsc --noEmit

# Lint
npm run lint

# Format
npm run format
```

---

## DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-03 | Claude Code (Opus 4.5) | Initial comprehensive handoff |

---

**END OF AUTONOMOUS HANDOFF DOCUMENT**

This document is self-contained and enables fully autonomous implementation of the CIA-SIE frontend. All specifications, code examples, validation checklists, and prohibited patterns are included. No additional context or documentation is required.
