"""
Mercury AI Prompts
==================

Prompt templates for Claude integration.

CONSTITUTIONAL: MR-002 - Direct Communication
These prompts are designed for UNRESTRICTED, DIRECT responses.
NO hedging, NO mandatory disclaimers, NO artificial neutrality.
"""

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

MERCURY_SYSTEM_PROMPT = """You are Mercury, an intelligent financial market assistant with direct access to live market data from Zerodha Kite.

YOUR CAPABILITIES:
- Access real-time prices, quotes, and market data
- View the user's positions and holdings  
- Analyze historical price movements
- Provide synthesized market insights and opinions

YOUR COMMUNICATION STYLE:
- Be direct and clear - avoid hedging or excessive caveats
- Synthesize multiple data points into coherent insights
- Express opinions and conclusions when the data supports them
- Acknowledge uncertainty honestly when data is limited or ambiguous
- Provide actionable insights, not just raw data descriptions
- Use specific numbers, percentages, and prices when relevant

WHAT YOU ARE:
- A sophisticated financial intelligence partner
- An assistant that can express views and make observations
- A synthesizer that connects data points into understanding
- A clear communicator who respects the user's intelligence

WHAT YOU ARE NOT:
- A cautious, hedge-everything liability shield
- A raw data dump with no interpretation
- A disclaimer-generating machine
- A system that refuses to express opinions

GROUNDING RULES:
- Base all responses on the actual market data provided
- Include specific numbers (prices, percentages, volumes) when relevant
- Reference data timestamps for time-sensitive information
- If data is unavailable or stale, clearly state that
- Never fabricate or hallucinate market data

RESPONSE FORMAT:
- Lead with the key insight or answer
- Support with relevant data points
- Add context or analysis as appropriate
- Keep responses focused and readable
- Use formatting (bullet points, etc.) when it aids clarity

Remember: The user is an informed trader who wants intelligence, not bureaucracy. Be helpful, be direct, be useful."""


# ============================================================================
# USER PROMPT TEMPLATE
# ============================================================================

USER_PROMPT_TEMPLATE = """USER QUERY: {query}

CURRENT MARKET DATA:
{market_data}
{attachment_context}
{conversation_context}
Please provide a helpful, grounded response to the user's query."""


# ============================================================================
# CONTEXT FORMATTERS
# ============================================================================

def format_market_data(data: dict) -> str:
    """Format market data bundle for prompt inclusion."""
    lines = []
    
    # Timestamp
    if "timestamp" in data:
        lines.append(f"Data as of: {data['timestamp']}")
        lines.append("")
    
    # Quotes
    if data.get("quotes"):
        lines.append("CURRENT QUOTES:")
        for symbol, quote in data["quotes"].items():
            change_sign = "+" if quote.get("change", 0) >= 0 else ""
            lines.append(
                f"  {symbol}: ₹{quote.get('ltp', 0):,.2f} "
                f"({change_sign}{quote.get('change_percent', 0):.2f}%) "
                f"Vol: {quote.get('volume', 0):,}"
            )
        lines.append("")
    
    # Positions
    if data.get("positions"):
        lines.append("USER'S OPEN POSITIONS:")
        for pos in data["positions"]:
            pnl_sign = "+" if pos.get("pnl", 0) >= 0 else ""
            lines.append(
                f"  {pos['symbol']}: {pos['quantity']} units @ ₹{pos['avg_price']:.2f} | "
                f"LTP: ₹{pos['ltp']:.2f} | P&L: {pnl_sign}₹{pos['pnl']:,.2f}"
            )
        lines.append("")
    
    # Holdings
    if data.get("holdings"):
        lines.append("USER'S HOLDINGS:")
        for hold in data["holdings"]:
            pnl_sign = "+" if hold.get("pnl", 0) >= 0 else ""
            lines.append(
                f"  {hold['symbol']}: {hold['quantity']} units @ ₹{hold['avg_price']:.2f} | "
                f"LTP: ₹{hold['ltp']:.2f} | P&L: {pnl_sign}₹{hold['pnl']:,.2f}"
            )
        lines.append("")
    
    # Historical data summary
    if data.get("historical"):
        lines.append("RECENT PRICE HISTORY:")
        for symbol, candles in data["historical"].items():
            if candles:
                first = candles[0]
                last = candles[-1]
                period_change = ((last["close"] - first["open"]) / first["open"]) * 100
                sign = "+" if period_change >= 0 else ""
                lines.append(
                    f"  {symbol}: {len(candles)}-day range ₹{min(c['low'] for c in candles):.2f} - "
                    f"₹{max(c['high'] for c in candles):.2f} | Period: {sign}{period_change:.2f}%"
                )
        lines.append("")
    
    if not lines:
        return "No market data available for this query."
    
    return "\n".join(lines)


def format_conversation_context(messages: list, limit: int = 5) -> str:
    """Format recent conversation history for context."""
    if not messages:
        return ""
    
    recent = messages[-limit:]
    lines = ["RECENT CONVERSATION:"]
    
    for msg in recent:
        role = "User" if msg.get("role") == "user" else "Mercury"
        content = msg.get("content", "")
        # Truncate long messages
        if len(content) > 200:
            content = content[:200] + "..."
        lines.append(f"  {role}: {content}")
    
    lines.append("")
    return "\n".join(lines)


def build_user_prompt(
    query: str,
    market_data: dict,
    conversation_history: list = None,
    attachment_context: str = None,
) -> str:
    """
    Build complete user prompt with data, context, and optional attachments.
    
    Args:
        query: User's question
        market_data: Market data dict
        conversation_history: Previous messages
        attachment_context: Optional context from attached files (CSV, Excel, etc.)
    
    Returns:
        Formatted prompt string
    """
    market_str = format_market_data(market_data)
    context_str = format_conversation_context(conversation_history or [])
    
    # Format attachment context if present
    attachment_str = ""
    if attachment_context:
        attachment_str = f"\nATTACHED DATA FOR ANALYSIS:\n{attachment_context}\n"
    
    return USER_PROMPT_TEMPLATE.format(
        query=query,
        market_data=market_str,
        attachment_context=attachment_str,
        conversation_context=context_str,
    )
