import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getSignalsByChart, getLatestSignal } from '@/services/signals'

export function useSignals(chartId: string, limit?: number) {
  return useQuery({
    queryKey: queryKeys.signals.byChart(chartId),
    queryFn: () => getSignalsByChart(chartId, { limit }),
    enabled: !!chartId,
  })
}

export function useLatestSignal(chartId: string) {
  return useQuery({
    queryKey: queryKeys.signals.latest(chartId),
    queryFn: () => getLatestSignal(chartId),
    enabled: !!chartId,
    staleTime: 30 * 1000, // 30 seconds
  })
}

