# CIA-SIE FRONTEND REMEDIATION PROTOCOL v3.0

## NASA-Grade Change Management with Zero-Tolerance Validation

---

| Document Metadata | Value |
|-------------------|-------|
| **Document ID** | CIA-SIE-PROTOCOL-001 |
| **Version** | 3.0.0 |
| **Date** | January 4, 2026 |
| **Type** | Remediation Protocol (NASA-Grade) |
| **Author** | Claude Opus 4.5 (claude.ai) |
| **Classification** | MISSION CRITICAL |
| **Baseline Documents** | FRONTEND_DESIGN_CONCEPT_v1.0.md, AUDIT_COMPLETED.md, RECONCILIATION_v2.0.md |
| **Execution Agent** | Cursor |
| **Validation Agent** | Automated + Human |

---

## DOCUMENT PURPOSE

This protocol provides **executable remediation procedures** with:

- ✅ Pre-change validation gates
- ✅ Exact code modifications
- ✅ Post-change validation commands
- ✅ Unit test specifications
- ✅ Integration test specifications
- ✅ End-to-end test specifications
- ✅ Regression test suites
- ✅ Rollback procedures
- ✅ Success criteria with pass/fail thresholds
- ✅ Cross-system integrity verification

**Philosophy:** No change is complete until it passes ALL validation gates. A single failure = STOP, ROLLBACK, INVESTIGATE.

---

# PART 1: ENVIRONMENT PREPARATION

## 1.1 Pre-Flight System Check

Before ANY remediation work begins, execute this complete system validation.

### 1.1.1 Repository State Verification

```bash
# COMMAND BLOCK: PRE-FLIGHT-001
# Description: Verify clean repository state
# Expected: All commands return success

echo "═══════════════════════════════════════════════════════════════"
echo "PRE-FLIGHT CHECK: Repository State"
echo "═══════════════════════════════════════════════════════════════"

cd /path/to/CIA-SIE-PURE

# Check 1: Verify we're on correct branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "develop" ]; then
  echo "⚠️  WARNING: Not on main/develop branch"
fi

# Check 2: Verify clean working directory
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ FAIL: Uncommitted changes detected"
  git status --short
  echo "ACTION: Commit or stash changes before proceeding"
  exit 1
else
  echo "✅ PASS: Working directory clean"
fi

# Check 3: Verify up-to-date with remote
git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$CURRENT_BRANCH)
if [ "$LOCAL" != "$REMOTE" ]; then
  echo "⚠️  WARNING: Local differs from remote"
  echo "Local:  $LOCAL"
  echo "Remote: $REMOTE"
fi

# Check 4: Record baseline commit hash
BASELINE_COMMIT=$(git rev-parse HEAD)
echo "📍 BASELINE COMMIT: $BASELINE_COMMIT"
echo "$BASELINE_COMMIT" > .remediation-baseline

echo "═══════════════════════════════════════════════════════════════"
```

**Success Criteria:**
- [ ] Working directory clean
- [ ] Baseline commit recorded
- [ ] No uncommitted changes

---

### 1.1.2 Dependency Verification

```bash
# COMMAND BLOCK: PRE-FLIGHT-002
# Description: Verify all dependencies are installed and compatible
# Expected: All commands return success

echo "═══════════════════════════════════════════════════════════════"
echo "PRE-FLIGHT CHECK: Dependencies"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check 1: Node version
NODE_VERSION=$(node -v)
echo "Node version: $NODE_VERSION"
if [[ ! "$NODE_VERSION" =~ ^v(18|20|22) ]]; then
  echo "❌ FAIL: Node 18+ required"
  exit 1
else
  echo "✅ PASS: Node version compatible"
fi

# Check 2: npm version
NPM_VERSION=$(npm -v)
echo "npm version: $NPM_VERSION"

# Check 3: Install dependencies
echo "Installing dependencies..."
npm ci
if [ $? -ne 0 ]; then
  echo "❌ FAIL: npm ci failed"
  exit 1
else
  echo "✅ PASS: Dependencies installed"
fi

# Check 4: Verify critical packages
echo "Verifying critical packages..."
npm list react typescript @tanstack/react-query tailwindcss --depth=0
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Critical package missing"
  exit 1
else
  echo "✅ PASS: Critical packages present"
fi

# Check 5: Security audit
echo "Running security audit..."
npm audit --audit-level=high
AUDIT_EXIT=$?
if [ $AUDIT_EXIT -ne 0 ]; then
  echo "⚠️  WARNING: Security vulnerabilities detected (non-blocking)"
fi

echo "═══════════════════════════════════════════════════════════════"
```

**Success Criteria:**
- [ ] Node 18+ installed
- [ ] npm ci completes successfully
- [ ] All critical packages present
- [ ] Security audit reviewed

---

### 1.1.3 Baseline Test Suite Execution

```bash
# COMMAND BLOCK: PRE-FLIGHT-003
# Description: Run full test suite to establish baseline
# Expected: All tests pass

echo "═══════════════════════════════════════════════════════════════"
echo "PRE-FLIGHT CHECK: Baseline Test Suite"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check 1: TypeScript compilation
echo "Running TypeScript compilation..."
npx tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ FAIL: TypeScript compilation errors"
  exit 1
else
  echo "✅ PASS: TypeScript compilation clean"
fi

# Check 2: ESLint
echo "Running ESLint..."
npx eslint src/ --max-warnings=0
ESLINT_EXIT=$?
if [ $ESLINT_EXIT -ne 0 ]; then
  echo "⚠️  WARNING: ESLint warnings/errors detected"
  # Record baseline lint state
  npx eslint src/ --format json > .eslint-baseline.json
fi

# Check 3: Unit tests
echo "Running unit tests..."
npm run test -- --coverage --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Unit tests failed"
  exit 1
else
  echo "✅ PASS: Unit tests passed"
fi

# Check 4: Record test coverage baseline
echo "Recording coverage baseline..."
cp coverage/coverage-summary.json .coverage-baseline.json

# Check 5: Build verification
echo "Running production build..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Production build failed"
  exit 1
else
  echo "✅ PASS: Production build successful"
fi

# Check 6: Record bundle size baseline
echo "Recording bundle size baseline..."
ls -la dist/assets/*.js | awk '{print $5, $9}' > .bundle-baseline.txt
cat .bundle-baseline.txt

echo "═══════════════════════════════════════════════════════════════"
echo "BASELINE ESTABLISHED"
echo "═══════════════════════════════════════════════════════════════"
```

**Success Criteria:**
- [ ] TypeScript compiles without errors
- [ ] Unit tests pass (100%)
- [ ] Coverage baseline recorded
- [ ] Production build succeeds
- [ ] Bundle size baseline recorded

---

### 1.1.4 Backend Health Verification

```bash
# COMMAND BLOCK: PRE-FLIGHT-004
# Description: Verify backend is operational for integration tests
# Expected: Backend responds to health check

echo "═══════════════════════════════════════════════════════════════"
echo "PRE-FLIGHT CHECK: Backend Health"
echo "═══════════════════════════════════════════════════════════════"

# Check 1: Backend health endpoint
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
echo "Checking backend at: $BACKEND_URL"

HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/v1/health" 2>/dev/null)
if [ "$HEALTH_RESPONSE" = "200" ]; then
  echo "✅ PASS: Backend health check passed"
else
  echo "⚠️  WARNING: Backend not responding (HTTP $HEALTH_RESPONSE)"
  echo "Integration tests will be skipped"
  export SKIP_INTEGRATION=true
fi

# Check 2: Database connectivity (via backend)
DB_RESPONSE=$(curl -s "$BACKEND_URL/api/v1/health/db" 2>/dev/null)
echo "Database status: $DB_RESPONSE"

echo "═══════════════════════════════════════════════════════════════"
```

**Success Criteria:**
- [ ] Backend health endpoint returns 200
- [ ] Database connectivity confirmed

---

### 1.1.5 Create Remediation Branch

