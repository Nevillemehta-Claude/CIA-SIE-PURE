/**
 * SignalHistoryList Component
 * 
 * Displays a chronological list of signals.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: Signals displayed chronologically, not by priority
 * - CR-003: No interpretation of signal sequence
 */

import { Clock } from 'lucide-react'
import { SignalBadge, EmptyState } from '@components/atoms'
import type { Signal } from '@/types/index'
import { formatDistanceToNow } from 'date-fns'

interface SignalHistoryListProps {
  /** Signals to display */
  signals: Signal[]
  /** Maximum number to display */
  limit?: number
}

/**
 * SignalHistoryList displays signals in chronological order.
 * 
 * CR-002 COMPLIANCE:
 * - Signals ordered by time, not priority or importance
 * - No "best" or "most reliable" signal indication
 */
export function SignalHistoryList({ 
  signals,
  limit 
}: SignalHistoryListProps) {
  const displayList = limit ? signals.slice(0, limit) : signals

  if (signals.length === 0) {
    return (
      <EmptyState
        title="No signals received"
        description="Signals will appear here when received from TradingView."
        icon={Clock}
      />
    )
  }

  return (
    <div className="space-y-2">
      {displayList.map((signal) => (
        <div 
          key={signal.signal_id}
          className="flex items-center justify-between p-3 rounded-lg bg-surface-tertiary/30 hover:bg-surface-tertiary/50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <SignalBadge direction={signal.direction} size="sm" />
            <div>
              <span className="text-sm font-medium">{signal.signal_type}</span>
              <div className="flex items-center gap-1 text-xs text-slate-500">
                <Clock className="h-3 w-3" aria-hidden="true" />
                {formatDistanceToNow(new Date(signal.signal_timestamp), { addSuffix: true })}
              </div>
            </div>
          </div>

          {/* Quick indicator preview */}
          <div className="hidden sm:flex items-center gap-3 text-xs text-slate-400">
            {Object.entries(signal.indicators).slice(0, 2).map(([key, value]) => (
              <span key={key}>
                {key}: {typeof value === 'number' ? value.toFixed(1) : String(value)}
              </span>
            ))}
          </div>
        </div>
      ))}

      {limit && signals.length > limit && (
        <p className="text-sm text-slate-500 text-center pt-2">
          +{signals.length - limit} more signals
        </p>
      )}
    </div>
  )
}

