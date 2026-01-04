import { apiClient, apiRequest } from './client'
import type { Signal } from '@/types/models'
import type { SignalListParams } from '@/types/api'

const PATH = '/signals'

export async function getSignalsByChart(
  chartId: string,
  params?: SignalListParams
): Promise<Signal[]> {
  return apiRequest(apiClient.get(`${PATH}/chart/${chartId}`, { params }))
}

export async function getLatestSignal(chartId: string): Promise<Signal | null> {
  try {
    return await apiRequest(apiClient.get(`${PATH}/chart/${chartId}/latest`))
  } catch {
    return null
  }
}

export async function getSignal(id: string): Promise<Signal> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}

