import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getInstruments, getInstrument } from '@/services/instruments'
import type { InstrumentListParams } from '@/types/api'

export function useInstruments(params?: InstrumentListParams) {
  return useQuery({
    queryKey: queryKeys.instruments.list(params),
    queryFn: () => getInstruments(params),
  })
}

export function useInstrument(id: string) {
  return useQuery({
    queryKey: queryKeys.instruments.detail(id),
    queryFn: () => getInstrument(id),
    enabled: !!id,
  })
}

