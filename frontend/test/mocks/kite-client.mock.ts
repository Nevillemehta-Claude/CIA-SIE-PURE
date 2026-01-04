/**
 * KITE CLIENT MOCK - Drop-in replacement for testing
 */

import { KiteQuoteFixtures, type KiteQuote } from '../fixtures/kite/quotes';
import { KiteErrorFixtures, type KiteErrorType } from '../fixtures/kite/errors';
import { KiteHistoricalFixtures, type KiteCandle } from '../fixtures/kite/historical';

export interface MockKiteClientConfig {
  shouldFail?: boolean;
  failureType?: KiteErrorType;
  latencyMs?: number;
}

export interface CallHistoryEntry {
  method: string;
  args: unknown[];
  timestamp: Date;
}

export class MockKiteClient {
  private shouldFail = false;
  private failureType: KiteErrorType | null = null;
  private latencyMs = 0;
  private callHistory: CallHistoryEntry[] = [];

  configure(config: MockKiteClientConfig): void {
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

  async getQuote(instruments: string[]): Promise<Record<string, Partial<KiteQuote>>> {
    this.callHistory.push({ method: 'getQuote', args: [instruments], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const result: Record<string, Partial<KiteQuote>> = {};
    instruments.forEach(instrument => {
      const quote = KiteQuoteFixtures.BULK_50[instrument];
      if (quote) {
        result[instrument] = quote;
      }
    });
    return result;
  }

  async getQuoteSingle(instrument: string): Promise<Partial<KiteQuote> | null> {
    const quotes = await this.getQuote([instrument]);
    return quotes[instrument] || null;
  }

  async getHistoricalData(
    token: number,
    interval: string,
    from: Date,
    to: Date
  ): Promise<KiteCandle[]> {
    this.callHistory.push({ 
      method: 'getHistoricalData', 
      args: [token, interval, from, to],
      timestamp: new Date()
    });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    // Return appropriate fixture based on token
    if (token === 738561) {
      return interval.includes('minute') 
        ? KiteHistoricalFixtures.RELIANCE_5MIN 
        : KiteHistoricalFixtures.RELIANCE_DAILY;
    }
    if (token === 408065) {
      return KiteHistoricalFixtures.INFY_DAILY;
    }
    if (token === 779521) {
      return KiteHistoricalFixtures.SBIN_DAILY;
    }

    // Return empty array for unknown tokens
    return [];
  }

  async getOHLC(instruments: string[]): Promise<Record<string, { ohlc: { open: number; high: number; low: number; close: number } }>> {
    this.callHistory.push({ method: 'getOHLC', args: [instruments], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const result: Record<string, { ohlc: { open: number; high: number; low: number; close: number } }> = {};
    instruments.forEach(instrument => {
      const quote = KiteQuoteFixtures.BULK_50[instrument];
      if (quote?.ohlc) {
        result[instrument] = { ohlc: quote.ohlc };
      }
    });
    return result;
  }

  async getLTP(instruments: string[]): Promise<Record<string, { last_price: number }>> {
    this.callHistory.push({ method: 'getLTP', args: [instruments], timestamp: new Date() });
    await this.simulateLatency();

    if (this.shouldFail) {
      throw this.createError();
    }

    const result: Record<string, { last_price: number }> = {};
    instruments.forEach(instrument => {
      const quote = KiteQuoteFixtures.BULK_50[instrument];
      if (quote?.last_price !== undefined) {
        result[instrument] = { last_price: quote.last_price };
      }
    });
    return result;
  }

  private async simulateLatency(): Promise<void> {
    if (this.latencyMs > 0) {
      await new Promise(resolve => setTimeout(resolve, this.latencyMs));
    }
  }

  private createError(): Error {
    const errorResponse = this.failureType 
      ? KiteErrorFixtures[this.failureType]
      : KiteErrorFixtures.NETWORK_TIMEOUT;
    
    const error = new Error(errorResponse.message);
    (error as Error & { type: string }).type = errorResponse.error_type;
    return error;
  }
}

export function createMockKiteClient(): MockKiteClient {
  return new MockKiteClient();
}

// Singleton instance for convenience
export const mockKiteClient = new MockKiteClient();

