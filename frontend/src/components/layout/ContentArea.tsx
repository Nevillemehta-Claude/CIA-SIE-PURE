/**
 * ContentArea Component
 * 
 * A wrapper for main content with consistent padding and max-width.
 */

import { clsx } from 'clsx'
import type { ReactNode } from 'react'

interface ContentAreaProps {
  /** Content to display */
  children: ReactNode
  /** Maximum width constraint */
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full'
  /** Additional CSS classes */
  className?: string
}

const MAX_WIDTH_CLASSES = {
  sm: 'max-w-screen-sm',
  md: 'max-w-screen-md',
  lg: 'max-w-screen-lg',
  xl: 'max-w-screen-xl',
  '2xl': 'max-w-screen-2xl',
  full: 'max-w-full',
} as const

/**
 * ContentArea provides consistent content wrapper styling.
 */
export function ContentArea({ 
  children, 
  maxWidth = '2xl',
  className 
}: ContentAreaProps) {
  return (
    <div 
      className={clsx(
        'mx-auto w-full',
        MAX_WIDTH_CLASSES[maxWidth],
        className
      )}
    >
      {children}
    </div>
  )
}

