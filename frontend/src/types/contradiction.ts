/**
 * Contradiction Type Definitions
 * 
 * GOVERNED BY: Constitutional Rule CR-002 - Never Resolve Contradictions
 * 
 * The Contradiction Detector identifies when chart signals conflict.
 * It does NOT resolve contradictions - only EXPOSES them.
 * 
 * PROHIBITED ACTIONS:
 * - Resolving which signal is "correct"
 * - Suggesting which to prioritize
 * - Hiding any contradiction
 */

import { Direction } from './enums'

/**
 * Represents a detected contradiction between two charts.
 * 
 * DISPLAY REQUIREMENTS (CR-002):
 * - Both charts displayed with EQUAL visual prominence
 * - No visual hierarchy suggesting one is "correct"
 * - Side-by-side layout with equal space allocation
 */
export interface Contradiction {
  /** ID of the first chart */
  chart_a_id: string
  /** Name of the first chart */
  chart_a_name: string
  /** Direction of the first chart's signal */
  chart_a_direction: Direction
  /** ID of the second chart */
  chart_b_id: string
  /** Name of the second chart */
  chart_b_name: string
  /** Direction of the second chart's signal */
  chart_b_direction: Direction
  /** When the contradiction was detected */
  detected_at: string
  // NOTE: NO resolution_hint, preferred_signal, or weight fields - prohibited
}

/**
 * API response for contradictions endpoint.
 */
export interface ContradictionsResponse {
  contradictions: Contradiction[]
  count: number
}

