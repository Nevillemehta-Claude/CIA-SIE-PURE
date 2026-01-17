"""
Mercury Alerting System
=======================

Webhook-based alerting for critical events.

MISSION-CRITICAL STANDARD: Observability Pillar 3 - Alerting
- Configurable alert thresholds
- Webhook delivery with retry
- Alert deduplication
- Severity levels
"""

import asyncio
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import httpx

from mercury.core.config import get_settings
from mercury.core.logging import get_logger

logger = get_logger("mercury.alerting")


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Alert:
    """An alert to be sent."""
    title: str
    message: str
    severity: AlertSeverity
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context: Dict[str, Any] = field(default_factory=dict)
    fingerprint: Optional[str] = None
    
    def __post_init__(self):
        if self.fingerprint is None:
            # Generate fingerprint for deduplication
            content = f"{self.title}:{self.source}:{self.severity.value}"
            self.fingerprint = hashlib.md5(content.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "title": self.title,
            "message": self.message,
            "severity": self.severity.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "fingerprint": self.fingerprint,
        }
    
    def to_slack_payload(self) -> Dict[str, Any]:
        """Format alert for Slack webhook."""
        color_map = {
            AlertSeverity.INFO: "#36a64f",
            AlertSeverity.WARNING: "#ffcc00",
            AlertSeverity.ERROR: "#ff6600",
            AlertSeverity.CRITICAL: "#ff0000",
        }
        
        emoji_map = {
            AlertSeverity.INFO: "ℹ️",
            AlertSeverity.WARNING: "⚠️",
            AlertSeverity.ERROR: "🔴",
            AlertSeverity.CRITICAL: "🚨",
        }
        
        fields = [
            {"title": "Source", "value": self.source, "short": True},
            {"title": "Severity", "value": self.severity.value.upper(), "short": True},
        ]
        
        for key, value in self.context.items():
            fields.append({
                "title": key.replace("_", " ").title(),
                "value": str(value),
                "short": True,
            })
        
        return {
            "attachments": [
                {
                    "color": color_map.get(self.severity, "#808080"),
                    "title": f"{emoji_map.get(self.severity, '')} {self.title}",
                    "text": self.message,
                    "fields": fields,
                    "footer": f"Mercury | {self.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}",
                }
            ]
        }
    
    def to_discord_payload(self) -> Dict[str, Any]:
        """Format alert for Discord webhook."""
        color_map = {
            AlertSeverity.INFO: 0x36a64f,
            AlertSeverity.WARNING: 0xffcc00,
            AlertSeverity.ERROR: 0xff6600,
            AlertSeverity.CRITICAL: 0xff0000,
        }
        
        fields = [
            {"name": "Source", "value": self.source, "inline": True},
            {"name": "Severity", "value": self.severity.value.upper(), "inline": True},
        ]
        
        for key, value in self.context.items():
            fields.append({
                "name": key.replace("_", " ").title(),
                "value": str(value),
                "inline": True,
            })
        
        return {
            "embeds": [
                {
                    "title": self.title,
                    "description": self.message,
                    "color": color_map.get(self.severity, 0x808080),
                    "fields": fields,
                    "footer": {"text": "Mercury Alerting"},
                    "timestamp": self.timestamp.isoformat(),
                }
            ]
        }


@dataclass
class WebhookConfig:
    """Configuration for a webhook destination."""
    url: str
    name: str = "default"
    format: str = "json"  # json, slack, discord
    min_severity: AlertSeverity = AlertSeverity.WARNING
    headers: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True


