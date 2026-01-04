# CIA-SIE MISSION CONTROL CONSOLE
## Cursor Implementation Handoff Protocol v1.1.0

**Document Type:** Implementation Handoff
**Parent Specification:** MCC_GENESIS_BUILD_SPECIFICATION.md
**Target Agent:** Cursor AI
**Handoff Date:** 2026-01-04
**Protocol Version:** 1.1.0 (Creative Latitude Revision)

---

## QUICK START FOR CURSOR

Copy everything below the line and paste into Cursor as your implementation prompt.

---

## CURSOR PROMPT START

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│        CIA-SIE MISSION CONTROL CONSOLE - CURSOR IMPLEMENTATION              │
│                                                                              │
│                    ⚡ CREATIVE LATITUDE PROTOCOL ⚡                          │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CRITICAL: READ THIS ENTIRE SECTION BEFORE PROCEEDING                       │
│                                                                              │
│  This handoff protocol operates under the CREATIVE LATITUDE DIRECTIVE.      │
│  You have FULL AUTHORITY to exercise your own expertise and judgment        │
│  in implementing this application.                                           │
│                                                                              │
│  The specifications provided are DIRECTIONAL GUIDANCE ONLY.                  │
│  You are NOT required to follow them exactly.                                │
│  You MAY propose superior alternatives.                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

## STEP 0: UNDERSTAND YOUR AUTHORITY

You are implementing the CIA-SIE Mission Control Console (MCC), an Electron-based desktop application that serves as the unified command center for the CIA-SIE ecosystem.

### What You MUST Do (INVIOLABLE)

1. **Produce an Implementation Plan FIRST** - Before writing ANY code
2. **Obtain User Approval** - Present your plan and await explicit approval
3. **Respect Constitutional Rules** - These cannot be violated
4. **Avoid Forbidden Dependencies** - These cannot be added

### What You MAY Do (YOUR DISCRETION)

1. **Replace ANY specified technology** with a more modern or performant alternative
2. **Redesign the architecture** if you determine a better approach
3. **Restructure the directory layout** according to your best practices
4. **Modify component designs** as you see fit
5. **Add ANY dependencies** that don't violate constitutional rules
6. **Enhance visual designs** beyond the mockups provided
7. **Propose entirely different solutions** if you believe they're superior

## STEP 1: CREATE YOUR IMPLEMENTATION PLAN (MANDATORY)

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   BEFORE WRITING ANY CODE, YOU MUST CREATE A DOCUMENT CALLED:               │
│                                                                              │
│   CURSOR_IMPLEMENTATION_PLAN.md                                             │
│                                                                              │
│   This is NOT optional. Implementation cannot proceed without it.           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

Your Implementation Plan MUST contain these sections:

### Section A: Executive Divergence Summary

List ALL areas where your approach differs from the reference specifications:

```markdown
## Executive Divergence Summary

| Area | Reference Spec | My Approach | Rationale |
|------|----------------|-------------|-----------|
| Framework | Electron 29.x | [Your choice] | [Why] |
| UI Library | React 18.x | [Your choice] | [Why] |
| State Mgmt | Zustand | [Your choice] | [Why] |
| Styling | Tailwind CSS | [Your choice] | [Why] |
| ... | ... | ... | ... |
```

### Section B: Technology Stack Declaration

For each technology decision:
- What the reference specification suggested
- What you will actually use
- Why your choice is appropriate
- Any impacts on other components

### Section C: Architecture Decisions

- Your proposed architecture (with diagrams if helpful)
- How it achieves the project goals
- Key differences from reference architecture
- Benefits of your approach

### Section D: Phase-by-Phase Implementation Plan

For each development phase:
- Phase name and goals
- Specific deliverables you will produce
- Dependencies and prerequisites
- Any risks or challenges

### Section E: GUI/UX Approach

- How you interpret the visual requirements
- Design system or component library you'll use
- Accessibility strategy
- Responsive/window sizing approach

### Section F: Risk Assessment

- Potential challenges with your chosen approach
- Mitigation strategies
- Fallback options if needed

## STEP 2: PRESENT PLAN AND AWAIT APPROVAL (MANDATORY)

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   After creating your Implementation Plan, STOP and present it to the       │
│   user (Neville). DO NOT write any implementation code until you            │
│   receive explicit approval.                                                 │
│                                                                              │
│   Say something like:                                                        │
│   "I've created my Implementation Plan. Please review it in                  │
│   CURSOR_IMPLEMENTATION_PLAN.md and let me know if you approve              │
│   or if you'd like me to adjust anything before I begin coding."            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

