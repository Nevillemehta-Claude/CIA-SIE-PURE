/**
 * WATCHLIST FIXTURES
 * User watchlist data for testing
 */

export interface Watchlist {
  id: string;
  name: string;
  description: string;
  symbols: string[];
  createdAt: string;
  updatedAt: string;
}

export const WATCHLIST_PORTFOLIO: Watchlist = {
  id: 'wl-001',
  name: 'My Portfolio',
  description: 'Stocks currently held in portfolio',
  symbols: ['NSE:RELIANCE', 'NSE:TCS', 'NSE:INFY', 'NSE:HDFCBANK', 'NSE:ICICIBANK'],
  createdAt: '2024-01-01T00:00:00.000Z',
  updatedAt: '2024-01-15T10:00:00.000Z'
};

export const WATCHLIST_BANKING: Watchlist = {
  id: 'wl-002',
  name: 'Banking Sector',
  description: 'Key banking stocks to monitor',
  symbols: ['NSE:HDFCBANK', 'NSE:ICICIBANK', 'NSE:SBIN', 'NSE:KOTAKBANK', 'NSE:AXISBANK', 'NSE:INDUSINDBK'],
  createdAt: '2024-01-02T00:00:00.000Z',
  updatedAt: '2024-01-15T09:30:00.000Z'
};

export const WATCHLIST_IT: Watchlist = {
  id: 'wl-003',
  name: 'IT Sector',
  description: 'Technology and IT services companies',
  symbols: ['NSE:TCS', 'NSE:INFY', 'NSE:WIPRO', 'NSE:HCLTECH', 'NSE:TECHM'],
  createdAt: '2024-01-03T00:00:00.000Z',
  updatedAt: '2024-01-14T16:00:00.000Z'
};

export const WATCHLIST_MOMENTUM: Watchlist = {
  id: 'wl-004',
  name: 'Momentum Plays',
  description: 'Stocks showing strong momentum',
  symbols: ['NSE:TATAMOTORS', 'NSE:M&M', 'NSE:ADANIENT', 'NSE:ADANIPORTS'],
  createdAt: '2024-01-10T00:00:00.000Z',
  updatedAt: '2024-01-15T10:30:00.000Z'
};

export const WATCHLIST_EMPTY: Watchlist = {
  id: 'wl-005',
  name: 'Empty Watchlist',
  description: 'New watchlist with no symbols',
  symbols: [],
  createdAt: '2024-01-15T10:00:00.000Z',
  updatedAt: '2024-01-15T10:00:00.000Z'
};

export const WATCHLIST_LARGE: Watchlist = {
  id: 'wl-006',
  name: 'NIFTY 50 Complete',
  description: 'All NIFTY 50 constituents',
  symbols: [
    'NSE:RELIANCE', 'NSE:TCS', 'NSE:HDFCBANK', 'NSE:INFY', 'NSE:ICICIBANK',
    'NSE:HINDUNILVR', 'NSE:HDFC', 'NSE:SBIN', 'NSE:BAJFINANCE', 'NSE:BHARTIARTL',
    'NSE:KOTAKBANK', 'NSE:ITC', 'NSE:AXISBANK', 'NSE:LT', 'NSE:ASIANPAINT',
    'NSE:MARUTI', 'NSE:SUNPHARMA', 'NSE:TITAN', 'NSE:ULTRACEMCO', 'NSE:NTPC',
    'NSE:NESTLEIND', 'NSE:WIPRO', 'NSE:M&M', 'NSE:POWERGRID', 'NSE:TATAMOTORS',
    'NSE:HCLTECH', 'NSE:COALINDIA', 'NSE:INDUSINDBK', 'NSE:ONGC', 'NSE:TECHM',
    'NSE:DRREDDY', 'NSE:JSWSTEEL', 'NSE:TATASTEEL', 'NSE:ADANIENT', 'NSE:BAJAJFINSV',
    'NSE:HDFCLIFE', 'NSE:BRITANNIA', 'NSE:DIVISLAB', 'NSE:CIPLA', 'NSE:EICHERMOT',
    'NSE:SBILIFE', 'NSE:APOLLOHOSP', 'NSE:GRASIM', 'NSE:BPCL', 'NSE:HEROMOTOCO',
    'NSE:ADANIPORTS', 'NSE:TATACONSUM', 'NSE:UPL', 'NSE:HINDALCO', 'NSE:SHREECEM'
  ],
  createdAt: '2024-01-01T00:00:00.000Z',
  updatedAt: '2024-01-15T10:30:00.000Z'
};

export const WatchlistFixtures = {
  PORTFOLIO: WATCHLIST_PORTFOLIO,
  BANKING: WATCHLIST_BANKING,
  IT: WATCHLIST_IT,
  MOMENTUM: WATCHLIST_MOMENTUM,
  EMPTY: WATCHLIST_EMPTY,
  LARGE: WATCHLIST_LARGE,
  ALL: [WATCHLIST_PORTFOLIO, WATCHLIST_BANKING, WATCHLIST_IT, WATCHLIST_MOMENTUM, WATCHLIST_EMPTY, WATCHLIST_LARGE]
};

