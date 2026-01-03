# CURSOR DEVELOPMENT GOVERNANCE
## CIA-SIE Gold Standard Development Operating Procedures

**Version:** 1.0
**Effective Date:** January 2026
**Predecessor:** CURSOR_ARCHITECTURE_GENERATION_DIRECTIVE.md (Phase 4)
**Purpose:** Govern all ongoing development to maintain certification

---

## EXECUTIVE SUMMARY

This document establishes the governance framework for all development activities on CIA-SIE after achieving Gold Standard certification. Every code change, feature addition, and modification must comply with these procedures to maintain constitutional compliance and certification level.

---

## PART I: GOVERNANCE PRINCIPLES

### 1.1 Core Principle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CERTIFICATION PRESERVATION                              │
│                                                                              │
│   The certified codebase is the BASELINE.                                   │
│   Every change must MAINTAIN or IMPROVE certification level.                │
│   Any change that degrades compliance is REJECTED.                          │
│                                                                              │
│   Development is constrained by:                                            │
│   1. Constitutional Rules (inviolable)                                      │
│   2. Architectural Flowcharts (the specification)                           │
│   3. This Governance Document (the process)                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Constitutional Rules (Reference)

These rules are INVIOLABLE and override all other considerations:

| # | Rule | Meaning |
|---|------|---------|
| 1 | Decision-Support ONLY | System NEVER executes trades or makes decisions for user |
| 2 | Never Resolve Contradictions | When signals conflict, show BOTH with equal weight |
| 3 | Descriptive NOT Prescriptive | AI describes what IS, never what user SHOULD do |

### 1.3 Prohibited Patterns

These patterns are NEVER allowed in CIA-SIE code:

```python
# PROHIBITED DATABASE COLUMNS:
weight = Column(...)      # ✗ PROHIBITED
score = Column(...)       # ✗ PROHIBITED
confidence = Column(...)  # ✗ PROHIBITED
recommendation = Column(...)  # ✗ PROHIBITED
priority = Column(...)    # ✗ PROHIBITED
rank = Column(...)        # ✗ PROHIBITED

# PROHIBITED FUNCTIONS:
def execute_trade(...)    # ✗ PROHIBITED
def place_order(...)      # ✗ PROHIBITED
def resolve_contradiction(...)  # ✗ PROHIBITED
def pick_winner(...)      # ✗ PROHIBITED
def aggregate_signals(...)  # ✗ PROHIBITED
def weighted_average(...)  # ✗ PROHIBITED

# PROHIBITED OUTPUT PATTERNS:
"You should..."           # ✗ PROHIBITED
"We recommend..."         # ✗ PROHIBITED
"This suggests..."        # ✗ PROHIBITED
"You must buy..."         # ✗ PROHIBITED
"You must sell..."        # ✗ PROHIBITED
```

---

## PART II: BRANCH STRATEGY

### 2.1 Branch Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          BRANCH HIERARCHY                                    │
│                                                                              │
│   main (protected)                                                          │
│   │                                                                         │
│   │   ← CERTIFIED BASELINE                                                  │
│   │   ← Only accepts PRs from develop after validation                      │
│   │   ← Never commit directly                                               │
│   │                                                                         │
│   └── develop                                                               │
│       │                                                                     │
│       │   ← Integration branch                                              │
│       │   ← Accepts PRs from feature branches                               │
│       │   ← Must pass CI before merge to main                               │
│       │                                                                     │
│       ├── feature/[name]                                                    │
│       │   ← Individual feature work                                         │
│       │   ← Created from develop                                            │
│       │   ← PR back to develop                                              │
│       │                                                                     │
│       ├── bugfix/[name]                                                     │
│       │   ← Bug fixes                                                       │
│       │   ← Created from develop                                            │
│       │   ← PR back to develop                                              │
│       │                                                                     │
│       └── hotfix/[name]                                                     │
│           ← Critical production fixes                                       │
│           ← Created from main                                               │
│           ← PR to main AND develop                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Branch Protection Rules

**main branch:**
```
□ Require pull request before merging
□ Require at least 1 approval
□ Require status checks to pass:
  - CI pipeline (all tests)
  - Constitutional compliance check
  - Security scan
□ Require branches to be up to date
□ Do not allow force push
□ Do not allow deletion
```

**develop branch:**
```
□ Require pull request before merging
□ Require status checks to pass:
  - CI pipeline (all tests)
  - Linting pass
□ Allow force push with lease (for rebasing)
□ Do not allow deletion
```

### 2.3 Branch Naming Convention

