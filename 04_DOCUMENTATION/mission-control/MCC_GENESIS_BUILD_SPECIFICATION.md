# CIA-SIE MISSION CONTROL CONSOLE
## Genesis Codex Build Specification v1.1.0

**Document Classification:** MISSION CRITICAL
**Project Status:** SPECIFICATION PHASE
**Parent Project:** CIA-SIE-PURE
**Build Framework:** Universal Software Genesis Codex
**Target Platform:** Electron 29.x + React 18.x

---

## EXECUTIVE SUMMARY

This document provides the complete build specification for the CIA-SIE Mission Control Console (MCC), structured according to the Universal Software Genesis Codex 12-stage development framework. The MCC serves as the unified command center for the CIA-SIE ecosystem, providing:

- **Process Orchestration**: Start/stop/monitor backend and frontend services
- **Unified Dashboard**: Real-time system health and signal status
- **Log Aggregation**: Consolidated view of all system logs
- **Configuration Management**: Centralized settings control
- **Quick Actions**: One-click access to common operations

### Constitutional Inheritance

The MCC inherits ALL constitutional rules from CIA-SIE-PURE:

| Rule | Description | MCC Application |
|------|-------------|-----------------|
| CR-001 | Decision-Support Only | NO trade execution buttons in MCC |
| CR-002 | Expose Never Resolve | Display contradictions, never aggregate |
| CR-003 | Descriptive AI Only | All AI narratives include disclaimer |

---

## ⚡ CREATIVE LATITUDE DIRECTIVE (INVIOLABLE)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MANDATORY CURSOR IMPLEMENTATION PROTOCOL                  │
│                          EFFECTIVE IMMEDIATELY                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  THIS DIRECTIVE SUPERSEDES ALL OTHER INSTRUCTIONS IN THIS DOCUMENT          │
│  EXCEPT FOR CONSTITUTIONAL RULES (CR-001, CR-002, CR-003, MCR-001-005)      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Directive 1: Specification Status Declaration

**ALL specifications, recommendations, technology choices, architecture patterns, directory structures, component designs, type definitions, configuration files, and implementation details contained in this document and its companion document (MCC_GUI_MOCKUP_REQUIREMENTS.md) are PROVIDED FOR DIRECTIONAL AND KNOWLEDGE PURPOSES ONLY.**

These specifications represent ONE POSSIBLE implementation approach. They are NOT mandatory requirements. They are NOT prescriptive instructions. They are reference material to inform Cursor's understanding of the project goals and context.

### Directive 2: Cursor Creative Authority

**Cursor is ENTIRELY AT LIBERTY to exercise its own free will, expertise, and professional judgment to:**

1. **Replace Technology Choices** - Substitute any specified technology with a more modern, performant, or suitable alternative
2. **Redesign Architecture** - Propose different architectural patterns that better achieve the stated goals
3. **Restructure Directory Layout** - Organize files and folders according to best practices Cursor determines
4. **Modify Component Design** - Create component structures that differ from those specified
5. **Revise Type Definitions** - Design type systems that Cursor considers more robust
6. **Select Different Libraries** - Choose dependencies Cursor deems more appropriate
7. **Optimize Implementation** - Apply performance optimizations and modern patterns
8. **Improve Visual Design** - Enhance the GUI mockups with superior UX/UI approaches

### Directive 3: Forbidden Dependencies (Constitutional Constraint)

**The ONLY dependency restrictions are those that violate constitutional principles:**

```
FORBIDDEN DEPENDENCIES (Constitutional Violations):
├── Telemetry/analytics services (violates user privacy)
├── Cloud APIs or external services (violates MCR-002: No External Network Calls)
├── Auto-update services (violates user control)
├── Trade execution APIs (violates CR-001: Decision-Support Only)
└── Any service that transmits data externally without explicit user action

ALL OTHER DEPENDENCIES ARE PERMITTED at Cursor's discretion.
Cursor may add any libraries, frameworks, or tools that improve the implementation.
```

### Directive 4: Mandatory Cursor Implementation Plan (INVIOLABLE)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   BEFORE WRITING ANY CODE, CURSOR MUST PRODUCE A                            │
│   "CURSOR IMPLEMENTATION PLAN" DOCUMENT                                      │
│                                                                              │
│   THIS REQUIREMENT IS INVIOLABLE AND CANNOT BE BYPASSED                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**The Cursor Implementation Plan MUST contain:**

#### Section A: Executive Divergence Summary
- List of ALL areas where Cursor's approach differs from this specification
- Clear statement of what was specified vs. what Cursor proposes instead
- This section ensures the user (Neville) is FULLY INFORMED of all deviations

#### Section B: Technology Stack Declaration
```
For each technology choice, state:
├── Reference Specification: [What this document specified]
├── Cursor Selection: [What Cursor will actually use]
├── Rationale: [Why this choice is superior or equivalent]
└── Impact: [How this affects other components]
```

#### Section C: Architecture Decisions
- Cursor's proposed architecture with diagrams
- Explanation of how it differs from the reference architecture
- Benefits of the chosen approach

#### Section D: Phase-by-Phase Implementation Plan
```
For each Genesis Codex stage (1-12), Cursor must detail:
├── Stage Name and Number
├── Cursor's Interpretation of Stage Goals
├── Specific Deliverables Cursor Will Produce
├── Any Deviations from Reference Specification
├── Proposed Timeline (if Cursor chooses to provide)
└── Dependencies and Prerequisites
```

#### Section E: GUI/UX Approach
- How Cursor will interpret or modify the visual mockups
- Any modern UI patterns or libraries Cursor will employ
- Accessibility approach

#### Section F: Risk Assessment
- Potential challenges with the chosen approach
- Mitigation strategies

### Directive 5: User Approval Gate (INVIOLABLE)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   THE USER (NEVILLE) MUST READ AND APPROVE THE CURSOR IMPLEMENTATION        │
│   PLAN IN ITS ENTIRETY BEFORE ANY CODE IMPLEMENTATION BEGINS                │
│                                                                              │
│   Cursor MUST pause and await explicit approval.                            │
│   "Proceed" or equivalent confirmation is required.                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**This approval gate serves to:**
1. Ensure the user understands exactly what Cursor intends to build
2. Surface any concerns before development resources are invested
3. Provide opportunity for course correction on architectural decisions
4. Document the agreed-upon approach for future reference

### Directive 6: Continuous Communication

Throughout implementation, Cursor SHOULD:
- Flag any additional deviations discovered during development
- Propose alternatives when encountering obstacles
- Seek clarification rather than assume when requirements are ambiguous

### Summary: What Remains Inviolable

| Category | Status |
|----------|--------|
| Constitutional Rules (CR-001, CR-002, CR-003) | **INVIOLABLE** - Cannot be modified |
| MCC-Specific Rules (MCR-001 through MCR-005) | **INVIOLABLE** - Cannot be modified |
| Forbidden Dependencies (telemetry, cloud, auto-update, trade APIs) | **INVIOLABLE** - Cannot be added |
| Cursor Implementation Plan Requirement | **INVIOLABLE** - Must be produced |
| User Approval Before Coding | **INVIOLABLE** - Must be obtained |
| Everything Else in This Document | **DIRECTIONAL** - Cursor may modify |

---

