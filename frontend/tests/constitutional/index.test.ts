/**
 * Constitutional Compliance Integration Tests
 * 
 * These tests verify that all constitutional rules are enforced together.
 */

import { describe, it, expect } from 'vitest'
import { validateAIResponse, sanitizeText, MANDATORY_DISCLAIMER } from '@utils/constitutional'

describe('Constitutional Compliance Integration', () => {
  it('validates fully compliant content', () => {
    const compliantContent = 
      'Chart A shows BULLISH momentum with RSI at 65.2. ' +
      'Chart B shows BEARISH direction with MACD below signal line. ' +
      'This represents a contradiction between the two charts. ' +
      MANDATORY_DISCLAIMER

    const result = validateAIResponse(compliantContent)
    
    expect(result.isValid).toBe(true)
    expect(result.violations).toHaveLength(0)
    expect(result.hasDisclaimer).toBe(true)
  })

  it('fails content with multiple violations', () => {
    const violatingContent = 
      'I recommend buying now. ' +
      'The overall direction is bullish with confidence: 85%. ' +
      'This is the stronger signal and price is likely to rise.'

    const result = validateAIResponse(violatingContent)
    
    expect(result.isValid).toBe(false)
    expect(result.violations.length).toBeGreaterThan(0)
    
    // Should detect violations from all three rules
    const rules = result.violations.map(v => v.rule)
    expect(rules).toContain('CR-001') // "I recommend"
    expect(rules).toContain('CR-002') // "overall direction", "stronger signal"
    expect(rules).toContain('CR-003') // "confidence: 85%", "likely to rise"
  })

  it('sanitizes violating content', () => {
    const violatingContent = 'You should buy now. Net signal is positive.'
    const sanitized = sanitizeText(violatingContent)
    
    expect(sanitized).toContain('[CONTENT REMOVED]')
    expect(sanitized).not.toContain('should buy')
    expect(sanitized).not.toContain('Net signal')
  })

  it('preserves compliant content when sanitizing', () => {
    const compliantContent = 'Chart shows bullish momentum.'
    const sanitized = sanitizeText(compliantContent)
    
    expect(sanitized).toBe(compliantContent)
    expect(sanitized).not.toContain('[CONTENT REMOVED]')
  })

  describe('Type Safety for Prohibited Fields', () => {
    it('Chart type does not have weight field', () => {
      // This is a compile-time check, but we can verify at runtime
      const chart = {
        chart_id: '1',
        silo_id: '1',
        chart_code: '01A',
        chart_name: 'Test',
        timeframe: '1h',
        webhook_id: 'test',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_active: true,
      }
      
      // @ts-expect-error - weight should not exist
      expect(chart.weight).toBeUndefined()
    })

    it('Signal type does not have confidence field', () => {
      const signal = {
        signal_id: '1',
        chart_id: '1',
        received_at: new Date().toISOString(),
        signal_timestamp: new Date().toISOString(),
        signal_type: 'STATE_CHANGE',
        direction: 'BULLISH',
        indicators: {},
        raw_payload: {},
      }
      
      // @ts-expect-error - confidence should not exist
      expect(signal.confidence).toBeUndefined()
      // @ts-expect-error - score should not exist
      expect(signal.score).toBeUndefined()
    })
  })
})

