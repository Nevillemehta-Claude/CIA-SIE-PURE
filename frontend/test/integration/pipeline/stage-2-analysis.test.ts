/**
 * STAGE 2: AI-DRIVEN ANALYSIS PIPELINE TESTS
 * Tests for grading, analysis, and surfacing logic
 */

import { createMockClaudeClient } from '../../mocks/claude-client.mock';
import { ClaudeAnalysisFixtures } from '../../fixtures/claude/analysis';
import { TradingViewSignalFixtures } from '../../fixtures/tradingview/signals';

// Helper function to calculate grade from signals
function calculateGrade(signals: typeof TradingViewSignalFixtures.STRONG_BULLISH): 'A' | 'B' | 'C' | 'D' | 'F' {
  const strength = signals.signalStrength;
  const signal = signals.overallSignal;
  
  // Strong buy with high confidence
  if (signal === 'strong_buy' && strength >= 0.8) return 'A';
  // Buy or strong buy with moderate confidence
  if ((signal === 'buy' || signal === 'strong_buy') && strength >= 0.6) return 'B';
  // Neutral or low confidence
  if (signal === 'neutral' || strength < 0.5) return 'C';
  // Strong sell with high confidence - check BEFORE moderate bearish
  if (signal === 'strong_sell' && strength >= 0.8) return 'F';
  // Sell or strong sell with moderate confidence
  if ((signal === 'sell' || signal === 'strong_sell') && strength >= 0.6) return 'D';
  
  return 'C';
}

// Helper function to get surfaced (actionable) items
function getSurfacedItems<T extends { confidence: number }>(
  analyses: T[],
  options: { threshold: number }
): T[] {
  return analyses
    .filter(a => a.confidence >= options.threshold)
    .sort((a, b) => b.confidence - a.confidence);
}

