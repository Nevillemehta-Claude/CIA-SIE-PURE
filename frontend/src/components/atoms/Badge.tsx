/**
 * Badge Component
 * 
 * A small status indicator badge.
 */

import { clsx } from 'clsx'
import type { ReactNode } from 'react'

type BadgeVariant = 'default' | 'success' | 'warning' | 'error' | 'info'

interface BadgeProps {
  /** Badge content */
  children: ReactNode
  /** Visual variant */
  variant?: BadgeVariant
  /** Size */
  size?: 'sm' | 'md'
  /** Additional CSS classes */
  className?: string
}

const VARIANT_CLASSES = {
  default: 'bg-slate-600 text-slate-200',
  success: 'bg-green-500/20 text-green-400',
  warning: 'bg-amber-500/20 text-amber-400',
  error: 'bg-red-500/20 text-red-400',
  info: 'bg-blue-500/20 text-blue-400',
} as const

const SIZE_CLASSES = {
  sm: 'px-1.5 py-0.5 text-xs',
  md: 'px-2 py-1 text-sm',
} as const

/**
 * Badge displays small labels or status indicators.
 */
export function Badge({ 
  children, 
  variant = 'default',
  size = 'sm',
  className 
}: BadgeProps) {
  return (
    <span 
      className={clsx(
        'inline-flex items-center rounded font-medium',
        VARIANT_CLASSES[variant],
        SIZE_CLASSES[size],
        className
      )}
    >
      {children}
    </span>
  )
}

