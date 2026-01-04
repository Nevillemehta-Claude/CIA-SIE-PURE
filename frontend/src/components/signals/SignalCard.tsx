import { formatDistanceToNow } from '@/lib/utils'
import { Card } from '@/components/common/Card'
import { Badge } from '@/components/common/Badge'
import { DirectionBadge } from './DirectionBadge'
import type { Signal } from '@/types/models'

interface SignalCardProps {
  signal: Signal
}

export function SignalCard({ signal }: SignalCardProps) {
  return (
    <Card className="space-y-3">
      <div className="flex items-center justify-between">
        <DirectionBadge direction={signal.direction} />
        <Badge>{signal.signal_type}</Badge>
      </div>

      <div className="text-sm text-slate-400">
        Received {formatDistanceToNow(signal.received_at)}
      </div>

      {signal.indicators && Object.keys(signal.indicators).length > 0 && (
        <div className="border-t border-slate-700 pt-3">
          <div className="text-xs font-medium uppercase text-slate-500">Indicators</div>
          <div className="mt-1 flex flex-wrap gap-2">
            {Object.entries(signal.indicators).map(([key, value]) => (
              <span
                key={key}
                className="rounded bg-surface-tertiary px-2 py-1 text-xs text-slate-300"
              >
                {key}: {value}
              </span>
            ))}
          </div>
        </div>
      )}
    </Card>
  )
}

