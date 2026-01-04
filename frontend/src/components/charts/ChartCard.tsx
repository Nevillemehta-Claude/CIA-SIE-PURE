import { Card } from '@/components/common/Card'
import { Badge } from '@/components/common/Badge'
import { DirectionBadge } from '@/components/signals/DirectionBadge'
import { FreshnessBadge } from '@/components/signals/FreshnessBadge'
import type { Chart } from '@/types/models'
import type { Signal } from '@/types/models'
import type { FreshnessStatus } from '@/types/enums'
import { BarChart3 } from 'lucide-react'

interface ChartCardProps {
  chart: Chart
  latestSignal?: Signal | null
  freshness?: FreshnessStatus
}

export function ChartCard({ chart, latestSignal, freshness = 'UNAVAILABLE' }: ChartCardProps) {
  return (
    <Card hover className="cursor-pointer">
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded bg-accent-primary/20">
              <BarChart3 className="h-4 w-4 text-accent-primary" />
            </div>
            <div>
              <div className="font-display font-semibold text-accent-primary">
                {chart.chart_code}
              </div>
              <div className="text-xs text-slate-400">{chart.chart_name}</div>
            </div>
          </div>
          <Badge>{chart.timeframe}</Badge>
        </div>

        <div className="flex items-center justify-between border-t border-slate-700 pt-3">
          {latestSignal ? (
            <DirectionBadge direction={latestSignal.direction} size="sm" />
          ) : (
            <span className="text-sm text-slate-500">No signal</span>
          )}
          <FreshnessBadge status={freshness} />
        </div>
      </div>
    </Card>
  )
}

