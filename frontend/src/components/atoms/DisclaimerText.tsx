/**
 * DisclaimerText Component
 * 
 * MANDATORY disclaimer for all AI-generated content.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-001):
 * This disclaimer MUST appear on ALL AI-generated content.
 * The text is fixed and immutable - it cannot be modified or hidden.
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 1
 */

import { clsx } from 'clsx'
import { Info } from 'lucide-react'

interface DisclaimerTextProps {
  /** Display variant */
  variant?: 'inline' | 'block' | 'compact'
  /** Additional CSS classes */
  className?: string
}

/**
 * The MANDATORY disclaimer text.
 * This text is immutable and must always be displayed exactly as written.
 */
const DISCLAIMER_TEXT = 
  "This is a description of what your charts are showing. " +
  "The interpretation and any decision is entirely yours."

/**
 * DisclaimerText displays the mandatory disclaimer for AI-generated content.
 * 
 * CR-001 COMPLIANCE: This component MUST be rendered alongside any
 * AI-generated narrative, chat response, or analysis.
 */
export function DisclaimerText({ 
  variant = 'block',
  className 
}: DisclaimerTextProps) {
  if (variant === 'inline') {
    return (
      <span 
        className={clsx('text-sm italic text-slate-400', className)}
        role="note"
        aria-label="Important disclaimer"
      >
        {DISCLAIMER_TEXT}
      </span>
    )
  }

  if (variant === 'compact') {
    return (
      <p 
        className={clsx(
          'flex items-center gap-2 text-xs text-slate-500 italic',
          className
        )}
        role="note"
        aria-label="Important disclaimer"
      >
        <Info className="h-3 w-3 flex-shrink-0" aria-hidden="true" />
        {DISCLAIMER_TEXT}
      </p>
    )
  }

  // Block variant (default)
  return (
    <div 
      className={clsx(
        'mt-4 rounded-lg border border-slate-600 bg-slate-800/50 p-4',
        className
      )}
      role="note"
      aria-label="Important disclaimer"
    >
      <div className="flex items-start gap-3">
        <Info 
          className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" 
          aria-hidden="true" 
        />
        <p className="text-sm italic text-slate-300">
          {DISCLAIMER_TEXT}
        </p>
      </div>
    </div>
  )
}

/**
 * Export the disclaimer text for use in validation.
 */
export const MANDATORY_DISCLAIMER = DISCLAIMER_TEXT

