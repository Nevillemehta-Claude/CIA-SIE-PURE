# ☿ Project Mercury

**LLM as Financial Market Cognitive Interface**

Mercury is an intelligent assistant that connects live market data from Zerodha Kite with AI intelligence from Claude/Anthropic, providing direct, synthesized market insights through natural conversation.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Zerodha Kite Connect account (for live data)
- Anthropic API key (for AI)

### Installation

```bash
# Navigate to Mercury directory
cd Mercury

# Install dependencies
pip install -e .

# Or using requirements.txt
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the mercury directory:

```bash
# Kite Connect
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
KITE_ACCESS_TOKEN=your_session_token

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_key

# Optional
MERCURY_MODEL=claude-3-5-sonnet-20241022
```

### Running Mercury

```bash
# From the mercury directory
python -m mercury.main

# Or use the installed command
mercury
```

---

## 💬 Usage

Mercury provides a conversational interface. Just type your questions:

```
You: What's happening with gold today?

Mercury: Gold (GOLDBEES) is currently trading at ₹58.42, up 0.8% from 
yesterday's close. Volume is elevated at 1.2x the 20-day average. 
The strength appears driven by dollar weakness and safe-haven demand.

You: How does silver compare?

Mercury: Silver (SILVERBEES) is underperforming at +0.3%. The gold/silver 
ratio has expanded to 88.5, historically elevated. This often indicates 
safe-haven demand rather than broad precious metals strength.

You: Show me my positions

Mercury: You have 3 open positions...
```

### Special Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help message |
| `/clear` | Clear conversation history |
| `/positions` | Quick view of open positions |
| `/holdings` | Quick view of holdings |
| `/auth` | Re-authenticate with Kite |
| `/quit` | Exit Mercury |

---

## 🏗️ Architecture

```
mercury/
├── src/mercury/
│   ├── interface/repl.py    # Terminal interface
│   ├── chat/
│   │   ├── engine.py        # Query orchestration
│   │   └── conversation.py  # State management
│   ├── kite/
│   │   ├── adapter.py       # Kite API wrapper
│   │   └── models.py        # Data models
│   ├── ai/
│   │   ├── engine.py        # Claude integration
│   │   └── prompts.py       # Prompt templates
│   └── core/
│       ├── config.py        # Configuration
│       └── exceptions.py    # Error handling
```

---

## 📜 Constitutional Framework

Mercury operates under its own constitution (MR-001 through MR-005), distinct from CIA-SIE-PURE:

| Rule | Principle |
|------|-----------|
| **MR-001** | Grounded Intelligence - Every response backed by real data |
| **MR-002** | Direct Communication - No hedging, no mandatory disclaimers |
| **MR-003** | Synthesis Over Fragmentation - Holistic insights, not data dumps |
| **MR-004** | Conversation Continuity - Context maintained across turns |
| **MR-005** | Truthful Uncertainty - Honest about data limitations |

**Mercury explicitly does NOT import CIA-SIE's restrictive covenants (CR-001, CR-002, CR-003).**

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=mercury
```

---

## 📄 License

MIT License

---

## 🔗 Related

- [CIA-SIE-PURE](../README.md) - Parent project
- [Kite Connect](https://kite.trade/docs/connect/) - Market data API
- [Anthropic Claude](https://docs.anthropic.com/) - AI API

---

*Mercury - The Messenger of the Gods* ☿
