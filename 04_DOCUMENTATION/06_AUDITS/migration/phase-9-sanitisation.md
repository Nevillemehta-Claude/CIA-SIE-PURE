# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 9: SANITISATION — LEGACY CLEANUP PLAN
# ═══════════════════════════════════════════════════════════════════════════════
# CEAD v2.0 | Forensic Codebase Restructuring
# Generated: January 13, 2026 12:20 IST
# ═══════════════════════════════════════════════════════════════════════════════

## SANITISATION STATUS

**CURRENT STATUS:** ✅ COMPLETE

Executed: January 13, 2026 12:18 IST
Method: Option B — Backup branch created, then sanitisation executed
Backup Branch: `backup-pre-sanitisation-20260113`

---

## LEGACY FILES IDENTIFIED FOR REMOVAL

The following files/directories at the repository root are now **duplicated** 
in their new domain locations and are candidates for removal:

### Category 1: Source Code (Now in CIA-SIE-Pure)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/src/` | `/CIA-SIE-Pure/src/` | DELETE |
| `/tests/` | `/CIA-SIE-Pure/tests/` | DELETE |
| `/alembic/` | `/CIA-SIE-Pure/alembic/` | DELETE |
| `/documentation/` | `/CIA-SIE-Pure/docs/` | DELETE |
| `/data/` | `/CIA-SIE-Pure/data/` | DELETE |
| `/docs/` | `/CIA-SIE-Pure/docs/` | DELETE |
| `/chat_history_export/` | `/CIA-SIE-Pure/docs/chat_history_export/` | DELETE |

### Category 2: Scripts (Now in CIA-SIE-Pure or Command-Control)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/scripts/` | `/CIA-SIE-Pure/scripts/` + `/Command-Control/scripts/` | DELETE |
| `/execute_all_tests_autonomous.py` | `/CIA-SIE-Pure/scripts/` | DELETE |
| `/extract_chat_history.py` | `/CIA-SIE-Pure/scripts/` | DELETE |
| `/generate_chronicle.py` | `/CIA-SIE-Pure/scripts/` | DELETE |
| `/run_comprehensive_tests.py` | `/CIA-SIE-Pure/scripts/` | DELETE |
| `/run_quick_tests.py` | `/CIA-SIE-Pure/scripts/` | DELETE |
| `/seed_sample_data.py` | `/CIA-SIE-Pure/scripts/` | DELETE |

### Category 3: Launchers (Now in Command-Control)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/start-cia-sie.command` | `/Command-Control/scripts/macos/` | DELETE |
| `/stop-cia-sie.command` | `/Command-Control/scripts/macos/` | DELETE |

### Category 4: Config (Now in CIA-SIE-Pure)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/alembic.ini` | `/CIA-SIE-Pure/alembic.ini` | DELETE |
| `/pyproject.toml` | `/CIA-SIE-Pure/pyproject.toml` | DELETE |

### Category 5: Mercury (Now in Mercury)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/projects/mercury/` | `/Mercury/` | DELETE |

### Category 6: Logs (Now in Quarantine)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/logs/` | `/quarantine/debug-logs/` | DELETE |

### Category 7: Duplicates (Now in Quarantine)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/Duplicates for Deletion/` | `/quarantine/duplicates/` | DELETE |

### Category 8: Engagement Documents (Now in Migration Logs)

| Original Location | New Location | Action |
|-------------------|--------------|--------|
| `/CEAD-v2.0-*.md` | `/migration-logs/` | DELETE |
| `/CURSOR-ENGAGEMENT-*.md` | `/migration-logs/` | DELETE |

### Category 9: Runtime Artifacts

| Location | Reason | Action |
|----------|--------|--------|
| `/pids/` | Empty runtime directory | DELETE |
| `/context/` | Empty placeholder | DELETE |
| `/prompts/` | Empty placeholder | DELETE |
| `/venv/` | Virtual environment (regenerable) | PRESERVE* |

*Note: venv should be preserved as it contains installed dependencies.

### Category 10: Other Files

| Location | Assessment | Action |
|----------|------------|--------|
| `/README.md` | Superseded by MASTER-README.md | DELETE |
| `/CIA-SIE-PURE.code-workspace` | Copied to quarantine | DELETE |

---

## FILES TO PRESERVE AT ROOT

