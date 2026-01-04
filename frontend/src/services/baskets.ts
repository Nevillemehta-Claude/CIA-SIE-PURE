import { apiClient, apiRequest } from './client'

const PATH = '/baskets'

/**
 * AnalyticalBasket - Matches backend AnalyticalBasket model exactly
 * @see src/cia_sie/core/models.py - AnalyticalBasket
 */
export interface AnalyticalBasket {
  basket_id: string
  basket_name: string  // FIXED: was 'name', backend uses 'basket_name'
  description: string | null
  basket_type: 'LOGICAL' | 'HIERARCHICAL' | 'CONTEXTUAL' | 'CUSTOM'  // FIXED: All enum values
  instrument_id: string | null  // ADDED: missing field
  chart_ids: string[]
  created_at: string
  updated_at: string  // ADDED: missing field
  is_active: boolean
}

/**
 * CreateBasketRequest - Matches backend BasketCreate model exactly
 * @see src/cia_sie/core/models.py - BasketCreate
 */
export interface CreateBasketRequest {
  basket_name: string  // FIXED: was 'name', backend uses 'basket_name'
  basket_type?: 'LOGICAL' | 'HIERARCHICAL' | 'CONTEXTUAL' | 'CUSTOM'  // FIXED: All enum values
  description?: string | null
  instrument_id?: string | null  // ADDED: missing field
  chart_ids?: string[]
}

export async function getBaskets(): Promise<AnalyticalBasket[]> {
  return apiRequest(apiClient.get(`${PATH}/`))
}

export async function getBasket(id: string): Promise<AnalyticalBasket> {
  return apiRequest(apiClient.get(`${PATH}/${id}`))
}

export async function createBasket(data: CreateBasketRequest): Promise<AnalyticalBasket> {
  return apiRequest(apiClient.post(`${PATH}/`, data))
}

export async function addChartToBasket(basketId: string, chartId: string): Promise<void> {
  return apiRequest(apiClient.post(`${PATH}/${basketId}/charts/${chartId}`))
}

export async function removeChartFromBasket(basketId: string, chartId: string): Promise<void> {
  return apiRequest(apiClient.delete(`${PATH}/${basketId}/charts/${chartId}`))
}

export async function deleteBasket(id: string): Promise<void> {
  return apiRequest(apiClient.delete(`${PATH}/${id}`))
}

