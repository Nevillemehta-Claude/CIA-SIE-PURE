/**
 * CLAUDE AI CLIENT MOCK - Drop-in replacement for testing
 */

import { ClaudeAnalysisFixtures, type ClaudeAnalysisResponse } from '../fixtures/claude/analysis';
import { ClaudeErrorFixtures, type ClaudeErrorType } from '../fixtures/claude/errors';

export interface MockClaudeClientConfig {
  shouldFail?: boolean;
  failureType?: ClaudeErrorType;
  latencyMs?: number;
  modelTier?: 'haiku' | 'sonnet' | 'opus';
}

export interface CallHistoryEntry {
  method: string;
  args: unknown[];
  timestamp: Date;
}

export interface AnalysisRequest {
  symbol: string;
  indicators: Record<string, unknown>;
  historicalData?: unknown[];
}

// Symbol to analysis fixture mapping
const SYMBOL_ANALYSIS_MAP: Record<string, keyof typeof ClaudeAnalysisFixtures> = {
  'NSE:RELIANCE': 'GRADE_A',
  'NSE:TCS': 'GRADE_B',
  'NSE:SBIN': 'GRADE_C_CONTRADICTORY',
  'NSE:HDFCBANK': 'GRADE_D',
  'NSE:INFY': 'GRADE_F',
  'NSE:WIPRO': 'NEUTRAL',
  'NSE:TITAN': 'TIMEFRAME_CONTRADICTION'
};

export class MockClaudeClient {
  private shouldFail = false;
  private failureType: ClaudeErrorType | null = null;
  private latencyMs = 0;
  private modelTier: 'haiku' | 'sonnet' | 'opus' = 'sonnet';
  private callHistory: CallHistoryEntry[] = [];
  private tokenUsage = { input: 0, output: 0 };

  configure(config: MockClaudeClientConfig): void {
    this.shouldFail = config.shouldFail ?? false;
    this.failureType = config.failureType ?? null;
    this.latencyMs = config.latencyMs ?? 0;
    this.modelTier = config.modelTier ?? 'sonnet';
  }

  reset(): void {
    this.shouldFail = false;
    this.failureType = null;
    this.latencyMs = 0;
    this.modelTier = 'sonnet';
    this.callHistory = [];
    this.tokenUsage = { input: 0, output: 0 };
  }

  getCallHistory(): CallHistoryEntry[] {
    return [...this.callHistory];
  }

  getCallCount(method?: string): number {
    if (method) {
      return this.callHistory.filter(c => c.method === method).length;
    }
    return this.callHistory.length;
  }

  getTokenUsage(): { input: number; output: number; total: number } {
    return {
      ...this.tokenUsage,
      total: this.tokenUsage.input + this.tokenUsage.output
    };
  }

  async analyzeStock(request: AnalysisRequest): Promise<ClaudeAnalysisResponse> {
    this.callHistory.push({ method: 'analyzeStock', args: [request], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    // Simulate token usage
    this.tokenUsage.input += 1500;
    this.tokenUsage.output += 800;

    const fixtureKey = SYMBOL_ANALYSIS_MAP[request.symbol];
    if (fixtureKey) {
      return { ...ClaudeAnalysisFixtures[fixtureKey] };
    }

    // Return neutral analysis for unknown symbols
    return { ...ClaudeAnalysisFixtures.NEUTRAL };
  }

  async analyzeMultipleStocks(requests: AnalysisRequest[]): Promise<ClaudeAnalysisResponse[]> {
    this.callHistory.push({ method: 'analyzeMultipleStocks', args: [requests], timestamp: new Date() });
    
    return Promise.all(requests.map(req => this.analyzeStock(req)));
  }

  async validateAnalysis(analysis: ClaudeAnalysisResponse): Promise<{ isValid: boolean; violations: string[] }> {
    this.callHistory.push({ method: 'validateAnalysis', args: [analysis], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const violations: string[] = [];
    
    // Check for execution commands (Constitutional Rule 1)
    const forbiddenPatterns = [/\bBUY\b/i, /\bSELL\b/i, /\bEXECUTE\b/i];
    forbiddenPatterns.forEach(pattern => {
      if (pattern.test(analysis.rationale)) {
        violations.push(`Contains forbidden execution command: ${pattern.source}`);
      }
    });

    // Check for contradiction resolution (Constitutional Rule 2)
    if (analysis.contradictions.length > 0) {
      const resolutionPatterns = [/on balance/i, /net bullish/i, /net bearish/i, /therefore/i];
      resolutionPatterns.forEach(pattern => {
        if (pattern.test(analysis.rationale)) {
          violations.push(`Attempts to resolve contradiction: ${pattern.source}`);
        }
      });
    }

    return {
      isValid: violations.length === 0,
      violations
    };
  }

  async checkBudget(): Promise<{ remainingTokens: number; isWithinBudget: boolean }> {
    this.callHistory.push({ method: 'checkBudget', args: [], timestamp: new Date() });
    
    const budgetLimit = 1000000; // 1M tokens
    const used = this.tokenUsage.input + this.tokenUsage.output;
    
    return {
      remainingTokens: budgetLimit - used,
      isWithinBudget: used < budgetLimit
    };
  }

  getModelTier(): string {
    return this.modelTier;
  }

  setModelTier(tier: 'haiku' | 'sonnet' | 'opus'): void {
    this.modelTier = tier;
  }

  private async simulateLatency(): Promise<void> {
    if (this.latencyMs > 0) {
      await new Promise(resolve => setTimeout(resolve, this.latencyMs));
    }
  }

  private createError(): Error {
    const errorResponse = this.failureType 
      ? ClaudeErrorFixtures[this.failureType]
      : ClaudeErrorFixtures.SERVER;
    
    const error = new Error(errorResponse.error.message);
    (error as Error & { type: string }).type = errorResponse.error.type;
    return error;
  }
}

export function createMockClaudeClient(): MockClaudeClient {
  return new MockClaudeClient();
}

// Singleton instance for convenience
export const mockClaudeClient = new MockClaudeClient();

