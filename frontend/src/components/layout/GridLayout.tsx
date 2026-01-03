/**
 * GridLayout Component
 * 
 * Responsive grid layout for cards and content.
 */

import { clsx } from 'clsx'
import type { ReactNode } from 'react'

interface GridLayoutProps {
  /** Grid content */
  children: ReactNode
  /** Number of columns */
  columns?: 1 | 2 | 3 | 4
  /** Gap between items */
  gap?: 'sm' | 'md' | 'lg'
  /** Additional CSS classes */
  className?: string
}

const COLUMN_CLASSES = {
  1: 'grid-cols-1',
  2: 'grid-cols-1 md:grid-cols-2',
  3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
  4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4',
} as const

const GAP_CLASSES = {
  sm: 'gap-3',
  md: 'gap-4 lg:gap-6',
  lg: 'gap-6 lg:gap-8',
} as const

/**
 * GridLayout provides a responsive grid for content.
 */
export function GridLayout({ 
  children, 
  columns = 3,
  gap = 'md',
  className 
}: GridLayoutProps) {
  return (
    <div 
      className={clsx(
        'grid',
        COLUMN_CLASSES[columns],
        GAP_CLASSES[gap],
        className
      )}
    >
      {children}
    </div>
  )
}

