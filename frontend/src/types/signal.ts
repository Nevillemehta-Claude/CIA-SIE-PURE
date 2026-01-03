/**
 * Signal Type Definitions
 * 
 * GOVERNED BY: ADAPTER_FINANCIAL_SERVICES.md, BACKEND_ARCHITECTURAL_FLOWCHART.md
 * 
 * CRITICAL CONSTRAINT: Signal has NO confidence/strength scores.
 * Per ADR-003: Scores imply system judgment which is PROHIBITED.
 */

import { Direction, SignalType } from './enums'

/**
 * A point-in-time data emission from a chart.
 * 
 * PROHIBITED FIELDS (per Section 0B):
 * - confidence: Implies reliability ranking
 * - strength: Implies priority
 * - score: Implies system judgment
 * - weight: Enables aggregation
 * - priority: Implies hierarchy
 * - rank: Implies superiority
 */
export interface Signal {
  /** Unique identifier for the signal */
  signal_id: string
  /** ID of the chart that emitted this signal */
  chart_id: string
  /** When the signal was received by the system */
  received_at: string
  /** Timestamp from the source (TradingView) */
  signal_timestamp: string
  /** Classification of signal origin */
  signal_type: SignalType
  /** Directional bias - NO aggregation performed */
  direction: Direction
  /** Raw indicator values - displayed as-is, not scored */
  indicators: Record<string, unknown>
  /** Original webhook payload preserved for audit trail */
  raw_payload: Record<string, unknown>
  // NOTE: Deliberately NO confidence or strength field - prohibited by Section 0B
}

/**
 * Signal creation request (for manual signals).
 */
export interface SignalCreateRequest {
  direction: Direction
  signal_type?: SignalType
  indicators?: Record<string, unknown>
}

