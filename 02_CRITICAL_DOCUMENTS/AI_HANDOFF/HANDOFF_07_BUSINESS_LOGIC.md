# HANDOFF_07: BUSINESS LOGIC ALGORITHMS

**Purpose:** Define core algorithms for signal processing, freshness calculation, and relationship detection
**Governance:** Gold Standard Specification v2.0.0

---

## 1. SIGNAL FRESHNESS CALCULATION

### Algorithm Overview

Signal freshness indicates how current a signal is. This is critical for user awareness.

### Threshold Configuration

Thresholds are configurable per silo:

| Status | Default Threshold | Description |
|--------|-------------------|-------------|
| CURRENT | ≤ 2 minutes | Signal is fresh and reliable |
| RECENT | ≤ 10 minutes | Signal is relatively recent |
| STALE | > 30 minutes | Signal is outdated, use with caution |
| UNAVAILABLE | No signal | No signal has ever been received |

### Implementation

```python
# Backend (Python)
from datetime import datetime, timedelta
from enum import Enum

class FreshnessStatus(Enum):
    CURRENT = "CURRENT"
    RECENT = "RECENT"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"

def calculate_freshness(
    signal_timestamp: datetime | None,
    current_threshold_min: int = 2,
    recent_threshold_min: int = 10,
    stale_threshold_min: int = 30
) -> FreshnessStatus:
    """
    Calculate signal freshness based on age.

    Args:
        signal_timestamp: When the signal was received (None if never)
        current_threshold_min: Minutes for CURRENT status
        recent_threshold_min: Minutes for RECENT status
        stale_threshold_min: Minutes for STALE status (beyond this = STALE)

    Returns:
        FreshnessStatus enum value
    """
    if signal_timestamp is None:
        return FreshnessStatus.UNAVAILABLE

    now = datetime.utcnow()
    age = now - signal_timestamp
    age_minutes = age.total_seconds() / 60

    if age_minutes <= current_threshold_min:
        return FreshnessStatus.CURRENT
    elif age_minutes <= recent_threshold_min:
        return FreshnessStatus.RECENT
    else:
        return FreshnessStatus.STALE
```

```typescript
// Frontend (TypeScript)
type FreshnessStatus = 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'

interface FreshnessThresholds {
  currentMinutes: number  // default: 2
  recentMinutes: number   // default: 10
  staleMinutes: number    // default: 30
}

const calculateFreshness = (
  signalTimestamp: string | null,
  thresholds: FreshnessThresholds = { currentMinutes: 2, recentMinutes: 10, staleMinutes: 30 }
): FreshnessStatus => {
  if (!signalTimestamp) {
    return 'UNAVAILABLE'
  }

  const now = new Date()
  const signalTime = new Date(signalTimestamp)
  const ageMinutes = (now.getTime() - signalTime.getTime()) / (1000 * 60)

  if (ageMinutes <= thresholds.currentMinutes) {
    return 'CURRENT'
  } else if (ageMinutes <= thresholds.recentMinutes) {
    return 'RECENT'
  } else {
    return 'STALE'
  }
}
```

---

## 2. CONTRADICTION DETECTION

### Definition

A **contradiction** occurs when two charts in the same silo show opposing directions:
- Chart A: BULLISH vs Chart B: BEARISH
- Chart A: BEARISH vs Chart B: BULLISH

NEUTRAL signals do NOT create contradictions.

### Algorithm

