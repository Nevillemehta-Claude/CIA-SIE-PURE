/**
 * CIA-SIE Frontend Application
 * 
 * Root application component with providers and routing.
 * 
 * GOVERNED BY: Constitutional Rules CR-001, CR-002, CR-003
 * @see ADAPTER_FINANCIAL_SERVICES.md
 */

import { Suspense } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppShell } from '@components/layout'
import { LoadingSpinner } from '@components/atoms'
import {
  DashboardPage,
  InstrumentsPage,
  InstrumentDetailPage,
  ChartDetailPage,
  SettingsPage,
  NotFoundPage,
} from '@/router'

/**
 * React Query client configuration.
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000, // 30 seconds
      gcTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: true,
    },
  },
})

/**
 * Loading fallback for lazy-loaded pages.
 */
function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <LoadingSpinner size="lg" label="Loading page..." />
    </div>
  )
}

/**
 * Root application component.
 * 
 * This is the entry point that sets up:
 * - React Query for server state management
 * - React Router for client-side routing
 * - AppShell for consistent layout
 */
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppShell />}>
            {/* Dashboard - Home page */}
            <Route 
              index 
              element={
                <Suspense fallback={<PageLoader />}>
                  <DashboardPage />
                </Suspense>
              } 
            />
            
            {/* Instruments */}
            <Route 
              path="instruments" 
              element={
                <Suspense fallback={<PageLoader />}>
                  <InstrumentsPage />
                </Suspense>
              } 
            />
            <Route 
              path="instruments/:instrumentId" 
              element={
                <Suspense fallback={<PageLoader />}>
                  <InstrumentDetailPage />
                </Suspense>
              } 
            />
            
            {/* Charts */}
            <Route 
              path="charts/:chartId" 
              element={
                <Suspense fallback={<PageLoader />}>
                  <ChartDetailPage />
                </Suspense>
              } 
            />
            
            {/* Settings */}
            <Route 
              path="settings" 
              element={
                <Suspense fallback={<PageLoader />}>
                  <SettingsPage />
                </Suspense>
              } 
            />
            
            {/* 404 - Not Found */}
            <Route 
              path="*" 
              element={
                <Suspense fallback={<PageLoader />}>
                  <NotFoundPage />
                </Suspense>
              } 
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

