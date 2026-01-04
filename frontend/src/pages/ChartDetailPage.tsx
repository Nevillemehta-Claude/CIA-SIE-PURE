import { useParams } from 'react-router-dom'
import { useChart } from '@/hooks/useCharts'
import { useSignals } from '@/hooks/useSignals'
import { SignalList } from '@/components/signals/SignalList'
import { PageHeader } from '@/components/layout/PageHeader'
import { Spinner } from '@/components/common/Spinner'
import { ErrorState } from '@/components/common/ErrorState'
import { Badge } from '@/components/common/Badge'
import { Card } from '@/components/common/Card'

export function ChartDetailPage() {
  const { chartId } = useParams<{ chartId: string }>()
  const { data: chart, isLoading: chartLoading, error: chartError } = useChart(chartId!)
  const { data: signals, isLoading: signalsLoading } = useSignals(chartId!, 20)

  if (chartLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  if (chartError || !chart) {
    return (
      <ErrorState
        title="Chart Not Found"
        message="The requested chart could not be found."
      />
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        title={`${chart.chart_code} - ${chart.chart_name}`}
        description={`Timeframe: ${chart.timeframe}`}
        backTo={`/silos/${chart.silo_id}`}
      />

      {/* Chart Info */}
      <Card>
        <div className="grid gap-4 sm:grid-cols-3">
          <div>
            <div className="text-sm text-slate-400">Chart Code</div>
            <div className="font-display text-lg font-semibold text-accent-primary">
              {chart.chart_code}
            </div>
          </div>
          <div>
            <div className="text-sm text-slate-400">Timeframe</div>
            <Badge>{chart.timeframe}</Badge>
          </div>
          <div>
            <div className="text-sm text-slate-400">Webhook ID</div>
            <code className="text-sm text-slate-300">{chart.webhook_id}</code>
          </div>
        </div>
      </Card>

      {/* Signal History */}
      <section>
        <h2 className="mb-4 font-display text-lg font-semibold">Signal History</h2>
        <SignalList signals={signals ?? []} isLoading={signalsLoading} />
      </section>
    </div>
  )
}

