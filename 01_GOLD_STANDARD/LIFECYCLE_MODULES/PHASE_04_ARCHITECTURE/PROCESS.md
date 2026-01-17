# PHASE 04: ARCHITECTURE DESIGN
## Process Guide

**Purpose:** Step-by-step process for designing system architecture using C4 model

---

## PROCESS OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 4 PROCESS FLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1          STEP 2          STEP 3          STEP 4    │
│  ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐    │
│  │Context│─────▶│Container│────▶│Evaluate│─────▶│Document│ │
│  │(C4 L1)│      │(C4 L2) │      │Options│       │Decisions│ │
│  └──────┘       └──────┘       └──────┘       └──────┘    │
│                                                             │
│  Shows:         Shows:         Analyzes:     Records:      │
│  - System       - Containers   - Trade-offs  - ADRs        │
│  - Users        - Tech stack   - Risks       - Rationale   │
│  - External     - Data flows   - Fit         - Diagrams    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## STEP 1: CONTEXT DIAGRAM (C4 Level 1)

### 1.1 Identify System Boundary

Define what is inside vs outside your system:

```markdown
## System Boundary Definition

**System Name:** [Name]

### Inside (Our Scope)
- [Component 1]
- [Component 2]

### Outside (External)
- [External System 1]
- [External System 2]
```

### 1.2 Identify Actors

```markdown
## Actors

### Users (People)
| Actor | Description | Interaction |
|-------|-------------|-------------|
| [Name] | [Who they are] | [How they interact] |

### External Systems
| System | Owner | Interface | Purpose |
|--------|-------|-----------|---------|
| [Name] | [Who owns] | [API/File/etc] | [What for] |
```

### 1.3 Draw Context Diagram

```
                     ┌─────────────┐
                     │   Actor 1   │
                     │   (User)    │
                     └──────┬──────┘
                            │
                            ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  External   │◄────▶│             │◄────▶│  External   │
│  System A   │      │   [YOUR     │      │  System B   │
└─────────────┘      │   SYSTEM]   │      └─────────────┘
                     │             │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Actor 2   │
                     │   (Admin)   │
                     └─────────────┘
```

### 1.4 Document Context

```markdown
## Context Diagram Documentation

**Diagram Version:** [X.Y]
**Last Updated:** [Date]

### Actors
1. **[Actor 1]**: [Description of interaction]
2. **[Actor 2]**: [Description of interaction]

### External Systems
1. **[System A]**: [What data/services exchanged]
2. **[System B]**: [What data/services exchanged]

### Key Data Flows
| From | To | Data | Protocol |
|------|-----|------|----------|
| Actor 1 | System | [Data] | HTTPS |
| System | External A | [Data] | REST API |
```

---

## STEP 2: CONTAINER DIAGRAM (C4 Level 2)

### 2.1 Identify Containers

A container is a separately deployable unit:

| Container Type | Examples |
|----------------|----------|
| Web Application | React SPA, Angular app |
| API Application | REST API, GraphQL server |
| Database | PostgreSQL, MongoDB |
| Message Queue | RabbitMQ, Kafka |
| File Storage | S3, Azure Blob |

### 2.2 Define Each Container

```markdown
## Container: [Name]

**Type:** [Web App/API/Database/Queue/etc]
**Technology:** [Specific technology]
**Purpose:** [What it does]

### Responsibilities
- [Responsibility 1]
- [Responsibility 2]

### Interfaces
| Interface | Type | Protocol | Description |
|-----------|------|----------|-------------|
| [Name] | Inbound/Outbound | [Protocol] | [Purpose] |

### Data Stored (if applicable)
- [Data type 1]
- [Data type 2]
```

### 2.3 Draw Container Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        [SYSTEM NAME]                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │   Web App   │────────▶│   API       │                   │
│  │   (React)   │  HTTP   │   (Node.js) │                   │
│  └─────────────┘         └──────┬──────┘                   │
│                                 │                           │
│                                 │ SQL                       │
│                                 ▼                           │
│                          ┌─────────────┐                   │
│                          │  Database   │                   │
│                          │ (PostgreSQL)│                   │
│                          └─────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 Define Container Interactions

