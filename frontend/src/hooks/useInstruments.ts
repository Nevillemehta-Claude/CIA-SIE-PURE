/**
 * Instruments Hooks
 * 
 * React Query hooks for instrument data.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  getInstruments, 
  getInstrument, 
  createInstrument, 
  updateInstrument, 
  deleteInstrument 
} from '@services/api'
import type { 
  InstrumentCreateRequest, 
  InstrumentUpdateRequest,
  InstrumentListParams 
} from '@/types/index'

/** Query keys for instruments */
export const instrumentKeys = {
  all: ['instruments'] as const,
  lists: () => [...instrumentKeys.all, 'list'] as const,
  list: (params?: InstrumentListParams) => [...instrumentKeys.lists(), params] as const,
  details: () => [...instrumentKeys.all, 'detail'] as const,
  detail: (id: string) => [...instrumentKeys.details(), id] as const,
}

/**
 * Hook to fetch all instruments.
 */
export function useInstruments(params?: InstrumentListParams) {
  return useQuery({
    queryKey: instrumentKeys.list(params),
    queryFn: () => getInstruments(params),
  })
}

/**
 * Hook to fetch a single instrument.
 */
export function useInstrument(instrumentId: string) {
  return useQuery({
    queryKey: instrumentKeys.detail(instrumentId),
    queryFn: () => getInstrument(instrumentId),
    enabled: !!instrumentId,
  })
}

/**
 * Hook to create a new instrument.
 */
export function useCreateInstrument() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: InstrumentCreateRequest) => createInstrument(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: instrumentKeys.lists() })
    },
  })
}

/**
 * Hook to update an instrument.
 */
export function useUpdateInstrument(instrumentId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: InstrumentUpdateRequest) => updateInstrument(instrumentId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: instrumentKeys.detail(instrumentId) })
      queryClient.invalidateQueries({ queryKey: instrumentKeys.lists() })
    },
  })
}

/**
 * Hook to delete an instrument.
 */
export function useDeleteInstrument() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (instrumentId: string) => deleteInstrument(instrumentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: instrumentKeys.lists() })
    },
  })
}

