import { AlertCircle, RefreshCw } from 'lucide-react'
import { Button } from './Button'

interface ErrorStateProps {
  title?: string
  message?: string
  onRetry?: () => void
}

export function ErrorState({
  title = 'Something went wrong',
  message = 'An error occurred while loading data.',
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="mb-4 rounded-full bg-red-500/10 p-4">
        <AlertCircle className="h-8 w-8 text-red-500" />
      </div>
      <h3 className="font-display text-lg font-semibold text-slate-300">{title}</h3>
      <p className="mt-2 max-w-sm text-sm text-slate-400">{message}</p>
      {onRetry && (
        <Button
          variant="secondary"
          size="sm"
          onClick={onRetry}
          leftIcon={<RefreshCw className="h-4 w-4" />}
          className="mt-4"
        >
          Try Again
        </Button>
      )}
    </div>
  )
}