| File/Directory | Reason |
|----------------|--------|
| `/CIA-SIE-Pure/` | Primary domain |
| `/Mercury/` | Frontend domain |
| `/Command-Control/` | Operations domain |
| `/shared/` | Cross-project resources |
| `/quarantine/` | Isolated items |
| `/migration-logs/` | Audit trail |
| `/MASTER-README.md` | New primary README |
| `/ARCHITECTURE-OVERVIEW.md` | Architecture documentation |
| `/MIGRATION-REPORT.md` | Migration audit |
| `/.git/` | Version control (DO NOT TOUCH) |
| `/.gitignore` | Git configuration |
| `/venv/` | Virtual environment |

---

## DELETION COMMAND SCRIPT

If approved, the following commands will remove legacy files:

```bash
#!/bin/bash
# CEAD v2.0 Phase 9 Sanitisation Script
# EXECUTE ONLY AFTER APPROVAL

cd /Users/nevillemehta/Downloads/CIA-SIE-PURE

# Category 1: Source Code
rm -rf src/
rm -rf tests/
rm -rf alembic/
rm -rf documentation/
rm -rf data/
rm -rf docs/
rm -rf chat_history_export/

# Category 2: Scripts
rm -rf scripts/
rm -f execute_all_tests_autonomous.py
rm -f extract_chat_history.py
rm -f generate_chronicle.py
rm -f run_comprehensive_tests.py
rm -f run_quick_tests.py
rm -f seed_sample_data.py

# Category 3: Launchers
rm -f start-cia-sie.command
rm -f stop-cia-sie.command

# Category 4: Config
rm -f alembic.ini
rm -f pyproject.toml

# Category 5: Mercury
rm -rf projects/

# Category 6: Logs
rm -rf logs/

# Category 7: Duplicates
rm -rf "Duplicates for Deletion/"

# Category 8: Engagement Documents
rm -f CEAD-v2.0-*.md
rm -f CURSOR-ENGAGEMENT-*.md

# Category 9: Runtime Artifacts
rm -rf pids/
rm -rf context/
rm -rf prompts/

# Category 10: Other Files
rm -f README.md
rm -f CIA-SIE-PURE.code-workspace

echo "✅ Sanitisation complete"
```

---

## PRE-DELETION CHECKLIST

Before executing sanitisation, confirm:

| # | Check | Status |
|---|-------|--------|
| 1 | All files copied to new locations | ✅ VERIFIED |
| 2 | Hash verification passed | ✅ VERIFIED |
| 3 | Git commit made before deletion | ⏳ PENDING |
| 4 | User has approved deletion | ⏳ PENDING |

---

## EXECUTION RECORD

### User Approval
- **Option Selected:** B — APPROVE WITH BACKUP
- **Approval Time:** January 13, 2026 12:17 IST

### Backup Branch Created
- **Branch Name:** `backup-pre-sanitisation-20260113`
- **Commit:** `5594980` — Pre-sanitisation checkpoint

### Sanitisation Executed
- **All legacy files removed** from repository root
- **Commit:** `26188ef` — Clean sovereign domain structure

---

## PHASE 9 STATUS

```
═══════════════════════════════════════════════════════════════════════════════
                    PHASE 9: SANITISATION — COMPLETE
═══════════════════════════════════════════════════════════════════════════════

STATUS: ✅ COMPLETE

ITEMS REMOVED:
├── Source directories:     7 ✓
├── Script files:           8 ✓
├── Launcher files:         2 ✓
├── Config files:           2 ✓
├── Mercury project:        1 directory ✓
├── Log directories:        1 ✓
├── Duplicate directories:  1 ✓
├── Engagement docs:        2 ✓
├── Runtime artifacts:      3 ✓
└── Other files:            2 ✓

TOTAL ITEMS REMOVED: ~29 files/directories

PRESERVED AT ROOT:
├── CIA-SIE-Pure/          ✅ 463 files
├── Mercury/               ✅ 57 files
├── Command-Control/       ✅ 7 files
├── shared/                ✅ (empty, ready for future)
├── quarantine/            ✅ 22 files
├── migration-logs/        ✅ 9 phase logs
├── MASTER-README.md       ✅
├── ARCHITECTURE-OVERVIEW.md ✅
├── MIGRATION-REPORT.md    ✅
├── .git/                  ✅
├── .gitignore             ✅
└── venv/                  ✅

BACKUP BRANCH: backup-pre-sanitisation-20260113

═══════════════════════════════════════════════════════════════════════════════
```

---

*Generated per CEAD v2.0 Section 9 Phase 9 | January 13, 2026*
