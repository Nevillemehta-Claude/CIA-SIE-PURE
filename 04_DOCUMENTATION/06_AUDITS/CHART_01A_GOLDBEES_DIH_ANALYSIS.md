# CHART 01A: GOLDBEES-DIH (Daily Institutional Health)

## Deep Analysis Report

**Generated**: 2026-01-12  
**Analyst**: CIA-SIE System  
**Methodology**: Institutional-Grade, Surgical Precision

---

## 1. FILE INVENTORY

| File | Type | Purpose | Status |
|------|------|---------|--------|
| `GOLDBEES_2026-01-12_22-12-22.png` | Screenshot | Visual chart capture | ✅ Analyzed |
| `NSE_GOLDBEES, 1D.csv` | Data Export | 300 rows, 31 columns | ✅ Analyzed |
| `Pine Code - CHART 01A.docx` | Pine Script | PRIMARY_SIGNAL indicator | ⏳ Pending extraction |
| `GOLDBEES MOMENTUM HEALTH INDICATOR.docx` | Pine Script | MOM-HEALTH indicator | ⏳ Pending extraction |

---

## 2. CHART CONFIGURATION

### 2.1 Instrument Details

| Attribute | Value |
|-----------|-------|
| **Symbol** | NSE:GOLDBEES |
| **Name** | Nippon India ETF Gold BeES |
| **Timeframe** | 1D (Daily) |
| **Exchange** | NSE (National Stock Exchange of India) |
| **Asset Class** | Gold ETF |
| **Data Range** | Oct 29, 2024 → Jan 12, 2026 (300 bars) |

### 2.2 Indicators On Chart

From visual inspection:

| Indicator | Type | Location |
|-----------|------|----------|
| HTF Trend Tracker [BigBeluga] | External | Main Panel |
| Previous Day High/Low + Separators | External | Main Panel |
| 52W (Highs/Lows) | Custom | Main Panel |
| OB 3H (3) | Custom | Main Panel |
| MOM-HEALTH | Custom | Label Panel |
| PMIE: PRIMARY_SIGNAL [GOLD_01A] | Custom | Main + Label |
| RSI (14, close) | Built-in | Panel 1 |
| MACD (12, 26, close) | Built-in | Panel 2 |

---

## 3. DATA STRUCTURE ANALYSIS

### 3.1 CSV Column Schema (31 columns)

```
OHLC Data:
├── time              (DateTime) - Bar timestamp
├── open              (Float) - Opening price
├── high              (Float) - High price
├── low               (Float) - Low price
└── close             (Float) - Closing price

Moving Averages:
├── EMA 20            (Float) - 20-period EMA
├── EMA 50            (Float) - 50-period EMA
└── EMA 200           (Float) - 200-period EMA

Risk Management:
└── Invalidation      (Float) - Stop loss / invalidation level

Signal Flags:
├── Bearish Divergence (0/1) - RSI bearish divergence flag
├── Bullish Divergence (0/1) - RSI bullish divergence flag
├── MACD Bull Cross   (0/1) - MACD bullish crossover
├── MACD Bear Cross   (0/1) - MACD bearish crossover
├── Bearish OB        (0/1) - Bearish order block detected
└── Bullish OB        (0/1) - Bullish order block detected

Sentiment:
└── Sentiment Line    (Empty) - DATA GAP - needs fix

Candle Overlay:
├── Candles (Open)    (Float) - Duplicate of open
├── Candles (High)    (Float) - Duplicate of high
├── Candles (Low)     (Float) - Duplicate of low
└── Candles (Close)   (Float) - Duplicate of close

Trend:
└── Trend             (Float) - Constant 10.225 - unclear purpose

52 Week:
├── 52 Week High      (Empty) - DATA GAP - needs fix
└── 52 Week Low       (Empty) - DATA GAP - needs fix

RSI Data:
├── RSI               (Float) - RSI(14) value
├── RSI-based MA      (Float) - Moving average of RSI
├── Regular Bullish   (Float) - Bullish divergence value
├── Regular Bullish Label (Float) - Label position
├── Regular Bearish   (Float) - Bearish divergence value
└── Regular Bearish Label (Float) - Label position

MACD Data:
├── Histogram         (Float) - MACD histogram
├── MACD              (Float) - MACD line
└── Signal            (Float) - Signal line
```

### 3.2 Data Quality Assessment

