"""
Mercury Chat Engine
===================

Main orchestration engine that connects user queries to data and AI.

CONSTITUTIONAL: MR-001 - Grounded Intelligence
CONSTITUTIONAL: MR-003 - Synthesis Over Fragmentation
CONSTITUTIONAL: MR-004 - Conversation Continuity

ARCHITECTURAL PRINCIPLE: LLM-Driven Intent Resolution
Instead of hardcoded keyword matching, we use Claude to understand
user intent. This allows Mercury to understand:
- Novel phrasings ("give me a pulse on the markets")
- Multiple languages (Hindi, Hinglish)
- Context and nuance
- Complex multi-part queries

This is the core of Mercury - it:
1. Receives user queries
2. Uses AI to understand intent and extract data needs
3. Fetches relevant data from Kite
4. Sends to AI with context for synthesis
5. Returns intelligent response
"""

import logging
import re
from typing import Optional

from mercury.ai.engine import AIEngine
from mercury.ai.intent import get_intent_resolver, IntentResult
from mercury.chat.conversation import Conversation
from mercury.kite.adapter import KiteAdapter
from mercury.core.exceptions import MercuryError

logger = logging.getLogger(__name__)


class ChatEngine:
    """
    Mercury's main orchestration engine.
    
    CONSTITUTIONAL: MR-001 - Every response grounded in data from Kite
    CONSTITUTIONAL: MR-003 - AI synthesizes, doesn't just dump data
    CONSTITUTIONAL: MR-004 - Conversation history maintained
    
    ARCHITECTURAL: LLM-driven intent resolution for natural language understanding
    """
    
    def __init__(
        self,
        kite: Optional[KiteAdapter] = None,
        ai: Optional[AIEngine] = None,
        use_llm_intent: bool = True,
    ):
        """
        Initialize Chat Engine.
        
        Args:
            kite: Kite adapter for market data (creates default if None)
            ai: AI engine for response generation (creates default if None)
            use_llm_intent: Use LLM for intent resolution (True) or fallback to keywords (False)
        """
        self.kite = kite or KiteAdapter()
        self.ai = ai or AIEngine()
        self.use_llm_intent = use_llm_intent
        self._intent_resolver = None
    
    @property
    def intent_resolver(self):
        """Lazy-initialize intent resolver."""
        if self._intent_resolver is None:
            self._intent_resolver = get_intent_resolver(use_fast_model=True)
        return self._intent_resolver
    
    async def process(
        self,
        query: str,
        conversation: Conversation,
        attachment_context: Optional[str] = None,
        image_attachments: Optional[list[dict]] = None,
    ) -> str:
        """
        Process a user query end-to-end.
        
        This is the main entry point for Mercury.
        
        FLOW:
        1. User query → LLM Intent Resolver → Structured data needs
        2. Data needs → Kite API → Market data
        3. Query + Data + Attachments → LLM Synthesizer → Intelligent response
        
        CONSTITUTIONAL: MR-001 - Fetches real data before generating
        CONSTITUTIONAL: MR-003 - Sends data to AI for synthesis
        CONSTITUTIONAL: MR-004 - Includes conversation history
        
        Args:
            query: User's natural language query
            conversation: Current conversation context
            attachment_context: Optional context from attached files (CSV, Excel, etc.)
            image_attachments: Optional list of image attachments for vision analysis
            
        Returns:
            AI-generated response grounded in market data
        """
        try:
            # 1. Add user message to conversation
            conversation.add_user_message(query)
            
            # 2. Get conversation context for intent resolution
            recent_messages = [
                msg.get("content", "")[:100] 
                for msg in conversation.get_history(limit=3)
            ]
            
            # 3. Use LLM to understand intent and extract data needs
            if self.use_llm_intent:
                intent = await self.intent_resolver.resolve(
                    query=query,
                    conversation_context=recent_messages,
                )
                instruments = intent.symbols
                include_positions = intent.needs_positions
                include_holdings = intent.needs_holdings
                include_history = intent.needs_historical
                
                logger.info(
                    f"Intent resolved: {intent.intent_summary} "
                    f"(confidence: {intent.confidence:.0%})"
                )
            else:
                # Fallback to rule-based extraction
                instruments = self.identify_instruments(query, conversation)
                data_needs = self.identify_data_needs(query)
                include_positions = "position" in data_needs
                include_holdings = "holding" in data_needs
                include_history = "history" in data_needs
            
            # 4. Update conversation context
            conversation.update_instrument_context(instruments)
            
            # 5. Fetch data from Kite
            data_bundle = await self.kite.get_data_bundle(
                symbols=instruments,
                include_positions=include_positions,
                include_holdings=include_holdings,
                include_history=include_history,
            )
            
            # 6. Convert to context dict for AI
            market_data = data_bundle.to_context_dict()
            
            # 7. Get conversation history
            history = conversation.get_history(limit=10)
            
            # 8. Generate AI response with optional attachment context
            response = await self.ai.generate(
                user_query=query,
                market_data=market_data,
                conversation_history=history[:-1],  # Exclude current query
                attachment_context=attachment_context,
                image_attachments=image_attachments,
            )
            
            # 9. Add assistant response to conversation
            conversation.add_assistant_message(response, market_data)
            
            return response
            
        except MercuryError as e:
            # Return user-friendly error message
            error_response = f"I encountered an issue: {e.user_message()}"
            conversation.add_assistant_message(error_response)
            return error_response
        except Exception as e:
            logger.error(f"Unexpected error in process: {e}")
            error_response = "I encountered an unexpected error. Please try again."
            conversation.add_assistant_message(error_response)
            return error_response
    
    def identify_instruments(
        self,
        query: str,
        conversation: Conversation,
    ) -> list[str]:
        """
        FALLBACK: Identify instruments using rule-based extraction.
        
        NOTE: This is only used when LLM intent resolution is disabled.
        Prefer LLM-driven intent resolution for better natural language understanding.
        
        Uses:
        - Explicit symbol mentions (all caps, 3+ chars)
        - Context from previous conversation turns
        
        Args:
            query: User's query
            conversation: Current conversation for context
            
        Returns:
            List of instrument symbols to fetch
        """
        query_lower = query.lower()
        instruments = []
        
        # Check for explicit symbols (all caps, 3+ chars)
        explicit_symbols = re.findall(r'\b([A-Z]{3,20})\b', query)
        instruments.extend(explicit_symbols)
        
        # Basic fallback aliases (minimal set for safety net)
        FALLBACK_ALIASES = {
            "market": ["NIFTY 50", "NIFTY BANK", "SENSEX"],
            "nifty": ["NIFTY 50"],
            "banknifty": ["NIFTY BANK"],
        }
        for alias, symbols in FALLBACK_ALIASES.items():
            if alias in query_lower:
                instruments.extend(symbols)
        
        # If query refers to previous context ("it", "that", etc.)
        context_words = ["it", "its", "that", "this", "them", "these", "those"]
        if any(word in query_lower.split() for word in context_words):
            instruments.extend(conversation.get_last_instruments(3))
        
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for inst in instruments:
            if inst not in seen:
                seen.add(inst)
                unique.append(inst)
        
        return unique[:10]
    
    def identify_data_needs(self, query: str) -> set[str]:
        """
        FALLBACK: Identify data needs using keyword matching.
        
        NOTE: This is only used when LLM intent resolution is disabled.
        Prefer LLM-driven intent resolution for better understanding.
        
        Args:
            query: User's query
            
        Returns:
            Set of data types needed: "quote", "position", "holding", "history"
        """
        query_lower = query.lower()
        needs = {"quote"}
        
        if any(word in query_lower for word in ["position", "p&l", "pnl", "trade"]):
            needs.add("position")
        
        if any(word in query_lower for word in ["holding", "portfolio", "invested"]):
            needs.add("holding")
        
        if any(word in query_lower for word in ["history", "week", "month", "trend"]):
            needs.add("history")
        
        return needs


async def quick_query(query: str) -> str:
    """
    Quick one-off query without conversation state.
    
    Useful for simple queries that don't need context.
    
    Args:
        query: User's question
        
    Returns:
        AI response
    """
    engine = ChatEngine()
    conversation = Conversation()
    return await engine.process(query, conversation)
