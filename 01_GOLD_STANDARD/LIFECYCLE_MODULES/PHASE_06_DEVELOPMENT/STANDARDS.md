# PHASE 06: DEVELOPMENT
## Standards Document

**Phase Number:** 6
**Purpose:** Define quality standards for the development phase

---

## CODE QUALITY STANDARDS

### TypeScript/JavaScript Standards

| Standard | Requirement | Enforcement |
|----------|-------------|-------------|
| Type Coverage | 100% - no `any` types | TypeScript strict mode |
| Null Safety | Explicit null handling | ESLint rules |
| Immutability | Prefer const, readonly | ESLint rules |
| Pure Functions | Side-effect free where possible | Code review |

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Files (components) | PascalCase | `UserProfile.tsx` |
| Files (utilities) | camelCase | `dateUtils.ts` |
| Functions | camelCase | `calculateTotal()` |
| Classes | PascalCase | `UserService` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES` |
| Interfaces | PascalCase, 'I' prefix optional | `UserProps` or `IUserProps` |
| Types | PascalCase | `SignalDirection` |

### Code Structure

```typescript
// File structure (component)
// 1. Imports
import { useState } from 'react'
import type { Props } from './types'

// 2. Types (if not in separate file)
interface ComponentProps {
  // ...
}

// 3. Constants
const DEFAULT_VALUE = 10

// 4. Component
export const Component: React.FC<ComponentProps> = ({ prop }) => {
  // Hooks first
  const [state, setState] = useState(DEFAULT_VALUE)

  // Handlers
  const handleClick = () => { /* ... */ }

  // Render
  return (/* ... */)
}

// 5. Exports (if not inline)
```

---

## TESTING STANDARDS

### Unit Testing

| Standard | Requirement |
|----------|-------------|
| Coverage Target | >90% statement coverage |
| Test Location | Co-located with source (file.test.ts) |
| Test Naming | `describe('Module', () => { it('should behavior', ...) })` |
| Assertions | Clear, specific assertions |
| Independence | Tests must not depend on each other |

### Test Structure

```typescript
describe('calculateFreshness', () => {
  // Setup
  beforeEach(() => {
    // Reset state
  })

  // Happy path
  it('should return CURRENT for timestamps within 2 minutes', () => {
    const result = calculateFreshness(recentTimestamp)
    expect(result).toBe('CURRENT')
  })

  // Edge cases
  it('should handle null timestamp', () => {
    const result = calculateFreshness(null)
    expect(result).toBe('UNAVAILABLE')
  })

  // Error cases
  it('should throw for invalid timestamp format', () => {
    expect(() => calculateFreshness('invalid')).toThrow(InvalidTimestampError)
  })
})
```

### Contract Testing

| Standard | Requirement |
|----------|-------------|
| API Contracts | OpenAPI specification compliance |
| Request Validation | All request schemas validated |
| Response Validation | All response schemas validated |
| Error Codes | All documented error codes tested |

---

## DOCUMENTATION STANDARDS

### Function Documentation

```typescript
/**
 * Calculates the freshness status of a signal based on its timestamp.
 *
 * @param timestamp - ISO 8601 timestamp of the signal, or null if never received
 * @param thresholds - Custom thresholds (optional, defaults to standard)
 * @returns FreshnessStatus indicating how current the signal is
 *
 * @example
 * const status = calculateFreshness('2026-01-14T10:30:00Z')
 * // Returns 'CURRENT' if within 2 minutes
 *
 * @throws {InvalidTimestampError} If timestamp format is invalid
 */
function calculateFreshness(
  timestamp: string | null,
  thresholds?: FreshnessThresholds
): FreshnessStatus {
  // ...
}
```

### Component Documentation

```typescript
/**
 * Displays the freshness status of a signal with appropriate styling.
 *
 * @component
 * @example
 * <FreshnessIndicator status="CURRENT" />
 *
 * @accessibility
 * - Uses semantic color + text for colorblind users
 * - Includes aria-label for screen readers
 */
