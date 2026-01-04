import { apiClient, apiRequest } from './client'
import type { Silo } from '@/types/models'
import type { SiloListParams } from '@/types/api'

const PATH = '/silos'

export async function getSilos(params?: SiloListParams): Promise<Silo[]> {
  return apiRequest(apiClient.get(`${PATH}/`, { params }))
}

export async function getSilo(id: string): Promise<Silo> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}