## STEP 3: IMPLEMENT YOUR APPROVED PLAN

Once approved, execute YOUR plan (not the reference specifications).

Continue to:
- Flag any additional deviations discovered during development
- Seek clarification when requirements are ambiguous
- Propose alternatives when encountering obstacles

---

## CONSTITUTIONAL RULES (INVIOLABLE - CANNOT BE MODIFIED)

These rules are ABSOLUTE. No exceptions. No workarounds.

### CR-001: DECISION-SUPPORT ONLY
- NO buttons labeled "Buy", "Sell", "Trade", "Execute"
- NO text containing "should", "recommend", "suggest", "consider"
- ONLY process control buttons: Start, Stop, Restart, View

### CR-002: EXPOSE NEVER RESOLVE
- Display contradictions side-by-side with EQUAL sizing
- NO aggregation, weighting, or "net" calculations
- NO visual hierarchy suggesting one side is "correct"

### CR-003: DESCRIPTIVE AI ONLY
- Disclaimer MUST appear on ALL AI-generated content
- Disclaimer is NOT dismissible or hideable

### MCR-001: NO AUTO-TRADE INTEGRATION
- MCC controls processes, NEVER executes trades

### MCR-002: NO EXTERNAL NETWORK CALLS
- MCC only communicates with local services
- No cloud APIs, no external services

### MCR-003: GRACEFUL DEGRADATION
- MCC remains functional if child processes fail

### MCR-004: EXPLICIT USER ACTIONS
- ALL process controls require user click
- NO automatic actions without user initiation

### MCR-005: AUDIT TRAIL LOGGING
- All user actions logged with timestamps

---

## FORBIDDEN DEPENDENCIES (INVIOLABLE - CANNOT BE ADDED)

These dependencies violate constitutional principles:

- Telemetry/analytics services (violates user privacy)
- Cloud APIs or external services (violates MCR-002)
- Auto-update services (violates user control)
- Trade execution APIs (violates CR-001)
- Any service that transmits data externally

**ALL OTHER DEPENDENCIES ARE PERMITTED** at your discretion.

---

## REFERENCE SPECIFICATIONS (DIRECTIONAL ONLY)

The following are provided as REFERENCE MATERIAL to inform your understanding.
You are NOT required to follow them. They represent ONE possible implementation.

### Reference Documents

| Document | Purpose | Your Authority |
|----------|---------|----------------|
| MCC_GENESIS_BUILD_SPECIFICATION.md | Reference architecture | May modify entirely |
| MCC_GUI_MOCKUP_REQUIREMENTS.md | Reference visual design | May redesign |
| MCC_HITL_APPROVAL_GATES.md | Approval checkpoints | Must respect gates |

### Reference Technology Stack (You May Replace Any/All)

```
Reference Stack (Directional Only):
├── electron: ^29.0.0          → You may use Tauri, NW.js, or other frameworks
├── react: ^18.2.0             → You may use Vue, Svelte, Solid, or vanilla JS
├── zustand: ^4.5.0            → You may use Redux, Jotai, Valtio, or other
├── tailwindcss: ^3.4.0        → You may use CSS-in-JS, SCSS, vanilla CSS, etc.
├── lucide-react: ^0.344.0     → You may use any icon library
├── electron-vite: ^2.0.0      → You may use any build tooling
└── typescript: ^5.3.3         → Recommended but not mandatory
```

### Reference Architecture

The MCC should provide these capabilities (implement as you see fit):

1. **Process Orchestration** - Start/stop/monitor CIA-SIE backend and frontend
2. **Health Monitoring** - Track service health status
3. **Log Aggregation** - View consolidated logs from all services
4. **WebView Embedding** - Display frontend and API docs within MCC
5. **Configuration Management** - Persist user settings
6. **System Tray** - Background operation capability

### Reference Implementation Phases

These phases are SUGGESTED. You may reorganize or combine them:

1. Project Scaffolding - Initialize your chosen framework/tooling
2. Main Process Core - Process management infrastructure
3. Process Orchestration - Child process spawning and monitoring
4. State Management - Application state infrastructure
5. Layout Components - Shell, navigation, title bar
6. Dashboard Components - Status displays and quick actions
7. Process/Log Components - Process cards, log viewer
8. Pages & Integration - Assemble into complete pages