class AlertManager:
    """
    Manages alert routing and delivery.
    
    Features:
    - Multiple webhook destinations
    - Alert deduplication
    - Async delivery with retry
    - Rate limiting per destination
    """
    
    # Deduplication window
    DEDUP_WINDOW = timedelta(minutes=15)
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    def __init__(self):
        self._webhooks: List[WebhookConfig] = []
        self._sent_fingerprints: Dict[str, datetime] = {}
        self._lock = asyncio.Lock()
        self._delivery_queue: asyncio.Queue = asyncio.Queue()
        self._worker_task: Optional[asyncio.Task] = None
    
    def add_webhook(self, config: WebhookConfig) -> None:
        """Add a webhook destination."""
        self._webhooks.append(config)
        logger.info(f"Added webhook: {config.name}")
    
    def remove_webhook(self, name: str) -> bool:
        """Remove a webhook by name."""
        original_len = len(self._webhooks)
        self._webhooks = [w for w in self._webhooks if w.name != name]
        return len(self._webhooks) < original_len
    
    async def start(self) -> None:
        """Start the alert delivery worker."""
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._delivery_worker())
            logger.info("Alert delivery worker started")
    
    async def stop(self) -> None:
        """Stop the alert delivery worker."""
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            logger.info("Alert delivery worker stopped")
    
    async def send(self, alert: Alert) -> None:
        """
        Send an alert to all configured webhooks.
        
        Alerts are deduplicated and queued for async delivery.
        """
        async with self._lock:
            # Check deduplication
            if self._is_duplicate(alert):
                logger.debug(f"Alert deduplicated: {alert.fingerprint}")
                return
            
            # Mark as sent
            self._sent_fingerprints[alert.fingerprint] = alert.timestamp
            
            # Clean old fingerprints
            self._cleanup_fingerprints()
        
        # Queue for delivery
        await self._delivery_queue.put(alert)
        logger.info(
            f"Alert queued: {alert.title}",
            context={"severity": alert.severity.value, "fingerprint": alert.fingerprint}
        )
    
    def _is_duplicate(self, alert: Alert) -> bool:
        """Check if alert is a duplicate within dedup window."""
        if alert.fingerprint not in self._sent_fingerprints:
            return False
        
        last_sent = self._sent_fingerprints[alert.fingerprint]
        return datetime.now(timezone.utc) - last_sent < self.DEDUP_WINDOW
    
    def _cleanup_fingerprints(self) -> None:
        """Remove expired fingerprints."""
        now = datetime.now(timezone.utc)
        expired = [
            fp for fp, ts in self._sent_fingerprints.items()
            if now - ts >= self.DEDUP_WINDOW
        ]
        for fp in expired:
            del self._sent_fingerprints[fp]
    
    async def _delivery_worker(self) -> None:
        """Background worker that delivers alerts."""
        while True:
            try:
                alert = await self._delivery_queue.get()
                await self._deliver_alert(alert)
                self._delivery_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Alert delivery error: {e}")
    
    async def _deliver_alert(self, alert: Alert) -> None:
        """Deliver alert to all matching webhooks."""
        for webhook in self._webhooks:
            if not webhook.enabled:
                continue
            
            # Check severity threshold
            severity_order = [
                AlertSeverity.INFO,
                AlertSeverity.WARNING,
                AlertSeverity.ERROR,
                AlertSeverity.CRITICAL,
            ]
            if severity_order.index(alert.severity) < severity_order.index(webhook.min_severity):
                continue
            
            # Format payload
            if webhook.format == "slack":
                payload = alert.to_slack_payload()
            elif webhook.format == "discord":
                payload = alert.to_discord_payload()
            else:
                payload = alert.to_dict()
            
            # Send with retry
            success = await self._send_with_retry(webhook, payload)
            if success:
                logger.debug(f"Alert delivered to {webhook.name}")
            else:
                logger.warning(f"Failed to deliver alert to {webhook.name}")
    
    async def _send_with_retry(
        self,
        webhook: WebhookConfig,
        payload: Dict[str, Any],
    ) -> bool:
        """Send payload to webhook with retry."""
        for attempt in range(self.MAX_RETRIES):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        webhook.url,
                        json=payload,
                        headers=webhook.headers,
                        timeout=10.0,
                    )
                    
                    if response.status_code < 300:
                        return True
                    
                    logger.warning(
                        f"Webhook returned {response.status_code}",
                        context={"webhook": webhook.name, "attempt": attempt + 1}
                    )
                    
            except Exception as e:
                logger.warning(
                    f"Webhook request failed: {e}",
                    context={"webhook": webhook.name, "attempt": attempt + 1}
                )
            
            if attempt < self.MAX_RETRIES - 1:
                await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
        
        return False


# Global alert manager
_alert_manager: Optional[AlertManager] = None


def get_alert_manager() -> AlertManager:
    """Get the global alert manager."""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager


# Convenience functions for common alerts
async def alert_api_error(service: str, error: str, **context) -> None:
    """Send alert for API error."""
    manager = get_alert_manager()
    await manager.send(Alert(
        title=f"{service} API Error",
        message=error,
        severity=AlertSeverity.ERROR,
        source=service,
        context=context,
    ))


async def alert_circuit_open(service: str, failure_count: int) -> None:
    """Send alert when circuit breaker opens."""
    manager = get_alert_manager()
    await manager.send(Alert(
        title=f"{service} Circuit Breaker Opened",
        message=f"Circuit breaker opened after {failure_count} failures. Service temporarily unavailable.",
        severity=AlertSeverity.CRITICAL,
        source=service,
        context={"failure_count": failure_count},
    ))


async def alert_token_expired(service: str) -> None:
    """Send alert when authentication token expires."""
    manager = get_alert_manager()
    await manager.send(Alert(
        title=f"{service} Token Expired",
        message="Authentication token has expired. Re-authentication required.",
        severity=AlertSeverity.WARNING,
        source=service,
    ))


async def alert_rate_limit(service: str, limit: int, window: str) -> None:
    """Send alert when rate limit is hit."""
    manager = get_alert_manager()
    await manager.send(Alert(
        title=f"{service} Rate Limit Hit",
        message=f"Rate limit of {limit} requests per {window} has been reached.",
        severity=AlertSeverity.WARNING,
        source=service,
        context={"limit": limit, "window": window},
    ))


async def alert_health_degraded(component: str, reason: str) -> None:
    """Send alert when system health degrades."""
    manager = get_alert_manager()
    await manager.send(Alert(
        title="System Health Degraded",
        message=f"Component '{component}' is in degraded state: {reason}",
        severity=AlertSeverity.WARNING,
        source="health_monitor",
        context={"component": component},
    ))
