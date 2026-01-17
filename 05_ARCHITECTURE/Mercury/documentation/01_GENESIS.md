# PROJECT MERCURY: GENESIS DOCUMENT

**Document ID**: MERCURY-GEN-001  
**Version**: 1.0.0  
**Classification**: FOUNDATION  
**Date**: 2026-01-13  

---

## STAGE I: GENESIS
> *"Every system begins with a vision that must be articulated before it can be built."*

---

## 1. PROJECT IDENTITY

| Attribute | Value |
|-----------|-------|
| **Project Name** | Mercury |
| **Codename** | The Messenger of the Gods |
| **Type** | LLM-as-Financial-Market-Cognitive-Interface |
| **Parent Project** | CIA-SIE-PURE (Independent Module) |

---

## 2. PROBLEM STATEMENT

### The Problem (Explicit, Unambiguous)

A trader requires **real-time, contextual, synthesized market intelligence** delivered through natural language conversation. Current solutions force the user to:

1. **Manually query** multiple data sources (broker platforms, charting tools, news feeds)
2. **Mentally synthesize** disparate data points into actionable understanding
3. **Navigate restrictive interfaces** that prevent direct answers
4. **Accept fragmented information** instead of holistic insights

### The Gap

No existing system provides:
- **Direct conversational access** to live market data
- **AI-powered synthesis** of market conditions into plain-English insights
- **Unrestricted cognitive assistance** that can express conviction, synthesize contradictions, and provide actionable guidance
- **Real-time grounding** of AI responses in actual market data

---

## 3. USER IDENTIFICATION

### Primary User: The Active Trader

| Attribute | Description |
|-----------|-------------|
| **Role** | Active trader managing personal portfolio |
| **Instruments** | 50+ instruments across equities, ETFs, commodities |
| **Frequency** | Multiple queries per trading session |
| **Need** | Rapid, accurate, synthesized market intelligence |
| **Technical Skill** | Comfortable with trading platforms, not a developer |

### User Persona: "The Informed Decider"

> *"I want to ask questions in plain English and get answers that help me understand what's happening in the market. I don't want hedged, disclaimer-laden responses. I want direct insights grounded in real data. I make the final decision, but I want an intelligent assistant that can actually assist."*

---

## 4. CORE PHILOSOPHY

### The Single Statement

> **"Mercury is an unrestricted cognitive interface that connects live market data to AI intelligence, providing direct, synthesized, actionable market insights through natural conversation."**

### Philosophy Elaboration

| Principle | Meaning |
|-----------|---------|
| **Unrestricted** | No artificial constraints on what the AI can express |
| **Cognitive Interface** | The AI thinks with you, not just reports to you |
| **Live Market Data** | Every response grounded in real, current data |
| **Direct Insights** | No hedging, no mandatory disclaimers, no artificial neutrality |
| **Natural Conversation** | Ask in plain English, receive in plain English |

---

## 5. SCOPE DEFINITION

### IN-SCOPE (What Mercury WILL Do)

| Capability | Description |
|------------|-------------|
| **Conversational Query** | Accept natural language questions about markets |
| **Data Fetching** | Retrieve live data from Kite API (quotes, positions, holdings, watchlists, historical data) |
| **AI Synthesis** | Process data through Claude to generate intelligent responses |
| **Direct Answers** | Provide synthesized insights without artificial constraints |
| **Context Awareness** | Maintain conversation context for follow-up questions |
| **Multi-Instrument** | Handle queries across any instrument available via Kite |

### OUT-OF-SCOPE (What Mercury Will NOT Do)

| Exclusion | Rationale |
|-----------|-----------|
| **Order Execution** | Mercury advises; user executes via their broker |
| **Portfolio Management** | Mercury provides insight; user manages positions |
| **Automated Trading** | Mercury is cognitive, not autonomous |
| **Charting/Visualization** | Mercury is conversational; charts are separate |
| **Alert Management** | Mercury responds to queries; alerts are separate |
| **Historical Analytics** | Limited to what Kite API provides |

---

## 6. SUCCESS CRITERIA

### Quantifiable Metrics

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| **Query-to-Response Time** | < 5 seconds | End-to-end latency |
| **Data Accuracy** | 100% | Response matches live Kite data |
| **Conversation Continuity** | 10+ turns | Context maintained across exchanges |
| **API Reliability** | 99%+ | Successful query completion rate |
| **User Satisfaction** | Subjective | User confirms utility |

### Functional Success Criteria

1. ✅ User can ask: *"What's the current price of GOLDBEES?"* → Receives accurate live price
2. ✅ User can ask: *"How has NIFTY performed this week?"* → Receives synthesized analysis
3. ✅ User can ask: *"What do you think about my gold positions?"* → Receives opinionated insight
4. ✅ User can ask: *"Should I be concerned about the market today?"* → Receives direct assessment
5. ✅ Follow-up questions maintain context from previous exchanges

---

## 7. CONSTRAINTS

### Technical Constraints

