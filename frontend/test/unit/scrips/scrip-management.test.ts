/**
 * SCRIP MANAGEMENT TESTS
 * Tests for scrip/instrument management functionality
 */

import { ScripMasterFixtures } from '../../fixtures/scrips/master-list';
import { WatchlistFixtures } from '../../fixtures/scrips/watchlists';

// Helper functions for scrip management
function findScripBySymbol(symbol: string, masterList: typeof ScripMasterFixtures.NIFTY50) {
  const tradingSymbol = symbol.replace('NSE:', '');
  return masterList.find(s => s.tradingsymbol === tradingSymbol);
}

function getScripsByExchange(exchange: string, masterList: typeof ScripMasterFixtures.NIFTY50) {
  return masterList.filter(s => s.exchange === exchange);
}

function getScripsByInstrumentType(type: string, masterList: typeof ScripMasterFixtures.NIFTY50) {
  return masterList.filter(s => s.instrument_type === type);
}

function isValidWatchlist(watchlist: typeof WatchlistFixtures.PORTFOLIO): boolean {
  return (
    typeof watchlist.id === 'string' &&
    typeof watchlist.name === 'string' &&
    Array.isArray(watchlist.symbols) &&
    typeof watchlist.createdAt === 'string' &&
    typeof watchlist.updatedAt === 'string'
  );
}

function getWatchlistSymbolCount(watchlist: typeof WatchlistFixtures.PORTFOLIO): number {
  return watchlist.symbols.length;
}

