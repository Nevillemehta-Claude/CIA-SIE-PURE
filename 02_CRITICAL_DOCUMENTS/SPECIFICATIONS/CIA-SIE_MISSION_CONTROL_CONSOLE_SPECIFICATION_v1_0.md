# CIA-SIE MISSION CONTROL CONSOLE
## Complete System Specification & Implementation Blueprint

---

| Document Metadata | Value |
|-------------------|-------|
| **Document ID** | CIA-SIE-SPEC-MCC-001 |
| **Version** | 1.0.0 |
| **Date** | January 4, 2026 |
| **Classification** | MISSION CRITICAL |
| **Author** | Claude Opus 4.5 (claude.ai) |
| **Status** | SPECIFICATION COMPLETE |
| **Audience** | Development Team, Cursor AI, Future Auditors |

---

# TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Vision & Conceptualization](#2-vision--conceptualization)
3. [The Science Behind the Console](#3-the-science-behind-the-console)
4. [System Architecture](#4-system-architecture)
5. [Component Specifications](#5-component-specifications)
6. [User Interface Design](#6-user-interface-design)
7. [State Management & Data Flow](#7-state-management--data-flow)
8. [Error Handling & Resilience](#8-error-handling--resilience)
9. [Implementation Phases](#9-implementation-phases)
10. [Testing & Validation](#10-testing--validation)
11. [Audit & Compliance](#11-audit--compliance)
12. [Deployment as Executable](#12-deployment-as-executable)
13. [Operational Procedures](#13-operational-procedures)
14. [Appendices](#14-appendices)

---

# 1. EXECUTIVE SUMMARY

## 1.1 Purpose

The **CIA-SIE Mission Control Console (MCC)** is a unified command center that provides single-click orchestration of the entire CIA-SIE trading intelligence ecosystem. It serves as the primary interface for system operators to:

- **IGNITE** all system components with one button press
- **MONITOR** real-time health of all services, APIs, and connections
- **CONTROL** individual subsystems with granular start/stop capabilities
- **DIAGNOSE** connectivity issues, glitches, and system anomalies
- **TERMINATE** gracefully or emergency-stop the entire system

## 1.2 Core Value Proposition

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   BEFORE MCC:                                                               │
│   ────────────                                                              │
│   1. Open terminal → cd backend → npm start                                 │
│   2. Open another terminal → cd frontend → npm run dev                      │
│   3. Manually verify Kite API connection                                    │
│   4. Check Claude API health                                                │
│   5. Verify TradingView webhook endpoint                                    │
│   6. Hope nothing crashed while doing steps 1-5                             │
│                                                                             │
│   AFTER MCC:                                                                │
│   ───────────                                                               │
│   1. Click bookmark → Press START → Watch everything ignite                 │
│   2. Real-time dashboard shows all systems GO/NO-GO                         │
│   3. Any failure is immediately visible with diagnostic info                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.3 Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Time to Full System Start | < 30 seconds | From button press to all-green status |
| Component Health Visibility | 100% | All monitored services have status indicators |
| Error Detection Latency | < 2 seconds | Time from failure to UI indication |
| Graceful Shutdown | < 10 seconds | Clean termination of all processes |
| System Recovery | Automatic | Self-healing for transient failures |

---

# 2. VISION & CONCEPTUALIZATION

## 2.1 The Metaphor: Spacecraft Launch Console

The MCC draws inspiration from NASA's Mission Control Center — a centralized command hub where every system's status is visible at a glance, where launch sequences are orchestrated with precision, and where anomalies are detected and addressed in real-time.

```
                    ╔═══════════════════════════════════════════════════════╗
                    ║                                                       ║
                    ║              CIA-SIE MISSION CONTROL                  ║
                    ║                                                       ║
                    ║   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ ║
                    ║   │ BACKEND │  │FRONTEND │  │KITE API │  │CLAUDE AI│ ║
                    ║   │  ████   │  │  ████   │  │  ████   │  │  ████   │ ║
                    ║   │  READY  │  │  READY  │  │  READY  │  │  READY  │ ║
                    ║   └─────────┘  └─────────┘  └─────────┘  └─────────┘ ║
                    ║                                                       ║
                    ║            ┌─────────────────────────┐                ║
                    ║            │                         │                ║
                    ║            │     [ LAUNCH ALL ]      │                ║
                    ║            │                         │                ║
                    ║            └─────────────────────────┘                ║
                    ║                                                       ║
                    ╚═══════════════════════════════════════════════════════╝
```

## 2.2 Design Philosophy

### 2.2.1 The Three Laws of Mission Control

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   LAW 1: VISIBILITY OVER ABSTRACTION                                        │
│   ─────────────────────────────────────                                     │
│   Every system component must have a visible status indicator.              │
│   Hidden states are forbidden. If it runs, it shows.                        │
│                                                                             │
│   LAW 2: CONTROL WITHOUT COMPLEXITY                                         │
│   ────────────────────────────────────                                      │
│   One button to start all. One button to stop all.                          │
│   Granular control available but never required for basic operation.        │
│                                                                             │
│   LAW 3: FAILURE IS INFORMATION                                             │
│   ────────────────────────────────                                          │
│   Every failure mode must be captured, classified, and communicated.        │
│   The console never lies about system state.                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2 Aesthetic Direction: Industrial Command Center

The visual design follows an **Industrial Utilitarian** aesthetic with elements of **Retro-Futurism**:

| Element | Design Choice | Rationale |
|---------|---------------|-----------|
| Color Scheme | Dark slate background (#0a0f14), amber warnings (#f59e0b), green go-states (#10b981), red alerts (#ef4444) | High contrast for instant status recognition |
| Typography | JetBrains Mono (data), Space Grotesk (headers) | Monospace for precision, geometric sans for authority |
| Layout | Grid-based control panels with clear boundaries | Structured like physical control panels |
| Animation | Subtle pulse on active systems, sharp transitions on state change | Conveys liveness without distraction |
| Sound | Optional audio cues for state changes (toggleable) | Multi-sensory awareness |

## 2.3 User Stories

### 2.3.1 Primary User Story

```
AS A system operator (Neville)
I WANT a single bookmarkable page that launches my entire trading system
SO THAT I can go from zero to operational in one click
AND monitor all components in real-time
AND be immediately alerted to any failures
```

### 2.3.2 Supporting User Stories

| ID | Story | Priority |
|----|-------|----------|
| US-001 | As an operator, I want to see which specific component failed when something goes wrong | CRITICAL |
| US-002 | As an operator, I want to start/stop individual services without affecting others | HIGH |
| US-003 | As an operator, I want to see connection latency for external APIs | MEDIUM |
| US-004 | As an operator, I want historical logs of system events | MEDIUM |
| US-005 | As an operator, I want the console to auto-reconnect on transient failures | HIGH |
| US-006 | As an operator, I want to select which services to monitor | MEDIUM |
| US-007 | As an operator, I want emergency shutdown capability | CRITICAL |

---

# 3. THE SCIENCE BEHIND THE CONSOLE

## 3.1 Process Orchestration Theory

The MCC operates on **Hierarchical Process Orchestration (HPO)** principles:

```
                              ┌───────────────────┐
                              │  MCC ORCHESTRATOR │
                              │    (Electron)     │
                              └─────────┬─────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
    ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
    │ PROCESS MANAGER │       │ PROCESS MANAGER │       │ HEALTH MONITOR  │
    │    (Backend)    │       │   (Frontend)    │       │  (All Services) │
    └────────┬────────┘       └────────┬────────┘       └────────┬────────┘
             │                         │                         │
             ▼                         ▼                         ▼
    ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
    │  Node.js Server │       │   Vite Dev/Prod │       │   Health Checks │
    │  (child_process)│       │  (child_process)│       │   (Intervals)   │
    └─────────────────┘       └─────────────────┘       └─────────────────┘
```

### 3.1.1 Key Concepts

**1. Child Process Management**

The MCC uses Node.js `child_process` module to spawn and manage system components:

```javascript
// Conceptual — actual implementation in Section 5
const backendProcess = spawn('npm', ['start'], {
  cwd: '/path/to/backend',
  env: { ...process.env, NODE_ENV: 'production' }
});

backendProcess.on('exit', (code) => {
  // Handle termination, trigger UI update
});
```

**2. Health Check Protocol**

Each component exposes a health endpoint that the MCC polls:

| Component | Health Endpoint | Check Interval | Timeout |
|-----------|-----------------|----------------|---------|
| Backend API | `GET /api/health` | 5 seconds | 3 seconds |
| Kite API | `GET /api/kite/status` | 10 seconds | 5 seconds |
| Claude API | `GET /api/claude/health` | 30 seconds | 10 seconds |
| TradingView Webhook | `GET /api/webhook/status` | 10 seconds | 5 seconds |
| Frontend | `GET /` (200 OK) | 5 seconds | 3 seconds |

**3. State Machine Model**

Each component follows a finite state machine:

```
                    ┌─────────┐
                    │  IDLE   │ ◄──────────────────────────────┐
                    └────┬────┘                                │
                         │ START                               │
                         ▼                                     │
                    ┌─────────┐                                │
           ┌───────►│STARTING │                                │
           │        └────┬────┘                                │
           │             │ READY                               │
           │             ▼                                     │
           │        ┌─────────┐         ┌─────────┐           │
           │        │ RUNNING │────────►│ FAILING │           │
           │        └────┬────┘ HEALTH  └────┬────┘           │
           │             │      FAIL         │                │
           │             │                   │ RECOVERED      │
           │             │ STOP         ┌────┘                │
           │             ▼              │                     │
           │        ┌─────────┐         │                     │
           │        │STOPPING │◄────────┘                     │
           │        └────┬────┘                               │
           │             │ STOPPED                            │
           │             ▼                                    │
           │        ┌─────────┐                               │
           └────────│ STOPPED │───────────────────────────────┘
                    └─────────┘            RESET
```

## 3.2 Inter-Process Communication (IPC)

The MCC uses **Event-Driven IPC** for real-time status updates:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          MCC IPC ARCHITECTURE                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────┐         IPC Channel         ┌─────────────────────┐   │
│   │   RENDERER  │◄───────────────────────────►│    MAIN PROCESS     │   │
│   │  (React UI) │                             │ (Node.js/Electron)  │   │
│   └─────────────┘                             └──────────┬──────────┘   │
│                                                          │              │
│                                                          │              │
│                              ┌────────────────────┬──────┴───────┐      │
│                              │                    │              │      │
│                              ▼                    ▼              ▼      │
│                        ┌──────────┐        ┌──────────┐   ┌──────────┐  │
│                        │ Backend  │        │ Frontend │   │  Health  │  │
│                        │ Process  │        │ Process  │   │ Monitor  │  │
│                        └──────────┘        └──────────┘   └──────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3.2.1 IPC Message Types

| Message Type | Direction | Payload | Purpose |
|--------------|-----------|---------|---------|
| `START_ALL` | Renderer → Main | `{}` | Initiate full system launch |
| `STOP_ALL` | Renderer → Main | `{ graceful: boolean }` | Terminate all processes |
| `START_SERVICE` | Renderer → Main | `{ serviceId: string }` | Start specific service |
| `STOP_SERVICE` | Renderer → Main | `{ serviceId: string }` | Stop specific service |
| `STATUS_UPDATE` | Main → Renderer | `{ serviceId, state, metrics }` | Real-time status |
| `LOG_ENTRY` | Main → Renderer | `{ serviceId, level, message, timestamp }` | Log streaming |
| `ERROR` | Main → Renderer | `{ serviceId, error, recoverable }` | Error notification |

## 3.3 Resilience Engineering

### 3.3.1 Failure Classification

| Class | Name | Examples | Response |
|-------|------|----------|----------|
| F1 | Transient | Network timeout, temporary API unavailability | Auto-retry with exponential backoff |
| F2 | Recoverable | Process crash, memory overflow | Auto-restart with circuit breaker |
| F3 | Degraded | Partial API failure, slow response | Continue with reduced functionality |
| F4 | Critical | Authentication failure, database down | Alert operator, halt dependent systems |
| F5 | Catastrophic | Disk failure, system corruption | Emergency shutdown, preserve state |

### 3.3.2 Circuit Breaker Pattern

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CIRCUIT BREAKER STATES                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐      3 failures      ┌─────────┐     timeout     ┌──────┐│
│   │ CLOSED  │ ──────────────────► │  OPEN   │ ─────────────► │HALF- ││
│   │(normal) │                      │(failing)│                │OPEN  ││
│   └────▲────┘                      └─────────┘                └──┬───┘│
│        │                                                         │     │
│        │ success                              1 failure ─────────┘     │
│        │                                                               │
│        └───────────────────── 1 success ───────────────────────────────┘
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3.3 Retry Policy

```javascript
// Exponential backoff with jitter
const retryPolicy = {
  maxRetries: 5,
  baseDelay: 1000,      // 1 second
  maxDelay: 30000,      // 30 seconds
  backoffMultiplier: 2,
  jitterFactor: 0.1     // ±10% randomization
};

function calculateDelay(attempt) {
  const exponentialDelay = Math.min(
    retryPolicy.baseDelay * Math.pow(retryPolicy.backoffMultiplier, attempt),
    retryPolicy.maxDelay
  );
  const jitter = exponentialDelay * retryPolicy.jitterFactor * (Math.random() * 2 - 1);
  return exponentialDelay + jitter;
}
```

---

# 4. SYSTEM ARCHITECTURE

## 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CIA-SIE MCC ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        ELECTRON APPLICATION                           │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                      RENDERER PROCESS                           │  │  │
│  │  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐   │  │  │
│  │  │  │  DASHBOARD    │  │  CONTROL      │  │  LOG VIEWER       │   │  │  │
│  │  │  │  COMPONENT    │  │  PANEL        │  │  COMPONENT        │   │  │  │
│  │  │  │               │  │               │  │                   │   │  │  │
│  │  │  │ • Status Grid │  │ • Start All   │  │ • Real-time logs  │   │  │  │
│  │  │  │ • Metrics     │  │ • Stop All    │  │ • Filters         │   │  │  │
│  │  │  │ • Alerts      │  │ • Individual  │  │ • Export          │   │  │  │
│  │  │  └───────────────┘  └───────────────┘  └───────────────────┘   │  │  │
│  │  │                                                                 │  │  │
│  │  │  ┌───────────────────────────────────────────────────────────┐ │  │  │
│  │  │  │                    STATE MANAGEMENT                       │ │  │  │
│  │  │  │                    (Zustand/Redux)                        │ │  │  │
│  │  │  └───────────────────────────────────────────────────────────┘ │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                │                                      │  │
│  │                                │ IPC Bridge                           │  │
│  │                                │                                      │  │
│  │  ┌─────────────────────────────▼───────────────────────────────────┐  │  │
│  │  │                       MAIN PROCESS                              │  │  │
│  │  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐   │  │  │
│  │  │  │  PROCESS      │  │  HEALTH       │  │  CONFIG           │   │  │  │
│  │  │  │  ORCHESTRATOR │  │  MONITOR      │  │  MANAGER          │   │  │  │
│  │  │  │               │  │               │  │                   │   │  │  │
│  │  │  │ • Spawn       │  │ • Poll        │  │ • Load paths      │   │  │  │
│  │  │  │ • Kill        │  │ • Timeout     │  │ • Env vars        │   │  │  │
│  │  │  │ • Monitor     │  │ • Alert       │  │ • Service config  │   │  │  │
│  │  │  └───────────────┘  └───────────────┘  └───────────────────┘   │  │  │
│  │  │                                                                 │  │  │
│  │  │  ┌───────────────────────────────────────────────────────────┐ │  │  │
│  │  │  │               CHILD PROCESS LAYER                         │ │  │  │
│  │  │  │                                                           │ │  │  │
│  │  │  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │ │  │  │
│  │  │  │   │ Backend │  │Frontend │  │  Kite   │  │ Claude  │    │ │  │  │
│  │  │  │   │ Server  │  │  Dev    │  │ Poller  │  │ Health  │    │ │  │  │
│  │  │  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘    │ │  │  │
│  │  │  │                                                           │ │  │  │
│  │  │  └───────────────────────────────────────────────────────────┘ │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Application Shell** | Electron 29.x | Cross-platform desktop app, Node.js backend, Chromium renderer |
| **Frontend Framework** | React 18.x | Component-based UI, excellent ecosystem |
| **State Management** | Zustand | Lightweight, TypeScript-first, perfect for IPC sync |
| **Styling** | Tailwind CSS + CSS Variables | Utility-first with theming support |
| **Build Tool** | Vite + electron-vite | Fast builds, HMR, optimized for Electron |
| **Process Management** | Node.js child_process | Native, reliable, full control |
| **IPC** | Electron IPC + contextBridge | Secure, typed communication |
| **Packaging** | electron-builder | DMG/App bundle for macOS |

## 4.3 Directory Structure

```
cia-sie-mission-control/
├── package.json
├── electron.vite.config.ts
├── tsconfig.json
├── tsconfig.node.json
├── tsconfig.web.json
│
├── src/
│   ├── main/                          # Electron Main Process
│   │   ├── index.ts                   # Entry point
│   │   ├── orchestrator/
│   │   │   ├── ProcessOrchestrator.ts # Core orchestration logic
│   │   │   ├── ProcessManager.ts      # Individual process management
│   │   │   └── HealthMonitor.ts       # Health check coordination
│   │   ├── services/
│   │   │   ├── BackendService.ts      # Backend process handler
│   │   │   ├── FrontendService.ts     # Frontend process handler
│   │   │   ├── KiteService.ts         # Kite API health checker
│   │   │   └── ClaudeService.ts       # Claude API health checker
│   │   ├── config/
│   │   │   ├── ConfigManager.ts       # Configuration loader
│   │   │   └── default.config.ts      # Default configuration
│   │   ├── ipc/
│   │   │   ├── handlers.ts            # IPC message handlers
│   │   │   └── channels.ts            # Channel definitions
│   │   └── utils/
│   │       ├── CircuitBreaker.ts      # Resilience pattern
│   │       ├── RetryPolicy.ts         # Retry logic
│   │       └── Logger.ts              # Structured logging
│   │
│   ├── preload/                       # Electron Preload Scripts
│   │   ├── index.ts                   # Context bridge exposure
│   │   └── api.ts                     # Exposed API definitions
│   │
│   ├── renderer/                      # React Frontend
│   │   ├── index.html
│   │   ├── main.tsx                   # React entry point
│   │   ├── App.tsx                    # Root component
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── Dashboard.tsx      # Main dashboard container
│   │   │   │   ├── ServiceCard.tsx    # Individual service status
│   │   │   │   ├── MetricsPanel.tsx   # Metrics visualization
│   │   │   │   └── AlertBanner.tsx    # Alert notifications
│   │   │   ├── Controls/
│   │   │   │   ├── MasterControls.tsx # Start All / Stop All
│   │   │   │   ├── ServiceToggle.tsx  # Individual service control
│   │   │   │   └── EmergencyStop.tsx  # Emergency shutdown
│   │   │   ├── Logs/
│   │   │   │   ├── LogViewer.tsx      # Real-time log display
│   │   │   │   ├── LogEntry.tsx       # Individual log entry
│   │   │   │   └── LogFilters.tsx     # Log filtering controls
│   │   │   └── Settings/
│   │   │       ├── SettingsPanel.tsx  # Configuration UI
│   │   │       └── ServiceConfig.tsx  # Per-service settings
│   │   ├── hooks/
│   │   │   ├── useIPC.ts              # IPC communication hook
│   │   │   ├── useServices.ts         # Service state hook
│   │   │   └── useLogs.ts             # Log subscription hook
│   │   ├── store/
│   │   │   ├── index.ts               # Zustand store
│   │   │   ├── servicesSlice.ts       # Service state slice
│   │   │   └── logsSlice.ts           # Logs state slice
│   │   ├── styles/
│   │   │   ├── globals.css            # Global styles + CSS variables
│   │   │   └── components/            # Component-specific styles
│   │   └── types/
│   │       ├── services.ts            # Service type definitions
│   │       ├── ipc.ts                 # IPC message types
│   │       └── config.ts              # Configuration types
│   │
│   └── shared/                        # Shared between main/renderer
│       ├── constants.ts               # Shared constants
│       ├── types.ts                   # Shared type definitions
│       └── utils.ts                   # Shared utilities
│
├── resources/                         # Static resources
│   ├── icon.icns                      # macOS app icon
│   ├── icon.png                       # Generic icon
│   └── entitlements.mac.plist         # macOS entitlements
│
├── config/                            # Runtime configuration
│   ├── services.json                  # Service definitions
│   └── paths.json                     # Project paths
│
├── build/                             # Build configuration
│   ├── entitlements.mac.plist
│   └── notarize.js                    # macOS notarization script
│
└── dist/                              # Build output
    ├── main/
    ├── preload/
    └── renderer/
```

## 4.4 Service Configuration Schema

```typescript
// src/shared/types.ts

interface ServiceDefinition {
  id: string;                          // Unique identifier
  name: string;                        // Display name
  type: 'process' | 'health-check';    // Service type
  category: 'core' | 'api' | 'utility'; // Grouping category
  
  // For process-type services
  process?: {
    command: string;                   // Command to run
    args: string[];                    // Command arguments
    cwd: string;                       // Working directory
    env?: Record<string, string>;      // Environment variables
    readyPattern?: RegExp;             // Pattern indicating ready state
    readyTimeout: number;              // Max time to reach ready (ms)
  };
  
  // For health-check services
  healthCheck: {
    endpoint: string;                  // URL to check
    method: 'GET' | 'POST';           // HTTP method
    expectedStatus: number;            // Expected HTTP status
    interval: number;                  // Check interval (ms)
    timeout: number;                   // Request timeout (ms)
    retries: number;                   // Retries before failing
  };
  
  // Dependencies
  dependsOn?: string[];                // Services that must start first
  
  // Resilience
  circuitBreaker: {
    failureThreshold: number;          // Failures before opening
    resetTimeout: number;              // Time before half-open (ms)
  };
  
  // UI
  icon: string;                        // Lucide icon name
  color: string;                       // Status color theme
}
```

---

# 5. COMPONENT SPECIFICATIONS

## 5.1 Process Orchestrator

The **Process Orchestrator** is the brain of the MCC — it coordinates the startup sequence, manages dependencies, and handles the overall system lifecycle.

### 5.1.1 Responsibilities

| Responsibility | Description |
|----------------|-------------|
| Dependency Resolution | Determine correct startup order based on service dependencies |
| Parallel Execution | Start independent services concurrently for speed |
| State Coordination | Maintain consistent view of all service states |
| Event Distribution | Propagate state changes to renderer process |
| Graceful Shutdown | Orchestrate orderly termination in reverse dependency order |

### 5.1.2 Startup Sequence Algorithm

```typescript
// Pseudocode for startup sequence

async function startAll(services: ServiceDefinition[]): Promise<void> {
  // 1. Build dependency graph
  const graph = buildDependencyGraph(services);
  
  // 2. Topological sort to get startup order
  const startupOrder = topologicalSort(graph);
  
  // 3. Group by dependency level for parallel execution
  const levels = groupByLevel(startupOrder);
  
  // 4. Start each level in sequence, services within level in parallel
  for (const level of levels) {
    await Promise.all(
      level.map(service => startService(service))
    );
    
    // Verify all services in level are ready before proceeding
    await verifyAllReady(level);
  }
  
  // 5. All services started — begin health monitoring
  startHealthMonitoring();
}
```

### 5.1.3 Dependency Graph for CIA-SIE

```
                              ┌───────────────────┐
                              │      START        │
                              └─────────┬─────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │   BACKEND API     │  Level 0
                              │   (must start     │
                              │    first)         │
                              └─────────┬─────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │   KITE API      │ │  CLAUDE API     │ │   TRADINGVIEW   │  Level 1
          │   CONNECTOR     │ │   CONNECTOR     │ │    WEBHOOK      │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │    FRONTEND       │  Level 2
                              │    (depends on    │
                              │     backend)      │
                              └───────────────────┘
```

## 5.2 Health Monitor

### 5.2.1 Health Check Implementation

```typescript
// src/main/orchestrator/HealthMonitor.ts

interface HealthCheckResult {
  serviceId: string;
  status: 'healthy' | 'unhealthy' | 'degraded';
  latency: number;          // Response time in ms
  timestamp: Date;
  details?: {
    statusCode?: number;
    message?: string;
    metrics?: Record<string, number>;
  };
}

class HealthMonitor {
  private intervals: Map<string, NodeJS.Timeout> = new Map();
  private circuitBreakers: Map<string, CircuitBreaker> = new Map();
  
  startMonitoring(service: ServiceDefinition): void {
    const interval = setInterval(async () => {
      const result = await this.checkHealth(service);
      this.processResult(service.id, result);
    }, service.healthCheck.interval);
    
    this.intervals.set(service.id, interval);
  }
  
  private async checkHealth(service: ServiceDefinition): Promise<HealthCheckResult> {
    const circuitBreaker = this.circuitBreakers.get(service.id);
    
    if (circuitBreaker?.isOpen()) {
      return {
        serviceId: service.id,
        status: 'unhealthy',
        latency: 0,
        timestamp: new Date(),
        details: { message: 'Circuit breaker open' }
      };
    }
    
    const start = Date.now();
    
    try {
      const response = await fetch(service.healthCheck.endpoint, {
        method: service.healthCheck.method,
        signal: AbortSignal.timeout(service.healthCheck.timeout)
      });
      
      const latency = Date.now() - start;
      
      if (response.status === service.healthCheck.expectedStatus) {
        circuitBreaker?.recordSuccess();
        return {
          serviceId: service.id,
          status: latency > service.healthCheck.timeout * 0.8 ? 'degraded' : 'healthy',
          latency,
          timestamp: new Date(),
          details: { statusCode: response.status }
        };
      } else {
        circuitBreaker?.recordFailure();
        return {
          serviceId: service.id,
          status: 'unhealthy',
          latency,
          timestamp: new Date(),
          details: { statusCode: response.status }
        };
      }
    } catch (error) {
      circuitBreaker?.recordFailure();
      return {
        serviceId: service.id,
        status: 'unhealthy',
        latency: Date.now() - start,
        timestamp: new Date(),
        details: { message: error.message }
      };
    }
  }
}
```

### 5.2.2 Health Status Indicators

| Status | Color | Icon | Description |
|--------|-------|------|-------------|
| `idle` | Gray (#6b7280) | Circle | Not started |
| `starting` | Yellow (#eab308) | Loader (animated) | Starting up |
| `healthy` | Green (#10b981) | CheckCircle | Running normally |
| `degraded` | Orange (#f97316) | AlertTriangle | Running but slow/partial |
| `unhealthy` | Red (#ef4444) | XCircle | Failed or not responding |
| `stopping` | Yellow (#eab308) | Loader (animated) | Shutting down |
| `stopped` | Gray (#6b7280) | StopCircle | Stopped |

## 5.3 IPC Bridge

### 5.3.1 Channel Definitions

```typescript
// src/shared/constants.ts

export const IPC_CHANNELS = {
  // Commands (Renderer → Main)
  START_ALL: 'mcc:start-all',
  STOP_ALL: 'mcc:stop-all',
  START_SERVICE: 'mcc:start-service',
  STOP_SERVICE: 'mcc:stop-service',
  GET_CONFIG: 'mcc:get-config',
  UPDATE_CONFIG: 'mcc:update-config',
  
  // Events (Main → Renderer)
  STATUS_UPDATE: 'mcc:status-update',
  LOG_ENTRY: 'mcc:log-entry',
  ERROR: 'mcc:error',
  SYSTEM_EVENT: 'mcc:system-event',
  
  // Bidirectional
  SYNC_STATE: 'mcc:sync-state'
} as const;
```

### 5.3.2 Preload Script (Context Bridge)

```typescript
// src/preload/index.ts

import { contextBridge, ipcRenderer } from 'electron';
import { IPC_CHANNELS } from '../shared/constants';

const api = {
  // Commands
  startAll: () => ipcRenderer.invoke(IPC_CHANNELS.START_ALL),
  stopAll: (graceful: boolean = true) => 
    ipcRenderer.invoke(IPC_CHANNELS.STOP_ALL, { graceful }),
  startService: (serviceId: string) => 
    ipcRenderer.invoke(IPC_CHANNELS.START_SERVICE, { serviceId }),
  stopService: (serviceId: string) => 
    ipcRenderer.invoke(IPC_CHANNELS.STOP_SERVICE, { serviceId }),
  
  // Configuration
  getConfig: () => ipcRenderer.invoke(IPC_CHANNELS.GET_CONFIG),
  updateConfig: (config: Partial<Config>) => 
    ipcRenderer.invoke(IPC_CHANNELS.UPDATE_CONFIG, config),
  
  // Event Listeners
  onStatusUpdate: (callback: (status: ServiceStatus) => void) => {
    const handler = (_event: any, status: ServiceStatus) => callback(status);
    ipcRenderer.on(IPC_CHANNELS.STATUS_UPDATE, handler);
    return () => ipcRenderer.removeListener(IPC_CHANNELS.STATUS_UPDATE, handler);
  },
  
  onLogEntry: (callback: (log: LogEntry) => void) => {
    const handler = (_event: any, log: LogEntry) => callback(log);
    ipcRenderer.on(IPC_CHANNELS.LOG_ENTRY, handler);
    return () => ipcRenderer.removeListener(IPC_CHANNELS.LOG_ENTRY, handler);
  },
  
  onError: (callback: (error: MCCError) => void) => {
    const handler = (_event: any, error: MCCError) => callback(error);
    ipcRenderer.on(IPC_CHANNELS.ERROR, handler);
    return () => ipcRenderer.removeListener(IPC_CHANNELS.ERROR, handler);
  }
};

contextBridge.exposeInMainWorld('mcc', api);
```

---

# 6. USER INTERFACE DESIGN

## 6.1 Layout Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HEADER BAR                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ 🚀 CIA-SIE MISSION CONTROL          [Settings] [Minimize] [Close]   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────┐  ┌───────────────────────────────┐│
│  │         MASTER CONTROLS             │  │        SYSTEM STATUS          ││
│  │                                     │  │                               ││
│  │  ┌───────────────────────────────┐  │  │   Overall: ████████ READY    ││
│  │  │                               │  │  │   Uptime: 04:32:15           ││
│  │  │        [ LAUNCH ALL ]         │  │  │   Memory: 342 MB             ││
│  │  │                               │  │  │   CPU: 12%                   ││
│  │  └───────────────────────────────┘  │  │                               ││
│  │                                     │  └───────────────────────────────┘│
│  │  ┌─────────────┐ ┌─────────────┐   │                                    │
│  │  │ STOP ALL    │ │ EMERGENCY   │   │                                    │
│  │  │   (Soft)    │ │    STOP     │   │                                    │
│  │  └─────────────┘ └─────────────┘   │                                    │
│  │                                     │                                    │
│  └─────────────────────────────────────┘                                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                              SERVICE GRID                                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌────────────┐│
│  │   BACKEND API   │ │   FRONTEND      │ │   KITE API      │ │ CLAUDE AI  ││
│  │                 │ │                 │ │                 │ │            ││
│  │     ████████    │ │     ████████    │ │     ████████    │ │  ████████  ││
│  │     RUNNING     │ │     RUNNING     │ │     RUNNING     │ │  RUNNING   ││
│  │                 │ │                 │ │                 │ │            ││
│  │  Latency: 12ms  │ │  Build: OK      │ │  Quotes: Live   │ │  Ready     ││
│  │  [Start] [Stop] │ │  [Start] [Stop] │ │  [Start] [Stop] │ │ [St] [Sp]  ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ └────────────┘│
│                                                                             │
│  ┌─────────────────┐ ┌─────────────────┐                                    │
│  │  TRADINGVIEW    │ │   DATABASE      │                                    │
│  │    WEBHOOK      │ │  (PostgreSQL)   │                                    │
│  │     ████████    │ │     ████████    │                                    │
│  │     RUNNING     │ │     RUNNING     │                                    │
│  │                 │ │                 │                                    │
│  │  Last: 2s ago   │ │  Pool: 10/10    │                                    │
│  │  [Start] [Stop] │ │  [Start] [Stop] │                                    │
│  └─────────────────┘ └─────────────────┘                                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                              LOG VIEWER                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Filter: [All ▼] [Backend ▼] [Frontend ▼] [APIs ▼]    [Clear] [Export]│  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ 10:32:15.234 [BACKEND]  INFO   Server started on port 3001           │  │
│  │ 10:32:16.102 [KITE]     INFO   Connected to Kite WebSocket           │  │
│  │ 10:32:16.445 [FRONTEND] INFO   Vite server ready on port 5173        │  │
│  │ 10:32:17.001 [CLAUDE]   INFO   API health check passed               │  │
│  │ 10:32:18.234 [SYSTEM]   INFO   All services operational              │  │
│  │ █                                                                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Service Card Component

```
┌────────────────────────────────────────┐
│  ╭────────────────────────────────╮    │
│  │         SERVICE NAME           │    │
│  │         ◉ ◉ ◉ ◉ ◉             │    │  ← Status LEDs
│  │            ████                │    │  ← State indicator bar
│  ╰────────────────────────────────╯    │
│                                        │
│   Status:  ● RUNNING                   │  ← Primary state
│   Latency: 12ms ▲                      │  ← Key metric
│   Uptime:  04:32:15                    │  ← Secondary metric
│                                        │
│   ┌────────────┐  ┌────────────┐       │
│   │   START    │  │    STOP    │       │  ← Individual controls
│   └────────────┘  └────────────┘       │
│                                        │
│   Last event: Connected successfully   │  ← Recent activity
│   2 seconds ago                        │
│                                        │
└────────────────────────────────────────┘
```

## 6.3 State Transitions & Animations

### 6.3.1 Launch Sequence Animation

When "LAUNCH ALL" is pressed:

```
Frame 0:    All cards show IDLE (gray)
Frame 1-10: "LAUNCH ALL" button pulses, text changes to "LAUNCHING..."
Frame 11:   Backend card → STARTING (yellow, spinner)
Frame 12:   Backend progress bar animates
Frame 20:   Backend → RUNNING (green, checkmark appears)
Frame 21:   Kite, Claude, TradingView cards → STARTING (parallel)
Frame 30:   APIs → RUNNING
Frame 31:   Frontend → STARTING
Frame 40:   Frontend → RUNNING
Frame 41:   System status → "ALL SYSTEMS GO" (green banner)
Frame 50:   "LAUNCH ALL" → "RUNNING" (disabled, green)
```

### 6.3.2 Failure Animation

When a service fails:

```
Frame 0:    Service card flashes red
Frame 1-5:  Card border pulses red
Frame 6:    Status changes to UNHEALTHY
Frame 7:    Alert banner slides down from top
Frame 8:    Log entry appears in red
Frame 9:    Retry indicator appears (if auto-retry enabled)
```

## 6.4 CSS Variables & Theming

```css
/* src/renderer/styles/globals.css */

:root {
  /* Primary Palette */
  --color-background: #0a0f14;
  --color-surface: #111827;
  --color-surface-elevated: #1f2937;
  --color-border: #374151;
  
  /* Status Colors */
  --color-idle: #6b7280;
  --color-starting: #eab308;
  --color-running: #10b981;
  --color-degraded: #f97316;
  --color-error: #ef4444;
  --color-stopping: #eab308;
  
  /* Text */
  --color-text-primary: #f9fafb;
  --color-text-secondary: #9ca3af;
  --color-text-muted: #6b7280;
  
  /* Typography */
  --font-display: 'Space Grotesk', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Animation */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 400ms ease;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
  --shadow-glow-green: 0 0 20px rgba(16, 185, 129, 0.3);
  --shadow-glow-red: 0 0 20px rgba(239, 68, 68, 0.3);
}
```

---

# 7. STATE MANAGEMENT & DATA FLOW

## 7.1 Zustand Store Structure

```typescript
// src/renderer/store/index.ts

import { create } from 'zustand';

interface ServiceState {
  id: string;
  status: 'idle' | 'starting' | 'running' | 'degraded' | 'unhealthy' | 'stopping' | 'stopped';
  latency?: number;
  lastCheck?: Date;
  error?: string;
  metrics?: Record<string, number>;
}

interface LogEntry {
  id: string;
  timestamp: Date;
  serviceId: string;
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
}

interface MCCState {
  // Service States
  services: Record<string, ServiceState>;
  
  // Logs
  logs: LogEntry[];
  logFilters: {
    levels: ('debug' | 'info' | 'warn' | 'error')[];
    services: string[];
  };
  
  // System State
  systemStatus: 'idle' | 'launching' | 'running' | 'stopping' | 'error';
  lastError?: string;
  
  // Actions
  updateServiceStatus: (serviceId: string, status: Partial<ServiceState>) => void;
  addLog: (entry: Omit<LogEntry, 'id'>) => void;
  clearLogs: () => void;
  setLogFilter: (filters: Partial<MCCState['logFilters']>) => void;
  setSystemStatus: (status: MCCState['systemStatus']) => void;
  reset: () => void;
}

export const useMCCStore = create<MCCState>((set) => ({
  services: {},
  logs: [],
  logFilters: {
    levels: ['debug', 'info', 'warn', 'error'],
    services: []
  },
  systemStatus: 'idle',
  
  updateServiceStatus: (serviceId, status) =>
    set((state) => ({
      services: {
        ...state.services,
        [serviceId]: {
          ...state.services[serviceId],
          ...status
        }
      }
    })),
    
  addLog: (entry) =>
    set((state) => ({
      logs: [
        { ...entry, id: crypto.randomUUID() },
        ...state.logs.slice(0, 999) // Keep last 1000 entries
      ]
    })),
    
  clearLogs: () => set({ logs: [] }),
  
  setLogFilter: (filters) =>
    set((state) => ({
      logFilters: { ...state.logFilters, ...filters }
    })),
    
  setSystemStatus: (systemStatus) => set({ systemStatus }),
  
  reset: () => set({
    services: {},
    logs: [],
    systemStatus: 'idle',
    lastError: undefined
  })
}));
```

## 7.2 IPC Event Synchronization

```typescript
// src/renderer/hooks/useIPC.ts

import { useEffect } from 'react';
import { useMCCStore } from '../store';

export function useIPCSync() {
  const updateServiceStatus = useMCCStore((s) => s.updateServiceStatus);
  const addLog = useMCCStore((s) => s.addLog);
  const setSystemStatus = useMCCStore((s) => s.setSystemStatus);
  
  useEffect(() => {
    // Subscribe to status updates
    const unsubStatus = window.mcc.onStatusUpdate((status) => {
      updateServiceStatus(status.serviceId, {
        status: status.state,
        latency: status.latency,
        lastCheck: new Date(),
        metrics: status.metrics
      });
    });
    
    // Subscribe to log entries
    const unsubLogs = window.mcc.onLogEntry((log) => {
      addLog({
        timestamp: new Date(log.timestamp),
        serviceId: log.serviceId,
        level: log.level,
        message: log.message
      });
    });
    
    // Subscribe to errors
    const unsubErrors = window.mcc.onError((error) => {
      addLog({
        timestamp: new Date(),
        serviceId: error.serviceId || 'system',
        level: 'error',
        message: error.message
      });
      
      if (!error.recoverable) {
        setSystemStatus('error');
      }
    });
    
    // Cleanup
    return () => {
      unsubStatus();
      unsubLogs();
      unsubErrors();
    };
  }, [updateServiceStatus, addLog, setSystemStatus]);
}
```

---

# 8. ERROR HANDLING & RESILIENCE

## 8.1 Error Classification Matrix

| Error Code | Category | Severity | Auto-Recovery | User Action |
|------------|----------|----------|---------------|-------------|
| E001 | Process Spawn Failure | CRITICAL | No | Check path configuration |
| E002 | Process Crash | HIGH | Yes (3 retries) | Check logs |
| E003 | Health Check Timeout | MEDIUM | Yes (exponential backoff) | Wait or investigate |
| E004 | Network Unreachable | HIGH | Yes (retry with backoff) | Check network |
| E005 | Authentication Failure | CRITICAL | No | Update credentials |
| E006 | Port Already in Use | CRITICAL | No | Kill conflicting process |
| E007 | Dependency Timeout | HIGH | Yes (restart dependency) | Check dependency |
| E008 | Memory Exhaustion | CRITICAL | No | Increase memory limit |
| E009 | Disk Full | CRITICAL | No | Free disk space |
| E010 | Configuration Error | CRITICAL | No | Fix configuration |

## 8.2 Circuit Breaker Implementation

```typescript
// src/main/utils/CircuitBreaker.ts

type CircuitState = 'closed' | 'open' | 'half-open';

interface CircuitBreakerConfig {
  failureThreshold: number;
  resetTimeout: number;
  halfOpenRequests: number;
}

export class CircuitBreaker {
  private state: CircuitState = 'closed';
  private failures: number = 0;
  private lastFailure?: Date;
  private halfOpenSuccesses: number = 0;
  
  constructor(private config: CircuitBreakerConfig) {}
  
  isOpen(): boolean {
    if (this.state === 'open') {
      // Check if reset timeout has passed
      if (this.lastFailure && 
          Date.now() - this.lastFailure.getTime() > this.config.resetTimeout) {
        this.state = 'half-open';
        this.halfOpenSuccesses = 0;
        return false;
      }
      return true;
    }
    return false;
  }
  
  recordSuccess(): void {
    if (this.state === 'half-open') {
      this.halfOpenSuccesses++;
      if (this.halfOpenSuccesses >= this.config.halfOpenRequests) {
        this.state = 'closed';
        this.failures = 0;
      }
    } else {
      this.failures = 0;
    }
  }
  
  recordFailure(): void {
    this.failures++;
    this.lastFailure = new Date();
    
    if (this.failures >= this.config.failureThreshold) {
      this.state = 'open';
    }
  }
  
  getState(): CircuitState {
    return this.state;
  }
  
  reset(): void {
    this.state = 'closed';
    this.failures = 0;
    this.lastFailure = undefined;
  }
}
```

## 8.3 Graceful Degradation Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GRACEFUL DEGRADATION MATRIX                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   SCENARIO: Backend API fails                                               │
│   ─────────────────────────────                                             │
│   → Frontend: Display "Backend Offline" banner                              │
│   → Kite API: Continue monitoring (data cached)                             │
│   → Claude AI: Disabled (depends on backend)                                │
│   → TradingView: Queue incoming webhooks                                    │
│                                                                             │
│   SCENARIO: Kite API disconnects                                            │
│   ───────────────────────────────                                           │
│   → Frontend: Show stale data indicator                                     │
│   → Backend: Continue with cached quotes                                    │
│   → Analysis: Mark as "Delayed Data"                                        │
│                                                                             │
│   SCENARIO: Claude AI unavailable                                           │
│   ─────────────────────────────────                                         │
│   → Stage 1 Analysis: Continue normally                                     │
│   → Stage 2 Analysis: Queue for later processing                            │
│   → Frontend: Show "AI Analysis Pending"                                    │
│                                                                             │
│   SCENARIO: Frontend crashes                                                │
│   ──────────────────────────────                                            │
│   → Backend: Continue operation                                             │
│   → APIs: Continue operation                                                │
│   → MCC: Offer restart option                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 9. IMPLEMENTATION PHASES

## 9.1 Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IMPLEMENTATION ROADMAP                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PHASE 1: Foundation (Week 1)                                              │
│   ────────────────────────────                                              │
│   ├── Electron project scaffolding                                          │
│   ├── Main process architecture                                             │
│   ├── IPC bridge setup                                                      │
│   └── Basic renderer shell                                                  │
│                                                                             │
│   PHASE 2: Process Management (Week 2)                                      │
│   ────────────────────────────────────                                      │
│   ├── Process Orchestrator implementation                                   │
│   ├── Service definitions for CIA-SIE                                       │
│   ├── Dependency resolution                                                 │
│   └── Basic start/stop functionality                                        │
│                                                                             │
│   PHASE 3: Health Monitoring (Week 3)                                       │
│   ─────────────────────────────────                                         │
│   ├── Health Monitor implementation                                         │
│   ├── Circuit breaker integration                                           │
│   ├── Real-time status updates                                              │
│   └── Error classification system                                           │
│                                                                             │
│   PHASE 4: UI Implementation (Week 4)                                       │
│   ────────────────────────────────────                                      │
│   ├── Dashboard layout                                                      │
│   ├── Service cards                                                         │
│   ├── Master controls                                                       │
│   └── Log viewer                                                            │
│                                                                             │
│   PHASE 5: Polish & Integration (Week 5)                                    │
│   ───────────────────────────────────────                                   │
│   ├── Animations & transitions                                              │
│   ├── Settings panel                                                        │
│   ├── Audio cues                                                            │
│   └── CIA-SIE backend integration                                           │
│                                                                             │
│   PHASE 6: Testing & Hardening (Week 6)                                     │
│   ──────────────────────────────────────                                    │
│   ├── Unit tests                                                            │
│   ├── Integration tests                                                     │
│   ├── Failure scenario testing                                              │
│   └── Performance optimization                                              │
│                                                                             │
│   PHASE 7: Packaging & Deployment (Week 7)                                  │
│   ─────────────────────────────────────────                                 │
│   ├── electron-builder configuration                                        │
│   ├── macOS code signing                                                    │
│   ├── DMG creation                                                          │
│   └── Installation documentation                                            │
│                                                                             │
│   PHASE 8: Audit & Certification (Week 8)                                   │
│   ─────────────────────────────────────────                                 │
│   ├── Gold Standard audit                                                   │
│   ├── Security review                                                       │
│   ├── Performance benchmarks                                                │
│   └── Documentation finalization                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 9.2 Detailed Phase Deliverables

### Phase 1: Foundation

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| Electron app scaffolding | `npm run dev` launches empty window |
| Main process entry point | Structured with clear initialization |
| IPC channels defined | All channels from spec implemented |
| Preload script | Context bridge exposes API correctly |
| Renderer shell | React app mounts, Tailwind working |
| Build pipeline | `npm run build` produces working app |

### Phase 2: Process Management

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| ProcessOrchestrator class | Can manage multiple services |
| Service configuration schema | All CIA-SIE services defined |
| Dependency resolver | Topological sort working |
| Process spawning | Backend starts successfully |
| Process termination | Clean shutdown with exit code 0 |
| Stdout/stderr capture | Logs streamed to main process |

### Phase 3: Health Monitoring

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| HealthMonitor class | Polls all configured endpoints |
| CircuitBreaker | Opens after threshold, resets correctly |
| Retry logic | Exponential backoff working |
| Status events | Real-time updates to renderer |
| Error classification | All E-codes implemented |
| Auto-recovery | Transient failures self-heal |

### Phase 4: UI Implementation

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| Dashboard layout | Matches wireframe spec |
| ServiceCard component | Shows all states correctly |
| MasterControls | Start/Stop All functional |
| LogViewer | Real-time updates, filters work |
| State management | Zustand store syncs with IPC |
| Responsive design | Works at 1280x720 minimum |

### Phase 5: Polish & Integration

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| Animations | All state transitions animated |
| Settings panel | Configuration persists |
| Audio cues | Toggle on/off, sounds play |
| CIA-SIE integration | All services monitored |
| Error banners | Display correctly |
| Keyboard shortcuts | Start/Stop with hotkeys |

### Phase 6: Testing & Hardening

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| Unit tests | >80% coverage main process |
| Component tests | All UI components tested |
| Integration tests | Full launch sequence tested |
| Failure tests | All E-codes trigger correctly |
| Performance | <100ms UI response time |
| Memory | <200MB baseline usage |

### Phase 7: Packaging & Deployment

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| electron-builder config | Builds without errors |
| macOS signing | Passes Gatekeeper |
| DMG package | Drag-to-install works |
| Auto-update | (Optional) Update mechanism |
| Installation docs | Clear setup instructions |
| Uninstaller | Clean removal |

### Phase 8: Audit & Certification

| Deliverable | Acceptance Criteria |
|-------------|---------------------|
| Gold Standard audit | All checks pass |
| Security review | No vulnerabilities |
| Performance report | Meets all targets |
| User documentation | Complete and accurate |
| Developer documentation | Code fully documented |
| Certification sign-off | Ready for production |

---

# 10. TESTING & VALIDATION

## 10.1 Test Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TEST PYRAMID                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              ▲                                              │
│                             ╱ ╲                                             │
│                            ╱   ╲                                            │
│                           ╱ E2E ╲         10% - Full system tests           │
│                          ╱───────╲                                          │
│                         ╱         ╲                                         │
│                        ╱Integration╲       30% - IPC, services, UI          │
│                       ╱─────────────╲                                       │
│                      ╱               ╲                                      │
│                     ╱   Unit Tests    ╲    60% - Functions, classes         │
│                    ╱───────────────────╲                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 10.2 Test Scenarios

### 10.2.1 Happy Path Tests

| Test ID | Scenario | Expected Result |
|---------|----------|-----------------|
| HP-001 | Launch all services | All services reach RUNNING state |
| HP-002 | Stop all services | All services reach STOPPED state |
| HP-003 | Start individual service | Only target service starts |
| HP-004 | Stop individual service | Only target service stops |
| HP-005 | Health check passes | Service remains RUNNING |
| HP-006 | View logs | Logs display in real-time |
| HP-007 | Filter logs | Only matching logs shown |
| HP-008 | Export logs | File downloads correctly |

### 10.2.2 Failure Path Tests

| Test ID | Scenario | Expected Result |
|---------|----------|-----------------|
| FP-001 | Backend fails to start | Error displayed, no cascade |
| FP-002 | Health check fails | Service shows UNHEALTHY |
| FP-003 | Process crashes | Auto-restart triggered |
| FP-004 | Network timeout | Retry with backoff |
| FP-005 | Circuit breaker opens | Service marked FAILING |
| FP-006 | Circuit breaker recovers | Service returns to RUNNING |
| FP-007 | Emergency stop | All processes killed immediately |
| FP-008 | Cascading failure | Dependent services handle gracefully |

### 10.2.3 Edge Case Tests

| Test ID | Scenario | Expected Result |
|---------|----------|-----------------|
| EC-001 | Rapid start/stop | No race conditions |
| EC-002 | Double-click launch | Idempotent behavior |
| EC-003 | Stop during startup | Clean abort |
| EC-004 | Start already running | No-op, no error |
| EC-005 | Log overflow | Old logs purged |
| EC-006 | Long-running session | No memory leaks |

## 10.3 Performance Benchmarks

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Launch to all-green | < 30 seconds | Timestamp first click to last green |
| Shutdown time | < 10 seconds | Timestamp stop to all processes dead |
| UI response | < 100ms | Performance.now() on user interactions |
| Memory baseline | < 200MB | Process memory after idle 5 minutes |
| Memory under load | < 400MB | Memory with all services + heavy logging |
| CPU idle | < 5% | CPU usage with all services running, no activity |

---

# 11. AUDIT & COMPLIANCE

## 11.1 Alignment with CIA-SIE Governance

The MCC must comply with all existing CIA-SIE governance documents:

| Document | Compliance Requirement |
|----------|----------------------|
| CIA-SIE_CURSOR_ENGAGEMENT_ALIGNMENT_v3 | Full access framework, 7-phase audit checklist |
| CIA-SIE_GOLDEN_STATE_SPECIFICATION_v1 | Three Constitutional Rules, Five Immutable Laws |
| Universal_Code_Audit_Framework_v2 | 8 Gold Standard Principles, 9-Phase methodology |
| CIA-SIE_DOMAIN_TEST_TEMPLATES | Test coverage requirements |

## 11.2 Constitutional Rule Compliance

The MCC itself does not execute trades or make decisions, but it must ensure the systems it orchestrates comply:

| Rule | MCC Compliance |
|------|----------------|
| CR-001: Decision-Support ONLY | MCC displays system status, never recommends trading actions |
| CR-002: Expose NEVER Resolve | MCC shows all errors/warnings, does not hide problems |
| CR-003: Descriptive AI ONLY | N/A (MCC contains no AI analysis) |

## 11.3 Audit Checklist

```markdown
## MCC AUDIT CHECKLIST

### Architecture Compliance
- [ ] Electron main/renderer separation maintained
- [ ] IPC channels use contextBridge (no nodeIntegration)
- [ ] No hardcoded paths (all configurable)
- [ ] Environment variables properly handled

### Process Management
- [ ] All services defined in configuration
- [ ] Dependency graph accurate
- [ ] Startup sequence correct
- [ ] Shutdown sequence correct (reverse order)
- [ ] No zombie processes after shutdown

### Health Monitoring
- [ ] All endpoints polled at correct intervals
- [ ] Circuit breakers configured correctly
- [ ] Retry policies follow spec
- [ ] Status updates reach renderer within 2s

### UI/UX
- [ ] All states visually distinct
- [ ] Animations smooth (60fps)
- [ ] Logs update in real-time
- [ ] Controls responsive

### Error Handling
- [ ] All E-codes implemented
- [ ] Errors logged with context
- [ ] User-facing error messages clear
- [ ] Recovery actions documented

### Security
- [ ] No sensitive data in logs
- [ ] Configuration file permissions correct
- [ ] No eval() or dynamic code execution
- [ ] Dependencies audited (npm audit)

### Performance
- [ ] Launch time < 30s
- [ ] Memory < 200MB baseline
- [ ] CPU < 5% idle
- [ ] No memory leaks

### Documentation
- [ ] README complete
- [ ] API documentation current
- [ ] User guide written
- [ ] Troubleshooting guide included
```

---

# 12. DEPLOYMENT AS EXECUTABLE

## 12.1 electron-builder Configuration

```javascript
// electron-builder.config.js

module.exports = {
  appId: 'com.cia-sie.mission-control',
  productName: 'CIA-SIE Mission Control',
  
  directories: {
    output: 'release/${version}'
  },
  
  files: [
    'dist/**/*',
    'package.json'
  ],
  
  extraResources: [
    {
      from: 'config',
      to: 'config',
      filter: ['**/*']
    }
  ],
  
  mac: {
    category: 'public.app-category.developer-tools',
    icon: 'resources/icon.icns',
    target: [
      { target: 'dmg', arch: ['x64', 'arm64'] },
      { target: 'zip', arch: ['x64', 'arm64'] }
    ],
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: 'build/entitlements.mac.plist',
    entitlementsInherit: 'build/entitlements.mac.plist'
  },
  
  dmg: {
    contents: [
      { x: 130, y: 220 },
      { x: 410, y: 220, type: 'link', path: '/Applications' }
    ],
    window: {
      width: 540,
      height: 380
    }
  },
  
  afterSign: 'build/notarize.js'
};
```

## 12.2 macOS Entitlements

```xml
<!-- build/entitlements.mac.plist -->

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
</dict>
</plist>
```

## 12.3 Installation Structure

After installation, the app resides in:

```
/Applications/CIA-SIE Mission Control.app/
├── Contents/
│   ├── Info.plist
│   ├── MacOS/
│   │   └── CIA-SIE Mission Control    # Executable
│   ├── Resources/
│   │   ├── app.asar                    # Application bundle
│   │   ├── app.asar.unpacked/          # Native modules
│   │   └── config/                     # Configuration files
│   │       ├── services.json           # Service definitions
│   │       └── paths.json              # CIA-SIE project paths
│   └── Frameworks/
│       └── Electron Framework.framework/
```

## 12.4 First-Run Configuration

On first launch, the MCC will:

1. **Detect CIA-SIE installation** — Scan common paths for the project
2. **Prompt for paths** — If not found, ask user to locate project directories
3. **Generate configuration** — Create `paths.json` with discovered locations
4. **Validate services** — Verify all required components are present
5. **Ready state** — Display dashboard with all services in IDLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FIRST RUN CONFIGURATION                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Welcome to CIA-SIE Mission Control!                                       │
│                                                                             │
│   Please locate your CIA-SIE project directories:                           │
│                                                                             │
│   Backend Directory:                                                        │
│   ┌────────────────────────────────────────────────────┐                   │
│   │ /Users/neville/Projects/CIA-SIE/backend            │  [Browse]         │
│   └────────────────────────────────────────────────────┘                   │
│                                                                             │
│   Frontend Directory:                                                       │
│   ┌────────────────────────────────────────────────────┐                   │
│   │ /Users/neville/Projects/CIA-SIE/frontend           │  [Browse]         │
│   └────────────────────────────────────────────────────┘                   │
│                                                                             │
│   ┌─────────────────────────────────┐                                      │
│   │        [ Save & Continue ]       │                                      │
│   └─────────────────────────────────┘                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 13. OPERATIONAL PROCEDURES

## 13.1 Daily Operation

### 13.1.1 Starting the System

1. **Launch MCC** — Double-click app or use Spotlight
2. **Verify all IDLE** — All service cards should show gray IDLE state
3. **Click LAUNCH ALL** — Single button press
4. **Monitor startup** — Watch progress indicators
5. **Confirm ALL GREEN** — System status shows "ALL SYSTEMS GO"

### 13.1.2 Monitoring During Operation

1. **Dashboard** — Keep MCC visible or in dock
2. **Alerts** — Watch for yellow/red status changes
3. **Logs** — Check periodically for warnings
4. **Latency** — Monitor API response times

### 13.1.3 Stopping the System

1. **Click STOP ALL** — Graceful shutdown
2. **Wait for completion** — All cards should show STOPPED
3. **Verify** — Check logs for clean shutdown messages
4. **Close MCC** — Optional, can leave running

## 13.2 Troubleshooting Guide

### 13.2.1 Service Won't Start

| Symptom | Possible Cause | Resolution |
|---------|----------------|------------|
| Stuck on STARTING | Process hanging | Check logs, may need manual kill |
| Immediate UNHEALTHY | Port conflict | Check if port in use, kill conflicting process |
| UNHEALTHY after a few seconds | Health check failing | Verify service is actually running |
| Error in logs | Configuration issue | Check service configuration |

### 13.2.2 Frequent Health Check Failures

| Symptom | Possible Cause | Resolution |
|---------|----------------|------------|
| Intermittent failures | Network instability | Check network, increase timeout |
| Consistent failures | Service actually down | Check service logs |
| Circuit breaker opens | Cascading failures | Restart dependent services |

### 13.2.3 MCC Itself Issues

| Symptom | Possible Cause | Resolution |
|---------|----------------|------------|
| MCC won't launch | Corrupted installation | Reinstall from DMG |
| UI not updating | IPC disconnection | Restart MCC |
| High memory usage | Log accumulation | Clear logs, check for leaks |

## 13.3 Emergency Procedures

### 13.3.1 Emergency Stop

When: System behaving erratically, potential data corruption

Action:
1. Click **EMERGENCY STOP** button
2. All processes killed immediately (SIGKILL)
3. State may be inconsistent
4. Review logs before restarting

### 13.3.2 Manual Recovery

If MCC becomes unresponsive:

```bash
# Terminal commands for manual recovery

# 1. Find and kill all related processes
pkill -f "CIA-SIE"
pkill -f "node.*backend"
pkill -f "vite"

# 2. Verify no orphan processes
ps aux | grep -E "(CIA-SIE|backend|vite)"

# 3. Relaunch MCC
open "/Applications/CIA-SIE Mission Control.app"
```

---

# 14. APPENDICES

## Appendix A: Complete IPC API Reference

```typescript
// Complete API exposed via window.mcc

interface MCCAPI {
  // Service Control
  startAll(): Promise<{ success: boolean; errors?: string[] }>;
  stopAll(graceful?: boolean): Promise<{ success: boolean }>;
  startService(serviceId: string): Promise<{ success: boolean; error?: string }>;
  stopService(serviceId: string): Promise<{ success: boolean; error?: string }>;
  restartService(serviceId: string): Promise<{ success: boolean; error?: string }>;
  
  // Configuration
  getConfig(): Promise<MCCConfig>;
  updateConfig(config: Partial<MCCConfig>): Promise<{ success: boolean }>;
  getServiceConfig(serviceId: string): Promise<ServiceDefinition>;
  updateServiceConfig(serviceId: string, config: Partial<ServiceDefinition>): Promise<{ success: boolean }>;
  
  // Status
  getSystemStatus(): Promise<SystemStatus>;
  getServiceStatus(serviceId: string): Promise<ServiceStatus>;
  getAllServiceStatuses(): Promise<Record<string, ServiceStatus>>;
  
  // Logs
  getLogs(options: LogQueryOptions): Promise<LogEntry[]>;
  clearLogs(): Promise<void>;
  exportLogs(format: 'json' | 'csv'): Promise<string>; // Returns file path
  
  // Events
  onStatusUpdate(callback: (status: ServiceStatus) => void): () => void;
  onLogEntry(callback: (entry: LogEntry) => void): () => void;
  onError(callback: (error: MCCError) => void): () => void;
  onSystemEvent(callback: (event: SystemEvent) => void): () => void;
  
  // Utilities
  ping(): Promise<boolean>;
  getVersion(): Promise<string>;
  openDevTools(): void;
}
```

## Appendix B: Service Configuration for CIA-SIE

```json
{
  "services": [
    {
      "id": "backend",
      "name": "Backend API",
      "type": "process",
      "category": "core",
      "process": {
        "command": "npm",
        "args": ["start"],
        "cwd": "${BACKEND_PATH}",
        "env": {
          "NODE_ENV": "production",
          "PORT": "3001"
        },
        "readyPattern": "Server started on port",
        "readyTimeout": 30000
      },
      "healthCheck": {
        "endpoint": "http://localhost:3001/api/health",
        "method": "GET",
        "expectedStatus": 200,
        "interval": 5000,
        "timeout": 3000,
        "retries": 3
      },
      "dependsOn": [],
      "circuitBreaker": {
        "failureThreshold": 3,
        "resetTimeout": 30000
      },
      "icon": "Server",
      "color": "blue"
    },
    {
      "id": "frontend",
      "name": "Frontend",
      "type": "process",
      "category": "core",
      "process": {
        "command": "npm",
        "args": ["run", "dev"],
        "cwd": "${FRONTEND_PATH}",
        "env": {
          "VITE_API_URL": "http://localhost:3001"
        },
        "readyPattern": "Local:",
        "readyTimeout": 60000
      },
      "healthCheck": {
        "endpoint": "http://localhost:5173",
        "method": "GET",
        "expectedStatus": 200,
        "interval": 5000,
        "timeout": 3000,
        "retries": 3
      },
      "dependsOn": ["backend"],
      "circuitBreaker": {
        "failureThreshold": 3,
        "resetTimeout": 30000
      },
      "icon": "Layout",
      "color": "green"
    },
    {
      "id": "kite",
      "name": "Kite API",
      "type": "health-check",
      "category": "api",
      "healthCheck": {
        "endpoint": "http://localhost:3001/api/kite/status",
        "method": "GET",
        "expectedStatus": 200,
        "interval": 10000,
        "timeout": 5000,
        "retries": 3
      },
      "dependsOn": ["backend"],
      "circuitBreaker": {
        "failureThreshold": 5,
        "resetTimeout": 60000
      },
      "icon": "TrendingUp",
      "color": "orange"
    },
    {
      "id": "claude",
      "name": "Claude AI",
      "type": "health-check",
      "category": "api",
      "healthCheck": {
        "endpoint": "http://localhost:3001/api/claude/health",
        "method": "GET",
        "expectedStatus": 200,
        "interval": 30000,
        "timeout": 10000,
        "retries": 2
      },
      "dependsOn": ["backend"],
      "circuitBreaker": {
        "failureThreshold": 3,
        "resetTimeout": 120000
      },
      "icon": "Brain",
      "color": "purple"
    },
    {
      "id": "tradingview",
      "name": "TradingView Webhook",
      "type": "health-check",
      "category": "api",
      "healthCheck": {
        "endpoint": "http://localhost:3001/api/webhook/status",
        "method": "GET",
        "expectedStatus": 200,
        "interval": 10000,
        "timeout": 5000,
        "retries": 3
      },
      "dependsOn": ["backend"],
      "circuitBreaker": {
        "failureThreshold": 5,
        "resetTimeout": 60000
      },
      "icon": "Activity",
      "color": "cyan"
    }
  ]
}
```

## Appendix C: Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| ⌘ + L | Launch All |
| ⌘ + S | Stop All |
| ⌘ + ⇧ + S | Emergency Stop |
| ⌘ + K | Clear Logs |
| ⌘ + E | Export Logs |
| ⌘ + , | Open Settings |
| ⌘ + 1-5 | Focus Service Card 1-5 |
| Space | Toggle selected service |
| ⌘ + R | Restart selected service |

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| Circuit Breaker | Pattern that prevents cascading failures by "opening" after repeated failures |
| Health Check | Periodic verification that a service is operational |
| HITL | Human-in-the-Loop — requiring human approval at critical decision points |
| IPC | Inter-Process Communication — mechanism for Electron main/renderer to communicate |
| MCC | Mission Control Console — the application being specified |
| Process Orchestrator | Component that manages starting/stopping of all services |
| Topological Sort | Algorithm to determine correct startup order from dependency graph |

---

# DOCUMENT CERTIFICATION

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CIA-SIE MISSION CONTROL CONSOLE                                             ║
║   COMPLETE SYSTEM SPECIFICATION & IMPLEMENTATION BLUEPRINT                    ║
║                                                                               ║
║   Version: 1.0.0                                                              ║
║   Date: January 4, 2026                                                       ║
║   Status: SPECIFICATION COMPLETE — READY FOR IMPLEMENTATION                   ║
║                                                                               ║
║   This document constitutes the authoritative specification for the           ║
║   CIA-SIE Mission Control Console. All implementation work must conform       ║
║   to the architecture, interfaces, and behaviors defined herein.              ║
║                                                                               ║
║   Document Sections: 14                                                       ║
║   Appendices: 4                                                               ║
║   Total Scope: Comprehensive                                                  ║
║                                                                               ║
║   Governance Alignment:                                                       ║
║   ✓ CIA-SIE_CURSOR_ENGAGEMENT_ALIGNMENT_v3                                   ║
║   ✓ CIA-SIE_GOLDEN_STATE_SPECIFICATION_v1                                    ║
║   ✓ Universal_Code_Audit_Framework_v2                                        ║
║                                                                               ║
║   Next Steps:                                                                 ║
║   1. Review specification with stakeholder                                    ║
║   2. Create HITL Protocol for Cursor implementation                           ║
║   3. Begin Phase 1: Foundation                                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

*End of CIA-SIE Mission Control Console Specification v1.0*
