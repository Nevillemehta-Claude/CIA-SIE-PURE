import { clsx } from 'clsx'
import { Clock, AlertTriangle, HelpCircle } from 'lucide-react'
import type { FreshnessStatus } from '@/types/enums'

interface FreshnessBadgeProps {
  status: FreshnessStatus
  showLabel?: boolean
}

const CONFIG = {
  CURRENT: { icon: Clock, label: 'Current', className: 'text-freshness-current' },
  RECENT: { icon: Clock, label: 'Recent', className: 'text-freshness-recent' },
  STALE: { icon: AlertTriangle, label: 'Stale', className: 'text-freshness-stale' },
  UNAVAILABLE: { icon: HelpCircle, label: 'No Data', className: 'text-freshness-unavailable' },
} as const

export function FreshnessBadge({ status, showLabel = true }: FreshnessBadgeProps) {
  const config = CONFIG[status]
  const Icon = config.icon

  return (
    <span className={clsx('inline-flex items-center gap-1 text-sm', config.className)}>
      <Icon className="h-4 w-4" />
      {showLabel && config.label}
    </span>
  )
}

