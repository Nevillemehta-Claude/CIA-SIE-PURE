import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getCharts, getChart } from '@/services/charts'

export function useCharts(siloId?: string) {
  return useQuery({
    queryKey: queryKeys.charts.list(siloId),
    queryFn: () => getCharts({ silo_id: siloId }),
    enabled: !!siloId,
  })
}

export function useChart(id: string) {
  return useQuery({
    queryKey: queryKeys.charts.detail(id),
    queryFn: () => getChart(id),
    enabled: !!id,
  })
}

