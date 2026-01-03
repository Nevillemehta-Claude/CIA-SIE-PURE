/**
 * Chat API Service
 * 
 * API calls for AI chat functionality.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-001: All responses include mandatory disclaimer
 * - CR-003: All content is validated for prescriptive language
 */

import { apiClient, apiRequest } from './client'
import type { 
  ChatRequest, 
  ChatResponse,
  ConversationHistoryResponse,
  HistoryParams 
} from '@/types/index'

/**
 * Send a chat message.
 * 
 * CR-001 COMPLIANCE: Response includes disclaimer field.
 * The disclaimer MUST be displayed with any AI response.
 */
export async function sendChatMessage(
  instrumentId: string,
  request: ChatRequest
): Promise<ChatResponse> {
  return apiRequest(
    apiClient.post(`/instruments/${instrumentId}/chat`, request)
  )
}

/**
 * Get conversation history for an instrument.
 */
export async function getConversationHistory(
  instrumentId: string,
  params?: HistoryParams
): Promise<ConversationHistoryResponse> {
  return apiRequest(
    apiClient.get(`/instruments/${instrumentId}/chat/history`, { params })
  )
}

