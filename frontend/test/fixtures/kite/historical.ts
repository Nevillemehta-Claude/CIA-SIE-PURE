/**
 * KITE API HISTORICAL DATA FIXTURES
 * OHLCV candle data for testing historical analysis
 */

export interface KiteCandle {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  oi?: number;
}

// RELIANCE - 20 days of daily data (bullish trend)
export const KITE_HISTORICAL_RELIANCE_DAILY: KiteCandle[] = [
  { date: '2024-01-01', open: 2380, high: 2395, low: 2370, close: 2388, volume: 2100000 },
  { date: '2024-01-02', open: 2390, high: 2408, low: 2385, close: 2402, volume: 2250000 },
  { date: '2024-01-03', open: 2405, high: 2420, low: 2398, close: 2412, volume: 2400000 },
  { date: '2024-01-04', open: 2415, high: 2430, low: 2408, close: 2425, volume: 2350000 },
  { date: '2024-01-05', open: 2428, high: 2445, low: 2420, close: 2438, volume: 2500000 },
  { date: '2024-01-08', open: 2440, high: 2455, low: 2432, close: 2448, volume: 2300000 },
  { date: '2024-01-09', open: 2450, high: 2468, low: 2445, close: 2462, volume: 2600000 },
  { date: '2024-01-10', open: 2465, high: 2478, low: 2458, close: 2470, volume: 2450000 },
  { date: '2024-01-11', open: 2472, high: 2485, low: 2465, close: 2478, volume: 2550000 },
  { date: '2024-01-12', open: 2480, high: 2495, low: 2475, close: 2488, volume: 2700000 },
  { date: '2024-01-15', open: 2445, high: 2468, low: 2440, close: 2456, volume: 2500000 },
  { date: '2024-01-16', open: 2458, high: 2472, low: 2452, close: 2465, volume: 2350000 },
  { date: '2024-01-17', open: 2468, high: 2482, low: 2460, close: 2475, volume: 2400000 },
  { date: '2024-01-18', open: 2478, high: 2492, low: 2470, close: 2485, volume: 2550000 },
  { date: '2024-01-19', open: 2488, high: 2505, low: 2482, close: 2498, volume: 2650000 },
  { date: '2024-01-22', open: 2500, high: 2518, low: 2495, close: 2512, volume: 2800000 },
  { date: '2024-01-23', open: 2515, high: 2530, low: 2508, close: 2525, volume: 2750000 },
  { date: '2024-01-24', open: 2528, high: 2545, low: 2520, close: 2538, volume: 2900000 },
  { date: '2024-01-25', open: 2540, high: 2558, low: 2535, close: 2552, volume: 2850000 },
  { date: '2024-01-26', open: 2555, high: 2572, low: 2548, close: 2565, volume: 3000000 }
];

// INFY - 20 days of daily data (bearish trend)
export const KITE_HISTORICAL_INFY_DAILY: KiteCandle[] = [
  { date: '2024-01-01', open: 1620, high: 1628, low: 1610, close: 1615, volume: 3000000 },
  { date: '2024-01-02', open: 1612, high: 1622, low: 1605, close: 1608, volume: 3200000 },
  { date: '2024-01-03', open: 1605, high: 1615, low: 1598, close: 1602, volume: 3400000 },
  { date: '2024-01-04', open: 1600, high: 1610, low: 1592, close: 1595, volume: 3300000 },
  { date: '2024-01-05', open: 1592, high: 1602, low: 1585, close: 1588, volume: 3500000 },
  { date: '2024-01-08', open: 1585, high: 1595, low: 1578, close: 1582, volume: 3600000 },
  { date: '2024-01-09', open: 1580, high: 1592, low: 1575, close: 1578, volume: 3700000 },
  { date: '2024-01-10', open: 1575, high: 1585, low: 1568, close: 1572, volume: 3550000 },
  { date: '2024-01-11', open: 1570, high: 1580, low: 1565, close: 1568, volume: 3650000 },
  { date: '2024-01-12', open: 1565, high: 1575, low: 1558, close: 1562, volume: 3800000 },
  { date: '2024-01-15', open: 1560, high: 1575, low: 1550, close: 1567, volume: 3500000 },
  { date: '2024-01-16', open: 1565, high: 1572, low: 1555, close: 1558, volume: 3400000 },
  { date: '2024-01-17', open: 1555, high: 1565, low: 1548, close: 1552, volume: 3600000 },
  { date: '2024-01-18', open: 1550, high: 1560, low: 1542, close: 1545, volume: 3750000 },
  { date: '2024-01-19', open: 1542, high: 1552, low: 1535, close: 1538, volume: 3900000 },
  { date: '2024-01-22', open: 1535, high: 1545, low: 1528, close: 1532, volume: 4000000 },
  { date: '2024-01-23', open: 1530, high: 1540, low: 1522, close: 1525, volume: 3850000 },
  { date: '2024-01-24', open: 1522, high: 1532, low: 1515, close: 1518, volume: 4100000 },
  { date: '2024-01-25', open: 1515, high: 1525, low: 1508, close: 1512, volume: 4000000 },
  { date: '2024-01-26', open: 1510, high: 1520, low: 1502, close: 1505, volume: 4200000 }
];