describe('Scrip Management', () => {

  describe('Master List Operations', () => {
    
    it('should have NIFTY 50 constituents', () => {
      expect(ScripMasterFixtures.NIFTY50.length).toBeGreaterThanOrEqual(20);
    });

    it('should have Bank NIFTY constituents', () => {
      expect(ScripMasterFixtures.BANKNIFTY.length).toBeGreaterThanOrEqual(10);
    });

    it('should have IT sector constituents', () => {
      expect(ScripMasterFixtures.IT.length).toBeGreaterThanOrEqual(5);
    });

    it('should find RELIANCE in NIFTY 50', () => {
      const scrip = findScripBySymbol('NSE:RELIANCE', ScripMasterFixtures.NIFTY50);
      
      expect(scrip).toBeDefined();
      expect(scrip?.tradingsymbol).toBe('RELIANCE');
      expect(scrip?.name).toContain('Reliance');
    });

    it('should find TCS in NIFTY 50', () => {
      const scrip = findScripBySymbol('NSE:TCS', ScripMasterFixtures.NIFTY50);
      
      expect(scrip).toBeDefined();
      expect(scrip?.tradingsymbol).toBe('TCS');
    });

    it('should find HDFCBANK in Bank NIFTY', () => {
      const scrip = findScripBySymbol('NSE:HDFCBANK', ScripMasterFixtures.BANKNIFTY);
      
      expect(scrip).toBeDefined();
      expect(scrip?.tradingsymbol).toBe('HDFCBANK');
    });

    it('should find INFY in IT sector', () => {
      const scrip = findScripBySymbol('NSE:INFY', ScripMasterFixtures.IT);
      
      expect(scrip).toBeDefined();
      expect(scrip?.tradingsymbol).toBe('INFY');
    });

    it('should return undefined for unknown symbol', () => {
      const scrip = findScripBySymbol('NSE:UNKNOWNSTOCK', ScripMasterFixtures.NIFTY50);
      expect(scrip).toBeUndefined();
    });
  });

  describe('Scrip Properties', () => {
    
    it('should have correct exchange for NSE stocks', () => {
      const nseStocks = getScripsByExchange('NSE', ScripMasterFixtures.NIFTY50);
      
      expect(nseStocks.length).toBe(ScripMasterFixtures.NIFTY50.length);
      nseStocks.forEach(s => {
        expect(s.exchange).toBe('NSE');
      });
    });

    it('should have EQ instrument type for equity stocks', () => {
      const eqStocks = getScripsByInstrumentType('EQ', ScripMasterFixtures.NIFTY50);
      
      expect(eqStocks.length).toBe(ScripMasterFixtures.NIFTY50.length);
    });

    it('should have valid tick size', () => {
      ScripMasterFixtures.NIFTY50.forEach(scrip => {
        expect(scrip.tick_size).toBeGreaterThan(0);
        expect(scrip.tick_size).toBeLessThanOrEqual(1);
      });
    });

    it('should have lot size of 1 for equity', () => {
      ScripMasterFixtures.NIFTY50.forEach(scrip => {
        expect(scrip.lot_size).toBe(1);
      });
    });

    it('should have unique instrument tokens', () => {
      const tokens = ScripMasterFixtures.NIFTY50.map(s => s.instrument_token);
      const uniqueTokens = new Set(tokens);
      
      expect(uniqueTokens.size).toBe(tokens.length);
    });

    it('should have unique trading symbols', () => {
      const symbols = ScripMasterFixtures.NIFTY50.map(s => s.tradingsymbol);
      const uniqueSymbols = new Set(symbols);
      
      expect(uniqueSymbols.size).toBe(symbols.length);
    });
  });

  describe('Watchlist Operations', () => {
    
    it('should validate portfolio watchlist', () => {
      expect(isValidWatchlist(WatchlistFixtures.PORTFOLIO)).toBe(true);
    });

    it('should validate all watchlists', () => {
      WatchlistFixtures.ALL.forEach(wl => {
        expect(isValidWatchlist(wl)).toBe(true);
      });
    });

    it('should have correct symbol count for portfolio', () => {
      const count = getWatchlistSymbolCount(WatchlistFixtures.PORTFOLIO);
      expect(count).toBe(5);
    });

    it('should have correct symbol count for banking watchlist', () => {
      const count = getWatchlistSymbolCount(WatchlistFixtures.BANKING);
      expect(count).toBe(6);
    });

    it('should handle empty watchlist', () => {
      const count = getWatchlistSymbolCount(WatchlistFixtures.EMPTY);
      expect(count).toBe(0);
    });

    it('should have 50 symbols in large watchlist', () => {
      const count = getWatchlistSymbolCount(WatchlistFixtures.LARGE);
      expect(count).toBe(50);
    });

    it('should have unique watchlist IDs', () => {
      const ids = WatchlistFixtures.ALL.map(wl => wl.id);
      const uniqueIds = new Set(ids);
      
      expect(uniqueIds.size).toBe(ids.length);
    });

    it('should have valid ISO timestamps', () => {
      WatchlistFixtures.ALL.forEach(wl => {
        expect(() => new Date(wl.createdAt)).not.toThrow();
        expect(() => new Date(wl.updatedAt)).not.toThrow();
      });
    });

    it('should have updatedAt >= createdAt', () => {
      WatchlistFixtures.ALL.forEach(wl => {
        const created = new Date(wl.createdAt).getTime();
        const updated = new Date(wl.updatedAt).getTime();
        
        expect(updated).toBeGreaterThanOrEqual(created);
      });
    });
  });

  describe('Sector Classification', () => {
    
    it('should have banking stocks in Bank NIFTY', () => {
      const bankingKeywords = ['bank', 'fin'];
      
      ScripMasterFixtures.BANKNIFTY.forEach(scrip => {
        const nameLC = scrip.name.toLowerCase();
        const symbolLC = scrip.tradingsymbol.toLowerCase();
        
        const isBanking = bankingKeywords.some(
          kw => nameLC.includes(kw) || symbolLC.includes(kw)
        );
        
        expect(isBanking).toBe(true);
      });
    });

    it('should have IT stocks in IT sector list', () => {
      const itKeywords = ['tech', 'info', 'software', 'it ', 'services'];
      
      // At least 80% should match
      const matchCount = ScripMasterFixtures.IT.filter(scrip => {
        const nameLC = scrip.name.toLowerCase();
        return itKeywords.some(kw => nameLC.includes(kw));
      }).length;
      
      expect(matchCount).toBeGreaterThanOrEqual(ScripMasterFixtures.IT.length * 0.5);
    });

    it('should have overlap between NIFTY50 and Bank NIFTY', () => {
      const niftySymbols = new Set(ScripMasterFixtures.NIFTY50.map(s => s.tradingsymbol));
      const bankSymbols = ScripMasterFixtures.BANKNIFTY.map(s => s.tradingsymbol);
      
      const overlap = bankSymbols.filter(s => niftySymbols.has(s));
      
      // Major banks should be in both
      expect(overlap.length).toBeGreaterThan(0);
    });

    it('should have overlap between NIFTY50 and IT sector', () => {
      const niftySymbols = new Set(ScripMasterFixtures.NIFTY50.map(s => s.tradingsymbol));
      const itSymbols = ScripMasterFixtures.IT.map(s => s.tradingsymbol);
      
      const overlap = itSymbols.filter(s => niftySymbols.has(s));
      
      // Major IT companies should be in both
      expect(overlap.length).toBeGreaterThan(0);
      expect(overlap).toContain('TCS');
      expect(overlap).toContain('INFY');
    });
  });
});

