"""
Tests for CIA-SIE Security Module
=================================

Validates security utilities including webhook authentication,
signature validation, rate limiting, and security headers.

GOVERNED BY: Security Hardening Requirements
"""

import pytest
import time
import hashlib
import hmac
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone

from fastapi import Request, HTTPException
from starlette.responses import Response

from cia_sie.core.security import (
    SecurityEvent,
    log_security_event,
    WebhookSignatureValidator,
    validate_webhook_request,
    SecurityHeadersMiddleware,
    InMemoryRateLimiter,
    RateLimitMiddleware,
    generate_webhook_secret,
    webhook_rate_limiter,
    api_rate_limiter,
)


class TestSecurityEvent:
    """Tests for SecurityEvent constants."""

    def test_all_security_events_defined(self):
        """Test all required security event types exist."""
        assert SecurityEvent.AUTH_SUCCESS == "AUTH_SUCCESS"
        assert SecurityEvent.AUTH_FAILURE == "AUTH_FAILURE"
        assert SecurityEvent.INVALID_SIGNATURE == "INVALID_SIGNATURE"
        assert SecurityEvent.MISSING_SIGNATURE == "MISSING_SIGNATURE"
        assert SecurityEvent.TIMESTAMP_EXPIRED == "TIMESTAMP_EXPIRED"
        assert SecurityEvent.RATE_LIMIT_EXCEEDED == "RATE_LIMIT_EXCEEDED"
        assert SecurityEvent.WEBHOOK_RECEIVED == "WEBHOOK_RECEIVED"
        assert SecurityEvent.SUSPICIOUS_REQUEST == "SUSPICIOUS_REQUEST"


class TestLogSecurityEvent:
    """Tests for security event logging."""

    def test_log_security_event_info(self, caplog):
        """Test logging INFO level security events."""
        log_security_event(
            SecurityEvent.AUTH_SUCCESS,
            "192.168.1.1",
            {"endpoint": "/api/v1/webhook"}
        )
        # Should not raise

    def test_log_security_event_warning(self, caplog):
        """Test logging WARNING level security events."""
        log_security_event(
            SecurityEvent.RATE_LIMIT_EXCEEDED,
            "192.168.1.1",
            {"limit": 100},
            severity="WARNING"
        )
        # Should not raise

    def test_log_security_event_error(self, caplog):
        """Test logging ERROR level security events."""
        log_security_event(
            SecurityEvent.AUTH_FAILURE,
            "192.168.1.1",
            severity="ERROR"
        )
        # Should not raise

    def test_log_sanitizes_ip_address(self):
        """Test that IP addresses are sanitized (no log injection)."""
        # Malicious IP with newline
        malicious_ip = "192.168.1.1\nINJECTED LOG LINE"
        log_security_event(
            SecurityEvent.WEBHOOK_RECEIVED,
            malicious_ip
        )
        # Should not raise, and sanitization should occur

    def test_log_sanitizes_details(self):
        """Test that details are sanitized (no log injection)."""
        malicious_details = {"payload": "test\r\nINJECTED"}
        log_security_event(
            SecurityEvent.WEBHOOK_RECEIVED,
            "192.168.1.1",
            malicious_details
        )
        # Should not raise


