# HANDOFF_03: CONSTITUTIONAL RULES

**THESE RULES ARE INVIOLABLE**
**ANY VIOLATION RENDERS THE APPLICATION NON-COMPLIANT**

---

## OVERVIEW

CIA-SIE is a **Data Repository Platform**, NOT an Intelligence Engine. This distinction is fundamental and governs every design decision.

---

## THE THREE CONSTITUTIONAL PRINCIPLES

### PRINCIPLE 1: Decision-Support, NOT Decision-Making

**WHAT THIS MEANS:**
- The system provides INFORMATION for the user to interpret
- The system NEVER suggests, recommends, or implies action
- All decisions remain 100% with the user

**FORBIDDEN PATTERNS:**

```
❌ "Based on the signals, you should consider buying"
❌ "The bullish consensus suggests a long position"
❌ "This is a good entry point"
❌ "You might want to wait for confirmation"
❌ Any form of "should", "recommend", "suggest", "consider"
```

**REQUIRED PATTERNS:**

```
✅ "Chart 01A shows BULLISH, Chart 02 shows BEARISH"
✅ "3 of 12 charts currently display bullish signals"
✅ "The interpretation and any decision is entirely yours"
```

---

### PRINCIPLE 2: Expose Contradictions, NEVER Resolve Them

**WHAT THIS MEANS:**
- When charts disagree, SHOW BOTH SIDES
- Never suggest which chart is "correct" or "more reliable"
- Never weight or prioritize one signal over another
- Never aggregate conflicting signals into a summary

**FORBIDDEN PATTERNS:**

```
❌ "Despite the bearish signal from Chart 02, the overall picture is bullish"
❌ "Chart 01A is more reliable because..."
❌ "The majority of charts show bullish, so..."
❌ "Weighing the signals, the balance favors..."
❌ Any form of conflict resolution
```

**REQUIRED PATTERNS:**

```
✅ "CONTRADICTION DETECTED: Chart 01A (BULLISH) vs Chart 02 (BEARISH)"
✅ "This contradiction is shown for your awareness. The system does NOT resolve this conflict."
✅ Display both charts with equal visual prominence
```

**UI REQUIREMENT:**
When displaying a contradiction, BOTH sides must have:
- Equal visual size
- Equal styling prominence
- No visual cues suggesting one is "better"

---

### PRINCIPLE 3: Descriptive AI, NOT Prescriptive AI

**WHAT THIS MEANS:**
- AI narratives DESCRIBE what the data shows
- AI narratives NEVER PRESCRIBE what to do
- Every AI narrative MUST end with the standard disclaimer

**FORBIDDEN AI OUTPUTS:**

```
❌ "I recommend..."
❌ "You should..."
❌ "The best action would be..."
❌ "Consider..."
❌ "A prudent approach would be..."
❌ "The signals suggest you..."
```

**REQUIRED AI DISCLAIMER:**
Every AI-generated narrative MUST end with:

```
"This is a description of what your charts are showing.
The interpretation and any decision is entirely yours."
```

This disclaimer is NON-NEGOTIABLE and must appear verbatim.

---

## PROHIBITED FEATURES

The following features are CONSTITUTIONALLY PROHIBITED and must NEVER be implemented:

### 1. NO Signal Scoring
```
❌ confidence: 0.85
❌ strength: "HIGH"
❌ quality: 4/5
❌ reliability: "EXCELLENT"
```

Scores imply system judgment about signal quality. This is prohibited.

### 2. NO Chart Weighting
```
❌ weight: 2.5
❌ importance: "HIGH"
❌ priority: 1
```

All charts have EQUAL standing. Weights imply some charts matter more.

### 3. NO Aggregation
```
❌ "Overall: BULLISH"
❌ "Net sentiment: +3"
❌ "Consensus: BEARISH"
❌ bullishCount: 7, bearishCount: 5
```

Aggregation implies a system opinion. Show individual charts only.

### 4. NO Recommendations
```
❌ "Suggested action: BUY"
❌ "Recommendation: WAIT"
❌ <BuyButton /> or <SellButton />
```

Action buttons or recommendations imply system guidance.

### 5. NO Predictions
```
❌ "Expected direction: UP"
❌ "Probability of rise: 65%"
❌ "Forecast: BULLISH"
```

Predictions imply system knows the future. It doesn't.

---

## REQUIRED FEATURES

### 1. Freshness Indicators
Every signal display MUST show how current the data is:
- `CURRENT` (≤2 min) - Green
- `RECENT` (≤10 min) - Yellow
- `STALE` (>30 min) - Red
- `UNAVAILABLE` (never received) - Gray

### 2. Constitutional Banner
The dashboard MUST display the three constitutional principles prominently.

### 3. Contradiction Alerts
When charts disagree, display a clear visual alert showing BOTH positions.

### 4. AI Disclaimer
Every AI narrative MUST end with the standard disclaimer.

---

## CODE REVIEW CHECKLIST

Before submitting any code, verify:

- [ ] No "should", "recommend", "suggest" in any user-facing text
- [ ] No signal scores or confidence values displayed
- [ ] No chart weights or priorities displayed
- [ ] No aggregation of signals (counts, percentages, consensus)
- [ ] Contradictions shown with equal visual weight to both sides
- [ ] AI narratives end with required disclaimer
- [ ] No action buttons (buy/sell/enter/exit)
- [ ] No predictions or forecasts
- [ ] Freshness indicators on all signals
- [ ] Constitutional banner visible on dashboard

---

## EXAMPLE: CORRECT VS INCORRECT UI

### INCORRECT (Violates Constitution)
```jsx
// ❌ WRONG - Aggregates and suggests
<Dashboard>
  <OverallSentiment value="BULLISH" confidence={0.85} />
  <Recommendation>Consider entering long position</Recommendation>
  <SignalStrength chart="01A" weight={2.5} />
</Dashboard>
```

### CORRECT (Compliant)
```jsx
// ✅ CORRECT - Descriptive only
<Dashboard>
  <ConstitutionalBanner />
  <SignalGrid>
    {charts.map(chart => (
      <ChartCard
        key={chart.chart_id}
        direction={chart.latest_signal?.direction}
        freshness={chart.freshness}
        // NO weight, NO score, NO recommendation
      />
    ))}
  </SignalGrid>
  <ContradictionAlerts contradictions={contradictions} />
  <NarrativePanel
    narrative={narrative}
    disclaimer="This is a description of what your charts are showing. The interpretation and any decision is entirely yours."
  />
</Dashboard>
```

---

## FINAL NOTE

These rules exist because CIA-SIE is designed as a DECISION-SUPPORT tool, not a DECISION-MAKING tool. The user is a sophisticated trader who:

1. Has their own trading methodology
2. Wants to see their data organized, not interpreted
3. Makes their own decisions based on their experience
4. Does NOT want the system to "think for them"

Respecting these constitutional principles respects the user's autonomy and expertise.
