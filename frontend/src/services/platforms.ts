import { apiClient, apiRequest } from './client'

const PATH = '/platforms'

/**
 * PlatformInfo - Matches backend PlatformInfo model exactly
 * @see src/cia_sie/api/routes/platforms.py - PlatformInfo
 */
export interface PlatformInfo {
  platform_name: string  // FIXED: was 'name'
  display_name: string
  supports_watchlist_import: boolean  // FIXED: was 'supports_webhooks'
  supports_real_time_signals: boolean  // FIXED: was 'supports_realtime'
  requires_authentication: boolean  // ADDED: missing field
  status: string  // ADDED: missing field
  is_connected: boolean  // FIXED: was 'connected'
}

/**
 * PlatformConnectRequest - Matches backend PlatformConnectRequest model
 * @see src/cia_sie/api/routes/platforms.py - PlatformConnectRequest
 */
export interface PlatformConnectRequest {
  platform: string  // FIXED: was 'platform_name'
  api_key?: string | null
  api_secret?: string | null
  access_token?: string | null
}

/**
 * PlatformConnectResponse - Matches backend PlatformConnectResponse model
 * @see src/cia_sie/api/routes/platforms.py - PlatformConnectResponse
 */
export interface PlatformConnectResponse {
  platform: string
  status: string
  is_connected: boolean
  error?: string | null
}

/**
 * WatchlistResponse - Matches backend WatchlistResponse model
 * @see src/cia_sie/api/routes/platforms.py - WatchlistResponse
 */
export interface WatchlistResponse {
  watchlist_id: string  // ADDED: missing field
  name: string
  instrument_count: number  // FIXED: was 'symbols'
  platform: string  // ADDED: missing field
}

/**
 * SetupInstructionsResponse - Matches backend SetupInstructionsResponse model
 * @see src/cia_sie/api/routes/platforms.py - SetupInstructionsResponse
 */
export interface SetupInstructionsResponse {
  platform: string  // FIXED: was 'platform_name'
  instructions: string  // FIXED: was 'steps'
  webhook_url_template?: string | null  // FIXED: was 'webhook_url'
  alert_message_template?: string | null  // ADDED: missing field
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