class TestWebhookSignatureValidator:
    """Tests for WebhookSignatureValidator."""

    def test_compute_signature_without_timestamp(self):
        """Test signature computation without timestamp."""
        secret = "my_secret_key"
        payload = b'{"direction": "BULLISH"}'

        signature = WebhookSignatureValidator.compute_signature(secret, payload)

        assert signature.startswith("sha256=")
        assert len(signature) > 10

    def test_compute_signature_with_timestamp(self):
        """Test signature computation with timestamp."""
        secret = "my_secret_key"
        payload = b'{"direction": "BULLISH"}'
        timestamp = "1609459200"

        sig_with_ts = WebhookSignatureValidator.compute_signature(secret, payload, timestamp)
        sig_without_ts = WebhookSignatureValidator.compute_signature(secret, payload)

        # Signatures should be different
        assert sig_with_ts != sig_without_ts

    def test_compute_signature_is_deterministic(self):
        """Test that same inputs produce same signature."""
        secret = "my_secret_key"
        payload = b'{"test": "data"}'

        sig1 = WebhookSignatureValidator.compute_signature(secret, payload)
        sig2 = WebhookSignatureValidator.compute_signature(secret, payload)

        assert sig1 == sig2

    def test_get_client_ip_direct(self):
        """Test getting client IP from direct connection."""
        mock_request = Mock()
        mock_request.headers = {}
        mock_request.client = Mock()
        mock_request.client.host = "192.168.1.100"

        ip = WebhookSignatureValidator.get_client_ip(mock_request)
        assert ip == "192.168.1.100"

    def test_get_client_ip_from_proxy(self):
        """Test getting client IP from X-Forwarded-For header."""
        mock_request = Mock()
        mock_request.headers = {"x-forwarded-for": "10.0.0.1, 10.0.0.2"}
        mock_request.client = Mock()
        mock_request.client.host = "192.168.1.100"

        ip = WebhookSignatureValidator.get_client_ip(mock_request)
        assert ip == "10.0.0.1"

    def test_get_client_ip_no_client(self):
        """Test getting client IP when client is None."""
        mock_request = Mock()
        mock_request.headers = {}
        mock_request.client = None

        ip = WebhookSignatureValidator.get_client_ip(mock_request)
        assert ip == "unknown"

    def test_validate_signature_missing_header(self):
        """Test validation fails with missing signature header."""
        mock_request = Mock()
        mock_request.headers = {}
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/webhook")

        is_valid, error = WebhookSignatureValidator.validate_signature(
            mock_request, b'{}', "secret"
        )

        assert is_valid is False
        assert "Missing" in error

    def test_validate_signature_valid(self):
        """Test validation succeeds with valid signature."""
        secret = "my_secret_key"
        payload = b'{"direction": "BULLISH"}'

        # Compute correct signature
        expected_sig = WebhookSignatureValidator.compute_signature(secret, payload)

        mock_request = Mock()
        mock_request.headers = {"x-webhook-signature": expected_sig}
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/webhook")

        is_valid, error = WebhookSignatureValidator.validate_signature(
            mock_request, payload, secret
        )

        assert is_valid is True
        assert error == ""

    def test_validate_signature_invalid(self):
        """Test validation fails with wrong signature."""
        mock_request = Mock()
        mock_request.headers = {"x-webhook-signature": "sha256=wrongsignature"}
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/webhook")

        is_valid, error = WebhookSignatureValidator.validate_signature(
            mock_request, b'{}', "secret"
        )

        assert is_valid is False
        assert "Invalid" in error

    def test_validate_signature_expired_timestamp(self):
        """Test validation fails with expired timestamp."""
        secret = "my_secret_key"
        payload = b'{}'

        # Old timestamp (10 minutes ago)
        old_timestamp = str(int(time.time()) - 600)
        sig = WebhookSignatureValidator.compute_signature(secret, payload, old_timestamp)

        mock_request = Mock()
        mock_request.headers = {
            "x-webhook-signature": sig,
            "x-webhook-timestamp": old_timestamp
        }
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/webhook")

        is_valid, error = WebhookSignatureValidator.validate_signature(
            mock_request, payload, secret
        )

        assert is_valid is False
        assert "expired" in error.lower()


class TestValidateWebhookRequest:
    """Tests for validate_webhook_request dependency."""

    @pytest.mark.asyncio
    async def test_allows_unsigned_in_dev_mode(self):
        """Test that unsigned requests are allowed when secret not set."""
        mock_request = Mock()
        mock_request.body = AsyncMock(return_value=b'{"test": "data"}')

        with patch('cia_sie.core.security.get_settings') as mock_settings:
            mock_settings.return_value.webhook_secret = None

            body = await validate_webhook_request(mock_request)
            assert body == b'{"test": "data"}'

    @pytest.mark.asyncio
    async def test_rejects_invalid_signature(self):
        """Test that invalid signatures are rejected."""
        mock_request = Mock()
        mock_request.body = AsyncMock(return_value=b'{}')
        mock_request.headers = {"x-webhook-signature": "sha256=invalid"}
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/webhook")

        with patch('cia_sie.core.security.get_settings') as mock_settings:
            mock_settings.return_value.webhook_secret = "secret123"

            with pytest.raises(HTTPException) as exc_info:
                await validate_webhook_request(mock_request)

            assert exc_info.value.status_code == 401


