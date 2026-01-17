# CIA-SIE REMEDIATION PROTOCOL v4.0

## NASA-Grade Human-in-the-Loop Change Management

---

| Document Metadata | Value |
|-------------------|-------|
| **Document ID** | CIA-SIE-PROTOCOL-002 |
| **Version** | 4.0.0 |
| **Date** | January 4, 2026 |
| **Type** | Human-in-the-Loop Remediation Protocol |
| **Author** | Claude Opus 4.5 (claude.ai) |
| **Classification** | MISSION CRITICAL |
| **Execution Model** | HITL (Human-in-the-Loop) |
| **Decision Authority** | Human Operator (Neville) |
| **Execution Agent** | Cursor |

---

## PROTOCOL PHILOSOPHY

### The Three Pillars

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   1. ANALYZE BEFORE ACT                                         │
│      Cursor must study the codebase and provide reasoned        │
│      recommendation BEFORE any code is touched                  │
│                                                                 │
│   2. HUMAN DECIDES                                              │
│      No execution proceeds without explicit human approval      │
│      at designated HALT gates                                   │
│                                                                 │
│   3. CONFIRM COMPLETION                                         │
│      Every phase ends with unambiguous finality statement       │
│      and verification that objectives were achieved             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Execution Flow

```
┌──────────────────┐
│ IMPACT ANALYSIS  │ ← Cursor analyzes: Should we do this?
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ ══ HALT GATE ══  │ ← Human reviews analysis, decides: PROCEED / SKIP / MODIFY
└────────┬─────────┘
         │ (Human says PROCEED)
         ▼
┌──────────────────┐
│ PRE-VALIDATION   │ ← Cursor verifies starting state
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ ══ HALT GATE ══  │ ← Human confirms: Ready to modify code?
└────────┬─────────┘
         │ (Human says PROCEED)
         ▼
┌──────────────────┐
│ CODE CHANGES     │ ← Cursor implements changes
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ POST-VALIDATION  │ ← Cursor runs all tests
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ ══ HALT GATE ══  │ ← Human reviews results: Accept / Rollback?
└────────┬─────────┘
         │ (Human says ACCEPT)
         ▼
┌──────────────────┐
│ COMMIT & CONFIRM │ ← Cursor commits, issues FINALITY STATEMENT
└────────┬─────────┘
         │
         ▼
    [Next Phase]
```

---

## CURSOR BEHAVIORAL REQUIREMENTS

### When Executing This Protocol, Cursor MUST:

1. **Never proceed past a HALT GATE without explicit human instruction**
   - Wait for: "PROCEED", "CONTINUE", "GO", "YES", or equivalent
   - If human says: "SKIP", "NO", "STOP" → Move to next item or halt entirely
   - If human says: "MODIFY" → Discuss modifications before proceeding

2. **Provide genuine analysis, not rubber-stamp approval**
   - Actually examine the codebase
   - Consider ripple effects specific to CIA-SIE
   - Recommend AGAINST remediation if analysis suggests it's harmful

3. **Issue clear FINALITY STATEMENTS**
   - Use exact phrasing specified in protocol
   - Never issue finality until ALL validations pass
   - If validations fail, issue FAILURE STATEMENT instead

4. **Maintain audit trail**
   - Document every decision point
   - Record human responses at each gate
   - Note any deviations from protocol

---

## STANDARD PHRASES

### Cursor Uses These Exact Phrases:

**At HALT GATES:**
```
═══════════════════════════════════════════════════════════════════
▶ HALT GATE: [Gate Name]
═══════════════════════════════════════════════════════════════════

[Analysis/Status Summary]

Awaiting your instruction:
• PROCEED - Continue to next step
• SKIP - Skip this item, move to next
• ROLLBACK - Undo changes and stop
• DISCUSS - I have questions before deciding

Your decision:
```

**FINALITY STATEMENTS:**
```
═══════════════════════════════════════════════════════════════════
✓ FINALITY CONFIRMATION: [Phase/Item Name]
═══════════════════════════════════════════════════════════════════

Status: COMPLETE
All validations: PASSED
Changes committed: YES
Rollback point: [commit hash]

This phase is DONE. Ready for next phase on your command.
═══════════════════════════════════════════════════════════════════
```

