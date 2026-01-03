# CURSOR REMEDIATION INSTRUCTIONS
## CIA-SIE Gold Standard Remediation Protocol

**Version:** 1.0
**Effective Date:** January 2026
**Predecessor:** CURSOR_AUDIT_INSTRUCTIONS.md (Phase 1)
**Successor:** CURSOR_VALIDATION_INSTRUCTIONS.md (Phase 3)

---

## EXECUTIVE SUMMARY

This document provides Cursor with complete, autonomous instructions to remediate all gaps identified during the Phase 1 Code Audit. Cursor shall systematically fix every issue documented in PHASE_9C (Gap Analysis) and PHASE_9D (Remediation Roadmap), following strict priority order and verification protocols.

---

## PART I: REMEDIATION PRINCIPLES

### 1.1 Core Remediation Philosophy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REMEDIATION HIERARCHY                                │
│                                                                              │
│   CRITICAL ──► Must fix before ANY other work. Blocks all progress.        │
│   HIGH ──────► Must fix before validation. Blocks certification.            │
│   MEDIUM ────► Should fix. Can proceed with documented technical debt.      │
│   LOW ───────► Nice to fix. Document and defer if time-constrained.         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Constitutional Remediation Priority

**ANY constitutional violation is automatically CRITICAL, regardless of assigned severity.**

Constitutional violations include:
- Decision-making logic (instead of decision-support)
- Contradiction resolution logic (instead of exposure)
- Prescriptive language in AI outputs
- Prohibited database columns (weight, score, confidence, recommendation, priority, rank)
- Missing mandatory disclaimers
- Signal aggregation or weighting logic

### 1.3 Remediation Standards

| Standard | Requirement |
|----------|-------------|
| **Minimal Change** | Fix only what is broken. Do not refactor surrounding code. |
| **Test Coverage** | Every fix must have or maintain test coverage. |
| **Verification** | Every fix must be verified before marking complete. |
| **Documentation** | Every fix must be logged with before/after evidence. |
| **Atomicity** | One fix category per commit. No bundled changes. |

---

## PART II: INPUT DOCUMENTS

### 2.1 Required Inputs

Before beginning remediation, Cursor MUST read and parse:

```
handoff/
├── PHASE_9C_GAP_ANALYSIS.md          ← Primary input (what to fix)
├── PHASE_9D_REMEDIATION_ROADMAP.md   ← Secondary input (how to fix)
├── PHASE_9A_REQUIREMENTS_TRACEABILITY_MATRIX.md ← Reference (requirements mapping)
└── PHASE_9B_COMPLIANCE_SCORECARD.md  ← Reference (current scores)
```

### 2.2 Gap Analysis Structure

PHASE_9C should contain gaps in this format:

```markdown
## GAP-001: [Gap Title]
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW
- **Category:** Constitutional | Security | Functional | Quality | Documentation
- **Location:** file_path:line_number
- **Description:** What is wrong
- **Impact:** Why it matters
- **Evidence:** Code snippet or test failure
```

### 2.3 Remediation Roadmap Structure

PHASE_9D should contain fixes in this format:

```markdown
## FIX-001: [Fix Title] (for GAP-001)
- **Priority:** 1 (highest) to N (lowest)
- **Effort:** Hours | Days | Weeks
- **Approach:** Step-by-step fix instructions
- **Verification:** How to confirm fix worked
- **Dependencies:** Other fixes that must come first
```

---

## PART III: REMEDIATION EXECUTION PROTOCOL

### 3.1 Initialization

Upon receiving this document, Cursor shall:

```
1. Output: "GOLD STANDARD REMEDIATION INITIATED"
2. Read PHASE_9C_GAP_ANALYSIS.md
3. Read PHASE_9D_REMEDIATION_ROADMAP.md
4. Parse all gaps into severity categories
5. Output gap count summary:
   "Found: X CRITICAL, Y HIGH, Z MEDIUM, W LOW gaps"
6. Begin remediation in priority order
```

### 3.2 Remediation Order

**STRICT ORDER - NO EXCEPTIONS:**

```
Phase 2.1: CRITICAL Constitutional Gaps
Phase 2.2: CRITICAL Security Gaps
Phase 2.3: CRITICAL Functional Gaps
Phase 2.4: HIGH Constitutional Gaps
Phase 2.5: HIGH Security Gaps
Phase 2.6: HIGH Functional Gaps
Phase 2.7: HIGH Quality Gaps
Phase 2.8: MEDIUM Gaps (all categories)
Phase 2.9: LOW Gaps (all categories)
Phase 2.10: Documentation Gaps
```

### 3.3 Per-Gap Remediation Procedure

