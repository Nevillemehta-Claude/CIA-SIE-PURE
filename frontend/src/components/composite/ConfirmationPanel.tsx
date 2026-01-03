/**
 * ConfirmationPanel Component
 * 
 * Displays confirmations (aligned signals) without implying strength.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * - No "stronger signal" language
 * - No confidence or reliability scoring
 * - Simply describes that signals align
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 2
 */

import { CheckCircle2 } from 'lucide-react'
import { Card, SignalBadge, ConfirmationIndicator, EmptyState } from '@components/atoms'
import type { Confirmation } from '@/types/index'

interface ConfirmationPanelProps {
  /** List of confirmations to display */
  confirmations: Confirmation[]
  /** Maximum number to display (optional) */
  maxDisplay?: number
}

/**
 * ConfirmationPanel displays aligned signals.
 * 
 * CR-002 COMPLIANCE:
 * - Does NOT imply aligned signals are "stronger"
 * - No confidence scoring or weighting
 * - Purely descriptive: "these charts align on X direction"
 */
export function ConfirmationPanel({ 
  confirmations,
  maxDisplay 
}: ConfirmationPanelProps) {
  const displayList = maxDisplay 
    ? confirmations.slice(0, maxDisplay) 
    : confirmations

  if (confirmations.length === 0) {
    return (
      <Card>
        <EmptyState
          title="No confirmations detected"
          description="No charts are currently showing aligned signals."
          icon={CheckCircle2}
        />
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5 text-accent-primary" aria-hidden="true" />
          <h3 className="font-display text-lg font-semibold">
            Confirmations
          </h3>
        </div>
        <ConfirmationIndicator count={confirmations.length} size="sm" />
      </div>

      <p className="text-sm text-slate-400">
        {/* CR-002: No "stronger signal" language */}
        Charts showing aligned directional signals.
      </p>

      {/* Confirmation Cards */}
      <div className="space-y-3">
        {displayList.map((confirmation) => (
          <Card 
            key={`${confirmation.chart_a_id}-${confirmation.chart_b_id}`}
            className="border-accent-primary/30 bg-accent-primary/5"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <SignalBadge 
                  direction={confirmation.aligned_direction} 
                  size="md" 
                />
                <div className="text-sm">
                  <span className="text-white font-medium">
                    {confirmation.chart_a_name}
                  </span>
                  <span className="text-slate-400"> and </span>
                  <span className="text-white font-medium">
                    {confirmation.chart_b_name}
                  </span>
                </div>
              </div>
              
              <span className="text-xs text-slate-500">
                {/* CR-002: No strength indicator - just "align" */}
                align
              </span>
            </div>
          </Card>
        ))}
      </div>

      {/* Show more indicator */}
      {maxDisplay && confirmations.length > maxDisplay && (
        <p className="text-sm text-slate-500 text-center">
          +{confirmations.length - maxDisplay} more confirmations
        </p>
      )}
    </div>
  )
}

