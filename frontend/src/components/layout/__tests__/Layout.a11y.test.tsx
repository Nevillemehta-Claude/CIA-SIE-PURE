/**
 * Layout Components Accessibility Tests
 * 
 * Tests WCAG 2.1 AA compliance for:
 * - Header (role="banner")
 * - Sidebar (role="navigation")
 * - AppShell (role="main")
 * 
 * @see CIA-SIE-PROTOCOL-001 v3.0 - D6-PHASE-2
 */

import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Header } from '../Header'
import { Sidebar } from '../Sidebar'
import { AppShell } from '../AppShell'

expect.extend(toHaveNoViolations)

// Create a fresh query client for each test
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        staleTime: 0,
      },
    },
  })

// Test wrapper with required providers
const TestWrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = createTestQueryClient()
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  )
}

describe('Layout Components Accessibility', () => {
  describe('Header', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have banner role', () => {
      render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      expect(screen.getByRole('banner')).toBeInTheDocument()
    })

    it('should have aria-label on header', () => {
      const { container } = render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      const header = container.querySelector('[role="banner"]')
      expect(header).toHaveAttribute('aria-label', 'CIA-SIE main header')
    })

    it('should have accessible link names', () => {
      render(
        <TestWrapper>
          <Header />
        </TestWrapper>
      )
      expect(screen.getByRole('link', { name: /open ai chat/i })).toBeInTheDocument()
      expect(screen.getByRole('link', { name: /open settings/i })).toBeInTheDocument()
    })
  })

  describe('Sidebar', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have implicit complementary role on aside', () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      const aside = container.querySelector('aside')
      // aside element has implicit role="complementary", we don't override it
      expect(aside).toBeInTheDocument()
    })

    it('should have aria-label on sidebar', () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      const aside = container.querySelector('aside')
      expect(aside).toHaveAttribute('aria-label', 'Main sidebar')
    })

    it('should have aria-label on nav element', () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      const nav = container.querySelector('nav')
      expect(nav).toHaveAttribute('aria-label', 'Primary navigation menu')
    })

    it('should have constitutional reminder with note role', () => {
      const { container } = render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      const reminder = container.querySelector('[role="note"]')
      expect(reminder).toBeInTheDocument()
      expect(reminder).toHaveAttribute('aria-label', 'Constitutional reminder')
    })

    it('should have accessible home link', () => {
      render(
        <TestWrapper>
          <Sidebar />
        </TestWrapper>
      )
      expect(screen.getByRole('link', { name: /cia-sie home/i })).toBeInTheDocument()
    })
  })

  describe('AppShell', () => {
    it('should have no accessibility violations', async () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })

    it('should have main landmark', () => {
      render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      expect(screen.getByRole('main')).toBeInTheDocument()
    })

    it('should have main content with correct id for skip links', () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      const main = container.querySelector('#main-content')
      expect(main).toBeInTheDocument()
    })

    it('should have focusable main content for skip link navigation', () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      const main = container.querySelector('#main-content')
      expect(main).toHaveAttribute('tabIndex', '-1')
    })

    it('should have aria-label on main content', () => {
      const { container } = render(
        <TestWrapper>
          <AppShell>
            <div>Test content</div>
          </AppShell>
        </TestWrapper>
      )
      const main = container.querySelector('main')
      expect(main).toHaveAttribute('aria-label', 'Main content')
    })

    it('should render children correctly', () => {
      render(
        <TestWrapper>
          <AppShell>
            <div data-testid="child-content">Test content</div>
          </AppShell>
        </TestWrapper>
      )
      expect(screen.getByTestId('child-content')).toBeInTheDocument()
    })
  })
})