For EACH gap, execute this procedure:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: UNDERSTAND                                                           │
│ ─────────────────────────────────────────────────────────────────────────── │
│ □ Read gap description from PHASE_9C                                        │
│ □ Read fix approach from PHASE_9D                                           │
│ □ Navigate to affected file(s)                                              │
│ □ Read surrounding context (50 lines before/after)                          │
│ □ Identify root cause                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: PLAN                                                                 │
│ ─────────────────────────────────────────────────────────────────────────── │
│ □ Determine minimal change required                                         │
│ □ Check for side effects on other code                                      │
│ □ Identify tests that cover this code                                       │
│ □ Plan verification approach                                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: IMPLEMENT                                                            │
│ ─────────────────────────────────────────────────────────────────────────── │
│ □ Make the fix                                                              │
│ □ Add/update tests if needed                                                │
│ □ Run affected tests                                                        │
│ □ Run linter (ruff check)                                                   │
│ □ Run formatter (ruff format)                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: VERIFY                                                               │
│ ─────────────────────────────────────────────────────────────────────────── │
│ □ Confirm gap condition no longer exists                                    │
│ □ Confirm no new issues introduced                                          │
│ □ Confirm tests pass                                                        │
│ □ Confirm constitutional compliance maintained                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: DOCUMENT                                                             │
│ ─────────────────────────────────────────────────────────────────────────── │
│ □ Log fix in REMEDIATION_LOG.md                                             │
│ □ Update PHASE_9C gap status to RESOLVED                                    │
│ □ Update PHASE_9B scorecard if applicable                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PART IV: REMEDIATION BY CATEGORY

### 4.1 Constitutional Gap Remediation

**These are the highest priority. Stop everything else until resolved.**

#### 4.1.1 Decision-Making Logic Found

```python
# VIOLATION PATTERN:
if signal.direction == "BULLISH":
    execute_buy_order()  # CONSTITUTIONAL VIOLATION

# REMEDIATION:
# Remove execution logic entirely. System is decision-SUPPORT only.
# Replace with:
if signal.direction == "BULLISH":
    display_signal(signal)  # Display only, no action
```

#### 4.1.2 Contradiction Resolution Found

```python
# VIOLATION PATTERN:
def resolve_contradiction(signal1, signal2):
    if signal1.strength > signal2.strength:
        return signal1  # CONSTITUTIONAL VIOLATION - resolving!

# REMEDIATION:
# Remove resolution logic. Return BOTH signals with equal weight.
def expose_contradiction(signal1, signal2):
    return ContradictionExposure(
        signal_a=signal1,
        signal_b=signal2,
        resolution=None  # NEVER resolve
    )
```

#### 4.1.3 Prescriptive Language Found

```python
# VIOLATION PATTERN:
narrative = "Based on signals, you should buy..."  # VIOLATION

# REMEDIATION:
narrative = "The signals show bullish momentum on daily timeframe..."  # Descriptive
# MUST add disclaimer
```

#### 4.1.4 Prohibited Column Found

```python
# VIOLATION PATTERN:
class Signal(Base):
    weight = Column(Float)  # PROHIBITED

# REMEDIATION:
# Remove column entirely. Do not rename, do not comment out.
class Signal(Base):
    # weight column removed - constitutional prohibition
    pass

# Also create migration to drop column if exists in DB
```

### 4.2 Security Gap Remediation

#### 4.2.1 SQL Injection Vulnerability

```python
# VIOLATION PATTERN:
query = f"SELECT * FROM signals WHERE id = {user_input}"  # VULNERABLE

# REMEDIATION:
query = select(Signal).where(Signal.id == user_input)  # Parameterized
```

#### 4.2.2 Hardcoded Secrets

```python
# VIOLATION PATTERN:
API_KEY = "sk-abc123..."  # HARDCODED SECRET

# REMEDIATION:
API_KEY = os.environ.get("API_KEY")  # Environment variable
# Add to .env.example as placeholder
```

#### 4.2.3 Missing Input Validation

```python
# VIOLATION PATTERN:
@router.post("/signals")
async def create_signal(data: dict):  # Unvalidated

# REMEDIATION:
@router.post("/signals")
async def create_signal(data: SignalCreate):  # Pydantic validation
```

### 4.3 Functional Gap Remediation

#### 4.3.1 Missing Error Handling

```python
# VIOLATION PATTERN:
response = await client.get(url)
data = response.json()  # No error handling

# REMEDIATION:
try:
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()
except httpx.HTTPError as e:
    logger.error(f"HTTP error: {e}")
    raise APIError(f"Failed to fetch: {e}")
```

#### 4.3.2 Missing Test Coverage

