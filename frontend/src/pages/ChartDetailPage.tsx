/**
 * ChartDetailPage Component
 *
 * Detail view for a single chart showing signal history and indicators.
 *
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: No confidence or strength scores displayed
 * - CR-003: All indicator values shown as-is, not interpreted
 */

import { useParams, Link } from 'react-router-dom'
import { PageHeader, ContentArea } from '@components/layout'
import { Card, LoadingSpinner, SignalBadge, FreshnessMeter, ErrorMessage } from '@components/atoms'
import { ArrowLeft, Clock } from 'lucide-react'
import { useChart, useSignalsByChart, useSilo } from '@/hooks'
import { useFreshness } from '@/hooks'
import { formatDistanceToNow } from 'date-fns'

/**
 * ChartDetailPage displays chart details and signal history.
 *
 * CRITICAL: This page does NOT display:
 * - Signal confidence scores
 * - Signal strength ratings
 * - Recommendations based on signals
 */
export function ChartDetailPage() {
  const { chartId } = useParams<{ chartId: string }>()

  // Fetch real data from API
  const { data: chart, isLoading: chartLoading, error: chartError } = useChart(chartId ?? '')
  const { data: signals, isLoading: signalsLoading } = useSignalsByChart(chartId ?? '', { limit: 20 })

  // Fetch parent silo for freshness thresholds
  const { data: silo } = useSilo(chart?.silo_id ?? '')

  const loading = chartLoading || signalsLoading

  // Calculate freshness for current signal
  const latestSignal = signals?.[0]
  const currentFreshness = useFreshness(
    latestSignal?.signal_timestamp,
    silo ? {
      current_threshold_min: silo.current_threshold_min,
      recent_threshold_min: silo.recent_threshold_min,
      stale_threshold_min: silo.stale_threshold_min,
    } : undefined
  )

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading chart..." />
        </div>
      </ContentArea>
    )
  }

  if (chartError || !chart) {
    return (
      <ContentArea>
        <PageHeader title="Chart Not Found" />
        <ErrorMessage
          title="Failed to load chart"
          message={chartError instanceof Error ? chartError.message : 'Chart not found'}
          onRetry={() => window.location.reload()}
        />
      </ContentArea>
    )
  }

  const breadcrumb = (
    <Link
      to="/"
      className="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-white transition-colors"
    >
      <ArrowLeft className="h-4 w-4" aria-hidden="true" />
      Back to Dashboard
    </Link>
  )

  return (
    <ContentArea maxWidth="lg">
      <PageHeader
        title={chart.chart_name}
        description={`${chart.chart_code} · ${chart.timeframe} timeframe`}
        breadcrumb={breadcrumb}
        actions={
          <FreshnessMeter status={currentFreshness} size="lg" />
        }
      />

      {/* Current Signal */}
      {latestSignal ? (
        <Card className="mb-6">
          <h2 className="font-display text-lg font-semibold mb-4">Current Signal</h2>
          <div className="flex items-center gap-4">
            <SignalBadge direction={latestSignal.direction} size="lg" />
            <div className="text-sm text-slate-400">
              Received {formatDistanceToNow(new Date(latestSignal.signal_timestamp), { addSuffix: true })}
            </div>
          </div>

          {/* Indicator Values - CR-003: Displayed as-is, not interpreted */}
          {latestSignal.indicators && Object.keys(latestSignal.indicators).length > 0 && (
            <div className="mt-4 pt-4 border-t border-slate-700">
              <h3 className="text-sm font-medium text-slate-300 mb-3">Indicator Values</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(latestSignal.indicators).map(([key, value]) => (
                  <div key={key} className="p-3 rounded-lg bg-surface-tertiary/50">
                    <p className="text-xs text-slate-500 uppercase">{key}</p>
                    <p className="text-lg font-mono font-semibold">
                      {typeof value === 'number' ? value.toFixed(2) : String(value)}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </Card>
      ) : (
        <Card className="mb-6">
          <h2 className="font-display text-lg font-semibold mb-4">Current Signal</h2>
          <div className="p-4 rounded-lg bg-surface-tertiary/30 text-center text-slate-400">
            <p>No signals received yet</p>
            <p className="text-xs mt-1">Signals will appear when TradingView sends them via webhook</p>
          </div>
        </Card>
      )}

      {/* Signal History - No ranking or priority implied */}
      <Card>
        <h2 className="font-display text-lg font-semibold mb-4">Signal History</h2>
        <p className="text-sm text-slate-400 mb-4">
          Previous signals from this chart. All signals shown chronologically.
        </p>

        {signals && signals.length > 0 ? (
          <div className="space-y-3">
            {signals.map((signal) => (
              <div
                key={signal.signal_id}
                className="flex items-center justify-between p-4 rounded-lg bg-surface-tertiary/30"
              >
                <div className="flex items-center gap-4">
                  <SignalBadge direction={signal.direction} size="sm" />
                  <div>
                    <span className="text-sm font-medium">{signal.signal_type}</span>
                    <div className="flex items-center gap-1 text-xs text-slate-500">
                      <Clock className="h-3 w-3" aria-hidden="true" />
                      {formatDistanceToNow(new Date(signal.signal_timestamp), { addSuffix: true })}
                    </div>
                  </div>
                </div>

                {/* Indicator preview */}
                {signal.indicators && (
                  <div className="hidden md:flex items-center gap-4 text-sm text-slate-400">
                    {Object.entries(signal.indicators).slice(0, 2).map(([key, value]) => (
                      <span key={key}>
                        {key}: {typeof value === 'number' ? value.toFixed(1) : String(value)}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="p-4 rounded-lg bg-surface-tertiary/30 text-center text-slate-400">
            <p>No signal history available</p>
          </div>
        )}
      </Card>
    </ContentArea>
  )
}
