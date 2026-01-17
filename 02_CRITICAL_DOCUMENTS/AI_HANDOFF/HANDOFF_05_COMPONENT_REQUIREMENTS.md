# HANDOFF_05: COMPONENT REQUIREMENTS

**Purpose:** Define exact components that must be implemented
**Reference:** `CIA-SIE_INTERACTIVE_USER_MANUAL.html`

---

## COMPONENT HIERARCHY

```
App
├── Layout
│   ├── Sidebar
│   │   ├── SidebarHeader
│   │   └── SidebarNav
│   │       └── NavItem
│   └── MainContent
│       ├── PageHeader
│       └── ContentArea
│
├── Pages
│   ├── Dashboard (CommandCenter)
│   │   ├── ConstitutionalBanner
│   │   ├── InstrumentSelector
│   │   ├── SignalGrid
│   │   │   └── ChartSignalCard
│   │   ├── ContradictionPanel
│   │   │   └── ContradictionAlert
│   │   ├── ConfirmationPanel
│   │   └── NarrativePanel
│   │
│   ├── InstrumentDetail
│   │   ├── InstrumentHeader
│   │   ├── SiloList
│   │   │   └── SiloCard
│   │   └── ChartGrid
│   │       └── ChartCard
│   │
│   ├── SiloDetail
│   │   ├── SiloHeader
│   │   ├── ChartSignalGrid
│   │   ├── RelationshipSummary
│   │   └── NarrativeDisplay
│   │
│   ├── ChartsReference
│   │   └── ChartInfoGrid
│   │       └── ChartInfoCard
│   │
│   └── Settings
│       └── SettingsForm
│
└── Shared Components
    ├── DirectionBadge
    ├── FreshnessIndicator
    ├── Accordion
    ├── Tabs
    ├── Card
    ├── Badge
    ├── CommandBox
    ├── InfoBox
    ├── Table
    ├── WorkflowDiagram
    ├── LoadingSpinner
    └── ErrorMessage
```

---

## DETAILED COMPONENT SPECIFICATIONS

### 1. Layout Component

**File:** `components/Layout.tsx`

**Purpose:** Main application layout with sidebar and content area

**Props:**
```typescript
interface LayoutProps {
  children: React.ReactNode
}
```

**Structure:**
```tsx
<div className="app-container">
  <Sidebar />
  <main className="main-content">
    {children}
  </main>
  <MobileToggle />
</div>
```

---

### 2. Sidebar Component

**File:** `components/Sidebar.tsx`

**Purpose:** Fixed navigation sidebar

**State:**
- `isOpen` (boolean) - Mobile menu state

**Sections:**
1. Header with logo "CIA-SIE"
2. Getting Started nav section
3. Using CIA-SIE nav section
4. Integration nav section
5. Reference nav section

**Behavior:**
- Fixed position on desktop
- Slides in/out on mobile (≤900px)
- Active nav item highlighted

---

### 3. ConstitutionalBanner Component

**File:** `components/ConstitutionalBanner.tsx`

**Purpose:** Display the three constitutional principles prominently

**Props:** None (static content)

**Content (EXACT):**
1. "Decision-Support NOT Decision-Making"
2. "Expose Contradictions, NEVER Resolve Them"
3. "Descriptive AI, NOT Prescriptive AI"

**Styling:**
- Yellow/amber gradient background
- Warning icon prefix
- Grid layout for three items

---

### 4. SignalGrid Component

**File:** `components/SignalGrid.tsx`

**Purpose:** Display all charts with their current signals

**Props:**
```typescript
interface SignalGridProps {
  siloId: string
}
```

**Data Fetching:**
```typescript
const { data } = useQuery({
  queryKey: ['relationships', siloId],
  queryFn: () => relationshipsApi.getForSilo(siloId)
})
```

**Renders:**
- Grid of `ChartSignalCard` components
- One card per chart in the silo

---

### 5. ChartSignalCard Component

