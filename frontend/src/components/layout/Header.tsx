/**
 * Header Component
 * 
 * Application header with logo, navigation, and global actions.
 * 
 * ACCESSIBILITY: Uses semantic header element and ARIA labels
 */

import { Link } from 'react-router-dom'
import { Activity, Settings, Menu } from 'lucide-react'
import { useState } from 'react'

/**
 * Header provides the top navigation bar.
 */
export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header 
      className="sticky top-0 z-50 border-b border-slate-700 bg-surface-secondary/95 backdrop-blur supports-[backdrop-filter]:bg-surface-secondary/80"
      role="banner"
    >
      <div className="flex h-14 md:h-16 items-center justify-between px-4 lg:px-8">
        {/* Logo and brand */}
        <Link 
          to="/" 
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
          aria-label="CIA-SIE Home"
        >
          <Activity className="h-6 w-6 text-accent-primary" aria-hidden="true" />
          <span className="font-display text-lg md:text-xl font-bold tracking-tight">
            CIA-SIE
          </span>
        </Link>

        {/* Desktop navigation */}
        <nav 
          className="hidden md:flex items-center gap-6"
          role="navigation"
          aria-label="Main navigation"
        >
          <Link 
            to="/" 
            className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
          >
            Dashboard
          </Link>
          <Link 
            to="/instruments" 
            className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
          >
            Instruments
          </Link>
        </nav>
        
        {/* Right side actions */}
        <div className="flex items-center gap-3">
          <Link 
            to="/settings" 
            className="rounded-lg p-2 hover:bg-surface-tertiary transition-colors"
            aria-label="Settings"
          >
            <Settings className="h-5 w-5 text-slate-400" aria-hidden="true" />
          </Link>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden rounded-lg p-2 hover:bg-surface-tertiary transition-colors"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
          >
            <Menu className="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </div>

      {/* Mobile navigation */}
      {mobileMenuOpen && (
        <nav 
          className="md:hidden border-t border-slate-700 px-4 py-3 bg-surface-secondary"
          role="navigation"
          aria-label="Mobile navigation"
        >
          <div className="flex flex-col gap-2">
            <Link 
              to="/" 
              className="px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-surface-tertiary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Dashboard
            </Link>
            <Link 
              to="/instruments" 
              className="px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-surface-tertiary transition-colors"
              onClick={() => setMobileMenuOpen(false)}
            >
              Instruments
            </Link>
          </div>
        </nav>
      )}
    </header>
  )
}

