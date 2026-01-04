/**
 * CLAUDE API ERROR FIXTURES
 * Error responses for testing AI service error handling
 */

export interface ClaudeErrorResponse {
  type: 'error';
  error: {
    type: string;
    message: string;
  };
}

export const CLAUDE_ERROR_RATE_LIMITED: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'rate_limit_error',
    message: 'Rate limit exceeded. Please retry after 60 seconds.'
  }
};

export const CLAUDE_ERROR_OVERLOADED: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'overloaded_error',
    message: 'The API is temporarily overloaded. Please try again later.'
  }
};

export const CLAUDE_ERROR_INVALID_REQUEST: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'invalid_request_error',
    message: 'The request body was invalid. Please check the request format.'
  }
};

export const CLAUDE_ERROR_AUTHENTICATION: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'authentication_error',
    message: 'Invalid API key provided.'
  }
};

export const CLAUDE_ERROR_PERMISSION: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'permission_error',
    message: 'Your API key does not have permission to access this resource.'
  }
};

export const CLAUDE_ERROR_NOT_FOUND: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'not_found_error',
    message: 'The requested resource was not found.'
  }
};

export const CLAUDE_ERROR_SERVER: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'api_error',
    message: 'An unexpected error occurred on the server. Please try again.'
  }
};

export const CLAUDE_ERROR_CONTEXT_LENGTH: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'invalid_request_error',
    message: 'The request exceeds the maximum context length allowed.'
  }
};

export const CLAUDE_ERROR_TIMEOUT: ClaudeErrorResponse = {
  type: 'error',
  error: {
    type: 'timeout_error',
    message: 'The request timed out. Please try again with a simpler prompt.'
  }
};

export const ClaudeErrorFixtures = {
  RATE_LIMITED: CLAUDE_ERROR_RATE_LIMITED,
  OVERLOADED: CLAUDE_ERROR_OVERLOADED,
  INVALID_REQUEST: CLAUDE_ERROR_INVALID_REQUEST,
  AUTHENTICATION: CLAUDE_ERROR_AUTHENTICATION,
  PERMISSION: CLAUDE_ERROR_PERMISSION,
  NOT_FOUND: CLAUDE_ERROR_NOT_FOUND,
  SERVER: CLAUDE_ERROR_SERVER,
  CONTEXT_LENGTH: CLAUDE_ERROR_CONTEXT_LENGTH,
  TIMEOUT: CLAUDE_ERROR_TIMEOUT
};

export type ClaudeErrorType = keyof typeof ClaudeErrorFixtures;

