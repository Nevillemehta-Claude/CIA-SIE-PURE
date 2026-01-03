/**
 * ErrorMessage Component
 * 
 * Displays error messages with appropriate styling.
 */

import { clsx } from 'clsx'
import { AlertCircle, XCircle } from 'lucide-react'

interface ErrorMessageProps {
  /** Error message to display */
  message: string
  /** Error title (optional) */
  title?: string
  /** Severity level */
  severity?: 'error' | 'warning'
  /** Additional CSS classes */
  className?: string
  /** Retry callback (optional) */
  onRetry?: () => void
}

/**
 * ErrorMessage displays error information to users.
 */
export function ErrorMessage({ 
  message, 
  title,
  severity = 'error',
  className,
  onRetry 
}: ErrorMessageProps) {
  const Icon = severity === 'error' ? XCircle : AlertCircle
  const colors = severity === 'error' 
    ? 'bg-red-500/10 border-red-500/30 text-red-400'
    : 'bg-amber-500/10 border-amber-500/30 text-amber-400'

  return (
    <div 
      className={clsx(
        'rounded-lg border p-4',
        colors,
        className
      )}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start gap-3">
        <Icon className="h-5 w-5 flex-shrink-0 mt-0.5" aria-hidden="true" />
        <div className="flex-1">
          {title && (
            <h4 className="font-semibold mb-1">{title}</h4>
          )}
          <p className="text-sm">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-3 text-sm font-medium underline hover:no-underline"
            >
              Try again
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

