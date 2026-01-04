/**
 * Accessibility Testing Setup for CIA-SIE
 * 
 * This file configures jest-axe for automated accessibility testing.
 * It extends Jest matchers with toHaveNoViolations() for WCAG compliance.
 * 
 * @see CIA-SIE-PROTOCOL-001 v3.0 - D6-PHASE-1
 */

import { configureAxe, toHaveNoViolations } from 'jest-axe'

// Extend Jest matchers with accessibility assertions
expect.extend(toHaveNoViolations)

/**
 * CIA-SIE Axe Configuration
 * 
 * Configured for WCAG 2.1 AA compliance with focus on:
 * - Color contrast for signal direction indicators
 * - Keyboard navigation for all interactive elements
 * - Screen reader compatibility for constitutional components
 */
export const axeConfig = configureAxe({
  rules: {
    // Ensure color contrast meets WCAG AA (4.5:1 for normal text)
    'color-contrast': { enabled: true },
    // Ensure all images have alt text
    'image-alt': { enabled: true },
    // Ensure all form inputs have labels
    'label': { enabled: true },
    // Ensure page has main landmark
    'landmark-one-main': { enabled: true },
    // Ensure buttons have accessible names
    'button-name': { enabled: true },
    // Ensure links have accessible names
    'link-name': { enabled: true },
    // Ensure ARIA attributes are valid
    'aria-valid-attr': { enabled: true },
    'aria-valid-attr-value': { enabled: true },
    // Ensure regions have accessible names
    'region': { enabled: true },
  },
})

/**
 * Helper function for component accessibility testing
 * 
 * Usage:
 * ```typescript
 * import { testAccessibility } from '@/test/setupAccessibility'
 * 
 * it('should have no accessibility violations', async () => {
 *   const { container } = render(<MyComponent />)
 *   await testAccessibility(container)
 * })
 * ```
 */
export const testAccessibility = async (container: HTMLElement): Promise<void> => {
  const results = await axeConfig(container)
  expect(results).toHaveNoViolations()
}

/**
 * Type augmentation for jest-axe
 * Ensures TypeScript recognizes toHaveNoViolations matcher
 */
declare global {
  namespace jest {
    interface Matchers<R> {
      toHaveNoViolations(): R
    }
  }
}

