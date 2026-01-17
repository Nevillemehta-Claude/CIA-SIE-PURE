# FRONTEND REPLACEMENT IMPLEMENTATION PLAN
## Institutional Approach to UI/UX Transformation

**Document Version:** 1.0  
**Date:** January 5, 2026  
**Status:** APPROVED FOR EXECUTION  

---

## PART A: BACKUP CONFIRMATION ✅

| Item | Status | Location |
|------|--------|----------|
| Full Project Backup | ✅ COMPLETE | `/Users/nevillemehta/Downloads/CIA-SIE-PURE_BACKUP_2026-01-05` |
| Backup Size | 671 MB | Complete copy including node_modules |
| Backup Date | January 5, 2026 | 5:34 PM |

**Recovery Command (if needed):**
```bash
rm -rf /Users/nevillemehta/Downloads/CIA-SIE-PURE
mv /Users/nevillemehta/Downloads/CIA-SIE-PURE_BACKUP_2026-01-05 /Users/nevillemehta/Downloads/CIA-SIE-PURE
```

---

## PART B: ENGINEERING ALREADY COMPLETED

### What Has Been Done (Design System Foundation)

| Component | Status | File Modified |
|-----------|--------|---------------|
| **Color Tokens (Frontend)** | ✅ Implemented | `frontend/tailwind.config.js` |
| **Color Tokens (MCC)** | ✅ Implemented | `mission-control/tailwind.config.ts` |
| **CSS Variables (Frontend)** | ✅ Implemented | `frontend/src/index.css` |
| **CSS Variables (MCC)** | ✅ Implemented | `mission-control/src/styles/globals.css` |
| **Typography** | ✅ Configured | Plus Jakarta Sans + JetBrains Mono |
| **Component Classes** | ✅ Defined | `.btn`, `.card`, `.badge`, etc. |
| **Visual Prototypes** | ✅ Created | 12 HTML files in `documentation/prototypes/` |
| **Functional Specification** | ✅ Complete | `UI_FUNCTIONAL_SPECIFICATION_COMPLETE.html` |

### What Remains To Be Done

| Component | Status | Action Required |
|-----------|--------|-----------------|
| Atomic Components (React) | ⬚ Pending | Build Button, Badge, Card, Input, etc. |
| Page Components (Frontend) | ⬚ Pending | Rebuild 8 screens |
| Page Components (MCC) | ⬚ Pending | Rebuild 4 screens |
| API Integration | ⬚ Pending | Wire components to backend |
| Testing | ⬚ Pending | Validate each module |

---

## PART C: MODULAR REPLACEMENT STRATEGY

### The Institutional Approach

We will **NOT** do a "big bang" replacement. Instead, we follow a **Modular Section-by-Section** approach:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     MODULAR REPLACEMENT STRATEGY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   PHASE 1: ATOMIC COMPONENTS                                                │
│   ├── Build in isolation (no breaking changes)                              │
│   ├── Test each component independently                                     │
│   └── Validate against prototype                                            │
│                                                                              │
│   PHASE 2: LAYOUT SHELL                                                     │
│   ├── Replace AppShell/Navigation                                           │
│   ├── Keep old page content temporarily                                     │
│   └── Validate navigation works                                             │
│                                                                              │
│   PHASE 3: PAGE-BY-PAGE REPLACEMENT                                         │
│   ├── Replace one page at a time                                            │
│   ├── Test each page before moving to next                                  │
│   └── Rollback capability at each step                                      │
│                                                                              │
│   PHASE 4: INTEGRATION VERIFICATION                                         │
│   ├── End-to-end circuit testing                                            │
│   ├── Constitutional compliance verification                                │
│   └── Performance validation                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## DETAILED EXECUTION PLAN

### PHASE 1: ATOMIC COMPONENTS (Foundation Layer)

**Principle:** Build components in isolation. No existing functionality is touched.

| Step | Component | Action | Validation | Rollback |
|------|-----------|--------|------------|----------|
| 1.1 | `Button.tsx` | Create new file | Matches prototype | Delete file |
| 1.2 | `Badge.tsx` | Create new file | Matches prototype | Delete file |
| 1.3 | `Card.tsx` | Create new file | Matches prototype | Delete file |
| 1.4 | `Input.tsx` | Create new file | Matches prototype | Delete file |
| 1.5 | `StatusDot.tsx` | Create new file | Matches prototype | Delete file |
| 1.6 | `Breadcrumb.tsx` | Create new file | Matches prototype | Delete file |
| 1.7 | `Toast.tsx` | Create new file | Matches prototype | Delete file |

**Location:** `frontend/src/components/ui/` (new folder)

**Constitutional Component:**
| Step | Component | Action | Special Rules |
|------|-----------|--------|---------------|
| 1.8 | `Disclaimer.tsx` | MODIFY existing | Text is HARDCODED, non-dismissible |

**HITL Gate 1:** Review all atomic components before proceeding.

---

### PHASE 2: LAYOUT SHELL (Structural Layer)

**Principle:** Replace the outer shell while keeping page content intact.

| Step | Component | Action | Validation | Rollback |
|------|-----------|--------|------------|----------|
| 2.1 | `AppShell.tsx` | Replace | New theme visible | Restore from backup |
| 2.2 | `Sidebar.tsx` | Replace | Navigation works | Restore from backup |
| 2.3 | `Header.tsx` | Replace/Create | Breadcrumbs work | Restore from backup |

**After Phase 2:** Application looks new but pages still have old content.

**HITL Gate 2:** Confirm navigation and shell work correctly.

---

