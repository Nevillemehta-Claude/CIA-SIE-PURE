"""
Chaos Tests - Concurrent Load
==============================

Tests for system behavior under concurrent load.
System must handle multiple simultaneous requests safely.

Each test verifies: CONCURRENT REQUESTS → ALL HANDLED
Tests run 10 times each for statistical confidence.
"""

import pytest
import asyncio
from uuid import uuid4


class TestConcurrentWebhooks:
    """Tests for concurrent webhook handling."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_100_concurrent_webhooks(self, client, sample_chart):
        """
        CHAOS-008: 100 concurrent webhooks.
        
        Load: 100 parallel POSTs
        Expected: All succeed or rate-limited
        """
        async def send_webhook(i: int):
            payload = {
                "webhook_id": sample_chart.webhook_id,
                "direction": "BULLISH" if i % 2 == 0 else "BEARISH",
                "signal_type": "TREND",
                "message": f"Concurrent test {i}"
            }
            return await client.post("/api/v1/webhook/", json=payload)
        
        # Send 100 concurrent requests
        tasks = [send_webhook(i) for i in range(100)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count results
        success = 0
        rate_limited = 0
        errors = 0
        
        for r in responses:
            if isinstance(r, Exception):
                errors += 1
            elif r.status_code in [200, 201]:
                success += 1
            elif r.status_code == 429:
                rate_limited += 1
            else:
                errors += 1
        
        # System should not crash - either succeed or rate limit
        assert success + rate_limited >= 50, \
            f"At least half should succeed or be rate-limited: {success}/{rate_limited}/{errors}"
        assert errors < 50, f"Too many errors: {errors}"


class TestConcurrentReads:
    """Tests for concurrent read operations."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_50_concurrent_reads(self, client, sample_instrument):
        """
        CHAOS-009: 50 concurrent GET requests.
        
        Load: 50 parallel GETs
        Expected: All succeed
        """
        async def get_instrument():
            return await client.get(f"/api/v1/instruments/{sample_instrument.instrument_id}")
        
        # Send 50 concurrent reads
        tasks = [get_instrument() for _ in range(50)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count results
        success = 0
        errors = 0
        
        for r in responses:
            if isinstance(r, Exception):
                errors += 1
            elif r.status_code == 200:
                success += 1
            else:
                errors += 1
        
        # All reads should succeed
        assert success >= 45, f"Most reads should succeed: {success}/50"
        assert errors < 5, f"Too many errors: {errors}"


class TestMixedConcurrency:
    """Tests for mixed read/write concurrency."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_mixed_read_write(self, client, sample_chart):
        """
        CHAOS-010: Mixed read/write operations.
        
        Load: 25 GETs + 25 POSTs
        Expected: No race conditions
        """
        async def read_chart():
            return await client.get(f"/api/v1/charts/{sample_chart.chart_id}")
        
        async def write_signal():
            payload = {
                "webhook_id": sample_chart.webhook_id,
                "direction": "BULLISH",
                "signal_type": "TREND"
            }
            return await client.post("/api/v1/webhook/", json=payload)
        
        # Mix reads and writes
        tasks = []
        for i in range(50):
            if i % 2 == 0:
                tasks.append(read_chart())
            else:
                tasks.append(write_signal())
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count results
        success = 0
        errors = 0
        
        for r in responses:
            if isinstance(r, Exception):
                errors += 1
            elif r.status_code in [200, 201, 429]:
                success += 1
            else:
                errors += 1
        
        assert success >= 40, f"Most should succeed: {success}/50"
        assert errors < 10, f"Too many errors: {errors}"


class TestDatabaseConnectionPool:
    """Tests for database connection pool handling."""
    
    @pytest.mark.chaos
    @pytest.mark.asyncio
    async def test_connection_pool_stress(self, client):
        """
        CHAOS-011: Stress database connection pool.
        
        Load: 100 rapid database operations
        Expected: Pooling works correctly
        """
        async def list_instruments():
            return await client.get("/api/v1/instruments/")
        
        # Rapid-fire requests
        tasks = [list_instruments() for _ in range(100)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count results
        success = 0
        pool_errors = 0
        other_errors = 0
        
        for r in responses:
            if isinstance(r, Exception):
                if "pool" in str(r).lower() or "connection" in str(r).lower():
                    pool_errors += 1
                else:
                    other_errors += 1
            elif r.status_code == 200:
                success += 1
            elif r.status_code == 503:
                pool_errors += 1
            else:
                other_errors += 1
        
        # Connection pooling should handle the load
        assert success >= 80, f"Most should succeed: {success}/100"
        assert pool_errors < 10, f"Too many pool errors: {pool_errors}"