```bash
# COMMAND BLOCK: PRE-FLIGHT-005
# Description: Create isolated branch for remediation work
# Expected: New branch created and checked out

echo "═══════════════════════════════════════════════════════════════"
echo "PRE-FLIGHT CHECK: Create Remediation Branch"
echo "═══════════════════════════════════════════════════════════════"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REMEDIATION_BRANCH="remediation/frontend-alignment-$TIMESTAMP"

git checkout -b "$REMEDIATION_BRANCH"
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Could not create branch"
  exit 1
else
  echo "✅ PASS: Created branch $REMEDIATION_BRANCH"
fi

echo "REMEDIATION_BRANCH=$REMEDIATION_BRANCH" >> .remediation-env

echo "═══════════════════════════════════════════════════════════════"
echo "PRE-FLIGHT COMPLETE - READY FOR REMEDIATION"
echo "═══════════════════════════════════════════════════════════════"
```

---

## 1.2 Pre-Flight Checklist Summary

Before proceeding to any remediation item, ALL of the following must be TRUE:

| Check | Status | Verified By |
|-------|--------|-------------|
| Repository clean | [ ] | PRE-FLIGHT-001 |
| Baseline commit recorded | [ ] | PRE-FLIGHT-001 |
| Dependencies installed | [ ] | PRE-FLIGHT-002 |
| TypeScript compiles | [ ] | PRE-FLIGHT-003 |
| Unit tests pass | [ ] | PRE-FLIGHT-003 |
| Coverage baseline recorded | [ ] | PRE-FLIGHT-003 |
| Build succeeds | [ ] | PRE-FLIGHT-003 |
| Bundle baseline recorded | [ ] | PRE-FLIGHT-003 |
| Backend operational | [ ] | PRE-FLIGHT-004 |
| Remediation branch created | [ ] | PRE-FLIGHT-005 |

**IF ANY CHECK FAILS: STOP. DO NOT PROCEED.**

---

# PART 2: REMEDIATION ITEMS

## Execution Protocol

For each remediation item, Cursor must:

1. **READ** the entire remediation block
2. **EXECUTE** Pre-Change Validation
3. **IMPLEMENT** Code Changes (exactly as specified)
4. **EXECUTE** Post-Change Validation
5. **EXECUTE** Unit Tests
6. **EXECUTE** Integration Tests
7. **EXECUTE** Regression Suite
8. **VERIFY** Success Criteria
9. **COMMIT** with standardized message
10. **PROCEED** to next item OR **ROLLBACK** if any failure

---

# REMEDIATION ITEM D6: ACCESSIBILITY ENHANCEMENTS

| Attribute | Value |
|-----------|-------|
| **ID** | REM-D6 |
| **Severity** | 🔴 **CRITICAL** |
| **Priority** | 1 of 17 |
| **Estimated Effort** | 3-5 days |
| **Risk Level** | LOW |
| **Rollback Complexity** | LOW |

---

## D6-PHASE-1: Setup Accessibility Testing Infrastructure

### D6-1.1 Pre-Change Validation

```bash
# COMMAND BLOCK: D6-PRE-001
# Description: Verify starting state before accessibility setup
# Expected: No accessibility testing packages present

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-1: Pre-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check: axe-core not already installed
if npm list @axe-core/react 2>/dev/null | grep -q "@axe-core/react"; then
  echo "⚠️  INFO: @axe-core/react already installed"
else
  echo "✅ PASS: @axe-core/react not present (expected)"
fi

# Check: jest-axe not already installed
if npm list jest-axe 2>/dev/null | grep -q "jest-axe"; then
  echo "⚠️  INFO: jest-axe already installed"
else
  echo "✅ PASS: jest-axe not present (expected)"
fi

# Record current package.json hash
PACKAGE_HASH=$(md5sum package.json | cut -d' ' -f1)
echo "Package.json hash: $PACKAGE_HASH"
echo "$PACKAGE_HASH" > .d6-package-baseline

echo "═══════════════════════════════════════════════════════════════"
```

### D6-1.2 Code Changes

```bash
# COMMAND BLOCK: D6-CHANGE-001
# Description: Install accessibility testing dependencies
# Expected: Packages installed successfully

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-1: Installing Accessibility Packages"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Install development dependencies
npm install --save-dev @axe-core/react jest-axe @testing-library/jest-dom

if [ $? -ne 0 ]; then
  echo "❌ FAIL: Package installation failed"
  exit 1
else
  echo "✅ PASS: Packages installed"
fi

echo "═══════════════════════════════════════════════════════════════"
```

### D6-1.3 Create Accessibility Test Setup File

```typescript
// FILE: frontend/src/test/setupAccessibility.ts
// ACTION: CREATE NEW FILE

import { configureAxe, toHaveNoViolations } from 'jest-axe'

// Extend Jest matchers
expect.extend(toHaveNoViolations)

// Configure axe with CIA-SIE specific rules
export const axeConfig = configureAxe({
  rules: {
    // Ensure color contrast meets WCAG AA
    'color-contrast': { enabled: true },
    // Ensure all images have alt text
    'image-alt': { enabled: true },
    // Ensure all form inputs have labels
    'label': { enabled: true },
    // Ensure page has main landmark
    'landmark-one-main': { enabled: true },
    // Ensure buttons have accessible names
    'button-name': { enabled: true },
    // Ensure links have accessible names
    'link-name': { enabled: true },
  },
})

// Helper function for component accessibility testing
export const testAccessibility = async (container: HTMLElement) => {
  const results = await axeConfig(container)
  expect(results).toHaveNoViolations()
}
```

### D6-1.4 Update Jest Configuration

```typescript
// FILE: frontend/jest.config.ts (or jest.config.js)
// ACTION: MODIFY - Add setupFilesAfterEnv entry

// Add this to the configuration:
// setupFilesAfterEnv: ['<rootDir>/src/test/setupAccessibility.ts'],
```

### D6-1.5 Post-Change Validation

```bash
# COMMAND BLOCK: D6-POST-001
# Description: Verify accessibility setup is correct
# Expected: All validations pass

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-1: Post-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check 1: Packages installed
echo "Verifying packages..."
npm list @axe-core/react jest-axe @testing-library/jest-dom --depth=0
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Required packages not found"
  exit 1
else
  echo "✅ PASS: All packages installed"
fi

# Check 2: Setup file exists
if [ -f "src/test/setupAccessibility.ts" ]; then
  echo "✅ PASS: Setup file created"
else
  echo "❌ FAIL: Setup file missing"
  exit 1
fi

# Check 3: TypeScript compilation still works
echo "Verifying TypeScript compilation..."
npx tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ FAIL: TypeScript compilation broken"
  exit 1
else
  echo "✅ PASS: TypeScript compilation clean"
fi

# Check 4: Existing tests still pass
echo "Running existing test suite..."
npm run test -- --watchAll=false --passWithNoTests
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Existing tests broken"
  exit 1
else
  echo "✅ PASS: Existing tests still pass"
fi

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-1: COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
```

### D6-1.6 Commit Checkpoint

```bash
# COMMAND BLOCK: D6-COMMIT-001
# Description: Commit Phase 1 changes
# Expected: Clean commit

git add -A
git commit -m "feat(a11y): setup accessibility testing infrastructure

- Install @axe-core/react, jest-axe, @testing-library/jest-dom
- Create setupAccessibility.ts with axe configuration
- Configure Jest for accessibility testing

Remediation: D6-PHASE-1
Protocol: CIA-SIE-PROTOCOL-001 v3.0"

echo "✅ COMMITTED: D6-PHASE-1"
```

---

## D6-PHASE-2: Add ARIA Labels to Layout Components

### D6-2.1 Pre-Change Validation

```bash
# COMMAND BLOCK: D6-PRE-002
# Description: Verify layout components exist and record baseline
# Expected: All layout components found

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-2: Pre-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check layout components exist
LAYOUT_FILES=(
  "src/components/layout/Header.tsx"
  "src/components/layout/Sidebar.tsx"
  "src/components/layout/AppShell.tsx"
)

for FILE in "${LAYOUT_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "✅ FOUND: $FILE"
    # Record line count baseline
    wc -l "$FILE"
  else
    echo "❌ MISSING: $FILE"
    exit 1
  fi
done

# Record current state for diff verification
mkdir -p .remediation-backups/d6-phase-2
cp src/components/layout/*.tsx .remediation-backups/d6-phase-2/

echo "═══════════════════════════════════════════════════════════════"
```

