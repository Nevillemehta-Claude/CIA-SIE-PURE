# HANDOFF_06: CSS DESIGN SYSTEM

**Source:** Extracted from `CIA-SIE_INTERACTIVE_USER_MANUAL.html`
**Purpose:** Exact styling specifications for frontend rebuild

---

## CSS VARIABLES (ROOT)

```css
:root {
    /* ═══════════════════════════════════════════════════════════════
       PRIMARY COLORS
       ═══════════════════════════════════════════════════════════════ */
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #3b82f6;

    /* ═══════════════════════════════════════════════════════════════
       BACKGROUND COLORS
       ═══════════════════════════════════════════════════════════════ */
    --bg-dark: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: #ffffff;
    --bg-page: #f8fafc;

    /* ═══════════════════════════════════════════════════════════════
       STATUS COLORS
       ═══════════════════════════════════════════════════════════════ */
    --success: #10b981;
    --success-light: #d1fae5;
    --warning: #f59e0b;
    --warning-light: #fef3c7;
    --danger: #ef4444;
    --danger-light: #fee2e2;
    --neutral: #64748b;

    /* ═══════════════════════════════════════════════════════════════
       TEXT COLORS
       ═══════════════════════════════════════════════════════════════ */
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;

    /* ═══════════════════════════════════════════════════════════════
       BORDER & SHADOW
       ═══════════════════════════════════════════════════════════════ */
    --border: #e2e8f0;
    --shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);

    /* ═══════════════════════════════════════════════════════════════
       BORDER RADIUS
       ═══════════════════════════════════════════════════════════════ */
    --radius: 12px;
    --radius-sm: 8px;
}
```

---

## BASE STYLES

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: var(--bg-page);
    color: var(--text-primary);
    line-height: 1.6;
}
```

---

## LAYOUT

### App Container
```css
.app-container {
    display: flex;
    min-height: 100vh;
}
```

### Sidebar
```css
.sidebar {
    width: 280px;
    background: var(--bg-dark);
    color: white;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    z-index: 100;
    transition: transform 0.3s ease;
}

.sidebar-header {
    padding: 24px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-logo {
    font-size: 24px;
    font-weight: 700;
    color: white;
}

.sidebar-subtitle {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

.sidebar-nav {
    padding: 16px 0;
}
```

### Navigation Items
```css
.nav-section {
    padding: 0 16px;
    margin-bottom: 8px;
}

.nav-section-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 8px 12px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    color: rgba(255,255,255,0.8);
    text-decoration: none;
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

.nav-icon {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}
```

### Main Content
```css
.main-content {
    flex: 1;
    margin-left: 280px;
    min-height: 100vh;
}

.content-area {
    padding: 40px;
    max-width: 1200px;
}
```

---

## PAGE HEADER

```css
.page-header {
    background: linear-gradient(135deg, var(--bg-dark) 0%, var(--primary-dark) 100%);
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

.header-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 12px;
}

.header-desc {
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    max-width: 600px;
}
```

---

## SECTIONS

```css
.section {
    margin-bottom: 40px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-title::before {
    content: '';
    width: 4px;
    height: 28px;
    background: var(--primary);
    border-radius: 2px;
}
```

---

## CARDS

```css
.card {
    background: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
}

.card-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--border);
}

.card-title {
    font-size: 18px;
    font-weight: 600;
}

.card-body {
    padding: 24px;
}
```

---

## ACCORDION

```css
.accordion {
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    margin-bottom: 16px;
}

.accordion-item {
    border-bottom: 1px solid var(--border);
    background: white;
}

.accordion-item:last-child {
    border-bottom: none;
}

.accordion-header {
    padding: 18px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: background 0.2s;
    user-select: none;
}

.accordion-header:hover {
    background: var(--bg-page);
}

.accordion-header-content {
    display: flex;
    align-items: center;
    gap: 16px;
}

.accordion-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
}

.accordion-title {
    font-size: 16px;
    font-weight: 500;
    color: var(--text-primary);
}

.accordion-subtitle {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 2px;
}

.accordion-icon {
    width: 24px;
    height: 24px;
    transition: transform 0.3s;
    color: var(--text-muted);
}

.accordion-item.open .accordion-icon {
    transform: rotate(180deg);
}

.accordion-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;
}

.accordion-item.open .accordion-body {
    max-height: 2000px;
}

.accordion-content {
    padding: 24px;
    border-top: 1px solid var(--border);
    background: var(--bg-page);
}
```

---

## BADGES

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

.badge.success {
    background: var(--success-light);
    color: #065f46;
}

.badge.warning {
    background: var(--warning-light);
    color: #92400e;
}

.badge.danger {
    background: var(--danger-light);
    color: #991b1b;
}

.badge.neutral {
    background: #f1f5f9;
    color: var(--text-secondary);
}
```

---

## INFO BOXES

```css
.info-box {
    padding: 20px;
    border-radius: var(--radius-sm);
    margin-bottom: 16px;
}

.info-box.success {
    background: var(--success-light);
    border-left: 4px solid var(--success);
}

.info-box.warning {
    background: var(--warning-light);
    border-left: 4px solid var(--warning);
}

.info-box.danger {
    background: var(--danger-light);
    border-left: 4px solid var(--danger);
}

.info-box.info {
    background: #dbeafe;
    border-left: 4px solid var(--primary);
}

.info-box-title {
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
```

---

## COMMAND BOX

