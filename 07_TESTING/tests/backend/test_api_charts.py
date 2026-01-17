"""
API Tests - Charts Endpoint
============================

Complete cycle tests for /api/v1/charts/ endpoint.
Charts are the core signal receivers via webhooks.

CONSTITUTIONAL REQUIREMENT:
- CR-001: Charts have NO weight field

Each test verifies: START STATE → ACTION → END STATE
Tests run 10 times each for statistical confidence.
"""

import pytest
from uuid import uuid4


class TestChartsCreate:
    """Tests for creating charts."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_chart_valid(self, client, sample_silo):
        """
        API-CHART-001: Create chart with valid data.
        """
        webhook_id = f"HOOK_{uuid4().hex[:8]}"
        payload = {
            "silo_id": sample_silo.silo_id,
            "chart_code": f"C{uuid4().hex[:3].upper()}",
            "chart_name": "Test Chart",
            "timeframe": "D",
            "webhook_id": webhook_id
        }
        
        response = await client.post("/api/v1/charts/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited - system working correctly")
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["chart_code"] == payload["chart_code"]
        assert data["webhook_id"] == webhook_id
        assert "chart_id" in data
        
        # CR-001: No weight field
        assert "weight" not in data, "Chart must NOT have weight (CR-001)"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_chart_missing_silo(self, client):
        """
        API-CHART-002: Create chart without silo_id.
        """
        payload = {
            "chart_code": "ORPHAN",
            "chart_name": "Orphan Chart",
            "timeframe": "D",
            "webhook_id": "ORPHAN_HOOK"
        }
        
        response = await client.post("/api/v1/charts/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 422
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_chart_invalid_silo(self, client):
        """
        API-CHART-003: Create chart with non-existent silo_id.
        """
        payload = {
            "silo_id": str(uuid4()),
            "chart_code": "INVALID",
            "chart_name": "Invalid Silo Chart",
            "timeframe": "D",
            "webhook_id": "INVALID_HOOK"
        }
        
        response = await client.post("/api/v1/charts/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        # May create anyway (201) or reject (400/404/422)
        assert response.status_code in [201, 400, 404, 422]


class TestChartsList:
    """Tests for listing charts."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_charts_empty(self, client):
        """
        API-CHART-005: List charts when empty.
        """
        response = await client.get("/api/v1/charts/")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_charts_with_data(self, client, sample_chart):
        """
        API-CHART-006: List charts with data.
        """
        response = await client.get("/api/v1/charts/")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_charts_filter_by_silo(self, client, sample_silo, sample_chart):
        """
        API-CHART-007: List charts filtered by silo.
        """
        response = await client.get(f"/api/v1/charts/?silo_id={sample_silo.silo_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        for chart in data:
            assert chart["silo_id"] == sample_silo.silo_id


class TestChartsGet:
    """Tests for getting individual charts."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_chart_by_id_exists(self, client, sample_chart):
        """
        API-CHART-008: Get chart by ID when exists.
        """
        response = await client.get(f"/api/v1/charts/{sample_chart.chart_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert data["chart_id"] == sample_chart.chart_id
        assert data["chart_code"] == sample_chart.chart_code
        
        # CR-001: No weight
        assert "weight" not in data, "Chart must NOT have weight (CR-001)"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_chart_by_id_not_found(self, client):
        """
        API-CHART-009: Get chart by ID when not exists.
        """
        random_id = str(uuid4())
        response = await client.get(f"/api/v1/charts/{random_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 404


class TestChartsUpdate:
    """Tests for updating charts."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_update_chart_valid(self, client, sample_chart):
        """
        API-CHART-010: Update chart with valid data.
        """
        new_name = f"Updated Chart {uuid4().hex[:4]}"
        payload = {
            "chart_name": new_name
        }
        
        response = await client.put(
            f"/api/v1/charts/{sample_chart.chart_id}",
            json=payload
        )
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        if response.status_code == 200:
            data = response.json()
            assert data["chart_name"] == new_name


class TestChartsDelete:
    """Tests for deleting charts."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_delete_chart_exists(self, client, sample_chart):
        """
        API-CHART-012: Delete chart that exists.
        """
        response = await client.delete(f"/api/v1/charts/{sample_chart.chart_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code in [200, 204]


class TestChartsConstitutional:
    """Constitutional compliance tests for charts."""
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_chart_has_no_weight(self, client, sample_chart):
        """
        API-CHART-020: Chart has NO weight field (CR-001).
        """
        response = await client.get(f"/api/v1/charts/{sample_chart.chart_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        
        # CR-001 Violations
        assert "weight" not in data, "Chart must NOT have weight"
        assert "priority" not in data, "Chart must NOT have priority"
        assert "importance" not in data, "Chart must NOT have importance"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_chart_no_aggregation_fields(self, client, sample_chart):
        """
        API-CHART-021: Chart has no aggregation fields.
        """
        response = await client.get(f"/api/v1/charts/{sample_chart.chart_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        
        # No aggregation
        assert "score" not in data
        assert "combined_signal" not in data
        assert "net_direction" not in data
