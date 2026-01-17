# PHASE 05: DETAILED SPECIFICATION
## Process Guide

**Purpose:** Step-by-step process for creating detailed technical specifications

---

## PROCESS OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 5 PROCESS FLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1          STEP 2          STEP 3          STEP 4    │
│  ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐    │
│  │Decompose│───▶│Specify│─────▶│Define │─────▶│Review │    │
│  │Components│   │APIs   │      │Data   │      │Specs  │    │
│  └──────┘       └──────┘       └──────┘       └──────┘    │
│                                                             │
│  C4 Level 3     OpenAPI/       Entity-        Technical    │
│  Diagrams       AsyncAPI       Relationship   Review       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## STEP 1: DECOMPOSE TO COMPONENTS (C4 Level 3)

### 1.1 Identify Components

For each container from Phase 4:

```markdown
## Container: [Name]

### Component Decomposition

| Component | Responsibility | Type |
|-----------|---------------|------|
| [Name] | [What it does] | [Service/Repository/Controller/etc] |
| [Name] | [What it does] | [Type] |
```

### 1.2 Component Specification

```markdown
## Component: [Name]

**Parent Container:** [Container name]
**ID:** CMP-[NNN]
**Type:** [Controller | Service | Repository | Handler | etc]

### Purpose
[What this component does - single responsibility]

### Responsibilities
1. [Specific responsibility]
2. [Specific responsibility]

### Does NOT Handle
- [What this component should NOT do]

### Dependencies
| Depends On | Type | Purpose |
|------------|------|---------|
| [Component] | Internal | [Why] |
| [External] | External | [Why] |

### Public Interface
[Methods/functions exposed]
```

### 1.3 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   API Container (Node.js)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Controller  │───▶│   Service    │───▶│  Repository  │  │
│  │  (Express)   │    │   (Logic)    │    │    (DB)      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                              │
│         ▼                   ▼                              │
│  ┌──────────────┐    ┌──────────────┐                     │
│  │  Middleware  │    │  Validator   │                     │
│  │  (Auth/Log)  │    │   (Joi)      │                     │
│  └──────────────┘    └──────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## STEP 2: SPECIFY APIs

### 2.1 REST API Specification (OpenAPI)

```yaml
openapi: 3.0.3
info:
  title: [API Name]
  version: 1.0.0
  description: [Description]

servers:
  - url: https://api.example.com/v1
    description: Production

paths:
  /resource:
    get:
      summary: List resources
      operationId: listResources
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          $ref: '#/components/responses/Unauthorized'
```

### 2.2 Endpoint Specification Template

```markdown
## Endpoint: [METHOD] [Path]

**Operation ID:** [operationId]
**Summary:** [Brief description]

### Request

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | string (UUID) | Resource ID |

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 20 | Max results |

**Request Body:**
```json
{
  "field": "value"
}
```

### Response

**Success (200):**
```json
{
  "id": "uuid",
  "field": "value"
}
```

**Errors:**
| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_REQUEST | Request validation failed |
| 401 | UNAUTHORIZED | Missing/invalid token |
| 404 | NOT_FOUND | Resource not found |
```

### 2.3 Event Specification (AsyncAPI)

```yaml
asyncapi: 2.6.0
info:
  title: [Event API Name]
  version: 1.0.0

channels:
  order/created:
    publish:
      summary: Order created event
      message:
        payload:
          type: object
          properties:
            orderId:
              type: string
            timestamp:
              type: string
              format: date-time
```

---

## STEP 3: DEFINE DATA MODEL

### 3.1 Entity Specification

```markdown
## Entity: [Name]

**Table/Collection:** [db_table_name]
**Description:** [What this entity represents]

### Attributes

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Primary key |
| name | VARCHAR(100) | NOT NULL | Display name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last modification |

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| idx_users_email | email | UNIQUE | Email lookup |
| idx_users_created | created_at | BTREE | Time-based queries |

### Relationships

| Related Entity | Type | FK Column | Description |
|----------------|------|-----------|-------------|
| Order | 1:N | user_id | User's orders |
| Role | N:M | (via user_roles) | User's roles |
```

### 3.2 Entity-Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │    Order     │       │   Product    │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │──1:N─▶│ id (PK)      │◀─N:M──│ id (PK)      │
│ name         │       │ user_id (FK) │       │ name         │
│ email        │       │ total        │       │ price        │
│ created_at   │       │ status       │       │ stock        │
└──────────────┘       └──────────────┘       └──────────────┘
```

### 3.3 Data Type Definitions

```markdown
## Custom Types

### Status Enum
| Value | Description |
|-------|-------------|
| PENDING | Initial state |
| ACTIVE | In progress |
| COMPLETED | Successfully finished |
| CANCELLED | User cancelled |
| FAILED | Error occurred |

### Money Type
- Precision: 2 decimal places
- Currency: Stored separately
- Storage: INTEGER (cents) or DECIMAL(19,4)
```

---

## STEP 4: REVIEW SPECIFICATIONS

### 4.1 Technical Review Checklist

**API Review:**
- [ ] All endpoints documented
- [ ] Request/response schemas complete
- [ ] Error responses standardized
- [ ] Authentication specified
- [ ] Versioning strategy defined

**Data Model Review:**
- [ ] All entities defined
- [ ] Relationships documented
- [ ] Constraints specified
- [ ] Indexes planned
- [ ] Migration strategy considered

**Component Review:**
- [ ] Single responsibility verified
- [ ] Dependencies minimized
- [ ] Interfaces well-defined
- [ ] Error handling specified

### 4.2 Specification Review Meeting

```markdown
## Specification Review Record

**Date:** [Date]
**Specifications Reviewed:** [List]
**Participants:** [Names]

### Review Results

| Spec | Status | Issues | Resolution |
|------|--------|--------|------------|
| [API 1] | Approved | None | - |
| [Entity 1] | Modified | Missing index | Added idx_x |

### Action Items
- [ ] [Action] - Owner: [Name] - Due: [Date]

### Sign-off
| Reviewer | Role | Approved |
|----------|------|----------|
| [Name] | Tech Lead | ✓ |
| [Name] | DBA | ✓ |
```

### 4.3 Update Traceability

Update RTM with specification links:

| REQ ID | Requirement | API Spec | Data Spec | Component |
|--------|-------------|----------|-----------|-----------|
| REQ-001 | User login | POST /auth/login | User entity | AuthService |

---

## DELIVERABLES CHECKLIST

- [ ] Component Diagrams (C4 Level 3)
- [ ] Component Specifications
- [ ] API Specifications (OpenAPI/AsyncAPI)
- [ ] Data Model Specifications
- [ ] Entity-Relationship Diagrams
- [ ] Updated RTM with design links
- [ ] Technical Review Sign-off

---

*PROCESS v1.0 | PHASE 05 | Gold Standard System*
