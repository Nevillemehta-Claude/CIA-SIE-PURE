import type {
  Contradiction,
  Confirmation,
  ChatMessage,
  AIModel,
} from './models'

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export interface HealthResponse {
  status: 'healthy' | 'unhealthy'
  app: string
  version: string
  environment: string
}

export interface NarrativeResponse {
  silo_id: string
  narrative: string
  generated_at: string
  model_used: string
  disclaimer: string
}

export interface PlainNarrativeResponse {
  text: string
  generated_at: string
}

export interface RelationshipResponse {
  silo_id: string
  contradictions: Contradiction[]
  confirmations: Confirmation[]
}

export interface ContradictionsResponse {
  contradictions: Contradiction[]
  count: number
}

export interface AIModelsResponse {
  models: AIModel[]
  default_model: string
  budget_remaining: number
}

export interface AIBudgetResponse {
  limit: number
  used: number
  remaining: number
  percentage_used: number
  alert_threshold: number
  alert_triggered: boolean
}

export interface AIUsageResponse {
  period: 'daily' | 'weekly' | 'monthly'
  input_tokens: number
  output_tokens: number
  total_cost: number
  requests_count: number
  model_breakdown: Record<string, { requests: number; cost: number }>
}

export interface ChatResponse {
  response: string
  conversation_id: string
  model_used: string
  tokens_used: number
  cost: number
}

export interface ChatHistoryResponse {
  scrip_id: string
  conversations: Array<{
    conversation_id: string
    messages: ChatMessage[]
    created_at: string
    total_tokens: number
    total_cost: number
  }>
}

// ============================================================================
// QUERY PARAMETER TYPES
// ============================================================================

export interface InstrumentListParams {
  active_only?: boolean
}

export interface SiloListParams {
  instrument_id?: string
  active_only?: boolean
}

export interface ChartListParams {
  silo_id?: string
  active_only?: boolean
}

export interface SignalListParams {
  limit?: number
}

export interface UsageParams {
  period?: 'daily' | 'weekly' | 'monthly'
}

