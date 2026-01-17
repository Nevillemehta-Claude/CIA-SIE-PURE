"""
CIA-SIE Claude API Client
=========================

Wrapper for Anthropic's Claude API.

This client is used for narrative generation only.
The narratives are DESCRIPTIVE, never PRESCRIPTIVE.
"""

import logging
from typing import Optional

from anthropic import AsyncAnthropic

from cia_sie.core.config import get_settings
from cia_sie.core.exceptions import AIProviderError

logger = logging.getLogger(__name__)


class ClaudeClient:
    """
    Async client for Claude API.

    Used exclusively for generating descriptive narratives.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize the Claude client.

        Args:
            api_key: Anthropic API key (defaults to settings)
            model: Model to use (defaults to settings)
        """
        settings = get_settings()
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.anthropic_model

        if not self.api_key:
            logger.warning("No Anthropic API key configured")

        self._client: Optional[AsyncAnthropic] = None

    @property
    def client(self) -> AsyncAnthropic:
        """Get or create the async client."""
        if self._client is None:
            if not self.api_key:
                raise AIProviderError(
                    "Anthropic API key not configured",
                    {"hint": "Set ANTHROPIC_API_KEY in environment"},
                )
            self._client = AsyncAnthropic(api_key=self.api_key)
        return self._client

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate a response from Claude.

        Args:
            system_prompt: System instructions for Claude
            user_prompt: User message/request
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (lower = more focused)

        Returns:
            Generated text response

        Raises:
            AIProviderError: If generation fails
        """
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise AIProviderError("Empty response from Claude", {"response": str(response)})

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise AIProviderError(
                f"Failed to generate narrative: {str(e)}", {"error_type": type(e).__name__}
            )

    async def health_check(self) -> bool:
        """
        Check if Claude API is accessible.

        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Simple test call
            await self.generate(
                system_prompt="Respond with 'OK'",
                user_prompt="Health check",
                max_tokens=10,
            )
            return True
        except Exception as e:
            logger.warning(f"Claude health check failed: {e}")
            return False
