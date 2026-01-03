/**
 * NotFoundPage Component
 * 
 * 404 error page for unmatched routes.
 */

import { Link } from 'react-router-dom'
import { ContentArea } from '@components/layout'
import { Home, ArrowLeft } from 'lucide-react'

/**
 * NotFoundPage displays when a route is not found.
 */
export function NotFoundPage() {
  return (
    <ContentArea>
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <p className="text-8xl font-display font-bold text-slate-700 mb-4">404</p>
        <h1 className="text-2xl font-display font-semibold mb-2">Page Not Found</h1>
        <p className="text-slate-400 mb-8 max-w-md">
          The page you're looking for doesn't exist or has been moved.
        </p>
        
        <div className="flex items-center gap-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-primary hover:bg-accent-primary/90 text-white font-medium transition-colors"
          >
            <Home className="h-4 w-4" aria-hidden="true" />
            Go to Dashboard
          </Link>
          <button
            onClick={() => window.history.back()}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-600 hover:bg-surface-tertiary text-slate-300 font-medium transition-colors"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Go Back
          </button>
        </div>
      </div>
    </ContentArea>
  )
}

