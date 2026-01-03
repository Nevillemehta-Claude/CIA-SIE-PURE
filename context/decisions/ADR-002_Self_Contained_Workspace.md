# ADR-002: Self-Contained Workspace Architecture

## Status
ACCEPTED

## Date
27 December 2025

## Context
The application needed a deployment strategy that would:
- Enable easy startup/shutdown
- Be portable and self-contained
- Not depend on global system installations
- Allow for easy backup and restoration

## Decision
We chose a **Self-Contained Workspace** architecture where all components reside within a single directory:

```
CIA_SIE_WORKSPACE/
├── src/              # Backend source code
├── frontend/         # Frontend source + node_modules
├── venv/             # Python virtual environment
├── data/             # SQLite database
├── logs/             # Application logs
├── start.sh          # Startup script
├── stop.sh           # Shutdown script
└── status.sh         # Status checker
```

## Rationale
- **Portability**: Entire application can be moved by copying one folder
- **Isolation**: No conflicts with other Python/Node projects
- **Simplicity**: Single location for all files
- **Backup-Friendly**: One folder to backup captures everything
- **Version Control**: Entire application can be version-controlled

## Consequences
### Positive
- Easy backup and restoration
- No dependency on global installations
- Clear boundaries of what constitutes "the application"
- Simple deployment (copy folder, run script)

### Negative
- Larger disk footprint (includes venv and node_modules)
- Updates to dependencies require updates within workspace

## Implementation
- All scripts use `PROJECT_DIR="/Users/nevillemehta/Documents/CIA_SIE_WORKSPACE"`
- Virtual environment at `$PROJECT_DIR/venv/`
- Node modules at `$PROJECT_DIR/frontend/node_modules/`
- Database at `$PROJECT_DIR/data/cia_sie.db`
