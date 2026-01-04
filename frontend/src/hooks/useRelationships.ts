import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getRelationships, getInstrumentRelationships } from '@/services/relationships'

export function useRelationships(siloId: string) {
  return useQuery({
    queryKey: queryKeys.relationships.bySilo(siloId),
    queryFn: () => getRelationships(siloId),
    enabled: !!siloId,
  })
}

export function useInstrumentRelationships(instrumentId: string) {
  return useQuery({
    queryKey: queryKeys.relationships.byInstrument(instrumentId),
    queryFn: () => getInstrumentRelationships(instrumentId),
    enabled: !!instrumentId,
  })
}

