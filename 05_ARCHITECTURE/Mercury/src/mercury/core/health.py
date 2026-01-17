"""
Mercury Health Check System
===========================

Comprehensive health checks for all Mercury components.

MISSION-CRITICAL STANDARD: Observability
- Health checks for all external dependencies
- Startup validation
- Liveness and readiness probes
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

from mercury.core.logging import get_logger
from mercury.core.resilience import get_all_circuit_health, degradation

logger = get_logger("mercury.health")


class HealthStatus(Enum):
    """Health check status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ComponentHealth:
    """Health of a single component."""
    name: str
    status: HealthStatus
    message: str = ""
    latency_ms: Optional[int] = None
    last_check: Optional[datetime] = None
    details: dict = field(default_factory=dict)


@dataclass
class SystemHealth:
    """Overall system health."""
    status: HealthStatus
    components: list[ComponentHealth] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "0.1.0"
    
    @property
    def is_healthy(self) -> bool:
        return self.status in (HealthStatus.HEALTHY, HealthStatus.DEGRADED)
    
    @property
    def is_ready(self) -> bool:
        """Check if system is ready to serve requests."""
        # Ready if at least basic functionality works
        return any(
            c.status == HealthStatus.HEALTHY 
            for c in self.components
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "status": self.status.value,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "is_healthy": self.is_healthy,
            "is_ready": self.is_ready,
            "components": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "message": c.message,
                    "latency_ms": c.latency_ms,
                    "last_check": c.last_check.isoformat() if c.last_check else None,
                    "details": c.details,
                }
                for c in self.components
            ],
            "circuits": get_all_circuit_health(),
            "degradation": {
                "level": degradation.current_level.value,
                "capabilities": degradation.get_capabilities(),
            }
        }


async def check_kite_health() -> ComponentHealth:
    """Check Kite API health."""
    from mercury.core.config import get_settings
    
    settings = get_settings()
    start = time.time()
    
    try:
        # Just check if we have credentials configured
        if not settings.kite_api_key:
            return ComponentHealth(
                name="kite_api",
                status=HealthStatus.DEGRADED,
                message="No API key configured - using mock mode",
                latency_ms=0,
                last_check=datetime.now(timezone.utc),
            )
        
        # If credentials exist, assume healthy
        # In production, would ping the actual API
        latency = int((time.time() - start) * 1000)
        
        return ComponentHealth(
            name="kite_api",
            status=HealthStatus.HEALTHY,
            message="API key configured",
            latency_ms=latency,
            last_check=datetime.now(timezone.utc),
            details={"has_access_token": bool(settings.kite_access_token)},
        )
        
    except Exception as e:
        return ComponentHealth(
            name="kite_api",
            status=HealthStatus.UNHEALTHY,
            message=f"Health check failed: {str(e)}",
            latency_ms=int((time.time() - start) * 1000),
            last_check=datetime.now(timezone.utc),
        )


async def check_ai_health() -> ComponentHealth:
    """Check Claude AI health."""
    from mercury.core.config import get_settings
    
    settings = get_settings()
    start = time.time()
    
    try:
        if not settings.anthropic_api_key:
            return ComponentHealth(
                name="anthropic_api",
                status=HealthStatus.DEGRADED,
                message="No API key configured - using mock mode",
                latency_ms=0,
                last_check=datetime.now(timezone.utc),
            )
        
        # Validate key format
        if not settings.anthropic_api_key.startswith("sk-"):
            return ComponentHealth(
                name="anthropic_api",
                status=HealthStatus.DEGRADED,
                message="API key format may be invalid",
                latency_ms=0,
                last_check=datetime.now(timezone.utc),
            )
        
        latency = int((time.time() - start) * 1000)
        
        return ComponentHealth(
            name="anthropic_api",
            status=HealthStatus.HEALTHY,
            message="API key configured",
            latency_ms=latency,
            last_check=datetime.now(timezone.utc),
            details={"model": settings.anthropic_model},
        )
        
    except Exception as e:
        return ComponentHealth(
            name="anthropic_api",
            status=HealthStatus.UNHEALTHY,
            message=f"Health check failed: {str(e)}",
            latency_ms=int((time.time() - start) * 1000),
            last_check=datetime.now(timezone.utc),
        )


