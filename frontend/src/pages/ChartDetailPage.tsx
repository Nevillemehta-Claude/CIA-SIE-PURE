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
import { Card, LoadingSpinner, SignalBadge, FreshnessMeter } from '@components/atoms'
import { ArrowLeft, Clock } from 'lucide-react'
import { Direction, FreshnessStatus, SignalType } from '@/types/index'
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
  
  // Placeholder data
  const chart = {
    chart_id: chartId || '1',
    chart_name: 'RSI Momentum',
    chart_code: '01A',
    timeframe: '1h',
    silo_name: 'Primary Analysis',
    instrument_symbol: 'NIFTY',
  }

  // Mock signal history - displayed without ranking or scoring
  const signals = [
    {
      signal_id: '1',
      direction: Direction.BULLISH,
      signal_type: SignalType.STATE_CHANGE,
      signal_timestamp: new Date(Date.now() - 5 * 60000).toISOString(),
      indicators: { rsi: 72.5, close: 24150 },
    },
    {
      signal_id: '2',
      direction: Direction.NEUTRAL,
      signal_type: SignalType.BAR_CLOSE,
      signal_timestamp: new Date(Date.now() - 65 * 60000).toISOString(),
      indicators: { rsi: 55.2, close: 24120 },
    },
    {
      signal_id: '3',
      direction: Direction.BEARISH,
      signal_type: SignalType.STATE_CHANGE,
      signal_timestamp: new Date(Date.now() - 130 * 60000).toISOString(),
      indicators: { rsi: 28.8, close: 24080 },
    },
  ]

  const loading = false
  const currentFreshness = FreshnessStatus.CURRENT

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading chart..." />
        </div>
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
        description={`${chart.chart_code} · ${chart.timeframe} timeframe · ${chart.instrument_symbol}`}
        breadcrumb={breadcrumb}
        actions={
          <FreshnessMeter status={currentFreshness} size="lg" />
        }
      />

      {/* Current Signal */}
      {signals[0] && (
        <Card className="mb-6">
          <h2 className="font-display text-lg font-semibold mb-4">Current Signal</h2>
          <div className="flex items-center gap-4">
            <SignalBadge direction={signals[0].direction} size="lg" />
            <div className="text-sm text-slate-400">
              Received {formatDistanceToNow(new Date(signals[0].signal_timestamp), { addSuffix: true })}
            </div>
          </div>
          
          {/* Indicator Values - CR-003: Displayed as-is, not interpreted */}
          <div className="mt-4 pt-4 border-t border-slate-700">
            <h3 className="text-sm font-medium text-slate-300 mb-3">Indicator Values</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(signals[0].indicators).map(([key, value]) => (
                <div key={key} className="p-3 rounded-lg bg-surface-tertiary/50">
                  <p className="text-xs text-slate-500 uppercase">{key}</p>
                  <p className="text-lg font-mono font-semibold">
                    {typeof value === 'number' ? value.toFixed(2) : String(value)}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Signal History - No ranking or priority implied */}
      <Card>
        <h2 className="font-display text-lg font-semibold mb-4">Signal History</h2>
        <p className="text-sm text-slate-400 mb-4">
          Previous signals from this chart. All signals shown chronologically.
        </p>
        
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
              <div className="hidden md:flex items-center gap-4 text-sm text-slate-400">
                {Object.entries(signal.indicators).slice(0, 2).map(([key, value]) => (
                  <span key={key}>
                    {key}: {typeof value === 'number' ? value.toFixed(1) : String(value)}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </ContentArea>
  )
}

