/**
 * Narrative Type Definitions
 * 
 * GOVERNED BY: Constitutional Rules CR-001 and CR-003
 * 
 * All narratives are DESCRIPTIVE, never PRESCRIPTIVE.
 * Every narrative MUST include the mandatory disclaimer.
 * 
 * PROHIBITED PATTERNS:
 * - Recommendations ("you should", "we recommend")
 * - Trading commands ("buy now", "sell now")
 * - Confidence scores
 * - Aggregation language ("overall direction", "net signal")
 */

import { NarrativeSectionType } from './enums'

/**
 * A section of the AI-generated narrative.
 * 
 * All sections are DESCRIPTIVE, never PRESCRIPTIVE.
 */
export interface NarrativeSection {
  /** Type of narrative section */
  section_type: NarrativeSectionType
  /** Descriptive content - validated for constitutional compliance */
  content: string
  /** IDs of charts referenced in this section */
  referenced_chart_ids: string[]
}

/**
 * Complete AI-generated narrative.
 * 
 * REQUIRED CLOSING STATEMENT:
 * "This is a description of what your charts are showing.
 * The interpretation and any decision is entirely yours."
 */
export interface Narrative {
  /** Unique identifier */
  narrative_id: string
  /** Silo this narrative describes */
  silo_id: string
  /** Narrative sections */
  sections: NarrativeSection[]
  /** MANDATORY disclaimer - must always be displayed */
  closing_statement: string
  /** Generation timestamp */
  generated_at: string
}

/**
 * Plain text narrative response.
 */
export interface PlainNarrativeResponse {
  text: string
  generated_at: string
}

/**
 * Narrative generation parameters.
 */
export interface NarrativeParams {
  /** Whether to use AI for generation */
  use_ai?: boolean
}