**FAILURE STATEMENTS:**
```
═══════════════════════════════════════════════════════════════════
✗ FAILURE: [Phase/Item Name]
═══════════════════════════════════════════════════════════════════

Status: FAILED
Failure point: [specific validation that failed]
Error details: [error message]

Recommended action: ROLLBACK to [commit hash]

Awaiting your instruction:
• ROLLBACK - Restore previous state
• RETRY - Attempt fix and retry
• INVESTIGATE - Examine failure in detail

Your decision:
```

---

# PART 1: PRE-FLIGHT SEQUENCE

## 1.1 Repository Analysis

Before any remediation work, Cursor must analyze the current state of the entire codebase.

### Cursor Executes:

```bash
# ANALYSIS BLOCK: REPO-SCAN-001
# Purpose: Understand current codebase state

echo "═══════════════════════════════════════════════════════════════"
echo "REPOSITORY ANALYSIS"
echo "═══════════════════════════════════════════════════════════════"

cd /path/to/CIA-SIE-PURE

# Frontend structure
echo "FRONTEND STRUCTURE:"
find frontend/src -type f -name "*.tsx" | head -50
echo ""
echo "Frontend component count: $(find frontend/src -name '*.tsx' | wc -l)"
echo "Frontend hook count: $(find frontend/src/hooks -name '*.ts' 2>/dev/null | wc -l)"
echo "Frontend test count: $(find frontend/src -name '*.test.*' | wc -l)"

# Backend structure
echo ""
echo "BACKEND STRUCTURE:"
find backend -type f -name "*.py" | head -50
echo ""
echo "Backend file count: $(find backend -name '*.py' | wc -l)"
echo "Backend test count: $(find backend -name 'test_*.py' | wc -l)"

# Dependencies
echo ""
echo "FRONTEND DEPENDENCIES:"
cat frontend/package.json | grep -A 50 '"dependencies"' | head -30

echo ""
echo "BACKEND DEPENDENCIES:"
cat backend/requirements.txt 2>/dev/null | head -30

# Git status
echo ""
echo "GIT STATUS:"
git log --oneline -10
git status --short
```

### Cursor Reports:

After running the analysis, Cursor provides a summary:

```
═══════════════════════════════════════════════════════════════════
REPOSITORY ANALYSIS COMPLETE
═══════════════════════════════════════════════════════════════════

Frontend:
• Components: [X] files
• Hooks: [X] files
• Tests: [X] files
• Key patterns observed: [observations]

Backend:
• Modules: [X] files
• Tests: [X] files
• API structure: [observations]

Integration points identified:
• [List of frontend-backend connections]

Potential risk areas:
• [Any concerns noted]

═══════════════════════════════════════════════════════════════════
▶ HALT GATE: PRE-FLIGHT ANALYSIS REVIEW
═══════════════════════════════════════════════════════════════════

I have completed the initial repository analysis.

Awaiting your instruction:
• PROCEED - Continue to environment validation
• DISCUSS - Review specific areas before continuing

Your decision:
```

---

## 1.2 Environment Validation

### Cursor Executes:

```bash
# VALIDATION BLOCK: ENV-CHECK-001

echo "═══════════════════════════════════════════════════════════════"
echo "ENVIRONMENT VALIDATION"
echo "═══════════════════════════════════════════════════════════════"

# [All checks from v3.0 Protocol Part 1]
# Node version, npm, dependencies, TypeScript, tests, build, backend health
```

### Cursor Reports:

```
═══════════════════════════════════════════════════════════════════
ENVIRONMENT VALIDATION RESULTS
═══════════════════════════════════════════════════════════════════

| Check | Status |
|-------|--------|
| Node version | ✅ v20.x |
| npm install | ✅ Success |
| TypeScript compilation | ✅ Clean |
| Unit tests | ✅ [X] passed |
| Production build | ✅ Success |
| Backend health | ✅ Responding |

Baseline recorded:
• Commit: [hash]
• Coverage: [X]%
• Bundle size: [X] KB

═══════════════════════════════════════════════════════════════════
▶ HALT GATE: ENVIRONMENT READY
═══════════════════════════════════════════════════════════════════

Environment is validated and baselines are recorded.
Ready to create remediation branch and begin work.

Awaiting your instruction:
• PROCEED - Create remediation branch
• STOP - Do not proceed (environment issues to resolve)

Your decision:
```

