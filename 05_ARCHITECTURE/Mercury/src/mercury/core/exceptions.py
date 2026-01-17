"""
Mercury Custom Exceptions
=========================

Application-specific exceptions with error codes.

CONSTITUTIONAL: MR-005 - Truthful Uncertainty
Exceptions are surfaced honestly to the user.
"""

from typing import Optional


class MercuryError(Exception):
    """Base exception for Mercury."""

    code: str = "E000"
    
    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def user_message(self) -> str:
        """Get user-friendly error message."""
        return self.message


class KiteAPIError(MercuryError):
    """Kite API call failed."""
    code = "E001"

    def user_message(self) -> str:
        return "There was an issue with the market data service. Please try again."


class KiteAuthError(MercuryError):
    """Kite authentication failed."""
    code = "E001"

    def user_message(self) -> str:
        return "Kite session expired. Please re-authenticate with /auth"


class KiteRateLimitError(MercuryError):
    """Kite rate limit exceeded."""
    code = "E002"

    def user_message(self) -> str:
        return "Too many requests. Please wait a moment and try again."


class SymbolNotFoundError(MercuryError):
    """Symbol doesn't exist."""
    code = "E003"

    def __init__(self, symbol: str):
        super().__init__(f"Symbol not found: {symbol}", {"symbol": symbol})
        self.symbol = symbol

    def user_message(self) -> str:
        return f"I couldn't find '{self.symbol}'. Please check the symbol name."


class NoDataAvailableError(MercuryError):
    """No data available for request."""
    code = "E004"

    def user_message(self) -> str:
        return "No data available for that request."


class AIEngineError(MercuryError):
    """Claude AI generation failed."""
    code = "E005"

    def user_message(self) -> str:
        return "AI service temporarily unavailable. Please try again."


class NetworkError(MercuryError):
    """Network connectivity issue."""
    code = "E006"

    def user_message(self) -> str:
        return "Network issue. Please check your connection."


class InvalidQueryError(MercuryError):
    """Cannot parse user query."""
    code = "E007"

    def user_message(self) -> str:
        return "I didn't understand that. Could you rephrase your question?"
