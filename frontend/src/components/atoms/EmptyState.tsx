/**
 * EmptyState Component
 * 
 * Displays a message when there's no data to show.
 */

import { clsx } from 'clsx'
import { Inbox, type LucideIcon } from 'lucide-react'

interface EmptyStateProps {
  /** Title text */
  title: string
  /** Description text */
  description?: string
  /** Custom icon */
  icon?: LucideIcon
  /** Action button (optional) */
  action?: {
    label: string
    onClick: () => void
  }
  /** Additional CSS classes */
  className?: string
}

/**
 * EmptyState displays when there's no data available.
 */
export function EmptyState({ 
  title, 
  description,
  icon: Icon = Inbox,
  action,
  className 
}: EmptyStateProps) {
  return (
    <div 
      className={clsx(
        'flex flex-col items-center justify-center py-12 text-center',
        className
      )}
    >
      <Icon className="h-12 w-12 text-slate-500 mb-4" aria-hidden="true" />
      <h3 className="font-display text-lg font-semibold text-slate-300 mb-1">
        {title}
      </h3>
      {description && (
        <p className="text-sm text-slate-500 max-w-sm">
          {description}
        </p>
      )}
      {action && (
        <button
          onClick={action.onClick}
          className="mt-4 px-4 py-2 text-sm font-medium rounded-lg bg-accent-primary hover:bg-accent-primary/90 text-white transition-colors"
        >
          {action.label}
        </button>
      )}
    </div>
  )
}

