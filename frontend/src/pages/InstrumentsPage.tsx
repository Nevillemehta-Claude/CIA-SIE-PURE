import { useInstruments } from '@/hooks/useInstruments'
import { InstrumentList } from '@/components/instruments/InstrumentList'
import { PageHeader } from '@/components/layout/PageHeader'

export function InstrumentsPage() {
  const { data: instruments, isLoading } = useInstruments()

  return (
    <div className="space-y-6">
      <PageHeader
        title="Instruments"
        description="All trading instruments in the system"
      />

      <InstrumentList instruments={instruments ?? []} isLoading={isLoading} />
    </div>
  )
}

