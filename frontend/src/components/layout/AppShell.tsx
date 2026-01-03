/**
 * AppShell Component
 * 
 * Main application layout wrapper providing consistent structure.
 * Includes header, sidebar, and main content area.
 * 
 * ACCESSIBILITY: Uses semantic HTML landmarks (header, nav, main, aside)
 */

import { Outlet } from 'react-router-dom'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

/**
 * AppShell provides the main application layout structure.
 */
export function AppShell() {
  return (
    <div className="min-h-screen bg-surface-primary text-white">
      {/* Skip link for accessibility */}
      <a 
        href="#main-content" 
        className="skip-link focus:top-0"
      >
        Skip to main content
      </a>
      
      <Header />
      
      <div className="flex">
        <Sidebar />
        
        <main 
          id="main-content"
          className="flex-1 p-4 md:p-6 lg:p-8"
          role="main"
          aria-label="Main content"
        >
          <Outlet />
        </main>
      </div>
    </div>
  )
}

