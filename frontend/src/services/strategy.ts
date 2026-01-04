import { apiClient, apiRequest } from './client'

const PATH = '/strategy'

export interface StrategyEvaluationRequest {
  silo_id: string
  include_narrative?: boolean
}

export interface StrategyEvaluationResponse {
  silo_id: string
  evaluation_id: string
  signals_analyzed: number
  contradictions_found: number
  confirmations_found: number
  overall_direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL' | 'MIXED'
  narrative?: string
  generated_at: string
}

export async function evaluateStrategy(data: StrategyEvaluationRequest): Promise<StrategyEvaluationResponse> {
  return apiRequest(apiClient.post(`${PATH}/evaluate`, data))
}

