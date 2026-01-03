/**
 * AI API Service
 * 
 * API calls for AI configuration and usage tracking.
 */

import { apiClient, apiRequest } from './client'
import type { 
  AIModelsResponse, 
  AIBudgetResponse, 
  AIHealthResponse,
  AIUsage,
  UsageParams 
} from '@/types/index'

const BASE_PATH = '/ai'

/**
 * Get available AI models.
 */
export async function getAIModels(): Promise<AIModelsResponse> {
  return apiRequest(apiClient.get(`${BASE_PATH}/models`))
}

/**
 * Get AI budget status.
 */
export async function getAIBudget(): Promise<AIBudgetResponse> {
  return apiRequest(apiClient.get(`${BASE_PATH}/budget`))
}

/**
 * Get AI health status.
 */
export async function getAIHealth(): Promise<AIHealthResponse> {
  return apiRequest(apiClient.get(`${BASE_PATH}/health`))
}

/**
 * Get AI usage statistics.
 */
export async function getAIUsage(
  params?: UsageParams
): Promise<AIUsage> {
  return apiRequest(apiClient.get(`${BASE_PATH}/usage`, { params }))
}

