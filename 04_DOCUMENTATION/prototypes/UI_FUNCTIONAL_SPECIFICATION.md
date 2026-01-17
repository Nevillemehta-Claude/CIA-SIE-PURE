# CIA-SIE UI Functional Specification
## Complete Element-by-Element Wireframe Documentation

**Version**: 1.0.0  
**Date**: January 5, 2026  
**Purpose**: Define every visual element, its function, user interaction, and system effects

---

## Table of Contents

1. [Global Elements](#1-global-elements)
2. [Frontend Dashboard](#2-frontend-dashboard)
3. [Instrument Detail](#3-instrument-detail)
4. [Silo Detail](#4-silo-detail)
5. [Chart Detail](#5-chart-detail)
6. [Basket List](#6-basket-list)
7. [Basket Detail](#7-basket-detail)
8. [AI Chat](#8-ai-chat)
9. [AI Settings](#9-ai-settings)
10. [MCC Dashboard](#10-mcc-dashboard)
11. [MCC Process Management](#11-mcc-process-management)
12. [MCC Log Viewer](#12-mcc-log-viewer)
13. [MCC Settings](#13-mcc-settings)
14. [User Flow Diagrams](#14-user-flow-diagrams)

---

## 1. Global Elements

These elements appear consistently across all screens.

### 1.1 Header Navigation Bar

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [Logo]  CIA-SIE    │  Dashboard  │  Instruments  │  Baskets  │  AI Chat   │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Element | Visual | Purpose | User Action | Before State | After State |
|---------|--------|---------|-------------|--------------|-------------|
| **Logo Icon** | 40×40px gradient box with chart icon | Brand identity, home navigation | Click | Current page | Navigates to Dashboard |
| **Logo Text** | "CIA-SIE" bold text | Brand reinforcement | Click | Current page | Navigates to Dashboard |
| **Dashboard Link** | Text button | Navigate to main overview | Click | Current page | Dashboard loads, link highlighted |
| **Instruments Link** | Text button | Navigate to instruments list | Click | Current page | Instrument list loads |
| **Baskets Link** | Text button | Navigate to baskets list | Click | Current page | Basket list loads |
| **AI Chat Link** | Text button | Open conversational AI | Click | Current page | Chat interface loads |

**Active State Behavior**:
- Current page link: Teal background (#0D9488), white text
- Other links: Gray text, hover shows light gray background

---

### 1.2 Constitutional Disclaimer Banner

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⚠️  Decision-Support Only: This system provides information for           │
│      decision-support only. All trading decisions remain solely your       │
│      responsibility.                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Element | Visual | Purpose | Constitutional Rule | User Action | Effect |
|---------|--------|---------|---------------------|-------------|--------|
| **Warning Icon** | Yellow triangle with "!" | Draw attention | CR-003 | None (display only) | N/A |
| **Disclaimer Text** | Yellow background, amber border | Legal protection, user reminder | CR-003: Immutable | **NONE ALLOWED** | Cannot be dismissed, hidden, or collapsed |

**CRITICAL**: This element is:
- ✅ Always visible on every page with data
- ✅ Non-dismissible (no X button)
- ✅ Non-collapsible (no minimize)
- ✅ Text is hardcoded (cannot be changed by backend)

---

### 1.3 Breadcrumb Navigation

```
Dashboard  >  NIFTY 50  >  Momentum Silo  >  NIFTY_MOM_5M
```

| Element | Visual | Purpose | User Action | Before State | After State |
|---------|--------|---------|-------------|--------------|-------------|
| **Parent Link** | Gray text with hover effect | Navigate up hierarchy | Click | Current detail page | Parent page loads |
| **Separator** | ">" chevron icon | Visual hierarchy indicator | None | N/A | N/A |
| **Current Page** | Black bold text | Show current location | None (not clickable) | N/A | N/A |

---

### 1.4 Direction Badges

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  ▲ BULLISH   │   │  ▼ BEARISH   │   │  ─ NEUTRAL   │
└──────────────┘   └──────────────┘   └──────────────┘
    Green              Red               Gray
```

| Badge | Background | Text Color | Arrow | Purpose |
|-------|------------|------------|-------|---------|
| **BULLISH** | #D1FAE5 (light green) | #10B981 (emerald) | ▲ | Indicates upward directional bias |
| **BEARISH** | #FEE2E2 (light red) | #EF4444 (red) | ▼ | Indicates downward directional bias |
| **NEUTRAL** | #F3F4F6 (light gray) | #6B7280 (gray) | ─ | Indicates no clear directional bias |

**Constitutional Compliance (CR-002)**:
- All three badges have **IDENTICAL sizes** (no larger badge for "stronger" signal)
- All three badges have **EQUAL visual weight** (similar saturation/contrast)

---

### 1.5 Freshness Badges

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────────┐
│  ● CURRENT │   │  ● RECENT  │   │  ● STALE   │   │ ● UNAVAILABLE  │
└────────────┘   └────────────┘   └────────────┘   └────────────────┘
    Green            Yellow           Orange            Gray
```

| Badge | Meaning | Threshold | Visual |
|-------|---------|-----------|--------|
| **CURRENT** | Signal is fresh | < heartbeat interval | Green dot + text |
| **RECENT** | Signal is aging | < 2× heartbeat | Yellow dot + text |
| **STALE** | Signal is old | > 2× heartbeat | Orange dot + text |
| **UNAVAILABLE** | No signal received | Never received or error | Gray dot + text |

**Purpose**: Purely informational. Does NOT affect signal validity or weight.

---

### 1.6 Standard Button Styles

| Button Type | Background | Text | Border | Use Case |
|-------------|------------|------|--------|----------|
| **Primary** | #0D9488 (teal) | White | None | Main actions (Save, Create, Generate) |
| **Secondary** | #F4F5F7 (gray) | Gray text | 1px gray | Secondary actions (Cancel, Edit) |
| **Danger** | Transparent | Red | 1px red | Destructive actions (Delete) |
| **Ghost** | Transparent | Gray | None | Minimal actions (inline links) |

**Interaction States**:
| State | Visual Change |
|-------|---------------|
| Hover | Slight darken (10%) |
| Active/Pressed | Slight darken (15%) |
| Disabled | 50% opacity, cursor: not-allowed |
| Loading | Spinner replaces icon |

---

## 2. Frontend Dashboard

**URL**: `/`  
**Purpose**: Provide an at-a-glance overview of all instruments and system status

### 2.1 Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HEADER NAVIGATION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Signal Intelligence Dashboard                          [+ Add Instrument]  │
│  Real-time signal monitoring across all instruments                         │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                         CONSTITUTIONAL DISCLAIMER                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ INSTRUMENTS │ │   SILOS     │ │   CHARTS    │ │  SIGNALS    │            │
│  │     5       │ │     12      │ │     47      │ │   1,247     │            │
│  │   Active    │ │ Configured  │ │  Monitored  │ │   Today     │            │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘            │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Instruments                                                                 │
│  ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ │
│  │ NIFTY 50             │ │ BANKNIFTY            │ │ RELIANCE             │ │
│  │ NSE:NIFTY            │ │ NSE:BANKNIFTY        │ │ NSE:RELIANCE         │ │
│  │ 3 Silos • 12 Charts  │ │ 2 Silos • 8 Charts   │ │ 2 Silos • 6 Charts   │ │
│  │ [===========] 100%   │ │ [========  ] 75%     │ │ [======    ] 60%     │ │
│  │                      │ │                      │ │                      │ │
│  │ View Details →       │ │ View Details →       │ │ View Details →       │ │
│  └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Element Specifications

#### Summary Statistics Cards

| Element | Purpose | Data Source | User Action | Effect |
|---------|---------|-------------|-------------|--------|
| **Instruments Count** | Show total active instruments | GET /api/v1/instruments | None (display) | N/A |
| **Silos Count** | Show total configured silos | Aggregated from instruments | None (display) | N/A |
| **Charts Count** | Show total monitored charts | Aggregated from silos | None (display) | N/A |
| **Signals Today** | Show signals received today | GET /api/v1/signals?today=true | None (display) | N/A |

#### Add Instrument Button

| Element | Visual | User Action | Before State | After State |
|---------|--------|-------------|--------------|-------------|
| **[+ Add Instrument]** | Teal primary button | Click | Dashboard visible | Modal opens with form |

**Modal Form Fields**:
| Field | Type | Validation | Purpose |
|-------|------|------------|---------|
| Symbol | Text input | Required, unique | Trading symbol (e.g., "NIFTY") |
| Exchange | Dropdown | Required | Exchange identifier (NSE, BSE) |
| Description | Text area | Optional | Human-readable description |

**Form Submission Flow**:
```
User fills form → Click "Create" → POST /api/v1/instruments → 
Success: Modal closes, instrument appears in grid, toast "Instrument created"
Error: Inline validation message, modal stays open
```

#### Instrument Cards

| Element | Purpose | User Action | Before State | After State |
|---------|---------|-------------|--------------|-------------|
| **Instrument Name** | Primary identifier | Click | Dashboard | Instrument Detail page |
| **Symbol** | Exchange:Symbol format | None (display) | N/A | N/A |
| **Silo/Chart Count** | Quick stats | None (display) | N/A | N/A |
| **Freshness Bar** | % of charts with CURRENT status | None (display) | N/A | N/A |
| **View Details →** | Navigation CTA | Click | Dashboard | Instrument Detail page |
| **Entire Card** | Clickable container | Click | Dashboard | Instrument Detail page |

**Card Hover Behavior**:
- Shadow deepens
- Border color changes to teal
- Slight upward translate (-2px)

---

## 3. Instrument Detail

**URL**: `/instruments/:instrumentId`  
**Purpose**: Show all silos for a specific instrument with summary statistics

### 3.1 Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HEADER NAVIGATION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Dashboard > NIFTY 50                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [Icon] NIFTY 50                                        [Edit] [Delete]     │
│         NSE:NIFTY • Index                                                    │
│         Created: Jan 1, 2026 • Last Signal: 2 min ago                       │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                         CONSTITUTIONAL DISCLAIMER                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Silos                                                   [+ Add Silo]        │
│  ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ │
│  │ 📊 Momentum          │ │ 📈 Trend             │ │ 📉 Volume            │ │
│  │ RSI + MACD           │ │ EMA Cross            │ │ OBV + Volume         │ │
│  │ 4 Charts             │ │ 3 Charts             │ │ 2 Charts             │ │
│  │ Heartbeat: 5 min     │ │ Heartbeat: 15 min    │ │ Heartbeat: 1 hour    │ │
│  │                      │ │                      │ │                      │ │
│  │ ┌────┐ ┌────┐       │ │ ┌────┐ ┌────┐       │ │ ┌────┐ ┌────┐       │ │
│  │ │BULL│ │BEAR│ ...   │ │ │BULL│ │BULL│       │ │ │BEAR│ │NEUT│       │ │
│  │ └────┘ └────┘       │ │ └────┘ └────┘       │ │ └────┘ └────┘       │ │
│  │                      │ │                      │ │                      │ │
│  │ View Silo →         │ │ View Silo →         │ │ View Silo →         │ │
│  └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  Contradictions (1)                                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ┌─────────────┐      ⚡ CONFLICTS      ┌─────────────┐                │  │
│  │ │ NIFTY_MOM_5M│         WITH          │NIFTY_MOM_15M│                │  │
│  │ │  ▲ BULLISH  │                       │  ▼ BEARISH  │                │  │
│  │ └─────────────┘                       └─────────────┘                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Element Specifications

#### Page Header

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Instrument Icon** | Visual identifier | None | N/A |
| **Instrument Name** | Primary title | None | N/A |
| **Symbol + Type** | Metadata | None | N/A |
| **Timestamps** | Creation and activity | None | N/A |
| **[Edit] Button** | Modify instrument | Click | Opens edit modal |
| **[Delete] Button** | Remove instrument | Click | Opens confirmation dialog |

**Delete Confirmation Flow**:
```
User clicks Delete → Confirmation modal appears:
  "Are you sure you want to delete NIFTY 50? 
   This will remove all silos, charts, and signal history."
  [Cancel] [Delete]
  
User clicks Delete → DELETE /api/v1/instruments/:id → 
  Success: Navigate to Dashboard, toast "Instrument deleted"
  Error: Toast error message
```

#### Silo Cards

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Silo Icon** | Category indicator | None | N/A |
| **Silo Name** | Primary identifier | Click | Navigate to Silo Detail |
| **Description** | Indicator types | None | N/A |
| **Chart Count** | Quick stat | None | N/A |
| **Heartbeat** | Freshness interval | None | N/A |
| **Mini Direction Badges** | Preview of chart signals | None | Shows current direction of each chart |
| **View Silo →** | Navigation CTA | Click | Navigate to Silo Detail |

**Constitutional Note (CR-002)**: Mini direction badges are displayed in a **horizontal row with equal spacing**. No badge is larger or more prominent than another.

#### Contradictions Panel

| Element | Purpose | Constitutional Rule | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **Section Header** | Identify contradictions | CR-002 | None | N/A |
| **Left Chart Box** | First conflicting chart | CR-002: Equal size | Click | Navigate to Chart Detail |
| **Conflict Separator** | Neutral visual divider | CR-002: No bias | None | N/A |
| **Right Chart Box** | Second conflicting chart | CR-002: Equal size | Click | Navigate to Chart Detail |

**CRITICAL (CR-002)**:
- Both boxes are **IDENTICAL in size** (not "primary vs secondary")
- Both boxes have **IDENTICAL styling** (no color difference implying priority)
- Separator is **NEUTRAL** (yellow/amber, not green/red)

---

## 4. Silo Detail

**URL**: `/instruments/:instrumentId/silos/:siloId`  
**Purpose**: Display all charts within a silo, contradictions, confirmations, and AI narrative

### 4.1 Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HEADER NAVIGATION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Dashboard > NIFTY 50 > Momentum Silo                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [Icon] Momentum Silo                                   [Edit] [Delete]     │
│         NIFTY 50 • RSI, MACD Indicators                                      │
│         Heartbeat: 5 min | Current < 2min | Recent < 10min | Stale > 30min  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                         CONSTITUTIONAL DISCLAIMER                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Charts in this Silo (4 charts)                          [+ Add Chart]       │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐│
│  │ NIFTY_MOM_5M   │ │ NIFTY_MOM_15M  │ │ NIFTY_MOM_1H   │ │ NIFTY_MOM_4H   ││
│  │ RSI+MACD • 5m  │ │ RSI+MACD • 15m │ │ RSI+MACD • 1H  │ │ RSI+MACD • 4H  ││
│  │ ▲ BULLISH      │ │ ▼ BEARISH      │ │ ▲ BULLISH      │ │ ─ NEUTRAL      ││
│  │ ● CURRENT      │ │ ● CURRENT      │ │ ● RECENT       │ │ ● STALE        ││
│  │ Updated: 2 min │ │ Updated: 3 min │ │ Updated: 8 min │ │ Updated: 45 min││
│  │ View Chart →   │ │ View Chart →   │ │ View Chart →   │ │ View Chart →   ││
│  └────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘│
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ ✓ CR-002: All charts displayed with EQUAL visual weight              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  Contradictions (1)                                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     [Same as Instrument Detail]                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  Confirmations (1)                                                           │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ┌─────────────┐      ✓ ALIGNS       ┌─────────────┐                   │  │
│  │ │ NIFTY_MOM_5M│        WITH         │ NIFTY_MOM_1H│                   │  │
│  │ │  ▲ BULLISH  │                     │  ▲ BULLISH  │                   │  │
│  │ └─────────────┘                     └─────────────┘                   │  │
│  │ ┌────────────────────────────────────────────────────────────────┐    │  │
│  │ │ ℹ️ Note: Confirmation does NOT mean "stronger signal"          │    │  │
│  │ └────────────────────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  AI Narrative                                            [Generate New]      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🤖 AI-Generated Description                                           │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ The Momentum Silo for NIFTY 50 currently shows mixed signals...       │  │
│  │ [Full narrative text]                                                 │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ ⚠️ MANDATORY DISCLAIMER (CR-003): This analysis is generated by AI   │  │
│  │    for informational purposes only. It does not constitute financial  │  │
│  │    advice. All trading decisions are solely your responsibility.      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Element Specifications

#### Charts Grid

| Element | Purpose | Constitutional Rule | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **Grid Layout** | 4 columns, equal width | CR-002: Equal visual weight | N/A | N/A |
| **Chart Card** | Container for chart info | CR-002: All same size | Click | Navigate to Chart Detail |
| **Chart Name** | Identifier | None | Click | Navigate to Chart Detail |
| **Timeframe** | Period + indicators | None | None | N/A |
| **Direction Badge** | Current signal direction | CR-002: No priority | None | N/A |
| **Freshness Badge** | Signal age status | Informational only | None | N/A |
| **Timestamp** | Last update time | None | None | N/A |
| **CR-002 Notice** | Constitutional reminder | Mandatory display | None | N/A |

#### Confirmations Panel

| Element | Purpose | Constitutional Rule | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **Section Header** | Identify confirmations | None | None | N/A |
| **Chart Boxes** | Two aligned charts | CR-002: Equal | Click | Navigate to Chart Detail |
| **Separator** | Green checkmark + "ALIGNS WITH" | Neutral | None | N/A |
| **Info Notice** | Anti-aggregation warning | CR-001 | None (display only) | N/A |

**Info Notice Text (Mandatory)**:
> "Confirmation does NOT mean 'stronger signal' — it is informational only. No aggregation is performed."

#### AI Narrative Section

| Element | Purpose | Constitutional Rule | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **Section Header** | Identify AI content | None | None | N/A |
| **[Generate New]** | Request fresh narrative | None | Click | API call, loading state, new narrative appears |
| **Narrative Body** | AI-generated description | CR-001, CR-003 | None (read only) | N/A |
| **Mandatory Disclaimer** | Legal/constitutional protection | CR-003: Non-removable | **NONE** | Cannot be hidden |

**Generate New Button Flow**:
```
User clicks [Generate New] → 
Button shows spinner, disabled → 
POST /api/v1/narratives/:siloId → 
AI generates description → 
Backend validates (no prohibited phrases) → 
Success: New narrative replaces old, toast "Narrative generated"
Error: Toast error, old narrative remains
```

**Narrative Validation (Backend)**:
The narrative MUST NOT contain:
- "you should", "I recommend", "consider buying/selling"
- "overall direction", "net bullish/bearish"
- Confidence scores, probability percentages
- Any prescriptive or advisory language

---

## 5. Chart Detail

**URL**: `/instruments/:instrumentId/silos/:siloId/charts/:chartId`  
**Purpose**: Display individual chart with current signal, history, and basket memberships

### 5.1 Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HEADER NAVIGATION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Dashboard > NIFTY 50 > Momentum Silo > NIFTY_MOM_5M                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [Icon] NIFTY_MOM_5M                                    [Edit] [Delete]     │
│         RSI + MACD • 5 Minute Timeframe                                      │
│         Momentum Silo • Created: Dec 15, 2025                               │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                         CONSTITUTIONAL DISCLAIMER                            │
├─────────────────────────────────────────────┬────────────────────────────────┤
│                                             │                                │
│  Current Signal                             │  Chart Details                 │
│  ┌───────────────────────────────────┐      │  ┌────────────────────────┐   │
│  │                                   │      │  │ Instrument: NIFTY 50   │   │
│  │            ▲                      │      │  │ Silo: Momentum         │   │
│  │                                   │      │  │ Timeframe: 5 Minute    │   │
│  │         BULLISH                   │      │  │ Indicators: RSI, MACD  │   │
│  │                                   │      │  │ Chart ID: c7a8b9d0...  │   │
│  │       ● CURRENT                   │      │  │ Total Signals: 1,247   │   │
│  │                                   │      │  └────────────────────────┘   │
│  │  Received: 2025-01-05 10:32:45    │      │                                │
│  └───────────────────────────────────┘      │  In Baskets                [+]│
│                                             │  ┌────────────────────────┐   │
│  Signal History (Last 10)                   │  │ 📁 Short-Term Momentum │   │
│  ┌───────────────────────────────────┐      │  │    LOGICAL             │   │
│  │ BULLISH  │ 10:32:45 │ CURRENT    │      │  ├────────────────────────┤   │
│  │ BEARISH  │ 10:27:12 │ RECENT     │      │  │ 📁 NIFTY Quick Signals │   │
│  │ BEARISH  │ 10:22:08 │ STALE      │      │  │    HIERARCHICAL        │   │
│  │ NEUTRAL  │ 10:17:33 │ STALE      │      │  └────────────────────────┘   │
│  │ BULLISH  │ 10:12:01 │ STALE      │      │                                │
│  └───────────────────────────────────┘      │                                │
│                                             │                                │
│  ┌───────────────────────────────────┐      │                                │
│  │ ✓ CR-001: This chart has NO      │      │                                │
│  │   weight. All charts are equal.   │      │                                │
│  └───────────────────────────────────┘      │                                │
│                                             │                                │
└─────────────────────────────────────────────┴────────────────────────────────┘
```

### 5.2 Element Specifications

#### Current Signal Display

| Element | Purpose | Visual | User Action | Effect |
|---------|---------|--------|-------------|--------|
| **Large Arrow** | Direction indicator | 64px ▲ or ▼ | None | N/A |
| **Direction Text** | Signal direction | Large bold text | None | N/A |
| **Freshness Badge** | Signal age | Colored badge | None | N/A |
| **Timestamp** | Exact signal time | Monospace font | None | N/A |

#### Signal History Table

| Column | Purpose | Format | User Action | Effect |
|--------|---------|--------|-------------|--------|
| **Direction** | Historical direction | Badge | None | N/A |
| **Time** | When received | HH:MM:SS | None | N/A |
| **Freshness** | Status at receipt | Badge | None | N/A |

**Note**: History is **read-only**. No aggregation or trend analysis is performed.

#### Baskets Panel

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **[+] Button** | Add to basket | Click | Opens basket selection modal |
| **Basket Item** | Shows membership | Click | Navigate to Basket Detail |
| **Basket Type Badge** | Classification | None | N/A |

**Add to Basket Modal**:
```
┌─────────────────────────────────────────┐
│  Add to Basket                          │
├─────────────────────────────────────────┤
│  Select basket(s):                      │
│  ☐ Short-Term Momentum (LOGICAL)        │
│  ☑ NIFTY Quick Signals (HIERARCHICAL)   │
│  ☐ Favorites (CUSTOM)                   │
│  ☐ + Create New Basket                  │
├─────────────────────────────────────────┤
│           [Cancel]  [Add to Selected]   │
└─────────────────────────────────────────┘
```

---

## 6. Basket List

**URL**: `/baskets`  
**Purpose**: Display all analytical baskets with filtering by type

### 6.1 Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HEADER NAVIGATION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Analytical Baskets                                      [+ Create Basket]  │
│  Organize and compare charts across different groupings                     │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ℹ️ Baskets are UI-only constructs                                      │ │
│  │    Baskets help you organize charts for comparison and viewing.        │ │
│  │    They have NO effect on signal processing, weighting, or aggregation.│ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────┤
│  [All Baskets] [Logical] [Hierarchical] [Contextual] [Custom]               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ │
│  │ 📁 Short-Term        │ │ 🔀 NIFTY Multi-TF    │ │ 🧭 Market Open       │ │
│  │    Momentum          │ │    HIERARCHICAL      │ │    Analysis          │ │
│  │    LOGICAL           │ │                      │ │    CONTEXTUAL        │ │
│  │                      │ │                      │ │                      │ │
│  │ 8 Charts • 3 Instr.  │ │ 12 Charts • 1 Instr. │ │ 6 Charts • 2 Instr.  │ │
│  │ Updated: 5 min ago   │ │ Updated: 12 min ago  │ │ Updated: 1 hour ago  │ │
│  │ View Basket →        │ │ View Basket →        │ │ View Basket →        │ │
│  └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Element Specifications

#### Info Banner

| Element | Purpose | Constitutional Rule | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **Info Icon** | Visual indicator | None | None | N/A |
| **Banner Text** | Explain basket purpose | CR-001: No aggregation | None (display only) | N/A |

**Banner Text (Mandatory)**:
> "Baskets help you organize charts for comparison and viewing purposes. They have NO effect on signal processing, weighting, or aggregation. Charts can belong to multiple baskets."

#### Filter Buttons

| Button | Purpose | User Action | Effect |
|--------|---------|-------------|--------|
| **All Baskets** | Show all | Click | Full list, button highlighted |
| **Logical** | Filter by type | Click | Only LOGICAL baskets shown |
| **Hierarchical** | Filter by type | Click | Only HIERARCHICAL baskets shown |
| **Contextual** | Filter by type | Click | Only CONTEXTUAL baskets shown |
| **Custom** | Filter by type | Click | Only CUSTOM baskets shown |

**Active State**: Selected filter has teal background and white text.

#### Basket Cards

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Basket Icon** | Type indicator (color-coded) | None | N/A |
| **Basket Name** | Primary identifier | Click | Navigate to Basket Detail |
| **Type Badge** | Classification | None | N/A |
| **Description** | Purpose explanation | None | N/A |
| **Chart/Instrument Count** | Quick stats | None | N/A |
| **Updated Timestamp** | Last modification | None | N/A |
| **View Basket →** | Navigation CTA | Click | Navigate to Basket Detail |

**Basket Type Colors**:
| Type | Icon | Badge Color |
|------|------|-------------|
| LOGICAL | Layers | Blue (#3B82F6) |
| HIERARCHICAL | Git Branch | Pink (#EC4899) |
| CONTEXTUAL | Compass | Teal (#14B8A6) |
| CUSTOM | Star | Purple (#A855F7) |

---

## 7. Basket Detail

**URL**: `/baskets/:basketId`  
**Purpose**: View and manage charts within a specific basket

### 7.1 Element Specifications

#### Summary Statistics

| Element | Purpose | Constitutional Note | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **Total Charts** | Count | N/A | None | N/A |
| **Bullish Count** | Charts with BULLISH | Display only, NOT aggregation | None | N/A |
| **Bearish Count** | Charts with BEARISH | Display only, NOT aggregation | None | N/A |
| **Neutral Count** | Charts with NEUTRAL | Display only, NOT aggregation | None | N/A |

**Warning Banner (Mandatory)**:
> "⚠️ Note: The summary counts above are for informational display only. They do NOT represent aggregation, weighting, or any form of scoring."

#### Charts Grid

Same as Silo Detail, with additional:

| Element | Purpose | User Action | Before State | After State |
|---------|---------|-------------|--------------|-------------|
| **[X] Remove Button** | Remove chart from basket | Click | Button hidden | Confirmation: "Remove from basket?" |
| | | Confirm | Chart in basket | Chart removed, grid updates |

**Remove Flow**:
```
User hovers card → [X] button appears (top right)
User clicks [X] → Confirmation toast: "Remove NIFTY_MOM_5M from this basket?"
                  [Cancel] [Remove]
User clicks Remove → DELETE /api/v1/baskets/:id/charts/:chartId
Success: Card fades out, counts update
```

---

## 8. AI Chat

**URL**: `/chat`  
**Purpose**: Conversational interface for AI-powered signal analysis

### 8.1 Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HEADER NAVIGATION                                 │
├─────────────────────┬───────────────────────────────────────────────────────┤
│                     │                                                        │
│  AI Conversations   │  [NIFTY 50]                    Model: [Claude Haiku ▼]│
│  Descriptive only   │                                                        │
│                     ├────────────────────────────────────────────────────────┤
│  Select Instrument: │                                                        │
│  [NIFTY 50      ▼]  │  You: What are the current signals showing?            │
│                     │                                                        │
│  ┌───────────────┐  │  ┌──────────────────────────────────────────────────┐ │
│  │ NIFTY Signal  │  │  │ 🤖 AI:                                            │ │
│  │ Analysis      │  │  │                                                   │ │
│  │ Today 10:35   │  │  │ Here is a description of the current signals...  │ │
│  ├───────────────┤  │  │                                                   │ │
│  │ BANKNIFTY     │  │  │ [Full response text]                              │ │
│  │ Contradictions│  │  │                                                   │ │
│  │ Today 9:15    │  │  │ ┌──────────────────────────────────────────────┐ │ │
│  └───────────────┘  │  │ │ ⚠️ DISCLAIMER: This analysis is generated    │ │ │
│                     │  │ │    by AI for informational purposes only...   │ │ │
│                     │  │ └──────────────────────────────────────────────┘ │ │
│  [+ New Chat]       │  └──────────────────────────────────────────────────┘ │
│                     │                                                        │
│                     ├────────────────────────────────────────────────────────┤
│                     │ [Type your message...                          ] [➤]  │
│                     │ ℹ️ AI responses are descriptive only.                  │
│                     │    No recommendations or predictions provided.         │
└─────────────────────┴────────────────────────────────────────────────────────┘
```

### 8.2 Element Specifications

#### Sidebar

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Title** | Section label | None | N/A |
| **Instrument Dropdown** | Select context | Change selection | New conversation starts for that instrument |
| **Conversation List** | History | Click item | Load that conversation |
| **[+ New Chat]** | Start fresh | Click | Clear chat, ready for new messages |

#### Chat Header

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Instrument Badge** | Current context | None | N/A |
| **Model Dropdown** | Select AI tier | Change selection | Future messages use selected model |

**Model Options**:
| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| Claude Haiku | ~1s | $0.001/query | Quick questions |
| Claude Sonnet | ~3s | $0.008/query | Detailed analysis |
| Claude Opus | ~8s | $0.040/query | Complex multi-silo narratives |

#### Message Display

| Element | Purpose | Constitutional Rule | User Action | Effect |
|---------|---------|---------------------|-------------|--------|
| **User Message** | Display user input | None | None | N/A |
| **AI Message** | Display AI response | CR-001, CR-003 | None | N/A |
| **Inline Disclaimer** | Per-message warning | CR-003: Mandatory | **NONE** | Cannot be hidden |
| **Timestamp** | When sent | None | None | N/A |
| **Model Badge** | Which AI used | None | None | N/A |

**Message Styling**:
- User: Teal background, right-aligned
- AI: White background with border, left-aligned

#### Input Area

| Element | Purpose | User Action | Before State | After State |
|---------|---------|-------------|--------------|-------------|
| **Text Input** | Compose message | Type | Empty/previous text | Text appears |
| **Send Button** | Submit message | Click | Enabled | Disabled during send |
| **Hint Text** | Reminder | None (display only) | N/A | N/A |

**Send Flow**:
```
User types message → Clicks Send (or Enter) →
Input disabled, button shows spinner →
POST /api/v1/chat/:instrumentId →
Backend validates response (no prohibited phrases) →
Success: AI message appears with disclaimer, input clears
Error: Toast error, input re-enabled
```

**Prohibited Response Check**:
If AI response contains prohibited phrases, backend:
1. Retries generation (up to 3 times)
2. If all fail, returns fallback: "Unable to generate a compliant response. Please try rephrasing your question."

---

## 9. AI Settings

**URL**: `/settings/ai`  
**Purpose**: Manage AI model preferences and usage budget

### 9.1 Element Specifications

#### Budget Section

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Spent This Month** | Current usage | None (display) | N/A |
| **Remaining** | Available budget | None (display) | N/A |
| **Monthly Limit** | Maximum allowed | Edit | Updates limit on save |
| **Progress Bar** | Visual usage | None (display) | N/A |
| **Warning Threshold** | Alert percentage | Edit | Triggers notification when reached |

#### Model Selection

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Model Cards** | Display options | Click | Selects as default |
| **Radio Indicator** | Shows selection | Click | Changes default model |
| **Speed/Cost Stats** | Comparison | None (display) | N/A |

#### Preference Toggles

| Toggle | Default | Purpose |
|--------|---------|---------|
| Auto-generate Narratives | ON | Generate AI narrative when viewing silos |
| Include Freshness Context | ON | Add freshness info to AI prompts |
| Verbose Contradictions | OFF | Detailed contradiction explanations |
| Budget Alerts | ON | Notify when approaching limit |

---

## 10. MCC Dashboard

**URL**: Electron app main screen  
**Purpose**: System overview with process status and health checks

### 10.1 Element Specifications

#### Process Status Cards

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Backend Card** | Show API status | Click [Start]/[Stop] | Process starts/stops |
| **Frontend Card** | Show UI status | Click [Start]/[Stop] | Process starts/stops |
| **Status Badge** | Running/Stopped/Error | None | N/A |
| **Quick Stats** | CPU/Memory/Uptime | None | N/A |

**Status Badge States**:
| State | Color | Dot Animation |
|-------|-------|---------------|
| Running | Green | Pulsing |
| Starting | Yellow | Pulsing fast |
| Stopped | Gray | None |
| Error | Red | None |

#### Health Check Panel

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Service Cards** | Show health status | None | N/A |
| **Status Icon** | Healthy/Degraded/Unhealthy | None | N/A |
| **Latency** | Response time | None | N/A |

#### Quick Actions

| Button | Purpose | User Action | Effect |
|--------|---------|-------------|--------|
| **Start All** | Launch everything | Click | Backend starts, then Frontend |
| **Stop All** | Shutdown everything | Click | Frontend stops, then Backend |
| **Restart All** | Full restart | Click | Stop All, then Start All |
| **Open Frontend** | Browser launch | Click | Opens localhost:5173 in browser |

---

## 11. MCC Process Management

**URL**: MCC → Processes tab  
**Purpose**: Detailed control over backend and frontend processes

### 11.1 Element Specifications

#### Process Detail Cards

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Process Name** | Identification | None | N/A |
| **Technology Badge** | Stack info | None | N/A |
| **Status Badge** | Current state | None | N/A |
| **CPU Usage** | Resource consumption | None | N/A |
| **Memory Usage** | RAM consumption | None | N/A |
| **Uptime** | Time since start | None | N/A |
| **PID** | Process ID | None | N/A |
| **Port** | Network port | None | N/A |
| **URL** | Access URL | Click | Opens in browser |
| **[Stop]** | Terminate process | Click | Process stops |
| **[Restart]** | Restart process | Click | Stop then Start |
| **[Open]** | Launch in browser | Click | Opens URL |

---

## 12. MCC Log Viewer

**URL**: MCC → Logs tab  
**Purpose**: Real-time log streaming with filtering

### 12.1 Element Specifications

#### Filter Bar

| Element | Purpose | User Action | Effect |
|---------|---------|-------------|--------|
| **Source Dropdown** | Filter by origin | Select | Only that source shown |
| **Level Toggles** | Filter by severity | Toggle | Enable/disable level |
| **Search Input** | Text search | Type | Highlights matches |

**Log Levels**:
| Level | Color | Purpose |
|-------|-------|---------|
| DEBUG | Blue | Detailed debugging |
| INFO | Green | General information |
| WARN | Yellow | Warnings |
| ERROR | Red | Errors |

#### Log Display

| Element | Purpose | Format |
|---------|---------|--------|
| **Timestamp** | When logged | YYYY-MM-DD HH:MM:SS.mmm |
| **Level** | Severity | Colored badge |
| **Source** | Origin | Service name |
| **Message** | Content | Monospace text |

#### Status Bar

| Element | Purpose |
|---------|---------|
| **Live Indicator** | Shows streaming status |
| **Entry Count** | Visible/total entries |
| **Auto-scroll Toggle** | Enable/disable |

---

## 13. MCC Settings

**URL**: MCC → Settings tab  
**Purpose**: Configure MCC behavior and paths

### 13.1 Element Specifications

#### Path Configuration

| Field | Purpose | User Action | Effect |
|-------|---------|-------------|--------|
| **Project Root** | Base directory | Browse button | Opens file picker |
| **Backend Directory** | API source | Browse/edit | Changes backend path |
| **Frontend Directory** | UI source | Browse/edit | Changes frontend path |
| **Database Path** | SQLite file | Browse/edit | Changes DB path |

#### Port Configuration

| Field | Default | Purpose |
|-------|---------|---------|
| **Backend Port** | 8000 | FastAPI server |
| **Frontend Port** | 5173 | Vite dev server |

#### Startup Toggles

| Toggle | Default | Purpose |
|--------|---------|---------|
| Auto-start Backend | ON | Launch on MCC start |
| Auto-start Frontend | ON | Launch on MCC start |
| Open in Browser | OFF | Auto-open frontend URL |
| Start Minimized | OFF | Start in tray |
| Launch at Login | OFF | System startup |

---

## 14. User Flow Diagrams

### 14.1 Signal Viewing Flow

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Dashboard  │────▶│ Instrument List │────▶│ Silo Detail  │────▶│Chart Detail │
│             │     │                 │     │              │     │             │
│ Click       │     │ Click           │     │ Click        │     │ View        │
│ Instrument  │     │ Silo            │     │ Chart        │     │ Signal      │
└─────────────┘     └─────────────────┘     └──────────────┘     └─────────────┘
                                                   │
                                                   ▼
                                            ┌──────────────┐
                                            │ View AI      │
                                            │ Narrative    │
                                            └──────────────┘
```

### 14.2 Basket Management Flow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ Basket List │────▶│ Create Modal │────▶│ Basket Detail │
│             │     │              │     │               │
│ Click       │     │ Fill form    │     │ Add charts    │
│ [+ Create]  │     │ Submit       │     │ via modal     │
└─────────────┘     └──────────────┘     └───────────────┘
                                                 │
                           ┌─────────────────────┼─────────────────────┐
                           ▼                     ▼                     ▼
                    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
                    │ Remove Chart │     │ Edit Basket  │     │Delete Basket │
                    │ Click [X]    │     │ Click [Edit] │     │Click[Delete] │
                    └──────────────┘     └──────────────┘     └──────────────┘
```

### 14.3 AI Chat Flow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Select      │────▶│ Type Message │────▶│ Send to API   │────▶│ View Response│
│ Instrument  │     │              │     │               │     │ + Disclaimer │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
                                                │
                                                ▼
                                         ┌──────────────┐
                                         │ Backend      │
                                         │ Validates    │
                                         │ Response     │
                                         │ (CR-001/003) │
                                         └──────────────┘
```

### 14.4 MCC Process Control Flow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ MCC Launch  │────▶│ Check Config │────▶│ Auto-Start?   │
│             │     │              │     │               │
└─────────────┘     └──────────────┘     └───────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    ▼                           ▼                           ▼
             ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
             │ YES: Start   │           │ NO: Wait for │           │ Error: Show  │
             │ Backend →    │           │ User Action  │           │ Notification │
             │ Frontend     │           │              │           │              │
             └──────────────┘           └──────────────┘           └──────────────┘
                    │
                    ▼
             ┌──────────────┐
             │ Health Check │
             │ Every 30s    │
             └──────────────┘
                    │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │Healthy │ │Degraded│ │Unhealthy│
    │ Green  │ │ Yellow │ │ Red    │
    └────────┘ └────────┘ └────────┘
```

---

## Summary: Constitutional Enforcement Points

| Screen | Element | Rule | Enforcement |
|--------|---------|------|-------------|
| All | Disclaimer Banner | CR-003 | Non-dismissible, always visible |
| Silo Detail | Charts Grid | CR-002 | Equal sizing, 4-column grid |
| Silo Detail | Contradiction Card | CR-002 | Equal-sized boxes, neutral separator |
| Silo Detail | Confirmation Note | CR-001 | "NOT stronger signal" warning |
| Silo Detail | AI Narrative | CR-001, CR-003 | Backend validation + inline disclaimer |
| Chart Detail | CR-001 Notice | CR-001 | "No weight" reminder |
| Basket List | Info Banner | CR-001 | "UI-only, no effect" message |
| Basket Detail | Warning Note | CR-001 | "Counts are not aggregation" |
| AI Chat | Per-Message Disclaimer | CR-003 | Attached to every AI response |
| AI Chat | Input Hint | CR-001 | "Descriptive only" reminder |

---

**Document End**

This specification defines every visual element, its purpose, user interactions, and system effects for the complete CIA-SIE application.

