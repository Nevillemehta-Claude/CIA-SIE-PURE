"""
Tests for Rate Limiter
======================

Tests for the token bucket and sliding window rate limiters.
"""

import pytest
import asyncio
import time
from datetime import datetime, timezone

from mercury.core.rate_limiter import (
    TokenBucketRateLimiter,
    SlidingWindowRateLimiter,
    RateLimitExceeded,
    get_kite_limiter,
    get_anthropic_limiter,
    get_all_limiter_status,
)


class TestTokenBucketRateLimiter:
    """Tests for TokenBucketRateLimiter."""
    
    @pytest.mark.asyncio
    async def test_acquire_immediate_when_tokens_available(self):
        """Test that acquire returns immediately when tokens are available."""
        limiter = TokenBucketRateLimiter(rate=10.0, burst=5)
        
        start = time.monotonic()
        await limiter.acquire()
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.1  # Should be nearly instant
    
    @pytest.mark.asyncio
    async def test_acquire_waits_when_no_tokens(self):
        """Test that acquire waits when no tokens available."""
        limiter = TokenBucketRateLimiter(rate=2.0, burst=1)  # 2 tokens/sec
        
        # Use the one token
        await limiter.acquire()
        
        # Next acquire should wait ~0.5 seconds
        start = time.monotonic()
        await limiter.acquire()
        elapsed = time.monotonic() - start
        
        assert elapsed >= 0.4  # Should wait about 0.5s
        assert elapsed < 1.0
    
    @pytest.mark.asyncio
    async def test_burst_allows_multiple_immediate(self):
        """Test that burst allows multiple immediate requests."""
        limiter = TokenBucketRateLimiter(rate=1.0, burst=5)
        
        start = time.monotonic()
        
        # Should be able to do 5 requests immediately
        for _ in range(5):
            await limiter.acquire()
        
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.2  # All 5 should be nearly instant
    
    @pytest.mark.asyncio
    async def test_non_blocking_raises_exception(self):
        """Test that non-blocking mode raises exception."""
        limiter = TokenBucketRateLimiter(rate=1.0, burst=1, blocking=False)
        
        # Use the one token
        await limiter.acquire()
        
        # Next should raise
        with pytest.raises(RateLimitExceeded):
            await limiter.acquire()
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager usage."""
        limiter = TokenBucketRateLimiter(rate=10.0, burst=5)
        
        async with limiter:
            pass  # Should work without error
        
        # Verify token was consumed
        assert limiter.available_tokens < 5
    
    @pytest.mark.asyncio
    async def test_decorator(self):
        """Test rate limit decorator."""
        limiter = TokenBucketRateLimiter(rate=10.0, burst=5)
        call_count = 0
        
        @limiter.limit
        async def limited_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = await limited_func()
        
        assert result == "success"
        assert call_count == 1
    
    def test_stats_tracking(self):
        """Test that stats are tracked correctly."""
        limiter = TokenBucketRateLimiter(rate=10.0, burst=5)
        
        assert limiter.stats.total_requests == 0
        
        asyncio.run(limiter.acquire())
        
        assert limiter.stats.total_requests == 1
        assert limiter.stats.last_request_time is not None
    
    def test_get_status(self):
        """Test status dictionary generation."""
        limiter = TokenBucketRateLimiter(rate=5.0, burst=3)
        
        status = limiter.get_status()
        
        assert status["rate"] == 5.0
        assert status["burst"] == 3
        assert "available_tokens" in status
        assert "stats" in status
    
    def test_reset(self):
        """Test reset functionality."""
        limiter = TokenBucketRateLimiter(rate=1.0, burst=5)
        
        # Use some tokens
        asyncio.run(limiter.acquire())
        asyncio.run(limiter.acquire())
        
        assert limiter.available_tokens < 5
        
        limiter.reset()
        
        assert limiter.available_tokens == 5.0


class TestSlidingWindowRateLimiter:
    """Tests for SlidingWindowRateLimiter."""
    
    @pytest.mark.asyncio
    async def test_acquire_under_limit(self):
        """Test acquire works when under limit."""
        limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60)
        
        start = time.monotonic()
        await limiter.acquire()
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.1
    
    @pytest.mark.asyncio
    async def test_respects_limit(self):
        """Test that limit is respected."""
        limiter = SlidingWindowRateLimiter(limit=3, window_seconds=1)
        
        # First 3 should be immediate
        for _ in range(3):
            await limiter.acquire()
        
        assert limiter.current_count == 3
        assert limiter.available_capacity == 0
    
    @pytest.mark.asyncio
    async def test_non_blocking_raises_at_limit(self):
        """Test non-blocking raises exception at limit."""
        limiter = SlidingWindowRateLimiter(limit=2, window_seconds=60, blocking=False)
        
        await limiter.acquire()
        await limiter.acquire()
        
        with pytest.raises(RateLimitExceeded):
            await limiter.acquire()
    
    @pytest.mark.asyncio
    async def test_window_expires(self):
        """Test that window expires and allows new requests."""
        limiter = SlidingWindowRateLimiter(limit=1, window_seconds=0.5)
        
        await limiter.acquire()
        
        # Wait for window to expire
        await asyncio.sleep(0.6)
        
        # Should be able to acquire again
        start = time.monotonic()
        await limiter.acquire()
        elapsed = time.monotonic() - start
        
        assert elapsed < 0.1
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager usage."""
        limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60)
        
        async with limiter:
            pass
        
        assert limiter.current_count == 1
    
    def test_get_status(self):
        """Test status dictionary generation."""
        limiter = SlidingWindowRateLimiter(limit=60, window_seconds=60)
        
        status = limiter.get_status()
        
        assert status["limit"] == 60
        assert status["window_seconds"] == 60
        assert "current_count" in status
        assert "available_capacity" in status


class TestPreConfiguredLimiters:
    """Tests for pre-configured rate limiters."""
    
    def test_kite_limiter_configured(self):
        """Test Kite limiter is properly configured."""
        limiter = get_kite_limiter()
        
        assert limiter.rate == 1.0  # 1 req/sec
        assert limiter.burst == 3
    
    def test_anthropic_limiter_configured(self):
        """Test Anthropic limiter is properly configured."""
        limiter = get_anthropic_limiter()
        
        assert limiter.limit == 60  # 60 req/min
        assert limiter.window_seconds == 60
    
    def test_get_all_limiter_status(self):
        """Test getting all limiter status."""
        status = get_all_limiter_status()
        
        assert "kite" in status
        assert "anthropic" in status


class TestRateLimitExceeded:
    """Tests for RateLimitExceeded exception."""
    
    def test_retry_after_included(self):
        """Test that retry_after is included in exception."""
        exc = RateLimitExceeded("Rate limited", retry_after=5.0)
        
        assert exc.retry_after == 5.0
        assert "Rate limited" in str(exc)
