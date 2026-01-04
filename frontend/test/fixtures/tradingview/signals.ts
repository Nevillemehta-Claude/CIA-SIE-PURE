/**
 * TRADINGVIEW SIGNAL MOCK FIXTURES
 * Technical analysis signals for testing
 */

export interface TradingViewIndicators {
  rsi: { value: number; signal: 'oversold' | 'neutral' | 'overbought'; period: number };
  macd: { value: number; signal: number; histogram: number; interpretation: 'bullish' | 'bearish' | 'neutral' };
  movingAverages: { sma20: number; sma50: number; sma200: number; pricePosition: string };
  bollingerBands: { upper: number; middle: number; lower: number; percentB: number };
  volume: { current: number; average20: number; ratio: number; trend: string };
  stochastic: { k: number; d: number; signal: string };
  atr: { value: number; percentOfPrice: number; volatilityLevel: string };
}

export interface TradingViewSignals {
  symbol: string;
  timestamp: string;
  indicators: TradingViewIndicators;
  overallSignal: 'strong_buy' | 'buy' | 'neutral' | 'sell' | 'strong_sell';
  signalStrength: number;
}

// STRONG BULLISH Scenario
export const TV_SIGNALS_STRONG_BULLISH: TradingViewSignals = {
  symbol: 'NSE:RELIANCE',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 35, signal: 'oversold', period: 14 },
    macd: { value: 15.50, signal: 10.25, histogram: 5.25, interpretation: 'bullish' },
    movingAverages: { sma20: 2420, sma50: 2380, sma200: 2250, pricePosition: 'above_all' },
    bollingerBands: { upper: 2520, middle: 2420, lower: 2320, percentB: 0.68 },
    volume: { current: 2500000, average20: 2000000, ratio: 1.25, trend: 'above_average' },
    stochastic: { k: 25, d: 22, signal: 'oversold' },
    atr: { value: 45.50, percentOfPrice: 1.85, volatilityLevel: 'medium' }
  },
  overallSignal: 'strong_buy',
  signalStrength: 0.85
};

// STRONG BEARISH Scenario
export const TV_SIGNALS_STRONG_BEARISH: TradingViewSignals = {
  symbol: 'NSE:INFY',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 72, signal: 'overbought', period: 14 },
    macd: { value: -12.50, signal: -8.25, histogram: -4.25, interpretation: 'bearish' },
    movingAverages: { sma20: 1600, sma50: 1620, sma200: 1580, pricePosition: 'below_all' },
    bollingerBands: { upper: 1650, middle: 1600, lower: 1550, percentB: 0.18 },
    volume: { current: 3500000, average20: 2800000, ratio: 1.25, trend: 'above_average' },
    stochastic: { k: 78, d: 75, signal: 'overbought' },
    atr: { value: 35.20, percentOfPrice: 2.25, volatilityLevel: 'high' }
  },
  overallSignal: 'strong_sell',
  signalStrength: 0.82
};

// CONTRADICTORY SIGNALS (For Constitutional Rule Testing)
export const TV_SIGNALS_CONTRADICTORY_RSI_MACD: TradingViewSignals = {
  symbol: 'NSE:SBIN',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 28, signal: 'oversold', period: 14 }, // BULLISH
    macd: { value: -8.50, signal: -5.25, histogram: -3.25, interpretation: 'bearish' }, // BEARISH
    movingAverages: { sma20: 640, sma50: 650, sma200: 620, pricePosition: 'mixed' },
    bollingerBands: { upper: 680, middle: 640, lower: 600, percentB: 0.32 },
    volume: { current: 4500000, average20: 4000000, ratio: 1.125, trend: 'above_average' },
    stochastic: { k: 22, d: 25, signal: 'oversold' }, // BULLISH
    atr: { value: 15.80, percentOfPrice: 2.53, volatilityLevel: 'high' }
  },
  overallSignal: 'neutral',
  signalStrength: 0.35 // Low confidence due to contradictions
};

// NEUTRAL Scenario
export const TV_SIGNALS_NEUTRAL: TradingViewSignals = {
  symbol: 'NSE:WIPRO',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 50, signal: 'neutral', period: 14 },
    macd: { value: 0.50, signal: 0.45, histogram: 0.05, interpretation: 'neutral' },
    movingAverages: { sma20: 485, sma50: 484, sma200: 480, pricePosition: 'above_all' },
    bollingerBands: { upper: 495, middle: 485, lower: 475, percentB: 0.50 },
    volume: { current: 2800000, average20: 2750000, ratio: 1.02, trend: 'average' },
    stochastic: { k: 50, d: 50, signal: 'neutral' },
    atr: { value: 8.50, percentOfPrice: 1.75, volatilityLevel: 'low' }
  },
  overallSignal: 'neutral',
  signalStrength: 0.50
};

