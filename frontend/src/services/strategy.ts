import { apiClient, apiRequest } from './client'

const PATH = '/strategy'

/**
 * StrategyEvaluationRequest - Matches backend StrategyEvaluationRequest model exactly
 * @see src/cia_sie/api/routes/strategy.py - StrategyEvaluationRequest
 */
export interface StrategyEvaluationRequest {
  scrip_id: string  // FIXED: was 'silo_id'
  strategy_description: string  // ADDED: required field from backend
  model?: string | null  // ADDED: optional model selection
}

/**
 * StrategyAnalysis - Matches backend StrategyAnalysis model
 * @see src/cia_sie/api/routes/strategy.py - StrategyAnalysis
 */
export interface StrategyAnalysis {
  alignment_with_signals: string
  contradictions_noted: string[]
  confirmations_noted: string[]
  freshness_concerns: string[]
}

/**
 * UsageInfo - AI usage information
 * @see src/cia_sie/api/routes/strategy.py - UsageInfo
 */
export interface StrategyUsageInfo {
  input_tokens: number
  output_tokens: number
  cost: number
  model_used: string
}

/**
 * StrategyEvaluationResponse - Matches backend StrategyEvaluationResponse model exactly
 * @see src/cia_sie/api/routes/strategy.py - StrategyEvaluationResponse
 */
export interface StrategyEvaluationResponse {
  analysis: StrategyAnalysis
  disclaimer: string
  usage: StrategyUsageInfo
}

export async function evaluateStrategy(data: StrategyEvaluationRequest): Promise<StrategyEvaluationResponse> {
  return apiRequest(apiClient.post(`${PATH}/evaluate`, data))
}

