import { apiClient, apiRequest } from './client'
import type { ChatResponse, ChatHistoryResponse } from '@/types/api'

const PATH = '/chat'

export async function sendMessage(
  scripId: string,
  message: string,
  model?: string
): Promise<ChatResponse> {
  return apiRequest(apiClient.post(`${PATH}/${scripId}`, { message, model }))
}

export async function getHistory(
  scripId: string,
  limit?: number
): Promise<ChatHistoryResponse> {
  return apiRequest(apiClient.get(`${PATH}/${scripId}/history`, { params: { limit } }))
}

