import { Link } from 'react-router-dom'
import { useBudget } from '@/hooks/useAI'
import { Settings, MessageSquare } from 'lucide-react'
import { BudgetIndicator } from '@/components/ai/BudgetIndicator'

export function Header() {
  const { data: budget } = useBudget()

  return (
    <header 
      className="sticky top-0 z-40 border-b border-slate-700 bg-surface-primary/80 backdrop-blur-sm"
      role="banner"
      aria-label="CIA-SIE main header"
    >
      <div className="flex h-16 items-center justify-between px-6">
        <div className="lg:hidden">
          <span className="font-display text-lg font-bold text-accent-primary">CIA-SIE</span>
        </div>

        <div className="flex-1" />

        <div className="flex items-center gap-4">
          {budget && (
            <div role="status" aria-live="polite" aria-label="AI budget status">
              <BudgetIndicator budget={budget} />
            </div>
          )}

          <Link
            to="/chat"
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-slate-300 transition-colors hover:bg-surface-secondary hover:text-white"
            aria-label="Open AI Chat"
          >
            <MessageSquare className="h-4 w-4" aria-hidden="true" />
            <span className="hidden sm:inline">Chat</span>
          </Link>

          <Link
            to="/settings"
            className="rounded-lg p-2 text-slate-400 transition-colors hover:bg-surface-secondary hover:text-white"
            aria-label="Open Settings"
          >
            <Settings className="h-5 w-5" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </header>
  )
}

