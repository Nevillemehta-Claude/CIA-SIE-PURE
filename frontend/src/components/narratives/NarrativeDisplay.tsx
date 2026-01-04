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
 * 
 * ACCESSIBILITY:
 * - section with aria-labelledby for clear structure
 * - aria-busy and role="status" for loading state
 * - Each narrative section is properly labeled
 */
export function NarrativeDisplay({ narrative, isLoading }: NarrativeDisplayProps) {
  if (isLoading) {
    return (
      <div
        className="flex items-center justify-center py-8"
        role="status"
        aria-busy="true"
        aria-label="Loading narrative"
      >
        <Spinner size="lg" />
      </div>
    )
  }

  if (!narrative) {
    return null
  }

  return (
    <section className="space-y-4" aria-labelledby="narrative-heading">
      <div className="flex items-center gap-2">
        <FileText className="h-5 w-5 text-accent-primary" aria-hidden="true" />
        <h3 id="narrative-heading" className="font-display text-lg font-semibold">
          Signal Narrative
        </h3>
      </div>

      <div className="space-y-4" role="region" aria-label="Narrative sections">
        {narrative.sections.map((section, index) => (
          <article
            key={`${section.section_type}-${index}`}
            className="rounded-lg border border-slate-700 bg-surface-secondary p-4"
            aria-label={`${section.section_type.replace('_', ' ')} section`}
          >
            <div className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">
              {section.section_type.replace('_', ' ')}
            </div>
            <p className="whitespace-pre-wrap text-slate-300">{section.content}</p>
          </article>
        ))}
      </div>

      {/* CONSTITUTIONAL: Disclaimer is MANDATORY and ALWAYS rendered */}
      <Disclaimer />
    </section>
  )
}
