/**
 * DATA VALIDATION UTILITY TESTS
 */

import { KiteQuoteFixtures } from '../../fixtures/kite/quotes';
import { TradingViewSignalFixtures } from '../../fixtures/tradingview/signals';
import { ClaudeAnalysisFixtures } from '../../fixtures/claude/analysis';

// Validation utility functions
function isValidQuote(quote: unknown): boolean {
  if (!quote || typeof quote !== 'object') return false;
  const q = quote as Record<string, unknown>;
  return (
    typeof q.last_price === 'number' &&
    typeof q.volume === 'number' &&
    q.ohlc !== undefined &&
    typeof (q.ohlc as Record<string, unknown>).open === 'number'
  );
}

function isValidOHLC(ohlc: { open: number; high: number; low: number; close: number }): boolean {
  return (
    ohlc.high >= ohlc.low &&
    ohlc.high >= ohlc.open &&
    ohlc.high >= ohlc.close &&
    ohlc.low <= ohlc.open &&
    ohlc.low <= ohlc.close
  );
}

function isValidSignalStrength(strength: number): boolean {
  return strength >= 0 && strength <= 1;
}

function isValidRSI(value: number): boolean {
  return value >= 0 && value <= 100;
}

function isValidGrade(grade: string): boolean {
  return ['A', 'B', 'C', 'D', 'F'].includes(grade);
}

function isValidConfidence(confidence: number): boolean {
  return confidence >= 0 && confidence <= 100;
}

describe('Data Validators', () => {

  describe('Quote Validation', () => {
    
    it('should validate valid quote object', () => {
      const quote = KiteQuoteFixtures.RELIANCE['NSE:RELIANCE'];
      expect(isValidQuote(quote)).toBe(true);
    });

    it('should reject null quote', () => {
      expect(isValidQuote(null)).toBe(false);
    });

    it('should reject undefined quote', () => {
      expect(isValidQuote(undefined)).toBe(false);
    });

    it('should reject quote without last_price', () => {
      expect(isValidQuote({ volume: 100 })).toBe(false);
    });

    it('should reject quote with invalid last_price type', () => {
      expect(isValidQuote({ last_price: '100', volume: 100, ohlc: { open: 100 } })).toBe(false);
    });
  });

  describe('OHLC Validation', () => {
    
    it('should validate normal OHLC', () => {
      const ohlc = { open: 100, high: 110, low: 95, close: 105 };
      expect(isValidOHLC(ohlc)).toBe(true);
    });

    it('should validate OHLC where high equals close', () => {
      const ohlc = { open: 100, high: 110, low: 95, close: 110 };
      expect(isValidOHLC(ohlc)).toBe(true);
    });

    it('should validate OHLC where low equals open', () => {
      const ohlc = { open: 95, high: 110, low: 95, close: 105 };
      expect(isValidOHLC(ohlc)).toBe(true);
    });

    it('should validate flat day (all equal)', () => {
      const ohlc = { open: 100, high: 100, low: 100, close: 100 };
      expect(isValidOHLC(ohlc)).toBe(true);
    });

    it('should reject high below low', () => {
      const ohlc = { open: 100, high: 90, low: 95, close: 105 };
      expect(isValidOHLC(ohlc)).toBe(false);
    });

    it('should reject high below open', () => {
      const ohlc = { open: 100, high: 98, low: 95, close: 97 };
      expect(isValidOHLC(ohlc)).toBe(false);
    });

    it('should reject low above close', () => {
      const ohlc = { open: 100, high: 110, low: 106, close: 105 };
      expect(isValidOHLC(ohlc)).toBe(false);
    });
  });

  describe('Signal Strength Validation', () => {
    
    it('should validate strength of 0', () => {
      expect(isValidSignalStrength(0)).toBe(true);
    });

    it('should validate strength of 1', () => {
      expect(isValidSignalStrength(1)).toBe(true);
    });

    it('should validate strength of 0.5', () => {
      expect(isValidSignalStrength(0.5)).toBe(true);
    });

    it('should reject negative strength', () => {
      expect(isValidSignalStrength(-0.1)).toBe(false);
    });

    it('should reject strength greater than 1', () => {
      expect(isValidSignalStrength(1.1)).toBe(false);
    });

    it('should validate all fixture signal strengths', () => {
      const allSignals = Object.values(TradingViewSignalFixtures);
      allSignals.forEach(signal => {
        expect(isValidSignalStrength(signal.signalStrength)).toBe(true);
      });
    });
  });

  describe('RSI Validation', () => {
    
    it('should validate RSI of 0', () => {
      expect(isValidRSI(0)).toBe(true);
    });

    it('should validate RSI of 100', () => {
      expect(isValidRSI(100)).toBe(true);
    });

    it('should validate RSI of 50', () => {
      expect(isValidRSI(50)).toBe(true);
    });

    it('should reject negative RSI', () => {
      expect(isValidRSI(-1)).toBe(false);
    });

    it('should reject RSI greater than 100', () => {
      expect(isValidRSI(101)).toBe(false);
    });

    it('should validate all fixture RSI values', () => {
      const allSignals = Object.values(TradingViewSignalFixtures);
      allSignals.forEach(signal => {
        expect(isValidRSI(signal.indicators.rsi.value)).toBe(true);
      });
    });
  });

  describe('Grade Validation', () => {
    
    it('should validate Grade A', () => {
      expect(isValidGrade('A')).toBe(true);
    });

    it('should validate Grade B', () => {
      expect(isValidGrade('B')).toBe(true);
    });

    it('should validate Grade C', () => {
      expect(isValidGrade('C')).toBe(true);
    });

    it('should validate Grade D', () => {
      expect(isValidGrade('D')).toBe(true);
    });

    it('should validate Grade F', () => {
      expect(isValidGrade('F')).toBe(true);
    });

    it('should reject Grade E', () => {
      expect(isValidGrade('E')).toBe(false);
    });

    it('should reject lowercase grade', () => {
      expect(isValidGrade('a')).toBe(false);
    });

    it('should reject empty string', () => {
      expect(isValidGrade('')).toBe(false);
    });

    it('should validate all fixture grades', () => {
      const allAnalyses = Object.values(ClaudeAnalysisFixtures);
      allAnalyses.forEach(analysis => {
        expect(isValidGrade(analysis.grade)).toBe(true);
      });
    });
  });

  describe('Confidence Validation', () => {
    
    it('should validate confidence of 0', () => {
      expect(isValidConfidence(0)).toBe(true);
    });

    it('should validate confidence of 100', () => {
      expect(isValidConfidence(100)).toBe(true);
    });

    it('should validate confidence of 50', () => {
      expect(isValidConfidence(50)).toBe(true);
    });

    it('should reject negative confidence', () => {
      expect(isValidConfidence(-1)).toBe(false);
    });

    it('should reject confidence greater than 100', () => {
      expect(isValidConfidence(101)).toBe(false);
    });

    it('should validate all fixture confidence values', () => {
      const allAnalyses = Object.values(ClaudeAnalysisFixtures);
      allAnalyses.forEach(analysis => {
        expect(isValidConfidence(analysis.confidence)).toBe(true);
      });
    });
  });
});

