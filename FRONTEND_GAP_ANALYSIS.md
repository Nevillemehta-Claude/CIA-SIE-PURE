# CIA-SIE Frontend Gap Analysis

## Executive Summary

**Critical Finding**: The frontend is a **non-functional shell**. While the backend provides 50+ working API endpoints, the frontend pages contain **hardcoded mock data** and do not actually fetch or display real data.

---

## Gap Matrix: Spec vs Backend vs Frontend

### 1. DASHBOARD PAGE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| Show all instruments | Required | `GET /instruments` ✅ | **HARDCODED** - Shows mock data | **CRITICAL** |
| Show contradictions count | Required | `GET /relationships/instrument/{id}` ✅ | **HARDCODED** - Static number | **CRITICAL** |
| Show confirmations count | Required | `GET /relationships/instrument/{id}` ✅ | **HARDCODED** - Static number | **CRITICAL** |
| Show active charts count | Required | `GET /charts` ✅ | **HARDCODED** - Static number | **CRITICAL** |
| List contradictions | Required | Returns full contradiction objects ✅ | **NOT CONNECTED** | **CRITICAL** |
| List confirmations | Required | Returns full confirmation objects ✅ | **NOT CONNECTED** | **CRITICAL** |
| Recent signals list | Required | `GET /signals/chart/{id}` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |

### 2. INSTRUMENTS PAGE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| List all instruments | Required | `GET /instruments` ✅ | **HARDCODED** - Mock cards | **CRITICAL** |
| Show silo count per instrument | Required | `GET /silos?instrument_id={id}` ✅ | **HARDCODED** | **CRITICAL** |
| Show chart count per instrument | Required | Available via silos→charts ✅ | **HARDCODED** | **CRITICAL** |
| Navigate to instrument detail | Required | N/A (frontend routing) | Link exists but **NO DATA** | **CRITICAL** |

### 3. INSTRUMENT DETAIL PAGE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| Show all silos for instrument | Required | `GET /silos?instrument_id={id}` ✅ | **NOT CONNECTED** | **CRITICAL** |
| Show charts per silo | Required | `GET /charts?silo_id={id}` ✅ | **NOT CONNECTED** | **CRITICAL** |
| Show signal per chart | Required | `GET /charts/{id}/signals?limit=1` ✅ | **NOT CONNECTED** | **CRITICAL** |
| Show freshness per chart | Required | Returned in relationship summary ✅ | **NOT CONNECTED** | **CRITICAL** |
| Show contradictions | Required | `GET /relationships/instrument/{id}` ✅ | **NOT CONNECTED** | **CRITICAL** |
| Show confirmations | Required | `GET /relationships/instrument/{id}` ✅ | **NOT CONNECTED** | **CRITICAL** |

### 4. SILO DETAIL PAGE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| Silo detail page | Required | Full API support ✅ | **PAGE DOES NOT EXIST** | **CRITICAL** |
| Show all charts in silo | Required | `GET /charts?silo_id={id}` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| Show relationship summary | Required | `GET /relationships/silo/{id}` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| AI Narrative panel | Required | `GET /narratives/silo/{id}` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |

### 5. CHART DETAIL PAGE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| Show current signal | Required | `GET /charts/{id}/signals?limit=1` ✅ | **HARDCODED** | **CRITICAL** |
| Show signal history | Required | `GET /charts/{id}/signals` ✅ | **HARDCODED** | **CRITICAL** |
| Show indicator values | Required | Returned in signal payload ✅ | **HARDCODED** | **CRITICAL** |
| Show freshness | Required | Calculated from timestamp ✅ | **HARDCODED** | **CRITICAL** |

### 6. AI CHAT INTERFACE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| Chat page/modal | Required | `POST /chat/{scrip_id}` ✅ | **PAGE DOES NOT EXIST** | **CRITICAL** |
| Send message | Required | Full API ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| Show conversation history | Required | `GET /chat/{scrip_id}/history` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| Model selection | Required | `GET /ai/models` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| Show mandatory disclaimer | Required | Returned in response ✅ | **NOT IMPLEMENTED** | **CRITICAL** |

### 7. ANALYTICAL BASKETS

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| Baskets page | Required | Full CRUD API ✅ | **PAGE DOES NOT EXIST** | **CRITICAL** |
| Create basket | Required | `POST /baskets` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| Add charts to basket | Required | `POST /baskets/{id}/charts/{chartId}` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |
| View basket contents | Required | `GET /baskets/{id}` ✅ | **NOT IMPLEMENTED** | **CRITICAL** |

### 8. SETTINGS PAGE

| Feature | Spec Requirement | Backend Status | Frontend Status | GAP |
|---------|------------------|----------------|-----------------|-----|
| AI model selection | Required | `GET /ai/models` ✅ | **HARDCODED** dropdown | **MEDIUM** |
| Budget display | Required | `GET /ai/budget` ✅ | **HARDCODED** | **MEDIUM** |
| Platform status | Required | `GET /platforms` ✅ | **HARDCODED** | **MEDIUM** |

