import { apiClient, apiRequest } from './client'
import type { NarrativeResponse, PlainNarrativeResponse } from '@/types/api'

const PATH = '/narratives'

export async function getNarrative(siloId: string): Promise<NarrativeResponse> {
  return apiRequest(apiClient.get(`${PATH}/silo/${siloId}`))
}

export async function getPlainNarrative(siloId: string): Promise<PlainNarrativeResponse> {
  return apiRequest(apiClient.get(`${PATH}/silo/${siloId}/plain`))
}

