"""
Mercury Background Health Monitor
==================================

Continuous background monitoring with auto-recovery.

AUTONOMOUS PRINCIPLE: Continuous observability.
The system continuously monitors its own health and recovers
from degradation without human intervention.

MISSION-CRITICAL STANDARD: Self-Healing Infrastructure
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Callable, Awaitable, Any
import weakref

from mercury.core.logging import get_logger
from mercury.core.health import get_system_health, HealthStatus, SystemHealth
from mercury.core.resilience import (
    kite_circuit,
    ai_circuit,
    CircuitState,
    degradation,
    DegradationLevel,
)

logger = get_logger("mercury.monitor")


class MonitorState(Enum):
    """State of the monitor."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


@dataclass
class HealthEvent:
    """Event emitted when health status changes."""
    timestamp: datetime
    previous_status: HealthStatus
    current_status: HealthStatus
    component: Optional[str] = None
    message: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for WebSocket transmission."""
        return {
            "type": "health_change",
            "timestamp": self.timestamp.isoformat(),
            "previous_status": self.previous_status.value,
            "current_status": self.current_status.value,
            "component": self.component,
            "message": self.message,
        }


@dataclass 
class CircuitEvent:
    """Event emitted when circuit breaker state changes."""
    timestamp: datetime
    circuit_name: str
    previous_state: CircuitState
    current_state: CircuitState
    
    def to_dict(self) -> dict:
        """Convert to dictionary for WebSocket transmission."""
        return {
            "type": "circuit_change",
            "timestamp": self.timestamp.isoformat(),
            "circuit": self.circuit_name,
            "previous_state": self.previous_state.value,
            "current_state": self.current_state.value,
        }


class HealthMonitor:
    """
    Background health monitoring with auto-recovery.
    
    AUTONOMOUS PRINCIPLE: Continuous observability.
    
    Features:
    - Periodic health checks (configurable interval)
    - Circuit breaker state monitoring
    - WebSocket broadcasting to connected clients
    - Adaptive check intervals based on health
    - Event-driven architecture for decoupling
    """
    
    # Check intervals in seconds
    NORMAL_INTERVAL = 30
    DEGRADED_INTERVAL = 10
    UNHEALTHY_INTERVAL = 5
    
    def __init__(self):
        """Initialize the health monitor."""
        self._state = MonitorState.STOPPED
        self._task: Optional[asyncio.Task] = None
        self._interval = self.NORMAL_INTERVAL
        
        # Use weak references to prevent memory leaks
        self._subscribers: list[weakref.ref] = []
        
        # Track previous states for change detection
        self._last_health_status: Optional[HealthStatus] = None
        self._last_circuit_states: dict[str, CircuitState] = {}
        
        # Callbacks for specific events
        self._on_degradation_callbacks: list[Callable[[DegradationLevel], Awaitable[None]]] = []
        self._on_recovery_callbacks: list[Callable[[], Awaitable[None]]] = []
        
        # Health history for trending
        self._health_history: list[tuple[datetime, HealthStatus]] = []
        self._max_history = 100
    
    @property
    def state(self) -> MonitorState:
        """Get monitor state."""
        return self._state
    
    @property
    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self._state == MonitorState.RUNNING
    
    async def start(self) -> None:
        """Start the background monitor."""
        if self._state == MonitorState.RUNNING:
            logger.warning("Monitor already running")
            return
        
        self._state = MonitorState.RUNNING
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Health monitor started", context={"interval": self._interval})
    
    async def stop(self) -> None:
        """Stop the background monitor."""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        
        self._state = MonitorState.STOPPED
        logger.info("Health monitor stopped")
    
    def pause(self) -> None:
        """Pause monitoring (task keeps running but skips checks)."""
        self._state = MonitorState.PAUSED
        logger.info("Health monitor paused")
    
    def resume(self) -> None:
        """Resume monitoring after pause."""
        if self._state == MonitorState.PAUSED:
            self._state = MonitorState.RUNNING
            logger.info("Health monitor resumed")
    
    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        logger.info("Monitor loop started")
        
        while self._state != MonitorState.STOPPED:
            try:
                if self._state == MonitorState.RUNNING:
                    await self._perform_check()
                
                await asyncio.sleep(self._interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                await asyncio.sleep(self._interval)
        
        logger.info("Monitor loop ended")
    
    async def _perform_check(self) -> None:
        """Perform a health check cycle."""
        try:
            # Get current health
            health = await get_system_health()
            
            # Record in history
            self._health_history.append((datetime.now(timezone.utc), health.status))
            if len(self._health_history) > self._max_history:
                self._health_history.pop(0)
            
            # Check for health status changes
            if self._last_health_status and health.status != self._last_health_status:
                event = HealthEvent(
                    timestamp=datetime.now(timezone.utc),
                    previous_status=self._last_health_status,
                    current_status=health.status,
                    message=self._get_status_change_message(
                        self._last_health_status, health.status
                    ),
                )
                await self._broadcast_event(event)
                
                # Trigger callbacks
                if health.status == HealthStatus.HEALTHY and self._last_health_status != HealthStatus.HEALTHY:
                    await self._emit_recovery()
                elif health.status != HealthStatus.HEALTHY and self._last_health_status == HealthStatus.HEALTHY:
                    await self._emit_degradation(degradation.current_level)
            
            self._last_health_status = health.status
            
            # Check circuit breaker states
            await self._check_circuits()
            
            # Adjust interval based on health
            self._adjust_interval(health.status)
            
            # Broadcast current health to subscribers
            await self._broadcast_health(health)
            
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    async def _check_circuits(self) -> None:
        """Check circuit breaker states for changes."""
        circuits = {
            "kite_api": kite_circuit,
            "anthropic_api": ai_circuit,
        }
        
        for name, circuit in circuits.items():
            current_state = circuit.state
            previous_state = self._last_circuit_states.get(name)
            
            if previous_state and current_state != previous_state:
                event = CircuitEvent(
                    timestamp=datetime.now(timezone.utc),
                    circuit_name=name,
                    previous_state=previous_state,
                    current_state=current_state,
                )
                await self._broadcast_event(event)
                
                # Log significant transitions
                if current_state == CircuitState.OPEN:
                    logger.warning(
                        f"Circuit {name} OPENED",
                        context={"from": previous_state.value}
                    )
                elif current_state == CircuitState.CLOSED and previous_state == CircuitState.OPEN:
                    logger.info(
                        f"Circuit {name} RECOVERED",
                        context={"from": previous_state.value}
                    )
            
            self._last_circuit_states[name] = current_state
    
    def _adjust_interval(self, status: HealthStatus) -> None:
        """Adjust check interval based on health status."""
        if status == HealthStatus.HEALTHY:
            new_interval = self.NORMAL_INTERVAL
        elif status == HealthStatus.DEGRADED:
            new_interval = self.DEGRADED_INTERVAL
        else:
            new_interval = self.UNHEALTHY_INTERVAL
        
        if new_interval != self._interval:
            logger.info(
                f"Adjusting monitor interval: {self._interval}s -> {new_interval}s",
                context={"status": status.value}
            )
            self._interval = new_interval
    
    def _get_status_change_message(
        self,
        previous: HealthStatus,
        current: HealthStatus,
    ) -> str:
        """Generate human-readable message for status change."""
        if current == HealthStatus.HEALTHY:
            return "System fully recovered"
        elif current == HealthStatus.DEGRADED:
            if previous == HealthStatus.HEALTHY:
                return "System degraded - some features may be unavailable"
            else:
                return "System partially recovered but still degraded"
        else:
            return "System unhealthy - limited functionality"
    
    # =========================================================================
    # SUBSCRIBER MANAGEMENT
    # =========================================================================
    
    def subscribe(self, subscriber: Any) -> None:
        """
        Subscribe to health events.
        
        Subscriber must have an async `send_json` method (like WebSocket).
        Uses weak references to prevent memory leaks.
        """
        # Clean up dead references
        self._subscribers = [ref for ref in self._subscribers if ref() is not None]
        
        # Add new subscriber
        self._subscribers.append(weakref.ref(subscriber))
        logger.debug(f"Subscriber added, total: {len(self._subscribers)}")
    
    def unsubscribe(self, subscriber: Any) -> None:
        """Unsubscribe from health events."""
        self._subscribers = [
            ref for ref in self._subscribers 
            if ref() is not None and ref() is not subscriber
        ]
    
    async def _broadcast_event(self, event: HealthEvent | CircuitEvent) -> None:
        """Broadcast an event to all subscribers."""
        data = event.to_dict()
        await self._broadcast(data)
    
    async def _broadcast_health(self, health: SystemHealth) -> None:
        """Broadcast current health status."""
        data = {
            "type": "health_update",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "health": health.to_dict(),
        }
        await self._broadcast(data)
    
    async def _broadcast(self, data: dict) -> None:
        """Broadcast data to all subscribers."""
        dead_refs = []
        
        for ref in self._subscribers:
            subscriber = ref()
            if subscriber is None:
                dead_refs.append(ref)
                continue
            
            try:
                await subscriber.send_json(data)
            except Exception as e:
                logger.debug(f"Failed to send to subscriber: {e}")
                dead_refs.append(ref)
        
        # Clean up dead references
        for ref in dead_refs:
            self._subscribers.remove(ref)
    
    # =========================================================================
    # CALLBACK MANAGEMENT
    # =========================================================================
    
    def on_degradation(
        self,
        callback: Callable[[DegradationLevel], Awaitable[None]],
    ) -> None:
        """Register callback for when system degrades."""
        self._on_degradation_callbacks.append(callback)
    
    def on_recovery(
        self,
        callback: Callable[[], Awaitable[None]],
    ) -> None:
        """Register callback for when system recovers."""
        self._on_recovery_callbacks.append(callback)
    
    async def _emit_degradation(self, level: DegradationLevel) -> None:
        """Emit degradation event."""
        for callback in self._on_degradation_callbacks:
            try:
                await callback(level)
            except Exception as e:
                logger.error(f"Degradation callback error: {e}")
    
    async def _emit_recovery(self) -> None:
        """Emit recovery event."""
        for callback in self._on_recovery_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error(f"Recovery callback error: {e}")
    
    # =========================================================================
    # STATUS & METRICS
    # =========================================================================
    
    def get_status(self) -> dict:
        """Get monitor status for API."""
        return {
            "state": self._state.value,
            "interval_seconds": self._interval,
            "subscribers": len([r for r in self._subscribers if r() is not None]),
            "last_health_status": self._last_health_status.value if self._last_health_status else None,
            "circuit_states": {
                name: state.value 
                for name, state in self._last_circuit_states.items()
            },
            "history_size": len(self._health_history),
        }
    
    def get_health_trend(self, minutes: int = 10) -> dict:
        """Get health trend over the last N minutes."""
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        
        recent = [
            (ts, status) 
            for ts, status in self._health_history 
            if ts >= cutoff
        ]
        
        if not recent:
            return {"trend": "unknown", "samples": 0}
        
        # Calculate health score (1 = healthy, 0.5 = degraded, 0 = unhealthy)
        scores = []
        for _, status in recent:
            if status == HealthStatus.HEALTHY:
                scores.append(1.0)
            elif status == HealthStatus.DEGRADED:
                scores.append(0.5)
            else:
                scores.append(0.0)
        
        avg_score = sum(scores) / len(scores)
        
        # Determine trend
        if len(scores) >= 3:
            first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
            
            if second_half > first_half + 0.1:
                trend = "improving"
            elif second_half < first_half - 0.1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "trend": trend,
            "avg_score": round(avg_score, 2),
            "samples": len(recent),
            "minutes": minutes,
        }


# Global monitor instance
_monitor: Optional[HealthMonitor] = None


def get_health_monitor() -> HealthMonitor:
    """Get or create the global health monitor."""
    global _monitor
    if _monitor is None:
        _monitor = HealthMonitor()
    return _monitor


async def start_health_monitor() -> None:
    """Start the global health monitor."""
    monitor = get_health_monitor()
    await monitor.start()


async def stop_health_monitor() -> None:
    """Stop the global health monitor."""
    monitor = get_health_monitor()
    await monitor.stop()
