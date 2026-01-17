"""
Mercury Rate Limiter
====================

Token bucket rate limiting for external API calls.

AUTONOMOUS PRINCIPLE: Self-throttling to prevent API bans.
The system automatically queues and paces requests to respect
API rate limits without dropping requests.

MISSION-CRITICAL STANDARD: Zero-Ban Operation
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, TypeVar, Callable, Awaitable, Any
from functools import wraps
from enum import Enum

from mercury.core.logging import get_logger

logger = get_logger("mercury.rate_limiter")

T = TypeVar("T")


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded and blocking is disabled."""
    
    def __init__(self, message: str, retry_after: float):
        super().__init__(message)
        self.retry_after = retry_after


@dataclass
class RateLimitStats:
    """Statistics for a rate limiter."""
    total_requests: int = 0
    total_waited_ms: float = 0
    total_rejected: int = 0
    max_wait_ms: float = 0
    last_request_time: Optional[datetime] = None
    
    @property
    def avg_wait_ms(self) -> float:
        """Average wait time per request."""
        if self.total_requests == 0:
            return 0.0
        return self.total_waited_ms / self.total_requests


class TokenBucketRateLimiter:
    """
    Async-safe token bucket rate limiter.
    
    AUTONOMOUS PRINCIPLE: Self-throttling to prevent API bans.
    
    The token bucket algorithm allows for bursting while maintaining
    a long-term rate limit. Tokens are added at a fixed rate, and
    each request consumes one token.
    
    Example:
        limiter = TokenBucketRateLimiter(rate=1.0, burst=1)  # 1 req/sec
        
        async with limiter:
            await call_api()
    
    Or with decorator:
        @limiter.limit
        async def call_api():
            ...
    """
    
    def __init__(
        self,
        rate: float,
        burst: int = 1,
        blocking: bool = True,
        max_wait: float = 60.0,
    ):
        """
        Initialize rate limiter.
        
        Args:
            rate: Tokens per second (e.g., 1.0 = 1 request per second)
            burst: Maximum tokens in bucket (allows bursting)
            blocking: If True, wait for tokens. If False, raise exception.
            max_wait: Maximum seconds to wait for a token
        """
        self.rate = rate
        self.burst = burst
        self.blocking = blocking
        self.max_wait = max_wait
        
        self._tokens = float(burst)
        self._last_update = time.monotonic()
        self._lock = asyncio.Lock()
        self._stats = RateLimitStats()
    
    @property
    def stats(self) -> RateLimitStats:
        """Get rate limiter statistics."""
        return self._stats
    
    @property
    def available_tokens(self) -> float:
        """Get current available tokens (approximate, not locked)."""
        elapsed = time.monotonic() - self._last_update
        return min(self._tokens + elapsed * self.rate, self.burst)
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_update
        self._tokens = min(self._tokens + elapsed * self.rate, self.burst)
        self._last_update = now
    
    async def acquire(self, tokens: int = 1) -> float:
        """
        Acquire tokens, waiting if necessary.
        
        Args:
            tokens: Number of tokens to acquire
            
        Returns:
            Time waited in seconds
            
        Raises:
            RateLimitExceeded: If blocking=False and no tokens available
        """
        start_time = time.monotonic()
        total_wait = 0.0
        
        async with self._lock:
            self._refill()
            
            while self._tokens < tokens:
                if not self.blocking:
                    wait_time = (tokens - self._tokens) / self.rate
                    raise RateLimitExceeded(
                        f"Rate limit exceeded, retry after {wait_time:.2f}s",
                        retry_after=wait_time,
                    )
                
                # Calculate wait time
                wait_needed = (tokens - self._tokens) / self.rate
                
                if total_wait + wait_needed > self.max_wait:
                    raise RateLimitExceeded(
                        f"Rate limit wait exceeded max_wait of {self.max_wait}s",
                        retry_after=wait_needed,
                    )
                
                # Wait and refill
                await asyncio.sleep(min(wait_needed, 1.0))  # Wait in chunks
                total_wait += min(wait_needed, 1.0)
                self._refill()
            
            # Consume tokens
            self._tokens -= tokens
            
            # Update stats
            self._stats.total_requests += 1
            self._stats.last_request_time = datetime.now(timezone.utc)
            
            if total_wait > 0:
                wait_ms = total_wait * 1000
                self._stats.total_waited_ms += wait_ms
                self._stats.max_wait_ms = max(self._stats.max_wait_ms, wait_ms)
                
                logger.debug(
                    f"Rate limiter waited {wait_ms:.1f}ms",
                    context={"tokens_remaining": self._tokens}
                )
        
        return total_wait
    
    async def __aenter__(self) -> "TokenBucketRateLimiter":
        """Async context manager entry - acquires a token."""
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        pass
    
    def limit(
        self,
        func: Callable[..., Awaitable[T]],
    ) -> Callable[..., Awaitable[T]]:
        """
        Decorator to rate limit an async function.
        
        Usage:
            @limiter.limit
            async def call_api():
                ...
        """
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            await self.acquire()
            return await func(*args, **kwargs)
        
        return wrapper
    
    def reset(self) -> None:
        """Reset the rate limiter to full burst capacity."""
        self._tokens = float(self.burst)
        self._last_update = time.monotonic()
        logger.debug("Rate limiter reset")
    
    def get_status(self) -> dict:
        """Get rate limiter status for API."""
        return {
            "rate": self.rate,
            "burst": self.burst,
            "available_tokens": round(self.available_tokens, 2),
            "blocking": self.blocking,
            "stats": {
                "total_requests": self._stats.total_requests,
                "avg_wait_ms": round(self._stats.avg_wait_ms, 2),
                "max_wait_ms": round(self._stats.max_wait_ms, 2),
                "total_rejected": self._stats.total_rejected,
            }
        }


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter for longer time windows.
    
    Better for rate limits like "60 requests per minute" where
    we need to track requests over a sliding time window.
    
    Example:
        limiter = SlidingWindowRateLimiter(limit=60, window_seconds=60)
    """
    
    def __init__(
        self,
        limit: int,
        window_seconds: float,
        blocking: bool = True,
    ):
        """
        Initialize sliding window rate limiter.
        
        Args:
            limit: Maximum requests in the window
            window_seconds: Window size in seconds
            blocking: If True, wait for capacity. If False, raise exception.
        """
        self.limit = limit
        self.window_seconds = window_seconds
        self.blocking = blocking
        
        self._timestamps: list[float] = []
        self._lock = asyncio.Lock()
        self._stats = RateLimitStats()
    
    @property
    def stats(self) -> RateLimitStats:
        """Get rate limiter statistics."""
        return self._stats
    
    def _clean_old_timestamps(self) -> None:
        """Remove timestamps outside the current window."""
        cutoff = time.monotonic() - self.window_seconds
        self._timestamps = [ts for ts in self._timestamps if ts > cutoff]
    
    @property
    def current_count(self) -> int:
        """Get current request count in window (approximate)."""
        cutoff = time.monotonic() - self.window_seconds
        return len([ts for ts in self._timestamps if ts > cutoff])
    
    @property
    def available_capacity(self) -> int:
        """Get available capacity (approximate)."""
        return max(0, self.limit - self.current_count)
    
    async def acquire(self) -> float:
        """
        Acquire permission for a request.
        
        Returns:
            Time waited in seconds
            
        Raises:
            RateLimitExceeded: If blocking=False and at capacity
        """
        start_time = time.monotonic()
        total_wait = 0.0
        
        async with self._lock:
            self._clean_old_timestamps()
            
            while len(self._timestamps) >= self.limit:
                if not self.blocking:
                    # Calculate when oldest will expire
                    oldest = min(self._timestamps)
                    retry_after = (oldest + self.window_seconds) - time.monotonic()
                    raise RateLimitExceeded(
                        f"Rate limit of {self.limit}/{self.window_seconds}s exceeded",
                        retry_after=max(0.1, retry_after),
                    )
                
                # Wait for oldest to expire
                oldest = min(self._timestamps)
                wait_time = (oldest + self.window_seconds) - time.monotonic()
                
                if wait_time > 0:
                    await asyncio.sleep(min(wait_time + 0.01, 1.0))
                    total_wait += min(wait_time + 0.01, 1.0)
                
                self._clean_old_timestamps()
            
            # Record this request
            self._timestamps.append(time.monotonic())
            
            # Update stats
            self._stats.total_requests += 1
            self._stats.last_request_time = datetime.now(timezone.utc)
            
            if total_wait > 0:
                wait_ms = total_wait * 1000
                self._stats.total_waited_ms += wait_ms
                self._stats.max_wait_ms = max(self._stats.max_wait_ms, wait_ms)
        
        return total_wait
    
    async def __aenter__(self) -> "SlidingWindowRateLimiter":
        """Async context manager entry."""
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        pass
    
    def limit(
        self,
        func: Callable[..., Awaitable[T]],
    ) -> Callable[..., Awaitable[T]]:
        """Decorator to rate limit an async function."""
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            await self.acquire()
            return await func(*args, **kwargs)
        
        return wrapper
    
    def get_status(self) -> dict:
        """Get rate limiter status for API."""
        return {
            "limit": self.limit,
            "window_seconds": self.window_seconds,
            "current_count": self.current_count,
            "available_capacity": self.available_capacity,
            "blocking": self.blocking,
            "stats": {
                "total_requests": self._stats.total_requests,
                "avg_wait_ms": round(self._stats.avg_wait_ms, 2),
                "max_wait_ms": round(self._stats.max_wait_ms, 2),
            }
        }


# ============================================================================
# PRE-CONFIGURED RATE LIMITERS FOR MERCURY
# ============================================================================

# Kite API: 1 request per second
kite_limiter = TokenBucketRateLimiter(
    rate=1.0,  # 1 token per second
    burst=3,   # Allow small bursts
    blocking=True,
    max_wait=30.0,
)

# Anthropic API: 60 requests per minute
anthropic_limiter = SlidingWindowRateLimiter(
    limit=60,
    window_seconds=60,
    blocking=True,
)


def get_kite_limiter() -> TokenBucketRateLimiter:
    """Get the Kite API rate limiter."""
    return kite_limiter


def get_anthropic_limiter() -> SlidingWindowRateLimiter:
    """Get the Anthropic API rate limiter."""
    return anthropic_limiter


def get_all_limiter_status() -> dict:
    """Get status of all rate limiters."""
    return {
        "kite": kite_limiter.get_status(),
        "anthropic": anthropic_limiter.get_status(),
    }
