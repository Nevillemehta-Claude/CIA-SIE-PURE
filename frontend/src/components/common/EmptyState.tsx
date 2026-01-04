import { Inbox } from 'lucide-react'

interface EmptyStateProps {
  title: string
  description?: string
  icon?: React.ReactNode
}

export function EmptyState({ title, description, icon }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="mb-4 rounded-full bg-surface-tertiary p-4">
        {icon ?? <Inbox className="h-8 w-8 text-slate-400" />}
      </div>
      <h3 className="font-display text-lg font-semibold text-slate-300">{title}</h3>
      {description && (
        <p className="mt-2 max-w-sm text-sm text-slate-400">{description}</p>
      )}
    </div>
  )
}

