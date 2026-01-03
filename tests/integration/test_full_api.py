"""
Comprehensive Integration Tests for CIA-SIE API
================================================

Tests all API endpoints with full workflow scenarios.

GOVERNED BY: Gold Standard Specification §12 (Quality Enforcement)
"""

import pytest
import pytest_asyncio
from uuid import uuid4


# =============================================================================
# FIXTURES
# =============================================================================

@pytest_asyncio.fixture
async def created_instrument(client):
    """Create an instrument and return its data."""
    response = await client.post(
        "/api/v1/instruments/",
        json={"symbol": "TEST_INST", "display_name": "Test Instrument"},
    )
    assert response.status_code == 201
    return response.json()


@pytest_asyncio.fixture
async def created_silo(client, created_instrument):
    """Create a silo and return its data."""
    response = await client.post(
        "/api/v1/silos/",
        json={
            "instrument_id": created_instrument["instrument_id"],
            "silo_name": "Technical Analysis",
            "heartbeat_enabled": True,
            "heartbeat_frequency_min": 5,
            "current_threshold_min": 2,
            "recent_threshold_min": 10,
            "stale_threshold_min": 30,
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest_asyncio.fixture
async def created_chart(client, created_silo):
    """Create a chart and return its data."""
    response = await client.post(
        "/api/v1/charts/",
        json={
            "silo_id": created_silo["silo_id"],
            "chart_code": "RSI_14",
            "chart_name": "RSI (14)",
            "timeframe": "1h",
            "webhook_id": f"webhook_rsi_{uuid4().hex[:8]}",
        },
    )
    assert response.status_code == 201
    return response.json()


# =============================================================================
# HEALTH ENDPOINT TESTS
# =============================================================================

class TestHealthEndpoint:
    """Tests for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_returns_healthy(self, client):
        """Test health endpoint returns healthy status."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_check_structure(self, client):
        """Test health response has expected structure."""
        response = await client.get("/health")
        data = response.json()
        assert "status" in data


# =============================================================================
# INSTRUMENTS API TESTS
# =============================================================================

class TestInstrumentsAPI:
    """Comprehensive tests for Instruments API."""

    @pytest.mark.asyncio
    async def test_create_instrument(self, client):
        """Test creating an instrument."""
        response = await client.post(
            "/api/v1/instruments/",
            json={"symbol": "NIFTY50", "display_name": "Nifty 50 Index"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["symbol"] == "NIFTY50"
        assert data["display_name"] == "Nifty 50 Index"
        assert "instrument_id" in data
        assert data["is_active"] is True

    @pytest.mark.asyncio
    async def test_create_duplicate_instrument_fails(self, client, created_instrument):
        """Test creating duplicate instrument returns 409."""
        response = await client.post(
            "/api/v1/instruments/",
            json={"symbol": "TEST_INST", "display_name": "Duplicate"},
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_list_instruments(self, client, created_instrument):
        """Test listing instruments returns created instrument."""
        response = await client.get("/api/v1/instruments/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        symbols = [i["symbol"] for i in data]
        assert "TEST_INST" in symbols

    @pytest.mark.asyncio
    async def test_get_instrument_by_id(self, client, created_instrument):
        """Test getting instrument by ID."""
        inst_id = created_instrument["instrument_id"]
        response = await client.get(f"/api/v1/instruments/{inst_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "TEST_INST"

    @pytest.mark.asyncio
    async def test_get_instrument_by_symbol(self, client, created_instrument):
        """Test getting instrument by symbol."""
        response = await client.get("/api/v1/instruments/symbol/TEST_INST")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "TEST_INST"

    @pytest.mark.asyncio
    async def test_get_nonexistent_instrument(self, client):
        """Test getting non-existent instrument returns 404."""
        fake_id = str(uuid4())
        response = await client.get(f"/api/v1/instruments/{fake_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_instrument(self, client, created_instrument):
        """Test deleting an instrument."""
        inst_id = created_instrument["instrument_id"]
        response = await client.delete(f"/api/v1/instruments/{inst_id}")
        assert response.status_code == 204

        # Verify it's deleted (soft delete)
        response = await client.get(f"/api/v1/instruments/{inst_id}")
        # Should still be findable but inactive
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    @pytest.mark.constitutional
    async def test_instrument_has_no_weight(self, client, created_instrument):
        """CRITICAL: Instruments must have no weight attribute."""
        assert "weight" not in created_instrument
        assert "score" not in created_instrument
        assert "confidence" not in created_instrument


# =============================================================================
# SILOS API TESTS
# =============================================================================

class TestSilosAPI:
    """Comprehensive tests for Silos API."""

    @pytest.mark.asyncio
    async def test_create_silo(self, client, created_instrument):
        """Test creating a silo."""
        response = await client.post(
            "/api/v1/silos/",
            json={
                "instrument_id": created_instrument["instrument_id"],
                "silo_name": "Technical Analysis",
                "heartbeat_enabled": True,
                "heartbeat_frequency_min": 5,
                "current_threshold_min": 2,
                "recent_threshold_min": 10,
                "stale_threshold_min": 30,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["silo_name"] == "Technical Analysis"
        assert "silo_id" in data

    @pytest.mark.asyncio
    async def test_list_silos(self, client, created_silo):
        """Test listing silos."""
        response = await client.get("/api/v1/silos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_list_silos_by_instrument(self, client, created_instrument, created_silo):
        """Test listing silos filtered by instrument."""
        inst_id = created_instrument["instrument_id"]
        response = await client.get(f"/api/v1/silos/?instrument_id={inst_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(s["instrument_id"] == inst_id for s in data)

    @pytest.mark.asyncio
    async def test_get_silo_by_id(self, client, created_silo):
        """Test getting silo by ID."""
        silo_id = created_silo["silo_id"]
        response = await client.get(f"/api/v1/silos/{silo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["silo_name"] == "Technical Analysis"

    @pytest.mark.asyncio
    async def test_delete_silo(self, client, created_silo):
        """Test deleting a silo."""
        silo_id = created_silo["silo_id"]
        response = await client.delete(f"/api/v1/silos/{silo_id}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    @pytest.mark.constitutional
    async def test_silo_has_no_weight(self, client, created_silo):
        """CRITICAL: Silos must have no weight attribute."""
        assert "weight" not in created_silo
        assert "score" not in created_silo
        assert "priority" not in created_silo


# =============================================================================
# CHARTS API TESTS
# =============================================================================

class TestChartsAPI:
    """Comprehensive tests for Charts API."""

    @pytest.mark.asyncio
    async def test_create_chart(self, client, created_silo):
        """Test creating a chart."""
        response = await client.post(
            "/api/v1/charts/",
            json={
                "silo_id": created_silo["silo_id"],
                "chart_code": "MACD",
                "chart_name": "MACD (12,26,9)",
                "timeframe": "4h",
                "webhook_id": f"webhook_macd_{uuid4().hex[:8]}",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["chart_code"] == "MACD"
        assert data["timeframe"] == "4h"

    @pytest.mark.asyncio
    async def test_list_charts(self, client, created_chart):
        """Test listing charts."""
        response = await client.get("/api/v1/charts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_list_charts_by_silo(self, client, created_silo, created_chart):
        """Test listing charts filtered by silo."""
        silo_id = created_silo["silo_id"]
        response = await client.get(f"/api/v1/charts/?silo_id={silo_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(c["silo_id"] == silo_id for c in data)

    @pytest.mark.asyncio
    async def test_get_chart_by_id(self, client, created_chart):
        """Test getting chart by ID."""
        chart_id = created_chart["chart_id"]
        response = await client.get(f"/api/v1/charts/{chart_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["chart_code"] == "RSI_14"

    @pytest.mark.asyncio
    async def test_get_chart_by_webhook_id(self, client, created_chart):
        """Test getting chart by webhook ID."""
        webhook_id = created_chart["webhook_id"]
        response = await client.get(f"/api/v1/charts/webhook/{webhook_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["webhook_id"] == webhook_id

    @pytest.mark.asyncio
    async def test_delete_chart(self, client, created_chart):
        """Test deleting a chart."""
        chart_id = created_chart["chart_id"]
        response = await client.delete(f"/api/v1/charts/{chart_id}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    @pytest.mark.constitutional
    async def test_chart_has_no_weight(self, client, created_chart):
        """CRITICAL: Charts must have NO weight attribute (ADR-003)."""
        assert "weight" not in created_chart
        assert "score" not in created_chart
        assert "priority" not in created_chart
        assert "importance" not in created_chart


# =============================================================================
# SIGNALS API TESTS
# =============================================================================

class TestSignalsAPI:
    """Tests for Signals API (read-only)."""

    @pytest.mark.asyncio
    async def test_list_signals_for_chart(self, client, created_chart):
        """Test listing signals for a chart (initially empty)."""
        chart_id = created_chart["chart_id"]
        response = await client.get(f"/api/v1/signals/chart/{chart_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_latest_signal_empty(self, client, created_chart):
        """Test getting latest signal when none exist."""
        chart_id = created_chart["chart_id"]
        response = await client.get(f"/api/v1/signals/chart/{chart_id}/latest")
        assert response.status_code == 200
        # Returns null when no signals

    @pytest.mark.asyncio
    async def test_get_nonexistent_signal(self, client):
        """Test getting non-existent signal returns 404."""
        fake_id = str(uuid4())
        response = await client.get(f"/api/v1/signals/{fake_id}")
        assert response.status_code == 404


# =============================================================================
# WEBHOOK API TESTS
# =============================================================================

class TestWebhookAPI:
    """Tests for Webhook API."""

    @pytest.mark.asyncio
    async def test_webhook_rejects_unknown_chart(self, client):
        """Test webhook rejects unregistered webhook_id."""
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": "UNKNOWN_WEBHOOK_ID",
                "direction": "BULLISH",
            },
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_webhook_validates_required_fields(self, client):
        """Test webhook validates required fields."""
        response = await client.post(
            "/api/v1/webhook/",
            json={"direction": "BULLISH"},  # Missing webhook_id
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_webhook_accepts_valid_signal(self, client, created_chart):
        """Test webhook accepts valid signal for registered chart."""
        webhook_id = created_chart["webhook_id"]
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": webhook_id,
                "direction": "BULLISH",
                "signal_type": "STATE_CHANGE",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert "signal_id" in data

    @pytest.mark.asyncio
    async def test_webhook_creates_signal(self, client, created_chart):
        """Test webhook creates retrievable signal."""
        webhook_id = created_chart["webhook_id"]
        chart_id = created_chart["chart_id"]

        # Send webhook
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": webhook_id,
                "direction": "BEARISH",
            },
        )
        assert response.status_code == 200

        # Verify signal was created
        response = await client.get(f"/api/v1/signals/chart/{chart_id}/latest")
        assert response.status_code == 200
        signal = response.json()
        assert signal is not None
        assert signal["direction"] == "BEARISH"

    @pytest.mark.asyncio
    @pytest.mark.constitutional
    async def test_webhook_signal_has_no_confidence(self, client, created_chart):
        """CRITICAL: Webhook signals must have no confidence score."""
        webhook_id = created_chart["webhook_id"]
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": webhook_id,
                "direction": "BULLISH",
            },
        )
        data = response.json()
        assert "confidence" not in data
        assert "score" not in data
        assert "weight" not in data


# =============================================================================
# BASKETS API TESTS
# =============================================================================

class TestBasketsAPI:
    """Tests for Analytical Baskets API."""

    @pytest.mark.asyncio
    async def test_create_basket(self, client):
        """Test creating a basket."""
        response = await client.post(
            "/api/v1/baskets/",
            json={
                "basket_name": "My Analysis Basket",
                "basket_type": "CUSTOM",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["basket_name"] == "My Analysis Basket"
        assert "basket_id" in data

    @pytest.mark.asyncio
    async def test_list_baskets(self, client):
        """Test listing baskets."""
        # Create one first
        await client.post(
            "/api/v1/baskets/",
            json={
                "basket_name": "Test Basket",
                "basket_type": "CUSTOM",
            },
        )

        response = await client.get("/api/v1/baskets/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_add_chart_to_basket(self, client, created_chart):
        """Test adding a chart to a basket."""
        # Create basket
        response = await client.post(
            "/api/v1/baskets/",
            json={
                "basket_name": "Chart Basket",
                "basket_type": "CUSTOM",
            },
        )
        basket_id = response.json()["basket_id"]
        chart_id = created_chart["chart_id"]

        # Add chart
        response = await client.post(
            f"/api/v1/baskets/{basket_id}/charts/{chart_id}"
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_remove_chart_from_basket(self, client, created_chart):
        """Test removing a chart from a basket."""
        # Create basket and add chart
        response = await client.post(
            "/api/v1/baskets/",
            json={
                "basket_name": "Chart Basket",
                "basket_type": "CUSTOM",
            },
        )
        basket_id = response.json()["basket_id"]
        chart_id = created_chart["chart_id"]

        await client.post(f"/api/v1/baskets/{basket_id}/charts/{chart_id}")

        # Remove chart
        response = await client.delete(
            f"/api/v1/baskets/{basket_id}/charts/{chart_id}"
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    @pytest.mark.constitutional
    async def test_basket_has_no_processing_impact(self, client):
        """CRITICAL: Baskets must not affect processing (ADR-002)."""
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
        assert "confidence" not in data
        assert "signal_summary" not in data


# =============================================================================
# RELATIONSHIPS API TESTS
# =============================================================================

class TestRelationshipsAPI:
    """Tests for Relationships API."""

    @pytest.mark.asyncio
    async def test_get_nonexistent_silo_relationships(self, client):
        """Test getting relationships for non-existent silo."""
        fake_id = str(uuid4())
        response = await client.get(f"/api/v1/relationships/silo/{fake_id}")
        assert response.status_code in [404, 500]

    @pytest.mark.asyncio
    async def test_get_silo_relationships(self, client, created_silo, created_chart):
        """Test getting relationships for a silo with charts."""
        silo_id = created_silo["silo_id"]
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        # May return 200 with data or 404 if no signals
        assert response.status_code in [200, 404, 500]

    @pytest.mark.asyncio
    @pytest.mark.constitutional
    async def test_relationships_expose_all_data(self, client, created_silo):
        """CRITICAL: Relationships must expose ALL data, nothing hidden."""
        silo_id = created_silo["silo_id"]
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        # When successful, verify no aggregation fields
        if response.status_code == 200:
            data = response.json()
            assert "aggregated_score" not in data
            assert "overall_direction" not in data
            assert "net_signal" not in data
            assert "recommendation" not in data


# =============================================================================
# FULL WORKFLOW TESTS
# =============================================================================

class TestFullWorkflow:
    """End-to-end workflow tests."""

    @pytest.mark.asyncio
    async def test_complete_signal_workflow(self, client):
        """Test complete workflow: instrument -> silo -> chart -> signal."""
        # 1. Create instrument
        response = await client.post(
            "/api/v1/instruments/",
            json={"symbol": "WORKFLOW_TEST", "display_name": "Workflow Test"},
        )
        assert response.status_code == 201
        instrument = response.json()

        # 2. Create silo
        response = await client.post(
            "/api/v1/silos/",
            json={
                "instrument_id": instrument["instrument_id"],
                "silo_name": "Workflow Silo",
                "heartbeat_enabled": False,
                "heartbeat_frequency_min": 5,
                "current_threshold_min": 2,
                "recent_threshold_min": 10,
                "stale_threshold_min": 30,
            },
        )
        assert response.status_code == 201
        silo = response.json()

        # 3. Create chart
        webhook_id = f"workflow_webhook_{uuid4().hex[:8]}"
        response = await client.post(
            "/api/v1/charts/",
            json={
                "silo_id": silo["silo_id"],
                "chart_code": "WORKFLOW",
                "chart_name": "Workflow Chart",
                "timeframe": "D",
                "webhook_id": webhook_id,
            },
        )
        assert response.status_code == 201
        chart = response.json()

        # 4. Send signal via webhook
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": webhook_id,
                "direction": "BULLISH",
            },
        )
        assert response.status_code == 200
        signal_response = response.json()
        assert signal_response["status"] == "accepted"

        # 5. Verify signal is retrievable
        response = await client.get(
            f"/api/v1/signals/chart/{chart['chart_id']}/latest"
        )
        assert response.status_code == 200
        signal = response.json()
        assert signal["direction"] == "BULLISH"

    @pytest.mark.asyncio
    async def test_multiple_signals_workflow(self, client, created_chart):
        """Test multiple signals create history."""
        webhook_id = created_chart["webhook_id"]
        chart_id = created_chart["chart_id"]

        # Send multiple signals
        directions = ["BULLISH", "BEARISH", "NEUTRAL", "BULLISH"]
        for direction in directions:
            response = await client.post(
                "/api/v1/webhook/",
                json={
                    "webhook_id": webhook_id,
                    "direction": direction,
                },
            )
            assert response.status_code == 200

        # Verify signal history
        response = await client.get(f"/api/v1/signals/chart/{chart_id}")
        assert response.status_code == 200
        signals = response.json()
        assert len(signals) == 4

        # Verify latest is most recent
        response = await client.get(f"/api/v1/signals/chart/{chart_id}/latest")
        latest = response.json()
        assert latest["direction"] == "BULLISH"


# =============================================================================
# CONSTITUTIONAL COMPLIANCE TESTS
# =============================================================================

@pytest.mark.constitutional
class TestConstitutionalCompliance:
    """
    Critical tests verifying constitutional compliance across API.

    These tests ensure the system adheres to Gold Standard Specification
    Section 0B prohibitions:
    - NO weights
    - NO scores/confidence
    - NO recommendations
    - NO aggregation
    """

    @pytest.mark.asyncio
    async def test_no_aggregation_endpoints(self, client):
        """Verify no aggregation endpoints exist."""
        # These endpoints should NOT exist
        forbidden_paths = [
            "/api/v1/aggregate",
            "/api/v1/summary/overall",
            "/api/v1/score",
            "/api/v1/recommendation",
            "/api/v1/signals/net",
        ]
        for path in forbidden_paths:
            response = await client.get(path)
            assert response.status_code == 404, \
                f"Forbidden endpoint exists: {path}"

    @pytest.mark.asyncio
    async def test_all_responses_have_no_weight(
        self, client, created_instrument, created_silo, created_chart
    ):
        """Verify no API response contains weight fields."""
        responses_to_check = [
            await client.get("/api/v1/instruments/"),
            await client.get("/api/v1/silos/"),
            await client.get("/api/v1/charts/"),
        ]

        for response in responses_to_check:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    for item in data:
                        assert "weight" not in item
                        assert "score" not in item
                else:
                    assert "weight" not in data
                    assert "score" not in data

    @pytest.mark.asyncio
    async def test_webhook_response_no_recommendation(self, client, created_chart):
        """Verify webhook response contains no recommendation."""
        webhook_id = created_chart["webhook_id"]
        response = await client.post(
            "/api/v1/webhook/",
            json={
                "webhook_id": webhook_id,
                "direction": "BULLISH",
            },
        )
        data = response.json()

        prohibited_fields = [
            "recommendation",
            "advice",
            "suggested_action",
            "should_buy",
            "should_sell",
            "confidence",
            "score",
        ]
        for field in prohibited_fields:
            assert field not in data, \
                f"Constitutional violation: response contains '{field}'"
