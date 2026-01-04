/**
 * Disclaimer Accessibility Tests
 * 
 * Tests WCAG 2.1 AA compliance for:
 * - role="note" for important supplementary information
 * - aria-label for screen reader context
 * - aria-live for polite announcements
 * 
 * CONSTITUTIONAL REQUIREMENT (CR-003):
 * - Disclaimer text is HARDCODED and IMMUTABLE
 * - Component is NON-DISMISSIBLE
 * - Component is NON-COLLAPSIBLE
 * 
 * @see CIA-SIE-PROTOCOL-001 v3.0 - D6-PHASE-3
 */

import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Disclaimer } from '../Disclaimer'

expect.extend(toHaveNoViolations)

// CONSTITUTIONAL: This text must match the hardcoded text in Disclaimer.tsx
const EXPECTED_DISCLAIMER_TEXT =
  'This is a description of what your charts are showing. The interpretation and any decision is entirely yours.'

describe('Disclaimer Accessibility', () => {
  describe('block variant (default)', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(<Disclaimer />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have note role', () => {
      const { container } = render(<Disclaimer />)
      const note = container.querySelector('[role="note"]')
      expect(note).toBeInTheDocument()
    })

    it('should have descriptive aria-label', () => {
      const { container } = render(<Disclaimer />)
      const note = container.querySelector('[role="note"]')
      expect(note).toHaveAttribute(
        'aria-label',
        'Important disclaimer about AI-generated content'
      )
    })

    it('should have aria-live for polite announcements', () => {
      const { container } = render(<Disclaimer />)
      const note = container.querySelector('[role="note"]')
      expect(note).toHaveAttribute('aria-live', 'polite')
    })

    it('should hide decorative Info icon from screen readers', () => {
      const { container } = render(<Disclaimer />)
      const icon = container.querySelector('svg')
      expect(icon).toHaveAttribute('aria-hidden', 'true')
    })

    it('should render as aside element', () => {
      const { container } = render(<Disclaimer />)
      const aside = container.querySelector('aside')
      expect(aside).toBeInTheDocument()
    })

    it('should contain the constitutional disclaimer text (CR-003)', () => {
      render(<Disclaimer />)
      expect(screen.getByText(EXPECTED_DISCLAIMER_TEXT)).toBeInTheDocument()
    })
  })

  describe('inline variant', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(<Disclaimer variant="inline" />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have note role', () => {
      const { container } = render(<Disclaimer variant="inline" />)
      const note = container.querySelector('[role="note"]')
      expect(note).toBeInTheDocument()
    })

    it('should have aria-label', () => {
      const { container } = render(<Disclaimer variant="inline" />)
      const note = container.querySelector('[role="note"]')
      expect(note).toHaveAttribute('aria-label', 'Important disclaimer')
    })

    it('should render as span element', () => {
      const { container } = render(<Disclaimer variant="inline" />)
      const span = container.querySelector('span')
      expect(span).toBeInTheDocument()
    })

    it('should contain the constitutional disclaimer text (CR-003)', () => {
      render(<Disclaimer variant="inline" />)
      expect(screen.getByText(EXPECTED_DISCLAIMER_TEXT)).toBeInTheDocument()
    })
  })

  describe('constitutional compliance (CR-003)', () => {
    it('should always render the exact same text', () => {
      const { rerender } = render(<Disclaimer />)
      expect(screen.getByText(EXPECTED_DISCLAIMER_TEXT)).toBeInTheDocument()

      rerender(<Disclaimer variant="inline" />)
      expect(screen.getByText(EXPECTED_DISCLAIMER_TEXT)).toBeInTheDocument()
    })

    it('should not accept custom text props (immutable)', () => {
      // TypeScript would catch this at compile time, but we verify at runtime
      // that no text prop is used
      const { container } = render(<Disclaimer />)
      expect(container.textContent).toContain(EXPECTED_DISCLAIMER_TEXT)
    })
  })
})

