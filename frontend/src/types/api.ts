/**
 * API Request/Response Type Definitions
 * 
 * GOVERNED BY: BACKEND_ARCHITECTURAL_FLOWCHART.md
 * 
 * All API types ensure constitutional compliance by:
 * - Including mandatory disclaimers in AI responses
 * - Excluding prohibited fields (weight, score, confidence)
 * - Preserving signal equality
 */

import { Direction, BasketType, MessageRole } from './enums'

// ============================================================================
// Request Types
// ============================================================================

/**
 * Chat request to AI assistant.
 */
export interface ChatRequest {
  message: string
  model?: string
  include_context?: boolean
  conversation_id?: string
}

/**
 * Strategy evaluation request.
 */
export interface StrategyEvaluateRequest {
  scrip_id: string
  strategy_description: string
  model?: string
}

/**
 * Webhook payload from TradingView.
 */
export interface WebhookPayload {
  webhook_id: string
  direction: Direction
  indicators?: Record<string, unknown>
}

/**
 * Basket creation request.
 */
export interface BasketCreateRequest {
  basket_name: string
  basket_type?: BasketType
  description?: string
  instrument_id?: string
  chart_ids?: string[]
}

// ============================================================================
// Response Types
// ============================================================================

/**
 * Chat response from AI assistant.
 * 
 * MANDATORY: disclaimer field must always be displayed (CR-001)
 */
export interface ChatResponse {
  conversation_id: string
  message: {
    role: 'assistant'
    content: string
  }
  context_used: {
    signals_included: number
    charts_referenced: string[]
  }
  usage: {
    input_tokens: number
    output_tokens: number
    cost: number
    model_used: string
  }
  /** MANDATORY - must always be displayed per CR-001 */
  disclaimer: string
}

/**
 * Strategy evaluation response.
 * 
 * MANDATORY: disclaimer field must always be displayed (CR-001)
 */
export interface StrategyEvaluateResponse {
  analysis: {
    alignment_with_signals: string
    contradictions_noted: string[]
    confirmations_noted: string[]
    freshness_concerns: string[]
  }
  /** MANDATORY - must always be displayed per CR-001 */
  disclaimer: string
  usage: {
    input_tokens: number
    output_tokens: number
    cost: number
    model_used: string
  }
}

/**
 * Webhook processing response.
 */
export interface WebhookResponse {
  status: 'accepted' | 'rejected'
  signal_id?: string
  chart_id?: string
  direction?: Direction
  received_at?: string
  error?: string
}

/**
 * AI models available response.
 */
export interface AIModelsResponse {
  models: AIModel[]
  default_model: string
  budget_remaining: number
}

/**
 * AI budget status response.
 */
export interface AIBudgetResponse {
  limit: number
  used: number
  remaining: number
  percentage_used: number
  alert_threshold: number
  alert_triggered: boolean
}

/**
 * AI health check response.
 */
export interface AIHealthResponse {
  status: 'healthy' | 'unhealthy'
  api_key_configured: boolean
  last_successful_call: string
  error_rate_24h: number
}

/**
 * Conversation history response.
 */
export interface ConversationHistoryResponse {
  scrip_id: string
  conversations: Array<{
    conversation_id: string
    messages: ChatMessage[]
    created_at: string
    total_tokens: number
    total_cost: number
  }>
}

/**
 * Platform status response.
 */
export interface PlatformStatusResponse {
  platform_name: string
  status: 'healthy' | 'unhealthy'
  last_heartbeat?: string
  latency_ms?: number
}

/**
 * Platform setup instructions response.
 */
export interface PlatformSetupResponse {
  platform_name: string
  display_name: string
  instructions: string[]
  documentation_url: string
}

/**
 * Health check response.
 */
export interface HealthStatus {
  status: 'healthy' | 'unhealthy'
  version: string
  timestamp: string
}

/**
 * Error response from API.
 */
export interface ErrorResponse {
  detail: string
}

// ============================================================================
// Supporting Types
// ============================================================================

/**
 * AI model information.
 */
export interface AIModel {
  id: string
  display_name: string
  description: string
  cost_per_1k_input_tokens: number
  cost_per_1k_output_tokens: number
  max_tokens: number
  capabilities: string[]
  recommended_for: string[]
}

/**
 * Chat message in a conversation.
 */
export interface ChatMessage {
  role: MessageRole
  content: string
  timestamp: string
}

/**
 * AI usage statistics.
 */
export interface AIUsage {
  period: string
  period_start: string
  period_end: string
  tokens_used: {
    input: number
    output: number
    total: number
  }
  cost: {
    amount: number
    currency: string
  }
  budget: {
    limit: number
    used: number
    remaining: number
    percentage_used: number
  }
  requests_count: number
  average_tokens_per_request: number
  model_breakdown: Array<{
    model_id: string
    requests: number
    tokens: number
    cost: number
  }>
}

/**
 * Analytical basket for grouping charts.
 * 
 * CRITICAL: Baskets are organizational/display constructs ONLY.
 * They have ZERO impact on signal processing.
 */
export interface AnalyticalBasket {
  basket_id: string
  basket_name: string
  basket_type: BasketType
  description?: string
  instrument_id?: string
  chart_ids: string[]
  created_at: string
  updated_at: string
  is_active: boolean
}

/**
 * Platform connection information.
 */
export interface Platform {
  platform_name: string
  display_name: string
  status: 'connected' | 'disconnected' | 'connecting'
  connected_at?: string
}

// ============================================================================
// Query Parameter Types
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

export interface NarrativeParams {
  use_ai?: boolean
}

export interface UsageParams {
  period?: 'daily' | 'weekly' | 'monthly'
}

export interface HistoryParams {
  limit?: number
}

