import type { Direction, SignalType, FreshnessStatus } from './enums'

// ============================================================================
// DOMAIN MODELS
// ============================================================================

export interface Instrument {
  instrument_id: string
  symbol: string
  display_name: string
  created_at: string
  updated_at: string
  is_active: boolean
  metadata: Record<string, unknown> | null
}

export interface Silo {
  silo_id: string
  instrument_id: string
  silo_name: string
  heartbeat_enabled: boolean
  heartbeat_frequency_min: number
  current_threshold_min: number
  recent_threshold_min: number
  stale_threshold_min: number
  created_at: string
  updated_at: string
  is_active: boolean
}

export interface Chart {
  chart_id: string
  silo_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  webhook_id: string
  created_at: string
  updated_at: string
  is_active: boolean
  // CONSTITUTIONAL: NO weight field
}

export interface Signal {
  signal_id: string
  chart_id: string
  received_at: string
  signal_timestamp: string
  signal_type: SignalType
  direction: Direction
  indicators: Record<string, number | string>
  raw_payload: Record<string, unknown>
  // CONSTITUTIONAL: NO confidence field
  // CONSTITUTIONAL: NO strength field
}

export interface Contradiction {
  chart_a_id: string
  chart_a_name: string
  chart_a_direction: Direction
  chart_b_id: string
  chart_b_name: string
  chart_b_direction: Direction
  detected_at: string
}

export interface Confirmation {
  chart_a_id: string
  chart_a_name: string
  chart_b_id: string
  chart_b_name: string
  aligned_direction: Direction
  detected_at: string
}

export interface ChartSignalStatus {
  chart_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  latest_signal: Signal | null
  freshness: FreshnessStatus
}

export interface RelationshipSummary {
  silo_id: string
  silo_name: string
  instrument_id: string
  instrument_symbol: string
  charts: ChartSignalStatus[]
  contradictions: Contradiction[]
  confirmations: Confirmation[]
  generated_at: string
}

export interface ChartWithSignal extends Chart {
  latest_signal?: Signal | null
  freshness: FreshnessStatus
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

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

