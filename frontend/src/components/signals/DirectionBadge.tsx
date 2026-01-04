import { clsx } from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import type { Direction } from '@/types/enums'

interface DirectionBadgeProps {
  direction: Direction
  showLabel?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const CONFIG = {
  BULLISH: {
    icon: TrendingUp,
    label: 'Bullish',
    className: 'bg-signal-bullish/20 text-signal-bullish border-signal-bullish/40',
  },
  BEARISH: {
    icon: TrendingDown,
    label: 'Bearish',
    className: 'bg-signal-bearish/20 text-signal-bearish border-signal-bearish/40',
  },
  NEUTRAL: {
    icon: Minus,
    label: 'Neutral',
    className: 'bg-signal-neutral/20 text-signal-neutral border-signal-neutral/40',
  },
} as const

const SIZE_CLASSES = {
  sm: { badge: 'px-2 py-0.5 text-xs gap-1', icon: 'h-3 w-3' },
  md: { badge: 'px-3 py-1 text-sm gap-1.5', icon: 'h-4 w-4' },
  lg: { badge: 'px-4 py-1.5 text-base gap-2', icon: 'h-5 w-5' },
} as const

export function DirectionBadge({
  direction,
  showLabel = true,
  size = 'md',
}: DirectionBadgeProps) {
  const config = CONFIG[direction]
  const sizeConfig = SIZE_CLASSES[size]
  const Icon = config.icon

  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full border font-medium',
        config.className,
        sizeConfig.badge
      )}
    >
      <Icon className={sizeConfig.icon} />
      {showLabel && config.label}
    </span>
  )
}

