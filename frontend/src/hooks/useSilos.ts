/**
 * Silos Hooks
 * 
 * React Query hooks for silo data.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  getSilos, 
  getSilosByInstrument, 
  getSilo, 
  createSilo, 
  deleteSilo 
} from '@services/api'
import type { SiloCreateRequest, SiloListParams } from '@/types/index'

/** Query keys for silos */
export const siloKeys = {
  all: ['silos'] as const,
  lists: () => [...siloKeys.all, 'list'] as const,
  list: (params?: SiloListParams) => [...siloKeys.lists(), params] as const,
  byInstrument: (instrumentId: string) => [...siloKeys.lists(), 'instrument', instrumentId] as const,
  details: () => [...siloKeys.all, 'detail'] as const,
  detail: (id: string) => [...siloKeys.details(), id] as const,
}

/**
 * Hook to fetch all silos.
 */
export function useSilos(params?: SiloListParams) {
  return useQuery({
    queryKey: siloKeys.list(params),
    queryFn: () => getSilos(params),
  })
}

/**
 * Hook to fetch silos for an instrument.
 */
export function useSilosByInstrument(instrumentId: string) {
  return useQuery({
    queryKey: siloKeys.byInstrument(instrumentId),
    queryFn: () => getSilosByInstrument(instrumentId),
    enabled: !!instrumentId,
  })
}

/**
 * Hook to fetch a single silo.
 */
export function useSilo(siloId: string) {
  return useQuery({
    queryKey: siloKeys.detail(siloId),
    queryFn: () => getSilo(siloId),
    enabled: !!siloId,
  })
}

/**
 * Hook to create a new silo.
 */
export function useCreateSilo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: SiloCreateRequest) => createSilo(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: siloKeys.lists() })
      queryClient.invalidateQueries({ 
        queryKey: siloKeys.byInstrument(variables.instrument_id) 
      })
    },
  })
}

/**
 * Hook to delete a silo.
 */
export function useDeleteSilo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (siloId: string) => deleteSilo(siloId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: siloKeys.lists() })
    },
  })
}

