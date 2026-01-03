/**
 * DisclaimerText Component Tests
 * 
 * Tests for the mandatory disclaimer component.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-001):
 * The disclaimer MUST be displayed with all AI-generated content.
 */

import { describe, it, expect } from 'vitest'
import { render, screen } from '../utils'
import { DisclaimerText, MANDATORY_DISCLAIMER } from '@components/atoms'

describe('DisclaimerText', () => {
  /**
   * CONSTITUTIONAL COMPLIANCE TEST (CR-001)
   * Verify that the mandatory disclaimer text is displayed.
   */
  it('displays the mandatory disclaimer text', () => {
    render(<DisclaimerText />)
    
    expect(
      screen.getByText(/This is a description of what your charts are showing/i)
    ).toBeInTheDocument()
    expect(
      screen.getByText(/The interpretation and any decision is entirely yours/i)
    ).toBeInTheDocument()
  })

  it('renders block variant by default', () => {
    render(<DisclaimerText />)
    
    const element = screen.getByRole('note')
    expect(element).toHaveClass('mt-4', 'rounded-lg')
  })

  it('renders inline variant correctly', () => {
    render(<DisclaimerText variant="inline" />)
    
    const element = screen.getByRole('note')
    expect(element).toHaveClass('italic')
    expect(element.tagName.toLowerCase()).toBe('span')
  })

  it('renders compact variant correctly', () => {
    render(<DisclaimerText variant="compact" />)
    
    const element = screen.getByRole('note')
    expect(element).toHaveClass('text-xs')
  })

  it('exports the mandatory disclaimer text constant', () => {
    expect(MANDATORY_DISCLAIMER).toContain('description')
    expect(MANDATORY_DISCLAIMER).toContain('interpretation')
    expect(MANDATORY_DISCLAIMER).toContain('entirely yours')
  })

  /**
   * CONSTITUTIONAL COMPLIANCE TEST (CR-001)
   * Verify that the disclaimer cannot be accidentally hidden.
   */
  it('always displays content regardless of variant', () => {
    const variants = ['inline', 'block', 'compact'] as const
    
    for (const variant of variants) {
      const { unmount } = render(<DisclaimerText variant={variant} />)
      
      expect(
        screen.getByText(/interpretation and any decision/i)
      ).toBeInTheDocument()
      
      unmount()
    }
  })
})

