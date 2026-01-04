/**
 * KITE API QUOTE MOCK FIXTURES
 * Schema validated against Kite Connect API v3
 */

export interface KiteQuote {
  instrument_token: number;
  timestamp: string;
  last_trade_time: string;
  last_price: number;
  last_quantity: number;
  buy_quantity: number;
  sell_quantity: number;
  volume: number;
  average_price: number;
  ohlc: {
    open: number;
    high: number;
    low: number;
    close: number;
  };
  net_change: number;
  oi: number;
  depth: {
    buy: Array<{ price: number; quantity: number; orders: number }>;
    sell: Array<{ price: number; quantity: number; orders: number }>;
  };
}

// RELIANCE Quote Fixture
export const KITE_QUOTE_RELIANCE = {
  'NSE:RELIANCE': {
    instrument_token: 738561,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T10:29:58.000Z',
    last_price: 2456.75,
    last_quantity: 100,
    buy_quantity: 150000,
    sell_quantity: 120000,
    volume: 2500000,
    average_price: 2450.25,
    ohlc: { open: 2445.00, high: 2468.50, low: 2440.00, close: 2442.30 },
    net_change: 14.45,
    oi: 0,
    depth: {
      buy: [
        { price: 2456.50, quantity: 500, orders: 5 },
        { price: 2456.25, quantity: 750, orders: 8 }
      ],
      sell: [
        { price: 2457.00, quantity: 400, orders: 4 },
        { price: 2457.25, quantity: 600, orders: 6 }
      ]
    }
  }
};

// TCS Quote Fixture
export const KITE_QUOTE_TCS = {
  'NSE:TCS': {
    instrument_token: 2953217,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T10:29:58.000Z',
    last_price: 3890.50,
    last_quantity: 50,
    buy_quantity: 85000,
    sell_quantity: 72000,
    volume: 1200000,
    average_price: 3885.00,
    ohlc: { open: 3875.00, high: 3905.00, low: 3870.00, close: 3880.25 },
    net_change: 10.25,
    oi: 0,
    depth: {
      buy: [
        { price: 3890.00, quantity: 300, orders: 3 },
        { price: 3889.75, quantity: 450, orders: 5 }
      ],
      sell: [
        { price: 3891.00, quantity: 250, orders: 2 },
        { price: 3891.50, quantity: 400, orders: 4 }
      ]
    }
  }
};

// INFY Quote Fixture  
export const KITE_QUOTE_INFY = {
  'NSE:INFY': {
    instrument_token: 408065,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T10:29:58.000Z',
    last_price: 1567.80,
    last_quantity: 75,
    buy_quantity: 200000,
    sell_quantity: 180000,
    volume: 3500000,
    average_price: 1560.50,
    ohlc: { open: 1555.00, high: 1575.00, low: 1550.00, close: 1558.40 },
    net_change: 9.40,
    oi: 0,
    depth: {
      buy: [
        { price: 1567.50, quantity: 600, orders: 6 },
        { price: 1567.25, quantity: 800, orders: 9 }
      ],
      sell: [
        { price: 1568.00, quantity: 500, orders: 5 },
        { price: 1568.25, quantity: 700, orders: 7 }
      ]
    }
  }
};

function generateMockQuote(token: number, price: number, volume: number): Partial<KiteQuote> {
  return {
    instrument_token: token,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T10:29:58.000Z',
    last_price: price,
    last_quantity: Math.floor(Math.random() * 100) + 10,
    buy_quantity: Math.floor(volume * 0.1),
    sell_quantity: Math.floor(volume * 0.08),
    volume: volume,
    average_price: price * 0.998,
    ohlc: {
      open: price * 0.99,
      high: price * 1.01,
      low: price * 0.98,
      close: price * 0.995
    },
    net_change: price * 0.005,
    oi: 0,
    depth: {
      buy: [
        { price: price - 0.5, quantity: 500, orders: 5 },
        { price: price - 0.75, quantity: 750, orders: 8 }
      ],
      sell: [
        { price: price + 0.5, quantity: 400, orders: 4 },
        { price: price + 0.75, quantity: 600, orders: 6 }
      ]
    }
  };
}

