import { apiClient, apiRequest } from './client'

const PATH = '/baskets'

export interface AnalyticalBasket {
  basket_id: string
  name: string
  description: string
  basket_type: 'CONFIRMATION' | 'DIVERGENCE' | 'CUSTOM'
  chart_ids: string[]
  created_at: string
  is_active: boolean
}

export interface CreateBasketRequest {
  name: string
  description: string
  basket_type: 'CONFIRMATION' | 'DIVERGENCE' | 'CUSTOM'
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

