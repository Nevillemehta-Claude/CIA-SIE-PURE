# CIA-SIE ECOSYSTEM — LAUNCH CENTER

## Quick Reference

All actionable commands are in this folder. **Double-click any `.command` file to execute.**

---

## 🚀 STARTUP SEQUENCE (Correct Order)

### First Time Ever? Run This First:
```
0_FIRST_TIME_SETUP.command
```
This installs dependencies and configures the environment.

### Regular Startup:
```
1_START_COMPOSITE_SYSTEM.command
```
This starts BOTH backend and frontend together.

---

## 📋 AVAILABLE COMMANDS

| File | Purpose | When to Use |
|------|---------|-------------|
| `0_FIRST_TIME_SETUP.command` | Install dependencies, create venv | **Once** on first use |
| `1_START_COMPOSITE_SYSTEM.command` | Start BOTH backend + frontend | **Normal operation** |
| `2_STOP_COMPOSITE_SYSTEM.command` | Stop ALL services | When done using |
| `3_START_BACKEND_ONLY.command` | Start only CIA-SIE-Pure | API development |
| `4_START_FRONTEND_ONLY.command` | Start only Mercury | Frontend testing |
| `5_SYSTEM_STATUS_CHECK.command` | Check what's running | Troubleshooting |

---

## 🔗 COMPONENT INDEPENDENCE

### What Can Run Independently?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COMPONENT INDEPENDENCE MATRIX                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   CIA-SIE-Pure (Backend)                                                    │
│   ├── CAN run alone: ✅ YES                                                 │
│   ├── Provides: REST API, Database, AI Narratives                           │
│   ├── Port: 8000                                                            │
│   └── Dependencies: None (self-contained)                                   │
│                                                                             │
│   Mercury (Frontend)                                                        │
│   ├── CAN run alone: ✅ YES (partial functionality)                         │
│   ├── Provides: Chat interface, Kite data, Claude AI                        │
│   ├── Port: 8001                                                            │
│   └── When alone:                                                           │
│       ├── ✅ Kite Connect market data: WORKS                                │
│       ├── ✅ Claude AI chat: WORKS                                          │
│       └── ❌ Backend API calls: FAILS (needs backend)                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Will One Block the Other?

**NO.** They run on different ports and are completely independent:

| Component | Port | Blocks Other? |
|-----------|------|---------------|
| CIA-SIE-Pure | 8000 | ❌ No |
| Mercury | 8001 | ❌ No |

You can:
- Run backend only ✅
- Run frontend only ✅
- Run both together ✅
- Stop one while other runs ✅

---

## 🔧 PREREQUISITES

Before using the system, ensure you have:

1. **Python 3.8+** installed
2. **API Keys** configured in `.env`:
   - `ANTHROPIC_API_KEY` — For AI chat (required for Claude features)
   - `KITE_API_KEY` — For market data (optional)
   - `KITE_API_SECRET` — For Kite authentication (optional)

---

## 📍 ACCESS POINTS

Once running:

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Frontend Chat | http://localhost:8001 | Mercury interface |
| Health Check | http://localhost:8000/health | Backend status |

---

## 🛑 TROUBLESHOOTING

### Port Already in Use?
Run `5_SYSTEM_STATUS_CHECK.command` to see what's using the ports, then run `2_STOP_COMPOSITE_SYSTEM.command`.

### Dependencies Missing?
Run `0_FIRST_TIME_SETUP.command` again.

### Can't Start?
1. Check `.env` file exists with API keys
2. Ensure virtual environment is activated
3. Check Python version: `python3 --version`

---

## 📁 FOLDER STRUCTURE

```
LAUNCH/
├── 0_FIRST_TIME_SETUP.command      ← Run once
├── 1_START_COMPOSITE_SYSTEM.command ← Main launcher
├── 2_STOP_COMPOSITE_SYSTEM.command  ← Main stopper
├── 3_START_BACKEND_ONLY.command     ← Backend only
├── 4_START_FRONTEND_ONLY.command    ← Frontend only
├── 5_SYSTEM_STATUS_CHECK.command    ← Status check
└── README.md                        ← This file
```

---

*CIA-SIE Ecosystem Launch Center | January 2026*
