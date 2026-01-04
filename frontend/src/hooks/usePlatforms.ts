import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getPlatforms,
  getPlatform,
  connectPlatform,
  disconnectPlatform,
  getPlatformHealth,
  getSetupInstructions,
  type PlatformConnectRequest,
} from '@/services/platforms'

const queryKeys = {
  all: ['platforms'] as const,
  list: () => [...queryKeys.all, 'list'] as const,
  detail: (name: string) => [...queryKeys.all, 'detail', name] as const,
  health: (name: string) => [...queryKeys.all, 'health', name] as const,
  setup: (name: string) => [...queryKeys.all, 'setup', name] as const,
}

export function usePlatforms() {
  return useQuery({
    queryKey: queryKeys.list(),
    queryFn: getPlatforms,
  })
}

export function usePlatform(name: string) {
  return useQuery({
    queryKey: queryKeys.detail(name),
    queryFn: () => getPlatform(name),
    enabled: !!name,
  })
}

export function usePlatformHealth(name: string) {
  return useQuery({
    queryKey: queryKeys.health(name),
    queryFn: () => getPlatformHealth(name),
    enabled: !!name,
    refetchInterval: 30000, // Refresh every 30 seconds
  })
}

export function useSetupInstructions(name: string) {
  return useQuery({
    queryKey: queryKeys.setup(name),
    queryFn: () => getSetupInstructions(name),
    enabled: !!name,
  })
}

export function useConnectPlatform() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: PlatformConnectRequest) => connectPlatform(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.all })
    },
  })
}

export function useDisconnectPlatform() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (name: string) => disconnectPlatform(name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.all })
    },
  })
}

