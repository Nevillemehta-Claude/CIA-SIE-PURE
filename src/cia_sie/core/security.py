"""
CIA-SIE Security Module
=======================

Security utilities for webhook authentication, signature validation,
rate limiting, and security event logging.

GOVERNED BY: Security Hardening Requirements (Production Readiness Plan)
"""

import hashlib
import hmac
import logging
import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from cia_sie.core.config import get_settings

# =============================================================================
# SECURITY EVENT LOGGER
# =============================================================================

security_logger = logging.getLogger("cia_sie.security")

# Configure security logger if not already configured
if not security_logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - SECURITY - %(levelname)s - %(message)s"))
    security_logger.addHandler(handler)
    security_logger.setLevel(logging.INFO)


class SecurityEvent:
    """Security event types for logging."""

    AUTH_SUCCESS = "AUTH_SUCCESS"
    AUTH_FAILURE = "AUTH_FAILURE"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    MISSING_SIGNATURE = "MISSING_SIGNATURE"
    TIMESTAMP_EXPIRED = "TIMESTAMP_EXPIRED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    WEBHOOK_RECEIVED = "WEBHOOK_RECEIVED"
    SUSPICIOUS_REQUEST = "SUSPICIOUS_REQUEST"


def log_security_event(
    event_type: str, ip_address: str, details: Optional[dict] = None, severity: str = "INFO"
):
    """
    Log a security event.

    Args:
        event_type: Type of security event (from SecurityEvent class)
        ip_address: Client IP address
        details: Additional event details
        severity: Log severity (INFO, WARNING, ERROR)

    Note:
        Sanitization is applied INLINE (not via function) so CodeQL
        can trace the data flow and recognize the log injection fix.
    """
    # INLINE sanitization for CodeQL recognition - remove newlines to prevent log injection
    # CodeQL requires .replace() to be directly on the logged variable, not in a helper function
    safe_ip = str(ip_address).replace("\n", "").replace("\r", "").replace("\t", "")[:45]

    # Sanitize details dict values inline
    safe_details: dict = {}
    if details:
        for k, v in details.items():
            safe_val = str(v).replace("\n", "").replace("\r", "").replace("\t", "")[:200]
            safe_details[k] = safe_val

    log_data = {
        "event": event_type,
        "ip": safe_ip,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **safe_details,
    }

    # Build message with sanitized values
    msg_ip = safe_ip
    msg_details = str(safe_details) if safe_details else ""

    if severity == "WARNING":
        security_logger.warning(f"{event_type} | IP: {msg_ip} | {msg_details}", extra=log_data)
    elif severity == "ERROR":
        security_logger.error(f"{event_type} | IP: {msg_ip} | {msg_details}", extra=log_data)
    else:
        security_logger.info(f"{event_type} | IP: {msg_ip} | {msg_details}", extra=log_data)


# =============================================================================
# WEBHOOK SIGNATURE VALIDATION
# =============================================================================


class WebhookSignatureValidator:
    """
    Validates webhook signatures using HMAC-SHA256.

    Supports TradingView and custom webhook formats.
    """

    # Signature expires after 5 minutes (300 seconds)
    TIMESTAMP_TOLERANCE_SECONDS = 300

    # Supported signature header names
    SIGNATURE_HEADERS = [
        "x-tradingview-signature",
        "x-webhook-signature",
        "x-signature",
    ]

    TIMESTAMP_HEADERS = [
        "x-tradingview-timestamp",
        "x-webhook-timestamp",
        "x-timestamp",
    ]

    @classmethod
    def get_client_ip(cls, request: Request) -> str:
        """Extract client IP from request, handling proxies."""
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    @classmethod
    def compute_signature(cls, secret: str, payload: bytes, timestamp: str = "") -> str:
        """
        Compute HMAC-SHA256 signature.

        Args:
            secret: Webhook secret key
            payload: Request body bytes
            timestamp: Optional timestamp to include in signature

        Returns:
            Hex-encoded signature
        """
        message = timestamp.encode() + payload if timestamp else payload
        signature = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
        return f"sha256={signature}"

    @classmethod
    def validate_signature(cls, request: Request, body: bytes, secret: str) -> tuple[bool, str]:
        """
        Validate webhook signature.

        Args:
            request: FastAPI request object
            body: Request body bytes
            secret: Webhook secret for validation

        Returns:
            Tuple of (is_valid, error_message)
        """
        client_ip = cls.get_client_ip(request)

        # Find signature header
        provided_signature = None
        for header in cls.SIGNATURE_HEADERS:
            provided_signature = request.headers.get(header)
            if provided_signature:
                break

        if not provided_signature:
            log_security_event(
                SecurityEvent.MISSING_SIGNATURE,
                client_ip,
                {"headers": list(request.headers.keys())},
                severity="WARNING",
            )
            return False, "Missing webhook signature header"

        # Find timestamp header (optional but recommended)
        timestamp = ""
        for header in cls.TIMESTAMP_HEADERS:
            timestamp = request.headers.get(header, "")
            if timestamp:
                break

        # Validate timestamp if provided
        if timestamp:
            try:
                ts_int = int(timestamp)
                current_time = int(time.time())
                if abs(current_time - ts_int) > cls.TIMESTAMP_TOLERANCE_SECONDS:
                    log_security_event(
                        SecurityEvent.TIMESTAMP_EXPIRED,
                        client_ip,
                        {"provided": ts_int, "current": current_time},
                        severity="WARNING",
                    )
                    return False, "Webhook timestamp expired"
            except ValueError:
                pass  # Non-integer timestamp, skip validation

        # Compute expected signature
        expected_signature = cls.compute_signature(secret, body, timestamp)

        # Normalize provided signature
        if not provided_signature.startswith("sha256="):
            provided_signature = f"sha256={provided_signature}"

        # Constant-time comparison to prevent timing attacks
        is_valid = hmac.compare_digest(expected_signature, provided_signature)

        if not is_valid:
            log_security_event(
                SecurityEvent.INVALID_SIGNATURE,
                client_ip,
                {"endpoint": str(request.url.path)},
                severity="WARNING",
            )
            return False, "Invalid webhook signature"

        log_security_event(
            SecurityEvent.AUTH_SUCCESS, client_ip, {"endpoint": str(request.url.path)}
        )
        return True, ""


