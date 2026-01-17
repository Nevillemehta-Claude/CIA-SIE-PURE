"""
Mercury Metrics Export
======================

Prometheus-style metrics collection and export for observability.

MISSION-CRITICAL STANDARD: Observability Pillar 2 - Metrics
- Counter, Gauge, Histogram metric types
- Thread-safe collection
- Prometheus text format export
- JSON format for API consumption
"""

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from mercury.core.logging import get_logger

logger = get_logger("mercury.metrics")


@dataclass
class MetricValue:
    """A single metric value with labels."""
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class Counter:
    """
    Monotonically increasing counter metric.
    
    Use for: request counts, error counts, messages processed.
    """
    
    def __init__(self, name: str, help_text: str = ""):
        self.name = name
        self.help_text = help_text
        self._values: Dict[Tuple, float] = defaultdict(float)
        self._lock = threading.Lock()
    
    def inc(self, value: float = 1.0, **labels) -> None:
        """Increment counter by value."""
        if value < 0:
            raise ValueError("Counter cannot be decremented")
        
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] += value
    
    def get(self, **labels) -> float:
        """Get current counter value."""
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            return self._values.get(label_key, 0.0)
    
    def get_all(self) -> List[MetricValue]:
        """Get all counter values."""
        with self._lock:
            return [
                MetricValue(value=v, labels=dict(k))
                for k, v in self._values.items()
            ]


class Gauge:
    """
    Metric that can increase or decrease.
    
    Use for: current queue size, active connections, memory usage.
    """
    
    def __init__(self, name: str, help_text: str = ""):
        self.name = name
        self.help_text = help_text
        self._values: Dict[Tuple, float] = defaultdict(float)
        self._lock = threading.Lock()
    
    def set(self, value: float, **labels) -> None:
        """Set gauge to value."""
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] = value
    
    def inc(self, value: float = 1.0, **labels) -> None:
        """Increment gauge."""
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] += value
    
    def dec(self, value: float = 1.0, **labels) -> None:
        """Decrement gauge."""
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            self._values[label_key] -= value
    
    def get(self, **labels) -> float:
        """Get current gauge value."""
        label_key = tuple(sorted(labels.items()))
        with self._lock:
            return self._values.get(label_key, 0.0)
    
    def get_all(self) -> List[MetricValue]:
        """Get all gauge values."""
        with self._lock:
            return [
                MetricValue(value=v, labels=dict(k))
                for k, v in self._values.items()
            ]


class Histogram:
    """
    Metric that samples observations and counts them in buckets.
    
    Use for: request latency, response sizes.
    """
    
    DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
    
    def __init__(
        self,
        name: str,
        help_text: str = "",
        buckets: Tuple[float, ...] = None,
    ):
        self.name = name
        self.help_text = help_text
        self.buckets = buckets or self.DEFAULT_BUCKETS
        self._counts: Dict[Tuple, Dict[float, int]] = defaultdict(lambda: defaultdict(int))
        self._sums: Dict[Tuple, float] = defaultdict(float)
        self._totals: Dict[Tuple, int] = defaultdict(int)
        self._lock = threading.Lock()
    
    def observe(self, value: float, **labels) -> None:
        """Record an observation."""
        label_key = tuple(sorted(labels.items()))
        
        with self._lock:
            self._sums[label_key] += value
            self._totals[label_key] += 1
            
            for bucket in self.buckets:
                if value <= bucket:
                    self._counts[label_key][bucket] += 1
            # Always increment +Inf bucket
            self._counts[label_key][float('inf')] += 1
    
    def get_stats(self, **labels) -> Dict[str, Any]:
        """Get histogram statistics."""
        label_key = tuple(sorted(labels.items()))
        
        with self._lock:
            total = self._totals.get(label_key, 0)
            sum_val = self._sums.get(label_key, 0)
            
            return {
                "count": total,
                "sum": sum_val,
                "mean": sum_val / total if total > 0 else 0,
                "buckets": dict(self._counts.get(label_key, {})),
            }


