import { Link } from 'react-router-dom'
import { useInstruments } from '@/hooks/useInstruments'
import { InstrumentCard } from '@/components/instruments/InstrumentCard'
import { Spinner } from '@/components/common/Spinner'
import { EmptyState } from '@/components/common/EmptyState'
import { PageHeader } from '@/components/layout/PageHeader'
import { Activity, AlertTriangle, FolderKanban } from 'lucide-react'

export function HomePage() {
  const { data: instruments, isLoading } = useInstruments({ active_only: true })

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Chart Intelligence Auditor & Signal Intelligence Engine"
      />

      {/* Constitutional Banner */}
      <div className="rounded-lg border-2 border-amber-500/30 bg-amber-500/5 p-6">
        <div className="mb-4 flex items-center gap-2 text-amber-400">
          <AlertTriangle className="h-5 w-5" />
          <span className="font-display font-semibold">Constitutional Principles</span>
        </div>
        <div className="grid gap-3 sm:grid-cols-3">
          <div className="flex items-start gap-3 rounded-lg bg-surface-secondary p-3">
            <div className="flex h-6 w-6 items-center justify-center rounded-full bg-amber-500/20 text-xs font-bold text-amber-400">
              1
            </div>
            <div className="text-sm text-slate-300">Decision-Support NOT Decision-Making</div>
          </div>
          <div className="flex items-start gap-3 rounded-lg bg-surface-secondary p-3">
            <div className="flex h-6 w-6 items-center justify-center rounded-full bg-amber-500/20 text-xs font-bold text-amber-400">
              2
            </div>
            <div className="text-sm text-slate-300">Expose Contradictions, NEVER Resolve Them</div>
          </div>
          <div className="flex items-start gap-3 rounded-lg bg-surface-secondary p-3">
            <div className="flex h-6 w-6 items-center justify-center rounded-full bg-amber-500/20 text-xs font-bold text-amber-400">
              3
            </div>
            <div className="text-sm text-slate-300">Descriptive AI, NOT Prescriptive AI</div>
          </div>
        </div>
      </div>

      {/* Instruments */}
      <div>
        <div className="mb-4 flex items-center gap-2">
          <Activity className="h-5 w-5 text-accent-primary" />
          <h2 className="font-display text-lg font-semibold">Instruments</h2>
        </div>

        {isLoading ? (
          <div className="flex h-64 items-center justify-center">
            <Spinner size="lg" />
          </div>
        ) : !instruments?.length ? (
          <EmptyState
            title="No Instruments"
            description="No active instruments found. Create one to get started."
            icon={<FolderKanban className="h-8 w-8 text-slate-400" />}
          />
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {instruments.map((instrument) => (
              <Link key={instrument.instrument_id} to={`/instruments/${instrument.instrument_id}`}>
                <InstrumentCard instrument={instrument} />
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

