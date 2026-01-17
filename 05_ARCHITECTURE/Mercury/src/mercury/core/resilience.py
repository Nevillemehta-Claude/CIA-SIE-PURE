"""
Mercury Resilience Patterns
===========================

Circuit breakers, retries, and graceful degradation.

MISSION-CRITICAL STANDARD: Resilience Pillar
- Circuit breaker for external services
- Graceful degradation hierarchy
- Retry with exponential backoff
- Health monitoring
"""

import asyncio
import inspect
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from mercury.core.logging import get_logger

logger = get_logger("mercury.resilience")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, rejecting calls
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class CircuitStats:
    """Statistics for a circuit breaker."""
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    total_requests: int = 0
    total_failures: int = 0
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate as percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.total_failures / self.total_requests) * 100


@dataclass
class CircuitBreakerConfig:
    """Configuration for a circuit breaker."""
    failure_threshold: int = 5       # Failures before opening
    success_threshold: int = 3       # Successes to close from half-open
    timeout_seconds: float = 30.0    # Time before trying half-open
    half_open_max_calls: int = 1     # Max calls in half-open state


class CircuitBreaker:
    """
    Circuit breaker for external service calls.
    
    Prevents cascade failures by failing fast when a service is down.
    
    Usage:
        breaker = CircuitBreaker("kite_api")
        
        @breaker.protect
        async def call_kite():
            ...
            
        # Or manually
        if breaker.allow_request():
            try:
                result = await call_external()
                breaker.record_success()
            except Exception:
                breaker.record_failure()
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None,
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.stats = CircuitStats()
        self._half_open_calls = 0
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self.stats.state
    
    def allow_request(self) -> bool:
        """
        Check if a request should be allowed.
        
        Returns:
            True if request should proceed, False if circuit is open
        """
        if self.stats.state == CircuitState.CLOSED:
            return True
        
        if self.stats.state == CircuitState.OPEN:
            # Check if timeout has elapsed
            if self.stats.last_failure_time:
                elapsed = (datetime.now(timezone.utc) - self.stats.last_failure_time).total_seconds()
                if elapsed >= self.config.timeout_seconds:
                    self._transition_to_half_open()
                    return True
            return False
        
        if self.stats.state == CircuitState.HALF_OPEN:
            # Allow limited calls in half-open
            if self._half_open_calls < self.config.half_open_max_calls:
                self._half_open_calls += 1
                return True
            return False
        
        return False
    
    def record_success(self) -> None:
        """Record a successful call."""
        self.stats.success_count += 1
        self.stats.total_requests += 1
        self.stats.last_success_time = datetime.now(timezone.utc)
        
        if self.stats.state == CircuitState.HALF_OPEN:
            if self.stats.success_count >= self.config.success_threshold:
                self._transition_to_closed()
        elif self.stats.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.stats.failure_count = 0
    
    def record_failure(self, error: Optional[Exception] = None) -> None:
        """Record a failed call."""
        self.stats.failure_count += 1
        self.stats.total_failures += 1
        self.stats.total_requests += 1
        self.stats.last_failure_time = datetime.now(timezone.utc)
        
        logger.warning(
            f"Circuit '{self.name}' recorded failure",
            context={
                "failure_count": self.stats.failure_count,
                "threshold": self.config.failure_threshold,
                "error": str(error) if error else None,
            }
        )
        
        if self.stats.state == CircuitState.HALF_OPEN:
            self._transition_to_open()
        elif self.stats.state == CircuitState.CLOSED:
            if self.stats.failure_count >= self.config.failure_threshold:
                self._transition_to_open()
    
    def _transition_to_open(self) -> None:
        """Transition to open state."""
        self.stats.state = CircuitState.OPEN
        self.stats.success_count = 0
        logger.warning(
            f"Circuit '{self.name}' OPENED - failing fast",
            context={"failure_count": self.stats.failure_count}
        )
    
    def _transition_to_half_open(self) -> None:
        """Transition to half-open state."""
        self.stats.state = CircuitState.HALF_OPEN
        self.stats.success_count = 0
        self._half_open_calls = 0
        logger.info(f"Circuit '{self.name}' half-open - testing")
    
    def _transition_to_closed(self) -> None:
        """Transition to closed state."""
        self.stats.state = CircuitState.CLOSED
        self.stats.failure_count = 0
        self._half_open_calls = 0
        logger.info(f"Circuit '{self.name}' CLOSED - recovered")
    
    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        self.stats = CircuitStats()
        self._half_open_calls = 0
        logger.info(f"Circuit '{self.name}' reset")
    
    def get_health(self) -> dict:
        """Get circuit health information."""
        return {
            "name": self.name,
            "state": self.stats.state.value,
            "failure_count": self.stats.failure_count,
            "success_count": self.stats.success_count,
            "failure_rate": round(self.stats.failure_rate, 2),
            "last_failure": self.stats.last_failure_time.isoformat() if self.stats.last_failure_time else None,
            "last_success": self.stats.last_success_time.isoformat() if self.stats.last_success_time else None,
        }
    
    def protect(self, func: Callable) -> Callable:
        """
        Decorator to protect a function with this circuit breaker.
        
        Works with both sync and async functions.
        """
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not self.allow_request():
                    raise CircuitOpenError(
                        f"Circuit '{self.name}' is open - request rejected"
                    )
                try:
                    result = await func(*args, **kwargs)
                    self.record_success()
                    return result
                except Exception as e:
                    self.record_failure(e)
                    raise
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                if not self.allow_request():
                    raise CircuitOpenError(
                        f"Circuit '{self.name}' is open - request rejected"
                    )
                try:
                    result = func(*args, **kwargs)
                    self.record_success()
                    return result
                except Exception as e:
                    self.record_failure(e)
                    raise
            return sync_wrapper


class CircuitOpenError(Exception):
    """Raised when circuit is open and rejecting requests."""
    pass


# Global circuit breakers for Mercury services
_circuit_breakers: dict[str, CircuitBreaker] = {}


def get_circuit_breaker(
    name: str,
    config: Optional[CircuitBreakerConfig] = None,
) -> CircuitBreaker:
    """Get or create a named circuit breaker."""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, config)
    return _circuit_breakers[name]


def get_all_circuit_health() -> dict[str, dict]:
    """Get health of all circuit breakers."""
    return {name: cb.get_health() for name, cb in _circuit_breakers.items()}


# Pre-configured circuit breakers for Mercury
kite_circuit = get_circuit_breaker(
    "kite_api",
    CircuitBreakerConfig(
        failure_threshold=3,      # Open after 3 failures
        success_threshold=2,      # Close after 2 successes
        timeout_seconds=60.0,     # Try again after 1 minute
    )
)

ai_circuit = get_circuit_breaker(
    "anthropic_api",
    CircuitBreakerConfig(
        failure_threshold=5,      # More tolerant
        success_threshold=3,
        timeout_seconds=30.0,     # Faster retry
    )
)


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True


async def retry_async(
    func: Callable,
    config: Optional[RetryConfig] = None,
    on_retry: Optional[Callable[[int, Exception], None]] = None,
) -> Any:
    """
    Retry an async function with exponential backoff.
    
    Args:
        func: Async callable to retry
        config: Retry configuration
        on_retry: Optional callback on each retry
        
    Returns:
        Result from successful call
        
    Raises:
        Last exception if all retries fail
    """
    config = config or RetryConfig()
    last_exception: Optional[Exception] = None
    
    for attempt in range(1, config.max_attempts + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            
            if attempt == config.max_attempts:
                break
            
            # Calculate delay with exponential backoff
            delay = min(
                config.initial_delay_seconds * (config.exponential_base ** (attempt - 1)),
                config.max_delay_seconds
            )
            
            # Add jitter to prevent thundering herd
            if config.jitter:
                import random
                delay = delay * (0.5 + random.random())
            
            if on_retry:
                on_retry(attempt, e)
            
            logger.warning(
                f"Retry {attempt}/{config.max_attempts} after {delay:.2f}s",
                context={"error": str(e)}
            )
            
            await asyncio.sleep(delay)
    
    raise last_exception


class DegradationLevel(Enum):
    """Levels of service degradation."""
    FULL = "full"           # Full functionality
    REDUCED = "reduced"     # Some features disabled
    MINIMAL = "minimal"     # Basic functionality only
    OFFLINE = "offline"     # No external services


@dataclass
class GracefulDegradation:
    """
    Manages graceful degradation of service.
    
    When external services fail, progressively degrade
    functionality while maintaining core operations.
    """
    
    current_level: DegradationLevel = DegradationLevel.FULL
    kite_available: bool = True
    ai_available: bool = True
    
    def assess(self) -> DegradationLevel:
        """Assess current degradation level based on service availability."""
        kite_health = kite_circuit.state
        ai_health = ai_circuit.state
        
        self.kite_available = kite_health != CircuitState.OPEN
        self.ai_available = ai_health != CircuitState.OPEN
        
        if self.kite_available and self.ai_available:
            self.current_level = DegradationLevel.FULL
        elif self.kite_available or self.ai_available:
            self.current_level = DegradationLevel.REDUCED
        else:
            self.current_level = DegradationLevel.OFFLINE
        
        return self.current_level
    
    def get_capabilities(self) -> dict[str, bool]:
        """Get available capabilities at current level."""
        self.assess()
        
        return {
            "live_quotes": self.kite_available,
            "ai_analysis": self.ai_available,
            "portfolio_data": self.kite_available,
            "recommendations": self.ai_available,
            "historical_data": self.kite_available,
            "conversation": True,  # Always available (local)
            "cached_data": True,   # Always available (local)
        }
    
    def get_status_message(self) -> str:
        """Get human-readable status message."""
        self.assess()
        
        if self.current_level == DegradationLevel.FULL:
            return "All systems operational"
        elif self.current_level == DegradationLevel.REDUCED:
            unavailable = []
            if not self.kite_available:
                unavailable.append("market data")
            if not self.ai_available:
                unavailable.append("AI analysis")
            return f"Operating in reduced mode. Unavailable: {', '.join(unavailable)}"
        else:
            return "Offline mode - external services unavailable"


# Global degradation manager
degradation = GracefulDegradation()
