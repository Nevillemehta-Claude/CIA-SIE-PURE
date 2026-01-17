# CIA-SIE FRONTEND FORENSIC ALIGNMENT AUDIT INSTRUMENT v1.0

---

| Document Metadata | Value |
|-------------------|-------|
| **Document ID** | CIA-SIE-AUDIT-001 |
| **Version** | 1.0.0 |
| **Date** | January 4, 2026 |
| **Type** | Forensic Alignment Audit Instrument |
| **Author** | Claude Opus 4.5 (claude.ai) |
| **Baseline Document** | FRONTEND_DESIGN_CONCEPT_v1.0.md (CIA-SIE-FDC-001) |
| **Target** | Actual Frontend Implementation |
| **Purpose** | Reconciliation Audit (Non-Destructive) |

---

## INSTRUCTIONS FOR CURSOR

You are executing a **Reconciliation Audit** — NOT a gap-fix audit.

**Your Role:**
1. Execute each test against the actual frontend codebase
2. Report findings in the exact format specified
3. Do NOT suggest fixes or modifications
4. Do NOT alter any code
5. Report WHAT EXISTS, not what should change

**Output Discipline:**
- For each test item, report: `ALIGNED`, `VARIANCE`, or `NOT FOUND`
- For `VARIANCE`: Document what was designed vs. what exists
- For `NOT FOUND`: Confirm the component/pattern is absent
- Include file paths and line numbers where applicable

**Critical Constraint:**
This is a documentation exercise. The implementation is the source of truth. You are mapping reality against the design baseline.

---

## AUDIT SECTION 1: COMPONENT INVENTORY

### 1.1 Core Layout Components

Execute verification against `src/` directory.

| Design Component | Expected Location | Audit Result | Actual Location (if different) | Notes |
|------------------|-------------------|--------------|-------------------------------|-------|
| `App` | `src/App.tsx` | [ ] | | |
| `AppShell` | `src/components/layout/AppShell.tsx` | [ ] | | |
| `Header` | `src/components/layout/Header.tsx` | [ ] | | |
| `Sidebar` | `src/components/layout/Sidebar.tsx` | [ ] | | |
| `MainContent` | `src/components/layout/MainContent.tsx` | [ ] | | |
| `MobileNavigation` | `src/components/layout/MobileNavigation.tsx` | [ ] | | |
| `Logo` | `src/components/layout/Logo.tsx` | [ ] | | |
| `GlobalSearch` | `src/components/layout/GlobalSearch.tsx` | [ ] | | |
| `BudgetIndicator` | `src/components/layout/BudgetIndicator.tsx` | [ ] | | |

**Auditor Output Format:**
```
COMPONENT: [Name]
DESIGNED LOCATION: [Path from design]
ACTUAL STATUS: ALIGNED | VARIANCE | NOT FOUND
ACTUAL LOCATION: [Real path if different]
NOTES: [Any observations]
```

### 1.2 Page Components

| Design Page | Expected Location | Audit Result | Actual Location | Route Path |
|-------------|-------------------|--------------|-----------------|------------|
| `Dashboard` (CommandCenter) | `src/pages/Dashboard/` | [ ] | | `/` |
| `InstrumentsPage` | `src/pages/Instruments/` | [ ] | | `/instruments` |
| `InstrumentDetailPage` | `src/pages/InstrumentDetail/` | [ ] | | `/instruments/:id` |
| `SiloDetailPage` | `src/pages/SiloDetail/` | [ ] | | `/silos/:id` |
| `ChartDetailPage` | `src/pages/ChartDetail/` | [ ] | | `/charts/:id` |
| `ChartsReferencePage` | `src/pages/ChartsReference/` | [ ] | | `/charts` |
| `ChatPage` | `src/pages/Chat/` | [ ] | | `/chat` |
| `SettingsPage` | `src/pages/Settings/` | [ ] | | `/settings` |
| `PlatformsPage` | `src/pages/Platforms/` | [ ] | | `/platforms` |
| `BasketsPage` | `src/pages/Baskets/` | [ ] | | `/baskets` |
| `NotFoundPage` | `src/pages/NotFound/` | [ ] | | `*` |

