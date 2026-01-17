# CIA-SIE LAUNCHER SYSTEM - OPERATIONAL GUIDE

**Document ID:** OPS-LAUNCHER-001  
**Version:** 1.0.0  
**Date:** 12 January 2026  
**Audience:** End Users, Operators, Developers  

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Quick Start](#2-quick-start)
3. [Starting the System](#3-starting-the-system)
4. [Stopping the System](#4-stopping-the-system)
5. [System Status](#5-system-status)
6. [Troubleshooting](#6-troubleshooting)
7. [Configuration](#7-configuration)
8. [Maintenance](#8-maintenance)
9. [FAQ](#9-faq)

---

## 1. OVERVIEW

### 1.1 What is the Launcher System?

The CIA-SIE Launcher System provides a simple way to start and stop the CIA-SIE platform. Instead of running multiple commands in the terminal, you can:

- **Double-click `start-cia-sie.command`** to start everything
- **Double-click `stop-cia-sie.command`** to stop everything

### 1.2 What Gets Started?

| Service | Description | Port |
|---------|-------------|------|
| **Backend API** | FastAPI server handling all business logic | 8000 |
| **ngrok Tunnel** | Webhook receiver for TradingView alerts | Dynamic |
| **Frontend** | React web interface (when built) | 5173 |

### 1.3 Prerequisites

Before using the launcher, ensure:

- ✅ macOS 13 (Ventura) or later
- ✅ Python virtual environment exists (`venv/` folder)
- ✅ ngrok installed (`brew install ngrok` or download from ngrok.com)
- ✅ Ports 8000 and 5173 are available

---

## 2. QUICK START

### 2.1 Starting the System

1. Open Finder
2. Navigate to `CIA-SIE-PURE` folder
3. Double-click `start-cia-sie.command`
4. A terminal window opens showing progress
5. Browser opens automatically when ready

### 2.2 Stopping the System

1. Double-click `stop-cia-sie.command`
2. Or press `Ctrl+C` in the running terminal
3. Wait for "SHUTDOWN COMPLETE" message

### 2.3 That's It!

No commands to remember. No technical knowledge required.

---

## 3. STARTING THE SYSTEM

### 3.1 Step-by-Step

1. **Locate the start file:**
   - File: `start-cia-sie.command`
   - Location: Project root folder

2. **Double-click the file:**
   - A Terminal window opens
   - You'll see progress messages

3. **Watch the progress:**
   ```
   ╔═══════════════════════════════════════════════════════════════╗
   ║   🚀 CIA-SIE SYSTEM IGNITION                                 ║
   ╚═══════════════════════════════════════════════════════════════╝

   STEP 1/6: Verifying prerequisites...
            └── ✓ Prerequisites verified

   STEP 2/6: Activating Python environment...
            └── ✓ Python environment activated
   
   [... more steps ...]
   ```

4. **Wait for completion:**
   ```
   ╔═══════════════════════════════════════════════════════════════╗
   ║   ✅ CIA-SIE SYSTEM IGNITION COMPLETE                        ║
   ║                                                               ║
   ║   Backend:   🟢 RUNNING    http://localhost:8000             ║
   ║   Tunnel:    🟢 RUNNING    https://abc123.ngrok.io           ║
   ║   Frontend:  ⚪ NOT BUILT  (frontend not yet created)        ║
   ╚═══════════════════════════════════════════════════════════════╝
   ```

5. **Browser opens automatically** to the API documentation page

### 3.2 What Happens Behind the Scenes

1. Python virtual environment activates
2. Backend server starts on port 8000
3. Health check verifies backend is ready
4. ngrok tunnel establishes (for webhooks)
5. Frontend starts (if built)
6. Browser opens to application

### 3.3 Terminal Window

- **Keep this window open** while using the system
- The system stays running as long as the terminal is open
- Press `Ctrl+C` to stop everything gracefully

---

## 4. STOPPING THE SYSTEM

### 4.1 Option A: Stop Script (Recommended)

1. Double-click `stop-cia-sie.command`
2. Watch the shutdown progress:
   ```
   ╔═══════════════════════════════════════════════════════════════╗
   ║   🛑 CIA-SIE SYSTEM SHUTDOWN                                 ║
   ╚═══════════════════════════════════════════════════════════════╝

   STEP 1/4: Stopping Frontend...
            └── Not running

   STEP 2/4: Stopping Tunnel...
            └── ✓ Stopped

   STEP 3/4: Stopping Backend...
            └── ✓ Stopped

   STEP 4/4: Cleaning up...
            └── ✓ Cleanup complete
   ```

3. Press Enter to close the window

### 4.2 Option B: Ctrl+C

1. Go to the terminal window where you started the system
2. Press `Ctrl+C`
3. The system will shut down gracefully

### 4.3 What Gets Stopped

- Backend server process
- ngrok tunnel process
- Frontend server process (if running)
- All PID files are cleaned up

---

## 5. SYSTEM STATUS

### 5.1 Check If Backend Is Running

Open your browser to: **http://localhost:8000/health**

You should see:
```json
{
  "status": "healthy",
  "app": "CIA-SIE",
  "version": "2.3.0"
}
```

### 5.2 Check API Documentation

Open your browser to: **http://localhost:8000/docs**

This shows the Swagger UI with all available API endpoints.

### 5.3 Check ngrok Tunnel

1. Open: **http://localhost:4040**
2. This shows the ngrok dashboard
3. You can see your public URL and request logs

### 5.4 Check Log Files

| Log | Location | Purpose |
|-----|----------|---------|
| Launcher | `logs/launcher.log` | Start/stop operations |
| Backend | `logs/backend.log` | API server output |
| ngrok | `logs/ngrok.log` | Tunnel output |
| Application | `logs/cia_sie.log` | Application logs |

---

## 6. TROUBLESHOOTING

### 6.1 Error: Port 8000 Already in Use

**Symptom:**
```
❌ ERROR: E003 - Port Conflict
Port 8000 is already in use by another process.
```

**Solution:**
1. Find what's using the port:
   ```bash
   lsof -i :8000
   ```
2. Stop the conflicting process
3. Or stop all CIA-SIE processes:
   ```bash
   pkill -f "uvicorn.*cia_sie"
   ```
4. Run start again

### 6.2 Error: Virtual Environment Not Found

**Symptom:**
```
❌ ERROR: E002 - Prerequisites Not Met
Virtual environment not found
```

**Solution:**
1. Create the virtual environment:
   ```bash
   cd /path/to/CIA-SIE-PURE
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
2. Run start again

### 6.3 Error: Backend Not Healthy

**Symptom:**
```
❌ ERROR: E005 - Health Check Failed
The backend server started but did not become healthy.
```

**Solution:**
1. Check the backend log:
   ```bash
   tail -50 logs/backend.log
   ```
2. Look for Python errors
3. Ensure database exists: `data/cia_sie.db`
4. Run start again

### 6.4 ngrok Tunnel Not Working

**Symptom:** No public URL displayed

**Solution:**
1. Verify ngrok is installed:
   ```bash
   ngrok version
   ```
2. Check ngrok auth:
   ```bash
   ngrok config check
   ```
3. If not configured:
   ```bash
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

### 6.5 System Seems Stuck

**Solution:**
1. Press `Ctrl+C` to abort
2. Run the stop script to clean up
3. Check for orphan processes:
   ```bash
   pgrep -f "uvicorn.*cia_sie"
   pgrep -f "ngrok http"
   ```
4. Kill any orphans:
   ```bash
   pkill -f "uvicorn.*cia_sie"
   pkill -f "ngrok http"
   ```
5. Start again

---

## 7. CONFIGURATION

### 7.1 Environment Variables

Override default settings with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CIA_SIE_BACKEND_PORT` | 8000 | Backend server port |
| `CIA_SIE_FRONTEND_PORT` | 5173 | Frontend server port |
| `CIA_SIE_OPEN_BROWSER` | true | Auto-open browser |
| `CIA_SIE_START_NGROK` | true | Start ngrok tunnel |

**Example:**
```bash
export CIA_SIE_BACKEND_PORT=9000
./start-cia-sie.command
```

### 7.2 Disable Features

**Disable browser auto-open:**
```bash
export CIA_SIE_OPEN_BROWSER=false
```

**Disable ngrok:**
```bash
export CIA_SIE_START_NGROK=false
```

### 7.3 Configuration File Location

All configuration: `scripts/launcher/config.sh`

You can edit this file directly, but environment variables take precedence.

---

## 8. MAINTENANCE

### 8.1 Log File Management

Logs are written to the `logs/` directory. To clear old logs:

```bash
rm logs/launcher.log
rm logs/backend.log
rm logs/ngrok.log
```

### 8.2 PID File Cleanup

If the system didn't shut down cleanly, PID files may remain:

```bash
rm pids/*.pid
```

### 8.3 Updating the System

After pulling new code:

1. Stop the system (if running)
2. Activate venv and update:
   ```bash
   source venv/bin/activate
   pip install -e .
   ```
3. Start the system again

---

## 9. FAQ

### Q: Can I run multiple instances?

**A:** No. Only one instance of CIA-SIE should run at a time on the same ports.

### Q: Where is my data stored?

**A:** Database: `data/cia_sie.db` (SQLite)

### Q: How do I access the API?

**A:** 
- Local: http://localhost:8000
- External: Use the ngrok URL displayed at startup

### Q: What's the ngrok URL for?

**A:** It allows TradingView to send webhook alerts to your local machine.

### Q: The frontend says "NOT BUILT" - is that a problem?

**A:** No. The frontend is a future phase. The backend and API are fully operational.

### Q: How do I see API logs?

**A:** Check `logs/backend.log` or `logs/cia_sie.log`

### Q: Can I run this on Windows?

**A:** Not yet. Currently macOS only. Windows support is planned.

---

## QUICK REFERENCE CARD

| Action | Command |
|--------|---------|
| **Start system** | Double-click `start-cia-sie.command` |
| **Stop system** | Double-click `stop-cia-sie.command` |
| **Check health** | http://localhost:8000/health |
| **API docs** | http://localhost:8000/docs |
| **ngrok dashboard** | http://localhost:4040 |
| **View logs** | `tail -f logs/launcher.log` |
| **Emergency stop** | `pkill -f "uvicorn.*cia_sie"` |

---

**END OF OPERATIONAL GUIDE**
