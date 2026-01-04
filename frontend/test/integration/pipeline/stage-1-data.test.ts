/**
 * STAGE 1: DATA INGESTION PIPELINE TESTS
 * Tests for data fetching and normalization
 */

import { createMockKiteClient } from '../../mocks/kite-client.mock';
import { createMockTradingViewClient } from '../../mocks/tradingview-client.mock';
import { KiteQuoteFixtures } from '../../fixtures/kite/quotes';
import { TradingViewSignalFixtures } from '../../fixtures/tradingview/signals';

describe('Stage 1: Data Ingestion Pipeline', () => {
  let kiteClient: ReturnType<typeof createMockKiteClient>;
  let tvClient: ReturnType<typeof createMockTradingViewClient>;

  beforeEach(() => {
    kiteClient = createMockKiteClient();
    tvClient = createMockTradingViewClient();
    kiteClient.reset();
    tvClient.reset();
  });

  describe('Kite API Data Fetching', () => {
    
    it('should fetch quotes for single instrument', async () => {
      const result = await kiteClient.getQuote(['NSE:RELIANCE']);
      
      expect(result['NSE:RELIANCE']).toBeDefined();
      expect(result['NSE:RELIANCE'].last_price).toBe(2456.75);
    });

    it('should fetch quotes for multiple instruments', async () => {
      const instruments = ['NSE:RELIANCE', 'NSE:TCS', 'NSE:INFY'];
      const result = await kiteClient.getQuote(instruments);
      
      expect(Object.keys(result)).toHaveLength(3);
      instruments.forEach(inst => {
        expect(result[inst]).toBeDefined();
      });
    });

    it('should handle 50 instruments batch request', async () => {
      const instruments = Object.keys(KiteQuoteFixtures.BULK_50);
      const result = await kiteClient.getQuote(instruments);
      
      expect(Object.keys(result).length).toBeGreaterThanOrEqual(40);
    });

    it('should return empty object for unknown instruments', async () => {
      const result = await kiteClient.getQuote(['NSE:UNKNOWNSTOCK']);
      
      expect(Object.keys(result)).toHaveLength(0);
    });

    it('should handle API errors gracefully', async () => {
      kiteClient.configure({ shouldFail: true, failureType: 'NETWORK_TIMEOUT' });
      
      await expect(kiteClient.getQuote(['NSE:RELIANCE'])).rejects.toThrow('Request timed out');
    });

    it('should handle token expiry error', async () => {
      kiteClient.configure({ shouldFail: true, failureType: 'TOKEN_EXPIRED' });
      
      await expect(kiteClient.getQuote(['NSE:RELIANCE'])).rejects.toThrow('Token is invalid');
    });

    it('should handle rate limiting error', async () => {
      kiteClient.configure({ shouldFail: true, failureType: 'RATE_LIMITED' });
      
      await expect(kiteClient.getQuote(['NSE:RELIANCE'])).rejects.toThrow('Too many requests');
    });

    it('should record call history', async () => {
      await kiteClient.getQuote(['NSE:RELIANCE']);
      await kiteClient.getQuote(['NSE:TCS']);
      
      expect(kiteClient.getCallCount()).toBe(2);
      expect(kiteClient.getCallCount('getQuote')).toBe(2);
    });
  });

  describe('Kite Historical Data', () => {
    
    it('should fetch daily historical data', async () => {
      const result = await kiteClient.getHistoricalData(
        738561, // RELIANCE token
        'day',
        new Date('2024-01-01'),
        new Date('2024-01-31')
      );
      
      expect(result.length).toBeGreaterThan(0);
    });

    it('should fetch intraday historical data', async () => {
      const result = await kiteClient.getHistoricalData(
        738561,
        '5minute',
        new Date('2024-01-15T09:15:00'),
        new Date('2024-01-15T15:30:00')
      );
      
      expect(result.length).toBeGreaterThan(0);
    });

    it('should return empty array for unknown token', async () => {
      const result = await kiteClient.getHistoricalData(
        999999,
        'day',
        new Date('2024-01-01'),
        new Date('2024-01-31')
      );
      
      expect(result).toEqual([]);
    });
  });

  describe('TradingView Signal Fetching', () => {
    
    it('should fetch technical signals for single symbol', async () => {
      const result = await tvClient.getTechnicalSignals('NSE:RELIANCE');
      
      expect(result.symbol).toBe('NSE:RELIANCE');
      expect(result.overallSignal).toBe('strong_buy');
      expect(result.signalStrength).toBe(0.85);
    });

    it('should fetch bulk signals for multiple symbols', async () => {
      const symbols = ['NSE:RELIANCE', 'NSE:INFY', 'NSE:SBIN'];
      const result = await tvClient.getBulkTechnicalSignals(symbols);
      
      expect(result).toHaveLength(3);
      expect(result.map(r => r.symbol)).toEqual(symbols);
    });

    it('should return neutral for unknown symbols', async () => {
      const result = await tvClient.getTechnicalSignals('NSE:UNKNOWNSTOCK');
      
      expect(result.overallSignal).toBe('neutral');
      expect(result.signalStrength).toBe(0.5);
    });

    it('should handle API errors gracefully', async () => {
      tvClient.configure({ shouldFail: true, failureType: 'SERVICE_UNAVAILABLE' });
      
      await expect(tvClient.getTechnicalSignals('NSE:RELIANCE'))
        .rejects.toThrow('TradingView service is temporarily unavailable');
    });

    it('should fetch individual indicators', async () => {
      const rsi = await tvClient.getIndicator('NSE:RELIANCE', 'rsi');
      
      expect(rsi.value).toBe(35);
      expect(rsi.signal).toBe('oversold');
    });
  });

  describe('Data Validation', () => {
    
    it('should validate quote has required fields', () => {
      const quote = KiteQuoteFixtures.RELIANCE['NSE:RELIANCE'];
      
      expect(quote.last_price).toBeDefined();
      expect(quote.volume).toBeDefined();
      expect(quote.ohlc).toBeDefined();
      expect(quote.ohlc.open).toBeDefined();
      expect(quote.ohlc.high).toBeDefined();
      expect(quote.ohlc.low).toBeDefined();
      expect(quote.ohlc.close).toBeDefined();
    });

    it('should validate signal has required indicators', () => {
      const signals = TradingViewSignalFixtures.STRONG_BULLISH;
      
      expect(signals.indicators.rsi).toBeDefined();
      expect(signals.indicators.macd).toBeDefined();
      expect(signals.indicators.movingAverages).toBeDefined();
      expect(signals.indicators.bollingerBands).toBeDefined();
      expect(signals.indicators.volume).toBeDefined();
      expect(signals.indicators.stochastic).toBeDefined();
      expect(signals.indicators.atr).toBeDefined();
    });

    it('should validate OHLC values are logically consistent', () => {
      const quote = KiteQuoteFixtures.RELIANCE['NSE:RELIANCE'];
      
      expect(quote.ohlc.high).toBeGreaterThanOrEqual(quote.ohlc.low);
      expect(quote.ohlc.high).toBeGreaterThanOrEqual(quote.ohlc.open);
      expect(quote.ohlc.high).toBeGreaterThanOrEqual(quote.ohlc.close);
      expect(quote.ohlc.low).toBeLessThanOrEqual(quote.ohlc.open);
      expect(quote.ohlc.low).toBeLessThanOrEqual(quote.ohlc.close);
    });

    it('should validate RSI is within 0-100 range', () => {
      const allSignals = Object.values(TradingViewSignalFixtures);
      
      allSignals.forEach(signals => {
        expect(signals.indicators.rsi.value).toBeGreaterThanOrEqual(0);
        expect(signals.indicators.rsi.value).toBeLessThanOrEqual(100);
      });
    });

    it('should validate signal strength is within 0-1 range', () => {
      const allSignals = Object.values(TradingViewSignalFixtures);
      
      allSignals.forEach(signals => {
        expect(signals.signalStrength).toBeGreaterThanOrEqual(0);
        expect(signals.signalStrength).toBeLessThanOrEqual(1);
      });
    });
  });

  describe('Edge Cases', () => {
    
    it('should handle zero volume quote', () => {
      const quote = KiteQuoteFixtures.ZERO_VOLUME['NSE:TESTSTOCK'];
      
      expect(quote.volume).toBe(0);
      expect(quote.buy_quantity).toBe(0);
      expect(quote.sell_quantity).toBe(0);
    });

    it('should handle circuit breaker (upper circuit)', () => {
      const quote = KiteQuoteFixtures.CIRCUIT_BREAKER_UP['NSE:CIRCUITSTOCK_UP'];
      
      expect(quote.buy_quantity).toBeGreaterThan(0);
      expect(quote.sell_quantity).toBe(0);
      expect(quote.net_change).toBe(20.00);
    });

    it('should handle circuit breaker (lower circuit)', () => {
      const quote = KiteQuoteFixtures.CIRCUIT_BREAKER_DOWN['NSE:CIRCUITSTOCK_DOWN'];
      
      expect(quote.buy_quantity).toBe(0);
      expect(quote.sell_quantity).toBeGreaterThan(0);
      expect(quote.net_change).toBe(-20.00);
    });

    it('should handle contradictory signals', () => {
      const signals = TradingViewSignalFixtures.CONTRADICTORY_RSI_MACD;
      
      // RSI shows oversold (bullish) but MACD is bearish
      expect(signals.indicators.rsi.signal).toBe('oversold');
      expect(signals.indicators.macd.interpretation).toBe('bearish');
      expect(signals.overallSignal).toBe('neutral');
      expect(signals.signalStrength).toBeLessThan(0.5);
    });
  });
});