```
feature/[ticket-id]-short-description
bugfix/[ticket-id]-short-description
hotfix/[ticket-id]-short-description

Examples:
feature/CIA-123-add-kite-refresh-token
bugfix/CIA-456-fix-signal-normalization
hotfix/CIA-789-critical-auth-fix
```

---

## PART III: PRE-COMMIT CHECKLIST

### 3.1 Before Every Commit

Every developer (including Cursor) must complete this checklist before committing:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PRE-COMMIT CHECKLIST                                                         │
│                                                                              │
│ CONSTITUTIONAL COMPLIANCE:                                                   │
│ □ No trade execution logic added                                            │
│ □ No contradiction resolution logic added                                   │
│ □ No prescriptive language in outputs                                       │
│ □ No prohibited columns in models                                           │
│ □ Disclaimers present on all AI outputs                                     │
│                                                                              │
│ CODE QUALITY:                                                                │
│ □ Linting passes: ruff check src/cia_sie                                   │
│ □ Formatting correct: ruff format --check src/cia_sie                      │
│ □ Type hints present on new functions                                       │
│ □ Docstrings on public functions                                            │
│                                                                              │
│ TESTING:                                                                     │
│ □ New code has tests                                                        │
│ □ All tests pass: pytest tests/                                             │
│ □ Coverage not decreased                                                    │
│                                                                              │
│ SECURITY:                                                                    │
│ □ No hardcoded secrets                                                      │
│ □ Input validation present                                                  │
│ □ No SQL injection vulnerabilities                                          │
│                                                                              │
│ ARCHITECTURE:                                                                │
│ □ Changes align with architectural flowcharts                               │
│ □ If architecture changed, flowcharts updated                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Automated Pre-Commit Checks

Configure pre-commit hooks to enforce:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: constitutional-check
        name: Constitutional Compliance Check
        entry: ./scripts/constitutional_check.sh
        language: script
        files: \.py$

      - id: ruff-lint
        name: Ruff Linting
        entry: ruff check
        language: system
        files: \.py$

      - id: ruff-format
        name: Ruff Format Check
        entry: ruff format --check
        language: system
        files: \.py$

      - id: pytest
        name: Run Tests
        entry: pytest tests/unit/ -x
        language: system
        pass_filenames: false
```

### 3.3 Constitutional Check Script

```bash
#!/bin/bash
# scripts/constitutional_check.sh

echo "=== Constitutional Compliance Check ==="

# Check for prohibited columns
echo "Checking for prohibited columns..."
VIOLATIONS=$(grep -rn "weight\s*=\|score\s*=\|confidence\s*=\|recommendation\s*=" src/cia_sie/dal/models.py 2>/dev/null | grep -v "# NOTE\|# ALLOWED")
if [ ! -z "$VIOLATIONS" ]; then
    echo "❌ CONSTITUTIONAL VIOLATION: Prohibited columns found!"
    echo "$VIOLATIONS"
    exit 1
fi

# Check for prescriptive language in AI outputs
echo "Checking for prescriptive language..."
PRESCRIPTIVE=$(grep -rn '".*should.*"\|".*recommend.*"\|".*suggest.*"\|".*must buy.*"\|".*must sell.*"' src/cia_sie/ai/ 2>/dev/null | grep -v "# filter\|# validate\|# check")
if [ ! -z "$PRESCRIPTIVE" ]; then
    echo "❌ CONSTITUTIONAL VIOLATION: Prescriptive language found!"
    echo "$PRESCRIPTIVE"
    exit 1
fi

# Check for execution logic
echo "Checking for execution logic..."
EXECUTION=$(grep -rn "execute_trade\|place_order\|submit_order" src/cia_sie/ 2>/dev/null)
if [ ! -z "$EXECUTION" ]; then
    echo "❌ CONSTITUTIONAL VIOLATION: Trade execution logic found!"
    echo "$EXECUTION"
    exit 1
fi

# Check for contradiction resolution
echo "Checking for contradiction resolution..."
RESOLUTION=$(grep -rn "resolve_contradiction\|pick_winner\|weighted_average" src/cia_sie/ 2>/dev/null)
if [ ! -z "$RESOLUTION" ]; then
    echo "❌ CONSTITUTIONAL VIOLATION: Contradiction resolution logic found!"
    echo "$RESOLUTION"
    exit 1
fi

