/**
 * Constitutional Validation Utilities
 * 
 * Functions for validating content against constitutional rules.
 * 
 * CONSTITUTIONAL RULES:
 * - CR-001: Decision-Support ONLY (no trading commands)
 * - CR-002: Never Resolve Contradictions (no aggregation)
 * - CR-003: Descriptive NOT Prescriptive (no recommendations)
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md
 */

/**
 * Prohibited patterns organized by rule.
 */
export const PROHIBITED_PATTERNS = {
  // CR-001: Trading commands
  CR001_TRADING_COMMANDS: [
    /you should (buy|sell|enter|exit)/i,
    /i recommend/i,
    /i suggest/i,
    /consider (buying|selling)/i,
    /buy now/i,
    /sell now/i,
    /enter (long|short) position/i,
    /exit position/i,
    /take profit/i,
    /cut (your )?losses/i,
    /you might want to/i,
    /the best action/i,
    /a prudent approach/i,
  ],
  
  // CR-002: Aggregation language
  CR002_AGGREGATION: [
    /overall direction/i,
    /net signal/i,
    /consensus (is|shows)/i,
    /majority of (signals|charts)/i,
    /on balance/i,
    /stronger signal/i,
    /more reliable/i,
    /signal strength/i,
    /weaker signal/i,
    /weighted average/i,
    /combined score/i,
  ],
  
  // CR-003: Confidence/prescriptive language
  CR003_PRESCRIPTIVE: [
    /confidence[:\s]+\d+%/i,
    /probability of/i,
    /likely to (rise|fall|increase|decrease)/i,
    /(high|low) probability/i,
    /rating[:\s]+\d/i,
    /certainty/i,
    /guaranteed/i,
    /will definitely/i,
  ],
} as const

/**
 * The mandatory disclaimer text.
 */
export const MANDATORY_DISCLAIMER = 
  "This is a description of what your charts are showing. " +
  "The interpretation and any decision is entirely yours."

/**
 * Violation type.
 */
export interface ConstitutionalViolation {
  rule: 'CR-001' | 'CR-002' | 'CR-003'
  pattern: string
  match: string
}

/**
 * Find all constitutional violations in text.
 */
export function findConstitutionalViolations(text: string): ConstitutionalViolation[] {
  const violations: ConstitutionalViolation[] = []
  
  // Check CR-001
  for (const pattern of PROHIBITED_PATTERNS.CR001_TRADING_COMMANDS) {
    const match = text.match(pattern)
    if (match) {
      violations.push({
        rule: 'CR-001',
        pattern: pattern.toString(),
        match: match[0],
      })
    }
  }
  
  // Check CR-002
  for (const pattern of PROHIBITED_PATTERNS.CR002_AGGREGATION) {
    const match = text.match(pattern)
    if (match) {
      violations.push({
        rule: 'CR-002',
        pattern: pattern.toString(),
        match: match[0],
      })
    }
  }
  
  // Check CR-003
  for (const pattern of PROHIBITED_PATTERNS.CR003_PRESCRIPTIVE) {
    const match = text.match(pattern)
    if (match) {
      violations.push({
        rule: 'CR-003',
        pattern: pattern.toString(),
        match: match[0],
      })
    }
  }
  
  return violations
}

/**
 * Check if text contains the required disclaimer.
 */
export function hasRequiredDisclaimer(text: string): boolean {
  // Check for key phrases from the disclaimer
  const key1 = "interpretation"
  const key2 = "decision"
  const key3 = "entirely yours"
  
  const lowerText = text.toLowerCase()
  return (
    lowerText.includes(key1) &&
    lowerText.includes(key2) &&
    lowerText.includes(key3)
  )
}

/**
 * Validate AI response for constitutional compliance.
 */
export function validateAIResponse(response: string): {
  isValid: boolean
  violations: ConstitutionalViolation[]
  hasDisclaimer: boolean
} {
  const violations = findConstitutionalViolations(response)
  const hasDisclaimer = hasRequiredDisclaimer(response)
  
  return {
    isValid: violations.length === 0 && hasDisclaimer,
    violations,
    hasDisclaimer,
  }
}

/**
 * Sanitize text by removing prohibited patterns.
 */
export function sanitizeText(text: string): string {
  let sanitized = text
  
  const allPatterns = [
    ...PROHIBITED_PATTERNS.CR001_TRADING_COMMANDS,
    ...PROHIBITED_PATTERNS.CR002_AGGREGATION,
    ...PROHIBITED_PATTERNS.CR003_PRESCRIPTIVE,
  ]
  
  for (const pattern of allPatterns) {
    sanitized = sanitized.replace(pattern, '[CONTENT REMOVED]')
  }
  
  return sanitized
}

