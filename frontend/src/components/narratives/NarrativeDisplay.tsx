import type { NarrativeResponse } from '@/types/api'
import { Disclaimer } from '@/components/common/Disclaimer'
import { Spinner } from '@/components/common/Spinner'
import { FileText } from 'lucide-react'

interface NarrativeDisplayProps {
  narrative?: NarrativeResponse
  isLoading?: boolean
}

/**
 * NarrativeDisplay - CBS-006 Implementation
 * 
 * CONSTITUTIONAL: Always renders the Disclaimer component.
 * The narrative is DESCRIPTIVE only - never prescriptive.
 */
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

      <div className="space-y-4">
        {narrative.sections.map((section, index) => (
          <div
            key={`${section.section_type}-${index}`}
            className="rounded-lg border border-slate-700 bg-surface-secondary p-4"
          >
            <div className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">
              {section.section_type.replace('_', ' ')}
            </div>
            <p className="whitespace-pre-wrap text-slate-300">{section.content}</p>
          </div>
        ))}
      </div>

      {/* CONSTITUTIONAL: Disclaimer is MANDATORY and ALWAYS rendered */}
      <Disclaimer />
    </div>
  )
}