### 1.3 Constitutional Components (★ CRITICAL)

These components are marked as constitutional-critical in the design. Their presence is mandatory.

| Component | Expected Location | Audit Result | Constitutional Rule |
|-----------|-------------------|--------------|---------------------|
| `ConstitutionalBanner` | `src/components/constitutional/ConstitutionalBanner.tsx` | [ ] | CR-001, CR-002, CR-003 |
| `Disclaimer` | `src/components/constitutional/Disclaimer.tsx` | [ ] | CR-003 |
| `NoResolutionNotice` | `src/components/constitutional/NoResolutionNotice.tsx` | [ ] | CR-002 |
| `ContradictionCard` | `src/components/relationships/ContradictionCard.tsx` | [ ] | CR-002 |
| `ContradictionPanel` | `src/components/relationships/ContradictionPanel.tsx` | [ ] | CR-002 |
| `NarrativeDisplay` | `src/components/ai/NarrativeDisplay.tsx` | [ ] | CR-003 |

### 1.4 Shared Components

| Component Category | Design Components | Found in Codebase | Missing |
|--------------------|-------------------|-------------------|---------|
| **Indicators** | DirectionBadge, FreshnessIndicator, SignalTypeBadge, StatusBadge | [ List found ] | [ List missing ] |
| **AI Components** | ModelSelector, TokenDisplay, CostDisplay, BudgetAlert, AIUsagePanel | [ List found ] | [ List missing ] |
| **Interactive** | Accordion, Tabs, Modal, Dropdown, Tooltip | [ List found ] | [ List missing ] |
| **Display** | Card, Badge, Table, InfoBox, CommandBox | [ List found ] | [ List missing ] |
| **Feedback** | LoadingSpinner, ErrorMessage, SuccessMessage, EmptyState | [ List found ] | [ List missing ] |

---

## AUDIT SECTION 2: STATE MANAGEMENT

### 2.1 State Management Technology

**Design Specifies:** React Query (TanStack Query) for server state

**Audit Task:** Verify presence and usage.

```
CHECK 1: Is @tanstack/react-query in package.json dependencies?
RESULT: [ YES | NO ]
VERSION: [ ]

CHECK 2: Is QueryClientProvider wrapping App?
FILE: [ ]
LINE: [ ]
RESULT: [ YES | NO ]

CHECK 3: Count of useQuery hooks in codebase:
COUNT: [ ]
FILES: [ List files using useQuery ]

CHECK 4: Count of useMutation hooks in codebase:
COUNT: [ ]
FILES: [ List files using useMutation ]
```

### 2.2 Query Key Structure

**Design Specifies:**
```typescript
queryKeys = {
  instruments: {
    all: ['instruments'],
    detail: (id) => ['instruments', id],
    silos: (id) => ['instruments', id, 'silos']
  },
  silos: {
    all: ['silos'],
    detail: (id) => ['silos', id],
    charts: (id) => ['silos', id, 'charts'],
    relationships: (id) => ['silos', id, 'relationships']
  },
  // ... etc
}
```

**Audit Task:** Document actual query key patterns used.

```
ACTUAL QUERY KEY PATTERNS FOUND:
1. [ Pattern ] - Used in [ File ]
2. [ Pattern ] - Used in [ File ]
3. [ Pattern ] - Used in [ File ]
...

ALIGNMENT STATUS: [ ALIGNED | VARIANCE | NOT FOUND ]
VARIANCE NOTES: [ If applicable ]
```

### 2.3 Stale Time Configuration

**Design Specifies:** 30 seconds for signal freshness

