/**
 * Signals Hooks
 *
 * React Query hooks for signal data.
 *
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: Signals returned as-is without ranking or scoring
 * - CR-003: No interpretation applied to signal data
 */

import { useQuery } from '@tanstack/react-query'
import { getSignalsByChart, getLatestSignal } from '@services/api'
import type { SignalListParams } from '@/types/index'

/** Query keys for signals */
export const signalKeys = {
  all: ['signals'] as const,
  byChart: (chartId: string) => [...signalKeys.all, 'chart', chartId] as const,
  byChartWithParams: (chartId: string, params?: SignalListParams) =>
    [...signalKeys.byChart(chartId), params] as const,
  latest: (chartId: string) => [...signalKeys.byChart(chartId), 'latest'] as const,
}

/**
 * Hook to fetch signals for a chart.
 *
 * CR-002 COMPLIANCE: Returns ALL signals without filtering or ranking.
 */
export function useSignalsByChart(chartId: string, params?: SignalListParams) {
  return useQuery({
    queryKey: signalKeys.byChartWithParams(chartId, params),
    queryFn: () => getSignalsByChart(chartId, params),
    enabled: !!chartId,
    // Refresh every 30 seconds to catch new signals
    refetchInterval: 30000,
  })
}

/**
 * Hook to fetch the latest signal for a chart.
 */
export function useLatestSignal(chartId: string) {
  return useQuery({
    queryKey: signalKeys.latest(chartId),
    queryFn: () => getLatestSignal(chartId),
    enabled: !!chartId,
    refetchInterval: 30000,
  })
}