---

## Data Flow Verification

### What SHOULD Happen (Per Spec):
```
User loads Dashboard
  → Frontend calls GET /api/v1/instruments
  → Frontend calls GET /api/v1/relationships/instrument/{id} for each
  → Dashboard displays real instruments with real contradiction/confirmation counts
  → User clicks instrument → loads real silo/chart data
  → User sees real signals, real contradictions, real AI narratives
```

### What ACTUALLY Happens:
```
User loads Dashboard
  → Frontend renders HARDCODED mock data
  → No API calls made
  → User sees fake static numbers
  → Navigation leads to more hardcoded pages
  → No real data ever displayed
```

---

## Root Cause Analysis

### Problem 1: Pages Don't Use Hooks
The frontend has well-defined hooks (`useInstruments`, `useSilos`, `useRelationships`, etc.) but the **pages don't use them**. Instead, pages render hardcoded JSX.

**Example - DashboardPage.tsx:**
```typescript
// WHAT EXISTS (hardcoded):
const stats = [
  { label: 'Active Charts', value: '12' },  // HARDCODED
  { label: 'Contradictions', value: '3' },   // HARDCODED
  ...
]

// WHAT SHOULD EXIST:
const { data: instruments } = useInstruments()
const { data: relationships } = useInstrumentRelationships(instrumentId)
// Then render actual data
```

### Problem 2: Missing Pages
Critical pages don't exist:
- `/silos/:siloId` - Silo Detail Page
- `/chat/:instrumentId` - AI Chat Interface
- `/baskets` - Analytical Baskets

### Problem 3: Components Not Wired
Composite components exist (ContradictionPanel, ConfirmationPanel, NarrativePanel, SignalHistoryList) but are **never rendered** in pages.

---

## Required Fixes (Priority Order)

### Phase 1: Core Data Display (Critical)

1. **DashboardPage.tsx** - Connect to real data
   - Use `useInstruments()` hook
   - Use `useInstrumentRelationships()` for each instrument
   - Render `ContradictionPanel` with real data
   - Render `ConfirmationPanel` with real data

2. **InstrumentsPage.tsx** - Connect to real data
   - Use `useInstruments()` hook
   - Use `useSilosByInstrument()` for counts
   - Render real instrument cards

3. **InstrumentDetailPage.tsx** - Connect to real data
   - Use `useInstrument(id)` hook
   - Use `useSilosByInstrument(id)` hook
   - Use `useInstrumentRelationships(id)` hook
   - Render real silos, charts, signals

### Phase 2: Missing Pages (Critical)

4. **Create SiloDetailPage.tsx**
   - Use `useSilo(id)` hook
   - Use `useRelationshipSummary(id)` hook
   - Use `useSiloNarrative(id)` hook
   - Render charts, contradictions, confirmations, narrative

5. **Create ChatPage.tsx**
   - Create `useChat()` hook for API calls
   - Implement message input and display
   - Show conversation history
   - Include mandatory disclaimer

6. **Create BasketsPage.tsx**
   - Create `useBaskets()` hook
   - Implement basket CRUD UI

### Phase 3: Signal History & Details (High)

7. **ChartDetailPage.tsx** - Connect to real data
   - Use actual signal API calls
   - Render `SignalHistoryList` with real data

### Phase 4: Settings & Configuration (Medium)

8. **SettingsPage.tsx** - Connect to real data
   - Use `useAIModels()` hook
   - Use `useAIBudget()` hook
   - Use `usePlatforms()` hook

---

## Verification Checklist

After fixes, verify each flow:

- [ ] Dashboard loads real instruments from API
- [ ] Dashboard shows real contradiction count
- [ ] Dashboard shows real confirmation count
- [ ] Clicking instrument loads real silos
- [ ] Each silo shows real charts
- [ ] Each chart shows real signal direction
- [ ] Each chart shows real freshness status
- [ ] ContradictionPanel shows real contradictions side-by-side
- [ ] ConfirmationPanel shows real confirmations
- [ ] NarrativePanel shows real AI narrative with disclaimer
- [ ] Chat sends messages and receives AI responses
- [ ] Baskets can be created and charts added

---

## Estimated Effort

| Phase | Components | Complexity |
|-------|------------|------------|
| Phase 1 | 3 pages | High - Core data wiring |
| Phase 2 | 3 new pages | High - New implementations |
| Phase 3 | 1 page | Medium - Signal history |
| Phase 4 | 1 page | Low - Settings wiring |

---

## Conclusion

The frontend is architecturally sound (good hooks, good components, good types) but **completely disconnected from real data**. The fix requires:

1. Wiring existing hooks to existing pages
2. Creating 3 missing pages
3. Rendering existing composite components

The backend is fully functional. This is purely a frontend integration problem.
