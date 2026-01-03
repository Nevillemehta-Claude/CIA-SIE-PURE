/**
 * SplitPane Component
 * 
 * Two-column layout with responsive behavior.
 * 
 * CONSTITUTIONAL COMPLIANCE (CR-002):
 * When used for contradictions, both panes MUST have equal width.
 */

import { clsx } from 'clsx'
import type { ReactNode } from 'react'

interface SplitPaneProps {
  /** Left pane content */
  left: ReactNode
  /** Right pane content */
  right: ReactNode
  /** Split ratio (applies to left pane, right is remainder) */
  ratio?: '1:1' | '1:2' | '2:1' | '1:3' | '3:1'
  /** Gap between panes */
  gap?: 'sm' | 'md' | 'lg'
  /** Additional CSS classes */
  className?: string
  /** Stack vertically on mobile */
  stackOnMobile?: boolean
}

const RATIO_CLASSES = {
  '1:1': 'lg:grid-cols-2',
  '1:2': 'lg:grid-cols-3',
  '2:1': 'lg:grid-cols-3',
  '1:3': 'lg:grid-cols-4',
  '3:1': 'lg:grid-cols-4',
} as const

const LEFT_SPAN_CLASSES = {
  '1:1': 'lg:col-span-1',
  '1:2': 'lg:col-span-1',
  '2:1': 'lg:col-span-2',
  '1:3': 'lg:col-span-1',
  '3:1': 'lg:col-span-3',
} as const

const RIGHT_SPAN_CLASSES = {
  '1:1': 'lg:col-span-1',
  '1:2': 'lg:col-span-2',
  '2:1': 'lg:col-span-1',
  '1:3': 'lg:col-span-3',
  '3:1': 'lg:col-span-1',
} as const

const GAP_CLASSES = {
  sm: 'gap-3',
  md: 'gap-4 lg:gap-6',
  lg: 'gap-6 lg:gap-8',
} as const

/**
 * SplitPane provides a two-column layout.
 * 
 * CR-002 COMPLIANCE: Use ratio="1:1" for contradiction displays
 * to ensure equal visual prominence.
 */
export function SplitPane({ 
  left, 
  right,
  ratio = '1:1',
  gap = 'md',
  className,
  stackOnMobile = true 
}: SplitPaneProps) {
  return (
    <div 
      className={clsx(
        'grid',
        stackOnMobile ? 'grid-cols-1' : RATIO_CLASSES[ratio],
        RATIO_CLASSES[ratio],
        GAP_CLASSES[gap],
        className
      )}
    >
      {/* Left pane */}
      <div className={LEFT_SPAN_CLASSES[ratio]}>
        {left}
      </div>
      
      {/* Right pane */}
      <div className={RIGHT_SPAN_CLASSES[ratio]}>
        {right}
      </div>
    </div>
  )
}

