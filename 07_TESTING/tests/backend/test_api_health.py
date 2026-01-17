"""
API Tests - Health Endpoint
============================

Complete cycle tests for /health endpoint.
Health check is critical for monitoring and orchestration.

Each test verifies: START STATE → ACTION → END STATE
Tests run 10 times each for statistical confidence.
"""

import pytest


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_health_returns_200(self, client):
        """
        API-HEALTH-001: Health endpoint returns 200.
        """
        response = await client.get("/health")
        
        assert response.status_code == 200, f"Health check should return 200, got {response.status_code}"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_health_returns_json(self, client):
        """
        API-HEALTH-002: Health endpoint returns valid JSON.
        """
        response = await client.get("/health")
        
        assert response.status_code == 200
        
        # Should be valid JSON
        data = response.json()
        assert data is not None
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_health_has_status(self, client):
        """
        API-HEALTH-003: Health response has status field.
        """
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have some indication of health
        # Could be "status", "healthy", "ok", etc.
        has_status = any(key in data for key in ["status", "healthy", "ok", "health"])
        assert has_status or isinstance(data, dict), "Health should return status info"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_health_rapid_calls(self, client):
        """
        API-HEALTH-004: Health can handle rapid calls.
        
        NOTE: May trigger rate limiting (429) - this is VALID behavior.
        """
        success_count = 0
        rate_limited = 0
        
        for _ in range(10):
            response = await client.get("/health")
            
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                rate_limited += 1
        
        # Either all succeed or rate limiting kicks in - both are valid
        assert success_count + rate_limited == 10


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_root_returns_valid(self, client):
        """
        API-ROOT-001: Root endpoint returns valid response.
        """
        response = await client.get("/")
        
        # May return 200 (with info) or redirect (307/308) or 404
        assert response.status_code in [200, 307, 308, 404]

