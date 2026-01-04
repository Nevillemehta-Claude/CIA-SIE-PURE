/**
 * TRADINGVIEW ERROR FIXTURES
 * Error responses for testing error handling
 */

export interface TradingViewErrorResponse {
  status: 'error';
  code: string;
  message: string;
  timestamp: string;
}

export const TV_ERROR_SYMBOL_NOT_FOUND: TradingViewErrorResponse = {
  status: 'error',
  code: 'SYMBOL_NOT_FOUND',
  message: 'The requested symbol could not be found.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_RATE_LIMITED: TradingViewErrorResponse = {
  status: 'error',
  code: 'RATE_LIMIT_EXCEEDED',
  message: 'Rate limit exceeded. Please wait before making more requests.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_INVALID_TIMEFRAME: TradingViewErrorResponse = {
  status: 'error',
  code: 'INVALID_TIMEFRAME',
  message: 'The specified timeframe is not supported.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_UNAUTHORIZED: TradingViewErrorResponse = {
  status: 'error',
  code: 'UNAUTHORIZED',
  message: 'Authentication required. Please provide valid credentials.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_SERVICE_UNAVAILABLE: TradingViewErrorResponse = {
  status: 'error',
  code: 'SERVICE_UNAVAILABLE',
  message: 'TradingView service is temporarily unavailable.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_DATA_UNAVAILABLE: TradingViewErrorResponse = {
  status: 'error',
  code: 'DATA_UNAVAILABLE',
  message: 'Technical analysis data is not available for this symbol.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_NETWORK_TIMEOUT: TradingViewErrorResponse = {
  status: 'error',
  code: 'NETWORK_TIMEOUT',
  message: 'Request timed out. Please try again.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TV_ERROR_INVALID_INDICATOR: TradingViewErrorResponse = {
  status: 'error',
  code: 'INVALID_INDICATOR',
  message: 'The requested indicator is not supported.',
  timestamp: '2024-01-15T10:30:00.000Z'
};

export const TradingViewErrorFixtures = {
  SYMBOL_NOT_FOUND: TV_ERROR_SYMBOL_NOT_FOUND,
  RATE_LIMITED: TV_ERROR_RATE_LIMITED,
  INVALID_TIMEFRAME: TV_ERROR_INVALID_TIMEFRAME,
  UNAUTHORIZED: TV_ERROR_UNAUTHORIZED,
  SERVICE_UNAVAILABLE: TV_ERROR_SERVICE_UNAVAILABLE,
  DATA_UNAVAILABLE: TV_ERROR_DATA_UNAVAILABLE,
  NETWORK_TIMEOUT: TV_ERROR_NETWORK_TIMEOUT,
  INVALID_INDICATOR: TV_ERROR_INVALID_INDICATOR
};

export type TradingViewErrorType = keyof typeof TradingViewErrorFixtures;

