# CIA-SIE-PURE + MERCURY
## USER MANUAL
### Composite System Operations Guide

**Version:** 1.0.0
**Date:** January 2026
**Classification:** Operational Documentation

---

## TABLE OF CONTENTS

1. [Quick Start Guide](#1-quick-start-guide)
2. [System Overview](#2-system-overview)
3. [Starting the System](#3-starting-the-system)
4. [Using Mercury (AI Chat Interface)](#4-using-mercury-ai-chat-interface)
5. [Using CIA-SIE (Backend API)](#5-using-cia-sie-backend-api)
6. [Stopping the System](#6-stopping-the-system)
7. [Troubleshooting](#7-troubleshooting)
8. [Quick Reference Card](#8-quick-reference-card)

---

## 1. QUICK START GUIDE

### Get Running in 3 Steps

**Step 1: Open Terminal**
```
Open Terminal application on your Mac
```

**Step 2: Start Mercury**
```bash
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury
source ../../venv/bin/activate
python -m mercury --web
```

**Step 3: Use the System**
```
Your browser will open automatically to:
http://localhost:8888

Start typing your questions in the chat box.
```

**That's it.** Mercury is now operational.

---

## 2. SYSTEM OVERVIEW

### What Is This System?

This is a **composite financial market intelligence platform** consisting of two integrated components:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    YOUR COMPOSITE SYSTEM                        │
│                                                                 │
│   ┌─────────────────────┐      ┌─────────────────────┐         │
│   │                     │      │                     │         │
│   │      MERCURY        │      │      CIA-SIE        │         │
│   │                     │      │                     │         │
│   │  AI Chat Interface  │      │   Backend Engine    │         │
│   │  for Market Data    │      │   Signal Storage    │         │
│   │                     │      │                     │         │
│   │  "Ask me anything   │      │  "I track and       │         │
│   │   about markets"    │      │   store signals"    │         │
│   │                     │      │                     │         │
│   └─────────────────────┘      └─────────────────────┘         │
│                                                                 │
│   Port: 8888                   Port: 8000                      │
│   Interface: Web Chat          Interface: API/Swagger          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Mercury — Your AI Financial Assistant

**What it does:**
- Answers questions about stocks, markets, and trading
- Fetches real-time market data from Kite API
- Provides AI-powered analysis using Claude
- Remembers conversation context for follow-up questions

**Example questions you can ask:**
- "What is RELIANCE trading at?"
- "Show me INFY's 52-week high"
- "Compare TCS and WIPRO"
- "What are my current positions?"
- "Analyze NIFTY trend"

### CIA-SIE — Your Signal Intelligence Engine

**What it does:**
- Stores signals from TradingView webhooks
- Tracks contradictions between different chart timeframes
- Tracks confirmations when signals align
- Provides structured API access to all data

---

## 3. STARTING THE SYSTEM

### Option A: Start Mercury Only (Recommended for Chat)

This is the simplest way to use the AI chat interface.

**Step 1: Open Terminal**

**Step 2: Navigate and Activate**
```bash
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury
source ../../venv/bin/activate
```

**Step 3: Launch Web Interface**
```bash
python -m mercury --web
```

**What You'll See:**
```
═══════════════════════════════════════════════════
 MERCURY LAUNCH READINESS CHECK
═══════════════════════════════════════════════════

 Kite Connect     ✅ AUTHENTICATED (234ms)
 Anthropic Claude ✅ AUTHENTICATED (567ms)

 Status: READY FOR LAUNCH
═══════════════════════════════════════════════════

Starting Mercury Web Interface...
Server running at: http://localhost:8888
```

**Your browser will open automatically.**

---

### Option B: Start Using Double-Click

**For Mercury:**
1. Open Finder
2. Navigate to: `/Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury/`
3. Double-click: `start-mercury.command`

**For CIA-SIE:**
1. Open Finder
2. Navigate to: `/Users/nevillemehta/Downloads/CIA-SIE-PURE/`
3. Double-click: `start-cia-sie.command`

---

### Option C: Start Both Systems Together

If you need both Mercury chat AND CIA-SIE backend:

**Terminal 1 — CIA-SIE:**
```bash
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE
./start-cia-sie.command
```

**Terminal 2 — Mercury:**
```bash
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury
source ../../venv/bin/activate
python -m mercury --web
```

---

### Option D: Check System Without Starting

To verify API connections without launching the full interface:

```bash
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury
source ../../venv/bin/activate
python -m mercury --check
```

**Output shows connection status only, then exits.**

---

## 4. USING MERCURY (AI CHAT INTERFACE)

### The Mercury Web Interface

When you open `http://localhost:8888`, you'll see:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                         MERCURY                                 │
│              Financial Market Intelligence                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  [Kite: ✅ Connected]  [Claude: ✅ Connected]          │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │                    CHAT AREA                            │   │
│  │                                                         │   │
│  │  Your conversations appear here                         │   │
│  │                                                         │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Type your question here...                      [Send] │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Suggestions:                                                   │
│  [What is NIFTY at?] [Show my positions] [Analyze RELIANCE]    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Status Indicators

| Indicator | Meaning |
|-----------|---------|
| ✅ Connected | API is working and authenticated |
| ⚠️ Degraded | API partially working (limited functionality) |
| ❌ Disconnected | API unavailable (check configuration) |

### How to Chat

1. **Type your question** in the text box at the bottom
2. **Press Enter** or click **Send**
3. **Wait** for the AI response (typically 2-4 seconds)
4. **Ask follow-up questions** — Mercury remembers context

### Example Conversation

```
You: What is RELIANCE trading at?

Mercury: RELIANCE (NSE:RELIANCE) is currently trading at ₹2,450.50, 
up 1.2% (+₹29.05) from yesterday's close. 

Today's range: ₹2,425.00 - ₹2,468.75
Volume: 3.2M shares traded

You: What about its 52-week high?

Mercury: RELIANCE's 52-week high is ₹2,856.15, reached on 
September 15, 2025. The current price of ₹2,450.50 is 
14.2% below this peak.

52-week low: ₹2,180.00 (January 2025)
Current position in range: 66.7%

You: Compare it to TCS

Mercury: Comparing RELIANCE and TCS:

| Metric          | RELIANCE    | TCS         |
|-----------------|-------------|-------------|
| Current Price   | ₹2,450.50   | ₹3,890.25   |
| Day Change      | +1.2%       | +0.8%       |
| 52W High        | ₹2,856.15   | ₹4,250.00   |
| 52W Low         | ₹2,180.00   | ₹3,420.00   |
| From 52W High   | -14.2%      | -8.5%       |

TCS is closer to its 52-week high compared to RELIANCE.
```

### What You Can Ask

| Category | Example Questions |
|----------|-------------------|
| **Price Checks** | "What is INFY at?", "NIFTY current price" |
| **Comparisons** | "Compare TCS and WIPRO", "HDFC vs ICICI" |
| **Analysis** | "Analyze RELIANCE", "What's happening with NIFTY?" |
| **Historical** | "52-week high of SBIN", "TATAMOTORS yearly range" |
| **Portfolio** | "Show my positions", "What am I holding?" |
| **General** | "Market overview", "Sector performance" |

### Suggestion Chips

Click the **suggestion buttons** below the chat for quick queries:
- These provide pre-formatted questions
- Good for discovering what Mercury can do
- Click any chip to send that query

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Shift+Enter` | New line (multi-line input) |
| `Ctrl+L` | Clear chat history |

---

## 5. USING CIA-SIE (BACKEND API)

### When to Use CIA-SIE

Use CIA-SIE when you need:
- Access to stored signals from TradingView
- Contradiction and confirmation tracking
- Raw API access for integration
- Swagger documentation for development

### Accessing CIA-SIE

**URL:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

### Available Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Check system health |
| `GET /api/instruments` | List all tracked instruments |
| `GET /api/signals` | View incoming signals |
| `GET /api/relationships` | See contradictions & confirmations |
| `GET /api/baskets` | View instrument baskets |
| `POST /webhook/tradingview/{chart_id}` | Receive TradingView alerts |

### Using Swagger UI

1. Open `http://localhost:8000/docs`
2. Click on any endpoint to expand it
3. Click **"Try it out"**
4. Fill in parameters (if any)
5. Click **"Execute"**
6. View the response

### Example API Call

**Check Health:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-13T10:30:00Z",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 6. STOPPING THE SYSTEM

### Stopping Mercury

**Method 1: Keyboard**
- In the terminal where Mercury is running
- Press `Ctrl+C`

**Method 2: Close Terminal**
- Simply close the terminal window

### Stopping CIA-SIE

**Method 1: Use Stop Command**
```bash
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE
./stop-cia-sie.command
```

**Method 2: Keyboard**
- Press `Ctrl+C` in the terminal

### Emergency Stop (All Systems)

If something is stuck:

```bash
# Kill all related processes
pkill -f "uvicorn"
pkill -f "python.*mercury"

# Verify ports are free
lsof -i :8000
lsof -i :8888
# (Should show no output)
```

---

## 7. TROUBLESHOOTING

### Common Issues and Solutions

---

#### Issue: "Port already in use"

**Symptom:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find what's using the port
lsof -i :8888

# Kill it
kill -9 <PID>

# Or kill all uvicorn processes
pkill -f uvicorn
```

---

#### Issue: "Kite: FAILED" at startup

**Symptom:**
```
Kite Connect ❌ FAILED
Message: Access token expired
```

**Solutions:**

1. **If using live Kite API:**
   - Your access token has expired
   - Log in to Kite and get a new token
   - Update `KITE_ACCESS_TOKEN` in `.env`

2. **If you want to use mock mode:**
   - Edit `projects/mercury/.env`
   - Set `KITE_MOCK_MODE=true`
   - Restart Mercury

---

#### Issue: "Anthropic: FAILED" at startup

**Symptom:**
```
Anthropic Claude ❌ FAILED
Message: API key invalid
```

**Solution:**
1. Check your API key at `console.anthropic.com`
2. Update `ANTHROPIC_API_KEY` in `projects/mercury/.env`
3. Restart Mercury

---

#### Issue: Browser doesn't open automatically

**Solution:**
Manually open: `http://localhost:8888`

---

#### Issue: Chat shows "Connecting..." indefinitely

**Solutions:**
1. Check if server is running (look at terminal)
2. Try refreshing the browser page
3. Check browser console for errors (F12)

---

#### Issue: AI responses are slow

**Possible causes:**
- Anthropic API under high load
- Network latency
- Complex query requiring more processing

**This is normal.** Wait for 5-10 seconds.

---

#### Issue: "Module not found" error

**Solution:**
```bash
# Make sure you're in the right directory
cd /Users/nevillemehta/Downloads/CIA-SIE-PURE/projects/mercury

# Make sure virtual environment is activated
source ../../venv/bin/activate

# Verify activation
which python
# Should show: .../CIA-SIE-PURE/venv/bin/python
```

---

### Getting Help

If issues persist:

1. **Check the logs:**
   ```bash
   cat /Users/nevillemehta/Downloads/CIA-SIE-PURE/logs/backend.log
   ```

2. **Run diagnostic check:**
   ```bash
   python -m mercury --check
   ```

3. **Verify configuration:**
   ```bash
   cat projects/mercury/.env
   # (Check API keys are set correctly)
   ```

---

## 8. QUICK REFERENCE CARD

### Essential Commands

| Action | Command |
|--------|---------|
| **Start Mercury (Web)** | `python -m mercury --web` |
| **Start Mercury (Terminal)** | `python -m mercury` |
| **Check APIs Only** | `python -m mercury --check` |
| **Start CIA-SIE** | `./start-cia-sie.command` |
| **Stop CIA-SIE** | `./stop-cia-sie.command` |
| **Stop Any Server** | `Ctrl+C` |

### URLs

| System | URL |
|--------|-----|
| Mercury Web Chat | `http://localhost:8888` |
| CIA-SIE API Docs | `http://localhost:8000/docs` |
| CIA-SIE Health | `http://localhost:8000/health` |
| Mercury Health | `http://localhost:8888/health` |
| Mercury Status | `http://localhost:8888/status` |

### File Locations

| File | Purpose |
|------|---------|
| `projects/mercury/.env` | Mercury configuration |
| `logs/backend.log` | CIA-SIE logs |
| `data/cia_sie.db` | Signal database |
| `start-cia-sie.command` | Launch CIA-SIE |
| `stop-cia-sie.command` | Stop CIA-SIE |
| `projects/mercury/start-mercury.command` | Launch Mercury |

### Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Connected / Working |
| ⚠️ | Degraded / Warning |
| ❌ | Failed / Error |
| 🔄 | Connecting / Loading |

---

## END OF USER MANUAL

---

**Document Version:** 1.0.0
**Last Updated:** January 2026
**Applicable To:** CIA-SIE-PURE + Mercury Composite System

---

*For technical architecture details, see the Aerospace Systems Manual.*
*For development documentation, see the /documentation folder.*
