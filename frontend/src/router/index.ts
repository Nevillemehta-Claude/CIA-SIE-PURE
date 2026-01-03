/**
 * Router Configuration
 * 
 * Defines all application routes.
 */

import { lazy } from 'react'

// Lazy load pages for code splitting
export const DashboardPage = lazy(() => 
  import('@pages/DashboardPage').then(m => ({ default: m.DashboardPage }))
)

export const InstrumentsPage = lazy(() => 
  import('@pages/InstrumentsPage').then(m => ({ default: m.InstrumentsPage }))
)

export const InstrumentDetailPage = lazy(() => 
  import('@pages/InstrumentDetailPage').then(m => ({ default: m.InstrumentDetailPage }))
)

export const ChartDetailPage = lazy(() => 
  import('@pages/ChartDetailPage').then(m => ({ default: m.ChartDetailPage }))
)

export const SettingsPage = lazy(() => 
  import('@pages/SettingsPage').then(m => ({ default: m.SettingsPage }))
)

export const NotFoundPage = lazy(() => 
  import('@pages/NotFoundPage').then(m => ({ default: m.NotFoundPage }))
)

/**
 * Route definitions.
 */
export const routes = {
  home: '/',
  instruments: '/instruments',
  instrumentDetail: '/instruments/:instrumentId',
  siloDetail: '/silos/:siloId',
  chartDetail: '/charts/:chartId',
  chat: '/chat',
  chatWithInstrument: '/chat/:instrumentId',
  settings: '/settings',
} as const

/**
 * Helper to build routes with parameters.
 */
export function buildRoute(
  route: keyof typeof routes,
  params?: Record<string, string>
): string {
  let path: string = routes[route]
  
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      path = path.replace(`:${key}`, value)
    })
  }
  
  return path
}

