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

export interface NarrativeSection {
  section_type: 'SIGNAL_SUMMARY' | 'CONTRADICTION' | 'CONFIRMATION' | 'FRESHNESS'
  content: string
  referenced_chart_ids: string[]
}

export interface NarrativeResponse {
  narrative_id: string
  silo_id: string
  sections: NarrativeSection[]
  closing_statement: string
  generated_at: string
}

export interface PlainNarrativeResponse {
  text: string
  generated_at: string
}

export interface ChartSignalData {
  chart_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  latest_signal: {
    signal_id: string
    chart_id: string
    received_at: string
    signal_timestamp: string
    signal_type: string
    direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
    indicators: Record<string, unknown>
    raw_payload: Record<string, unknown>
  } | null
  freshness: 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'
}

export interface RelationshipResponse {
  silo_id: string
  silo_name: string
  instrument_id: string
  instrument_symbol: string
  charts: ChartSignalData[]
  contradictions: Contradiction[]
  confirmations: Confirmation[]
  generated_at: string
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
  within_budget: boolean
  percentage_used: number
  remaining: number
  alert_level: string | null
  message: string | null
  // Computed fields for UI (derived from API + known limit)
  limit?: number
  used?: number
  alert_triggered?: boolean
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