## GENESIS CODEX STAGE MAP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL SOFTWARE GENESIS CODEX                          │
│                         12-STAGE LIFECYCLE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────┐   ┌─────────────┐   ┌──────────────┐   ┌─────────────┐       │
│   │ STAGE 1 │──▶│   STAGE 2   │──▶│   STAGE 3    │──▶│   STAGE 4   │       │
│   │ GENESIS │   │ CONSTITUTION│   │ ARCHITECTURE │   │SPECIFICATION│       │
│   │  [G]    │   │     [C]     │   │     [A]      │   │     [S]     │       │
│   └─────────┘   └─────────────┘   └──────────────┘   └─────────────┘       │
│       │                                                      │              │
│       │              HITL GATE 1: VISION APPROVAL            │              │
│       └──────────────────────────────────────────────────────┘              │
│                                                                              │
│   ┌─────────────┐   ┌───────────┐   ┌─────────────┐   ┌──────────────┐     │
│   │   STAGE 5   │──▶│  STAGE 6  │──▶│   STAGE 7   │──▶│   STAGE 8    │     │
│   │IMPLEMENTATION│  │ VALIDATION│   │ INTEGRATION │   │ VERIFICATION │     │
│   │     [I]     │   │    [V]    │   │     [I]     │   │     [V]      │     │
│   └─────────────┘   └───────────┘   └─────────────┘   └──────────────┘     │
│       │                                                      │              │
│       │              HITL GATE 2: CODE APPROVAL              │              │
│       └──────────────────────────────────────────────────────┘              │
│                                                                              │
│   ┌─────────────────┐   ┌─────────────┐   ┌─────────────────┐              │
│   │    STAGE 9      │──▶│  STAGE 10   │──▶│    STAGE 11     │              │
│   │ RECONCILIATION  │   │ REMEDIATION │   │  CERTIFICATION  │              │
│   │      [R]        │   │     [R]     │   │      [C]        │              │
│   └─────────────────┘   └─────────────┘   └─────────────────┘              │
│       │                                                      │              │
│       │              HITL GATE 3: LAUNCH APPROVAL            │              │
│       └──────────────────────────────────────────────────────┘              │
│                                                                              │
│                        ┌─────────────┐                                      │
│                        │  STAGE 12   │                                      │
│                        │  OPERATION  │                                      │
│                        │     [O]     │                                      │
│                        └─────────────┘                                      │
│                              │                                               │
│                    HITL GATE 4: OPERATIONAL HANDOFF                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# STAGE 1: GENESIS
## Vision Articulation

### 1.1 Project Vision Statement

The CIA-SIE Mission Control Console transforms the current multi-terminal workflow into a unified, NASA-inspired command center that provides complete visibility and control over all CIA-SIE components through a single Electron-based desktop application.

### 1.2 Problem Statement

**Current State:**
```
Terminal 1: cd backend && python -m uvicorn src.main:app --reload
Terminal 2: cd frontend && npm run dev
Terminal 3: Watching logs
Terminal 4: Monitoring health
Browser: localhost:5173 for frontend
Browser: localhost:8000/docs for API
```

**Target State:**
```
Single Application: CIA-SIE Mission Control Console
├── One-click start/stop for all services
├── Unified dashboard with real-time metrics
├── Integrated log viewer with filtering
├── Embedded web views for frontend/API
└── System tray integration for background operation
```

### 1.3 Success Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| Startup Time | Application launch to ready | < 3 seconds |
| Process Launch | Backend + Frontend spawn | < 5 seconds |
| Memory Footprint | Total RAM usage | < 500 MB |
| CPU Idle | Background monitoring | < 2% |
| Crash Recovery | Auto-restart on failure | 100% |

### 1.4 Stakeholder Identification

| Stakeholder | Role | Responsibility |
|-------------|------|----------------|
| User (Nevil) | Product Owner | Approve all HITL gates |
| Claude Code | Specification Author | This document |
| Cursor | Implementation Agent | Code generation |

---

# STAGE 2: CONSTITUTION
## Inviolable Principles

### 2.1 Inherited Constitutional Rules

The MCC MUST enforce all CIA-SIE constitutional rules:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONSTITUTIONAL COMPLIANCE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CR-001: DECISION-SUPPORT ONLY                                       │
│  ─────────────────────────────────────────────────────────────────  │
│  ✓ Process controls: Start, Stop, Restart (ALLOWED)                 │
│  ✗ Trade actions: Buy, Sell, Enter, Exit (FORBIDDEN)                │
│  ✓ Navigation: View Dashboard, View Signals (ALLOWED)               │
│  ✗ Recommendations: "You should...", "Consider..." (FORBIDDEN)      │
│                                                                      │
│  CR-002: EXPOSE NEVER RESOLVE                                        │
│  ─────────────────────────────────────────────────────────────────  │
│  ✓ Display contradictions side-by-side                              │
│  ✗ Aggregate or weight contradictions                               │
│  ✓ Show confirmation counts                                         │
│  ✗ Calculate "net" signals                                          │
│                                                                      │
│  CR-003: DESCRIPTIVE AI ONLY                                         │
│  ─────────────────────────────────────────────────────────────────  │
│  ✓ "Your charts show..."                                            │
│  ✗ "You should consider..."                                         │
│  ✓ Mandatory disclaimer on all AI content                           │
│  ✗ Dismissible/hideable disclaimers                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 MCC-Specific Constitutional Rules

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| MCR-001 | No Auto-Trade Integration | MCC controls processes, never executes trades |
| MCR-002 | No External Network Calls | MCC only communicates with local services |
| MCR-003 | Graceful Degradation | MCC remains functional if child processes fail |
| MCR-004 | Explicit User Actions | All process controls require user click |
| MCR-005 | Audit Trail Logging | All user actions logged with timestamps |

### 2.3 Technology Constraints

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REFERENCE TECHNOLOGY STACK                                │
│              (DIRECTIONAL ONLY - SEE CREATIVE LATITUDE DIRECTIVE)            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  The following stack is provided as a REFERENCE IMPLEMENTATION ONLY.        │
│  Cursor has FULL AUTHORITY to substitute any or all of these technologies   │
│  with alternatives that Cursor determines to be more modern, performant,    │
│  or suitable for the project goals.                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

REFERENCE DEPENDENCIES (Cursor May Replace):
├── electron: ^29.0.0          (or alternative desktop framework)
├── react: ^18.2.0             (or alternative UI library)
├── react-dom: ^18.2.0         (if React is used)
├── zustand: ^4.5.0            (or alternative state management)
├── tailwindcss: ^3.4.0        (or alternative styling approach)
├── lucide-react: ^0.344.0     (or alternative icon library)
├── electron-vite: ^2.0.0      (or alternative build tooling)
└── @vitejs/plugin-react: ^4.2.1 (if React/Vite are used)

Cursor is encouraged to evaluate and potentially select:
├── More recent versions of specified libraries
├── Alternative frameworks (Tauri, etc.) if justified
├── Modern styling solutions (CSS-in-JS, etc.)
├── Performance-optimized alternatives
└── Any libraries that improve developer experience or end-user experience

