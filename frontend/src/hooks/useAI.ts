import { useQuery } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { getModels, getBudget, getUsage } from '@/services/ai'

export function useModels() {
  return useQuery({
    queryKey: queryKeys.ai.models,
    queryFn: getModels,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useBudget() {
  return useQuery({
    queryKey: queryKeys.ai.budget,
    queryFn: getBudget,
    refetchInterval: 60 * 1000, // Refetch every minute
  })
}

export function useUsage(period?: 'daily' | 'weekly' | 'monthly') {
  return useQuery({
    queryKey: queryKeys.ai.usage(period),
    queryFn: () => getUsage({ period }),
  })
}

