/**
 * InstrumentCard Component
 * 
 * Displays an instrument with summary info.
 */

import { Link } from 'react-router-dom'
import { LineChart, ChevronRight } from 'lucide-react'
import { Card, Badge } from '@components/atoms'
import type { Instrument } from '@/types/index'

interface InstrumentCardProps {
  /** Instrument data */
  instrument: Instrument
  /** Silo count */
  siloCount?: number
  /** Chart count */
  chartCount?: number
}

/**
 * InstrumentCard displays a summary of an instrument.
 */
export function InstrumentCard({ 
  instrument,
  siloCount = 0,
  chartCount = 0 
}: InstrumentCardProps) {
  return (
    <Link to={`/instruments/${instrument.instrument_id}`}>
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
          <span>{siloCount} silos · {chartCount} charts</span>
          <ChevronRight className="h-4 w-4" aria-hidden="true" />
        </div>
      </Card>
    </Link>
  )
}

