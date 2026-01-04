/**
 * SCRIP MASTER DATA FIXTURES
 * Instrument master data for testing
 */

export interface ScripMaster {
  instrument_token: number;
  tradingsymbol: string;
  name: string;
  exchange: string;
  segment: string;
  instrument_type: string;
  tick_size: number;
  lot_size: number;
  expiry?: string;
  strike?: number;
}

// NIFTY 50 Constituents (partial list)
export const SCRIP_MASTER_NIFTY50: ScripMaster[] = [
  { instrument_token: 738561, tradingsymbol: 'RELIANCE', name: 'Reliance Industries Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2953217, tradingsymbol: 'TCS', name: 'Tata Consultancy Services Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 408065, tradingsymbol: 'INFY', name: 'Infosys Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 341249, tradingsymbol: 'HDFC', name: 'Housing Development Finance Corporation Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1270529, tradingsymbol: 'ICICIBANK', name: 'ICICI Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 779521, tradingsymbol: 'SBIN', name: 'State Bank of India', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1260545, tradingsymbol: 'HDFCBANK', name: 'HDFC Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1922817, tradingsymbol: 'KOTAKBANK', name: 'Kotak Mahindra Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 81153, tradingsymbol: 'BAJFINANCE', name: 'Bajaj Finance Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1510401, tradingsymbol: 'AXISBANK', name: 'Axis Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1346049, tradingsymbol: 'INDUSINDBK', name: 'IndusInd Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2939649, tradingsymbol: 'LT', name: 'Larsen & Toubro Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 424961, tradingsymbol: 'ITC', name: 'ITC Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 356865, tradingsymbol: 'HINDUNILVR', name: 'Hindustan Unilever Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2815745, tradingsymbol: 'MARUTI', name: 'Maruti Suzuki India Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 884737, tradingsymbol: 'TATAMOTORS', name: 'Tata Motors Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 519937, tradingsymbol: 'M&M', name: 'Mahindra & Mahindra Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 857857, tradingsymbol: 'SUNPHARMA', name: 'Sun Pharmaceutical Industries Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 225537, tradingsymbol: 'DRREDDY', name: 'Dr. Reddys Laboratories Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 177665, tradingsymbol: 'CIPLA', name: 'Cipla Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 897537, tradingsymbol: 'TITAN', name: 'Titan Company Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 60417, tradingsymbol: 'ASIANPAINT', name: 'Asian Paints Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2952193, tradingsymbol: 'ULTRACEMCO', name: 'UltraTech Cement Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 315393, tradingsymbol: 'GRASIM', name: 'Grasim Industries Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2714625, tradingsymbol: 'BHARTIARTL', name: 'Bharti Airtel Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 969473, tradingsymbol: 'WIPRO', name: 'Wipro Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1850625, tradingsymbol: 'HCLTECH', name: 'HCL Technologies Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 3465729, tradingsymbol: 'TECHM', name: 'Tech Mahindra Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 633601, tradingsymbol: 'ONGC', name: 'Oil and Natural Gas Corporation Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2977281, tradingsymbol: 'NTPC', name: 'NTPC Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 }
];

// Bank NIFTY Constituents
export const SCRIP_MASTER_BANKNIFTY: ScripMaster[] = [
  { instrument_token: 1260545, tradingsymbol: 'HDFCBANK', name: 'HDFC Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1270529, tradingsymbol: 'ICICIBANK', name: 'ICICI Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 779521, tradingsymbol: 'SBIN', name: 'State Bank of India', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1922817, tradingsymbol: 'KOTAKBANK', name: 'Kotak Mahindra Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1510401, tradingsymbol: 'AXISBANK', name: 'Axis Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1346049, tradingsymbol: 'INDUSINDBK', name: 'IndusInd Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2745857, tradingsymbol: 'BANDHANBNK', name: 'Bandhan Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 4922113, tradingsymbol: 'FEDERALBNK', name: 'Federal Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2865921, tradingsymbol: 'IDFCFIRSTB', name: 'IDFC First Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 3637761, tradingsymbol: 'PNB', name: 'Punjab National Bank', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2796801, tradingsymbol: 'BANKBARODA', name: 'Bank of Baroda', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2763265, tradingsymbol: 'AUBANK', name: 'AU Small Finance Bank Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 }
];

// IT Sector Constituents
export const SCRIP_MASTER_IT: ScripMaster[] = [
  { instrument_token: 2953217, tradingsymbol: 'TCS', name: 'Tata Consultancy Services Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 408065, tradingsymbol: 'INFY', name: 'Infosys Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 969473, tradingsymbol: 'WIPRO', name: 'Wipro Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 1850625, tradingsymbol: 'HCLTECH', name: 'HCL Technologies Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 3465729, tradingsymbol: 'TECHM', name: 'Tech Mahindra Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2883073, tradingsymbol: 'LTIM', name: 'LTIMindtree Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2889473, tradingsymbol: 'MPHASIS', name: 'Mphasis Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 173057, tradingsymbol: 'COFORGE', name: 'Coforge Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2912513, tradingsymbol: 'PERSISTENT', name: 'Persistent Systems Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 },
  { instrument_token: 2760193, tradingsymbol: 'LTTS', name: 'L&T Technology Services Limited', exchange: 'NSE', segment: 'NSE', instrument_type: 'EQ', tick_size: 0.05, lot_size: 1 }
];

export const ScripMasterFixtures = {
  NIFTY50: SCRIP_MASTER_NIFTY50,
  BANKNIFTY: SCRIP_MASTER_BANKNIFTY,
  IT: SCRIP_MASTER_IT
};