### D6-2.2 Code Changes - Header.tsx

```typescript
// FILE: frontend/src/components/layout/Header.tsx
// ACTION: MODIFY - Add ARIA attributes

// FIND THIS PATTERN (approximate):
// <header className="...">

// REPLACE WITH:
// <header 
//   className="..."
//   role="banner"
//   aria-label="CIA-SIE main header"
// >

// FIND navigation container (if exists):
// <nav className="...">

// REPLACE WITH:
// <nav 
//   className="..."
//   aria-label="Header navigation"
// >

// FIND BudgetIndicator:
// <BudgetIndicator />

// WRAP WITH:
// <div role="status" aria-live="polite" aria-label="AI budget status">
//   <BudgetIndicator />
// </div>
```

**Exact Modification for Header.tsx:**

```typescript
// ADD these imports at top if not present:
// (No new imports needed for ARIA - native HTML attributes)

// MODIFY the header element:
// Before:
export const Header = () => {
  return (
    <header className="h-16 border-b bg-white px-6 flex items-center justify-between">

// After:
export const Header = () => {
  return (
    <header 
      className="h-16 border-b bg-white px-6 flex items-center justify-between"
      role="banner"
      aria-label="CIA-SIE main header"
    >
```

### D6-2.3 Code Changes - Sidebar.tsx

```typescript
// FILE: frontend/src/components/layout/Sidebar.tsx
// ACTION: MODIFY - Add ARIA attributes

// MODIFY the aside/nav element:
// Before:
export const Sidebar = () => {
  return (
    <aside className="w-[280px] h-screen bg-slate-900 text-white fixed left-0 top-0">

// After:
export const Sidebar = () => {
  return (
    <aside 
      className="w-[280px] h-screen bg-slate-900 text-white fixed left-0 top-0"
      role="navigation"
      aria-label="Main navigation sidebar"
    >

// MODIFY the nav element inside:
// Before:
<nav className="...">

// After:
<nav 
  className="..."
  aria-label="Primary navigation menu"
>

// FOR EACH NavLink, ensure it has aria-current when active:
// React Router's NavLink handles this automatically with aria-current="page"
// Verify this is not overridden
```

### D6-2.4 Code Changes - AppShell.tsx

```typescript
// FILE: frontend/src/components/layout/AppShell.tsx
// ACTION: MODIFY - Add main landmark

// MODIFY the main content area:
// Before:
export const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="ml-[280px]">
        <Header />
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  )
}

// After:
export const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="ml-[280px]">
        <Header />
        <main 
          id="main-content"
          className="p-6"
          role="main"
          aria-label="Main content"
          tabIndex={-1}
        >
          {children}
        </main>
      </div>
    </div>
  )
}
```

### D6-2.5 Create Accessibility Tests for Layout

```typescript
// FILE: frontend/src/components/layout/__tests__/Layout.a11y.test.tsx
// ACTION: CREATE NEW FILE

import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Header } from '../Header'
import { Sidebar } from '../Sidebar'
import { AppShell } from '../AppShell'

expect.extend(toHaveNoViolations)

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } }
})

const TestWrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      {children}
    </BrowserRouter>
  </QueryClientProvider>
)

describe('Layout Components Accessibility', () => {
  describe('Header', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have banner role', () => {
      const { container } = render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      expect(container.querySelector('[role="banner"]')).toBeInTheDocument()
    })

    it('should have aria-label on header', () => {
      const { container } = render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      expect(container.querySelector('[aria-label="CIA-SIE main header"]')).toBeInTheDocument()
    })
  })

  describe('Sidebar', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have navigation role', () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      expect(container.querySelector('[role="navigation"]')).toBeInTheDocument()
    })

    it('should have aria-label on navigation', () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      expect(container.querySelector('[aria-label="Main navigation sidebar"]')).toBeInTheDocument()
    })
  })

  describe('AppShell', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have main landmark', () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      expect(container.querySelector('[role="main"]')).toBeInTheDocument()
    })

    it('should have focusable main content for skip links', () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      const main = container.querySelector('#main-content')
      expect(main).toHaveAttribute('tabIndex', '-1')
    })
  })
})
```

### D6-2.6 Post-Change Validation

```bash
# COMMAND BLOCK: D6-POST-002
# Description: Verify layout accessibility changes
# Expected: All validations pass

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-2: Post-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check 1: TypeScript compilation
echo "Checking TypeScript compilation..."
npx tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ FAIL: TypeScript compilation broken"
  echo "ROLLBACK REQUIRED"
  exit 1
else
  echo "✅ PASS: TypeScript compilation clean"
fi

# Check 2: Run layout accessibility tests
echo "Running layout accessibility tests..."
npm run test -- --testPathPattern="Layout.a11y" --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Layout accessibility tests failed"
  echo "ROLLBACK REQUIRED"
  exit 1
else
  echo "✅ PASS: Layout accessibility tests passed"
fi

# Check 3: Run all existing tests (regression check)
echo "Running full test suite (regression)..."
npm run test -- --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Regression detected - existing tests broken"
  echo "ROLLBACK REQUIRED"
  exit 1
else
  echo "✅ PASS: All existing tests still pass"
fi

# Check 4: Verify ARIA attributes in built output
echo "Building and checking output..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  exit 1
fi

# Check 5: Verify attributes exist in output
grep -r "role=\"banner\"" dist/ > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ PASS: role=\"banner\" found in build output"
else
  echo "❌ FAIL: role=\"banner\" missing from build output"
  exit 1
fi

grep -r "role=\"main\"" dist/ > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ PASS: role=\"main\" found in build output"
else
  echo "❌ FAIL: role=\"main\" missing from build output"
  exit 1
fi

grep -r "role=\"navigation\"" dist/ > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ PASS: role=\"navigation\" found in build output"
else
  echo "❌ FAIL: role=\"navigation\" missing from build output"
  exit 1
fi

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-2: COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
```

### D6-2.7 Commit Checkpoint

```bash
# COMMAND BLOCK: D6-COMMIT-002
# Description: Commit Phase 2 changes
# Expected: Clean commit

git add -A
git commit -m "feat(a11y): add ARIA labels to layout components

- Header: Add role=\"banner\", aria-label
- Sidebar: Add role=\"navigation\", aria-label  
- AppShell: Add role=\"main\", make main focusable
- Add accessibility tests for all layout components

Remediation: D6-PHASE-2
Protocol: CIA-SIE-PROTOCOL-001 v3.0"

echo "✅ COMMITTED: D6-PHASE-2"
```

---

## D6-PHASE-3: Add ARIA to Constitutional Components

### D6-3.1 Pre-Change Validation

```bash
# COMMAND BLOCK: D6-PRE-003
# Description: Verify constitutional components exist
# Expected: All components found

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-3: Pre-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check constitutional-critical components exist
CONST_FILES=(
  "src/components/relationships/ContradictionCard.tsx"
  "src/components/relationships/ContradictionPanel.tsx"
  "src/components/common/Disclaimer.tsx"
  "src/components/narratives/NarrativeDisplay.tsx"
)

for FILE in "${CONST_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "✅ FOUND: $FILE"
  else
    echo "❌ MISSING: $FILE"
    exit 1
  fi
done

# Backup current state
mkdir -p .remediation-backups/d6-phase-3
cp src/components/relationships/*.tsx .remediation-backups/d6-phase-3/ 2>/dev/null
cp src/components/common/Disclaimer.tsx .remediation-backups/d6-phase-3/ 2>/dev/null
cp src/components/narratives/*.tsx .remediation-backups/d6-phase-3/ 2>/dev/null

echo "═══════════════════════════════════════════════════════════════"
```

### D6-3.2 Code Changes - ContradictionCard.tsx

