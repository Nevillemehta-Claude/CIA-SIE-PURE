import { clsx } from 'clsx'
import type { AIBudgetResponse } from '@/types/api'
import { DollarSign } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'

interface BudgetIndicatorProps {
  budget: AIBudgetResponse
}

export function BudgetIndicator({ budget }: BudgetIndicatorProps) {
  const { percentage_used, remaining, alert_triggered } = budget

  const getStatusColor = () => {
    if (percentage_used >= 90) return 'text-red-400'
    if (percentage_used >= 80) return 'text-amber-400'
    if (percentage_used >= 50) return 'text-yellow-400'
    return 'text-green-400'
  }

  const getProgressColor = () => {
    if (percentage_used >= 90) return 'bg-red-500'
    if (percentage_used >= 80) return 'bg-amber-500'
    if (percentage_used >= 50) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  return (
    <div className="flex items-center gap-2">
      <DollarSign className={clsx('h-4 w-4', getStatusColor())} />
      <div className="hidden sm:block">
        <div className="flex items-center gap-2">
          <div className="h-1.5 w-20 overflow-hidden rounded-full bg-slate-700">
            <div
              className={clsx('h-full transition-all', getProgressColor())}
              style={{ width: `${Math.min(percentage_used, 100)}%` }}
            />
          </div>
          <span className={clsx('text-xs font-medium', getStatusColor())}>
            {formatCurrency(remaining)}
          </span>
        </div>
      </div>
      {alert_triggered && (
        <span className="rounded bg-red-500/20 px-1.5 py-0.5 text-xs text-red-400">
          Low
        </span>
      )}
    </div>
  )
}