### PHASE 3: PAGE-BY-PAGE REPLACEMENT (Content Layer)

**Principle:** One page at a time. Test. Move to next.

#### Frontend Pages (8 screens)

| Step | Page | Action | Dependencies | Validation |
|------|------|--------|--------------|------------|
| 3.1 | `Dashboard.tsx` | Replace | Instrument list API | Data displays |
| 3.2 | `InstrumentDetail.tsx` | Replace | Silo list API | Data displays |
| 3.3 | `SiloDetail.tsx` | Replace | Chart list API | Data displays |
| 3.4 | `ChartDetail.tsx` | Replace | Signal API | Data displays |
| 3.5 | `BasketList.tsx` | Create NEW | Basket API | CRUD works |
| 3.6 | `BasketDetail.tsx` | Create NEW | Basket API | CRUD works |
| 3.7 | `AIChat.tsx` | Replace | Chat API | Messages flow |
| 3.8 | `AISettings.tsx` | Replace | AI config API | Settings save |

**HITL Gate 3A:** Frontend pages complete and functional.

#### MCC Pages (4 screens)

| Step | Page | Action | Dependencies | Validation |
|------|------|--------|--------------|------------|
| 3.9 | `MCCDashboard.tsx` | Replace | IPC status | Status shows |
| 3.10 | `ProcessManagement.tsx` | Replace | IPC process | Start/Stop works |
| 3.11 | `LogViewer.tsx` | Replace | IPC logs | Logs stream |
| 3.12 | `Settings.tsx` | Replace | Config store | Settings save |

**HITL Gate 3B:** MCC pages complete and functional.

---

### PHASE 4: INTEGRATION VERIFICATION (Validation Layer)

**Principle:** End-to-end testing of all circuits.

| Step | Circuit | Test | Expected Result |
|------|---------|------|-----------------|
| 4.1 | Signal Ingestion | Simulate webhook | Signal appears in UI |
| 4.2 | Relationship Exposure | View contradictions | Both sides equal weight |
| 4.3 | AI Narrative | Generate narrative | Disclaimer present |
| 4.4 | MCC Control | Start/Stop backend | Status updates |
| 4.5 | Baskets | Create/Add/Remove | CRUD works |
| 4.6 | Constitutional | Check all CR rules | No violations |

**HITL Gate 4:** Full system operational.

---

## SAFETY MECHANISMS

### At Each Step:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STEP EXECUTION PROTOCOL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1. BEFORE ACTION                                                          │
│      └── Confirm which file(s) will be modified                             │
│                                                                              │
│   2. EXECUTE ACTION                                                         │
│      └── Make the change (create/modify/replace)                            │
│                                                                              │
│   3. IMMEDIATE VALIDATION                                                   │
│      ├── Does it compile? (no syntax errors)                                │
│      ├── Does it render? (visual check)                                     │
│      └── Does it function? (click test)                                     │
│                                                                              │
│   4. IF FAILURE                                                             │
│      └── Rollback to previous state before proceeding                       │
│                                                                              │
│   5. IF SUCCESS                                                             │
│      └── Mark complete, proceed to next step                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Rollback Options:

| Level | Scope | Command |
|-------|-------|---------|
| File | Single file | `git checkout -- <file>` or restore from backup |
| Phase | Multiple files | Restore specific folder from backup |
| Full | Entire project | Restore full backup |

---

## ESTIMATED TIMELINE

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Atomic Components | 2-3 hours | 3 hours |
| Phase 2: Layout Shell | 1-2 hours | 5 hours |
| Phase 3: Frontend Pages | 4-6 hours | 11 hours |
| Phase 3: MCC Pages | 2-3 hours | 14 hours |
| Phase 4: Integration | 2-3 hours | 17 hours |
| **Total** | **~15-20 hours** | Spread across sessions |

---

## WHAT GETS REMOVED vs REPLACED vs ENHANCED

### REMOVED (Old code deleted):
- Old dark theme color definitions
- Old component styling
- Unused CSS classes

### REPLACED (New code in place of old):
- `AppShell.tsx` → New bright theme shell
- `Dashboard.tsx` → New dashboard layout
- All page components → New designs

### ENHANCED (New functionality added):
- Basket screens (NEW - did not exist before)
- Breadcrumb navigation (NEW)
- Toast notifications (NEW)
- Improved accessibility (NEW)

### PRESERVED (No changes):
- All API service files (`services/*.ts`)
- All hook files (`hooks/*.ts`)
- All type definitions (`types/*.ts`)
- Backend integration logic
- Constitutional enforcement code

---

## CONSTITUTIONAL COMPLIANCE CHECKPOINTS

At each HITL Gate, verify:

| Rule | Check | How to Verify |
|------|-------|---------------|
| CR-001 | No aggregation UI elements | No "overall score" anywhere |
| CR-002 | Equal weight for contradictions | Both sides same size/style |
| CR-003 | Disclaimer present | Hardcoded, non-dismissible |
| CBS-001 | SSOT for signals | Data flows from API only |
| CBS-002 | No client-side weighting | No weight calculations in JS |

---

## APPROVAL

This plan follows the established specifications:
- Gold Standard Unified Framework (GSUF)
- Constitutional Rules (CR-001, CR-002, CR-003)
- Component Build Standards (CBS-001 through CBS-004)
- HITL Approval Gates at each phase

**Ready to execute upon your command.**

---

*Document created: January 5, 2026*
*Location: `documentation/03_SPECIFICATIONS/FRONTEND_REPLACEMENT_IMPLEMENTATION_PLAN.md`*