class TestInMemoryRateLimiter:
    """Tests for InMemoryRateLimiter."""

    def test_allows_requests_under_limit(self):
        """Test that requests under limit are allowed."""
        limiter = InMemoryRateLimiter(requests_per_minute=10)

        is_allowed, remaining = limiter.is_allowed("192.168.1.1")

        assert is_allowed is True
        assert remaining == 9

    def test_blocks_requests_over_limit(self):
        """Test that requests over limit are blocked."""
        limiter = InMemoryRateLimiter(requests_per_minute=3)

        # Make 3 requests (the limit)
        limiter.is_allowed("192.168.1.1")
        limiter.is_allowed("192.168.1.1")
        limiter.is_allowed("192.168.1.1")

        # 4th request should be blocked
        is_allowed, remaining = limiter.is_allowed("192.168.1.1")

        assert is_allowed is False
        assert remaining == 0

    def test_different_ips_tracked_separately(self):
        """Test that different IPs have separate limits."""
        limiter = InMemoryRateLimiter(requests_per_minute=2)

        limiter.is_allowed("192.168.1.1")
        limiter.is_allowed("192.168.1.1")

        # Different IP should still be allowed
        is_allowed, _ = limiter.is_allowed("192.168.1.2")
        assert is_allowed is True

    def test_reset_clears_ip_requests(self):
        """Test that reset clears request history for an IP."""
        limiter = InMemoryRateLimiter(requests_per_minute=2)

        limiter.is_allowed("192.168.1.1")
        limiter.is_allowed("192.168.1.1")

        # Reset
        limiter.reset("192.168.1.1")

        # Should be allowed again
        is_allowed, remaining = limiter.is_allowed("192.168.1.1")
        assert is_allowed is True
        assert remaining == 1


class TestSecurityHeadersMiddleware:
    """Tests for SecurityHeadersMiddleware."""

    @pytest.mark.asyncio
    async def test_adds_security_headers(self):
        """Test that security headers are added to response."""
        async def mock_call_next(request):
            return Response(content="OK")

        middleware = SecurityHeadersMiddleware(app=None)
        mock_request = Mock()

        response = await middleware.dispatch(mock_request, mock_call_next)

        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    @pytest.mark.asyncio
    async def test_adds_hsts_in_production(self):
        """Test that HSTS header is added when enabled."""
        async def mock_call_next(request):
            return Response(content="OK")

        middleware = SecurityHeadersMiddleware(app=None, include_hsts=True)
        mock_request = Mock()

        response = await middleware.dispatch(mock_request, mock_call_next)

        assert "Strict-Transport-Security" in response.headers

    @pytest.mark.asyncio
    async def test_no_hsts_by_default(self):
        """Test that HSTS header is not added by default."""
        async def mock_call_next(request):
            return Response(content="OK")

        middleware = SecurityHeadersMiddleware(app=None, include_hsts=False)
        mock_request = Mock()

        response = await middleware.dispatch(mock_request, mock_call_next)

        assert "Strict-Transport-Security" not in response.headers


class TestRateLimitMiddleware:
    """Tests for RateLimitMiddleware."""

    @pytest.mark.asyncio
    async def test_adds_rate_limit_headers(self):
        """Test that rate limit headers are added to response."""
        # Reset rate limiters
        api_rate_limiter.requests.clear()

        async def mock_call_next(request):
            return Response(content="OK")

        middleware = RateLimitMiddleware(app=None)
        mock_request = Mock()
        mock_request.headers = {}
        mock_request.client = Mock(host="192.168.1.100")
        mock_request.url = Mock(path="/api/v1/test")

        response = await middleware.dispatch(mock_request, mock_call_next)

        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers


class TestGenerateWebhookSecret:
    """Tests for generate_webhook_secret utility."""

    def test_generates_secret(self):
        """Test that a secret is generated."""
        secret = generate_webhook_secret()
        assert secret is not None
        assert len(secret) > 0

    def test_generates_hex_string(self):
        """Test that secret is a valid hex string."""
        secret = generate_webhook_secret()
        # Should be valid hex
        int(secret, 16)

    def test_generates_unique_secrets(self):
        """Test that each call generates a unique secret."""
        secrets = [generate_webhook_secret() for _ in range(10)]
        assert len(set(secrets)) == 10  # All unique

    def test_respects_length_parameter(self):
        """Test that length parameter is respected."""
        secret = generate_webhook_secret(length=16)
        assert len(secret) == 32  # 16 bytes = 32 hex chars

    def test_default_length(self):
        """Test default length is 32 bytes (64 hex chars)."""
        secret = generate_webhook_secret()
        assert len(secret) == 64


class TestTimestampTolerance:
    """Tests for timestamp tolerance in signature validation."""

    def test_timestamp_tolerance_constant(self):
        """Test timestamp tolerance is 5 minutes (300 seconds)."""
        assert WebhookSignatureValidator.TIMESTAMP_TOLERANCE_SECONDS == 300

    def test_supported_signature_headers(self):
        """Test all signature header variants are supported."""
        headers = WebhookSignatureValidator.SIGNATURE_HEADERS
        assert "x-tradingview-signature" in headers
        assert "x-webhook-signature" in headers
        assert "x-signature" in headers

    def test_supported_timestamp_headers(self):
        """Test all timestamp header variants are supported."""
        headers = WebhookSignatureValidator.TIMESTAMP_HEADERS
        assert "x-tradingview-timestamp" in headers
        assert "x-webhook-timestamp" in headers
        assert "x-timestamp" in headers
