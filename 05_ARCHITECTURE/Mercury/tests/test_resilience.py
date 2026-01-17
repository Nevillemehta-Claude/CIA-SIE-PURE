"""
Tests for Mercury Resilience Patterns
=====================================

Tests for circuit breakers, retries, and graceful degradation.
"""

import asyncio
import pytest
from mercury.core.resilience import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    CircuitOpenError,
    RetryConfig,
    retry_async,
    GracefulDegradation,
    DegradationLevel,
    get_circuit_breaker,
)


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""
    
    def test_initial_state_closed(self):
        """Should start in closed state."""
        breaker = CircuitBreaker("test")
        assert breaker.state == CircuitState.CLOSED
    
    def test_allows_requests_when_closed(self):
        """Should allow requests when closed."""
        breaker = CircuitBreaker("test")
        assert breaker.allow_request() is True
    
    def test_opens_after_failures(self):
        """Should open after failure threshold."""
        config = CircuitBreakerConfig(failure_threshold=3)
        breaker = CircuitBreaker("test", config)
        
        # Record failures
        for _ in range(3):
            breaker.record_failure()
        
        assert breaker.state == CircuitState.OPEN
        assert breaker.allow_request() is False
    
    def test_resets_on_success(self):
        """Should reset failure count on success."""
        config = CircuitBreakerConfig(failure_threshold=3)
        breaker = CircuitBreaker("test", config)
        
        breaker.record_failure()
        breaker.record_failure()
        assert breaker.stats.failure_count == 2
        
        breaker.record_success()
        assert breaker.stats.failure_count == 0
    
    def test_manual_reset(self):
        """Should be manually resettable."""
        breaker = CircuitBreaker("test")
        breaker.record_failure()
        breaker.record_failure()
        breaker.record_failure()
        breaker.record_failure()
        breaker.record_failure()
        
        assert breaker.state == CircuitState.OPEN
        
        breaker.reset()
        assert breaker.state == CircuitState.CLOSED
        assert breaker.stats.failure_count == 0
    
    def test_health_report(self):
        """Should provide health information."""
        breaker = CircuitBreaker("test_circuit")
        breaker.record_success()
        breaker.record_failure()
        
        health = breaker.get_health()
        
        assert health["name"] == "test_circuit"
        assert health["state"] == "closed"
        assert health["success_count"] == 1
        assert health["failure_count"] == 1
    
    def test_protect_decorator_sync(self):
        """Should protect sync functions."""
        breaker = CircuitBreaker("test")
        
        @breaker.protect
        def my_func():
            return "success"
        
        result = my_func()
        assert result == "success"
        assert breaker.stats.success_count == 1
    
    def test_protect_decorator_failure(self):
        """Should record failure on exception."""
        breaker = CircuitBreaker("test")
        
        @breaker.protect
        def failing_func():
            raise ValueError("test error")
        
        with pytest.raises(ValueError):
            failing_func()
        
        assert breaker.stats.failure_count == 1


class TestCircuitBreakerAsync:
    """Async tests for CircuitBreaker."""
    
    @pytest.mark.asyncio
    async def test_protect_async_function(self):
        """Should protect async functions."""
        breaker = CircuitBreaker("test")
        
        @breaker.protect
        async def async_func():
            await asyncio.sleep(0.01)
            return "async success"
        
        result = await async_func()
        assert result == "async success"
        assert breaker.stats.success_count == 1
    
    @pytest.mark.asyncio
    async def test_rejects_when_open(self):
        """Should reject requests when open."""
        config = CircuitBreakerConfig(failure_threshold=1)
        breaker = CircuitBreaker("test", config)
        breaker.record_failure()
        
        @breaker.protect
        async def async_func():
            return "should not run"
        
        with pytest.raises(CircuitOpenError):
            await async_func()


class TestRetryAsync:
    """Tests for retry_async function."""
    
    @pytest.mark.asyncio
    async def test_succeeds_on_first_try(self):
        """Should return immediately on success."""
        call_count = 0
        
        async def func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = await retry_async(func)
        assert result == "success"
        assert call_count == 1
    
    @pytest.mark.asyncio
    async def test_retries_on_failure(self):
        """Should retry on failure."""
        call_count = 0
        
        async def func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("failing")
            return "success"
        
        config = RetryConfig(max_attempts=3, initial_delay_seconds=0.01)
        result = await retry_async(func, config)
        
        assert result == "success"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_exhausts_retries(self):
        """Should raise after exhausting retries."""
        call_count = 0
        
        async def func():
            nonlocal call_count
            call_count += 1
            raise ValueError("always fails")
        
        config = RetryConfig(max_attempts=3, initial_delay_seconds=0.01)
        
        with pytest.raises(ValueError):
            await retry_async(func, config)
        
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_on_retry_callback(self):
        """Should call on_retry callback."""
        retries = []
        
        async def func():
            if len(retries) < 2:
                raise ValueError("retry me")
            return "success"
        
        def on_retry(attempt, exc):
            retries.append((attempt, str(exc)))
        
        config = RetryConfig(max_attempts=3, initial_delay_seconds=0.01)
        result = await retry_async(func, config, on_retry=on_retry)
        
        assert result == "success"
        assert len(retries) == 2


class TestGracefulDegradation:
    """Tests for GracefulDegradation class."""
    
    def test_initial_state(self):
        """Should start with full capability."""
        degradation = GracefulDegradation()
        assert degradation.current_level == DegradationLevel.FULL
    
    def test_get_capabilities(self):
        """Should return capability dict."""
        degradation = GracefulDegradation()
        caps = degradation.get_capabilities()
        
        assert "live_quotes" in caps
        assert "ai_analysis" in caps
        assert "conversation" in caps
    
    def test_status_message(self):
        """Should provide status message."""
        degradation = GracefulDegradation()
        message = degradation.get_status_message()
        assert "operational" in message.lower()


class TestGetCircuitBreaker:
    """Tests for circuit breaker factory."""
    
    def test_creates_new_breaker(self):
        """Should create new circuit breaker."""
        breaker = get_circuit_breaker("unique_test_name")
        assert breaker.name == "unique_test_name"
    
    def test_returns_same_instance(self):
        """Should return same instance for same name."""
        breaker1 = get_circuit_breaker("shared_name")
        breaker2 = get_circuit_breaker("shared_name")
        assert breaker1 is breaker2
