/**
 * Sidebar Component
 * 
 * Navigation sidebar with quick links and instrument list.
 * 
 * ACCESSIBILITY: Uses semantic nav element with ARIA labels
 */

import { Link, useLocation } from 'react-router-dom'
import { clsx } from 'clsx'
import { 
  LayoutDashboard, 
  LineChart, 
  MessageSquare, 
  Settings,
  ChevronRight 
} from 'lucide-react'

interface NavItem {
  label: string
  path: string
  icon: React.ComponentType<{ className?: string }>
}

const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Instruments', path: '/instruments', icon: LineChart },
  { label: 'AI Chat', path: '/chat', icon: MessageSquare },
  { label: 'Settings', path: '/settings', icon: Settings },
]

/**
 * Sidebar provides persistent navigation.
 */
export function Sidebar() {
  const location = useLocation()

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/'
    return location.pathname.startsWith(path)
  }

  return (
    <aside 
      className="hidden md:flex flex-col w-56 lg:w-64 border-r border-slate-700 bg-surface-primary min-h-[calc(100vh-4rem)]"
      role="complementary"
      aria-label="Sidebar navigation"
    >
      <nav 
        className="flex-1 p-4"
        role="navigation"
        aria-label="Sidebar navigation"
      >
        <ul className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon
            const active = isActive(item.path)
            
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={clsx(
                    'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                    active 
                      ? 'bg-accent-primary/20 text-accent-primary' 
                      : 'text-slate-400 hover:text-white hover:bg-surface-tertiary'
                  )}
                  aria-current={active ? 'page' : undefined}
                >
                  <Icon className="h-5 w-5" aria-hidden="true" />
                  <span className="flex-1">{item.label}</span>
                  {active && (
                    <ChevronRight className="h-4 w-4" aria-hidden="true" />
                  )}
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* Footer info */}
      <div className="p-4 border-t border-slate-700">
        <p className="text-xs text-slate-500 text-center">
          CIA-SIE v1.0
        </p>
        <p className="text-xs text-slate-600 text-center mt-1">
          Decision Support Only
        </p>
      </div>
    </aside>
  )
}

