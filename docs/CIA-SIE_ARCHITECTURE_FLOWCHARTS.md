# CIA-SIE Application Architecture Flowcharts

> **Chart Intelligence Auditor & Signal Intelligence Engine**
> Professional Architecture Documentation

---

## Table of Contents

1. [High-Level System Architecture](#1-high-level-system-architecture)
2. [Data Model Entity Relationship](#2-data-model-entity-relationship)
3. [Signal Ingestion Flow](#3-signal-ingestion-flow)
4. [Contradiction & Confirmation Detection](#4-contradiction--confirmation-detection)
5. [AI Narrative Generation Pipeline](#5-ai-narrative-generation-pipeline)
6. [Zerodha Kite OAuth Integration](#6-zerodha-kite-oauth-integration)
7. [Constitutional Rules Decision Tree](#7-constitutional-rules-decision-tree)
8. [API Endpoint Structure](#8-api-endpoint-structure)
9. [Complete User Journey](#9-complete-user-journey)
10. [Component Dependency Graph](#10-component-dependency-graph)

---

## 1. High-Level System Architecture

### C4 Context Diagram

```mermaid
C4Context
    title CIA-SIE System Context Diagram

    Person(trader, "Trader", "Financial analyst using the system for decision support")

    System(ciasie, "CIA-SIE", "Chart Intelligence Auditor & Signal Intelligence Engine")

    System_Ext(tradingview, "TradingView", "Chart analysis platform sending webhook signals")
    System_Ext(kite, "Zerodha Kite", "Brokerage platform for watchlist import")
    System_Ext(claude, "Claude AI", "Anthropic's AI for narrative generation")

    Rel(trader, ciasie, "Views signals, contradictions, narratives")
    Rel(tradingview, ciasie, "Sends webhook signals", "HTTPS/JSON")
    Rel(ciasie, kite, "OAuth, imports watchlist", "HTTPS/REST")
    Rel(ciasie, claude, "Generates narratives", "HTTPS/API")
```

### Layered Architecture

```mermaid
flowchart TB
    subgraph External["External Layer"]
        TV[TradingView Webhooks]
        KITE[Zerodha Kite API]
        CLAUDE[Claude AI API]
    end

    subgraph API["API Layer (FastAPI)"]
        INST_API["/api/v1/instruments"]
        SILO_API["/api/v1/silos"]
        CHART_API["/api/v1/charts"]
        SIG_API["/api/v1/signals"]
        PLAT_API["/api/v1/platforms"]
    end

    subgraph Business["Business Logic Layer"]
        SIG_SVC[Signal Service]
        EXP_ENG[Exposure Engine]
        NAR_GEN[Narrative Generator]
        KITE_ADAPT[Kite Adapter]
    end

    subgraph Data["Data Access Layer"]
        INST_REPO[Instrument Repository]
        SILO_REPO[Silo Repository]
        CHART_REPO[Chart Repository]
        SIG_REPO[Signal Repository]
    end

    subgraph Storage["Storage Layer"]
        DB[(SQLite Database)]
    end

    TV --> SIG_API
    KITE --> PLAT_API

    INST_API --> INST_REPO
    SILO_API --> SILO_REPO
    CHART_API --> CHART_REPO
    SIG_API --> SIG_SVC
    PLAT_API --> KITE_ADAPT

    SIG_SVC --> SIG_REPO
    SIG_SVC --> EXP_ENG
    EXP_ENG --> NAR_GEN
    NAR_GEN --> CLAUDE
    KITE_ADAPT --> KITE

    INST_REPO --> DB
    SILO_REPO --> DB
    CHART_REPO --> DB
    SIG_REPO --> DB

    style External fill:#e1f5fe
    style API fill:#fff3e0
    style Business fill:#f3e5f5
    style Data fill:#e8f5e9
    style Storage fill:#fce4ec
```

---

## 2. Data Model Entity Relationship

```mermaid
erDiagram
    INSTRUMENT ||--o{ SILO : contains
    SILO ||--o{ CHART : contains
    CHART ||--o{ SIGNAL : receives

    INSTRUMENT {
        uuid id PK
        string symbol UK
        string name
        string exchange
        string instrument_type
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    SILO {
        uuid id PK
        uuid instrument_id FK
        string name
        string description
        string timeframe_group
        json metadata
        datetime created_at
        datetime updated_at
    }

    CHART {
        uuid id PK
        uuid silo_id FK
        string timeframe
        string chart_type
        string tradingview_url
        boolean is_active
        json settings
        datetime created_at
        datetime updated_at
    }

    SIGNAL {
        uuid id PK
        uuid chart_id FK
        string signal_type
        string direction
        float price
        float strength
        string indicator_name
        json indicator_data
        string source
        datetime timestamp
        datetime created_at
    }
```

### Hierarchy Visualization

```mermaid
flowchart TD
    subgraph Instrument["INSTRUMENT (e.g., RELIANCE)"]
        I[Symbol: RELIANCE<br/>Exchange: NSE<br/>Type: Equity]
    end

    subgraph Silos["SILOS (Timeframe Groups)"]
        S1[Intraday Silo<br/>1m, 5m, 15m charts]
        S2[Swing Silo<br/>1H, 4H, Daily charts]
        S3[Positional Silo<br/>Weekly, Monthly charts]
    end

    subgraph Charts["CHARTS (Individual Timeframes)"]
        C1[1-Minute Chart]
        C2[5-Minute Chart]
        C3[15-Minute Chart]
        C4[1-Hour Chart]
        C5[4-Hour Chart]
        C6[Daily Chart]
    end

    subgraph Signals["SIGNALS (From TradingView)"]
        SIG1[RSI Oversold<br/>Direction: BULLISH]
        SIG2[MACD Cross<br/>Direction: BEARISH]
        SIG3[Support Break<br/>Direction: BEARISH]
        SIG4[EMA Golden Cross<br/>Direction: BULLISH]
    end

    I --> S1
    I --> S2
    I --> S3

    S1 --> C1
    S1 --> C2
    S1 --> C3
    S2 --> C4
    S2 --> C5
    S2 --> C6

    C1 --> SIG1
    C2 --> SIG2
    C4 --> SIG3
    C6 --> SIG4

    style Instrument fill:#bbdefb
    style Silos fill:#c8e6c9
    style Charts fill:#fff9c4
    style Signals fill:#ffccbc
```

---

## 3. Signal Ingestion Flow

### Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant TV as TradingView
    participant WH as Webhook Endpoint
    participant VAL as Signal Validator
    participant SVC as Signal Service
    participant REPO as Signal Repository
    participant DB as Database
    participant EXP as Exposure Engine

    TV->>WH: POST /api/v1/signals/webhook
    Note over TV,WH: JSON payload with signal data

    WH->>VAL: Validate payload schema

    alt Invalid Payload
        VAL-->>WH: ValidationError
        WH-->>TV: 422 Unprocessable Entity
    else Valid Payload
        VAL-->>WH: Validated SignalCreate
        WH->>SVC: create_signal(signal_data)

        SVC->>SVC: Lookup chart_id from payload
        SVC->>REPO: save(signal)
        REPO->>DB: INSERT INTO signals
        DB-->>REPO: Signal created
        REPO-->>SVC: Signal object

        SVC->>EXP: analyze_exposures(chart_id)
        Note over EXP: Async background task

        SVC-->>WH: Signal created
        WH-->>TV: 201 Created
    end
```

### Signal Processing Pipeline

```mermaid
flowchart LR
    subgraph Input["Signal Input"]
        RAW[Raw Webhook<br/>JSON Payload]
    end

    subgraph Validation["Validation Stage"]
        SCHEMA[Schema Validation<br/>Pydantic Models]
        ENUM[Enum Validation<br/>signal_type, direction]
        REF[Reference Validation<br/>chart_id exists?]
    end

    subgraph Processing["Processing Stage"]
        ENRICH[Data Enrichment<br/>Add timestamps, IDs]
        NORM[Normalization<br/>Standardize values]
    end

    subgraph Storage["Storage Stage"]
        PERSIST[Persist to DB<br/>Signal Repository]
    end

    subgraph Analysis["Analysis Stage"]
        EXPOSE[Exposure Engine<br/>Contradiction Check]
        NARR[Narrative Trigger<br/>If needed]
    end

    RAW --> SCHEMA
    SCHEMA --> ENUM
    ENUM --> REF
    REF --> ENRICH
    ENRICH --> NORM
    NORM --> PERSIST
    PERSIST --> EXPOSE
    EXPOSE --> NARR

    style Input fill:#e3f2fd
    style Validation fill:#fff8e1
    style Processing fill:#f3e5f5
    style Storage fill:#e8f5e9
    style Analysis fill:#ffebee
```

---

## 4. Contradiction & Confirmation Detection

### Detection Logic Flowchart

```mermaid
flowchart TD
    START([New Signal Received]) --> FETCH[Fetch all signals<br/>for same instrument]

    FETCH --> GROUP[Group signals by<br/>chart/timeframe]

    GROUP --> COMPARE{Compare<br/>directions}

    COMPARE -->|Same Direction<br/>Different Timeframes| CONF[CONFIRMATION<br/>Detected]
    COMPARE -->|Opposite Direction<br/>Different Timeframes| CONTRA[CONTRADICTION<br/>Detected]
    COMPARE -->|Same Direction<br/>Same Timeframe| REINFORCE[Signal<br/>Reinforcement]
    COMPARE -->|No Related<br/>Signals| ISOLATED[Isolated<br/>Signal]

    CONF --> WEIGHT_C[Calculate<br/>Confirmation Weight]
    CONTRA --> WEIGHT_X[Calculate<br/>Contradiction Weight]

    WEIGHT_C --> STORE_EXP[Store Exposure<br/>Record]
    WEIGHT_X --> STORE_EXP
    REINFORCE --> STORE_EXP
    ISOLATED --> STORE_EXP

    STORE_EXP --> NOTIFY[Trigger UI<br/>Notification]

    style CONF fill:#c8e6c9,stroke:#2e7d32
    style CONTRA fill:#ffcdd2,stroke:#c62828
    style REINFORCE fill:#fff9c4,stroke:#f9a825
    style ISOLATED fill:#e1f5fe,stroke:#0277bd
```

### Exposure Engine State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle: System Start

    Idle --> Analyzing: New Signal

    Analyzing --> CheckingContradictions: Fetch Related Signals

    CheckingContradictions --> ContradictionFound: Opposite Directions
    CheckingContradictions --> ConfirmationFound: Same Directions
    CheckingContradictions --> NoExposure: No Related Signals

    ContradictionFound --> GeneratingAlert: Create Alert
    ConfirmationFound --> GeneratingAlert: Create Alert
    NoExposure --> Idle: Return

    GeneratingAlert --> TriggerNarrative: If threshold met
    GeneratingAlert --> Idle: Below threshold

    TriggerNarrative --> Idle: Narrative queued
```

### Contradiction Example

```mermaid
flowchart LR
    subgraph Daily["Daily Chart"]
        D_SIG[EMA Golden Cross<br/>Direction: BULLISH<br/>Strength: 0.8]
    end

    subgraph Hourly["1-Hour Chart"]
        H_SIG[RSI Overbought<br/>Direction: BEARISH<br/>Strength: 0.7]
    end

    subgraph FiveMin["5-Min Chart"]
        M_SIG[MACD Bearish Cross<br/>Direction: BEARISH<br/>Strength: 0.6]
    end

    D_SIG -.->|CONTRADICTS| H_SIG
    D_SIG -.->|CONTRADICTS| M_SIG
    H_SIG -->|CONFIRMS| M_SIG

    subgraph Result["Exposure Result"]
        RES[Mixed Signal State<br/>Long-term: Bullish<br/>Short-term: Bearish<br/>⚠️ CONTRADICTION ALERT]
    end

    D_SIG --> Result
    H_SIG --> Result
    M_SIG --> Result

    style D_SIG fill:#c8e6c9
    style H_SIG fill:#ffcdd2
    style M_SIG fill:#ffcdd2
    style Result fill:#fff3e0
```

---

## 5. AI Narrative Generation Pipeline

### Generation Flow

```mermaid
sequenceDiagram
    autonumber
    participant UI as User Interface
    participant API as Narrative API
    participant SVC as Narrative Service
    participant EXP as Exposure Engine
    participant FILTER as Constitutional Filter
    participant CLAUDE as Claude AI
    participant DB as Database

    UI->>API: GET /narratives/{instrument_id}
    API->>SVC: generate_narrative(instrument_id)

    SVC->>EXP: get_current_exposures()
    EXP-->>SVC: Exposure data

    SVC->>SVC: Build context prompt
    Note over SVC: Include signals, contradictions,<br/>timeframes, indicators

    SVC->>CLAUDE: Generate narrative
    CLAUDE-->>SVC: Raw AI response

    SVC->>FILTER: apply_constitutional_rules(response)

    alt Contains Prohibited Patterns
        FILTER->>FILTER: Remove "should", "recommend", etc.
        FILTER->>FILTER: Add mandatory disclaimer
        FILTER-->>SVC: Filtered narrative
    else Clean Response
        FILTER-->>SVC: Approved narrative
    end

    SVC->>DB: Cache narrative
    SVC-->>API: NarrativeResponse
    API-->>UI: JSON with narrative + disclaimer
```

### Constitutional Filtering Pipeline

```mermaid
flowchart TD
    RAW[Raw AI Response] --> CHECK1{Contains<br/>'should'?}

    CHECK1 -->|Yes| REMOVE1[Remove/Replace<br/>with descriptive]
    CHECK1 -->|No| CHECK2

    REMOVE1 --> CHECK2{Contains<br/>'recommend'?}

    CHECK2 -->|Yes| REMOVE2[Remove/Replace<br/>with descriptive]
    CHECK2 -->|No| CHECK3

    REMOVE2 --> CHECK3{Contains<br/>'suggest'?}

    CHECK3 -->|Yes| REMOVE3[Remove/Replace<br/>with descriptive]
    CHECK3 -->|No| CHECK4

    REMOVE3 --> CHECK4{Resolves<br/>contradiction?}

    CHECK4 -->|Yes| REJECT[REJECT<br/>Regenerate]
    CHECK4 -->|No| DISCLAIMER

    REJECT --> RAW

    DISCLAIMER[Add Mandatory<br/>Disclaimer] --> OUTPUT[Compliant<br/>Narrative Output]

    style RAW fill:#e3f2fd
    style REJECT fill:#ffcdd2
    style OUTPUT fill:#c8e6c9
    style DISCLAIMER fill:#fff9c4
```

---

## 6. Zerodha Kite OAuth Integration

### OAuth Flow Sequence

```mermaid
sequenceDiagram
    autonumber
    participant User as User Browser
    participant App as CIA-SIE Backend
    participant Kite as Kite Connect API

    User->>App: Click "Connect Kite"
    App->>App: Generate state token
    App-->>User: Redirect to Kite login

    User->>Kite: Login with credentials
    Kite->>Kite: Authenticate user
    Kite-->>User: Redirect with request_token

    User->>App: GET /callback?request_token=xxx
    App->>Kite: Exchange request_token for access_token
    Note over App,Kite: POST /session/token

    Kite-->>App: access_token + user info
    App->>App: Store tokens securely
    App-->>User: Success! Connected

    Note over User,Kite: Subsequent API Calls

    User->>App: Import watchlist
    App->>Kite: GET /portfolio/holdings
    Note over App,Kite: Authorization: token xxx
    Kite-->>App: Holdings data
    App->>App: Create instruments from holdings
    App-->>User: Watchlist imported
```

### Kite Integration State Diagram

```mermaid
stateDiagram-v2
    [*] --> Disconnected

    Disconnected --> Redirecting: User clicks Connect
    Redirecting --> AwaitingCallback: Redirect to Kite

    AwaitingCallback --> ExchangingToken: Callback received
    AwaitingCallback --> Disconnected: User cancels

    ExchangingToken --> Connected: Token valid
    ExchangingToken --> Error: Token invalid

    Error --> Disconnected: Retry

    Connected --> Importing: Import watchlist
    Importing --> Connected: Import complete
    Importing --> Error: Import failed

    Connected --> Disconnected: Token expired
    Connected --> Disconnected: User disconnects
```

---

## 7. Constitutional Rules Decision Tree

### Rule 1: Decision-Support NOT Decision-Making

```mermaid
flowchart TD
    INPUT[AI Output Text] --> SCAN1{Contains<br/>'should'?}

    SCAN1 -->|Yes| FAIL1[❌ VIOLATION<br/>Rule 1]
    SCAN1 -->|No| SCAN2{Contains<br/>'recommend'?}

    SCAN2 -->|Yes| FAIL1
    SCAN2 -->|No| SCAN3{Contains<br/>'suggest'?}

    SCAN3 -->|Yes| FAIL1
    SCAN3 -->|No| SCAN4{Contains<br/>'must'?}

    SCAN4 -->|Yes| FAIL1
    SCAN4 -->|No| SCAN5{Contains<br/>'buy/sell<br/>imperative'?}

    SCAN5 -->|Yes| FAIL1
    SCAN5 -->|No| PASS1[✅ PASS<br/>Rule 1]

    FAIL1 --> REWRITE[Rewrite as<br/>descriptive statement]
    REWRITE --> INPUT

    style FAIL1 fill:#ffcdd2
    style PASS1 fill:#c8e6c9
    style REWRITE fill:#fff9c4
```

### Rule 2: Expose Contradictions, NEVER Resolve

```mermaid
flowchart TD
    CONTRA[Contradiction<br/>Detected] --> DISPLAY{How to<br/>display?}

    DISPLAY --> EQUAL[Equal Visual Weight<br/>Both directions shown]
    DISPLAY --> UNEQUAL[One direction<br/>emphasized]

    EQUAL --> CHECK_RES{Does AI<br/>resolve it?}
    UNEQUAL --> FAIL2[❌ VIOLATION<br/>Rule 2]

    CHECK_RES -->|"'Despite X, Y is stronger'"| FAIL2
    CHECK_RES -->|"'X exists, Y also exists'"| PASS2[✅ PASS<br/>Rule 2]

    FAIL2 --> REBALANCE[Rebalance to<br/>equal weight]
    REBALANCE --> EQUAL

    style FAIL2 fill:#ffcdd2
    style PASS2 fill:#c8e6c9
    style EQUAL fill:#e8f5e9
    style UNEQUAL fill:#ffcdd2
```

### Rule 3: Descriptive AI, NOT Prescriptive

```mermaid
flowchart TD
    NARRATIVE[AI Narrative] --> HAS_DISC{Has<br/>Disclaimer?}

    HAS_DISC -->|No| ADD_DISC[Add Mandatory<br/>Disclaimer]
    HAS_DISC -->|Yes| CHECK_TONE{Tone<br/>Check}

    ADD_DISC --> CHECK_TONE

    CHECK_TONE --> DESCRIPTIVE["'RSI is at 75'<br/>'MACD crossed'"]
    CHECK_TONE --> PRESCRIPTIVE["'RSI suggests overbought'<br/>'MACD indicates buy'"]

    DESCRIPTIVE --> PASS3[✅ PASS<br/>Rule 3]
    PRESCRIPTIVE --> FAIL3[❌ VIOLATION<br/>Rule 3]

    FAIL3 --> CONVERT[Convert to<br/>pure description]
    CONVERT --> DESCRIPTIVE

    style PASS3 fill:#c8e6c9
    style FAIL3 fill:#ffcdd2
    style ADD_DISC fill:#fff9c4
    style DESCRIPTIVE fill:#e8f5e9
    style PRESCRIPTIVE fill:#ffcdd2
```

### Allowed vs Prohibited Language

```mermaid
flowchart LR
    subgraph Prohibited["❌ PROHIBITED"]
        P1["'You should buy'"]
        P2["'We recommend selling'"]
        P3["'This suggests going long'"]
        P4["'The indicator says buy'"]
        P5["'Despite bearish signals,<br/>bullish trend is stronger'"]
    end

    subgraph Allowed["✅ ALLOWED"]
        A1["'RSI is at 30'"]
        A2["'Price crossed above EMA'"]
        A3["'MACD histogram is positive'"]
        A4["'Daily shows bullish,<br/>hourly shows bearish'"]
        A5["'Volume increased 50%'"]
    end

    style Prohibited fill:#ffcdd2
    style Allowed fill:#c8e6c9
```

---

## 8. API Endpoint Structure

### Endpoint Hierarchy

```mermaid
flowchart TD
    ROOT["/api/v1"] --> INST["/instruments"]
    ROOT --> SILO["/silos"]
    ROOT --> CHART["/charts"]
    ROOT --> SIG["/signals"]
    ROOT --> PLAT["/platforms"]

    INST --> INST_LIST["GET / - List all"]
    INST --> INST_CREATE["POST / - Create"]
    INST --> INST_GET["GET /{id} - Get one"]
    INST --> INST_UPDATE["PUT /{id} - Update"]
    INST --> INST_DELETE["DELETE /{id} - Delete"]
    INST --> INST_SILOS["GET /{id}/silos - Get silos"]

    SILO --> SILO_LIST["GET / - List all"]
    SILO --> SILO_CREATE["POST / - Create"]
    SILO --> SILO_GET["GET /{id} - Get one"]
    SILO --> SILO_CHARTS["GET /{id}/charts - Get charts"]

    CHART --> CHART_LIST["GET / - List all"]
    CHART --> CHART_CREATE["POST / - Create"]
    CHART --> CHART_GET["GET /{id} - Get one"]
    CHART --> CHART_SIGNALS["GET /{id}/signals - Get signals"]

    SIG --> SIG_LIST["GET / - List all"]
    SIG --> SIG_WEBHOOK["POST /webhook - TradingView"]
    SIG --> SIG_GET["GET /{id} - Get one"]

    PLAT --> KITE_LOGIN["GET /kite/login - Start OAuth"]
    PLAT --> KITE_CALLBACK["GET /kite/callback - OAuth callback"]
    PLAT --> KITE_STATUS["GET /kite/status - Check connection"]
    PLAT --> KITE_IMPORT["POST /kite/import - Import watchlist"]

    style ROOT fill:#e3f2fd
    style INST fill:#fff9c4
    style SILO fill:#f3e5f5
    style CHART fill:#e8f5e9
    style SIG fill:#ffccbc
    style PLAT fill:#b2dfdb
```

### Request/Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant Router as FastAPI Router
    participant Deps as Dependencies
    participant Service as Service Layer
    participant Repo as Repository
    participant DB as Database

    Client->>Router: HTTP Request
    Router->>Deps: Inject dependencies
    Note over Deps: DB Session, Auth, etc.
    Deps-->>Router: Dependencies ready

    Router->>Service: Business logic call
    Service->>Repo: Data access call
    Repo->>DB: SQL Query
    DB-->>Repo: Result set
    Repo-->>Service: Domain objects
    Service-->>Router: Response DTO
    Router-->>Client: HTTP Response
```

---

## 9. Complete User Journey

### End-to-End State Diagram

```mermaid
stateDiagram-v2
    [*] --> Landing: Open Application

    Landing --> ConnectKite: Click Connect Kite
    Landing --> ManualSetup: Manual instrument setup

    ConnectKite --> KiteOAuth: Redirect to Kite
    KiteOAuth --> WatchlistImport: OAuth Success
    KiteOAuth --> Landing: OAuth Failed

    WatchlistImport --> InstrumentsReady: Instruments created
    ManualSetup --> InstrumentsReady: Manual entry

    InstrumentsReady --> ConfigureSilos: Organize timeframes
    ConfigureSilos --> ConfigureCharts: Add charts to silos
    ConfigureCharts --> SetupWebhooks: Configure TradingView

    SetupWebhooks --> AwaitingSignals: Webhooks active

    state AwaitingSignals {
        [*] --> Listening
        Listening --> ProcessSignal: Signal received
        ProcessSignal --> CheckExposure: Signal stored
        CheckExposure --> Listening: No contradiction
        CheckExposure --> AlertUser: Contradiction found
        AlertUser --> Listening: Alert acknowledged
    }

    AwaitingSignals --> ViewDashboard: Check status
    ViewDashboard --> ViewNarrative: Request AI analysis
    ViewNarrative --> ViewDashboard: Analysis complete

    ViewDashboard --> AwaitingSignals: Continue monitoring
```

### User Journey Flowchart

```mermaid
flowchart TD
    START([User Opens App]) --> CONNECT{Connect<br/>Kite?}

    CONNECT -->|Yes| OAUTH[Complete Kite<br/>OAuth Flow]
    CONNECT -->|No| MANUAL[Manual Instrument<br/>Entry]

    OAUTH --> IMPORT[Import Watchlist<br/>from Kite]
    IMPORT --> INSTRUMENTS[Instruments<br/>Created]
    MANUAL --> INSTRUMENTS

    INSTRUMENTS --> SILOS[Create Silos<br/>Group by Timeframe]

    SILOS --> CHARTS[Add Charts<br/>to Each Silo]

    CHARTS --> WEBHOOKS[Configure TradingView<br/>Webhooks]

    WEBHOOKS --> LIVE[System Goes Live<br/>Awaiting Signals]

    LIVE --> SIGNAL[Signal Received<br/>from TradingView]

    SIGNAL --> PROCESS[Signal Processed<br/>& Stored]

    PROCESS --> EXPOSURE{Exposure<br/>Check}

    EXPOSURE -->|Contradiction| ALERT[⚠️ Contradiction<br/>Alert Displayed]
    EXPOSURE -->|Confirmation| CONFIRM[✅ Confirmation<br/>Indicator]
    EXPOSURE -->|Isolated| STORE[Signal Stored<br/>No Alert]

    ALERT --> DASH[View Dashboard]
    CONFIRM --> DASH
    STORE --> DASH

    DASH --> NARRATIVE{Request AI<br/>Narrative?}

    NARRATIVE -->|Yes| GENERATE[Generate Narrative<br/>with Disclaimer]
    NARRATIVE -->|No| LIVE

    GENERATE --> READ[Read Descriptive<br/>Analysis]
    READ --> DECIDE[User Makes<br/>Own Decision]
    DECIDE --> LIVE

    style START fill:#e3f2fd
    style ALERT fill:#ffcdd2
    style CONFIRM fill:#c8e6c9
    style GENERATE fill:#fff9c4
    style DECIDE fill:#e8f5e9
```

---

## 10. Component Dependency Graph

### Module Dependencies

```mermaid
flowchart TD
    subgraph API["API Layer"]
        APP[app.py<br/>FastAPI Application]
        ROUTES[routes/<br/>Endpoint Definitions]
        DEPS[dependencies.py<br/>Dependency Injection]
    end

    subgraph Services["Service Layer"]
        INST_SVC[instrument_service.py]
        SILO_SVC[silo_service.py]
        CHART_SVC[chart_service.py]
        SIG_SVC[signal_service.py]
        EXP_SVC[exposure_service.py]
        NARR_SVC[narrative_service.py]
    end

    subgraph Core["Core Layer"]
        CONFIG[config.py<br/>Settings]
        MODELS[models.py<br/>SQLAlchemy]
        SCHEMAS[schemas.py<br/>Pydantic]
        CONST[constitutional.py<br/>Rules Engine]
    end

    subgraph Platforms["Platform Adapters"]
        KITE_ADAPT[kite.py<br/>Kite Connect]
        TV_ADAPT[tradingview.py<br/>Webhook Parser]
    end

    subgraph External["External"]
        CLAUDE_API[Claude API]
        KITE_API[Kite Connect API]
    end

    APP --> ROUTES
    ROUTES --> DEPS
    DEPS --> Services

    Services --> Core
    Services --> Platforms

    NARR_SVC --> CONST
    NARR_SVC --> CLAUDE_API
    KITE_ADAPT --> KITE_API

    style API fill:#e3f2fd
    style Services fill:#fff9c4
    style Core fill:#f3e5f5
    style Platforms fill:#e8f5e9
    style External fill:#ffccbc
```

### Data Flow Summary

```mermaid
flowchart LR
    TV[TradingView] -->|Webhook| SIG[Signal API]
    KITE[Kite Connect] -->|OAuth + Data| PLAT[Platform API]

    SIG --> DB[(Database)]
    PLAT --> DB

    DB --> EXP[Exposure Engine]
    EXP --> NARR[Narrative Generator]
    NARR --> CLAUDE[Claude AI]

    CLAUDE --> FILTER[Constitutional Filter]
    FILTER --> UI[User Interface]

    UI -->|Read Only| DB

    style TV fill:#e3f2fd
    style KITE fill:#e3f2fd
    style CLAUDE fill:#e3f2fd
    style FILTER fill:#ffcdd2
    style UI fill:#c8e6c9
```

---

## Appendix: File Structure

```
src/cia_sie/
├── api/
│   ├── app.py                 # FastAPI application
│   ├── dependencies.py        # Dependency injection
│   └── routes/
│       ├── instruments.py     # Instrument endpoints
│       ├── silos.py           # Silo endpoints
│       ├── charts.py          # Chart endpoints
│       ├── signals.py         # Signal endpoints
│       └── platforms.py       # Platform endpoints
├── core/
│   ├── config.py              # Application settings
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   └── constitutional.py      # Constitutional rules
├── services/
│   ├── instrument_service.py  # Instrument business logic
│   ├── silo_service.py        # Silo business logic
│   ├── chart_service.py       # Chart business logic
│   ├── signal_service.py      # Signal business logic
│   ├── exposure_service.py    # Exposure detection
│   └── narrative_service.py   # AI narrative generation
├── platforms/
│   ├── kite.py                # Kite Connect adapter
│   └── tradingview.py         # TradingView webhook parser
└── repositories/
    ├── instrument_repo.py     # Instrument data access
    ├── silo_repo.py           # Silo data access
    ├── chart_repo.py          # Chart data access
    └── signal_repo.py         # Signal data access
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Compliant / Allowed |
| ❌ | Violation / Prohibited |
| ⚠️ | Warning / Alert |
| 🔒 | Security / Auth Required |
| 📊 | Data / Analytics |
| 🤖 | AI / Automation |

---

*Generated for CIA-SIE v1.0 - Chart Intelligence Auditor & Signal Intelligence Engine*
