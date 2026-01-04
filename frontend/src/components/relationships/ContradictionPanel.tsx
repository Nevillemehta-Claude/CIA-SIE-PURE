import type { Contradiction } from '@/types/models'
import { ContradictionCard } from './ContradictionCard'
import { AlertTriangle } from 'lucide-react'

interface ContradictionPanelProps {
  contradictions: Contradiction[]
}

export function ContradictionPanel({ contradictions }: ContradictionPanelProps) {
  if (contradictions.length === 0) {
    return (
      <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
        <div className="flex items-center gap-2 text-slate-400">
          <AlertTriangle className="h-5 w-5" />
          <span>No contradictions detected</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <AlertTriangle className="h-5 w-5 text-amber-500" />
        <h3 className="font-display text-lg font-semibold">
          Contradictions ({contradictions.length})
        </h3>
      </div>

      <div className="grid gap-4">
        {contradictions.map((c) => (
          <ContradictionCard
            key={`${c.chart_a_id}-${c.chart_b_id}`}
            contradiction={c}
          />
        ))}
      </div>
    </div>
  )
}