```python
# Backend (Python)
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class ChartSignal:
    chart_id: str
    chart_code: str
    chart_name: str
    direction: str  # 'BULLISH', 'BEARISH', 'NEUTRAL'
    freshness: str

@dataclass
class Contradiction:
    chart_a_id: str
    chart_a_code: str
    chart_a_name: str
    chart_a_direction: str
    chart_b_id: str
    chart_b_code: str
    chart_b_name: str
    chart_b_direction: str
    detected_at: datetime

def detect_contradictions(signals: List[ChartSignal]) -> List[Contradiction]:
    """
    Detect all contradictions between chart signals.

    A contradiction exists when:
    - Two charts have opposing directions (BULLISH vs BEARISH)
    - NEUTRAL signals do not create contradictions

    Returns:
        List of Contradiction objects (unordered, no priority)
    """
    contradictions = []

    # Filter to only BULLISH and BEARISH signals
    directional_signals = [s for s in signals if s.direction in ('BULLISH', 'BEARISH')]

    # Compare all pairs
    for i, signal_a in enumerate(directional_signals):
        for signal_b in directional_signals[i+1:]:
            # Check for opposition
            if (signal_a.direction == 'BULLISH' and signal_b.direction == 'BEARISH') or \
               (signal_a.direction == 'BEARISH' and signal_b.direction == 'BULLISH'):

                contradictions.append(Contradiction(
                    chart_a_id=signal_a.chart_id,
                    chart_a_code=signal_a.chart_code,
                    chart_a_name=signal_a.chart_name,
                    chart_a_direction=signal_a.direction,
                    chart_b_id=signal_b.chart_id,
                    chart_b_code=signal_b.chart_code,
                    chart_b_name=signal_b.chart_name,
                    chart_b_direction=signal_b.direction,
                    detected_at=datetime.utcnow()
                ))

    return contradictions
```

### CRITICAL RULES

1. **NO RESOLUTION:** Contradictions are NEVER resolved by the system
2. **EQUAL DISPLAY:** Both charts in a contradiction must be displayed with equal prominence
3. **NO PRIORITY:** Do not suggest which chart is "more correct"
4. **NO WEIGHTING:** Do not weight contradictions by chart importance

---

## 3. CONFIRMATION DETECTION

### Definition

A **confirmation** occurs when two or more charts in the same silo show the same direction:
- Chart A: BULLISH + Chart B: BULLISH = Confirmation
- Chart A: BEARISH + Chart B: BEARISH = Confirmation

NEUTRAL signals do NOT create confirmations.

### Algorithm

```python
# Backend (Python)
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Confirmation:
    chart_ids: List[str]
    chart_codes: List[str]
    chart_names: List[str]
    aligned_direction: str  # 'BULLISH' or 'BEARISH'
    detected_at: datetime

def detect_confirmations(signals: List[ChartSignal]) -> List[Confirmation]:
    """
    Detect all confirmations between chart signals.

    A confirmation exists when:
    - Two or more charts show the same direction (BULLISH or BEARISH)
    - NEUTRAL signals do not create confirmations

    Returns:
        List of Confirmation objects (one per direction with all aligned charts)
    """
    confirmations = []

    # Group by direction
    bullish_signals = [s for s in signals if s.direction == 'BULLISH']
    bearish_signals = [s for s in signals if s.direction == 'BEARISH']

    # Create confirmation for BULLISH if 2+ charts
    if len(bullish_signals) >= 2:
        confirmations.append(Confirmation(
            chart_ids=[s.chart_id for s in bullish_signals],
            chart_codes=[s.chart_code for s in bullish_signals],
            chart_names=[s.chart_name for s in bullish_signals],
            aligned_direction='BULLISH',
            detected_at=datetime.utcnow()
        ))

    # Create confirmation for BEARISH if 2+ charts
    if len(bearish_signals) >= 2:
        confirmations.append(Confirmation(
            chart_ids=[s.chart_id for s in bearish_signals],
            chart_codes=[s.chart_code for s in bearish_signals],
            chart_names=[s.chart_name for s in bearish_signals],
            aligned_direction='BEARISH',
            detected_at=datetime.utcnow()
        ))

    return confirmations
```

### CRITICAL RULES

1. **DESCRIPTIVE ONLY:** Confirmations describe alignment, NOT trading signals
2. **NO STRENGTH:** Do not assign "strength" to confirmations
3. **NO COUNT WEIGHTING:** 5 confirming charts is not "better" than 2

