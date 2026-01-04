/**
 * KITE API ERROR FIXTURES
 * All possible error responses for testing error handling
 */

export interface KiteErrorResponse {
  status: 'error';
  message: string;
  error_type: string;
}

export const KITE_ERROR_TOKEN_EXPIRED: KiteErrorResponse = {
  status: 'error',
  message: 'Token is invalid or has expired.',
  error_type: 'TokenException'
};

export const KITE_ERROR_RATE_LIMITED: KiteErrorResponse = {
  status: 'error',
  message: 'Too many requests. Please try again later.',
  error_type: 'NetworkException'
};

export const KITE_ERROR_INVALID_INSTRUMENT: KiteErrorResponse = {
  status: 'error',
  message: 'Instrument not found or not tradable.',
  error_type: 'InputException'
};

export const KITE_ERROR_NETWORK_TIMEOUT: KiteErrorResponse = {
  status: 'error',
  message: 'Request timed out. Please try again.',
  error_type: 'NetworkException'
};

export const KITE_ERROR_MARKET_CLOSED: KiteErrorResponse = {
  status: 'error',
  message: 'Market is closed.',
  error_type: 'InputException'
};

export const KITE_ERROR_PERMISSION_DENIED: KiteErrorResponse = {
  status: 'error',
  message: 'Permission denied. Insufficient privileges.',
  error_type: 'PermissionException'
};

export const KITE_ERROR_GENERAL_EXCEPTION: KiteErrorResponse = {
  status: 'error',
  message: 'An unknown error occurred.',
  error_type: 'GeneralException'
};

export const KITE_ERROR_ORDER_VARIETY_INVALID: KiteErrorResponse = {
  status: 'error',
  message: 'Invalid order variety for this instrument.',
  error_type: 'OrderException'
};

export const KITE_ERROR_DATA_NOT_FOUND: KiteErrorResponse = {
  status: 'error',
  message: 'No data found for the requested period.',
  error_type: 'DataException'
};

export const KITE_ERROR_SESSION_EXPIRED: KiteErrorResponse = {
  status: 'error',
  message: 'Your session has expired. Please login again.',
  error_type: 'TokenException'
};

export const KiteErrorFixtures = {
  TOKEN_EXPIRED: KITE_ERROR_TOKEN_EXPIRED,
  RATE_LIMITED: KITE_ERROR_RATE_LIMITED,
  INVALID_INSTRUMENT: KITE_ERROR_INVALID_INSTRUMENT,
  NETWORK_TIMEOUT: KITE_ERROR_NETWORK_TIMEOUT,
  MARKET_CLOSED: KITE_ERROR_MARKET_CLOSED,
  PERMISSION_DENIED: KITE_ERROR_PERMISSION_DENIED,
  GENERAL_EXCEPTION: KITE_ERROR_GENERAL_EXCEPTION,
  ORDER_VARIETY_INVALID: KITE_ERROR_ORDER_VARIETY_INVALID,
  DATA_NOT_FOUND: KITE_ERROR_DATA_NOT_FOUND,
  SESSION_EXPIRED: KITE_ERROR_SESSION_EXPIRED
};

export type KiteErrorType = keyof typeof KiteErrorFixtures;

