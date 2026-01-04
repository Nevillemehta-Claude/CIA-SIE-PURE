# CIA-SIE MISSION CONTROL CONSOLE
## GUI Mockup Requirements v1.1.0

**Document Type:** Visual Design Specification
**Parent Specification:** MCC_GENESIS_BUILD_SPECIFICATION.md
**Design Language:** NASA Mission Control Inspired

---

## DESIGN PHILOSOPHY

The Mission Control Console draws inspiration from NASA's Mission Control Center, emphasizing:

1. **Information Density** - Maximum data visibility without clutter
2. **Status At A Glance** - Immediate visual recognition of system state
3. **Professional Aesthetic** - Dark theme with high contrast indicators
4. **Operational Focus** - Tools for monitoring and control, not decoration

---

## ⚡ CREATIVE LATITUDE DIRECTIVE (INVIOLABLE)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MANDATORY CURSOR IMPLEMENTATION PROTOCOL                  │
│                          VISUAL DESIGN SPECIFICATIONS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  THIS DIRECTIVE APPLIES TO ALL VISUAL SPECIFICATIONS IN THIS DOCUMENT       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Visual Design Latitude

**ALL visual specifications in this document—including colors, typography, spacing, component mockups, layout dimensions, animation specifications, and icon choices—are PROVIDED FOR DIRECTIONAL AND KNOWLEDGE PURPOSES ONLY.**

These mockups represent ONE POSSIBLE visual approach. Cursor has **FULL CREATIVE AUTHORITY** to:

1. **Redesign the Color Palette** - Use different colors, themes, or dynamic theming
2. **Substitute Typography** - Choose fonts Cursor considers more suitable or modern
3. **Modify Component Designs** - Create components with different dimensions, layouts, or styling
4. **Enhance Animations** - Implement more sophisticated or subtle motion design
5. **Replace Icons** - Use different icon libraries or custom icons
6. **Reimagine Page Layouts** - Propose layouts that Cursor deems more usable
7. **Add Visual Features** - Introduce visual improvements not specified here
8. **Adopt Modern UI Patterns** - Implement contemporary design patterns and micro-interactions

### What This Document Provides

| Aspect | Document Purpose | Cursor Authority |
|--------|------------------|------------------|
| Color Palette | Example color scheme with NASA inspiration | May replace entirely |
| Typography | Reference font choices and sizes | May substitute |
| Component Mockups | ASCII representations of possible components | May redesign |
| Page Layouts | Example page structures | May restructure |
| Animations | Suggested motion specifications | May enhance or replace |
| Responsive Design | Reference breakpoints | May adjust |
| Accessibility | WCAG 2.1 AA guidelines | **SHOULD maintain or exceed** |

### Design Principles (Recommended, Not Required)

The following principles are **RECOMMENDED** but Cursor may propose alternatives with justification:

- Dark theme for reduced eye strain during extended use
- High contrast status indicators for quick recognition
- Information density balanced with clarity
- Professional aesthetic suitable for serious operational use

### Cursor Implementation Plan: GUI/UX Section

When producing the **Cursor Implementation Plan** (required by the parent specification), Cursor MUST include a GUI/UX section that details:

1. **Visual Approach** - How Cursor interprets or modifies these mockups
2. **Design System** - Any design system or component library Cursor will employ
3. **Accessibility Strategy** - How WCAG compliance will be achieved
4. **Animation Philosophy** - Cursor's approach to motion design
5. **Responsive Strategy** - How different window sizes will be handled

### What Remains Inviolable

| Requirement | Status |
|-------------|--------|
| No Buy/Sell/Trade buttons (CR-001) | **INVIOLABLE** |
| No prescriptive language in UI text | **INVIOLABLE** |
| Accessibility (WCAG 2.1 AA minimum) | **STRONGLY RECOMMENDED** |
| Everything else in this document | **DIRECTIONAL** - Cursor may modify |

---

## COLOR PALETTE

