import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getBaskets,
  getBasket,
  createBasket,
  addChartToBasket,
  removeChartFromBasket,
  deleteBasket,
  type CreateBasketRequest,
} from '@/services/baskets'

const queryKeys = {
  all: ['baskets'] as const,
  list: () => [...queryKeys.all, 'list'] as const,
  detail: (id: string) => [...queryKeys.all, 'detail', id] as const,
}

export function useBaskets() {
  return useQuery({
    queryKey: queryKeys.list(),
    queryFn: getBaskets,
  })
}

export function useBasket(id: string) {
  return useQuery({
    queryKey: queryKeys.detail(id),
    queryFn: () => getBasket(id),
    enabled: !!id,
  })
}

export function useCreateBasket() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CreateBasketRequest) => createBasket(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.all })
    },
  })
}

export function useAddChartToBasket() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ basketId, chartId }: { basketId: string; chartId: string }) =>
      addChartToBasket(basketId, chartId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.all })
    },
  })
}

export function useRemoveChartFromBasket() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ basketId, chartId }: { basketId: string; chartId: string }) =>
      removeChartFromBasket(basketId, chartId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.all })
    },
  })
}

export function useDeleteBasket() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => deleteBasket(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.all })
    },
  })
}

