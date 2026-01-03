/**
 * DashboardPage Component
 * 
 * Main dashboard showing signal overview with equal prominence for all signals.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: Contradictions displayed with equal prominence - no resolution
 * - CR-002: No "net signal" or "overall direction" displays
 * - CR-003: All text is descriptive, not prescriptive
 */

import { PageHeader, ContentArea, GridLayout } from '@components/layout'
import { Card, EmptyState, LoadingSpinner, ContradictionAlert, ConfirmationIndicator } from '@components/atoms'
import { Activity, LineChart, AlertTriangle, CheckCircle2 } from 'lucide-react'

/**
 * DashboardPage displays the main signal overview.
 * 
 * CRITICAL: This page does NOT display:
 * - Aggregated directions
 * - Net signals
 * - Confidence scores
 * - Signal rankings
 */
export function DashboardPage() {
  // Placeholder data for demonstration
  const loading = false
  const hasData = true

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading dashboard..." />
        </div>
      </ContentArea>
    )
  }

  if (!hasData) {
    return (
      <ContentArea>
        <PageHeader 
          title="Dashboard"
          description="Signal overview and relationship summary"
        />
        <EmptyState
          title="No instruments configured"
          description="Add an instrument to start receiving signals from your TradingView charts."
          icon={LineChart}
          action={{
            label: 'Add Instrument',
            onClick: () => { /* Navigate to add instrument */ }
          }}
        />
      </ContentArea>
    )
  }

  return (
    <ContentArea>
      <PageHeader 
        title="Dashboard"
        description="Signal overview and relationship summary"
      />

      {/* Quick Stats - NOTE: No aggregation, just counts */}
      <GridLayout columns={4} gap="md" className="mb-8">
        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-accent-primary/20">
            <Activity className="h-6 w-6 text-accent-primary" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">12</p>
            <p className="text-sm text-slate-400">Active Charts</p>
          </div>
        </Card>

        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-green-500/20">
            <LineChart className="h-6 w-6 text-green-500" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">8</p>
            <p className="text-sm text-slate-400">Current Signals</p>
          </div>
        </Card>

        {/* Contradictions Count - Equal prominence */}
        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-amber-500/20">
            <AlertTriangle className="h-6 w-6 text-amber-500" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">3</p>
            <p className="text-sm text-slate-400">Contradictions</p>
          </div>
        </Card>

        {/* Confirmations Count - Equal prominence */}
        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-blue-500/20">
            <CheckCircle2 className="h-6 w-6 text-blue-500" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">4</p>
            <p className="text-sm text-slate-400">Confirmations</p>
          </div>
        </Card>
      </GridLayout>

      {/* Relationship Summary - CR-002: No aggregation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Contradictions Section */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display text-lg font-semibold flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" aria-hidden="true" />
              Detected Contradictions
            </h2>
            <ContradictionAlert count={3} size="sm" />
          </div>
          <p className="text-sm text-slate-400 mb-4">
            {/* CR-002: Descriptive language only */}
            Charts showing opposing signals. View details for full context.
          </p>
          {/* Placeholder for ContradictionPanel */}
          <div className="space-y-3">
            <div className="p-3 rounded-lg bg-surface-tertiary/50 border border-amber-500/20">
              <p className="text-sm">Chart A shows BULLISH vs Chart B shows BEARISH</p>
            </div>
            <div className="p-3 rounded-lg bg-surface-tertiary/50 border border-amber-500/20">
              <p className="text-sm">Chart C shows BEARISH vs Chart D shows BULLISH</p>
            </div>
          </div>
        </Card>

        {/* Confirmations Section */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display text-lg font-semibold flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-blue-500" aria-hidden="true" />
              Detected Confirmations
            </h2>
            <ConfirmationIndicator count={4} size="sm" />
          </div>
          <p className="text-sm text-slate-400 mb-4">
            {/* CR-002: No "stronger signal" language */}
            Charts showing aligned signals.
          </p>
          {/* Placeholder for ConfirmationPanel */}
          <div className="space-y-3">
            <div className="p-3 rounded-lg bg-surface-tertiary/50 border border-blue-500/20">
              <p className="text-sm">Charts A, E, F align on BULLISH</p>
            </div>
            <div className="p-3 rounded-lg bg-surface-tertiary/50 border border-blue-500/20">
              <p className="text-sm">Charts G, H align on BEARISH</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <h2 className="font-display text-lg font-semibold mb-4">
          Recent Signal Activity
        </h2>
        <p className="text-sm text-slate-400">
          Latest signals received from your charts.
        </p>
        {/* Placeholder for SignalHistoryList */}
      </Card>
    </ContentArea>
  )
}

