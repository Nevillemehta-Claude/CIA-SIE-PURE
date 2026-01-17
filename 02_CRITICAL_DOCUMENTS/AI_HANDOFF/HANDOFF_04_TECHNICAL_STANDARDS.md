# HANDOFF_04: TECHNICAL STANDARDS

**Purpose:** Define engineering excellence requirements
**Standard:** Enterprise-Grade, Production-Ready Code
**Governance:** Gold Standard Specification v2.0.0

---

## MASTER REFERENCE

This document implements standards from the **CIA-SIE Gold Standard Specification**.
For complete governance details, see: `specifications/architecture/00_GOLD_STANDARD_SPECIFICATION.md`

---

## FIVE IMMUTABLE LAWS OF DEVELOPMENT

These laws are **NON-NEGOTIABLE**. Every implementation decision must align with these principles.

### Law 1: Meaning Precedes Implementation
```
WHAT before HOW.
Requirements before code.
Understanding before building.
```
- No code shall be written without clear, documented requirements
- Every function must have a defined purpose before implementation
- "Why are we building this?" must be answered before "How do we build this?"

### Law 2: Structure Precedes Intelligence
```
Data structures before algorithms.
Schema before logic.
Foundation before features.
```
- Database schema must be finalized before business logic
- Data models must be defined before service layer development
- Type definitions must exist before functions that use them

### Law 3: Validation Precedes Optimisation
```
Correct before fast.
Working before elegant.
Tested before deployed.
```
- All code must be functionally correct before performance optimization
- Unit tests must pass before refactoring for efficiency
- "Make it work, make it right, make it fast" - in that order

### Law 4: Explicit Precedes Implicit
```
No magic.
No hidden behavior.
No undocumented side effects.
```
- All dependencies must be explicitly declared
- All side effects must be documented
- No "convention over configuration" that hides behavior

### Law 5: Reversibility Precedes Commitment
```
Design for rollback.
Every change undoable.
Every deployment reversible.
```
- Every database migration must have a rollback script
- Every deployment must be reversible within 5 minutes
- No "one-way door" decisions without explicit approval

---

## SIX ARCHITECTURE PRINCIPLES

### Principle 1: Single Source of Truth (SSOT)
Each piece of data has ONE authoritative source. No duplication of business logic.
- Database is the single source of truth for persistent data
- No duplicate validation logic between frontend and backend

### Principle 2: Loose Coupling
Components interact through well-defined interfaces. Changes isolated to single component.
- Services communicate through defined API contracts
- No direct database access from presentation layer

### Principle 3: High Cohesion
Related functionality grouped together. Each module has single, clear purpose.
- Feature-based folder structure, not type-based
- Each service handles one domain concept

### Principle 4: Explicit Contracts
API contracts documented and versioned. Breaking changes require version bump.
- TypeScript interfaces for all data structures
- Semantic versioning for API changes

### Principle 5: Fail-Safe Defaults
System fails to safe state. Missing config = secure defaults. Unknown input = reject.
- All configuration has sensible, secure defaults
- Invalid input returns 400 Bad Request, never processed

### Principle 6: Deterministic Behaviour
Same input = same output. No hidden state. Reproducible results.
- Pure functions where possible
- Idempotent API operations where applicable

---

## TECHNICAL INQUIRY FRAMEWORK

Before implementing, the following domains must be addressed with specificity.

---

## 1. ARCHITECTURAL STANDARDS

### 1.1 Architectural Patterns

| Pattern | Application |
|---------|-------------|
| **Component-Based Architecture** | React components with single responsibility |
| **Container/Presenter Pattern** | Separate data fetching from presentation |
| **State Management** | React Query for server state, Context for UI state |
| **Event-Driven Updates** | Polling/WebSocket for real-time signal updates |

### 1.2 Separation of Concerns

```
frontend/src/
├── components/     # Presentational components (pure, no side effects)
├── containers/     # Data-fetching containers
├── hooks/          # Custom React hooks
├── services/       # API communication layer
├── types/          # TypeScript type definitions
├── utils/          # Pure utility functions
└── styles/         # Global styles and theme
```

