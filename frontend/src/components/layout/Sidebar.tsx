import { NavLink } from 'react-router-dom'
import { clsx } from 'clsx'
import { Activity, BarChart3, FolderKanban, Settings, MessageSquare, Home, Plug, Layers, BookOpen } from 'lucide-react'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: Home },
  { to: '/instruments', label: 'Instruments', icon: Activity },
  { to: '/baskets', label: 'Baskets', icon: Layers },
  { to: '/platforms', label: 'Platforms', icon: Plug },
  { to: '/charts', label: 'Chart Reference', icon: BookOpen },
  { to: '/chat', label: 'AI Chat', icon: MessageSquare },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export function Sidebar() {
  return (
    <aside 
      className="fixed inset-y-0 left-0 z-50 hidden w-64 flex-col border-r border-slate-700 bg-surface-primary lg:flex"
      aria-label="Main sidebar"
    >
      {/* Logo */}
      <div className="flex h-16 items-center border-b border-slate-700 px-6">
        <NavLink to="/" className="flex items-center gap-3" aria-label="CIA-SIE Home">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent-primary" aria-hidden="true">
            <BarChart3 className="h-5 w-5 text-white" />
          </div>
          <div>
            <div className="font-display text-lg font-bold text-white">CIA-SIE</div>
            <div className="text-xs text-slate-400">Chart Intelligence</div>
          </div>
        </NavLink>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4" aria-label="Primary navigation menu">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-accent-primary text-white'
                  : 'text-slate-300 hover:bg-surface-secondary hover:text-white'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Constitutional Banner */}
      <div 
        className="border-t border-slate-700 p-4"
        role="note"
        aria-label="Constitutional reminder"
      >
        <div className="rounded-lg bg-amber-500/10 p-3">
          <div className="flex items-center gap-2 text-xs font-medium text-amber-400">
            <FolderKanban className="h-4 w-4" aria-hidden="true" />
            Decision-Support Only
          </div>
          <p className="mt-1 text-xs text-slate-400">
            This tool describes data. Decisions are yours.
          </p>
        </div>
      </div>
    </aside>
  )
}

