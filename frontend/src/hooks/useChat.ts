import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/queryKeys'
import { sendMessage, getHistory } from '@/services/chat'

export function useHistory(scripId: string) {
  return useQuery({
    queryKey: queryKeys.chat.history(scripId),
    queryFn: () => getHistory(scripId),
    enabled: !!scripId,
  })
}

export function useSendMessage(scripId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ message, model }: { message: string; model?: string }) =>
      sendMessage(scripId, message, model),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.chat.history(scripId) })
      queryClient.invalidateQueries({ queryKey: queryKeys.ai.budget })
    },
  })
}

