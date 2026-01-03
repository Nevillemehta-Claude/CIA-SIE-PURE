/**
 * Freshness Hook
 * 
 * Calculates freshness status from timestamps.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-003):
 * Freshness is purely DESCRIPTIVE - it does NOT invalidate data.
 * Stale data is still displayed; this just indicates age.
 */

import { useMemo } from 'react'
import { FreshnessStatus } from '@/types/index'
import type { FreshnessThresholds } from '@/types/index'
import { differenceInMinutes } from 'date-fns'

/**
 * Default freshness thresholds (in minutes).
 */
const DEFAULT_THRESHOLDS: FreshnessThresholds = {
  current_threshold_min: 2,
  recent_threshold_min: 10,
  stale_threshold_min: 30,
}

/**
 * Calculate freshness status from a timestamp.
 * 
 * CR-003 COMPLIANCE: This function only DESCRIBES data age.
 * It does NOT invalidate or suppress stale data.
 */
export function calculateFreshness(
  timestamp: string | Date | null | undefined,
  thresholds: FreshnessThresholds = DEFAULT_THRESHOLDS
): FreshnessStatus {
  if (!timestamp) {
    return FreshnessStatus.UNAVAILABLE
  }

  const signalTime = typeof timestamp === 'string' ? new Date(timestamp) : timestamp
  const now = new Date()
  const ageMinutes = differenceInMinutes(now, signalTime)

  if (ageMinutes <= thresholds.current_threshold_min) {
    return FreshnessStatus.CURRENT
  }
  
  if (ageMinutes <= thresholds.recent_threshold_min) {
    return FreshnessStatus.RECENT
  }
  
  return FreshnessStatus.STALE
}

/**
 * Hook to calculate freshness status.
 * 
 * @param timestamp - The timestamp to evaluate
 * @param thresholds - Optional custom thresholds
 * @returns Freshness status (purely descriptive)
 */
export function useFreshness(
  timestamp: string | Date | null | undefined,
  thresholds?: FreshnessThresholds
): FreshnessStatus {
  return useMemo(
    () => calculateFreshness(timestamp, thresholds),
    [timestamp, thresholds]
  )
}

/**
 * Hook to get freshness for multiple timestamps.
 */
export function useFreshnessMultiple(
  timestamps: (string | Date | null | undefined)[],
  thresholds?: FreshnessThresholds
): FreshnessStatus[] {
  return useMemo(
    () => timestamps.map(ts => calculateFreshness(ts, thresholds)),
    [timestamps, thresholds]
  )
}

