/**
 * Relationships Hooks
 * 
 * React Query hooks for relationship data.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-002: Data returned as-is without resolution or ranking
 */

import { useQuery } from '@tanstack/react-query'
import { 
  getRelationshipSummary, 
  getContradictions,
  getInstrumentRelationships 
} from '@services/api'

/** Query keys for relationships */
export const relationshipKeys = {
  all: ['relationships'] as const,
  summaries: () => [...relationshipKeys.all, 'summary'] as const,
  summary: (siloId: string) => [...relationshipKeys.summaries(), siloId] as const,
  contradictions: () => [...relationshipKeys.all, 'contradictions'] as const,
  contradiction: (siloId: string) => [...relationshipKeys.contradictions(), siloId] as const,
  byInstrument: (instrumentId: string) => [...relationshipKeys.all, 'instrument', instrumentId] as const,
}

/**
 * Hook to fetch relationship summary for a silo.
 * 
 * CR-002 COMPLIANCE: Returns ALL relationships without filtering or ranking.
 */
export function useRelationshipSummary(siloId: string) {
  return useQuery({
    queryKey: relationshipKeys.summary(siloId),
    queryFn: () => getRelationshipSummary(siloId),
    enabled: !!siloId,
    // Refresh every 30 seconds to catch new signals
    refetchInterval: 30000,
  })
}

/**
 * Hook to fetch contradictions for a silo.
 * 
 * CR-002 COMPLIANCE: Returns ALL contradictions without resolution.
 */
export function useContradictions(siloId: string) {
  return useQuery({
    queryKey: relationshipKeys.contradiction(siloId),
    queryFn: () => getContradictions(siloId),
    enabled: !!siloId,
    refetchInterval: 30000,
  })
}

/**
 * Hook to fetch relationship summaries for an instrument.
 */
export function useInstrumentRelationships(instrumentId: string) {
  return useQuery({
    queryKey: relationshipKeys.byInstrument(instrumentId),
    queryFn: () => getInstrumentRelationships(instrumentId),
    enabled: !!instrumentId,
    refetchInterval: 30000,
  })
}

