/**
 * Custom React Hooks
 *
 * Re-exports all custom hooks.
 */

// Data hooks
export {
  useInstruments,
  useInstrument,
  useCreateInstrument,
  useUpdateInstrument,
  useDeleteInstrument,
  instrumentKeys
} from './useInstruments'

export {
  useSilos,
  useSilosByInstrument,
  useSilo,
  useCreateSilo,
  useDeleteSilo,
  siloKeys
} from './useSilos'

export {
  useCharts,
  useChartsBySilo,
  useChart,
  useCreateChart,
  useUpdateChart,
  useDeleteChart,
  chartKeys
} from './useCharts'

export {
  useSignalsByChart,
  useLatestSignal,
  signalKeys
} from './useSignals'

export {
  useRelationshipSummary,
  useContradictions,
  useInstrumentRelationships,
  relationshipKeys
} from './useRelationships'

export {
  useSiloNarrative,
  useSiloNarrativePlain,
  useChartNarrative,
  narrativeKeys
} from './useNarratives'

// Utility hooks
export {
  useConstitutionalValidation,
  type ValidationResult
} from './useConstitutionalValidation'

export {
  useFreshness,
  useFreshnessMultiple,
  calculateFreshness
} from './useFreshness'