```css
.command-box {
    background: var(--bg-dark);
    color: #10b981;
    font-family: 'Monaco', 'Menlo', monospace;
    padding: 16px 20px;
    border-radius: var(--radius-sm);
    margin: 12px 0;
    font-size: 14px;
    overflow-x: auto;
}

.command-prefix {
    color: var(--text-muted);
    user-select: none;
}
```

---

## TABLES

```css
.table-wrapper {
    overflow-x: auto;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

th, td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

th {
    background: var(--bg-page);
    font-weight: 600;
    color: var(--text-secondary);
}

tr:last-child td {
    border-bottom: none;
}

tr:hover td {
    background: var(--bg-page);
}
```

---

## TABS

```css
.tabs {
    display: flex;
    gap: 0;
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
    transition: all 0.2s;
}

.tab:hover {
    color: var(--primary);
}

.tab.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}
```

---

## GRID LAYOUTS

```css
.grid {
    display: grid;
    gap: 20px;
}

.grid-2 {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.grid-3 {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.grid-4 {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
```

---

## CHART GRID

```css
.chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
}

.chart-item {
    background: white;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
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
    margin-bottom: 6px;
}

.chart-role {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.02em;
}
```

---

## SIGNAL CARDS

```css
.signal-demo {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.signal-card {
    flex: 1;
    min-width: 160px;
    padding: 20px;
    border-radius: var(--radius);
    text-align: center;
}

.signal-card.bullish {
    background: var(--success-light);
    border: 2px solid var(--success);
}

.signal-card.bearish {
    background: var(--danger-light);
    border: 2px solid var(--danger);
}

.signal-card.neutral {
    background: #f1f5f9;
    border: 2px solid var(--neutral);
}

.signal-icon {
    font-size: 32px;
    margin-bottom: 8px;
}

.signal-title {
    font-weight: 600;
    margin-bottom: 4px;
}

.signal-desc {
    font-size: 12px;
    color: var(--text-secondary);
}
```

---

## CONSTITUTIONAL BANNER

```css
.constitution-banner {
    background: linear-gradient(135deg, var(--warning-light) 0%, #fef9c3 100%);
    border: 2px solid var(--warning);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 30px;
}

.constitution-title {
    font-size: 18px;
    font-weight: 600;
    color: #92400e;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.constitution-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
}

.constitution-item {
    background: white;
    padding: 14px 18px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: #92400e;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.constitution-number {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    flex-shrink: 0;
}
```

---

## WORKFLOW DIAGRAM

```css
.workflow {
    display: flex;
    align-items: stretch;
    gap: 0;
    overflow-x: auto;
    padding: 20px 0;
}

.workflow-step {
    flex: 1;
    min-width: 180px;
    text-align: center;
    position: relative;
}

.workflow-step-content {
    background: white;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 16px;
    margin: 0 20px;
    position: relative;
    z-index: 1;
}

.workflow-step-number {
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 24px;
    height: 24px;
    background: var(--primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
}

.workflow-step-icon {
    font-size: 28px;
    margin-bottom: 12px;
}

.workflow-step-title {
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 6px;
}

.workflow-step-desc {
    font-size: 12px;
    color: var(--text-muted);
}

.workflow-step::after {
    content: '';
    position: absolute;
    top: 50%;
    right: 0;
    width: 40px;
    height: 2px;
    background: var(--border);
}

.workflow-step:last-child::after {
    display: none;
}
```

---

## QUICK REFERENCE CARDS

```css
.ref-card {
    background: white;
    border-radius: var(--radius);
    padding: 20px;
    box-shadow: var(--shadow);
    border-top: 4px solid var(--primary);
}

.ref-card-title {
    font-weight: 600;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ref-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
}

.ref-item:last-child {
    border-bottom: none;
}

.ref-label {
    font-size: 13px;
    color: var(--text-secondary);
    min-width: 100px;
}

.ref-value {
    font-size: 13px;
    font-weight: 500;
}
```

---

## RESPONSIVE DESIGN

```css
/* Mobile Toggle Button */
.mobile-toggle {
    display: none;
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 56px;
    height: 56px;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: var(--shadow-lg);
    z-index: 200;
    font-size: 24px;
}

/* Mobile Breakpoint: 900px */
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
        align-items: center;
        justify-content: center;
    }

    .page-header {
        padding: 40px 24px;
    }

    .content-area {
        padding: 24px;
    }

    .workflow {
        flex-direction: column;
    }

    .workflow-step::after {
        display: none;
    }
}

/* Print styles */
@media print {
    .sidebar, .mobile-toggle {
        display: none;
    }

    .main-content {
        margin-left: 0;
    }

    .accordion-body {
        max-height: none !important;
    }
}
```

---

## FOOTER

```css
.footer {
    background: var(--bg-dark);
    color: rgba(255,255,255,0.7);
    padding: 40px;
    margin-top: 60px;
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-bottom: 16px;
}

.footer-links a {
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    font-size: 14px;
}

.footer-links a:hover {
    color: white;
}
```

---

## TAILWIND CSS EQUIVALENTS

If using TailwindCSS, here are the equivalent classes:

| Custom CSS | TailwindCSS |
|------------|-------------|
| `--primary` | `blue-600` |
| `--bg-dark` | `slate-900` |
| `--bg-page` | `slate-50` |
| `--success` | `emerald-500` |
| `--warning` | `amber-500` |
| `--danger` | `red-500` |
| `--text-primary` | `slate-900` |
| `--text-secondary` | `slate-600` |
| `--text-muted` | `slate-400` |
| `--border` | `slate-200` |
| `--radius` | `rounded-xl` |
| `--radius-sm` | `rounded-lg` |