class MetricsRegistry:
    """
    Central registry for all metrics.
    
    Provides methods to export metrics in various formats.
    """
    
    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._lock = threading.Lock()
    
    def counter(self, name: str, help_text: str = "") -> Counter:
        """Get or create a counter."""
        with self._lock:
            if name not in self._counters:
                self._counters[name] = Counter(name, help_text)
            return self._counters[name]
    
    def gauge(self, name: str, help_text: str = "") -> Gauge:
        """Get or create a gauge."""
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = Gauge(name, help_text)
            return self._gauges[name]
    
    def histogram(
        self,
        name: str,
        help_text: str = "",
        buckets: Tuple[float, ...] = None,
    ) -> Histogram:
        """Get or create a histogram."""
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(name, help_text, buckets)
            return self._histograms[name]
    
    def to_prometheus(self) -> str:
        """Export metrics in Prometheus text format."""
        lines = []
        
        # Counters
        for name, counter in self._counters.items():
            if counter.help_text:
                lines.append(f"# HELP {name} {counter.help_text}")
            lines.append(f"# TYPE {name} counter")
            
            for mv in counter.get_all():
                labels_str = self._format_labels(mv.labels)
                lines.append(f"{name}{labels_str} {mv.value}")
        
        # Gauges
        for name, gauge in self._gauges.items():
            if gauge.help_text:
                lines.append(f"# HELP {name} {gauge.help_text}")
            lines.append(f"# TYPE {name} gauge")
            
            for mv in gauge.get_all():
                labels_str = self._format_labels(mv.labels)
                lines.append(f"{name}{labels_str} {mv.value}")
        
        # Histograms
        for name, histogram in self._histograms.items():
            if histogram.help_text:
                lines.append(f"# HELP {name} {histogram.help_text}")
            lines.append(f"# TYPE {name} histogram")
            
            # TODO: Export histogram buckets in Prometheus format
        
        return "\n".join(lines)
    
    def to_json(self) -> Dict[str, Any]:
        """Export metrics as JSON."""
        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "counters": {},
            "gauges": {},
            "histograms": {},
        }
        
        for name, counter in self._counters.items():
            result["counters"][name] = {
                "help": counter.help_text,
                "values": [
                    {"value": mv.value, "labels": mv.labels}
                    for mv in counter.get_all()
                ],
            }
        
        for name, gauge in self._gauges.items():
            result["gauges"][name] = {
                "help": gauge.help_text,
                "values": [
                    {"value": mv.value, "labels": mv.labels}
                    for mv in gauge.get_all()
                ],
            }
        
        for name, histogram in self._histograms.items():
            result["histograms"][name] = {
                "help": histogram.help_text,
                "stats": histogram.get_stats(),
            }
        
        return result
    
    def _format_labels(self, labels: Dict[str, str]) -> str:
        """Format labels for Prometheus output."""
        if not labels:
            return ""
        
        pairs = [f'{k}="{v}"' for k, v in sorted(labels.items())]
        return "{" + ",".join(pairs) + "}"


# Global metrics registry
_registry: Optional[MetricsRegistry] = None


def get_metrics_registry() -> MetricsRegistry:
    """Get the global metrics registry."""
    global _registry
    if _registry is None:
        _registry = MetricsRegistry()
    return _registry


# Alias for backwards compatibility
def get_registry() -> MetricsRegistry:
    """Get the global metrics registry (alias for get_metrics_registry)."""
    return get_metrics_registry()


# Alias for backwards compatibility
def get_metrics():
    """Get pre-defined Mercury metrics (alias for get_mercury_metrics)."""
    return get_mercury_metrics()


# Convenience functions for common operations
def inc_queries(service: str = "default") -> None:
    """Increment query counter."""
    registry = get_metrics_registry()
    counter = registry.counter("mercury_queries_total", "Total queries processed")
    counter.inc(service=service)


def observe_query_duration(duration_seconds: float, service: str = "default") -> None:
    """Record query duration."""
    registry = get_metrics_registry()
    histogram = registry.histogram("mercury_query_duration_seconds", "Query duration in seconds")
    histogram.observe(duration_seconds, service=service)


class time_query:
    """Context manager to time a query and record the duration."""
    
    def __init__(self, service: str = "default"):
        self.service = service
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        if self.start_time:
            duration = time.time() - self.start_time
            observe_query_duration(duration, self.service)
        return False


# Pre-defined metrics for Mercury
def get_mercury_metrics():
    """Get pre-defined Mercury metrics."""
    registry = get_metrics_registry()
    
    return {
        # Request metrics
        "requests_total": registry.counter(
            "mercury_requests_total",
            "Total number of requests processed"
        ),
        "requests_errors": registry.counter(
            "mercury_requests_errors_total",
            "Total number of request errors"
        ),
        
        # API call metrics
        "api_calls_total": registry.counter(
            "mercury_api_calls_total",
            "Total API calls by service"
        ),
        "api_call_duration": registry.histogram(
            "mercury_api_call_duration_seconds",
            "API call duration in seconds"
        ),
        
        # Connection metrics
        "active_connections": registry.gauge(
            "mercury_active_connections",
            "Number of active connections"
        ),
        "circuit_state": registry.gauge(
            "mercury_circuit_breaker_state",
            "Circuit breaker state (0=closed, 1=open, 2=half-open)"
        ),
        
        # Chat metrics
        "chat_queries_total": registry.counter(
            "mercury_chat_queries_total",
            "Total chat queries processed"
        ),
        "chat_query_duration": registry.histogram(
            "mercury_chat_query_duration_seconds",
            "Chat query processing time"
        ),
        
        # Token metrics
        "tokens_used": registry.counter(
            "mercury_tokens_used_total",
            "Total AI tokens consumed"
        ),
    }
