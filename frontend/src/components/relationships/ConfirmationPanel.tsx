import type { Confirmation } from '@/types/models'
import { ConfirmationCard } from './ConfirmationCard'
import { CheckCircle2 } from 'lucide-react'

interface ConfirmationPanelProps {
  confirmations: Confirmation[]
}

export function ConfirmationPanel({ confirmations }: ConfirmationPanelProps) {
  if (confirmations.length === 0) {
    return (
      <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
        <div className="flex items-center gap-2 text-slate-400">
          <CheckCircle2 className="h-5 w-5" />
          <span>No confirmations detected</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <CheckCircle2 className="h-5 w-5 text-green-500" />
        <h3 className="font-display text-lg font-semibold">
          Confirmations ({confirmations.length})
        </h3>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {confirmations.map((c, index) => (
          <ConfirmationCard 
            key={`${c.chart_a_id}-${c.chart_b_id}-${index}`} 
            confirmation={c} 
          />
        ))}
      </div>
    </div>
  )
}