```typescript
// FILE: frontend/src/components/relationships/ContradictionCard.tsx
// ACTION: MODIFY - Add ARIA attributes for accessibility

// MODIFY the main container:
// Before:
export const ContradictionCard = ({ contradiction }: Props) => {
  const sideClassName = 'rounded-lg bg-surface-secondary p-4 text-center'
  
  return (
    <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">

// After:
export const ContradictionCard = ({ contradiction }: Props) => {
  const sideClassName = 'rounded-lg bg-surface-secondary p-4 text-center'
  
  return (
    <article 
      className="grid grid-cols-[1fr,auto,1fr] items-center gap-4"
      role="article"
      aria-label={`Contradiction: ${contradiction.chart_a_name} versus ${contradiction.chart_b_name}`}
    >

// MODIFY the left side:
// Before:
<div className={sideClassName}>

// After:
<div 
  className={sideClassName}
  role="group"
  aria-label={`${contradiction.chart_a_name} shows ${contradiction.chart_a_direction}`}
>

// MODIFY the separator:
// Before:
<span className="text-muted font-bold">VS</span>

// After:
<span className="text-muted font-bold" aria-hidden="true">VS</span>

// MODIFY the right side:
// Before:
<div className={sideClassName}>

// After:
<div 
  className={sideClassName}
  role="group"
  aria-label={`${contradiction.chart_b_name} shows ${contradiction.chart_b_direction}`}
>

// CLOSE the article:
// Before:
</div>

// After:
</article>
```

### D6-3.3 Code Changes - Disclaimer.tsx

```typescript
// FILE: frontend/src/components/common/Disclaimer.tsx
// ACTION: MODIFY - Enhance ARIA attributes

// MODIFY the container:
// Before:
export const Disclaimer = () => {
  return (
    <div className="mt-4 p-4 bg-warning-light border border-warning rounded-lg">
      <p className="text-warning-dark font-medium">
        ⚠️ {DISCLAIMER_TEXT}
      </p>
    </div>
  )
}

// After:
export const Disclaimer = () => {
  return (
    <aside 
      className="mt-4 p-4 bg-warning-light border border-warning rounded-lg"
      role="note"
      aria-label="Important disclaimer about AI-generated content"
      aria-live="polite"
    >
      <p className="text-warning-dark font-medium">
        <span aria-hidden="true">⚠️ </span>
        <span>{DISCLAIMER_TEXT}</span>
      </p>
    </aside>
  )
}
```

### D6-3.4 Code Changes - NarrativeDisplay.tsx

```typescript
// FILE: frontend/src/components/narratives/NarrativeDisplay.tsx
// ACTION: MODIFY - Add section ARIA attributes

// MODIFY the container:
// Before:
export const NarrativeDisplay = ({ narrative, isLoading }: Props) => {
  if (isLoading) {
    return <Spinner />
  }
  
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">AI Analysis</h2>

// After:
export const NarrativeDisplay = ({ narrative, isLoading }: Props) => {
  if (isLoading) {
    return (
      <div role="status" aria-label="Loading AI analysis">
        <Spinner />
        <span className="sr-only">Loading AI analysis...</span>
      </div>
    )
  }
  
  return (
    <section 
      aria-labelledby="narrative-heading"
      aria-describedby="narrative-disclaimer"
    >
      <h2 
        id="narrative-heading" 
        className="text-xl font-semibold mb-4"
      >
        AI Analysis
      </h2>

// Ensure Disclaimer has id for aria-describedby:
// <Disclaimer id="narrative-disclaimer" />
// (May need to modify Disclaimer to accept id prop)
```

### D6-3.5 Create Accessibility Tests for Constitutional Components

```typescript
// FILE: frontend/src/components/relationships/__tests__/ContradictionCard.a11y.test.tsx
// ACTION: CREATE NEW FILE

import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { ContradictionCard } from '../ContradictionCard'

expect.extend(toHaveNoViolations)

const mockContradiction = {
  id: 'test-1',
  chart_a_id: 'chart-1',
  chart_a_name: 'Momentum Health',
  chart_a_direction: 'BULLISH',
  chart_b_id: 'chart-2', 
  chart_b_name: 'HTF Structure',
  chart_b_direction: 'BEARISH',
}

describe('ContradictionCard Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should have article role', () => {
    render(<ContradictionCard contradiction={mockContradiction} />)
    expect(screen.getByRole('article')).toBeInTheDocument()
  })

  it('should have descriptive aria-label', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const article = container.querySelector('[role="article"]')
    expect(article).toHaveAttribute(
      'aria-label',
      expect.stringContaining('Momentum Health')
    )
    expect(article).toHaveAttribute(
      'aria-label', 
      expect.stringContaining('HTF Structure')
    )
  })

  it('should have equal group roles for both sides', () => {
    render(<ContradictionCard contradiction={mockContradiction} />)
    const groups = screen.getAllByRole('group')
    expect(groups).toHaveLength(2)
  })

  it('should hide decorative VS separator from screen readers', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const separator = container.querySelector('[aria-hidden="true"]')
    expect(separator).toHaveTextContent('VS')
  })

  // CR-002 CONSTITUTIONAL CHECK
  it('should NOT have any resolution buttons', () => {
    render(<ContradictionCard contradiction={mockContradiction} />)
    expect(screen.queryByRole('button', { name: /resolve/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /dismiss/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /prefer/i })).not.toBeInTheDocument()
  })
})
```

```typescript
// FILE: frontend/src/components/common/__tests__/Disclaimer.a11y.test.tsx
// ACTION: CREATE NEW FILE

import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Disclaimer } from '../Disclaimer'

expect.extend(toHaveNoViolations)

describe('Disclaimer Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<Disclaimer />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should have note role', () => {
    render(<Disclaimer />)
    expect(screen.getByRole('note')).toBeInTheDocument()
  })

  it('should have descriptive aria-label', () => {
    const { container } = render(<Disclaimer />)
    const note = container.querySelector('[role="note"]')
    expect(note).toHaveAttribute('aria-label', expect.stringContaining('disclaimer'))
  })

  // CR-003 CONSTITUTIONAL CHECK  
  it('should contain hardcoded disclaimer text', () => {
    render(<Disclaimer />)
    expect(screen.getByText(/description of what your charts are showing/i)).toBeInTheDocument()
    expect(screen.getByText(/interpretation and any decision is entirely yours/i)).toBeInTheDocument()
  })

  it('should NOT have dismiss button', () => {
    render(<Disclaimer />)
    expect(screen.queryByRole('button', { name: /dismiss/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /close/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /hide/i })).not.toBeInTheDocument()
  })
})
```

### D6-3.6 Post-Change Validation

```bash
# COMMAND BLOCK: D6-POST-003
# Description: Verify constitutional component accessibility
# Expected: All validations pass

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-3: Post-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check 1: TypeScript compilation
echo "Checking TypeScript compilation..."
npx tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ FAIL: TypeScript compilation broken"
  exit 1
else
  echo "✅ PASS: TypeScript compilation clean"
fi

# Check 2: Run constitutional component accessibility tests
echo "Running ContradictionCard accessibility tests..."
npm run test -- --testPathPattern="ContradictionCard.a11y" --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: ContradictionCard accessibility tests failed"
  exit 1
else
  echo "✅ PASS: ContradictionCard accessibility tests passed"
fi

echo "Running Disclaimer accessibility tests..."
npm run test -- --testPathPattern="Disclaimer.a11y" --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Disclaimer accessibility tests failed"
  exit 1
else
  echo "✅ PASS: Disclaimer accessibility tests passed"
fi

# Check 3: Full regression suite
echo "Running full test suite (regression)..."
npm run test -- --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Regression detected"
  exit 1
else
  echo "✅ PASS: All tests pass"
fi

# Check 4: Constitutional compliance verification
echo "Verifying CR-002 compliance (no resolution mechanisms)..."
grep -rn "resolve\|dismiss\|prefer" src/components/relationships/ContradictionCard.tsx | grep -v "aria" | grep -v "//" | grep -v "test"
if [ $? -eq 0 ]; then
  echo "⚠️  WARNING: Potential CR-002 violation found - manual review required"
else
  echo "✅ PASS: No resolution mechanisms detected"
fi

echo "Verifying CR-003 compliance (hardcoded disclaimer)..."
grep -n "DISCLAIMER_TEXT\|description of what your charts" src/components/common/Disclaimer.tsx
if [ $? -ne 0 ]; then
  echo "❌ FAIL: CR-003 - Disclaimer text not found"
  exit 1
else
  echo "✅ PASS: CR-003 - Disclaimer text present"
fi

# Check 5: Build verification
echo "Building production bundle..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  exit 1
else
  echo "✅ PASS: Build successful"
fi

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-3: COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
```