// BULLISH BREAKOUT Scenario
export const TV_SIGNALS_BULLISH_BREAKOUT: TradingViewSignals = {
  symbol: 'NSE:TATAMOTORS',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 62, signal: 'neutral', period: 14 },
    macd: { value: 8.75, signal: 5.50, histogram: 3.25, interpretation: 'bullish' },
    movingAverages: { sma20: 710, sma50: 695, sma200: 680, pricePosition: 'above_all' },
    bollingerBands: { upper: 745, middle: 720, lower: 695, percentB: 0.85 },
    volume: { current: 5200000, average20: 3200000, ratio: 1.625, trend: 'breakout_volume' },
    stochastic: { k: 75, d: 68, signal: 'bullish_momentum' },
    atr: { value: 22.50, percentOfPrice: 3.10, volatilityLevel: 'high' }
  },
  overallSignal: 'buy',
  signalStrength: 0.72
};

// BEARISH BREAKDOWN Scenario
export const TV_SIGNALS_BEARISH_BREAKDOWN: TradingViewSignals = {
  symbol: 'NSE:HDFCBANK',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 38, signal: 'neutral', period: 14 },
    macd: { value: -10.25, signal: -6.75, histogram: -3.50, interpretation: 'bearish' },
    movingAverages: { sma20: 1680, sma50: 1700, sma200: 1720, pricePosition: 'below_all' },
    bollingerBands: { upper: 1720, middle: 1680, lower: 1640, percentB: 0.12 },
    volume: { current: 3800000, average20: 1800000, ratio: 2.11, trend: 'breakdown_volume' },
    stochastic: { k: 18, d: 25, signal: 'bearish_momentum' },
    atr: { value: 32.50, percentOfPrice: 1.97, volatilityLevel: 'medium' }
  },
  overallSignal: 'sell',
  signalStrength: 0.68
};

// DIVERGENCE - Price Up, RSI Down (Bearish Divergence)
export const TV_SIGNALS_BEARISH_DIVERGENCE: TradingViewSignals = {
  symbol: 'NSE:TITAN',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 55, signal: 'neutral', period: 14 }, // Lower than previous peak despite higher price
    macd: { value: 5.25, signal: 4.50, histogram: 0.75, interpretation: 'bullish' },
    movingAverages: { sma20: 3150, sma50: 3100, sma200: 3000, pricePosition: 'above_all' },
    bollingerBands: { upper: 3280, middle: 3180, lower: 3080, percentB: 0.65 },
    volume: { current: 420000, average20: 450000, ratio: 0.93, trend: 'below_average' },
    stochastic: { k: 58, d: 62, signal: 'bearish_cross' },
    atr: { value: 65.00, percentOfPrice: 2.03, volatilityLevel: 'medium' }
  },
  overallSignal: 'neutral',
  signalStrength: 0.45
};

// BULLISH DIVERGENCE - Price Down, RSI Up
export const TV_SIGNALS_BULLISH_DIVERGENCE: TradingViewSignals = {
  symbol: 'NSE:ASIANPAINT',
  timestamp: '2024-01-15T10:30:00.000Z',
  indicators: {
    rsi: { value: 42, signal: 'neutral', period: 14 }, // Higher than previous low despite lower price
    macd: { value: -3.50, signal: -4.25, histogram: 0.75, interpretation: 'neutral' },
    movingAverages: { sma20: 3080, sma50: 3100, sma200: 3050, pricePosition: 'below_short_term' },
    bollingerBands: { upper: 3150, middle: 3080, lower: 3010, percentB: 0.35 },
    volume: { current: 480000, average20: 500000, ratio: 0.96, trend: 'average' },
    stochastic: { k: 35, d: 30, signal: 'bullish_cross' },
    atr: { value: 55.00, percentOfPrice: 1.80, volatilityLevel: 'medium' }
  },
  overallSignal: 'neutral',
  signalStrength: 0.48
};

export const TradingViewSignalFixtures = {
  STRONG_BULLISH: TV_SIGNALS_STRONG_BULLISH,
  STRONG_BEARISH: TV_SIGNALS_STRONG_BEARISH,
  CONTRADICTORY_RSI_MACD: TV_SIGNALS_CONTRADICTORY_RSI_MACD,
  NEUTRAL: TV_SIGNALS_NEUTRAL,
  BULLISH_BREAKOUT: TV_SIGNALS_BULLISH_BREAKOUT,
  BEARISH_BREAKDOWN: TV_SIGNALS_BEARISH_BREAKDOWN,
  BEARISH_DIVERGENCE: TV_SIGNALS_BEARISH_DIVERGENCE,
  BULLISH_DIVERGENCE: TV_SIGNALS_BULLISH_DIVERGENCE
};

