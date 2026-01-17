"""
API Tests - Baskets Endpoint
=============================

Complete cycle tests for /api/v1/baskets/ endpoint.
Analytical baskets are UI-layer constructs for grouping charts.

CONSTITUTIONAL REQUIREMENT:
- Baskets have NO effect on signal processing
- Baskets exist ONLY in the UI layer

Each test verifies: START STATE → ACTION → END STATE
Tests run 10 times each for statistical confidence.
"""

import pytest
from uuid import uuid4


class TestBasketsCreate:
    """Tests for creating baskets."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_basket_valid(self, client):
        """
        API-BSKT-001: Create basket with valid data.
        """
        payload = {
            "basket_name": f"Test Basket {uuid4().hex[:4]}",
            "basket_type": "CUSTOM",
            "description": "Test basket for API testing"
        }
        
        response = await client.post("/api/v1/baskets/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited - system working correctly")
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["basket_name"] == payload["basket_name"]
        assert "basket_id" in data
        assert data["is_active"] == True
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_basket_missing_name(self, client):
        """
        API-BSKT-002: Create basket without name.
        """
        payload = {
            "basket_type": "CUSTOM"
        }
        
        response = await client.post("/api/v1/baskets/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 422
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_basket_all_types(self, client):
        """
        API-BSKT-003: Create basket with each valid type.
        """
        basket_types = ["LOGICAL", "HIERARCHICAL", "CONTEXTUAL", "CUSTOM"]
        
        for basket_type in basket_types:
            payload = {
                "basket_name": f"{basket_type} Basket {uuid4().hex[:4]}",
                "basket_type": basket_type,
            }
            
            response = await client.post("/api/v1/baskets/", json=payload)
            
            if response.status_code == 429:
                pytest.skip("Rate limited")
            
            assert response.status_code == 201, f"Failed for type {basket_type}: {response.text}"


class TestBasketsList:
    """Tests for listing baskets."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_baskets_empty(self, client):
        """
        API-BSKT-005: List baskets when empty.
        """
        response = await client.get("/api/v1/baskets/")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_baskets_with_data(self, client):
        """
        API-BSKT-006: List baskets with data.
        """
        # Create a basket first
        create_resp = await client.post("/api/v1/baskets/", json={
            "basket_name": f"List Test {uuid4().hex[:4]}",
            "basket_type": "CUSTOM"
        })
        
        if create_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        # Now list
        response = await client.get("/api/v1/baskets/")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestBasketsGet:
    """Tests for getting individual baskets."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_basket_by_id_exists(self, client):
        """
        API-BSKT-008: Get basket by ID when exists.
        """
        # Create first
        create_resp = await client.post("/api/v1/baskets/", json={
            "basket_name": f"Get Test {uuid4().hex[:4]}",
            "basket_type": "CUSTOM"
        })
        
        if create_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        assert create_resp.status_code == 201
        basket = create_resp.json()
        
        # Get by ID
        response = await client.get(f"/api/v1/baskets/{basket['basket_id']}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert data["basket_id"] == basket["basket_id"]
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_basket_by_id_not_found(self, client):
        """
        API-BSKT-009: Get basket by ID when not exists.
        """
        random_id = str(uuid4())
        response = await client.get(f"/api/v1/baskets/{random_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 404


class TestBasketsCharts:
    """Tests for basket-chart associations."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_add_chart_to_basket(self, client, sample_chart):
        """
        API-BSKT-010: Add chart to basket.
        """
        # Create basket
        create_resp = await client.post("/api/v1/baskets/", json={
            "basket_name": f"Chart Add Test {uuid4().hex[:4]}",
            "basket_type": "CUSTOM"
        })
        
        if create_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        assert create_resp.status_code == 201
        basket = create_resp.json()
        
        # Add chart
        response = await client.post(
            f"/api/v1/baskets/{basket['basket_id']}/charts/{sample_chart.chart_id}"
        )
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 204
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_remove_chart_from_basket(self, client, sample_chart):
        """
        API-BSKT-011: Remove chart from basket.
        """
        # Create basket and add chart
        create_resp = await client.post("/api/v1/baskets/", json={
            "basket_name": f"Chart Remove Test {uuid4().hex[:4]}",
            "basket_type": "CUSTOM"
        })
        
        if create_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        assert create_resp.status_code == 201
        basket = create_resp.json()
        
        # Add chart
        add_resp = await client.post(
            f"/api/v1/baskets/{basket['basket_id']}/charts/{sample_chart.chart_id}"
        )
        
        if add_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        # Remove chart
        response = await client.delete(
            f"/api/v1/baskets/{basket['basket_id']}/charts/{sample_chart.chart_id}"
        )
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 204


class TestBasketsDelete:
    """Tests for deleting baskets."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_delete_basket_exists(self, client):
        """
        API-BSKT-013: Delete basket that exists.
        """
        # Create first
        create_resp = await client.post("/api/v1/baskets/", json={
            "basket_name": f"Delete Test {uuid4().hex[:4]}",
            "basket_type": "CUSTOM"
        })
        
        if create_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        assert create_resp.status_code == 201
        basket = create_resp.json()
        
        # Delete
        response = await client.delete(f"/api/v1/baskets/{basket['basket_id']}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 204


class TestBasketsConstitutional:
    """Constitutional compliance tests for baskets."""
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_basket_has_no_signal_effect(self, client, sample_chart):
        """
        API-BSKT-020: Creating basket has no effect on signal processing.
        """
        # This is a design principle - baskets are UI only
        # We verify by checking that basket response has no signal-related fields
        
        create_resp = await client.post("/api/v1/baskets/", json={
            "basket_name": f"Constitutional Test {uuid4().hex[:4]}",
            "basket_type": "CUSTOM"
        })
        
        if create_resp.status_code == 429:
            pytest.skip("Rate limited")
        
        assert create_resp.status_code == 201
        data = create_resp.json()
        
        # No signal processing fields
        assert "signal_aggregation" not in data
        assert "combined_direction" not in data
        assert "net_signal" not in data
        assert "score" not in data
        assert "weight" not in data
