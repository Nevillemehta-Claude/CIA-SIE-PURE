"""
Tests for Mercury Health Check System
=====================================

Tests for health checks and system status.
"""

import pytest
from mercury.core.health import (
    HealthStatus,
    ComponentHealth,
    SystemHealth,
    check_config_health,
    check_memory_health,
    get_system_health,
)


class TestHealthStatus:
    """Tests for HealthStatus enum."""
    
    def test_healthy_values(self):
        """Should have expected status values."""
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.DEGRADED.value == "degraded"
        assert HealthStatus.UNHEALTHY.value == "unhealthy"


class TestComponentHealth:
    """Tests for ComponentHealth dataclass."""
    
    def test_create_healthy_component(self):
        """Should create healthy component."""
        health = ComponentHealth(
            name="test_component",
            status=HealthStatus.HEALTHY,
            message="All good",
            latency_ms=10,
        )
        
        assert health.name == "test_component"
        assert health.status == HealthStatus.HEALTHY
    
    def test_with_details(self):
        """Should include details."""
        health = ComponentHealth(
            name="test",
            status=HealthStatus.HEALTHY,
            details={"version": "1.0.0"},
        )
        
        assert health.details["version"] == "1.0.0"


class TestSystemHealth:
    """Tests for SystemHealth dataclass."""
    
    def test_is_healthy_when_healthy(self):
        """Should report healthy when all healthy."""
        health = SystemHealth(
            status=HealthStatus.HEALTHY,
            components=[
                ComponentHealth(name="a", status=HealthStatus.HEALTHY),
                ComponentHealth(name="b", status=HealthStatus.HEALTHY),
            ]
        )
        
        assert health.is_healthy is True
    
    def test_is_healthy_when_degraded(self):
        """Should still be healthy when degraded."""
        health = SystemHealth(
            status=HealthStatus.DEGRADED,
            components=[
                ComponentHealth(name="a", status=HealthStatus.HEALTHY),
                ComponentHealth(name="b", status=HealthStatus.DEGRADED),
            ]
        )
        
        assert health.is_healthy is True
    
    def test_is_not_healthy_when_unhealthy(self):
        """Should not be healthy when unhealthy."""
        health = SystemHealth(
            status=HealthStatus.UNHEALTHY,
            components=[
                ComponentHealth(name="a", status=HealthStatus.UNHEALTHY),
            ]
        )
        
        assert health.is_healthy is False
    
    def test_is_ready_with_one_healthy(self):
        """Should be ready if at least one component healthy."""
        health = SystemHealth(
            status=HealthStatus.DEGRADED,
            components=[
                ComponentHealth(name="a", status=HealthStatus.HEALTHY),
                ComponentHealth(name="b", status=HealthStatus.UNHEALTHY),
            ]
        )
        
        assert health.is_ready is True
    
    def test_to_dict(self):
        """Should convert to dictionary."""
        health = SystemHealth(
            status=HealthStatus.HEALTHY,
            components=[
                ComponentHealth(name="test", status=HealthStatus.HEALTHY, message="OK"),
            ]
        )
        
        result = health.to_dict()
        
        assert result["status"] == "healthy"
        assert result["is_healthy"] is True
        assert len(result["components"]) == 1
        assert result["components"][0]["name"] == "test"


class TestHealthChecks:
    """Tests for individual health check functions."""
    
    @pytest.mark.asyncio
    async def test_check_config_health(self):
        """Should check configuration."""
        health = await check_config_health()
        
        assert health.name == "configuration"
        assert health.status in (HealthStatus.HEALTHY, HealthStatus.UNHEALTHY)
        assert health.latency_ms is not None
    
    @pytest.mark.asyncio
    async def test_check_memory_health(self):
        """Should check memory."""
        health = await check_memory_health()
        
        assert health.name == "memory"
        assert health.status in (HealthStatus.HEALTHY, HealthStatus.UNKNOWN)


class TestGetSystemHealth:
    """Tests for get_system_health function."""
    
    @pytest.mark.asyncio
    async def test_returns_system_health(self):
        """Should return SystemHealth object."""
        health = await get_system_health()
        
        assert isinstance(health, SystemHealth)
        assert health.status is not None
        assert len(health.components) > 0
    
    @pytest.mark.asyncio
    async def test_includes_all_components(self):
        """Should include all standard components."""
        health = await get_system_health()
        
        component_names = [c.name for c in health.components]
        
        assert "configuration" in component_names
        assert "memory" in component_names
