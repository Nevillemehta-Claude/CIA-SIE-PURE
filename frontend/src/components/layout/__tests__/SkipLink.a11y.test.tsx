import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { SkipLink } from '../SkipLink'

expect.extend(toHaveNoViolations)

describe('SkipLink Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<SkipLink />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should render a link element', () => {
    render(<SkipLink />)
    const link = screen.getByRole('link', { name: /skip to main content/i })
    expect(link).toBeInTheDocument()
  })

  it('should link to #main-content', () => {
    render(<SkipLink />)
    const link = screen.getByRole('link', { name: /skip to main content/i })
    expect(link).toHaveAttribute('href', '#main-content')
  })

  it('should have sr-only class for visual hiding', () => {
    render(<SkipLink />)
    const link = screen.getByRole('link', { name: /skip to main content/i })
    expect(link).toHaveClass('sr-only')
  })

  it('should have focus classes', () => {
    render(<SkipLink />)
    const link = screen.getByRole('link', { name: /skip to main content/i })
    expect(link).toHaveClass('focus:not-sr-only')
    expect(link).toHaveClass('focus:z-50')
    expect(link).toHaveClass('focus:absolute')
  })
})