---

## 4. WEBHOOK SIGNAL PROCESSING

### Webhook Payload Format

TradingView sends webhooks in this format:

```json
{
  "webhook_id": "SAMPLE_01A",
  "direction": "BULLISH",
  "timestamp": "2025-12-30T10:00:00Z",
  "indicators": {
    "rsi": 35,
    "macd": "crossing_up"
  }
}
```

### Processing Algorithm

```python
# Backend (Python)
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any

class WebhookPayload(BaseModel):
    webhook_id: str
    direction: str
    timestamp: Optional[str] = None
    indicators: Optional[Dict[str, Any]] = None

    @validator('direction')
    def validate_direction(cls, v):
        valid_directions = {'BULLISH', 'BEARISH', 'NEUTRAL'}
        if v.upper() not in valid_directions:
            raise ValueError(f'direction must be one of {valid_directions}')
        return v.upper()

    @validator('webhook_id')
    def validate_webhook_id(cls, v):
        # webhook_id format: {SYMBOL}_{CHART_CODE}
        # e.g., SAMPLE_01A, SAMPLE_02
        if not v or '_' not in v:
            raise ValueError('webhook_id must be in format SYMBOL_CHARTCODE')
        return v

async def process_webhook(payload: WebhookPayload) -> Signal:
    """
    Process incoming webhook and create signal.

    Steps:
    1. Validate payload
    2. Find chart by webhook_id
    3. Create signal record
    4. Trigger relationship recalculation
    5. Return created signal
    """
    # 1. Find chart
    chart = await get_chart_by_webhook_id(payload.webhook_id)
    if not chart:
        raise NotFoundException(f"No chart found for webhook_id: {payload.webhook_id}")

    # 2. Determine signal type
    latest_signal = await get_latest_signal(chart.chart_id)
    if latest_signal and latest_signal.direction == payload.direction:
        signal_type = SignalType.HEARTBEAT  # Same direction = heartbeat
    else:
        signal_type = SignalType.STATE_CHANGE  # Direction changed

    # 3. Create signal
    signal = Signal(
        chart_id=chart.chart_id,
        signal_type=signal_type,
        direction=payload.direction,
        signal_timestamp=payload.timestamp or datetime.utcnow(),
        indicators=payload.indicators,
        raw_payload=payload.dict()
    )
    await save_signal(signal)

    # 4. Trigger relationship recalculation (async)
    await recalculate_relationships(chart.silo_id)

    return signal
```

---

## 5. NARRATIVE GENERATION

### Structure

AI-generated narratives follow a strict structure:

```
1. SIGNAL SUMMARY
   - Count of current signals
   - Overview of directions

2. CONTRADICTION SECTION (if any)
   - List each contradiction
   - No resolution or preference

3. CONFIRMATION SECTION (if any)
   - List aligned charts
   - No strength indication

4. FRESHNESS SECTION
   - Note any stale signals
   - Note any unavailable signals

5. MANDATORY DISCLAIMER
   "This is a description of what your charts are showing.
   The interpretation and any decision is entirely yours."
```

### Algorithm

