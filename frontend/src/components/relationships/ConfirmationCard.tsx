import type { Confirmation } from '@/types/models'
import { DirectionBadge } from '@/components/signals/DirectionBadge'
import { ArrowLeftRight } from 'lucide-react'

interface ConfirmationCardProps {
  confirmation: Confirmation
}

/**
 * ConfirmationCard - Displays a single confirmation between two charts
 * 
 * Shows the two charts that are aligned in the same direction.
 */
export function ConfirmationCard({ confirmation }: ConfirmationCardProps) {
  return (
    <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-4">
      {/* Direction badge */}
      <div className="mb-3 flex items-center justify-center">
        <DirectionBadge direction={confirmation.aligned_direction} />
      </div>

      {/* Chart pair display */}
      <div className="flex items-center justify-center gap-3">
        <span className="rounded bg-surface-tertiary px-3 py-1 text-sm text-slate-300">
          {confirmation.chart_a_name}
        </span>
        <ArrowLeftRight className="h-4 w-4 text-green-500" />
        <span className="rounded bg-surface-tertiary px-3 py-1 text-sm text-slate-300">
          {confirmation.chart_b_name}
        </span>
      </div>
    </div>
  )
}
