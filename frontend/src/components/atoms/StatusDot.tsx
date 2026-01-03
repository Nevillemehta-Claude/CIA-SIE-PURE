/**
 * StatusDot Component
 * 
 * A simple status indicator dot for various states.
 * 
 * @description Used for connection status, health checks, etc.
 */

import { clsx } from 'clsx'

type StatusType = 'success' | 'warning' | 'error' | 'info' | 'neutral'

interface StatusDotProps {
  /** Status type determining the color */
  status: StatusType
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
  /** Whether to show pulsing animation */
  pulse?: boolean
  /** Accessible label */
  label?: string
}

const STATUS_COLORS = {
  success: 'bg-green-500',
  warning: 'bg-yellow-500',
  error: 'bg-red-500',
  info: 'bg-blue-500',
  neutral: 'bg-gray-500',
} as const

const SIZE_CLASSES = {
  sm: 'h-2 w-2',
  md: 'h-3 w-3',
  lg: 'h-4 w-4',
} as const

/**
 * StatusDot displays a colored dot indicating status.
 */
export function StatusDot({ 
  status, 
  size = 'md',
  pulse = false,
  label 
}: StatusDotProps) {
  return (
    <span 
      className={clsx(
        'inline-block rounded-full',
        STATUS_COLORS[status],
        SIZE_CLASSES[size],
        pulse && 'animate-pulse'
      )}
      role="status"
      aria-label={label || `Status: ${status}`}
    />
  )
}

