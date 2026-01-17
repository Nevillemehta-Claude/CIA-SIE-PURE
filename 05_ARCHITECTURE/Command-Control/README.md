# Command-Control

## Overview

Command-Control is the **Operations CLI** for the CIA-SIE Trading Intelligence Platform. It provides all the scripts and commands needed to start, stop, restart, and monitor the system components.

## Technology Stack

- **Shell Scripts:** Bash (.sh)
- **macOS Launchers:** .command files (double-click to execute)
- **Python CLI:** Optional Python utilities

## Directory Structure

```
Command-Control/
├── scripts/
│   ├── macos/             # macOS .command launcher files
│   │   ├── start-cia-sie.command
│   │   ├── stop-cia-sie.command
│   │   ├── 0_FIRST_TIME_SETUP.command
│   │   ├── 1_START_COMPOSITE_SYSTEM.command
│   │   ├── 2_STOP_COMPOSITE_SYSTEM.command
│   │   ├── 3_START_BACKEND_ONLY.command
│   │   ├── 4_START_FRONTEND_ONLY.command
│   │   └── 5_SYSTEM_STATUS_CHECK.command
│   └── shell/             # Shell scripts
│       ├── config.sh
│       ├── health-check.sh
│       ├── ignite.sh
│       ├── shutdown.sh
│       └── utils.sh
├── docs/
│   ├── usage-guide/
│   └── command-reference/
├── config/
│   ├── cli-settings/
│   └── defaults/
└── tests/
    └── command-validation/
```

## Quick Start

### Starting the System

**Option 1: Composite System (Backend + Frontend)**
```bash
cd Command-Control/scripts/macos
./1_START_COMPOSITE_SYSTEM.command
```

**Option 2: Backend Only**
```bash
./3_START_BACKEND_ONLY.command
```

**Option 3: Frontend Only**
```bash
./4_START_FRONTEND_ONLY.command
```

### Stopping the System
```bash
cd Command-Control/scripts/macos
./2_STOP_COMPOSITE_SYSTEM.command
```

### System Status Check
```bash
./5_SYSTEM_STATUS_CHECK.command
```

### First-Time Setup
```bash
./0_FIRST_TIME_SETUP.command
```

## Command Reference

| Command | Purpose | File |
|---------|---------|------|
| Start All | Launch backend and frontend | `1_START_COMPOSITE_SYSTEM.command` |
| Stop All | Stop all running services | `2_STOP_COMPOSITE_SYSTEM.command` |
| Backend Only | Start CIA-SIE-Pure backend | `3_START_BACKEND_ONLY.command` |
| Frontend Only | Start Mercury frontend | `4_START_FRONTEND_ONLY.command` |
| Status Check | Check system health | `5_SYSTEM_STATUS_CHECK.command` |
| First Setup | Initial environment setup | `0_FIRST_TIME_SETUP.command` |

## Shell Scripts

Located in `scripts/shell/`:

- **config.sh** — Configuration loading and environment setup
- **health-check.sh** — System health verification
- **ignite.sh** — Service startup logic
- **shutdown.sh** — Graceful service shutdown
- **utils.sh** — Shared utility functions

## Usage on macOS

All `.command` files are designed to be double-clickable in Finder:

1. Navigate to `Command-Control/scripts/macos/`
2. Double-click the desired command
3. Terminal will open and execute the script

## Related Projects

- [CIA-SIE-Pure](../CIA-SIE-Pure/README.md) — Core backend engine
- [Mercury](../Mercury/README.md) — Frontend interface

## Documentation

- [Usage Guide](./docs/usage-guide/)
- [Command Reference](./docs/command-reference/)

---
*Part of the CIA-SIE Trading Intelligence Platform*
*Restructured per CEAD v2.0*
