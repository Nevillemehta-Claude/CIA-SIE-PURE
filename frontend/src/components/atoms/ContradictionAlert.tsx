/**
 * ContradictionAlert Component
 * 
 * Visual indicator for contradictions with appropriate styling.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * This is an alert indicator only - it does NOT resolve or suggest
 * which signal is "correct". It simply alerts the user that
 * conflicting signals exist.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 2
 */

import { clsx } from 'clsx'
import { AlertTriangle } from 'lucide-react'

interface ContradictionAlertProps {
  /** Number of contradictions (optional - display only) */
  count?: number
  /** Size variant */
  size?: 'sm' | 'md' | 'lg'
  /** Whether to show pulsing animation */
  pulse?: boolean
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
 * ContradictionAlert displays an alert for detected contradictions.
 * 
 * CR-002 COMPLIANCE: This component only ALERTS about contradictions.
 * It does NOT resolve them or suggest which signal to follow.
 */
export function ContradictionAlert({ 
  count,
  size = 'md',
  pulse = false 
}: ContradictionAlertProps) {
  return (
    <span 
      className={clsx(
        'inline-flex items-center rounded-full border font-medium',
        'bg-amber-500/20 text-amber-500 border-amber-500/40',
        SIZE_CLASSES[size],
        pulse && 'animate-pulse'
      )}
      role="alert"
      aria-label={count !== undefined 
        ? `${count} contradictions detected` 
        : 'Contradiction detected'}
    >
      <AlertTriangle className={ICON_SIZES[size]} aria-hidden="true" />
      <span>
        {count !== undefined ? `${count} ` : ''}
        Contradiction{count !== 1 ? 's' : ''}
      </span>
    </span>
  )
}

