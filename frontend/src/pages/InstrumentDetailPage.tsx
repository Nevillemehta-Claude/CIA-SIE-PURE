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
import { Card, LoadingSpinner, EmptyState, SignalBadge, FreshnessMeter } from '@components/atoms'
import { ChevronRight, LineChart, ArrowLeft } from 'lucide-react'
import { Direction, FreshnessStatus } from '@/types/index'

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
  
  // Placeholder data
  const loading = false
  const instrument = {
    instrument_id: instrumentId || '1',
    symbol: 'NIFTY',
    display_name: 'Nifty 50 Index',
  }

  // Mock silos with charts
  const silos = [
    {
      silo_id: '1',
      silo_name: 'Primary Analysis',
      charts: [
        { chart_id: '1', chart_name: 'RSI Momentum', direction: Direction.BULLISH, freshness: FreshnessStatus.CURRENT },
        { chart_id: '2', chart_name: 'MACD Trend', direction: Direction.BEARISH, freshness: FreshnessStatus.RECENT },
        { chart_id: '3', chart_name: 'Moving Averages', direction: Direction.BULLISH, freshness: FreshnessStatus.CURRENT },
      ]
    },
    {
      silo_id: '2', 
      silo_name: 'Secondary Analysis',
      charts: [
        { chart_id: '4', chart_name: 'Volume Profile', direction: Direction.NEUTRAL, freshness: FreshnessStatus.STALE },
        { chart_id: '5', chart_name: 'Bollinger Bands', direction: Direction.BEARISH, freshness: FreshnessStatus.CURRENT },
      ]
    }
  ]

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading instrument..." />
        </div>
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
        {silos.map((silo) => (
          <Card key={silo.silo_id} padding="lg">
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
            <GridLayout columns={3} gap="md">
              {silo.charts.map((chart) => (
                <Card 
                  key={chart.chart_id} 
                  variant="outlined"
                  className="hover:border-accent-primary/50 transition-colors"
                  interactive
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <LineChart className="h-5 w-5 text-slate-400" aria-hidden="true" />
                      <span className="font-medium">{chart.chart_name}</span>
                    </div>
                    <FreshnessMeter status={chart.freshness} showLabel={false} size="sm" />
                  </div>
                  
                  {/* CR-002: Direction displayed with equal prominence */}
                  <SignalBadge direction={chart.direction} size="md" />
                </Card>
              ))}
            </GridLayout>
          </Card>
        ))}
      </div>

      {silos.length === 0 && (
        <EmptyState
          title="No silos configured"
          description="Create a silo to organize your charts for this instrument."
          icon={LineChart}
        />
      )}
    </ContentArea>
  )
}

