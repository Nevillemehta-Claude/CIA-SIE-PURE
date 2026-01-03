/**
 * DirectionArrow Component
 * 
 * Simple directional arrow icon for compact displays.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * All arrows have equal visual weight. No direction is emphasized.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 2
 */

import { clsx } from 'clsx'
import { ArrowUp, ArrowDown, Minus } from 'lucide-react'
import { Direction } from '@/types/index'

interface DirectionArrowProps {
  /** The signal direction */
  direction: Direction
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
  /** Whether to show background */
  withBackground?: boolean
}

const DIRECTION_CONFIG = {
  [Direction.BULLISH]: {
    icon: ArrowUp,
    className: 'text-signal-bullish',
    bgClassName: 'bg-signal-bullish/20',
  },
  [Direction.BEARISH]: {
    icon: ArrowDown,
    className: 'text-signal-bearish',
    bgClassName: 'bg-signal-bearish/20',
  },
  [Direction.NEUTRAL]: {
    icon: Minus,
    className: 'text-signal-neutral',
    bgClassName: 'bg-signal-neutral/20',
  },
} as const

const ICON_SIZES = {
  sm: 'h-4 w-4',
  md: 'h-5 w-5',
  lg: 'h-6 w-6',
} as const

const CONTAINER_SIZES = {
  sm: 'p-1',
  md: 'p-1.5',
  lg: 'p-2',
} as const

/**
 * DirectionArrow displays a simple arrow indicating direction.
 * 
 * CR-002 COMPLIANCE: All arrows use the same sizing and weight.
 */
export function DirectionArrow({ 
  direction, 
  size = 'md',
  withBackground = false 
}: DirectionArrowProps) {
  const config = DIRECTION_CONFIG[direction]
  const Icon = config.icon

  return (
    <span 
      className={clsx(
        'inline-flex items-center justify-center',
        config.className,
        withBackground && [config.bgClassName, 'rounded-full', CONTAINER_SIZES[size]]
      )}
      role="img"
      aria-label={`Direction: ${direction.toLowerCase()}`}
    >
      <Icon className={ICON_SIZES[size]} aria-hidden="true" />
    </span>
  )
}