CONSTITUTIONAL FORBIDDEN (INVIOLABLE - Cannot Be Added):
├── External analytics (violates user privacy)
├── Cloud services/external APIs (violates MCR-002)
├── Auto-update services (violates user control)
├── Telemetry of any kind (violates user privacy)
└── Trade execution APIs (violates CR-001)
```

---

# STAGE 3: ARCHITECTURE
## System Structure

### 3.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         MISSION CONTROL CONSOLE                               │
│                        Electron Application Shell                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                          MAIN PROCESS                                    │ │
│  │                        (Node.js Runtime)                                 │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐  │ │
│  │  │   Window    │  │   Process   │  │     IPC     │  │    Config     │  │ │
│  │  │  Manager    │  │  Orchestrator│  │   Bridge    │  │   Manager     │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────────┘  │ │
│  │         │                │                │                  │          │ │
│  └─────────┼────────────────┼────────────────┼──────────────────┼──────────┘ │
│            │                │                │                  │            │
│            ▼                ▼                ▼                  ▼            │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                     CONTEXT BRIDGE (Secure IPC)                         │ │
│  │                   preload.ts - contextBridge.exposeInMainWorld          │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│            │                │                │                  │            │
│            ▼                ▼                ▼                  ▼            │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        RENDERER PROCESS                                  │ │
│  │                      (React Application)                                 │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐  │ │
│  │  │  Dashboard  │  │   Process   │  │     Log     │  │   Settings    │  │ │
│  │  │    View     │  │   Controls  │  │   Viewer    │  │     View      │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────────┘  │ │
│  │                                                                          │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │ │
│  │  │  WebView:   │  │  WebView:   │  │   Quick     │                      │ │
│  │  │  Frontend   │  │  API Docs   │  │  Actions    │                      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                      │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Child Process Management
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          MANAGED CHILD PROCESSES                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────┐          ┌─────────────────────────┐           │
│  │      BACKEND PROCESS    │          │     FRONTEND PROCESS    │           │
│  │   python -m uvicorn     │          │       npm run dev       │           │
│  │   src.main:app          │          │      (Vite server)      │           │
│  │   Port: 8000            │          │      Port: 5173         │           │
│  └─────────────────────────┘          └─────────────────────────┘           │
│              │                                    │                          │
│              └────────────────┬───────────────────┘                          │
│                               ▼                                              │
│                    ┌─────────────────────┐                                  │
│                    │   HEALTH MONITOR    │                                  │
│                    │  /health endpoints  │                                  │
│                    │  Process heartbeats │                                  │
│                    └─────────────────────┘                                  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Directory Structure

```
mission-control/
├── electron/
│   ├── main/
│   │   ├── index.ts              # Main process entry
│   │   ├── windowManager.ts      # BrowserWindow management
│   │   ├── processOrchestrator.ts # Child process control
│   │   ├── healthMonitor.ts      # Service health checks
│   │   ├── configManager.ts      # Persistent settings
│   │   ├── logAggregator.ts      # Log collection/streaming
│   │   └── ipc/
│   │       ├── handlers.ts       # IPC message handlers
│   │       └── channels.ts       # Channel constants
│   └── preload/
│       └── index.ts              # Context bridge setup
├── src/
│   ├── main.tsx                  # React entry point
│   ├── App.tsx                   # Root component
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppShell.tsx      # Main layout
│   │   │   ├── Sidebar.tsx       # Navigation
│   │   │   └── TitleBar.tsx      # Custom title bar
│   │   ├── dashboard/
│   │   │   ├── StatusPanel.tsx   # Service status grid
│   │   │   ├── MetricsCard.tsx   # Individual metric
│   │   │   └── QuickActions.tsx  # Action buttons
│   │   ├── processes/
│   │   │   ├── ProcessCard.tsx   # Process status/controls
│   │   │   ├── ProcessList.tsx   # All processes view
│   │   │   └── OutputViewer.tsx  # Process stdout/stderr
│   │   ├── logs/
│   │   │   ├── LogViewer.tsx     # Main log display
│   │   │   ├── LogFilter.tsx     # Filter controls
│   │   │   └── LogEntry.tsx      # Single log line
│   │   ├── webviews/
│   │   │   ├── FrontendView.tsx  # Embedded frontend
│   │   │   └── APIDocsView.tsx   # Embedded Swagger
│   │   └── settings/
│   │       ├── SettingsForm.tsx  # Configuration UI
│   │       └── PathSelector.tsx  # Directory picker
│   ├── stores/
│   │   ├── processStore.ts       # Zustand: process state
│   │   ├── logStore.ts           # Zustand: log entries
│   │   ├── settingsStore.ts      # Zustand: app settings
│   │   └── healthStore.ts        # Zustand: health status
│   ├── hooks/
│   │   ├── useIPC.ts             # IPC communication
│   │   ├── useProcess.ts         # Process control
│   │   └── useHealth.ts          # Health monitoring
│   ├── types/
│   │   ├── electron.d.ts         # Electron API types
│   │   ├── process.ts            # Process state types
│   │   └── ipc.ts                # IPC message types
│   └── styles/
│       └── index.css             # Tailwind + custom styles
├── package.json
├── electron-vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
└── index.html
```

### 3.3 IPC Channel Specification

```typescript
// electron/main/ipc/channels.ts

export const IPC_CHANNELS = {
  // Process Control
  PROCESS_START: 'process:start',
  PROCESS_STOP: 'process:stop',
  PROCESS_RESTART: 'process:restart',
  PROCESS_STATUS: 'process:status',
  PROCESS_OUTPUT: 'process:output',

  // Health Monitoring
  HEALTH_CHECK: 'health:check',
  HEALTH_UPDATE: 'health:update',

  // Log Management
  LOG_STREAM: 'log:stream',
  LOG_CLEAR: 'log:clear',
  LOG_EXPORT: 'log:export',

  // Configuration
  CONFIG_GET: 'config:get',
  CONFIG_SET: 'config:set',
  CONFIG_RESET: 'config:reset',

  // Window Control
  WINDOW_MINIMIZE: 'window:minimize',
  WINDOW_MAXIMIZE: 'window:maximize',
  WINDOW_CLOSE: 'window:close',

  // System
  APP_VERSION: 'app:version',
  APP_QUIT: 'app:quit',
} as const;
```

### 3.4 State Management Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ZUSTAND STORE TOPOLOGY                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        processStore                                │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ {                                                            │  │  │
│  │  │   processes: {                                               │  │  │
│  │  │     backend: { status, pid, uptime, memory, cpu },          │  │  │
│  │  │     frontend: { status, pid, uptime, memory, cpu }          │  │  │
│  │  │   },                                                         │  │  │
│  │  │   actions: { start, stop, restart, setStatus }              │  │  │
│  │  │ }                                                            │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                         logStore                                   │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ {                                                            │  │  │
│  │  │   entries: LogEntry[],                                       │  │  │
│  │  │   filters: { level, source, search },                       │  │  │
│  │  │   actions: { addEntry, clear, setFilter, exportLogs }       │  │  │
│  │  │ }                                                            │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                       healthStore                                  │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ {                                                            │  │  │
│  │  │   services: {                                                │  │  │
│  │  │     backend: { healthy, lastCheck, responseTime },          │  │  │
│  │  │     frontend: { healthy, lastCheck, responseTime },         │  │  │
│  │  │     database: { healthy, lastCheck, connectionCount }       │  │  │
│  │  │   },                                                         │  │  │
│  │  │   actions: { checkHealth, updateStatus }                    │  │  │
│  │  │ }                                                            │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      settingsStore                                 │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ {                                                            │  │  │
│  │  │   paths: { project, backend, frontend },                    │  │  │
│  │  │   ports: { backend: 8000, frontend: 5173 },                 │  │  │
│  │  │   behavior: { autoStart, minimizeToTray, checkInterval },   │  │  │
│  │  │   actions: { update, reset, load, save }                    │  │  │
│  │  │ }                                                            │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# STAGE 4: SPECIFICATION
## Interface Control Document

### 4.1 Type Definitions

```typescript
// src/types/process.ts

export type ProcessName = 'backend' | 'frontend';

