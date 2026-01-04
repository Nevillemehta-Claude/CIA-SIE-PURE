# Cursor Prompt: Build CIA-SIE Frontend

Copy the entire content below and paste it into Cursor as your prompt.

---

## PROMPT START

```
You are tasked with implementing the complete frontend for CIA-SIE (Chart Intelligence Auditor & Signal Intelligence Engine).

## Primary Specification Document

Read and follow this specification exactly:
/specifications/CIA-SIE_FRONTEND_BUILD_SPECIFICATION_ICD.md

This is a 2,593-line Interface Control Document (ICD) that contains:
- Exact project structure
- Exact TypeScript types
- Exact API service implementations
- Exact React Query hooks
- Exact component implementations
- Exact page implementations

## Implementation Order

Execute in this exact sequence:

### Phase 1: Project Setup
1. Create `frontend/` directory in the project root
2. Create `package.json` exactly as specified in Section 2 (REQ-TECH-011)
3. Create `vite.config.ts` exactly as specified in Section 2 (REQ-TECH-012)
4. Create `tailwind.config.js` exactly as specified in Section 2 (REQ-TECH-013)
5. Create `tsconfig.json` with standard Vite React settings
6. Create `postcss.config.js` for Tailwind
7. Create `index.html` with root div
8. Run `npm install` to install dependencies

### Phase 2: Types (src/types/)
1. Create `src/types/enums.ts` - copy exactly from Section 6
2. Create `src/types/models.ts` - copy exactly from Section 6
3. Create `src/types/api.ts` - copy exactly from Section 6
4. Create `src/types/index.ts` - re-export all types

### Phase 3: API Services (src/services/)
1. Create `src/services/client.ts` - copy exactly from Section 7
2. Create `src/services/instruments.ts` - copy exactly from Section 7
3. Create `src/services/silos.ts` - copy exactly from Section 7
4. Create `src/services/charts.ts` - copy exactly from Section 7
5. Create `src/services/signals.ts` - copy exactly from Section 7
6. Create `src/services/relationships.ts` - copy exactly from Section 7
7. Create `src/services/narratives.ts` - copy exactly from Section 7
8. Create `src/services/ai.ts` - copy exactly from Section 7
9. Create `src/services/chat.ts` - copy exactly from Section 7
10. Create `src/services/index.ts` - re-export all services

### Phase 4: Query Configuration (src/lib/)
1. Create `src/lib/queryClient.ts` - copy exactly from Section 10
2. Create `src/lib/queryKeys.ts` - copy exactly from Section 8

### Phase 5: React Query Hooks (src/hooks/)
1. Create `src/hooks/useInstruments.ts` - copy exactly from Section 8
2. Create `src/hooks/useSilos.ts` - copy exactly from Section 8
3. Create `src/hooks/useCharts.ts` - copy exactly from Section 8
4. Create `src/hooks/useSignals.ts` - copy exactly from Section 8
5. Create `src/hooks/useRelationships.ts` - copy exactly from Section 8
6. Create `src/hooks/useNarratives.ts` - copy exactly from Section 8
7. Create `src/hooks/useAI.ts` - copy exactly from Section 8
8. Create `src/hooks/useChat.ts` - copy exactly from Section 8
9. Create `src/hooks/index.ts` - re-export all hooks

### Phase 6: Common Components (src/components/common/)
1. Create `Spinner.tsx` - loading indicator
2. Create `Button.tsx` - standard button
3. Create `Card.tsx` - card container
4. Create `EmptyState.tsx` - empty state display
5. Create `ErrorState.tsx` - error display
6. Create `Disclaimer.tsx` - CRITICAL: copy exactly from CBS-003 in Section 5

### Phase 7: Signal Components (src/components/signals/)
1. Create `DirectionBadge.tsx` - CRITICAL: copy exactly from CBS-001 in Section 5
2. Create `FreshnessBadge.tsx` - copy exactly from CBS-002 in Section 5
3. Create `SignalCard.tsx` - individual signal display
4. Create `SignalList.tsx` - signal list container

### Phase 8: Relationship Components (src/components/relationships/)
1. Create `ContradictionCard.tsx` - CRITICAL: copy exactly from CBS-004 in Section 5
2. Create `ContradictionPanel.tsx` - copy exactly from CBS-005 in Section 5
3. Create `ConfirmationCard.tsx` - confirmation display
4. Create `ConfirmationPanel.tsx` - confirmation container

### Phase 9: Narrative Components (src/components/narratives/)
1. Create `NarrativeDisplay.tsx` - CRITICAL: copy exactly from CBS-006 in Section 5
2. Create `NarrativeSection.tsx` - section display

### Phase 10: Layout Components (src/components/layout/)
1. Create `AppShell.tsx` - main layout wrapper
2. Create `Header.tsx` - top header with navigation
3. Create `Sidebar.tsx` - side navigation
4. Create `PageHeader.tsx` - page title component

### Phase 11: Feature Components
1. Create `src/components/instruments/InstrumentCard.tsx`
2. Create `src/components/instruments/InstrumentList.tsx`
3. Create `src/components/instruments/InstrumentSelector.tsx`
4. Create `src/components/silos/SiloCard.tsx`
5. Create `src/components/silos/SiloList.tsx`
6. Create `src/components/charts/ChartCard.tsx`
7. Create `src/components/charts/ChartList.tsx`
8. Create `src/components/ai/BudgetIndicator.tsx`
9. Create `src/components/ai/ChatInterface.tsx`
10. Create `src/components/ai/ModelSelector.tsx`

### Phase 12: Pages (src/pages/)
1. Create `HomePage.tsx` - copy from Section 9
2. Create `InstrumentsPage.tsx` - instrument list page
3. Create `InstrumentDetailPage.tsx` - instrument detail with silos
4. Create `SiloDetailPage.tsx` - CRITICAL: copy from Section 9
5. Create `ChartDetailPage.tsx` - chart with signal history
6. Create `ChatPage.tsx` - AI chat interface
7. Create `SettingsPage.tsx` - AI settings and usage
8. Create `NotFoundPage.tsx` - 404 page

### Phase 13: App Entry
1. Create `src/index.css` - Tailwind imports + custom styles
2. Create `src/main.tsx` - React DOM render
3. Create `src/App.tsx` - copy exactly from Section 10

### Phase 14: Verification
Run the verification matrix from Section 11:
- Confirm NO "Buy", "Sell", "Enter", "Exit" buttons exist
- Confirm DirectionBadge uses equal sizing for all directions
- Confirm ContradictionCard uses grid-cols-[1fr,auto,1fr]
- Confirm Disclaimer component is always rendered with NarrativeDisplay
- Confirm Disclaimer has no close/dismiss functionality

## CONSTITUTIONAL RULES - NON-NEGOTIABLE

These rules CANNOT be violated under ANY circumstances:

### CR-001: DECISION-SUPPORT ONLY
- NO buttons labeled "Buy", "Sell", "Enter", "Exit"
- NO text containing "should", "recommend", "suggest", "consider"
- NO action prompts implying trading decisions

### CR-002: NEVER RESOLVE CONTRADICTIONS
- ContradictionCard MUST use grid-cols-[1fr,auto,1fr] for EQUAL sizing
- Both sides of contradiction use IDENTICAL CSS classes
- NO visual hierarchy suggesting one side is "correct"
- NO aggregation, weighting, or "net" calculations

### CR-003: DESCRIPTIVE NOT PRESCRIPTIVE
- Disclaimer component MUST appear on ALL AI-generated content
- Disclaimer text is EXACTLY: "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."
- Disclaimer is NOT dismissible, collapsible, or hideable

## Backend API

The backend is already running at http://127.0.0.1:8000
Vite proxy is configured to forward /api requests to the backend.

## Start Implementation

Begin with Phase 1: Project Setup. Create the frontend directory and all configuration files first, then proceed through each phase in order.

After completing all phases, run `npm run dev` to start the development server and verify the frontend connects to the backend.
```

## PROMPT END

---

## How to Use This Prompt

1. Open Cursor
2. Open the CIA-SIE-PURE project folder
3. Open a new chat with Cursor
4. Copy everything between "PROMPT START" and "PROMPT END" above
5. Paste it into Cursor
6. Press Enter

Cursor will then systematically build the entire frontend following the ICD specification.
