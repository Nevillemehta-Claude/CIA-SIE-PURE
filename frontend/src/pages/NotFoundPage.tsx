import { Link } from 'react-router-dom'
import { Button } from '@/components/common/Button'
import { Home, AlertCircle } from 'lucide-react'

export function NotFoundPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
      <div className="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-surface-tertiary">
        <AlertCircle className="h-10 w-10 text-slate-400" />
      </div>
      <h1 className="font-display text-3xl font-bold">404</h1>
      <p className="mt-2 text-slate-400">Page not found</p>
      <p className="mt-1 max-w-sm text-sm text-slate-500">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/" className="mt-6">
        <Button leftIcon={<Home className="h-4 w-4" />}>
          Back to Dashboard
        </Button>
      </Link>
    </div>
  )
}

