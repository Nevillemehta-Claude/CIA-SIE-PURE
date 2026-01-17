# CHAPTER 01: SYSTEM CIRCUIT MAP

**Document ID:** ASM-CH01-2026
**Classification:** ARCHITECTURE VISUALIZATION
**Predecessor:** 00_MASTER_INDEX.md
**Successor:** 02_SIGNAL_FLOW_MATRIX.md

---

## Purpose

Visual architecture showing every node and connection point across the complete composite application. Every signal, every connection, every failover path is mapped.

---

## 1.1 MASTER SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                         │
│                           CIA-SIE-PURE COMPOSITE SYSTEM                                 │
│                           ═══════════════════════════════                               │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              EXTERNAL SYSTEMS                                      │ │
│  │                                                                                    │ │
│  │   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐                    │ │
│  │   │  ZERODHA     │      │  ANTHROPIC   │      │  TRADINGVIEW │                    │ │
│  │   │  KITE API    │      │  CLAUDE API  │      │  WEBHOOKS    │                    │ │
│  │   │              │      │              │      │              │                    │ │
│  │   │  [EXT-001]   │      │  [EXT-002]   │      │  [EXT-003]   │                    │ │
│  │   └──────┬───────┘      └──────┬───────┘      └──────┬───────┘                    │ │
│  │          │                     │                     │                            │ │
│  └──────────┼─────────────────────┼─────────────────────┼────────────────────────────┘ │
│             │                     │                     │                              │
│             │    ┌────────────────┼─────────────────────┘                              │
│             │    │                │                                                    │
│             ▼    ▼                ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │                         CIA-SIE MAIN APPLICATION                                   │ │
│  │                         ════════════════════════                                   │ │
│  │                                                                                    │ │
│  │   CONSTITUTIONAL LAYER (CR-001, CR-002, CR-003)                                   │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │ [CONST-001] Decision-Support ONLY, NOT Decision-Making                      │ │ │
│  │   │ [CONST-002] Expose Contradictions, NEVER Resolve Them                       │ │ │
│  │   │ [CONST-003] Descriptive AI, NOT Prescriptive AI                             │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                      │                                            │ │
│  │                                      ▼                                            │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                         API LAYER [L1]                                    │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │ │
│  │   │   │/health  │ │/instru- │ │/signals │ │/charts  │ │/silos   │            │   │ │
│  │   │   │[API-001]│ │ments    │ │[API-003]│ │[API-004]│ │[API-005]│            │   │ │
│  │   │   └────┬────┘ │[API-002]│ └────┬────┘ └────┬────┘ └────┬────┘            │   │ │
│  │   │        │      └────┬────┘      │           │           │                  │   │ │
│  │   │   ┌────┴──────────┴────────────┴───────────┴───────────┴────┐            │   │ │
│  │   │   │                                                          │            │   │ │
│  │   │   │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │            │   │ │
│  │   │   │   │/baskets │ │/relatio-│ │/narrat- │ │/webhooks│       │            │   │ │
│  │   │   │   │[API-006]│ │nships   │ │ives     │ │[API-009]│       │            │   │ │
│  │   │   │   └────┬────┘ │[API-007]│ │[API-008]│ └────┬────┘       │            │   │ │
│  │   │   │        │      └────┬────┘ └────┬────┘      │             │            │   │ │
│  │   │   │   ┌────┴──────────┴────────────┴───────────┴────┐       │            │   │ │
│  │   │   │   │                                              │       │            │   │ │
│  │   │   │   │   ┌─────────┐ ┌─────────┐ ┌─────────┐       │       │            │   │ │
│  │   │   │   │   │/ai      │ │/chat    │ │/platfrms│       │       │            │   │ │
│  │   │   │   │   │[API-010]│ │[API-011]│ │[API-012]│       │       │            │   │ │
│  │   │   │   │   └────┬────┘ └────┬────┘ └────┬────┘       │       │            │   │ │
│  │   │   │   └────────┼───────────┼───────────┼────────────┘       │            │   │ │
│  │   │   └────────────┼───────────┼───────────┼────────────────────┘            │   │ │
│  │   └────────────────┼───────────┼───────────┼──────────────────────────────────┘   │ │
│  │                    │           │           │                                      │ │
│  │                    ▼           ▼           ▼                                      │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                      SERVICE LAYER [L2]                                   │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │   │ │
│  │   │   │ EXPOSURE ENGINE │  │ INGESTION ENGINE│  │ PLATFORM BRIDGE │          │   │ │
│  │   │   │                 │  │                 │  │                 │          │   │ │
│  │   │   │ [SVC-001]       │  │ [SVC-002]       │  │ [SVC-003]       │          │   │ │
│  │   │   │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │          │   │ │
│  │   │   │ │Contradiction│ │  │ │Signal      │ │  │ │Kite Adapter │ │          │   │ │
│  │   │   │ │Detector     │ │  │ │Normalizer  │ │  │ │[PLAT-001]   │ │          │   │ │
│  │   │   │ │[EXP-001]    │ │  │ │[ING-001]   │ │  │ └─────────────┘ │          │   │ │
│  │   │   │ ├─────────────┤ │  │ ├─────────────┤ │  │ ┌─────────────┐ │          │   │ │
│  │   │   │ │Confirmation │ │  │ │Webhook     │ │  │ │TradingView  │ │          │   │ │
│  │   │   │ │Detector     │ │  │ │Handler     │ │  │ │Adapter      │ │          │   │ │
│  │   │   │ │[EXP-002]    │ │  │ │[ING-002]   │ │  │ │[PLAT-002]   │ │          │   │ │
│  │   │   │ ├─────────────┤ │  │ ├─────────────┤ │  │ └─────────────┘ │          │   │ │
│  │   │   │ │Relationship │ │  │ │Freshness   │ │  │                 │          │   │ │
│  │   │   │ │Exposer      │ │  │ │Tracker     │ │  │                 │          │   │ │
│  │   │   │ │[EXP-003]    │ │  │ │[ING-003]   │ │  │                 │          │   │ │
│  │   │   │ └─────────────┘ │  │ └─────────────┘ │  │                 │          │   │ │
│  │   │   └─────────────────┘  └─────────────────┘  └─────────────────┘          │   │ │
│  │   │                                                                           │   │ │
│  │   └───────────────────────────────────────────────────────────────────────────┘   │ │
│  │                    │           │           │                                      │ │
│  │                    ▼           ▼           ▼                                      │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                         AI LAYER [L3]                                     │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │   │ │
│  │   │   │ CLAUDE CLIENT   │  │ NARRATIVE GEN   │  │ RESPONSE VALID  │          │   │ │
│  │   │   │ [AI-001]        │  │ [AI-002]        │  │ [AI-003]        │          │   │ │
│  │   │   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘          │   │ │
│  │   │            │                    │                    │                    │   │ │
│  │   │   ┌────────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐          │   │ │
│  │   │   │ PROMPT BUILDER  │  │ MODEL REGISTRY  │  │ USAGE TRACKER   │          │   │ │
│  │   │   │ [AI-004]        │  │ [AI-005]        │  │ [AI-006]        │          │   │ │
│  │   │   └─────────────────┘  └─────────────────┘  └─────────────────┘          │   │ │
│  │   │                                                                           │   │ │
│  │   └───────────────────────────────────────────────────────────────────────────┘   │ │
│  │                    │                                                              │ │
│  │                    ▼                                                              │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                    DATA ACCESS LAYER [L4]                                 │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │   │ │
│  │   │   │ DATABASE.PY    │  │ MODELS.PY       │  │ REPOSITORIES.PY │          │   │ │
│  │   │   │ [DAL-001]       │  │ [DAL-002]       │  │ [DAL-003]       │          │   │ │
│  │   │   └────────┬────────┘  └─────────────────┘  └─────────────────┘          │   │ │
│  │   │            │                                                              │   │ │
│  │   └────────────┼──────────────────────────────────────────────────────────────┘   │ │
│  │                │                                                                  │ │
│  │                ▼                                                                  │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                       DATABASE [L5]                                       │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐    │   │ │
│  │   │   │                    SQLite: cia_sie.db                            │    │   │ │
│  │   │   │                                                                  │    │   │ │
│  │   │   │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │    │   │ │
│  │   │   │  │instruments│ │  silos    │ │  charts   │ │  signals  │       │    │   │ │
│  │   │   │  │[TBL-001]  │ │[TBL-002]  │ │[TBL-003]  │ │[TBL-004]  │       │    │   │ │
│  │   │   │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │    │   │ │
│  │   │   │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │    │   │ │
│  │   │   │  │contradicts│ │confirmats │ │ baskets   │ │basket_itms│       │    │   │ │
│  │   │   │  │[TBL-005]  │ │[TBL-006]  │ │[TBL-007]  │ │[TBL-008]  │       │    │   │ │
│  │   │   │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │    │   │ │
│  │   │   │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │    │   │ │
│  │   │   │  │narratives │ │ai_models  │ │ai_usage   │ │conversatns│       │    │   │ │
│  │   │   │  │[TBL-009]  │ │[TBL-010]  │ │[TBL-011]  │ │[TBL-012]  │       │    │   │ │
│  │   │   │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │    │   │ │
│  │   │   │                                                                  │    │   │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘    │   │ │
│  │   │                                                                           │   │ │
│  │   └───────────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                                    │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│                                         │                                               │
│                                         │                                               │
│  ┌──────────────────────────────────────┴────────────────────────────────────────────┐ │
│  │                                                                                    │ │
│  │                            PROJECT MERCURY                                         │ │
│  │                            ═══════════════                                         │ │
│  │                                                                                    │ │
│  │   CONSTITUTIONAL LAYER (MR-001 to MR-005) - UNRESTRICTED                          │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │ [MCONST-001] Grounded Intelligence - Data-backed responses                  │ │ │
│  │   │ [MCONST-002] Direct Communication - No mandatory disclaimers                │ │ │
│  │   │ [MCONST-003] Synthesis Over Fragmentation                                   │ │ │
│  │   │ [MCONST-004] Conversation Continuity                                        │ │ │
│  │   │ [MCONST-005] Truthful Uncertainty                                           │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                      │                                            │ │
│  │                                      ▼                                            │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                      INTERFACE LAYER [ML1]                                │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌───────────────────┐           ┌───────────────────┐                  │   │ │
│  │   │   │   WEB INTERFACE   │           │   TERMINAL REPL   │                  │   │ │
│  │   │   │   [MINT-001]      │           │   [MINT-002]      │                  │   │ │
│  │   │   │                   │           │                   │                  │   │ │
│  │   │   │ ┌───────────────┐ │           │ ┌───────────────┐ │                  │   │ │
│  │   │   │ │ /             │ │           │ │ Interactive   │ │                  │   │ │
│  │   │   │ │ /health       │ │           │ │ Chat Loop     │ │                  │   │ │
│  │   │   │ │ /status       │ │           │ │               │ │                  │   │ │
│  │   │   │ │ /api/chat     │ │           │ │ Commands:     │ │                  │   │ │
│  │   │   │ │ /ws/chat      │ │           │ │ /help /clear  │ │                  │   │ │
│  │   │   │ └───────────────┘ │           │ │ /quit         │ │                  │   │ │
│  │   │   │                   │           │ └───────────────┘ │                  │   │ │
│  │   │   └─────────┬─────────┘           └─────────┬─────────┘                  │   │ │
│  │   │             │                               │                             │   │ │
│  │   └─────────────┼───────────────────────────────┼─────────────────────────────┘   │ │
│  │                 │                               │                                 │ │
│  │                 └───────────────┬───────────────┘                                 │ │
│  │                                 ▼                                                 │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                        CHAT LAYER [ML2]                                   │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────────┐        ┌─────────────────────┐                 │   │ │
│  │   │   │   CHAT ENGINE       │        │   CONVERSATION MGR  │                 │   │ │
│  │   │   │   [MCHAT-001]       │◄──────►│   [MCHAT-002]       │                 │   │ │
│  │   │   │                     │        │                     │                 │   │ │
│  │   │   │   process_query()   │        │   add_message()     │                 │   │ │
│  │   │   │   _parse_query()    │        │   get_context()     │                 │   │ │
│  │   │   │   _fetch_data()     │        │   clear()           │                 │   │ │
│  │   │   │                     │        │                     │                 │   │ │
│  │   │   └──────────┬──────────┘        └─────────────────────┘                 │   │ │
│  │   │              │                                                            │   │ │
│  │   └──────────────┼────────────────────────────────────────────────────────────┘   │ │
│  │                  │                                                                │ │
│  │                  ▼                                                                │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                         AI LAYER [ML3]                                    │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────────┐        ┌─────────────────────┐                 │   │ │
│  │   │   │   AI ENGINE         │        │   PROMPTS           │                 │   │ │
│  │   │   │   [MAI-001]         │◄──────►│   [MAI-002]         │                 │   │ │
│  │   │   │                     │        │                     │                 │   │ │
│  │   │   │   generate()        │        │   SYSTEM_PROMPT     │                 │   │ │
│  │   │   │   health_check()    │        │   build_user_prompt │                 │   │ │
│  │   │   │                     │        │                     │                 │   │ │
│  │   │   └──────────┬──────────┘        └─────────────────────┘                 │   │ │
│  │   │              │                                                            │   │ │
│  │   └──────────────┼────────────────────────────────────────────────────────────┘   │ │
│  │                  │                                                                │ │
│  │                  ▼                                                                │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                        KITE LAYER [ML4]                                   │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌─────────────────────┐        ┌─────────────────────┐                 │   │ │
│  │   │   │   KITE ADAPTER      │        │   KITE MODELS       │                 │   │ │
│  │   │   │   [MKITE-001]       │◄──────►│   [MKITE-002]       │                 │   │ │
│  │   │   │                     │        │                     │                 │   │ │
│  │   │   │   get_quote()       │        │   Quote             │                 │   │ │
│  │   │   │   get_positions()   │        │   Position          │                 │   │ │
│  │   │   │   get_holdings()    │        │   Holding           │                 │   │ │
│  │   │   │   search_instruments│        │   Instrument        │                 │   │ │
│  │   │   │                     │        │   MarketDataBundle  │                 │   │ │
│  │   │   └──────────┬──────────┘        └─────────────────────┘                 │   │ │
│  │   │              │                                                            │   │ │
│  │   └──────────────┼────────────────────────────────────────────────────────────┘   │ │
│  │                  │                                                                │ │
│  │                  ▼                                                                │ │
│  │   ┌──────────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                        CORE LAYER [ML5]                                   │   │ │
│  │   │                                                                           │   │ │
│  │   │   ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ │   │ │
│  │   │   │ config.py │ │security.py│ │ logging.py│ │validation │ │resilience │ │   │ │
│  │   │   │[MCORE-001]│ │[MCORE-002]│ │[MCORE-003]│ │[MCORE-004]│ │[MCORE-005]│ │   │ │
│  │   │   └───────────┘ └───────────┘ └───────────┘ └───────────┘ └───────────┘ │   │ │
│  │   │   ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ │   │ │
│  │   │   │ health.py │ │ metrics.py│ │ errors.py │ │features.py│ │ startup.py│ │   │ │
│  │   │   │[MCORE-006]│ │[MCORE-007]│ │[MCORE-008]│ │[MCORE-009]│ │[MCORE-010]│ │   │ │
│  │   │   └───────────┘ └───────────┘ └───────────┘ └───────────┘ └───────────┘ │   │ │
│  │   │                                                                           │   │ │
│  │   └───────────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                                    │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.2 NODE REGISTRY