### 1.3 Scalability & Maintainability

- **Modular Components:** Each component in its own file
- **Prop Drilling Avoided:** Use Context or composition
- **Type Safety:** Full TypeScript coverage
- **Consistent Patterns:** Same patterns across all components

---

## 2. FRONTEND DEVELOPMENT STANDARDS

### 2.1 UI/UX Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Intuitive Navigation** | Sidebar + clear visual hierarchy |
| **Minimal Cognitive Load** | Information grouped logically, progressive disclosure |
| **Immediate Feedback** | Loading states, error states, success confirmations |
| **Accessibility** | WCAG 2.1 AA compliance |

### 2.2 Technology Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **React 18+** | UI Framework | Component model, hooks, concurrent features |
| **TypeScript 5+** | Type Safety | Catch errors at compile time |
| **Vite** | Build Tool | Fast HMR, optimized builds |
| **TailwindCSS** | Styling | Utility-first, consistent design system |
| **React Query** | Server State | Caching, background updates, optimistic UI |
| **Axios** | HTTP Client | Already implemented in api.ts |

### 2.3 Performance Benchmarks

| Metric | Target |
|--------|--------|
| **First Contentful Paint (FCP)** | < 1.5s |
| **Time to Interactive (TTI)** | < 3.0s |
| **Lighthouse Performance Score** | > 90 |
| **Bundle Size (gzipped)** | < 200KB initial |

### 2.4 Responsive Design

```css
/* Primary breakpoint */
@media (max-width: 900px) {
    /* Sidebar collapses to hamburger menu */
    /* Single column layout */
    /* Touch-friendly targets (min 44px) */
}
```

### 2.5 Accessibility Compliance

- **Semantic HTML:** Use correct elements (button, nav, main, aside)
- **ARIA Labels:** Where semantic HTML insufficient
- **Keyboard Navigation:** Full functionality via keyboard
- **Color Contrast:** WCAG AA minimum (4.5:1 for text)
- **Focus Indicators:** Visible focus states

---

## 3. BACKEND INTEGRATION STANDARDS

### 3.1 API Communication

```typescript
// Use the existing api.ts service layer
// All API calls go through this centralized service
import { instrumentsApi, silosApi, chartsApi } from '../services/api'

// Handle loading, error, and success states
const { data, isLoading, error } = useQuery({
  queryKey: ['instruments'],
  queryFn: () => instrumentsApi.list()
})
```

### 3.2 Error Handling

```typescript
// Centralized error boundary
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>

// API error handling
try {
  const data = await api.get('/endpoint')
} catch (error) {
  if (axios.isAxiosError(error)) {
    // Handle HTTP errors
    showToast(error.response?.data?.detail || 'An error occurred')
  }
}
```

### 3.3 Data Validation

- Validate API responses match TypeScript types
- Use Zod or similar for runtime validation if needed
- Never trust external data without validation

---

## 4. ALGORITHMIC EXCELLENCE & CODE EFFICIENCY

### 4.1 Performance Optimization

| Technique | Application |
|-----------|-------------|
| **Memoization** | `useMemo` for expensive calculations |
| **Callback Stability** | `useCallback` for event handlers passed to children |
| **Virtualization** | For lists > 100 items |
| **Code Splitting** | Lazy load routes and heavy components |
| **Image Optimization** | WebP format, lazy loading |

### 4.2 Minimalistic Coding

```typescript
// ❌ Verbose
const filteredCharts = charts.filter(chart => {
  if (chart.is_active === true) {
    return true
  } else {
    return false
  }
})

// ✅ Minimal
const filteredCharts = charts.filter(chart => chart.is_active)
```

### 4.3 Code Elegance

- **Single Responsibility:** Each function does one thing
- **Pure Functions:** No side effects where possible
- **Descriptive Names:** Self-documenting code
- **Avoid Magic Numbers:** Use named constants

