# PHASE 05: DETAILED SPECIFICATION
## Standards

**Purpose:** Quality standards for technical specifications

---

## API SPECIFICATION STANDARDS

### OpenAPI Requirements

Every REST API specification MUST include:

| Section | Required | Description |
|---------|----------|-------------|
| info.title | ✓ | API name |
| info.version | ✓ | Semantic version |
| info.description | ✓ | Purpose and scope |
| servers | ✓ | Environment URLs |
| security | ✓ | Auth requirements |
| paths | ✓ | All endpoints |
| components/schemas | ✓ | All data types |
| components/responses | ✓ | Standard errors |

### Endpoint Naming Standards

| Rule | Good | Bad |
|------|------|-----|
| Use nouns | /users | /getUsers |
| Plural for collections | /orders | /order |
| Lowercase | /user-profiles | /UserProfiles |
| Hyphens for multi-word | /order-items | /orderItems |
| No trailing slash | /users | /users/ |
| No verbs | /users/{id} | /users/{id}/delete |

### HTTP Method Usage

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve | Yes | Yes |
| POST | Create | No | No |
| PUT | Full update | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove | Yes | No |

### Response Status Codes

| Range | Meaning | Common Codes |
|-------|---------|--------------|
| 2xx | Success | 200, 201, 204 |
| 4xx | Client error | 400, 401, 403, 404, 409 |
| 5xx | Server error | 500, 502, 503 |

**Standard Usage:**
| Code | When to Use |
|------|-------------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (created) |
| 204 | Successful DELETE (no content) |
| 400 | Invalid request format |
| 401 | Missing/invalid authentication |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, version) |
| 500 | Unexpected server error |

---

## ERROR RESPONSE STANDARDS

### Standard Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email format is invalid"
      }
    ],
    "requestId": "uuid-for-tracing"
  }
}
```

### Error Code Naming

Format: `[DOMAIN]_[ERROR_TYPE]`

| Code | Meaning |
|------|---------|
| AUTH_INVALID_CREDENTIALS | Login failed |
| AUTH_TOKEN_EXPIRED | Token no longer valid |
| USER_NOT_FOUND | User doesn't exist |
| USER_EMAIL_EXISTS | Duplicate email |
| ORDER_INVALID_STATUS | Status transition invalid |

---

## DATA MODEL STANDARDS

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Table | snake_case, plural | user_accounts |
| Column | snake_case | created_at |
| Primary Key | id | id |
| Foreign Key | [entity]_id | user_id |
| Index | idx_[table]_[columns] | idx_users_email |
| Constraint | [type]_[table]_[detail] | uk_users_email |

### Required Columns

Every table MUST have:

| Column | Type | Purpose |
|--------|------|---------|
| id | UUID or BIGINT | Primary key |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last modification |

### Soft Delete Standard (When Used)

| Column | Type | Purpose |
|--------|------|---------|
| deleted_at | TIMESTAMP NULL | Deletion time (null = active) |
| deleted_by | UUID NULL | Who deleted |

### Data Type Standards

| Concept | Type | Notes |
|---------|------|-------|
| Primary key | UUID | Prefer over auto-increment |
| Money | DECIMAL(19,4) | Never use FLOAT |
| Timestamps | TIMESTAMP WITH TIME ZONE | Always with timezone |
| Boolean | BOOLEAN | Not INTEGER |
| Enum | VARCHAR or ENUM | Document allowed values |
| JSON | JSONB (Postgres) | With schema validation |

---

## COMPONENT SPECIFICATION STANDARDS

### Single Responsibility

Each component MUST:
- Have ONE clear purpose
- Have ONE reason to change
- Fit in ONE sentence description

### Interface Standards

Public interfaces MUST specify:

```markdown
## Method: [name]

**Signature:** `functionName(param1: Type, param2: Type): ReturnType`

**Purpose:** [What this method does]

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | [Description] |

**Returns:** [Type and description]

**Throws:**
| Error | When |
|-------|------|
| ValidationError | Input invalid |
| NotFoundError | Resource missing |

**Example:**
```typescript
const result = await functionName('value1', 123);
```
```

### Dependency Rules

| Rule | Description |
|------|-------------|
| Explicit | All dependencies declared |
| Injected | Dependencies passed in, not created |
| Interface | Depend on interfaces, not implementations |
| Direction | Lower layers don't depend on higher |

---

## SPECIFICATION COMPLETENESS CHECKLIST

### API Specification
- [ ] All endpoints documented
- [ ] All request parameters defined
- [ ] All response schemas defined
- [ ] All error responses documented
- [ ] Authentication requirements clear
- [ ] Rate limiting documented
- [ ] Versioning strategy defined
- [ ] Examples provided

### Data Model Specification
- [ ] All entities defined
- [ ] All attributes have types
- [ ] All constraints specified
- [ ] Relationships documented
- [ ] Indexes defined
- [ ] Audit columns included
- [ ] Migration notes provided

### Component Specification
- [ ] Purpose clearly stated
- [ ] Responsibilities listed
- [ ] Dependencies documented
- [ ] Public interface defined
- [ ] Error handling specified
- [ ] State management documented (if stateful)

---

## TRACEABILITY STANDARDS

### Specification to Requirements

Every specification element MUST trace to:
- At least one requirement
- No more requirements than necessary

### Specification to Tests

Every specification MUST have:
- At least one test case reference
- Clear acceptance criteria

### RTM Update

After Phase 5, RTM MUST include:

| Column | Content |
|--------|---------|
| REQ ID | Requirement identifier |
| Spec ID | Specification identifier |
| API Spec | OpenAPI operation reference |
| Data Spec | Entity/table reference |
| Component | Component reference |
| Test Cases | Test case references |

---

## VERSION CONTROL

### Specification Versioning

Format: `[Major].[Minor].[Patch]`

| Change Type | Version Impact |
|-------------|----------------|
| Breaking change | Major |
| New feature | Minor |
| Bug fix/clarification | Patch |

### Change Documentation

Every specification change MUST record:
- What changed
- Why it changed
- Impact assessment
- Migration notes (if breaking)

---

*STANDARDS v1.0 | PHASE 05 | Gold Standard System*
