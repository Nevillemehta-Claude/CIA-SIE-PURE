/**
 * Confirmation Type Definitions
 * 
 * GOVERNED BY: Constitutional Rule CR-002
 * 
 * The Confirmation Detector identifies when chart signals align.
 * It does NOT weight or prioritize confirmations - only describes alignment.
 * 
 * PROHIBITED PATTERNS:
 * - "Stronger signal" language
 * - Confidence scoring
 * - Priority ranking
 */

import { Direction } from './enums'

/**
 * Represents detected alignment between two charts.
 * 
 * NOTE: Does NOT weight or prioritize confirmations.
 * Simply describes that two charts show the same direction.
 */
export interface Confirmation {
  /** ID of the first chart */
  chart_a_id: string
  /** Name of the first chart */
  chart_a_name: string
  /** ID of the second chart */
  chart_b_id: string
  /** Name of the second chart */
  chart_b_name: string
  /** The direction both charts align on */
  aligned_direction: Direction
  /** When the confirmation was detected */
  detected_at: string
  // NOTE: NO strength, confidence, or weight fields - prohibited
}

/**
 * API response for confirmations endpoint.
 */
export interface ConfirmationsResponse {
  confirmations: Confirmation[]
  count: number
}

