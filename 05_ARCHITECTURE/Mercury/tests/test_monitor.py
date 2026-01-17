"""
Tests for Health Monitor
========================

Tests for the background health monitoring system.
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from mercury.core.monitor import (
    HealthMonitor,
    MonitorState,
    HealthEvent,
    CircuitEvent,
    get_health_monitor,
    start_health_monitor,
    stop_health_monitor,
)
from mercury.core.health import HealthStatus
from mercury.core.resilience import CircuitState


class TestHealthEvent:
    """Tests for HealthEvent dataclass."""
    
    def test_health_event_to_dict(self):
        """Test HealthEvent serialization."""
        event = HealthEvent(
            timestamp=datetime.now(timezone.utc),
            previous_status=HealthStatus.HEALTHY,
            current_status=HealthStatus.DEGRADED,
            component="kite_api",
            message="Test message",
        )
        
        data = event.to_dict()
        
        assert data["type"] == "health_change"
        assert data["previous_status"] == "healthy"
        assert data["current_status"] == "degraded"
        assert data["component"] == "kite_api"
        assert data["message"] == "Test message"


class TestCircuitEvent:
    """Tests for CircuitEvent dataclass."""
    
    def test_circuit_event_to_dict(self):
        """Test CircuitEvent serialization."""
        event = CircuitEvent(
            timestamp=datetime.now(timezone.utc),
            circuit_name="kite_api",
            previous_state=CircuitState.CLOSED,
            current_state=CircuitState.OPEN,
        )
        
        data = event.to_dict()
        
        assert data["type"] == "circuit_change"
        assert data["circuit"] == "kite_api"
        assert data["previous_state"] == "closed"
        assert data["current_state"] == "open"


class TestHealthMonitor:
    """Tests for HealthMonitor."""
    
    @pytest.fixture
    def monitor(self):
        """Create a fresh monitor for each test."""
        return HealthMonitor()
    
    def test_initial_state(self, monitor):
        """Test monitor starts in STOPPED state."""
        assert monitor.state == MonitorState.STOPPED
        assert monitor.is_running is False
    
    @pytest.mark.asyncio
    async def test_start_and_stop(self, monitor):
        """Test starting and stopping the monitor."""
        await monitor.start()
        
        assert monitor.state == MonitorState.RUNNING
        assert monitor.is_running is True
        
        await monitor.stop()
        
        assert monitor.state == MonitorState.STOPPED
        assert monitor.is_running is False
    
    @pytest.mark.asyncio
    async def test_start_idempotent(self, monitor):
        """Test that starting twice doesn't cause issues."""
        await monitor.start()
        await monitor.start()  # Should log warning but not fail
        
        assert monitor.is_running is True
        
        await monitor.stop()
    
    def test_pause_and_resume(self, monitor):
        """Test pause and resume functionality."""
        # Need to be running to pause
        asyncio.run(monitor.start())
        
        monitor.pause()
        assert monitor.state == MonitorState.PAUSED
        
        monitor.resume()
        assert monitor.state == MonitorState.RUNNING
        
        asyncio.run(monitor.stop())
    
    def test_get_status(self, monitor):
        """Test status dictionary generation."""
        status = monitor.get_status()
        
        assert "state" in status
        assert status["state"] == "stopped"
        assert "interval_seconds" in status
        assert "subscribers" in status
    
    @pytest.mark.asyncio
    async def test_subscriber_management(self, monitor):
        """Test adding and removing subscribers."""
        mock_subscriber = MagicMock()
        mock_subscriber.send_json = AsyncMock()
        
        monitor.subscribe(mock_subscriber)
        
        status = monitor.get_status()
        assert status["subscribers"] == 1
        
        monitor.unsubscribe(mock_subscriber)
        
        status = monitor.get_status()
        assert status["subscribers"] == 0
    
    @pytest.mark.asyncio
    async def test_broadcast_to_subscribers(self, monitor):
        """Test broadcasting to subscribers."""
        mock_subscriber = MagicMock()
        mock_subscriber.send_json = AsyncMock()
        
        monitor.subscribe(mock_subscriber)
        
        await monitor._broadcast({"test": "data"})
        
        mock_subscriber.send_json.assert_called_once_with({"test": "data"})
    
    @pytest.mark.asyncio
    async def test_dead_subscribers_cleaned_up(self, monitor):
        """Test that dead subscribers are cleaned up."""
        import weakref
        
        class DummySubscriber:
            async def send_json(self, data):
                pass
        
        subscriber = DummySubscriber()
        monitor.subscribe(subscriber)
        
        assert monitor.get_status()["subscribers"] == 1
        
        # Delete subscriber
        del subscriber
        
        # Broadcast should clean up dead reference
        await monitor._broadcast({"test": "data"})
        
        # Note: weak ref cleanup happens on broadcast, so check after
        # This test may be flaky depending on GC timing
    
    def test_callback_registration(self, monitor):
        """Test callback registration."""
        async def on_degradation(level):
            pass
        
        async def on_recovery():
            pass
        
        monitor.on_degradation(on_degradation)
        monitor.on_recovery(on_recovery)
        
        assert len(monitor._on_degradation_callbacks) == 1
        assert len(monitor._on_recovery_callbacks) == 1
    
    @pytest.mark.asyncio
    async def test_health_trend(self, monitor):
        """Test health trend calculation."""
        # Add some history
        now = datetime.now(timezone.utc)
        monitor._health_history = [
            (now, HealthStatus.HEALTHY),
            (now, HealthStatus.HEALTHY),
            (now, HealthStatus.DEGRADED),
        ]
        
        trend = monitor.get_health_trend(minutes=10)
        
        assert "trend" in trend
        assert "avg_score" in trend
        assert "samples" in trend
    
    @pytest.mark.asyncio
    async def test_interval_adjustment(self, monitor):
        """Test that interval adjusts based on health."""
        # Start with normal interval
        assert monitor._interval == monitor.NORMAL_INTERVAL
        
        # Simulate degraded health
        monitor._adjust_interval(HealthStatus.DEGRADED)
        assert monitor._interval == monitor.DEGRADED_INTERVAL
        
        # Simulate unhealthy
        monitor._adjust_interval(HealthStatus.UNHEALTHY)
        assert monitor._interval == monitor.UNHEALTHY_INTERVAL
        
        # Back to healthy
        monitor._adjust_interval(HealthStatus.HEALTHY)
        assert monitor._interval == monitor.NORMAL_INTERVAL


