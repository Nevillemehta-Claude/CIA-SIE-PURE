import type { NarrativeResponse } from '@/types/api'
import { Disclaimer } from '@/components/common/Disclaimer'
import { Spinner } from '@/components/common/Spinner'
import { FileText } from 'lucide-react'

interface NarrativeDisplayProps {
  narrative?: NarrativeResponse
  isLoading?: boolean
}

export function NarrativeDisplay({ narrative, isLoading }: NarrativeDisplayProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!narrative) {
    return null
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <FileText className="h-5 w-5 text-accent-primary" />
        <h3 className="font-display text-lg font-semibold">Signal Narrative</h3>
      </div>

      <div className="rounded-lg border border-slate-700 bg-surface-secondary p-4">
        <p className="whitespace-pre-wrap text-slate-300">{narrative.narrative}</p>
      </div>

      {/* CONSTITUTIONAL: Disclaimer is MANDATORY and ALWAYS rendered */}
      <Disclaimer />
    </div>
  )
}