describe('Stage 2: AI-Driven Analysis Pipeline', () => {
  let claudeClient: ReturnType<typeof createMockClaudeClient>;

  beforeEach(() => {
    claudeClient = createMockClaudeClient();
    claudeClient.reset();
  });

  describe('Grading Algorithm', () => {
    
    it('should assign Grade A for strong bullish signals', () => {
      const signals = TradingViewSignalFixtures.STRONG_BULLISH;
      const grade = calculateGrade(signals);
      expect(grade).toBe('A');
    });

    it('should assign Grade B for moderate bullish signals', () => {
      const signals = TradingViewSignalFixtures.BULLISH_BREAKOUT;
      const grade = calculateGrade(signals);
      expect(grade).toBe('B');
    });

    it('should assign Grade C for contradictory signals', () => {
      const signals = TradingViewSignalFixtures.CONTRADICTORY_RSI_MACD;
      const grade = calculateGrade(signals);
      expect(grade).toBe('C');
    });

    it('should assign Grade C for neutral signals', () => {
      const signals = TradingViewSignalFixtures.NEUTRAL;
      const grade = calculateGrade(signals);
      expect(grade).toBe('C');
    });

    it('should assign Grade D for moderate bearish signals', () => {
      const signals = TradingViewSignalFixtures.BEARISH_BREAKDOWN;
      const grade = calculateGrade(signals);
      expect(grade).toBe('D');
    });

    it('should assign Grade F for strong bearish signals', () => {
      const signals = TradingViewSignalFixtures.STRONG_BEARISH;
      const grade = calculateGrade(signals);
      expect(grade).toBe('F');
    });
  });

  describe('Claude Analysis Integration', () => {
    
    it('should analyze stock with mocked response', async () => {
      const result = await claudeClient.analyzeStock({
        symbol: 'NSE:RELIANCE',
        indicators: TradingViewSignalFixtures.STRONG_BULLISH.indicators
      });
      
      expect(result.grade).toBe('A');
      expect(result.confidence).toBe(88);
    });

    it('should return contradictory analysis for SBIN', async () => {
      const result = await claudeClient.analyzeStock({
        symbol: 'NSE:SBIN',
        indicators: TradingViewSignalFixtures.CONTRADICTORY_RSI_MACD.indicators
      });
      
      expect(result.grade).toBe('C');
      expect(result.contradictions.length).toBeGreaterThan(0);
    });

    it('should analyze multiple stocks in batch', async () => {
      const requests = [
        { symbol: 'NSE:RELIANCE', indicators: {} },
        { symbol: 'NSE:TCS', indicators: {} },
        { symbol: 'NSE:SBIN', indicators: {} }
      ];
      
      const results = await claudeClient.analyzeMultipleStocks(requests);
      
      expect(results).toHaveLength(3);
      expect(results[0].grade).toBe('A');
      expect(results[1].grade).toBe('B');
      expect(results[2].grade).toBe('C');
    });

    it('should track token usage', async () => {
      await claudeClient.analyzeStock({ symbol: 'NSE:RELIANCE', indicators: {} });
      await claudeClient.analyzeStock({ symbol: 'NSE:TCS', indicators: {} });
      
      const usage = claudeClient.getTokenUsage();
      
      expect(usage.input).toBeGreaterThan(0);
      expect(usage.output).toBeGreaterThan(0);
      expect(usage.total).toBe(usage.input + usage.output);
    });

    it('should handle API errors', async () => {
      claudeClient.configure({ shouldFail: true, failureType: 'RATE_LIMITED' });
      
      await expect(claudeClient.analyzeStock({ symbol: 'NSE:RELIANCE', indicators: {} }))
        .rejects.toThrow('Rate limit exceeded');
    });

    it('should support model tier selection', () => {
      claudeClient.setModelTier('opus');
      expect(claudeClient.getModelTier()).toBe('opus');
      
      claudeClient.setModelTier('haiku');
      expect(claudeClient.getModelTier()).toBe('haiku');
    });
  });

  describe('Analysis Validation', () => {
    
    it('should validate clean analysis as compliant', async () => {
      const validation = await claudeClient.validateAnalysis(ClaudeAnalysisFixtures.GRADE_A);
      
      expect(validation.isValid).toBe(true);
      expect(validation.violations).toHaveLength(0);
    });

    it('should validate contradictory analysis as compliant', async () => {
      const validation = await claudeClient.validateAnalysis(ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY);
      
      expect(validation.isValid).toBe(true);
      expect(validation.violations).toHaveLength(0);
    });
  });

  describe('Actionable Surfacing', () => {
    
    it('should surface Grade A items as actionable', () => {
      const analyses = [
        { symbol: 'NSE:RELIANCE', ...ClaudeAnalysisFixtures.GRADE_A },
        { symbol: 'NSE:TCS', ...ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY }
      ];
      
      const surfaced = getSurfacedItems(analyses, { threshold: 70 });
      
      expect(surfaced.map(s => s.symbol)).toContain('NSE:RELIANCE');
    });

    it('should NOT surface Grade C items (ambiguous)', () => {
      const analyses = [
        { symbol: 'NSE:SBIN', ...ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY }
      ];
      
      const surfaced = getSurfacedItems(analyses, { threshold: 70 });
      
      expect(surfaced.length).toBe(0);
    });

    it('should rank by confidence descending', () => {
      const analyses = [
        { symbol: 'NSE:A', grade: 'A' as const, confidence: 75 },
        { symbol: 'NSE:B', grade: 'A' as const, confidence: 90 },
        { symbol: 'NSE:C', grade: 'A' as const, confidence: 82 }
      ];
      
      const surfaced = getSurfacedItems(analyses, { threshold: 70 });
      
      expect(surfaced[0].symbol).toBe('NSE:B'); // Highest confidence first
      expect(surfaced[1].symbol).toBe('NSE:C');
      expect(surfaced[2].symbol).toBe('NSE:A');
    });

    it('should respect confidence threshold', () => {
      const analyses = [
        { symbol: 'NSE:A', confidence: 85 },
        { symbol: 'NSE:B', confidence: 65 },
        { symbol: 'NSE:C', confidence: 75 }
      ];
      
      const surfaced = getSurfacedItems(analyses, { threshold: 70 });
      
      expect(surfaced).toHaveLength(2);
      expect(surfaced.map(s => s.symbol)).not.toContain('NSE:B');
    });

    it('should handle empty analysis array', () => {
      const surfaced = getSurfacedItems([], { threshold: 70 });
      expect(surfaced).toHaveLength(0);
    });
  });

  describe('Budget Management', () => {
    
    it('should check budget availability', async () => {
      const budget = await claudeClient.checkBudget();
      
      expect(budget.remainingTokens).toBeGreaterThan(0);
      expect(budget.isWithinBudget).toBe(true);
    });

    it('should update budget after analysis calls', async () => {
      const initialBudget = await claudeClient.checkBudget();
      
      await claudeClient.analyzeStock({ symbol: 'NSE:RELIANCE', indicators: {} });
      
      const updatedBudget = await claudeClient.checkBudget();
      
      expect(updatedBudget.remainingTokens).toBeLessThan(initialBudget.remainingTokens);
    });
  });

  describe('Error Handling', () => {
    
    it('should handle overloaded API', async () => {
      claudeClient.configure({ shouldFail: true, failureType: 'OVERLOADED' });
      
      await expect(claudeClient.analyzeStock({ symbol: 'NSE:RELIANCE', indicators: {} }))
        .rejects.toThrow('API is temporarily overloaded');
    });

    it('should handle authentication error', async () => {
      claudeClient.configure({ shouldFail: true, failureType: 'AUTHENTICATION' });
      
      await expect(claudeClient.analyzeStock({ symbol: 'NSE:RELIANCE', indicators: {} }))
        .rejects.toThrow('Invalid API key');
    });

    it('should handle context length error', async () => {
      claudeClient.configure({ shouldFail: true, failureType: 'CONTEXT_LENGTH' });
      
      await expect(claudeClient.analyzeStock({ symbol: 'NSE:RELIANCE', indicators: {} }))
        .rejects.toThrow('maximum context length');
    });
  });
});