**Audit Task:**
```
STALE TIME CONFIGURATION FOUND:
- Default: [ value ]
- Signal-specific: [ value ]
- Location: [ file:line ]

ALIGNMENT STATUS: [ ALIGNED | VARIANCE | NOT FOUND ]
```

---

## AUDIT SECTION 3: FOLDER STRUCTURE

### 3.1 Top-Level Structure

**Design Specifies:**
```
src/
├── components/
├── pages/
├── hooks/
├── services/
├── types/
├── utils/
├── constants/
├── styles/
└── assets/
```

**Audit Task:** Run `ls -la src/` and document:

```
ACTUAL TOP-LEVEL STRUCTURE:
src/
├── [ actual folders ]
...

DESIGNED BUT MISSING: [ list ]
EXISTS BUT NOT DESIGNED: [ list ]
```

### 3.2 Components Subfolder Structure

**Design Specifies:**
```
components/
├── layout/
├── constitutional/
├── relationships/
├── ai/
├── indicators/
├── interactive/
├── display/
└── feedback/
```

**Audit Task:** Run `ls -la src/components/` and document:

```
ACTUAL COMPONENTS STRUCTURE:
components/
├── [ actual folders ]
...

DESIGNED BUT MISSING: [ list ]
EXISTS BUT NOT DESIGNED: [ list ]
```

---

## AUDIT SECTION 4: CONSTITUTIONAL COMPLIANCE (★ CRITICAL)

### 4.1 CR-001: Decision-Support ONLY — No Confidence/Strength Fields

**Design Mandate:** No confidence scores, strength ratings, or system judgment displayed.

**Audit Task:** Search entire frontend codebase for violations.

```bash
# Execute these searches and report findings:
grep -rn "confidence" src/
grep -rn "strength" src/
grep -rn "weight" src/
grep -rn "score" src/
grep -rn "rating" src/
grep -rn "recommendation" src/
grep -rn "suggest" src/
```

**Output Format:**
```
CR-001 VIOLATION SEARCH RESULTS:

"confidence" matches:
- [ file:line ] - [ context ] - [ VIOLATION | ACCEPTABLE ]
...

"strength" matches:
- [ file:line ] - [ context ] - [ VIOLATION | ACCEPTABLE ]
...

(Continue for each term)

OVERALL CR-001 STATUS: [ COMPLIANT | VIOLATIONS FOUND ]
VIOLATION COUNT: [ ]
```

### 4.2 CR-002: Expose, NEVER Resolve — Equal Visual Weight

**Design Mandate:** ContradictionCard must display both sides with identical styling. No resolution mechanism.

**Audit Task:** Locate ContradictionCard component and verify:

```
FILE LOCATION: [ ]

CHECK 1: Grid layout uses equal columns (1fr auto 1fr or equivalent)?
CODE SNIPPET: [ ]
RESULT: [ YES | NO | N/A ]

CHECK 2: Both sides use identical className/styling?
LEFT SIDE CLASS: [ ]
RIGHT SIDE CLASS: [ ]
RESULT: [ IDENTICAL | DIFFERENT | N/A ]

CHECK 3: No "resolve" or "dismiss" or "prefer" functionality?
SEARCH RESULTS: [ ]
RESULT: [ COMPLIANT | VIOLATION ]

CHECK 4: No visual hierarchy indicators (primary/secondary styling)?
RESULT: [ COMPLIANT | VIOLATION ]

CR-002 OVERALL STATUS: [ COMPLIANT | VIOLATIONS FOUND ]
```

### 4.3 CR-003: Descriptive AI ONLY — Mandatory Disclaimer

**Design Mandate:** Hardcoded disclaimer must appear with ALL AI-generated content. Cannot be dismissed.

**Audit Task:**