---

## 1.3 Remediation Branch Creation

### Cursor Executes:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REMEDIATION_BRANCH="remediation/hitl-protocol-$TIMESTAMP"
git checkout -b "$REMEDIATION_BRANCH"
```

### Cursor Reports:

```
═══════════════════════════════════════════════════════════════════
✓ FINALITY CONFIRMATION: PRE-FLIGHT SEQUENCE
═══════════════════════════════════════════════════════════════════

Status: COMPLETE
Remediation branch: remediation/hitl-protocol-[timestamp]
Baseline commit: [hash]
All systems: READY

Pre-flight sequence is DONE. 
Ready to begin remediation item analysis on your command.
═══════════════════════════════════════════════════════════════════
```

---

# PART 2: REMEDIATION IMPACT ANALYSIS FRAMEWORK

## For Each Remediation Item, Cursor Must:

### Step 1: Study the Requirement

Read and understand what the remediation item asks for.

### Step 2: Examine Existing Code

Actually look at the relevant files in both frontend AND backend:

```bash
# Example for D6 (Accessibility)
# Cursor examines:

# Frontend layout components
cat frontend/src/components/layout/Header.tsx
cat frontend/src/components/layout/Sidebar.tsx
cat frontend/src/components/layout/AppShell.tsx

# Constitutional components
cat frontend/src/components/relationships/ContradictionCard.tsx
cat frontend/src/components/common/Disclaimer.tsx

# Check for existing ARIA usage
grep -rn "aria-" frontend/src/
grep -rn "role=" frontend/src/