```python
# Backend (Python)
from typing import List

@dataclass
class NarrativeSection:
    section_type: str  # 'SIGNAL_SUMMARY', 'CONTRADICTION', 'CONFIRMATION', 'FRESHNESS'
    content: str
    referenced_chart_ids: List[str]

MANDATORY_DISCLAIMER = """This is a description of what your charts are showing.
The interpretation and any decision is entirely yours."""

async def generate_narrative(
    silo_id: str,
    use_ai: bool = True,
    model: str = "claude-3-sonnet"
) -> Narrative:
    """
    Generate narrative for a silo.

    Args:
        silo_id: The silo to generate for
        use_ai: Whether to use Claude AI (True) or template (False)
        model: Claude model to use if use_ai=True

    Returns:
        Narrative with sections and mandatory disclaimer
    """
    # Get data
    signals = await get_signals_for_silo(silo_id)
    contradictions = detect_contradictions(signals)
    confirmations = detect_confirmations(signals)

    sections = []

    # 1. Signal Summary
    current_count = sum(1 for s in signals if s.freshness == 'CURRENT')
    total_count = len(signals)
    bullish_count = sum(1 for s in signals if s.direction == 'BULLISH')
    bearish_count = sum(1 for s in signals if s.direction == 'BEARISH')

    summary_content = f"Currently, {current_count} of {total_count} charts have current signals. "
    summary_content += f"{bullish_count} show BULLISH, {bearish_count} show BEARISH."

    sections.append(NarrativeSection(
        section_type='SIGNAL_SUMMARY',
        content=summary_content,
        referenced_chart_ids=[s.chart_id for s in signals]
    ))

    # 2. Contradictions
    if contradictions:
        for c in contradictions:
            content = f"Chart {c.chart_a_code} ({c.chart_a_direction}) contradicts "
            content += f"Chart {c.chart_b_code} ({c.chart_b_direction})."
            sections.append(NarrativeSection(
                section_type='CONTRADICTION',
                content=content,
                referenced_chart_ids=[c.chart_a_id, c.chart_b_id]
            ))

    # 3. Confirmations
    if confirmations:
        for c in confirmations:
            codes = ', '.join(c.chart_codes)
            content = f"Charts {codes} all show {c.aligned_direction} alignment."
            sections.append(NarrativeSection(
                section_type='CONFIRMATION',
                content=content,
                referenced_chart_ids=c.chart_ids
            ))

    # 4. Freshness
    stale_signals = [s for s in signals if s.freshness == 'STALE']
    unavailable_signals = [s for s in signals if s.freshness == 'UNAVAILABLE']

    if stale_signals:
        codes = ', '.join(s.chart_code for s in stale_signals)
        sections.append(NarrativeSection(
            section_type='FRESHNESS',
            content=f"Charts {codes} have stale data.",
            referenced_chart_ids=[s.chart_id for s in stale_signals]
        ))

    if unavailable_signals:
        codes = ', '.join(s.chart_code for s in unavailable_signals)
        sections.append(NarrativeSection(
            section_type='FRESHNESS',
            content=f"Charts {codes} have no signal data.",
            referenced_chart_ids=[s.chart_id for s in unavailable_signals]
        ))

    # If using AI, enhance with Claude
    if use_ai:
        sections = await enhance_with_ai(sections, model)

    return Narrative(
        silo_id=silo_id,
        sections=sections,
        closing_statement=MANDATORY_DISCLAIMER,
        generated_at=datetime.utcnow()
    )
```

---

## 6. AI RESPONSE VALIDATION

### Purpose

All AI responses MUST be validated before returning to user to ensure constitutional compliance.

### Prohibited Patterns

```python
# Backend (Python)
import re
from typing import Tuple

PROHIBITED_PATTERNS = [
    (r'\bshould\b', "Contains 'should' - implies recommendation"),
    (r'\brecommend\b', "Contains 'recommend' - direct recommendation"),
    (r'\bsuggest\b', "Contains 'suggest' - implies recommendation"),
    (r'\bconsider\b', "Contains 'consider' - implies recommendation"),
    (r'\bbuy\b.*\bnow\b', "Contains 'buy now' - trading advice"),
    (r'\bsell\b.*\bnow\b', "Contains 'sell now' - trading advice"),
    (r'\bconfidence\b.*\d+%', "Contains confidence percentage"),
    (r'\bprobability\b', "Contains probability - implies prediction"),
    (r'\blikely\b.*\bprofit\b', "Contains profit prediction"),
    (r'\brisk\s*score\b', "Contains risk score"),
    (r'\brating\b.*\d+', "Contains numerical rating"),
]

MANDATORY_DISCLAIMER = "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."

def validate_ai_response(response: str) -> Tuple[bool, str | None]:
    """
    Validate AI response for constitutional compliance.

    Args:
        response: The AI-generated text

    Returns:
        Tuple of (is_valid, violation_reason)
    """
    # Check for prohibited patterns
    for pattern, reason in PROHIBITED_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return (False, reason)

    # Check for mandatory disclaimer
    if MANDATORY_DISCLAIMER not in response:
        return (False, "Missing mandatory disclaimer")

    return (True, None)

async def get_validated_ai_response(prompt: str, model: str) -> str:
    """
    Get AI response with validation and retry.

    If response fails validation, regenerate with stricter prompt.
    Maximum 3 attempts before falling back to template.
    """
    for attempt in range(3):
        response = await call_claude_api(prompt, model)

        is_valid, reason = validate_ai_response(response)
        if is_valid:
            return response

        # Log violation and retry with stricter prompt
        logger.warning(f"AI response failed validation: {reason}. Attempt {attempt + 1}/3")
        prompt = add_stricter_constraints(prompt, reason)

    # Fallback to template response
    return generate_template_response()
```

