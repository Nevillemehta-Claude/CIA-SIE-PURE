/**
 * Constitutional Rule CR-002 Tests
 * 
 * Tests for: Never Resolve Contradictions
 * The system must NEVER pick sides, aggregate, weight, hide, or average conflicting signals.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 2
 */

import { describe, it, expect } from 'vitest'
import { findConstitutionalViolations } from '@utils/constitutional'
import { PROHIBITED_FIELDS } from '@constants/constitutional'

describe('CR-002: Never Resolve Contradictions', () => {
  describe('Aggregation Language Detection', () => {
    it('detects "overall direction" as violation', () => {
      const violations = findConstitutionalViolations('The overall direction is bullish')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })

    it('detects "net signal" as violation', () => {
      const violations = findConstitutionalViolations('Net signal is positive')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })

    it('detects "consensus shows" as violation', () => {
      const violations = findConstitutionalViolations('Consensus shows bullish bias')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })

    it('detects "majority of signals" as violation', () => {
      const violations = findConstitutionalViolations('Majority of signals point up')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })

    it('detects "on balance" as violation', () => {
      const violations = findConstitutionalViolations('On balance, signals favor bulls')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })

    it('detects "stronger signal" as violation', () => {
      const violations = findConstitutionalViolations('Chart A has a stronger signal')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })

    it('detects "more reliable" as violation', () => {
      const violations = findConstitutionalViolations('This signal is more reliable')
      
      expect(violations.length).toBeGreaterThan(0)
      expect(violations.some(v => v.rule === 'CR-002')).toBe(true)
    })
  })

  describe('Prohibited Fields', () => {
    it('defines all prohibited fields', () => {
      expect(PROHIBITED_FIELDS).toContain('weight')
      expect(PROHIBITED_FIELDS).toContain('score')
      expect(PROHIBITED_FIELDS).toContain('confidence')
      expect(PROHIBITED_FIELDS).toContain('recommendation')
      expect(PROHIBITED_FIELDS).toContain('priority')
      expect(PROHIBITED_FIELDS).toContain('rank')
      expect(PROHIBITED_FIELDS).toContain('overall_direction')
      expect(PROHIBITED_FIELDS).toContain('net_signal')
    })
  })

  describe('Compliant Content', () => {
    it('allows describing individual contradictions', () => {
      const text = 'Chart A shows BULLISH while Chart B shows BEARISH. ' +
                   'These signals are in contradiction.'
      const violations = findConstitutionalViolations(text)
      
      const cr002Violations = violations.filter(v => v.rule === 'CR-002')
      expect(cr002Violations.length).toBe(0)
    })

    it('allows listing all signals without aggregation', () => {
      const text = 'Chart A: BULLISH. Chart B: BEARISH. Chart C: NEUTRAL.'
      const violations = findConstitutionalViolations(text)
      
      const cr002Violations = violations.filter(v => v.rule === 'CR-002')
      expect(cr002Violations.length).toBe(0)
    })

    it('allows describing alignment without implying strength', () => {
      const text = 'Charts A and B both show BULLISH direction.'
      const violations = findConstitutionalViolations(text)
      
      const cr002Violations = violations.filter(v => v.rule === 'CR-002')
      expect(cr002Violations.length).toBe(0)
    })
  })
})

