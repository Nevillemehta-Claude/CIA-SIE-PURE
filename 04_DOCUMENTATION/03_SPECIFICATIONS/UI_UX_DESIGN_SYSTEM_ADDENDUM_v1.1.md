# UI/UX Design System Addendum v1.1

## Gap Resolution & Full Integration Specifications

**Document ID:** SPEC-UIUX-001-A  
**Version:** 1.1.0  
**Date:** January 5, 2026  
**Status:** AUTHORITATIVE  
**Purpose:** Resolve all gaps identified in Design Validation Report v1.0

---

# TABLE OF CONTENTS

1. [Gap Resolution Summary](#1-gap-resolution-summary)
2. [Basket List Screen](#2-basket-list-screen)
3. [Basket Detail Screen](#3-basket-detail-screen)
4. [Icon Library Specification (Lucide)](#4-icon-library-specification-lucide)
5. [Breadcrumb Component Specification](#5-breadcrumb-component-specification)
6. [Navigation Link Specification](#6-navigation-link-specification)
7. [MCC Frontend Launcher Clarification](#7-mcc-frontend-launcher-clarification)
8. [Integration Matrix](#8-integration-matrix)
9. [Data Flow: Baskets Circuit](#9-data-flow-baskets-circuit)

---

# 1. GAP RESOLUTION SUMMARY

| Gap ID | Description | Resolution | Status |
|--------|-------------|------------|--------|
| GAP-001 | Avatar/Icon not specified | Lucide Icons library specified | ✅ RESOLVED |
| GAP-002 | Breadcrumb not specified | Full specification added | ✅ RESOLVED |
| GAP-003 | Navigation Link not specified | Full specification added | ✅ RESOLVED |
| GAP-004 | Basket List wireframe missing | Full wireframe added | ✅ RESOLVED |
| GAP-005 | Basket Detail wireframe missing | Full wireframe added | ✅ RESOLVED |
| GAP-006 | MCC Frontend Launcher unclear | Clarified as button, not screen | ✅ RESOLVED |

---

# 2. BASKET LIST SCREEN

## 2.1 Screen Purpose

Baskets are **UI-layer organizational constructs** that allow users to group charts for comparative analysis. 

**CONSTITUTIONAL COMPLIANCE:**
- Baskets have NO effect on signal processing (CR-001)
- Creating/modifying baskets has ZERO impact on signals
- Charts can belong to multiple baskets
- Baskets are purely for user convenience

## 2.2 Wireframe

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                               ║
║   BASKET LIST SCREEN - BRIGHT THEME                                                                           ║
║   ═════════════════════════════════                                                                           ║
║                                                                                                               ║
║   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ◉ CIA-SIE                        Dashboard  |  Instruments  |  Baskets  |  AI Chat           │ │   ║
║   │   │                                                                              ^^^^^^^^           │ │   ║
║   │   │   Active nav: Teal underline                                                 (active)           │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ⚠️ DISCLAIMER: Baskets are organizational tools only. They do NOT affect signal processing   │ │   ║
║   │   │   or analysis. All trading decisions remain solely with you.                                    │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Background: #FEF3C7, Border-left: 4px #FBBF24                                                  │ │   ║
║   │   │   CANNOT BE DISMISSED (CR-003)                                                                  │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ANALYTICAL BASKETS                                                        + Create Basket     │ │   ║
║   │   │   ══════════════════                                                                            │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Group charts for comparative analysis                                     🔍 Search...        │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Title: 24px Semibold                                                                          │ │   ║
║   │   │   Description: 14px Muted                                                                       │ │   ║
║   │   │   Button: Primary teal                                                                          │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   FILTER BY TYPE                                                                                │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │ │   ║
║   │   │   │     All      │ │   Logical    │ │ Hierarchical │ │  Contextual  │ │    Custom    │          │ │   ║
║   │   │   │   (active)   │ │              │ │              │ │              │ │              │          │ │   ║
║   │   │   └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘          │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Filter pills: Active = Teal background, Inactive = Gray outline                               │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   BASKETS GRID (3 columns on desktop, 2 on tablet, 1 on mobile)                                 │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────────────┐│ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   │  📁  NIFTY Momentum         │ │  📁  Bank Nifty Timeframes  │ │  📁  Cross-Index Compare    ││ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   │  ┌─────────────────────┐    │ │  ┌─────────────────────┐    │ │  ┌─────────────────────┐    ││ │   ║
║   │   │   │  │  LOGICAL            │    │ │  │  HIERARCHICAL       │    │ │  │  CONTEXTUAL         │    ││ │   ║
║   │   │   │  └─────────────────────┘    │ │  └─────────────────────┘    │ │  └─────────────────────┘    ││ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   │  Charts comparing           │ │  Organized by timeframe     │ │  Cross-instrument           ││ │   ║
║   │   │   │  momentum indicators        │ │  hierarchy                  │ │  comparison basket          ││ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   │  ─────────────────────────  │ │  ─────────────────────────  │ │  ─────────────────────────  ││ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   │  📊 4 charts                │ │  📊 6 charts                │ │  📊 8 charts                ││ │   ║
║   │   │   │  🏷️ NIFTY 50                │ │  🏷️ Bank Nifty              │ │  🏷️ Multiple                ││ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   │  View Basket →              │ │  View Basket →              │ │  View Basket →              ││ │   ║
║   │   │   │                             │ │                             │ │                             ││ │   ║
║   │   │   └─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────────────┘│ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Card styling:                                                                                 │ │   ║
║   │   │   - Background: #FFFFFF                                                                         │ │   ║
║   │   │   - Border: 1px #E5E7EB                                                                         │ │   ║
║   │   │   - Border-radius: 12px                                                                         │ │   ║
║   │   │   - Hover: Shadow increases, cursor pointer                                                     │ │   ║
║   │   │   - Icon: Lucide FolderKanban, Violet (#8B5CF6)                                                  │ │   ║
║   │   │   - Type badge: Colored per type                                                                │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   EMPTY STATE (when no baskets exist)                                                           │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │                              📁                                                                  │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │                       No Baskets Yet                                                            │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │           Create a basket to group charts for comparative analysis.                             │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │                      ┌────────────────────────┐                                                  │ │   ║
║   │   │                      │    + Create Basket     │                                                  │ │   ║
║   │   │                      └────────────────────────┘                                                  │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Icon: 64px, Muted gray                                                                        │ │   ║
║   │   │   Title: 20px Semibold                                                                          │ │   ║
║   │   │   Description: 14px Muted                                                                       │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 2.3 Basket Type Color Coding

| Type | Badge Background | Badge Text | Badge Border |
|------|------------------|------------|--------------|
| LOGICAL | #DBEAFE (Blue-100) | #1E40AF (Blue-800) | #3B82F6 |
| HIERARCHICAL | #E0E7FF (Indigo-100) | #3730A3 (Indigo-800) | #6366F1 |
| CONTEXTUAL | #FCE7F3 (Pink-100) | #9D174D (Pink-800) | #EC4899 |
| CUSTOM | #F3E8FF (Purple-100) | #6B21A8 (Purple-800) | #A855F7 |

## 2.4 Data Integration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   BASKET LIST DATA FLOW                                                     │
│   ═════════════════════                                                     │
│                                                                             │
│   Frontend Component                                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  BasketsPage.tsx                                                    │   │
│   │                                                                     │   │
│   │  Uses: useBaskets() hook                                            │   │
│   │                                                                     │   │
│   └───────────────────────────────────┬─────────────────────────────────┘   │
│                                       │                                     │
│                                       ▼                                     │
│   React Query Hook                                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  useBaskets.ts                                                      │   │
│   │                                                                     │   │
│   │  queryKey: ['baskets', 'list']                                      │   │
│   │  queryFn: getBaskets()                                              │   │
│   │                                                                     │   │
│   └───────────────────────────────────┬─────────────────────────────────┘   │
│                                       │                                     │
│                                       ▼                                     │
│   API Service                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  services/baskets.ts                                                │   │
│   │                                                                     │   │
│   │  GET /api/v1/baskets/                                               │   │
│   │  Returns: AnalyticalBasket[]                                        │   │
│   │                                                                     │   │
│   └───────────────────────────────────┬─────────────────────────────────┘   │
│                                       │                                     │
│                                       ▼                                     │
│   Backend API Route                                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  routes/baskets.py - list_baskets()                                 │   │
│   │                                                                     │   │
│   │  Calls: BasketRepository.get_all()                                  │   │
│   │  Returns: list[AnalyticalBasket]                                    │   │
│   │                                                                     │   │
│   └───────────────────────────────────┬─────────────────────────────────┘   │
│                                       │                                     │
│                                       ▼                                     │
│   Database                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  AnalyticalBasketDB                                                 │   │
│   │                                                                     │   │
│   │  Fields: basket_id, basket_name, basket_type, description,          │   │
│   │          instrument_id, chart_ids, created_at, updated_at, is_active│   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. BASKET DETAIL SCREEN

## 3.1 Screen Purpose

View and manage a single basket, including:
- Basket metadata (name, type, description)
- List of charts in the basket
- Add/remove charts
- View signal status of included charts
- Delete basket

## 3.2 Wireframe

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                               ║
║   BASKET DETAIL SCREEN - BRIGHT THEME                                                                         ║
║   ═══════════════════════════════════                                                                         ║
║                                                                                                               ║
║   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                                                       │   ║
║   │   ← Back to Baskets                                                                                   │   ║
║   │                                                                                                       │   ║
║   │   Breadcrumb: Baskets > NIFTY Momentum                                                                │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   📁 NIFTY Momentum                                                ✏️ Edit    🗑️ Delete         │ │   ║
║   │   │   ═════════════════                                                                             │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ┌─────────────────────┐                                                                       │ │   ║
║   │   │   │      LOGICAL        │     Charts comparing momentum indicators across timeframes            │ │   ║
║   │   │   └─────────────────────┘                                                                       │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Instrument: NIFTY 50                    Created: Jan 1, 2026                                  │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Icon: 48px Lucide FolderKanban, Violet                                                        │ │   ║
║   │   │   Name: 28px Semibold                                                                           │ │   ║
║   │   │   Type badge: Colored per type                                                                  │ │   ║
║   │   │   Description: 14px Regular                                                                     │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ⚠️ DISCLAIMER: Baskets are organizational tools only. They do NOT affect signal processing.  │ │   ║
║   │   │   All trading decisions remain solely with you.                                                 │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   CHARTS IN THIS BASKET                                                   + Add Chart         │   │   ║
║   │   │   ═════════════════════                                                                       │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   4 charts                                                                                    │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────┐ │   │   ║
║   │   │   │                     │ │                     │ │                     │ │                 │ │   │   ║
║   │   │   │   NIFTY_01A         │ │   NIFTY_01B         │ │   NIFTY_02A         │ │   NIFTY_02B     │ │   │   ║
║   │   │   │   5min              │ │   15min             │ │   5min              │ │   15min         │ │   │   ║
║   │   │   │                     │ │                     │ │                     │ │                 │ │   │   ║
║   │   │   │   ▲ BULLISH         │ │   ▼ BEARISH         │ │   ▲ BULLISH         │ │   ─ NEUTRAL     │ │   │   ║
║   │   │   │                     │ │                     │ │                     │ │                 │ │   │   ║
║   │   │   │   ● CURRENT         │ │   ● CURRENT         │ │   ● RECENT          │ │   ● STALE       │ │   │   ║
║   │   │   │                     │ │                     │ │                     │ │                 │ │   │   ║
║   │   │   │   ✕ Remove          │ │   ✕ Remove          │ │   ✕ Remove          │ │   ✕ Remove      │ │   │   ║
║   │   │   │                     │ │                     │ │                     │ │                 │ │   │   ║
║   │   │   └─────────────────────┘ └─────────────────────┘ └─────────────────────┘ └─────────────────┘ │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   Chart cards: Same as Silo Detail, but with "Remove" button                                  │   │   ║
║   │   │   All charts have EQUAL SIZE (CR-002)                                                         │   │   ║
║   │   │   Remove button: Ghost style, red icon                                                        │   │   ║
║   │   │                                                                                               │   │   ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │   ║
║   │                                                                                                       │   ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   SIGNAL COMPARISON                                                                           │   │   ║
║   │   │   ═════════════════                                                                           │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────┐ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   │   DIRECTION SUMMARY                                                                     │ │   │   ║
║   │   │   │   ─────────────────                                                                     │ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   │   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐               │ │   │   ║
║   │   │   │   │                    │  │                    │  │                    │               │ │   │   ║
║   │   │   │   │   ▲ BULLISH        │  │   ▼ BEARISH        │  │   ─ NEUTRAL        │               │ │   │   ║
║   │   │   │   │                    │  │                    │  │                    │               │ │   │   ║
║   │   │   │   │   2 charts         │  │   1 chart          │  │   1 chart          │               │ │   │   ║
║   │   │   │   │                    │  │                    │  │                    │               │ │   │   ║
║   │   │   │   └────────────────────┘  └────────────────────┘  └────────────────────┘               │ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   │   NOTE: This is a COUNT, not an aggregation. No "overall" direction is implied.        │ │   │   ║
║   │   │   │   Equal visual weight for all direction boxes (CR-002)                                  │ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────────────────┘ │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   CONTRADICTIONS IN BASKET                                                                    │   │   ║
║   │   │   ════════════════════════                                                                    │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   1 contradiction detected among basket charts                                                │   │   ║
║   │   │                                                                                               │   │   ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────┐ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   │   ┌─────────────────────┐        ⚡        ┌─────────────────────┐                      │ │   │   ║
║   │   │   │   │                     │    CONFLICTS     │                     │                      │ │   │   ║
║   │   │   │   │   NIFTY_01A         │       WITH       │   NIFTY_01B         │                      │ │   │   ║
║   │   │   │   │   5min              │                  │   15min             │                      │ │   │   ║
║   │   │   │   │                     │                  │                     │                      │ │   │   ║
║   │   │   │   │   ▲ BULLISH         │                  │   ▼ BEARISH         │                      │ │   │   ║
║   │   │   │   │                     │                  │                     │                      │ │   │   ║
║   │   │   │   └─────────────────────┘                  └─────────────────────┘                      │ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   │   EQUAL VISUAL WEIGHT (CR-002)                                                          │ │   │   ║
║   │   │   │                                                                                         │ │   │   ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────────────────┘ │   │   ║
║   │   │                                                                                               │   │   ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │   ║
║   │                                                                                                       │   ║
║   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 3.3 Add Chart Modal (Basket-Specific)

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                               ║
║   ADD CHART TO BASKET MODAL                                                                                   ║
║   ═════════════════════════                                                                                   ║
║                                                                                                               ║
║   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Add Chart to Basket                                                                       ✕   │ │   ║
║   │   │   ═══════════════════                                                                           │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Select Instrument                                                                             │ │   ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │ │   ║
║   │   │   │  NIFTY 50                                                                          ▼   │   │ │   ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────────────────┘   │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Select Chart                                                                                  │ │   ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │ │   ║
║   │   │   │                                                                                         │   │ │   ║
║   │   │   │   ☐ NIFTY_01A (5min) - Already in basket                                                │   │ │   ║
║   │   │   │   ☐ NIFTY_01B (15min) - Already in basket                                               │   │ │   ║
║   │   │   │   ☑ NIFTY_01C (1hour) - Available                                                       │   │ │   ║
║   │   │   │   ☐ NIFTY_01D (4hour) - Available                                                       │   │ │   ║
║   │   │   │                                                                                         │   │ │   ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────────────────┘   │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   Already in basket: Grayed out, disabled                                                       │ │   ║
║   │   │   Available: Checkbox enabled                                                                   │ │   ║
║   │   │   Charts can belong to MULTIPLE baskets                                                         │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                                                                                 │ │   ║
║   │   │   ⚠️ Adding charts to a basket has NO effect on signal processing.                              │ │   ║
║   │   │                                                                                                 │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │   ║
║   │   │                                           ┌────────────────┐  ┌────────────────┐                │ │   ║
║   │   │                                           │    Cancel      │  │   Add Charts   │                │ │   ║
║   │   │                                           └────────────────┘  └────────────────┘                │ │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │   ║
║   │                                                                                                       │   ║
║   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 4. ICON LIBRARY SPECIFICATION (LUCIDE)

## 4.1 Library Selection

**Library:** Lucide Icons  
**Version:** Latest stable  
**License:** MIT (permissive, commercial use allowed)  
**Package:** `lucide-react`

### Why Lucide?
- Tree-shakeable (only imports used icons)
- Consistent 24px grid
- 1000+ icons
- Active maintenance
- TypeScript support
- React-native compatible (future-proofing)

## 4.2 Installation

```bash
npm install lucide-react
```

## 4.3 Icon Mapping

### Navigation Icons

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Dashboard | `LayoutDashboard` | Sidebar navigation |
| Instruments | `LineChart` | Sidebar navigation |
| Baskets | `FolderKanban` | Sidebar navigation |
| AI Chat | `MessageSquare` | Sidebar navigation |
| Settings | `Settings` | Sidebar navigation |
| Processes | `Activity` | MCC sidebar |
| Logs | `ScrollText` | MCC sidebar |

### Action Icons

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Add/Create | `Plus` | Add buttons |
| Edit | `Pencil` | Edit buttons |
| Delete | `Trash2` | Delete buttons |
| Close | `X` | Modal close, toast dismiss |
| Back | `ArrowLeft` | Back navigation |
| View/Open | `ExternalLink` | Open in new tab |
| Refresh | `RefreshCw` | Refresh data |
| Search | `Search` | Search inputs |
| Filter | `Filter` | Filter dropdowns |

### Status Icons

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Success | `CheckCircle` | Success states |
| Error | `XCircle` | Error states |
| Warning | `AlertTriangle` | Warning states |
| Info | `Info` | Info states |
| Loading | `Loader2` | Loading spinner (animate-spin) |

### Direction Icons

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Bullish | `TrendingUp` | Direction badge (or custom ▲) |
| Bearish | `TrendingDown` | Direction badge (or custom ▼) |
| Neutral | `Minus` | Direction badge (or custom ─) |

### Entity Icons

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Instrument | `LineChart` | Instrument cards |
| Silo | `Layers` | Silo cards |
| Chart | `BarChart3` | Chart cards |
| Signal | `Zap` | Signal indicators |
| Basket | `FolderKanban` | Basket cards |
| Contradiction | `Zap` | Contradiction separator |
| Confirmation | `Check` | Confirmation separator |

### Process Icons (MCC)

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Start | `Play` | Start process |
| Stop | `Square` | Stop process |
| Restart | `RotateCcw` | Restart process |
| Emergency Stop | `OctagonX` | Emergency stop |
| Backend | `Server` | Backend status |
| Frontend | `Monitor` | Frontend status |
| Database | `Database` | Database status |

## 4.4 Icon Sizing Standards

| Context | Size | Class |
|---------|------|-------|
| Inline text | 16px | `h-4 w-4` |
| Button icon | 16px | `h-4 w-4` |
| Card icon | 20px | `h-5 w-5` |
| Section header | 24px | `h-6 w-6` |
| Empty state | 48px | `h-12 w-12` |
| Large display | 64px | `h-16 w-16` |

## 4.5 Icon Color Standards

| Context | Color | CSS Variable |
|---------|-------|--------------|
| Default | Gray-500 | `text-gray-500` |
| Primary action | Teal-500 | `text-teal-500` |
| Success | Emerald-500 | `text-emerald-500` |
| Warning | Amber-500 | `text-amber-500` |
| Error | Red-500 | `text-red-500` |
| Muted | Gray-400 | `text-gray-400` |

---

# 5. BREADCRUMB COMPONENT SPECIFICATION

## 5.1 Visual Specification

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   BREADCRUMB COMPONENT                                                        ║
║   ════════════════════                                                        ║
║                                                                               ║
║   STRUCTURE                                                                   ║
║   ─────────                                                                   ║
║                                                                               ║
║   Home  /  Instruments  /  NIFTY 50  /  Silo 01                              ║
║   ^^^^     ^^^^^^^^^^^     ^^^^^^^^     ^^^^^^^                               ║
║   Link     Link            Link         Current (not link)                    ║
║                                                                               ║
║   STYLING                                                                     ║
║   ───────                                                                     ║
║                                                                               ║
║   Container:                                                                  ║
║   - Display: flex                                                             ║
║   - Align-items: center                                                       ║
║   - Gap: 8px                                                                  ║
║   - Font-size: 14px                                                           ║
║                                                                               ║
║   Links:                                                                      ║
║   - Color: #6B7280 (Gray-500)                                                 ║
║   - Hover: #0D9488 (Teal-500)                                                 ║
║   - Text-decoration: none                                                     ║
║   - Cursor: pointer                                                           ║
║                                                                               ║
║   Separator:                                                                  ║
║   - Icon: ChevronRight from Lucide (or "/" character)                         ║
║   - Color: #D1D5DB (Gray-300)                                                 ║
║   - Size: 16px                                                                ║
║                                                                               ║
║   Current (last item):                                                        ║
║   - Color: #111827 (Gray-900)                                                 ║
║   - Font-weight: 500 (Medium)                                                 ║
║   - Cursor: default                                                           ║
║   - Not clickable                                                             ║
║                                                                               ║
║   ACCESSIBILITY                                                               ║
║   ─────────────                                                               ║
║                                                                               ║
║   - Use <nav aria-label="Breadcrumb">                                         ║
║   - Use <ol> for ordered list                                                 ║
║   - Current item: aria-current="page"                                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 5.2 React Component Interface

```typescript
interface BreadcrumbItem {
  label: string
  href?: string  // If undefined, treated as current page
}

interface BreadcrumbProps {
  items: BreadcrumbItem[]
  separator?: 'chevron' | 'slash'  // Default: 'chevron'
}
```

---

# 6. NAVIGATION LINK SPECIFICATION

## 6.1 Visual Specification

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   NAVIGATION LINK COMPONENT                                                   ║
║   ═════════════════════════                                                   ║
║                                                                               ║
║   STATES                                                                      ║
║   ──────                                                                      ║
║                                                                               ║
║   DEFAULT                                                                     ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │  📊  Dashboard                                                          │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║   - Background: transparent                                                   ║
║   - Text: #4B5563 (Gray-600)                                                  ║
║   - Icon: #6B7280 (Gray-500)                                                  ║
║   - Padding: 12px 16px                                                        ║
║   - Border-radius: 8px                                                        ║
║                                                                               ║
║   HOVER                                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │  📊  Dashboard                                                          │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║   - Background: #F4F5F7 (Cloud)                                               ║
║   - Text: #111827 (Gray-900)                                                  ║
║   - Icon: #0D9488 (Teal-500)                                                  ║
║   - Transition: 150ms ease                                                    ║
║                                                                               ║
║   ACTIVE (Current Page)                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │▌ 📊  Dashboard                                                          │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║   - Background: #FFFFFF (White)                                               ║
║   - Text: #0D9488 (Teal-500)                                                  ║
║   - Icon: #0D9488 (Teal-500)                                                  ║
║   - Left border: 3px solid #0D9488                                            ║
║   - Font-weight: 500 (Medium)                                                 ║
║                                                                               ║
║   STRUCTURE                                                                   ║
║   ─────────                                                                   ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │  [Icon 20px]  [Gap 12px]  [Label 14px]                                  │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 6.2 React Component Interface

```typescript
interface NavLinkProps {
  href: string
  icon: LucideIcon
  label: string
  isActive?: boolean
  onClick?: () => void
}
```

---

# 7. MCC FRONTEND LAUNCHER CLARIFICATION

## 7.1 Resolution

The "MCC Frontend Launcher" is **NOT a separate screen**. It is a **button** on the MCC Dashboard that opens the frontend application in the user's default browser.

## 7.2 Implementation

```
Location: MCC Dashboard → Quick Actions section

Button: "Open Frontend"
Icon: Lucide ExternalLink
Action: window.electron.openExternal(`http://localhost:${frontendPort}`)

Constitutional Compliance:
- MCR-002: Only opens localhost URLs
- MCR-004: Requires explicit user click
```

## 7.3 Updated Screen Count

| Category | Count | Screens |
|----------|-------|---------|
| MCC Screens | 4 | Dashboard, Process Management, Log Viewer, Settings |
| Frontend Screens | 8 | Dashboard, Instrument Detail, Silo Detail, Chart Detail, Basket List, Basket Detail, AI Chat, AI Settings |
| **Total** | **12** | (Not 13 - Frontend Launcher was miscounted) |

---

# 8. INTEGRATION MATRIX

## 8.1 Basket Integration Points

| Layer | Component | Integration | Status |
|-------|-----------|-------------|--------|
| **Backend API** | `routes/baskets.py` | CRUD endpoints | ✅ EXISTS |
| **Backend Model** | `models.py:AnalyticalBasket` | Domain model | ✅ EXISTS |
| **Backend DB** | `dal/models.py:AnalyticalBasketDB` | Database model | ✅ EXISTS |
| **Backend Repo** | `repositories.py:BasketRepository` | Data access | ✅ EXISTS |
| **Frontend Service** | `services/baskets.ts` | API client | ✅ EXISTS |
| **Frontend Hook** | `hooks/useBaskets.ts` | React Query | ✅ EXISTS |
| **Frontend Page** | `pages/BasketsPage.tsx` | List view | ✅ EXISTS (needs update) |
| **Frontend Page** | `pages/BasketDetailPage.tsx` | Detail view | ❌ NEEDS CREATION |
| **Frontend Types** | `types/models.ts` | TypeScript types | ⚠️ NEEDS UPDATE |
| **Frontend Route** | `App.tsx` | Route definition | ✅ EXISTS |
| **UI Design** | Design System | Wireframes | ✅ ADDED (this document) |

## 8.2 Icon Integration Points

| Layer | Component | Integration | Status |
|-------|-----------|-------------|--------|
| **Package** | `package.json` | `lucide-react` dependency | ⚠️ VERIFY |
| **Usage** | All components | Import from `lucide-react` | ✅ ALREADY USED |
| **Standardization** | Design System | Icon mapping | ✅ ADDED (this document) |

---

# 9. DATA FLOW: BASKETS CIRCUIT

## 9.1 Circuit Diagram

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                               ║
║   CIRCUIT 6: BASKETS DATA FLOW                                                                                ║
║   ════════════════════════════                                                                                ║
║                                                                                                               ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                         │ ║
║   │   USER INTERACTION                                                                                      │ ║
║   │   ════════════════                                                                                      │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                         │ ║
║   │   │ View Baskets │───▶│Create Basket │───▶│ Add Chart    │───▶│Remove Chart  │                         │ ║
║   │   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘                         │ ║
║   │          │                   │                   │                   │                                  │ ║
║   │          ▼                   ▼                   ▼                   ▼                                  │ ║
║   │                                                                                                         │ ║
║   │   FRONTEND COMPONENTS                                                                                   │ ║
║   │   ═══════════════════                                                                                   │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                         │ ║
║   │   │ BasketsPage  │    │CreateBasket  │    │AddChartModal │    │BasketDetail  │                         │ ║
║   │   │              │    │   Modal      │    │              │    │   Page       │                         │ ║
║   │   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘                         │ ║
║   │          │                   │                   │                   │                                  │ ║
║   │          ▼                   ▼                   ▼                   ▼                                  │ ║
║   │                                                                                                         │ ║
║   │   REACT QUERY HOOKS                                                                                     │ ║
║   │   ═════════════════                                                                                     │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                         │ ║
║   │   │ useBaskets() │    │useCreateBask │    │useAddChart   │    │useRemoveChart│                         │ ║
║   │   │              │    │   et()       │    │  ToBasket()  │    │  FromBasket()│                         │ ║
║   │   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘                         │ ║
║   │          │                   │                   │                   │                                  │ ║
║   │          ▼                   ▼                   ▼                   ▼                                  │ ║
║   │                                                                                                         │ ║
║   │   API SERVICE                                                                                           │ ║
║   │   ═══════════                                                                                           │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                         │ ║
║   │   │GET /baskets/ │    │POST /baskets/│    │POST /baskets │    │DELETE /basket│                         │ ║
║   │   │              │    │              │    │/{id}/charts/ │    │s/{id}/charts/│                         │ ║
║   │   │              │    │              │    │{chart_id}    │    │{chart_id}    │                         │ ║
║   │   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘                         │ ║
║   │          │                   │                   │                   │                                  │ ║
║   │          ▼                   ▼                   ▼                   ▼                                  │ ║
║   │                                                                                                         │ ║
║   │   BACKEND API ROUTES                                                                                    │ ║
║   │   ══════════════════                                                                                    │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                         │ ║
║   │   │list_baskets()│    │create_basket │    │add_chart_to  │    │remove_chart  │                         │ ║
║   │   │              │    │   ()         │    │  _basket()   │    │  _from_basket│                         │ ║
║   │   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘                         │ ║
║   │          │                   │                   │                   │                                  │ ║
║   │          ▼                   ▼                   ▼                   ▼                                  │ ║
║   │                                                                                                         │ ║
║   │   REPOSITORY LAYER                                                                                      │ ║
║   │   ════════════════                                                                                      │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ║
║   │   │                                                                                                  │ │ ║
║   │   │   BasketRepository                                                                               │ │ ║
║   │   │   ────────────────                                                                               │ │ ║
║   │   │   • get_all()                                                                                    │ │ ║
║   │   │   • get_by_instrument()                                                                          │ │ ║
║   │   │   • get_with_charts()                                                                            │ │ ║
║   │   │   • create()                                                                                     │ │ ║
║   │   │   • add_chart_to_basket()                                                                        │ │ ║
║   │   │   • remove_chart_from_basket()                                                                   │ │ ║
║   │   │   • delete()                                                                                     │ │ ║
║   │   │                                                                                                  │ │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ║
║   │          │                                                                                              │ ║
║   │          ▼                                                                                              │ ║
║   │                                                                                                         │ ║
║   │   DATABASE                                                                                              │ ║
║   │   ════════                                                                                              │ ║
║   │                                                                                                         │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ║
║   │   │                                                                                                  │ │ ║
║   │   │   AnalyticalBasketDB                          BasketChartDB (junction table)                     │ │ ║
║   │   │   ──────────────────                          ──────────────────────────────                     │ │ ║
║   │   │   • basket_id (PK)                            • basket_id (FK)                                   │ │ ║
║   │   │   • basket_name                               • chart_id (FK)                                    │ │ ║
║   │   │   • basket_type                               • added_at                                         │ │ ║
║   │   │   • description                                                                                  │ │ ║
║   │   │   • instrument_id (FK, nullable)                                                                 │ │ ║
║   │   │   • created_at                                                                                   │ │ ║
║   │   │   • updated_at                                                                                   │ │ ║
║   │   │   • is_active                                                                                    │ │ ║
║   │   │                                                                                                  │ │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ║
║   │                                                                                                         │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                                                                               ║
║   CONSTITUTIONAL COMPLIANCE                                                                                   ║
║   ═════════════════════════                                                                                   ║
║                                                                                                               ║
║   ✅ Baskets have NO effect on signal processing                                                              ║
║   ✅ Creating/modifying baskets has ZERO impact on signals                                                    ║
║   ✅ Charts can belong to multiple baskets                                                                    ║
║   ✅ Baskets are purely UI-layer organizational constructs                                                    ║
║   ✅ No aggregation, scoring, or weighting of basket contents                                                 ║
║   ✅ Equal visual weight for all charts in basket (CR-002)                                                    ║
║   ✅ Disclaimer present on all basket screens (CR-003)                                                        ║
║                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# APPENDIX: UPDATED COMPONENT INVENTORY

## Complete List (Updated)

### Atomic Components (15) - UNCHANGED
1. Button (Primary, Secondary, Danger, Ghost, Emergency)
2. Direction Badge (Bullish, Bearish, Neutral)
3. Freshness Badge (Current, Recent, Stale, Unavailable)
4. Status Indicator (Running, Starting, Stopped, Error)
5. Input Field (Text, Number, Textarea)
6. Select/Dropdown
7. Toggle/Switch
8. Card (Base, Instrument, Silo, Chart Mini, **Basket**)
9. Toast (Success, Error, Warning, Info)
10. Modal (Base container)
11. Skeleton Loader
12. Progress Bar
13. **Breadcrumb** ← ADDED SPECIFICATION
14. **Navigation Link** ← ADDED SPECIFICATION
15. **Icon (Lucide)** ← ADDED SPECIFICATION

### MCC Screens (4) - CORRECTED
1. MCC Dashboard
2. MCC Process Management
3. MCC Log Viewer
4. MCC Settings

### Frontend Screens (8) - UPDATED
1. Main Dashboard
2. Instrument Detail
3. Silo Detail
4. Chart Detail
5. **Basket List** ← ADDED WIREFRAME
6. **Basket Detail** ← ADDED WIREFRAME
7. AI Chat
8. AI Settings

### Modals (7) - UPDATED
1. Add Instrument
2. Add Silo
3. Add Chart
4. **Add Chart to Basket** ← ADDED
5. Edit (generic for all entities)
6. Delete Confirmation
7. AI Budget Settings

### Composite Components (9) - UPDATED
1. Contradiction Card
2. Confirmation Card
3. Signal History Table
4. AI Chat Message (User)
5. AI Chat Message (AI)
6. Narrative Display
7. Process Status Card
8. Log Entry Row
9. **Basket Card** ← ADDED

---

**END OF ADDENDUM**

**Document Statistics:**
- Gaps Resolved: 6/6 (100%)
- New Wireframes Added: 2 (Basket List, Basket Detail)
- New Component Specs: 3 (Breadcrumb, Navigation Link, Icon Library)
- Integration Points Verified: 11
- Constitutional Compliance: 100%


