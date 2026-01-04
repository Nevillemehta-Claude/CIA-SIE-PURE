# CIA-SIE v0.dev Component Prompt Library

**Purpose:** Ready-to-paste prompts for generating all CIA-SIE frontend components using v0.dev
**Usage:** Copy each prompt → Paste into v0.dev → Copy generated code → Save to project
**Created:** January 3, 2026

---

## Table of Contents

1. [Atomic Components](#1-atomic-components)
2. [Layout Components](#2-layout-components)
3. [Page Components](#3-page-components)
4. [Composite Components](#4-composite-components)
5. [Form Components](#5-form-components)
6. [Feedback Components](#6-feedback-components)

---

## Design System Reference

Before generating components, v0.dev needs to know our design tokens:

```
COLORS:
- BULLISH: text-emerald-600, bg-emerald-50, border-emerald-200
  dark: text-emerald-400, bg-emerald-950, border-emerald-800

- BEARISH: text-red-600, bg-red-50, border-red-200
  dark: text-red-400, bg-red-950, border-red-800

- NEUTRAL: text-gray-600, bg-gray-50, border-gray-200
  dark: text-gray-400, bg-gray-800, border-gray-700

- CURRENT: text-green-600, bg-green-50
- RECENT: text-amber-600, bg-amber-50
- STALE: text-red-600, bg-red-50
- UNAVAILABLE: text-gray-400, bg-gray-100

- CONNECTED: text-green-500
- CONNECTING: text-amber-500 (with pulse)
- DISCONNECTED: text-red-500

ICONS: lucide-react only
RADIUS: rounded-lg (buttons), rounded-xl (cards), rounded-full (badges)
SHADOWS: shadow-sm (cards), shadow-lg (dropdowns), shadow-xl (modals)
```

---

## 1. ATOMIC COMPONENTS

### 1.1 SignalBadge

```
Create a SignalBadge React component with TypeScript and Tailwind CSS.

PURPOSE: Displays market direction (BULLISH/BEARISH/NEUTRAL) as a colored badge.

PROPS:
- direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL' (required)
- size?: 'sm' | 'md' | 'lg' (default: 'md')
- showIcon?: boolean (default: true)
- showLabel?: boolean (default: true)
- className?: string

VISUAL DESIGN:
- Pill-shaped badge (rounded-full)
- Icon + text label side by side
- BULLISH: emerald-600 text, emerald-50 bg, emerald-200 border, ArrowUp icon
- BEARISH: red-600 text, red-50 bg, red-200 border, ArrowDown icon
- NEUTRAL: gray-600 text, gray-50 bg, gray-200 border, Minus icon

SIZES:
- sm: text-xs, px-2, py-0.5, icon w-3 h-3
- md: text-sm, px-3, py-1, icon w-4 h-4
- lg: text-base, px-4, py-1.5, icon w-5 h-5

CRITICAL REQUIREMENTS:
- All three direction variants MUST have exactly equal visual size and weight
- No variant should appear "stronger" or more prominent than others
- This is a constitutional requirement - equal treatment of all signals

Use lucide-react for icons. Support dark mode.
```

---

### 1.2 FreshnessMeter

```
Create a FreshnessMeter React component with TypeScript and Tailwind CSS.

PURPOSE: Shows how fresh/stale a data signal is with visual indicator and relative time.

PROPS:
- status: 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE' (required)
- timestamp?: Date | string (optional - used to calculate relative time)
- showLabel?: boolean (default: true)
- size?: 'sm' | 'md' (default: 'md')
- className?: string

VISUAL DESIGN:
- Small colored dot + status label + relative time
- Horizontal layout: [dot] [label] [time]

STATUS COLORS:
- CURRENT: green-500 dot (with subtle pulse animation), "Current" label
- RECENT: amber-500 dot, "Recent" label
- STALE: red-500 dot, "Stale" label
- UNAVAILABLE: gray-400 dot, "No data" label

RELATIVE TIME FORMAT:
- < 1 minute: "just now"
- < 60 minutes: "Xm ago"
- < 24 hours: "Xh ago"
- < 7 days: "Xd ago"
- else: formatted date

CRITICAL REQUIREMENTS:
- This component is DESCRIPTIVE only
- No "quality score" or "reliability" language
- Simply states the freshness status factually

Use lucide-react for any icons. Support dark mode.
Include a helper function to calculate relative time from timestamp.
```

---

### 1.3 ScripCard

```
Create a ScripCard React component with TypeScript and Tailwind CSS.

PURPOSE: Card displaying a single trading instrument with its current signal status.

PROPS:
- instrumentId: string (required)
- symbol: string (required, e.g., "RELIANCE")
- displayName: string (required, e.g., "Reliance Industries")
- direction?: 'BULLISH' | 'BEARISH' | 'NEUTRAL' | null
- freshness?: 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'
- lastSignalTime?: Date
- siloCount?: number
- chartCount?: number
- onClick?: () => void
- className?: string

VISUAL DESIGN:
- Card with rounded-xl, subtle border, shadow-sm
- Hover: shadow-md, slight scale (1.02)
- Clickable (cursor-pointer)

LAYOUT:
┌─────────────────────────────────────┐
│ SYMBOL            [SignalBadge]     │  <- Header row
│ Display Name                        │  <- Subheader (gray, smaller)
├─────────────────────────────────────┤
│ [FreshnessMeter]                    │  <- Freshness row
│ X silos • Y charts                  │  <- Stats row (gray, small)
└─────────────────────────────────────┘

STATES:
- With signal: Show SignalBadge with direction
- No signal: Show gray "No Signal" placeholder badge
- Loading: Skeleton animation

CRITICAL REQUIREMENTS:
- No aggregate scores or confidence displays
- No "signal strength" indicators
- All cards must have equal visual treatment regardless of direction

Use lucide-react for icons. Support dark mode.
Compose with SignalBadge and FreshnessMeter components (assume they exist).
```

---

### 1.4 ContradictionAlert

```
Create a ContradictionAlert React component with TypeScript and Tailwind CSS.

PURPOSE: Displays when two charts show conflicting signals. Shows BOTH signals with EQUAL prominence.

PROPS:
- contradiction: {
    chartA: { chartId: string, chartName: string, direction: 'BULLISH' | 'BEARISH', timeframe: string }
    chartB: { chartId: string, chartName: string, direction: 'BULLISH' | 'BEARISH', timeframe: string }
    description?: string
  }
- onDismiss?: () => void (optional - if dismissible)
- className?: string

VISUAL DESIGN:
- Warning banner with amber-50 background, amber-200 border
- AlertTriangle icon from lucide-react in amber-600
- Header: "Contradiction Detected" in amber-800 font-medium

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ ⚠ Contradiction Detected                              [dismiss]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┐         ┌─────────────────┐              │
│   │ Chart A Name    │   VS    │ Chart B Name    │              │
│   │ [timeframe]     │         │ [timeframe]     │              │
│   │ [SignalBadge]   │         │ [SignalBadge]   │              │
│   └─────────────────┘         └─────────────────┘              │
│                                                                 │
│   "Chart A and Chart B show opposing directions"               │
└─────────────────────────────────────────────────────────────────┘

CRITICAL REQUIREMENTS (CONSTITUTIONAL):
- Both chart boxes MUST be exactly the same size
- Both SignalBadges MUST have equal visual prominence
- NO indication of which signal is "correct" or "more reliable"
- NO resolution or recommendation - just EXPOSE the contradiction
- The word "VS" should be neutral, not implying competition

Use lucide-react for icons. Support dark mode.
```

---

### 1.5 ConfirmationIndicator

```
Create a ConfirmationIndicator React component with TypeScript and Tailwind CSS.

PURPOSE: Shows when multiple charts agree on the same direction (confirmation).

PROPS:
- confirmation: {
    charts: Array<{ chartId: string, chartName: string, timeframe: string }>
    alignedDirection: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
    description?: string
  }
- className?: string

VISUAL DESIGN:
- Subtle info banner with blue-50 background, blue-200 border
- CheckCircle2 icon from lucide-react in blue-600
- Shows aligned direction with single SignalBadge
- Lists confirming charts below

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ ✓ Signals Aligned                              [SignalBadge]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Charts in agreement:                                         │
│   • Chart A (1H)                                               │
│   • Chart B (4H)                                               │
│   • Chart C (1D)                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

CRITICAL REQUIREMENTS (CONSTITUTIONAL):
- NO "stronger signal" language
- NO "higher confidence" due to confirmation
- NO "more reliable" statements
- Simply state: "These charts show the same direction"
- Do NOT imply that confirmation = better or more trustworthy

Use lucide-react for icons. Support dark mode.
```

---

### 1.6 NarrativePanel

```
Create a NarrativePanel React component with TypeScript and Tailwind CSS.

PURPOSE: Displays AI-generated narrative analysis with mandatory disclaimer.

PROPS:
- narrative: string (the AI-generated text, required)
- model: string (e.g., "claude-3-5-sonnet", required)
- generatedAt: Date | string (required)
- tokensUsed?: number
- cost?: number
- isLoading?: boolean (default: false)
- onRegenerate?: () => void (optional)
- className?: string

VISUAL DESIGN:
- Card with rounded-xl, border, subtle shadow
- Clean white/dark background

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ AI Analysis                               [model badge] [time] │
│                                                    [regenerate]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ [Narrative text content - multiple paragraphs possible]        │
│                                                                 │
│ Lorem ipsum dolor sit amet, consectetur adipiscing elit.       │
│ Sed do eiusmod tempor incididunt ut labore et dolore magna     │
│ aliqua.                                                        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ ℹ️ This is a description of what your charts are showing.      │
│    The interpretation and any decision is entirely yours.      │
├─────────────────────────────────────────────────────────────────┤
│ Tokens: 1,234 • Cost: $0.02                          [copy]    │
└─────────────────────────────────────────────────────────────────┘

LOADING STATE:
- Show skeleton animation for narrative area
- Keep header and disclaimer visible

CRITICAL REQUIREMENTS (CONSTITUTIONAL):
- The disclaimer section MUST always be visible
- The disclaimer CANNOT be collapsed, hidden, or dismissed
- The disclaimer MUST say exactly: "This is a description of what your
  charts are showing. The interpretation and any decision is entirely yours."
- Use Info icon (blue) for the disclaimer, not warning

Use lucide-react for icons. Support dark mode.
Include copy-to-clipboard functionality for the narrative.
```

---

### 1.7 DisclaimerText

```
Create a DisclaimerText React component with TypeScript and Tailwind CSS.

PURPOSE: Standardized disclaimer that appears on all AI-generated content.

PROPS:
- variant?: 'inline' | 'block' | 'footer' (default: 'block')
- className?: string

DISCLAIMER TEXT (exact, do not modify):
"This is a description of what your charts are showing. The interpretation and any decision is entirely yours."

VARIANTS:
- inline: Single line, smaller text, info icon, for tight spaces
- block: Full box with background, icon, for prominent display
- footer: Bottom-anchored, full width, for page/section footers

VISUAL DESIGN:
- block: bg-blue-50, border-blue-200, rounded-lg, p-4
- inline: text-gray-500, text-sm, with small info icon
- footer: bg-gray-50, border-t, py-3, text-center

CRITICAL REQUIREMENTS (CONSTITUTIONAL):
- This component CANNOT accept children or custom text
- The disclaimer text is FIXED and IMMUTABLE
- No close button, no collapse, no dismiss functionality
- Must always be visible when rendered

Use lucide-react Info icon. Support dark mode.
```

---

### 1.8 ModelSelector

```
Create a ModelSelector React component with TypeScript and Tailwind CSS.

PURPOSE: Dropdown to select AI model for narrative generation.

PROPS:
- value: string (current model, required)
- onChange: (model: string) => void (required)
- disabled?: boolean (default: false)
- className?: string

AVAILABLE MODELS:
- claude-3-haiku-20240307: "Haiku" - "Fast & economical"
- claude-3-5-sonnet-20241022: "Sonnet" - "Balanced"
- claude-3-opus-20240229: "Opus" - "Most capable"

VISUAL DESIGN:
- Dropdown select with custom styling
- Show model name + description
- Current selection shows abbreviated name + icon

LAYOUT:
┌─────────────────────────────────┐
│ 🤖 Sonnet              ▼       │
└─────────────────────────────────┘
         │
         ▼ (dropdown open)
┌─────────────────────────────────┐
│ ○ Haiku                        │
│   Fast & economical            │
├─────────────────────────────────┤
│ ● Sonnet                       │
│   Balanced                     │
├─────────────────────────────────┤
│ ○ Opus                         │
│   Most capable                 │
└─────────────────────────────────┘

CRITICAL REQUIREMENTS:
- NO "recommended" label on any option
- All options presented with equal visual weight
- User makes the choice, no default recommendation

Use lucide-react for icons. Support dark mode.
Use Radix UI Select or similar headless component pattern.
```

---

### 1.9 CostDisplay

```
Create a CostDisplay React component with TypeScript and Tailwind CSS.

PURPOSE: Shows token usage and cost for AI operations.

PROPS:
- inputTokens?: number
- outputTokens?: number
- totalTokens?: number
- cost?: number (in USD)
- model?: string
- className?: string

VISUAL DESIGN:
- Compact inline display or expanded card view
- Use monospace font for numbers

COMPACT LAYOUT (inline):
Tokens: 1,234 • Cost: $0.02

EXPANDED LAYOUT (card):
┌─────────────────────────────────┐
│ Usage Details                   │
├─────────────────────────────────┤
│ Input tokens:     892          │
│ Output tokens:    342          │
│ Total tokens:   1,234          │
├─────────────────────────────────┤
│ Model: claude-3-5-sonnet       │
│ Cost: $0.02                    │
└─────────────────────────────────┘

Format numbers with thousand separators (1,234 not 1234).
Format cost with 2-4 decimal places.

Use lucide-react Coins icon. Support dark mode.
```

---

### 1.10 BudgetAlert

```
Create a BudgetAlert React component with TypeScript and Tailwind CSS.

PURPOSE: Displays warnings when AI budget usage is high.

PROPS:
- used: number (amount used in USD)
- limit: number (budget limit in USD)
- percentUsed?: number (calculated if not provided)
- className?: string

STATES:
- normal (< 80%): No display or subtle gray info
- warning (80-90%): Amber warning banner
- critical (90-99%): Red warning banner
- exceeded (≥ 100%): Red error banner, AI features may be disabled

VISUAL DESIGN:

Warning state (80-90%):
┌─────────────────────────────────────────────────────────────────┐
│ ⚠️ Budget Warning: 85% used ($42.50 of $50.00)                 │
│ ████████████████████░░░░                                        │
└─────────────────────────────────────────────────────────────────┘

Critical state (90-99%):
┌─────────────────────────────────────────────────────────────────┐
│ 🚨 Budget Critical: 95% used ($47.50 of $50.00)                │
│ ██████████████████████░░                                        │
│ AI features will be disabled when budget is exceeded.          │
└─────────────────────────────────────────────────────────────────┘

Exceeded state (≥ 100%):
┌─────────────────────────────────────────────────────────────────┐
│ ❌ Budget Exceeded: $52.30 of $50.00 (105%)                    │
│ ████████████████████████                                        │
│ AI features are currently disabled. Contact admin.             │
└─────────────────────────────────────────────────────────────────┘

Include progress bar visualization.
Use lucide-react for icons. Support dark mode.
```

---

### 1.11 TimeframeSelector

```
Create a TimeframeSelector React component with TypeScript and Tailwind CSS.

PURPOSE: Select or filter by chart timeframe.

PROPS:
- value: string | string[] (single or multi-select)
- onChange: (value: string | string[]) => void
- options?: Array<{ value: string, label: string }>
- multiple?: boolean (default: false)
- className?: string

DEFAULT OPTIONS:
- 1m: "1 Minute"
- 5m: "5 Minutes"
- 15m: "15 Minutes"
- 1h: "1 Hour"
- 4h: "4 Hours"
- 1d: "1 Day"
- 1w: "1 Week"

VISUAL DESIGN:

Single select (dropdown):
┌─────────────────────────────────┐
│ ⏱️ 1 Hour                ▼     │
└─────────────────────────────────┘

Multi-select (pill toggles):
┌─────────────────────────────────────────────────────────────────┐
│ [1m] [5m] [15m] [●1h] [●4h] [1d] [1w]                          │
└─────────────────────────────────────────────────────────────────┘

Active pills are filled, inactive are outlined.

Use lucide-react Clock icon. Support dark mode.
```

---

### 1.12 ConnectionStatus

```
Create a ConnectionStatus React component with TypeScript and Tailwind CSS.

PURPOSE: Shows connection status to backend/WebSocket/external services.

PROPS:
- service: 'backend' | 'websocket' | 'kite' (required)
- status: 'connected' | 'connecting' | 'disconnected' | 'error' (required)
- label?: string (custom label, otherwise derived from service)
- onReconnect?: () => void (optional - shows reconnect button when disconnected)
- className?: string

VISUAL DESIGN:
- Compact: colored dot + label
- Connecting state has pulse animation

STATUS INDICATORS:
- connected: green-500 solid dot, "Connected" or service name
- connecting: amber-500 pulsing dot, "Connecting..."
- disconnected: red-500 solid dot, "Disconnected" + reconnect option
- error: red-500 dot with X, error message + retry option

LAYOUTS:
Compact:  ● Backend Connected
          ◐ WebSocket Connecting...
          ○ Kite Disconnected [Reconnect]

Expanded (for status bar):
┌─────────────────────────────────────────────────────────────────┐
│ ● API  │  ◐ WebSocket  │  ○ Kite [Connect]                     │
└─────────────────────────────────────────────────────────────────┘

Use lucide-react for icons. Support dark mode.
```

---

## 2. LAYOUT COMPONENTS

### 2.1 AppShell

```
Create an AppShell React component with TypeScript and Tailwind CSS.

PURPOSE: Root layout wrapper that provides consistent structure for all pages.

PROPS:
- children: React.ReactNode (main content)
- sidebar?: React.ReactNode (optional sidebar override)
- topbar?: React.ReactNode (optional topbar override)
- statusbar?: React.ReactNode (optional statusbar override)
- sidebarCollapsed?: boolean (default: false)
- onSidebarToggle?: () => void
- className?: string

LAYOUT STRUCTURE:
┌─────────────────────────────────────────────────────────────────────────────┐
│ [TopBar - full width, fixed height 64px]                                    │
├────────────────┬────────────────────────────────────────────────────────────┤
│                │                                                            │
│   [Sidebar]    │              [Main Content Area]                          │
│    280px       │                                                            │
│    fixed       │              Scrollable                                   │
│                │              Padded (p-6)                                 │
│                │                                                            │
│                │                                                            │
│                │                                                            │
├────────────────┴────────────────────────────────────────────────────────────┤
│ [StatusBar - full width, fixed height 40px]                                │
└─────────────────────────────────────────────────────────────────────────────┘

RESPONSIVE:
- Desktop (≥1024px): Sidebar visible, 280px wide
- Tablet (768-1023px): Sidebar collapsible, icon-only when collapsed (64px)
- Mobile (<768px): Sidebar hidden, hamburger menu in topbar

Use lucide-react for icons. Support dark mode with bg-gray-900.
Main content area should have subtle gray background (gray-50 light, gray-900 dark).
```

---

### 2.2 Sidebar

```
Create a Sidebar React component with TypeScript and Tailwind CSS.

PURPOSE: Left navigation panel with menu items and branding.

PROPS:
- items: Array<{
    id: string
    label: string
    icon: string (lucide icon name)
    href: string
    badge?: string | number
    children?: Array<same structure>
  }>
- activeItemId?: string
- collapsed?: boolean (default: false)
- onItemClick?: (item) => void
- className?: string

VISUAL DESIGN:
- Fixed width: 280px (expanded), 64px (collapsed)
- White/dark background with subtle right border
- Smooth collapse transition (300ms)

LAYOUT:
┌─────────────────────────────┐
│ [Logo] CIA-SIE              │ <- Brand area, h-16
├─────────────────────────────┤
│                             │
│ 🏠 Dashboard                │ <- Nav items
│ 📊 Instruments         (5)  │ <- With badge
│   └─ RELIANCE              │ <- Nested items
│   └─ INFY                  │
│ ⚙️ Settings                 │
│                             │
├─────────────────────────────┤
│ [ConnectionStatus]          │ <- Bottom section
│ v2.3.0                      │ <- Version
└─────────────────────────────┘

COLLAPSED STATE:
┌────────┐
│ [Logo] │
├────────┤
│   🏠   │
│   📊   │
│   ⚙️   │
├────────┤
│   ●    │
└────────┘

Active item: bg-blue-50 (light) / bg-blue-900/20 (dark), blue-600 text
Hover: bg-gray-50 (light) / bg-gray-800 (dark)

Use lucide-react for icons. Support dark mode.
Include tooltip on hover when collapsed.
```

---

### 2.3 TopBar

```
Create a TopBar React component with TypeScript and Tailwind CSS.

PURPOSE: Top navigation bar with search, actions, and user menu.

PROPS:
- title?: string (page title)
- showSearch?: boolean (default: true)
- onSearch?: (query: string) => void
- actions?: React.ReactNode (custom action buttons)
- user?: { name: string, email?: string, avatar?: string }
- onMenuClick?: () => void (mobile hamburger)
- className?: string

VISUAL DESIGN:
- Fixed height: 64px (h-16)
- White/dark background with subtle bottom border
- Sticky at top

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│ [≡] [Page Title]        [🔍 Search...]           [🔔] [⚙️] [👤 User ▼]     │
└─────────────────────────────────────────────────────────────────────────────┘

ELEMENTS:
- Hamburger menu (mobile only, triggers onMenuClick)
- Page title (optional, from props or route)
- Search input (expandable on mobile)
- Notification bell (optional)
- Settings quick link
- User dropdown (name, email, sign out)

SEARCH:
- Rounded input with search icon
- Placeholder: "Search instruments..."
- Keyboard shortcut hint: ⌘K

USER DROPDOWN:
┌─────────────────────────┐
│ John Doe                │
│ john@example.com        │
├─────────────────────────┤
│ 👤 Profile              │
│ ⚙️ Settings             │
├─────────────────────────┤
│ 🚪 Sign Out             │
└─────────────────────────┘

Use lucide-react for icons. Support dark mode.
```

---

### 2.4 StatusBar

```
Create a StatusBar React component with TypeScript and Tailwind CSS.

PURPOSE: Bottom bar showing system status, connections, and quick info.

PROPS:
- connections?: Array<{
    service: string
    status: 'connected' | 'connecting' | 'disconnected' | 'error'
  }>
- alerts?: Array<{ id: string, message: string, type: 'info' | 'warning' | 'error' }>
- version?: string
- lastUpdated?: Date
- className?: string

VISUAL DESIGN:
- Fixed height: 40px (h-10)
- Gray background (gray-100 light, gray-800 dark)
- Subtle top border

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│ ● API  ● WebSocket  ○ Kite    │ ⚠️ 1 alert    │ Updated: 2m ago   v2.3.0  │
└─────────────────────────────────────────────────────────────────────────────┘

LEFT: Connection status indicators
CENTER: Alert summary (click to expand)
RIGHT: Last update time, version

ALERT EXPANSION (on click):
Shows popover with full alert messages

TEXT SIZE: text-xs
All elements vertically centered

Use lucide-react for icons. Support dark mode.
```

---

## 3. PAGE COMPONENTS

### 3.1 Dashboard Page

```
Create a Dashboard React page component with TypeScript and Tailwind CSS.

PURPOSE: Overview page showing all instruments with their latest signals.

PROPS:
- instruments: Array<Instrument with signal data>
- isLoading?: boolean
- error?: string

VISUAL DESIGN:
- Clean grid layout of ScripCards
- Header with title and actions

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│ Dashboard                                    [+ Add Instrument] [⟳ Refresh]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ ScripCard   │ │ ScripCard   │ │ ScripCard   │ │ ScripCard   │          │
│  │ RELIANCE    │ │ INFY        │ │ TCS         │ │ HDFCBANK    │          │
│  │ [BULLISH]   │ │ [BEARISH]   │ │ [NEUTRAL]   │ │ [BULLISH]   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ ScripCard   │ │ ScripCard   │ │ + Add New   │                          │
│  │ ICICIBANK   │ │ SBIN        │ │             │                          │
│  │ [BEARISH]   │ │ [BULLISH]   │ │             │                          │
│  └─────────────┘ └─────────────┘ └─────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

GRID:
- Desktop: 4 columns
- Tablet: 3 columns
- Mobile: 1-2 columns
- Gap: 6 (gap-6)

LOADING: Show skeleton grid
EMPTY: Show "No instruments yet" + Add button
ERROR: Show error message + retry button

CRITICAL REQUIREMENTS:
- NO aggregate overview like "Market Sentiment: Bullish"
- NO summary statistics like "5 Bullish, 2 Bearish"
- Each instrument displayed independently with equal treatment

Use lucide-react for icons. Support dark mode.
```

---

### 3.2 InstrumentDetail Page

```
Create an InstrumentDetail React page component with TypeScript and Tailwind CSS.

PURPOSE: Deep dive into a single instrument showing all silos and signals.

PROPS:
- instrument: Instrument
- silos: Array<Silo with charts and signals>
- isLoading?: boolean
- error?: string

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│ ← Back    RELIANCE - Reliance Industries                        [⟳] [⚙️]  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ SILOS                                                                       │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ Primary Silo                                              [Expand All] ││
│ │ 12 charts • Last updated: 2m ago                                       ││
│ ├─────────────────────────────────────────────────────────────────────────┤│
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐││
│ │ │Chart 1  │ │Chart 2  │ │Chart 3  │ │Chart 4  │ │Chart 5  │ │Chart 6 │││
│ │ │1H       │ │4H       │ │1D       │ │1H       │ │4H       │ │1D      │││
│ │ │BULLISH  │ │BULLISH  │ │BEARISH  │ │NEUTRAL  │ │BULLISH  │ │BULLISH │││
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ CONTRADICTIONS (if any)                                                    │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ [ContradictionAlert: Chart 2 (BULLISH) vs Chart 3 (BEARISH)]           ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ CONFIRMATIONS (if any)                                                     │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ [ConfirmationIndicator: Charts 1,2,5,6 aligned BULLISH]                ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ AI ANALYSIS                                           [ModelSelector] [▶]  │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ [NarrativePanel with analysis]                                         ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

CRITICAL REQUIREMENTS:
- Contradictions and Confirmations shown as equal sections
- NO "overall signal" summary at the top
- Each chart shown with equal visual treatment
- AI Analysis section has mandatory disclaimer

Use lucide-react for icons. Support dark mode.
```

---

### 3.3 SiloView Page

```
Create a SiloView React page component with TypeScript and Tailwind CSS.

PURPOSE: Detailed view of a single silo with all its charts and signals.

PROPS:
- silo: Silo with full chart data
- charts: Array<Chart with latest signal>
- contradictions: Array<Contradiction>
- confirmations: Array<Confirmation>
- narrative?: string
- isLoading?: boolean

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│ ← Back to RELIANCE    Primary Silo                         [Generate AI]   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Freshness Settings: Current ≤2m • Recent ≤10m • Stale >30m      [Edit]    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ CHARTS (12)                                              [Grid] [List]     │
│ ┌──────────────────────────────────────────────────────────────────────────┐
│ │  Chart details with signals in grid or list view                        │
│ └──────────────────────────────────────────────────────────────────────────┘
│                                                                             │
│ RELATIONSHIPS                                                               │
│ ┌───────────────────────────────┐ ┌───────────────────────────────────────┐│
│ │ Contradictions (2)            │ │ Confirmations (1)                     ││
│ │ [ContradictionAlert]          │ │ [ConfirmationIndicator]               ││
│ │ [ContradictionAlert]          │ │                                       ││
│ └───────────────────────────────┘ └───────────────────────────────────────┘│
│                                                                             │
│ AI NARRATIVE                                                                │
│ ┌──────────────────────────────────────────────────────────────────────────┐
│ │ [NarrativePanel]                                                         │
│ └──────────────────────────────────────────────────────────────────────────┘
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

CRITICAL REQUIREMENTS:
- All charts displayed with equal visual treatment
- Contradictions and Confirmations as peer sections (neither more prominent)
- NO summary or aggregate at the top

Use lucide-react for icons. Support dark mode.
```

---

### 3.4 Settings Page

```
Create a Settings React page component with TypeScript and Tailwind CSS.

PURPOSE: Application configuration and preferences.

SECTIONS:
1. Display Preferences (theme, density)
2. AI Configuration (default model, budget)
3. Notification Settings
4. Platform Connections (Kite status)
5. Data Management (clear cache, export)

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│ Settings                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ DISPLAY                                                                     │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ Theme              [Light ▼]                                            ││
│ │ Display Density    [Comfortable ▼]                                      ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ AI CONFIGURATION                                                           │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ Default Model      [ModelSelector]                                      ││
│ │ Monthly Budget     [$50.00        ]                                     ││
│ │ Current Usage      $32.50 (65%)   [View Details]                        ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ PLATFORM CONNECTIONS                                                       │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ Kite Connect       ● Connected as user@email.com    [Disconnect]        ││
│ │                    Last synced: 2 minutes ago       [Sync Now]          ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ DATA MANAGEMENT                                                            │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ [Clear Cache]  [Export Data]  [Import Data]                             ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Use form controls, toggles, dropdowns as appropriate.
Include save/cancel for sections with changes.

Use lucide-react for icons. Support dark mode.
```

---

### 3.5 NotFound Page (404)

```
Create a NotFound React page component with TypeScript and Tailwind CSS.

PURPOSE: 404 error page when route doesn't exist.

VISUAL DESIGN:
- Centered content
- Friendly illustration or icon
- Clear message
- Navigation options

LAYOUT:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                           ┌─────────────────┐                              │
│                           │                 │                              │
│                           │   404 icon      │                              │
│                           │   or graphic    │                              │
│                           │                 │                              │
│                           └─────────────────┘                              │
│                                                                             │
│                           Page Not Found                                   │
│                                                                             │
│              The page you're looking for doesn't exist                     │
│              or has been moved.                                            │
│                                                                             │
│                     [← Go to Dashboard]                                    │
│                                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Use lucide-react FileQuestion or similar icon.
Support dark mode.
```

---

## 4. COMPOSITE COMPONENTS

### 4.1 ChartCard

```
Create a ChartCard React component with TypeScript and Tailwind CSS.

PURPOSE: Displays a single chart within a silo with its signal status.

PROPS:
- chart: {
    chartId: string
    chartCode: string
    chartName: string
    timeframe: string
    webhookId: string
  }
- signal?: {
    direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
    signalType: string
    timestamp: Date
    indicators?: Record<string, number>
  }
- freshness?: 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'
- onClick?: () => void
- className?: string

LAYOUT:
┌─────────────────────────────────────┐
│ 01A - RSI Momentum           [1H]  │ <- Code, Name, Timeframe badge
├─────────────────────────────────────┤
│                                     │
│         [SignalBadge]               │ <- Large, centered
│           BULLISH                   │
│                                     │
├─────────────────────────────────────┤
│ ● Current • 2m ago                  │ <- Freshness
│ RSI: 65.4 • MACD: 0.23             │ <- Key indicators (if available)
└─────────────────────────────────────┘

NO SIGNAL STATE:
┌─────────────────────────────────────┐
│ 01A - RSI Momentum           [1H]  │
├─────────────────────────────────────┤
│                                     │
│      [Awaiting Signal]              │ <- Gray, dashed border
│                                     │
├─────────────────────────────────────┤
│ ○ No data                          │
└─────────────────────────────────────┘

Use lucide-react for icons. Support dark mode.
Card should be clickable with hover effect.
```

---

### 4.2 SignalHistory

```
Create a SignalHistory React component with TypeScript and Tailwind CSS.

PURPOSE: Shows historical signals for a chart in a timeline format.

PROPS:
- signals: Array<{
    signalId: string
    direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
    timestamp: Date
    indicators?: Record<string, number>
  }>
- limit?: number (default: 10)
- onLoadMore?: () => void
- className?: string

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ Signal History                                     [Load More]  │
├─────────────────────────────────────────────────────────────────┤
│ ● BULLISH    Today 10:30 AM           RSI: 65.4                │
│ │                                                               │
│ ● BEARISH    Today 9:15 AM            RSI: 32.1                │
│ │                                                               │
│ ● BULLISH    Yesterday 4:45 PM        RSI: 58.7                │
│ │                                                               │
│ ● NEUTRAL    Yesterday 2:30 PM        RSI: 50.2                │
│ │                                                               │
│ ● BEARISH    Jan 2, 11:00 AM          RSI: 28.9                │
└─────────────────────────────────────────────────────────────────┘

Timeline visual with colored dots for each signal.
Dots colored by direction.
Vertical line connecting them.

CRITICAL:
- NO trend analysis like "3 of last 5 signals were bullish"
- NO pattern detection language
- Simply list signals chronologically

Use lucide-react for icons. Support dark mode.
```

---

## 5. FORM COMPONENTS

### 5.1 InstrumentForm

```
Create an InstrumentForm React component with TypeScript and Tailwind CSS.

PURPOSE: Form for creating or editing an instrument.

PROPS:
- initialValues?: { symbol: string, displayName: string }
- onSubmit: (values) => void
- onCancel: () => void
- isLoading?: boolean
- error?: string

FIELDS:
- Symbol (required, uppercase, max 20 chars)
- Display Name (required, max 100 chars)

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ Add Instrument                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Symbol *                                                        │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ RELIANCE                                                     ││
│ └─────────────────────────────────────────────────────────────┘│
│ Unique identifier (e.g., RELIANCE, INFY, TCS)                  │
│                                                                 │
│ Display Name *                                                  │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Reliance Industries Ltd                                      ││
│ └─────────────────────────────────────────────────────────────┘│
│ Human-readable name                                             │
│                                                                 │
│                                    [Cancel]  [Create Instrument]│
└─────────────────────────────────────────────────────────────────┘

Validation on blur and submit.
Error messages below fields in red.
Submit button disabled while loading.

Use lucide-react for icons. Support dark mode.
```

---

### 5.2 SiloForm

```
Create a SiloForm React component with TypeScript and Tailwind CSS.

PURPOSE: Form for creating or editing a silo with freshness thresholds.

PROPS:
- instrumentId: string
- initialValues?: Silo
- onSubmit: (values) => void
- onCancel: () => void
- isLoading?: boolean

FIELDS:
- Silo Name (required)
- Heartbeat Enabled (toggle)
- Heartbeat Frequency (minutes, if enabled)
- Current Threshold (minutes, default 2)
- Recent Threshold (minutes, default 10)
- Stale Threshold (minutes, default 30)

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ Create Silo                                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Silo Name *                                                     │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Primary                                                      ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ Heartbeat Monitoring                                 [  ON  ]  │
│                                                                 │
│ Heartbeat Frequency (minutes)                                   │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ 5                                                            ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ Freshness Thresholds                                            │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│ │ Current: 2  │ │ Recent: 10  │ │ Stale: 30   │ minutes        │
│ └─────────────┘ └─────────────┘ └─────────────┘                │
│                                                                 │
│                                         [Cancel]  [Create Silo]│
└─────────────────────────────────────────────────────────────────┘

Use lucide-react for icons. Support dark mode.
```

---

## 6. FEEDBACK COMPONENTS

### 6.1 Toast

```
Create a Toast React component with TypeScript and Tailwind CSS.

PURPOSE: Transient notification messages.

PROPS:
- message: string
- type: 'success' | 'error' | 'warning' | 'info'
- duration?: number (ms, default 5000, 0 for persistent)
- onDismiss?: () => void
- action?: { label: string, onClick: () => void }

VISUAL DESIGN:
Position: top-right, stacked
Animation: slide in from right

TYPES:
- success: green-50 bg, green-600 icon (CheckCircle)
- error: red-50 bg, red-600 icon (XCircle)
- warning: amber-50 bg, amber-600 icon (AlertTriangle)
- info: blue-50 bg, blue-600 icon (Info)

LAYOUT:
┌─────────────────────────────────────────────┐
│ ✓ Instrument created successfully      [×] │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ✗ Failed to save changes. [Retry]      [×] │
└─────────────────────────────────────────────┘

Include ToastProvider/useToast hook for triggering toasts.
Max 3 toasts visible, oldest dismissed first.

Use lucide-react for icons. Support dark mode.
```

---

### 6.2 ConfirmDialog

```
Create a ConfirmDialog React component with TypeScript and Tailwind CSS.

PURPOSE: Modal dialog for confirming destructive actions.

PROPS:
- isOpen: boolean
- onClose: () => void
- onConfirm: () => void
- title: string
- message: string
- confirmLabel?: string (default: "Confirm")
- cancelLabel?: string (default: "Cancel")
- variant?: 'danger' | 'warning' | 'info' (default: 'danger')
- isLoading?: boolean

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│ Delete Instrument                                          [×]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ⚠️  Are you sure you want to delete "RELIANCE"?               │
│                                                                 │
│      This action cannot be undone. All silos, charts,          │
│      and signals will be permanently removed.                  │
│                                                                 │
│                                     [Cancel]  [Delete]          │
└─────────────────────────────────────────────────────────────────┘

DANGER variant: red confirm button
WARNING variant: amber confirm button
INFO variant: blue confirm button

Modal overlay: bg-black/50
Focus trapped inside dialog
Escape to close

Use lucide-react for icons. Support dark mode.
```

---

### 6.3 EmptyState

```
Create an EmptyState React component with TypeScript and Tailwind CSS.

PURPOSE: Placeholder when no data is available.

PROPS:
- icon?: string (lucide icon name)
- title: string
- description?: string
- action?: { label: string, onClick: () => void }
- className?: string

LAYOUT:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                        ┌─────────┐                             │
│                        │  📊     │                             │
│                        └─────────┘                             │
│                                                                 │
│                    No Instruments Yet                          │
│                                                                 │
│          Add your first instrument to start                    │
│          tracking signals.                                     │
│                                                                 │
│                    [+ Add Instrument]                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Centered, muted colors
Icon in gray-300 (large, 64px)
Title in gray-900 font-medium
Description in gray-500

Use lucide-react for icons. Support dark mode.
```

---

### 6.4 Skeleton

```
Create Skeleton React components with TypeScript and Tailwind CSS.

PURPOSE: Loading placeholder animations.

COMPONENTS:
- Skeleton (base rectangle)
- SkeletonText (text line)
- SkeletonCard (card shape)
- SkeletonAvatar (circle)

PROPS (base Skeleton):
- width?: string | number
- height?: string | number
- className?: string
- rounded?: 'none' | 'sm' | 'md' | 'lg' | 'full'

VISUAL:
- bg-gray-200 (light) / bg-gray-700 (dark)
- animate-pulse
- Rounded corners matching component being loaded

EXAMPLES:

SkeletonText:
████████████████████████████████████

SkeletonCard:
┌─────────────────────────────────────┐
│ ████████████  ████                  │
│ ██████████████████████████          │
│                                     │
│ ████████  ████████████              │
└─────────────────────────────────────┘

SkeletonAvatar:
(●)

Support dark mode.
```

---

## Usage Instructions

### How to Use This Library:

1. **Go to v0.dev** and sign in

2. **Copy a prompt** from this document

3. **Paste into v0.dev** and generate

4. **Review the output** - v0 may offer multiple variants

5. **Copy the code** to your project:
   ```
   frontend/src/components/common/SignalBadge.tsx
   frontend/src/components/common/FreshnessMeter.tsx
   etc.
   ```

6. **Review with Claude Code** for constitutional compliance

7. **Commit to repository**

### Generation Order (Recommended):

```
1. Atomic Components (foundations)
   └── SignalBadge, FreshnessMeter, DisclaimerText first

2. Layout Components
   └── AppShell, Sidebar, TopBar, StatusBar

3. Composite Components
   └── ScripCard, ChartCard, NarrativePanel
   └── ContradictionAlert, ConfirmationIndicator

4. Feedback Components
   └── Toast, ConfirmDialog, EmptyState, Skeleton

5. Page Components (last - compose from above)
   └── Dashboard, InstrumentDetail, SiloView, Settings
```

---

## Constitutional Compliance Checklist

After generating each component, verify:

- [ ] No "stronger/weaker signal" visual treatment
- [ ] No confidence indicators
- [ ] No aggregate scores
- [ ] Equal visual weight for all signal directions
- [ ] Disclaimer always visible on AI content
- [ ] No resolution of contradictions
- [ ] No trading action buttons (buy/sell)
- [ ] No prescriptive language in any text

---

*Document created: January 3, 2026*
*For use with: CIA-SIE Frontend Development*
