/**
 * Constitutional Rule CR-003 Tests
 * 
 * Tests for: Descriptive NOT Prescriptive
 * The system must NEVER use prescriptive language for investment actions.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 3
 */

import { describe, it, expect } from 'vitest'
import { findConstitutionalViolations, hasRequiredDisclaimer } from '@utils/constitutional'
import { calculateFreshness } from '@hooks/useFreshness'
import { FreshnessStatus } from '@/types/index'

describe('CR-003: Descriptive NOT Prescriptive', () => {
  describe('Prescriptive Language Detection', () => {
    it('detects confidence percentage as violation', () => {
      const violations = findConstitutionalViolations('Confidence: 85%')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-003')).toBe(true)
    })

    it('detects "probability of" as violation', () => {
      const violations = findConstitutionalViolations('Probability of increase is high')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-003')).toBe(true)
    })

    it('detects "likely to rise" as violation', () => {
      const violations = findConstitutionalViolations('Price is likely to rise')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-003')).toBe(true)
    })

    it('detects "likely to fall" as violation', () => {
      const violations = findConstitutionalViolations('Stock is likely to fall')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-003')).toBe(true)
    })

    it('detects "high probability" as violation', () => {
      const violations = findConstitutionalViolations('High probability of breakout')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-003')).toBe(true)
    })

    it('detects rating scores as violation', () => {
      const violations = findConstitutionalViolations('Rating: 8/10')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-003')).toBe(true)
    })
  })

  describe('Disclaimer Validation', () => {
    it('validates proper disclaimer', () => {
      const content = 'The interpretation and any decision is entirely yours.'
      expect(hasRequiredDisclaimer(content)).toBe(true)
    })

    it('rejects missing disclaimer', () => {
      const content = 'Chart shows bullish signal.'
      expect(hasRequiredDisclaimer(content)).toBe(false)
    })

    it('validates full disclaimer text', () => {
      const content = 
        'This is a description of what your charts are showing. ' +
        'The interpretation and any decision is entirely yours.'
      expect(hasRequiredDisclaimer(content)).toBe(true)
    })
  })

  describe('Freshness Is Descriptive Only', () => {
    it('returns CURRENT status for recent timestamps', () => {
      const now = new Date()
      const status = calculateFreshness(now.toISOString())
      
      expect(status).toBe(FreshnessStatus.CURRENT)
    })

    it('returns STALE status for old timestamps', () => {
      const old = new Date(Date.now() - 60 * 60 * 1000) // 1 hour ago
      const status = calculateFreshness(old.toISOString())
      
      expect(status).toBe(FreshnessStatus.STALE)
    })

    it('returns UNAVAILABLE for null timestamp', () => {
      const status = calculateFreshness(null)
      
      expect(status).toBe(FreshnessStatus.UNAVAILABLE)
    })

    it('uses descriptive status names', () => {
      // All status values should be descriptive, not prescriptive
      const statuses = Object.values(FreshnessStatus)
      
      // Should NOT contain action-oriented words
      for (const status of statuses) {
        expect(status).not.toMatch(/invalid/i)
        expect(status).not.toMatch(/ignore/i)
        expect(status).not.toMatch(/discard/i)
      }
    })
  })

  describe('Compliant Content', () => {
    it('allows factual indicator descriptions', () => {
      const text = 'RSI is at 72.5, which is in overbought territory.'
      const violations = findConstitutionalViolations(text)
      
      const cr003Violations = violations.filter(v => v.rule === 'CR-003')
      expect(cr003Violations.length).toBe(0)
    })

    it('allows direction statements', () => {
      const text = 'The signal shows BULLISH direction.'
      const violations = findConstitutionalViolations(text)
      
      const cr003Violations = violations.filter(v => v.rule === 'CR-003')
      expect(cr003Violations.length).toBe(0)
    })

    it('allows historical descriptions', () => {
      const text = 'The previous signal was BEARISH, current signal is BULLISH.'
      const violations = findConstitutionalViolations(text)
      
      const cr003Violations = violations.filter(v => v.rule === 'CR-003')
      expect(cr003Violations.length).toBe(0)
    })
  })
})

