/**
 * Silos API Service
 * 
 * API calls for silo management.
 */

import { apiClient, apiRequest } from './client'
import type { 
  Silo, 
  SiloCreateRequest,
  SiloListParams 
} from '@/types/index'

const BASE_PATH = '/silos'

/**
 * Get all silos.
 */
export async function getSilos(
  params?: SiloListParams
): Promise<Silo[]> {
  return apiRequest(apiClient.get(BASE_PATH, { params }))
}

/**
 * Get silos for a specific instrument.
 */
export async function getSilosByInstrument(
  instrumentId: string
): Promise<Silo[]> {
  return apiRequest(apiClient.get(BASE_PATH, { 
    params: { instrument_id: instrumentId } 
  }))
}

/**
 * Get a single silo by ID.
 */
export async function getSilo(
  siloId: string
): Promise<Silo> {
  return apiRequest(apiClient.get(`${BASE_PATH}/${siloId}`))
}

/**
 * Create a new silo.
 */
export async function createSilo(
  data: SiloCreateRequest
): Promise<Silo> {
  return apiRequest(apiClient.post(BASE_PATH, data))
}

/**
 * Delete a silo.
 */
export async function deleteSilo(
  siloId: string
): Promise<void> {
  await apiClient.delete(`${BASE_PATH}/${siloId}`)
}

