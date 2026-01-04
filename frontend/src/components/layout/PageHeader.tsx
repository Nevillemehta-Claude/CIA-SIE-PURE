import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

interface PageHeaderProps {
  title: string
  description?: string
  backTo?: string
  actions?: React.ReactNode
}

export function PageHeader({ title, description, backTo, actions }: PageHeaderProps) {
  return (
    <div className="mb-6 flex items-start justify-between">
      <div className="space-y-1">
        {backTo && (
          <Link
            to={backTo}
            className="mb-2 inline-flex items-center gap-1 text-sm text-slate-400 transition-colors hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Link>
        )}
        <h1 className="font-display text-2xl font-bold">{title}</h1>
        {description && <p className="text-sm text-slate-400">{description}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  )
}

