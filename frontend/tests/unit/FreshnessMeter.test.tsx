/**
 * FreshnessMeter Component Tests
 * 
 * Tests for the FreshnessMeter atomic component.
 */

import { describe, it, expect } from 'vitest'
import { render, screen } from '../utils'
import { FreshnessMeter } from '@components/atoms'
import { FreshnessStatus } from '@/types/index'

describe('FreshnessMeter', () => {
  it('renders current status correctly', () => {
    render(<FreshnessMeter status={FreshnessStatus.CURRENT} />)
    
    expect(screen.getByText('Current')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveAttribute(
      'aria-label',
      'Freshness: Current'
    )
  })

  it('renders recent status correctly', () => {
    render(<FreshnessMeter status={FreshnessStatus.RECENT} />)
    
    expect(screen.getByText('Recent')).toBeInTheDocument()
  })

  it('renders stale status correctly', () => {
    render(<FreshnessMeter status={FreshnessStatus.STALE} />)
    
    expect(screen.getByText('Stale')).toBeInTheDocument()
  })

  it('renders unavailable status correctly', () => {
    render(<FreshnessMeter status={FreshnessStatus.UNAVAILABLE} />)
    
    expect(screen.getByText('No Data')).toBeInTheDocument()
  })

  it('hides label when showLabel is false', () => {
    render(<FreshnessMeter status={FreshnessStatus.CURRENT} showLabel={false} />)
    
    expect(screen.queryByText('Current')).not.toBeInTheDocument()
  })

  /**
   * CONSTITUTIONAL COMPLIANCE TEST (CR-003)
   * Verify that freshness is purely descriptive.
   */
  it('uses descriptive language only', () => {
    render(<FreshnessMeter status={FreshnessStatus.STALE} />)
    
    // Should use descriptive label, not prescriptive
    expect(screen.getByText('Stale')).toBeInTheDocument()
    
    // Should NOT contain prescriptive language
    expect(screen.queryByText(/invalid/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/ignore/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/do not use/i)).not.toBeInTheDocument()
  })
})

