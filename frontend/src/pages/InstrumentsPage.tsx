/**
 * InstrumentsPage Component
 * 
 * Lists all configured instruments.
 */

import { Link } from 'react-router-dom'
import { PageHeader, ContentArea, GridLayout } from '@components/layout'
import { Card, EmptyState, Badge } from '@components/atoms'
import { LineChart, ChevronRight, Plus } from 'lucide-react'

/**
 * InstrumentsPage displays all configured instruments.
 */
export function InstrumentsPage() {
  // Placeholder data
  const instruments = [
    {
      instrument_id: '1',
      symbol: 'NIFTY',
      display_name: 'Nifty 50 Index',
      silo_count: 2,
      chart_count: 12,
      is_active: true,
    },
    {
      instrument_id: '2',
      symbol: 'BANKNIFTY',
      display_name: 'Bank Nifty Index',
      silo_count: 1,
      chart_count: 8,
      is_active: true,
    },
    {
      instrument_id: '3',
      symbol: 'RELIANCE',
      display_name: 'Reliance Industries',
      silo_count: 1,
      chart_count: 6,
      is_active: false,
    },
  ]

  if (instruments.length === 0) {
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
        {instruments.map((instrument) => (
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
                <span>{instrument.silo_count} silos · {instrument.chart_count} charts</span>
                <ChevronRight className="h-4 w-4" aria-hidden="true" />
              </div>
            </Card>
          </Link>
        ))}
      </GridLayout>
    </ContentArea>
  )
}