---

## REFERENCE CODE EXAMPLES (DIRECTIONAL ONLY)

The following code examples are provided for CONTEXT ONLY.
You should write your own implementations based on your chosen stack.

### Example: IPC Channel Structure (if using Electron)

```typescript
// This is a REFERENCE. Design your own channel structure.
export const IPC_CHANNELS = {
  PROCESS_START: 'process:start',
  PROCESS_STOP: 'process:stop',
  PROCESS_RESTART: 'process:restart',
  PROCESS_STATUS: 'process:status',
  HEALTH_CHECK: 'health:check',
  HEALTH_UPDATE: 'health:update',
  LOG_STREAM: 'log:stream',
  CONFIG_GET: 'config:get',
  CONFIG_SET: 'config:set',
  WINDOW_MINIMIZE: 'window:minimize',
  WINDOW_MAXIMIZE: 'window:maximize',
  WINDOW_CLOSE: 'window:close',
} as const;
```

### Example: Process State Type (reference only)

```typescript
// This is a REFERENCE. Design your own type system.
export type ProcessStatus =
  | 'stopped'
  | 'starting'
  | 'running'
  | 'stopping'
  | 'crashed'
  | 'restarting';

export interface ProcessState {
  name: string;
  status: ProcessStatus;
  pid: number | null;
  startTime: number | null;
  restartCount: number;
  lastError: string | null;
}
```

### Example: Visual Theme (reference only)

```javascript
// This is a REFERENCE. Design your own visual system.
colors: {
  mcc: {
    bg: '#0a0a0f',       // Dark background
    panel: '#12121a',    // Panel background
    border: '#1e1e2e',   // Borders
    accent: '#3b82f6',   // Primary accent
    success: '#22c55e',  // Running/healthy
    warning: '#f59e0b',  // Starting/degraded
    error: '#ef4444',    // Crashed/unhealthy
  }
}
```

---

## HITL APPROVAL GATES

You must pause for user approval at these checkpoints:

### Gate 0: Implementation Plan (NEW - MANDATORY)
- Present your CURSOR_IMPLEMENTATION_PLAN.md
- Await explicit approval before ANY coding

### Gate 1: Core Infrastructure
- Demonstrate running application shell
- Show process management working

### Gate 2: UI Components
- Show complete UI layout
- Demonstrate component functionality

### Gate 3: Full Integration
- Full functional demonstration
- Run tests
- Constitutional compliance audit

---

## COMMUNICATION DURING IMPLEMENTATION

As you work:
- **Flag deviations** - If you discover additional changes needed
- **Propose alternatives** - When you encounter obstacles
- **Ask questions** - When requirements are ambiguous
- **Show progress** - At natural checkpoints

---

## SUMMARY: YOUR WORKFLOW

1. READ this prompt and the reference specifications
2. DECIDE your implementation approach (may differ from references)
3. CREATE your CURSOR_IMPLEMENTATION_PLAN.md document
4. PRESENT your plan to the user
5. AWAIT explicit approval
6. IMPLEMENT your approved plan
7. PAUSE at HITL gates for approval
8. COMPLETE and demonstrate

Remember: The reference specifications provide CONTEXT and DIRECTION.
YOU provide the IMPLEMENTATION EXPERTISE.
```

## CURSOR PROMPT END

---

## HOW TO USE THIS DOCUMENT

1. Open Cursor
2. Open the CIA-SIE-PURE project folder
3. Open a new chat with Cursor
4. Copy everything between "CURSOR PROMPT START" and "CURSOR PROMPT END"
5. Paste it into Cursor
6. Press Enter

Cursor will:
1. Create an Implementation Plan with its proposed approach
2. Present the plan for your review
3. Await your approval before writing any code
4. Implement according to its approved plan

This ensures you (Neville) are fully informed of Cursor's intended approach before any development investment.

---

## DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-04 | Claude Code | Initial handoff protocol |
| 1.1.0 | 2026-01-04 | Claude Code | **MAJOR REVISION**: Complete rewrite under Creative Latitude Directive. Changed from prescriptive "copy exactly" approach to directional guidance. Added mandatory Implementation Plan requirement. All code examples now clearly marked as reference only. Cursor granted full creative authority within constitutional bounds. |

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