```markdown
## Container Interactions

| From | To | Protocol | Data | Sync/Async |
|------|-----|----------|------|------------|
| Web App | API | HTTPS/REST | JSON | Sync |
| API | Database | TCP/SQL | Queries | Sync |
| API | Queue | AMQP | Events | Async |
```

---

## STEP 3: EVALUATE OPTIONS

### 3.1 Technology Selection

For each major decision:

```markdown
## Technology Decision: [Area]

### Context
[Why this decision is needed]

### Options Considered

**Option A: [Name]**
- Pros: [List]
- Cons: [List]
- Risk: [Assessment]
- Cost: [Assessment]

**Option B: [Name]**
- Pros: [List]
- Cons: [List]
- Risk: [Assessment]
- Cost: [Assessment]

### Evaluation Matrix

| Criterion | Weight | Option A | Option B |
|-----------|--------|----------|----------|
| Performance | 25% | 4/5 | 3/5 |
| Scalability | 20% | 5/5 | 4/5 |
| Team Skills | 20% | 3/5 | 5/5 |
| Cost | 15% | 4/5 | 3/5 |
| Ecosystem | 10% | 4/5 | 5/5 |
| Security | 10% | 5/5 | 4/5 |
| **Weighted** | **100%** | **4.05** | **3.9** |

### Recommendation
[Selected option and why]
```

### 3.2 Architecture Patterns

Evaluate applicable patterns:

| Pattern | When to Use | Trade-offs |
|---------|-------------|------------|
| Monolith | Simple apps, small teams | Easy start, scaling limits |
| Microservices | Complex domains, large teams | Flexible, operational complexity |
| Event-Driven | Async workflows, decoupling | Scalable, debugging harder |
| Serverless | Variable load, managed ops | Auto-scale, vendor lock-in |

### 3.3 Risk Assessment

```markdown
## Architecture Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Strategy] |
| [Risk 2] | H/M/L | H/M/L | [Strategy] |
```

---

## STEP 4: DOCUMENT DECISIONS

### 4.1 Architecture Decision Records (ADRs)

```markdown
# ADR-[NUMBER]: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** [Date]
**Deciders:** [Names]

## Context
[What is the issue that we're seeing that is motivating this decision]

## Decision
[What is the change that we're proposing and/or doing]

## Consequences
[What becomes easier or more difficult to do because of this change]

### Positive
- [Consequence 1]
- [Consequence 2]

### Negative
- [Consequence 1]
- [Consequence 2]

### Neutral
- [Consequence 1]

## Alternatives Considered
- [Alternative 1]: Rejected because [reason]
- [Alternative 2]: Rejected because [reason]
```

### 4.2 Architecture Document Structure

```markdown
# Architecture Document

## 1. Introduction
- Purpose
- Scope
- Definitions

## 2. Architectural Goals
- Quality attributes
- Constraints
- Assumptions

## 3. System Context (C4 L1)
- Context diagram
- External interfaces

## 4. Container View (C4 L2)
- Container diagram
- Container descriptions
- Technology stack

## 5. Cross-Cutting Concerns
- Security
- Logging
- Error handling
- Configuration

## 6. Deployment View
- Infrastructure
- Environments
- Scaling strategy

## 7. Decision Log
- ADR index

## Appendices
- Glossary
- References
```

---

## DELIVERABLES CHECKLIST

- [ ] Context Diagram (C4 Level 1)
- [ ] Container Diagram (C4 Level 2)
- [ ] Technology Selection Documentation
- [ ] Architecture Decision Records (ADRs)
- [ ] Architecture Document
- [ ] Updated RTM (Design references)

---

*PROCESS v1.0 | PHASE 04 | Gold Standard System*
