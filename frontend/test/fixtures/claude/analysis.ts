/**
 * CLAUDE AI ANALYSIS MOCK FIXTURES
 * 
 * CRITICAL: All responses comply with CIA-SIE Constitutional Rules:
 * 1. Decision support only (no execution commands)
 * 2. Never resolve contradictions
 * 3. Descriptive language only
 */

export interface ClaudeAnalysisResponse {
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  confidence: number;
  rationale: string;
  bullishFactors: string[];
  bearishFactors: string[];
  contradictions: string[]; // MUST be preserved, never resolved
  technicalSummary: string;
  riskAssessment: string;
  timestamp: string;
}

// GRADE A - Strong Bullish
export const CLAUDE_ANALYSIS_GRADE_A: ClaudeAnalysisResponse = {
  grade: 'A',
  confidence: 88,
  rationale: `RELIANCE exhibits strong bullish technical characteristics across multiple timeframes. 
Price action shows consistent higher highs and higher lows formation. Momentum indicators 
align positively with RSI emerging from oversold territory while maintaining upward trajectory.

Moving average alignment displays ideal bullish configuration with price trading above all 
major averages (20, 50, 200-day). The golden cross formation continues to provide support.`,
  
  bullishFactors: [
    'Price trading above 20, 50, and 200-day moving averages',
    'RSI at 35 emerging from oversold zone, indicating potential bounce',
    'MACD histogram positive and expanding at +5.25',
    'Volume 25% above 20-day average showing strong participation',
    'Golden cross formation (50-day crossed above 200-day) intact',
    'Stochastic %K crossed above %D from oversold territory'
  ],
  
  bearishFactors: [
    'Approaching previous resistance zone at 2480-2500 level',
    'Sector rotation showing some weakness in broader energy complex'
  ],
  
  contradictions: [], // No contradictions in clear bullish scenario
  
  technicalSummary: `Bullish momentum across multiple indicators with volume confirmation.`,
  riskAssessment: `Support at 2420 (20-day MA) and 2380 (50-day MA).`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

// GRADE B - Moderately Bullish
export const CLAUDE_ANALYSIS_GRADE_B: ClaudeAnalysisResponse = {
  grade: 'B',
  confidence: 72,
  rationale: `TCS displays moderately bullish technical posture with some caveats. Price structure 
maintains above key moving averages though momentum readings suggest potential consolidation ahead.

The stock demonstrates resilience at support levels, with buyers stepping in consistently. 
Volume patterns remain constructive though not at breakout levels.`,
  
  bullishFactors: [
    'Price holding above 50-day and 200-day moving averages',
    'RSI at 55 in healthy neutral-bullish territory',
    'MACD above signal line, maintaining positive momentum',
    'Bollinger %B at 0.58 showing price in upper half of range'
  ],
  
  bearishFactors: [
    'Volume trending below 20-day average',
    '20-day MA flattening, suggesting momentum slowdown',
    'IT sector facing global headwinds in near term'
  ],
  
  contradictions: [], // Minor concerns but no major contradictions
  
  technicalSummary: `Moderately bullish with some consolidation indicators.`,
  riskAssessment: `Key support at 3850 (50-day MA). Stop-loss consideration below 3800.`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

// GRADE C - Contradictory (Critical for Constitutional Rule Testing)
export const CLAUDE_ANALYSIS_GRADE_C_CONTRADICTORY: ClaudeAnalysisResponse = {
  grade: 'C',
  confidence: 45,
  rationale: `SBIN presents a technically complex picture with contradictory signals across 
momentum and trend indicators. Analysis reveals conflicting readings that warrant careful 
consideration rather than directional conviction.

RSI reading of 28 places the stock in oversold territory, historically associated with 
bounce potential. However, MACD remains in bearish configuration with negative histogram 
expanding, suggesting continued downward momentum.

**IMPORTANT: These contradictions are presented as observed without resolution. 
Market participants may interpret these signals differently based on their timeframe 
and methodology.**`,
  
  bullishFactors: [
    'RSI at 28 indicates oversold conditions historically associated with bounces',
    'Price holding above 200-day moving average at 620',
    'Stochastic %K at 22 in oversold zone',
    'High volume suggests capitulation may be occurring'
  ],
  
  bearishFactors: [
    'MACD histogram at -3.25 and expanding negatively',
    'Price below both 20-day (640) and 50-day (650) moving averages',
    'Bollinger %B at 0.32 indicates price in lower half of range',
    'No bullish divergence confirmed yet'
  ],
  
  contradictions: [
    'RSI oversold (bullish) contradicts MACD bearish momentum - signals present opposing bias',
    'Stochastic oversold reading conflicts with expanding negative MACD histogram',
    'Price below short-term MAs (bearish) but above 200-day MA (bullish) - timeframe conflict',
    'High volume could indicate either capitulation (bullish) or distribution (bearish)'
  ],
  
  technicalSummary: `Mixed picture with momentum indicators providing conflicting signals.`,
  riskAssessment: `Elevated volatility at 2.53% ATR. Key support at 620 (200-day MA).`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

// GRADE D - Moderately Bearish
export const CLAUDE_ANALYSIS_GRADE_D: ClaudeAnalysisResponse = {
  grade: 'D',
  confidence: 68,
  rationale: `HDFCBANK displays moderately bearish technical characteristics. Price action shows 
weakness below key moving averages with momentum indicators confirming downward bias.

The breakdown below 20-day and 50-day moving averages suggests near-term selling pressure 
remains intact. Volume on decline days exceeds up-day volume, indicating distribution.`,
  
  bullishFactors: [
    'RSI at 38 approaching oversold territory',
    'Historical support zone at 1620-1640 level approaching',
    'Long-term trend (200-day) still intact'
  ],
  
  bearishFactors: [
    'Price below 20-day and 50-day moving averages',
    'MACD bearish crossover with negative histogram at -3.50',
    'Volume spike on breakdown indicates conviction selling',
    'Bollinger %B at 0.12 near lower band'
  ],
  
  contradictions: [], // Clear directional bias
  
  technicalSummary: `Bearish momentum with technical breakdown patterns evident.`,
  riskAssessment: `Critical support at 1640. Breach opens target to 1580 (200-day MA).`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

// GRADE F - Strong Bearish
export const CLAUDE_ANALYSIS_GRADE_F: ClaudeAnalysisResponse = {
  grade: 'F',
  confidence: 82,
  rationale: `INFY displays strong bearish technical characteristics across multiple indicators. 
Price has broken below all major moving averages, signaling trend deterioration. 
MACD configuration decidedly bearish with negative histogram expanding.`,
  
  bullishFactors: [
    'High ATR suggests potential for sharp snapback rallies',
    'Extreme oversold readings on some oscillators'
  ],
  
  bearishFactors: [
    'Price below all major moving averages (20, 50, 200-day)',
    'RSI recently overbought at 72, failed rally attempt',
    'MACD histogram at -4.25, strongly negative',
    'Above-average volume on declines confirms distribution',
    'Death cross threatening (50-day approaching 200-day from above)'
  ],
  
  contradictions: [], // Clear bearish picture
  
  technicalSummary: `Strong bearish momentum with multiple confirmation signals.`,
  riskAssessment: `No clear support until 1500 level. High volatility expected.`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

// NEUTRAL - No Clear Direction
export const CLAUDE_ANALYSIS_NEUTRAL: ClaudeAnalysisResponse = {
  grade: 'C',
  confidence: 50,
  rationale: `WIPRO displays neutral technical characteristics with indicators clustered around 
equilibrium levels. Price consolidates within a defined range with no clear directional bias.

The absence of momentum in either direction suggests a wait-and-see approach may be 
appropriate until clearer signals emerge.`,
  
  bullishFactors: [
    'Price maintaining above all major moving averages',
    'Bollinger Bands contracting, suggesting potential breakout ahead',
    'Volume stabilizing near average levels'
  ],
  
  bearishFactors: [
    'RSI flat at 50, no momentum',
    'MACD at zero line with minimal histogram',
    'Low volatility reducing trading opportunities'
  ],
  
  contradictions: [], // Neutral, not contradictory
  
  technicalSummary: `Neutral consolidation pattern with low volatility.`,
  riskAssessment: `Range support at 475, resistance at 495. Breakout direction unclear.`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

// Multi-Timeframe Contradiction
export const CLAUDE_ANALYSIS_TIMEFRAME_CONTRADICTION: ClaudeAnalysisResponse = {
  grade: 'C',
  confidence: 42,
  rationale: `TITAN presents differing signals across timeframes. Daily charts show bullish 
momentum while weekly timeframe indicates potential exhaustion at resistance.

Intraday patterns suggest strength but longer-term indicators warrant caution. This 
timeframe divergence creates uncertainty regarding near-term direction.

**These multi-timeframe contradictions are presented as observed. Different trading 
styles may prioritize different timeframes.**`,
  
  bullishFactors: [
    'Daily RSI at 62 in bullish territory',
    'Daily MACD positive with expanding histogram',
    'Intraday higher lows pattern intact',
    'Above 20-day and 50-day moving averages'
  ],
  
  bearishFactors: [
    'Weekly RSI showing bearish divergence at 55',
    'Weekly MACD histogram declining despite higher prices',
    'Approaching historical resistance at 3300',
    'Volume declining on recent rallies'
  ],
  
  contradictions: [
    'Daily bullish momentum contradicts weekly bearish divergence',
    'Short-term strength conflicts with longer-term exhaustion signals',
    'Price making higher highs but RSI making lower highs (weekly)',
    'Volume confirming daily strength but declining on weekly basis'
  ],
  
  technicalSummary: `Mixed multi-timeframe signals require careful interpretation.`,
  riskAssessment: `Key support at 3100. Resistance at 3280-3300 zone.`,
  timestamp: '2024-01-15T10:35:00.000Z'
};

export const ClaudeAnalysisFixtures = {
  GRADE_A: CLAUDE_ANALYSIS_GRADE_A,
  GRADE_B: CLAUDE_ANALYSIS_GRADE_B,
  GRADE_C_CONTRADICTORY: CLAUDE_ANALYSIS_GRADE_C_CONTRADICTORY,
  GRADE_D: CLAUDE_ANALYSIS_GRADE_D,
  GRADE_F: CLAUDE_ANALYSIS_GRADE_F,
  NEUTRAL: CLAUDE_ANALYSIS_NEUTRAL,
  TIMEFRAME_CONTRADICTION: CLAUDE_ANALYSIS_TIMEFRAME_CONTRADICTION
};