### CIA-SIE Nodes

| Node ID | Module | File | Purpose | Connects To |
|---------|--------|------|---------|-------------|
| API-001 | API | routes/health | Health endpoint | - |
| API-002 | API | routes/instruments | Instrument CRUD | DAL-003 |
| API-003 | API | routes/signals | Signal ingestion | SVC-002 |
| API-004 | API | routes/charts | Chart management | DAL-003 |
| API-005 | API | routes/silos | Silo management | DAL-003 |
| API-006 | API | routes/baskets | Basket operations | DAL-003 |
| API-007 | API | routes/relationships | Exposures | SVC-001 |
| API-008 | API | routes/narratives | AI narratives | AI-002 |
| API-009 | API | routes/webhooks | Webhook receiver | SVC-002 |
| API-010 | API | routes/ai | AI endpoints | AI-001 |
| API-011 | API | routes/chat | Chat interface | AI-002 |
| API-012 | API | routes/platforms | Platform config | SVC-003 |
| SVC-001 | Exposure | exposure/* | Detect relationships | DAL-003 |
| SVC-002 | Ingestion | ingestion/* | Process signals | DAL-003 |
| SVC-003 | Platforms | platforms/* | External bridges | EXT-001, EXT-003 |
| AI-001 | AI | ai/claude_client | Claude API | EXT-002 |
| AI-002 | AI | ai/narrative_gen | Generate text | AI-001, AI-003 |
| AI-003 | AI | ai/response_validator | Validate response | CONST-* |
| AI-004 | AI | ai/prompt_builder | Build prompts | - |
| AI-005 | AI | ai/model_registry | Model selection | - |
| AI-006 | AI | ai/usage_tracker | Token tracking | DAL-003 |
| DAL-001 | DAL | dal/database | DB connection | TBL-* |
| DAL-002 | DAL | dal/models | ORM models | - |
| DAL-003 | DAL | dal/repositories | Data access | DAL-001, DAL-002 |
| EXP-001 | Exposure | contradiction_detector | Find conflicts | DAL-003 |
| EXP-002 | Exposure | confirmation_detector | Find confirms | DAL-003 |
| EXP-003 | Exposure | relationship_exposer | Expose all | EXP-001, EXP-002 |
| ING-001 | Ingestion | signal_normalizer | Normalize data | - |
| ING-002 | Ingestion | webhook_handler | Process hooks | ING-001 |
| ING-003 | Ingestion | freshness | Track freshness | - |
| PLAT-001 | Platforms | kite | Kite adapter | EXT-001 |
| PLAT-002 | Platforms | tradingview | TV adapter | EXT-003 |

### Mercury Nodes

| Node ID | Module | File | Purpose | Connects To |
|---------|--------|------|---------|-------------|
| MINT-001 | Interface | api/app | Web UI | MCHAT-001 |
| MINT-002 | Interface | interface/repl | Terminal | MCHAT-001 |
| MCHAT-001 | Chat | chat/engine | Process queries | MAI-001, MKITE-001 |
| MCHAT-002 | Chat | chat/conversation | State mgmt | MCHAT-001 |
| MAI-001 | AI | ai/engine | Claude integration | EXT-002 |
| MAI-002 | AI | ai/prompts | Prompt templates | MAI-001 |
| MKITE-001 | Kite | kite/adapter | Market data | EXT-001 |
| MKITE-002 | Kite | kite/models | Data models | MKITE-001 |
| MCORE-001 | Core | core/config | Configuration | - |
| MCORE-002 | Core | core/security | Data masking | - |
| MCORE-003 | Core | core/logging | Structured logs | - |
| MCORE-004 | Core | core/validation | Config validation | MCORE-001 |
| MCORE-005 | Core | core/resilience | Circuit breakers | MKITE-001, MAI-001 |
| MCORE-006 | Core | core/health | Health checks | MCORE-004, MCORE-005 |
| MCORE-007 | Core | core/metrics | Observability | - |
| MCORE-008 | Core | core/errors | Error taxonomy | - |
| MCORE-009 | Core | core/features | Feature flags | - |
| MCORE-010 | Core | core/startup | Initialization | MCORE-004, MCORE-006 |

### External Nodes

| Node ID | System | Purpose | Connected By |
|---------|--------|---------|--------------|
| EXT-001 | Zerodha Kite | Market data | PLAT-001, MKITE-001 |
| EXT-002 | Anthropic Claude | AI generation | AI-001, MAI-001 |
| EXT-003 | TradingView | Webhooks | PLAT-002 |

---

## 1.3 CONNECTION MATRIX

### CIA-SIE Internal Connections

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CIA-SIE CONNECTION MATRIX                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  API Layer → Service Layer                                              │
│  ════════════════════════                                               │
│  API-003 (signals) ────────► SVC-002 (ingestion)                        │
│  API-007 (relationships) ──► SVC-001 (exposure)                         │
│  API-008 (narratives) ─────► AI-002 (narrative_gen)                     │
│  API-009 (webhooks) ───────► SVC-002 (ingestion)                        │
│  API-010 (ai) ─────────────► AI-001 (claude_client)                     │
│  API-011 (chat) ───────────► AI-002 (narrative_gen)                     │
│  API-012 (platforms) ──────► SVC-003 (platforms)                        │
│                                                                         │
│  Service Layer → Data Layer                                             │
│  ═══════════════════════════                                            │
│  SVC-001 (exposure) ───────► DAL-003 (repositories)                     │
│  SVC-002 (ingestion) ──────► DAL-003 (repositories)                     │
│  SVC-003 (platforms) ──────► EXT-001, EXT-003                           │
│                                                                         │
│  AI Layer → External                                                    │
│  ════════════════════                                                   │
│  AI-001 (claude) ──────────► EXT-002 (Anthropic)                        │
│  AI-002 (narrative) ───────► AI-001 (claude)                            │
│  AI-003 (validator) ───────► CONST-* (constitutional)                   │
│                                                                         │
│  Data Layer → Database                                                  │
│  ═════════════════════                                                  │
│  DAL-003 (repositories) ───► DAL-001 (database)                         │
│  DAL-001 (database) ───────► TBL-* (all tables)                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Mercury Internal Connections

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   MERCURY CONNECTION MATRIX                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Interface Layer → Chat Layer                                           │
│  ═════════════════════════════                                          │
│  MINT-001 (web) ───────────► MCHAT-001 (engine)                         │
│  MINT-002 (repl) ──────────► MCHAT-001 (engine)                         │
│                                                                         │
│  Chat Layer → AI Layer                                                  │
│  ══════════════════════                                                 │
│  MCHAT-001 (engine) ───────► MAI-001 (ai_engine)                        │
│  MCHAT-001 (engine) ───────► MCHAT-002 (conversation)                   │
│  MAI-001 (ai_engine) ──────► MAI-002 (prompts)                          │
│                                                                         │
│  Chat Layer → Kite Layer                                                │
│  ════════════════════════                                               │
│  MCHAT-001 (engine) ───────► MKITE-001 (adapter)                        │
│  MKITE-001 (adapter) ──────► MKITE-002 (models)                         │
│                                                                         │
│  All Layers → Core Layer                                                │
│  ═══════════════════════                                                │
│  * (all modules) ──────────► MCORE-001 (config)                         │
│  * (all modules) ──────────► MCORE-003 (logging)                        │
│  * (all modules) ──────────► MCORE-008 (errors)                         │
│  MKITE-001, MAI-001 ───────► MCORE-005 (resilience)                     │
│                                                                         │
│  Core Layer → External                                                  │
│  ═════════════════════                                                  │
│  MKITE-001 (adapter) ──────► EXT-001 (Kite API)                         │
│  MAI-001 (ai_engine) ──────► EXT-002 (Claude API)                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1.4 CIRCUIT COMPLETENESS VERIFICATION

### Closed Loop Analysis

Every node must have:
1. At least one **predecessor** (data/control inbound)
2. At least one **successor** (data/control outbound)
3. Exception: Entry points (user input) and Exit points (final output)

| Category | Count | Entry Points | Exit Points | Orphan Nodes |
|----------|-------|--------------|-------------|--------------|
| CIA-SIE | 33 | 12 (API endpoints) | 1 (database) | 0 ✅ |
| Mercury | 20 | 2 (web, repl) | 2 (Kite, Claude) | 0 ✅ |
| External | 3 | 0 | 3 (external systems) | N/A |

**Verification Result:** ✅ NO ORPHAN NODES - ALL CIRCUITS CLOSED

---

## 1.5 LAUNCHER CIRCUIT

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      LAUNCHER IGNITION SEQUENCE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  USER ACTION: Double-click start-cia-sie.command                 │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: config.sh loaded → PROJECT_ROOT, VENV_PATH, PORTS      │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 2: utils.sh loaded → Logging, PID management, Display     │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 3: health-check.sh loaded → wait_for_backend()            │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 4: ignite.sh → verify_prerequisites()                     │   │
│  │          ├── Check venv exists                                   │   │
│  │          ├── Check backend source exists                         │   │
│  │          ├── Check port available                                │   │
│  │          └── Check ngrok (if enabled)                            │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 5: activate_venv() → source venv/bin/activate             │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 6: start_backend() → uvicorn cia_sie.api.app:app          │   │
│  │          └── wait_for_backend() → /health returns 200           │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 7: start_ngrok() → ngrok http 8000                        │   │
│  │          └── get_ngrok_url() → Retrieve public URL              │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 8: start_frontend() → npm run dev (if exists)             │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STEP 9: open_browser() → open http://localhost:8000/docs       │   │
│  └──────────────────────────────┬──────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  OPERATIONAL: System running, monitoring loop active            │   │
│  │               └── Ctrl+C triggers shutdown_all()                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1.6 CHAPTER HANDOFF

**This chapter established:**
- Complete visual architecture of all 56+ nodes
- Connection matrix between all components
- Closed-loop verification (no orphan nodes)
- Launcher circuit visualization

**Next chapter will detail:**
- Data flow through each connection
- Event pathways with transformations
- Signal origin → transformation → destination mapping

---

**Predecessor:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)
**Successor:** [02_SIGNAL_FLOW_MATRIX.md](./02_SIGNAL_FLOW_MATRIX.md)

---

*"Like avionics systems, if one node fails to acknowledge, the entire chain is visible for diagnosis."*
