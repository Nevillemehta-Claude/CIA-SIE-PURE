/**
 * Constitutional Validation Hook
 * 
 * Validates AI content for constitutional compliance.
 * This is a DEFENSE-IN-DEPTH mechanism - the backend should
 * already validate content, but we double-check on the frontend.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-001: Checks for prohibited trading commands
 * - CR-002: Checks for aggregation language
 * - CR-003: Checks for prescriptive language
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md
 */

import { useMemo } from 'react'

/**
 * Prohibited patterns that violate constitutional rules.
 */
const PROHIBITED_PATTERNS = [
  // CR-001: Trading commands
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
  
  // CR-002: Aggregation language
  /overall direction/i,
  /net signal/i,
  /consensus (is|shows)/i,
  /majority of (signals|charts)/i,
  /on balance/i,
  /stronger signal/i,
  /more reliable/i,
  /signal strength/i,
  
  // CR-003: Confidence/probability language
  /confidence[:\s]+\d+%/i,
  /probability of/i,
  /likely to (rise|fall|increase|decrease)/i,
  /(high|low) probability/i,
  /rating[:\s]+\d/i,
]

/**
 * Mandatory disclaimer that should be present.
 */
const MANDATORY_DISCLAIMER = 
  "The interpretation and any decision is entirely yours"

/**
 * Validation result type.
 */
export interface ValidationResult {
  /** Whether the content is valid */
  isValid: boolean
  /** List of violations found */
  violations: string[]
  /** Whether the content was modified */
  wasModified: boolean
  /** The content (original or sanitized) */
  content: string
  /** Whether the mandatory disclaimer is present */
  hasDisclaimer: boolean
}

/**
 * Options for validation.
 */
interface ValidationOptions {
  /** Whether to sanitize content by removing violations */
  sanitize?: boolean
  /** Whether to check for disclaimer */
  checkDisclaimer?: boolean
}

/**
 * Find constitutional violations in content.
 */
function findViolations(content: string): string[] {
  const violations: string[] = []
  
  for (const pattern of PROHIBITED_PATTERNS) {
    const match = content.match(pattern)
    if (match) {
      violations.push(`Found prohibited pattern: "${match[0]}"`)
    }
  }
  
  return violations
}

/**
 * Check if mandatory disclaimer is present.
 */
function hasDisclaimer(content: string): boolean {
  return content.toLowerCase().includes(MANDATORY_DISCLAIMER.toLowerCase())
}

/**
 * Sanitize content by replacing violations.
 */
function sanitizeContent(content: string): string {
  let sanitized = content
  
  for (const pattern of PROHIBITED_PATTERNS) {
    sanitized = sanitized.replace(pattern, '[REMOVED]')
  }
  
  return sanitized
}

/**
 * Hook to validate AI content for constitutional compliance.
 * 
 * @param content - The content to validate
 * @param options - Validation options
 * @returns Validation result
 */
export function useConstitutionalValidation(
  content: string | undefined,
  options: ValidationOptions = {}
): ValidationResult | null {
  const { sanitize = false, checkDisclaimer = true } = options

  return useMemo(() => {
    if (!content) return null

    const violations = findViolations(content)
    const disclaimerPresent = checkDisclaimer ? hasDisclaimer(content) : true
    
    let finalContent = content
    let wasModified = false
    
    if (sanitize && violations.length > 0) {
      finalContent = sanitizeContent(content)
      wasModified = true
    }
    
    return {
      isValid: violations.length === 0 && disclaimerPresent,
      violations,
      wasModified,
      content: finalContent,
      hasDisclaimer: disclaimerPresent,
    }
  }, [content, sanitize, checkDisclaimer])
}

