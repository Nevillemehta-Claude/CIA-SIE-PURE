"""
Mercury OAuth Manager
=====================

Automatic OAuth lifecycle management for Kite Connect.

AUTONOMOUS PRINCIPLE: Self-healing authentication.
When tokens expire, the system gracefully prompts for re-authentication
without crashing or losing state.

MISSION-CRITICAL STANDARD: Zero-Defect Token Management
"""

import asyncio
import json
import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Callable, Awaitable
from enum import Enum

from mercury.core.logging import get_logger
from mercury.core.config import get_settings

logger = get_logger("mercury.oauth")


class TokenState(Enum):
    """State of the access token."""
    VALID = "valid"
    EXPIRED = "expired"
    MISSING = "missing"
    INVALID = "invalid"


@dataclass
class TokenInfo:
    """Information about a stored token."""
    access_token: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    
    def is_expired(self) -> bool:
        """Check if token is expired."""
        if self.expires_at is None:
            # Kite tokens expire at 6 AM IST next day
            # If created today before 6 AM, expires at 6 AM today
            # If created today after 6 AM, expires at 6 AM tomorrow
            ist = timezone(timedelta(hours=5, minutes=30))
            now = datetime.now(ist)
            created_ist = self.created_at.astimezone(ist)
            
            # Token expires at 6 AM IST
            expiry = created_ist.replace(hour=6, minute=0, second=0, microsecond=0)
            if created_ist.hour >= 6:
                expiry += timedelta(days=1)
            
            return now >= expiry
        
        return datetime.now(timezone.utc) >= self.expires_at
    
    def time_until_expiry(self) -> Optional[timedelta]:
        """Get time until token expires."""
        if self.expires_at:
            return self.expires_at - datetime.now(timezone.utc)
        
        # Calculate based on Kite's 6 AM IST expiry
        ist = timezone(timedelta(hours=5, minutes=30))
        now = datetime.now(ist)
        created_ist = self.created_at.astimezone(ist)
        
        expiry = created_ist.replace(hour=6, minute=0, second=0, microsecond=0)
        if created_ist.hour >= 6:
            expiry += timedelta(days=1)
        
        return expiry - now
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "access_token": self.access_token,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "user_id": self.user_id,
            "user_name": self.user_name,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TokenInfo":
        """Create from dictionary."""
        return cls(
            access_token=data["access_token"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            user_id=data.get("user_id"),
            user_name=data.get("user_name"),
        )


class TokenExpiredError(Exception):
    """Raised when the access token has expired."""
    
    def __init__(self, message: str, auth_url: Optional[str] = None):
        super().__init__(message)
        self.auth_url = auth_url


class OAuthManager:
    """
    Automatic OAuth lifecycle management for Kite Connect.
    
    AUTONOMOUS PRINCIPLE: Self-healing authentication.
    
    Features:
    - Persistent token storage in ~/.mercury/
    - Automatic expiry detection
    - Graceful degradation on token issues
    - Event emission for UI notification
    - Thread-safe token access
    """
    
    def __init__(
        self,
        token_dir: Optional[Path] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
    ):
        """
        Initialize OAuth Manager.
        
        Args:
            token_dir: Directory to store tokens (default: ~/.mercury)
            api_key: Kite API key (default: from settings)
            api_secret: Kite API secret (default: from settings)
        """
        settings = get_settings()
        
        self.token_dir = token_dir or Path.home() / ".mercury"
        self.token_file = self.token_dir / "kite_token.json"
        self.api_key = api_key or settings.kite_api_key
        self.api_secret = api_secret or settings.kite_api_secret
        
        self._token_info: Optional[TokenInfo] = None
        self._lock = asyncio.Lock()
        self._auth_required_callbacks: list[Callable[[], Awaitable[None]]] = []
        
        # Ensure token directory exists
        self.token_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing token on init
        self._load_token()
    
    @property
    def login_url(self) -> str:
        """Get the Kite login URL."""
        if not self.api_key:
            raise ValueError("KITE_API_KEY not configured")
        return f"https://kite.zerodha.com/connect/login?api_key={self.api_key}&v=3"
    
    @property
    def has_valid_token(self) -> bool:
        """Check if we have a valid (non-expired) token."""
        if self._token_info is None:
            return False
        return not self._token_info.is_expired()
    
    @property
    def token_state(self) -> TokenState:
        """Get the current token state."""
        if self._token_info is None:
            # Check if we have a token in env but not loaded
            settings = get_settings()
            if settings.kite_access_token:
                return TokenState.VALID  # Assume env token is valid
            return TokenState.MISSING
        
        if self._token_info.is_expired():
            return TokenState.EXPIRED
        
        return TokenState.VALID
    
    def _load_token(self) -> Optional[TokenInfo]:
        """Load token from file."""
        try:
            if self.token_file.exists():
                with open(self.token_file, "r") as f:
                    data = json.load(f)
                self._token_info = TokenInfo.from_dict(data)
                logger.info(
                    "Loaded token from file",
                    context={
                        "user": self._token_info.user_name,
                        "expired": self._token_info.is_expired(),
                    }
                )
                return self._token_info
        except Exception as e:
            logger.warning(f"Failed to load token: {e}")
        
        return None
    
    def _save_token(self, token_info: TokenInfo) -> None:
        """Save token to file."""
        try:
            with open(self.token_file, "w") as f:
                json.dump(token_info.to_dict(), f, indent=2)
            
            # Set restrictive permissions (owner read/write only)
            self.token_file.chmod(0o600)
            
            logger.info("Token saved to file")
        except Exception as e:
            logger.error(f"Failed to save token: {e}")
    
    def _invalidate_token(self) -> None:
        """Invalidate the current token."""
        self._token_info = None
        
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            logger.info("Token invalidated")
        except Exception as e:
            logger.warning(f"Failed to delete token file: {e}")
    
    async def get_valid_token(self) -> str:
        """
        Get a valid access token.
        
        Returns:
            Valid access token string
            
        Raises:
            TokenExpiredError: If token is expired or missing
        """
        async with self._lock:
            # First check settings (env var takes precedence)
            settings = get_settings()
            if settings.kite_access_token:
                # Env token - assume valid, will fail on API call if not
                return settings.kite_access_token
            
            # Check stored token
            if self._token_info and not self._token_info.is_expired():
                return self._token_info.access_token
            
            # Token expired or missing
            state = "expired" if self._token_info else "missing"
            raise TokenExpiredError(
                f"Kite session {state}. Please re-authenticate.",
                auth_url=self.login_url,
            )
    
    async def handle_oauth_callback(
        self,
        request_token: str,
    ) -> TokenInfo:
        """
        Handle the OAuth callback with request token.
        
        Exchanges request_token for access_token.
        
        Args:
            request_token: The request token from Kite callback
            
        Returns:
            TokenInfo with the new access token
            
        Raises:
            ValueError: If exchange fails
        """
        if not self.api_key or not self.api_secret:
            raise ValueError("KITE_API_KEY and KITE_API_SECRET required for OAuth")
        
        # Generate checksum
        checksum_string = f"{self.api_key}{request_token}{self.api_secret}"
        checksum = hashlib.sha256(checksum_string.encode()).hexdigest()
        
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.kite.trade/session/token",
                    data={
                        "api_key": self.api_key,
                        "request_token": request_token,
                        "checksum": checksum,
                    },
                )
                
                if response.status_code != 200:
                    error_msg = response.json().get("message", "Token exchange failed")
                    logger.error(f"OAuth token exchange failed: {error_msg}")
                    raise ValueError(f"OAuth failed: {error_msg}")
                
                data = response.json()
                token_data = data.get("data", {})
                
                access_token = token_data.get("access_token")
                if not access_token:
                    raise ValueError("No access token in response")
                
                # Create token info
                token_info = TokenInfo(
                    access_token=access_token,
                    created_at=datetime.now(timezone.utc),
                    user_id=token_data.get("user_id"),
                    user_name=token_data.get("user_name"),
                )
                
                # Save token
                async with self._lock:
                    self._token_info = token_info
                    self._save_token(token_info)
                
                logger.info(
                    "OAuth completed successfully",
                    context={"user": token_info.user_name}
                )
                
                return token_info
                
        except httpx.RequestError as e:
            logger.error(f"OAuth network error: {e}")
            raise ValueError(f"Network error during OAuth: {e}")
    
    async def handle_token_exception(self, error: Exception) -> None:
        """
        Handle a token-related exception from the Kite API.
        
        This invalidates the token and notifies subscribers.
        
        Args:
            error: The exception that was raised
        """
        error_str = str(error).lower()
        error_type = type(error).__name__
        
        is_token_error = (
            "TokenException" in error_type or
            "token" in error_str or
            "session" in error_str or
            "authentication" in error_str
        )
        
        if is_token_error:
            logger.warning("Token exception detected, invalidating token")
            self._invalidate_token()
            
            # Notify subscribers
            await self._emit_auth_required()
    
    def on_auth_required(
        self,
        callback: Callable[[], Awaitable[None]],
    ) -> None:
        """
        Register a callback for when authentication is required.
        
        Args:
            callback: Async callback to invoke
        """
        self._auth_required_callbacks.append(callback)
    
    async def _emit_auth_required(self) -> None:
        """Emit auth required event to all subscribers."""
        for callback in self._auth_required_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error(f"Auth callback error: {e}")
    
    def get_status(self) -> dict:
        """Get current OAuth status for API response."""
        state = self.token_state
        settings = get_settings()
        
        # Check if we have a token from either file or env var
        has_token = self._token_info is not None or bool(settings.kite_access_token)
        
        result = {
            "state": state.value,
            "has_token": has_token,
            "token_source": "file" if self._token_info else ("env" if settings.kite_access_token else None),
            "login_url": self.login_url if self.api_key else None,
        }
        
        if self._token_info:
            result.update({
                "user_name": self._token_info.user_name,
                "user_id": self._token_info.user_id,
                "created_at": self._token_info.created_at.isoformat(),
                "is_expired": self._token_info.is_expired(),
            })
            
            time_left = self._token_info.time_until_expiry()
            if time_left:
                result["expires_in_seconds"] = int(time_left.total_seconds())
        elif settings.kite_access_token:
            result.update({
                "user_name": "env_configured",
                "is_expired": False,  # Assume env token is valid until API error
            })
        
        return result


# Global OAuth manager instance
_oauth_manager: Optional[OAuthManager] = None


def get_oauth_manager() -> OAuthManager:
    """Get or create the global OAuth manager."""
    global _oauth_manager
    if _oauth_manager is None:
        _oauth_manager = OAuthManager()
    return _oauth_manager
