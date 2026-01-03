/**
 * ChartCard Component
 * 
 * Displays a chart with its current signal.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * - No weight or priority displayed
 * - Equal visual treatment for all charts
 */

import { LineChart } from 'lucide-react'
import { Card, SignalBadge, FreshnessMeter } from '@components/atoms'
import type { Chart } from '@/types/index'
import { Direction, FreshnessStatus } from '@/types/index'

interface ChartCardProps {
  /** Chart data */
  chart: Chart
  /** Current signal direction (if any) */
  direction?: Direction
  /** Current freshness status */
  freshness?: FreshnessStatus
  /** Click handler */
  onClick?: () => void
}

/**
 * ChartCard displays a chart's current status.
 * 
 * CR-002 COMPLIANCE:
 * - No weight field displayed (doesn't exist in Chart type)
 * - No priority or ranking indicator
 * - Equal visual weight for all chart cards
 */
export function ChartCard({ 
  chart,
  direction,
  freshness = FreshnessStatus.UNAVAILABLE,
  onClick 
}: ChartCardProps) {
  return (
    <Card 
      interactive={!!onClick}
      onClick={onClick}
      className="hover:border-accent-primary/50 transition-colors"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <LineChart className="h-5 w-5 text-slate-400" aria-hidden="true" />
          <div>
            <h4 className="font-medium text-white">{chart.chart_name}</h4>
            <p className="text-xs text-slate-500">
              {chart.chart_code} · {chart.timeframe}
            </p>
          </div>
        </div>
        <FreshnessMeter status={freshness} showLabel={false} size="sm" />
      </div>

      {direction ? (
        <SignalBadge direction={direction} size="md" />
      ) : (
        <span className="text-sm text-slate-500 italic">No signal</span>
      )}
    </Card>
  )
}

