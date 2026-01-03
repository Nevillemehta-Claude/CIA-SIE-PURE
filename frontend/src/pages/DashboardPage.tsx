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

import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { PageHeader, ContentArea, GridLayout } from '@components/layout'
import { Card, EmptyState, LoadingSpinner, ContradictionAlert, ConfirmationIndicator, ErrorMessage } from '@components/atoms'
import { ContradictionPanel, ConfirmationPanel } from '@components/composite'
import { Activity, LineChart, AlertTriangle, CheckCircle2 } from 'lucide-react'
import { useInstruments, useCharts } from '@/hooks'
import type { Contradiction, Confirmation } from '@/types'

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
  // Fetch real data from API
  const { data: instruments, isLoading: instrumentsLoading, error: instrumentsError } = useInstruments({ active_only: true })
  const { data: charts, isLoading: chartsLoading, error: chartsError } = useCharts({ active_only: true })

  // Aggregate loading and error states
  const loading = instrumentsLoading || chartsLoading
  const error = instrumentsError || chartsError

  // Calculate stats from real data
  const stats = useMemo(() => {
    const activeCharts = charts?.length ?? 0
    // For signals, we count charts that have at least one signal (approximation)
    // In a full implementation, we'd have a signals count endpoint
    const currentSignals = charts?.filter(c => c.is_active).length ?? 0

    return { activeCharts, currentSignals }
  }, [charts])

  // Note: For contradictions and confirmations, we'd need to fetch relationship
  // summaries for each silo. For now, we'll display placeholder until
  // relationship data is fetched. In a production app, you'd have a dedicated
  // dashboard endpoint or aggregate the data client-side.
  const contradictions: Contradiction[] = useMemo(() => [], [])
  const confirmations: Confirmation[] = useMemo(() => [], [])

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading dashboard..." />
        </div>
      </ContentArea>
    )
  }

  if (error) {
    return (
      <ContentArea>
        <PageHeader
          title="Dashboard"
          description="Signal overview and relationship summary"
        />
        <ErrorMessage
          title="Failed to load dashboard"
          message={error instanceof Error ? error.message : 'An error occurred while loading data'}
          onRetry={() => window.location.reload()}
        />
      </ContentArea>
    )
  }

  const hasData = (instruments?.length ?? 0) > 0

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
            <p className="text-2xl font-bold">{stats.activeCharts}</p>
            <p className="text-sm text-slate-400">Active Charts</p>
          </div>
        </Card>

        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-green-500/20">
            <LineChart className="h-6 w-6 text-green-500" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">{stats.currentSignals}</p>
            <p className="text-sm text-slate-400">Current Signals</p>
          </div>
        </Card>

        {/* Contradictions Count - Equal prominence */}
        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-amber-500/20">
            <AlertTriangle className="h-6 w-6 text-amber-500" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">{contradictions.length}</p>
            <p className="text-sm text-slate-400">Contradictions</p>
          </div>
        </Card>

        {/* Confirmations Count - Equal prominence */}
        <Card className="flex items-center gap-4">
          <div className="p-3 rounded-lg bg-blue-500/20">
            <CheckCircle2 className="h-6 w-6 text-blue-500" aria-hidden="true" />
          </div>
          <div>
            <p className="text-2xl font-bold">{confirmations.length}</p>
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
            <ContradictionAlert count={contradictions.length} size="sm" />
          </div>
          <p className="text-sm text-slate-400 mb-4">
            {/* CR-002: Descriptive language only */}
            Charts showing opposing signals. View details for full context.
          </p>
          {contradictions.length > 0 ? (
            <ContradictionPanel contradictions={contradictions} />
          ) : (
            <div className="p-4 rounded-lg bg-surface-tertiary/30 text-center text-slate-400">
              <p>No contradictions detected</p>
              <p className="text-xs mt-1">Contradictions appear when charts show opposing signals</p>
            </div>
          )}
        </Card>

        {/* Confirmations Section */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display text-lg font-semibold flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-blue-500" aria-hidden="true" />
              Detected Confirmations
            </h2>
            <ConfirmationIndicator count={confirmations.length} size="sm" />
          </div>
          <p className="text-sm text-slate-400 mb-4">
            {/* CR-002: No "stronger signal" language */}
            Charts showing aligned signals.
          </p>
          {confirmations.length > 0 ? (
            <ConfirmationPanel confirmations={confirmations} />
          ) : (
            <div className="p-4 rounded-lg bg-surface-tertiary/30 text-center text-slate-400">
              <p>No confirmations detected</p>
              <p className="text-xs mt-1">Confirmations appear when charts show aligned signals</p>
            </div>
          )}
        </Card>
      </div>

      {/* Active Instruments List */}
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-display text-lg font-semibold">
            Active Instruments
          </h2>
          <Link
            to="/instruments"
            className="text-sm text-accent-primary hover:underline"
          >
            View All
          </Link>
        </div>
        <div className="space-y-3">
          {instruments?.slice(0, 5).map((instrument) => (
            <Link
              key={instrument.instrument_id}
              to={`/instruments/${instrument.instrument_id}`}
              className="flex items-center justify-between p-3 rounded-lg bg-surface-tertiary/30 hover:bg-surface-tertiary/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <LineChart className="h-5 w-5 text-slate-400" aria-hidden="true" />
                <div>
                  <p className="font-medium">{instrument.symbol}</p>
                  <p className="text-sm text-slate-400">{instrument.display_name}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </Card>
    </ContentArea>
  )
}