```
DISCLAIMER COMPONENT SEARCH:

CHECK 1: Disclaimer component exists?
LOCATION: [ ]
RESULT: [ YES | NO ]

CHECK 2: Disclaimer text is hardcoded (not from props/state/API)?
CODE SNIPPET: [ ]
RESULT: [ HARDCODED | DYNAMIC | N/A ]

CHECK 3: Disclaimer text matches specification?
EXPECTED: "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."
ACTUAL: [ ]
RESULT: [ MATCH | MISMATCH | N/A ]

CHECK 4: No dismiss/close/hide functionality?
RESULT: [ COMPLIANT | VIOLATION ]

CHECK 5: Disclaimer rendered with NarrativeDisplay?
FILE: [ ]
LINE: [ ]
RESULT: [ YES | NO | N/A ]

CHECK 6: Disclaimer rendered in ChatInterface/ChatPage?
FILE: [ ]
LINE: [ ]
RESULT: [ YES | NO | N/A ]

CR-003 OVERALL STATUS: [ COMPLIANT | VIOLATIONS FOUND ]
```

---

## AUDIT SECTION 5: INTEGRATION CONTRACT

### 5.1 API Service Layer

**Design Specifies:** Centralized API service with typed endpoints.

**Audit Task:**

```
API SERVICE LOCATION: [ ]

ENDPOINTS IMPLEMENTED:
| Endpoint Pattern | Implemented | File:Line |
|------------------|-------------|-----------|
| /api/v1/instruments/* | [ YES/NO ] | [ ] |
| /api/v1/silos/* | [ YES/NO ] | [ ] |
| /api/v1/charts/* | [ YES/NO ] | [ ] |
| /api/v1/signals/* | [ YES/NO ] | [ ] |
| /api/v1/relationships/* | [ YES/NO ] | [ ] |
| /api/v1/narratives/* | [ YES/NO ] | [ ] |
| /api/v1/chat/* | [ YES/NO ] | [ ] |
| /api/v1/ai/* | [ YES/NO ] | [ ] |
| /api/v1/platforms/* | [ YES/NO ] | [ ] |
| /api/v1/baskets/* | [ YES/NO ] | [ ] |
| /api/v1/webhook/* | [ YES/NO ] | [ ] |
| /api/v1/strategy/* | [ YES/NO ] | [ ] |
```

### 5.2 TypeScript Types

**Design Specifies:** Full type coverage for all API responses.

**Audit Task:** Verify types directory and coverage.

```
TYPES DIRECTORY: [ ]

KEY TYPES DEFINED:
| Type Name | Defined | File |
|-----------|---------|------|
| Instrument | [ ] | [ ] |
| Silo | [ ] | [ ] |
| Chart | [ ] | [ ] |
| Signal | [ ] | [ ] |
| Contradiction | [ ] | [ ] |
| Confirmation | [ ] | [ ] |
| Narrative | [ ] | [ ] |
| ChatMessage | [ ] | [ ] |
| AIModel | [ ] | [ ] |
| BudgetStatus | [ ] | [ ] |

TYPES ALIGNMENT: [ FULL | PARTIAL | MINIMAL ]
```

---

## AUDIT SECTION 6: TECHNICAL SPECIFICATIONS

### 6.1 Framework/Stack

**Design Specifies:**
- React 18+
- TypeScript
- React Router v6
- TanStack Query
- Tailwind CSS

**Audit Task:** Check package.json

```
PACKAGE.JSON AUDIT:

| Dependency | Specified | Actual Version | Status |
|------------|-----------|----------------|--------|
| react | 18+ | [ ] | [ ] |
| typescript | Yes | [ ] | [ ] |
| react-router-dom | v6 | [ ] | [ ] |
| @tanstack/react-query | Yes | [ ] | [ ] |
| tailwindcss | Yes | [ ] | [ ] |

ADDITIONAL DEPENDENCIES NOT IN DESIGN: [ list ]
```

### 6.2 Naming Conventions

**Design Specifies:**
- Components: PascalCase
- Files: PascalCase.tsx for components
- Hooks: camelCase starting with "use"
- Utils: camelCase
- Constants: SCREAMING_SNAKE_CASE

