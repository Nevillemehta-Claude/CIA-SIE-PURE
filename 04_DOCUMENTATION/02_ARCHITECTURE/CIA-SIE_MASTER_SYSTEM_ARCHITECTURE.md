# CIA-SIE MASTER SYSTEM ARCHITECTURE
## Comprehensive Design & Data Flow Specification
### Mission-Critical Precision Level

---

| **Document Metadata** | **Value** |
|----------------------|-----------|
| **Document ID** | CIA-SIE-ARCH-MASTER-001 |
| **Version** | 1.0.0 |
| **Classification** | MISSION CRITICAL |
| **Date Created** | January 5, 2026 |
| **Author** | Claude Opus 4.5 |
| **Validation Passes** | 6 (See Appendix Z) |
| **Constitutional Compliance** | CR-001, CR-002, CR-003 ✅ |
| **MCC Compliance** | MCR-001 through MCR-005 ✅ |

---

# TABLE OF CONTENTS

1. [System Overview & Philosophy](#1-system-overview--philosophy)
2. [Master Architecture Diagram](#2-master-architecture-diagram)
3. [Component Layer Breakdown](#3-component-layer-breakdown)
4. [Data Flow Diagrams](#4-data-flow-diagrams)
5. [State Machine Diagrams](#5-state-machine-diagrams)
6. [Entity Relationship Diagrams](#6-entity-relationship-diagrams)
7. [Sequence Diagrams](#7-sequence-diagrams)
8. [Constitutional Enforcement Checkpoints](#8-constitutional-enforcement-checkpoints)
9. [MCC ↔ Backend Integration Map](#9-mcc--backend-integration-map)
10. [Frontend ↔ Backend Integration Map](#10-frontend--backend-integration-map)
11. [Error Handling & Recovery Flows](#11-error-handling--recovery-flows)
12. [Security Architecture](#12-security-architecture)
13. [Appendix: Validation Evidence](#appendix-validation-evidence)

---

# 1. SYSTEM OVERVIEW & PHILOSOPHY

## 1.1 Foundational Decision (ADR-001)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CIA-SIE is a DATA REPOSITORY, not an INTELLIGENCE ENGINE                   ║
║                                                                               ║
║   ┌───────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                       │   ║
║   │   WHAT WE DO:                    WHAT WE NEVER DO:                   │   ║
║   │   ═══════════                    ════════════════                    │   ║
║   │                                                                       │   ║
║   │   ✓ Store signals with          ✗ Aggregate signals into            │   ║
║   │     full fidelity                  composite scores                  │   ║
║   │                                                                       │   ║
║   │   ✓ EXPOSE contradictions       ✗ RESOLVE contradictions            │   ║
║   │     showing both sides             by weighting/prioritizing         │   ║
║   │                                                                       │   ║
║   │   ✓ Provide DESCRIPTIVE         ✗ Provide PRESCRIPTIVE              │   ║
║   │     AI narratives                  recommendations                   │   ║
║   │                                                                       │   ║
║   │   ✓ Display information         ✗ Suggest, recommend, or            │   ║
║   │     for user interpretation        imply any action                  │   ║
║   │                                                                       │   ║
║   │   ✓ Preserve USER AUTHORITY     ✗ Make decisions for the user       │   ║
║   │                                                                       │   ║
║   └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
║   This philosophy permeates EVERY layer of the system.                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 1.2 System Purpose

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CIA-SIE ECOSYSTEM PURPOSE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   The CIA-SIE system exists to:                                              │
│                                                                              │
│   1. RECEIVE trading signals from TradingView via webhooks                   │
│   2. STORE all signals with complete fidelity and provenance                 │
│   3. ORGANIZE signals by Instrument → Silo → Chart hierarchy                 │
│   4. DETECT contradictions (opposing signals) and confirmations              │
│   5. EXPOSE relationships without resolving or weighting                     │
│   6. GENERATE AI narratives that DESCRIBE (never prescribe)                  │
│   7. DISPLAY freshness of all signals with visual indicators                 │
│   8. PRESENT information for the USER to interpret and decide                │
│                                                                              │
│   The USER is a sophisticated trader who:                                    │
│   • Has their own trading methodology                                        │
│   • Wants data organized, NOT interpreted                                    │
│   • Makes their OWN decisions based on their expertise                       │
│   • Does NOT want the system to "think for them"                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.3 The Three Constitutional Rules (INVIOLABLE)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ⚖️ CONSTITUTIONAL RULES (INVIOLABLE) ⚖️                   │
│                                                                              │
│   ANY VIOLATION OF THESE RULES RENDERS THE SYSTEM NON-COMPLIANT              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ╔═══════════════════════════════════════════════════════════════════════╗ │
│   ║ CR-001: DECISION-SUPPORT ONLY                                         ║ │
│   ╠═══════════════════════════════════════════════════════════════════════╣ │
│   ║                                                                       ║ │
│   ║  The system provides INFORMATION, never RECOMMENDATIONS.              ║ │
│   ║                                                                       ║ │
│   ║  FORBIDDEN:                      REQUIRED:                            ║ │
│   ║  • "should", "recommend"         • "shows", "displays"                ║ │
│   ║  • "suggest", "consider"         • "indicates", "is"                  ║ │
│   ║  • Buy/Sell/Enter/Exit buttons   • View/Explore buttons only          ║ │
│   ║  • Action-oriented language      • Descriptive language               ║ │
│   ║                                                                       ║ │
│   ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                              │
│   ╔═══════════════════════════════════════════════════════════════════════╗ │
│   ║ CR-002: EXPOSE CONTRADICTIONS, NEVER RESOLVE THEM                     ║ │
│   ╠═══════════════════════════════════════════════════════════════════════╣ │
│   ║                                                                       ║ │
│   ║  When charts disagree, show BOTH with EQUAL visual weight.            ║ │
│   ║                                                                       ║ │
│   ║  FORBIDDEN:                      REQUIRED:                            ║ │
│   ║  • Chart weighting (weight: 2.5) • Equal visual prominence            ║ │
│   ║  • Signal scoring (score: 85%)   • Side-by-side display               ║ │
│   ║  • Aggregation ("Overall: BUY")  • No resolution language             ║ │
│   ║  • "Consensus", "net sentiment"  • "Contradiction detected"           ║ │
│   ║                                                                       ║ │
│   ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                              │
│   ╔═══════════════════════════════════════════════════════════════════════╗ │
│   ║ CR-003: DESCRIPTIVE AI, NOT PRESCRIPTIVE AI                           ║ │
│   ╠═══════════════════════════════════════════════════════════════════════╣ │
│   ║                                                                       ║ │
│   ║  AI describes what data shows, never what to do.                      ║ │
│   ║                                                                       ║ │
│   ║  FORBIDDEN:                      REQUIRED:                            ║ │
│   ║  • "I recommend..."              • "The data shows..."                ║ │
│   ║  • "You should..."               • "Chart X indicates..."             ║ │
│   ║  • Predictions/forecasts         • Factual descriptions               ║ │
│   ║  • Probability percentages       • MANDATORY DISCLAIMER               ║ │
│   ║                                                                       ║ │
│   ║  ┌────────────────────────────────────────────────────────────────┐   ║ │
│   ║  │ MANDATORY DISCLAIMER (must appear on ALL AI output):           │   ║ │
│   ║  │                                                                │   ║ │
│   ║  │ "This analysis is generated by AI for informational purposes  │   ║ │
│   ║  │  only. It does not constitute financial advice. All trading   │   ║ │
│   ║  │  decisions are solely your responsibility."                   │   ║ │
│   ║  └────────────────────────────────────────────────────────────────┘   ║ │
│   ║                                                                       ║ │
│   ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.4 MCC-Specific Constitutional Rules

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MCC CONSTITUTIONAL RULES (INVIOLABLE)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   MCR-001: NO AUTO-TRADE                                                     │
│   ─────────────────────                                                      │
│   MCC may control processes but NEVER execute trades automatically.          │
│   No trade execution APIs may be integrated.                                  │
│                                                                              │
│   MCR-002: NO EXTERNAL NETWORK CALLS                                          │
│   ───────────────────────────────────                                         │
│   MCC may NOT make network calls except to localhost services.               │
│   Forbidden: Telemetry, cloud APIs, analytics, auto-updates.                 │
│                                                                              │
│   MCR-003: GRACEFUL DEGRADATION                                               │
│   ─────────────────────────────                                               │
│   MCC must remain functional even if child processes fail.                   │
│   UI must never crash due to backend unavailability.                         │
│                                                                              │
│   MCR-004: EXPLICIT USER ACTIONS                                              │
│   ─────────────────────────────                                               │
│   All actions require explicit user click. No auto-start on launch.          │
│   No automatic process restarts without user confirmation.                   │
│                                                                              │
│   MCR-005: AUDIT TRAIL LOGGING                                                │
│   ───────────────────────────                                                 │
│   All user actions must be logged with timestamp.                            │
│   Process state changes must be recorded.                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 2. MASTER ARCHITECTURE DIAGRAM

## 2.1 Complete System Overview

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                                               ║
║                                           CIA-SIE COMPLETE SYSTEM ARCHITECTURE                                                 ║
║                                           ═══════════════════════════════════                                                  ║
║                                                                                                                               ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐     ║
║   │                                                                                                                     │     ║
║   │                                      CONSOLIDATED GUI LAYER                                                          │     ║
║   │                                      ════════════════════════                                                        │     ║
║   │                                                                                                                     │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │                          MISSION CONTROL CONSOLE (MCC)                                                    │     │     ║
║   │   │                          Electron 35.x + React 19.x                                                       │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ┌─────────────────────────────────┐   ┌─────────────────────────────────────────────────────────────┐   │     │     ║
║   │   │   │                                 │   │                                                             │   │     │     ║
║   │   │   │      MAIN PROCESS               │   │               RENDERER PROCESS                              │   │     │     ║
║   │   │   │      (Node.js)                  │   │               (React/Zustand)                               │   │     │     ║
║   │   │   │                                 │   │                                                             │   │     │     ║
║   │   │   │  ┌───────────────────────────┐  │   │   ┌────────────────┐  ┌────────────────┐  ┌─────────────┐   │   │     │     ║
║   │   │   │  │ Process Orchestrator      │  │   │   │ Dashboard Page │  │ Processes Page │  │ Logs Page   │   │   │     │     ║
║   │   │   │  │ • spawn/kill processes    │  │   │   │ • SystemStatus │  │ • ServiceGrid  │  │ • LogViewer │   │   │     │     ║
║   │   │   │  │ • stdout/stderr capture   │  │   │   │ • QuickActions │  │ • ProcessCards │  │ • Filters   │   │   │     │     ║
║   │   │   │  └───────────────────────────┘  │   │   └────────────────┘  └────────────────┘  └─────────────┘   │   │     │     ║
║   │   │   │                                 │   │                                                             │   │     │     ║
║   │   │   │  ┌───────────────────────────┐  │   │   ┌────────────────┐  ┌────────────────┐  ┌─────────────┐   │   │     │     ║
║   │   │   │  │ Health Monitor            │  │   │   │ Frontend Page  │  │ API Docs Page  │  │ Settings    │   │   │     │     ║
║   │   │   │  │ • HTTP polling (5s)       │  │   │   │ • WebView      │  │ • WebView      │  │ • Config    │   │   │     │     ║
║   │   │   │  │ • Status broadcasting     │  │   │   │ • Embedded App │  │ • Swagger UI   │  │ • Paths     │   │   │     │     ║
║   │   │   │  └───────────────────────────┘  │   │   └────────────────┘  └────────────────┘  └─────────────┘   │   │     │     ║
║   │   │   │                                 │   │                                                             │   │     │     ║
║   │   │   │  ┌───────────────────────────┐  │   │   ┌─────────────────────────────────────────────────────┐   │   │     │     ║
║   │   │   │  │ Config Manager            │  │   │   │                    ZUSTAND STORES                   │   │   │     │     ║
║   │   │   │  │ • Load/save config        │  │   │   │  • processStore  • healthStore  • configStore      │   │   │     │     ║
║   │   │   │  │ • Path resolution         │  │   │   │  • logStore                                         │   │   │     │     ║
║   │   │   │  └───────────────────────────┘  │   │   └─────────────────────────────────────────────────────┘   │   │     │     ║
║   │   │   │                                 │   │                                                             │   │     │     ║
║   │   │   └─────────────────────────────────┘   └─────────────────────────────────────────────────────────────┘   │     │     ║
║   │   │                     │                                              │                                       │     │     ║
║   │   │                     │  IPC BRIDGE (contextBridge)                  │                                       │     │     ║
║   │   │                     │  • process:start-all                         │                                       │     │     ║
║   │   │                     │  • process:stop-all                          │                                       │     │     ║
║   │   │                     │  • process:status                            │                                       │     │     ║
║   │   │                     │  • log:entry                                 │                                       │     │     ║
║   │   │                     │  • config:get/set                            │                                       │     │     ║
║   │   │                     └──────────────────────────────────────────────┘                                       │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                                                                                     │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │                          FRONTEND APPLICATION (Embedded or Browser)                                        │     │     ║
║   │   │                          React 18.x + TypeScript + TailwindCSS + React Query                              │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐   │     │     ║
║   │   │   │ Dashboard       │  │ InstrumentPage  │  │ SiloPage        │  │ ChatPage        │  │ Settings      │   │     │     ║
║   │   │   │                 │  │                 │  │                 │  │                 │  │               │   │     │     ║
║   │   │   │ • Constitutional│  │ • InstrumentList│  │ • SignalGrid    │  │ • ChatPanel     │  │ • AIModel     │   │     │     ║
║   │   │   │   Banner ⚖️      │  │ • SiloList      │  │ • Contradictions│  │ • MessageList   │  │ • Budget      │   │     │     ║
║   │   │   │ • SignalGrid    │  │ • ChartList     │  │ • Confirmations │  │ • Disclaimer ⚖️  │  │ • Theme       │   │     │     ║
║   │   │   │ • Narrative ⚖️   │  │ • AddInstrument │  │ • Narrative ⚖️   │  │ • ModelSelect   │  │               │   │     │     ║
║   │   │   └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘  └───────────────┘   │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐     │     │     ║
║   │   │   │                                     REACT QUERY LAYER                                            │     │     │     ║
║   │   │   │  useInstruments • useSilos • useCharts • useSignals • useRelationships • useNarrative • useChat  │     │     │     ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘     │     │     ║
║   │   │                                              │                                                            │     │     ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐     │     │     ║
║   │   │   │                                     API SERVICE LAYER (Axios)                                    │     │     │     ║
║   │   │   │  instrumentsApi • silosApi • chartsApi • signalsApi • relationshipsApi • narrativesApi • aiApi   │     │     │     ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────────────────────────┘     │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ⚖️ = Constitutional Enforcement Point                                                                   │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                                                                                     │     ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘     ║
║                                                              │                                                                 ║
║                                                              │ HTTP/REST                                                       ║
║                                                              ▼                                                                 ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐     ║
║   │                                                                                                                     │     ║
║   │                                      BACKEND LAYER                                                                   │     ║
║   │                                      FastAPI + Python + SQLAlchemy                                                   │     ║
║   │                                                                                                                     │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                         API ROUTES LAYER                                                   │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   /instruments  /silos  /charts  /signals  /relationships  /narratives  /ai  /chat  /webhook  /platforms │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ⚖️ Constitutional Validation: No aggregation endpoints, no recommendation endpoints                      │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                              │                                                       │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                         SERVICE LAYER                                                      │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ContradictionDetector  ConfirmationDetector  FreshnessCalculator  NarrativeGenerator  ResponseValidator │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ⚖️ Constitutional Logic: EXPOSE only, never resolve; No aggregation; Validate AI responses              │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                              │                                                       │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                         AI LAYER                                                           │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ClaudeClient  PromptBuilder  ModelRegistry  UsageTracker  BudgetManager  ResponseValidator               │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ⚖️ Constitutional Validation: 35+ prohibited patterns, MANDATORY_DISCLAIMER, retry with corrections     │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                              │                                                       │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                         DATA ACCESS LAYER                                                  │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   InstrumentRepository  SiloRepository  ChartRepository  SignalRepository  ConversationRepository          │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                              │                                                       │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │                                         DATABASE LAYER                                                     │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   SQLite + SQLAlchemy                                                                                      │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   ⚖️ Constitutional Schema: NO weight, score, confidence, recommendation, priority, rank columns          │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   │   Tables: instruments, silos, charts, signals, contradictions, confirmations, conversations, ai_usage     │     │     ║
║   │   │                                                                                                           │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                                                                                     │     ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘     ║
║                                                              │                                                                 ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐     ║
║   │                                      EXTERNAL INTEGRATIONS                                                           │     ║
║   │                                                                                                                     │     ║
║   │   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐                                               │     ║
║   │   │  TradingView    │     │  Kite Connect   │     │  Anthropic AI   │                                               │     ║
║   │   │  (Webhooks IN)  │     │  (OAuth2)       │     │  (Claude API)   │                                               │     ║
║   │   │                 │     │                 │     │                 │                                               │     ║
║   │   │  Signal         │     │  Market Data    │     │  Narrative      │                                               │     ║
║   │   │  Ingestion      │     │  (Optional)     │     │  Generation     │                                               │     ║
║   │   └─────────────────┘     └─────────────────┘     └─────────────────┘                                               │     ║
║   │                                                                                                                     │     ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘     ║
║                                                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 3. COMPONENT LAYER BREAKDOWN

## 3.1 Layer Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM LAYERS (Top to Bottom)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   LAYER 1: MISSION CONTROL CONSOLE (MCC)                                     │
│   ════════════════════════════════════════                                   │
│   • Technology: Electron 35.x + React 19.x + Zustand                        │
│   • Purpose: Process orchestration, unified dashboard, log aggregation      │
│   • Components: Main Process, Renderer Process, IPC Bridge                  │
│   • Constitutional: MCR-001 through MCR-005                                  │
│                                                                              │
│   LAYER 2: FRONTEND APPLICATION                                              │
│   ═══════════════════════════════                                            │
│   • Technology: React 18.x + TypeScript + TailwindCSS + React Query         │
│   • Purpose: Signal visualization, narrative display, user interaction      │
│   • Components: Pages, Hooks, Services, Types                               │
│   • Constitutional: CR-001, CR-002, CR-003 enforcement in UI                │
│                                                                              │
│   LAYER 3: API LAYER                                                         │
│   ═══════════════════                                                        │
│   • Technology: FastAPI + Pydantic                                          │
│   • Purpose: HTTP endpoints, request validation, response serialization     │
│   • Components: Routes, Middleware, Schemas                                  │
│   • Constitutional: No aggregation endpoints, schema constraints             │
│                                                                              │
│   LAYER 4: SERVICE LAYER                                                     │
│   ════════════════════════                                                   │
│   • Technology: Python                                                       │
│   • Purpose: Business logic, relationship detection, narrative generation   │
│   • Components: Detectors, Calculators, Generators, Validators              │
│   • Constitutional: EXPOSE-only logic, no resolution                         │
│                                                                              │
│   LAYER 5: AI LAYER                                                          │
│   ═════════════════                                                          │
│   • Technology: Anthropic SDK (Claude)                                       │
│   • Purpose: Narrative generation, response validation                      │
│   • Components: Client, PromptBuilder, Validator, UsageTracker              │
│   • Constitutional: 35+ prohibited patterns, MANDATORY_DISCLAIMER           │
│                                                                              │
│   LAYER 6: DATA ACCESS LAYER                                                 │
│   ══════════════════════════════                                             │
│   • Technology: SQLAlchemy 2.0                                               │
│   • Purpose: Database abstraction, CRUD operations                          │
│   • Components: Repositories, Models                                         │
│   • Constitutional: Pydantic models prohibit forbidden fields               │
│                                                                              │
│   LAYER 7: DATABASE LAYER                                                    │
│   ═══════════════════════════                                                │
│   • Technology: SQLite                                                       │
│   • Purpose: Persistent storage                                              │
│   • Constitutional: Schema has NO weight/score/confidence columns           │
│                                                                              │
│   LAYER 8: EXTERNAL INTEGRATIONS                                             │
│   ══════════════════════════════════                                         │
│   • TradingView: Webhook ingestion (signals IN)                              │
│   • Kite Connect: OAuth2 market data (optional)                              │
│   • Anthropic: Claude API for narratives                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 4. DATA FLOW DIAGRAMS

## 4.1 Master Data Flow - Signal Lifecycle

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            COMPLETE SIGNAL LIFECYCLE (End-to-End)                                      ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   ┌──────────────┐                                                                                    ║
║   │  TradingView │                                                                                    ║
║   │   Webhook    │                                                                                    ║
║   └──────┬───────┘                                                                                    ║
║          │ POST /webhook/receive                                                                      ║
║          │ {chart_code, direction, timestamp}                                                          ║
║          ▼                                                                                            ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              WEBHOOK HANDLER                                                  │    ║
║   │                                                                                              │    ║
║   │   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐       │    ║
║   │   │   1. VERIFY    │───▶│   2. PARSE     │───▶│  3. NORMALIZE  │───▶│  4. LOOKUP     │       │    ║
║   │   │   Signature    │    │   Payload      │    │   Direction    │    │   Chart ID     │       │    ║
║   │   │   (HMAC-256)   │    │   (JSON)       │    │   (ENUM)       │    │   (webhook_id) │       │    ║
║   │   └────────────────┘    └────────────────┘    └────────────────┘    └────────┬───────┘       │    ║
║   │                                                                               │              │    ║
║   └───────────────────────────────────────────────────────────────────────────────┼──────────────┘    ║
║                                                                                   │                   ║
║                                                                                   ▼                   ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              SIGNAL CREATION                                                  │    ║
║   │                                                                                              │    ║
║   │   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐       │    ║
║   │   │  5. CREATE     │───▶│ 6. STORE       │───▶│  7. CALCULATE  │───▶│ 8. DETECT      │       │    ║
║   │   │  Signal Object │    │ to Database    │    │  Freshness     │    │ Relationships  │       │    ║
║   │   │                │    │ (signals)      │    │  (CURRENT)     │    │ (see 4.3)      │       │    ║
║   │   │  signal_id:    │    │                │    │                │    │                │       │    ║
║   │   │    UUID        │    │  ⚖️ NO:         │    │  ≤2min=CURRENT │    │ ⚖️ EXPOSE ONLY  │       │    ║
║   │   │  chart_id:     │    │  • weight      │    │  ≤10min=RECENT │    │ No resolution  │       │    ║
║   │   │    FK          │    │  • score       │    │  >30min=STALE  │    │ No weighting   │       │    ║
║   │   │  direction:    │    │  • confidence  │    │                │    │                │       │    ║
║   │   │    ENUM        │    │  • priority    │    │                │    │                │       │    ║
║   │   │  timestamp:    │    │                │    │                │    │                │       │    ║
║   │   │    UTC         │    │                │    │                │    │                │       │    ║
║   │   └────────────────┘    └────────────────┘    └────────────────┘    └────────┬───────┘       │    ║
║   │                                                                               │              │    ║
║   └───────────────────────────────────────────────────────────────────────────────┼──────────────┘    ║
║                                                                                   │                   ║
║                                                                                   ▼                   ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              USER INTERFACE                                                   │    ║
║   │                                                                                              │    ║
║   │   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐       │    ║
║   │   │  9. QUERY      │───▶│ 10. FETCH      │───▶│ 11. RENDER     │───▶│ 12. DISPLAY    │       │    ║
║   │   │  React Query   │    │  Relationships │    │  SignalGrid    │    │  With          │       │    ║
║   │   │  (useSignals)  │    │  (useRelation) │    │  Contradiction │    │  Freshness     │       │    ║
║   │   │                │    │                │    │  Confirmation  │    │  Badges        │       │    ║
║   │   │  staleTime:    │    │  ⚖️ EQUAL       │    │                │    │                │       │    ║
║   │   │    60s         │    │  visual weight │    │ ⚖️ Side-by-side │    │  🟢 CURRENT     │       │    ║
║   │   │                │    │  for both      │    │   display      │    │  🟡 RECENT      │       │    ║
║   │   │                │    │                │    │                │    │  🔴 STALE       │       │    ║
║   │   └────────────────┘    └────────────────┘    └────────────────┘    └────────────────┘       │    ║
║   │                                                                                              │    ║
║   └──────────────────────────────────────────────────────────────────────────────────────────────┘    ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 4.2 Narrative Generation Flow

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            NARRATIVE GENERATION (AI Pipeline)                                          ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   ┌────────────────────┐                                                                              ║
║   │   User Request     │                                                                              ║
║   │   "Generate        │                                                                              ║
║   │    Narrative"      │                                                                              ║
║   └──────────┬─────────┘                                                                              ║
║              │                                                                                        ║
║              ▼                                                                                        ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              1. CONTEXT ASSEMBLY                                              │    ║
║   │                                                                                              │    ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────┐    │    ║
║   │   │  Gather:                                                                             │    │    ║
║   │   │  • All active charts in silo                                                         │    │    ║
║   │   │  • Latest signal per chart (direction + timestamp)                                   │    │    ║
║   │   │  • Freshness status per signal                                                       │    │    ║
║   │   │  • Detected contradictions (pairs of opposing signals)                               │    │    ║
║   │   │  • Detected confirmations (groups of aligned signals)                                │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │  ⚖️ NO aggregation: Raw data passed, no scores computed                               │    │    ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────┘    │    ║
║   │                                                                                              │    ║
║   └──────────────────────────────────────────────────────────────────────────────────────────────┘    ║
║              │                                                                                        ║
║              ▼                                                                                        ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              2. PROMPT CONSTRUCTION                                           │    ║
║   │                                                                                              │    ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────┐    │    ║
║   │   │  SYSTEM PROMPT (Constitutional Constraints Built-In):                                │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │  "You are a data description assistant. Your role is to DESCRIBE what the          │    │    ║
║   │   │   trading signals show, NEVER to recommend, suggest, or advise action.              │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │   FORBIDDEN: 'should', 'recommend', 'suggest', 'consider', 'buy', 'sell',           │    │    ║
║   │   │              'enter', 'exit', 'likely', 'probably', 'will', predictions,            │    │    ║
║   │   │              confidence scores, overall assessments, net sentiments                  │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │   REQUIRED: End with exact disclaimer: 'This analysis is generated by AI...'"       │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │  USER PROMPT:                                                                        │    │    ║
║   │   │  {context_data_serialized}                                                           │    │    ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────┘    │    ║
║   │                                                                                              │    ║
║   └──────────────────────────────────────────────────────────────────────────────────────────────┘    ║
║              │                                                                                        ║
║              ▼                                                                                        ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              3. AI GENERATION (Claude)                                        │    ║
║   │                                                                                              │    ║
║   │   Model Selection:                                                                           │    ║
║   │   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                                   │    ║
║   │   │ claude-3-haiku│  │claude-3.5-son │  │ claude-opus-4 │                                   │    ║
║   │   │ (Fast/Cheap)  │  │ (Default)     │  │ (Complex)     │                                   │    ║
║   │   └───────────────┘  └───────────────┘  └───────────────┘                                   │    ║
║   │                                                                                              │    ║
║   │   Request → Anthropic API → Raw Response                                                     │    ║
║   │                                                                                              │    ║
║   └──────────────────────────────────────────────────────────────────────────────────────────────┘    ║
║              │                                                                                        ║
║              ▼                                                                                        ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              4. RESPONSE VALIDATION ⚖️                                        │    ║
║   │                                                                                              │    ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────┐    │    ║
║   │   │  ResponseValidator checks 35+ prohibited patterns:                                   │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │  RECOMMENDATION PATTERNS:    PREDICTION PATTERNS:     ACTION PATTERNS:              │    │    ║
║   │   │  • /should\b/i               • /will\s+(?:likely|)/i   • /\bbuy\b/i                  │    │    ║
║   │   │  • /recommend/i              • /probably/i             • /\bsell\b/i                 │    │    ║
║   │   │  • /suggest/i                • /expect/i               • /\benter\b/i                │    │    ║
║   │   │  • /consider/i               • /forecast/i             • /\bexit\b/i                 │    │    ║
║   │   │  • /advise/i                 • /\d+%\s*chance/i        • /take\s+position/i          │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │  AGGREGATION PATTERNS:                                                               │    │    ║
║   │   │  • /overall/i  • /consensus/i  • /net\s+sentiment/i  • /score/i  • /rating/i        │    │    ║
║   │   │                                                                                      │    │    ║
║   │   │  MANDATORY DISCLAIMER CHECK:                                                          │    │    ║
║   │   │  Must contain: "This analysis is generated by AI..."                                 │    │    ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────┘    │    ║
║   │                                                                                              │    ║
║   └─────────────────────────────────────────┬───────────────────────────────────────────────────┘    ║
║                                             │                                                        ║
║              ┌──────────────────────────────┴──────────────────────────────┐                         ║
║              │                                                             │                         ║
║              ▼                                                             ▼                         ║
║   ┌──────────────────┐                                          ┌──────────────────┐                 ║
║   │   ✅ VALID        │                                          │   ❌ INVALID      │                 ║
║   │                  │                                          │                  │                 ║
║   │  • No violations │                                          │  • Violations    │                 ║
║   │  • Disclaimer OK │                                          │    detected      │                 ║
║   │                  │                                          │  • Retry count   │                 ║
║   │  Proceed to      │                                          │    < 3?          │                 ║
║   │  response        │                                          │                  │                 ║
║   └────────┬─────────┘                                          └────────┬─────────┘                 ║
║            │                                                             │                           ║
║            │                                                             │ YES: Add correction        ║
║            │                                                             │ guidance to prompt,        ║
║            │                                                             │ regenerate                 ║
║            │                                                             │                           ║
║            │                                                             │ NO: Use template           ║
║            │                                                             │ fallback response          ║
║            │                                                             │                           ║
║            ▼                                                             ▼                           ║
║   ┌──────────────────────────────────────────────────────────────────────────────────────────────┐    ║
║   │                              5. RESPONSE DELIVERY                                             │    ║
║   │                                                                                              │    ║
║   │   {                                                                                          │    ║
║   │     "silo_id": "...",                                                                        │    ║
║   │     "sections": [                                                                            │    ║
║   │       {"section_type": "SIGNAL_SUMMARY", "content": "...", "chart_ids": [...]},             │    ║
║   │       {"section_type": "CONTRADICTION", "content": "...", "chart_ids": [...]},              │    ║
║   │       {"section_type": "CONFIRMATION", "content": "...", "chart_ids": [...]}                │    ║
║   │     ],                                                                                       │    ║
║   │     "closing_statement": "This analysis is generated by AI for informational purposes...",  │    ║
║   │     "generated_at": "2026-01-05T...",                                                        │    ║
║   │     "model_used": "claude-3.5-sonnet",                                                       │    ║
║   │     "tokens_used": 1247,                                                                     │    ║
║   │     "cost": 0.0087                                                                           │    ║
║   │   }                                                                                          │    ║
║   │                                                                                              │    ║
║   └──────────────────────────────────────────────────────────────────────────────────────────────┘    ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 4.3 Contradiction & Confirmation Detection Flow

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            RELATIONSHIP DETECTION (Contradictions & Confirmations)                     ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   INPUT: All latest signals for charts in a Silo                                                      ║
║                                                                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────┐     ║
║   │                                                                                             │     ║
║   │   Chart 01A: BULLISH (2 min ago)  🟢                                                        │     ║
║   │   Chart 01B: BULLISH (5 min ago)  🟢                                                        │     ║
║   │   Chart 02:  BEARISH (3 min ago)  🟢                                                        │     ║
║   │   Chart 03:  BULLISH (45 min ago) 🔴                                                        │     ║
║   │   Chart 04:  NEUTRAL (1 min ago)  🟢                                                        │     ║
║   │   Chart 05:  BEARISH (8 min ago)  🟡                                                        │     ║
║   │                                                                                             │     ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────┘     ║
║                                               │                                                       ║
║                                               ▼                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────┐     ║
║   │                         CONTRADICTION DETECTION                                              │     ║
║   │                                                                                             │     ║
║   │   Algorithm:                                                                                │     ║
║   │   FOR each pair of charts (A, B) in silo:                                                   │     ║
║   │     IF (A.direction == BULLISH AND B.direction == BEARISH) OR                               │     ║
║   │        (A.direction == BEARISH AND B.direction == BULLISH):                                 │     ║
║   │       CREATE Contradiction(chart_a=A, chart_b=B)                                            │     ║
║   │                                                                                             │     ║
║   │   ⚖️ CRITICAL: We EXPOSE, we NEVER:                                                          │     ║
║   │      • Prioritize one chart over another                                                    │     ║
║   │      • Weight by timeframe                                                                  │     ║
║   │      • Suggest which is "correct"                                                           │     ║
║   │      • Aggregate into "net" direction                                                       │     ║
║   │                                                                                             │     ║
║   │   OUTPUT:                                                                                   │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │  Contradiction 1: Chart 01A (BULLISH) ↔ Chart 02 (BEARISH)                        │     │     ║
║   │   │  Contradiction 2: Chart 01A (BULLISH) ↔ Chart 05 (BEARISH)                        │     │     ║
║   │   │  Contradiction 3: Chart 01B (BULLISH) ↔ Chart 02 (BEARISH)                        │     │     ║
║   │   │  Contradiction 4: Chart 01B (BULLISH) ↔ Chart 05 (BEARISH)                        │     │     ║
║   │   │  Contradiction 5: Chart 03 (BULLISH) ↔ Chart 02 (BEARISH)                         │     │     ║
║   │   │  Contradiction 6: Chart 03 (BULLISH) ↔ Chart 05 (BEARISH)                         │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                                                             │     ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────┘     ║
║                                               │                                                       ║
║                                               ▼                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────┐     ║
║   │                         CONFIRMATION DETECTION                                               │     ║
║   │                                                                                             │     ║
║   │   Algorithm:                                                                                │     ║
║   │   GROUP charts by direction (excluding NEUTRAL):                                            │     ║
║   │     BULLISH_GROUP = [charts where direction == BULLISH]                                     │     ║
║   │     BEARISH_GROUP = [charts where direction == BEARISH]                                     │     ║
║   │                                                                                             │     ║
║   │   FOR each group with 2+ charts:                                                            │     ║
║   │     CREATE Confirmation(charts=group, direction=group_direction)                            │     ║
║   │                                                                                             │     ║
║   │   ⚖️ CRITICAL: We NEVER:                                                                     │     ║
║   │      • Calculate "strength" based on count                                                  │     ║
║   │      • Assign confidence scores                                                             │     ║
║   │      • Imply that more = better                                                             │     ║
║   │                                                                                             │     ║
║   │   OUTPUT:                                                                                   │     ║
║   │   ┌───────────────────────────────────────────────────────────────────────────────────┐     │     ║
║   │   │  Confirmation 1: [Chart 01A, Chart 01B, Chart 03] → BULLISH                       │     │     ║
║   │   │  Confirmation 2: [Chart 02, Chart 05] → BEARISH                                   │     │     ║
║   │   └───────────────────────────────────────────────────────────────────────────────────┘     │     ║
║   │                                                                                             │     ║
║   │   ⚖️ NOTE: Both confirmations are shown with EQUAL prominence.                              │     ║
║   │           We do NOT say "3 BULLISH vs 2 BEARISH = more bullish"                             │     ║
║   │                                                                                             │     ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────┘     ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 5. STATE MACHINE DIAGRAMS

## 5.1 Process State Machine (MCC)

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            MCC PROCESS STATE MACHINE                                                   ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║                                    ┌─────────────────┐                                                ║
║                                    │                 │                                                ║
║                                    │     IDLE        │ ◄───────────────────────────────────┐          ║
║                                    │  (Initial)      │                                     │          ║
║                                    │                 │                                     │          ║
║                                    └────────┬────────┘                                     │          ║
║                                             │                                              │          ║
║                                             │ User clicks "Start"                          │          ║
║                                             │ (MCR-004: Explicit action)                   │          ║
║                                             ▼                                              │          ║
║                                    ┌─────────────────┐                                     │          ║
║                                    │                 │                                     │          ║
║                                    │   STARTING      │                                     │          ║
║                                    │  (Spawning)     │                                     │          ║
║                                    │                 │                                     │          ║
║                                    └────────┬────────┘                                     │          ║
║                                             │                                              │          ║
║                        ┌────────────────────┼────────────────────┐                         │          ║
║                        │                    │                    │                         │          ║
║                        ▼                    ▼                    ▼                         │          ║
║             ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐                │          ║
║             │ Backend Process  │ │ Frontend Process │ │   Error During   │                │          ║
║             │ started          │ │ started          │ │   Start          │                │          ║
║             └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘                │          ║
║                      │                    │                    │                          │          ║
║                      │                    │                    │ Spawn failure            │          ║
║                      │                    │                    ▼                          │          ║
║                      │                    │           ┌──────────────────┐                │          ║
║                      │                    │           │                  │                │          ║
║                      │                    │           │  START_FAILED    │────────────────┘          ║
║                      │                    │           │                  │   Auto-return             ║
║                      │                    │           └──────────────────┘   to IDLE                 ║
║                      │                    │                                                          ║
║                      └────────────────────┤                                                          ║
║                                           │ Both processes healthy                                   ║
║                                           ▼                                                          ║
║                                    ┌─────────────────┐                                               ║
║                                    │                 │                                               ║
║                                    │    RUNNING      │ ◄───────────────────┐                         ║
║                                    │   (Healthy)     │                     │                         ║
║                                    │                 │                     │                         ║
║                                    └────────┬────────┘                     │                         ║
║                                             │                              │                         ║
║                       ┌─────────────────────┼──────────────────────┐       │                         ║
║                       │                     │                      │       │                         ║
║                       ▼                     ▼                      ▼       │                         ║
║            ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐│                         ║
║            │ User clicks Stop │  │ Process crashed  │  │ Health check     ││ Recovery                ║
║            │                  │  │                  │  │ passes           │┘ successful              ║
║            └────────┬─────────┘  └────────┬─────────┘  └──────────────────┘                          ║
║                     │                     │                                                          ║
║                     │                     ▼                                                          ║
║                     │           ┌──────────────────┐                                                 ║
║                     │           │                  │                                                 ║
║                     │           │   DEGRADED       │─────────────────┐                               ║
║                     │           │  (Partial)       │                 │                               ║
║                     │           │                  │                 │ Both processes                ║
║                     │           └────────┬─────────┘                 │ fail                          ║
║                     │                    │                           │                               ║
║                     │                    │ User confirms restart      │                               ║
║                     │                    │ (MCR-004)                  │                               ║
║                     │                    ▼                           ▼                               ║
║                     │           ┌──────────────────┐        ┌──────────────────┐                     ║
║                     │           │                  │        │                  │                     ║
║                     │           │   RESTARTING     │        │     CRASHED      │                     ║
║                     │           │                  │        │   (All down)     │                     ║
║                     │           └────────┬─────────┘        └────────┬─────────┘                     ║
║                     │                    │                           │                               ║
║                     │                    │ Success                   │ User clicks                   ║
║                     │                    ▼                           │ "Restart"                     ║
║                     │                  RUNNING ◄─────────────────────┘                               ║
║                     │                                                                                ║
║                     ▼                                                                                ║
║            ┌──────────────────┐                                                                      ║
║            │                  │                                                                      ║
║            │   STOPPING       │                                                                      ║
║            │  (Graceful)      │                                                                      ║
║            │                  │                                                                      ║
║            └────────┬─────────┘                                                                      ║
║                     │                                                                                ║
║                     │ All processes terminated                                                       ║
║                     ▼                                                                                ║
║            ┌──────────────────┐                                                                      ║
║            │                  │                                                                      ║
║            │     STOPPED      │ ─────────────────────────────────────────────────────────┐           ║
║            │   (Clean exit)   │                                                          │           ║
║            │                  │                                                          │           ║
║            └──────────────────┘                                                          │           ║
║                                                                                          │           ║
║                                                                                          ▼           ║
║                                                                                        IDLE          ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 5.2 Signal Freshness State Machine

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            SIGNAL FRESHNESS STATE MACHINE                                              ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   Signal received                                                                                     ║
║        │                                                                                              ║
║        ▼                                                                                              ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │  🟢 CURRENT     │ ◄────────────────────────────── New signal received                             ║
║   │  (≤ 2 minutes)  │                                                                                 ║
║   │                 │                                                                                 ║
║   └────────┬────────┘                                                                                 ║
║            │                                                                                          ║
║            │ Time > 2 minutes                                                                         ║
║            ▼                                                                                          ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │  🟡 RECENT      │                                                                                 ║
║   │  (≤ 10 minutes) │                                                                                 ║
║   │                 │                                                                                 ║
║   └────────┬────────┘                                                                                 ║
║            │                                                                                          ║
║            │ Time > 10 minutes                                                                        ║
║            ▼                                                                                          ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │  🔴 STALE       │                                                                                 ║
║   │  (> 10 minutes) │                                                                                 ║
║   │                 │                                                                                 ║
║   └─────────────────┘                                                                                 ║
║                                                                                                       ║
║                                                                                                       ║
║   Never received (chart exists, no signals):                                                          ║
║                                                                                                       ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │  ⚫ UNAVAILABLE  │ ──────────────────────────────► CURRENT (when first signal arrives)            ║
║   │  (No signals)   │                                                                                 ║
║   │                 │                                                                                 ║
║   └─────────────────┘                                                                                 ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 5.3 AI Budget State Machine

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            AI BUDGET STATE MACHINE                                                     ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │    ✅ OK         │                                                                                 ║
║   │   (< 80%)       │ ◄─────────────── New period starts / Budget increased                           ║
║   │                 │                                                                                 ║
║   │  Normal ops     │                                                                                 ║
║   │  No warnings    │                                                                                 ║
║   │                 │                                                                                 ║
║   └────────┬────────┘                                                                                 ║
║            │                                                                                          ║
║            │ Usage ≥ 80%                                                                              ║
║            ▼                                                                                          ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │   ⚠️ WARNING     │                                                                                 ║
║   │   (80-90%)      │                                                                                 ║
║   │                 │                                                                                 ║
║   │  Dismissible    │                                                                                 ║
║   │  alert banner   │                                                                                 ║
║   │                 │                                                                                 ║
║   └────────┬────────┘                                                                                 ║
║            │                                                                                          ║
║            │ Usage ≥ 90%                                                                              ║
║            ▼                                                                                          ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │  🔴 CRITICAL    │                                                                                 ║
║   │   (90-100%)     │                                                                                 ║
║   │                 │                                                                                 ║
║   │  Require user   │                                                                                 ║
║   │  confirmation   │                                                                                 ║
║   │  before AI ops  │                                                                                 ║
║   │                 │                                                                                 ║
║   └────────┬────────┘                                                                                 ║
║            │                                                                                          ║
║            │ Usage ≥ 100%                                                                             ║
║            ▼                                                                                          ║
║   ┌─────────────────┐                                                                                 ║
║   │                 │                                                                                 ║
║   │  🚫 BLOCKED     │                                                                                 ║
║   │   (≥ 100%)      │                                                                                 ║
║   │                 │                                                                                 ║
║   │  All AI ops     │                                                                                 ║
║   │  denied         │                                                                                 ║
║   │                 │                                                                                 ║
║   │  Modal shown:   │                                                                                 ║
║   │  "Budget        │                                                                                 ║
║   │   Exhausted"    │                                                                                 ║
║   │                 │                                                                                 ║
║   └─────────────────┘                                                                                 ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 6. ENTITY RELATIONSHIP DIAGRAMS

## 6.1 Complete Data Model

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            CIA-SIE ENTITY RELATIONSHIP DIAGRAM                                         ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │                              CORE DOMAIN ENTITIES                                                │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                                                                       ║
║                                                                                                       ║
║         ┌────────────────────────────────┐                                                            ║
║         │          INSTRUMENTS            │                                                            ║
║         ├────────────────────────────────┤                                                            ║
║         │ PK  instrument_id: UUID        │                                                            ║
║         │     symbol: VARCHAR(20)        │                                                            ║
║         │     display_name: VARCHAR(100) │                                                            ║
║         │     is_active: BOOLEAN         │                                                            ║
║         │     created_at: TIMESTAMP      │                                                            ║
║         │     updated_at: TIMESTAMP      │                                                            ║
║         │                                │                                                            ║
║         │  ⚖️ PROHIBITED COLUMNS:         │                                                            ║
║         │     • weight                   │                                                            ║
║         │     • priority                 │                                                            ║
║         │     • importance               │                                                            ║
║         └───────────────┬────────────────┘                                                            ║
║                         │                                                                             ║
║                         │ 1:N                                                                         ║
║                         ▼                                                                             ║
║         ┌────────────────────────────────┐                                                            ║
║         │            SILOS               │                                                            ║
║         ├────────────────────────────────┤                                                            ║
║         │ PK  silo_id: UUID              │                                                            ║
║         │ FK  instrument_id: UUID        │                                                            ║
║         │     silo_name: VARCHAR(100)    │                                                            ║
║         │     description: TEXT          │                                                            ║
║         │     is_active: BOOLEAN         │                                                            ║
║         │     created_at: TIMESTAMP      │                                                            ║
║         │                                │                                                            ║
║         │  ⚖️ PROHIBITED COLUMNS:         │                                                            ║
║         │     • aggregation_method       │                                                            ║
║         │     • consensus_direction      │                                                            ║
║         └───────────────┬────────────────┘                                                            ║
║                         │                                                                             ║
║                         │ 1:N                                                                         ║
║                         ▼                                                                             ║
║         ┌────────────────────────────────┐                                                            ║
║         │           CHARTS               │                                                            ║
║         ├────────────────────────────────┤                                                            ║
║         │ PK  chart_id: UUID             │                                                            ║
║         │ FK  silo_id: UUID              │                                                            ║
║         │     chart_code: VARCHAR(20)    │   Example: "01A", "02", "03"                               ║
║         │     chart_name: VARCHAR(100)   │                                                            ║
║         │     timeframe: VARCHAR(10)     │   Example: "5m", "15m", "1h", "1d"                         ║
║         │     webhook_id: VARCHAR(100)   │   Unique identifier for webhook routing                   ║
║         │     is_active: BOOLEAN         │                                                            ║
║         │     created_at: TIMESTAMP      │                                                            ║
║         │                                │                                                            ║
║         │  ⚖️ PROHIBITED COLUMNS:         │                                                            ║
║         │     • weight                   │                                                            ║
║         │     • priority                 │                                                            ║
║         │     • importance               │                                                            ║
║         │     • reliability              │                                                            ║
║         │     • accuracy                 │                                                            ║
║         └───────────────┬────────────────┘                                                            ║
║                         │                                                                             ║
║                         │ 1:N                                                                         ║
║                         ▼                                                                             ║
║         ┌────────────────────────────────┐                                                            ║
║         │          SIGNALS               │                                                            ║
║         ├────────────────────────────────┤                                                            ║
║         │ PK  signal_id: UUID            │                                                            ║
║         │ FK  chart_id: UUID             │                                                            ║
║         │     signal_type: ENUM          │   STATE_CHANGE | HEARTBEAT                                 ║
║         │     direction: ENUM            │   BULLISH | BEARISH | NEUTRAL                              ║
║         │     signal_timestamp: TIMESTAMP│                                                            ║
║         │     received_at: TIMESTAMP     │                                                            ║
║         │     raw_payload: JSON          │                                                            ║
║         │                                │                                                            ║
║         │  ⚖️ PROHIBITED COLUMNS:         │                                                            ║
║         │     • confidence               │                                                            ║
║         │     • strength                 │                                                            ║
║         │     • score                    │                                                            ║
║         │     • quality                  │                                                            ║
║         │     • reliability              │                                                            ║
║         └────────────────────────────────┘                                                            ║
║                                                                                                       ║
║                                                                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │                              RELATIONSHIP ENTITIES (Computed, Not Stored)                        │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                                                                       ║
║                                                                                                       ║
║         ┌────────────────────────────────┐         ┌────────────────────────────────┐                 ║
║         │       CONTRADICTIONS           │         │       CONFIRMATIONS            │                 ║
║         │       (Computed View)          │         │       (Computed View)          │                 ║
║         ├────────────────────────────────┤         ├────────────────────────────────┤                 ║
║         │     chart_a_id: UUID           │         │     chart_ids: UUID[]          │                 ║
║         │     chart_a_code: VARCHAR      │         │     chart_codes: VARCHAR[]     │                 ║
║         │     chart_a_direction: ENUM    │         │     aligned_direction: ENUM    │                 ║
║         │     chart_b_id: UUID           │         │     detected_at: TIMESTAMP     │                 ║
║         │     chart_b_code: VARCHAR      │         │                                │                 ║
║         │     chart_b_direction: ENUM    │         │  ⚖️ PROHIBITED FIELDS:          │                 ║
║         │     detected_at: TIMESTAMP     │         │     • strength                 │                 ║
║         │                                │         │     • confidence               │                 ║
║         │  ⚖️ PROHIBITED FIELDS:          │         │     • count (for "X confirm") │                 ║
║         │     • resolution               │         └────────────────────────────────┘                 ║
║         │     • preferred_chart          │                                                            ║
║         │     • recommendation           │                                                            ║
║         └────────────────────────────────┘                                                            ║
║                                                                                                       ║
║                                                                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │                              AI ENTITIES                                                         │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                                                                       ║
║                                                                                                       ║
║         ┌────────────────────────────────┐         ┌────────────────────────────────┐                 ║
║         │        CONVERSATIONS           │         │         AI_USAGE               │                 ║
║         ├────────────────────────────────┤         ├────────────────────────────────┤                 ║
║         │ PK  conversation_id: UUID      │         │ PK  usage_id: UUID             │                 ║
║         │ FK  scrip_id: UUID             │         │ FK  conversation_id: UUID      │                 ║
║         │     started_at: TIMESTAMP      │         │     model: VARCHAR(50)         │                 ║
║         │     last_message_at: TIMESTAMP │         │     input_tokens: INTEGER      │                 ║
║         │                                │         │     output_tokens: INTEGER     │                 ║
║         └───────────────┬────────────────┘         │     cost: DECIMAL(10,6)        │                 ║
║                         │                          │     created_at: TIMESTAMP      │                 ║
║                         │ 1:N                      └────────────────────────────────┘                 ║
║                         ▼                                                                             ║
║         ┌────────────────────────────────┐                                                            ║
║         │          MESSAGES              │                                                            ║
║         ├────────────────────────────────┤                                                            ║
║         │ PK  message_id: UUID           │                                                            ║
║         │ FK  conversation_id: UUID      │                                                            ║
║         │     role: ENUM                 │   USER | ASSISTANT | SYSTEM                                ║
║         │     content: TEXT              │                                                            ║
║         │     timestamp: TIMESTAMP       │                                                            ║
║         │     tokens_used: INTEGER       │                                                            ║
║         │                                │                                                            ║
║         │  Note: ASSISTANT messages      │                                                            ║
║         │  always include DISCLAIMER     │                                                            ║
║         └────────────────────────────────┘                                                            ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 7. SEQUENCE DIAGRAMS

## 7.1 Complete Signal Ingestion Sequence

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            WEBHOOK SIGNAL INGESTION SEQUENCE                                           ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   TradingView        WebhookHandler       SignalValidator       SignalRepo          Database          ║
║        │                   │                    │                   │                   │             ║
║        │  POST /webhook    │                    │                   │                   │             ║
║        │  {chart_code,     │                    │                   │                   │             ║
║        │   direction,      │                    │                   │                   │             ║
║        │   timestamp}      │                    │                   │                   │             ║
║        │──────────────────▶│                    │                   │                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │ Verify HMAC-256    │                   │                   │             ║
║        │                   │ signature          │                   │                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │ validate(payload)  │                   │                   │             ║
║        │                   │───────────────────▶│                   │                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │ Normalize         │                   │             ║
║        │                   │                    │ direction to ENUM │                   │             ║
║        │                   │                    │ (BULLISH|BEARISH  │                   │             ║
║        │                   │                    │  |NEUTRAL)        │                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │ ⚖️ Reject if:      │                   │             ║
║        │                   │                    │ • "confidence"    │                   │             ║
║        │                   │                    │ • "score"         │                   │             ║
║        │                   │                    │ • "recommendation"│                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │     validated      │                   │                   │             ║
║        │                   │◀───────────────────│                   │                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │              find_chart(webhook_id)    │                   │             ║
║        │                   │───────────────────────────────────────▶│                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │                   │ SELECT chart      │             ║
║        │                   │                    │                   │ WHERE webhook_id  │             ║
║        │                   │                    │                   │──────────────────▶│             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │                   │     chart         │             ║
║        │                   │                    │                   │◀──────────────────│             ║
║        │                   │                    │       chart       │                   │             ║
║        │                   │◀───────────────────────────────────────│                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │              create_signal(chart_id, direction, ts)        │             ║
║        │                   │───────────────────────────────────────▶│                   │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │                   │ INSERT INTO       │             ║
║        │                   │                    │                   │ signals           │             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │                   │ ⚖️ Schema has NO:  │             ║
║        │                   │                    │                   │ • weight          │             ║
║        │                   │                    │                   │ • score           │             ║
║        │                   │                    │                   │ • confidence      │             ║
║        │                   │                    │                   │──────────────────▶│             ║
║        │                   │                    │                   │                   │             ║
║        │                   │                    │                   │     signal_id     │             ║
║        │                   │                    │                   │◀──────────────────│             ║
║        │                   │                    │    signal         │                   │             ║
║        │                   │◀───────────────────────────────────────│                   │             ║
║        │                   │                    │                   │                   │             ║
║        │  200 OK           │                    │                   │                   │             ║
║        │  {signal_id}      │                    │                   │                   │             ║
║        │◀──────────────────│                    │                   │                   │             ║
║        │                   │                    │                   │                   │             ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 7.2 Dashboard Data Loading Sequence

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            DASHBOARD DATA LOADING SEQUENCE                                             ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   User         Dashboard       ReactQuery        ApiService        Backend           Database         ║
║    │               │               │                 │                │                  │            ║
║    │ Navigate to   │               │                 │                │                  │            ║
║    │ /dashboard    │               │                 │                │                  │            ║
║    │──────────────▶│               │                 │                │                  │            ║
║    │               │               │                 │                │                  │            ║
║    │               │ Mount         │                 │                │                  │            ║
║    │               │──────────────▶│                 │                │                  │            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │  ┌──────────────────────────────────────────────┐   │            ║
║    │               │               │  │     PARALLEL QUERIES (React Query)          │   │            ║
║    │               │               │  └──────────────────────────────────────────────┘   │            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │ useInstruments  │                │                  │            ║
║    │               │               │────────────────▶│                │                  │            ║
║    │               │               │                 │ GET /instruments                  │            ║
║    │               │               │                 │───────────────▶│                  │            ║
║    │               │               │                 │                │ SELECT           │            ║
║    │               │               │                 │                │─────────────────▶│            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │ useSilos        │                │   instruments    │            ║
║    │               │               │────────────────▶│                │◀─────────────────│            ║
║    │               │               │                 │ GET /silos     │                  │            ║
║    │               │               │                 │───────────────▶│                  │            ║
║    │               │               │                 │                │ SELECT           │            ║
║    │               │               │                 │                │─────────────────▶│            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │ useRelationships│                │     silos        │            ║
║    │               │               │────────────────▶│                │◀─────────────────│            ║
║    │               │               │                 │GET /relationships/silo/{id}       │            ║
║    │               │               │                 │───────────────▶│                  │            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │                 │                │ Compute:         │            ║
║    │               │               │                 │                │ • Contradictions │            ║
║    │               │               │                 │                │ • Confirmations  │            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │                 │                │ ⚖️ NO aggregation │            ║
║    │               │               │                 │                │ ⚖️ EQUAL weight   │            ║
║    │               │               │                 │                │                  │            ║
║    │               │               │◀────────────────┼────────────────│                  │            ║
║    │               │               │    All data     │                │                  │            ║
║    │               │               │    cached       │                │                  │            ║
║    │               │               │                 │                │                  │            ║
║    │               │◀──────────────│                 │                │                  │            ║
║    │               │  Render       │                 │                │                  │            ║
║    │               │               │                 │                │                  │            ║
║    │               │  ┌──────────────────────────────────────────────────────────────┐   │            ║
║    │               │  │  Dashboard displays:                                         │   │            ║
║    │               │  │  • ConstitutionalBanner ⚖️                                    │   │            ║
║    │               │  │  • SignalGrid (all charts with freshness badges)            │   │            ║
║    │               │  │  • ContradictionPanel (pairs, EQUAL visual weight) ⚖️        │   │            ║
║    │               │  │  • ConfirmationPanel (groups, NO strength scores) ⚖️         │   │            ║
║    │               │  │  • NarrativePanel (with MANDATORY disclaimer) ⚖️             │   │            ║
║    │               │  └──────────────────────────────────────────────────────────────┘   │            ║
║    │               │                 │                │                  │               │            ║
║    │◀──────────────│                 │                │                  │               │            ║
║    │   View        │                 │                │                  │               │            ║
║    │   rendered    │                 │                │                  │               │            ║
║    │               │                 │                │                  │               │            ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

## 7.3 AI Chat Sequence

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            AI CHAT INTERACTION SEQUENCE                                                ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   User       ChatPanel      useSendMsg      ApiService      ChatRoute       AIService     Anthropic   ║
║    │             │              │               │               │               │              │      ║
║    │ Type        │              │               │               │               │              │      ║
║    │ message     │              │               │               │               │              │      ║
║    │────────────▶│              │               │               │               │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │ Submit       │               │               │               │              │      ║
║    │             │─────────────▶│               │               │               │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │ POST /chat    │               │               │              │      ║
║    │             │              │ {scrip_id,    │               │               │              │      ║
║    │             │              │  message,     │               │               │              │      ║
║    │             │              │  model}       │               │               │              │      ║
║    │             │              │──────────────▶│               │               │              │      ║
║    │             │              │               │POST           │               │              │      ║
║    │             │              │               │──────────────▶│               │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │ Load context  │              │      ║
║    │             │              │               │               │ (signals,     │              │      ║
║    │             │              │               │               │  contradicts, │              │      ║
║    │             │              │               │               │  confirms)    │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │ Build prompt  │              │      ║
║    │             │              │               │               │──────────────▶│              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │               │ ⚖️ Prompt     │      ║
║    │             │              │               │               │               │ includes:    │      ║
║    │             │              │               │               │               │ • FORBIDDEN  │      ║
║    │             │              │               │               │               │   patterns   │      ║
║    │             │              │               │               │               │ • Required   │      ║
║    │             │              │               │               │               │   disclaimer │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │               │ Generate     │      ║
║    │             │              │               │               │               │─────────────▶│      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │               │   response   │      ║
║    │             │              │               │               │               │◀─────────────│      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │ Validate ⚖️    │              │      ║
║    │             │              │               │               │◀──────────────│              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │ ┌─────────────────────────┐  │      ║
║    │             │              │               │               │ │ ResponseValidator       │  │      ║
║    │             │              │               │               │ │ • 35+ prohibited patterns│  │      ║
║    │             │              │               │               │ │ • MANDATORY_DISCLAIMER  │  │      ║
║    │             │              │               │               │ │                         │  │      ║
║    │             │              │               │               │ │ If invalid → retry      │  │      ║
║    │             │              │               │               │ │ with corrections        │  │      ║
║    │             │              │               │               │ └─────────────────────────┘  │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │               │ Append        │              │      ║
║    │             │              │               │               │ disclaimer    │              │      ║
║    │             │              │               │               │ if missing    │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │              │               │◀──────────────│               │              │      ║
║    │             │              │               │   ChatResponse│               │              │      ║
║    │             │              │               │   {response,  │               │              │      ║
║    │             │              │               │    disclaimer,│               │              │      ║
║    │             │              │               │    tokens,    │               │              │      ║
║    │             │              │               │    cost}      │               │              │      ║
║    │             │              │◀──────────────│               │               │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │◀─────────────│               │               │               │              │      ║
║    │             │ Update UI    │               │               │               │              │      ║
║    │             │              │               │               │               │              │      ║
║    │             │ Show message │               │               │               │              │      ║
║    │             │ + disclaimer │               │               │               │              │      ║
║    │◀────────────│ ⚖️            │               │               │               │              │      ║
║    │             │              │               │               │               │              │      ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 8. CONSTITUTIONAL ENFORCEMENT CHECKPOINTS

## 8.1 Five-Layer Defense-in-Depth

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            CONSTITUTIONAL ENFORCEMENT LAYERS                                           ║
║                                                                                                       ║
║   Every layer of the system enforces constitutional compliance.                                        ║
║   A violation at ANY layer blocks the operation.                                                       ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │   LAYER 1: DATABASE SCHEMA                                                                       │ ║
║   │   ════════════════════════════                                                                   │ ║
║   │                                                                                                 │ ║
║   │   The schema PHYSICALLY CANNOT store prohibited data:                                            │ ║
║   │                                                                                                 │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   TABLES DO NOT CONTAIN:                                                             │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   instruments: ❌ weight, priority, importance, rank                                  │      │ ║
║   │   │   silos:       ❌ aggregation_method, consensus_direction, net_sentiment              │      │ ║
║   │   │   charts:      ❌ weight, priority, importance, reliability, accuracy                 │      │ ║
║   │   │   signals:     ❌ confidence, strength, score, quality, reliability                   │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   These columns DO NOT EXIST in the schema. They CANNOT be added without             │      │ ║
║   │   │   a schema migration that would be flagged as a constitutional violation.            │      │ ║
║   │   │                                                                                      │      │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘      │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                      │                                                ║
║                                                      ▼                                                ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │   LAYER 2: DOMAIN MODELS (Pydantic)                                                              │ ║
║   │   ═══════════════════════════════════                                                            │ ║
║   │                                                                                                 │ ║
║   │   Python domain models have explicit PROHIBITED comments:                                        │ ║
║   │                                                                                                 │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   class ChartResponse(BaseModel):                                                    │      │ ║
║   │   │       chart_id: str                                                                  │      │ ║
║   │   │       chart_code: str                                                                │      │ ║
║   │   │       # PROHIBITED: weight, priority, importance - CONSTITUTIONAL VIOLATION          │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   class SignalResponse(BaseModel):                                                   │      │ ║
║   │   │       signal_id: str                                                                 │      │ ║
║   │   │       direction: Direction                                                           │      │ ║
║   │   │       # PROHIBITED: confidence, strength, score - CONSTITUTIONAL VIOLATION           │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   class RelationshipSummaryResponse(BaseModel):                                      │      │ ║
║   │   │       contradictions: List[Contradiction]                                            │      │ ║
║   │   │       confirmations: List[Confirmation]                                              │      │ ║
║   │   │       # PROHIBITED: overall_direction, consensus, net_sentiment - VIOLATION          │      │ ║
║   │   │                                                                                      │      │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘      │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                      │                                                ║
║                                                      ▼                                                ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │   LAYER 3: BUSINESS LOGIC                                                                        │ ║
║   │   ═══════════════════════════                                                                    │ ║
║   │                                                                                                 │ ║
║   │   Service classes implement EXPOSE-only logic:                                                   │ ║
║   │                                                                                                 │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   ContradictionDetector:                                                             │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ ✅ DOES: Find pairs of charts with opposing directions                      │     │      │ ║
║   │   │   │ ✅ DOES: Return both charts with equal status                               │     │      │ ║
║   │   │   │ ❌ NEVER: Suggest which chart is "correct"                                  │     │      │ ║
║   │   │   │ ❌ NEVER: Weight by timeframe or recency                                    │     │      │ ║
║   │   │   │ ❌ NEVER: Provide a "resolution" field                                      │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   ConfirmationDetector:                                                              │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ ✅ DOES: Group charts with same direction                                   │     │      │ ║
║   │   │   │ ✅ DOES: Return list of aligned chart IDs                                   │     │      │ ║
║   │   │   │ ❌ NEVER: Calculate "strength" based on count                               │     │      │ ║
║   │   │   │ ❌ NEVER: Assign confidence scores                                          │     │      │ ║
║   │   │   │ ❌ NEVER: Imply that more confirmations = better                            │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   FreshnessCalculator:                                                               │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ ✅ DOES: Calculate age of signal in minutes                                 │     │      │ ║
║   │   │   │ ✅ DOES: Return categorical status (CURRENT/RECENT/STALE)                   │     │      │ ║
║   │   │   │ ❌ NEVER: Use freshness to weight signal importance                         │     │      │ ║
║   │   │   │ ❌ NEVER: Suggest stale signals are "less valid"                            │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘      │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                      │                                                ║
║                                                      ▼                                                ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │   LAYER 4: AI RESPONSE VALIDATION                                                                │ ║
║   │   ═══════════════════════════════════                                                            │ ║
║   │                                                                                                 │ ║
║   │   ResponseValidator checks every AI output against 35+ prohibited patterns:                      │ ║
║   │                                                                                                 │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   RECOMMENDATION PATTERNS (CR-001):                                                  │      │ ║
║   │   │   /should\b/i, /recommend/i, /suggest/i, /consider/i, /advise/i,                    │      │ ║
║   │   │   /you might/i, /it would be/i, /prudent/i, /wise/i                                 │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   PREDICTION PATTERNS (CR-003):                                                      │      │ ║
║   │   │   /will\s+(?:likely|probably)/i, /expect/i, /forecast/i,                            │      │ ║
║   │   │   /\d+%\s*(?:chance|probability)/i, /going to/i, /is expected/i                     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   ACTION PATTERNS (CR-001):                                                          │      │ ║
║   │   │   /\bbuy\b/i, /\bsell\b/i, /\benter\b/i, /\bexit\b/i,                               │      │ ║
║   │   │   /take\s+position/i, /go\s+(?:long|short)/i                                        │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   AGGREGATION PATTERNS (CR-002):                                                     │      │ ║
║   │   │   /overall/i, /consensus/i, /net\s+sentiment/i, /balance\s+of/i,                    │      │ ║
║   │   │   /majority/i, /predominantly/i, /on\s+the\s+whole/i                                │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   SCORE PATTERNS (CR-002):                                                           │      │ ║
║   │   │   /score/i, /rating/i, /confidence/i, /strength/i, /\d+\s*out\s*of/i                │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   MANDATORY DISCLAIMER CHECK:                                                        │      │ ║
║   │   │   Response MUST contain: "This analysis is generated by AI..."                      │      │ ║
║   │   │   If missing → Append automatically before returning                                 │      │ ║
║   │   │                                                                                      │      │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘      │ ║
║   │                                                                                                 │ ║
║   │   On violation:                                                                                  │ ║
║   │   1. Log violation details                                                                      │ ║
║   │   2. If retry_count < 3: Regenerate with stricter prompt (include violation feedback)           │ ║
║   │   3. If retry_count >= 3: Use template fallback response                                        │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                      │                                                ║
║                                                      ▼                                                ║
║   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ ║
║   │                                                                                                 │ ║
║   │   LAYER 5: UI CONSTRAINTS                                                                        │ ║
║   │   ═══════════════════════                                                                        │ ║
║   │                                                                                                 │ ║
║   │   Frontend components enforce visual constitutional compliance:                                  │ ║
║   │                                                                                                 │ ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   ConstitutionalBanner:                                                              │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ • Always visible on Dashboard                                              │     │      │ ║
║   │   │   │ • Displays three constitutional principles                                 │     │      │ ║
║   │   │   │ • Cannot be dismissed or hidden                                            │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   ContradictionPanel:                                                                │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ • Both charts displayed with EQUAL visual size                             │     │      │ ║
║   │   │   │ • Same styling, same prominence                                            │     │      │ ║
║   │   │   │ • NO visual cues suggesting one is "better"                                │     │      │ ║
║   │   │   │ • NO resolution or "resolve" button                                        │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   NarrativePanel:                                                                    │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ • Disclaimer ALWAYS visible at bottom                                      │     │      │ ║
║   │   │   │ • Disclaimer styled distinctly (border, background)                        │     │      │ ║
║   │   │   │ • Cannot be collapsed or hidden                                            │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   │   Action Buttons:                                                                    │      │ ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │      │ ║
║   │   │   │ ✅ ALLOWED: View, Explore, Navigate, Refresh, Generate Narrative            │     │      │ ║
║   │   │   │ ❌ FORBIDDEN: Buy, Sell, Enter, Exit, Trade, Execute                        │     │      │ ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │      │ ║
║   │   │                                                                                      │      │ ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘      │ ║
║   │                                                                                                 │ ║
║   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# 9. MCC ↔ BACKEND INTEGRATION MAP

## 9.1 MCC Process Orchestration

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                            MCC → BACKEND INTEGRATION                                                   ║
║                                                                                                       ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║                                                                                                       ║
║   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                                               │   ║
║   │                              MCC MAIN PROCESS                                                  │   ║
║   │                                                                                               │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────┐     │   ║
║   │   │                           ProcessOrchestrator                                        │     │   ║
║   │   │                                                                                     │     │   ║
║   │   │   ┌──────────────────────┐                    ┌──────────────────────┐              │     │   ║
║   │   │   │                      │                    │                      │              │     │   ║
║   │   │   │   Backend Process    │                    │   Frontend Process   │              │     │   ║
║   │   │   │                      │                    │                      │              │     │   ║
║   │   │   │   spawn('python',    │                    │   spawn('npm',       │              │     │   ║
║   │   │   │     ['-m', 'uvicorn',│                    │     ['run', 'dev'],  │              │     │   ║
║   │   │   │      'src.main:app', │                    │     {cwd: frontend/})│              │     │   ║
║   │   │   │      '--port=8000']) │                    │                      │              │     │   ║
║   │   │   │                      │                    │   Listens on:        │              │     │   ║
║   │   │   │   Listens on:        │                    │   localhost:5173     │              │     │   ║
║   │   │   │   localhost:8000     │                    │                      │              │     │   ║
║   │   │   │                      │                    │                      │              │     │   ║
║   │   │   └──────────┬───────────┘                    └───────────┬──────────┘              │     │   ║
║   │   │              │                                            │                         │     │   ║
║   │   │              │ stdout/stderr                              │ stdout/stderr           │     │   ║
║   │   │              ▼                                            ▼                         │     │   ║
║   │   │   ┌─────────────────────────────────────────────────────────────────────────────┐   │     │   ║
║   │   │   │                           LogAggregator                                      │   │     │   ║
║   │   │   │                                                                             │   │     │   ║
║   │   │   │   • Captures all process output                                             │   │     │   ║
║   │   │   │   • Parses log levels (INFO, WARN, ERROR)                                   │   │     │   ║
║   │   │   │   • Broadcasts via IPC to Renderer                                          │   │     │   ║
║   │   │   │   • Stores in ring buffer (last 10000 lines)                                │   │     │   ║
║   │   │   │                                                                             │   │     │   ║
║   │   │   └─────────────────────────────────────────────────────────────────────────────┘   │     │   ║
║   │   │                                                                                     │     │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────┘     │   ║
║   │                                                                                               │   ║
║   │   ┌─────────────────────────────────────────────────────────────────────────────────────┐     │   ║
║   │   │                            HealthMonitor                                             │     │   ║
║   │   │                                                                                     │     │   ║
║   │   │   Every 5 seconds:                                                                  │     │   ║
║   │   │                                                                                     │     │   ║
║   │   │   ┌────────────────────────────┐    ┌────────────────────────────┐                  │     │   ║
║   │   │   │                            │    │                            │                  │     │   ║
║   │   │   │   GET localhost:8000/health│    │   GET localhost:5173       │                  │     │   ║
║   │   │   │                            │    │   (HEAD request)           │                  │     │   ║
║   │   │   │   Expected: 200 OK         │    │                            │                  │     │   ║
║   │   │   │   {status: "healthy",      │    │   Expected: 200 OK         │                  │     │   ║
║   │   │   │    database: "ok",         │    │                            │                  │     │   ║
║   │   │   │    ai: "ok"}               │    │                            │                  │     │   ║
║   │   │   │                            │    │                            │                  │     │   ║
║   │   │   └────────────────────────────┘    └────────────────────────────┘                  │     │   ║
║   │   │                                                                                     │     │   ║
║   │   │   Results broadcast via IPC:                                                        │     │   ║
║   │   │   {                                                                                 │     │   ║
║   │   │     backend: {status: 'healthy', responseTime: 45, lastCheck: '...'},              │     │   ║
║   │   │     frontend: {status: 'healthy', responseTime: 12, lastCheck: '...'}              │     │   ║
║   │   │   }                                                                                 │     │   ║
║   │   │                                                                                     │     │   ║
║   │   │   MCR-003: If health check fails, UI remains functional (graceful degradation)      │     │   ║
║   │   │                                                                                     │     │   ║
║   │   └─────────────────────────────────────────────────────────────────────────────────────┘     │   ║
║   │                                                                                               │   ║
║   └───────────────────────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                                       ║
║                                              │                                                        ║
║                                              │ IPC Bridge                                             ║
║                                              │ (contextBridge)                                        ║
║                                              ▼                                                        ║
║                                                                                                       ║
║   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                                                                                               │   ║
║   │                              MCC RENDERER PROCESS                                              │   ║
║   │                                                                                               │   ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐    │   ║
║   │   │                              ZUSTAND STORES                                           │    │   ║
║   │   │                                                                                      │    │   ║
║   │   │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │    │   ║
║   │   │   │ processStore   │  │ healthStore    │  │ logStore       │  │ configStore    │     │    │   ║
║   │   │   │                │  │                │  │                │  │                │     │    │   ║
║   │   │   │ • backend      │  │ • backend      │  │ • entries[]    │  │ • paths        │     │    │   ║
║   │   │   │ • frontend     │  │   .status      │  │ • filters      │  │ • settings     │     │    │   ║
║   │   │   │ • all          │  │   .responseTime│  │ • searchQuery  │  │                │     │    │   ║
║   │   │   │                │  │ • frontend     │  │                │  │                │     │    │   ║
║   │   │   │ Actions:       │  │   .status      │  │ Actions:       │  │ Actions:       │     │    │   ║
║   │   │   │ • startAll()   │  │   .responseTime│  │ • addEntry()   │  │ • load()       │     │    │   ║
║   │   │   │ • stopAll()    │  │                │  │ • clear()      │  │ • save()       │     │    │   ║
║   │   │   │ • restart()    │  │ Subscribed to  │  │ • filter()     │  │ • setPath()    │     │    │   ║
║   │   │   │                │  │ IPC updates    │  │                │  │                │     │    │   ║
║   │   │   └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘     │    │   ║
║   │   │                                                                                      │    │   ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘    │   ║
║   │                                                                                               │   ║
║   │   ┌──────────────────────────────────────────────────────────────────────────────────────┐    │   ║
║   │   │                              DASHBOARD COMPONENTS                                     │    │   ║
║   │   │                                                                                      │    │   ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │    │   ║
║   │   │   │                                                                            │     │    │   ║
║   │   │   │   SystemStatus          QuickActions            ServiceGrid               │     │    │   ║
║   │   │   │   ┌──────────────┐      ┌──────────────┐        ┌──────────────────┐      │     │    │   ║
║   │   │   │   │ 🟢 Backend   │      │ ▶️ Start All  │        │ Backend          │      │     │    │   ║
║   │   │   │   │ 🟢 Frontend  │      │ ⏹️ Stop All   │        │ ├─ Status: 🟢    │      │     │    │   ║
║   │   │   │   │ 🟢 Database  │      │ 🔄 Restart    │        │ ├─ Port: 8000    │      │     │    │   ║
║   │   │   │   │              │      │              │        │ └─ PID: 12345    │      │     │    │   ║
║   │   │   │   │ All healthy  │      │ MCR-004:     │        │                  │      │     │    │   ║
║   │   │   │   │              │      │ Explicit     │        │ Frontend         │      │     │    │   ║
║   │   │   │   │              │      │ user action  │        │ ├─ Status: 🟢    │      │     │    │   ║
║   │   │   │   │              │      │ required     │        │ ├─ Port: 5173    │      │     │    │   ║
║   │   │   │   │              │      │              │        │ └─ PID: 12346    │      │     │    │   ║
║   │   │   │   └──────────────┘      └──────────────┘        └──────────────────┘      │     │    │   ║
║   │   │   │                                                                            │     │    │   ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │    │   ║
║   │   │                                                                                      │    │   ║
║   │   │   ┌────────────────────────────────────────────────────────────────────────────┐     │    │   ║
║   │   │   │                                                                            │     │    │   ║
║   │   │   │   Embedded WebViews                                                        │     │    │   ║
║   │   │   │                                                                            │     │    │   ║
║   │   │   │   ┌─────────────────────────┐    ┌─────────────────────────┐               │     │    │   ║
║   │   │   │   │                         │    │                         │               │     │    │   ║
║   │   │   │   │   Frontend App          │    │   API Documentation     │               │     │    │   ║
║   │   │   │   │   (localhost:5173)      │    │   (localhost:8000/docs) │               │     │    │   ║
║   │   │   │   │                         │    │                         │               │     │    │   ║
║   │   │   │   │   MCR-002: Only         │    │   MCR-002: Only         │               │     │    │   ║
║   │   │   │   │   localhost allowed     │    │   localhost allowed     │               │     │    │   ║
║   │   │   │   │                         │    │                         │               │     │    │   ║
║   │   │   │   └─────────────────────────┘    └─────────────────────────┘               │     │    │   ║
║   │   │   │                                                                            │     │    │   ║
║   │   │   └────────────────────────────────────────────────────────────────────────────┘     │    │   ║
║   │   │                                                                                      │    │   ║
║   │   └──────────────────────────────────────────────────────────────────────────────────────┘    │   ║
║   │                                                                                               │   ║
║   └───────────────────────────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

[Document continues in Part 4...]

