/**
 * CIA-SIE Frontend Type Definitions
 * 
 * Re-exports all types from individual files.
 * Import types from '@types' throughout the application.
 * 
 * GOVERNED BY: ADAPTER_FINANCIAL_SERVICES.md, BACKEND_ARCHITECTURAL_FLOWCHART.md
 * 
 * PROHIBITED FIELDS (not included in any type):
 * - weight: Enables aggregation (CR-002)
 * - score: Implies judgment (CR-002)
 * - confidence: Implies reliability ranking (CR-002)
 * - priority: Implies hierarchy (CR-002)
 * - rank: Implies superiority (CR-002)
 * - recommendation: Prescriptive content (CR-001, CR-003)
 */

// Enums
export {
  Direction,
  FreshnessStatus,
  SignalType,
  BasketType,
  NarrativeSectionType,
  ValidationStatus,
  AIModelTier,
  UsagePeriod,
  MessageRole,
} from './enums'

// Signal types
export type { Signal, SignalCreateRequest } from './signal'

// Instrument types
export type {
  Instrument,
  InstrumentCreateRequest,
  InstrumentUpdateRequest,
  Silo,
  SiloCreateRequest,
} from './instrument'

// Chart types
export type {
  Chart,
  ChartCreateRequest,
  ChartUpdateRequest,
} from './chart'

// Contradiction types
export type {
  Contradiction,
  ContradictionsResponse,
} from './contradiction'

// Confirmation types
export type {
  Confirmation,
  ConfirmationsResponse,
} from './confirmation'

// Narrative types
export type {
  NarrativeSection,
  Narrative,
  PlainNarrativeResponse,
  NarrativeParams,
} from './narrative'

// Freshness types
export type {
  ChartSignalStatus,
  RelationshipSummary,
  FreshnessThresholds,
} from './freshness'

// API types
export type {
  ChatRequest,
  StrategyEvaluateRequest,
  WebhookPayload,
  BasketCreateRequest,
  ChatResponse,
  StrategyEvaluateResponse,
  WebhookResponse,
  AIModelsResponse,
  AIBudgetResponse,
  AIHealthResponse,
  ConversationHistoryResponse,
  PlatformStatusResponse,
  PlatformSetupResponse,
  HealthStatus,
  ErrorResponse,
  AIModel,
  ChatMessage,
  AIUsage,
  AnalyticalBasket,
  Platform,
  InstrumentListParams,
  SiloListParams,
  ChartListParams,
  SignalListParams,
  UsageParams,
  HistoryParams,
} from './api'

