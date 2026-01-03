/**
 * Constitutional Constants
 * 
 * Constants related to constitutional rule enforcement.
 * 
 * CONSTITUTIONAL RULES:
 * - CR-001: Decision-Support ONLY
 * - CR-002: Never Resolve Contradictions  
 * - CR-003: Descriptive NOT Prescriptive
 */

/**
 * Mandatory disclaimer text.
 * MUST be displayed with all AI-generated content.
 */
export const MANDATORY_DISCLAIMER = 
  "This is a description of what your charts are showing. " +
  "The interpretation and any decision is entirely yours."

/**
 * Prohibited fields that must never appear in the UI.
 */
export const PROHIBITED_FIELDS = [
  'weight',
  'score',
  'confidence',
  'recommendation',
  'priority',
  'rank',
  'overall_direction',
  'net_signal',
] as const

/**
 * Constitutional rule descriptions.
 */
export const CONSTITUTIONAL_RULES = {
  'CR-001': {
    name: 'Decision-Support ONLY',
    description: 'The system must NEVER make investment decisions or output actionable trading commands.',
    enforcement: 'No Buy/Sell buttons, no order forms, mandatory disclaimer on AI content.',
  },
  'CR-002': {
    name: 'Never Resolve Contradictions',
    description: 'The system must NEVER pick sides, aggregate, weight, hide, or average conflicting signals.',
    enforcement: 'Equal visual prominence, no aggregation, no "winner" indication.',
  },
  'CR-003': {
    name: 'Descriptive NOT Prescriptive',
    description: 'The system must NEVER use prescriptive language for investment actions.',
    enforcement: 'No "should", "recommend", "suggest" language. AI responses validated.',
  },
} as const