| Status | Column(s) | Issue | Impact |
|--------|-----------|-------|--------|
| ⚠️ EMPTY | `Sentiment Line` | No data exported | Missing sentiment analysis |
| ⚠️ EMPTY | `52 Week High` | No data exported | Missing context |
| ⚠️ EMPTY | `52 Week Low` | No data exported | Missing context |
| ❓ UNCLEAR | `Trend` | Constant 10.225 | Purpose unknown |
| ✅ OK | All other columns | Data present | Functional |

---

## 4. LATEST DATA POINT (Jan 12, 2026)

### 4.1 Price Action

| Metric | Value | Change |
|--------|-------|--------|
| **Open** | ₹115.70 | — |
| **High** | ₹117.00 | NEW 52W HIGH |
| **Low** | ₹114.81 | — |
| **Close** | ₹116.76 | +₹3.15 (+2.77%) |

### 4.2 Technical Indicators

| Indicator | Value | Signal |
|-----------|-------|--------|
| **EMA 20** | 111.69 | Price above ✅ |
| **EMA 50** | 107.59 | Price above ✅ |
| **EMA 200** | 92.70 | Price above ✅ |
| **EMA Stack** | Perfect alignment | 🟢 BULLISH |
| **Invalidation** | 109.70 | -6.0% from current |

### 4.3 Momentum Indicators

| Indicator | Value | Zone | Signal |
|-----------|-------|------|--------|
| **RSI(14)** | 71.82 | Overbought (>70) | ⚠️ CAUTION |
| **RSI MA** | 65.37 | Neutral | — |
| **MACD Line** | 2.01 | Positive | 🟢 BULLISH |
| **Signal Line** | 1.95 | — | — |
| **Histogram** | +0.07 | Positive | 🟢 BULLISH |

### 4.4 Active Signals

| Signal | Status | Bar Date |
|--------|--------|----------|
| **MACD Bull Cross** | ✅ ACTIVE | 2026-01-12 |
| **Bearish Divergence** | ❌ Inactive | — |
| **Bullish Divergence** | ❌ Inactive | — |
| **Bearish OB** | ❌ Inactive | — |
| **Bullish OB** | ❌ Inactive | — |

---

## 5. SIGNAL HISTORY ANALYSIS

### 5.1 MACD Bull Crosses (Last 10)

| Date | Close | Subsequent Performance |
|------|-------|----------------------|
| 2026-01-12 | 116.76 | Current |
| 2025-11-27 | 104.11 | +12.1% to now |
| 2025-11-13 | 105.37 | Followed by pullback |
| 2025-09-09 | 91.17 | +28.0% to now |
| 2025-08-28 | 84.42 | +38.3% to now |
| 2025-08-04 | 83.23 | +40.3% to now |
| 2025-07-15 | 81.67 | +43.0% to now |
| 2025-06-03 | 80.97 | +44.2% to now |
| 2025-04-11 | 77.90 | +49.9% to now |
| 2025-04-01 | 76.72 | +52.2% to now |

### 5.2 Order Block Events (Last 10)

| Date | Type | Price Level |
|------|------|-------------|
| 2025-12-30 | Bearish OB | 111.17 |
| 2025-12-15 | Bearish OB | 110.95 |
| 2025-12-05 | Bearish OB | 106.89 |
| 2025-11-17 | Bearish OB | 101.94 |
| 2025-11-12 | Bearish OB | 102.69 |
| 2025-10-23 | Bullish OB | 101.70 |
| 2025-09-24 | Bearish OB | 94.64 |
| 2025-09-05 | Bearish OB | 88.65 |
| 2025-08-11 | Bearish OB | 83.23 |
| 2025-07-14 | Bearish OB | 81.88 |

---

## 6. WEBHOOK PAYLOAD DESIGN

### 6.1 Proposed JSON Schema

