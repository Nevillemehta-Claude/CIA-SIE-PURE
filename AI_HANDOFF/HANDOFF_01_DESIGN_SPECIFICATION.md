# HANDOFF_01: DESIGN SPECIFICATION

**Source:** `CIA-SIE_INTERACTIVE_USER_MANUAL.html`
**Purpose:** Define exact visual requirements for frontend rebuild

---

## 1. OVERALL LAYOUT

### Application Container
```
+------------------+----------------------------------------+
|                  |                                        |
|    SIDEBAR       |           MAIN CONTENT                 |
|    (280px)       |           (flex: 1)                    |
|    Fixed         |           Scrollable                   |
|                  |                                        |
+------------------+----------------------------------------+
```

### Layout CSS
```css
.app-container {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 280px;
    background: #0f172a;  /* --bg-dark */
    position: fixed;
    height: 100vh;
    overflow-y: auto;
}

.main-content {
    flex: 1;
    margin-left: 280px;
    min-height: 100vh;
}
```

---

## 2. COLOR PALETTE (CSS Variables)

```css
:root {
    /* Primary Colors */
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #3b82f6;

    /* Background Colors */
    --bg-dark: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: #ffffff;
    --bg-page: #f8fafc;

    /* Status Colors */
    --success: #10b981;
    --success-light: #d1fae5;
    --warning: #f59e0b;
    --warning-light: #fef3c7;
    --danger: #ef4444;
    --danger-light: #fee2e2;
    --neutral: #64748b;

    /* Text Colors */
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;

    /* Utility */
    --border: #e2e8f0;
    --shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
    --radius: 12px;
    --radius-sm: 8px;
}
```

---

## 3. TYPOGRAPHY

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
}

/* Headers */
.header-title { font-size: 36px; font-weight: 700; }
.section-title { font-size: 24px; font-weight: 600; }
.card-title { font-size: 18px; font-weight: 600; }
.accordion-title { font-size: 16px; font-weight: 500; }

/* Body Text */
.body-text { font-size: 14px; }
.small-text { font-size: 13px; }
.tiny-text { font-size: 12px; }
.label-text { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; }
```

---

## 4. SIDEBAR NAVIGATION

### Structure
```
SIDEBAR
├── Header
│   ├── Logo: "CIA-SIE"
│   └── Subtitle: "Interactive User Manual v1.0"
│
├── Nav Section: "Getting Started"
│   ├── 1. Introduction
│   ├── 2. System Requirements
│   └── 3. Starting the App
│
├── Nav Section: "Using CIA-SIE"
│   ├── 4. User Interface
│   ├── 5. Instruments
│   ├── 6. Signals
│   ├── 7. Contradictions
│   └── 8. AI Narratives
│
├── Nav Section: "Integration"
│   ├── 9. TradingView Setup
│   └── 10. Settings
│
└── Nav Section: "Reference"
    ├── ! Troubleshooting
    ├── ? Quick Reference
    └── # 12 Sample Charts
```

### Nav Item Styling
```css
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 8px;
    color: rgba(255,255,255,0.8);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}

.nav-item:hover {
    background: rgba(255,255,255,0.1);
    color: white;
}

.nav-item.active {
    background: var(--primary);
    color: white;
}
```

---

## 5. PAGE HEADER

### Visual
```
+------------------------------------------------------------------------+
|  [Badge: User Manual v1.0.0 | December 2025]                           |
|                                                                        |
|  CIA-SIE Interactive User Manual                                       |
|  Chart Intelligence Auditor & Signal Intelligence Engine               |
+------------------------------------------------------------------------+
```

### CSS
```css
.page-header {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
    color: white;
    padding: 60px 40px;
}

.header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    margin-bottom: 16px;
}
```

---

## 6. CONSTITUTIONAL BANNER (CRITICAL)

This banner MUST appear prominently on dashboard:

```
+------------------------------------------------------------------------+
|  ⚠ Constitutional Principles - Read First                              |
|                                                                        |
|  [1] Decision-Support NOT Decision-Making                              |
|  [2] Expose Contradictions, NEVER Resolve Them                         |
|  [3] Descriptive AI, NOT Prescriptive AI                               |
+------------------------------------------------------------------------+
```

### CSS
```css
.constitution-banner {
    background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
    border: 2px solid #f59e0b;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 30px;
}

