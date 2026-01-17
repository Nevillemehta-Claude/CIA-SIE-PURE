# CIA-SIE Documentation Index

> **Last Updated:** 2026-01-04
> **Purpose:** Central navigation hub for all project documentation

---

## Quick Navigation

### Architecture Documentation

Technical architecture and data flow documentation:

| Document | Description |
|----------|-------------|
| [Backend Architecture](architecture/BACKEND_ARCHITECTURE.md) | Backend layered architecture with Mermaid diagrams |
| [Frontend Data Flow](architecture/FRONTEND_DATA_FLOW.md) | Complete component hierarchy and data flow mapping |
| [Integration Architecture](architecture/INTEGRATION_ARCHITECTURE.md) | Universal frontend-backend integration patterns |
| [Master Data Reference](architecture/MASTER_DATA_REFERENCE.md) | Single source of truth for all data structures |
| [Backend Flowcharts](architecture/BACKEND_FLOWCHARTS.md) | Architectural flowcharts with Mermaid diagrams |
| [Data Types Reference](architecture/DATA_TYPES_REFERENCE.md) | Backend to frontend data architecture |
| [PlantUML Diagrams](architecture/diagrams/) | Professional-grade PlantUML architecture diagrams |

---

### Formal Specifications

Interface Control Documents and technical specifications:

| Document | Description |
|----------|-------------|
| [ICD Frontend Build](specifications/ICD_FRONTEND_BUILD.md) | NASA-style Interface Control Document for Cursor |
| [ICD Verification Report](specifications/ICD_VERIFICATION_REPORT.md) | Forensic verification of ICD compliance |
| [Frontend Tech Spec](specifications/FRONTEND_TECH_SPEC.md) | Frontend technical specification (4,190 lines) |

---

### Governance & Frameworks

Constitutional rules and quality frameworks:

| Document | Description |
|----------|-------------|
| [Gold Standard Framework](governance/GOLD_STANDARD_FRAMEWORK.md) | Universal audit framework v3.0 (1,367 lines) |
| [Financial Services Adapter](governance/FINANCIAL_SERVICES_ADAPTER.md) | Domain-specific adapter for financial services |
| [Cross-Cutting Concerns](governance/CROSS_CUTTING_CONCERNS.md) | Logging, security, and testing concerns |

---

### Audits & Reports

Project maturity and compliance audits:

| Document | Description |
|----------|-------------|
| [Project Maturity Audit (MD)](audits/PROJECT_MATURITY_AUDIT.md) | Exhaustive project maturity audit (1,185 lines) |
| [Project Maturity Audit (HTML)](audits/PROJECT_MATURITY_AUDIT.html) | Interactive HTML version with styling |
| [System Architecture Visual](audits/SYSTEM_ARCHITECTURE_VISUAL.html) | Visual HTML representation of architecture |

---

## Related Documentation

### AI Handoff Package

Complete documentation suite for AI agent handoff:

| Document | Description |
|----------|-------------|
| [HANDOFF_00_README](../AI_HANDOFF/HANDOFF_00_README.md) | Index and overview |
| [HANDOFF_01_DESIGN_SPECIFICATION](../AI_HANDOFF/HANDOFF_01_DESIGN_SPECIFICATION.md) | Visual design requirements |
| [HANDOFF_02_API_ENDPOINTS](../AI_HANDOFF/HANDOFF_02_API_ENDPOINTS.md) | Complete API documentation |
| [HANDOFF_03_CONSTITUTIONAL_RULES](../AI_HANDOFF/HANDOFF_03_CONSTITUTIONAL_RULES.md) | Inviolable system rules |
| [HANDOFF_04_TECHNICAL_STANDARDS](../AI_HANDOFF/HANDOFF_04_TECHNICAL_STANDARDS.md) | Engineering standards |
| [HANDOFF_05_COMPONENT_REQUIREMENTS](../AI_HANDOFF/HANDOFF_05_COMPONENT_REQUIREMENTS.md) | Component specifications |
| [HANDOFF_06_CSS_DESIGN_SYSTEM](../AI_HANDOFF/HANDOFF_06_CSS_DESIGN_SYSTEM.md) | CSS and styling system |
| [HANDOFF_07_BUSINESS_LOGIC](../AI_HANDOFF/HANDOFF_07_BUSINESS_LOGIC.md) | Core business algorithms |
| [HANDOFF_08_IMPLEMENTATION_STATUS](../AI_HANDOFF/HANDOFF_08_IMPLEMENTATION_STATUS.md) | Current implementation gaps |
| [AUTONOMOUS_HANDOFF_COMPREHENSIVE](../AI_HANDOFF/AUTONOMOUS_HANDOFF_COMPREHENSIVE.md) | Standalone comprehensive version |

---

### Architecture Decision Records (ADRs)

Strategic architectural decisions:

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](../context/decisions/ADR-001_Data_Repository_Model.md) | Data Repository Model | Accepted |
| [ADR-002](../context/decisions/ADR-002_Self_Contained_Workspace.md) | Self-Contained Workspace | Accepted |
| [ADR-003](../context/decisions/ADR-003_AI_Model_Selection.md) | AI Model Selection (Haiku/Sonnet/Opus) | Accepted |

---

### AI Prompts & Tools

Prompts and configurations for AI tooling:

| Document | Description |
|----------|-------------|
| [Cursor Prompt](../prompts/CURSOR_PROMPT.md) | Prompt template for Cursor AI |
| [V0 Component Prompts](../prompts/V0_COMPONENT_PROMPTS.md) | Component generation prompts for v0.dev |
| [Project Configuration](../prompts/PROJECT_CONFIGURATION.md) | Audit configuration for AI tools |

---

## Document Categories

### By Audience

| Audience | Recommended Reading |
|----------|---------------------|
| **New Developers** | Master Data Reference, Integration Architecture, ADRs |
| **Frontend Engineers** | Frontend Data Flow, ICD Frontend Build, Component Requirements |
| **Backend Engineers** | Backend Architecture, Backend Flowcharts, API Endpoints |
| **AI/ML Engineers** | Constitutional Rules, AI Model Selection, Gold Standard Framework |
| **Auditors** | Project Maturity Audit, Gold Standard Framework, ICD Verification |
| **Project Managers** | README, Implementation Status, Cross-Cutting Concerns |

### By Purpose

| Purpose | Documents |
|---------|-----------|
| **Understanding the System** | Master Data Reference, Integration Architecture |
| **Building New Features** | ICD Frontend Build, Component Requirements, Technical Standards |
| **Code Review** | Constitutional Rules, Gold Standard Framework |
| **Onboarding** | AI Handoff Package (all 10 files) |
| **Compliance** | Project Maturity Audit, ICD Verification Report |

---

## Document Statistics

| Category | Files | Total Lines |
|----------|-------|-------------|
| Architecture | 7 | ~5,500 |
| Specifications | 3 | ~7,000 |
| Governance | 3 | ~2,500 |
| Audits | 3 | ~2,500 |
| AI Handoff | 10 | ~4,000 |
| ADRs | 3 | ~300 |
| Prompts | 3 | ~900 |
| **Total** | **32** | **~22,700** |

---

## Constitutional Markers

Key constitutional compliance markers across documentation:

- **CR-001**: Decision-Support Only (no recommendations)
- **CR-002**: Never Resolve Contradictions (expose with equal weight)
- **CR-003**: Descriptive Not Prescriptive (mandatory disclaimers)

---

*This index was generated during the documentation reorganization on 2026-01-04*