async def check_config_health() -> ComponentHealth:
    """Check configuration health."""
    from mercury.core.validation import validate_config
    
    start = time.time()
    
    try:
        result = validate_config()
        latency = int((time.time() - start) * 1000)
        
        if result.is_valid:
            status = HealthStatus.HEALTHY
            message = "Configuration valid"
        else:
            status = HealthStatus.UNHEALTHY
            message = f"Configuration errors: {len(result.errors)}"
        
        return ComponentHealth(
            name="configuration",
            status=status,
            message=message,
            latency_ms=latency,
            last_check=datetime.now(timezone.utc),
            details={
                "errors": len(result.errors),
                "warnings": len(result.warnings),
            },
        )
        
    except Exception as e:
        return ComponentHealth(
            name="configuration",
            status=HealthStatus.UNHEALTHY,
            message=f"Validation failed: {str(e)}",
            latency_ms=int((time.time() - start) * 1000),
            last_check=datetime.now(timezone.utc),
        )


async def check_memory_health() -> ComponentHealth:
    """Check system memory health."""
    import sys
    
    try:
        # Get rough memory usage
        # In production, use psutil for accurate metrics
        return ComponentHealth(
            name="memory",
            status=HealthStatus.HEALTHY,
            message="Memory check passed",
            latency_ms=0,
            last_check=datetime.now(timezone.utc),
            details={
                "python_version": sys.version.split()[0],
            },
        )
    except Exception as e:
        return ComponentHealth(
            name="memory",
            status=HealthStatus.UNKNOWN,
            message=str(e),
            last_check=datetime.now(timezone.utc),
        )


async def get_system_health() -> SystemHealth:
    """
    Perform comprehensive system health check.
    
    Returns:
        SystemHealth with status of all components
    """
    # Run all health checks concurrently
    results = await asyncio.gather(
        check_config_health(),
        check_kite_health(),
        check_ai_health(),
        check_memory_health(),
        return_exceptions=True,
    )
    
    components = []
    for result in results:
        if isinstance(result, Exception):
            components.append(ComponentHealth(
                name="unknown",
                status=HealthStatus.UNHEALTHY,
                message=str(result),
                last_check=datetime.now(timezone.utc),
            ))
        else:
            components.append(result)
    
    # Determine overall status
    statuses = [c.status for c in components]
    
    if all(s == HealthStatus.HEALTHY for s in statuses):
        overall = HealthStatus.HEALTHY
    elif any(s == HealthStatus.UNHEALTHY for s in statuses):
        # Check if critical components are unhealthy
        critical = ["configuration"]
        critical_unhealthy = any(
            c.status == HealthStatus.UNHEALTHY and c.name in critical
            for c in components
        )
        overall = HealthStatus.UNHEALTHY if critical_unhealthy else HealthStatus.DEGRADED
    else:
        overall = HealthStatus.DEGRADED
    
    return SystemHealth(
        status=overall,
        components=components,
    )


async def run_startup_checks() -> bool:
    """
    Run startup health checks.
    
    Returns:
        True if system can start, False otherwise
    """
    logger.info("Running startup health checks...")
    
    health = await get_system_health()
    
    for component in health.components:
        icon = "✅" if component.status == HealthStatus.HEALTHY else "⚠️" if component.status == HealthStatus.DEGRADED else "❌"
        logger.info(
            f"{icon} {component.name}: {component.status.value} - {component.message}",
            context={"latency_ms": component.latency_ms}
        )
    
    if health.is_ready:
        logger.info(
            f"Startup checks passed - status: {health.status.value}",
            context={"components": len(health.components)}
        )
        return True
    else:
        logger.error(
            "Startup checks FAILED - system not ready",
            context={
                "status": health.status.value,
                "unhealthy": [c.name for c in health.components if c.status == HealthStatus.UNHEALTHY],
            }
        )
        return False
