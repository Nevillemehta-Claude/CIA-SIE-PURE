import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getNarrative } from '@/services/narratives'

export function useNarrative(siloId: string) {
  return useQuery({
    queryKey: queryKeys.narratives.bySilo(siloId),
    queryFn: () => getNarrative(siloId),
    enabled: !!siloId,
    staleTime: 60 * 1000, // 1 minute
  })
}

