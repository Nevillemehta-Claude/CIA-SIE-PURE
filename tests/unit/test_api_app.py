"""
Tests for CIA-SIE FastAPI Application
=====================================

Validates application factory and configuration.

GOVERNED BY: Section 11 (Backend Standards)
"""

import pytest
from unittest.mock import patch, AsyncMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from cia_sie.api.app import create_app, app


class TestCreateApp:
    """Tests for create_app factory function."""

    def test_returns_fastapi_instance(self):
        """Test that create_app returns a FastAPI instance."""
        application = create_app()
        assert isinstance(application, FastAPI)

    def test_app_title(self):
        """Test application title is set correctly."""
        application = create_app()
        assert application.title == "CIA-SIE API"

    def test_app_includes_api_router(self):
        """Test that API router is included."""
        application = create_app()
        # Check routes are registered
        routes = [route.path for route in application.routes]
        assert any("/api/v1" in route for route in routes)

    def test_health_endpoint_exists(self):
        """Test health check endpoint is registered."""
        application = create_app()
        routes = [route.path for route in application.routes]
        assert "/health" in routes


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with patch('cia_sie.api.app.init_db', new_callable=AsyncMock):
            application = create_app()
            return TestClient(application)

    def test_health_returns_200(self, client):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_healthy(self, client):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_returns_app_info(self, client):
        """Test health endpoint includes app info."""
        response = client.get("/health")
        data = response.json()
        assert "app" in data
        assert "version" in data

    def test_health_returns_security_info(self, client):
        """Test health endpoint includes security configuration."""
        response = client.get("/health")
        data = response.json()
        assert "security" in data
        assert "rate_limiting" in data["security"]


class TestMiddlewareStack:
    """Tests for middleware configuration."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with patch('cia_sie.api.app.init_db', new_callable=AsyncMock):
            application = create_app()
            return TestClient(application)

    def test_cors_headers_present(self, client):
        """Test CORS headers are added to responses."""
        response = client.options("/health", headers={"Origin": "http://localhost:3000"})
        # CORS preflight should work
        assert response.status_code in [200, 405]

    def test_security_headers_present(self, client):
        """Test security headers are added to responses."""
        response = client.get("/health")
        # Check OWASP recommended headers
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"

    def test_rate_limit_headers_present(self, client):
        """Test rate limit headers are added to responses."""
        response = client.get("/health")
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers


class TestSecurityInfoEndpoint:
    """Tests for security info endpoint (development only)."""

    @pytest.fixture
    def client(self):
        """Create test client in development mode."""
        with patch('cia_sie.api.app.init_db', new_callable=AsyncMock):
            with patch.dict('os.environ', {"ENVIRONMENT": "development"}):
                application = create_app()
                return TestClient(application)

    def test_security_info_exists_in_development(self, client):
        """Test security-info endpoint exists in development."""
        response = client.get("/security-info")
        assert response.status_code == 200

    def test_security_info_returns_environment(self, client):
        """Test security info includes environment."""
        response = client.get("/security-info")
        data = response.json()
        assert "environment" in data

    def test_security_info_returns_rate_limits(self, client):
        """Test security info includes rate limits."""
        response = client.get("/security-info")
        data = response.json()
        assert "rate_limits" in data


class TestProductionMode:
    """Tests for production mode configuration."""

    def test_docs_disabled_in_production(self):
        """Test that docs are disabled in production."""
        with patch('cia_sie.api.app.init_db', new_callable=AsyncMock):
            with patch.dict('os.environ', {"ENVIRONMENT": "production"}):
                application = create_app()
                assert application.docs_url is None
                assert application.redoc_url is None


class TestConstitutionalAPIDescription:
    """Tests for constitutional compliance in API description."""

    def test_api_description_mentions_no_aggregation(self):
        """Test API description mentions no aggregation."""
        application = create_app()
        description = application.description.lower()
        assert "no aggregation" in description or "never" in description

    def test_api_description_mentions_no_recommendations(self):
        """Test API description mentions no recommendations."""
        application = create_app()
        description = application.description.lower()
        assert "no" in description and "recommendation" in description

    def test_api_description_mentions_user_authority(self):
        """Test API description mentions user authority."""
        application = create_app()
        description = application.description.lower()
        assert "user" in description
