"""
Mercury AI Engine
=================

Claude API integration for intelligent response generation.

CONSTITUTIONAL: MR-002 - Direct Communication
This engine does NOT use CIA-SIE's ResponseValidator.
Responses are UNRESTRICTED - no prohibited patterns, no mandatory disclaimers.

CONSTITUTIONAL: MR-003 - Synthesis Over Fragmentation
Prompts are designed to encourage synthesis and insight.

AUTONOMOUS ENHANCEMENTS:
- Rate limiting to prevent API quota exhaustion
- Circuit breaker integration for resilience
"""

import logging
from typing import Optional

from mercury.core.config import get_settings
from mercury.core.exceptions import AIEngineError
from mercury.core.rate_limiter import get_anthropic_limiter, RateLimitExceeded
from mercury.core.resilience import ai_circuit, CircuitOpenError
from mercury.ai.prompts import MERCURY_SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)


class AIEngine:
    """
    AI Engine for Mercury using Claude/Anthropic.
    
    CONSTITUTIONAL: MR-002 - NO RESPONSE VALIDATION
    Unlike CIA-SIE's ValidatedResponseGenerator, this engine:
    - Does NOT check for prohibited patterns
    - Does NOT inject mandatory disclaimers
    - Does NOT restrict recommendations or opinions
    
    Responses are passed through directly from Claude.
    
    AUTONOMOUS FEATURES:
    - Rate limiting (60 requests/minute sliding window)
    - Circuit breaker protection (fails fast when API is down)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize AI Engine.
        
        Args:
            api_key: Anthropic API key (defaults to settings)
            model: Model ID to use (defaults to settings)
        """
        settings = get_settings()
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.anthropic_model
        self.max_tokens = settings.max_tokens
        self._client = None
        self._rate_limiter = get_anthropic_limiter()
        
    @property
    def client(self):
        """Get or create Anthropic client."""
        if self._client is None:
            if not self.api_key:
                logger.warning("No Anthropic API key configured, using mock mode")
                return MockAnthropicClient()
            
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key)
            except ImportError:
                logger.warning("anthropic package not installed, using mock mode")
                return MockAnthropicClient()
            except Exception as e:
                raise AIEngineError(f"Failed to initialize Anthropic client: {e}")
        
        return self._client
    
    async def generate(
        self,
        user_query: str,
        market_data: dict,
        conversation_history: list = None,
        max_tokens: Optional[int] = None,
        attachment_context: Optional[str] = None,
        image_attachments: Optional[list[dict]] = None,
    ) -> str:
        """
        Generate AI response grounded in market data and optional attachments.
        
        CONSTITUTIONAL: MR-001 - Response is grounded in market_data
        CONSTITUTIONAL: MR-002 - Response is NOT validated/filtered
        CONSTITUTIONAL: MR-003 - Prompt encourages synthesis
        CONSTITUTIONAL: MR-004 - conversation_history provides continuity
        
        AUTONOMOUS: Rate limited and circuit breaker protected.
        FEATURE: Supports file attachments (CSV, Excel, JSON, Images)
        
        Args:
            user_query: The user's question
            market_data: Fetched market data (dict format)
            conversation_history: Previous messages for context
            max_tokens: Override default max tokens
            attachment_context: Optional context from attached files (spreadsheets, etc.)
            image_attachments: Optional list of image dicts for Claude vision
            
        Returns:
            AI-generated response text (UNRESTRICTED)
            
        Raises:
            AIEngineError: If generation fails
        """
        # Check circuit breaker
        if not ai_circuit.allow_request():
            raise AIEngineError(
                "AI service circuit breaker is open - service temporarily unavailable"
            )
        
        try:
            # Apply rate limiting
            await self._rate_limiter.acquire()
            
            # Build the prompt with optional attachment context
            user_prompt = build_user_prompt(
                query=user_query,
                market_data=market_data,
                conversation_history=conversation_history,
                attachment_context=attachment_context,
            )
            
            # Build messages for Claude
            messages = []
            
            # Add conversation history as messages
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                    })
            
            # Build current message content (may include images)
            if image_attachments:
                # Multi-modal message with images
                content = []
                
                # Add images first
                for img in image_attachments:
                    content.append(img)
                
                # Add text prompt
                content.append({
                    "type": "text",
                    "text": user_prompt,
                })
                
                messages.append({
                    "role": "user",
                    "content": content,
                })
            else:
                # Standard text-only message
                messages.append({
                    "role": "user",
                    "content": user_prompt,
                })
            
            # Generate response
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                system=MERCURY_SYSTEM_PROMPT,
                messages=messages,
            )
            
            # Record success with circuit breaker
            ai_circuit.record_success()
            
            # Extract text from response
            if response.content and len(response.content) > 0:
                result = response.content[0].text
                
                # CONSTITUTIONAL: MR-002 - NO validation, NO disclaimer injection
                # The response is returned DIRECTLY without modification
                return result
            
            raise AIEngineError("Empty response from Claude")
            
        except RateLimitExceeded as e:
            raise AIEngineError(f"Rate limit exceeded: {e}")
        except AIEngineError:
            raise
        except Exception as e:
            # Record failure with circuit breaker
            ai_circuit.record_failure(e)
            logger.error(f"AI generation failed: {e}")
            raise AIEngineError(f"Generation failed: {e}")
    
    async def health_check(self) -> bool:
        """Check if AI service is available."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}],
            )
            return len(response.content) > 0
        except Exception as e:
            logger.warning(f"AI health check failed: {e}")
            return False


class MockAnthropicClient:
    """Mock Anthropic client for development without API access."""
    
    class MockMessages:
        def create(self, **kwargs):
            """Return mock response."""
            query = kwargs.get("messages", [{}])[-1].get("content", "")
            
            # Generate contextual mock response
            mock_response = self._generate_mock_response(query)
            
            return MockResponse(mock_response)
        
        def _generate_mock_response(self, query: str) -> str:
            """
            Generate a contextual mock response.
            
            NOTE: This is MOCK MODE only - used when no API keys are configured.
            Responses are generic and instrument-agnostic. In production with
            real API keys, actual market data drives the AI responses.
            """
            query_lower = query.lower()
            
            if "position" in query_lower or "portfolio" in query_lower:
                return (
                    "[MOCK MODE] Looking at your positions, I would analyze your "
                    "current holdings and provide P&L insights. In production mode "
                    "with Kite API connected, I'll show your actual positions."
                )
            elif "holding" in query_lower:
                return (
                    "[MOCK MODE] I would display your delivery holdings with "
                    "current valuations and returns. Connect Kite API for live data."
                )
            elif "compare" in query_lower:
                return (
                    "[MOCK MODE] I would compare the instruments you mentioned, "
                    "analyzing their relative performance, correlation, and key metrics. "
                    "Connect both APIs for live comparisons."
                )
            elif "price" in query_lower or "quote" in query_lower:
                return (
                    "[MOCK MODE] I would fetch the current price and quote data "
                    "for the instrument you specified. Connect Kite API for live quotes."
                )
            else:
                return (
                    "[MOCK MODE] I've received your query. In production mode with "
                    "API keys configured, I would fetch live market data from Kite "
                    "and provide intelligent, data-grounded analysis. "
                    "Please configure KITE_API_KEY and ANTHROPIC_API_KEY in your .env file."
                )
    
    def __init__(self):
        self.messages = self.MockMessages()


class MockResponse:
    """Mock response object."""
    
    def __init__(self, text: str):
        self.content = [MockContent(text)]


class MockContent:
    """Mock content block."""
    
    def __init__(self, text: str):
        self.text = text
