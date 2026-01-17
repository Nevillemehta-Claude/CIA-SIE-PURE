# DOCUMENTATION PRINCIPLES
## Universal Laws of Technical Writing

**Module:** DOCUMENTATION
**Version:** 1.0

---

## THE DOCUMENTATION CREED

> "If it's not documented, it doesn't exist. If it's documented but wrong, it's worse than not existing."

Documentation is not an afterthought. It is a first-class artifact that enables understanding, maintenance, and evolution.

---

## THE SEVEN DOCUMENTATION PRINCIPLES

### PRINCIPLE 1: DOCUMENTATION IS A PRODUCT

**Statement:** Documentation deserves the same quality standards as code. It is not a byproduct of development - it IS development.

**Implications:**
- Documentation is planned, not improvised
- Documentation is reviewed, not just written
- Documentation has owners and maintainers
- Documentation has quality standards

---

### PRINCIPLE 2: ACCURACY OVER EXISTENCE

**Statement:** Wrong documentation is worse than no documentation. Documentation that misleads causes more harm than gaps.

**Corollary:** Every update to code must evaluate documentation impact. Stale documentation is a compliance violation.

**Rule:** If you cannot verify a document's accuracy, mark it as "UNVERIFIED" and schedule verification.

---

### PRINCIPLE 3: WRITE FOR THE READER

**Statement:** Documentation exists for the reader, not the writer. Write what they need to know, not what you want to say.

**Reader-centric questions:**
- What does the reader already know?
- What do they need to accomplish?
- What questions will they have?
- What mistakes might they make?

---

### PRINCIPLE 4: LIVE DOCUMENTATION

**Statement:** Documentation must stay synchronized with the system it describes. Contemporaneous updates, not retrospective documentation sprints.

**Living documentation practices:**
- Update docs with code changes
- Auto-generate where possible
- Review docs in code reviews
- Test docs like code

---

### PRINCIPLE 5: RIGHT LEVEL OF DETAIL

**Statement:** Too little detail leaves questions unanswered. Too much detail overwhelms and becomes stale. Match detail to purpose.

| Purpose | Detail Level |
|---------|--------------|
| Overview | High-level, conceptual |
| Tutorial | Step-by-step, detailed |
| Reference | Comprehensive, precise |
| Troubleshooting | Problem-solution pairs |

---

### PRINCIPLE 6: SINGLE SOURCE OF TRUTH

**Statement:** Information lives in ONE place. Other documents reference it. Duplication creates drift.

**SSOT examples:**
- API spec: OpenAPI file
- Data model: Schema definition
- Config options: Config file with comments
- Business rules: Specification document

---

### PRINCIPLE 7: DEFENSIVE DOCUMENTATION

**Statement:** Documentation anticipates problems. It documents not just how things work, but how they fail and how to recover.

**Defensive documentation includes:**
- Known limitations
- Error scenarios
- Troubleshooting guides
- Recovery procedures
- Security considerations

---

## WHAT TO DOCUMENT

### Always Document

| Item | Why |
|------|-----|
| Architecture | Understand system structure |
| APIs | Enable integration |
| Configuration | Enable operation |
| Decisions | Understand rationale |
| Runbooks | Enable operations |

### Document If Complex

| Item | When |
|------|------|
| Algorithms | Non-obvious logic |
| Business rules | Domain-specific behavior |
| Integrations | External dependencies |
| Security | Access control, encryption |

### Don't Document

| Item | Why |
|------|-----|
| Self-explanatory code | Code is documentation |
| Implementation details | Changes frequently |
| Obvious behavior | Wastes reader time |

---

## HOW TO WRITE

### Structure

```
1. Start with WHY (purpose)
2. Explain WHAT (overview)
3. Detail HOW (specifics)
4. Address WHEN things go wrong (troubleshooting)
```

### Style

| Do | Don't |
|----|-------|
| Use active voice | Use passive voice |
| Be concise | Be verbose |
| Use concrete examples | Use abstract descriptions |
| Use consistent terminology | Use synonyms randomly |
| Write complete sentences | Write fragments |

### Format

| Element | Use For |
|---------|---------|
| Headings | Navigation and structure |
| Lists | Multiple items |
| Tables | Comparisons, specs |
| Code blocks | Examples, commands |
| Diagrams | Architecture, flow |

---

## DOCUMENTATION QUALITY CHECKLIST

Before publishing any documentation:

- [ ] **Accurate:** Verified against current system
- [ ] **Complete:** Covers what reader needs
- [ ] **Clear:** Understandable without prior knowledge
- [ ] **Consistent:** Terminology and format match conventions
- [ ] **Current:** Reflects latest version
- [ ] **Findable:** Discoverable in documentation system

---

## DOCUMENTATION DEBT

Like technical debt, documentation debt accumulates when documentation is deferred or neglected.

**Signs of documentation debt:**
- "The docs are out of date"
- "Ask Bob, he knows how it works"
- "We'll document it later"
- Onboarding takes weeks
- Same questions asked repeatedly

**Managing documentation debt:**
- Track as part of backlog
- Allocate time each sprint
- Update docs with code changes
- Treat doc bugs like code bugs

---

## METRICS

| Metric | What It Measures |
|--------|------------------|
| Coverage | % of APIs/components documented |
| Freshness | Time since last update |
| Accuracy | % of docs verified current |
| Findability | Can readers find what they need |
| Usefulness | Does it answer questions |

---

*PRINCIPLES v1.0 | DOCUMENTATION | BIBLE_MODULES*
