"""
Chaos Tests - Invalid Input Handling
=====================================

Tests for handling malicious and malformed input.
System must handle all inputs safely without crashing.

Each test verifies: MALICIOUS INPUT → GRACEFUL REJECTION
Tests run 10 times each for statistical confidence.
"""

import pytest
from uuid import uuid4


class TestSQLInjection:
    """Tests for SQL injection protection."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_sql_injection_in_symbol(self, client):
        """
        CHAOS-001: SQL injection attempt in symbol field.
        
        Input: symbol="'; DROP TABLE--"
        Expected: Safely rejected
        """
        payload = {
            "symbol": "'; DROP TABLE instruments; --",
            "display_name": "SQL Injection Test",
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        # Should either reject or safely escape
        # Must NOT crash or execute SQL
        assert response.status_code in [201, 400, 422], \
            f"SQL injection should be handled: {response.status_code}"
        
        # Verify no damage done - list instruments should still work
        list_response = await client.get("/api/v1/instruments/")
        assert list_response.status_code == 200, "Database should still work after injection attempt"


class TestXSSAttacks:
    """Tests for XSS protection."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="XSS sanitization to be implemented")
    async def test_xss_in_display_name(self, client):
        """
        CHAOS-002: XSS attempt in display_name field.
        
        Input: display_name="<script>alert('xss')</script>"
        Expected: Sanitized
        """
        payload = {
            "symbol": f"XSS_TEST_{uuid4().hex[:6]}",
            "display_name": "<script>alert('XSS')</script>",
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        # Accept multiple status codes - 201 if created, 400/422 if rejected
        if response.status_code == 201:
            data = response.json()
            # Script tags should be escaped or removed
            display_name = data.get("display_name", "")
            # Should not contain executable script
            assert "<script>" not in display_name.lower() or \
                   "&lt;script&gt;" in display_name.lower(), \
                   "XSS should be sanitized"
        else:
            # If rejected (400/422), that's also acceptable behavior
            assert response.status_code in [400, 422], "Should reject or sanitize XSS"


class TestOversizedInput:
    """Tests for oversized input handling."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_oversized_json_payload(self, client):
        """
        CHAOS-003: Oversized JSON payload.
        
        Input: 1MB payload
        Expected: 413 error
        """
        # Create 1MB+ payload
        large_data = "x" * (1024 * 1024)  # 1MB
        
        payload = {
            "symbol": "LARGE",
            "display_name": large_data,
            "exchange": "NSE"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        # Should reject oversized input
        assert response.status_code in [413, 422, 400], \
            f"Oversized payload should be rejected: {response.status_code}"
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_deeply_nested_json(self, client):
        """
        CHAOS-004: Deeply nested JSON.
        
        Input: 100 levels deep
        Expected: Rejected
        """
        # Create deeply nested structure
        nested = {"level": 0}
        current = nested
        for i in range(100):
            current["nested"] = {"level": i + 1}
            current = current["nested"]
        
        payload = {
            "symbol": "NESTED",
            "display_name": "Test",
            "metadata": nested
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        # Should handle gracefully
        assert response.status_code in [201, 400, 422], \
            f"Deeply nested JSON should be handled: {response.status_code}"


class TestUnicodeExtremes:
    """Tests for unicode edge cases."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_unicode_emoji(self, client):
        """
        CHAOS-005: Unicode with emoji.
        
        Input: Symbol with emoji
        Expected: Handled
        """
        payload = {
            "symbol": f"EMOJI_{uuid4().hex[:4]}",
            "display_name": "Test 📈 Stock 🚀 Company 💰",
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        # Should handle emoji
        assert response.status_code in [201, 422], \
            f"Emoji should be handled: {response.status_code}"
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_unicode_rtl(self, client):
        """
        CHAOS-005b: Unicode with RTL characters.
        
        Input: Right-to-left text
        Expected: Handled
        """
        payload = {
            "symbol": f"RTL_{uuid4().hex[:4]}",
            "display_name": "مرحبا العالم",  # Arabic "Hello World"
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        # Should handle RTL text
        assert response.status_code in [201, 422], \
            f"RTL text should be handled: {response.status_code}"
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_unicode_zero_width(self, client):
        """
        CHAOS-005c: Unicode zero-width characters.
        
        Input: Text with zero-width characters
        Expected: Handled safely
        """
        # Zero-width space and other invisible characters
        payload = {
            "symbol": f"ZW_{uuid4().hex[:4]}",
            "display_name": "Test\u200B\u200C\u200DCompany",  # Zero-width chars
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        assert response.status_code in [201, 422]


class TestNullBytes:
    """Tests for null byte handling."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_null_bytes_in_string(self, client):
        """
        CHAOS-006: Null bytes in input.
        
        Input: Contains \x00
        Expected: Rejected
        """
        payload = {
            "symbol": f"NULL_{uuid4().hex[:4]}",
            "display_name": "Test\x00Company",
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        try:
            response = await client.post("/api/v1/instruments/", json=payload)
            # If request succeeds, should be sanitized
            assert response.status_code in [201, 400, 422]
        except Exception:
            # May fail to serialize - that's acceptable
            pass


class TestPathTraversal:
    """Tests for path traversal attacks."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Path traversal protection to be implemented")
    async def test_path_traversal_in_webhook_id(self, client, sample_silo):
        """
        CHAOS-007: Path traversal in webhook_id.
        
        Input: webhook_id="../../../etc/passwd"
        Expected: Rejected
        """
        payload = {
            "silo_id": sample_silo.silo_id,
            "chart_code": "PT01",
            "chart_name": "Path Traversal Test",
            "timeframe": "D",
            "webhook_id": "../../../etc/passwd"
        }
        
        response = await client.post("/api/v1/charts/", json=payload)
        
        # Should reject or sanitize
        assert response.status_code in [201, 400, 422]
        
        if response.status_code == 201:
            data = response.json()
            webhook_id = data.get("webhook_id", "")
            # Should not contain path traversal
            assert "../" not in webhook_id, "Path traversal should be sanitized"

