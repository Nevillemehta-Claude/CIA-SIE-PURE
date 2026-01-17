# CLAUDE CODE EXECUTION COMMANDS

**Purpose:** Terminal commands for forensic audit execution
**Environment:** Claude Code with bash access

---

## PHASE 1: FILE INVENTORY

### 1.1 Count All Source Files
```bash
find src/cia_sie -name "*.py" | wc -l
```

### 1.2 List All Source Files with Line Counts
```bash
find src/cia_sie -name "*.py" -exec wc -l {} \; | sort -n
```

### 1.3 Generate Source File Inventory
```bash
find src/cia_sie -name "*.py" -exec echo "FILE: {}" \; -exec wc -l {} \; -exec head -5 {} \;
```

### 1.4 List All Test Files
```bash
find tests -name "*.py" | wc -l
find tests -name "test_*.py" -o -name "*_test.py"
```

---

## PHASE 2: CONSTITUTIONAL COMPLIANCE CHECKS

### 2.1 Search for PROHIBITED Database Columns
```bash
# These should return ZERO matches
echo "=== Checking for 'weight' column ==="
grep -rn "weight" src/cia_sie/dal/models.py || echo "PASS: No weight column"

echo "=== Checking for 'score' column ==="
grep -rn "score" src/cia_sie/dal/models.py || echo "PASS: No score column"

echo "=== Checking for 'confidence' column ==="
grep -rn "confidence" src/cia_sie/dal/models.py || echo "PASS: No confidence column"

echo "=== Checking for 'recommendation' column ==="
grep -rn "recommendation" src/cia_sie/dal/models.py || echo "PASS: No recommendation column"

echo "=== Checking for 'priority' on signals ==="
grep -rn "priority" src/cia_sie/dal/models.py || echo "PASS: No priority column"

echo "=== Checking for 'rank' column ==="
grep -rn "rank" src/cia_sie/dal/models.py || echo "PASS: No rank column"
```

### 2.2 Search for PROHIBITED AI Response Patterns
```bash
echo "=== Checking AI prompts for prohibited patterns ==="
grep -rn "you should" src/cia_sie/ai/ || echo "PASS: No 'you should'"
grep -rn "I recommend" src/cia_sie/ai/ || echo "PASS: No 'I recommend'"
grep -rn "consider buying" src/cia_sie/ai/ || echo "PASS: No 'consider buying'"
grep -rn "overall direction" src/cia_sie/ai/ || echo "PASS: No 'overall direction'"
grep -rn "net signal" src/cia_sie/ai/ || echo "PASS: No 'net signal'"
grep -rn "consensus" src/cia_sie/ai/ || echo "PASS: No 'consensus'"
```

### 2.3 Verify Response Validator Exists
```bash
echo "=== Checking response validator ==="
cat src/cia_sie/ai/response_validator.py | head -100
```

### 2.4 Check for Aggregation Functions
```bash
echo "=== Checking for aggregation logic ==="
grep -rn "sum\|average\|mean\|aggregate" src/cia_sie/exposure/ || echo "PASS: No aggregation"
grep -rn "weighted" src/cia_sie/ || echo "PASS: No weighted calculations"
```

---

## PHASE 3: API ENDPOINT INVENTORY

### 3.1 Find All Route Definitions
```bash
echo "=== API Route Definitions ==="
grep -rn "@router\." src/cia_sie/api/routes/
```

### 3.2 List All Endpoint Methods
```bash
echo "=== GET Endpoints ==="
grep -rn "@router.get" src/cia_sie/api/routes/

echo "=== POST Endpoints ==="
grep -rn "@router.post" src/cia_sie/api/routes/

echo "=== PUT Endpoints ==="
grep -rn "@router.put" src/cia_sie/api/routes/

echo "=== DELETE Endpoints ==="
grep -rn "@router.delete" src/cia_sie/api/routes/
```

### 3.3 Extract Route Paths
```bash
grep -rho "@router\.\(get\|post\|put\|delete\)(\"[^\"]*\"" src/cia_sie/api/routes/ | sort | uniq
```

---

## PHASE 4: DATABASE SCHEMA AUDIT

### 4.1 List All SQLAlchemy Models
```bash
echo "=== Database Models ==="
grep -n "class.*Base" src/cia_sie/dal/models.py
```

### 4.2 Extract All Column Definitions
```bash
echo "=== Column Definitions ==="
grep -n "Column\|relationship\|ForeignKey" src/cia_sie/dal/models.py
```

### 4.3 Check Migration History
```bash
echo "=== Alembic Migrations ==="
ls -la alembic/versions/
cat alembic/versions/*.py | grep -A5 "def upgrade"
```

---

## PHASE 5: TEST COVERAGE ANALYSIS

### 5.1 Run Tests with Coverage
```bash
pytest tests/ --cov=src/cia_sie --cov-report=term-missing
```

