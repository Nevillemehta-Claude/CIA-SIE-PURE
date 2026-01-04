import { Info } from 'lucide-react'

interface DisclaimerProps {
  variant?: 'inline' | 'block'
}

/**
 * Disclaimer Component - CBS-003 Implementation
 * 
 * CONSTITUTIONAL REQUIREMENT (CR-003):
 * - Text is HARDCODED and IMMUTABLE
 * - Component is NON-DISMISSIBLE
 * - Component is NON-COLLAPSIBLE
 * - MUST be rendered with every narrative/AI output
 * 
 * ACCESSIBILITY:
 * - role="note" identifies this as important supplementary information
 * - aria-label provides context for screen readers
 * - aria-live="polite" announces when disclaimer appears
 * 
 * @see ICD Section: Component Behavioral Specifications - CBS-003
 */
// CONSTITUTIONAL: This text is HARDCODED and CANNOT be changed
const DISCLAIMER_TEXT =
  'This is a description of what your charts are showing. The interpretation and any decision is entirely yours.'

export function Disclaimer({ variant = 'block' }: DisclaimerProps) {
  if (variant === 'inline') {
    return (
      <span
        className="text-sm italic text-slate-400"
        role="note"
        aria-label="Important disclaimer"
      >
        {DISCLAIMER_TEXT}
      </span>
    )
  }

  return (
    <aside
      className="mt-4 rounded-lg border border-slate-600 bg-slate-800/50 p-4"
      role="note"
      aria-label="Important disclaimer about AI-generated content"
      aria-live="polite"
    >
      <div className="flex items-start gap-3">
        <Info className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" aria-hidden="true" />
        <p className="text-sm italic text-slate-300">{DISCLAIMER_TEXT}</p>
      </div>
    </aside>
  )
}

