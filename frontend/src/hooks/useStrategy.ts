import { useMutation } from '@tanstack/react-query'
import { evaluateStrategy, type StrategyEvaluationRequest } from '@/services/strategy'

export function useEvaluateStrategy() {
  return useMutation({
    mutationFn: (data: StrategyEvaluationRequest) => evaluateStrategy(data),
  })
}

