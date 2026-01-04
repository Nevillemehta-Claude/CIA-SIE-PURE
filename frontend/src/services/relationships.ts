import { apiClient, apiRequest } from './client'
import type { RelationshipResponse, ContradictionsResponse } from '@/types/api'

const PATH = '/relationships'

export async function getRelationships(siloId: string): Promise<RelationshipResponse> {
  return apiRequest(apiClient.get(`${PATH}/silo/${siloId}`))
}

export async function getContradictions(siloId: string): Promise<ContradictionsResponse> {
  return apiRequest(apiClient.get(`${PATH}/contradictions/silo/${siloId}`))
}

export async function getInstrumentRelationships(
  instrumentId: string
): Promise<RelationshipResponse> {
  return apiRequest(apiClient.get(`${PATH}/instrument/${instrumentId}`))
}