```python
# VIOLATION: Function has no tests

# REMEDIATION:
# Create test file or add to existing test file
def test_function_name():
    # Arrange
    input_data = {...}

    # Act
    result = function_name(input_data)

    # Assert
    assert result == expected
```

### 4.4 Quality Gap Remediation

#### 4.4.1 Type Hints Missing

```python
# VIOLATION PATTERN:
def process_signal(signal, options):
    ...

# REMEDIATION:
def process_signal(signal: Signal, options: ProcessOptions) -> ProcessedSignal:
    ...
```

#### 4.4.2 Documentation Missing

```python
# VIOLATION PATTERN:
def complex_function(a, b, c):
    ...

# REMEDIATION:
def complex_function(a: TypeA, b: TypeB, c: TypeC) -> Result:
    """Process inputs and return result.

    Args:
        a: Description of a
        b: Description of b
        c: Description of c

    Returns:
        Processed result

    Raises:
        ValueError: If inputs invalid
    """
    ...
```

---

## PART V: REMEDIATION LOG FORMAT

### 5.1 Log File Creation

Create `handoff/REMEDIATION_LOG.md` with this structure:

```markdown
# REMEDIATION LOG
## CIA-SIE Gold Standard Remediation

**Started:** [timestamp]
**Completed:** [timestamp]
**Total Gaps:** X
**Resolved:** Y
**Deferred:** Z

---

## Summary by Severity

| Severity | Found | Fixed | Deferred | Remaining |
|----------|-------|-------|----------|-----------|
| CRITICAL | X | X | 0 | 0 |
| HIGH | X | X | 0 | 0 |
| MEDIUM | X | X | X | 0 |
| LOW | X | X | X | 0 |

---

## Detailed Fix Log

### FIX-001: [Title]
- **Gap Reference:** GAP-001
- **Severity:** CRITICAL
- **Category:** Constitutional
- **File:** src/cia_sie/path/file.py
- **Line:** 123

**Before:**
```python
[code that was wrong]
```

**After:**
```python
[code that is now correct]
```

**Verification:**
- [x] Tests pass
- [x] Linter pass
- [x] Constitutional check pass

**Committed:** [commit hash]

---
```

### 5.2 Commit Message Format

After each severity category, commit with this format:

```
Remediate [SEVERITY] [CATEGORY] gaps ([N] fixes)

Fixes:
- GAP-001: [brief description]
- GAP-002: [brief description]
- ...

All fixes verified and tested.

Governed by: CURSOR_REMEDIATION_INSTRUCTIONS.md
```

---

## PART VI: VERIFICATION PROTOCOLS

### 6.1 Constitutional Verification

After ALL remediation, run these checks:

```bash
# Check for prohibited columns
grep -rn "weight\s*=" src/cia_sie/dal/models.py
grep -rn "score\s*=" src/cia_sie/dal/models.py
grep -rn "confidence\s*=" src/cia_sie/dal/models.py
grep -rn "recommendation\s*=" src/cia_sie/dal/models.py

# Expected: No output (no matches)

# Check for prescriptive language in AI module
grep -rn "should" src/cia_sie/ai/
grep -rn "recommend" src/cia_sie/ai/
grep -rn "suggest" src/cia_sie/ai/
grep -rn "must buy" src/cia_sie/ai/
grep -rn "must sell" src/cia_sie/ai/

# Expected: Only in validation/filtering code, not in output generation
```

### 6.2 Test Verification

```bash
# Run full test suite
python -m pytest tests/ -v --tb=short

# Run with coverage
python -m pytest tests/ --cov=src/cia_sie --cov-report=term-missing

# Expected: All tests pass, coverage maintained or improved
```

### 6.3 Linting Verification

```bash
# Check linting
ruff check src/cia_sie

# Check formatting
ruff format --check src/cia_sie

# Expected: No errors
```

---

## PART VII: GATE CONDITIONS

