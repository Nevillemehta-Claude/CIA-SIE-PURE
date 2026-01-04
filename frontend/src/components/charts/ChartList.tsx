import { Link } from 'react-router-dom'
import { ChartCard } from './ChartCard'
import { EmptyState } from '@/components/common/EmptyState'
import { Spinner } from '@/components/common/Spinner'
import type { Chart } from '@/types/models'
import { BarChart3 } from 'lucide-react'

interface ChartListProps {
  charts: Chart[]
  isLoading?: boolean
}

export function ChartList({ charts, isLoading }: ChartListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner size="lg" />
      </div>
    )
  }

  if (charts.length === 0) {
    return (
      <EmptyState
        title="No Charts"
        description="No charts found for this silo."
        icon={<BarChart3 className="h-8 w-8 text-slate-400" />}
      />
    )
  }

  // CONSTITUTIONAL: All charts displayed with EQUAL visual prominence
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {charts.map((chart) => (
        <Link key={chart.chart_id} to={`/charts/${chart.chart_id}`}>
          <ChartCard chart={chart} />
        </Link>
      ))}
    </div>
  )
}