# Check backend API responses (do they include accessibility-relevant data?)
cat backend/app/api/routes/*.py | head -100
```

### Step 3: Analyze Impact

Consider:
- Does this change align with the existing architecture?
- Will it conflict with any existing patterns?
- Does it affect backend contracts?
- What's the actual benefit vs. effort?
- Are there risks specific to CIA-SIE?

### Step 4: Formulate Recommendation

Provide one of:
- **RECOMMEND: PROCEED** — Clear benefit, low risk
- **RECOMMEND: PROCEED WITH CAUTION** — Benefit exists but risks need management
- **RECOMMEND: DEFER** — Not critical now, better done later
- **RECOMMEND: SKIP** — Costs outweigh benefits for this system
- **RECOMMEND: MODIFY** — The remediation should be adjusted

### Step 5: Present to Human

Issue analysis report and wait at HALT GATE.

---

# PART 3: REMEDIATION ITEMS WITH HITL GATES

---

## REMEDIATION ITEM D6: ACCESSIBILITY ENHANCEMENTS

### D6-ANALYSIS: Impact Study

**Cursor Must Execute:**

```bash
# ANALYSIS BLOCK: D6-IMPACT-001
# Purpose: Analyze accessibility remediation impact on CIA-SIE

echo "═══════════════════════════════════════════════════════════════"
echo "D6 IMPACT ANALYSIS: ACCESSIBILITY ENHANCEMENTS"
echo "═══════════════════════════════════════════════════════════════"

cd frontend

# 1. Check current ARIA usage
echo "Current ARIA attribute usage:"
grep -rn "aria-" src/ --include="*.tsx" | wc -l
echo "Files with ARIA:"
grep -rl "aria-" src/ --include="*.tsx"

# 2. Check current role usage
echo ""
echo "Current role attribute usage:"
grep -rn "role=" src/ --include="*.tsx" | wc -l

# 3. Check semantic HTML usage
echo ""
echo "Semantic HTML elements used:"
grep -rE "<(header|main|nav|aside|article|section|footer)" src/ --include="*.tsx" | wc -l

# 4. Check for existing keyboard handlers
echo ""
echo "Keyboard event handlers:"
grep -rn "onKeyDown\|onKeyUp\|onKeyPress" src/ --include="*.tsx" | wc -l

# 5. Check constitutional components (critical for CR compliance)
echo ""
echo "Constitutional component analysis:"
echo "ContradictionCard:"
cat src/components/relationships/ContradictionCard.tsx 2>/dev/null | head -60
echo ""
echo "Disclaimer:"
cat src/components/common/Disclaimer.tsx 2>/dev/null

# 6. Check test infrastructure
echo ""
echo "Existing test setup:"
ls -la src/test/ 2>/dev/null
cat jest.config.* 2>/dev/null | head -30

# 7. Check if accessibility packages exist
echo ""
echo "Accessibility packages in dependencies:"
cat package.json | grep -i "axe\|a11y\|accessibility"
```

**Cursor Must Then Provide This Analysis Report:**

```
═══════════════════════════════════════════════════════════════════
D6 IMPACT ANALYSIS REPORT: ACCESSIBILITY ENHANCEMENTS
═══════════════════════════════════════════════════════════════════

CURRENT STATE ASSESSMENT:
─────────────────────────

Existing ARIA Implementation:
• ARIA attributes found: [X] instances across [Y] files
• Role attributes found: [X] instances
• Semantic HTML usage: [Good/Limited/Poor]

Observation: [Cursor's genuine assessment of current accessibility state]

CONSTITUTIONAL COMPONENT REVIEW:
────────────────────────────────

ContradictionCard (CR-002 Critical):
• Current structure: [Description]
• Accessibility gaps: [List]
• Risk of modification: [Assessment]
• Will ARIA additions affect CR-002 compliance? [Yes/No + explanation]

Disclaimer (CR-003 Critical):
• Current structure: [Description]
• Accessibility gaps: [List]
• Risk of modification: [Assessment]
• Will ARIA additions affect CR-003 compliance? [Yes/No + explanation]

BACKEND IMPACT:
───────────────

• Does accessibility require backend changes? [Yes/No]
• API contracts affected: [None/List]
• Data structure changes needed: [None/List]

BENEFIT ANALYSIS:
─────────────────

Benefits of implementing D6:
1. [Specific benefit for CIA-SIE]
2. [Specific benefit for CIA-SIE]
3. [Specific benefit for CIA-SIE]

Quantifiable impact:
• Users affected: [Estimate - e.g., "X% of users with assistive technology"]
• Compliance achieved: [WCAG 2.1 AA]
• Legal risk mitigation: [Assessment]

RISK ANALYSIS:
──────────────

Risks of implementing D6:
1. [Specific risk] — Mitigation: [How to address]
2. [Specific risk] — Mitigation: [How to address]

Risks of NOT implementing D6:
1. [Specific risk]
2. [Specific risk]

EFFORT VS. VALUE:
─────────────────

Estimated effort: [X] days
Value delivered: [High/Medium/Low]
Ratio assessment: [Favorable/Neutral/Unfavorable]

INTERACTION WITH OTHER REMEDIATIONS:
────────────────────────────────────

• Dependencies: [Does D6 depend on other items?]
• Blockers: [Does D6 block other items?]
• Synergies: [Does D6 make other items easier?]

═══════════════════════════════════════════════════════════════════
MY RECOMMENDATION
═══════════════════════════════════════════════════════════════════

RECOMMEND: [PROCEED / PROCEED WITH CAUTION / DEFER / SKIP / MODIFY]

Reasoning:
[Cursor's genuine, specific reasoning based on the analysis above]

If PROCEED WITH CAUTION or MODIFY, specific concerns:
[List specific things to watch for or changes to the approach]

═══════════════════════════════════════════════════════════════════
▶ HALT GATE: D6 IMPLEMENTATION DECISION
═══════════════════════════════════════════════════════════════════

I have completed the impact analysis for D6 (Accessibility).

Awaiting your instruction:
• PROCEED - Accept recommendation and begin implementation
• SKIP - Skip D6, move to next remediation item
• MODIFY - Discuss changes to the approach
• DISCUSS - I have questions about this analysis

Your decision:
```

---

### D6-PHASE-1: Setup Accessibility Testing Infrastructure

**(Only executes if Human said PROCEED at previous HALT GATE)**

#### D6-1.1 Pre-Implementation Gate

```
═══════════════════════════════════════════════════════════════════
▶ HALT GATE: D6-PHASE-1 PRE-IMPLEMENTATION
═══════════════════════════════════════════════════════════════════

About to implement: Accessibility testing infrastructure setup

Changes to be made:
1. Install @axe-core/react, jest-axe, @testing-library/jest-dom
2. Create src/test/setupAccessibility.ts
3. Update jest.config.ts

Files affected:
• package.json (dependency addition)
• package-lock.json (auto-generated)
• jest.config.ts (configuration change)
• src/test/setupAccessibility.ts (new file)

Estimated time: 10-15 minutes
Rollback complexity: LOW (simple npm uninstall + file deletion)

Awaiting your instruction:
• PROCEED - Make these changes
• SKIP - Skip this phase
• DISCUSS - Review changes in more detail

Your decision:
```

#### D6-1.2 Implementation

**(Only executes if Human said PROCEED)**

Cursor executes all code changes from v3.0 protocol.

#### D6-1.3 Post-Implementation Validation

```bash
# Cursor runs all validation commands
npx tsc --noEmit
npm run test -- --watchAll=false
npm run build
```

#### D6-1.4 Validation Results Gate

```
═══════════════════════════════════════════════════════════════════
▶ HALT GATE: D6-PHASE-1 VALIDATION RESULTS
═══════════════════════════════════════════════════════════════════

Implementation complete. Validation results:

| Check | Result |
|-------|--------|
| Packages installed | ✅ @axe-core/react, jest-axe, @testing-library/jest-dom |
| Setup file created | ✅ src/test/setupAccessibility.ts |
| TypeScript compilation | ✅ Clean |
| Existing tests | ✅ All passing |
| Build | ✅ Success |

All validations PASSED.

Awaiting your instruction:
• ACCEPT - Commit these changes and proceed to next phase
• ROLLBACK - Undo changes and stop
• REVIEW - Show me specific files/changes before accepting

Your decision:
```

#### D6-1.5 Finality

**(Only executes if Human said ACCEPT)**

```bash
git add -A
git commit -m "feat(a11y): setup accessibility testing infrastructure [D6-PHASE-1]"
```

```
═══════════════════════════════════════════════════════════════════
✓ FINALITY CONFIRMATION: D6-PHASE-1
═══════════════════════════════════════════════════════════════════

Status: COMPLETE
Commit: [hash]
Changes: 4 files (2 modified, 2 new)

Phase D6-PHASE-1 is DONE.
Ready for D6-PHASE-2 on your command.

Awaiting your instruction:
• PROCEED - Continue to D6-PHASE-2
• PAUSE - Stop here, resume later
• SKIP-TO - Jump to different remediation item

Your decision:
═══════════════════════════════════════════════════════════════════
```

---

### D6-PHASE-2: Add ARIA Labels to Layout Components

**(Only executes if Human said PROCEED)**

#### D6-2.1 Pre-Implementation Analysis

```
═══════════════════════════════════════════════════════════════════
▶ HALT GATE: D6-PHASE-2 PRE-IMPLEMENTATION
═══════════════════════════════════════════════════════════════════

About to implement: ARIA labels for layout components

Current state of target files:
─────────────────────────────

Header.tsx (41 lines):
• Current: <header className="...">
• Proposed: <header role="banner" aria-label="CIA-SIE main header" className="...">
• Risk: NONE — additive change only

Sidebar.tsx (66 lines):
• Current: <aside className="...">
• Proposed: <aside role="navigation" aria-label="Main navigation sidebar" className="...">
• Risk: NONE — additive change only
• Note: Contains mini constitutional banner (lines 51-62) — will preserve

AppShell.tsx (22 lines):
• Current: <div className="p-6">{children}</div>
• Proposed: <main id="main-content" role="main" aria-label="Main content" tabIndex={-1}>{children}</main>
• Risk: LOW — semantic element change (div → main)

Backend impact: NONE
Constitutional compliance impact: NONE (layout only, not constitutional components)

Test files to be created:
• src/components/layout/__tests__/Layout.a11y.test.tsx

Awaiting your instruction:
• PROCEED - Make these changes
• SKIP - Skip this phase
• DISCUSS - Review in more detail

Your decision:
```

#### D6-2.2 through D6-2.5

[Same pattern: Implementation → Validation → Results Gate → Human Decision → Finality]

---

### D6-PHASE-3: Constitutional Components (CRITICAL)

#### D6-3.0 Special Warning Gate

```
═══════════════════════════════════════════════════════════════════
⚠️  CRITICAL GATE: CONSTITUTIONAL COMPONENT MODIFICATION
═══════════════════════════════════════════════════════════════════

WARNING: This phase modifies CONSTITUTIONAL COMPONENTS

Components affected:
• ContradictionCard.tsx — CR-002 CRITICAL
• Disclaimer.tsx — CR-003 CRITICAL

These components enforce the three constitutional rules of CIA-SIE:
• CR-001: Decision-Support ONLY
• CR-002: Expose, NEVER Resolve
• CR-003: Descriptive AI ONLY

Changes proposed are ADDITIVE ONLY (ARIA attributes) and will:
• NOT add any resolution mechanisms to ContradictionCard
• NOT add any dismiss functionality to Disclaimer
• NOT change any business logic
• NOT affect visual presentation

However, due to the critical nature of these components, I recommend:
1. Extra scrutiny of changes
2. Post-implementation constitutional compliance verification
3. Manual review of rendered output

Awaiting your instruction:
• PROCEED - I understand the risks, continue with caution
• SKIP - Skip constitutional component modifications
• REVIEW-DETAILED - Show me exact line-by-line changes first

Your decision:
```

#### D6-3.1 Detailed Change Preview (if Human requests REVIEW-DETAILED)

```
═══════════════════════════════════════════════════════════════════
DETAILED CHANGE PREVIEW: ContradictionCard.tsx
═══════════════════════════════════════════════════════════════════

CURRENT CODE (lines 15-35):
───────────────────────────
export const ContradictionCard = ({ contradiction }: Props) => {
  const sideClassName = 'rounded-lg bg-surface-secondary p-4 text-center'
  
  return (
    <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">
      <div className={sideClassName}>
        <p className="font-medium">{contradiction.chart_a_name}</p>
        <DirectionBadge direction={contradiction.chart_a_direction} />
      </div>
      
      <span className="text-muted font-bold">VS</span>
      
      <div className={sideClassName}>
        <p className="font-medium">{contradiction.chart_b_name}</p>
        <DirectionBadge direction={contradiction.chart_b_direction} />
      </div>
    </div>
  )
}

PROPOSED CODE (changes highlighted):
────────────────────────────────────
export const ContradictionCard = ({ contradiction }: Props) => {
  const sideClassName = 'rounded-lg bg-surface-secondary p-4 text-center'
  
  return (
    <article                                                          // CHANGED: div → article
      className="grid grid-cols-[1fr,auto,1fr] items-center gap-4"
      role="article"                                                  // ADDED
      aria-label={`Contradiction: ${contradiction.chart_a_name} versus ${contradiction.chart_b_name}`}  // ADDED
    >
      <div 
        className={sideClassName}
        role="group"                                                  // ADDED
        aria-label={`${contradiction.chart_a_name} shows ${contradiction.chart_a_direction}`}  // ADDED
      >
        <p className="font-medium">{contradiction.chart_a_name}</p>
        <DirectionBadge direction={contradiction.chart_a_direction} />
      </div>
      
      <span className="text-muted font-bold" aria-hidden="true">VS</span>  // ADDED: aria-hidden
      
      <div 
        className={sideClassName}
        role="group"                                                  // ADDED
        aria-label={`${contradiction.chart_b_name} shows ${contradiction.chart_b_direction}`}  // ADDED
      >
        <p className="font-medium">{contradiction.chart_b_name}</p>
        <DirectionBadge direction={contradiction.chart_b_direction} />
      </div>
    </article>                                                        // CHANGED: div → article
  )
}

CR-002 COMPLIANCE VERIFICATION:
───────────────────────────────
✓ Grid remains grid-cols-[1fr,auto,1fr] — EQUAL WEIGHT PRESERVED
✓ Both sides use identical sideClassName — EQUAL STYLING PRESERVED
✓ No "resolve", "dismiss", "prefer" added — NO RESOLUTION MECHANISM
✓ No onClick handlers added — NO INTERACTION CHANGE

Awaiting your instruction:
• PROCEED - Changes look safe, continue
• ABORT - Do not modify this component
• MODIFY - Suggest different approach

Your decision:
```

---

### D6-PHASE-4 and D6-PHASE-5

[Same HITL pattern continues for all phases]

---

### D6-COMPLETION: Final Constitutional Verification

```
═══════════════════════════════════════════════════════════════════
▶ HALT GATE: D6 FINAL CONSTITUTIONAL VERIFICATION
═══════════════════════════════════════════════════════════════════

Before certifying D6 complete, executing constitutional compliance check:

[Cursor runs CONSTITUTIONAL-CHECK from v3.0 protocol]

Results:
────────
CR-001 (Decision-Support ONLY): ✅ PASS — 0 violations
CR-002 (Expose, NEVER Resolve): ✅ PASS — 0 violations
CR-003 (Descriptive AI ONLY): ✅ PASS — 0 violations

Accessibility improvements verified:
────────────────────────────────────
• Lighthouse score: 97 (target: 95+) ✅
• All ARIA tests passing: ✅
• Keyboard navigation working: ✅
• Skip link functional: ✅

═══════════════════════════════════════════════════════════════════

All validations PASSED.
Constitutional compliance VERIFIED.

Awaiting your instruction:
• CERTIFY - Confirm D6 remediation complete
• AUDIT - Perform additional manual verification
• ROLLBACK - Undo all D6 changes

Your decision:
```

### D6-FINALITY

**(Only executes if Human said CERTIFY)**

```
═══════════════════════════════════════════════════════════════════
✓ FINALITY CONFIRMATION: D6 ACCESSIBILITY ENHANCEMENTS
═══════════════════════════════════════════════════════════════════

REMEDIATION D6: COMPLETE

Summary of changes:
• Phase 1: Accessibility testing infrastructure ✓
• Phase 2: ARIA labels on layout components ✓
• Phase 3: ARIA labels on constitutional components ✓
• Phase 4: Keyboard navigation ✓
• Phase 5: Lighthouse verification ✓

Commits made: 5
Total files changed: 18
Tests added: 12
Constitutional compliance: VERIFIED

Lighthouse Accessibility Score: 97/100

This remediation is DONE and CERTIFIED.

═══════════════════════════════════════════════════════════════════

Awaiting your instruction for next remediation item:
• NEXT - Proceed to D1 (ChartsReferencePage)
• SKIP-TO [ID] - Jump to specific item
• PAUSE - Stop remediation session
• COMPLETE - End remediation (no more items)

Your decision:
═══════════════════════════════════════════════════════════════════
```

---

# PART 4: REMEDIATION ITEM ANALYSIS TEMPLATES

## For Each Remaining Item, Cursor Uses This Template:

### [ITEM-ID]: [Item Name]

#### Analysis Phase

```
═══════════════════════════════════════════════════════════════════
[ITEM-ID] IMPACT ANALYSIS: [Item Name]
═══════════════════════════════════════════════════════════════════

WHAT IS BEING REMEDIATED:
─────────────────────────
[Description from design concept]

CURRENT STATE IN CODEBASE:
──────────────────────────
[Cursor's actual examination of relevant files]

Frontend files examined:
• [file1]: [observations]
• [file2]: [observations]

Backend files examined (if relevant):
• [file1]: [observations]

ALIGNMENT WITH EXISTING ARCHITECTURE:
─────────────────────────────────────
[Does this fit naturally? Conflicts?]

BENEFIT ANALYSIS:
─────────────────
For CIA-SIE specifically:
1. [Benefit]
2. [Benefit]

RISK ANALYSIS:
──────────────
1. [Risk] — Mitigation: [approach]

EFFORT ESTIMATE:
────────────────
[X hours/days]

RECOMMENDATION:
───────────────
[PROCEED / PROCEED WITH CAUTION / DEFER / SKIP / MODIFY]

Reasoning: [Specific to THIS codebase]

═══════════════════════════════════════════════════════════════════
▶ HALT GATE: [ITEM-ID] IMPLEMENTATION DECISION
═══════════════════════════════════════════════════════════════════

Awaiting your instruction:
• PROCEED - Begin implementation
• SKIP - Move to next item
• MODIFY - Discuss changes
• DISCUSS - I have questions

Your decision:
```

---

# PART 5: SESSION MANAGEMENT

## Starting a Session

When beginning a remediation session, Cursor must:

```
═══════════════════════════════════════════════════════════════════
CIA-SIE REMEDIATION SESSION INITIATED
═══════════════════════════════════════════════════════════════════

Protocol: CIA-SIE-PROTOCOL-002 v4.0 (HITL)
Date: [Current date]
Operator: [Human name if known]

Session mode: Human-in-the-Loop
Decision authority: Human Operator

I will:
✓ Analyze before acting
✓ Wait at all HALT GATES for your decision
✓ Issue clear FINALITY statements
✓ Never proceed without your explicit instruction

Remediation items in queue:
1. D6 - Accessibility Enhancements [CRITICAL]
2. D1 - ChartsReferencePage [MEDIUM]
3. D2 - NoResolutionNotice [MEDIUM]
4. D4 - MobileNavigation [MEDIUM - V2]
5. D5 - GlobalSearch [MEDIUM]
6. D3 - Interactive Components [LOW]

Ready to begin with PRE-FLIGHT SEQUENCE.

Awaiting your instruction:
• START - Begin pre-flight checks
• SKIP-TO [ID] - Start at specific item
• REVIEW - Discuss approach first

Your decision:
═══════════════════════════════════════════════════════════════════
```

## Pausing a Session

```
═══════════════════════════════════════════════════════════════════
SESSION PAUSED
═══════════════════════════════════════════════════════════════════

Current state saved:
• Last completed: [Phase/Item]
• Next pending: [Phase/Item]
• Branch: [branch name]
• Latest commit: [hash]

To resume, start a new conversation and say:
"Resume CIA-SIE remediation from [Phase/Item]"

═══════════════════════════════════════════════════════════════════
```

## Ending a Session

```
═══════════════════════════════════════════════════════════════════
CIA-SIE REMEDIATION SESSION COMPLETE
═══════════════════════════════════════════════════════════════════

Session summary:
────────────────

Items completed:
• D6 - Accessibility ✓

Items skipped:
• D1 - ChartsReferencePage (Human decision: SKIP)

Items remaining:
• D2, D3, D4, D5

Total commits: [X]
Total files changed: [Y]
All tests passing: ✅
Constitutional compliance: ✅

Branch ready for merge: remediation/hitl-protocol-[timestamp]

═══════════════════════════════════════════════════════════════════
```

---

# PART 6: CURSOR INSTRUCTION SUMMARY

## When You Give This Protocol to Cursor, Include:

```
CURSOR OPERATING INSTRUCTIONS
═════════════════════════════

You are executing CIA-SIE-PROTOCOL-002 v4.0 (Human-in-the-Loop).

MANDATORY BEHAVIORS:

1. NEVER proceed past a HALT GATE without my explicit instruction
   - Wait for: PROCEED, CONTINUE, GO, YES, ACCEPT, CERTIFY
   - On: SKIP, NO, STOP → Move on or halt as appropriate
   - On: DISCUSS, MODIFY, REVIEW → Engage in dialogue

2. ALWAYS provide genuine analysis
   - Actually examine the codebase
   - Give honest recommendations (including "don't do this")
   - Base analysis on THIS specific project, not generic advice

3. ALWAYS issue FINALITY statements
   - Use the exact format from the protocol
   - Only issue after ALL validations pass
   - Include commit hash for rollback reference

4. MAINTAIN conversation
   - Each HALT GATE is a pause, not an end
   - After my decision, continue the protocol
   - Keep me informed of what's happening

5. ON ANY FAILURE
   - Stop immediately
   - Report failure clearly
   - Wait for my decision (ROLLBACK, RETRY, INVESTIGATE)

BEGIN NOW with the SESSION INITIATION message.
```

---

# DOCUMENT END

**Protocol Status:** READY FOR EXECUTION
**Execution Model:** Human-in-the-Loop (HITL)
**Decision Authority:** Human Operator
**Cursor Role:** Analysis + Execution + Reporting

---

*End of CIA-SIE Remediation Protocol v4.0*
