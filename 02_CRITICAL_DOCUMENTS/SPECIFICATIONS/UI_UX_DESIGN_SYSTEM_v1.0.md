# CIA-SIE UI/UX Design System v1.0

## Complete Interface Specification

**Document ID:** SPEC-UIUX-001  
**Version:** 1.0.0  
**Date:** January 5, 2026  
**Status:** AUTHORITATIVE  
**Design Philosophy:** Bright, Motivational, Professional

---

# TABLE OF CONTENTS

1. [Design Philosophy](#1-design-philosophy)
2. [Design System Foundation](#2-design-system-foundation)
3. [Atomic Components](#3-atomic-components)
4. [MCC Screens](#4-mcc-screens)
5. [Frontend Application Screens](#5-frontend-application-screens)
6. [AI & Chat Screens](#6-ai--chat-screens)
7. [Forms & Modals](#7-forms--modals)
8. [Interaction Specifications](#8-interaction-specifications)
9. [Screen Flow Diagram](#9-screen-flow-diagram)
10. [Accessibility Requirements](#10-accessibility-requirements)
11. [Constitutional UI Rules](#11-constitutional-ui-rules)

---

# 1. DESIGN PHILOSOPHY

## 1.1 Core Principles

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CIA-SIE DESIGN PHILOSOPHY                                                   ║
║   ═════════════════════════                                                   ║
║                                                                               ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   BRIGHT & MOTIVATIONAL                                                 │ ║
║   │   ─────────────────────                                                 │ ║
║   │   • Clean white/cream backgrounds                                       │ ║
║   │   • Vibrant accent colors (teal, coral, gold)                          │ ║
║   │   • Generous whitespace for breathing room                              │ ║
║   │   • Subtle gradients for depth and energy                              │ ║
║   │                                                                         │ ║
║   │   PROFESSIONAL & TRUSTWORTHY                                            │ ║
║   │   ──────────────────────────                                            │ ║
║   │   • Financial-grade typography (clear, readable)                        │ ║
║   │   • Consistent visual language                                          │ ║
║   │   • No gimmicks or distractions                                        │ ║
║   │   • Data-first hierarchy                                               │ ║
║   │                                                                         │ ║
║   │   PURPOSEFUL & EFFICIENT                                                │ ║
║   │   ──────────────────────                                                │ ║
║   │   • Every element serves a function                                    │ ║
║   │   • Zero decorative clutter                                            │ ║
║   │   • Instant comprehension                                              │ ║
║   │   • Millisecond interactions                                           │ ║
║   │                                                                         │ ║
║   │   CONSTITUTIONALLY COMPLIANT                                            │ ║
║   │   ──────────────────────────                                            │ ║
║   │   • Equal visual weight for contradictions                             │ ║
║   │   • Mandatory disclaimer always visible                                │ ║
║   │   • No action-oriented language                                        │ ║
║   │   • Information display, never recommendation                          │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 1.2 Inspiration

- **Bloomberg Terminal** — Data density, professional trust
- **Notion** — Clean whitespace, modern typography
- **Linear** — Smooth interactions, purposeful design
- **Stripe Dashboard** — Financial clarity, bright professionalism

---

# 2. DESIGN SYSTEM FOUNDATION

## 2.1 Color Palette

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   COLOR PALETTE - BRIGHT & MOTIVATIONAL                                       ║
║   ═════════════════════════════════════                                       ║
║                                                                               ║
║   PRIMARY BACKGROUNDS                                                         ║
║   ───────────────────                                                         ║
║   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 ║
║   │                │  │                │  │                │                 ║
║   │    #FFFFFF     │  │    #FAFBFC     │  │    #F4F5F7     │                 ║
║   │    Pure White  │  │    Snow        │  │    Cloud       │                 ║
║   │    (Primary)   │  │    (Cards)     │  │    (Sidebar)   │                 ║
║   │                │  │                │  │                │                 ║
║   └────────────────┘  └────────────────┘  └────────────────┘                 ║
║                                                                               ║
║   ACCENT COLORS (Vibrant & Energetic)                                        ║
║   ───────────────────────────────────                                        ║
║   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 ║
║   │   ████████     │  │   ████████     │  │   ████████     │                 ║
║   │    #0D9488     │  │    #F97316     │  │    #8B5CF6     │                 ║
║   │    Teal        │  │    Coral       │  │    Violet      │                 ║
║   │    (Primary    │  │    (Warning/   │  │    (AI/        │                 ║
║   │     Action)    │  │     Attention) │  │     Special)   │                 ║
║   └────────────────┘  └────────────────┘  └────────────────┘                 ║
║                                                                               ║
║   SEMANTIC COLORS (Signal States)                                            ║
║   ───────────────────────────────                                            ║
║   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 ║
║   │   ████████     │  │   ████████     │  │   ████████     │                 ║
║   │    #10B981     │  │    #EF4444     │  │    #6B7280     │                 ║
║   │    Emerald     │  │    Rose        │  │    Slate       │                 ║
║   │    (BULLISH)   │  │    (BEARISH)   │  │    (NEUTRAL)   │                 ║
║   └────────────────┘  └────────────────┘  └────────────────┘                 ║
║                                                                               ║
║   FRESHNESS COLORS                                                           ║
║   ────────────────                                                           ║
║   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 ║
║   │   ████████     │  │   ████████     │  │   ████████     │                 ║
║   │    #22C55E     │  │    #EAB308     │  │    #DC2626     │                 ║
║   │    Green       │  │    Amber       │  │    Red         │                 ║
║   │    (CURRENT)   │  │    (RECENT)    │  │    (STALE)     │                 ║
║   └────────────────┘  └────────────────┘  └────────────────┘                 ║
║                                                                               ║
║   TEXT COLORS                                                                 ║
║   ───────────                                                                 ║
║   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 ║
║   │                │  │                │  │                │                 ║
║   │    #111827     │  │    #4B5563     │  │    #9CA3AF     │                 ║
║   │    Charcoal    │  │    Gray        │  │    Silver      │                 ║
║   │    (Headings)  │  │    (Body)      │  │    (Muted)     │                 ║
║   │                │  │                │  │                │                 ║
║   └────────────────┘  └────────────────┘  └────────────────┘                 ║
║                                                                               ║
║   CONSTITUTIONAL COLORS (Special Purpose)                                    ║
║   ───────────────────────────────────────                                    ║
║   ┌────────────────┐  ┌────────────────┐                                     ║
║   │   ████████     │  │   ████████     │                                     ║
║   │    #FEF3C7     │  │    #FBBF24     │                                     ║
║   │    Cream       │  │    Gold        │                                     ║
║   │    (Banner BG) │  │    (Banner     │                                     ║
║   │                │  │     Border)    │                                     ║
║   └────────────────┘  └────────────────┘                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### CSS Variables

```css
:root {
  /* Backgrounds */
  --bg-primary: #FFFFFF;
  --bg-secondary: #FAFBFC;
  --bg-tertiary: #F4F5F7;
  --bg-hover: #F0F1F3;
  
  /* Accent */
  --accent-primary: #0D9488;      /* Teal */
  --accent-primary-light: #14B8A6;
  --accent-primary-dark: #0F766E;
  --accent-secondary: #F97316;    /* Coral */
  --accent-tertiary: #8B5CF6;     /* Violet */
  
  /* Semantic - Directions */
  --color-bullish: #10B981;       /* Emerald */
  --color-bullish-bg: #D1FAE5;
  --color-bearish: #EF4444;       /* Rose */
  --color-bearish-bg: #FEE2E2;
  --color-neutral: #6B7280;       /* Slate */
  --color-neutral-bg: #F3F4F6;
  
  /* Semantic - Freshness */
  --color-current: #22C55E;
  --color-current-bg: #DCFCE7;
  --color-recent: #EAB308;
  --color-recent-bg: #FEF9C3;
  --color-stale: #DC2626;
  --color-stale-bg: #FEE2E2;
  
  /* Text */
  --text-primary: #111827;
  --text-secondary: #4B5563;
  --text-muted: #9CA3AF;
  --text-inverse: #FFFFFF;
  
  /* Constitutional */
  --constitutional-bg: #FEF3C7;
  --constitutional-border: #FBBF24;
  --constitutional-text: #92400E;
  
  /* Borders */
  --border-light: #E5E7EB;
  --border-medium: #D1D5DB;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.10);
}
```

## 2.2 Typography

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   TYPOGRAPHY SYSTEM                                                           ║
║   ═════════════════                                                           ║
║                                                                               ║
║   FONT FAMILIES                                                               ║
║   ─────────────                                                               ║
║                                                                               ║
║   Primary:    "Plus Jakarta Sans"                                             ║
║               Modern, professional, excellent readability                     ║
║               Use for: Headings, body text, UI elements                       ║
║                                                                               ║
║   Monospace:  "JetBrains Mono"                                                ║
║               Technical, clear numbers                                        ║
║               Use for: Prices, codes, timestamps, data                        ║
║                                                                               ║
║   SCALE                                                                       ║
║   ─────                                                                       ║
║                                                                               ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   Display       48px / 3rem      Bold     "CIA-SIE"                     │ ║
║   │   ════════════════════════════════════════════════════                  │ ║
║   │                                                                         │ ║
║   │   H1            32px / 2rem      Semibold "Dashboard"                   │ ║
║   │   ════════════════════════════════════════════════                      │ ║
║   │                                                                         │ ║
║   │   H2            24px / 1.5rem    Semibold "Instruments"                 │ ║
║   │   ══════════════════════════════════════════════                        │ ║
║   │                                                                         │ ║
║   │   H3            20px / 1.25rem   Medium   "NIFTY 50"                    │ ║
║   │   ════════════════════════════════════════════                          │ ║
║   │                                                                         │ ║
║   │   H4            16px / 1rem      Medium   "Silo Name"                   │ ║
║   │   ══════════════════════════════════════                                │ ║
║   │                                                                         │ ║
║   │   Body          16px / 1rem      Regular  "Description text..."         │ ║
║   │   Body Small    14px / 0.875rem  Regular  "Secondary info..."           │ ║
║   │   Caption       12px / 0.75rem   Regular  "Timestamps, hints"           │ ║
║   │                                                                         │ ║
║   │   Mono Data     14px / 0.875rem  Medium   "24,532.50"                   │ ║
║   │   Mono Code     13px / 0.8125rem Regular  "NIFTY_01A"                   │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### CSS

```css
/* Font imports */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --font-primary: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Scale */
  --text-display: 3rem;      /* 48px */
  --text-h1: 2rem;           /* 32px */
  --text-h2: 1.5rem;         /* 24px */
  --text-h3: 1.25rem;        /* 20px */
  --text-h4: 1rem;           /* 16px */
  --text-body: 1rem;         /* 16px */
  --text-small: 0.875rem;    /* 14px */
  --text-caption: 0.75rem;   /* 12px */
  
  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

## 2.3 Spacing System

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   SPACING SYSTEM (8px Base Grid)                                              ║
║   ══════════════════════════════                                              ║
║                                                                               ║
║   --space-1:   4px   (0.25rem)  ─  Tight, inline elements                    ║
║   --space-2:   8px   (0.5rem)   ─  Icon gaps, small padding                  ║
║   --space-3:   12px  (0.75rem)  ─  Input padding, badge padding              ║
║   --space-4:   16px  (1rem)     ─  Card padding, standard gap                ║
║   --space-5:   20px  (1.25rem)  ─  Section padding                           ║
║   --space-6:   24px  (1.5rem)   ─  Card gap, large padding                   ║
║   --space-8:   32px  (2rem)     ─  Section gap                               ║
║   --space-10:  40px  (2.5rem)   ─  Page padding                              ║
║   --space-12:  48px  (3rem)     ─  Large section gap                         ║
║   --space-16:  64px  (4rem)     ─  Major section dividers                    ║
║                                                                               ║
║   BORDER RADIUS                                                               ║
║   ─────────────                                                               ║
║   --radius-sm:   4px   ─  Badges, small elements                             ║
║   --radius-md:   8px   ─  Buttons, inputs                                    ║
║   --radius-lg:   12px  ─  Cards, panels                                      ║
║   --radius-xl:   16px  ─  Modals, large containers                           ║
║   --radius-full: 9999px ─  Pills, avatars                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

# 3. ATOMIC COMPONENTS

## 3.1 Buttons

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   BUTTON SYSTEM                                                               ║
║   ═════════════                                                               ║
║                                                                               ║
║   PRIMARY (Main Actions)                                                      ║
║   ──────────────────────                                                      ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────┐   Background: #0D9488 (Teal)                    │ ║
║   │   │                   │   Text: #FFFFFF                                 │ ║
║   │   │   Start All       │   Border: none                                  │ ║
║   │   │                   │   Padding: 12px 24px                            │ ║
║   │   └───────────────────┘   Border-radius: 8px                            │ ║
║   │                           Font: 14px Semibold                           │ ║
║   │   Hover: #14B8A6 (lighter)                                              │ ║
║   │   Active: #0F766E (darker)                                              │ ║
║   │   Disabled: #9CA3AF background, #FFFFFF text                            │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   SECONDARY (Alternative Actions)                                            ║
║   ───────────────────────────────                                            ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────┐   Background: transparent                       │ ║
║   │   │                   │   Text: #0D9488                                 │ ║
║   │   │   View Details    │   Border: 1px solid #0D9488                     │ ║
║   │   │                   │   Padding: 12px 24px                            │ ║
║   │   └───────────────────┘   Border-radius: 8px                            │ ║
║   │                                                                         │ ║
║   │   Hover: #0D9488 background, #FFFFFF text                               │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   DANGER (Destructive Actions)                                               ║
║   ────────────────────────────                                               ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────┐   Background: #EF4444 (Rose)                    │ ║
║   │   │                   │   Text: #FFFFFF                                 │ ║
║   │   │   Delete          │   Border: none                                  │ ║
║   │   │                   │                                                 │ ║
║   │   └───────────────────┘   Hover: #DC2626 (darker)                       │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   GHOST (Subtle Actions)                                                     ║
║   ──────────────────────                                                     ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────┐   Background: transparent                       │ ║
║   │   │                   │   Text: #4B5563                                 │ ║
║   │   │   Cancel          │   Border: none                                  │ ║
║   │   │                   │                                                 │ ║
║   │   └───────────────────┘   Hover: #F4F5F7 background                     │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   EMERGENCY (Critical Actions - MCC Only)                                    ║
║   ───────────────────────────────────────                                    ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────┐   Background: #DC2626                           │ ║
║   │   │ ⚡ EMERGENCY STOP │   Text: #FFFFFF Bold                            │ ║
║   │   │                   │   Border: 2px solid #991B1B                     │ ║
║   │   └───────────────────┘   Animation: Subtle pulse when active           │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   BUTTON SIZES                                                               ║
║   ────────────                                                               ║
║   Small:   Padding 8px 16px,  Font 12px                                      ║
║   Medium:  Padding 12px 24px, Font 14px  (Default)                           ║
║   Large:   Padding 16px 32px, Font 16px                                      ║
║                                                                               ║
║   BUTTON STATES                                                              ║
║   ─────────────                                                              ║
║   Default → Hover → Active → Focus → Disabled → Loading                      ║
║                                                                               ║
║   Loading state: Show spinner icon, disable click                            ║
║   Focus state: 2px ring in accent color with 2px offset                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 3.2 Direction Badges

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   DIRECTION BADGES (Signal States)                                           ║
║   ════════════════════════════════                                           ║
║                                                                               ║
║   BULLISH                                                                    ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #D1FAE5 (Emerald-100)               │ ║
║   │   │  ▲  BULLISH     │   Text: #065F46 (Emerald-800)                     │ ║
║   │   └─────────────────┘   Border: 1px solid #10B981                       │ ║
║   │                         Icon: ▲ (Up arrow)                              │ ║
║   │                         Padding: 6px 12px                               │ ║
║   │                         Border-radius: 6px                              │ ║
║   │                         Font: 12px Semibold Uppercase                   │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   BEARISH                                                                    ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #FEE2E2 (Rose-100)                  │ ║
║   │   │  ▼  BEARISH     │   Text: #991B1B (Rose-800)                        │ ║
║   │   └─────────────────┘   Border: 1px solid #EF4444                       │ ║
║   │                         Icon: ▼ (Down arrow)                            │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   NEUTRAL                                                                    ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #F3F4F6 (Gray-100)                  │ ║
║   │   │  ─  NEUTRAL     │   Text: #374151 (Gray-700)                        │ ║
║   │   └─────────────────┘   Border: 1px solid #6B7280                       │ ║
║   │                         Icon: ─ (Horizontal line)                       │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   SIZES                                                                      ║
║   ─────                                                                      ║
║   Small (sm):  Padding 4px 8px,  Font 10px, Icon 10px                       ║
║   Medium (md): Padding 6px 12px, Font 12px, Icon 12px  (Default)            ║
║   Large (lg):  Padding 8px 16px, Font 14px, Icon 14px                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 3.3 Freshness Badges

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   FRESHNESS BADGES (Signal Age)                                              ║
║   ═════════════════════════════                                              ║
║                                                                               ║
║   CURRENT (≤2 minutes)                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #DCFCE7 (Green-100)                 │ ║
║   │   │  ● CURRENT      │   Text: #166534 (Green-800)                       │ ║
║   │   └─────────────────┘   Dot: #22C55E (pulsing animation)                │ ║
║   │                         Font: 11px Medium Uppercase                     │ ║
║   │                         Padding: 4px 10px                               │ ║
║   │                         Border-radius: 9999px (pill)                    │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   RECENT (2-10 minutes)                                                      ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #FEF9C3 (Amber-100)                 │ ║
║   │   │  ● RECENT       │   Text: #854D0E (Amber-800)                       │ ║
║   │   └─────────────────┘   Dot: #EAB308 (static)                           │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   STALE (>10 minutes)                                                        ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #FEE2E2 (Red-100)                   │ ║
║   │   │  ● STALE        │   Text: #991B1B (Red-800)                         │ ║
║   │   └─────────────────┘   Dot: #DC2626 (static)                           │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   UNAVAILABLE (No signal)                                                    ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────┐   Background: #F3F4F6 (Gray-100)                  │ ║
║   │   │  ○ NO DATA      │   Text: #6B7280 (Gray-500)                        │ ║
║   │   └─────────────────┘   Dot: Empty circle                               │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 3.4 Status Indicators

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   STATUS INDICATORS (Process/Service States)                                 ║
║   ══════════════════════════════════════════                                 ║
║                                                                               ║
║   RUNNING / HEALTHY                                                          ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────────────┐   Dot: #22C55E (Green)                  │ ║
║   │   │  ●  Running               │   Animation: Gentle pulse              │ ║
║   │   └───────────────────────────┘   Text: #166534                         │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   STARTING / PENDING                                                         ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────────────┐   Dot: #EAB308 (Amber)                  │ ║
║   │   │  ◐  Starting...           │   Animation: Spinning                  │ ║
║   │   └───────────────────────────┘   Text: #854D0E                         │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   STOPPED                                                                    ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────────────┐   Dot: #6B7280 (Gray)                   │ ║
║   │   │  ○  Stopped               │   Animation: None                       │ ║
║   │   └───────────────────────────┘   Text: #4B5563                         │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   ERROR / CRASHED                                                            ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌───────────────────────────┐   Dot: #EF4444 (Red)                    │ ║
║   │   │  ●  Crashed               │   Animation: Rapid pulse               │ ║
║   │   └───────────────────────────┘   Text: #991B1B                         │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 3.5 Cards

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CARD SYSTEM                                                                 ║
║   ═══════════                                                                 ║
║                                                                               ║
║   BASE CARD                                                                   ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────────────────────────────────────────────────────┐   │ ║
║   │   │                                                                 │   │ ║
║   │   │   Background: #FFFFFF                                           │   │ ║
║   │   │   Border: 1px solid #E5E7EB                                     │   │ ║
║   │   │   Border-radius: 12px                                           │   │ ║
║   │   │   Padding: 24px                                                 │   │ ║
║   │   │   Shadow: 0 1px 2px rgba(0,0,0,0.05)                           │   │ ║
║   │   │                                                                 │   │ ║
║   │   │   Hover: Shadow increases, border #D1D5DB                       │   │ ║
║   │   │                                                                 │   │ ║
║   │   └─────────────────────────────────────────────────────────────────┘   │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   INSTRUMENT CARD                                                            ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────────────────────────────────────────────────────┐   │ ║
║   │   │  NIFTY 50                                              View →   │   │ ║
║   │   │  ─────────────────────────────────────────────────────────────  │   │ ║
║   │   │                                                                 │   │ ║
║   │   │  3 Silos  •  12 Charts  •  5 Contradictions                    │   │ ║
║   │   │                                                                 │   │ ║
║   │   │  Last signal: 45 seconds ago                    ● CURRENT      │   │ ║
║   │   │                                                                 │   │ ║
║   │   └─────────────────────────────────────────────────────────────────┘   │ ║
║   │                                                                         │ ║
║   │   Hover: Entire card clickable, background #FAFBFC                      │ ║
║   │   Contradiction count uses coral color if > 0                           │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   CHART MINI-CARD                                                            ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌─────────────────────┐   Width: 120px                                │ ║
║   │   │  Chart 01A          │   Height: auto                                │ ║
║   │   │  5min               │   Background: #FAFBFC                         │ ║
║   │   │                     │   Border-radius: 8px                          │ ║
║   │   │  ▲ BULLISH          │   Padding: 12px                               │ ║
║   │   │                     │                                               │ ║
║   │   │  ● CURRENT          │   Chart code: 14px Mono Semibold             │ ║
║   │   └─────────────────────┘   Timeframe: 12px Muted                       │ ║
║   │                             Direction: Badge component                  │ ║
║   │                             Freshness: Badge component                  │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 3.6 Input Fields

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   INPUT FIELDS                                                               ║
║   ════════════                                                               ║
║                                                                               ║
║   TEXT INPUT                                                                 ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   Label *                                                               │ ║
║   │   ┌─────────────────────────────────────────────────────────────────┐   │ ║
║   │   │  Placeholder text...                                            │   │ ║
║   │   └─────────────────────────────────────────────────────────────────┘   │ ║
║   │   Helper text appears here                                              │ ║
║   │                                                                         │ ║
║   │   STATES:                                                               │ ║
║   │   Default:  Border #D1D5DB, Background #FFFFFF                          │ ║
║   │   Focus:    Border #0D9488 (2px), Shadow ring                           │ ║
║   │   Error:    Border #EF4444, Background #FEF2F2                          │ ║
║   │   Disabled: Background #F4F5F7, Text #9CA3AF                            │ ║
║   │                                                                         │ ║
║   │   Padding: 12px 16px                                                    │ ║
║   │   Border-radius: 8px                                                    │ ║
║   │   Font: 14px Regular                                                    │ ║
║   │   Label: 14px Medium, margin-bottom 6px                                 │ ║
║   │   Helper: 12px, color #6B7280 or #EF4444 for errors                    │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   SELECT / DROPDOWN                                                          ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   Model Selection                                                       │ ║
║   │   ┌─────────────────────────────────────────────────────────┬───────┐   │ ║
║   │   │  Claude 3.5 Sonnet (Recommended)                        │   ▼   │   │ ║
║   │   └─────────────────────────────────────────────────────────┴───────┘   │ ║
║   │                                                                         │ ║
║   │   Dropdown menu:                                                        │ ║
║   │   ┌─────────────────────────────────────────────────────────────────┐   │ ║
║   │   │  ✓ Claude 3.5 Sonnet (Recommended)                              │   │ ║
║   │   │    Claude 3 Haiku (Fast)                                        │   │ ║
║   │   │    Claude 3 Opus (Complex)                                      │   │ ║
║   │   └─────────────────────────────────────────────────────────────────┘   │ ║
║   │                                                                         │ ║
║   │   Menu: White background, shadow-lg, border-radius 8px                  │ ║
║   │   Item hover: Background #F4F5F7                                        │ ║
║   │   Selected: Checkmark icon, text #0D9488                                │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║   TOGGLE / SWITCH                                                            ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                         │ ║
║   │   ┌────────────────────────────────────────────────────────────────┐    │ ║
║   │   │  Enable Heartbeat                              ┌──────────┐   │    │ ║
║   │   │                                                │  ●───────│   │    │ ║
║   │   │                                                └──────────┘   │    │ ║
║   │   └────────────────────────────────────────────────────────────────┘    │ ║
║   │                                                                         │ ║
║   │   Off: Background #D1D5DB, knob left                                    │ ║
║   │   On:  Background #0D9488, knob right                                   │ ║
║   │   Size: 44px × 24px, knob 20px                                          │ ║
║   │   Animation: 150ms ease transition                                      │ ║
║   │                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

# 4. MCC SCREENS

## 4.1 MCC Dashboard

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                               ║
║   MCC DASHBOARD - BRIGHT THEME                                                                                ║
║   ════════════════════════════                                                                                ║
║                                                                                                               ║
║   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │  ◉ CIA-SIE Mission Control                                              ─    □    ✕           │ │   ║
║   │   │  Background: Linear gradient #FFFFFF → #FAFBFC                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌────────────────────┬────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                    │                                                                            │ │   ║
║   │   │   SIDEBAR          │   MAIN CONTENT                                                             │ │   ║
║   │   │   Background:      │   Background: #FFFFFF                                                      │ │   ║
║   │   │   #F4F5F7          │                                                                            │ │   ║
║   │   │                    │   ┌────────────────────────────────────────────────────────────────────┐   │ │   ║
║   │   │   ┌──────────────┐ │   │  SYSTEM STATUS                                                    │   │ │   ║
║   │   │   │ ● Dashboard  │ │   │  ════════════                                                     │   │ │   ║
║   │   │   └──────────────┘ │   │                                                                    │   │ │   ║
║   │   │   Selected:        │   │  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐   │   │ │   ║
║   │   │   BG #FFFFFF       │   │  │                  │ │                  │ │                  │   │   │ │   ║
║   │   │   Left border      │   │  │  🌐 BACKEND      │ │  💻 FRONTEND     │ │  🗄️ DATABASE     │   │   │ │   ║
║   │   │   #0D9488 (3px)    │   │  │                  │ │                  │ │                  │   │   │ │   ║
║   │   │                    │   │  │  ● Running       │ │  ● Running       │ │  ● Connected     │   │   │ │   ║
║   │   │   ○ Processes      │   │  │  Port 8000       │ │  Port 5174       │ │  245 KB          │   │   │ │   ║
║   │   │   ○ Logs           │   │  │  Uptime: 2h 15m  │ │  Uptime: 2h 14m  │ │  12 tables       │   │   │ │   ║
║   │   │   ○ Frontend       │   │  │                  │ │                  │ │                  │   │   │ │   ║
║   │   │   ○ API Docs       │   │  └──────────────────┘ └──────────────────┘ └──────────────────┘   │   │ │   ║
║   │   │   ○ Settings       │   │                                                                    │   │ │   ║
║   │   │                    │   │  Status cards: White bg, subtle shadow, green top border           │   │ │   ║
║   │   │   Unselected:      │   │                                                                    │   │ │   ║
║   │   │   Transparent      │   └────────────────────────────────────────────────────────────────────┘   │ │   ║
║   │   │   Text #4B5563     │                                                                            │ │   ║
║   │   │                    │   ┌────────────────────────────────────────────────────────────────────┐   │ │   ║
║   │   │   Hover:           │   │  QUICK ACTIONS                                                    │   │ │   ║
║   │   │   BG #FFFFFF       │   │  ═════════════                                                    │   │ │   ║
║   │   │                    │   │                                                                    │   │ │   ║
║   │   │                    │   │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────┐   │   │ │   ║
║   │   │                    │   │  │            │ │            │ │            │ │                │   │   │ │   ║
║   │   │                    │   │  │  ▶ START   │ │  ■ STOP    │ │  ↻ RESTART │ │ ⚡ EMERGENCY   │   │   │ │   ║
║   │   │                    │   │  │    ALL     │ │    ALL     │ │    ALL     │ │    STOP       │   │   │ │   ║
║   │   │                    │   │  │            │ │            │ │            │ │                │   │   │ │   ║
║   │   │                    │   │  │  Teal      │ │  Amber     │ │  Teal      │ │  Red pulsing  │   │   │ │   ║
║   │   │                    │   │  │  outline   │ │  outline   │ │  outline   │ │  filled       │   │   │ │   ║
║   │   │                    │   │  └────────────┘ └────────────┘ └────────────┘ └────────────────┘   │   │ │   ║
║   │   │                    │   │                                                                    │   │ │   ║
║   │   │                    │   │  ┌─────────────────────────────┐ ┌─────────────────────────────┐   │   │ │   ║
║   │   │                    │   │  │  🌐 Open Frontend           │ │  📖 Open API Docs           │   │   │ │   ║
║   │   │                    │   │  │  localhost:5174             │ │  localhost:8000/docs        │   │   │ │   ║
║   │   │                    │   │  └─────────────────────────────┘ └─────────────────────────────┘   │   │ │   ║
║   │   │                    │   │                                                                    │   │ │   ║
║   │   │                    │   │  Navigation buttons: White bg, teal left accent on hover          │   │ │   ║
║   │   │                    │   │                                                                    │   │ │   ║
║   │   │                    │   └────────────────────────────────────────────────────────────────────┘   │ │   ║
║   │   │                    │                                                                            │ │   ║
║   │   │   ─────────────    │   ┌────────────────────────────────────────────────────────────────────┐   │ │   ║
║   │   │                    │   │  RECENT ACTIVITY                                                   │   │ │   ║
║   │   │   v1.0.0           │   │  ═══════════════                                                   │   │ │   ║
║   │   │   © 2026           │   │                                                                    │   │ │   ║
║   │   │                    │   │  15:42:31  Backend started successfully                            │   │ │   ║
║   │   │                    │   │  15:42:33  Frontend started successfully                           │   │ │   ║
║   │   │                    │   │  15:42:35  Health check passed                                     │   │ │   ║
║   │   │                    │   │  15:43:01  Webhook received: NIFTY_01A                             │   │ │   ║
║   │   │                    │   │                                                                    │   │ │   ║
║   │   │                    │   │  Timestamps: Mono font, muted color                                │   │ │   ║
║   │   │                    │   │  Messages: Regular font, primary color                             │   │ │   ║
║   │   │                    │   │                                                                    │   │ │   ║
║   │   │                    │   └────────────────────────────────────────────────────────────────────┘   │ │   ║
║   │   │                    │                                                                            │ │   ║
║   │   └────────────────────┴────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

*[Document continues with remaining sections...]*


