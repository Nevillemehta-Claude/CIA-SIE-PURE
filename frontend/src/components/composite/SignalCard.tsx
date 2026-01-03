/**
 * SignalCard Component
 * 
 * Displays a single signal with its details.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: No confidence or strength indicators
 * - CR-002: Signal displayed with equal visual weight
 * - CR-003: Indicator values shown as-is, not interpreted
 */

import { clsx } from 'clsx'
import { Clock } from 'lucide-react'
import { SignalBadge, FreshnessMeter, Card } from '@components/atoms'
import type { ChartSignalStatus } from '@/types/index'
import { formatDistanceToNow } from 'date-fns'

interface SignalCardProps {
  /** Chart with signal status */
  chartStatus: ChartSignalStatus
  /** Additional CSS classes */
  className?: string
  /** Click handler */
  onClick?: () => void
}

/**
 * SignalCard displays a chart's current signal status.
 * 
 * CR-002 COMPLIANCE: 
 * - No confidence score displayed
 * - No signal strength indicator
 * - Equal visual weight regardless of direction
 */
export function SignalCard({ 
  chartStatus, 
  className,
  onClick 
}: SignalCardProps) {
  const { chart_name, chart_code, timeframe, latest_signal, freshness } = chartStatus

  return (
    <Card 
      className={clsx('transition-colors', className)}
      interactive={!!onClick}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-medium text-white">{chart_name}</h3>
          <p className="text-xs text-slate-500">{chart_code} · {timeframe}</p>
        </div>
        <FreshnessMeter status={freshness} showLabel={false} size="sm" />
      </div>

      {/* Signal Display - CR-002: Equal prominence */}
      {latest_signal ? (
        <div className="space-y-3">
          <SignalBadge direction={latest_signal.direction} size="md" />
          
          <div className="flex items-center gap-1 text-xs text-slate-500">
            <Clock className="h-3 w-3" aria-hidden="true" />
            <span>
              {formatDistanceToNow(new Date(latest_signal.signal_timestamp), { addSuffix: true })}
            </span>
          </div>

          {/* Indicator Preview - CR-003: Raw values only */}
          {Object.keys(latest_signal.indicators).length > 0 && (
            <div className="pt-3 border-t border-slate-700">
              <div className="flex flex-wrap gap-2">
                {Object.entries(latest_signal.indicators).slice(0, 3).map(([key, value]) => (
                  <span 
                    key={key} 
                    className="text-xs px-2 py-1 bg-surface-tertiary/50 rounded"
                  >
                    {key}: {typeof value === 'number' ? value.toFixed(1) : String(value)}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <p className="text-sm text-slate-500 italic">No signal data</p>
      )}
    </Card>
  )
}