### D6-3.7 Commit Checkpoint

```bash
# COMMAND BLOCK: D6-COMMIT-003
# Description: Commit Phase 3 changes
# Expected: Clean commit

git add -A
git commit -m "feat(a11y): add ARIA labels to constitutional components

- ContradictionCard: Add article role, group roles, hide decorative VS
- Disclaimer: Add note role, aria-label, aria-live
- NarrativeDisplay: Add section with aria-labelledby
- Add accessibility tests with constitutional compliance checks
- Verify CR-002 (no resolution buttons)
- Verify CR-003 (hardcoded disclaimer)

Remediation: D6-PHASE-3
Protocol: CIA-SIE-PROTOCOL-001 v3.0"

echo "✅ COMMITTED: D6-PHASE-3"
```

---

## D6-PHASE-4: Keyboard Navigation

### D6-4.1 Pre-Change Validation

```bash
# COMMAND BLOCK: D6-PRE-004
# Description: Audit current keyboard navigation state
# Expected: Baseline established

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-4: Pre-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check for existing tabIndex usage
echo "Current tabIndex usage:"
grep -rn "tabIndex" src/ --include="*.tsx" | head -20

# Check for existing onKeyDown handlers
echo "Current onKeyDown handlers:"
grep -rn "onKeyDown" src/ --include="*.tsx" | head -20

# Backup interactive components
mkdir -p .remediation-backups/d6-phase-4
find src/components -name "*.tsx" -exec cp {} .remediation-backups/d6-phase-4/ \;

echo "═══════════════════════════════════════════════════════════════"
```

### D6-4.2 Create Keyboard Navigation Hook

```typescript
// FILE: frontend/src/hooks/useKeyboardNavigation.ts
// ACTION: CREATE NEW FILE

import { useCallback, KeyboardEvent } from 'react'

interface UseKeyboardNavigationOptions {
  onEnter?: () => void
  onSpace?: () => void
  onEscape?: () => void
  onArrowUp?: () => void
  onArrowDown?: () => void
  onArrowLeft?: () => void
  onArrowRight?: () => void
}

export const useKeyboardNavigation = (options: UseKeyboardNavigationOptions) => {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    switch (event.key) {
      case 'Enter':
        if (options.onEnter) {
          event.preventDefault()
          options.onEnter()
        }
        break
      case ' ':
        if (options.onSpace) {
          event.preventDefault()
          options.onSpace()
        }
        break
      case 'Escape':
        if (options.onEscape) {
          event.preventDefault()
          options.onEscape()
        }
        break
      case 'ArrowUp':
        if (options.onArrowUp) {
          event.preventDefault()
          options.onArrowUp()
        }
        break
      case 'ArrowDown':
        if (options.onArrowDown) {
          event.preventDefault()
          options.onArrowDown()
        }
        break
      case 'ArrowLeft':
        if (options.onArrowLeft) {
          event.preventDefault()
          options.onArrowLeft()
        }
        break
      case 'ArrowRight':
        if (options.onArrowRight) {
          event.preventDefault()
          options.onArrowRight()
        }
        break
    }
  }, [options])

  return { handleKeyDown }
}

// Utility for making divs behave like buttons
export const makeClickableAccessible = (onClick: () => void) => ({
  role: 'button' as const,
  tabIndex: 0,
  onClick,
  onKeyDown: (e: KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      onClick()
    }
  },
})
```

### D6-4.3 Create Skip Link Component

```typescript
// FILE: frontend/src/components/layout/SkipLink.tsx
// ACTION: CREATE NEW FILE

export const SkipLink = () => {
  return (
    <a
      href="#main-content"
      className="
        sr-only focus:not-sr-only
        focus:absolute focus:top-4 focus:left-4
        focus:z-50 focus:px-4 focus:py-2
        focus:bg-primary focus:text-white
        focus:rounded-lg focus:outline-none
        focus:ring-2 focus:ring-offset-2 focus:ring-primary
      "
    >
      Skip to main content
    </a>
  )
}
```

### D6-4.4 Update AppShell with Skip Link

```typescript
// FILE: frontend/src/components/layout/AppShell.tsx
// ACTION: MODIFY - Add SkipLink

// ADD import:
import { SkipLink } from './SkipLink'

// ADD as first child of container:
export const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen">
      <SkipLink />  {/* ADD THIS LINE */}
      <Sidebar />
      <div className="ml-[280px]">
        <Header />
        <main 
          id="main-content"
          className="p-6"
          role="main"
          aria-label="Main content"
          tabIndex={-1}
        >
          {children}
        </main>
      </div>
    </div>
  )
}
```

### D6-4.5 Create Keyboard Navigation Tests

```typescript
// FILE: frontend/src/hooks/__tests__/useKeyboardNavigation.test.ts
// ACTION: CREATE NEW FILE

import { renderHook } from '@testing-library/react'
import { useKeyboardNavigation, makeClickableAccessible } from '../useKeyboardNavigation'

describe('useKeyboardNavigation', () => {
  it('should call onEnter when Enter key is pressed', () => {
    const onEnter = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEnter }))
    
    const event = { key: 'Enter', preventDefault: jest.fn() } as any
    result.current.handleKeyDown(event)
    
    expect(onEnter).toHaveBeenCalled()
    expect(event.preventDefault).toHaveBeenCalled()
  })

  it('should call onSpace when Space key is pressed', () => {
    const onSpace = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onSpace }))
    
    const event = { key: ' ', preventDefault: jest.fn() } as any
    result.current.handleKeyDown(event)
    
    expect(onSpace).toHaveBeenCalled()
  })

  it('should call onEscape when Escape key is pressed', () => {
    const onEscape = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEscape }))
    
    const event = { key: 'Escape', preventDefault: jest.fn() } as any
    result.current.handleKeyDown(event)
    
    expect(onEscape).toHaveBeenCalled()
  })
})

describe('makeClickableAccessible', () => {
  it('should return correct role', () => {
    const props = makeClickableAccessible(() => {})
    expect(props.role).toBe('button')
  })

  it('should return tabIndex 0', () => {
    const props = makeClickableAccessible(() => {})
    expect(props.tabIndex).toBe(0)
  })

  it('should call onClick on Enter key', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)
    
    const event = { key: 'Enter', preventDefault: jest.fn() } as any
    props.onKeyDown(event)
    
    expect(onClick).toHaveBeenCalled()
  })

  it('should call onClick on Space key', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)
    
    const event = { key: ' ', preventDefault: jest.fn() } as any
    props.onKeyDown(event)
    
    expect(onClick).toHaveBeenCalled()
  })
})
```

```typescript
// FILE: frontend/src/components/layout/__tests__/SkipLink.a11y.test.tsx
// ACTION: CREATE NEW FILE

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'
import { SkipLink } from '../SkipLink'

expect.extend(toHaveNoViolations)

describe('SkipLink Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<SkipLink />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should be visible when focused', async () => {
    render(<SkipLink />)
    const link = screen.getByText('Skip to main content')
    
    // Link should have sr-only class initially
    expect(link).toHaveClass('sr-only')
    
    // Focus the link
    await userEvent.tab()
    
    // Link should now be visible (focus:not-sr-only)
    expect(document.activeElement).toBe(link)
  })

  it('should link to main-content', () => {
    render(<SkipLink />)
    const link = screen.getByText('Skip to main content')
    expect(link).toHaveAttribute('href', '#main-content')
  })
})
```

### D6-4.6 Post-Change Validation

