# CIA-SIE API ENDPOINT REGISTRY
## Complete API Route Documentation

---

**Generated:** 2026-01-15
**Base URL:** `/api/v1`
**Total Endpoints:** 54

---

## EXECUTIVE SUMMARY

| Router | Prefix | Endpoints | Status |
|--------|--------|-----------|--------|
| instruments | /instruments | 6 | ✅ Active |
| silos | /silos | 4 | ✅ Active |
| charts | /charts | 5 | ✅ Active |
| signals | /signals | 3 | ✅ Active |
| webhooks | /webhook | 3 | ✅ Active |
| relationships | /relationships | 3 | ✅ Active |
| narratives | /narratives | 2 | ✅ Active |
| baskets | /baskets | 6 | ✅ Active |
| ai | /ai | 6 | ✅ Active |
| chat | /chat | 2 | ✅ Active |
| strategy | /strategy | 1 | ✅ Active |
| platforms | /platforms | 14 | ✅ Active |
| market-intelligence | /market-intelligence | 1 | ✅ Active |

---

## 1. INSTRUMENTS API

**Router:** `instruments_router`
**Prefix:** `/api/v1/instruments`
**Tag:** Instruments

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/` | List all instruments | `list[Instrument]` |
| POST | `/` | Create new instrument | `Instrument` (201) |
| GET | `/{instrument_id}` | Get instrument by ID | `Instrument` |
| GET | `/symbol/{symbol}` | Get instrument by symbol | `Instrument` |
| PATCH | `/{instrument_id}` | Update instrument | `Instrument` |
| DELETE | `/{instrument_id}` | Delete instrument | 204 No Content |

### Source References
- `GET /` - instruments.py:38
- `POST /` - instruments.py:53
- `GET /{instrument_id}` - instruments.py:87
- `GET /symbol/{symbol}` - instruments.py:104
- `PATCH /{instrument_id}` - instruments.py:121
- `DELETE /{instrument_id}` - instruments.py:145

---

## 2. SILOS API

**Router:** `silos_router`
**Prefix:** `/api/v1/silos`
**Tag:** Silos

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/` | List all silos | `list[Silo]` |
| POST | `/` | Create new silo | `Silo` (201) |
| GET | `/{silo_id}` | Get silo by ID | `Silo` |
| DELETE | `/{silo_id}` | Delete silo | 204 No Content |

### Source References
- `GET /` - silos.py:38
- `POST /` - silos.py:54
- `GET /{silo_id}` - silos.py:81
- `DELETE /{silo_id}` - silos.py:98

---

## 3. CHARTS API

**Router:** `charts_router`
**Prefix:** `/api/v1/charts`
**Tag:** Charts

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/` | List all charts | `list[Chart]` |
| POST | `/` | Create new chart | `Chart` (201) |
| GET | `/{chart_id}` | Get chart by ID | `Chart` |
| GET | `/webhook/{webhook_id}` | Get chart by webhook ID | `Chart` |
| DELETE | `/{chart_id}` | Delete chart | 204 No Content |

### Source References
- `GET /` - charts.py:40
- `POST /` - charts.py:56
- `GET /{chart_id}` - charts.py:84
- `GET /webhook/{webhook_id}` - charts.py:101
- `DELETE /{chart_id}` - charts.py:118

---

## 4. SIGNALS API

**Router:** `signals_router`
**Prefix:** `/api/v1/signals`
**Tag:** Signals

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/chart/{chart_id}` | Get signals for chart | `list[Signal]` |
| GET | `/chart/{chart_id}/latest` | Get latest signal | `Optional[Signal]` |
| GET | `/{signal_id}` | Get signal by ID | `Signal` |

### Source References
- `GET /chart/{chart_id}` - signals.py:41
- `GET /chart/{chart_id}/latest` - signals.py:56
- `GET /{signal_id}` - signals.py:70

---

## 5. WEBHOOKS API