// BULK 50 SCRIPS for performance testing
export const KITE_BULK_QUOTES_50: Record<string, Partial<KiteQuote>> = {
  ...KITE_QUOTE_RELIANCE,
  ...KITE_QUOTE_TCS,
  ...KITE_QUOTE_INFY,
  'NSE:HDFC': generateMockQuote(341249, 2750.50, 1500000),
  'NSE:ICICIBANK': generateMockQuote(1270529, 1025.75, 2200000),
  'NSE:SBIN': generateMockQuote(779521, 625.50, 4500000),
  'NSE:HDFCBANK': generateMockQuote(1260545, 1650.25, 1800000),
  'NSE:KOTAKBANK': generateMockQuote(1922817, 1750.00, 1100000),
  'NSE:BAJFINANCE': generateMockQuote(81153, 7250.00, 800000),
  'NSE:AXISBANK': generateMockQuote(1510401, 1125.50, 2500000),
  'NSE:INDUSINDBK': generateMockQuote(1346049, 1450.75, 900000),
  'NSE:LT': generateMockQuote(2939649, 3150.00, 600000),
  'NSE:ITC': generateMockQuote(424961, 465.50, 5500000),
  'NSE:HINDUNILVR': generateMockQuote(356865, 2550.00, 700000),
  'NSE:MARUTI': generateMockQuote(2815745, 10500.00, 300000),
  'NSE:TATAMOTORS': generateMockQuote(884737, 725.00, 3200000),
  'NSE:M&M': generateMockQuote(519937, 1625.00, 1200000),
  'NSE:SUNPHARMA': generateMockQuote(857857, 1150.00, 1000000),
  'NSE:DRREDDY': generateMockQuote(225537, 5600.00, 250000),
  'NSE:CIPLA': generateMockQuote(177665, 1225.00, 800000),
  'NSE:TITAN': generateMockQuote(897537, 3200.00, 450000),
  'NSE:ASIANPAINT': generateMockQuote(60417, 3050.00, 500000),
  'NSE:ULTRACEMCO': generateMockQuote(2952193, 8200.00, 200000),
  'NSE:GRASIM': generateMockQuote(315393, 2100.00, 400000),
  'NSE:BHARTIARTL': generateMockQuote(2714625, 1050.00, 2000000),
  'NSE:ONGC': generateMockQuote(633601, 215.50, 6000000),
  'NSE:NTPC': generateMockQuote(2977281, 285.00, 4500000),
  'NSE:POWERGRID': generateMockQuote(3834113, 245.00, 3500000),
  'NSE:COALINDIA': generateMockQuote(5215745, 375.00, 2500000),
  'NSE:HINDALCO': generateMockQuote(348929, 550.00, 2000000),
  'NSE:JSWSTEEL': generateMockQuote(3001089, 825.00, 1500000),
  'NSE:TATASTEEL': generateMockQuote(895745, 140.00, 8000000),
  'NSE:ADANIPORTS': generateMockQuote(3861249, 1050.00, 1200000),
  'NSE:ADANIENT': generateMockQuote(6401, 2850.00, 700000),
  'NSE:WIPRO': generateMockQuote(969473, 485.00, 2800000),
  'NSE:HCLTECH': generateMockQuote(1850625, 1425.00, 1000000),
  'NSE:TECHM': generateMockQuote(3465729, 1275.00, 800000),
  'NSE:NESTLEIND': generateMockQuote(4598529, 2450.00, 150000),
  'NSE:BRITANNIA': generateMockQuote(140033, 5100.00, 200000),
  'NSE:DIVISLAB': generateMockQuote(2800641, 3750.00, 300000),
  'NSE:APOLLOHOSP': generateMockQuote(152321, 6100.00, 180000),
  'NSE:EICHERMOT': generateMockQuote(232961, 3850.00, 250000),
  'NSE:HEROMOTOCO': generateMockQuote(345089, 4200.00, 350000),
  'NSE:BAJAJ-AUTO': generateMockQuote(4267265, 6500.00, 200000),
  'NSE:BPCL': generateMockQuote(134657, 525.00, 2200000),
  'NSE:SBILIFE': generateMockQuote(5582849, 1425.00, 600000),
  'NSE:HDFCLIFE': generateMockQuote(119553, 625.00, 1500000),
  'NSE:UPL': generateMockQuote(2889473, 525.00, 900000),
  'NSE:TATACONSUM': generateMockQuote(878593, 925.00, 700000),
  'NSE:SHREECEM': generateMockQuote(794369, 26500.00, 50000),
  'NSE:BAJAJHLDNG': generateMockQuote(4268801, 7500.00, 30000),
};

// EDGE CASE: Zero Volume
export const KITE_QUOTE_ZERO_VOLUME = {
  'NSE:TESTSTOCK': {
    instrument_token: 999999,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T09:15:00.000Z',
    last_price: 100.00,
    last_quantity: 0,
    buy_quantity: 0,
    sell_quantity: 0,
    volume: 0,
    average_price: 100.00,
    ohlc: { open: 100.00, high: 100.00, low: 100.00, close: 100.00 },
    net_change: 0,
    oi: 0,
    depth: {
      buy: [],
      sell: []
    }
  }
};

// EDGE CASE: Circuit Breaker (Upper)
export const KITE_QUOTE_CIRCUIT_BREAKER_UP = {
  'NSE:CIRCUITSTOCK_UP': {
    instrument_token: 888888,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T09:20:00.000Z',
    last_price: 120.00,
    last_quantity: 100,
    buy_quantity: 5000000,
    sell_quantity: 0,
    volume: 1000000,
    average_price: 115.00,
    ohlc: { open: 100.00, high: 120.00, low: 100.00, close: 100.00 },
    net_change: 20.00, // 20% up - circuit breaker hit
    oi: 0,
    depth: {
      buy: [
        { price: 120.00, quantity: 5000000, orders: 10000 }
      ],
      sell: []
    }
  }
};

// EDGE CASE: Circuit Breaker (Lower)
export const KITE_QUOTE_CIRCUIT_BREAKER_DOWN = {
  'NSE:CIRCUITSTOCK_DOWN': {
    instrument_token: 777777,
    timestamp: '2024-01-15T10:30:00.000Z',
    last_trade_time: '2024-01-15T09:20:00.000Z',
    last_price: 80.00,
    last_quantity: 100,
    buy_quantity: 0,
    sell_quantity: 5000000,
    volume: 1000000,
    average_price: 85.00,
    ohlc: { open: 100.00, high: 100.00, low: 80.00, close: 100.00 },
    net_change: -20.00, // 20% down - circuit breaker hit
    oi: 0,
    depth: {
      buy: [],
      sell: [
        { price: 80.00, quantity: 5000000, orders: 10000 }
      ]
    }
  }
};

export const KiteQuoteFixtures = {
  RELIANCE: KITE_QUOTE_RELIANCE,
  TCS: KITE_QUOTE_TCS,
  INFY: KITE_QUOTE_INFY,
  BULK_50: KITE_BULK_QUOTES_50,
  ZERO_VOLUME: KITE_QUOTE_ZERO_VOLUME,
  CIRCUIT_BREAKER_UP: KITE_QUOTE_CIRCUIT_BREAKER_UP,
  CIRCUIT_BREAKER_DOWN: KITE_QUOTE_CIRCUIT_BREAKER_DOWN
};

