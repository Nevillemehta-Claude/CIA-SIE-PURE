import type { Confirmation } from '@/types/models'
import { DirectionBadge } from '@/components/signals/DirectionBadge'

interface ConfirmationCardProps {
  confirmation: Confirmation
}

export function ConfirmationCard({ confirmation }: ConfirmationCardProps) {
  return (
    <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
      <div className="mb-3 flex items-center gap-2">
        <DirectionBadge direction={confirmation.direction} />
        <span className="text-sm text-slate-400">
          {confirmation.count} charts aligned
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {confirmation.charts.map((chart) => (
          <span
            key={chart.chart_id}
            className="rounded bg-surface-tertiary px-2 py-1 text-xs text-slate-300"
          >
            {chart.chart_name}
          </span>
        ))}
      </div>
    </div>
  )
}