**Router:** `webhooks_router`
**Prefix:** `/api/v1/webhook`
**Tag:** Webhooks

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| POST | `/` | Receive TradingView alert | `dict` |
| POST | `/manual` | Manually submit signal | `dict` |
| GET | `/health` | Webhook health check | `dict` |

### Source References
- `POST /` - webhooks.py:68
- `POST /manual` - webhooks.py:185
- `GET /health` - webhooks.py:260

### Webhook Payload Schema
```json
{
  "webhook_id": "GOLDBEES_01A_PRIMARY",
  "direction": "BULLISH|BEARISH|NEUTRAL",
  "signal_type": "STATE_CHANGE|BAR_CLOSE|HEARTBEAT|MANUAL",
  "timestamp": "2026-01-15T10:30:00Z",
  "indicators": {}
}
```

---

## 6. RELATIONSHIPS API

**Router:** `relationships_router`
**Prefix:** `/api/v1/relationships`
**Tag:** Relationships

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/silo/{silo_id}` | Get silo relationships | `RelationshipSummary` |
| GET | `/instrument/{instrument_id}` | Get all instrument relationships | `list[RelationshipSummary]` |
| GET | `/contradictions/silo/{silo_id}` | Get silo contradictions | `list[Contradiction]` |

### Source References
- `GET /silo/{silo_id}` - relationships.py:48
- `GET /instrument/{instrument_id}` - relationships.py:79
- `GET /contradictions/silo/{silo_id}` - relationships.py:98

### Constitutional Note
This endpoint EXPOSES contradictions - it does NOT resolve them.

---

## 7. NARRATIVES API

**Router:** `narratives_router`
**Prefix:** `/api/v1/narratives`
**Tag:** Narratives

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/silo/{silo_id}` | Generate AI narrative | `Narrative` |
| GET | `/silo/{silo_id}/plain` | Get plain text narrative | `str` |

### Source References
- `GET /silo/{silo_id}` - narratives.py:64
- `GET /silo/{silo_id}/plain` - narratives.py:113

### Constitutional Note
All narratives are DESCRIPTIVE only. Each includes mandatory disclaimer.

---

## 8. BASKETS API

**Router:** `baskets_router`
**Prefix:** `/api/v1/baskets`
**Tag:** Analytical Baskets

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/` | List all baskets | `list[AnalyticalBasket]` |
| POST | `/` | Create new basket | `AnalyticalBasket` (201) |
| GET | `/{basket_id}` | Get basket by ID | `AnalyticalBasket` |
| POST | `/{basket_id}/charts/{chart_id}` | Add chart to basket | 204 No Content |
| DELETE | `/{basket_id}/charts/{chart_id}` | Remove chart from basket | 204 No Content |
| DELETE | `/{basket_id}` | Delete basket | 204 No Content |

### Source References
- `GET /` - baskets.py:36
- `POST /` - baskets.py:55
- `GET /{basket_id}` - baskets.py:85
- `POST /{basket_id}/charts/{chart_id}` - baskets.py:102
- `DELETE /{basket_id}/charts/{chart_id}` - baskets.py:122
- `DELETE /{basket_id}` - baskets.py:141

### Constitutional Note
Baskets are UI-ONLY constructs. They do NOT affect signal processing.

---

## 9. AI MANAGEMENT API

**Router:** `ai_router`
**Prefix:** `/api/v1/ai`
**Tag:** AI Management

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/models` | List available models | `list[ModelResponse]` |
| GET | `/models/summary` | Get models summary | `ModelsListResponse` |
| GET | `/usage` | Get usage statistics | `UsageResponse` |
| GET | `/budget` | Get budget status | `BudgetStatusResponse` |
| POST | `/configure` | Configure AI settings | `ConfigureResponse` |
| GET | `/health` | AI health check | `dict` |

### Source References
- `GET /models` - ai.py:167
- `GET /models/summary` - ai.py:181
- `GET /usage` - ai.py:199
- `GET /budget` - ai.py:238
- `POST /configure` - ai.py:251
- `GET /health` - ai.py:294

