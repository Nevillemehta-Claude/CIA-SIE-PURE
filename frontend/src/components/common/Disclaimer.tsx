import { Info } from 'lucide-react'

interface DisclaimerProps {
  variant?: 'inline' | 'block'
}

// CONSTITUTIONAL: This text is HARDCODED and CANNOT be changed
const DISCLAIMER_TEXT =
  'This is a description of what your charts are showing. The interpretation and any decision is entirely yours.'

export function Disclaimer({ variant = 'block' }: DisclaimerProps) {
  if (variant === 'inline') {
    return <span className="text-sm italic text-slate-400">{DISCLAIMER_TEXT}</span>
  }

  return (
    <div className="mt-4 rounded-lg border border-slate-600 bg-slate-800/50 p-4">
      <div className="flex items-start gap-3">
        <Info className="mt-0.5 h-5 w-5 flex-shrink-0 text-accent-primary" />
        <p className="text-sm italic text-slate-300">{DISCLAIMER_TEXT}</p>
      </div>
    </div>
  )
}

