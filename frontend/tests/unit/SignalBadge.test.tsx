/**
 * SignalBadge Component Tests
 * 
 * Tests for the SignalBadge atomic component.
 */

import { describe, it, expect } from 'vitest'
import { render, screen } from '../utils'
import { SignalBadge } from '@components/atoms'
import { Direction } from '@/types/index'

describe('SignalBadge', () => {
  it('renders bullish direction correctly', () => {
    render(<SignalBadge direction={Direction.BULLISH} />)
    
    expect(screen.getByText('Bullish')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveAttribute(
      'aria-label', 
      'Direction: Bullish'
    )
  })

  it('renders bearish direction correctly', () => {
    render(<SignalBadge direction={Direction.BEARISH} />)
    
    expect(screen.getByText('Bearish')).toBeInTheDocument()
  })

  it('renders neutral direction correctly', () => {
    render(<SignalBadge direction={Direction.NEUTRAL} />)
    
    expect(screen.getByText('Neutral')).toBeInTheDocument()
  })

  it('hides label when showLabel is false', () => {
    render(<SignalBadge direction={Direction.BULLISH} showLabel={false} />)
    
    expect(screen.queryByText('Bullish')).not.toBeInTheDocument()
  })

  /**
   * CONSTITUTIONAL COMPLIANCE TEST (CR-002)
   * Verify that all directions have equal visual treatment.
   */
  it('gives equal visual prominence to all directions', () => {
    const { rerender } = render(<SignalBadge direction={Direction.BULLISH} />)
    const bullishElement = screen.getByRole('status')
    const bullishClasses = bullishElement.className

    rerender(<SignalBadge direction={Direction.BEARISH} />)
    const bearishElement = screen.getByRole('status')
    const bearishClasses = bearishElement.className

    rerender(<SignalBadge direction={Direction.NEUTRAL} />)
    const neutralElement = screen.getByRole('status')
    const neutralClasses = neutralElement.className

    // All should have the same structural classes (padding, font, border-radius)
    // Only color classes should differ
    expect(bullishClasses).toContain('rounded-full')
    expect(bearishClasses).toContain('rounded-full')
    expect(neutralClasses).toContain('rounded-full')
    
    expect(bullishClasses).toContain('border')
    expect(bearishClasses).toContain('border')
    expect(neutralClasses).toContain('border')
  })

  it('renders different sizes correctly', () => {
    const { rerender } = render(<SignalBadge direction={Direction.BULLISH} size="sm" />)
    expect(screen.getByRole('status')).toHaveClass('text-xs')

    rerender(<SignalBadge direction={Direction.BULLISH} size="md" />)
    expect(screen.getByRole('status')).toHaveClass('text-sm')

    rerender(<SignalBadge direction={Direction.BULLISH} size="lg" />)
    expect(screen.getByRole('status')).toHaveClass('text-base')
  })
})

