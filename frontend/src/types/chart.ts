/**
 * Chart Type Definitions
 * 
 * GOVERNED BY: ADAPTER_FINANCIAL_SERVICES.md, BACKEND_ARCHITECTURAL_FLOWCHART.md
 * 
 * CRITICAL CONSTRAINT: Chart has NO weight attribute.
 * Per ADR-003: Weights enable aggregation which is PROHIBITED.
 * All charts have equal standing. User determines importance through interpretation.
 */

/**
 * A TradingView chart that emits signals via webhook.
 * 
 * PROHIBITED FIELDS (per Section 0B):
 * - weight: Enables weighted aggregation
 * - priority: Enables ranking
 * - rank: Explicit ordering
 * - score: Implies judgment
 */
export interface Chart {
  /** Unique identifier */
  chart_id: string
  /** Parent silo ID */
  silo_id: string
  /** Short code for the chart (e.g., 01A, 02B) */
  chart_code: string
  /** Human-readable chart name */
  chart_name: string
  /** Timeframe (e.g., 1m, 5m, 15m, 1h, 4h, D, W, M) */
  timeframe: string
  /** Unique webhook identifier for signal ingestion */
  webhook_id: string
  /** Creation timestamp */
  created_at: string
  /** Last update timestamp */
  updated_at: string
  /** Whether the chart is active */
  is_active: boolean
  // NOTE: Deliberately NO weight field - prohibited by Section 0B
}

/**
 * Request to create a new chart.
 */
export interface ChartCreateRequest {
  silo_id: string
  chart_code: string
  chart_name: string
  timeframe: string
  webhook_id: string
}

/**
 * Request to update a chart.
 */
export interface ChartUpdateRequest {
  chart_name?: string
  timeframe?: string
  is_active?: boolean
}

