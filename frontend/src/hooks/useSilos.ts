import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getSilos, getSilo } from '@/services/silos'

export function useSilos(instrumentId?: string) {
  return useQuery({
    queryKey: queryKeys.silos.list(instrumentId),
    queryFn: () => getSilos({ instrument_id: instrumentId }),
    enabled: !!instrumentId,
  })
}

export function useSilo(id: string) {
  return useQuery({
    queryKey: queryKeys.silos.detail(id),
    queryFn: () => getSilo(id),
    enabled: !!id,
  })
}