```typescript
// Constants
const FRESHNESS_THRESHOLDS = {
  CURRENT_MINUTES: 2,
  RECENT_MINUTES: 10,
  STALE_MINUTES: 30
} as const

// Pure function
const getFreshnessStatus = (minutesAgo: number): FreshnessStatus => {
  if (minutesAgo <= FRESHNESS_THRESHOLDS.CURRENT_MINUTES) return 'CURRENT'
  if (minutesAgo <= FRESHNESS_THRESHOLDS.RECENT_MINUTES) return 'RECENT'
  if (minutesAgo <= FRESHNESS_THRESHOLDS.STALE_MINUTES) return 'STALE'
  return 'UNAVAILABLE'
}
```

---

## 5. CODE QUALITY & DEPLOYMENT GRADE

### 5.1 Production Tier

**Target: Enterprise-Grade**

| Characteristic | Requirement |
|----------------|-------------|
| **Error Handling** | Comprehensive, graceful degradation |
| **Logging** | Structured, appropriate levels |
| **Security** | XSS prevention, CSRF protection |
| **Performance** | Optimized, monitored |
| **Documentation** | Complete, up-to-date |

### 5.2 Code Quality Metrics

| Metric | Target | Enforcement |
|--------|--------|-------------|
| **TypeScript Coverage** | 100% (no `any` types) | CI/CD gate |
| **Unit Test Coverage** | > 90% | CI/CD gate |
| **Integration Test Coverage** | > 80% | CI/CD gate |
| **Technical Debt Ratio** | < 3% | Weekly review |
| **Documentation Coverage** | 100% for public APIs | PR review |
| **Cyclomatic Complexity** | < 10 per function | Linter rule |
| **Code Duplication** | < 3% | Static analysis |
| **File Size** | < 300 lines per component | PR review |

### 5.3 Testing Strategy

| Test Type | Coverage |
|-----------|----------|
| **Unit Tests** | Individual components, utilities |
| **Integration Tests** | API integration, state management |
| **E2E Tests** | Critical user flows |

```typescript
// Example component test
describe('FreshnessIndicator', () => {
  it('displays green badge for CURRENT status', () => {
    render(<FreshnessIndicator status="CURRENT" />)
    expect(screen.getByText('CURRENT')).toHaveClass('badge-success')
  })
})
```

### 5.4 Build & Deployment

```bash
# Development
npm run dev          # Start dev server on port 3000

# Production build
npm run build        # TypeScript compile + Vite build
npm run preview      # Preview production build

# Quality checks
npm run lint         # ESLint
npm run typecheck    # TypeScript compiler check
npm run test         # Vitest
```

---

## 6. SECURITY STANDARDS

### 6.1 OWASP Top 10 Mitigation

| Vulnerability | Mitigation |
|---------------|------------|
| **XSS** | React's built-in escaping, no `dangerouslySetInnerHTML` |
| **Injection** | Parameterized API calls only |
| **Sensitive Data Exposure** | No secrets in frontend code |
| **Security Misconfiguration** | Proper CORS, CSP headers |

### 6.2 Frontend Security Checklist

- [ ] No hardcoded API keys or secrets
- [ ] No user input rendered as HTML without sanitization
- [ ] Validate all external data
- [ ] Use HTTPS for all API calls (handled by proxy)
- [ ] No sensitive data in localStorage

---

## 7. FILE NAMING CONVENTIONS

```
components/
├── CommandCenter.tsx        # PascalCase for components
├── CommandCenter.test.tsx   # Test file with same name + .test
├── CommandCenter.module.css # CSS modules with same name

hooks/
├── useInstruments.ts        # camelCase with 'use' prefix
├── useRelationships.ts

services/
├── api.ts                   # camelCase for services/utilities

types/
├── index.ts                 # Barrel export for types
```

---

## 8. CODE STYLE REQUIREMENTS

### 8.1 TypeScript Best Practices

```typescript
// ✅ Use interfaces for object types
interface ChartProps {
  chart: Chart
  onSelect?: (chartId: string) => void
}

// ✅ Use type for unions
type FreshnessStatus = 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'

// ✅ Use const assertions for enums
const DIRECTIONS = {
  BULLISH: 'BULLISH',
  BEARISH: 'BEARISH',
  NEUTRAL: 'NEUTRAL'
} as const

// ❌ Avoid any type
const data: any = response  // BAD
const data: unknown = response  // Better, then narrow
```