echo "✅ Constitutional compliance check passed!"
exit 0
```

---

## PART IV: PULL REQUEST REQUIREMENTS

### 4.1 PR Template

All PRs must use this template:

```markdown
## Description
[Brief description of what this PR does]

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Constitutional Compliance Checklist
- [ ] No trade execution logic added
- [ ] No contradiction resolution logic added
- [ ] No prescriptive language in outputs
- [ ] No prohibited database columns
- [ ] All AI outputs include mandatory disclaimer
- [ ] Signals displayed with equal visual weight

## Testing Checklist
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated (if applicable)
- [ ] All tests passing
- [ ] Coverage maintained or improved

## Architecture Checklist
- [ ] Changes align with BACKEND_ARCHITECTURAL_FLOWCHART.md
- [ ] Changes align with FRONTEND_ARCHITECTURAL_FLOWCHART.md
- [ ] Flowcharts updated if architecture changed
- [ ] RTM updated if requirements affected

## Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] Bandit scan passes

## Screenshots (if UI changes)
[Add screenshots here]

## Additional Notes
[Any additional context]
```

### 4.2 PR Review Criteria

Reviewers must verify:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PR REVIEW CHECKLIST (For Reviewers)                                         │
│                                                                              │
│ CONSTITUTIONAL (Must all be YES):                                           │
│ □ Does this PR maintain decision-support only principle?                    │
│ □ Does this PR avoid resolving contradictions?                              │
│ □ Does this PR maintain descriptive (not prescriptive) language?            │
│                                                                              │
│ QUALITY:                                                                     │
│ □ Is the code readable and maintainable?                                    │
│ □ Are there sufficient tests?                                               │
│ □ Does it follow existing patterns?                                         │
│                                                                              │
│ ARCHITECTURE:                                                                │
│ □ Does it align with the architectural flowcharts?                          │
│ □ Is the change in scope (not scope creep)?                                 │
│                                                                              │
│ SECURITY:                                                                    │
│ □ Are there any security concerns?                                          │
│ □ Is input properly validated?                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Merge Requirements

Before merging to develop:
```
□ At least 1 approval
□ All CI checks passing
□ Constitutional compliance check passing
□ No unresolved comments
□ Branch up to date with develop
```

Before merging to main:
```
□ All develop requirements PLUS:
□ Full integration test suite passing
□ Security scan clean
□ Constitutional compliance verified
□ Documentation updated
```

---

## PART V: COMMIT MESSAGE STANDARDS

### 5.1 Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 5.2 Types

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation changes |
| style | Formatting, missing semi-colons, etc. |
| refactor | Code change that neither fixes a bug nor adds a feature |
| test | Adding or modifying tests |
| chore | Maintenance tasks |

### 5.3 Examples

```
feat(signals): add freshness indicator to signal display

Add visual indicator showing signal freshness status.
- CURRENT: ≤2 minutes (green)
- RECENT: ≤10 minutes (yellow)
- STALE: >30 minutes (red)

Closes #123
```

```
fix(constitutional): ensure all AI outputs include disclaimer

AI responses were missing mandatory disclaimer in some edge cases.
This fix ensures disclaimer is always appended.

Constitutional Rule 3 compliance verified.

Closes #456
```

---

## PART VI: FEATURE DEVELOPMENT WORKFLOW

### 6.1 Standard Feature Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FEATURE DEVELOPMENT WORKFLOW                                                 │
│                                                                              │
│ 1. CREATE BRANCH                                                            │
│    git checkout develop                                                     │
│    git pull origin develop                                                  │
│    git checkout -b feature/CIA-XXX-feature-name                             │
│                                                                              │
│ 2. REFERENCE ARCHITECTURE                                                   │
│    □ Read relevant sections of BACKEND_ARCHITECTURAL_FLOWCHART.md          │
│    □ Read relevant sections of FRONTEND_ARCHITECTURAL_FLOWCHART.md         │
│    □ Identify components/flows affected                                     │
│                                                                              │
│ 3. IMPLEMENT                                                                │
│    □ Write tests first (TDD recommended)                                    │
│    □ Implement feature per architectural specification                      │
│    □ Follow existing code patterns                                          │
│    □ Add documentation                                                      │
│                                                                              │
│ 4. VALIDATE                                                                 │
│    □ Run pre-commit checks                                                  │
│    □ Run full test suite                                                    │
│    □ Run constitutional compliance check                                    │
│    □ Self-review against PR checklist                                       │
│                                                                              │
│ 5. COMMIT                                                                   │
│    git add .                                                                │
│    git commit -m "feat(scope): description"                                 │
│                                                                              │
│ 6. PUSH & PR                                                                │
│    git push -u origin feature/CIA-XXX-feature-name                          │
│    Create PR using template                                                 │
│                                                                              │
│ 7. REVIEW                                                                   │
│    □ Address review comments                                                │
│    □ Get approval                                                           │
│                                                                              │
│ 8. MERGE                                                                    │
│    Squash and merge to develop                                              │
│    Delete feature branch                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Cursor-Specific Workflow

When Cursor implements a feature:

```
1. Output: "Starting feature: [feature name]"