### 5.2 Check Which Files Have No Tests
```bash
echo "=== Source files ==="
find src/cia_sie -name "*.py" | wc -l

echo "=== Test files ==="
find tests -name "test_*.py" | wc -l
```

### 5.3 List Untested Modules
```bash
# Compare source modules to test modules
echo "=== Source Modules ==="
find src/cia_sie -name "*.py" -not -name "__init__.py" | sed 's|src/cia_sie/||' | sort

echo "=== Test Modules ==="
find tests -name "test_*.py" | sed 's|tests/||;s|test_||;s|_test||' | sort
```

---

## PHASE 6: INTEGRATION VERIFICATION

### 6.1 Check Kite Integration
```bash
echo "=== Kite Platform Adapter ==="
cat src/cia_sie/platforms/kite.py | head -100
```

### 6.2 Check Claude AI Integration
```bash
echo "=== Claude Client ==="
cat src/cia_sie/ai/claude_client.py | head -100
```

### 6.3 Check Webhook Handler
```bash
echo "=== Webhook Handler ==="
cat src/cia_sie/ingestion/webhook_handler.py | head -100
```

---

## PHASE 7: DOCUMENTATION ANALYSIS

### 7.1 List All Markdown Documentation
```bash
find documentation -name "*.md" | wc -l
find documentation -name "*.md"
```

### 7.2 Read Architecture Flowcharts
```bash
cat documentation/02_ARCHITECTURE/BACKEND_FLOWCHARTS.md
```

### 7.3 Read Existing Audit Reports
```bash
ls documentation/06_AUDITS/
cat documentation/06_AUDITS/handoff_audit/PHASE_2_BACKEND_CODE_AUDIT.md
```

---

## PHASE 8: GAP DETECTION

### 8.1 Find TODO/FIXME Comments
```bash
grep -rn "TODO\|FIXME\|XXX\|HACK" src/cia_sie/
```

### 8.2 Find Empty Files
```bash
find src/cia_sie -name "*.py" -empty
```

### 8.3 Find Files with Only Imports (Stub Files)
```bash
for f in $(find src/cia_sie -name "*.py"); do
    lines=$(grep -v "^#\|^$\|^import\|^from" "$f" | wc -l)
    if [ "$lines" -lt 5 ]; then
        echo "STUB: $f ($lines lines of code)"
    fi
done
```

---

## QUICK FULL AUDIT SCRIPT

Run this single script for a complete audit:

```bash
#!/bin/bash
echo "========================================"
echo "CIA-SIE-PURE BACKEND FORENSIC AUDIT"
echo "========================================"
echo ""

echo "1. FILE INVENTORY"
echo "-----------------"
echo "Source files: $(find src/cia_sie -name '*.py' | wc -l)"
echo "Test files: $(find tests -name '*.py' | wc -l)"
echo "Doc files: $(find documentation -name '*.md' | wc -l)"
echo ""

echo "2. CONSTITUTIONAL COMPLIANCE"
echo "----------------------------"
echo "Checking for prohibited columns..."
grep -l "weight\|score\|confidence\|recommendation" src/cia_sie/dal/models.py && echo "VIOLATION FOUND!" || echo "PASS: No prohibited columns"
echo ""

echo "3. API ENDPOINTS"
echo "----------------"
echo "Total routes: $(grep -r '@router\.' src/cia_sie/api/routes/ | wc -l)"
echo "GET: $(grep -r '@router.get' src/cia_sie/api/routes/ | wc -l)"
echo "POST: $(grep -r '@router.post' src/cia_sie/api/routes/ | wc -l)"
echo "PUT: $(grep -r '@router.put' src/cia_sie/api/routes/ | wc -l)"
echo "DELETE: $(grep -r '@router.delete' src/cia_sie/api/routes/ | wc -l)"
echo ""

echo "4. DATABASE TABLES"
echo "------------------"
grep "class.*Base" src/cia_sie/dal/models.py
echo ""

echo "5. POTENTIAL ISSUES"
echo "-------------------"
echo "TODOs: $(grep -r 'TODO' src/cia_sie/ | wc -l)"
echo "FIXMEs: $(grep -r 'FIXME' src/cia_sie/ | wc -l)"
echo ""

echo "========================================"
echo "AUDIT COMPLETE"
echo "========================================"
```

---

## OUTPUT FORMAT

After running these commands, Claude Code should produce:

1. **FORENSIC_AUDIT_INVENTORY.md** - File counts and listings
2. **CONSTITUTIONAL_COMPLIANCE_MATRIX.md** - Pass/fail for each check
3. **API_ENDPOINT_REGISTRY.md** - All routes documented
4. **GAP_ANALYSIS_REPORT.md** - Issues found
5. **MASTER_BACKEND_FLOWCHART.md** - Synthesized architecture

---

**END OF EXECUTION COMMANDS**
