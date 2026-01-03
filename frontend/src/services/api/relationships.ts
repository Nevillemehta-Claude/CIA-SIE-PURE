/**
 * Relationships API Service
 * 
 * API calls for relationship summaries, contradictions, and confirmations.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - These endpoints return ALL relationships
 * - No filtering, resolution, or ranking is performed
 */

import { apiClient, apiRequest } from './client'
import type { 
  RelationshipSummary, 
  ContradictionsResponse 
} from '@/types/index'

/**
 * Get relationship summary for a silo.
 * 
 * CR-002 COMPLIANCE: Returns ALL contradictions and confirmations.
 * The backend does not resolve or rank relationships.
 */
export async function getRelationshipSummary(
  siloId: string
): Promise<RelationshipSummary> {
  return apiRequest(
    apiClient.get(`/silos/${siloId}/relationships`)
  )
}

/**
 * Get contradictions for a silo.
 * 
 * CR-002 COMPLIANCE: Returns ALL contradictions without resolution.
 */
export async function getContradictions(
  siloId: string
): Promise<ContradictionsResponse> {
  return apiRequest(
    apiClient.get(`/silos/${siloId}/contradictions`)
  )
}

/**
 * Get relationship summary for an instrument (across all silos).
 */
export async function getInstrumentRelationships(
  instrumentId: string
): Promise<RelationshipSummary[]> {
  return apiRequest(
    apiClient.get(`/instruments/${instrumentId}/relationships`)
  )
}

