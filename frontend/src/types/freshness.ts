/**
 * Freshness Type Definitions
 * 
 * GOVERNED BY: Constitutional Rule CR-003 - Descriptive NOT Prescriptive
 * 
 * Freshness is purely DESCRIPTIVE - it does NOT invalidate or suppress data.
 * All data is displayed regardless of freshness.
 * Stale data is NOT hidden or treated as "less valid".
 */

import { FreshnessStatus, Direction } from './enums'
import type { Signal } from './signal'

/**
 * Current status of a chart including its latest signal and freshness.
 */
export interface ChartSignalStatus {
  /** Chart ID */
  chart_id: string
  /** Chart code */
  chart_code: string
  /** Chart name */
  chart_name: string
  /** Chart timeframe */
  timeframe: string
  /** Latest signal (null if no signals received) */
  latest_signal: Signal | null
  /** Freshness status - purely descriptive */
  freshness: FreshnessStatus
}

/**
 * Complete relationship summary for a silo.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - Returns ALL charts (none hidden)
 * - Returns ALL contradictions (none resolved)
 * - Returns ALL confirmations (none weighted)
 * - NO aggregation anywhere
 * - NO scores anywhere
 * - NO recommendations anywhere
 */
export interface RelationshipSummary {
  /** Silo ID */
  silo_id: string
  /** Silo name */
  silo_name: string
  /** Parent instrument ID */
  instrument_id: string
  /** Parent instrument symbol */
  instrument_symbol: string
  /** All charts with their current status - displayed equally */
  charts: ChartSignalStatus[]
  /** All contradictions - exposed, not resolved */
  contradictions: Array<{
    chart_a_id: string
    chart_a_name: string
    chart_a_direction: Direction
    chart_b_id: string
    chart_b_name: string
    chart_b_direction: Direction
    detected_at: string
  }>
  /** All confirmations - described, not weighted */
  confirmations: Array<{
    chart_a_id: string
    chart_a_name: string
    chart_b_id: string
    chart_b_name: string
    aligned_direction: Direction
    detected_at: string
  }>
  /** Generation timestamp */
  generated_at: string
}

/**
 * Freshness calculation thresholds.
 */
export interface FreshnessThresholds {
  /** Minutes for CURRENT status */
  current_threshold_min: number
  /** Minutes for RECENT status */
  recent_threshold_min: number
  /** Minutes for STALE status */
  stale_threshold_min: number
}