### 7.1 Remediation Completion Criteria

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ REMEDIATION COMPLETE WHEN:                                                   │
│                                                                              │
│ □ ALL CRITICAL gaps resolved (mandatory)                                    │
│ □ ALL HIGH gaps resolved (mandatory)                                        │
│ □ ALL Constitutional gaps resolved regardless of severity (mandatory)       │
│ □ MEDIUM gaps resolved OR documented as technical debt                      │
│ □ LOW gaps resolved OR documented as technical debt                         │
│ □ All tests passing                                                         │
│ □ All linting passing                                                       │
│ □ REMEDIATION_LOG.md complete                                               │
│ □ All commits pushed                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Blocking Conditions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CANNOT PROCEED TO PHASE 3 (VALIDATION) IF:                                  │
│                                                                              │
│ ✗ Any CRITICAL gap remains unresolved                                       │
│ ✗ Any HIGH gap remains unresolved                                           │
│ ✗ Any Constitutional violation remains                                      │
│ ✗ Tests failing                                                             │
│ ✗ REMEDIATION_LOG.md incomplete                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Proceed Conditions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PROCEED TO PHASE 3 WHEN:                                                     │
│                                                                              │
│ ✓ Zero CRITICAL gaps remaining                                              │
│ ✓ Zero HIGH gaps remaining                                                  │
│ ✓ Zero Constitutional violations                                            │
│ ✓ All tests passing                                                         │
│ ✓ REMEDIATION_LOG.md complete with all fixes documented                     │
│ ✓ Final commit: "Complete Phase 2 remediation"                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PART VIII: AUTONOMOUS EXECUTION DIRECTIVE

### 8.1 Execution Command

Upon receiving this document, Cursor shall:

```
1. Output: "GOLD STANDARD REMEDIATION INITIATED"

2. Read and parse:
   - handoff/PHASE_9C_GAP_ANALYSIS.md
   - handoff/PHASE_9D_REMEDIATION_ROADMAP.md

3. Output gap summary:
   "GAPS IDENTIFIED:
    - CRITICAL: X
    - HIGH: Y
    - MEDIUM: Z
    - LOW: W
    - TOTAL: N"

4. Create handoff/REMEDIATION_LOG.md

5. Execute remediation in priority order (Part III)

6. After each severity category:
   - Run tests
   - Run linter
   - Commit with prescribed message format
   - Update REMEDIATION_LOG.md

7. After all remediation:
   - Run full verification (Part VI)
   - Output final summary
   - Commit: "Complete Phase 2 remediation"

8. Output: "PHASE 2 REMEDIATION COMPLETE"
   Output: "Proceed to Phase 3: Validation"
```

### 8.2 Error Handling

```
IF a fix causes tests to fail:
    1. Revert the fix
    2. Log the issue in REMEDIATION_LOG.md
    3. Mark gap as BLOCKED with reason
    4. Continue to next gap
    5. Return to blocked gaps after completing others

IF a fix is unclear or ambiguous:
    1. Log uncertainty in REMEDIATION_LOG.md
    2. Implement most conservative fix
    3. Add TODO comment for human review
    4. Continue remediation

IF dependencies between gaps exist:
    1. Fix dependencies first
    2. Log dependency chain in REMEDIATION_LOG.md
    3. Verify dependency fix before dependent fix
```

### 8.3 Human Escalation

```
ESCALATE TO HUMAN IF:
    - Gap resolution conflicts with Constitutional rules
    - Fix would require architectural changes
    - Fix breaks more than it resolves
    - Unclear business logic decision required

ESCALATION FORMAT:
    "HUMAN REVIEW REQUIRED:
     Gap: GAP-XXX
     Issue: [description]
     Options:
       A) [option]
       B) [option]
     Recommendation: [if any]
     Blocking: [Yes/No]"
```

---

## PART IX: REFERENCE QUICK CHECKS

### 9.1 Constitutional Quick Reference

| Rule | Check | Pass Criteria |
|------|-------|---------------|
| Rule 1 | No execution logic | Zero trade/order execution code |
| Rule 2 | No resolution logic | Contradictions exposed, never resolved |
| Rule 3 | Descriptive only | No should/recommend/suggest in outputs |

### 9.2 Prohibited Patterns

```python
# NEVER ALLOWED:
execute_trade()
place_order()
signal.weight
signal.score
signal.confidence
"you should"
"we recommend"
"suggests buying"
resolve_contradiction()
pick_winner()
aggregate_signals()
weighted_average()
```

### 9.3 Required Patterns

```python
# ALWAYS REQUIRED:
display_signal()           # Instead of execute
expose_contradiction()     # Instead of resolve
"The chart shows..."       # Instead of "You should..."
DISCLAIMER                 # On all AI outputs
```

---

## COMPLETION CHECKLIST

Before declaring Phase 2 complete:

```
□ PHASE_9C gaps: All CRITICAL resolved
□ PHASE_9C gaps: All HIGH resolved
□ PHASE_9C gaps: All Constitutional resolved
□ Tests: All passing
□ Linting: All passing
□ REMEDIATION_LOG.md: Complete
□ Commits: All pushed
□ Constitutional verification: Passed
□ Ready for Phase 3: Validation
```

---

**END OF CURSOR_REMEDIATION_INSTRUCTIONS.md**

*This document governs Phase 2 of the CIA-SIE Gold Standard Development Lifecycle.*
