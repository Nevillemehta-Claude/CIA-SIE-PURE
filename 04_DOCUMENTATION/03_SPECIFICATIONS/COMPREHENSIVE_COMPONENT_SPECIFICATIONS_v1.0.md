# CIA-SIE Comprehensive Component Specifications v1.0

**Document ID:** SPEC-4B-001  
**Version:** 1.0  
**Date:** January 5, 2026  
**Status:** AUTHORITATIVE  
**Classification:** Technical Specification

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-05 | AI Assistant | Initial comprehensive specification |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Backend Component Specifications](#2-backend-component-specifications)
3. [Frontend Component Specifications](#3-frontend-component-specifications)
4. [Mission Control Console Specifications](#4-mission-control-console-specifications)
5. [API Contract Specifications](#5-api-contract-specifications)
6. [UI/UX Specifications](#6-uiux-specifications)
7. [Data Flow Specifications](#7-data-flow-specifications)
8. [Constitutional Enforcement Specifications](#8-constitutional-enforcement-specifications)
9. [Integration Specifications](#9-integration-specifications)
10. [Test Case Specifications](#10-test-case-specifications)
11. [Appendices](#11-appendices)

---

## 1. Executive Summary

This document provides comprehensive specifications for every component of the CIA-SIE platform, derived from the Phase 4A Forensic Codebase Analysis. It serves as the authoritative reference for:

- **Component Behavior**: What each component does and does not do
- **API Contracts**: Exact request/response schemas
- **UI Patterns**: Consistent user interface behaviors
- **Constitutional Enforcement**: How constitutional rules are enforced at each layer
- **Integration Points**: How components communicate

### Scope

| Layer | Components | Status |
|-------|------------|--------|
| Backend | 48 Python files across 7 modules | Specified |
| Frontend | 84 TypeScript/TSX files | Specified |
| MCC | 41 TypeScript files (Electron + React) | Specified |

---

## 2. Backend Component Specifications

### 2.1 Core Module (`src/cia_sie/core/`)

#### 2.1.1 Configuration (`config.py`)

**Purpose:** Centralized configuration management using Pydantic Settings.

**Specification:**

```yaml
Component: Settings
Type: Pydantic BaseSettings
Source: Environment variables + .env file
Caching: @lru_cache for singleton pattern

Configuration Categories:
  Application:
    - app_name: str = "CIA-SIE"
    - app_version: str = "2.3.0"
    - debug: bool = False
    - environment: str = "development"
  
  Database:
    - database_url: str = "sqlite+aiosqlite:///./data/cia_sie.db"
  
  API Server:
    - api_host: str = "0.0.0.0"
    - api_port: int = 8000
  
  AI Provider:
    - anthropic_api_key: Optional[str]
    - anthropic_model: str = "claude-3-5-sonnet-20241022"
    - ai_budget_limit: float = 50.0
    - ai_budget_alert_threshold: int = 80
    - ai_rate_limit_requests_per_minute: int = 20
    - ai_fallback_model: str = "claude-3-haiku-20240307"
  
  Webhook:
    - webhook_secret: Optional[str]
  
  Platform Integration:
    - kite_api_key: Optional[str]
    - kite_api_secret: Optional[str]
    - kite_redirect_uri: str
  
  Freshness Defaults:
    - default_current_threshold_min: int = 2
    - default_recent_threshold_min: int = 10
    - default_stale_threshold_min: int = 30
  
  CORS:
    - cors_origins: str = "http://localhost:3000,http://localhost:5173"

PROHIBITED Configuration (Constitutional):
  - aggregation_weights: NEVER ADD
  - scoring_thresholds: NEVER ADD
  - recommendation_rules: NEVER ADD
  - signal_priority_config: NEVER ADD
  - confidence_calculation_params: NEVER ADD
```

#### 2.1.2 Domain Models (`models.py`)

**Purpose:** Pydantic models representing core business entities.

**Specification:**

| Model | Fields | Constitutional Notes |
|-------|--------|---------------------|
| `Instrument` | instrument_id, symbol, display_name, created_at, updated_at, is_active, metadata | - |
| `Silo` | silo_id, instrument_id, silo_name, heartbeat_*, threshold_*, timestamps, is_active | Thresholds are DESCRIPTIVE only |
| `Chart` | chart_id, silo_id, chart_code, chart_name, timeframe, webhook_id, timestamps, is_active | **NO weight field** |
| `Signal` | signal_id, chart_id, received_at, signal_timestamp, signal_type, direction, indicators, raw_payload | **NO confidence/strength fields** |
| `AnalyticalBasket` | basket_id, basket_name, basket_type, description, instrument_id, chart_ids, timestamps | UI-only, NO processing impact |
| `Contradiction` | chart_a_*, chart_b_*, detected_at | Exposed, NEVER resolved |
| `Confirmation` | chart_a_*, chart_b_*, aligned_direction, detected_at | NOT weighted |
| `Narrative` | narrative_id, silo_id, sections, closing_statement, generated_at | MANDATORY closing statement |

**Behavioral Constraints:**

```
Chart:
  MUST NOT have: weight, priority, importance, rank
  ALL charts have EQUAL standing
  
Signal:
  MUST NOT have: confidence, strength, score, probability
  RAW data only - no system judgment
  
Narrative:
  MUST have closing_statement = "This is a description of what your charts 
  are showing. The interpretation and any decision is entirely yours."
```

#### 2.1.3 Enumerations (`enums.py`)

**Specification:**

| Enum | Values | Purpose |
|------|--------|---------|
| `SignalType` | HEARTBEAT, STATE_CHANGE, BAR_CLOSE, MANUAL | Signal origin classification |
| `Direction` | BULLISH, BEARISH, NEUTRAL | Signal directional bias |
| `FreshnessStatus` | CURRENT, RECENT, STALE, UNAVAILABLE | Data age (DESCRIPTIVE only) |
| `BasketType` | LOGICAL, HIERARCHICAL, CONTEXTUAL, CUSTOM | UI grouping only |
| `NarrativeSectionType` | SIGNAL_SUMMARY, CONTRADICTION, CONFIRMATION, FRESHNESS | Narrative structure |
| `ValidationStatus` | VALID, INVALID, REMEDIATED | AI response validation |
| `AIModelTier` | HAIKU, SONNET, OPUS | Claude model tiers |
| `UsagePeriod` | DAILY, WEEKLY, MONTHLY | Budget tracking periods |
| `MessageRole` | user, assistant | Chat conversation roles |

#### 2.1.4 Exceptions (`exceptions.py`)

**Specification:**

| Exception | Base | Purpose |
|-----------|------|---------|
| `CIASIEError` | Exception | Base for all custom exceptions |
| `InstrumentNotFoundError` | CIASIEError | Instrument lookup failed |
| `SiloNotFoundError` | CIASIEError | Silo lookup failed |
| `ChartNotFoundError` | CIASIEError | Chart lookup failed |
| `SignalNotFoundError` | CIASIEError | Signal lookup failed |
| `BasketNotFoundError` | CIASIEError | Basket lookup failed |
| `ValidationError` | CIASIEError | Input validation failed |
| `DuplicateError` | CIASIEError | Unique constraint violation |
| `InvalidWebhookPayloadError` | CIASIEError | Webhook payload invalid |
| `WebhookNotRegisteredError` | CIASIEError | webhook_id not found |
| `DatabaseError` | CIASIEError | Database operation failed |
| `AIProviderError` | CIASIEError | Claude API failed |
| `PlatformAdapterError` | CIASIEError | Platform integration failed |
| `ConstitutionalViolationError` | CIASIEError | **CRITICAL**: Code violates constitution |
| `AggregationAttemptError` | ConstitutionalViolationError | Attempted to aggregate signals |
| `RecommendationAttemptError` | ConstitutionalViolationError | Attempted to recommend |
| `ContradictionResolutionAttemptError` | ConstitutionalViolationError | Attempted to resolve contradiction |

#### 2.1.5 Security (`security.py`)

**Specification:**

```yaml
WebhookSignatureValidator:
  Algorithm: HMAC-SHA256
  Headers Checked:
    - x-tradingview-signature
    - x-webhook-signature
    - x-signature
  Timestamp Tolerance: 300 seconds (5 minutes)
  Signature Format: "sha256={hex_digest}"
  Comparison: Constant-time (hmac.compare_digest)

SecurityHeadersMiddleware:
  Headers Applied:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    - Referrer-Policy: strict-origin-when-cross-origin
    - Permissions-Policy: geolocation=(), microphone=(), camera=()
  Production-Only:
    - Strict-Transport-Security: max-age=31536000; includeSubDomains

RateLimitMiddleware:
  Webhook Limit: 60 requests/minute per IP
  API Limit: 100 requests/minute per IP
  Response on Exceed: 429 Too Many Requests
  Headers Added: X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After

SecurityEvent Logging:
  Events: AUTH_SUCCESS, AUTH_FAILURE, INVALID_SIGNATURE, MISSING_SIGNATURE,
          TIMESTAMP_EXPIRED, RATE_LIMIT_EXCEEDED, WEBHOOK_RECEIVED, SUSPICIOUS_REQUEST
  Format: JSON with timestamp, IP, event type, details
  Sanitization: Newlines/tabs removed from all logged values
```

---

### 2.2 Data Access Layer (`src/cia_sie/dal/`)

#### 2.2.1 Database Configuration (`database.py`)

**Specification:**

```yaml
Engine:
  Type: AsyncEngine (SQLAlchemy 2.0)
  URL: sqlite+aiosqlite:///./data/cia_sie.db
  Echo: Controlled by settings.debug
  
Session Factory:
  Type: async_sessionmaker[AsyncSession]
  expire_on_commit: False
  autoflush: False

Session Management:
  Context Manager: get_async_session()
  FastAPI Dependency: get_session_dependency()
  Transaction: Auto-commit on success, rollback on exception
```

#### 2.2.2 ORM Models (`models.py`)

**Specification:**

```yaml
InstrumentDB:
  Table: instruments
  Primary Key: instrument_id (UUID string)
  Columns:
    - symbol: String(50), unique, not null
    - display_name: String(100), not null
    - created_at: DateTime, default=utcnow
    - updated_at: DateTime, default=utcnow, onupdate=utcnow
    - is_active: Boolean, default=True
    - metadata_json: JSON, nullable
  Relationships:
    - silos: one-to-many with SiloDB
    - baskets: one-to-many with AnalyticalBasketDB

SiloDB:
  Table: silos
  Primary Key: silo_id (UUID string)
  Foreign Keys: instrument_id -> instruments.instrument_id
  Columns:
    - silo_name: String(100), not null
    - heartbeat_enabled: Boolean, default=True
    - heartbeat_frequency_min: Integer, default=5
    - current_threshold_min: Integer, default=2
    - recent_threshold_min: Integer, default=10
    - stale_threshold_min: Integer, default=30
    - timestamps, is_active
  Constraints:
    - UniqueConstraint(instrument_id, silo_name)
    - Index on instrument_id
  Relationships:
    - instrument: many-to-one with InstrumentDB
    - charts: one-to-many with ChartDB

ChartDB:
  Table: charts
  Primary Key: chart_id (UUID string)
  Foreign Keys: silo_id -> silos.silo_id
  Columns:
    - chart_code: String(50), not null
    - chart_name: String(100), not null
    - timeframe: String(10), not null
    - webhook_id: String(100), unique, not null
    - timestamps, is_active
  Constraints:
    - UniqueConstraint(silo_id, chart_code)
    - Index on silo_id
    - Index on webhook_id
  PROHIBITED COLUMNS:
    - weight: NEVER ADD
    - priority: NEVER ADD
    - importance: NEVER ADD
  Relationships:
    - silo: many-to-one with SiloDB
    - signals: one-to-many with SignalDB

SignalDB:
  Table: signals
  Primary Key: signal_id (UUID string)
  Foreign Keys: chart_id -> charts.chart_id
  Columns:
    - received_at: DateTime, default=utcnow, not null
    - signal_timestamp: DateTime, not null
    - signal_type: String(20), not null
    - direction: String(20), not null
    - indicators: JSON, default="{}"
    - raw_payload: JSON, default="{}"
  Constraints:
    - Index on chart_id
    - Index on signal_timestamp
  PROHIBITED COLUMNS:
    - confidence: NEVER ADD
    - strength: NEVER ADD
    - score: NEVER ADD
    - probability: NEVER ADD
  Relationships:
    - chart: many-to-one with ChartDB

AnalyticalBasketDB:
  Table: analytical_baskets
  Primary Key: basket_id (UUID string)
  Foreign Keys: instrument_id -> instruments.instrument_id (nullable)
  Columns:
    - basket_name: String(100), not null
    - basket_type: String(20), default="CUSTOM"
    - description: Text, nullable
    - timestamps, is_active
  CRITICAL: UI-only construct, NO processing impact

BasketChartDB:
  Table: basket_charts
  Primary Key: (basket_id, chart_id) composite
  Purpose: Many-to-many relationship

ConversationDB:
  Table: conversations
  Primary Key: conversation_id (UUID string)
  Purpose: AI chat history storage
  Columns:
    - instrument_id: Foreign key
    - messages: JSON array of {role, content, timestamp}
    - model_used: String(50)
    - total_tokens: Integer
    - total_cost: Numeric(10,6)

AIUsageDB:
  Table: ai_usage
  Primary Key: id (UUID string)
  Purpose: Token/cost tracking for budget management
  Columns:
    - period_type: DAILY/WEEKLY/MONTHLY
    - period_start/end: Date
    - input_tokens, output_tokens: Integer
    - total_cost: Numeric(10,6)
    - requests_count: Integer
    - model_breakdown: JSON
```

#### 2.2.3 Repositories (`repositories.py`)

**Specification:**

| Repository | Entity | Methods |
|------------|--------|---------|
| `InstrumentRepository` | InstrumentDB | get_by_id, get_by_symbol, get_all, get_with_silos, create, update, delete |
| `SiloRepository` | SiloDB | get_by_id, get_all, get_by_instrument, get_with_charts, get_with_full_hierarchy, create, delete |
| `ChartRepository` | ChartDB | get_by_id, get_by_webhook_id, get_all, get_by_silo, get_with_latest_signal, create, delete |
| `SignalRepository` | SignalDB | get_by_id, get_all, get_by_chart, get_latest_by_chart, get_latest_by_charts (batch), create, delete |
| `BasketRepository` | AnalyticalBasketDB | get_by_id, get_all, get_with_charts, get_by_instrument, create, add_chart_to_basket, remove_chart_from_basket, delete |

**Common Patterns:**
- All repositories use async/await
- Soft delete via is_active=False (except signals which are immutable)
- Duplicate detection before create
- Session passed via dependency injection

---

### 2.3 API Layer (`src/cia_sie/api/`)

#### 2.3.1 Application Factory (`app.py`)

**Specification:**

```yaml
Application:
  Framework: FastAPI
  Title: CIA-SIE API
  Description: Chart Intelligence Auditor & Signal Intelligence Engine
  Version: 2.3.0
  OpenAPI URL: /openapi.json
  Docs: /docs (Swagger UI)

Middleware Stack (order matters):
  1. RateLimitMiddleware
  2. SecurityHeadersMiddleware
  3. CORSMiddleware
     - origins: from settings.cors_origins_list
     - methods: ["*"]
     - headers: ["*"]
     - credentials: True

Routers Included:
  - /instruments (instruments.router)
  - /silos (silos.router)
  - /charts (charts.router)
  - /signals (signals.router)
  - /webhooks (webhooks.router)
  - /relationships (relationships.router)
  - /narratives (narratives.router)
  - /baskets (baskets.router)
  - /platforms (platforms.router)
  - /ai (ai.router)
  - /chat (chat.router)
  - /strategy (strategy.router)

Startup:
  - Initialize database (create tables)
  - Log startup message

Endpoints:
  - GET /health: Returns {"status": "healthy", ...}
  - GET /security-info (dev only): Returns security configuration
```

---

### 2.4 AI Services (`src/cia_sie/ai/`)

#### 2.4.1 Claude Client (`claude_client.py`)

**Specification:**

```yaml
ClaudeClient:
  Purpose: Async wrapper for Anthropic API
  
  Constructor:
    - api_key: Optional[str] (defaults to settings)
    - model: Optional[str] (defaults to settings)
  
  Methods:
    generate(system_prompt, user_prompt, max_tokens=2000, temperature=0.3) -> str
      - Creates message with system prompt
      - Returns text content from first response block
      - Raises AIProviderError on failure
    
    health_check() -> bool
      - Sends minimal test request
      - Returns True if accessible
```

#### 2.4.2 Response Validator (`response_validator.py`)

**Specification:**

```yaml
AIResponseValidator:
  Purpose: Constitutional compliance checking for AI outputs
  
  Constructor:
    - strict_mode: bool = True (CRITICAL violations always reject)
    - allow_remediation: bool = True (WARNING violations can be fixed)
    - log_violations: bool = True (audit trail)
  
  Prohibited Pattern Categories (30+ patterns):
    Recommendations:
      - "you should" (CRITICAL)
      - "I recommend" (CRITICAL)
      - "I suggest" (CRITICAL)
      - "consider buying/selling" (CRITICAL)
      - "you might want to" (CRITICAL)
      - "the best action/approach" (CRITICAL)
    
    Trading Actions:
      - "buy/sell now" (CRITICAL)
      - "enter long/short position" (CRITICAL)
      - "exit position" (CRITICAL)
      - "take profit" (CRITICAL)
      - "cut losses" (CRITICAL)
    
    Aggregation:
      - "overall direction is/shows" (CRITICAL)
      - "net signal/direction" (CRITICAL)
      - "consensus is/shows" (CRITICAL)
      - "majority of signals show" (CRITICAL)
      - "on balance" (WARNING)
    
    Confidence/Probability:
      - "confidence level/score: N" (CRITICAL)
      - "N% confident/probability" (CRITICAL)
      - "probability of/that" (CRITICAL)
      - "likely to rise/fall" (CRITICAL)
      - "high/low probability" (CRITICAL)
    
    Predictions:
      - "will likely rise/fall" (CRITICAL)
      - "expected to rise/fall" (CRITICAL)
      - "forecast is/shows" (CRITICAL)
      - "price target" (CRITICAL)
    
    Rankings:
      - "more reliable/accurate than" (CRITICAL)
      - "stronger/weaker signal" (CRITICAL)
      - "signal strength: N" (CRITICAL)
      - "risk score: N" (CRITICAL)
      - "rating N/N" (CRITICAL)
  
  Methods:
    validate(response: str) -> ValidationResult
      - Checks all prohibited patterns
      - Checks mandatory disclaimer
      - Returns is_valid, status, violations, remediated_text
    
    validate_or_raise(response: str) -> str
      - Raises ConstitutionalViolationError if invalid

ValidatedResponseGenerator:
  Purpose: Automatic retry on validation failure
  Max Retries: 3
  Strategy: Add stricter constraints to prompt, reduce temperature
```

#### 2.4.3 Narrative Generator (`narrative_generator.py`)

**Specification:**

```yaml
NarrativeGenerator:
  Purpose: Generate descriptive narratives for signal relationships
  
  Constructor:
    - claude_client: Optional[ClaudeClient]
    - prompt_builder: Optional[NarrativePromptBuilder]
    - validator: Optional[AIResponseValidator]
    - max_retries: int = 3
  
  Methods:
    generate_silo_narrative(summary: RelationshipSummary, use_validated_generator=True) -> Narrative
      - Builds prompt from summary
      - Generates via Claude with validation
      - Falls back to generate_fallback_narrative on failure
      - Returns Narrative with mandatory closing statement
    
    generate_chart_narrative(chart_status, instrument_symbol, use_validated_generator=True) -> Narrative
    
    generate_fallback_narrative(summary: RelationshipSummary) -> Narrative
      - No AI, pure template-based
      - Lists all charts with directions
      - Lists contradictions and confirmations
      - Always includes mandatory closing statement
  
  Required Closing Statement:
    "This is a description of what your charts are showing. 
     The interpretation and any decision is entirely yours."
```

---

### 2.5 Exposure Services (`src/cia_sie/exposure/`)

#### 2.5.1 Relationship Exposer (`relationship_exposer.py`)

**Specification:**

```yaml
RelationshipExposer:
  Purpose: Surface ALL signal relationships for display
  
  Constitutional Constraints:
    - Returns ALL charts (none hidden)
    - Returns ALL contradictions (none resolved)
    - Returns ALL confirmations (none weighted)
    - NO aggregation anywhere
    - NO scores anywhere
    - NO recommendations anywhere
  
  Constructor:
    - silo_repository: SiloRepository
    - chart_repository: ChartRepository
    - signal_repository: SignalRepository
    - contradiction_detector: Optional[ContradictionDetector]
    - confirmation_detector: Optional[ConfirmationDetector]
    - freshness_calculator: Optional[FreshnessCalculator]
  
  Methods:
    expose_for_silo(silo_id: str, as_of: Optional[datetime]) -> RelationshipSummary
      1. Get silo with full hierarchy
      2. For each active chart:
         a. Get latest signal
         b. Calculate freshness status
         c. Build ChartSignalStatus
      3. Detect all contradictions
      4. Detect all confirmations
      5. Return RelationshipSummary with everything exposed
    
    expose_for_instrument(instrument_id: str, as_of: Optional[datetime]) -> list[RelationshipSummary]
      - Returns summary for each silo of the instrument
```

#### 2.5.2 Contradiction Detector (`contradiction_detector.py`)

**Specification:**

```yaml
ContradictionDetector:
  Purpose: Identify BULLISH vs BEARISH conflicts
  
  Constitutional Constraints:
    - DETECTS contradictions only
    - NEVER resolves them
    - NEVER suggests which is "right"
    - NEVER weights or prioritizes
    - NEVER hides any contradiction
  
  Methods:
    detect(chart_statuses: Sequence[ChartSignalStatus]) -> list[Contradiction]
      - Filter to charts with non-NEUTRAL signals
      - Compare all pairs
      - BULLISH vs BEARISH = contradiction
      - Return ALL contradictions found
    
    _is_contradiction(direction_a, direction_b) -> bool
      - True if (BULLISH vs BEARISH) or (BEARISH vs BULLISH)
      - NEUTRAL never creates contradictions
```

#### 2.5.3 Confirmation Detector (`confirmation_detector.py`)

**Specification:**

```yaml
ConfirmationDetector:
  Purpose: Identify aligned signals
  
  Constitutional Constraints:
    - DOES NOT weight confirmations
    - More confirmations ≠ "stronger signal" (that's aggregation)
    - Purely informational
  
  Methods:
    detect(chart_statuses: Sequence[ChartSignalStatus]) -> list[Confirmation]
      - Filter to charts with non-NEUTRAL signals
      - Compare all pairs
      - Same direction = confirmation
      - Return ALL confirmations found
    
    group_by_direction(chart_statuses) -> dict[Direction, list[ChartSignalStatus]]
      - For DISPLAY only, not aggregation
```

---

### 2.6 Ingestion Services (`src/cia_sie/ingestion/`)

#### 2.6.1 Webhook Handler (`webhook_handler.py`)

**Specification:**

```yaml
WebhookHandler:
  Purpose: Receive and STORE signals
  
  Constitutional Constraints:
    DOES:
      - Validate JSON structure
      - Store signal in database
      - Return signal_id
    
    DOES NOT:
      - Aggregate signals
      - Compute scores
      - Make judgments
  
  Methods:
    process_webhook(payload: dict, received_at: Optional[datetime]) -> Signal
      1. Validate and normalize payload
      2. Find chart by webhook_id
      3. Create SignalDB record
      4. Store in database
      5. Return Signal domain model
    
    _validate_and_normalize(payload: dict) -> WebhookPayload
      - Required: webhook_id, direction
      - Optional: signal_type (default: STATE_CHANGE), timestamp (default: now)
      - Direction must be: BULLISH, BEARISH, or NEUTRAL
      - Extra fields become indicators

TradingViewPayloadAdapter:
  Purpose: Normalize TradingView-specific field names
  Field Mappings:
    - chart_id/chartId/chart/id -> webhook_id
    - bias/signal/trend -> direction
    - type/alertType -> signal_type
    - time/alertTime -> timestamp
```

#### 2.6.2 Freshness Calculator (`freshness.py`)

**Specification:**

```yaml
FreshnessCalculator:
  Purpose: Calculate DESCRIPTIVE freshness labels
  
  Constitutional Note:
    Freshness is DESCRIPTIVE only
    Does NOT invalidate or suppress data
    All data displayed regardless of freshness
  
  Methods:
    calculate(signal_timestamp, current_threshold_min, recent_threshold_min, stale_threshold_min, as_of) -> FreshnessStatus
      - age = as_of - signal_timestamp
      - if age < current_threshold: CURRENT
      - elif age < recent_threshold: RECENT
      - elif age < stale_threshold: STALE
      - else: UNAVAILABLE (but data still shown)
```

---

## 3. Frontend Component Specifications

### 3.1 Application Structure

**Specification:**

```yaml
Entry Point: main.tsx
  - Renders App within React.StrictMode
  - Wraps with QueryClientProvider

Root Component: App.tsx
  Router: BrowserRouter (React Router v6)
  Layout: AppShell (wraps all routes)
  
Routes:
  - / : HomePage
  - /instruments : InstrumentsPage
  - /instruments/:instrumentId : InstrumentDetailPage
  - /silos/:siloId : SiloDetailPage
  - /charts : ChartsReferencePage
  - /charts/:chartId : ChartDetailPage
  - /chat : ChatPage
  - /chat/:scripId : ChatPage (with instrument context)
  - /platforms : PlatformsPage
  - /baskets : BasketsPage
  - /settings : SettingsPage
  - * : NotFoundPage
```

### 3.2 Component Hierarchy

#### 3.2.1 Layout Components (`components/layout/`)

```yaml
AppShell:
  Purpose: Main application layout wrapper
  Contains: Header, Sidebar, main content area, SkipLink
  Responsibilities:
    - Responsive layout
    - Navigation state management
    - Accessibility landmarks

Header:
  Purpose: Top navigation bar
  Contains: Logo, navigation links, user menu
  
Sidebar:
  Purpose: Side navigation
  Contains: Navigation menu, quick links
  
PageHeader:
  Purpose: Page title and actions
  Props: title, subtitle, actions (ReactNode)

SkipLink:
  Purpose: Accessibility - skip to main content
  Behavior: Hidden until focused
```

#### 3.2.2 Common Components (`components/common/`)

```yaml
Button:
  Variants: primary, secondary, ghost, danger
  Sizes: sm, md, lg
  States: default, hover, active, disabled, loading
  Accessibility: role="button", aria-disabled, aria-busy

Card:
  Purpose: Container with consistent styling
  Props: title, children, actions, className
  
Badge:
  Purpose: Status/label display
  Variants: default, success, warning, error, info
  
Spinner:
  Purpose: Loading indicator
  Sizes: sm, md, lg
  Accessibility: role="status", aria-label="Loading"

ErrorState:
  Purpose: Error display with retry option
  Props: error, onRetry
  
EmptyState:
  Purpose: No-data display
  Props: title, description, action

Disclaimer:
  Purpose: Constitutional mandatory disclaimer
  CRITICAL SPECIFICATION:
    - Text is HARDCODED and IMMUTABLE
    - Component is NON-DISMISSIBLE
    - Component is NON-COLLAPSIBLE
    - MUST render with every AI/narrative output
  
  Hardcoded Text:
    "This is a description of what your charts are showing. 
     The interpretation and any decision is entirely yours."
  
  Variants:
    - block: Full-width aside with icon
    - inline: Italicized text
  
  Accessibility:
    - role="note"
    - aria-label="Important disclaimer"
    - aria-live="polite" (block variant)
```

#### 3.2.3 Signal Components (`components/signals/`)

```yaml
DirectionBadge:
  Purpose: Display signal direction with color coding
  Props: direction: Direction, size?: 'sm' | 'md' | 'lg'
  Colors:
    - BULLISH: Green (bg-emerald-500/20, text-emerald-400)
    - BEARISH: Red (bg-red-500/20, text-red-400)
    - NEUTRAL: Gray (bg-slate-500/20, text-slate-400)
  Constitutional Note:
    - ALL directions styled IDENTICALLY in structure
    - Only color differs
    - No direction styled as "better" or "worse"

FreshnessBadge:
  Purpose: Display data freshness status
  Props: freshness: FreshnessStatus
  Colors:
    - CURRENT: Green
    - RECENT: Yellow
    - STALE: Orange
    - UNAVAILABLE: Gray
  Constitutional Note:
    - Freshness is DESCRIPTIVE only
    - Does NOT imply data should be ignored

SignalCard:
  Purpose: Display single signal details
  Props: signal: Signal, chartName?: string
  Shows: direction, signal_type, timestamp, indicators

SignalList:
  Purpose: Display list of signals for a chart
  Props: signals: Signal[], loading?: boolean
```

#### 3.2.4 Relationship Components (`components/relationships/`)

```yaml
ContradictionCard:
  Purpose: Display detected contradiction
  CRITICAL SPECIFICATION (CBS-004):
    Layout: grid-cols-[1fr,auto,1fr]
      - EQUAL sizing for both sides
      - IDENTICAL styling for Chart A and Chart B
    Separator: Neutral arrows + "vs"
      - Implies NO preference
      - aria-hidden="true" (decorative)
    
  Accessibility:
    - article role with descriptive aria-label
    - group roles for each side
  
  Constitutional Requirement:
    - System EXPOSES contradictions
    - System NEVER RESOLVES them
    - Visual design must not suggest either side is "correct"

ContradictionPanel:
  Purpose: Container for multiple ContradictionCards
  Props: contradictions: Contradiction[]
  Empty State: "No contradictions detected"

ConfirmationCard:
  Purpose: Display detected confirmation
  Layout: Two charts showing same direction
  
ConfirmationPanel:
  Purpose: Container for multiple ConfirmationCards
  Props: confirmations: Confirmation[]
```

#### 3.2.5 AI Components (`components/ai/`)

```yaml
ChatInterface:
  Purpose: Per-instrument AI chat
  Props: scripId: string, initialMessages?: ChatMessage[]
  Features:
    - Message history display
    - Input field with submit
    - Model selector integration
    - Budget indicator
    - ALWAYS shows Disclaimer after assistant messages
  
ModelSelector:
  Purpose: Select Claude model tier
  Props: value: string, onChange: (model: string) => void
  Options: Haiku (fast/cheap), Sonnet (balanced), Opus (capable)
  Shows: Cost per 1K tokens, capabilities

BudgetIndicator:
  Purpose: Display AI budget status
  Props: usage: UsageInfo
  Shows: Percentage used, remaining budget, alert threshold warning
```

### 3.3 State Management

#### 3.3.1 React Query Configuration (`lib/queryClient.ts`)

```yaml
QueryClient Configuration:
  defaultOptions:
    queries:
      staleTime: 30000 (30 seconds)
      cacheTime: 300000 (5 minutes)
      retry: 3
      retryDelay: exponentialBackoff
      refetchOnWindowFocus: true
```

#### 3.3.2 Query Keys (`lib/queryKeys.ts`)

```yaml
Query Key Structure:
  instruments:
    all: ['instruments']
    byId: (id) => ['instruments', id]
    withSilos: (id) => ['instruments', id, 'silos']
  
  silos:
    all: ['silos']
    byId: (id) => ['silos', id]
    byInstrument: (instrumentId) => ['silos', 'instrument', instrumentId]
  
  charts:
    all: ['charts']
    byId: (id) => ['charts', id]
    bySilo: (siloId) => ['charts', 'silo', siloId]
  
  signals:
    byChart: (chartId) => ['signals', 'chart', chartId]
    latest: (chartId) => ['signals', 'chart', chartId, 'latest']
  
  relationships:
    bySilo: (siloId) => ['relationships', 'silo', siloId]
    byInstrument: (instrumentId) => ['relationships', 'instrument', instrumentId]
  
  narratives:
    bySilo: (siloId) => ['narratives', 'silo', siloId]
  
  ai:
    models: ['ai', 'models']
    usage: (period) => ['ai', 'usage', period]
    budget: ['ai', 'budget']
  
  chat:
    history: (scripId) => ['chat', scripId, 'history']
```

### 3.4 API Service Layer (`services/`)

**Specification:**

```yaml
Base Client (client.ts):
  Library: Axios
  baseURL: '/api/v1'
  Headers: Content-Type: application/json
  Interceptors: Error logging

Service Pattern:
  Each service file exports async functions
  Functions use apiRequest() helper for response extraction
  
Services:
  instruments.ts: CRUD operations for instruments
  silos.ts: CRUD operations for silos
  charts.ts: CRUD operations for charts
  signals.ts: Read operations for signals
  relationships.ts: Get relationship summaries
  narratives.ts: Generate/get narratives
  baskets.ts: CRUD operations for baskets
  platforms.ts: Platform adapter operations
  ai.ts: AI model/usage/budget operations
  chat.ts: Chat message operations
  strategy.ts: Strategy evaluation
```

### 3.5 Type Definitions (`types/`)

**Specification:**

```yaml
enums.ts:
  - Direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL'
  - SignalType: 'HEARTBEAT' | 'STATE_CHANGE' | 'BAR_CLOSE' | 'MANUAL'
  - FreshnessStatus: 'CURRENT' | 'RECENT' | 'STALE' | 'UNAVAILABLE'
  - BasketType: 'LOGICAL' | 'HIERARCHICAL' | 'CONTEXTUAL' | 'CUSTOM'
  - ModelTier: 'HAIKU' | 'SONNET' | 'OPUS'
  - ValidationStatus, NarrativeSectionType, UsagePeriod, MessageRole

models.ts:
  All domain interfaces matching backend Pydantic models
  INCLUDES Constitutional comments:
    - Chart: "// CONSTITUTIONAL: NO weight field"
    - Signal: "// CONSTITUTIONAL: NO confidence field"

api.ts:
  Request/Response types for API operations
```

---

## 4. Mission Control Console Specifications

### 4.1 Electron Main Process (`electron/main/`)

#### 4.1.1 Application Entry (`index.ts`)

**Specification:**

```yaml
Application Lifecycle:
  Startup:
    1. Request single instance lock (prevent duplicates)
    2. Initialize ConfigManager
    3. Initialize ProcessOrchestrator
    4. Initialize HealthMonitor
    5. Register all IPC handlers
    6. Create main window
    7. Create system tray
    8. Start health monitoring
  
  Shutdown:
    1. Stop health monitoring
    2. Force cleanup all managed processes
    3. Exit application

Single Instance:
  - Uses app.requestSingleInstanceLock()
  - Second instance focuses existing window

System Tray:
  Menu Items:
    - Show Mission Control
    - Start All Services
    - Stop All Services
    - Quit
  
Window Controls (IPC):
  - WINDOW_MINIMIZE
  - WINDOW_MAXIMIZE
  - WINDOW_CLOSE (respects minimize-to-tray setting)

Utility IPC:
  - SHELL_OPEN_EXTERNAL: Only localhost URLs allowed (Constitutional: MCR-002)
  - DIALOG_OPEN_DIRECTORY
  - APP_VERSION
  - APP_QUIT
```

#### 4.1.2 Process Orchestrator (`process/orchestrator.ts`)

**Specification:**

```yaml
ProcessOrchestrator:
  Purpose: Manage child processes for backend and frontend
  
  Process Configurations:
    Backend:
      command: venv/bin/python (or venv\\Scripts\\python.exe on Windows)
      args: ['-m', 'uvicorn', 'cia_sie.api.app:app', '--reload', '--port', '8000']
      cwd: projectRoot
      port: 8000
    
    Frontend:
      command: npm
      args: ['run', 'dev', '--', '--port', '5174']
      cwd: frontendPath
      port: 5174
  
  Process States:
    - stopped: Not running
    - starting: Spawning
    - running: Active and healthy
    - stopping: Graceful shutdown in progress
    - crashed: Exited with error
    - restarting: Stop + start cycle
  
  Methods:
    start(name: ProcessName): Promise<void>
      1. Acquire mutex lock (prevent concurrent starts)
      2. Check not already running
      3. Ensure port available (kill orphans if needed)
      4. Spawn child process
      5. Attach stdout/stderr handlers
      6. Update state and broadcast
    
    stop(name: ProcessName, graceful=true): Promise<void>
      1. Send SIGTERM
      2. Wait up to 5 seconds
      3. Force SIGKILL if not exited
    
    restart(name: ProcessName): Promise<void>
      - stop() then start()
    
    startAll(): Promise<void>
      - Start backend, wait 2s, start frontend
    
    stopAll(): Promise<void>
      - Stop both in parallel
    
    forceCleanup(): Promise<void>
      - Kill all processes immediately
      - Kill orphans on configured ports
      - Called on app shutdown
  
  Robustness Features:
    - Mutex locks prevent race conditions
    - Port availability check before start
    - Orphan process detection and cleanup
    - Process group cleanup on Unix
    - taskkill /F /T on Windows
```

#### 4.1.3 Health Monitor (`process/health.ts`)

**Specification:**

```yaml
HealthMonitor:
  Purpose: Periodic health checks on managed services
  
  Check Interval: Configurable (default 5000ms)
  
  Services Monitored:
    - backend: HTTP check to http://localhost:8000/health
    - frontend: HTTP check to http://localhost:5174/
    - database: Inferred from backend health response
  
  Health Status:
    - healthy: Service responding normally
    - degraded: 1-2 consecutive failures
    - unhealthy: 3+ consecutive failures
    - unknown: Process not running (not same as unhealthy)
  
  ServiceHealth Structure:
    - name: string
    - healthy: boolean
    - status: HealthStatus
    - lastCheck: timestamp
    - responseTime: ms
    - consecutiveFailures: number
    - details: optional metadata
  
  Methods:
    start(): Start periodic checks
    stop(): Stop periodic checks
    checkAll(): Check all services, broadcast results
    checkService(name, url): HTTP check with 3s timeout
    checkBackendDatabase(port): Infer from backend /health
  
  Broadcast:
    - Sends HEALTH_UPDATE to all windows
```

#### 4.1.4 IPC Channels (`ipc/channels.ts`)

**Specification:**

```yaml
IPC Channel Categories:
  Window:
    - window:minimize
    - window:maximize
    - window:close
    - window:isMaximized
  
  Process Management:
    - process:start
    - process:stop
    - process:restart
    - process:status
    - process:output (stream)
    - process:startAll
    - process:stopAll
    - process:restartAll
    - process:emergencyStop
  
  Logs:
    - log:stream (real-time)
    - log:clear
    - log:export
    - log:getAll
  
  Health:
    - health:update (broadcast)
    - health:check
  
  Configuration:
    - config:get
    - config:set
    - config:reset
  
  Utility:
    - shell:openExternal (localhost only)
    - dialog:openDirectory
    - app:version
    - app:quit
```

### 4.2 Renderer Process (`src/`)

#### 4.2.1 State Stores (Zustand)

**Specification:**

```yaml
processStore:
  State:
    - processes: Record<ProcessName, ProcessState>
    - isLoading: Record<ProcessName, boolean>
  
  Actions:
    - setProcessState(name, state)
    - setAllProcessStates(states)
    - setLoading(name, loading)
    - startProcess(name) - calls window.electron.startProcess
    - stopProcess(name)
    - restartProcess(name)
    - startAll()
    - stopAll()
    - restartAll()
    - emergencyStop()
    - refreshStatus()
  
  IPC Subscription:
    - Listens to window.electron.onProcessStatus
    - Auto-updates state on broadcasts

healthStore:
  State:
    - services: Record<string, ServiceHealth>
    - timestamp: number
  
  IPC Subscription:
    - Listens to window.electron.onHealthUpdate

logStore:
  State:
    - entries: LogEntry[]
    - filters: {level, source}
  
  Actions:
    - addEntry(entry)
    - clearLogs()
    - setFilter(filter)
    - exportLogs(format)

settingsStore:
  State:
    - ports: {backend, frontend}
    - paths: {projectRoot, frontend}
    - behavior: {minimizeToTray, healthCheckInterval, autoStart}
    - logging: {maxEntries}
  
  Persistence: Via IPC to ConfigManager

uiStore:
  State:
    - sidebarCollapsed: boolean
    - activeDialog: string | null
  Actions:
    - toggleSidebar()
    - openDialog(id)
    - closeDialog()
```

#### 4.2.2 Dashboard Components

**Specification:**

```yaml
StatusPanel:
  Purpose: Display process status at a glance
  Shows: Backend status, Frontend status, Database status
  Colors: Green (healthy), Yellow (degraded), Red (unhealthy), Gray (unknown)

MetricsPanel:
  Purpose: Display system metrics
  Shows: Uptime, Memory usage, CPU usage, Request counts

QuickActions:
  Purpose: One-click process controls
  Actions:
    - Start All
    - Stop All
    - Restart All
    - Emergency Stop (confirmation required)

RecentActivity:
  Purpose: Show recent log entries
  Shows: Last 10 entries with level, source, message
  Link: "View All" to full logs page
```

---

## 5. API Contract Specifications

### 5.1 Request/Response Schemas

#### 5.1.1 Instruments API

```yaml
GET /instruments:
  Query Parameters:
    - active_only: boolean = true
  Response: Instrument[]

POST /instruments:
  Request Body:
    symbol: string (required, 1-50 chars)
    display_name: string (required, 1-100 chars)
    metadata: object (optional)
  Response: Instrument (201 Created)
  Errors:
    - 409 Conflict: Symbol already exists

GET /instruments/{instrument_id}:
  Path Parameters:
    - instrument_id: string (UUID)
  Response: Instrument
  Errors:
    - 404 Not Found

PATCH /instruments/{instrument_id}:
  Request Body (all optional):
    display_name: string
    is_active: boolean
  Response: Instrument

DELETE /instruments/{instrument_id}:
  Response: 204 No Content
  Behavior: Soft delete (is_active = false)
```

#### 5.1.2 Webhooks API

```yaml
POST /webhooks:
  Headers Required (production):
    - X-Webhook-Signature: sha256={signature}
    - X-Webhook-Timestamp: {unix_timestamp} (optional but recommended)
  
  Request Body:
    webhook_id: string (required) - Must match registered chart
    direction: string (required) - BULLISH | BEARISH | NEUTRAL
    signal_type: string (optional) - default: STATE_CHANGE
    timestamp: string/number (optional) - ISO 8601 or Unix timestamp
    {additional fields}: become indicators
  
  Response:
    status: "accepted"
    signal_id: string (UUID)
    chart_id: string (UUID)
    direction: string
    received_at: string (ISO 8601)
  
  Errors:
    - 400 Bad Request: Invalid JSON, missing fields, invalid direction
    - 401 Unauthorized: Invalid signature (production only)
    - 404 Not Found: webhook_id not registered
  
  Constitutional Note:
    DOES: Store signal
    DOES NOT: Aggregate, score, or judge

POST /webhooks/manual:
  Same as POST /webhooks but forces signal_type = "MANUAL"
```

#### 5.1.3 Relationships API

```yaml
GET /relationships/silo/{silo_id}:
  Response: RelationshipSummary
    silo_id: string
    silo_name: string
    instrument_id: string
    instrument_symbol: string
    charts: ChartSignalStatus[]
    contradictions: Contradiction[]
    confirmations: Confirmation[]
    generated_at: string
  
  Constitutional Note:
    - Returns ALL charts (none hidden)
    - Returns ALL contradictions (none resolved)
    - Returns ALL confirmations (none weighted)

GET /relationships/instrument/{instrument_id}:
  Response: RelationshipSummary[] (one per silo)

GET /relationships/contradictions/silo/{silo_id}:
  Response:
    silo_id: string
    silo_name: string
    contradiction_count: number
    contradictions: array of {chart_a, chart_b} objects
    note: "These conflicting signals are presented for your review. 
           The system does not determine which signal is correct."
```

#### 5.1.4 Chat API

```yaml
POST /chat/{scrip_id}:
  Path Parameters:
    - scrip_id: string (instrument ID)
  
  Request Body:
    message: string (required, 1-2000 chars)
    model: string (optional) - Claude model ID
    include_context: boolean = true
    conversation_id: string (optional) - for continuity
  
  Response:
    conversation_id: string
    message:
      role: "assistant"
      content: string (AI response)
      timestamp: string
    context_used:
      signals_included: number
      charts_referenced: string[]
    usage:
      input_tokens: number
      output_tokens: number
      cost: number
      model_used: string
    disclaimer: "This is a description of what your charts are showing. 
                 The interpretation and any decision is entirely yours."
  
  Errors:
    - 404 Not Found: Instrument not found
    - 503 Service Unavailable: AI budget exhausted
  
  Constitutional Note:
    - All responses are DESCRIPTIVE only
    - NO recommendations, predictions, or trading advice
    - Mandatory disclaimer included in every response
```

#### 5.1.5 Strategy Evaluation API

```yaml
POST /strategy/evaluate:
  Request Body:
    scrip_id: string (required) - Instrument ID
    strategy_description: string (required, 10-1000 chars)
      Example: "I am considering entering a long position"
    model: string (optional) - Claude model ID
  
  Response:
    analysis:
      alignment_with_signals: string (descriptive text)
      contradictions_noted: string[]
      confirmations_noted: string[]
      freshness_concerns: string[]
    disclaimer: "This analysis describes how your stated strategy aligns 
                 with current chart signals. It is NOT a recommendation 
                 to proceed or not proceed. The decision is entirely yours."
    usage:
      input_tokens: number
      output_tokens: number
      cost: number
      model_used: string
  
  CRITICAL PROHIBITIONS:
    - MUST NEVER return recommendations
    - MUST NEVER return probability of success
    - MUST NEVER return risk scores
    - MUST NEVER use "you should" statements
```

---

## 6. UI/UX Specifications

### 6.1 Layout Specifications

```yaml
Application Layout:
  Type: Sidebar + Header + Content
  
  Header:
    Height: 64px
    Position: Fixed top
    Contents: Logo, Navigation, User Menu
  
  Sidebar:
    Width: 256px (expanded), 64px (collapsed)
    Position: Fixed left
    Collapsible: Yes
    Contents: Navigation menu
  
  Content Area:
    Position: Right of sidebar, below header
    Padding: 24px
    Max Width: 1400px (centered)
  
  Responsive Breakpoints:
    sm: 640px
    md: 768px
    lg: 1024px
    xl: 1280px
    2xl: 1536px
```

### 6.2 Color System

```yaml
Color Palette:
  Background:
    primary: slate-900 (#0f172a)
    secondary: slate-800 (#1e293b)
    tertiary: slate-700 (#334155)
  
  Text:
    primary: slate-100 (#f1f5f9)
    secondary: slate-300 (#cbd5e1)
    muted: slate-400 (#94a3b8)
  
  Accent:
    primary: blue-500 (#3b82f6)
    secondary: blue-400 (#60a5fa)
  
  Semantic:
    success: emerald-500 (#10b981)
    warning: amber-500 (#f59e0b)
    error: red-500 (#ef4444)
    info: blue-500 (#3b82f6)
  
  Direction Colors (Constitutional):
    BULLISH: emerald-500/400
    BEARISH: red-500/400
    NEUTRAL: slate-500/400
    
    Note: All directions have IDENTICAL structure
          Only color differs
          No direction styled as "better"
```

### 6.3 Typography

```yaml
Font Family:
  Sans: Inter, system-ui, sans-serif
  Mono: JetBrains Mono, monospace

Font Sizes:
  xs: 12px
  sm: 14px
  base: 16px
  lg: 18px
  xl: 20px
  2xl: 24px
  3xl: 30px
  4xl: 36px

Line Heights:
  tight: 1.25
  normal: 1.5
  relaxed: 1.75
```

### 6.4 Component Patterns

```yaml
Cards:
  Border Radius: 8px
  Background: slate-800
  Border: 1px solid slate-700
  Padding: 16px or 24px
  Shadow: sm or none

Buttons:
  Border Radius: 6px
  Padding: 8px 16px (md), 6px 12px (sm), 12px 24px (lg)
  Transition: 150ms
  Focus: ring-2 ring-offset-2

Inputs:
  Border Radius: 6px
  Border: 1px solid slate-600
  Background: slate-700
  Focus: border-blue-500

Badges:
  Border Radius: 9999px (pill)
  Padding: 2px 8px
  Font Size: xs or sm
```

### 6.5 Interaction Specifications

```yaml
Loading States:
  - Skeleton placeholders for content
  - Spinner for actions in progress
  - aria-busy="true" on loading elements

Error States:
  - ErrorState component with retry button
  - Toast notifications for non-blocking errors
  - Form validation inline

Empty States:
  - EmptyState component with helpful message
  - Clear call-to-action when applicable

Transitions:
  - 150ms for most interactions
  - 300ms for page transitions
  - ease-in-out timing function

Keyboard Navigation:
  - All interactive elements focusable
  - Tab order follows visual order
  - Escape closes modals/dropdowns
  - Enter activates buttons
```

---

## 7. Data Flow Specifications

### 7.1 Signal Ingestion Flow

```
TradingView Alert
      │
      ▼
┌─────────────────────┐
│  POST /webhooks     │
│  (HMAC validation)  │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  WebhookHandler     │
│  - Validate payload │
│  - Normalize format │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  ChartRepository    │
│  - Find by webhook  │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  SignalRepository   │
│  - Create signal    │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  SQLite Database    │
│  - signals table    │
└─────────────────────┘
      │
      ▼
   Response: { signal_id, chart_id, direction }
```

### 7.2 Relationship Exposure Flow

```
Frontend Request: GET /relationships/silo/{id}
      │
      ▼
┌─────────────────────┐
│ RelationshipExposer │
│ - Get silo + charts │
└─────────────────────┘
      │
      ├──────────────────────────────────┐
      ▼                                  ▼
┌─────────────────────┐    ┌─────────────────────┐
│  SignalRepository   │    │ FreshnessCalculator │
│  - Latest signals   │    │ - Calculate status  │
└─────────────────────┘    └─────────────────────┘
      │                                  │
      └──────────────┬───────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│         Build ChartSignalStatus[]           │
└─────────────────────────────────────────────┘
      │
      ├──────────────────────────────────┐
      ▼                                  ▼
┌─────────────────────┐    ┌─────────────────────┐
│ContradictionDetector│    │ConfirmationDetector │
│  - Detect conflicts │    │  - Detect alignment │
└─────────────────────┘    └─────────────────────┘
      │                                  │
      └──────────────┬───────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│           RelationshipSummary               │
│  - ALL charts (none hidden)                 │
│  - ALL contradictions (none resolved)       │
│  - ALL confirmations (none weighted)        │
└─────────────────────────────────────────────┘
```

### 7.3 AI Narrative Flow

```
Frontend Request: GET /narratives/silo/{id}
      │
      ▼
┌─────────────────────┐
│ RelationshipExposer │
│ - Get full summary  │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ NarrativePromptBuilder │
│ - Build system prompt  │
│ - Build user prompt    │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  ClaudeClient       │
│  - Send to API      │
│  - Get response     │
└─────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│         AIResponseValidator                  │
│  - Check 30+ prohibited patterns            │
│  - Verify mandatory disclaimer              │
│  - CRITICAL violations: REJECT              │
│  - WARNING violations: REMEDIATE            │
└─────────────────────────────────────────────┘
      │
      ▼ (if valid or remediated)
┌─────────────────────┐
│  Narrative          │
│  - sections[]       │
│  - closing_statement│
└─────────────────────┘
      │
      ▼ (if invalid after 3 retries)
┌─────────────────────┐
│ generate_fallback_  │
│ narrative()         │
│ - Template-based    │
│ - No AI needed      │
└─────────────────────┘
```

### 7.4 Frontend State Flow

```
Component Mount
      │
      ▼
┌─────────────────────┐
│  useQuery Hook      │
│  - Check cache      │
└─────────────────────┘
      │
      ├─ Cache hit ──────────────────────────┐
      │                                       │
      ▼ Cache miss                            │
┌─────────────────────┐                       │
│  API Service        │                       │
│  - axios.get()      │                       │
└─────────────────────┘                       │
      │                                       │
      ▼                                       │
┌─────────────────────┐                       │
│  Backend API        │                       │
└─────────────────────┘                       │
      │                                       │
      ▼                                       │
┌─────────────────────┐                       │
│  Cache Update       │◄──────────────────────┘
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Component Render   │
│  - Display data     │
└─────────────────────┘
```

---

## 8. Constitutional Enforcement Specifications

### 8.1 Enforcement Points

```yaml
Database Layer:
  ChartDB:
    - NO weight column
    - NO priority column
    - NO importance column
  SignalDB:
    - NO confidence column
    - NO strength column
    - NO score column
    - NO probability column
  
  Enforcement: Schema design prevents prohibited fields

Domain Model Layer:
  Chart:
    - Pydantic model has no weight field
    - Comments explicitly state prohibition
  Signal:
    - Pydantic model has no confidence/strength
    - Comments explicitly state prohibition
  
  Enforcement: Type system prevents prohibited attributes

API Layer:
  Webhooks:
    - Store only, no aggregation
    - Docstrings document DOES/DOES NOT
  Relationships:
    - Returns ALL, hides NONE
    - Returns contradictions unresolved
  Narratives:
    - Response validated before return
    - Fallback if validation fails
  Strategy:
    - Describes alignment only
    - Never recommends
  
  Enforcement: Business logic and documentation

AI Layer:
  Response Validator:
    - 30+ prohibited patterns
    - Regex matching (case-insensitive)
    - Mandatory disclaimer check
    - Retry with stricter constraints
  
  Enforcement: Runtime validation with rejection

Frontend Layer:
  Disclaimer Component:
    - Hardcoded, immutable text
    - Non-dismissible
    - Non-collapsible
  ContradictionCard:
    - Equal sizing for both sides
    - Identical styling
    - Neutral separator
  Type Definitions:
    - Comments mark prohibited fields
  
  Enforcement: Component design and type comments
```

### 8.2 Validation Patterns

```yaml
Prohibited Phrase Detection:
  Method: Compiled regex patterns
  Case: Case-insensitive
  Severity:
    - CRITICAL: Always reject, no remediation
    - WARNING: Attempt remediation, log
  
  Pattern Categories:
    1. Recommendation Language
    2. Trading Action Language
    3. Aggregation Language
    4. Confidence/Probability Language
    5. Prediction Language
    6. Ranking Language
  
  Total Patterns: 30+

Mandatory Disclaimer Verification:
  Required Text: "This is a description of what your charts are showing. 
                  The interpretation and any decision is entirely yours."
  
  Acceptable Variations:
    - "interpretation.*decision.*yours"
    - "decision.*entirely yours"
    - "interpretation.*yours"
  
  Missing: Treated as CRITICAL violation
```

---

## 9. Integration Specifications

### 9.1 MCC ↔ Backend/Frontend IPC

```yaml
Process Control Flow:
  
  Renderer → Main:
    window.electron.startProcess('backend')
    window.electron.stopProcess('frontend')
    window.electron.getProcessStatus()
  
  Main → Renderer:
    IPC_CHANNELS.PROCESS_STATUS broadcast
    IPC_CHANNELS.LOG_STREAM broadcast
    IPC_CHANNELS.HEALTH_UPDATE broadcast

Health Check Flow:
  
  Main Process:
    - HTTP GET http://localhost:8000/health (backend)
    - HTTP GET http://localhost:5174/ (frontend)
  
  Results Broadcast:
    - HEALTH_UPDATE channel to all windows
  
  Renderer Subscription:
    - healthStore.services updated automatically

Log Aggregation:
  
  Child Process → Main:
    - stdout/stderr captured
    - Parsed into LogEntry
  
  Main → Renderer:
    - LOG_STREAM channel
    - logStore.entries updated
```

### 9.2 Frontend ↔ Backend API

```yaml
Connection:
  Protocol: HTTP
  Base URL: /api/v1 (proxied by Vite in development)
  Content-Type: application/json

Authentication:
  Currently: None (single-user desktop app)
  Webhooks: HMAC-SHA256 signature

Error Handling:
  4xx Errors:
    - Display user-friendly message
    - Log to console
  5xx Errors:
    - Display generic error
    - Show retry option
  Network Errors:
    - Show offline indicator
    - Retry with exponential backoff

Caching:
  React Query:
    - staleTime: 30 seconds
    - cacheTime: 5 minutes
    - Automatic refetch on window focus
```

### 9.3 Backend ↔ Claude API

```yaml
Connection:
  Provider: Anthropic
  Library: anthropic Python SDK (AsyncAnthropic)
  Authentication: API key in environment

Request Format:
  model: claude-3-5-sonnet-20241022 (configurable)
  max_tokens: 2000 (typical)
  temperature: 0.3 (factual/descriptive)
  system: Constitutional constraints
  messages: [{"role": "user", "content": "..."}]

Response Processing:
  1. Extract text from response.content[0].text
  2. Validate against prohibited patterns
  3. Check for mandatory disclaimer
  4. If invalid: retry up to 3 times
  5. If still invalid: use fallback narrative

Error Handling:
  - AIProviderError on API failure
  - Fallback narrative if AI unavailable
  - Budget check before each request
```

### 9.4 Backend ↔ Platform Adapters

```yaml
TradingView:
  Type: Webhook-based
  Authentication: HMAC-SHA256
  Payload Normalization: TradingViewPayloadAdapter
  
  Webhook URL Format:
    http://your-domain/api/v1/webhooks
  
  Expected Payload:
    {
      "webhook_id": "CHART_01",
      "direction": "BULLISH",
      "signal_type": "STATE_CHANGE",
      ...indicators
    }

Kite Connect (Zerodha):
  Type: OAuth 2.0 + REST API
  Authentication Flow:
    1. Redirect to Kite login page
    2. User authorizes app
    3. Callback with request_token
    4. Exchange for access_token
    5. Store token in adapter
  
  Capabilities:
    - Watchlist import
    - Instrument lookup
  
  Note: Does NOT auto-execute trades (Constitutional)
```

---

## 10. Test Case Specifications

### 10.1 Unit Test Specifications

```yaml
Backend Unit Tests:
  Location: tests/unit/

  Domain Models (test_models.py):
    - test_instrument_creation_valid
    - test_instrument_symbol_validation
    - test_silo_threshold_validation
    - test_chart_no_weight_attribute
    - test_signal_no_confidence_attribute
    - test_direction_enum_values
    - test_freshness_enum_values
  
  Repositories (test_repositories.py):
    - test_instrument_repository_create
    - test_instrument_repository_duplicate_symbol
    - test_silo_repository_by_instrument
    - test_chart_repository_by_webhook_id
    - test_signal_repository_latest_by_chart
    - test_basket_repository_add_chart
  
  Services (test_services.py):
    - test_freshness_calculator_current
    - test_freshness_calculator_stale
    - test_contradiction_detector_finds_conflict
    - test_contradiction_detector_neutral_ignored
    - test_confirmation_detector_finds_alignment
    - test_webhook_handler_validates_payload
    - test_webhook_handler_rejects_invalid_direction
  
  AI Validation (test_response_validator.py):
    - test_rejects_you_should
    - test_rejects_i_recommend
    - test_rejects_buy_now
    - test_rejects_overall_direction
    - test_rejects_confidence_score
    - test_rejects_price_prediction
    - test_requires_mandatory_disclaimer
    - test_remediation_adds_disclaimer
    - test_valid_response_passes

Frontend Unit Tests:
  Location: frontend/test/

  Hooks:
    - test_useInstruments_fetches_data
    - test_useRelationships_returns_summary
    - test_useChat_sends_message
  
  Components:
    - test_DirectionBadge_renders_bullish
    - test_DirectionBadge_renders_bearish
    - test_Disclaimer_is_non_dismissible
    - test_ContradictionCard_equal_sizing
```

### 10.2 Integration Test Specifications

```yaml
API Integration Tests:
  Location: tests/integration/

  Webhook Flow:
    - test_webhook_to_signal_storage
    - test_webhook_invalid_signature_rejected
    - test_webhook_unknown_id_returns_404
  
  Relationship Flow:
    - test_silo_relationships_returns_all_charts
    - test_contradictions_detected_correctly
    - test_confirmations_detected_correctly
  
  Narrative Flow:
    - test_narrative_includes_disclaimer
    - test_narrative_falls_back_on_ai_failure
```

### 10.3 Constitutional Compliance Tests

```yaml
Schema Compliance:
  - test_chart_table_has_no_weight_column
  - test_signal_table_has_no_confidence_column
  - test_schema_migration_rejects_prohibited_columns

Model Compliance:
  - test_chart_model_rejects_weight_attribute
  - test_signal_model_rejects_confidence_attribute

API Compliance:
  - test_relationships_returns_all_contradictions
  - test_relationships_does_not_resolve
  - test_narrative_has_mandatory_disclaimer

AI Compliance:
  - test_validator_catches_all_prohibited_patterns
  - test_validator_retries_on_failure
  - test_fallback_narrative_is_compliant
```

### 10.4 E2E Test Specifications

```yaml
Critical User Flows:
  
  Instrument Creation:
    1. Navigate to /instruments
    2. Click "Add Instrument"
    3. Fill symbol and display_name
    4. Submit form
    5. Verify instrument appears in list
  
  Signal Reception:
    1. Create instrument, silo, chart
    2. Send webhook with valid payload
    3. Navigate to chart detail page
    4. Verify signal displayed
    5. Verify direction badge correct
  
  Contradiction Display:
    1. Create silo with 2 charts
    2. Send BULLISH to chart A
    3. Send BEARISH to chart B
    4. Navigate to silo detail
    5. Verify ContradictionCard displayed
    6. Verify equal sizing (measure DOM)
  
  AI Chat:
    1. Navigate to /chat/{instrument_id}
    2. Enter question
    3. Submit
    4. Verify response appears
    5. Verify Disclaimer component visible
    6. Verify disclaimer is not dismissible
```

---

## 11. Appendices

### 11.1 Constitutional Rules Reference

| Code | Rule | Enforcement |
|------|------|-------------|
| CR-001 | Decision-support, not decision-making | API docs, AI validation |
| CR-002 | Expose contradictions, never resolve | RelationshipExposer, ContradictionCard |
| CR-003 | Mandatory disclaimer | Response validator, Disclaimer component |
| P-01 | No signal aggregation | No aggregation code exists |
| P-02 | No chart weights | No weight column in schema |
| P-03 | No contradiction resolution | Detector only, no resolver |
| P-04 | No recommendations | 30+ prohibited patterns |
| P-05 | No confidence scores | No confidence column in schema |
| MCR-001 | IPC validation | Defined channels only |
| MCR-002 | URL restrictions | Localhost only for shell.openExternal |

### 11.2 File Inventory

| Layer | Directory | File Count |
|-------|-----------|------------|
| Backend Core | src/cia_sie/core/ | 5 |
| Backend DAL | src/cia_sie/dal/ | 4 |
| Backend API | src/cia_sie/api/ | 14 |
| Backend AI | src/cia_sie/ai/ | 6 |
| Backend Exposure | src/cia_sie/exposure/ | 4 |
| Backend Ingestion | src/cia_sie/ingestion/ | 3 |
| Backend Platforms | src/cia_sie/platforms/ | 5 |
| Frontend Components | frontend/src/components/ | 30 |
| Frontend Hooks | frontend/src/hooks/ | 14 |
| Frontend Pages | frontend/src/pages/ | 12 |
| Frontend Services | frontend/src/services/ | 14 |
| MCC Main | mission-control/electron/main/ | 9 |
| MCC Renderer | mission-control/src/ | 32 |
| **TOTAL** | | **173** |

---

**Document Status:** COMPLETE  
**Next Phase:** Implementation validation and test execution

---

*This specification is the authoritative reference for CIA-SIE component behavior, API contracts, and constitutional compliance. All development work must conform to these specifications.*

