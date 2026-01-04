import { apiClient, apiRequest } from './client'
import type { Chart } from '@/types/models'
import type { ChartListParams } from '@/types/api'

const PATH = '/charts'

export async function getCharts(params?: ChartListParams): Promise<Chart[]> {
  return apiRequest(apiClient.get(`${PATH}/`, { params }))
}

export async function getChart(id: string): Promise<Chart> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}

