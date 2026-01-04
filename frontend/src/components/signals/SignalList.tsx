import { SignalCard } from './SignalCard'
import { EmptyState } from '@/components/common/EmptyState'
import { Spinner } from '@/components/common/Spinner'
import type { Signal } from '@/types/models'
import { Radio } from 'lucide-react'

interface SignalListProps {
  signals: Signal[]
  isLoading?: boolean
}

export function SignalList({ signals, isLoading }: SignalListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner size="lg" />
      </div>
    )
  }

  if (signals.length === 0) {
    return (
      <EmptyState
        title="No Signals"
        description="No signals have been received for this chart yet."
        icon={<Radio className="h-8 w-8 text-slate-400" />}
      />
    )
  }

  return (
    <div className="space-y-4">
      {signals.map((signal) => (
        <SignalCard key={signal.signal_id} signal={signal} />
      ))}
    </div>
  )
}