2. Read architectural flowcharts:
   - docs/BACKEND_ARCHITECTURAL_FLOWCHART.md (if backend)
   - docs/FRONTEND_ARCHITECTURAL_FLOWCHART.md (if frontend)

3. Identify affected sections:
   - List components to modify
   - List new components to create
   - List tests to add

4. Implement in order:
   a. Add/modify tests first
   b. Implement feature
   c. Run tests
   d. Run linting
   e. Run constitutional check

5. If any check fails:
   - Fix immediately
   - Do not proceed until passing

6. Commit with proper message format

7. Output summary:
   "Feature complete: [feature name]
    Files modified: X
    Tests added: Y
    Constitutional check: PASS"
```

---

## PART VII: CERTIFICATION MAINTENANCE

### 7.1 Periodic Re-Validation

To maintain certification:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ RE-VALIDATION SCHEDULE                                                       │
│                                                                              │
│ AFTER EACH MAJOR FEATURE:                                                   │
│ □ Run 15-layer validation (abbreviated)                                    │
│ □ Verify certification level maintained                                     │
│                                                                              │
│ WEEKLY:                                                                      │
│ □ Run full test suite                                                       │
│ □ Run security scan                                                         │
│ □ Run constitutional compliance check                                       │
│                                                                              │
│ MONTHLY:                                                                     │
│ □ Run full 15-layer validation                                             │
│ □ Update dependency versions                                                │
│ □ Review and update documentation                                           │
│                                                                              │
│ QUARTERLY:                                                                   │
│ □ Full audit cycle (9-phase)                                               │
│ □ Architecture review                                                       │
│ □ Constitutional rule review                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Certification Level Tracking

Track certification in `CERTIFICATION_STATUS.md`:

```markdown
# CIA-SIE Certification Status

## Current Level: GOLD

| Date | Event | Level | Notes |
|------|-------|-------|-------|
| 2026-01-03 | Initial Certification | GOLD | Phase 3 validation passed |
| 2026-01-15 | Post-feature validation | GOLD | Feature X added, level maintained |
| ... | ... | ... | ... |

## Constitutional Compliance
Last verified: [date]
Status: COMPLIANT

## Next Scheduled Validation
Full validation due: [date]
```

### 7.3 Degradation Response

If certification level drops:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CERTIFICATION DEGRADATION RESPONSE                                           │
│                                                                              │
│ IF level drops from GOLD to SILVER:                                         │
│ 1. Immediately identify cause                                               │
│ 2. Create bugfix branch                                                     │
│ 3. Remediate within 5 business days                                         │
│ 4. Re-validate                                                              │
│                                                                              │
│ IF level drops to BRONZE:                                                   │
│ 1. STOP all new feature work                                                │
│ 2. Prioritize remediation                                                   │
│ 3. Full audit if cause unclear                                              │
│ 4. Must restore to SILVER+ before new features                              │
│                                                                              │
│ IF level drops to FAILED (constitutional violation):                        │
│ 1. IMMEDIATE CODE FREEZE                                                    │
│ 2. Identify and revert offending change                                     │
│ 3. Full constitutional audit                                                │
│ 4. Post-mortem required                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PART VIII: DOCUMENTATION MAINTENANCE

### 8.1 Documentation Updates Required

When code changes:

| Change Type | Documentation Update Required |
|-------------|-------------------------------|
| New API endpoint | API docs, OpenAPI spec |
| New component | Component docs, flowcharts |
| Schema change | Database docs, migration notes |
| New feature | User documentation, README |
| Architecture change | Flowcharts, ADRs |
| Bug fix | Changelog |

### 8.2 Architecture Decision Records

For significant decisions, create ADR:

```markdown
# ADR-XXX: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue that we're seeing that motivates this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
[What becomes easier or more difficult because of this change?]