**File:** `components/ChartSignalCard.tsx`

**Purpose:** Display single chart with signal status

**Props:**
```typescript
interface ChartSignalCardProps {
  chartCode: string
  chartName: string
  timeframe: string
  direction: Direction | null
  freshness: FreshnessStatus
  onClick?: () => void
}
```

**Visual Elements:**
- Chart code (large, primary color)
- Chart name
- Timeframe badge
- Direction indicator (arrow + color)
- Freshness badge

**NO weight or score displays (prohibited)**

---

### 6. DirectionBadge Component

**File:** `components/DirectionBadge.tsx`

**Purpose:** Display BULLISH/BEARISH/NEUTRAL with appropriate styling

**Props:**
```typescript
interface DirectionBadgeProps {
  direction: Direction | null
  size?: 'sm' | 'md' | 'lg'
}
```

**Visual:**
| Direction | Arrow | Color |
|-----------|-------|-------|
| BULLISH | ↑ | Green (#10b981) |
| BEARISH | ↓ | Red (#ef4444) |
| NEUTRAL | → | Gray (#64748b) |
| null | — | Gray |

---

### 7. FreshnessIndicator Component

**File:** `components/FreshnessIndicator.tsx`

**Purpose:** Show signal freshness status

**Props:**
```typescript
interface FreshnessIndicatorProps {
  status: FreshnessStatus
  showLabel?: boolean
}
```

**Visual:**
| Status | Icon | Color | Label |
|--------|------|-------|-------|
| CURRENT | 🟢 | Green | "Current" |
| RECENT | 🟡 | Yellow | "Recent" |
| STALE | 🔴 | Red | "Stale" |
| UNAVAILABLE | ⚫ | Gray | "Unavailable" |

---

### 8. ContradictionAlert Component

**File:** `components/ContradictionAlert.tsx`

**Purpose:** Display a contradiction between two charts

**Props:**
```typescript
interface ContradictionAlertProps {
  contradiction: Contradiction
}
```

**CRITICAL VISUAL REQUIREMENTS:**
- Both charts displayed with EQUAL prominence
- No visual suggestion of which is "correct"
- Warning color scheme (amber/yellow)
- Clear "CONTRADICTION DETECTED" header
- Disclaimer text: "This contradiction is shown for your awareness. The system does NOT resolve this conflict."

**Layout:**
```
+--------------------------------------------------+
| ⚠ CONTRADICTION DETECTED                          |
|                                                   |
| +-----------+     ⇄     +-----------+            |
| | Chart 01A |           | Chart 02  |            |
| | ↑ BULLISH |           | ↓ BEARISH |            |
| +-----------+           +-----------+            |
|                                                   |
| Note: System does NOT resolve this conflict.     |
+--------------------------------------------------+
```

---

### 9. NarrativePanel Component

**File:** `components/NarrativePanel.tsx`

**Purpose:** Display AI-generated narrative with mandatory disclaimer

**Props:**
```typescript
interface NarrativePanelProps {
  siloId: string
  autoLoad?: boolean
}
```

**Sections Rendered:**
1. Signal Summary section
2. Contradiction section (if any)
3. Confirmation section (if any)
4. Freshness section
5. **MANDATORY: Closing statement/disclaimer**

**Disclaimer (MUST appear):**
```
"This is a description of what your charts are showing.
The interpretation and any decision is entirely yours."
```

---

### 10. Accordion Component

**File:** `components/Accordion.tsx`

**Purpose:** Collapsible content sections

**Props:**
```typescript
interface AccordionProps {
  items: AccordionItem[]
  defaultOpen?: string[]
}

interface AccordionItem {
  id: string
  number?: string | number
  title: string
  subtitle?: string
  children: React.ReactNode
}
```

**Behavior:**
- Click header to toggle open/close
- Smooth animation (0.3s)
- Chevron icon rotates on open

---

### 11. Tabs Component

**File:** `components/Tabs.tsx`

**Purpose:** Tab navigation for AI model selection

**Props:**
```typescript
interface TabsProps {
  tabs: Tab[]
  activeTab: string
  onChange: (tabId: string) => void
}

interface Tab {
  id: string
  label: string
  content: React.ReactNode
}
```

**Use Case:** AI Model selection (Haiku/Sonnet/Opus)

---

### 12. ChartInfoCard Component

**File:** `components/ChartInfoCard.tsx`

**Purpose:** Display chart details in 12 Sample Charts reference

**Props:**
```typescript
interface ChartInfoCardProps {
  code: string
  name: string
  timeframe: string
  description: string
  webhookId: string
}
```

**12 Charts Data:**
| Code | Name | Timeframe | Webhook ID |
|------|------|-----------|------------|
| 01A | Momentum Health | Daily | SAMPLE_01A |
| 02 | HTF Structure | Weekly | SAMPLE_02 |
| 04A | Risk Extension | 3H | SAMPLE_04A |
| 04B | Support/Resistance | 3H | SAMPLE_04B |
| 05A | VWAP Execution | Daily | SAMPLE_05A |
| 05B | Momentum Exhaustion | Daily | SAMPLE_05B |
| 05C | Extension Risk | Daily | SAMPLE_05C |
| 05D | VWAP Deviation | Daily | SAMPLE_05D |
| 06 | Macro Correlation | Daily | SAMPLE_06 |
| 07 | Primary Trend | Daily | SAMPLE_07 |
| 08 | Volume Analysis | Daily | SAMPLE_08 |
| 09 | Order Flow | Daily | SAMPLE_09 |

---

### 13. WorkflowDiagram Component

**File:** `components/WorkflowDiagram.tsx`

**Purpose:** Horizontal step visualization

**Props:**
```typescript
interface WorkflowDiagramProps {
  steps: WorkflowStep[]
}

interface WorkflowStep {
  number: number
  icon: string
  title: string
  description: string
}
```

**Startup Workflow Steps:**
1. Open Terminal
2. Navigate to workspace
3. Run ./start.sh
4. Browser opens

---

### 14. InfoBox Component

**File:** `components/InfoBox.tsx`

**Purpose:** Styled information callouts

**Props:**
```typescript
interface InfoBoxProps {
  variant: 'success' | 'warning' | 'danger' | 'info'
  title?: string
  children: React.ReactNode
}
```

**Styling:**
- Left border accent color
- Light background tint
- Optional icon based on variant

---

### 15. CommandBox Component

**File:** `components/CommandBox.tsx`

**Purpose:** Display terminal commands

**Props:**
```typescript
interface CommandBoxProps {
  command: string
  prefix?: string  // Default: "$ "
}
```

**Styling:**
- Dark background (#0f172a)
- Green text (#10b981)
- Monospace font
- Prefix in gray (non-selectable)

---

### 16. QuickReferenceCard Component

**File:** `components/QuickReferenceCard.tsx`

**Purpose:** Reference information display

**Props:**
```typescript
interface QuickReferenceCardProps {
  title: string
  icon?: string
  items: { label: string; value: React.ReactNode }[]
}
```

---

## PAGE COMPONENTS

### Dashboard Page (CommandCenter)

**File:** `pages/Dashboard.tsx`

**Structure:**
```tsx
<Layout>
  <PageHeader
    badge="Dashboard"
    title="CIA-SIE Command Center"
    description="Chart Intelligence Auditor & Signal Intelligence Engine"
  />
  <ContentArea>
    <ConstitutionalBanner />

    <Section title="Signal Overview">
      <InstrumentSelector />
      <SignalGrid siloId={selectedSiloId} />
    </Section>

    <Section title="Relationships">
      <ContradictionPanel siloId={selectedSiloId} />
      <ConfirmationPanel siloId={selectedSiloId} />
    </Section>

    <Section title="AI Narrative">
      <NarrativePanel siloId={selectedSiloId} />
    </Section>
  </ContentArea>
</Layout>
```

---

### Charts Reference Page

**File:** `pages/ChartsReference.tsx`

**Structure:**
```tsx
<Layout>
  <PageHeader
    badge="Reference"
    title="12 Sample Charts"
    description="Complete chart configuration reference"
  />
  <ContentArea>
    <ChartInfoGrid>
      {SAMPLE_CHARTS.map(chart => (
        <ChartInfoCard key={chart.code} {...chart} />
      ))}
    </ChartInfoGrid>
  </ContentArea>
</Layout>
```

---

## ROUTING

```typescript
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/instruments" element={<InstrumentList />} />
        <Route path="/instruments/:id" element={<InstrumentDetail />} />
        <Route path="/silos/:id" element={<SiloDetail />} />
        <Route path="/charts" element={<ChartsReference />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/troubleshooting" element={<Troubleshooting />} />
      </Routes>
    </BrowserRouter>
  )
}
```

---

## DATA FLOW

```
API (localhost:8000)
        ↓
   api.ts service
        ↓
   React Query hooks
        ↓
   Container components (fetch data)
        ↓
   Presenter components (display data)
```

---

## STATE MANAGEMENT

| State Type | Solution |
|------------|----------|
| **Server State** | React Query (caching, background updates) |
| **UI State** | React useState/useReducer |
| **Global UI State** | React Context (selected silo, theme) |
| **URL State** | React Router (current page, params) |

---

## HOOKS TO IMPLEMENT

### useInstruments (exists - update if needed)
```typescript
const useInstruments = (activeOnly = true) => {
  return useQuery({
    queryKey: ['instruments', activeOnly],
    queryFn: () => instrumentsApi.list(activeOnly)
  })
}
```

### useRelationships (exists - update if needed)
```typescript
const useRelationships = (siloId: string) => {
  return useQuery({
    queryKey: ['relationships', siloId],
    queryFn: () => relationshipsApi.getForSilo(siloId),
    enabled: !!siloId
  })
}
```

### useNarrative (new)
```typescript
const useNarrative = (siloId: string, useAi = true) => {
  return useQuery({
    queryKey: ['narrative', siloId, useAi],
    queryFn: () => narrativesApi.generateForSilo(siloId, useAi),
    enabled: !!siloId,
    staleTime: 60000  // Cache for 1 minute
  })
}
```

---

---

## AI-RELATED COMPONENTS

### 17. ModelSelector Component

**File:** `components/ModelSelector.tsx`

**Purpose:** Allow user to select Claude model (Haiku/Sonnet/Opus)

**Props:**
```typescript
interface ModelSelectorProps {
  selectedModel: string
  onModelChange: (modelId: string) => void
  disabled?: boolean
  showCosts?: boolean
  showDescriptions?: boolean
}
```

**Visual Layout:**
```
┌─────────────────────────────────────────────────────┐
│  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │  Haiku  │  │ Sonnet  │  │  Opus   │             │
│  │  ○ ○ ○  │  │ ○ ○ ○ ○ │  │○ ○ ○ ○ ○│             │
│  │  Fast   │  │ Balanced│  │ Powerful│             │
│  │ $0.0003 │  │ $0.003  │  │ $0.015  │             │
│  └─────────┘  └─────────┘  └─────────┘             │
│       ↑            ↑            ↑                   │
│    Selected     Default      Complex               │
└─────────────────────────────────────────────────────┘
```

**Behavior:**
- Three tabs/cards for each model
- Selected model highlighted with primary color
- Shows capability dots (more dots = more capable)
- Optional cost display per 1K tokens
- Disabled state grays out unavailable models

**Data Fetching:**
```typescript
const { data: models } = useQuery({
  queryKey: ['ai-models'],
  queryFn: () => aiApi.getModels()
})
```

---

### 18. TokenDisplay Component

**File:** `components/TokenDisplay.tsx`

**Purpose:** Show estimated and actual token usage

**Props:**
```typescript
interface TokenDisplayProps {
  estimatedTokens?: number
  actualTokens?: number
  model: string
  showCost?: boolean
}
```

**Visual:**
```
┌────────────────────────────┐
│ Tokens: ~1,250 ($0.004)    │
│ ████████░░ 1.2K / 4K max   │
└────────────────────────────┘
```

**Styling:**
- Compact inline display
- Color coding: green (< 50%), yellow (50-80%), red (> 80%)
- Shows cost estimate when `showCost` is true

---

### 19. CostDisplay Component

**File:** `components/CostDisplay.tsx`

**Purpose:** Show cost per request and cumulative period cost

**Props:**
```typescript
interface CostDisplayProps {
  requestCost?: number
  periodCost: number
  budgetLimit: number
  periodType: 'daily' | 'weekly' | 'monthly'
  currency?: string
}
```

**Visual:**
```
┌────────────────────────────────────┐
│ This request: $0.009               │
│ Monthly usage: $12.50 / $50.00     │
│ ██████████████░░░░░░  25%          │
└────────────────────────────────────┘
```

**Behavior:**
- Shows request cost (if provided)
- Shows period usage with progress bar
- Progress bar changes color at thresholds:
  - Green: < 50%
  - Yellow: 50-80%
  - Orange: 80-90%
  - Red: > 90%

---

### 20. BudgetAlert Component

**File:** `components/BudgetAlert.tsx`

**Purpose:** Display budget warnings and blocks

**Props:**
```typescript
interface BudgetAlertProps {
  percentageUsed: number
  budgetRemaining: number
  onDismiss?: () => void
  onRequestIncrease?: () => void
}
```

**Visual States:**

**At 80% (Warning):**
```
┌─────────────────────────────────────────────────────┐
│ ⚠️ BUDGET WARNING                            [×]    │
│ You have used 80% of your monthly AI budget.        │
│ Remaining: $10.00                                   │
└─────────────────────────────────────────────────────┘
```
- Yellow/amber background
- Dismissible

**At 90% (Critical):**
```
┌─────────────────────────────────────────────────────┐
│ 🔴 BUDGET CRITICAL                           [×]    │
│ You have used 90% of your monthly AI budget.        │
│ Remaining: $5.00                                    │
│ Each AI request will require confirmation.          │
└─────────────────────────────────────────────────────┘
```
- Red/orange background
- Not dismissible

**At 100% (Blocked):**
```
┌─────────────────────────────────────────────────────┐
│ 🚫 BUDGET EXHAUSTED                                 │
│ Your monthly AI budget has been exhausted.          │
│ AI features are disabled until next billing period. │
│                                                     │
│ [Request Budget Increase]                           │
└─────────────────────────────────────────────────────┘
```
- Red background
- Blocking modal
- Action button to request increase

---

### 21. AIUsagePanel Component

**File:** `components/AIUsagePanel.tsx`

**Purpose:** Dashboard panel showing AI usage statistics

**Props:**
```typescript
interface AIUsagePanelProps {
  period?: 'daily' | 'weekly' | 'monthly'
}
```

**Visual:**
```
┌─────────────────────────────────────────────────────┐
│ AI USAGE                               [Daily ▼]   │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Requests Today: 45                                  │
│ Tokens Used: 125,000                                │
│ Cost: $2.50                                         │
│                                                     │
│ By Model:                                           │
│ ┌──────────┬──────────┬──────────┐                 │
│ │ Haiku    │ Sonnet   │ Opus     │                 │
│ │ 30 req   │ 12 req   │ 3 req    │                 │
│ │ $0.25    │ $1.75    │ $0.50    │                 │
│ └──────────┴──────────┴──────────┘                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Data Fetching:**
```typescript
const { data: usage } = useQuery({
  queryKey: ['ai-usage', period],
  queryFn: () => aiApi.getUsage(period)
})
```

---

### 22. ChatPanel Component

**File:** `components/ChatPanel.tsx`

**Purpose:** Per-instrument conversation interface

**Props:**
```typescript
interface ChatPanelProps {
  instrumentId: string
  defaultModel?: string
}
```

**Visual:**
```
┌─────────────────────────────────────────────────────┐
│ CHAT WITH AI                    [Haiku|Sonnet|Opus] │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ 👤 What signals are current for this instrument?│ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ 🤖 Currently, 8 of 12 charts display signals.   │ │
│ │ Chart 01A shows BULLISH, while Chart 02 shows  │ │
│ │ BEARISH, indicating a contradiction...          │ │
│ │                                                 │ │
│ │ This is a description of what your charts are  │ │
│ │ showing. The interpretation and any decision   │ │
│ │ is entirely yours.                             │ │
│ │                                        ─────── │ │
│ │                                        $0.009  │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
├─────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────┐ [Send]   │
│ │ Type your question...                 │          │
│ └───────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

**Behavior:**
- Model selector at top
- Scrollable message history
- Cost shown per message
- Disclaimer ALWAYS visible in AI responses
- Input field with send button

**CRITICAL:** AI responses MUST be descriptive only. Validate before display.

---

---

## ADDITIONAL COMPONENTS (Referenced in Hierarchy)

### 23. PageHeader Component

**File:** `components/PageHeader.tsx`

**Purpose:** Consistent page header with badge, title, and description

**Props:**
```typescript
interface PageHeaderProps {
  badge: string
  title: string
  description: string
}
```

**Visual:**
```
┌────────────────────────────────────────┐
│ [Dashboard]                             │
│ CIA-SIE Command Center                  │
│ Chart Intelligence Auditor & Signal...  │
└────────────────────────────────────────┘
```

---

### 24. InstrumentSelector Component

**File:** `components/InstrumentSelector.tsx`

**Purpose:** Dropdown to select active instrument

**Props:**
```typescript
interface InstrumentSelectorProps {
  selectedId: string | null
  onSelect: (instrumentId: string) => void
}
```

**Data Fetching:**
```typescript
const { data: instruments } = useQuery({
  queryKey: ['instruments', true],
  queryFn: () => instrumentsApi.list(true)
})
```

---

### 25. ContradictionPanel Component

**File:** `components/ContradictionPanel.tsx`

**Purpose:** Container for all contradictions in a silo

**Props:**
```typescript
interface ContradictionPanelProps {
  siloId: string
}
```

**Renders:**
- Header: "Contradictions Detected" with count badge
- List of `ContradictionAlert` components
- Empty state: "No contradictions detected" (neutral, not positive)

**CRITICAL:** No "all clear" celebration - contradictions are informational, not bad.

---

### 26. ConfirmationPanel Component

**File:** `components/ConfirmationPanel.tsx`

**Purpose:** Container for all confirmations in a silo

**Props:**
```typescript
interface ConfirmationPanelProps {
  siloId: string
}
```

**Visual:**
- Shows aligned signals grouped by direction
- Equal visual weight to contradictions (confirmations are NOT "better")

**CRITICAL:** No implied preference for confirmations over contradictions.

---

### 27. LoadingSpinner Component

**File:** `components/LoadingSpinner.tsx`

**Purpose:** Loading state indicator

**Props:**
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  label?: string
}
```

---

### 28. ErrorMessage Component

**File:** `components/ErrorMessage.tsx`

**Purpose:** Display API or system errors

**Props:**
```typescript
interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}
```

---

### 29. Card Component (Generic)

**File:** `components/Card.tsx`

**Purpose:** Generic container card

**Props:**
```typescript
interface CardProps {
  title?: string
  children: React.ReactNode
  className?: string
}
```

---

### 30. Badge Component (Generic)

**File:** `components/Badge.tsx`

**Purpose:** Generic badge for labels

**Props:**
```typescript
interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
  children: React.ReactNode
}
```

---

### 31. Table Component

**File:** `components/Table.tsx`

**Purpose:** Data table for list views

**Props:**
```typescript
interface TableProps<T> {
  columns: Column<T>[]
  data: T[]
  onRowClick?: (row: T) => void
}

interface Column<T> {
  key: keyof T | string
  header: string
  render?: (row: T) => React.ReactNode
}
```

---

## ADDITIONAL PAGE SPECIFICATIONS

### InstrumentList Page

**File:** `pages/InstrumentList.tsx`

**Purpose:** List all instruments with navigation to details

**Structure:**
```tsx
<Layout>
  <PageHeader
    badge="Instruments"
    title="All Instruments"
    description="Manage your trading instruments"
  />
  <ContentArea>
    <Table
      columns={[
        { key: 'symbol', header: 'Symbol' },
        { key: 'display_name', header: 'Name' },
        { key: 'is_active', header: 'Status', render: (row) => <Badge>...</Badge> },
      ]}
      data={instruments}
      onRowClick={(row) => navigate(`/instruments/${row.instrument_id}`)}
    />
  </ContentArea>
</Layout>
```

---

### InstrumentDetail Page

**File:** `pages/InstrumentDetail.tsx`

**Purpose:** Detailed view of single instrument with silos

**Structure:**
```tsx
<Layout>
  <PageHeader
    badge="Instrument"
    title={instrument.display_name}
    description={`Symbol: ${instrument.symbol}`}
  />
  <ContentArea>
    <Section title="Silos">
      {silos.map(silo => (
        <SiloCard key={silo.silo_id} silo={silo} />
      ))}
    </Section>
    <Section title="AI Chat">
      <ChatPanel instrumentId={instrumentId} />
    </Section>
  </ContentArea>
</Layout>
```

---

### SiloDetail Page

**File:** `pages/SiloDetail.tsx`

**Purpose:** Full silo view with charts, relationships, and narrative

**Structure:**
```tsx
<Layout>
  <PageHeader
    badge="Silo"
    title={silo.silo_name}
    description="Analysis container"
  />
  <ContentArea>
    <SignalGrid siloId={siloId} />
    <ContradictionPanel siloId={siloId} />
    <ConfirmationPanel siloId={siloId} />
    <NarrativePanel siloId={siloId} />
  </ContentArea>
</Layout>
```

---

### Settings Page

**File:** `pages/Settings.tsx`

**Purpose:** Application and AI configuration

**Sections:**
1. AI Model Selection (ModelSelector)
2. Budget Configuration (budget limit input)
3. Alert Thresholds (80%, 90% inputs)
4. Platform Connections (TradingView, etc.)

**CRITICAL:** Settings do NOT include any "strategy preferences" or "risk tolerance" - the system does not make decisions based on user preferences.

---

### Troubleshooting Page

**File:** `pages/Troubleshooting.tsx`

**Purpose:** Help users diagnose common issues

**Sections:**
1. Connection Issues
2. Signal Not Updating
3. AI Errors
4. Webhook Configuration

---

## IMPLEMENTATION ORDER

1. **Foundation:** Layout, Sidebar, PageHeader
2. **Core Components:** DirectionBadge, FreshnessIndicator, Card, Badge
3. **Data Display:** SignalGrid, ChartSignalCard
4. **Critical:** ConstitutionalBanner, ContradictionAlert, NarrativePanel
5. **Utilities:** Accordion, Tabs, InfoBox, CommandBox, Table, LoadingSpinner, ErrorMessage
6. **AI Components:** ModelSelector, TokenDisplay, CostDisplay, BudgetAlert, AIUsagePanel, ChatPanel
7. **Container Panels:** InstrumentSelector, ContradictionPanel, ConfirmationPanel
8. **Pages:** Dashboard, ChartsReference, InstrumentList, InstrumentDetail, SiloDetail, Settings, Troubleshooting
9. **Polish:** Animations, responsive design, accessibility
