# PROJECT MERCURY: OPERATIONAL HANDOFF

**Document ID**: MERCURY-OPS-001  
**Version**: 1.0.0  
**Date**: 2026-01-13  

---

## STAGE XII: OPERATION
> *"Delivery is not completion; stewardship begins at release."*

---

## 1. QUICK START GUIDE

### 1.1 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Zerodha Kite Connect account (optional, for live data)
- Anthropic API key (optional, for AI responses)

### 1.2 Installation

```bash
# Navigate to Mercury directory
cd /path/to/CIA-SIE-PURE/projects/mercury

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Mercury
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

### 1.3 Configuration

Create `.env` file in the mercury directory:

```bash
# Required for live market data
KITE_API_KEY=your_kite_api_key
KITE_API_SECRET=your_kite_api_secret
KITE_ACCESS_TOKEN=your_session_token

# Required for AI responses
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional configuration
MERCURY_MODEL=claude-3-5-sonnet-20241022
MERCURY_MAX_TOKENS=2000
MERCURY_CONVERSATION_LIMIT=20
```

**Note**: Without API keys, Mercury runs in mock mode with simulated data.

### 1.4 Running Mercury

```bash
# Method 1: Using the installed command
mercury

# Method 2: Using Python module
python -m mercury.main

# Method 3: Direct script
python src/mercury/main.py
```

---

## 2. USAGE GUIDE

### 2.1 Basic Queries

```
You: What's the price of GOLDBEES?
Mercury: [AI response with current price data]

You: How has NIFTY performed this week?
Mercury: [AI response with historical analysis]

You: Compare gold and silver
Mercury: [AI response comparing both instruments]
```

### 2.2 Portfolio Queries

```
You: Show me my positions
Mercury: [AI summary of open positions]

You: What's my P&L today?
Mercury: [AI analysis of profit/loss]

You: How are my holdings doing?
Mercury: [AI summary of holdings performance]
```

### 2.3 Contextual Follow-ups

```
You: What's the price of GOLDBEES?
Mercury: [Response about GOLDBEES]

You: How has it performed this week?
Mercury: [Response about GOLDBEES weekly performance - context maintained]

You: Compare it with silver
Mercury: [Comparison of GOLDBEES vs silver - context maintained]
```

### 2.4 Special Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help and available commands |
| `/clear` | Clear conversation history |
| `/positions` | Quick view of open positions |
| `/holdings` | Quick view of holdings |
| `/auth` | Show authentication instructions |
| `/quit` | Exit Mercury |

---

## 3. KITE AUTHENTICATION

### 3.1 Getting API Credentials

1. Log in to [Kite Connect](https://developers.kite.trade/)
2. Create a new app
3. Note your API Key and API Secret
4. Set the redirect URL to `http://127.0.0.1:8000/callback`

### 3.2 Getting Access Token

The access token is a daily session token. To obtain:

1. Visit: `https://kite.zerodha.com/connect/login?v=3&api_key=YOUR_API_KEY`
2. Log in with your Zerodha credentials
3. You'll be redirected with a `request_token` parameter
4. Exchange for access token using API

**Manual token exchange**:
```python
from kiteconnect import KiteConnect
kite = KiteConnect(api_key="your_api_key")
data = kite.generate_session("request_token", "your_api_secret")
print(data["access_token"])  # Add this to .env
```

### 3.3 Token Refresh

Access tokens expire daily. You'll need to re-authenticate each trading day.

---

## 4. TROUBLESHOOTING

### 4.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Kite session expired" | Access token expired | Re-authenticate and update .env |
| "AI service unavailable" | Missing/invalid Anthropic key | Check ANTHROPIC_API_KEY |
| "Symbol not found" | Invalid symbol name | Check exact symbol (e.g., GOLDBEES not GOLD) |
| Mock data appearing | API keys not set | Configure .env with valid keys |

### 4.2 Debug Mode

Set in .env:
```bash
DEBUG=true
```

This enables verbose logging to help diagnose issues.

---

## 5. FILE STRUCTURE

```
projects/mercury/
├── documentation/
│   ├── 01_GENESIS.md
│   ├── 02_CONSTITUTION.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_SPECIFICATION.md
│   ├── 05_INTEGRATION_VERIFICATION.md
│   ├── 06_RECONCILIATION.md
│   ├── 07_CERTIFICATION.md
│   └── 08_OPERATION.md
├── src/mercury/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── kite/
│   │   ├── adapter.py
│   │   └── models.py
│   ├── ai/
│   │   ├── engine.py
│   │   └── prompts.py
│   ├── chat/
│   │   ├── engine.py
│   │   └── conversation.py
│   └── interface/
│       └── repl.py
├── tests/
│   ├── test_chat_engine.py
│   └── test_conversation.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── .env (create this)
```

---

## 6. MAINTENANCE

### 6.1 Updating Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### 6.2 Running Tests

```bash
pytest tests/
```

### 6.3 Logs

Mercury logs to stdout. Redirect for persistence:
```bash
mercury 2>&1 | tee mercury.log
```

---

## 7. FEEDBACK LOOP

To report issues or request features:

1. Document the issue with reproduction steps
2. Note any error messages
3. Include Mercury version (`mercury --version` or check `__init__.py`)

---

## 8. VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-13 | Initial release |

---

## 9. OPERATIONAL SIGN-OFF

**Stage XII: OPERATION - COMPLETE** ✅

Mercury is certified and ready for operational use.

---

**Handoff Complete**: AI Development Assistant  
**Date**: 2026-01-13  
**Version**: 1.0.0