// SBIN - 20 days of daily data (sideways/consolidating)
export const KITE_HISTORICAL_SBIN_DAILY: KiteCandle[] = [
  { date: '2024-01-01', open: 620, high: 628, low: 615, close: 625, volume: 4200000 },
  { date: '2024-01-02', open: 626, high: 632, low: 618, close: 622, volume: 4100000 },
  { date: '2024-01-03', open: 620, high: 630, low: 615, close: 628, volume: 4300000 },
  { date: '2024-01-04', open: 630, high: 635, low: 620, close: 623, volume: 4000000 },
  { date: '2024-01-05', open: 622, high: 632, low: 618, close: 630, volume: 4400000 },
  { date: '2024-01-08', open: 632, high: 638, low: 625, close: 627, volume: 4200000 },
  { date: '2024-01-09', open: 625, high: 635, low: 620, close: 633, volume: 4500000 },
  { date: '2024-01-10', open: 635, high: 640, low: 628, close: 630, volume: 4100000 },
  { date: '2024-01-11', open: 628, high: 638, low: 622, close: 635, volume: 4600000 },
  { date: '2024-01-12', open: 637, high: 642, low: 630, close: 632, volume: 4300000 },
  { date: '2024-01-15', open: 630, high: 640, low: 620, close: 625, volume: 4500000 },
  { date: '2024-01-16', open: 623, high: 633, low: 618, close: 630, volume: 4400000 },
  { date: '2024-01-17', open: 632, high: 638, low: 625, close: 627, volume: 4200000 },
  { date: '2024-01-18', open: 625, high: 635, low: 620, close: 633, volume: 4600000 },
  { date: '2024-01-19', open: 635, high: 642, low: 628, close: 630, volume: 4300000 },
  { date: '2024-01-22', open: 628, high: 638, low: 622, close: 635, volume: 4700000 },
  { date: '2024-01-23', open: 637, high: 645, low: 630, close: 632, volume: 4400000 },
  { date: '2024-01-24', open: 630, high: 640, low: 625, close: 638, volume: 4800000 },
  { date: '2024-01-25', open: 640, high: 648, low: 632, close: 635, volume: 4500000 },
  { date: '2024-01-26', open: 633, high: 642, low: 628, close: 640, volume: 4900000 }
];

// 5-minute intraday data (1 day)
export const KITE_HISTORICAL_RELIANCE_5MIN: KiteCandle[] = [
  { date: '2024-01-15T09:15:00', open: 2445, high: 2450, low: 2442, close: 2448, volume: 150000 },
  { date: '2024-01-15T09:20:00', open: 2448, high: 2455, low: 2446, close: 2453, volume: 145000 },
  { date: '2024-01-15T09:25:00', open: 2454, high: 2458, low: 2450, close: 2455, volume: 138000 },
  { date: '2024-01-15T09:30:00', open: 2456, high: 2462, low: 2454, close: 2460, volume: 142000 },
  { date: '2024-01-15T09:35:00', open: 2460, high: 2465, low: 2458, close: 2463, volume: 135000 },
  { date: '2024-01-15T09:40:00', open: 2463, high: 2468, low: 2461, close: 2466, volume: 128000 },
  { date: '2024-01-15T09:45:00', open: 2466, high: 2470, low: 2464, close: 2468, volume: 132000 },
  { date: '2024-01-15T09:50:00', open: 2468, high: 2472, low: 2465, close: 2470, volume: 140000 },
  { date: '2024-01-15T09:55:00', open: 2470, high: 2475, low: 2468, close: 2473, volume: 148000 },
  { date: '2024-01-15T10:00:00', open: 2472, high: 2478, low: 2470, close: 2476, volume: 155000 },
  { date: '2024-01-15T10:05:00', open: 2476, high: 2480, low: 2472, close: 2478, volume: 160000 },
  { date: '2024-01-15T10:10:00', open: 2478, high: 2482, low: 2475, close: 2480, volume: 152000 },
  { date: '2024-01-15T10:15:00', open: 2480, high: 2485, low: 2478, close: 2483, volume: 145000 },
  { date: '2024-01-15T10:20:00', open: 2483, high: 2488, low: 2480, close: 2485, volume: 138000 },
  { date: '2024-01-15T10:25:00', open: 2485, high: 2490, low: 2482, close: 2488, volume: 142000 },
  { date: '2024-01-15T10:30:00', open: 2488, high: 2492, low: 2485, close: 2490, volume: 150000 }
];

export const KiteHistoricalFixtures = {
  RELIANCE_DAILY: KITE_HISTORICAL_RELIANCE_DAILY,
  INFY_DAILY: KITE_HISTORICAL_INFY_DAILY,
  SBIN_DAILY: KITE_HISTORICAL_SBIN_DAILY,
  RELIANCE_5MIN: KITE_HISTORICAL_RELIANCE_5MIN
};