| Constraint | Impact |
|------------|--------|
| **Kite API Rate Limits** | Must respect API quotas |
| **Kite API Scope** | Limited to data Kite exposes |
| **Claude API Costs** | Token usage has financial cost |
| **Network Dependency** | Requires internet connectivity |
| **Authentication** | Requires valid Kite session |

### Business Constraints

| Constraint | Impact |
|------------|--------|
| **Personal Use Only** | Not for redistribution or commercial use |
| **No Regulatory Compliance** | Personal tool, not regulated advice |
| **Single User** | Designed for individual use |

---

## 8. ANTI-PATTERNS (What Mercury is NOT)

### Anti-Pattern 1: Mercury is NOT a Restricted Assistant

**Wrong**: An AI that hedges every statement, adds disclaimers to every response, and refuses to express opinions.

**Right**: An AI that engages directly, synthesizes information, and provides clear insights.

### Anti-Pattern 2: Mercury is NOT a Data Dump

**Wrong**: An AI that simply returns raw API data without interpretation.

**Right**: An AI that transforms data into understanding.

### Anti-Pattern 3: Mercury is NOT a Decision-Maker

**Wrong**: An AI that makes decisions on behalf of the user.

**Right**: An AI that informs and advises while the user decides.

### Anti-Pattern 4: Mercury is NOT Constrained by CIA-SIE Rules

**Wrong**: Importing CR-001, CR-002, CR-003 restrictions.

**Right**: Operating under Mercury's own unrestricted constitution.

---

## 9. RELATIONSHIP TO CIA-SIE-PURE

### Independence Declaration

Mercury is an **independent module** within the CIA-SIE-PURE workspace. It:

- **SHARES**: Infrastructure (Python, FastAPI, project structure)
- **SHARES**: Kite API integration code (platforms/kite.py)
- **DOES NOT SHARE**: Constitutional rules (CR-001, CR-002, CR-003)
- **DOES NOT SHARE**: Response validation (prohibited patterns)
- **DOES NOT SHARE**: Mandatory disclaimers

### Architectural Relationship

```
CIA-SIE-PURE (Workspace)
├── src/cia_sie/          # Existing application (Constitutional)
│   ├── ai/               # Constrained AI layer
│   ├── platforms/kite.py # SHARED: Kite integration
│   └── ...
│
└── projects/mercury/     # NEW: Mercury (Unrestricted)
    ├── src/mercury/      # Mercury-specific code
    │   ├── ai/           # UNRESTRICTED AI layer
    │   ├── kite/         # Kite adapter (uses shared code)
    │   └── chat/         # Conversational interface
    └── ...
```

---

## 10. VISION STATEMENT

### The Future State

When Mercury is complete, the user will:

1. **Open a terminal or simple interface**
2. **Type a question in plain English** about any market topic
3. **Receive an intelligent, grounded, direct response** within seconds
4. **Continue the conversation** with follow-up questions
5. **Make informed decisions** based on AI-synthesized insights

### The Experience

```
User: What's happening with gold today?

Mercury: Gold (XAUUSD) is currently trading at $2,045.30, up 0.8% from 
yesterday's close. GOLDBEES on NSE is at ₹58.42, tracking the global 
move. Volume is elevated at 1.2x the 20-day average, suggesting 
institutional participation. Given the weak dollar (DXY down 0.3%) 
and rising treasury yields, this looks like a flight-to-safety bid 
rather than inflation positioning. Your current GOLDBEES position 
is up 12% from your average entry - you might consider whether 
this strength is an opportunity to add or take partial profits.

User: How does this compare to silver?

Mercury: Silver is underperforming gold today, up only 0.3%. The 
gold/silver ratio has expanded to 88.5, historically elevated. 
SILVERBEES is at ₹82.15. When gold leads silver like this, it 
often indicates safe-haven demand rather than industrial metals 
strength. Your silver position is smaller but showing similar 
gains. The ratio suggests silver may have catch-up potential 
if this becomes a sustained precious metals rally.
```

---

## 11. GENESIS VALIDATION CHECKLIST

| Condition | Status | Evidence |
|-----------|--------|----------|
| Vision document exists | ✅ | This document |
| Problem statement is explicit | ✅ | Section 2 |
| User is identified with specificity | ✅ | Section 3 |
| Scope is bounded (IN and OUT) | ✅ | Section 5 |
| Success criteria are measurable | ✅ | Section 6 |
| Constraints are acknowledged | ✅ | Section 7 |
| Core philosophy in one sentence | ✅ | Section 4 |
| At least 3 anti-patterns documented | ✅ | Section 8 (4 documented) |

---

## 12. GENESIS SIGN-OFF

**Stage I: GENESIS is COMPLETE.**

This document establishes the foundational vision for Project Mercury. All subsequent stages will trace back to this genesis.

---

**Prepared by**: AI Development Assistant  
**Date**: 2026-01-13  
**Next Stage**: CONSTITUTION (Stage II)
