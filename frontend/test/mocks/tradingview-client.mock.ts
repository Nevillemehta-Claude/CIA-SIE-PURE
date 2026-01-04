/**
 * TRADINGVIEW CLIENT MOCK - Drop-in replacement for testing
 */

import { TradingViewSignalFixtures, type TradingViewSignals } from '../fixtures/tradingview/signals';
import { TradingViewErrorFixtures, type TradingViewErrorType } from '../fixtures/tradingview/errors';

export interface MockTradingViewClientConfig {
  shouldFail?: boolean;
  failureType?: TradingViewErrorType;
  latencyMs?: number;
}

export interface CallHistoryEntry {
  method: string;
  args: unknown[];
  timestamp: Date;
}

// Symbol to fixture mapping
const SYMBOL_FIXTURE_MAP: Record<string, keyof typeof TradingViewSignalFixtures> = {
  'NSE:RELIANCE': 'STRONG_BULLISH',
  'NSE:INFY': 'STRONG_BEARISH',
  'NSE:SBIN': 'CONTRADICTORY_RSI_MACD',
  'NSE:WIPRO': 'NEUTRAL',
  'NSE:TATAMOTORS': 'BULLISH_BREAKOUT',
  'NSE:HDFCBANK': 'BEARISH_BREAKDOWN',
  'NSE:TITAN': 'BEARISH_DIVERGENCE',
  'NSE:ASIANPAINT': 'BULLISH_DIVERGENCE'
};

export class MockTradingViewClient {
  private shouldFail = false;
  private failureType: TradingViewErrorType | null = null;
  private latencyMs = 0;
  private callHistory: CallHistoryEntry[] = [];

  configure(config: MockTradingViewClientConfig): void {
    this.shouldFail = config.shouldFail ?? false;
    this.failureType = config.failureType ?? null;
    this.latencyMs = config.latencyMs ?? 0;
  }

  reset(): void {
    this.shouldFail = false;
    this.failureType = null;
    this.latencyMs = 0;
    this.callHistory = [];
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

  async getTechnicalSignals(symbol: string): Promise<TradingViewSignals> {
    this.callHistory.push({ method: 'getTechnicalSignals', args: [symbol], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const fixtureKey = SYMBOL_FIXTURE_MAP[symbol];
    if (fixtureKey) {
      return { ...TradingViewSignalFixtures[fixtureKey], symbol };
    }

    // Return neutral for unknown symbols
    return { ...TradingViewSignalFixtures.NEUTRAL, symbol };
  }

  async getBulkTechnicalSignals(symbols: string[]): Promise<TradingViewSignals[]> {
    this.callHistory.push({ method: 'getBulkTechnicalSignals', args: [symbols], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    return Promise.all(symbols.map(symbol => this.getTechnicalSignals(symbol)));
  }

  async getIndicator(symbol: string, indicator: string): Promise<{ value: number; signal: string }> {
    this.callHistory.push({ method: 'getIndicator', args: [symbol, indicator], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const signals = await this.getTechnicalSignals(symbol);
    const indicators = signals.indicators as Record<string, unknown>;
    
    if (indicator === 'rsi') {
      const rsi = indicators.rsi as { value: number; signal: string };
      return { value: rsi.value, signal: rsi.signal };
    }
    if (indicator === 'macd') {
      const macd = indicators.macd as { value: number; interpretation: string };
      return { value: macd.value, signal: macd.interpretation };
    }

    return { value: 0, signal: 'neutral' };
  }

  async getOverallSignal(symbol: string): Promise<{ signal: string; strength: number }> {
    this.callHistory.push({ method: 'getOverallSignal', args: [symbol], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const signals = await this.getTechnicalSignals(symbol);
    return {
      signal: signals.overallSignal,
      strength: signals.signalStrength
    };
  }

  private async simulateLatency(): Promise<void> {
    if (this.latencyMs > 0) {
      await new Promise(resolve => setTimeout(resolve, this.latencyMs));
    }
  }

  private createError(): Error {
    const errorResponse = this.failureType 
      ? TradingViewErrorFixtures[this.failureType]
      : TradingViewErrorFixtures.NETWORK_TIMEOUT;
    
    const error = new Error(errorResponse.message);
    (error as Error & { code: string }).code = errorResponse.code;
    return error;
  }
}

export function createMockTradingViewClient(): MockTradingViewClient {
  return new MockTradingViewClient();
}

// Singleton instance for convenience
export const mockTradingViewClient = new MockTradingViewClient();