```

---

## ERROR HANDLING STANDARDS

### Error Hierarchy

```typescript
// Base error class
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number
  ) {
    super(message)
  }
}

// Specific errors
class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 'VALIDATION_ERROR', 400)
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404)
  }
}
```

### Error Handling Pattern

```typescript
// DO
try {
  const result = await fetchData()
  return result
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('Validation failed', { error })
    throw error  // Let caller handle
  }
  if (error instanceof NotFoundError) {
    return null  // Expected case, handle gracefully
  }
  // Unexpected error
  logger.error('Unexpected error in fetchData', { error })
  throw new AppError('Internal error', 'INTERNAL_ERROR', 500)
}

// DON'T
try {
  const result = await fetchData()
  return result
} catch (error) {
  console.log(error)  // Not enough context
  return null  // Swallowing all errors
}
```

---

## PERFORMANCE STANDARDS

### Complexity Limits

| Metric | Maximum | Tool |
|--------|---------|------|
| Cyclomatic Complexity | 10 per function | ESLint |
| File Length | 300 lines | ESLint |
| Function Length | 50 lines | ESLint |
| Nesting Depth | 4 levels | ESLint |

### Optimization Guidelines

| Technique | When to Use |
|-----------|-------------|
| Memoization | Expensive calculations |
| useCallback | Handlers passed to children |
| useMemo | Derived state calculations |
| Virtualization | Lists > 100 items |
| Code Splitting | Large components |
| Lazy Loading | Non-critical features |

---

## SECURITY STANDARDS

### Input Validation

```typescript
// Always validate external data
const validated = schema.parse(externalData)

// Never trust user input
const sanitized = sanitizeHtml(userInput)

// Parameterize all queries
const result = db.query('SELECT * FROM users WHERE id = $1', [userId])
```

### Forbidden Patterns

| Pattern | Why Forbidden | Alternative |
|---------|---------------|-------------|
| `eval()` | Code injection risk | Use safe alternatives |
| `dangerouslySetInnerHTML` | XSS risk | Sanitize first |
| Hardcoded secrets | Exposure risk | Environment variables |
| SQL concatenation | Injection risk | Parameterized queries |

---

## CODE REVIEW STANDARDS

### Review Checklist

**Functionality**
- [ ] Implements specification correctly
- [ ] Handles edge cases
- [ ] Handles errors appropriately

**Quality**
- [ ] No code duplication
- [ ] Functions are focused (single responsibility)
- [ ] Names are descriptive
- [ ] No magic numbers

**Testing**
- [ ] Unit tests cover new code
- [ ] Tests cover happy path and edge cases
- [ ] Tests are independent and repeatable

**Security**
- [ ] No hardcoded secrets
- [ ] Input is validated
- [ ] Output is escaped where necessary

**Documentation**
- [ ] Complex logic is documented
- [ ] Public APIs have JSDoc comments
- [ ] README updated if necessary

---

## COMMIT STANDARDS

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Purpose |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no code change |
| refactor | Restructure, no behavior change |
| test | Add or update tests |
| chore | Build, tools, dependencies |

### Example

```
feat(auth): add token refresh mechanism

Implement automatic token refresh when access token expires.
Includes retry logic with exponential backoff.

Closes #123
```

---

## ANTI-PATTERNS TO AVOID

### 1. Copy-Paste Programming
**Smell:** Same code in multiple places
**Fix:** Extract to shared utility

### 2. Magic Numbers
**Smell:** `if (status === 2)`
**Fix:** `if (status === STATUS.APPROVED)`

### 3. God Function
**Smell:** Function doing 10 things
**Fix:** Split into focused functions

### 4. Callback Hell
**Smell:** Deeply nested callbacks
**Fix:** Use async/await, Promises

### 5. Premature Optimization
**Smell:** Complex caching before measuring
**Fix:** Profile first, optimize second

---

*PHASE 06 STANDARDS v1.0 | LIFECYCLE_MODULES | Gold Standard System*