export type ProcessStatus =
  | 'stopped'      // Not running
  | 'starting'     // Spawning process
  | 'running'      // Healthy and active
  | 'stopping'     // Graceful shutdown in progress
  | 'crashed'      // Exited with error
  | 'restarting';  // Automatic restart in progress

export interface ProcessState {
  name: ProcessName;
  status: ProcessStatus;
  pid: number | null;
  startTime: number | null;
  uptime: number;
  memory: number;         // MB
  cpu: number;            // Percentage
  restartCount: number;
  lastError: string | null;
}

export interface ProcessConfig {
  name: ProcessName;
  command: string;
  args: string[];
  cwd: string;
  env: Record<string, string>;
  port: number;
  healthEndpoint: string;
}
```

```typescript
// src/types/ipc.ts

export interface IPCRequest<T = unknown> {
  channel: string;
  payload: T;
  requestId: string;
}

export interface IPCResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  requestId: string;
}

// Process Control Messages
export interface ProcessStartRequest {
  name: ProcessName;
  force?: boolean;
}

export interface ProcessStopRequest {
  name: ProcessName;
  graceful?: boolean;
  timeout?: number;
}

export interface ProcessStatusResponse {
  processes: Record<ProcessName, ProcessState>;
}
```

```typescript
// src/types/log.ts

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';
export type LogSource = 'backend' | 'frontend' | 'mcc' | 'system';

export interface LogEntry {
  id: string;
  timestamp: number;
  level: LogLevel;
  source: LogSource;
  message: string;
  metadata?: Record<string, unknown>;
}

export interface LogFilter {
  levels: LogLevel[];
  sources: LogSource[];
  search: string;
  startTime?: number;
  endTime?: number;
}
```

```typescript
// src/types/health.ts

export interface ServiceHealth {
  name: string;
  healthy: boolean;
  lastCheck: number;
  responseTime: number;    // ms
  details?: Record<string, unknown>;
}

export interface SystemHealth {
  overall: 'healthy' | 'degraded' | 'unhealthy';
  services: Record<string, ServiceHealth>;
  lastUpdate: number;
}
```

### 4.2 Component Specifications

#### CBS-MCC-001: ProcessCard

```typescript
// src/components/processes/ProcessCard.tsx

interface ProcessCardProps {
  process: ProcessState;
  onStart: () => void;
  onStop: () => void;
  onRestart: () => void;
  onViewLogs: () => void;
}

/**
 * CONSTITUTIONAL COMPLIANCE:
 * - Buttons: Start, Stop, Restart, View Logs (ALLOWED - process control)
 * - NO buttons: Buy, Sell, Trade, Execute (FORBIDDEN)
 */
```

**Visual Specification:**
```
┌─────────────────────────────────────────────────────────────────┐
│  ● Backend Server                                    [Running]  │
│  ─────────────────────────────────────────────────────────────  │
│  PID: 12345    Uptime: 2h 34m    Memory: 156 MB    CPU: 1.2%   │
│  Port: 8000    Health: ✓ Healthy                               │
│  ─────────────────────────────────────────────────────────────  │
│  [Stop]    [Restart]    [View Logs]                            │
└─────────────────────────────────────────────────────────────────┘
```

#### CBS-MCC-002: StatusPanel

```typescript
// src/components/dashboard/StatusPanel.tsx

interface StatusPanelProps {
  health: SystemHealth;
  processes: Record<ProcessName, ProcessState>;
}

/**
 * Grid layout showing all service statuses
 * Equal-weight display (no service prioritized over others)
 */
```

**Visual Specification:**
```
┌────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM STATUS                                     │
├────────────────────┬────────────────────┬────────────────────┬─────────────┤
│  ● Backend         │  ● Frontend        │  ● Database        │  ● Overall  │
│    Running         │    Running         │    Connected       │    Healthy  │
│    Port 8000       │    Port 5173       │    SQLite          │    ✓ ✓ ✓   │
│    ✓ Healthy       │    ✓ Healthy       │    ✓ Healthy       │             │
└────────────────────┴────────────────────┴────────────────────┴─────────────┘
```

#### CBS-MCC-003: LogViewer

```typescript
// src/components/logs/LogViewer.tsx

interface LogViewerProps {
  entries: LogEntry[];
  filter: LogFilter;
  onFilterChange: (filter: LogFilter) => void;
  maxEntries?: number;  // Default: 1000
}

/**
 * Virtual scrolling for performance
 * Color coding by log level
 * Source filtering
 */
```

**Visual Specification:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Filters: [All Levels ▼]  [All Sources ▼]  [🔍 Search...          ]  [Clear]│
├─────────────────────────────────────────────────────────────────────────────┤
│  10:45:23.456  [INFO]   backend   Server started on port 8000               │
│  10:45:23.789  [INFO]   frontend  Vite dev server running                   │
│  10:45:24.012  [DEBUG]  backend   Database connection established           │
│  10:45:25.567  [WARN]   backend   Slow query detected: 245ms                │
│  10:45:26.890  [ERROR]  frontend  Failed to fetch /api/health               │
│  ...                                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Showing 156 entries (filtered from 1,234 total)              [Export Logs] │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### CBS-MCC-004: QuickActions

```typescript
// src/components/dashboard/QuickActions.tsx

interface QuickActionsProps {
  onStartAll: () => void;
  onStopAll: () => void;
  onRestartAll: () => void;
  onOpenFrontend: () => void;
  onOpenAPIDocs: () => void;
}

/**
 * CONSTITUTIONAL COMPLIANCE:
 * - Only process control and navigation actions
 * - NO trade-related actions
 */