> **Note:** The following color palette is a REFERENCE DESIGN. Cursor has full authority to substitute with an alternative palette that achieves the design goals stated above.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           COLOR SYSTEM                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BACKGROUNDS                                                                 │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ████████  mcc-bg       #0a0a0f   Main application background              │
│  ████████  mcc-panel    #12121a   Panel/card backgrounds                   │
│  ████████  mcc-border   #1e1e2e   Borders and dividers                     │
│  ████████  mcc-hover    #1a1a24   Hover state backgrounds                  │
│                                                                              │
│  STATUS COLORS                                                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ████████  mcc-success  #22c55e   Running, healthy, connected              │
│  ████████  mcc-warning  #f59e0b   Starting, stopping, degraded             │
│  ████████  mcc-error    #ef4444   Crashed, unhealthy, failed               │
│  ████████  mcc-neutral  #64748b   Stopped, unknown, idle                   │
│                                                                              │
│  ACCENT COLORS                                                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ████████  mcc-accent   #3b82f6   Primary actions, highlights              │
│  ████████  mcc-text     #e2e8f0   Primary text                             │
│  ████████  mcc-muted    #94a3b8   Secondary text, labels                   │
│                                                                              │
│  LOG LEVEL COLORS                                                            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ████████  log-debug    #8b5cf6   DEBUG level messages                     │
│  ████████  log-info     #3b82f6   INFO level messages                      │
│  ████████  log-warn     #f59e0b   WARN level messages                      │
│  ████████  log-error    #ef4444   ERROR level messages                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## TYPOGRAPHY

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TYPOGRAPHY SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Font Family: "Inter", system-ui, sans-serif                                │
│  Monospace: "JetBrains Mono", "Fira Code", monospace                        │
│                                                                              │
│  SIZES                                                                       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  text-xs    12px   0.75rem   Labels, metadata                               │
│  text-sm    14px   0.875rem  Body text, buttons                             │
│  text-base  16px   1rem      Primary content                                │
│  text-lg    18px   1.125rem  Section headers                                │
│  text-xl    20px   1.25rem   Page headers                                   │
│  text-2xl   24px   1.5rem    Dashboard metrics                              │
│                                                                              │
│  WEIGHTS                                                                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  font-normal    400   Body text                                             │
│  font-medium    500   Labels, buttons                                       │
│  font-semibold  600   Headers                                               │
│  font-bold      700   Emphasis, alerts                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## COMPONENT MOCKUPS

### 1. Custom Title Bar

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ═══════════════════════════════════════════════════════════════════════   │
│  ░░░ CIA-SIE MISSION CONTROL ░░░                           [_] [□] [×]     │
│  ═══════════════════════════════════════════════════════════════════════   │
└─────────────────────────────────────────────────────────────────────────────┘