---

## 10. CHAT API

**Router:** `chat_router`
**Prefix:** `/api/v1/chat`
**Tag:** AI Chat

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| POST | `/{scrip_id}` | Send chat message | `ChatResponse` |
| GET | `/{scrip_id}/history` | Get chat history | `ChatHistoryResponse` |

### Source References
- `POST /{scrip_id}` - chat.py:215
- `GET /{scrip_id}/history` - chat.py:360

### Constitutional Note
All chat responses are DESCRIPTIVE. No recommendations provided.

---

## 11. STRATEGY API

**Router:** `strategy_router`
**Prefix:** `/api/v1/strategy`
**Tag:** Strategy Analysis

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| POST | `/evaluate` | Evaluate strategy | `StrategyEvaluationResponse` |

### Source References
- `POST /evaluate` - strategy.py:258

---

## 12. PLATFORMS API

**Router:** `platforms_router`
**Prefix:** `/api/v1/platforms`
**Tag:** Platform Integration

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| GET | `/` | List platforms | `list[PlatformInfo]` |
| GET | `/{platform_name}` | Get platform info | `PlatformInfo` |
| POST | `/connect` | Connect platform | `PlatformConnectResponse` |
| POST | `/{platform_name}/disconnect` | Disconnect platform | `dict` |
| GET | `/{platform_name}/health` | Platform health | `dict` |
| GET | `/{platform_name}/watchlists` | Get watchlists | `list[WatchlistResponse]` |
| GET | `/{platform_name}/watchlists/{watchlist_name}/instruments` | Get watchlist instruments | `list` |
| GET | `/{platform_name}/setup` | Get setup instructions | `SetupInstructionsResponse` |
| GET | `/kite/login` | Kite OAuth login | Redirect |
| GET | `/kite/callback` | Kite OAuth callback | `dict` |
| GET | `/kite/status` | Kite connection status | `dict` |
| GET | `/kite/holdings` | Get holdings | `dict` |
| GET | `/kite/positions` | Get positions | `dict` |
| GET | `/kite/profile` | Get profile | `dict` |

### Source References
- `GET /` - platforms.py:111
- `GET /{platform_name}` - platforms.py:127
- `POST /connect` - platforms.py:145
- `POST /{platform_name}/disconnect` - platforms.py:188
- `GET /{platform_name}/health` - platforms.py:204
- `GET /{platform_name}/watchlists` - platforms.py:224
- `GET /{platform_name}/watchlists/{watchlist_name}/instruments` - platforms.py:270
- `GET /{platform_name}/setup` - platforms.py:315
- `GET /kite/login` - platforms.py:356
- `GET /kite/callback` - platforms.py:375
- `GET /kite/status` - platforms.py:464
- `GET /kite/holdings` - platforms.py:483
- `GET /kite/positions` - platforms.py:518
- `GET /kite/profile` - platforms.py:553

---

## 13. MARKET INTELLIGENCE API

**Router:** `market_intelligence_router`
**Prefix:** `/api/v1/market-intelligence`
**Tag:** Market Intelligence

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| POST | `/query` | Execute market query | `MarketQueryResponse` |

### Source References
- `POST /query` - market_intelligence.py:67

---

## 14. HEALTH ENDPOINT

**Location:** `api/app.py:165`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Application health check |

### Response Schema
```json
{
  "status": "healthy",
  "app": "CIA-SIE",
  "version": "1.0.0",
  "environment": "development|production",
  "security": {
    "webhook_auth_enabled": true,
    "cors_restricted": true,
    "rate_limiting": "enabled",
    "security_headers": "enabled"
  }
}
```

---

## ENDPOINT STATISTICS

| Method | Count |
|--------|-------|
| GET | 36 |
| POST | 14 |
| PATCH | 1 |
| DELETE | 5 |
| **TOTAL** | **56** |

---

**END OF API ENDPOINT REGISTRY**
