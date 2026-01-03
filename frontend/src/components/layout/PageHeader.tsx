/**
 * PageHeader Component
 * 
 * Consistent page header with title, description, and optional actions.
 */

import { clsx } from 'clsx'
import type { ReactNode } from 'react'

interface PageHeaderProps {
  /** Page title */
  title: string
  /** Optional description */
  description?: string
  /** Action buttons or elements */
  actions?: ReactNode
  /** Breadcrumb or navigation element */
  breadcrumb?: ReactNode
  /** Additional CSS classes */
  className?: string
}

/**
 * PageHeader provides consistent page header styling.
 */
export function PageHeader({ 
  title, 
  description,
  actions,
  breadcrumb,
  className 
}: PageHeaderProps) {
  return (
    <div className={clsx('mb-6 lg:mb-8', className)}>
      {breadcrumb && (
        <div className="mb-3">{breadcrumb}</div>
      )}
      
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl md:text-3xl font-bold text-white">
            {title}
          </h1>
          {description && (
            <p className="mt-1 text-sm md:text-base text-slate-400">
              {description}
            </p>
          )}
        </div>
        
        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  )
}

