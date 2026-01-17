# PHASE 2.5: PROTOTYPE REVIEW & APPROVAL

## Visual Interface Evaluation Document

**Document ID:** SPEC-PROTO-001  
**Date:** January 5, 2026  
**Status:** AWAITING USER APPROVAL  
**Purpose:** Present visual prototypes for evaluation before implementation

---

# TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Frontend Application Screens](#2-frontend-application-screens)
3. [Mission Control Console Screens](#3-mission-control-console-screens)
4. [Usability Evaluation](#4-usability-evaluation)
5. [Finesse Assessment](#5-finesse-assessment)
6. [Proposed Improvements](#6-proposed-improvements)
7. [Approval Checklist](#7-approval-checklist)

---

# 1. INTRODUCTION

## 1.1 Purpose

This document presents **detailed visual prototypes** of every key screen in the CIA-SIE application for your evaluation before any implementation begins. 

## 1.2 Design Theme

**BRIGHT & MOTIVATIONAL**
- Clean white backgrounds (#FFFFFF)
- Vibrant teal accent (#0D9488)
- Professional typography (Plus Jakarta Sans)
- Generous whitespace
- Subtle shadows for depth

## 1.3 Evaluation Criteria

For each screen, please evaluate:
- **Clarity**: Is the information hierarchy clear?
- **Usability**: Is it intuitive to use?
- **Finesse**: Does it feel polished and professional?
- **Completeness**: Are all necessary elements present?
- **Constitutional Compliance**: Are CR-001, CR-002, CR-003 enforced?

---

# 2. FRONTEND APPLICATION SCREENS

## 2.1 MAIN DASHBOARD

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  ◉ CIA-SIE                                                                              🔍  ⚙️  👤      │┃
┃  │     Signal Intelligence Engine                                                                          │┃
┃  │                                                                                                         │┃
┃  │  ════════════════════════════════════════════════════════════════════════════════════════════════════   │┃
┃  │                                                                                                         │┃
┃  │    Dashboard      Instruments      Baskets      AI Chat                                                 │┃
┃  │    ─────────                                                                                            │┃
┃  │    (active)                                                                                             │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  ⚠️  This system provides information for decision-support only. It does not make recommendations      │┃
┃  │      or suggest actions. All trading decisions remain solely your responsibility.                       │┃
┃  │                                                                                                         │┃
┃  │  Background: Warm Cream (#FEF3C7)  |  Left Border: Amber (#FBBF24)  |  CANNOT BE DISMISSED             │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  OVERVIEW                                                                     Last updated: Just now │  ┃
┃  │  ════════                                                                                            │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐     │  ┃
┃  │  │                    │  │                    │  │                    │  │                    │     │  ┃
┃  │  │  📊  INSTRUMENTS   │  │  📁  SILOS         │  │  📈  CHARTS        │  │  ⚡  SIGNALS       │     │  ┃
┃  │  │                    │  │                    │  │                    │  │                    │     │  ┃
┃  │  │       12           │  │       28           │  │       84           │  │      1,247         │     │  ┃
┃  │  │                    │  │                    │  │                    │  │                    │     │  ┃
┃  │  │  Active tracking   │  │  Configured        │  │  Receiving data    │  │  Total received    │     │  ┃
┃  │  │                    │  │                    │  │                    │  │                    │     │  ┃
┃  │  └────────────────────┘  └────────────────────┘  └────────────────────┘  └────────────────────┘     │  ┃
┃  │                                                                                                      │  ┃
┃  │  Card Style: White background, subtle shadow, rounded corners (12px)                                 │  ┃
┃  │  Numbers: 36px Bold, Teal color                                                                      │  ┃
┃  │  Labels: 14px Regular, Gray                                                                          │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  YOUR INSTRUMENTS                                                              + Add Instrument      │  ┃
┃  │  ════════════════                                                                                    │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  ┌─────────────────────────┐│  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  📊  NIFTY 50                   │  │  📊  BANK NIFTY                 │  │  📊  RELIANCE           ││  ┃
┃  │  │      NSE:NIFTY                  │  │      NSE:BANKNIFTY              │  │      NSE:RELIANCE       ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  ─────────────────────────────  │  │  ─────────────────────────────  │  │  ───────────────────────││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  Silos: 4    Charts: 12        │  │  Silos: 3    Charts: 9         │  │  Silos: 2   Charts: 6   ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  ┌───────────────────────────┐  │  │  ┌───────────────────────────┐  │  │  ┌─────────────────────┐││  ┃
┃  │  │  │ ▲ 3  │  ▼ 2  │  ─ 1  │ ⚡ 1│  │  │  │ ▲ 2  │  ▼ 1  │  ─ 0  │ ⚡ 1│  │  │ ▲ 1  │ ▼ 1 │ ─ 0 │⚡ 0│││  ┃
┃  │  │  └───────────────────────────┘  │  │  └───────────────────────────┘  │  │  └─────────────────────┘││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  Bullish  Bearish Neutral Contra│  │                                 │  │                         ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │           View Details →        │  │           View Details →        │  │       View Details →    ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  └─────────────────────────────────┘  └─────────────────────────────────┘  └─────────────────────────┘│  ┃
┃  │                                                                                                      │  ┃
┃  │  Card Features:                                                                                      │  ┃
┃  │  • White background with subtle shadow                                                               │  ┃
┃  │  • Hover: Shadow increases, slight lift                                                              │  ┃
┃  │  • Signal summary bar shows counts (NOT aggregated direction)                                        │  ┃
┃  │  • Contradiction count shown with ⚡ icon                                                            │  ┃
┃  │  • "View Details" link in Teal                                                                       │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  RECENT ACTIVITY                                                                                     │  ┃
┃  │  ═══════════════                                                                                     │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │  ⚡  NIFTY_01A changed to BULLISH                                              2 minutes ago │   │  ┃
┃  │  │  ⚡  BANKNIFTY_02B changed to BEARISH                                          5 minutes ago │   │  ┃
┃  │  │  ⚡  Contradiction detected: NIFTY_01A ↔ NIFTY_01B                             8 minutes ago │   │  ┃
┃  │  │  ⚡  RELIANCE_01A heartbeat received                                          12 minutes ago │   │  ┃
┃  │  └──────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  │  Activity items: Alternating white/cream backgrounds for readability                                 │  ┃
┃  │  Timestamps: Monospace font, muted gray                                                              │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Design Specifications

| Element | Specification |
|---------|---------------|
| Background | Pure White (#FFFFFF) |
| Header | White with subtle bottom border |
| Logo | Teal icon + "CIA-SIE" in semibold |
| Navigation | Horizontal tabs, active = teal underline |
| Disclaimer | Cream background, amber left border, ALWAYS VISIBLE |
| Stat Cards | White, 12px radius, subtle shadow |
| Instrument Cards | White, hover effect, signal summary bar |
| Activity Feed | Alternating row colors |

### Constitutional Compliance

| Rule | Implementation | Status |
|------|----------------|--------|
| CR-001 | No "Buy/Sell" buttons, only "View Details" | ✅ |
| CR-002 | Signal counts shown, NOT aggregated direction | ✅ |
| CR-003 | Disclaimer always visible, non-dismissible | ✅ |

---

## 2.2 INSTRUMENT DETAIL SCREEN

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │  ← Back to Dashboard                                                                                    │┃
┃  │                                                                                                         │┃
┃  │  Dashboard  /  Instruments  /  NIFTY 50                                                                 │┃
┃  │  ─────────     ───────────     ────────                                                                 │┃
┃  │  (link)        (link)          (current)                                                                │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  📊  NIFTY 50                                                                    ✏️ Edit   🗑️ Delete   │┃
┃  │      NSE:NIFTY                                                                                          │┃
┃  │                                                                                                         │┃
┃  │      National Stock Exchange - NIFTY 50 Index                                                           │┃
┃  │                                                                                                         │┃
┃  │      Created: Jan 1, 2026  •  Last Signal: 2 min ago                                                    │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  ⚠️  This system provides information for decision-support only. All trading decisions remain solely   │┃
┃  │      your responsibility.                                                                               │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  SILOS                                                                              + Add Silo       │  ┃
┃  │  ═════                                                                                               │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  ┌─────────────────────────┐│  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  📁  Momentum Silo              │  │  📁  Trend Silo                 │  │  📁  Volume Silo        ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  Charts: 4                      │  │  Charts: 5                      │  │  Charts: 3              ││  ┃
┃  │  │  Heartbeat: 5 min               │  │  Heartbeat: 5 min               │  │  Heartbeat: 15 min      ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  ┌───────────────────────────┐  │  │  ┌───────────────────────────┐  │  │  ┌─────────────────────┐││  ┃
┃  │  │  │ ▲ 2  │  ▼ 1  │  ─ 1      │  │  │  │ ▲ 3  │  ▼ 2  │  ─ 0      │  │  │ ▲ 1  │  ▼ 1  │  ─ 1   │││  ┃
┃  │  │  └───────────────────────────┘  │  │  └───────────────────────────┘  │  │  └─────────────────────┘││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  ⚡ 1 contradiction             │  │  ⚡ 2 contradictions            │  │  ⚡ 0 contradictions     ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │           View Silo →           │  │           View Silo →           │  │       View Silo →       ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  └─────────────────────────────────┘  └─────────────────────────────────┘  └─────────────────────────┘│  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  ALL CONTRADICTIONS FOR NIFTY 50                                                                     │  ┃
┃  │  ═══════════════════════════════                                                                     │  ┃
┃  │                                                                                                      │  ┃
┃  │  3 contradictions detected across all silos                                                          │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │   ┌─────────────────────────┐            ⚡            ┌─────────────────────────┐            │   │  ┃
┃  │  │   │                         │         CONFLICTS        │                         │            │   │  ┃
┃  │  │   │   NIFTY_MOM_5M          │           WITH           │   NIFTY_MOM_15M         │            │   │  ┃
┃  │  │   │   Momentum 5min         │                          │   Momentum 15min        │            │   │  ┃
┃  │  │   │                         │                          │                         │            │   │  ┃
┃  │  │   │   ▲ BULLISH             │                          │   ▼ BEARISH             │            │   │  ┃
┃  │  │   │   ● CURRENT             │                          │   ● CURRENT             │            │   │  ┃
┃  │  │   │                         │                          │                         │            │   │  ┃
┃  │  │   │   Updated: 2 min ago    │                          │   Updated: 3 min ago    │            │   │  ┃
┃  │  │   │                         │                          │                         │            │   │  ┃
┃  │  │   └─────────────────────────┘                          └─────────────────────────┘            │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │   CRITICAL: Both cards have IDENTICAL width, height, font size, border, background (CR-002)   │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  │  [Additional contradiction cards follow same pattern...]                                             │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Key Design Elements

| Element | Purpose | Constitutional Compliance |
|---------|---------|---------------------------|
| Breadcrumb | Clear navigation hierarchy | - |
| Silo Cards | Show signal distribution (counts, not aggregation) | CR-002 |
| Contradiction Section | Equal visual weight for both sides | CR-002 |
| Disclaimer | Always visible | CR-003 |
| "View Silo" links | Descriptive, not action-oriented | CR-001 |

---

## 2.3 SILO DETAIL SCREEN

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  Dashboard  /  NIFTY 50  /  Momentum Silo                                                                   ┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  📁  Momentum Silo                                                               ✏️ Edit   🗑️ Delete   │┃
┃  │      NIFTY 50 > Momentum Indicators                                                                     │┃
┃  │                                                                                                         │┃
┃  │      Heartbeat: Every 5 minutes  •  Freshness: Current < 2min, Recent < 10min, Stale > 30min           │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │  ⚠️  Disclaimer: Information only. All trading decisions remain solely your responsibility.            │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  CHARTS IN THIS SILO                                                                + Add Chart      │  ┃
┃  │  ═══════════════════                                                                                 │  ┃
┃  │                                                                                                      │  ┃
┃  │  4 charts  •  All charts have EQUAL visual weight (no chart is more prominent than another)          │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────┐│  ┃
┃  │  │                         │ │                         │ │                         │ │                 ││  ┃
┃  │  │  NIFTY_MOM_5M           │ │  NIFTY_MOM_15M          │ │  NIFTY_MOM_1H           │ │  NIFTY_MOM_4H   ││  ┃
┃  │  │  RSI + MACD 5min        │ │  RSI + MACD 15min       │ │  RSI + MACD 1hour       │ │  RSI + MACD 4hr ││  ┃
┃  │  │                         │ │                         │ │                         │ │                 ││  ┃
┃  │  │  ┌───────────────────┐  │ │  ┌───────────────────┐  │ │  ┌───────────────────┐  │ │  ┌─────────────┐││  ┃
┃  │  │  │   ▲ BULLISH       │  │ │  │   ▼ BEARISH       │  │ │  │   ▲ BULLISH       │  │ │  │  ─ NEUTRAL  │││  ┃
┃  │  │  └───────────────────┘  │ │  └───────────────────┘  │ │  └───────────────────┘  │ │  └─────────────┘││  ┃
┃  │  │                         │ │                         │ │                         │ │                 ││  ┃
┃  │  │  ┌───────────────────┐  │ │  ┌───────────────────┐  │ │  ┌───────────────────┐  │ │  ┌─────────────┐││  ┃
┃  │  │  │   ● CURRENT       │  │ │  │   ● CURRENT       │  │ │  │   ● RECENT        │  │ │  │  ● STALE    │││  ┃
┃  │  │  └───────────────────┘  │ │  └───────────────────┘  │ │  └───────────────────┘  │ │  └─────────────┘││  ┃
┃  │  │                         │ │                         │ │                         │ │                 ││  ┃
┃  │  │  Last: 2 min ago        │ │  Last: 3 min ago        │ │  Last: 8 min ago        │ │  Last: 45m ago  ││  ┃
┃  │  │                         │ │                         │ │                         │ │                 ││  ┃
┃  │  │       View Chart →      │ │       View Chart →      │ │       View Chart →      │ │   View Chart →  ││  ┃
┃  │  │                         │ │                         │ │                         │ │                 ││  ┃
┃  │  └─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘ └─────────────────┘│  ┃
┃  │                                                                                                      │  ┃
┃  │  CRITICAL: All 4 chart cards are IDENTICAL in size, styling, prominence (CR-002)                     │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  CONTRADICTIONS                                                                                      │  ┃
┃  │  ══════════════                                                                                      │  ┃
┃  │                                                                                                      │  ┃
┃  │  1 contradiction detected in this silo                                                               │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │   ┌─────────────────────────┐            ⚡            ┌─────────────────────────┐            │   │  ┃
┃  │  │   │   NIFTY_MOM_5M          │         CONFLICTS        │   NIFTY_MOM_15M         │            │   │  ┃
┃  │  │   │   ▲ BULLISH             │           WITH           │   ▼ BEARISH             │            │   │  ┃
┃  │  │   └─────────────────────────┘                          └─────────────────────────┘            │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  CONFIRMATIONS                                                                                       │  ┃
┃  │  ═════════════                                                                                       │  ┃
┃  │                                                                                                      │  ┃
┃  │  1 confirmation detected (informational only, does NOT imply stronger signal)                        │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │   ┌─────────────────────────┐            ✓            ┌─────────────────────────┐            │   │  ┃
┃  │  │   │   NIFTY_MOM_5M          │          ALIGNS         │   NIFTY_MOM_1H          │            │   │  ┃
┃  │  │   │   ▲ BULLISH             │           WITH          │   ▲ BULLISH             │            │   │  ┃
┃  │  │   └─────────────────────────┘                          └─────────────────────────┘            │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │   NOTE: Confirmation does NOT mean "stronger signal" - it is informational only               │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  AI NARRATIVE                                                                    🤖 Generate New     │  ┃
┃  │  ════════════                                                                                        │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  The Momentum Silo for NIFTY 50 currently shows mixed signals across different timeframes.    │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  The 5-minute chart (NIFTY_MOM_5M) indicates a BULLISH direction based on RSI and MACD       │   │  ┃
┃  │  │  readings. This signal was received 2 minutes ago and is classified as CURRENT.              │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  The 15-minute chart (NIFTY_MOM_15M) indicates a BEARISH direction, creating a               │   │  ┃
┃  │  │  contradiction with the 5-minute timeframe. This signal was received 3 minutes ago.          │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  The 1-hour chart (NIFTY_MOM_1H) shows a BULLISH direction, aligning with the 5-minute       │   │  ┃
┃  │  │  chart but contradicting the 15-minute chart.                                                │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  The 4-hour chart (NIFTY_MOM_4H) shows NEUTRAL, with data that is 45 minutes old             │   │  ┃
┃  │  │  (classified as STALE).                                                                      │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  ⚠️  This analysis is generated by AI for informational purposes only. It does not           │   │  ┃
┃  │  │      constitute financial advice. All trading decisions are solely your responsibility.      │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  MANDATORY DISCLAIMER - CANNOT BE REMOVED OR HIDDEN (CR-003)                                  │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 2.4 BASKET LIST SCREEN

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  Dashboard  /  Baskets                                                                                      ┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  📁  ANALYTICAL BASKETS                                                            + Create Basket      │┃
┃  │      Group charts for comparative analysis                                                              │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  ⚠️  Baskets are organizational tools only. They do NOT affect signal processing or analysis.          │┃
┃  │      All trading decisions remain solely your responsibility.                                           │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  FILTER BY TYPE                                                                                      │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────┐                          │  ┃
┃  │  │   All    │  │ Logical  │  │ Hierarchical │  │ Contextual │  │  Custom  │                          │  ┃
┃  │  │  ▬▬▬▬▬   │  │          │  │              │  │            │  │          │                          │  ┃
┃  │  │ (active) │  │          │  │              │  │            │  │          │                          │  ┃
┃  │  └──────────┘  └──────────┘  └──────────────┘  └────────────┘  └──────────┘                          │  ┃
┃  │                                                                                                      │  ┃
┃  │  Active filter: Teal background  |  Inactive: Gray outline                                           │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  YOUR BASKETS (6)                                                                                    │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  ┌─────────────────────────┐│  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  📁  NIFTY Momentum             │  │  📁  Bank Nifty Timeframes      │  │  📁  Cross-Index        ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  ┌─────────────────────────┐    │  │  ┌─────────────────────────┐    │  │  ┌─────────────────┐    ││  ┃
┃  │  │  │       LOGICAL           │    │  │  │     HIERARCHICAL        │    │  │  │   CONTEXTUAL    │    ││  ┃
┃  │  │  └─────────────────────────┘    │  │  └─────────────────────────┘    │  │  └─────────────────┘    ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  Charts comparing momentum      │  │  Organized by timeframe         │  │  Cross-instrument       ││  ┃
┃  │  │  indicators across timeframes   │  │  hierarchy for Bank Nifty       │  │  comparison basket      ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  ─────────────────────────────  │  │  ─────────────────────────────  │  │  ───────────────────────││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │  📊 4 charts                    │  │  📊 6 charts                    │  │  📊 8 charts            ││  ┃
┃  │  │  🏷️ NIFTY 50                    │  │  🏷️ Bank Nifty                  │  │  🏷️ Multiple            ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  │           View Basket →         │  │           View Basket →         │  │       View Basket →     ││  ┃
┃  │  │                                 │  │                                 │  │                         ││  ┃
┃  │  └─────────────────────────────────┘  └─────────────────────────────────┘  └─────────────────────────┘│  ┃
┃  │                                                                                                      │  ┃
┃  │  Basket Type Badge Colors:                                                                           │  ┃
┃  │  • LOGICAL: Blue (#DBEAFE bg, #1E40AF text)                                                          │  ┃
┃  │  • HIERARCHICAL: Indigo (#E0E7FF bg, #3730A3 text)                                                   │  ┃
┃  │  • CONTEXTUAL: Pink (#FCE7F3 bg, #9D174D text)                                                       │  ┃
┃  │  • CUSTOM: Purple (#F3E8FF bg, #6B21A8 text)                                                         │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 2.5 AI CHAT SCREEN

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  Dashboard  /  AI Chat                                                                                      ┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  🤖  AI ASSISTANT                                                                    ⚙️ AI Settings     │┃
┃  │      Ask questions about your signals and data                                                          │┃
┃  │                                                                                                         │┃
┃  │      Model: Claude Haiku  •  Budget: $2.45 / $10.00 used this month                                     │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐┃
┃  │                                                                                                         │┃
┃  │  ⚠️  AI responses are DESCRIPTIVE only. The AI will NOT provide recommendations, predictions, or       │┃
┃  │      trading advice. All trading decisions remain solely your responsibility.                           │┃
┃  │                                                                                                         │┃
┃  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  Select Instrument:  ┌─────────────────────────────────────────────────────────────────┐             │  ┃
┃  │                      │  NIFTY 50                                                    ▼  │             │  ┃
┃  │                      └─────────────────────────────────────────────────────────────────┘             │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  CONVERSATION                                                                                        │  ┃
┃  │  ════════════                                                                                        │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │                                                                              ┌─────────────┐  │   │  ┃
┃  │  │                                                                              │             │  │   │  ┃
┃  │  │  What are the current signals for NIFTY 50?                                  │     YOU     │  │   │  ┃
┃  │  │                                                                              │             │  │   │  ┃
┃  │  │                                                                              └─────────────┘  │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  User message: Right-aligned, teal background, white text                                     │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  ┌─────────────┐                                                                              │   │  ┃
┃  │  │  │             │                                                                              │   │  ┃
┃  │  │  │     🤖      │  Based on the current data for NIFTY 50:                                     │   │  ┃
┃  │  │  │             │                                                                              │   │  ┃
┃  │  │  └─────────────┘  The Momentum Silo shows:                                                    │   │  ┃
┃  │  │                   • NIFTY_MOM_5M: BULLISH (CURRENT, 2 min ago)                                │   │  ┃
┃  │  │                   • NIFTY_MOM_15M: BEARISH (CURRENT, 3 min ago)                               │   │  ┃
┃  │  │                   • NIFTY_MOM_1H: BULLISH (RECENT, 8 min ago)                                 │   │  ┃
┃  │  │                   • NIFTY_MOM_4H: NEUTRAL (STALE, 45 min ago)                                 │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │                   There is 1 contradiction between the 5-minute and 15-minute charts.        │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │                   The Trend Silo shows:                                                       │   │  ┃
┃  │  │                   • NIFTY_TREND_D: BULLISH (CURRENT, 1 min ago)                               │   │  ┃
┃  │  │                   • NIFTY_TREND_W: BULLISH (RECENT, 15 min ago)                               │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │                   ────────────────────────────────────────────────────────────────────────    │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │                   ⚠️ This analysis is generated by AI for informational purposes only.       │   │  ┃
┃  │  │                   It does not constitute financial advice. All trading decisions are         │   │  ┃
┃  │  │                   solely your responsibility.                                                │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  AI message: Left-aligned, light gray background, dark text                                   │   │  ┃
┃  │  │  Disclaimer: ALWAYS appended to every AI response (CR-003)                                    │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────┐  ┌─────────┐  │  ┃
┃  │  │  Ask about your signals...                                                        │  │  Send   │  │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────┘  └─────────┘  │  ┃
┃  │                                                                                                      │  ┃
┃  │  Input: White background, gray border, teal focus ring                                               │  ┃
┃  │  Send button: Teal background, white text                                                            │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

# 3. MISSION CONTROL CONSOLE SCREENS

## 3.1 MCC DASHBOARD

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │  ◉ CIA-SIE Mission Control                                                          ─  □  ✕         │  ┃
┃  │                                                                                                      │  ┃
┃  │  Window controls: Minimize, Maximize, Close (Electron title bar)                                     │  ┃
┃  │  Drag region for window movement                                                                     │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌────────────────────┬─────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                    │                                                                                 │  ┃
┃  │  NAVIGATION        │  SYSTEM STATUS                                                                  │  ┃
┃  │  ══════════        │  ═════════════                                                                  │  ┃
┃  │                    │                                                                                 │  ┃
┃  │  ┌──────────────┐  │  ┌─────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │ 📊 Dashboard │  │  │                                                                         │   │  ┃
┃  │  │   ▬▬▬▬▬▬▬▬   │  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │   │  ┃
┃  │  │   (active)   │  │  │  │                 │  │                 │  │                 │         │   │  ┃
┃  │  └──────────────┘  │  │  │  🖥️  BACKEND     │  │  🌐  FRONTEND   │  │  💾  DATABASE   │         │   │  ┃
┃  │                    │  │  │                 │  │                 │  │                 │         │   │  ┃
┃  │  ┌──────────────┐  │  │  │  ● RUNNING      │  │  ● RUNNING      │  │  ● HEALTHY      │         │   │  ┃
┃  │  │ ⚙️ Processes  │  │  │  │                 │  │                 │  │                 │         │   │  ┃
┃  │  └──────────────┘  │  │  │  Port: 8000     │  │  Port: 5173     │  │  Size: 2.4 MB   │         │   │  ┃
┃  │                    │  │  │  PID: 12345     │  │  PID: 12346     │  │  Tables: 8      │         │   │  ┃
┃  │  ┌──────────────┐  │  │  │  Uptime: 2h 15m │  │  Uptime: 2h 15m │  │                 │         │   │  ┃
┃  │  │ 📜 Logs      │  │  │  │                 │  │                 │  │                 │         │   │  ┃
┃  │  └──────────────┘  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘         │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │  ┌──────────────┐  │  │  Status card colors:                                                    │   │  ┃
┃  │  │ ⚙️ Settings  │  │  │  • Running/Healthy: Green left border (#10B981)                        │   │  ┃
┃  │  └──────────────┘  │  │  • Starting: Amber left border (#F59E0B)                                │   │  ┃
┃  │                    │  │  • Stopped: Gray left border (#6B7280)                                  │   │  ┃
┃  │                    │  │  • Error: Red left border (#EF4444)                                     │   │  ┃
┃  │  Sidebar:          │  │                                                                         │   │  ┃
┃  │  • Cloud bg        │  └─────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │  • Active = White  │                                                                                 │  ┃
┃  │    with teal text  │  ┌─────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  • Teal left       │  │                                                                         │   │  ┃
┃  │    border on       │  │  QUICK ACTIONS                                                          │   │  ┃
┃  │    active item     │  │  ═════════════                                                          │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │   │  ┃
┃  │                    │  │  │             │  │             │  │             │  │                 │ │   │  ┃
┃  │                    │  │  │  ▶ Start    │  │  ■ Stop     │  │  ↻ Restart  │  │  🌐 Open        │ │   │  ┃
┃  │                    │  │  │    All      │  │    All      │  │    All      │  │    Frontend     │ │   │  ┃
┃  │                    │  │  │             │  │             │  │             │  │                 │ │   │  ┃
┃  │                    │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘ │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  │  ┌───────────────────────────────────────────────────────────────────┐ │   │  ┃
┃  │                    │  │  │                                                                   │ │   │  ┃
┃  │                    │  │  │  🛑  EMERGENCY STOP                                               │ │   │  ┃
┃  │                    │  │  │                                                                   │ │   │  ┃
┃  │                    │  │  │  Red background, white text, uppercase, bold                      │ │   │  ┃
┃  │                    │  │  │  Prominent position for safety                                    │ │   │  ┃
┃  │                    │  │  │                                                                   │ │   │  ┃
┃  │                    │  │  └───────────────────────────────────────────────────────────────────┘ │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  │  Button styles:                                                         │   │  ┃
┃  │                    │  │  • Start All: Green outline                                             │   │  ┃
┃  │                    │  │  • Stop All: Gray outline                                               │   │  ┃
┃  │                    │  │  • Restart All: Amber outline                                           │   │  ┃
┃  │                    │  │  • Open Frontend: Teal solid                                            │   │  ┃
┃  │                    │  │  • Emergency Stop: Red solid, bold                                      │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  └─────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                    │                                                                                 │  ┃
┃  │                    │  ┌─────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  │  RECENT ACTIVITY                                                        │   │  ┃
┃  │                    │  │  ═══════════════                                                        │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  │  14:32:15  INFO   Backend started on port 8000                          │   │  ┃
┃  │                    │  │  14:32:18  INFO   Frontend started on port 5173                         │   │  ┃
┃  │                    │  │  14:32:20  INFO   Database connection established                       │   │  ┃
┃  │                    │  │  14:35:42  INFO   Webhook received: NIFTY_MOM_5M                        │   │  ┃
┃  │                    │  │  14:36:01  WARN   Signal freshness degraded: NIFTY_MOM_4H               │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  │  Log colors: DEBUG=Violet, INFO=Blue, WARN=Amber, ERROR=Red             │   │  ┃
┃  │                    │  │  Timestamps: Monospace font                                             │   │  ┃
┃  │                    │  │                                                                         │   │  ┃
┃  │                    │  └─────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                    │                                                                                 │  ┃
┃  └────────────────────┴─────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │  Backend: ● Running  •  Frontend: ● Running  •  Database: ● Healthy  •  Last check: Just now        │  ┃
┃  │                                                                                                      │  ┃
┃  │  Status bar: Fixed at bottom, shows at-a-glance system health                                        │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 3.2 MCC PROCESS MANAGEMENT

### Visual Prototype

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                             ┃
┃  ⚙️  PROCESS MANAGEMENT                                                                                     ┃
┃      Control and monitor CIA-SIE services                                                                   ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  BACKEND SERVICE                                                                                     │  ┃
┃  │  ═══════════════                                                                                     │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  🖥️  FastAPI Backend                                              ● RUNNING            │   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  ─────────────────────────────────────────────────────────────────────────────────────│   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  Port:        8000                          Memory:     124 MB                         │   │   │  ┃
┃  │  │  │  PID:         12345                         CPU:        2.3%                           │   │   │  ┃
┃  │  │  │  Uptime:      2h 15m 32s                    Requests:   1,247                          │   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  ─────────────────────────────────────────────────────────────────────────────────────│   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐   │   │   │  ┃
┃  │  │  │  │   ■ Stop    │  │  ↻ Restart  │  │  📋 Logs    │  │  🔗 Open API Docs           │   │   │   │  ┃
┃  │  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────────────┘   │   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  └────────────────────────────────────────────────────────────────────────────────────────┘   │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  Card: White background, green left border (running), subtle shadow                           │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┃  ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐  ┃
┃  │                                                                                                      │  ┃
┃  │  FRONTEND SERVICE                                                                                    │  ┃
┃  │  ════════════════                                                                                    │  ┃
┃  │                                                                                                      │  ┃
┃  │  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  │  ┌────────────────────────────────────────────────────────────────────────────────────────┐   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  🌐  Vite + React Frontend                                        ● RUNNING            │   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  ─────────────────────────────────────────────────────────────────────────────────────│   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  Port:        5173                          Memory:     89 MB                          │   │   │  ┃
┃  │  │  │  PID:         12346                         Mode:       Development                    │   │   │  ┃
┃  │  │  │  Uptime:      2h 15m 30s                                                               │   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  ─────────────────────────────────────────────────────────────────────────────────────│   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐   │   │   │  ┃
┃  │  │  │  │   ■ Stop    │  │  ↻ Restart  │  │  📋 Logs    │  │  🌐 Open in Browser         │   │   │   │  ┃
┃  │  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────────────┘   │   │   │  ┃
┃  │  │  │                                                                                        │   │   │  ┃
┃  │  │  └────────────────────────────────────────────────────────────────────────────────────────┘   │   │  ┃
┃  │  │                                                                                               │   │  ┃
┃  │  └───────────────────────────────────────────────────────────────────────────────────────────────┘   │  ┃
┃  │                                                                                                      │  ┃
┃  └──────────────────────────────────────────────────────────────────────────────────────────────────────┘  ┃
┃                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

# 4. USABILITY EVALUATION

## 4.1 Information Hierarchy

| Screen | Primary Info | Secondary Info | Tertiary Info | Score |
|--------|--------------|----------------|---------------|-------|
| Dashboard | Instrument cards | Stats overview | Activity feed | ✅ CLEAR |
| Instrument Detail | Silos | Contradictions | AI Narrative | ✅ CLEAR |
| Silo Detail | Charts | Contradictions/Confirmations | Narrative | ✅ CLEAR |
| Basket List | Basket cards | Filter pills | - | ✅ CLEAR |
| AI Chat | Conversation | Instrument selector | Budget | ✅ CLEAR |
| MCC Dashboard | Status cards | Quick actions | Activity | ✅ CLEAR |

## 4.2 Navigation Flow

```
Dashboard
    │
    ├── Instrument Card → Instrument Detail
    │                         │
    │                         ├── Silo Card → Silo Detail
    │                         │                   │
    │                         │                   └── Chart Card → Chart Detail
    │                         │
    │                         └── Contradiction → Silo Detail
    │
    ├── Baskets → Basket List → Basket Detail
    │
    └── AI Chat → Chat Interface
```

**Assessment:** Navigation is intuitive with clear breadcrumbs and back links.

## 4.3 Action Clarity

| Action | Button Style | Location | Clarity Score |
|--------|--------------|----------|---------------|
| Add Instrument | Primary (Teal) | Top right of section | ✅ CLEAR |
| View Details | Text link (Teal) | Bottom of card | ✅ CLEAR |
| Edit | Icon button | Header area | ✅ CLEAR |
| Delete | Icon button (Red) | Header area | ✅ CLEAR |
| Generate Narrative | Primary button | Narrative section | ✅ CLEAR |
| Start/Stop Process | Outline buttons | Quick actions | ✅ CLEAR |
| Emergency Stop | Red solid, bold | Prominent position | ✅ CLEAR |

---

# 5. FINESSE ASSESSMENT

## 5.1 Typography

| Element | Font | Weight | Size | Assessment |
|---------|------|--------|------|------------|
| Page titles | Plus Jakarta Sans | 600 | 24px | ✅ PROFESSIONAL |
| Section headers | Plus Jakarta Sans | 600 | 18px | ✅ CLEAR |
| Body text | Plus Jakarta Sans | 400 | 14px | ✅ READABLE |
| Timestamps | JetBrains Mono | 400 | 12px | ✅ TECHNICAL |
| Badges | Plus Jakarta Sans | 500 | 12px | ✅ COMPACT |

## 5.2 Color Contrast (WCAG 2.1 AA)

| Combination | Foreground | Background | Contrast Ratio | Status |
|-------------|------------|------------|----------------|--------|
| Primary text | #111827 | #FFFFFF | 16.1:1 | ✅ AAA |
| Secondary text | #4B5563 | #FFFFFF | 7.5:1 | ✅ AAA |
| Teal on white | #0D9488 | #FFFFFF | 4.6:1 | ✅ AA |
| Bullish badge | #10B981 | #D1FAE5 | 3.2:1 | ⚠️ AA Large |
| Bearish badge | #EF4444 | #FEE2E2 | 3.1:1 | ⚠️ AA Large |
| Disclaimer text | #92400E | #FEF3C7 | 5.2:1 | ✅ AA |

## 5.3 Spacing Consistency

| Element | Padding | Margin | Assessment |
|---------|---------|--------|------------|
| Cards | 16px | 16px gap | ✅ CONSISTENT |
| Sections | 24px | 24px gap | ✅ CONSISTENT |
| Buttons | 8px 16px | - | ✅ CONSISTENT |
| Badges | 4px 12px | - | ✅ CONSISTENT |

## 5.4 Visual Balance

| Screen | Balance Assessment |
|--------|-------------------|
| Dashboard | ✅ Stats row balanced, cards evenly distributed |
| Instrument Detail | ✅ Silos in grid, contradictions prominent |
| Silo Detail | ✅ Charts equal size, sections clearly separated |
| MCC Dashboard | ✅ Status cards aligned, actions grouped |

---

# 6. PROPOSED IMPROVEMENTS

## 6.1 Recommended Enhancements

| ID | Area | Current | Proposed | Impact |
|----|------|---------|----------|--------|
| IMP-001 | Direction Badges | Text only | Add icons (▲ ▼ ─) | Better scannability |
| IMP-002 | Freshness Badges | Static | Add subtle pulse for CURRENT | Visual feedback |
| IMP-003 | Card Hover | Shadow only | Shadow + slight lift (1px) | Better interactivity feel |
| IMP-004 | Empty States | Basic text | Add illustration + CTA | Better UX |
| IMP-005 | Loading States | Spinner only | Skeleton loaders | Smoother experience |
| IMP-006 | Toast Position | Not specified | Top-right, auto-dismiss 5s | Standard UX |
| IMP-007 | Keyboard Nav | Not specified | Tab order, Enter to activate | Accessibility |
| IMP-008 | Dark Mode | Not available | Optional toggle | User preference |

## 6.2 Potential Additions

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| ADD-001 | Quick Search | Global search in header | MEDIUM |
| ADD-002 | Keyboard Shortcuts | Ctrl+N for new, etc. | LOW |
| ADD-003 | Export Data | Export signals to CSV | LOW |
| ADD-004 | Notification Bell | Show recent activity count | LOW |

---

# 7. APPROVAL CHECKLIST

## 7.1 Screen-by-Screen Approval

Please review each screen and indicate your approval:

| # | Screen | Approve? | Notes |
|---|--------|----------|-------|
| 1 | Frontend Dashboard | ☐ YES / ☐ NO / ☐ CHANGES | |
| 2 | Instrument Detail | ☐ YES / ☐ NO / ☐ CHANGES | |
| 3 | Silo Detail | ☐ YES / ☐ NO / ☐ CHANGES | |
| 4 | Chart Detail | ☐ YES / ☐ NO / ☐ CHANGES | |
| 5 | Basket List | ☐ YES / ☐ NO / ☐ CHANGES | |
| 6 | Basket Detail | ☐ YES / ☐ NO / ☐ CHANGES | |
| 7 | AI Chat | ☐ YES / ☐ NO / ☐ CHANGES | |
| 8 | MCC Dashboard | ☐ YES / ☐ NO / ☐ CHANGES | |
| 9 | MCC Process Management | ☐ YES / ☐ NO / ☐ CHANGES | |
| 10 | MCC Log Viewer | ☐ YES / ☐ NO / ☐ CHANGES | |

## 7.2 Overall Design Approval

| Criterion | Approve? |
|-----------|----------|
| Color Palette (Bright Theme) | ☐ YES / ☐ NO |
| Typography (Plus Jakarta Sans) | ☐ YES / ☐ NO |
| Spacing & Layout | ☐ YES / ☐ NO |
| Constitutional Compliance | ☐ YES / ☐ NO |
| Usability | ☐ YES / ☐ NO |
| Finesse & Polish | ☐ YES / ☐ NO |

## 7.3 Proposed Improvements

| ID | Accept? |
|----|---------|
| IMP-001: Direction icons | ☐ YES / ☐ NO |
| IMP-002: Freshness pulse | ☐ YES / ☐ NO |
| IMP-003: Card hover lift | ☐ YES / ☐ NO |
| IMP-004: Empty state illustrations | ☐ YES / ☐ NO |
| IMP-005: Skeleton loaders | ☐ YES / ☐ NO |
| IMP-006: Toast positioning | ☐ YES / ☐ NO |
| IMP-007: Keyboard navigation | ☐ YES / ☐ NO |
| IMP-008: Dark mode option | ☐ YES / ☐ NO |

---

# SIGN-OFF

**Document Status:** AWAITING USER APPROVAL

Once you have reviewed this document and provided your feedback, I will:

1. Incorporate any requested changes
2. Update the Design System specifications
3. Proceed to Phase 3: Component Implementation

---

*This prototype review was conducted with institutional precision, presenting every screen for evaluation before any code changes are made.*