.constitution-title {
    font-size: 18px;
    font-weight: 600;
    color: #92400e;
}
```

---

## 7. SIGNAL DIRECTION CARDS

### Visual
```
+----------------+  +----------------+  +----------------+
|       ↑        |  |       ↓        |  |       →        |
|    BULLISH     |  |    BEARISH     |  |    NEUTRAL     |
|  Upward bias   |  |  Downward bias |  |  No clear bias |
+----------------+  +----------------+  +----------------+
     GREEN              RED               GRAY
```

### CSS
```css
.signal-card.bullish {
    background: #d1fae5;
    border: 2px solid #10b981;
}

.signal-card.bearish {
    background: #fee2e2;
    border: 2px solid #ef4444;
}

.signal-card.neutral {
    background: #f1f5f9;
    border: 2px solid #64748b;
}
```

---

## 8. FRESHNESS INDICATORS

| Status | Color | Icon | Threshold |
|--------|-------|------|-----------|
| CURRENT | Green (#10b981) | 🟢 | ≤ 2 minutes |
| RECENT | Yellow (#f59e0b) | 🟡 | ≤ 10 minutes |
| STALE | Red (#ef4444) | 🔴 | > 30 minutes |
| UNAVAILABLE | Gray (#64748b) | ⚫ | Never received |

### Badge CSS
```css
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.badge.success { background: #d1fae5; color: #065f46; }
.badge.warning { background: #fef3c7; color: #92400e; }
.badge.danger { background: #fee2e2; color: #991b1b; }
.badge.neutral { background: #f1f5f9; color: #475569; }
```

---

## 9. CONTRADICTION DISPLAY (CRITICAL)

When charts disagree, show BOTH sides without resolution:

```
+------------------------------------------------------------------------+
|  ⚠ CONTRADICTION DETECTED                                              |
|                                                                        |
|  +------------------+      ⇄      +------------------+                 |
|  | Chart 01A        |             | Chart 02         |                 |
|  | Momentum Health  |             | HTF Structure    |                 |
|  |     ↑ BULLISH    |             |     ↓ BEARISH    |                 |
|  +------------------+             +------------------+                 |
|                                                                        |
|  Note: This contradiction is shown for your awareness.                 |
|  The system does NOT resolve this conflict.                            |
+------------------------------------------------------------------------+
```

---

## 10. ACCORDION COMPONENT

Used throughout for collapsible sections:

```css
.accordion-item {
    border-bottom: 1px solid var(--border);
    background: white;
}

.accordion-header {
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
}

.accordion-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;
}

.accordion-item.open .accordion-body {
    max-height: 2000px;
}
```

---

## 11. WORKFLOW DIAGRAM

Horizontal step indicator:

```
[1]──────[2]──────[3]──────[4]
 │        │        │        │
 Open    Navigate  Run     Browser
Terminal          Script   Opens
```

---

## 12. RESPONSIVE DESIGN

### Breakpoint: 900px

```css
@media (max-width: 900px) {
    .sidebar {
        transform: translateX(-100%);
    }

    .sidebar.open {
        transform: translateX(0);
    }

    .main-content {
        margin-left: 0;
    }

    .mobile-toggle {
        display: flex;
    }

    .page-header {
        padding: 40px 24px;
    }

    .content-area {
        padding: 24px;
    }
}
```

---

## 13. 12 SAMPLE CHART GRID

Display all 12 charts in a responsive grid:

```
+--------+--------+--------+--------+
|  01A   |   02   |  04A   |  04B   |
|Momentum| HTF    | Risk   | S/R    |
+--------+--------+--------+--------+
|  05A   |  05B   |  05C   |  05D   |
| VWAP   |Momentum|Extension| VWAP  |
+--------+--------+--------+--------+
|   06   |   07   |   08   |   09   |
| Macro  |Primary |Volume  | Order  |
+--------+--------+--------+--------+
```

### Grid CSS
```css
.chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
}

.chart-item {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    transition: all 0.2s;
}

.chart-item:hover {
    border-color: var(--primary);
    box-shadow: var(--shadow);
}

.chart-code {
    font-size: 20px;
    font-weight: 700;
    color: var(--primary);
}
```

---

## 14. COMMAND BOX (Terminal Display)

```css
.command-box {
    background: #0f172a;
    color: #10b981;
    font-family: 'Monaco', 'Menlo', monospace;
    padding: 16px 20px;
    border-radius: 8px;
    font-size: 14px;
}

.command-prefix {
    color: #94a3b8;
    user-select: none;
}
```

---

## 15. TAB COMPONENT

For AI model selection (Haiku/Sonnet/Opus):

```css
.tabs {
    display: flex;
    border-bottom: 2px solid var(--border);
    margin-bottom: 24px;
}

.tab {
    padding: 12px 24px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}

.tab.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}
```
