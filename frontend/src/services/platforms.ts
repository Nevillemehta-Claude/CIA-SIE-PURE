import { apiClient, apiRequest } from './client'

const PATH = '/platforms'

export interface PlatformInfo {
  name: string
  display_name: string
  description: string
  connected: boolean
  supports_webhooks: boolean
  supports_realtime: boolean
  setup_url?: string
}

export interface PlatformConnectRequest {
  platform_name: string
  credentials?: Record<string, string>
}

export interface PlatformConnectResponse {
  status: 'connected' | 'pending' | 'failed'
  message: string
  requires_oauth?: boolean
  oauth_url?: string
}

export interface WatchlistResponse {
  name: string
  symbols: string[]
}

export interface SetupInstructionsResponse {
  platform_name: string
  steps: string[]
  webhook_url: string
  example_payload: Record<string, unknown>
}

export async function getPlatforms(): Promise<PlatformInfo[]> {
  return apiRequest(apiClient.get(`${PATH}/`))
}

export async function getPlatform(name: string): Promise<PlatformInfo> {
  return apiRequest(apiClient.get(`${PATH}/${name}`))
}

export async function connectPlatform(data: PlatformConnectRequest): Promise<PlatformConnectResponse> {
  return apiRequest(apiClient.post(`${PATH}/connect`, data))
}

export async function disconnectPlatform(name: string): Promise<void> {
  return apiRequest(apiClient.post(`${PATH}/${name}/disconnect`))
}

export async function getPlatformHealth(name: string): Promise<{ status: string; message?: string }> {
  return apiRequest(apiClient.get(`${PATH}/${name}/health`))
}

export async function getPlatformWatchlists(name: string): Promise<WatchlistResponse[]> {
  return apiRequest(apiClient.get(`${PATH}/${name}/watchlists`))
}

export async function getSetupInstructions(name: string): Promise<SetupInstructionsResponse> {
  return apiRequest(apiClient.get(`${PATH}/${name}/setup`))
}

