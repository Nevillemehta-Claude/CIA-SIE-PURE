/**
 * Signals API Service
 * 
 * API calls for signal retrieval.
 * 
 * NOTE: Signals are received via webhooks and cannot be created directly.
 */

import { apiClient, apiRequest } from './client'
import type { Signal, SignalListParams } from '@/types/index'

// Signals base path
const SIGNALS_PATH = '/signals'

/**
 * Get signals for a specific chart.
 */
export async function getSignalsByChart(
  chartId: string,
  params?: SignalListParams
): Promise<Signal[]> {
  return apiRequest(
    apiClient.get(`${SIGNALS_PATH}/chart/${chartId}`, { params })
  )
}

/**
 * Get the latest signal for a chart.
 * Uses dedicated /latest endpoint for efficiency.
 */
export async function getLatestSignal(
  chartId: string
): Promise<Signal | null> {
  try {
    return await apiRequest(
      apiClient.get(`${SIGNALS_PATH}/chart/${chartId}/latest`)
    )
  } catch {
    return null
  }
}

