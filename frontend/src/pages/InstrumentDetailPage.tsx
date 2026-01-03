/**
 * InstrumentDetailPage Component
 *
 * Detail view for a single instrument showing all silos and charts.
 *
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: All charts displayed with equal prominence
 * - CR-002: No aggregated/net direction displayed
 * - CR-003: Descriptive language only
 */

import { useParams, Link } from 'react-router-dom'
import { PageHeader, ContentArea, GridLayout } from '@components/layout'
import { Card, LoadingSpinner, EmptyState, SignalBadge, FreshnessMeter, ErrorMessage } from '@components/atoms'
import { ChevronRight, LineChart, ArrowLeft } from 'lucide-react'
import { useInstrument, useSilosByInstrument, useChartsBySilo, useLatestSignal } from '@/hooks'
import { useFreshness } from '@/hooks'
import type { Chart, Silo } from '@/types'
import { Direction } from '@/types'

/**
 * ChartWithSignal component - displays a chart with its latest signal
 */
function ChartWithSignal({ chart, silo }: { chart: Chart; silo: Silo }) {
  const { data: latestSignal, isLoading } = useLatestSignal(chart.chart_id)

  // Calculate freshness from latest signal
  const freshness = useFreshness(
    latestSignal?.signal_timestamp ?? null,
    {
      current_threshold_min: silo.current_threshold_min,
      recent_threshold_min: silo.recent_threshold_min,
      stale_threshold_min: silo.stale_threshold_min,
    }
  )

  const direction = latestSignal?.direction ?? Direction.NEUTRAL

  return (
    <Link to={`/charts/${chart.chart_id}`}>
      <Card
        variant="outlined"
        className="hover:border-accent-primary/50 transition-colors"
        interactive
      >
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <LineChart className="h-5 w-5 text-slate-400" aria-hidden="true" />
            <span className="font-medium">{chart.chart_name}</span>
          </div>
          {isLoading ? (
            <div className="w-16 h-4 bg-surface-tertiary animate-pulse rounded" />
          ) : (
            <FreshnessMeter status={freshness} showLabel={false} size="sm" />
          )}
        </div>

        {/* CR-002: Direction displayed with equal prominence */}
        {isLoading ? (
          <div className="w-20 h-6 bg-surface-tertiary animate-pulse rounded" />
        ) : (
          <SignalBadge direction={direction} size="md" />
        )}

        <p className="text-xs text-slate-500 mt-2">{chart.timeframe} timeframe</p>
      </Card>
    </Link>
  )
}

/**
 * SiloSection component - displays a silo with its charts
 */
function SiloSection({ silo }: { silo: Silo }) {
  const { data: charts, isLoading } = useChartsBySilo(silo.silo_id)

  return (
    <Card padding="lg">
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-display text-xl font-semibold">
          {silo.silo_name}
        </h2>
        <Link
          to={`/silos/${silo.silo_id}`}
          className="text-sm text-accent-primary hover:underline flex items-center gap-1"
        >
          View Details
          <ChevronRight className="h-4 w-4" aria-hidden="true" />
        </Link>
      </div>

      {/*
        Chart Grid - CONSTITUTIONAL: All charts have equal size and prominence
        No visual hierarchy suggesting one chart is more important
      */}
      {isLoading ? (
        <GridLayout columns={3} gap="md">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-32 bg-surface-tertiary animate-pulse rounded-lg" />
          ))}
        </GridLayout>
      ) : charts && charts.length > 0 ? (
        <GridLayout columns={3} gap="md">
          {charts.map((chart) => (
            <ChartWithSignal key={chart.chart_id} chart={chart} silo={silo} />
          ))}
        </GridLayout>
      ) : (
        <div className="p-4 rounded-lg bg-surface-tertiary/30 text-center text-slate-400">
          <p>No charts configured for this silo</p>
        </div>
      )}
    </Card>
  )
}

/**
 * InstrumentDetailPage displays all data for a single instrument.
 *
 * CRITICAL: This page does NOT display:
 * - Overall instrument direction
 * - Aggregated signal summary
 * - Signal priority or ranking
 */
export function InstrumentDetailPage() {
  const { instrumentId } = useParams<{ instrumentId: string }>()

  // Fetch real data from API
  const { data: instrument, isLoading: instrumentLoading, error: instrumentError } = useInstrument(instrumentId ?? '')
  const { data: silos, isLoading: silosLoading } = useSilosByInstrument(instrumentId ?? '')

  const loading = instrumentLoading || silosLoading

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading instrument..." />
        </div>
      </ContentArea>
    )
  }

  if (instrumentError || !instrument) {
    return (
      <ContentArea>
        <PageHeader title="Instrument Not Found" />
        <ErrorMessage
          title="Failed to load instrument"
          message={instrumentError instanceof Error ? instrumentError.message : 'Instrument not found'}
          onRetry={() => window.location.reload()}
        />
      </ContentArea>
    )
  }

  const breadcrumb = (
    <Link
      to="/instruments"
      className="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-white transition-colors"
    >
      <ArrowLeft className="h-4 w-4" aria-hidden="true" />
      Back to Instruments
    </Link>
  )

  return (
    <ContentArea>
      <PageHeader
        title={instrument.display_name}
        description={`Symbol: ${instrument.symbol}`}
        breadcrumb={breadcrumb}
      />

      {/* Silos List - Each silo displayed equally */}
      <div className="space-y-8">
        {silos && silos.length > 0 ? (
          silos.map((silo) => (
            <SiloSection key={silo.silo_id} silo={silo} />
          ))
        ) : (
          <EmptyState
            title="No silos configured"
            description="Create a silo to organize your charts for this instrument."
            icon={LineChart}
          />
        )}
      </div>
    </ContentArea>
  )
}