**Audit Task:** Sample 10 files from each category and verify:

```
NAMING CONVENTION AUDIT:

Components (sample 10):
1. [ filename ] - [ COMPLIANT | VIOLATION ]
...

Hooks (sample all):
1. [ filename ] - [ COMPLIANT | VIOLATION ]
...

OVERALL NAMING COMPLIANCE: [ HIGH | MEDIUM | LOW ]
```

### 6.3 Accessibility

**Design Specifies:** WCAG 2.1 AA compliance

**Audit Task:** Spot-check critical components:

```
ACCESSIBILITY SPOT CHECK:

| Component | Has aria-label/role | Has semantic HTML | Keyboard navigable |
|-----------|---------------------|-------------------|-------------------|
| Sidebar navigation | [ ] | [ ] | [ ] |
| ContradictionCard | [ ] | [ ] | [ ] |
| Disclaimer | [ ] | [ ] | [ ] |
| Modal (if exists) | [ ] | [ ] | [ ] |
| Form inputs | [ ] | [ ] | [ ] |

ACCESSIBILITY ESTIMATE: [ GOOD | NEEDS WORK | POOR ]
```

---

## AUDIT SECTION 7: ROUTE CONFIGURATION

**Design Specifies:** React Router v6 with specific route structure.

**Audit Task:** Locate router configuration and document:

```
ROUTER FILE: [ ]

ROUTES DEFINED:
| Path | Component | Matches Design |
|------|-----------|----------------|
| / | [ ] | [ ] |
| /instruments | [ ] | [ ] |
| /instruments/:id | [ ] | [ ] |
| /silos/:id | [ ] | [ ] |
| /charts | [ ] | [ ] |
| /charts/:id | [ ] | [ ] |
| /chat | [ ] | [ ] |
| /settings | [ ] | [ ] |
| /platforms | [ ] | [ ] |
| /baskets | [ ] | [ ] |
| * (404) | [ ] | [ ] |

ROUTES IN CODE BUT NOT DESIGN: [ list ]
ROUTES IN DESIGN BUT NOT CODE: [ list ]
```

---

## AUDIT SECTION 8: FRESHNESS INDICATOR LOGIC

**Design Specifies:**
- CURRENT: < 5 minutes (green)
- RECENT: 5-30 minutes (yellow)  
- STALE: 30-60 minutes (orange)
- UNAVAILABLE: > 60 minutes or no data (red)

**Audit Task:** Locate freshness calculation logic:

```
FRESHNESS LOGIC LOCATION: [ ]

THRESHOLDS IMPLEMENTED:
| Status | Design Threshold | Actual Threshold | Match |
|--------|------------------|------------------|-------|
| CURRENT | < 5 min | [ ] | [ ] |
| RECENT | 5-30 min | [ ] | [ ] |
| STALE | 30-60 min | [ ] | [ ] |
| UNAVAILABLE | > 60 min | [ ] | [ ] |

COLOR MAPPING:
| Status | Design Color | Actual Color | Match |
|--------|--------------|--------------|-------|
| CURRENT | green | [ ] | [ ] |
| RECENT | yellow | [ ] | [ ] |
| STALE | orange | [ ] | [ ] |
| UNAVAILABLE | red | [ ] | [ ] |
```

---

## AUDIT SECTION 9: BUDGET ALERT THRESHOLDS

**Design Specifies:**
- 80% — Warning (yellow)
- 90% — Critical (orange)
- 100% — Exhausted (red)

**Audit Task:** Locate budget alert logic:

```
BUDGET ALERT LOCATION: [ ]

THRESHOLDS IMPLEMENTED:
| Level | Design Threshold | Actual Threshold | Match |
|-------|------------------|------------------|-------|
| Warning | 80% | [ ] | [ ] |
| Critical | 90% | [ ] | [ ] |
| Exhausted | 100% | [ ] | [ ] |

ALERT STYLING MATCHES DESIGN: [ YES | NO | PARTIAL ]
```

