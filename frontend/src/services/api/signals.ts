/**
 * Signals API Service
 * 
 * API calls for signal retrieval.
 * 
 * NOTE: Signals are received via webhooks and cannot be created directly.
 */

import { apiClient, apiRequest } from './client'
import type { Signal, SignalListParams } from '@/types/index'

// Note: Signals are accessed via chart endpoints, not their own base path

/**
 * Get signals for a specific chart.
 */
export async function getSignalsByChart(
  chartId: string,
  params?: SignalListParams
): Promise<Signal[]> {
  return apiRequest(
    apiClient.get(`/charts/${chartId}/signals`, { params })
  )
}

/**
 * Get the latest signal for a chart.
 */
export async function getLatestSignal(
  chartId: string
): Promise<Signal | null> {
  try {
    const signals = await getSignalsByChart(chartId, { limit: 1 })
    return signals[0] || null
  } catch {
    return null
  }
}