### 8.2 React Best Practices

```tsx
// ✅ Functional components with TypeScript
const ChartCard: React.FC<ChartProps> = ({ chart, onSelect }) => {
  // ...
}

// ✅ Destructure props
const { chart_id, chart_name, direction } = chart

// ✅ Use fragments to avoid unnecessary divs
return (
  <>
    <Header />
    <Content />
  </>
)

// ✅ Conditional rendering
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}
```

---

## 9. DOCUMENTATION REQUIREMENTS

### 9.1 Component Documentation

```tsx
/**
 * Displays a single chart with its current signal status.
 *
 * @param chart - The chart entity to display
 * @param freshness - Current freshness status of the latest signal
 * @param onSelect - Optional callback when chart is selected
 *
 * @example
 * <ChartCard
 *   chart={chart}
 *   freshness="CURRENT"
 *   onSelect={(id) => navigate(`/charts/${id}`)}
 * />
 */
const ChartCard: React.FC<ChartCardProps> = ({ chart, freshness, onSelect }) => {
  // ...
}
```

### 9.2 Complex Logic Documentation

```typescript
/**
 * Calculates signal freshness based on time since last signal.
 *
 * Thresholds (configurable per silo):
 * - CURRENT: ≤ 2 minutes (default)
 * - RECENT: ≤ 10 minutes (default)
 * - STALE: > 30 minutes (default)
 * - UNAVAILABLE: No signal received
 *
 * @param lastSignalTime - ISO timestamp of last signal
 * @param thresholds - Silo-specific threshold configuration
 * @returns FreshnessStatus enum value
 */
const calculateFreshness = (
  lastSignalTime: string | null,
  thresholds: FreshnessThresholds
): FreshnessStatus => {
  // ...
}
```

---

---

## 10. STAGE-GATE GOVERNANCE

Development must pass through these gates before deployment.

### Gate 1: Design Review
**Entry Criteria:**
- Requirements documented
- Architecture Decision Record (ADR) created
- API specification drafted

**Exit Criteria:**
- Architecture approved by tech lead
- Security concerns addressed
- API design reviewed

### Gate 2: Code Review
**Entry Criteria:**
- Feature branch created
- Code implemented
- Unit tests written

**Exit Criteria:**
- PR approved by 2 reviewers
- All comments addressed
- Static analysis passed
- Test coverage met (>90%)

### Gate 3: Security Review
**Entry Criteria:**
- Code review passed
- Integration tests passed

**Exit Criteria:**
- No critical/high vulnerabilities
- OWASP checklist verified
- Secrets scan passed

### Gate 4: Performance Review
**Entry Criteria:**
- Security review passed
- Load tests executed

**Exit Criteria:**
- Response time targets met (<200ms p95)
- No memory leaks detected
- Bundle size acceptable (<500KB)

### Gate 5: Release Review
**Entry Criteria:**
- All prior gates passed
- Documentation complete

**Exit Criteria:**
- Release notes approved
- Rollback procedure verified
- Monitoring configured

---

## 11. PERFORMANCE TARGETS

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (p95) | < 200ms | Server-side timing |
| API Response Time (p99) | < 500ms | Server-side timing |
| First Contentful Paint | < 1.5s | Lighthouse |
| Time to Interactive | < 3.0s | Lighthouse |
| Largest Contentful Paint | < 2.5s | Lighthouse |
| Cumulative Layout Shift | < 0.1 | Lighthouse |
| Bundle Size (gzipped) | < 500KB | Build output |

---

## 12. TESTING REQUIREMENTS

### Testing Pyramid

```
                    /\
                   /  \
                  / E2E \        <- 10% of tests
                 /______\
                /        \
               / Contract  \     <- 20% of tests
              /____________\
             /              \
            /  Integration   \   <- 30% of tests
           /__________________\
          /                    \
         /     Unit Tests       \  <- 40% of tests
        /________________________\
```