```

**Visual Specification:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            QUICK ACTIONS                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │
│  │ ▶ Start All │  │ ■ Stop All  │  │ ↻ Restart   │                          │
│  └─────────────┘  └─────────────┘  └─────────────┘                          │
│                                                                              │
│  ┌─────────────────────────┐  ┌─────────────────────────┐                   │
│  │ 🌐 Open Frontend        │  │ 📖 Open API Docs        │                   │
│  └─────────────────────────┘  └─────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Page Specifications

#### Page: Dashboard (Home)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ═══════════════════════════════════════════════════════════════════════════   │
│  ░░░ CIA-SIE MISSION CONTROL ░░░                           [_] [□] [×]         │
│  ═══════════════════════════════════════════════════════════════════════════   │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│              │                                                                   │
│  ┌────────┐  │   ┌──────────────────────────────────────────────────────────┐  │
│  │ 🏠     │  │   │                    SYSTEM STATUS                         │  │
│  │Dashboard│  │   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  └────────┘  │   │  │ Backend  │ │ Frontend │ │ Database │ │ Overall  │   │  │
│              │   │  │ Running  │ │ Running  │ │Connected │ │ Healthy  │   │  │
│  ┌────────┐  │   │  │   ●      │ │   ●      │ │   ●      │ │  ✓✓✓    │   │  │
│  │ 📋     │  │   │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  │Processes│  │   └──────────────────────────────────────────────────────────┘  │
│  └────────┘  │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│  ┌────────┐  │   │                   QUICK ACTIONS                          │  │
│  │ 📜     │  │   │  [▶ Start All]  [■ Stop All]  [↻ Restart All]           │  │
│  │ Logs   │  │   │  [🌐 Open Frontend]  [📖 Open API Docs]                  │  │
│  └────────┘  │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│  ┌────────┐  │   ┌──────────────────────────────────────────────────────────┐  │
│  │ 🌐     │  │   │                  RECENT ACTIVITY                         │  │
│  │Frontend│  │   │  10:45:23  Backend started successfully                  │  │
│  └────────┘  │   │  10:45:24  Frontend dev server running                   │  │
│              │   │  10:45:25  Health check: All systems nominal             │  │
│  ┌────────┐  │   └──────────────────────────────────────────────────────────┘  │
│  │ 📖     │  │                                                                   │
│  │API Docs│  │   ┌──────────────────────────────────────────────────────────┐  │
│  └────────┘  │   │                   SYSTEM METRICS                         │  │
│              │   │  Memory: 312 MB    CPU: 2.1%    Uptime: 4h 23m           │  │
│  ┌────────┐  │   └──────────────────────────────────────────────────────────┘  │
│  │ ⚙️     │  │                                                                   │
│  │Settings│  │                                                                   │
│  └────────┘  │                                                                   │
│              │                                                                   │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│  CIA-SIE Mission Control v1.0.0    Backend: ● Running    Frontend: ● Running   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Page: Processes

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ═══════════════════════════════════════════════════════════════════════════   │
│  ░░░ CIA-SIE MISSION CONTROL ░░░                           [_] [□] [×]         │
│  ═══════════════════════════════════════════════════════════════════════════   │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│              │                                                                   │
│  [Sidebar]   │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  BACKEND SERVER                                [Running] │  │
│              │   │  ─────────────────────────────────────────────────────── │  │
│              │   │  Command: python -m uvicorn src.main:app --reload        │  │
│              │   │  PID: 12345    Port: 8000    Health: ✓ Healthy           │  │
│              │   │  Uptime: 4h 23m    Memory: 156 MB    CPU: 1.2%          │  │
│              │   │  Restarts: 0       Last Error: None                      │  │
│              │   │  ─────────────────────────────────────────────────────── │  │
│              │   │  [Stop]  [Restart]  [View Logs]  [View Output]           │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
│              │   ┌──────────────────────────────────────────────────────────┐  │
│              │   │  FRONTEND SERVER                               [Running] │  │
│              │   │  ─────────────────────────────────────────────────────── │  │
│              │   │  Command: npm run dev                                    │  │
│              │   │  PID: 12346    Port: 5173    Health: ✓ Healthy           │  │
│              │   │  Uptime: 4h 23m    Memory: 156 MB    CPU: 0.8%          │  │
│              │   │  Restarts: 0       Last Error: None                      │  │
│              │   │  ─────────────────────────────────────────────────────── │  │
│              │   │  [Stop]  [Restart]  [View Logs]  [View Output]           │  │
│              │   └──────────────────────────────────────────────────────────┘  │
│              │                                                                   │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│  CIA-SIE Mission Control v1.0.0    Backend: ● Running    Frontend: ● Running   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Page: Logs

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ═══════════════════════════════════════════════════════════════════════════   │
│  ░░░ CIA-SIE MISSION CONTROL ░░░                           [_] [□] [×]         │
│  ═══════════════════════════════════════════════════════════════════════════   │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│              │                                                                   │
│  [Sidebar]   │   ┌─────────────────────────────────────────────────────────┐   │
│              │   │ Filters:                                                 │   │
│              │   │ Level: [All ▼]  Source: [All ▼]  [🔍 Search...    ]     │   │
│              │   │ [Auto-scroll ✓]  [Timestamps ✓]  [Clear]  [Export]      │   │
│              │   └─────────────────────────────────────────────────────────┘   │
│              │                                                                   │
│              │   ┌─────────────────────────────────────────────────────────┐   │
│              │   │ 10:45:23.456  INFO   backend   Server started           │   │
│              │   │ 10:45:23.789  INFO   frontend  Vite server running      │   │
│              │   │ 10:45:24.012  DEBUG  backend   DB connected             │   │
│              │   │ 10:45:25.567  WARN   backend   Slow query: 245ms        │   │
│              │   │ 10:45:26.890  ERROR  frontend  Fetch failed: /api/health│   │
│              │   │ 10:45:27.123  INFO   backend   Request: GET /api/health │   │
│              │   │ 10:45:27.456  DEBUG  backend   Response: 200 OK         │   │
│              │   │ 10:45:28.789  INFO   mcc       Health check passed      │   │
│              │   │ ...                                                      │   │
│              │   │                                                          │   │
│              │   │                                                          │   │
│              │   │                                                          │   │
│              │   └─────────────────────────────────────────────────────────┘   │
│              │   Showing 234 entries (filtered from 1,456 total)               │
│              │                                                                   │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│  CIA-SIE Mission Control v1.0.0    Backend: ● Running    Frontend: ● Running   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

# STAGE 5: IMPLEMENTATION
## Code Generation (Cursor Handoff)

### 5.1 Implementation Phases

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     IMPLEMENTATION PHASE SEQUENCE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: Project Scaffolding                                               │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Create mission-control/ directory                                        │
│  □ Initialize Electron + React project with electron-vite                   │
│  □ Configure TypeScript, Tailwind, ESLint                                   │
│  □ Set up package.json with all dependencies                                │
│                                                                              │
│  PHASE 2: Main Process Core                                                  │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement windowManager.ts (BrowserWindow lifecycle)                     │
│  □ Implement configManager.ts (electron-store)                              │
│  □ Set up IPC channels and handlers                                         │
│  □ Implement preload script with contextBridge                              │
│                                                                              │
│  PHASE 3: Process Orchestration                                              │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement processOrchestrator.ts (child_process spawn)                   │
│  □ Implement healthMonitor.ts (HTTP health checks)                          │
│  □ Implement logAggregator.ts (stdout/stderr streaming)                     │
│  □ Add circuit breaker for crash recovery                                   │
│                                                                              │
│  PHASE 4: Zustand Stores                                                     │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement processStore.ts                                                 │
│  □ Implement logStore.ts                                                     │
│  □ Implement healthStore.ts                                                  │
│  □ Implement settingsStore.ts                                                │
│                                                                              │
│  PHASE 5: Layout Components                                                  │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement AppShell.tsx                                                    │
│  □ Implement Sidebar.tsx                                                     │
│  □ Implement TitleBar.tsx (custom Electron title bar)                       │
│                                                                              │
│  PHASE 6: Dashboard Components                                               │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement StatusPanel.tsx                                                 │
│  □ Implement MetricsCard.tsx                                                 │
│  □ Implement QuickActions.tsx                                                │
│                                                                              │
│  PHASE 7: Process & Log Components                                           │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement ProcessCard.tsx                                                 │
│  □ Implement ProcessList.tsx                                                 │
│  □ Implement LogViewer.tsx                                                   │
│  □ Implement LogFilter.tsx                                                   │
│                                                                              │
│  PHASE 8: Pages & Integration                                                │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Implement DashboardPage.tsx                                               │
│  □ Implement ProcessesPage.tsx                                               │
│  □ Implement LogsPage.tsx                                                    │
│  □ Implement SettingsPage.tsx                                                │
│  □ Implement WebView pages (Frontend, API Docs)                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Configuration Files

#### package.json
```json
{
  "name": "cia-sie-mission-control",
  "version": "1.0.0",
  "description": "Mission Control Console for CIA-SIE",
  "main": "./out/main/index.js",
  "scripts": {
    "dev": "electron-vite dev",
    "build": "electron-vite build",
    "preview": "electron-vite preview",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "zustand": "^4.5.0",
    "lucide-react": "^0.344.0",
    "electron-store": "^8.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "electron": "^29.0.0",
    "electron-vite": "^2.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "typescript": "^5.3.3"
  }
}
```

#### electron-vite.config.ts
```typescript
import { defineConfig, externalizeDepsPlugin } from 'electron-vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  main: {
    plugins: [externalizeDepsPlugin()],
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, 'electron/main/index.ts')
        }
      }
    }
  },
  preload: {
    plugins: [externalizeDepsPlugin()],
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, 'electron/preload/index.ts')
        }
      }
    }
  },
  renderer: {
    root: '.',
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, 'index.html')
        }
      }
    },
    plugins: [react()]
  }
});
```

---

# STAGE 6: VALIDATION
## Testing Strategy

### 6.1 Test Categories

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TEST PYRAMID                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              ┌───────────┐                                   │
│                              │   E2E     │  ◄── Playwright                  │
│                              │  Tests    │      (2-3 critical paths)        │
│                            ┌─┴───────────┴─┐                                │
│                            │ Integration   │  ◄── Vitest                    │
│                            │    Tests      │      (IPC, Process mgmt)       │
│                          ┌─┴───────────────┴─┐                              │
│                          │   Component Tests  │  ◄── Vitest + Testing Lib  │
│                          │                    │      (React components)     │
│                        ┌─┴────────────────────┴─┐                           │
│                        │      Unit Tests         │  ◄── Vitest             │
│                        │                         │      (Stores, utilities) │
│                        └─────────────────────────┘                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Constitutional Compliance Tests

```typescript
// tests/constitutional.test.ts