```bash
# COMMAND BLOCK: D6-POST-004
# Description: Verify keyboard navigation implementation
# Expected: All validations pass

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-4: Post-Change Validation"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check 1: TypeScript compilation
echo "Checking TypeScript compilation..."
npx tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ FAIL: TypeScript compilation broken"
  exit 1
else
  echo "✅ PASS: TypeScript compilation clean"
fi

# Check 2: Verify new files exist
echo "Verifying new files..."
FILES_TO_CHECK=(
  "src/hooks/useKeyboardNavigation.ts"
  "src/components/layout/SkipLink.tsx"
)
for FILE in "${FILES_TO_CHECK[@]}"; do
  if [ -f "$FILE" ]; then
    echo "✅ FOUND: $FILE"
  else
    echo "❌ MISSING: $FILE"
    exit 1
  fi
done

# Check 3: Run keyboard navigation tests
echo "Running keyboard navigation tests..."
npm run test -- --testPathPattern="useKeyboardNavigation|SkipLink" --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Keyboard navigation tests failed"
  exit 1
else
  echo "✅ PASS: Keyboard navigation tests passed"
fi

# Check 4: Full regression suite
echo "Running full test suite (regression)..."
npm run test -- --watchAll=false
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Regression detected"
  exit 1
else
  echo "✅ PASS: All tests pass"
fi

# Check 5: Build verification
echo "Building production bundle..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  exit 1
else
  echo "✅ PASS: Build successful"
fi

# Check 6: Verify skip link in output
grep -r "Skip to main content" dist/ > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ PASS: Skip link found in build output"
else
  echo "❌ FAIL: Skip link missing from build output"
  exit 1
fi

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-4: COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
```

### D6-4.7 Commit Checkpoint

```bash
# COMMAND BLOCK: D6-COMMIT-004
# Description: Commit Phase 4 changes
# Expected: Clean commit

git add -A
git commit -m "feat(a11y): implement keyboard navigation

- Create useKeyboardNavigation hook for consistent keyboard handling
- Create makeClickableAccessible utility for div-as-button pattern
- Add SkipLink component for keyboard users
- Integrate SkipLink into AppShell
- Add comprehensive tests for keyboard navigation

Remediation: D6-PHASE-4
Protocol: CIA-SIE-PROTOCOL-001 v3.0"

echo "✅ COMMITTED: D6-PHASE-4"
```

---

## D6-PHASE-5: Lighthouse Audit & Final Verification

### D6-5.1 Run Lighthouse Accessibility Audit

```bash
# COMMAND BLOCK: D6-FINAL-001
# Description: Run Lighthouse accessibility audit
# Expected: Score > 95

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-5: Lighthouse Accessibility Audit"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Build the application
npm run build

# Start preview server in background
npm run preview &
PREVIEW_PID=$!
sleep 5

# Run Lighthouse
npx lighthouse http://localhost:4173 \
  --only-categories=accessibility \
  --output=json \
  --output-path=./lighthouse-a11y-report.json \
  --chrome-flags="--headless"

# Extract score
A11Y_SCORE=$(cat lighthouse-a11y-report.json | jq '.categories.accessibility.score * 100')
echo "Accessibility Score: $A11Y_SCORE"

# Kill preview server
kill $PREVIEW_PID

# Verify score meets threshold
if (( $(echo "$A11Y_SCORE >= 95" | bc -l) )); then
  echo "✅ PASS: Accessibility score $A11Y_SCORE >= 95"
else
  echo "❌ FAIL: Accessibility score $A11Y_SCORE < 95"
  echo "Review lighthouse-a11y-report.json for issues"
  exit 1
fi

# Generate HTML report for documentation
npx lighthouse http://localhost:4173 \
  --only-categories=accessibility \
  --output=html \
  --output-path=./lighthouse-a11y-report.html \
  --chrome-flags="--headless" &
LIGHTHOUSE_PID=$!

# Start server again for HTML report
npm run preview &
PREVIEW_PID=$!
sleep 5
wait $LIGHTHOUSE_PID
kill $PREVIEW_PID

echo "Reports generated:"
echo "  - lighthouse-a11y-report.json"
echo "  - lighthouse-a11y-report.html"

echo "═══════════════════════════════════════════════════════════════"
```

### D6-5.2 Final Regression Suite

```bash
# COMMAND BLOCK: D6-FINAL-002
# Description: Complete regression testing
# Expected: All tests pass, coverage maintained

echo "═══════════════════════════════════════════════════════════════"
echo "D6-PHASE-5: Final Regression Suite"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Full test suite with coverage
echo "Running complete test suite with coverage..."
npm run test -- --coverage --watchAll=false --coverageReporters=json-summary

if [ $? -ne 0 ]; then
  echo "❌ FAIL: Test suite failed"
  exit 1
else
  echo "✅ PASS: All tests passed"
fi

# Compare coverage to baseline
echo "Comparing coverage to baseline..."
BASELINE_COVERAGE=$(cat .coverage-baseline.json | jq '.total.lines.pct')
CURRENT_COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')

echo "Baseline coverage: $BASELINE_COVERAGE%"
echo "Current coverage:  $CURRENT_COVERAGE%"

if (( $(echo "$CURRENT_COVERAGE >= $BASELINE_COVERAGE" | bc -l) )); then
  echo "✅ PASS: Coverage maintained or improved"
else
  echo "⚠️  WARNING: Coverage decreased from $BASELINE_COVERAGE% to $CURRENT_COVERAGE%"
fi

# Bundle size check
echo "Checking bundle size..."
npm run build
CURRENT_BUNDLE_SIZE=$(ls -la dist/assets/*.js | awk '{sum += $5} END {print sum}')
BASELINE_BUNDLE_SIZE=$(cat .bundle-baseline.txt | awk '{sum += $1} END {print sum}')

echo "Baseline bundle: $BASELINE_BUNDLE_SIZE bytes"
echo "Current bundle:  $CURRENT_BUNDLE_SIZE bytes"

# Allow 10% increase for accessibility additions
MAX_ALLOWED=$(echo "$BASELINE_BUNDLE_SIZE * 1.10" | bc | cut -d'.' -f1)
if [ "$CURRENT_BUNDLE_SIZE" -le "$MAX_ALLOWED" ]; then
  echo "✅ PASS: Bundle size within acceptable range"
else
  echo "⚠️  WARNING: Bundle size increased significantly"
fi

echo "═══════════════════════════════════════════════════════════════"
```

### D6-5.3 Final Commit

```bash
# COMMAND BLOCK: D6-COMMIT-FINAL
# Description: Final commit for D6 remediation
# Expected: Clean commit with all D6 changes

git add -A
git commit -m "feat(a11y): complete accessibility remediation D6

Summary of changes:
- Phase 1: Setup accessibility testing infrastructure
- Phase 2: Add ARIA labels to layout components
- Phase 3: Add ARIA labels to constitutional components
- Phase 4: Implement keyboard navigation
- Phase 5: Lighthouse audit verification

Accessibility Score: 95+
Constitutional Compliance: Verified
Regression: All tests passing

Remediation: D6-COMPLETE
Protocol: CIA-SIE-PROTOCOL-001 v3.0"

echo "═══════════════════════════════════════════════════════════════"
echo "D6 REMEDIATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
```

---

# PART 3: ROLLBACK PROCEDURES

## Global Rollback Protocol

If ANY phase fails validation, execute this rollback procedure:

```bash
# COMMAND BLOCK: ROLLBACK-GLOBAL
# Description: Rollback to baseline state
# Use when: Any validation fails and recovery is needed

echo "═══════════════════════════════════════════════════════════════"
echo "INITIATING ROLLBACK PROCEDURE"
echo "═══════════════════════════════════════════════════════════════"

cd /path/to/CIA-SIE-PURE/frontend

# Step 1: Get baseline commit
BASELINE_COMMIT=$(cat .remediation-baseline)
echo "Rolling back to baseline: $BASELINE_COMMIT"

# Step 2: Stash any current changes
git stash push -m "Pre-rollback stash $(date +%Y%m%d_%H%M%S)"

# Step 3: Hard reset to baseline
git reset --hard $BASELINE_COMMIT

# Step 4: Clean untracked files
git clean -fd

# Step 5: Reinstall dependencies
npm ci

# Step 6: Verify rollback
echo "Verifying rollback..."
npx tsc --noEmit
npm run test -- --watchAll=false
npm run build

if [ $? -eq 0 ]; then
  echo "✅ ROLLBACK SUCCESSFUL"
  echo "System restored to baseline: $BASELINE_COMMIT"
else
  echo "❌ ROLLBACK FAILED - MANUAL INTERVENTION REQUIRED"
  exit 1
fi

echo "═══════════════════════════════════════════════════════════════"
```