---

## AUDIT OUTPUT SUMMARY

Complete this summary after all sections:

```
═══════════════════════════════════════════════════════════════════
CIA-SIE FRONTEND FORENSIC ALIGNMENT AUDIT — SUMMARY REPORT
═══════════════════════════════════════════════════════════════════

AUDIT DATE: [ ]
BASELINE: FRONTEND_DESIGN_CONCEPT_v1.0.md
TARGET: [ repository path ]

───────────────────────────────────────────────────────────────────
SECTION RESULTS
───────────────────────────────────────────────────────────────────

| Section | Status | Aligned | Variance | Not Found |
|---------|--------|---------|----------|-----------|
| 1. Component Inventory | [ ] | [ ] | [ ] | [ ] |
| 2. State Management | [ ] | [ ] | [ ] | [ ] |
| 3. Folder Structure | [ ] | [ ] | [ ] | [ ] |
| 4. Constitutional Compliance | [ ] | [ ] | [ ] | [ ] |
| 5. Integration Contract | [ ] | [ ] | [ ] | [ ] |
| 6. Technical Specifications | [ ] | [ ] | [ ] | [ ] |
| 7. Route Configuration | [ ] | [ ] | [ ] | [ ] |
| 8. Freshness Indicator | [ ] | [ ] | [ ] | [ ] |
| 9. Budget Alerts | [ ] | [ ] | [ ] | [ ] |

───────────────────────────────────────────────────────────────────
CONSTITUTIONAL COMPLIANCE (★ CRITICAL)
───────────────────────────────────────────────────────────────────

| Rule | Status | Violations |
|------|--------|------------|
| CR-001: Decision-Support ONLY | [ PASS / FAIL ] | [ count ] |
| CR-002: Expose, NEVER Resolve | [ PASS / FAIL ] | [ count ] |
| CR-003: Descriptive AI ONLY | [ PASS / FAIL ] | [ count ] |

───────────────────────────────────────────────────────────────────
VARIANCE REGISTER
───────────────────────────────────────────────────────────────────

| ID | Section | Design Says | Implementation Has | Classification |
|----|---------|-------------|-------------------|----------------|
| V1 | [ ] | [ ] | [ ] | [ ] |
| V2 | [ ] | [ ] | [ ] | [ ] |
...

Classification Key:
- ACCEPTABLE: Valid implementation choice, document rationale
- REVIEW: Needs human decision on whether to align
- CRITICAL: Constitutional violation, requires attention

───────────────────────────────────────────────────────────────────
UNDOCUMENTED ADDITIONS
───────────────────────────────────────────────────────────────────

Components/features found in implementation but not in design:

| Item | Location | Recommended Action |
|------|----------|-------------------|
| [ ] | [ ] | Document in design / Remove / Keep |
...

───────────────────────────────────────────────────────────────────
AUDIT COMPLETE
───────────────────────────────────────────────────────────────────

Auditor: Cursor (Claude Opus 4.5)
Audit Instrument: CIA-SIE-AUDIT-001 v1.0.0
Audit Instrument Author: Claude Opus 4.5 (claude.ai)

This audit is a RECONCILIATION exercise. The implementation is the 
source of truth. Variances require documentation, not necessarily 
correction.

Next Step: Return this completed audit to Claude (claude.ai) for 
interpretation and reconciliation report generation.
```

---

## EXECUTION CHECKLIST FOR CURSOR

Before returning audit results:

- [ ] All 9 sections completed
- [ ] Every checkbox/field populated
- [ ] Constitutional compliance section fully executed
- [ ] Summary table completed
- [ ] Variance register populated
- [ ] Undocumented additions listed
- [ ] No code was modified during audit
- [ ] File paths and line numbers included where requested

---

*End of Audit Instrument*