---

## 7. DYNAMIC MODEL SELECTION

### Selection Algorithm

```python
# Backend (Python)
from enum import Enum

class ClaudeModel(Enum):
    HAIKU = "claude-3-haiku"
    SONNET = "claude-3-sonnet"
    OPUS = "claude-opus-4"

def select_model(
    user_specified: str | None,
    token_estimate: int,
    charts_involved: int,
    complexity: str  # 'simple', 'standard', 'complex'
) -> ClaudeModel:
    """
    Dynamically select appropriate Claude model.

    Priority:
    1. User override (if specified)
    2. Token-based selection
    3. Complexity-based selection
    4. Default to Sonnet
    """
    # 1. User override always wins
    if user_specified:
        try:
            return ClaudeModel(user_specified)
        except ValueError:
            pass  # Invalid model, continue to auto-select

    # 2. Token-based selection
    if token_estimate < 500:
        return ClaudeModel.HAIKU

    # 3. Complexity-based selection
    if charts_involved > 6:
        return ClaudeModel.OPUS

    if complexity == 'complex':
        return ClaudeModel.OPUS

    if complexity == 'simple':
        return ClaudeModel.HAIKU

    # 4. Default
    return ClaudeModel.SONNET
```

---

## 8. COST CALCULATION

### Token Costs (as of 2025)

| Model | Input (per 1K) | Output (per 1K) |
|-------|----------------|-----------------|
| Haiku | $0.00025 | $0.00125 |
| Sonnet | $0.003 | $0.015 |
| Opus | $0.015 | $0.075 |

### Algorithm

```python
# Backend (Python)
from decimal import Decimal

MODEL_COSTS = {
    "claude-3-haiku": {
        "input": Decimal("0.00025"),
        "output": Decimal("0.00125")
    },
    "claude-3-sonnet": {
        "input": Decimal("0.003"),
        "output": Decimal("0.015")
    },
    "claude-opus-4": {
        "input": Decimal("0.015"),
        "output": Decimal("0.075")
    }
}

def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int
) -> Decimal:
    """
    Calculate cost for an AI request.

    Args:
        model: Model ID
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Cost in USD as Decimal
    """
    costs = MODEL_COSTS.get(model, MODEL_COSTS["claude-3-sonnet"])

    input_cost = (Decimal(input_tokens) / 1000) * costs["input"]
    output_cost = (Decimal(output_tokens) / 1000) * costs["output"]

    return (input_cost + output_cost).quantize(Decimal("0.00001"))
```

---

## 9. BUDGET MANAGEMENT

### Alert Thresholds

| Threshold | Action |
|-----------|--------|
| 80% | Display warning banner (dismissible) |
| 90% | Display critical banner (not dismissible) |
| 100% | Block AI requests, show modal |

### Algorithm