async def validate_webhook_request(request: Request) -> bytes:
    """
    Dependency for validating webhook requests.

    Args:
        request: FastAPI request object

    Returns:
        Request body bytes if valid

    Raises:
        HTTPException: If validation fails
    """
    settings = get_settings()

    # If no secret configured, allow all requests (development mode)
    if not settings.webhook_secret:
        security_logger.warning(
            "WEBHOOK_SECRET not configured - accepting unsigned webhooks (DEVELOPMENT MODE)"
        )
        return await request.body()

    body = await request.body()

    is_valid, error_message = WebhookSignatureValidator.validate_signature(
        request, body, settings.webhook_secret
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Webhook authentication failed: {error_message}",
        )

    return body


# =============================================================================
# SECURITY HEADERS MIDDLEWARE
# =============================================================================


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.

    Implements OWASP recommended security headers.
    """

    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    # Headers to add only in production (when HTTPS is enforced)
    PRODUCTION_HEADERS = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }

    def __init__(self, app, include_hsts: bool = False):
        """
        Initialize middleware.

        Args:
            app: ASGI application
            include_hsts: Whether to include HSTS header (enable in production)
        """
        super().__init__(app)
        self.include_hsts = include_hsts

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Add security headers
        for header, value in self.SECURITY_HEADERS.items():
            response.headers[header] = value

        # Add HSTS in production
        if self.include_hsts:
            for header, value in self.PRODUCTION_HEADERS.items():
                response.headers[header] = value

        return response


# =============================================================================
# RATE LIMITING
# =============================================================================


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter.

    For production, consider using Redis-based rate limiting.
    """

    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests allowed per minute per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = {}

    def _cleanup_old_requests(self, ip: str, current_time: float):
        """Remove requests older than 1 minute."""
        if ip in self.requests:
            cutoff = current_time - 60
            self.requests[ip] = [t for t in self.requests[ip] if t > cutoff]

    def is_allowed(self, ip: str) -> tuple[bool, int]:
        """
        Check if request is allowed.

        Args:
            ip: Client IP address

        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        current_time = time.time()
        self._cleanup_old_requests(ip, current_time)

        if ip not in self.requests:
            self.requests[ip] = []

        request_count = len(self.requests[ip])
        remaining = max(0, self.requests_per_minute - request_count)

        if request_count >= self.requests_per_minute:
            return False, 0

        self.requests[ip].append(current_time)
        return True, remaining - 1

    def reset(self, ip: str):
        """Reset rate limit for an IP."""
        if ip in self.requests:
            del self.requests[ip]


# Global rate limiter instance
webhook_rate_limiter = InMemoryRateLimiter(requests_per_minute=60)
api_rate_limiter = InMemoryRateLimiter(requests_per_minute=100)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware.

    Applies different limits to different endpoints.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = WebhookSignatureValidator.get_client_ip(request)
        path = request.url.path

        # Choose rate limiter based on endpoint
        if "/webhook" in path:
            rate_limiter = webhook_rate_limiter
            limit_name = "webhook"
        else:
            rate_limiter = api_rate_limiter
            limit_name = "api"

        is_allowed, remaining = rate_limiter.is_allowed(client_ip)

        if not is_allowed:
            log_security_event(
                SecurityEvent.RATE_LIMIT_EXCEEDED,
                client_ip,
                {"endpoint": path, "limit_type": limit_name},
                severity="WARNING",
            )
            return Response(
                content='{"detail": "Rate limit exceeded. Please try again later."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(rate_limiter.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def generate_webhook_secret(length: int = 32) -> str:
    """
    Generate a secure random webhook secret.

    Args:
        length: Length of the secret in bytes (will be hex-encoded)

    Returns:
        Hex-encoded random secret
    """
    import secrets

    return secrets.token_hex(length)
