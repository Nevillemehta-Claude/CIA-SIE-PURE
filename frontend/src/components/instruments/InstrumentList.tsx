import { Link } from 'react-router-dom'
import { InstrumentCard } from './InstrumentCard'
import { EmptyState } from '@/components/common/EmptyState'
import { Spinner } from '@/components/common/Spinner'
import type { Instrument } from '@/types/models'
import { Activity } from 'lucide-react'

interface InstrumentListProps {
  instruments: Instrument[]
  isLoading?: boolean
}

export function InstrumentList({ instruments, isLoading }: InstrumentListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner size="lg" />
      </div>
    )
  }

  if (instruments.length === 0) {
    return (
      <EmptyState
        title="No Instruments"
        description="No instruments found. Create one to get started."
        icon={<Activity className="h-8 w-8 text-slate-400" />}
      />
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {instruments.map((instrument) => (
        <Link key={instrument.instrument_id} to={`/instruments/${instrument.instrument_id}`}>
          <InstrumentCard instrument={instrument} />
        </Link>
      ))}
    </div>
  )
}

