/**
 * Charts API Service
 * 
 * API calls for chart management.
 */

import { apiClient, apiRequest } from './client'
import type { 
  Chart, 
  ChartCreateRequest,
  ChartUpdateRequest,
  ChartListParams 
} from '@/types/index'

const BASE_PATH = '/charts'

/**
 * Get all charts.
 */
export async function getCharts(
  params?: ChartListParams
): Promise<Chart[]> {
  return apiRequest(apiClient.get(BASE_PATH, { params }))
}

/**
 * Get charts for a specific silo.
 */
export async function getChartsBySilo(
  siloId: string
): Promise<Chart[]> {
  return apiRequest(apiClient.get(BASE_PATH, { 
    params: { silo_id: siloId } 
  }))
}

/**
 * Get a single chart by ID.
 */
export async function getChart(
  chartId: string
): Promise<Chart> {
  return apiRequest(apiClient.get(`${BASE_PATH}/${chartId}`))
}

/**
 * Create a new chart.
 */
export async function createChart(
  data: ChartCreateRequest
): Promise<Chart> {
  return apiRequest(apiClient.post(BASE_PATH, data))
}

/**
 * Update a chart.
 */
export async function updateChart(
  chartId: string,
  data: ChartUpdateRequest
): Promise<Chart> {
  return apiRequest(apiClient.patch(`${BASE_PATH}/${chartId}`, data))
}

/**
 * Delete a chart.
 */
export async function deleteChart(
  chartId: string
): Promise<void> {
  await apiClient.delete(`${BASE_PATH}/${chartId}`)
}