```python
# Backend (Python)
from enum import Enum

class BudgetStatus(Enum):
    OK = "ok"
    WARNING = "warning"      # 80%
    CRITICAL = "critical"    # 90%
    EXHAUSTED = "exhausted"  # 100%

def check_budget_status(
    used: Decimal,
    limit: Decimal,
    warning_threshold: int = 80,
    critical_threshold: int = 90
) -> BudgetStatus:
    """
    Check current budget status.
    """
    if limit <= 0:
        return BudgetStatus.OK  # Unlimited

    percentage = (used / limit) * 100

    if percentage >= 100:
        return BudgetStatus.EXHAUSTED
    elif percentage >= critical_threshold:
        return BudgetStatus.CRITICAL
    elif percentage >= warning_threshold:
        return BudgetStatus.WARNING
    else:
        return BudgetStatus.OK

async def can_make_ai_request(
    estimated_cost: Decimal,
    require_confirmation: bool = False
) -> Tuple[bool, str | None]:
    """
    Check if an AI request can be made.

    Returns:
        Tuple of (allowed, reason_if_blocked)
    """
    usage = await get_current_usage()
    budget = await get_budget_limit()

    status = check_budget_status(usage.total_cost, budget.limit)

    if status == BudgetStatus.EXHAUSTED:
        return (False, "Monthly budget exhausted")

    if status == BudgetStatus.CRITICAL and not require_confirmation:
        return (False, "Budget critical - confirmation required")

    projected = usage.total_cost + estimated_cost
    if projected > budget.limit:
        return (False, "Request would exceed budget")

    return (True, None)
```

---

## 10. 12 SAMPLE CHARTS REFERENCE

### Static Chart Configuration

```typescript
// Frontend constant
const SAMPLE_CHARTS = [
  { code: '01A', name: 'Momentum Health', timeframe: 'Daily', webhookId: 'SAMPLE_01A' },
  { code: '02', name: 'HTF Structure', timeframe: 'Weekly', webhookId: 'SAMPLE_02' },
  { code: '04A', name: 'Risk Extension', timeframe: '3H', webhookId: 'SAMPLE_04A' },
  { code: '04B', name: 'Support/Resistance', timeframe: '3H', webhookId: 'SAMPLE_04B' },
  { code: '05A', name: 'VWAP Execution', timeframe: 'Daily', webhookId: 'SAMPLE_05A' },
  { code: '05B', name: 'Momentum Exhaustion', timeframe: 'Daily', webhookId: 'SAMPLE_05B' },
  { code: '05C', name: 'Extension Risk', timeframe: 'Daily', webhookId: 'SAMPLE_05C' },
  { code: '05D', name: 'VWAP Deviation', timeframe: 'Daily', webhookId: 'SAMPLE_05D' },
  { code: '06', name: 'Macro Correlation', timeframe: 'Daily', webhookId: 'SAMPLE_06' },
  { code: '07', name: 'Primary Trend', timeframe: 'Daily', webhookId: 'SAMPLE_07' },
  { code: '08', name: 'Volume Analysis', timeframe: 'Daily', webhookId: 'SAMPLE_08' },
  { code: '09', name: 'Order Flow', timeframe: 'Daily', webhookId: 'SAMPLE_09' },
] as const
```

---

## SUMMARY: ALGORITHM CHECKLIST

| Algorithm | Location | Critical Rules |
|-----------|----------|----------------|
| Freshness Calculation | Backend + Frontend | Use configurable thresholds per silo |
| Contradiction Detection | Backend | NEVER resolve, display with equal prominence |
| Confirmation Detection | Backend | NEVER assign strength or priority |
| Webhook Processing | Backend | Validate direction, find chart by webhook_id |
| Narrative Generation | Backend | ALWAYS include mandatory disclaimer |
| AI Response Validation | Backend | Reject prohibited patterns |
| Model Selection | Backend | User override takes priority |
| Cost Calculation | Backend | Use current model pricing |
| Budget Management | Backend + Frontend | Alert at 80%, 90%, block at 100% |