## Constitutional Compliance
[How does this decision maintain constitutional rules?]
```

---

## PART IX: CURSOR AUTONOMOUS OPERATION

### 9.1 Cursor Operating Constraints

When Cursor works autonomously on CIA-SIE:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CURSOR OPERATING RULES                                                       │
│                                                                              │
│ ALWAYS:                                                                      │
│ □ Read architectural flowcharts before implementing                         │
│ □ Run constitutional check before committing                                │
│ □ Run tests before committing                                               │
│ □ Follow commit message format                                              │
│ □ Update documentation when changing functionality                          │
│ □ Maintain or improve test coverage                                         │
│                                                                              │
│ NEVER:                                                                       │
│ ✗ Add trade execution logic                                                 │
│ ✗ Add contradiction resolution logic                                        │
│ ✗ Add prescriptive language to outputs                                      │
│ ✗ Add prohibited database columns                                           │
│ ✗ Commit failing tests                                                      │
│ ✗ Commit without constitutional check                                       │
│ ✗ Deviate from architectural flowcharts without justification               │
│                                                                              │
│ WHEN UNCERTAIN:                                                              │
│ □ Ask for clarification                                                     │
│ □ Reference this governance document                                        │
│ □ Reference architectural flowcharts                                        │
│ □ Choose the more conservative option                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Cursor Task Acknowledgment

When Cursor receives a development task:

```
1. Output: "Task received: [task description]"

2. Constitutional pre-check:
   "Analyzing task for constitutional implications..."
   IF task conflicts with constitutional rules:
       "⚠️ CONSTITUTIONAL CONCERN: [explanation]"
       "This task cannot proceed as specified because: [reason]"
       "Suggested alternative: [alternative]"
       STOP and await clarification
   ELSE:
       "Constitutional pre-check: PASS"

3. Architecture check:
   "Identifying affected components..."
   List components to modify
   Confirm alignment with flowcharts

4. Proceed with implementation per Section VI workflow
```

---

## PART X: REFERENCE DOCUMENTS

### 10.1 Document Hierarchy

```
CURSOR_AUDIT_INSTRUCTIONS.md
    ↓ (outputs gaps)
CURSOR_REMEDIATION_INSTRUCTIONS.md
    ↓ (fixes gaps)
CURSOR_VALIDATION_INSTRUCTIONS.md
    ↓ (certifies)
CURSOR_ARCHITECTURE_GENERATION_DIRECTIVE.md
    ↓ (generates flowcharts)
CURSOR_DEVELOPMENT_GOVERNANCE.md  ← YOU ARE HERE
    ↓ (governs ongoing work)
Active Development
```

### 10.2 Quick Reference Links

| Document | Purpose |
|----------|---------|
| `docs/BACKEND_ARCHITECTURAL_FLOWCHART.md` | Backend architecture |
| `docs/FRONTEND_ARCHITECTURAL_FLOWCHART.md` | Frontend architecture |
| `docs/CROSS_CUTTING_CONCERNS.md` | Logging, security, testing |
| `handoff/PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md` | Requirements mapping |
| `handoff/VALIDATION_REPORT.md` | Certification evidence |
| `CERTIFICATION_STATUS.md` | Current certification level |

---

## COMPLETION CHECKLIST

Before considering governance fully established:

```
□ This document committed to repository
□ Pre-commit hooks configured
□ Branch protection rules enabled
□ PR template in place
□ Constitutional check script created
□ Team (including Cursor) briefed on process
□ CERTIFICATION_STATUS.md created
□ First development task completed following governance
```

---

## APPENDIX: QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CIA-SIE GOVERNANCE QUICK REFERENCE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ CONSTITUTIONAL RULES (Inviolable):                                          │
│   1. Decision-Support ONLY                                                  │
│   2. Never Resolve Contradictions                                           │
│   3. Descriptive NOT Prescriptive                                           │
│                                                                              │
│ PROHIBITED COLUMNS: weight, score, confidence, recommendation, priority     │
│                                                                              │
│ BRANCH FLOW: feature/* → develop → main                                     │
│                                                                              │
│ BEFORE COMMIT:                                                              │
│   □ ruff check src/cia_sie                                                 │
│   □ ruff format --check src/cia_sie                                        │
│   □ pytest tests/                                                           │
│   □ ./scripts/constitutional_check.sh                                       │
│                                                                              │
│ PR MUST HAVE:                                                               │
│   □ Constitutional compliance checklist complete                            │
│   □ Tests passing                                                           │
│   □ At least 1 approval                                                     │
│                                                                              │
│ ESCALATE IF:                                                                │
│   □ Task conflicts with constitutional rules                                │
│   □ Architecture change required                                            │
│   □ Certification might be affected                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**END OF CURSOR_DEVELOPMENT_GOVERNANCE.md**

*This document governs Phase 5 (and all subsequent development) of the CIA-SIE Gold Standard Development Lifecycle.*
