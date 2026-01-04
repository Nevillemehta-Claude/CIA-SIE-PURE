import type { Contradiction } from '@/types/models'
import { DirectionBadge } from '@/components/signals/DirectionBadge'
import { ArrowLeftRight } from 'lucide-react'

interface ContradictionCardProps {
  contradiction: Contradiction
}

/**
 * ContradictionCard Component - CBS-004 Implementation
 * 
 * CONSTITUTIONAL REQUIREMENT (CR-002):
 * - Uses grid-cols-[1fr,auto,1fr] to ensure EQUAL sizing of both sides
 * - IDENTICAL styling applied to both Chart A and Chart B
 * - Neutral separator (arrows + "vs") implies NO preference
 * - System EXPOSES contradictions but NEVER resolves them
 * 
 * @see ICD Section: Component Behavioral Specifications - CBS-004
 */
export function ContradictionCard({ contradiction }: ContradictionCardProps) {
  // CONSTITUTIONAL: Both sides use IDENTICAL styling
  const sideClassName = 'rounded-lg bg-surface-secondary p-3 text-center'

  return (
    <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-4">
      {/* CONSTITUTIONAL: Grid ensures EQUAL sizing */}
      <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4">
        {/* Chart A */}
        <div className={sideClassName}>
          <div className="mb-2 text-sm text-slate-400">{contradiction.chart_a_name}</div>
          <DirectionBadge direction={contradiction.chart_a_direction} size="lg" />
        </div>

        {/* Neutral Separator */}
        <div className="flex flex-col items-center gap-1">
          <ArrowLeftRight className="h-5 w-5 text-slate-500" />
          <span className="text-xs text-slate-500">vs</span>
        </div>

        {/* Chart B - IDENTICAL to Chart A */}
        <div className={sideClassName}>
          <div className="mb-2 text-sm text-slate-400">{contradiction.chart_b_name}</div>
          <DirectionBadge direction={contradiction.chart_b_direction} size="lg" />
        </div>
      </div>
    </div>
  )
}