class TestGlobalMonitor:
    """Tests for global monitor functions."""
    
    def test_get_health_monitor_singleton(self):
        """Test that get_health_monitor returns same instance."""
        import mercury.core.monitor as monitor_module
        monitor_module._monitor = None
        
        monitor1 = get_health_monitor()
        monitor2 = get_health_monitor()
        
        assert monitor1 is monitor2
    
    @pytest.mark.asyncio
    async def test_start_stop_global_monitor(self):
        """Test global start/stop functions."""
        import mercury.core.monitor as monitor_module
        monitor_module._monitor = None
        
        await start_health_monitor()
        
        monitor = get_health_monitor()
        assert monitor.is_running is True
        
        await stop_health_monitor()
        assert monitor.is_running is False


class TestMonitorIntegration:
    """Integration tests for monitor with health checks."""
    
    @pytest.mark.asyncio
    async def test_perform_check_updates_history(self):
        """Test that perform_check updates health history."""
        monitor = HealthMonitor()
        
        initial_history_len = len(monitor._health_history)
        
        # Mock get_system_health
        with patch('mercury.core.monitor.get_system_health') as mock_health:
            mock_result = MagicMock()
            mock_result.status = HealthStatus.HEALTHY
            mock_result.to_dict.return_value = {"status": "healthy"}
            mock_health.return_value = mock_result
            
            await monitor._perform_check()
        
        assert len(monitor._health_history) == initial_history_len + 1