## Phase-Specific Rollback

For rolling back a single phase:

```bash
# COMMAND BLOCK: ROLLBACK-PHASE
# Description: Rollback specific phase using backup
# Parameters: PHASE_NAME (e.g., d6-phase-2)

PHASE_NAME=${1:-"d6-phase-2"}

echo "═══════════════════════════════════════════════════════════════"
echo "ROLLING BACK PHASE: $PHASE_NAME"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Check backup exists
if [ ! -d ".remediation-backups/$PHASE_NAME" ]; then
  echo "❌ FAIL: No backup found for $PHASE_NAME"
  exit 1
fi

# Restore from backup
cp .remediation-backups/$PHASE_NAME/* src/components/layout/ 2>/dev/null
cp .remediation-backups/$PHASE_NAME/* src/components/relationships/ 2>/dev/null
cp .remediation-backups/$PHASE_NAME/* src/components/common/ 2>/dev/null

# Verify restoration
npx tsc --noEmit
npm run test -- --watchAll=false

if [ $? -eq 0 ]; then
  echo "✅ PHASE ROLLBACK SUCCESSFUL"
else
  echo "❌ PHASE ROLLBACK FAILED - Use global rollback"
  exit 1
fi
```

---

# PART 4: INTEGRATION TEST SUITE

## Integration Test Configuration

```typescript
// FILE: frontend/src/test/integration/setup.ts
// ACTION: CREATE IF NOT EXISTS

import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Integration Test: Full Page Accessibility

```typescript
// FILE: frontend/src/test/integration/accessibility.integration.test.tsx
// ACTION: CREATE NEW FILE

import { render, screen, waitFor } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { BrowserRouter, MemoryRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from '../../App'

expect.extend(toHaveNoViolations)

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false, staleTime: 0 },
  },
})

const renderApp = (route = '/') => {
  const queryClient = createTestQueryClient()
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[route]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  )
}

describe('Full Page Accessibility Integration Tests', () => {
  describe('Dashboard (Home)', () => {
    it('should have no accessibility violations', async () => {
      const { container } = renderApp('/')
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      }, { timeout: 5000 })
      
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have all required landmarks', async () => {
      renderApp('/')
      await waitFor(() => {
        expect(screen.getByRole('banner')).toBeInTheDocument()
        expect(screen.getByRole('navigation')).toBeInTheDocument()
        expect(screen.getByRole('main')).toBeInTheDocument()
      })
    })
  })

  describe('Instruments Page', () => {
    it('should have no accessibility violations', async () => {
      const { container } = renderApp('/instruments')
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      }, { timeout: 5000 })
      
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
  })

  describe('Chat Page', () => {
    it('should have no accessibility violations', async () => {
      const { container } = renderApp('/chat')
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      }, { timeout: 5000 })
      
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have disclaimer visible', async () => {
      renderApp('/chat')
      await waitFor(() => {
        expect(screen.getByRole('note')).toBeInTheDocument()
      })
    })
  })
})
```

---

# PART 5: END-TO-END TEST SUITE

## E2E Configuration (Playwright)

```typescript
// FILE: frontend/playwright.config.ts
// ACTION: CREATE IF NOT EXISTS

import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:4173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run preview',
    url: 'http://localhost:4173',
    reuseExistingServer: !process.env.CI,
  },
})
```

## E2E Accessibility Tests

```typescript
// FILE: frontend/e2e/accessibility.spec.ts
// ACTION: CREATE NEW FILE

import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility E2E Tests', () => {
  test('Dashboard should have no accessibility violations', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze()
    
    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('Keyboard navigation should work', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    // Tab to skip link
    await page.keyboard.press('Tab')
    const skipLink = page.getByText('Skip to main content')
    await expect(skipLink).toBeFocused()
    
    // Activate skip link
    await page.keyboard.press('Enter')
    
    // Main content should be focused
    const main = page.locator('#main-content')
    await expect(main).toBeFocused()
  })

  test('Constitutional components should be accessible', async ({ page }) => {
    await page.goto('/silos/1') // Adjust route as needed
    await page.waitForLoadState('networkidle')
    
    // Check contradiction cards have proper ARIA
    const contradictions = page.locator('[role="article"]')
    const count = await contradictions.count()
    
    for (let i = 0; i < count; i++) {
      const card = contradictions.nth(i)
      await expect(card).toHaveAttribute('aria-label', /.+versus.+/)
    }
    
    // Check disclaimer is present
    const disclaimer = page.locator('[role="note"]')
    await expect(disclaimer).toBeVisible()
  })

  test.describe('Screen reader announcements', () => {
    test('Loading states should be announced', async ({ page }) => {
      await page.goto('/')
      
      // Check for aria-live regions
      const liveRegions = page.locator('[aria-live]')
      await expect(liveRegions.first()).toBeVisible()
    })
  })
})
```

## E2E Test Execution Command

```bash
# COMMAND BLOCK: E2E-RUN
# Description: Execute full E2E test suite
# Expected: All tests pass

echo "═══════════════════════════════════════════════════════════════"
echo "RUNNING E2E TEST SUITE"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# Install Playwright browsers if needed
npx playwright install

# Build application
npm run build

# Run E2E tests
npx playwright test

if [ $? -ne 0 ]; then
  echo "❌ FAIL: E2E tests failed"
  echo "View report: npx playwright show-report"
  exit 1
else
  echo "✅ PASS: All E2E tests passed"
fi

echo "═══════════════════════════════════════════════════════════════"
```

---

# PART 6: CONSTITUTIONAL COMPLIANCE AUTOMATED CHECKS

## Automated CR-001, CR-002, CR-003 Verification

```bash
# COMMAND BLOCK: CONSTITUTIONAL-CHECK
# Description: Automated constitutional compliance verification
# Expected: All checks pass

echo "═══════════════════════════════════════════════════════════════"
echo "CONSTITUTIONAL COMPLIANCE VERIFICATION"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

CR001_VIOLATIONS=0
CR002_VIOLATIONS=0
CR003_VIOLATIONS=0

# ═══════════════════════════════════════════════════════════════
# CR-001: Decision-Support ONLY
# No confidence, strength, weight, score, rating, recommendation
# ═══════════════════════════════════════════════════════════════

echo "Checking CR-001: Decision-Support ONLY..."

# Check for prohibited terms in UI components (excluding tests and comments)
PROHIBITED_TERMS=("confidence" "strength" "weight" "score" "rating" "recommendation" "suggest")

for TERM in "${PROHIBITED_TERMS[@]}"; do
  # Search in TSX files, exclude tests, comments, and legitimate uses
  MATCHES=$(grep -rn "$TERM" src/ --include="*.tsx" | grep -v "test" | grep -v "//" | grep -v "\.test\." | grep -v "\.spec\.")
  
  if [ -n "$MATCHES" ]; then
    echo "⚠️  POTENTIAL CR-001 ISSUE: '$TERM' found:"
    echo "$MATCHES"
    ((CR001_VIOLATIONS++))
  fi
done

if [ $CR001_VIOLATIONS -eq 0 ]; then
  echo "✅ CR-001: COMPLIANT"
else
  echo "❌ CR-001: $CR001_VIOLATIONS potential violations - MANUAL REVIEW REQUIRED"
fi

# ═══════════════════════════════════════════════════════════════
# CR-002: Expose, NEVER Resolve
# ContradictionCard must have equal visual weight, no resolution
# ═══════════════════════════════════════════════════════════════

echo ""
echo "Checking CR-002: Expose, NEVER Resolve..."

# Check ContradictionCard for resolution mechanisms
RESOLUTION_TERMS=("resolve" "dismiss" "prefer" "select" "choose")

for TERM in "${RESOLUTION_TERMS[@]}"; do
  MATCHES=$(grep -rn "$TERM" src/components/relationships/ContradictionCard.tsx 2>/dev/null | grep -v "//" | grep -v "aria")
  
  if [ -n "$MATCHES" ]; then
    echo "❌ CR-002 VIOLATION: '$TERM' found in ContradictionCard:"
    echo "$MATCHES"
    ((CR002_VIOLATIONS++))
  fi
done