SPECIFICATIONS:
- Height: 40px
- Background: mcc-bg (#0a0a0f)
- Title: "CIA-SIE MISSION CONTROL" in uppercase, centered
- Font: 14px, font-weight 600, letter-spacing 0.1em
- Window controls: minimize, maximize/restore, close
- Draggable region for window movement
- Double-click to maximize/restore
```

### 2. Sidebar Navigation

```
┌──────────────┐
│              │
│  ┌────────┐  │
│  │ 🏠     │  │  ← Active state: mcc-accent background
│  │Dashboard│  │    Hover: mcc-hover background
│  └────────┘  │    Text: mcc-text when active, mcc-muted when inactive
│              │
│  ┌────────┐  │
│  │ 📋     │  │
│  │Processes│  │
│  └────────┘  │
│              │
│  ┌────────┐  │
│  │ 📜     │  │
│  │ Logs   │  │
│  └────────┘  │
│              │
│  ┌────────┐  │
│  │ 🌐     │  │
│  │Frontend│  │
│  └────────┘  │
│              │
│  ┌────────┐  │
│  │ 📖     │  │
│  │API Docs│  │
│  └────────┘  │
│              │
│  ┌────────┐  │
│  │ ⚙️     │  │
│  │Settings│  │
│  └────────┘  │
│              │
└──────────────┘

SPECIFICATIONS:
- Width: 80px (collapsed) / 200px (expanded)
- Background: mcc-panel (#12121a)
- Border-right: 1px solid mcc-border
- Icon size: 24px
- Label: text-xs, hidden when collapsed
- Active indicator: 3px left border in mcc-accent
- Hover: background mcc-hover
```

### 3. Status Panel (Dashboard)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM STATUS                                     │
├────────────────────┬────────────────────┬────────────────────┬─────────────┤
│                    │                    │                    │             │
│  ●  Backend        │  ●  Frontend       │  ●  Database       │  Overall    │
│                    │                    │                    │             │
│  RUNNING           │  RUNNING           │  CONNECTED         │  HEALTHY    │
│                    │                    │                    │             │
│  Port 8000         │  Port 5173         │  SQLite            │  ✓ ✓ ✓     │
│  45ms response     │  23ms response     │  1 connection      │             │
│                    │                    │                    │             │
└────────────────────┴────────────────────┴────────────────────┴─────────────┘

SPECIFICATIONS:
- Container: mcc-panel background, rounded-lg, p-4
- Grid: 4 equal columns (grid-cols-4)
- Status indicator (●):
  - Running/Healthy: mcc-success + pulse animation
  - Starting/Degraded: mcc-warning + pulse animation
  - Stopped/Unhealthy: mcc-error (static)
- Status text: uppercase, font-semibold, text-sm
- Details: text-xs, mcc-muted color
- Overall column: shows combined status
```

### 4. Process Card

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ●  Backend Server                                    [Running]  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Command    python -m uvicorn src.main:app --reload             │
│  PID        12345                                                │
│  Port       8000                                                 │
│  Uptime     2h 34m 12s                                          │
│  Memory     156 MB                                               │
│  CPU        1.2%                                                 │
│  Health     ✓ Healthy (45ms)                                    │
│  Restarts   0                                                    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  [  Stop  ]    [  Restart  ]    [  View Logs  ]                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

SPECIFICATIONS:
- Container: mcc-panel background, rounded-lg, p-6
- Header: flex with status indicator, name, and badge
- Status badge:
  - Running: bg-success/20 text-success border-success
  - Stopped: bg-neutral/20 text-neutral border-neutral
  - Crashed: bg-error/20 text-error border-error
- Details grid: 2 columns, text-sm
- Labels: mcc-muted color
- Values: mcc-text color, monospace for technical values
- Buttons: flex gap-3, standard button styling
```

### 5. Process Control Buttons

```
BUTTON STATES:

[  Start  ]     Default state
├── Background: transparent
├── Border: 1px solid mcc-success
├── Text: mcc-success
├── Icon: Play icon (lucide-react)
└── Hover: bg-success/10

[  Stop  ]      Default state
├── Background: transparent
├── Border: 1px solid mcc-error
├── Text: mcc-error
├── Icon: Square icon (lucide-react)
└── Hover: bg-error/10

[  Restart  ]   Default state
├── Background: transparent
├── Border: 1px solid mcc-warning
├── Text: mcc-warning
├── Icon: RefreshCw icon (lucide-react)
└── Hover: bg-warning/10

[  View Logs  ] Default state
├── Background: transparent
├── Border: 1px solid mcc-accent
├── Text: mcc-accent
├── Icon: Terminal icon (lucide-react)
└── Hover: bg-accent/10

DISABLED STATE (all buttons):
├── Opacity: 0.5
├── Cursor: not-allowed
└── No hover effect

BUTTON SIZE:
├── Padding: px-4 py-2
├── Font: text-sm font-medium
├── Border-radius: rounded-md
└── Min-width: 100px
```

### 6. Quick Actions Panel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            QUICK ACTIONS                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │                 │  │                 │  │                 │              │
│  │    ▶ Start      │  │    ■ Stop       │  │   ↻ Restart     │              │
│  │      All        │  │      All        │  │      All        │              │
│  │                 │  │                 │  │                 │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
│  ┌───────────────────────────────┐  ┌───────────────────────────────┐       │
│  │                               │  │                               │       │
│  │   🌐 Open Frontend            │  │   📖 Open API Docs            │       │
│  │   localhost:5173              │  │   localhost:8000/docs         │       │
│  │                               │  │                               │       │
│  └───────────────────────────────┘  └───────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

SPECIFICATIONS:
- Container: mcc-panel background, rounded-lg, p-6
- Section title: text-lg font-semibold mb-4
- Action buttons (top row):
  - Size: 120px x 80px
  - Layout: flex flex-col items-center justify-center
  - Gap: gap-4
- Navigation buttons (bottom row):
  - Size: full width, 60px height
  - Layout: flex items-center gap-3
  - URL text: text-xs mcc-muted
```

### 7. Log Viewer

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Filters:                                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────────────┐  ┌──────┐ │
│  │ All Levels ▼│  │ All Sources▼│  │ 🔍 Search...              │  │Clear │ │
│  └─────────────┘  └─────────────┘  └───────────────────────────┘  └──────┘ │
│                                                                              │
│  ☑ Auto-scroll    ☑ Timestamps    ☑ Line numbers                           │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  001  10:45:23.456  INFO   backend   Server started on port 8000            │
│  002  10:45:23.789  INFO   frontend  Vite dev server running at 5173        │
│  003  10:45:24.012  DEBUG  backend   Database connection established        │
│  004  10:45:25.567  WARN   backend   Slow query detected: 245ms             │
│  005  10:45:26.890  ERROR  frontend  Failed to fetch /api/health            │
│  006  10:45:27.123  INFO   backend   Request: GET /api/instruments          │
│  007  10:45:27.456  DEBUG  backend   Response: 200 OK (23ms)                │
│  008  10:45:28.789  INFO   mcc       Health check passed                    │
│                                                                              │
│  ...                                                                         │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Showing 234 of 1,456 entries                           [Export]            │
└─────────────────────────────────────────────────────────────────────────────┘

SPECIFICATIONS:
- Container: full height, flex flex-col
- Filter bar: h-16, flex items-center gap-4, bg-mcc-panel
- Dropdowns: w-32, bg-mcc-bg, border-mcc-border
- Search: flex-1 max-w-xs, bg-mcc-bg
- Checkboxes: accent-mcc-accent
- Log area: flex-1, overflow-auto, font-mono text-sm
- Line format: line-number | timestamp | level | source | message
- Level badges:
  - DEBUG: bg-purple-500/20 text-purple-400
  - INFO: bg-blue-500/20 text-blue-400
  - WARN: bg-yellow-500/20 text-yellow-400
  - ERROR: bg-red-500/20 text-red-400
- Source: mcc-muted, w-20 truncate
- Message: mcc-text, flex-1
- Footer: h-12, flex justify-between items-center
```

### 8. Metrics Cards

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│                     │  │                     │  │                     │
│  TOTAL MEMORY       │  │  CPU USAGE          │  │  UPTIME             │
│                     │  │                     │  │                     │
│  312 MB             │  │  2.1%               │  │  4h 23m             │
│                     │  │                     │  │                     │
│  ░░░░░░░░░░░░░     │  │  ░░                 │  │  ████████████████   │
│  62% of 500MB limit │  │  Target: <5%        │  │  Since 06:12:34     │
│                     │  │                     │  │                     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘

SPECIFICATIONS:
- Size: 200px x 140px
- Background: mcc-panel
- Border-radius: rounded-lg
- Padding: p-4
- Label: text-xs uppercase mcc-muted font-medium tracking-wide
- Value: text-2xl font-bold mcc-text
- Progress bar: h-2 rounded-full bg-mcc-bg
- Progress fill: bg-mcc-accent (or success/warning/error based on threshold)
- Subtext: text-xs mcc-muted
```

### 9. Settings Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  SETTINGS                                                                    │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PATHS                                                                       │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Project Root                                                                │
│  ┌───────────────────────────────────────────────────────────────┐ [Browse] │
│  │ /Users/nevil/Downloads/CIA-SIE-PURE                           │          │
│  └───────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  Backend Directory                                                           │
│  ┌───────────────────────────────────────────────────────────────┐ [Browse] │
│  │ /Users/nevil/Downloads/CIA-SIE-PURE                           │          │
│  └───────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  Frontend Directory                                                          │
│  ┌───────────────────────────────────────────────────────────────┐ [Browse] │
│  │ /Users/nevil/Downloads/CIA-SIE-PURE/frontend                  │          │
│  └───────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  PORTS                                                                       │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Backend Port          Frontend Port                                         │
│  ┌─────────────┐       ┌─────────────┐                                      │
│  │    8000     │       │    5173     │                                      │
│  └─────────────┘       └─────────────┘                                      │
│                                                                              │
│  BEHAVIOR                                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ☐ Auto-start services on launch                                            │
│  ☑ Minimize to system tray when closed                                      │
│  ☑ Show notifications for status changes                                    │
│                                                                              │
│  Health Check Interval                                                       │
│  ┌─────────────┐                                                            │
│  │  5000 ms    │                                                            │
│  └─────────────┘                                                            │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│                                     [Reset to Defaults]    [Save Settings]  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

SPECIFICATIONS:
- Layout: max-w-2xl mx-auto
- Section headers: text-lg font-semibold mb-4, uppercase tracking-wide
- Section dividers: border-t border-mcc-border my-6
- Input fields:
  - Background: bg-mcc-bg
  - Border: border border-mcc-border
  - Focus: ring-2 ring-mcc-accent
  - Font: font-mono for paths
- Browse button: secondary style, w-24
- Port inputs: w-32, text-center
- Checkboxes: accent-mcc-accent, with label to right
- Number inputs: w-32
- Action buttons:
  - Reset: secondary/outline style
  - Save: primary style with mcc-accent background
```

### 10. WebView Container

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  FRONTEND VIEW                                            [↗ Open External] │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │                                                                        │  │
│  │                    [WebView: localhost:5173]                          │  │
│  │                                                                        │  │
│  │                    CIA-SIE Frontend Application                       │  │
│  │                    embedded in Electron WebView                       │  │
│  │                                                                        │  │
│  │                                                                        │  │
│  │                                                                        │  │
│  │                                                                        │  │
│  │                                                                        │  │
│  │                                                                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ● Connected    URL: http://localhost:5173    [Reload]  [DevTools]  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

SPECIFICATIONS:
- Header: flex justify-between items-center h-12
- Title: text-lg font-semibold
- External link button: icon button with external-link icon
- WebView container: flex-1, border border-mcc-border rounded-lg overflow-hidden
- Status bar: h-10 flex items-center gap-4 px-4 bg-mcc-panel
- Connection indicator: same as status panel
- URL: font-mono text-sm mcc-muted
- Actions: Reload and DevTools buttons, icon-only
```

---

## PAGE LAYOUTS

### Dashboard Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  [Title Bar: CIA-SIE MISSION CONTROL]                          [_] [□] [×]     │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│              │                                                                   │
│  [Sidebar]   │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │                    SYSTEM STATUS                         │  │
│  Dashboard   │   │  [Backend] [Frontend] [Database] [Overall]              │  │
│  ───────     │   └──────────────────────────────────────────────────────────┘  │
│  Processes   │                                                                   │
│  Logs        │   ┌──────────────────────────────────────────────────────────┐  │
│  Frontend    │   │                   QUICK ACTIONS                          │  │
│  API Docs    │   │  [Start All] [Stop All] [Restart All]                   │  │
│  Settings    │   │  [Open Frontend] [Open API Docs]                         │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│              │   ┌─────────────┬─────────────┬─────────────┐                   │
│              │   │  Memory     │  CPU        │  Uptime     │                   │
│              │   │  312 MB     │  2.1%       │  4h 23m     │                   │
│              │   └─────────────┴─────────────┴─────────────┘                   │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │                  RECENT ACTIVITY                         │  │
│              │   │  [Last 10 log entries...]                               │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│  [Status Bar: Version | Backend Status | Frontend Status]                       │
└─────────────────────────────────────────────────────────────────────────────────┘

GRID:
- Main content: grid gap-6
- Status panel: full width
- Quick actions: full width
- Metrics: grid-cols-3
- Recent activity: full width
```

### Processes Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  [Title Bar]                                                   [_] [□] [×]     │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│              │                                                                   │
│  [Sidebar]   │   PROCESSES                                                      │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  [ProcessCard: Backend]                                  │  │
│              │   │  ● Running | PID 12345 | Port 8000 | 156 MB             │  │
│              │   │  [Stop] [Restart] [View Logs] [View Output]             │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  [ProcessCard: Frontend]                                 │  │
│              │   │  ● Running | PID 12346 | Port 5173 | 89 MB              │  │
│              │   │  [Stop] [Restart] [View Logs] [View Output]             │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  PROCESS OUTPUT                                          │  │
│              │   │  [Real-time stdout/stderr from selected process]        │  │
│              │   │  ...                                                     │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│  [Status Bar]                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

GRID:
- Process cards: grid-cols-1 gap-4
- Output viewer: full width, flex-1
```

### Logs Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  [Title Bar]                                                   [_] [□] [×]     │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│              │                                                                   │
│  [Sidebar]   │   LOGS                                                           │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  [Filter Bar]                                            │  │
│              │   │  Level: [▼] Source: [▼] Search: [    ] [Clear]          │  │
│              │   │  ☑ Auto-scroll  ☑ Timestamps  ☑ Line numbers            │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  [Log Entries - Virtual Scrolling]                       │  │
│              │   │  001 10:45:23 INFO   backend   Server started...         │  │
│              │   │  002 10:45:24 INFO   frontend  Vite running...           │  │
│              │   │  003 10:45:25 DEBUG  backend   DB connected...           │  │
│              │   │  ...                                                      │  │
│              │   │                                                           │  │
│              │   │                                                           │  │
│              │   │                                                           │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  Showing 234 of 1,456 entries            [Export Logs]   │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│  [Status Bar]                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

LAYOUT:
- Filter bar: sticky top, bg-mcc-panel
- Log viewer: flex-1, virtual scrolling
- Footer: sticky bottom, bg-mcc-panel
```

---

## RESPONSIVE BREAKPOINTS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RESPONSIVE DESIGN                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Minimum Window Size: 1024 x 768                                            │
│                                                                              │
│  BREAKPOINTS:                                                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  sm:  1024px   Minimum supported width, sidebar collapsed by default       │
│  md:  1280px   Sidebar expanded, 2-column layouts                          │
│  lg:  1440px   Full feature display, 3-column metrics                      │
│  xl:  1920px   Maximum content width with side margins                     │
│                                                                              │
│  SIDEBAR BEHAVIOR:                                                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│  < 1280px: Collapsed (80px), icons only, expandable on hover               │
│  ≥ 1280px: Expanded (200px), icons + labels                                │
│                                                                              │
│  CONTENT AREA:                                                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Padding: p-6                                                                │
│  Max-width: 1600px                                                          │
│  Centered: mx-auto                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ANIMATION SPECIFICATIONS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ANIMATIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STATUS INDICATOR PULSE                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  @keyframes pulse {                                                          │
│    0%, 100% { opacity: 1; }                                                 │
│    50% { opacity: 0.5; }                                                    │
│  }                                                                           │
│  Duration: 2s                                                                │
│  Applied to: Running/Healthy status indicators                              │
│                                                                              │
│  BUTTON HOVER TRANSITION                                                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  transition: all 150ms ease-in-out                                          │
│  Properties: background-color, border-color, transform                       │
│                                                                              │
│  SIDEBAR EXPAND/COLLAPSE                                                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  transition: width 200ms ease-out                                           │
│                                                                              │
│  PAGE TRANSITIONS                                                            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  transition: opacity 150ms ease-in-out                                      │
│  Enter: opacity 0 → 1                                                       │
│  Exit: opacity 1 → 0                                                        │
│                                                                              │
│  LOG ENTRY APPEAR                                                            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  @keyframes slideIn {                                                        │
│    from { opacity: 0; transform: translateY(-10px); }                       │
│    to { opacity: 1; transform: translateY(0); }                             │
│  }                                                                           │
│  Duration: 200ms                                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ICON SPECIFICATIONS

Using Lucide React icons throughout:

| Icon | Usage | Size |
|------|-------|------|
| `Home` | Dashboard nav | 24px |
| `Layers` | Processes nav | 24px |
| `ScrollText` | Logs nav | 24px |
| `Globe` | Frontend nav | 24px |
| `BookOpen` | API Docs nav | 24px |
| `Settings` | Settings nav | 24px |
| `Play` | Start button | 16px |
| `Square` | Stop button | 16px |
| `RefreshCw` | Restart button | 16px |
| `Terminal` | View logs | 16px |
| `ExternalLink` | Open external | 16px |
| `Minus` | Minimize window | 16px |
| `Square` | Maximize window | 16px |
| `X` | Close window | 16px |
| `Search` | Search input | 16px |
| `ChevronDown` | Dropdown | 16px |
| `Check` | Checkbox checked | 16px |
| `Circle` | Status indicator | 8px |
| `Download` | Export | 16px |
| `Folder` | Browse | 16px |

---

## ACCESSIBILITY REQUIREMENTS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ACCESSIBILITY (WCAG 2.1 AA)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  COLOR CONTRAST                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Text on backgrounds: minimum 4.5:1 ratio                                 │
│  □ Large text (18px+): minimum 3:1 ratio                                    │
│  □ UI components: minimum 3:1 ratio against adjacent colors                 │
│                                                                              │
│  KEYBOARD NAVIGATION                                                         │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ All interactive elements focusable via Tab                               │
│  □ Focus visible with ring-2 ring-mcc-accent                                │
│  □ Escape closes modals/dropdowns                                           │
│  □ Enter activates buttons                                                  │
│  □ Arrow keys navigate within components                                    │
│                                                                              │
│  SCREEN READERS                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ All images have alt text                                                 │
│  □ Buttons have accessible names                                            │
│  □ Status changes announced via aria-live                                   │
│  □ Form inputs have associated labels                                       │
│                                                                              │
│  MOTION                                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Respect prefers-reduced-motion                                           │
│  □ No flashing content > 3 times per second                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-04 | Claude Code | Initial mockup specification |
| 1.1.0 | 2026-01-04 | Claude Code | **MAJOR REVISION**: Added Creative Latitude Directive granting Cursor full visual design freedom. All color, typography, component, and layout specifications now serve as directional guidance only. Cursor explicitly permitted to redesign, enhance, or replace any visual element. |

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
