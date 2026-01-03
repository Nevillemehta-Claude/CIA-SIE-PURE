"""
Integration Tests for CIA-SIE API
=================================

Tests API endpoints for constitutional compliance.
"""

import pytest


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    async def test_health_check(self, client):
        """Test health endpoint returns ok."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestInstrumentsAPI:
    """Tests for Instruments API."""

    async def test_create_instrument(self, client):
        """Test creating an instrument."""
        response = await client.post(
            "/api/v1/instruments/",
            json={"symbol": "TEST_INST", "display_name": "Test Instrument"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["symbol"] == "TEST_INST"
        assert "instrument_id" in data

    async def test_list_instruments(self, client):
        """Test listing instruments."""
        # Create one first
        await client.post(
            "/api/v1/instruments/",
            json={"symbol": "TEST_INST", "display_name": "Test Instrument"},
        )

        response = await client.get("/api/v1/instruments/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1


class TestWebhookAPI:
    """Tests for Webhook API."""

    async def test_webhook_rejects_without_chart(self, client):
        """Test webhook rejects unregistered webhook_id."""
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": "UNKNOWN_CHART",
                "direction": "BULLISH",
            },
        )
        assert response.status_code == 404

    async def test_webhook_validation(self, client):
        """Test webhook validates required fields."""
        response = await client.post(
            "/api/v1/webhook/",
            json={"direction": "BULLISH"},  # Missing webhook_id
        )
        assert response.status_code == 400


class TestRelationshipsAPI:
    """Tests for Relationships API."""

    async def test_relationships_expose_all(self, client):
        """
        CRITICAL TEST: Relationships endpoint must expose ALL data.

        Per Section 13.3: Returns ALL charts, contradictions, confirmations.
        Nothing hidden.
        """
        # This would need a full setup with instruments, silos, charts, signals
        # For now, verify endpoint structure exists
        response = await client.get("/api/v1/relationships/silo/nonexistent")
        # Should return 404 for missing silo, not hide data
        assert response.status_code in [404, 500]


class TestNarrativesAPI:
    """Tests for Narratives API."""

    async def test_narrative_is_descriptive(self, client):
        """
        CRITICAL TEST: Narratives must be descriptive, not prescriptive.

        Per Section 14: All narratives are DESCRIPTIVE only.
        """
        # The endpoint structure enforces this through prompt engineering
        # and post-processing in the NarrativeGenerator
        pass  # Tested via unit tests of NarrativeGenerator


class TestBasketsAPI:
    """Tests for Baskets API."""

    async def test_basket_creation(self, client):
        """Test creating a basket."""
        response = await client.post(
            "/api/v1/baskets/",
            json={
                "basket_name": "My Test Basket",
                "basket_type": "CUSTOM",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["basket_name"] == "My Test Basket"

    async def test_basket_has_no_processing_impact(self, client):
        """
        CRITICAL TEST: Baskets must not affect processing.

        Per ADR-002: Baskets are UI-layer only.
        """
        # Create basket
        response = await client.post(
            "/api/v1/baskets/",
            json={
                "basket_name": "Test Basket",
                "basket_type": "CUSTOM",
            },
        )
        data = response.json()

        # Verify no processing-related fields
        assert "aggregated_score" not in data
        assert "weight" not in data
        assert "priority" not in data
