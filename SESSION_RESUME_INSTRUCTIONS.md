# SESSION RESUME INSTRUCTIONS
**Date:** 2026-01-03
**Session:** Frontend Development Initiation

---

## CURRENT STATE

### Completed
- Backend code complete and audited (9-phase audit CERTIFIED)
- `governance/FRONTEND_TECH_SPEC.md` generated (4,190 lines)
- `governance/V0_COMPONENT_PROMPTS.md` created (29 component prompts)
- Both files committed to GitHub (commit e228872)

### In Progress
- **Step 1 of 47:** Create frontend project scaffold
- User is about to paste Cursor prompt in fresh Agent window

---

## 47-STEP ROADMAP TO FUNCTIONING APPLICATION

### PHASE A: Frontend Code Generation (Steps 1-11) - PRIMARY TOOL: Cursor
| Step | Task | Status |
|------|------|--------|
| 1 | Create frontend project scaffold | **NEXT** |
| 2 | Generate TypeScript types/interfaces | Pending |
| 3 | Generate atomic components | Pending |
| 4 | Generate layout components | Pending |
| 5 | Generate page components | Pending |
| 6 | Generate composite components | Pending |
| 7 | Generate API service layer | Pending |
| 8 | Generate state management (React Query) | Pending |
| 9 | Generate routing configuration | Pending |
| 10 | Generate CSS/Tailwind styling | Pending |
| 11 | Commit frontend code | Pending |

### PHASE B: Frontend Testing (Steps 12-16) - Cursor + Claude Code
| Step | Task | Status |
|------|------|--------|
| 12 | Generate unit tests for components | Pending |
| 13 | Generate constitutional compliance tests | Pending |
| 14 | Run frontend test suite | Pending |
| 15 | Fix any failing tests | Pending |
| 16 | Commit test code | Pending |

### PHASE C: Frontend Audit (Steps 17-20) - Cursor
| Step | Task | Status |
|------|------|--------|
| 17 | Phase 3: Frontend Code Audit | Pending |
| 18 | Constitutional compliance verification | Pending |
| 19 | Update Phase 9E certification | Pending |
| 20 | Commit audit deliverables | Pending |

### PHASE D: Integration (Steps 21-26) - Claude Code + Cursor
| Step | Task | Status |
|------|------|--------|
| 21 | Configure frontend API base URL | Pending |
| 22 | Verify CORS configuration in backend | Pending |
| 23 | Create integration test suite | Pending |
| 24 | Run integration tests | Pending |
| 25 | Fix any integration issues | Pending |
| 26 | Commit integration fixes | Pending |

### PHASE E: CI/CD Pipeline (Steps 27-31) - Cursor + GitHub
| Step | Task | Status |
|------|------|--------|
| 27 | Add frontend build job to CI | Pending |
| 28 | Add frontend test job to CI | Pending |
| 29 | Add frontend constitutional test job | Pending |
| 30 | Verify CI pipeline passes | Pending |
| 31 | Commit CI updates | Pending |

### PHASE F: Local Environment (Steps 32-39) - Claude Code
| Step | Task | Status |
|------|------|--------|
| 32 | Create backend startup script | Pending |
| 33 | Create frontend startup script | Pending |
| 34 | Create combined dev script | Pending |
| 35 | Initialize database with migrations | Pending |
| 36 | Seed database with test data | Pending |
| 37 | Start backend server | Pending |
| 38 | Start frontend dev server | Pending |
| 39 | Verify application loads in browser | Pending |

### PHASE G: End-to-End Verification (Steps 40-47) - Claude Code
| Step | Task | Status |
|------|------|--------|
| 40 | Test signal ingestion flow | Pending |
| 41 | Test confirmation detection | Pending |
| 42 | Test contradiction detection | Pending |
| 43 | Test AI narrative generation | Pending |
| 44 | Test freshness indicators | Pending |
| 45 | Verify no prohibited UI elements | Pending |
| 46 | Document verification results | Pending |
| 47 | Commit verification document | Pending |

---

## CURSOR PROMPT FOR STEP 1 (Ready to Paste)

```
Read ALL documents in these directories:
- governance/
- handoff/

TASK: Create the frontend project scaffold

LOCKED TECH STACK (do not deviate):
- React 18.2
- TypeScript 5.3
- Vite 5.0
- Tailwind CSS 3.4
- React Query 5.17
- React Router 6.21
- Axios 1.6
- Lucide React 0.303
- Vitest 1.1

REQUIREMENTS:

1. Create a new `frontend/` directory at project root

2. Initialize Vite project with React + TypeScript template

3. Install exact dependencies:
   npm install react@18.2 react-dom@18.2
   npm install @tanstack/react-query@5.17
   npm install react-router-dom@6.21
   npm install axios@1.6
   npm install lucide-react@0.303
   npm install -D tailwindcss@3.4 postcss autoprefixer
   npm install -D vitest @testing-library/react @testing-library/jest-dom

4. Create folder structure:
   frontend/
   ├── src/
   │   ├── components/
   │   │   ├── atoms/
   │   │   ├── layout/
   │   │   └── composite/
   │   ├── pages/
   │   ├── hooks/
   │   ├── services/
   │   │   └── api/
   │   ├── types/
   │   ├── utils/
   │   ├── styles/
   │   ├── router/
   │   ├── App.tsx
   │   └── main.tsx
   ├── tests/
   │   ├── unit/
   │   └── constitutional/
   ├── public/
   ├── index.html
   ├── vite.config.ts
   ├── tailwind.config.js
   ├── postcss.config.js
   ├── tsconfig.json
   └── package.json

5. Configure Tailwind with CIA-SIE design tokens from FRONTEND_TECH_SPEC.md Section 16

6. Create placeholder index files in each directory

7. Configure Vite for development (proxy to backend localhost:8000)

8. Configure Vitest for testing

OUTPUT: Working scaffold that runs with `npm run dev`
```

---

## TOOL RESPONSIBILITIES

| Tool | Role |
|------|------|
| **Claude Code** | Orchestrator, prompt creation, verification, commits, running tests |
| **Cursor** | Code generation (frontend scaffold, components, tests) |
| **GitHub** | Version control, CI/CD |

---

## KEY FILES

| File | Purpose |
|------|---------|
| `governance/FRONTEND_TECH_SPEC.md` | Complete frontend specification (4,190 lines) |
| `governance/V0_COMPONENT_PROMPTS.md` | Component prompts (not using v0.dev per user) |
| `governance/CIA-SIE_AUDIT_CONFIGURATION.md` | Project audit configuration |
| `handoff/BACKEND_ARCHITECTURAL_FLOWCHART.md` | Backend architecture reference |

---

## TO RESUME THIS SESSION

1. Open Claude Code in `/Users/nevillemehta/Downloads/CIA-SIE-PURE`
2. Say: "Continue from SESSION_RESUME_INSTRUCTIONS.md - Step 1 frontend scaffold"
3. If Cursor completed Step 1, say: "Cursor completed Step 1, verify and proceed to Step 2"

---

**END OF SESSION SAVE**
