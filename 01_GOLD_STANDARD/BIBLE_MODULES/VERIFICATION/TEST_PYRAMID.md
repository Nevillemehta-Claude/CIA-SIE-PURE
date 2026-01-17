# THE TEST PYRAMID
## Layered Verification Strategy

**Module:** VERIFICATION
**Version:** 1.0

---

## THE PYRAMID

```
                         /\
                        /  \
                       / E2E \           10%
                      /  Tests \         (Slow, Expensive)
                     /──────────\
                    /            \
                   /  Integration  \     20%
                  /     Tests       \    (Medium Speed)
                 /──────────────────\
                /                    \
               /    Contract Tests    \  20%
              /                        \ (API Boundaries)
             /──────────────────────────\
            /                            \
           /        Unit Tests            \  50%
          /                                \ (Fast, Cheap)
         /──────────────────────────────────\
```

**Pyramid principle:** More tests at lower levels, fewer at higher levels.

---

## LAYER 1: UNIT TESTS (50%)

### What They Test
- Individual functions
- Individual methods
- Individual components (in isolation)
- Pure logic

### Characteristics
| Attribute | Value |
|-----------|-------|
| Speed | Milliseconds per test |
| Dependencies | None (mocked) |
| Isolation | Complete |
| Determinism | 100% |

### What Makes a Good Unit Test
- Tests ONE thing
- Fast (< 100ms)
- No external dependencies
- No network, database, filesystem
- Deterministic (same result every time)

### Example
```typescript
describe('calculateFreshness', () => {
  it('returns CURRENT for timestamp within 2 minutes', () => {
    const twoMinutesAgo = new Date(Date.now() - 2 * 60 * 1000)
    expect(calculateFreshness(twoMinutesAgo)).toBe('CURRENT')
  })

  it('returns STALE for timestamp over 30 minutes', () => {
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000)
    expect(calculateFreshness(oneHourAgo)).toBe('STALE')
  })
})
```

### Coverage Target
- Statement coverage: >90%
- Branch coverage: >80%

---

## LAYER 2: CONTRACT TESTS (20%)

### What They Test
- API request/response schemas
- Interface boundaries
- Data format agreements
- Error response formats

### Characteristics
| Attribute | Value |
|-----------|-------|
| Speed | Seconds per test |
| Dependencies | API specification |
| Isolation | Tests boundary only |
| Determinism | 100% |

### What Makes a Good Contract Test
- Validates against OpenAPI/Swagger spec
- Tests both valid and invalid requests
- Tests all response codes
- Tests error formats

### Example
```typescript
describe('GET /api/v1/instruments', () => {
  it('returns array of instruments matching schema', async () => {
    const response = await api.get('/instruments')
    expect(response.status).toBe(200)
    expect(response.data).toMatchSchema(InstrumentListSchema)
  })

  it('returns 401 for unauthenticated request', async () => {
    const response = await api.get('/instruments', { auth: null })
    expect(response.status).toBe(401)
    expect(response.data).toMatchSchema(ErrorSchema)
  })
})
```

### Coverage Target
- 100% of API endpoints
- All documented status codes

---

## LAYER 3: INTEGRATION TESTS (20%)

### What They Test
- Component interactions
- Service-to-service communication
- Database operations
- Message queue flows

### Characteristics
| Attribute | Value |
|-----------|-------|
| Speed | Seconds to minutes |
| Dependencies | Other services, databases |
| Isolation | Partial (test doubles for externals) |
| Determinism | High (with proper setup) |

### What Makes a Good Integration Test
- Tests real interactions between components
- Uses real database (test instance)
- Tests transaction boundaries
- Tests error propagation

### Example
```typescript
describe('UserService + Database', () => {
  beforeEach(async () => {
    await database.reset()
  })

  it('persists user and retrieves by ID', async () => {
    const user = await userService.create({ name: 'Test' })
    const retrieved = await userService.findById(user.id)
    expect(retrieved.name).toBe('Test')
  })

  it('rolls back transaction on validation error', async () => {
    await expect(userService.create({ name: null }))
      .rejects.toThrow(ValidationError)
    const count = await userService.count()
    expect(count).toBe(0)
  })
})
```

### Coverage Target
- All service interactions
- All database operations
- All integration points

---

## LAYER 4: END-TO-END TESTS (10%)

### What They Test
- Complete user flows
- System behavior from UI to database
- Real browser interactions
- Production-like environment

### Characteristics
| Attribute | Value |
|-----------|-------|
| Speed | Minutes per test |
| Dependencies | Full system |
| Isolation | None |
| Determinism | Lower (environment-dependent) |

### What Makes a Good E2E Test
- Tests critical user journeys
- Uses real browser
- Tests real API (not mocked)
- Minimal number, maximum coverage

### Example
```typescript
describe('User Registration Flow', () => {
  it('completes registration and reaches dashboard', async () => {
    await page.goto('/register')
    await page.fill('#email', 'test@example.com')
    await page.fill('#password', 'SecurePass123!')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('Welcome')
  })
})
```

### Coverage Target
- All critical user journeys
- Happy paths for main features
- Key error scenarios

---

## TEST DISTRIBUTION

| Layer | Percentage | Typical Count |
|-------|------------|---------------|
| Unit | 50% | Hundreds to thousands |
| Contract | 20% | Tens to hundreds |
| Integration | 20% | Tens to hundreds |
| E2E | 10% | Tens |

---

## WHY THE PYRAMID SHAPE?

### Lower Tests Are Better Because:
- **Faster:** Milliseconds vs. minutes
- **Cheaper:** No infrastructure needed
- **More Focused:** Isolate failures precisely
- **More Stable:** Fewer moving parts

### Higher Tests Still Needed Because:
- **Real Integration:** Catch interface mismatches
- **User Perspective:** Verify actual workflows
- **System Behavior:** Validate emergent properties

---

## ANTI-PATTERN: THE ICE CREAM CONE

```
           /─────────────────\
          /                   \
         /    Many E2E Tests   \    <- EXPENSIVE, SLOW
        /                       \
       /─────────────────────────\
      /                           \
     /    Some Integration Tests   \
    /                               \
   /─────────────────────────────────\
  /                                   \
 /         Few Unit Tests              \  <- SHOULD BE MANY
/                                       \
```

**Problem:** Too many slow, expensive tests; too few fast, cheap tests.
**Result:** Slow feedback, brittle tests, missed bugs.
**Fix:** Invert the pyramid.

---

## ANTI-PATTERN: THE HOURGLASS

```
        /─────────\
       /           \
      /  Many E2E   \
     /               \
    /─────────────────\
          |     |
          |     |       <- FEW INTEGRATION
          |     |
    \─────────────────/
     \               /
      \  Many Unit  /
       \           /
        \─────────/
```

**Problem:** Missing middle layer.
**Result:** E2E tests catch integration bugs (slowly and painfully).
**Fix:** Add integration test layer.

---

*TEST_PYRAMID v1.0 | VERIFICATION | BIBLE_MODULES*
