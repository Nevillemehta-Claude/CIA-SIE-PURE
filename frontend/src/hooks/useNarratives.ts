/**
 * Narratives Hooks
 * 
 * React Query hooks for AI-generated narrative content.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-001: Responses include mandatory disclaimer
 * - CR-003: Content is validated as descriptive only
 */

import { useQuery } from '@tanstack/react-query'
import { 
  getSiloNarrative, 
  getSiloNarrativePlain,
  getChartNarrative 
} from '@services/api'
import type { NarrativeParams } from '@/types/index'

/** Query keys for narratives */
export const narrativeKeys = {
  all: ['narratives'] as const,
  silos: () => [...narrativeKeys.all, 'silo'] as const,
  silo: (siloId: string, params?: NarrativeParams) => 
    [...narrativeKeys.silos(), siloId, params] as const,
  siloPlain: (siloId: string) => [...narrativeKeys.silos(), siloId, 'plain'] as const,
  charts: () => [...narrativeKeys.all, 'chart'] as const,
  chart: (chartId: string, params?: NarrativeParams) => 
    [...narrativeKeys.charts(), chartId, params] as const,
}

/**
 * Hook to fetch narrative for a silo.
 * 
 * CR-001 COMPLIANCE: Response includes closing_statement (disclaimer).
 * Components using this hook MUST display the disclaimer.
 */
export function useSiloNarrative(siloId: string, params?: NarrativeParams) {
  return useQuery({
    queryKey: narrativeKeys.silo(siloId, params),
    queryFn: () => getSiloNarrative(siloId, params),
    enabled: !!siloId,
    // Don't auto-refresh narratives (expensive AI calls)
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

/**
 * Hook to fetch plain text narrative for a silo.
 */
export function useSiloNarrativePlain(siloId: string) {
  return useQuery({
    queryKey: narrativeKeys.siloPlain(siloId),
    queryFn: () => getSiloNarrativePlain(siloId),
    enabled: !!siloId,
    staleTime: 5 * 60 * 1000,
  })
}

/**
 * Hook to fetch narrative for a chart.
 * 
 * CR-001 COMPLIANCE: Response includes closing_statement (disclaimer).
 */
export function useChartNarrative(chartId: string, params?: NarrativeParams) {
  return useQuery({
    queryKey: narrativeKeys.chart(chartId, params),
    queryFn: () => getChartNarrative(chartId, params),
    enabled: !!chartId,
    staleTime: 5 * 60 * 1000,
  })
}