describe('Constitutional Compliance', () => {
  describe('CR-001: Decision-Support Only', () => {
    it('should not render Buy/Sell/Trade buttons', () => {
      // Scan all components for forbidden button labels
    });

    it('should not contain prescriptive language', () => {
      // Scan for "should", "recommend", "suggest", "consider"
    });
  });

  describe('MCR-001: No Auto-Trade Integration', () => {
    it('should only expose process control actions', () => {
      // Verify IPC channels are limited to process control
    });
  });

  describe('MCR-004: Explicit User Actions', () => {
    it('should require user click for all process controls', () => {
      // Verify no automatic process starts without user action
    });
  });
});
```

### 6.3 Test File Structure

```
mission-control/
├── tests/
│   ├── unit/
│   │   ├── stores/
│   │   │   ├── processStore.test.ts
│   │   │   ├── logStore.test.ts
│   │   │   └── healthStore.test.ts
│   │   └── utils/
│   │       └── formatting.test.ts
│   ├── integration/
│   │   ├── ipc.test.ts
│   │   ├── processOrchestrator.test.ts
│   │   └── healthMonitor.test.ts
│   ├── component/
│   │   ├── ProcessCard.test.tsx
│   │   ├── StatusPanel.test.tsx
│   │   └── LogViewer.test.tsx
│   ├── e2e/
│   │   ├── startup.spec.ts
│   │   └── processControl.spec.ts
│   └── constitutional/
│       └── compliance.test.ts
└── vitest.config.ts
```

---

# STAGE 7: INTEGRATION
## Component Boundaries

### 7.1 Integration Points

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION BOUNDARY MAP                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MCC Application                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                      │    │
│  │  Main Process ◄────────────────────────────────────────────────────┐│    │
│  │       │                                                            ││    │
│  │       │ IPC                                                        ││    │
│  │       ▼                                                            ││    │
│  │  Renderer Process                                                  ││    │
│  │                                                                    ││    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│            │                           │                           │         │
│            │ spawn()                   │ HTTP                      │ HTTP    │
│            ▼                           ▼                           ▼         │
│  ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐  │
│  │  CIA-SIE        │        │  CIA-SIE        │        │  SQLite         │  │
│  │  Backend        │◄──────▶│  Frontend       │        │  Database       │  │
│  │  (Port 8000)    │        │  (Port 5173)    │        │                 │  │
│  └─────────────────┘        └─────────────────┘        └─────────────────┘  │
│                                                                              │
│  INTEGRATION CONTRACTS:                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • MCC → Backend: HTTP GET /health (health check)                           │
│  • MCC → Frontend: HTTP GET / (availability check)                          │
│  • MCC → Backend: Process spawn (python -m uvicorn...)                      │
│  • MCC → Frontend: Process spawn (npm run dev)                              │
│  • Renderer → Main: IPC channels (process control, config)                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Integration Test Checklist

| Test ID | Integration Point | Test Description | Pass Criteria |
|---------|-------------------|------------------|---------------|
| INT-001 | MCC → Backend Spawn | Spawn backend process | Process running, PID available |
| INT-002 | MCC → Frontend Spawn | Spawn frontend process | Process running, PID available |
| INT-003 | MCC → Backend Health | HTTP health check | 200 OK within 1s |
| INT-004 | MCC → Frontend Health | HTTP availability | 200 OK within 1s |
| INT-005 | IPC: Process Control | Start/stop via IPC | Correct state transitions |
| INT-006 | IPC: Log Streaming | Log events via IPC | Entries appear in UI |
| INT-007 | Process Crash Recovery | Kill backend, verify restart | Auto-restart within 5s |

---

# STAGE 8: VERIFICATION
## Audit & Compliance

### 8.1 Verification Matrix

| Requirement ID | Requirement | Verification Method | Status |
|----------------|-------------|---------------------|--------|
| REQ-CONST-001 | No Buy/Sell buttons | Code scan + UI audit | ☐ |
| REQ-CONST-002 | No prescriptive language | Text search audit | ☐ |
| REQ-CONST-003 | Disclaimer on AI content | Component audit | ☐ |
| REQ-FUNC-001 | Start backend process | Integration test | ☐ |
| REQ-FUNC-002 | Stop backend process | Integration test | ☐ |
| REQ-FUNC-003 | Start frontend process | Integration test | ☐ |
| REQ-FUNC-004 | Stop frontend process | Integration test | ☐ |
| REQ-FUNC-005 | Health monitoring | Integration test | ☐ |
| REQ-FUNC-006 | Log aggregation | Integration test | ☐ |
| REQ-FUNC-007 | WebView embedding | Manual test | ☐ |
| REQ-PERF-001 | Startup < 3s | Performance test | ☐ |
| REQ-PERF-002 | Memory < 500MB | Performance test | ☐ |
| REQ-PERF-003 | CPU idle < 2% | Performance test | ☐ |

### 8.2 Audit Procedure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VERIFICATION AUDIT PROCEDURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: Code Scan                                                           │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ grep -r "Buy\|Sell\|Trade\|Execute" src/                                 │
│  □ grep -r "should\|recommend\|suggest" src/                                │
│  □ Verify 0 matches for forbidden terms                                      │
│                                                                              │
│  STEP 2: Component Audit                                                     │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Review all button labels in components                                    │
│  □ Verify process control buttons only                                       │
│  □ Verify no trade-related actions                                           │
│                                                                              │
│  STEP 3: Test Execution                                                      │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Run full test suite: npm test                                             │
│  □ Verify 100% pass rate on constitutional tests                            │
│  □ Verify 100% pass rate on integration tests                               │
│                                                                              │
│  STEP 4: Manual Verification                                                 │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Launch application                                                        │
│  □ Test all process controls                                                 │
│  □ Verify WebView embedding                                                  │
│  □ Test log viewer functionality                                             │
│                                                                              │
│  STEP 5: Performance Verification                                            │
│  ────────────────────────────────────────────────────────────────────────   │
│  □ Measure cold start time                                                   │
│  □ Measure memory usage (Activity Monitor)                                   │
│  □ Measure idle CPU usage                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# STAGE 9: RECONCILIATION
## Variance Documentation

### 9.1 Gap Taxonomy

Following the Genesis Codex gap classification:

| Gap Type | Description | Resolution Method |
|----------|-------------|-------------------|
| Schema Gap | Type mismatch between components | TypeScript strict mode |
| Phantom Gap | Referenced but non-existent code | ESLint no-undef rule |
| Orphan Gap | Unreferenced code | ESLint no-unused-vars |
| Contract Gap | API mismatch | Integration tests |
| Temporal Gap | Race conditions | Async/await patterns |
| Auth Gap | Security boundary violation | contextIsolation: true |
| State Gap | Inconsistent state | Zustand atomic updates |
| Error Gap | Unhandled errors | try/catch + ErrorBoundary |

### 9.2 Reconciliation Checklist

| Item | Specification | Implementation | Variance | Resolution |
|------|---------------|----------------|----------|------------|
| Process spawn | child_process.spawn | - | - | - |
| Health check | HTTP GET /health | - | - | - |
| IPC channels | 12 channels defined | - | - | - |
| Zustand stores | 4 stores defined | - | - | - |
| React pages | 6 pages defined | - | - | - |

---

# STAGE 10: REMEDIATION
## Systematic Correction

### 10.1 Remediation Protocol

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REMEDIATION WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  On Gap Detection:                                                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│    ┌────────────┐      ┌────────────┐      ┌────────────┐                  │
│    │  DETECT    │ ──▶  │  CLASSIFY  │ ──▶  │  DOCUMENT  │                  │
│    │   Gap      │      │   Gap Type │      │   in RTM   │                  │
│    └────────────┘      └────────────┘      └────────────┘                  │
│           │                                       │                          │
│           ▼                                       ▼                          │
│    ┌────────────┐      ┌────────────┐      ┌────────────┐                  │
│    │  ASSESS    │ ──▶  │  IMPLEMENT │ ──▶  │  VERIFY    │                  │
│    │   Impact   │      │    Fix     │      │    Fix     │                  │
│    └────────────┘      └────────────┘      └────────────┘                  │
│                                                   │                          │
│                                                   ▼                          │
│                                            ┌────────────┐                   │
│                                            │   UPDATE   │                   │
│                                            │    RTM     │                   │
│                                            └────────────┘                   │
│                                                                              │
│  Impact Assessment Scale:                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│  CRITICAL: Constitutional violation → Immediate fix required                │
│  HIGH: Feature broken → Fix before next stage                               │
│  MEDIUM: Sub-optimal behavior → Fix before certification                    │
│  LOW: Minor issue → Fix if time permits                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# STAGE 11: CERTIFICATION
## Launch Readiness

### 11.1 Certification Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LAUNCH READINESS CERTIFICATION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CONSTITUTIONAL COMPLIANCE                                      Status       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ No Buy/Sell/Trade buttons in UI                              ☐ PASS      │
│  □ No prescriptive language in text                             ☐ PASS      │
│  □ Disclaimer present on all AI content                         ☐ PASS      │
│  □ Only process control actions available                       ☐ PASS      │
│  □ All user actions require explicit click                      ☐ PASS      │
│                                                                              │
│  FUNCTIONAL REQUIREMENTS                                        Status       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Backend process control (start/stop/restart)                 ☐ PASS      │
│  □ Frontend process control (start/stop/restart)                ☐ PASS      │
│  □ Health monitoring with auto-refresh                          ☐ PASS      │
│  □ Log aggregation with filtering                               ☐ PASS      │
│  □ WebView embedding (Frontend + API Docs)                      ☐ PASS      │
│  □ Settings persistence                                         ☐ PASS      │
│  □ System tray integration                                      ☐ PASS      │
│                                                                              │
│  PERFORMANCE REQUIREMENTS                                       Status       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Cold start < 3 seconds                                       ☐ PASS      │
│  □ Memory usage < 500 MB                                        ☐ PASS      │
│  □ CPU idle < 2%                                                ☐ PASS      │
│  □ Process spawn < 5 seconds                                    ☐ PASS      │
│                                                                              │
│  TEST COVERAGE                                                  Status       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  □ Unit tests passing                                           ☐ PASS      │
│  □ Integration tests passing                                    ☐ PASS      │
│  □ E2E tests passing                                            ☐ PASS      │
│  □ Constitutional compliance tests passing                      ☐ PASS      │
│                                                                              │
│  CERTIFICATION SIGNATURE                                                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Certified by: _____________________  Date: _______________                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# STAGE 12: OPERATION
## Stewardship

### 12.1 Operational Procedures

#### Start Procedure
```
1. Launch CIA-SIE Mission Control
2. Wait for dashboard to load (< 3 seconds)
3. Click "Start All" or individual process start buttons
4. Verify green status indicators for all services
5. Begin using CIA-SIE via embedded frontend view
```

#### Stop Procedure
```
1. Click "Stop All" in Quick Actions
2. Wait for graceful shutdown (< 5 seconds)
3. Verify red status indicators for all services
4. Close Mission Control window or minimize to tray
```

#### Troubleshooting
```
Issue: Backend fails to start
Action: Check port 8000 availability, review logs