```json
{
  "chart_id": "CHART_01A",
  "instrument": "NSE:GOLDBEES",
  "timeframe": "1D",
  "timestamp": "{{time}}",
  "timestamp_iso": "{{timenow}}",
  
  "price": {
    "open": {{open}},
    "high": {{high}},
    "low": {{low}},
    "close": {{close}}
  },
  
  "ema": {
    "ema20": {{plot("EMA 20")}},
    "ema50": {{plot("EMA 50")}},
    "ema200": {{plot("EMA 200")}}
  },
  
  "risk": {
    "invalidation": {{plot("Invalidation")}},
    "distance_pct": {{(close - plot("Invalidation")) / close * 100}}
  },
  
  "rsi": {
    "value": {{plot("RSI")}},
    "ma": {{plot("RSI-based MA")}},
    "zone": "{{rsi_zone}}"
  },
  
  "macd": {
    "line": {{plot("MACD")}},
    "signal": {{plot("Signal")}},
    "histogram": {{plot("Histogram")}}
  },
  
  "signals": {
    "macd_bull_cross": {{macd_bull_cross ? 1 : 0}},
    "macd_bear_cross": {{macd_bear_cross ? 1 : 0}},
    "bullish_divergence": {{bullish_div ? 1 : 0}},
    "bearish_divergence": {{bearish_div ? 1 : 0}},
    "bullish_ob": {{bullish_ob ? 1 : 0}},
    "bearish_ob": {{bearish_ob ? 1 : 0}}
  },
  
  "trend": {
    "ema_stack": "{{ema_stack_status}}",
    "bias": "{{trend_bias}}"
  }
}
```

### 6.2 Excel Column Mapping

| Excel Column | JSON Path | Description |
|--------------|-----------|-------------|
| A: Timestamp | `timestamp_iso` | ISO 8601 format |
| B: Open | `price.open` | Opening price |
| C: High | `price.high` | High price |
| D: Low | `price.low` | Low price |
| E: Close | `price.close` | Closing price |
| F: EMA20 | `ema.ema20` | 20-period EMA |
| G: EMA50 | `ema.ema50` | 50-period EMA |
| H: EMA200 | `ema.ema200` | 200-period EMA |
| I: Invalidation | `risk.invalidation` | Stop loss level |
| J: Risk% | `risk.distance_pct` | Distance to invalidation |
| K: RSI | `rsi.value` | RSI(14) value |
| L: RSI_MA | `rsi.ma` | RSI moving average |
| M: RSI_Zone | `rsi.zone` | Overbought/Oversold/Neutral |
| N: MACD | `macd.line` | MACD line |
| O: Signal | `macd.signal` | Signal line |
| P: Histogram | `macd.histogram` | MACD histogram |
| Q: MACD_Bull | `signals.macd_bull_cross` | Bull cross flag |
| R: MACD_Bear | `signals.macd_bear_cross` | Bear cross flag |
| S: Bull_Div | `signals.bullish_divergence` | Bullish divergence |
| T: Bear_Div | `signals.bearish_divergence` | Bearish divergence |
| U: Bull_OB | `signals.bullish_ob` | Bullish order block |
| V: Bear_OB | `signals.bearish_ob` | Bearish order block |
| W: EMA_Stack | `trend.ema_stack` | BULLISH/BEARISH/MIXED |
| X: Bias | `trend.bias` | Overall trend bias |

---

## 7. RECOMMENDED PINE CODE UPGRADES

### 7.1 Data Export Fixes

1. **Add 52 Week High/Low to plotted values**
```pine
plot(ta.highest(high, 252), "52W High", display=display.data_window)
plot(ta.lowest(low, 252), "52W Low", display=display.data_window)
```

2. **Fix Sentiment Line export**
```pine
sentimentValue = (rsi - 50) / 50  // Example calculation
plot(sentimentValue, "Sentiment Line", display=display.data_window)
```

3. **Clarify Trend variable**
```pine
// Make trend meaningful
trendScore = close > ema20 ? 1 : 0
trendScore := trendScore + (close > ema50 ? 1 : 0)
trendScore := trendScore + (close > ema200 ? 1 : 0)
plot(trendScore, "Trend Score", display=display.data_window)
```

### 7.2 Webhook Alert Integration

```pine
// Alert condition for any signal
alertCondition = macdBullCross or macdBearCross or bullishDiv or bearishDiv or bullishOB or bearishOB

if alertCondition
    alert(str.format('{"chart":"01A","symbol":"{0}","close":{1},"signal":"{2}"}', 
        syminfo.ticker, close, signalType), alert.freq_once_per_bar)
```

---

## 8. NEXT STEPS

- [ ] Extract Pine code from .docx files
- [ ] Verify indicator logic matches CSV output
- [ ] Design webhook endpoint for data ingestion
- [ ] Create Excel template with proper column mapping
- [ ] Test alert firing and data capture

---

*Report generated following institutional-grade methodology with surgical precision.*
