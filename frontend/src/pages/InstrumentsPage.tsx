/**
 * InstrumentsPage Component
 *
 * Lists all configured instruments.
 */

import { Link } from 'react-router-dom'
import { PageHeader, ContentArea, GridLayout } from '@components/layout'
import { Card, EmptyState, Badge, LoadingSpinner, ErrorMessage } from '@components/atoms'
import { LineChart, ChevronRight, Plus } from 'lucide-react'
import { useInstruments, useSilos, useCharts } from '@/hooks'
import { useMemo } from 'react'

/**
 * InstrumentsPage displays all configured instruments.
 */
export function InstrumentsPage() {
  // Fetch real data from API
  const { data: instruments, isLoading: instrumentsLoading, error: instrumentsError } = useInstruments()
  const { data: silos, isLoading: silosLoading } = useSilos()
  const { data: charts, isLoading: chartsLoading } = useCharts()

  const loading = instrumentsLoading || silosLoading || chartsLoading

  // Calculate silo and chart counts per instrument
  const instrumentStats = useMemo(() => {
    if (!instruments) return {}

    const stats: Record<string, { siloCount: number; chartCount: number }> = {}

    instruments.forEach(instrument => {
      const instrumentSilos = silos?.filter(s => s.instrument_id === instrument.instrument_id) ?? []
      const siloIds = instrumentSilos.map(s => s.silo_id)
      const instrumentCharts = charts?.filter(c => siloIds.includes(c.silo_id)) ?? []

      stats[instrument.instrument_id] = {
        siloCount: instrumentSilos.length,
        chartCount: instrumentCharts.length,
      }
    })

    return stats
  }, [instruments, silos, charts])

  if (loading) {
    return (
      <ContentArea>
        <div className="flex items-center justify-center min-h-[400px]">
          <LoadingSpinner size="lg" label="Loading instruments..." />
        </div>
      </ContentArea>
    )
  }

  if (instrumentsError) {
    return (
      <ContentArea>
        <PageHeader title="Instruments" />
        <ErrorMessage
          title="Failed to load instruments"
          message={instrumentsError instanceof Error ? instrumentsError.message : 'An error occurred'}
          onRetry={() => window.location.reload()}
        />
      </ContentArea>
    )
  }

  if (!instruments || instruments.length === 0) {
    return (
      <ContentArea>
        <PageHeader title="Instruments" />
        <EmptyState
          title="No instruments configured"
          description="Add your first instrument to start receiving signals."
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
        title="Instruments"
        description="Manage your configured trading instruments"
        actions={
          <button className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-primary hover:bg-accent-primary/90 text-white text-sm font-medium transition-colors">
            <Plus className="h-4 w-4" aria-hidden="true" />
            Add Instrument
          </button>
        }
      />

      <GridLayout columns={3} gap="md">
        {instruments.map((instrument) => {
          const stats = instrumentStats[instrument.instrument_id] ?? { siloCount: 0, chartCount: 0 }

          return (
            <Link
              key={instrument.instrument_id}
              to={`/instruments/${instrument.instrument_id}`}
            >
              <Card
                interactive
                className="h-full hover:border-accent-primary/50 transition-colors"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-accent-primary/20">
                      <LineChart className="h-5 w-5 text-accent-primary" aria-hidden="true" />
                    </div>
                    <div>
                      <h3 className="font-display font-semibold">{instrument.symbol}</h3>
                      <p className="text-sm text-slate-400">{instrument.display_name}</p>
                    </div>
                  </div>
                  <Badge variant={instrument.is_active ? 'success' : 'default'}>
                    {instrument.is_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>

                <div className="flex items-center justify-between text-sm text-slate-400">
                  <span>{stats.siloCount} silos · {stats.chartCount} charts</span>
                  <ChevronRight className="h-4 w-4" aria-hidden="true" />
                </div>
              </Card>
            </Link>
          )
        })}
      </GridLayout>
    </ContentArea>
  )
}
