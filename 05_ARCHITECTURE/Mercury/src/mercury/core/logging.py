"""
Mercury Structured Logging
==========================

Structured JSON logging for mission-critical observability.

MISSION-CRITICAL STANDARD: Observability Pillar 1 - Logging
- All logs in structured JSON format
- Correlation IDs for request tracing
- Sensitive data automatically masked
- Severity levels properly classified
"""

import json
import logging
import sys
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Optional

from mercury.core.security import sanitize_dict, sanitize_text

# Context variable for request correlation
correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


def get_correlation_id() -> str:
    """Get current correlation ID or generate new one."""
    cid = correlation_id_var.get()
    if cid is None:
        cid = str(uuid.uuid4())[:8]  # Short correlation ID
        correlation_id_var.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    """Set correlation ID for current context."""
    correlation_id_var.set(cid)


def new_correlation_id() -> str:
    """Generate and set a new correlation ID."""
    cid = str(uuid.uuid4())[:8]
    correlation_id_var.set(cid)
    return cid


class StructuredFormatter(logging.Formatter):
    """
    JSON structured log formatter.
    
    Produces logs in the format:
    {
        "timestamp": "2026-01-13T10:30:00.000Z",
        "level": "INFO",
        "service": "mercury",
        "component": "chat",
        "correlation_id": "abc12345",
        "message": "Query processed",
        "context": {...},
        "duration_ms": 150
    }
    """
    
    def __init__(self, service: str = "mercury"):
        super().__init__()
        self.service = service
    
    def format(self, record: logging.LogRecord) -> str:
        # Base log entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self.service,
            "component": self._extract_component(record.name),
            "correlation_id": get_correlation_id(),
            "message": sanitize_text(record.getMessage()),
        }
        
        # Add extra context if provided
        if hasattr(record, 'context') and record.context:
            log_entry["context"] = sanitize_dict(record.context)
        
        # Add duration if provided
        if hasattr(record, 'duration_ms'):
            log_entry["duration_ms"] = record.duration_ms
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": sanitize_text(str(record.exc_info[1])) if record.exc_info[1] else None,
            }
        
        # Add source location for errors
        if record.levelno >= logging.ERROR:
            log_entry["source"] = {
                "file": record.filename,
                "line": record.lineno,
                "function": record.funcName,
            }
        
        return json.dumps(log_entry, default=str)
    
    def _extract_component(self, logger_name: str) -> str:
        """Extract component from logger name."""
        parts = logger_name.split('.')
        if len(parts) >= 2:
            return parts[-1]  # Last part of module path
        return logger_name


class HumanReadableFormatter(logging.Formatter):
    """
    Human-readable formatter for development.
    
    Produces logs like:
    2026-01-13 10:30:00 [INFO] [abc12345] chat: Query processed (150ms)
    """
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m',
    }
    
    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors
    
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        level = record.levelname
        cid = get_correlation_id()
        component = record.name.split('.')[-1]
        message = sanitize_text(record.getMessage())
        
        # Add duration if present
        duration = ""
        if hasattr(record, 'duration_ms'):
            duration = f" ({record.duration_ms}ms)"
        
        if self.use_colors:
            color = self.COLORS.get(level, '')
            reset = self.COLORS['RESET']
            return f"{timestamp} {color}[{level}]{reset} [{cid}] {component}: {message}{duration}"
        else:
            return f"{timestamp} [{level}] [{cid}] {component}: {message}{duration}"


class MercuryLogger:
    """
    Enhanced logger with structured logging support.
    
    Usage:
        logger = MercuryLogger("mercury.chat")
        logger.info("Query processed", context={"query": "...", "symbols": [...]}, duration_ms=150)
    """
    
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
    
    def _log(
        self,
        level: int,
        message: str,
        context: Optional[dict] = None,
        duration_ms: Optional[int] = None,
        exc_info: bool = False,
    ) -> None:
        """Internal logging method."""
        extra = {}
        if context:
            extra['context'] = context
        if duration_ms is not None:
            extra['duration_ms'] = duration_ms
        
        self._logger.log(level, message, extra=extra, exc_info=exc_info)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, exc_info: bool = True, **kwargs) -> None:
        """Log error message."""
        self._log(logging.ERROR, message, exc_info=exc_info, **kwargs)
    
    def critical(self, message: str, exc_info: bool = True, **kwargs) -> None:
        """Log critical message."""
        self._log(logging.CRITICAL, message, exc_info=exc_info, **kwargs)
    
    def query_start(self, query: str) -> str:
        """Log query start and return correlation ID."""
        cid = new_correlation_id()
        self.info("Query started", context={"query_preview": query[:100]})
        return cid
    
    def query_complete(self, duration_ms: int, success: bool = True) -> None:
        """Log query completion."""
        if success:
            self.info("Query completed", duration_ms=duration_ms)
        else:
            self.warning("Query failed", duration_ms=duration_ms)
    
    def api_call(
        self,
        service: str,
        endpoint: str,
        duration_ms: int,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """Log external API call."""
        context = {
            "service": service,
            "endpoint": endpoint,
            "success": success,
        }
        if error:
            context["error"] = sanitize_text(error)
        
        level = logging.INFO if success else logging.WARNING
        self._log(level, f"API call to {service}", context=context, duration_ms=duration_ms)


def setup_logging(
    level: str = "INFO",
    json_format: bool = False,
    service: str = "mercury",
) -> None:
    """
    Configure logging for Mercury.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON format (True) or human-readable (False)
        service: Service name for log entries
    """
    root_logger = logging.getLogger("mercury")
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))
    
    # Set formatter
    if json_format:
        formatter = StructuredFormatter(service=service)
    else:
        formatter = HumanReadableFormatter(use_colors=True)
    
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Prevent propagation to root logger
    root_logger.propagate = False


def get_logger(name: str) -> MercuryLogger:
    """Get a Mercury logger instance."""
    return MercuryLogger(name)
