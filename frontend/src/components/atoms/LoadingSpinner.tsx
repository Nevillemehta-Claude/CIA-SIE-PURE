/**
 * LoadingSpinner Component
 * 
 * A loading indicator for async operations.
 */

import { clsx } from 'clsx'
import { Loader2 } from 'lucide-react'

interface LoadingSpinnerProps {
  /** Size variant */
  size?: 'sm' | 'md' | 'lg' | 'xl'
  /** Accessible label */
  label?: string
  /** Additional CSS classes */
  className?: string
}

const SIZE_CLASSES = {
  sm: 'h-4 w-4',
  md: 'h-6 w-6',
  lg: 'h-8 w-8',
  xl: 'h-12 w-12',
} as const

/**
 * LoadingSpinner displays an animated loading indicator.
 */
export function LoadingSpinner({ 
  size = 'md',
  label = 'Loading...',
  className 
}: LoadingSpinnerProps) {
  return (
    <div 
      className={clsx('flex items-center justify-center', className)}
      role="status"
      aria-label={label}
    >
      <Loader2 
        className={clsx('animate-spin text-accent-primary', SIZE_CLASSES[size])} 
        aria-hidden="true"
      />
      <span className="sr-only">{label}</span>
    </div>
  )
}

