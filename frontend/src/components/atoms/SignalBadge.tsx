/**
 * SignalBadge Component
 * 
 * Displays a signal direction with EQUAL visual prominence for all directions.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * All directions have equal visual weight - no direction is displayed as
 * "more important" than another. Saturation and brightness are matched.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Section 0B
 */

import { clsx } from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { Direction } from '@/types/index'

interface SignalBadgeProps {
  /** The signal direction to display */
  direction: Direction
  /** Whether to show the text label */
  showLabel?: boolean
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
}

/**
 * Configuration for each direction.
 * CONSTITUTIONAL: All configs use the same opacity levels and styling patterns
 * to ensure equal visual weight.
 */
const DIRECTION_CONFIG = {
  [Direction.BULLISH]: {
    icon: TrendingUp,
    label: 'Bullish',
    className: 'bg-signal-bullish/20 text-signal-bullish border-signal-bullish/40',
  },
  [Direction.BEARISH]: {
    icon: TrendingDown,
    label: 'Bearish',
    className: 'bg-signal-bearish/20 text-signal-bearish border-signal-bearish/40',
  },
  [Direction.NEUTRAL]: {
    icon: Minus,
    label: 'Neutral',
    className: 'bg-signal-neutral/20 text-signal-neutral border-signal-neutral/40',
  },
} as const

const SIZE_CLASSES = {
  sm: 'px-2 py-0.5 text-xs gap-1',
  md: 'px-3 py-1 text-sm gap-1.5',
  lg: 'px-4 py-1.5 text-base gap-2',
} as const

const ICON_SIZES = {
  sm: 'h-3 w-3',
  md: 'h-4 w-4',
  lg: 'h-5 w-5',
} as const

/**
 * SignalBadge displays a signal direction with equal visual weight.
 * 
 * CR-002 COMPLIANCE: No visual hierarchy between directions.
 * All directions use the same structural styling (padding, borders, opacity).
 */
export function SignalBadge({ 
  direction, 
  showLabel = true,
  size = 'md' 
}: SignalBadgeProps) {
  const config = DIRECTION_CONFIG[direction]
  const Icon = config.icon
  
  return (
    <span 
      className={clsx(
        'inline-flex items-center rounded-full border font-medium',
        config.className,
        SIZE_CLASSES[size]
      )}
      role="status"
      aria-label={`Direction: ${config.label}`}
    >
      <Icon className={ICON_SIZES[size]} aria-hidden="true" />
      {showLabel && config.label}
    </span>
  )
}

