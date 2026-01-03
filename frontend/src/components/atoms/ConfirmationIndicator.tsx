/**
 * ConfirmationIndicator Component
 * 
 * Visual indicator for signal confirmations.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * This indicates alignment only - it does NOT imply that aligned signals
 * are "stronger" or more reliable than individual signals.
 * No confidence scores or strength indicators.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 2
 */

import { clsx } from 'clsx'
import { CheckCircle2 } from 'lucide-react'

interface ConfirmationIndicatorProps {
  /** Number of confirmations (optional - display only) */
  count?: number
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
}

const SIZE_CLASSES = {
  sm: 'text-xs px-2 py-0.5 gap-1',
  md: 'text-sm px-3 py-1 gap-1.5',
  lg: 'text-base px-4 py-1.5 gap-2',
} as const

const ICON_SIZES = {
  sm: 'h-3 w-3',
  md: 'h-4 w-4',
  lg: 'h-5 w-5',
} as const

/**
 * ConfirmationIndicator displays when signals align.
 * 
 * CR-002 COMPLIANCE: This is purely descriptive.
 * It does NOT imply that confirmations are "stronger" signals.
 */
export function ConfirmationIndicator({ 
  count,
  size = 'md' 
}: ConfirmationIndicatorProps) {
  return (
    <span 
      className={clsx(
        'inline-flex items-center rounded-full border font-medium',
        'bg-accent-primary/20 text-accent-primary border-accent-primary/40',
        SIZE_CLASSES[size]
      )}
      role="status"
      aria-label={count !== undefined 
        ? `${count} confirmations detected` 
        : 'Confirmation detected'}
    >
      <CheckCircle2 className={ICON_SIZES[size]} aria-hidden="true" />
      <span>
        {count !== undefined ? `${count} ` : ''}
        Confirmation{count !== 1 ? 's' : ''}
      </span>
    </span>
  )
}

