/**
 * Instrument Type Definitions
 * 
 * GOVERNED BY: BACKEND_ARCHITECTURAL_FLOWCHART.md
 */

/**
 * A tradeable financial asset identified by a unique symbol.
 */
export interface Instrument {
  /** Unique identifier */
  instrument_id: string
  /** Trading symbol (e.g., NIFTY, BANKNIFTY) */
  symbol: string
  /** Human-readable name */
  display_name: string
  /** Creation timestamp */
  created_at: string
  /** Last update timestamp */
  updated_at: string
  /** Whether the instrument is active */
  is_active: boolean
  /** Optional metadata */
  metadata?: Record<string, unknown>
}

/**
 * Request to create a new instrument.
 */
export interface InstrumentCreateRequest {
  symbol: string
  display_name: string
  metadata?: Record<string, unknown>
}

/**
 * Request to update an instrument.
 */
export interface InstrumentUpdateRequest {
  display_name?: string
  is_active?: boolean
  metadata?: Record<string, unknown>
}

/**
 * A logical container grouping charts for a single instrument.
 */
export interface Silo {
  /** Unique identifier */
  silo_id: string
  /** Parent instrument ID */
  instrument_id: string
  /** Silo name */
  silo_name: string
  /** Whether heartbeat monitoring is enabled */
  heartbeat_enabled: boolean
  /** Heartbeat frequency in minutes */
  heartbeat_frequency_min: number
  /** Threshold for CURRENT freshness (minutes) */
  current_threshold_min: number
  /** Threshold for RECENT freshness (minutes) */
  recent_threshold_min: number
  /** Threshold for STALE freshness (minutes) */
  stale_threshold_min: number
  /** Creation timestamp */
  created_at: string
  /** Last update timestamp */
  updated_at: string
  /** Whether the silo is active */
  is_active: boolean
}

/**
 * Request to create a new silo.
 */
export interface SiloCreateRequest {
  instrument_id: string
  silo_name: string
  heartbeat_enabled?: boolean
  heartbeat_frequency_min?: number
  current_threshold_min?: number
  recent_threshold_min?: number
  stale_threshold_min?: number
}

