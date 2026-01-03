/**
 * Charts Hooks
 *
 * React Query hooks for chart data.
 *
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: Charts returned without ranking or weighting
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getCharts,
  getChartsBySilo,
  getChart,
  createChart,
  updateChart,
  deleteChart
} from '@services/api'
import type {
  ChartCreateRequest,
  ChartUpdateRequest,
  ChartListParams
} from '@/types/index'

/** Query keys for charts */
export const chartKeys = {
  all: ['charts'] as const,
  lists: () => [...chartKeys.all, 'list'] as const,
  list: (params?: ChartListParams) => [...chartKeys.lists(), params] as const,
  bySilo: (siloId: string) => [...chartKeys.lists(), 'silo', siloId] as const,
  details: () => [...chartKeys.all, 'detail'] as const,
  detail: (id: string) => [...chartKeys.details(), id] as const,
}

/**
 * Hook to fetch all charts.
 */
export function useCharts(params?: ChartListParams) {
  return useQuery({
    queryKey: chartKeys.list(params),
    queryFn: () => getCharts(params),
  })
}

/**
 * Hook to fetch charts for a specific silo.
 */
export function useChartsBySilo(siloId: string) {
  return useQuery({
    queryKey: chartKeys.bySilo(siloId),
    queryFn: () => getChartsBySilo(siloId),
    enabled: !!siloId,
  })
}

/**
 * Hook to fetch a single chart.
 */
export function useChart(chartId: string) {
  return useQuery({
    queryKey: chartKeys.detail(chartId),
    queryFn: () => getChart(chartId),
    enabled: !!chartId,
  })
}

/**
 * Hook to create a new chart.
 */
export function useCreateChart() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ChartCreateRequest) => createChart(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: chartKeys.lists() })
      queryClient.invalidateQueries({
        queryKey: chartKeys.bySilo(variables.silo_id)
      })
    },
  })
}

/**
 * Hook to update a chart.
 */
export function useUpdateChart(chartId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ChartUpdateRequest) => updateChart(chartId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chartKeys.detail(chartId) })
      queryClient.invalidateQueries({ queryKey: chartKeys.lists() })
    },
  })
}

/**
 * Hook to delete a chart.
 */
export function useDeleteChart() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (chartId: string) => deleteChart(chartId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chartKeys.lists() })
    },
  })
}
