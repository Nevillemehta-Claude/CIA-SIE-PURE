# CIA-SIE COMPLETE REBUILD - AI IMPLEMENTATION PACKAGE

**Date:** 02 January 2026
**Version:** 3.0.0 (aligned with current implementation + test coverage)
**Purpose:** Complete backend + frontend rebuild with Claude AI integration
**Prepared by:** Claude (Anthropic)
**Governance:** Gold Standard Specification v2.0.0

---

## MASTER GOVERNANCE DOCUMENT

**CRITICAL: Read this first before any implementation:**
```
specifications/architecture/00_GOLD_STANDARD_SPECIFICATION.md
```

This Gold Standard Specification contains:
- Three Constitutional Rules (INVIOLABLE)
- Five Immutable Laws of Development
- Six Architecture Principles
- Complete Claude AI Integration Specs
- All Quality, Security, and Testing Standards
- Stage-Gate Governance Process
- Anti-Patterns to Avoid

---

## PACKAGE CONTENTS

| Document | Purpose |
|----------|---------|
| **GOLD STANDARD SPECIFICATION** | Master governance document (in Gold Audit Standards/) |
| `HANDOFF_01_DESIGN_SPECIFICATION.md` | Visual design requirements from HTML mockup |
| `HANDOFF_02_API_ENDPOINTS.md` | Complete API documentation including Claude AI endpoints |
| `HANDOFF_03_CONSTITUTIONAL_RULES.md` | Inviolable rules the application MUST follow |
| `HANDOFF_04_TECHNICAL_STANDARDS.md` | Engineering standards, laws, principles, gates |
| `HANDOFF_05_COMPONENT_REQUIREMENTS.md` | Detailed component specifications including AI components |
| `HANDOFF_06_CSS_DESIGN_SYSTEM.md` | Extracted CSS variables and styling |
| `HANDOFF_07_BUSINESS_LOGIC.md` | Core algorithms (freshness, contradictions, signals) |
| `HANDOFF_08_IMPLEMENTATION_STATUS.md` | **NEW** Gap analysis: what exists vs. what must be built |

---

## CRITICAL CONTEXT

### What Happened
The original React frontend in `frontend/src/components/` was a basic implementation that does NOT match the designed GUI in `CIA-SIE_INTERACTIVE_USER_MANUAL.html`. Additionally, the backend requires new Claude AI integration endpoints.

### What Was Purged
All React components in `frontend/src/components/` have been deleted. The following are preserved:
- `frontend/src/services/api.ts` - Working API connection layer
- `frontend/src/types/index.ts` - TypeScript type definitions
- `frontend/package.json` - Dependencies (React, Vite, TailwindCSS)
- `frontend/vite.config.ts` - Build configuration (port 3000)

### What Must Be Built

**BACKEND (New Claude AI Integration):**
1. New API routes for Claude AI (`/api/v1/ai/*`, `/api/v1/chat/*`, `/api/v1/strategy/*`)
2. Dynamic model selection service (Haiku/Sonnet/Opus)
3. Token counting and cost tracking
4. Budget management and alerts
5. Conversation history persistence
6. AI response validation (safety checks)

**FRONTEND (Complete Rebuild):**
1. Matches the visual design in `CIA-SIE_INTERACTIVE_USER_MANUAL.html`
2. Connects to the existing + new backend API (documented in HANDOFF_02)
3. Follows ALL constitutional rules (documented in HANDOFF_03)
4. Meets technical standards (documented in HANDOFF_04)
5. Implements all components including AI components (documented in HANDOFF_05)
6. Implements business logic algorithms (documented in HANDOFF_07)

---

## DESIGN REFERENCE FILE

**PRIMARY DESIGN SOURCE:**
```
/Users/nevillemehta/Downloads/CIA-SIE/CIA-SIE_INTERACTIVE_USER_MANUAL.html
```

Open this file in a browser to see EXACTLY how the interface should look. This 1,890-line HTML file contains:
- Complete visual design
- Color scheme and CSS variables
- Component layouts
- Responsive breakpoints
- Interactive behaviors (accordions, tabs, navigation)

---

## QUICK START

### Phase 1: Understanding (Do First)
1. Read **Gold Standard Specification** in Gold Audit Standards/ (master governance)
2. Read `HANDOFF_03_CONSTITUTIONAL_RULES.md` (non-negotiable rules)
3. Read `HANDOFF_04_TECHNICAL_STANDARDS.md` (laws, principles, standards)

### Phase 2: Backend Implementation
1. Review `HANDOFF_02_API_ENDPOINTS.md` Section 11-13 (Claude AI endpoints)
2. Review `HANDOFF_07_BUSINESS_LOGIC.md` (algorithms)
3. Implement new AI routes, services, and models
4. Implement AI response validation

### Phase 3: Frontend Implementation
1. Open `CIA-SIE_INTERACTIVE_USER_MANUAL.html` in browser as visual reference
2. Implement components per `HANDOFF_05_COMPONENT_REQUIREMENTS.md`
3. Use CSS from `HANDOFF_06_CSS_DESIGN_SYSTEM.md`
4. Implement AI components (ModelSelector, ChatPanel, etc.)

### Phase 4: Verification
1. Run through all stage gates (HANDOFF_04 Section 10)
2. Complete verification checklist below
3. Ensure all tests pass with >90% coverage

---

## VERIFICATION CHECKLIST

### Constitutional Compliance
- [ ] NO buy/sell recommendations anywhere in UI or API
- [ ] NO scoring or weighting of signals
- [ ] NO confidence percentages
- [ ] Contradictions are displayed, NEVER resolved
- [ ] All AI narratives end with mandatory disclaimer
- [ ] AI responses validated for prohibited patterns

### Backend Verification
- [ ] All core API endpoints working (instruments, silos, charts, signals)
- [ ] All Claude AI endpoints working (/ai/models, /ai/usage, /chat, /strategy)
- [ ] Dynamic model selection functioning
- [ ] Token counting and cost tracking working
- [ ] Budget alerts triggering at 80%, 90%, 100%
- [ ] AI response validation rejecting unsafe content
- [ ] Conversation history persisting

### Frontend Verification
- [ ] Visual appearance matches `CIA-SIE_INTERACTIVE_USER_MANUAL.html`
- [ ] All API endpoints connect correctly
- [ ] Responsive design works at 900px breakpoint
- [ ] All freshness indicators display correctly
- [ ] Signal directions (BULLISH/BEARISH/NEUTRAL) show correctly
- [ ] Model selector functioning (Haiku/Sonnet/Opus)
- [ ] Chat panel working with disclaimer display
- [ ] Budget alerts displaying appropriately
- [ ] Keyboard navigation working (WCAG 2.1 AA)

### Quality Verification
- [ ] Unit test coverage > 90%
- [ ] Integration test coverage > 80%
- [ ] No TypeScript `any` types
- [ ] Cyclomatic complexity < 10
- [ ] No anti-patterns present
- [ ] All 5 stage gates passed

---

## SUPPORT FILES

The backend is fully functional. Test it:
```bash
# Start the platform
source .venv/bin/activate
cd src && uvicorn cia_sie.main:app --reload --port 8000

# API documentation
open http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```
