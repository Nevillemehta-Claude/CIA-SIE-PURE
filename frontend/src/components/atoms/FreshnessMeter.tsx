/**
 * FreshnessMeter Component
 * 
 * Displays data freshness status.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-003):
 * Freshness is purely DESCRIPTIVE - it does NOT invalidate or suppress data.
 * All data is displayed regardless of freshness status.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Section 0C
 */

import { clsx } from 'clsx'
import { Clock, AlertTriangle, HelpCircle, Zap } from 'lucide-react'
import { FreshnessStatus } from '@/types/index'

interface FreshnessMeterProps {
  /** Freshness status to display */
  status: FreshnessStatus
  /** Whether to show the text label */
  showLabel?: boolean
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
}

/**
 * Configuration for each freshness status.
 * NOTE: These are purely DESCRIPTIVE indicators - they do NOT affect data validity.
 */
const FRESHNESS_CONFIG = {
  [FreshnessStatus.CURRENT]: {
    icon: Zap,
    label: 'Current',
    className: 'text-freshness-current',
    description: 'Data from the most recent bar',
  },
  [FreshnessStatus.RECENT]: {
    icon: Clock,
    label: 'Recent',
    className: 'text-freshness-recent',
    description: 'Data within expected update frequency',
  },
  [FreshnessStatus.STALE]: {
    icon: AlertTriangle,
    label: 'Stale',
    className: 'text-freshness-stale',
    description: 'Data older than expected',
  },
  [FreshnessStatus.UNAVAILABLE]: {
    icon: HelpCircle,
    label: 'No Data',
    className: 'text-freshness-unavailable',
    description: 'No signal data available',
  },
} as const

const SIZE_CLASSES = {
  sm: 'text-xs gap-1',
  md: 'text-sm gap-1.5',
  lg: 'text-base gap-2',
} as const

const ICON_SIZES = {
  sm: 'h-3 w-3',
  md: 'h-4 w-4',
  lg: 'h-5 w-5',
} as const

/**
 * FreshnessMeter displays data freshness in a purely descriptive manner.
 * 
 * CR-003 COMPLIANCE: This is informational only and does not imply
 * that stale data should be ignored or is less valid.
 */
export function FreshnessMeter({ 
  status, 
  showLabel = true,
  size = 'md' 
}: FreshnessMeterProps) {
  const config = FRESHNESS_CONFIG[status]
  const Icon = config.icon

  return (
    <span 
      className={clsx('inline-flex items-center', config.className, SIZE_CLASSES[size])}
      role="status"
      aria-label={`Freshness: ${config.label}`}
      title={config.description}
    >
      <Icon className={ICON_SIZES[size]} aria-hidden="true" />
      {showLabel && <span>{config.label}</span>}
    </span>
  )
}

