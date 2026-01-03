/**
 * API Client Configuration
 * 
 * Configures Axios with interceptors for request/response handling.
 */

import axios, { type AxiosError, type AxiosResponse } from 'axios'
import type { ErrorResponse } from '@/types/index'

/**
 * Base API client instance.
 * Uses Vite's proxy configuration in development.
 */
export const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor for logging and request modification.
 */
apiClient.interceptors.request.use(
  (config) => {
    // Log requests in development
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor for error handling.
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError<ErrorResponse>) => {
    // Log errors in development
    if (import.meta.env.DEV) {
      console.error('[API Error]', error.response?.data || error.message)
    }

    // Transform error for consistent handling
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    const enhancedError = new Error(message) as Error & { 
      status?: number
      originalError?: AxiosError
    }
    enhancedError.status = error.response?.status
    enhancedError.originalError = error

    return Promise.reject(enhancedError)
  }
)

/**
 * Helper function to extract data from response.
 */
export async function apiRequest<T>(
  promise: Promise<AxiosResponse<T>>
): Promise<T> {
  const response = await promise
  return response.data
}