Issue: Frontend fails to start
Action: Check port 5173 availability, review logs

Issue: Health check fails
Action: Restart affected service, check network

Issue: High memory usage
Action: Restart application, check for log overflow
```

### 12.2 Maintenance Schedule

| Task | Frequency | Description |
|------|-----------|-------------|
| Log cleanup | Weekly | Clear old log files |
| Dependency update | Monthly | Check for security updates |
| Performance audit | Quarterly | Review resource usage |
| Constitutional audit | On change | Verify no violations |

---

# HITL APPROVAL GATES

## Gate 1: Vision Approval

**HITL CHECKPOINT: VISION & ARCHITECTURE APPROVAL**

Before proceeding to implementation, the user must approve:

1. ☐ The vision statement aligns with user expectations
2. ☐ The architecture diagram is understood and accepted
3. ☐ The component structure is approved
4. ☐ The GUI mockups represent the desired interface
5. ☐ The constitutional rules are complete and correct

**User Approval Required:** YES / NO
**Date:** _______________
**Signature:** _______________

---

## Gate 2: Code Approval

**HITL CHECKPOINT: IMPLEMENTATION APPROVAL**

After Cursor generates code, the user must approve:

1. ☐ All implementation phases are complete
2. ☐ All tests pass
3. ☐ Constitutional compliance verified
4. ☐ No security vulnerabilities detected
5. ☐ Performance targets met

**User Approval Required:** YES / NO
**Date:** _______________
**Signature:** _______________

---

## Gate 3: Launch Approval

**HITL CHECKPOINT: LAUNCH READINESS**

Before deploying to production use, the user must approve:

1. ☐ All certification checklist items pass
2. ☐ Operational procedures documented
3. ☐ Troubleshooting guide complete
4. ☐ User acceptance testing complete
5. ☐ Ready for daily use

**User Approval Required:** YES / NO
**Date:** _______________
**Signature:** _______________

---

## Gate 4: Operational Handoff

**HITL CHECKPOINT: OPERATIONAL STATUS**

After launch, confirm transition to operation:

1. ☐ Application running in production mode
2. ☐ User trained on operational procedures
3. ☐ Maintenance schedule established
4. ☐ Support channels identified
5. ☐ Handoff complete

**User Approval Required:** YES / NO
**Date:** _______________
**Signature:** _______________

---

# CURSOR HANDOFF PROTOCOL

## Handoff Instructions for Cursor

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│             ⚡ CURSOR IMPLEMENTATION PROTOCOL (REVISED) ⚡                   │
│                                                                              │
│     THIS PROTOCOL SUPERSEDES ALL PREVIOUS HANDOFF INSTRUCTIONS               │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 0: READ THE CREATIVE LATITUDE DIRECTIVE                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Before proceeding, read and understand the "Creative Latitude Directive"   │
│  section at the beginning of this document. It grants you FULL AUTHORITY    │
│  to deviate from all specifications EXCEPT constitutional rules.             │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 1: CREATE YOUR IMPLEMENTATION PLAN (MANDATORY - BEFORE ANY CODE)      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  You MUST produce a "CURSOR_IMPLEMENTATION_PLAN.md" document containing:    │
│                                                                              │
│    Section A: Executive Divergence Summary                                   │
│    - Every area where your approach differs from this specification         │
│    - What was specified vs. what you will do instead                        │
│                                                                              │
│    Section B: Technology Stack Declaration                                   │
│    - For each technology: specified version → your selection + rationale    │
│                                                                              │
│    Section C: Architecture Decisions                                         │
│    - Your proposed architecture with diagrams                               │
│    - How it differs from the reference and why                              │
│                                                                              │
│    Section D: Phase-by-Phase Plan                                            │
│    - Your interpretation of each Genesis Codex stage                        │
│    - Specific deliverables you will produce                                 │
│                                                                              │
│    Section E: GUI/UX Approach                                                │
│    - How you will interpret the visual mockups                              │
│    - Design system and libraries you will employ                            │
│                                                                              │
│    Section F: Risk Assessment                                                │
│    - Potential challenges and mitigation strategies                         │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 2: AWAIT USER APPROVAL (MANDATORY - CANNOT BE SKIPPED)                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Present your Implementation Plan to the user (Neville).                    │
│  The user MUST read and approve your plan before you write ANY code.        │
│  DO NOT proceed until you receive explicit approval.                        │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STEP 3: IMPLEMENT YOUR APPROVED PLAN                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Execute according to YOUR plan, not the reference specifications.          │
│  Flag any additional deviations discovered during implementation.           │
│  Seek clarification when requirements are ambiguous.                        │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CONSTITUTIONAL RULES (INVIOLABLE - CANNOT BE MODIFIED):                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│  CR-001: NO Buy/Sell/Trade buttons                                          │
│  CR-002: Display contradictions, never aggregate                            │
│  CR-003: Descriptive AI only with mandatory disclaimers                     │
│  MCR-001: No auto-trade integration                                          │
│  MCR-002: No external network calls                                          │
│  MCR-003: Graceful degradation                                               │
│  MCR-004: Explicit user actions for all controls                            │
│  MCR-005: Audit trail logging                                                │
│                                                                              │
│  FORBIDDEN DEPENDENCIES (INVIOLABLE):                                        │
│  - Telemetry/analytics                                                       │
│  - Cloud APIs/external services                                              │
│  - Auto-update services                                                      │
│  - Trade execution APIs                                                      │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  YOUR CREATIVE FREEDOM (EXPLICITLY GRANTED):                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ✓ Replace any specified technology with better alternatives                │
│  ✓ Redesign architecture for better performance                             │
│  ✓ Restructure directories as you see fit                                   │
│  ✓ Modify component designs                                                 │
│  ✓ Add any non-forbidden dependencies                                       │
│  ✓ Enhance visual designs beyond mockups                                    │
│  ✓ Apply modern patterns and optimizations                                  │
│  ✓ Propose solutions superior to what was specified                         │
│                                                                              │
│  The specification documents provide CONTEXT and DIRECTION.                 │
│  You provide the IMPLEMENTATION EXPERTISE.                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Reference Documents (Directional Only)

| Document | Purpose | Your Authority |
|----------|---------|----------------|
| MCC_GENESIS_BUILD_SPECIFICATION.md | Reference architecture & structure | May modify entirely |
| MCC_GUI_MOCKUP_REQUIREMENTS.md | Reference visual design | May redesign |
| MCC_HITL_APPROVAL_GATES.md | Approval checkpoints | Must respect gates |

## Critical Reminder

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   The user (Neville) MUST be fully informed of your intended approach       │
│   BEFORE you write code. Your Implementation Plan is not optional.          │
│                                                                              │
│   This ensures:                                                              │
│   1. The user understands exactly what will be built                        │
│   2. Concerns are surfaced before development investment                    │
│   3. There are no surprises in the final deliverable                        │
│   4. The approach is documented for future reference                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# APPENDIX A: REQUIREMENTS TRACEABILITY MATRIX

| Req ID | Requirement | Specification Section | Implementation | Test | Status |
|--------|-------------|----------------------|----------------|------|--------|
| REQ-VIS-001 | Unified command center | Stage 1, §1.1 | - | - | ☐ |
| REQ-VIS-002 | NASA-inspired metaphor | Stage 1, §1.2 | - | - | ☐ |
| REQ-CON-001 | No trade buttons | Stage 2, §2.1 | - | CONST-001 | ☐ |
| REQ-CON-002 | No prescriptive text | Stage 2, §2.1 | - | CONST-002 | ☐ |
| REQ-ARC-001 | Electron main/renderer | Stage 3, §3.1 | - | - | ☐ |
| REQ-ARC-002 | IPC via contextBridge | Stage 3, §3.3 | - | INT-005 | ☐ |
| REQ-ARC-003 | Zustand state mgmt | Stage 3, §3.4 | - | UNIT-* | ☐ |
| REQ-SPC-001 | ProcessCard component | Stage 4, §4.2 | - | COMP-001 | ☐ |
| REQ-SPC-002 | StatusPanel component | Stage 4, §4.2 | - | COMP-002 | ☐ |
| REQ-SPC-003 | LogViewer component | Stage 4, §4.2 | - | COMP-003 | ☐ |
| REQ-IMP-001 | Phase 1-8 complete | Stage 5, §5.1 | - | - | ☐ |
| REQ-VAL-001 | All tests pass | Stage 6, §6.1 | - | ALL | ☐ |
| REQ-INT-001 | Backend spawn | Stage 7, §7.1 | - | INT-001 | ☐ |
| REQ-INT-002 | Frontend spawn | Stage 7, §7.1 | - | INT-002 | ☐ |
| REQ-VER-001 | Verification matrix | Stage 8, §8.1 | - | - | ☐ |
| REQ-CER-001 | Launch readiness | Stage 11, §11.1 | - | - | ☐ |

---

# APPENDIX B: GLOSSARY

| Term | Definition |
|------|------------|
| CIA-SIE | Chart Intelligence Auditor & Signal Intelligence Engine |
| MCC | Mission Control Console |
| HITL | Human-in-the-Loop (approval gates requiring user confirmation) |
| IPC | Inter-Process Communication (Electron main ↔ renderer) |
| RTM | Requirements Traceability Matrix |
| Genesis Codex | Universal Software Genesis Codex (12-stage development framework) |
| Constitutional Rule | Inviolable principle that cannot be overridden |
| Gap | Variance between specification and implementation |

---

# DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-04 | Claude Code | Initial specification |
| 1.1.0 | 2026-01-04 | Claude Code | **MAJOR REVISION**: Added Creative Latitude Directive granting Cursor full implementation freedom within constitutional bounds. Specifications now serve as directional guidance only. Mandatory Cursor Implementation Plan requirement added before any code is written. Technology stack constraints relaxed to permit any dependencies that don't violate constitutional rules. Cursor Handoff Protocol completely revised. |

---

**END OF SPECIFICATION**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
