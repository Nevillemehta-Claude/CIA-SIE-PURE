import { apiClient, apiRequest } from './client'
import type { AIModelsResponse, AIBudgetResponse, AIUsageResponse, UsageParams } from '@/types/api'

const PATH = '/ai'

export async function getModels(): Promise<AIModelsResponse> {
  return apiRequest(apiClient.get(`${PATH}/models`))
}

export async function getBudget(): Promise<AIBudgetResponse> {
  return apiRequest(apiClient.get(`${PATH}/budget`))
}

export async function getUsage(params?: UsageParams): Promise<AIUsageResponse> {
  return apiRequest(apiClient.get(`${PATH}/usage`, { params }))
}

export async function getHealth(): Promise<{ status: string }> {
  return apiRequest(apiClient.get(`${PATH}/health`))
}

