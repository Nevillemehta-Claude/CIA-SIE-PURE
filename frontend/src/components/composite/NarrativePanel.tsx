/**
 * NarrativePanel Component
 * 
 * Displays AI-generated narrative WITH mandatory disclaimer.
 * 
 * CONSTITUTIONAL COMPLIANCE:
 * - CR-001: MANDATORY disclaimer always displayed
 * - CR-003: Content is descriptive only
 * 
 * @see ADAPTER_FINANCIAL_SERVICES.md Rule 1, Rule 3
 */

import { FileText, RefreshCw } from 'lucide-react'
import { Card, DisclaimerText, LoadingSpinner, EmptyState } from '@components/atoms'
import type { Narrative, NarrativeSection } from '@/types/index'
import { NarrativeSectionType } from '@/types/index'

interface NarrativePanelProps {
  /** Narrative to display */
  narrative: Narrative | null
  /** Loading state */
  isLoading?: boolean
  /** Error message */
  error?: string | null
  /** Refresh callback */
  onRefresh?: () => void
}

/**
 * Section type styling configuration.
 */
const SECTION_STYLES = {
  [NarrativeSectionType.SIGNAL_SUMMARY]: {
    borderColor: 'border-l-accent-primary',
    bgColor: 'bg-accent-primary/5',
  },
  [NarrativeSectionType.CONTRADICTION]: {
    borderColor: 'border-l-amber-500',
    bgColor: 'bg-amber-500/5',
  },
  [NarrativeSectionType.CONFIRMATION]: {
    borderColor: 'border-l-blue-500',
    bgColor: 'bg-blue-500/5',
  },
  [NarrativeSectionType.FRESHNESS]: {
    borderColor: 'border-l-slate-500',
    bgColor: 'bg-slate-500/5',
  },
} as const

/**
 * Renders a single narrative section.
 */
function NarrativeSectionDisplay({ section }: { section: NarrativeSection }) {
  const styles = SECTION_STYLES[section.section_type]

  return (
    <div 
      className={`border-l-4 ${styles.borderColor} ${styles.bgColor} pl-4 py-3 rounded-r-lg`}
    >
      <p className="text-sm text-slate-300 leading-relaxed">
        {section.content}
      </p>
    </div>
  )
}

/**
 * NarrativePanel displays AI-generated narrative content.
 * 
 * CR-001 COMPLIANCE: The DisclaimerText component is ALWAYS rendered
 * when narrative content is displayed. This is a constitutional requirement.
 */
export function NarrativePanel({ 
  narrative, 
  isLoading,
  error,
  onRefresh 
}: NarrativePanelProps) {
  if (isLoading) {
    return (
      <Card>
        <div className="flex flex-col items-center justify-center py-8">
          <LoadingSpinner size="lg" label="Generating narrative..." />
          <p className="mt-4 text-sm text-slate-400">
            Generating AI narrative...
          </p>
        </div>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <EmptyState
          title="Narrative unavailable"
          description={error}
          icon={FileText}
          action={onRefresh ? {
            label: 'Try Again',
            onClick: onRefresh,
          } : undefined}
        />
      </Card>
    )
  }

  if (!narrative) {
    return (
      <Card>
        <EmptyState
          title="No narrative available"
          description="Generate a narrative to see AI-powered signal descriptions."
          icon={FileText}
          action={onRefresh ? {
            label: 'Generate Narrative',
            onClick: onRefresh,
          } : undefined}
        />
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-accent-primary" aria-hidden="true" />
          <h3 className="font-display text-lg font-semibold">
            Signal Narrative
          </h3>
        </div>
        {onRefresh && (
          <button
            onClick={onRefresh}
            className="p-2 rounded-lg hover:bg-surface-tertiary transition-colors"
            aria-label="Refresh narrative"
          >
            <RefreshCw className="h-4 w-4 text-slate-400" />
          </button>
        )}
      </div>

      {/* Narrative Content */}
      <Card>
        <div className="space-y-4">
          {narrative.sections.map((section, index) => (
            <NarrativeSectionDisplay key={index} section={section} />
          ))}
        </div>

        {/* 
          MANDATORY DISCLAIMER - CR-001 COMPLIANCE
          This disclaimer MUST always be displayed with AI-generated content.
          It cannot be hidden, minimized, or modified.
        */}
        <DisclaimerText variant="block" />
      </Card>
    </div>
  )
}