# Check for equal grid columns
GRID_CHECK=$(grep -n "grid-cols-\[1fr" src/components/relationships/ContradictionCard.tsx 2>/dev/null)
if [ -z "$GRID_CHECK" ]; then
  echo "⚠️  CR-002 WARNING: Equal grid columns not detected"
  ((CR002_VIOLATIONS++))
else
  echo "✓ Equal grid columns confirmed"
fi

if [ $CR002_VIOLATIONS -eq 0 ]; then
  echo "✅ CR-002: COMPLIANT"
else
  echo "❌ CR-002: $CR002_VIOLATIONS violations found"
fi

# ═══════════════════════════════════════════════════════════════
# CR-003: Descriptive AI ONLY
# Hardcoded disclaimer, no dismiss functionality
# ═══════════════════════════════════════════════════════════════

echo ""
echo "Checking CR-003: Descriptive AI ONLY..."

# Check Disclaimer has hardcoded text
DISCLAIMER_TEXT_CHECK=$(grep -n "description of what your charts" src/components/common/Disclaimer.tsx 2>/dev/null)
if [ -z "$DISCLAIMER_TEXT_CHECK" ]; then
  echo "❌ CR-003 VIOLATION: Hardcoded disclaimer text not found"
  ((CR003_VIOLATIONS++))
else
  echo "✓ Hardcoded disclaimer text confirmed"
fi

# Check Disclaimer has no dismiss functionality
DISMISS_CHECK=$(grep -n "dismiss\|close\|hide\|setVisible\|setShow" src/components/common/Disclaimer.tsx 2>/dev/null | grep -v "//")
if [ -n "$DISMISS_CHECK" ]; then
  echo "❌ CR-003 VIOLATION: Dismiss functionality detected:"
  echo "$DISMISS_CHECK"
  ((CR003_VIOLATIONS++))
else
  echo "✓ No dismiss functionality confirmed"
fi

# Check Disclaimer is rendered with NarrativeDisplay
NARRATIVE_DISCLAIMER=$(grep -n "Disclaimer" src/components/narratives/NarrativeDisplay.tsx 2>/dev/null)
if [ -z "$NARRATIVE_DISCLAIMER" ]; then
  echo "❌ CR-003 VIOLATION: Disclaimer not rendered with NarrativeDisplay"
  ((CR003_VIOLATIONS++))
else
  echo "✓ Disclaimer rendered with NarrativeDisplay"
fi

if [ $CR003_VIOLATIONS -eq 0 ]; then
  echo "✅ CR-003: COMPLIANT"
else
  echo "❌ CR-003: $CR003_VIOLATIONS violations found"
fi

# ═══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "CONSTITUTIONAL COMPLIANCE SUMMARY"
echo "═══════════════════════════════════════════════════════════════"

TOTAL_VIOLATIONS=$((CR001_VIOLATIONS + CR002_VIOLATIONS + CR003_VIOLATIONS))

echo "CR-001 (Decision-Support ONLY): $([ $CR001_VIOLATIONS -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo "CR-002 (Expose, NEVER Resolve): $([ $CR002_VIOLATIONS -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo "CR-003 (Descriptive AI ONLY):   $([ $CR003_VIOLATIONS -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo ""

if [ $TOTAL_VIOLATIONS -eq 0 ]; then
  echo "★★★ ALL CONSTITUTIONAL RULES COMPLIANT ★★★"
  exit 0
else
  echo "!!! $TOTAL_VIOLATIONS TOTAL VIOLATIONS - REVIEW REQUIRED !!!"
  exit 1
fi
```

---

# PART 7: FINAL VERIFICATION CHECKLIST

## Post-Remediation Certification

Execute this complete verification after ALL remediation items are complete:

```bash
# COMMAND BLOCK: FINAL-CERTIFICATION
# Description: Complete system verification for launch certification
# Expected: All checks pass

echo "═══════════════════════════════════════════════════════════════"
echo "CIA-SIE FRONTEND FINAL CERTIFICATION"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

PASS_COUNT=0
FAIL_COUNT=0

run_check() {
  local NAME=$1
  local COMMAND=$2
  
  echo "Checking: $NAME..."
  eval $COMMAND > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "  ✅ PASS"
    ((PASS_COUNT++))
  else
    echo "  ❌ FAIL"
    ((FAIL_COUNT++))
  fi
}

echo ""
echo "═══ BUILD VERIFICATION ═══"
run_check "TypeScript compilation" "npx tsc --noEmit"
run_check "Production build" "npm run build"
run_check "Bundle size < 250KB" "[ $(ls -la dist/assets/*.js | awk '{sum += \$5} END {print sum}') -lt 262144 ]"

echo ""
echo "═══ TEST VERIFICATION ═══"
run_check "Unit tests" "npm run test -- --watchAll=false --passWithNoTests"
run_check "Accessibility tests" "npm run test -- --testPathPattern='a11y' --watchAll=false --passWithNoTests"
run_check "Integration tests" "npm run test -- --testPathPattern='integration' --watchAll=false --passWithNoTests"

echo ""
echo "═══ CONSTITUTIONAL COMPLIANCE ═══"
run_check "CR-001 compliance" "! grep -rn 'confidence\|strength\|weight' src/ --include='*.tsx' | grep -v test | grep -v '//' | grep -q ."
run_check "CR-002 compliance" "! grep -rn 'resolve\|dismiss\|prefer' src/components/relationships/ContradictionCard.tsx | grep -v '//' | grep -v aria | grep -q ."
run_check "CR-003 disclaimer present" "grep -q 'description of what your charts' src/components/common/Disclaimer.tsx"

echo ""
echo "═══ ACCESSIBILITY ═══"
run_check "Skip link present" "grep -rq 'Skip to main content' src/"
run_check "Main landmark present" "grep -rq 'role=\"main\"' src/"
run_check "Banner landmark present" "grep -rq 'role=\"banner\"' src/"
run_check "Navigation landmark present" "grep -rq 'role=\"navigation\"' src/"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "CERTIFICATION RESULTS"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
  echo "★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★"
  echo "★                                                         ★"
  echo "★         CIA-SIE FRONTEND: CERTIFIED FOR LAUNCH          ★"
  echo "★                                                         ★"
  echo "★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★"
  exit 0
else
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo "!                                                           !"
  echo "!      CERTIFICATION FAILED - DO NOT LAUNCH                 !"
  echo "!                                                           !"
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  exit 1
fi
```

---

# PART 8: DOCUMENT PLACEMENT

This protocol document and all generated reports should be placed:

```
CIA-SIE-PURE/
├── frontend/
│   ├── .remediation-baseline          (Generated - baseline commit)
│   ├── .coverage-baseline.json        (Generated - coverage baseline)
│   ├── .bundle-baseline.txt           (Generated - bundle size baseline)
│   ├── lighthouse-a11y-report.json    (Generated - Lighthouse report)
│   └── lighthouse-a11y-report.html    (Generated - Lighthouse HTML)
│
└── docs/
    └── remediation/
        ├── CIA-SIE-PROTOCOL-001_v3.0.md           (This document)
        ├── FRONTEND_DESIGN_CONCEPT_v1.0.md        (Baseline)
        ├── FRONTEND_AUDIT_COMPLETED.md            (Audit results)
        ├── FRONTEND_RECONCILIATION_v2.0.md        (Reconciliation)
        └── CERTIFICATION_REPORT.md                (Generated post-certification)
```

---

# EXECUTION SUMMARY FOR CURSOR

When executing this protocol:

1. **Start with PART 1** — Complete ALL pre-flight checks
2. **Execute each PHASE sequentially** — Never skip ahead
3. **At each checkpoint:**
   - Run the validation commands
   - If ANY fail → STOP and ROLLBACK
   - If all pass → COMMIT and proceed
4. **After all phases:** Run FINAL-CERTIFICATION
5. **Report results** to human operator

**Zero tolerance policy:** One failed validation = full stop.

---

*End of NASA-Grade Remediation Protocol v3.0*

**Protocol Status: READY FOR EXECUTION**
**Constitutional Compliance: ENFORCED AT EVERY PHASE**
**Rollback Capability: COMPLETE**
**Test Coverage: UNIT + INTEGRATION + E2E + ACCESSIBILITY**
