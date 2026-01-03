/**
 * Constitutional Rule CR-001 Tests
 * 
 * Tests for: Decision-Support ONLY
 * The system must NEVER make investment decisions or output actionable trading commands.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 1
 */

import { describe, it, expect } from 'vitest'
import { 
  findConstitutionalViolations, 
  validateAIResponse,
  MANDATORY_DISCLAIMER 
} from '@utils/constitutional'

describe('CR-001: Decision-Support ONLY', () => {
  describe('Trading Command Detection', () => {
    it('detects "you should buy" as violation', () => {
      const violations = findConstitutionalViolations('You should buy now')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "you should sell" as violation', () => {
      const violations = findConstitutionalViolations('You should sell immediately')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "I recommend" as violation', () => {
      const violations = findConstitutionalViolations('I recommend entering a position')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "I suggest" as violation', () => {
      const violations = findConstitutionalViolations('I suggest buying more shares')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "consider buying" as violation', () => {
      const violations = findConstitutionalViolations('Consider buying at this level')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "enter long position" as violation', () => {
      const violations = findConstitutionalViolations('Enter long position here')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "take profit" as violation', () => {
      const violations = findConstitutionalViolations('Take profit at resistance')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })

    it('detects "cut losses" as violation', () => {
      const violations = findConstitutionalViolations('Cut your losses now')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations[0].rule).toBe('CR-001')
    })
  })

  describe('Compliant Content', () => {
    it('allows descriptive statements about signals', () => {
      const text = 'Chart A shows bullish momentum. RSI is at 72.5.'
      const violations = findConstitutionalViolations(text)
      
      const cr001Violations = violations.filter(v => v.rule === 'CR-001')
      expect(cr001Violations.length).toBe(0)
    })

    it('allows factual descriptions of price movement', () => {
      const text = 'The price has moved from 24000 to 24150.'
      const violations = findConstitutionalViolations(text)
      
      const cr001Violations = violations.filter(v => v.rule === 'CR-001')
      expect(cr001Violations.length).toBe(0)
    })

    it('allows description of indicator values', () => {
      const text = 'MACD histogram shows negative divergence.'
      const violations = findConstitutionalViolations(text)
      
      const cr001Violations = violations.filter(v => v.rule === 'CR-001')
      expect(cr001Violations.length).toBe(0)
    })
  })

  describe('Mandatory Disclaimer', () => {
    it('validates presence of mandatory disclaimer', () => {
      const contentWithDisclaimer = 
        'Chart shows bullish signal. ' + MANDATORY_DISCLAIMER
      const result = validateAIResponse(contentWithDisclaimer)
      
      expect(result.hasDisclaimer).toBe(true)
    })

    it('fails validation without disclaimer', () => {
      const contentWithoutDisclaimer = 'Chart shows bullish signal.'
      const result = validateAIResponse(contentWithoutDisclaimer)
      
      expect(result.hasDisclaimer).toBe(false)
      expect(result.isValid).toBe(false)
    })
  })
})

