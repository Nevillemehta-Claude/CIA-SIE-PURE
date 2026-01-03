/**
 * ContradictionPanel Component
 * 
 * Displays contradictions with side-by-side layout and EQUAL prominence.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * - NEVER resolve contradictions
 * - Display both sides with IDENTICAL styling
 * - No visual hierarchy suggesting one is "correct"
 * - No aggregation or "winner" indication
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 2
 */

import { AlertTriangle, ArrowLeftRight } from 'lucide-react'
import { Card, SignalBadge, ContradictionAlert, EmptyState } from '@components/atoms'
import type { Contradiction } from '@/types/index'

interface ContradictionPanelProps {
  /** List of contradictions to display */
  contradictions: Contradiction[]
  /** Maximum number to display (optional) */
  maxDisplay?: number
}

/**
 * ContradictionPanel displays ALL contradictions with equal prominence.
 * 
 * CR-002 COMPLIANCE:
 * - Both charts in each contradiction have IDENTICAL styling
 * - No resolution, preference, or ranking is shown
 * - Equal space allocated to each side
 */
export function ContradictionPanel({ 
  contradictions,
  maxDisplay 
}: ContradictionPanelProps) {
  const displayList = maxDisplay 
    ? contradictions.slice(0, maxDisplay) 
    : contradictions

  if (contradictions.length === 0) {
    return (
      <Card>
        <EmptyState
          title="No contradictions detected"
          description="All charts are showing aligned or neutral signals."
          icon={AlertTriangle}
        />
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-amber-500" aria-hidden="true" />
          <h3 className="font-display text-lg font-semibold">
            Contradictions
          </h3>
        </div>
        <ContradictionAlert count={contradictions.length} size="sm" />
      </div>

      <p className="text-sm text-slate-400">
        {/* CR-002: Descriptive text only - no resolution suggested */}
        Charts showing opposing directional signals.
      </p>

      {/* 
        Contradiction Cards - CONSTITUTIONAL:
        Each contradiction displays both sides with IDENTICAL styling.
        The grid layout ensures equal space allocation.
      */}
      <div className="space-y-4">
        {displayList.map((contradiction) => (
          <Card 
            key={`${contradiction.chart_a_id}-${contradiction.chart_b_id}`}
            className="border-amber-500/30 bg-amber-500/5"
          >
            {/* 
              Grid layout: [Chart A] [vs] [Chart B]
              CONSTITUTIONAL: Both sides have equal column width (1fr)
            */}
            <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">
              {/* Chart A - EQUAL SIZE */}
              <div className="rounded-lg bg-surface-secondary p-4 text-center">
                <p className="text-sm text-slate-400 mb-2">
                  {contradiction.chart_a_name}
                </p>
                <SignalBadge 
                  direction={contradiction.chart_a_direction} 
                  size="lg" 
                />
              </div>

              {/* Separator - Neutral, no bias */}
              <div className="flex flex-col items-center gap-1">
                <ArrowLeftRight 
                  className="h-5 w-5 text-slate-500" 
                  aria-hidden="true" 
                />
                <span className="text-xs text-slate-500">vs</span>
              </div>

              {/* Chart B - IDENTICAL to Chart A styling */}
              <div className="rounded-lg bg-surface-secondary p-4 text-center">
                <p className="text-sm text-slate-400 mb-2">
                  {contradiction.chart_b_name}
                </p>
                <SignalBadge 
                  direction={contradiction.chart_b_direction} 
                  size="lg" 
                />
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Show more indicator */}
      {maxDisplay && contradictions.length > maxDisplay && (
        <p className="text-sm text-slate-500 text-center">
          +{contradictions.length - maxDisplay} more contradictions
        </p>
      )}
    </div>
  )
}