### Test Types Required

| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Unit Tests** | > 90% | Isolated function/method tests |
| **Contract Tests** | 100% of API endpoints | API contract validation |
| **Integration Tests** | > 80% | Component interaction tests |
| **Failure Mode Tests** | All error paths | Error handling, recovery |
| **AI-Specific Tests** | All AI endpoints | Hallucination detection, prompt injection prevention |

### AI-Specific Testing Requirements

```typescript
// Test AI safety constraints
describe('AI Response Validation', () => {
  it('rejects responses containing recommendations', async () => {
    const unsafeResponse = "You should buy now because..."
    const result = validateAIResponse(unsafeResponse)
    expect(result.valid).toBe(false)
  })

  it('rejects responses without disclaimer', async () => {
    const noDisclaimerResponse = "Chart shows bullish signal."
    const result = validateAIResponse(noDisclaimerResponse)
    expect(result.valid).toBe(false)
  })

  it('accepts valid descriptive responses with disclaimer', async () => {
    const validResponse = `Chart 01A displays a BULLISH signal.

    This is a description of what your charts are showing.
    The interpretation and any decision is entirely yours.`
    const result = validateAIResponse(validResponse)
    expect(result.valid).toBe(true)
  })
})
```

---

## 13. ANTI-PATTERNS TO AVOID

These patterns are **PROHIBITED**. Code exhibiting these patterns must be refactored.

### 1. Big Ball of Mud
**Description:** No clear structure, everything depends on everything.
**Signs:** Circular dependencies, god classes, changes require many file edits.
**Prevention:** Enforce module boundaries, regular architecture reviews.

### 2. Golden Hammer
**Description:** Using one solution for all problems.
**Signs:** Same pattern everywhere regardless of fit.
**Prevention:** ADRs for significant decisions, evaluate alternatives.

### 3. Premature Optimisation
**Description:** Optimizing before measuring, before correctness.
**Signs:** Complex caching without profiling, micro-optimizations in non-critical paths.
**Prevention:** "Make it work, make it right, make it fast" - in order.

### 4. Copy-Paste Programming
**Description:** Duplicating code instead of abstracting.
**Signs:** Similar code in multiple places, bug fixes needed in multiple locations.
**Prevention:** DRY principle enforcement, code duplication metrics.

### 5. Magic Numbers
**Description:** Hardcoded values without explanation.
**Signs:** Numbers in code without context.
**Prevention:** Named constants for all magic values.

### 6. God Object
**Description:** One class/component that does everything.
**Signs:** Classes with 1000+ lines, components with 20+ props.
**Prevention:** Single Responsibility Principle, maximum file size limits.

### 7. Spaghetti Code
**Description:** Tangled control flow, impossible to follow.
**Signs:** Deep nesting (> 4 levels), impossible to unit test.
**Prevention:** Cyclomatic complexity limits, extract method refactoring.

---

## 14. SUMMARY: IMPLEMENTATION CHECKLIST

| Standard | Requirement | Verified |
|----------|-------------|----------|
| **Five Laws** | All 5 immutable laws followed | [ ] |
| **Architecture Principles** | All 6 principles applied | [ ] |
| Architecture | Component-based, separation of concerns | [ ] |
| TypeScript | 100% coverage, no `any` types | [ ] |
| Performance | FCP < 1.5s, TTI < 3.0s, API < 200ms | [ ] |
| Accessibility | WCAG 2.1 AA compliant | [ ] |
| Security | OWASP Top 10 mitigated | [ ] |
| Testing | > 90% unit, > 80% integration | [ ] |
| Documentation | 100% for public APIs | [ ] |
| Code Quality | Complexity < 10, Debt < 3%, Duplication < 3% | [ ] |
| Responsive | Works at 900px breakpoint | [ ] |
| Constitutional | No violations of HANDOFF_03 | [ ] |
| **Stage Gates** | All 5 gates passed | [ ] |
| **Anti-Patterns** | None of 7 anti-patterns present | [ ] |
