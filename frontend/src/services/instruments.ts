import { apiClient, apiRequest } from './client'
import type { Instrument } from '@/types/models'
import type { InstrumentListParams } from '@/types/api'

const PATH = '/instruments'

export async function getInstruments(params?: InstrumentListParams): Promise<Instrument[]> {
  return apiRequest(apiClient.get(`${PATH}/`, { params }))
}

export async function getInstrument(id: string): Promise<Instrument> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}

export async function getInstrumentBySymbol(symbol: string): Promise<Instrument> {
  return apiRequest(apiClient.get(`${PATH}/symbol/${symbol}`))
}

