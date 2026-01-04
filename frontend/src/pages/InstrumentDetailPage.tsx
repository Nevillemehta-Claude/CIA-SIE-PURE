import { useParams } from 'react-router-dom'
import { useInstrument } from '@/hooks/useInstruments'
import { useSilos } from '@/hooks/useSilos'
import { SiloList } from '@/components/silos/SiloList'
import { PageHeader } from '@/components/layout/PageHeader'
import { Spinner } from '@/components/common/Spinner'
import { ErrorState } from '@/components/common/ErrorState'

export function InstrumentDetailPage() {
  const { instrumentId } = useParams<{ instrumentId: string }>()
  const { data: instrument, isLoading: instrumentLoading, error: instrumentError } = useInstrument(instrumentId!)
  const { data: silos, isLoading: silosLoading } = useSilos(instrumentId)

  if (instrumentLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  if (instrumentError || !instrument) {
    return (
      <ErrorState
        title="Instrument Not Found"
        message="The requested instrument could not be found."
      />
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        title={instrument.display_name}
        description={`Symbol: ${instrument.symbol}`}
        backTo="/instruments"
      />

      <section>
        <h2 className="mb-4 font-display text-lg font-semibold">Silos</h2>
        <SiloList silos={silos ?? []} isLoading={silosLoading} />
      </section>
    </div>
  )
}

