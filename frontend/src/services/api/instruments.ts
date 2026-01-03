/**
 * Instruments API Service
 * 
 * API calls for instrument management.
 */

import { apiClient, apiRequest } from './client'
import type { 
  Instrument, 
  InstrumentCreateRequest, 
  InstrumentUpdateRequest,
  InstrumentListParams 
} from '@/types/index'

const BASE_PATH = '/instruments'

/**
 * Get all instruments.
 */
export async function getInstruments(
  params?: InstrumentListParams
): Promise<Instrument[]> {
  return apiRequest(apiClient.get(BASE_PATH, { params }))
}

/**
 * Get a single instrument by ID.
 */
export async function getInstrument(
  instrumentId: string
): Promise<Instrument> {
  return apiRequest(apiClient.get(`${BASE_PATH}/${instrumentId}`))
}

/**
 * Create a new instrument.
 */
export async function createInstrument(
  data: InstrumentCreateRequest
): Promise<Instrument> {
  return apiRequest(apiClient.post(BASE_PATH, data))
}

/**
 * Update an instrument.
 */
export async function updateInstrument(
  instrumentId: string,
  data: InstrumentUpdateRequest
): Promise<Instrument> {
  return apiRequest(apiClient.patch(`${BASE_PATH}/${instrumentId}`, data))
}

/**
 * Delete an instrument.
 */
export async function deleteInstrument(
  instrumentId: string
): Promise<void> {
  await apiClient.delete(`${BASE_PATH}/${instrumentId}`)
}

