/**
 * ContradictionCard Accessibility Tests
 * 
 * Tests WCAG 2.1 AA compliance for:
 * - article role with descriptive aria-label
 * - group roles for Chart A and Chart B
 * - Decorative VS separator hidden from screen readers
 * 
 * CONSTITUTIONAL REQUIREMENT (CR-002):
 * - Equal visual treatment verified through identical ARIA structure
 * 
 * @see CIA-SIE-PROTOCOL-001 v3.0 - D6-PHASE-3
 */

import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { ContradictionCard } from '../ContradictionCard'
import type { Contradiction } from '@/types/models'

expect.extend(toHaveNoViolations)

// Test fixture
const mockContradiction: Contradiction = {
  chart_a_id: 'chart-a-1',
  chart_a_name: 'RSI (14)',
  chart_a_direction: 'BULLISH',
  chart_b_id: 'chart-b-1',
  chart_b_name: 'MACD',
  chart_b_direction: 'BEARISH',
  detected_at: '2024-01-15T10:30:00Z',
}

describe('ContradictionCard Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should have article role', () => {
    render(<ContradictionCard contradiction={mockContradiction} />)
    expect(screen.getByRole('article')).toBeInTheDocument()
  })

  it('should have descriptive aria-label on article', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const article = container.querySelector('article')
    expect(article).toHaveAttribute(
      'aria-label',
      'Signal contradiction: RSI (14) shows BULLISH while MACD shows BEARISH'
    )
  })

  it('should have group roles for both chart sides', () => {
    render(<ContradictionCard contradiction={mockContradiction} />)
    const groups = screen.getAllByRole('group')
    expect(groups).toHaveLength(2)
  })

  it('should have aria-label on Chart A group', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const groups = container.querySelectorAll('[role="group"]')
    expect(groups[0]).toHaveAttribute('aria-label', 'RSI (14): BULLISH')
  })

  it('should have aria-label on Chart B group', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const groups = container.querySelectorAll('[role="group"]')
    expect(groups[1]).toHaveAttribute('aria-label', 'MACD: BEARISH')
  })

  it('should hide decorative VS separator from screen readers', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const separator = container.querySelector('[aria-hidden="true"]')
    expect(separator).toBeInTheDocument()
    expect(separator).toHaveTextContent('vs')
  })

  it('should have IDENTICAL structure for both sides (CR-002)', () => {
    const { container } = render(
      <ContradictionCard contradiction={mockContradiction} />
    )
    const groups = container.querySelectorAll('[role="group"]')
    
    // Both groups should have the same structure
    expect(groups[0].className).toBe(groups[1].className)
  })

  describe('with different directions', () => {
    it('should correctly announce neutral directions', async () => {
      const neutralContradiction: Contradiction = {
        ...mockContradiction,
        chart_a_direction: 'NEUTRAL',
        chart_b_direction: 'BULLISH',
      }
      const { container } = render(
        <ContradictionCard contradiction={neutralContradiction} />
      )
      const article = container.querySelector('article')
      expect(article).toHaveAttribute(
        'aria-label',
        'Signal contradiction: RSI (14) shows NEUTRAL while MACD shows BULLISH'
      )
    })
  })
})

