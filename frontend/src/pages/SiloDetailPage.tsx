import { useParams } from 'react-router-dom'
import { useSilo } from '@/hooks/useSilos'
import { useCharts } from '@/hooks/useCharts'
import { useRelationships } from '@/hooks/useRelationships'
import { useNarrative } from '@/hooks/useNarratives'
import { ChartList } from '@/components/charts/ChartList'
import { ContradictionPanel } from '@/components/relationships/ContradictionPanel'
import { ConfirmationPanel } from '@/components/relationships/ConfirmationPanel'
import { NarrativeDisplay } from '@/components/narratives/NarrativeDisplay'
import { PageHeader } from '@/components/layout/PageHeader'
import { Spinner } from '@/components/common/Spinner'
import { ErrorState } from '@/components/common/ErrorState'

export function SiloDetailPage() {
  const { siloId } = useParams<{ siloId: string }>()
  const { data: silo, isLoading: siloLoading, error: siloError } = useSilo(siloId!)
  const { data: charts, isLoading: chartsLoading } = useCharts(siloId)
  const { data: relationships } = useRelationships(siloId!)
  const { data: narrative, isLoading: narrLoading } = useNarrative(siloId!)

  if (siloLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  if (siloError || !silo) {
    return (
      <ErrorState
        title="Silo Not Found"
        message="The requested silo could not be found."
      />
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        title={silo.silo_name}
        description="Analysis container"
        backTo={`/instruments/${silo.instrument_id}`}
      />

      {/* Charts Section */}
      <section>
        <h2 className="mb-4 font-display text-lg font-semibold">Charts</h2>
        <ChartList charts={charts ?? []} isLoading={chartsLoading} />
      </section>

      {/* CONSTITUTIONAL: Contradictions shown with EQUAL prominence */}
      <section>
        <ContradictionPanel
          contradictions={relationships?.contradictions ?? []}
        />
      </section>

      {/* Confirmations Section */}
      <section>
        <ConfirmationPanel
          confirmations={relationships?.confirmations ?? []}
        />
      </section>

      {/* CONSTITUTIONAL: Narrative with MANDATORY disclaimer */}
      <section>
        <NarrativeDisplay
          narrative={narrative}
          isLoading={narrLoading}
        />
      </section>
    </div>
  )
}

