# FINANCIAL SERVICES DOMAIN ADAPTER
## Gold Standard Framework Extension for Trading & Investment Applications

---

**Document ID:** GSUF-TIER2-FIN-001
**Version:** 1.0.0
**Classification:** Domain-Specific Adapter
**Applicability:** Trading platforms, investment tools, financial decision-support systems
**Parent Framework:** GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0.md
**Regulatory Alignment:** SEC, FINRA, MiFID II, SOX Section 404

---

## PURPOSE

This adapter extends the Gold Standard Unified Framework with domain-specific rules for **financial services applications** — particularly trading platforms, investment signal aggregators, and market analysis tools.

**Critical Distinction:** Financial decision-support tools must NEVER cross the line from information presentation to investment advice. This adapter enforces that boundary.

---

## TABLE OF CONTENTS

1. [Constitutional Rules](#1-constitutional-rules)
2. [Prohibited Patterns Registry](#2-prohibited-patterns-registry)
3. [Mandatory Artefacts](#3-mandatory-artefacts)
4. [Data Model Constraints](#4-data-model-constraints)
5. [Regulatory Compliance Mapping](#5-regulatory-compliance-mapping)
6. [Verification Procedures](#6-verification-procedures)
7. [Domain-Specific Test Requirements](#7-domain-specific-test-requirements)

---

# 1. CONSTITUTIONAL RULES

Constitutional rules are **absolute constraints** that cannot be violated under any circumstances. A single violation renders the entire system non-compliant.

---

## CR-001: DECISION-SUPPORT ONLY

### Statement

The system provides **information aggregation and presentation ONLY**. It does NOT provide investment advice, recommendations, or execute trades on behalf of users.

### Prohibition

The system shall NEVER:
- Execute trades automatically
- Place orders on behalf of users
- Make buy/sell/hold recommendations
- Suggest position sizes
- Provide price targets
- Indicate optimal entry/exit points
- Generate trading signals with directional bias

### Requirement

The system SHALL:
- Present raw signals from connected platforms WITHOUT interpretation
- Display market data WITHOUT editorial commentary
- Show confirmations and contradictions WITHOUT resolution
- Require explicit user action for any trading activity
- Maintain clear separation between information display and trade execution

### Rationale

Investment advice requires registration with regulatory bodies (SEC, FINRA, FCA, etc.). Crossing this boundary without registration exposes the application and its operators to significant legal liability.

### Detection Method

```bash
# Search for recommendation language
grep -rn -E "(recommend|should\s+(buy|sell|hold)|suggest|advise|optimal|best\s+(time|price|entry|exit))" src/

# Search for trade execution
grep -rn -E "(execute.*trade|place.*order|submit.*order|auto.*trade)" src/

# Search for position sizing
grep -rn -E "(position\s*size|lot\s*size|quantity.*recommend)" src/
```

### Violation Severity

**CRITICAL** — Renders entire system non-compliant. Immediate remediation required.

---

## CR-002: NEVER RESOLVE CONTRADICTIONS

### Statement

When multiple data sources present conflicting signals, the system shall present ALL signals with equal prominence. It shall NEVER attempt to resolve, reconcile, or weight contradictory information.

### Prohibition

The system shall NEVER:
- Hide or de-emphasise contradictory signals
- Apply weighting to favour one signal over another
- Use algorithms to "resolve" conflicting data
- Present a "consensus" view that masks disagreement
- Filter signals based on perceived reliability
- Rank signals by confidence or probability

### Requirement

The system SHALL:
- Display ALL signals from ALL connected sources
- Present contradictions explicitly and prominently
- Use equal visual weight for conflicting signals
- Preserve the original signal metadata without modification
- Allow users to see the full picture and make their own judgments

### Rationale

Resolving contradictions is a form of investment advice. The act of choosing which signal to emphasise implies a recommendation. Users must see all available information to make informed decisions.

### Detection Method

```bash
# Search for resolution logic
grep -rn -E "(resolve.*conflict|reconcile|consensus|aggregate.*signal)" src/

# Search for weighting
grep -rn -E "(weight|score|rank|priority|confidence)" src/

# Search for filtering
grep -rn -E "(filter.*signal|hide.*signal|suppress)" src/
```

### Violation Severity

**CRITICAL** — Renders entire system non-compliant. Immediate remediation required.

---

## CR-003: DESCRIPTIVE NOT PRESCRIPTIVE

### Statement

All system outputs shall be **descriptive** (stating what IS) rather than **prescriptive** (stating what SHOULD BE). The system describes market conditions; it does not prescribe actions.

### Prohibition

The system shall NEVER use prescriptive language including:
- "should" / "shouldn't"
- "recommend" / "recommended"
- "suggest" / "suggested"
- "advise" / "advised"
- "consider" (in advisory context)
- "opportunity" (implying action)
- "ideal" / "optimal"
- "buy" / "sell" / "hold" (as directives)
- "action required"
- "don't miss"
- "act now"

### Requirement

The system SHALL use only descriptive language:
- "Signal indicates..." (not "You should...")
- "Data shows..." (not "Consider buying...")
- "Source reports..." (not "Recommended action...")
- "Confirmation detected" (not "Good opportunity")
- "Contradiction exists" (not "Caution advised")

### Detection Method

```bash
# Comprehensive prescriptive language search
grep -rn -E "(should|shouldn't|recommend|suggest|advise|consider\s+buying|consider\s+selling|opportunity|optimal|ideal|act\s+now|don't\s+miss|action\s+required)" src/

# Check UI components for prescriptive text
grep -rn -E "(should|recommend|suggest|advise)" src/ --include="*.tsx" --include="*.jsx" --include="*.vue" --include="*.html"

# Check API responses
grep -rn -E "(should|recommend|suggest|advise)" src/ --include="*.py" --include="*.ts" --include="*.js"
```

### Violation Severity

**CRITICAL** — Renders entire system non-compliant. Immediate remediation required.

---

# 2. PROHIBITED PATTERNS REGISTRY

## 2.1 Prohibited Language Patterns

| Category | Prohibited Terms | Allowed Alternatives |
|----------|------------------|---------------------|
| **Recommendations** | recommend, suggestion, advise, guidance | signal indicates, data shows, source reports |
| **Directives** | should, must, need to, have to | is, shows, indicates, presents |
| **Urgency** | act now, don't miss, limited time, opportunity | current state, present condition |
| **Confidence** | confident, certain, likely, probably | reported, indicated, signaled |
| **Quality Judgment** | best, optimal, ideal, good, bad | higher, lower, above, below |
| **Actions** | buy, sell, hold (as commands) | bullish signal, bearish signal, neutral |

## 2.2 Prohibited Code Patterns

| Pattern | Why Prohibited | Detection |
|---------|----------------|-----------|
| `weight = ` in models | Implies signal prioritisation | `grep -rn "weight\s*=" src/` |
| `score = ` in models | Implies quality ranking | `grep -rn "score\s*=" src/` |
| `confidence = ` in models | Implies reliability judgment | `grep -rn "confidence\s*=" src/` |
| `priority = ` for signals | Implies recommendation | `grep -rn "priority\s*=" src/` |
| `rank = ` for signals | Implies ordering by quality | `grep -rn "rank\s*=" src/` |
| `recommendation = ` | Direct violation | `grep -rn "recommendation\s*=" src/` |
| `aggregate()` on signals | May resolve contradictions | `grep -rn "aggregate" src/` |
| `average()` on signals | Combines/resolves signals | `grep -rn "average.*signal" src/` |
| `weighted_average()` | Explicit weighting | `grep -rn "weighted" src/` |

## 2.3 Prohibited UI Patterns

| Pattern | Why Prohibited | Alternative |
|---------|----------------|-------------|
| Traffic light indicators (green/red) for signals | Implies good/bad judgment | Neutral colour indicators |
| "Strength" meters | Implies quality ranking | Raw value display |
| "Confidence" badges | Implies reliability judgment | Source attribution only |
| Sorted signals by "importance" | Implies prioritisation | Chronological or alphabetical |
| Hidden/collapsed contradictions | De-emphasises conflicts | Equal prominence display |
| "Top picks" or "Best signals" | Direct recommendation | "Recent signals" or "All signals" |

---

# 3. MANDATORY ARTEFACTS

## 3.1 Disclaimer Requirements

Every financial services application MUST display appropriate disclaimers.

### Required Disclaimer Elements

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MANDATORY DISCLAIMER CONTENT                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. NOT INVESTMENT ADVICE                                                    │
│    "This application provides information aggregation only. It does not     │
│    provide investment advice, recommendations, or trading signals."         │
│                                                                             │
│ 2. USER RESPONSIBILITY                                                      │
│    "All trading decisions are made solely by the user. The user assumes    │
│    full responsibility for any trading activity."                           │
│                                                                             │
│ 3. NO GUARANTEES                                                            │
│    "Past performance does not guarantee future results. Trading involves   │
│    substantial risk of loss."                                               │
│                                                                             │
│ 4. DATA ACCURACY                                                            │
│    "Data is provided as-is from third-party sources. Accuracy is not       │
│    guaranteed."                                                             │
│                                                                             │
│ 5. PROFESSIONAL ADVICE                                                      │
│    "Consult a licensed financial advisor before making investment          │
│    decisions."                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Disclaimer Placement

| Location | Requirement |
|----------|-------------|
| Application Footer | Persistent disclaimer visible on all pages |
| Login/Registration | Full disclaimer with acknowledgment checkbox |
| Signal Display Pages | Contextual reminder |
| Trade Execution Interface | Prominent warning before any trade action |
| API Documentation | Clear statement of informational purpose |

### Verification

```bash
# Search for disclaimer implementation
grep -rn -E "(disclaimer|not.*investment.*advice|not.*recommendation)" src/
grep -rn -E "(user.*responsibility|trading.*risk)" src/
```

---

## 3.2 Signal Attribution Requirements

Every signal displayed MUST include:

| Attribute | Requirement |
|-----------|-------------|
| **Source** | Platform/service that generated the signal |
| **Timestamp** | When the signal was generated (not received) |
| **Original Data** | Unmodified signal content |
| **Freshness Indicator** | Age of signal clearly displayed |

### Prohibited Modifications

- Paraphrasing signal content
- Combining signals into summaries
- Removing signal metadata
- Changing signal timestamps

---

# 4. DATA MODEL CONSTRAINTS

## 4.1 Prohibited Database Columns

The following column names are **PROHIBITED** in any signal-related tables:

| Prohibited Column | Reason |
|-------------------|--------|
| `weight` | Implies signal prioritisation |
| `score` | Implies quality ranking |
| `confidence` | Implies reliability judgment |
| `priority` | Implies recommendation ordering |
| `rank` | Implies quality hierarchy |
| `recommendation` | Direct advisory content |
| `action` | Implies prescribed behaviour |
| `rating` | Implies quality judgment |

## 4.2 Required Database Columns

Signal tables SHOULD include:

| Required Column | Purpose |
|-----------------|---------|
| `source` | Attribution to originating platform |
| `source_timestamp` | When signal was generated |
| `received_timestamp` | When signal was received |
| `raw_content` | Unmodified signal data |
| `signal_type` | Classification (bullish/bearish/neutral) |
| `instrument` | Associated financial instrument |

## 4.3 Verification Query

```sql
-- Check for prohibited columns in signal tables
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name IN ('weight', 'score', 'confidence', 'priority', 'rank', 'recommendation', 'action', 'rating')
AND table_name LIKE '%signal%';

-- Should return ZERO rows
```

---

# 5. REGULATORY COMPLIANCE MAPPING

## 5.1 Applicable Regulations

| Regulation | Jurisdiction | Key Requirements | Framework Sections |
|------------|--------------|------------------|-------------------|
| **SEC Rule** | USA | No unregistered investment advice | CR-001, CR-003 |
| **FINRA Rules** | USA | Suitability, fair communication | CR-001, CR-002, CR-003 |
| **MiFID II** | EU | Best execution, client categorisation | CR-001, Section 3 |
| **FCA COBS** | UK | Fair, clear, not misleading | CR-003, Section 2 |
| **SOX 404** | USA | Internal controls documentation | All sections |

## 5.2 Regulatory Risk Matrix

| Constitutional Rule | Regulatory Risk if Violated |
|--------------------|----------------------------|
| CR-001 (Decision-Support Only) | Unregistered investment advisor (SEC), unsuitable recommendations (FINRA) |
| CR-002 (Never Resolve Contradictions) | Misleading communications (FINRA), unfair presentation (FCA) |
| CR-003 (Descriptive Not Prescriptive) | Investment advice without registration, misleading promotions |

## 5.3 Audit Trail Requirements

For regulatory compliance, maintain:

| Audit Element | Retention Period | Purpose |
|---------------|------------------|---------|
| Signal receipt logs | 7 years | Prove no modification |
| User action logs | 7 years | Prove user-initiated trades |
| System configuration | 7 years | Prove compliant design |
| Disclaimer acknowledgments | 7 years | Prove user informed |

---

# 6. VERIFICATION PROCEDURES

## 6.1 Constitutional Compliance Verification Script

```bash
#!/bin/bash
# constitutional_check.sh
# Run this script to verify constitutional compliance

echo "=== CONSTITUTIONAL COMPLIANCE CHECK ==="
echo ""

# CR-001: Decision-Support Only
echo "--- CR-001: Decision-Support Only ---"
echo "Checking for recommendation language..."
VIOLATIONS=$(grep -rn -E "(recommend|should\s+(buy|sell|hold)|suggest|advise)" src/ --include="*.py" --include="*.ts" --include="*.tsx" | wc -l)
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "FAIL: Found $VIOLATIONS potential violations"
    grep -rn -E "(recommend|should\s+(buy|sell|hold)|suggest|advise)" src/ --include="*.py" --include="*.ts" --include="*.tsx"
else
    echo "PASS: No recommendation language found"
fi
echo ""

# CR-002: Never Resolve Contradictions
echo "--- CR-002: Never Resolve Contradictions ---"
echo "Checking for weighting/scoring patterns..."
VIOLATIONS=$(grep -rn -E "(weight\s*=|score\s*=|confidence\s*=|priority\s*=|rank\s*=)" src/ --include="*.py" | wc -l)
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "FAIL: Found $VIOLATIONS potential violations"
    grep -rn -E "(weight\s*=|score\s*=|confidence\s*=|priority\s*=|rank\s*=)" src/ --include="*.py"
else
    echo "PASS: No weighting/scoring patterns found"
fi
echo ""

# CR-003: Descriptive Not Prescriptive
echo "--- CR-003: Descriptive Not Prescriptive ---"
echo "Checking for prescriptive language..."
VIOLATIONS=$(grep -rn -E "(should|shouldn't|must\s+buy|must\s+sell|opportunity|optimal|ideal)" src/ --include="*.py" --include="*.ts" --include="*.tsx" | grep -v "# " | grep -v "// " | wc -l)
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "FAIL: Found $VIOLATIONS potential violations"
    grep -rn -E "(should|shouldn't|must\s+buy|must\s+sell|opportunity|optimal|ideal)" src/ --include="*.py" --include="*.ts" --include="*.tsx" | grep -v "# " | grep -v "// "
else
    echo "PASS: No prescriptive language found"
fi
echo ""

echo "=== CHECK COMPLETE ==="
```

## 6.2 Database Schema Verification

```python
# verify_schema.py
# Run to verify no prohibited columns exist

PROHIBITED_COLUMNS = [
    'weight', 'score', 'confidence', 'priority',
    'rank', 'recommendation', 'action', 'rating'
]

def verify_models(models_file: str) -> list:
    """Check ORM models for prohibited columns."""
    violations = []
    with open(models_file, 'r') as f:
        content = f.read()
        for col in PROHIBITED_COLUMNS:
            if f'{col} =' in content or f'{col}=' in content:
                violations.append(col)
    return violations

# Usage
violations = verify_models('src/dal/models.py')
if violations:
    print(f"FAIL: Prohibited columns found: {violations}")
else:
    print("PASS: No prohibited columns in models")
```

## 6.3 UI Text Verification

```bash
# Check all user-facing strings for prescriptive language
grep -rn -E "(should|recommend|suggest|advise|opportunity|consider\s+buying)" \
    src/ \
    --include="*.tsx" \
    --include="*.jsx" \
    --include="*.vue" \
    --include="*.html" \
    --include="*.json"
```

---

# 7. DOMAIN-SPECIFIC TEST REQUIREMENTS

## 7.1 Required Test Categories

| Test Category | Purpose | Minimum Coverage |
|---------------|---------|------------------|
| Constitutional Compliance Tests | Verify CR-001, CR-002, CR-003 | **100%** |
| Signal Integrity Tests | Verify signals not modified | 100% |
| Disclaimer Presence Tests | Verify disclaimers displayed | 100% |
| Attribution Tests | Verify source/timestamp shown | 100% |
| Contradiction Display Tests | Verify conflicts shown equally | 100% |

## 7.2 Example Test Cases

### CR-001 Test: No Recommendations

```python
def test_no_recommendation_language_in_responses():
    """Verify API responses contain no recommendation language."""
    prohibited_terms = ['recommend', 'should', 'suggest', 'advise', 'consider buying']

    response = client.get('/api/signals')
    response_text = response.json()

    for term in prohibited_terms:
        assert term.lower() not in str(response_text).lower(), \
            f"Prohibited term '{term}' found in API response"
```

### CR-002 Test: No Signal Weighting

```python
def test_signals_have_no_weight_or_score():
    """Verify signal objects contain no weight/score fields."""
    prohibited_fields = ['weight', 'score', 'confidence', 'priority', 'rank']

    signals = get_all_signals()

    for signal in signals:
        for field in prohibited_fields:
            assert not hasattr(signal, field), \
                f"Signal has prohibited field: {field}"
```

### CR-003 Test: Descriptive Language Only

```python
def test_ui_uses_descriptive_language():
    """Verify UI components use descriptive, not prescriptive language."""
    prescriptive_patterns = [
        r'\bshould\b',
        r'\bshouldn\'t\b',
        r'\brecommend',
        r'\bsuggest',
        r'\badvise',
        r'\bopportunity\b',
        r'\boptimal\b'
    ]

    ui_files = glob.glob('src/**/*.tsx', recursive=True)

    for filepath in ui_files:
        with open(filepath, 'r') as f:
            content = f.read()
            for pattern in prescriptive_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                assert not matches, \
                    f"Prescriptive language '{pattern}' found in {filepath}"
```

### Contradiction Display Test

```python
def test_contradictions_displayed_equally():
    """Verify contradictory signals shown with equal prominence."""
    # Create conflicting signals
    bullish_signal = create_signal(direction='bullish', source='A')
    bearish_signal = create_signal(direction='bearish', source='B')

    # Get display representation
    display = render_signals([bullish_signal, bearish_signal])

    # Both must be visible
    assert bullish_signal.id in display
    assert bearish_signal.id in display

    # Neither should be visually de-emphasised
    assert 'hidden' not in get_signal_css(bullish_signal)
    assert 'hidden' not in get_signal_css(bearish_signal)
    assert 'opacity' not in get_signal_css(bullish_signal)
    assert 'opacity' not in get_signal_css(bearish_signal)
```

---

# DOCUMENT METADATA

```yaml
document_id: GSUF-TIER2-FIN-001
version: 1.0.0
type: Domain Adapter
domain: Financial Services
parent_framework: GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0

applicable_to:
  - Trading platforms
  - Investment signal aggregators
  - Market analysis tools
  - Portfolio tracking applications
  - Financial decision-support systems

constitutional_rules:
  - CR-001: Decision-Support Only
  - CR-002: Never Resolve Contradictions
  - CR-003: Descriptive Not Prescriptive

regulatory_alignment:
  - SEC (Securities and Exchange Commission)
  - FINRA (Financial Industry Regulatory Authority)
  - MiFID II (Markets in Financial Instruments Directive)
  - FCA COBS (Financial Conduct Authority)
  - SOX Section 404

usage:
  This adapter is used in conjunction with:
  1. TIER 1: GOLD_STANDARD_UNIFIED_FRAMEWORK_v3.0.md (methodology)
  2. TIER 3: [PROJECT]_AUDIT_CONFIGURATION.md (project-specific)
```

---

**END OF DOCUMENT**

*Financial Services Domain Adapter v1.0*
*Gold Standard Framework Extension*
*For Trading & Investment Applications*
