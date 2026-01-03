/**
 * Card Component
 * 
 * A versatile card container for content grouping.
 */

import { clsx } from 'clsx'
import type { ReactNode } from 'react'

interface CardProps {
  /** Card content */
  children: ReactNode
  /** Visual variant */
  variant?: 'default' | 'elevated' | 'outlined'
  /** Padding size */
  padding?: 'none' | 'sm' | 'md' | 'lg'
  /** Additional CSS classes */
  className?: string
  /** Optional click handler */
  onClick?: () => void
  /** Whether the card is interactive */
  interactive?: boolean
}

const VARIANT_CLASSES = {
  default: 'rounded-lg border border-slate-700 bg-surface-secondary',
  elevated: 'rounded-lg border border-slate-600 bg-surface-secondary shadow-lg shadow-black/20',
  outlined: 'rounded-lg border-2 border-slate-600 bg-transparent',
} as const

const PADDING_CLASSES = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
} as const

/**
 * Card provides a container for grouping related content.
 */
export function Card({ 
  children, 
  variant = 'default',
  padding = 'md',
  className,
  onClick,
  interactive = false 
}: CardProps) {
  const isClickable = onClick || interactive

  return (
    <div 
      className={clsx(
        VARIANT_CLASSES[variant],
        PADDING_CLASSES[padding],
        isClickable && 'cursor-pointer transition-colors hover:bg-surface-tertiary/50',
        className
      )}
      onClick={onClick}
      role={isClickable ? 'button' : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onKeyDown={isClickable ? (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          onClick?.()
        }
      } : undefined}
    >
      {children}
    </div>
  )
}

