/**
 * Narratives API Service
 * 
 * API calls for AI-generated narrative content.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-001: All responses include mandatory disclaimer
 * - CR-003: All content is descriptive, not prescriptive
 */

import { apiClient, apiRequest } from './client'
import type { Narrative, PlainNarrativeResponse, NarrativeParams } from '@/types/index'

/**
 * Get narrative for a silo.
 * 
 * CR-001 COMPLIANCE: Response includes mandatory disclaimer.
 * The disclaimer MUST be displayed with any AI content.
 */
export async function getSiloNarrative(
  siloId: string,
  params?: NarrativeParams
): Promise<Narrative> {
  return apiRequest(
    apiClient.get(`/silos/${siloId}/narrative`, { params })
  )
}

/**
 * Get plain text narrative for a silo.
 * 
 * CR-001 COMPLIANCE: Response is validated for constitutional compliance.
 */
export async function getSiloNarrativePlain(
  siloId: string
): Promise<PlainNarrativeResponse> {
  return apiRequest(
    apiClient.get(`/silos/${siloId}/narrative/plain`)
  )
}

/**
 * Get narrative for a specific chart.
 * 
 * CR-001 COMPLIANCE: Response includes mandatory disclaimer.
 */
export async function getChartNarrative(
  chartId: string,
  params?: NarrativeParams
): Promise<Narrative> {
  return apiRequest(
    apiClient.get(`/charts/${chartId}/narrative`, { params })
  )
}

