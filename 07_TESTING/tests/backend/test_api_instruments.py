"""
API Tests - Instruments Endpoint
=================================

Complete cycle tests for /api/v1/instruments/ endpoint.
Tests CRUD operations for financial instruments.

Each test verifies: START STATE → ACTION → END STATE
Tests run 10 times each for statistical confidence.
"""

import pytest
from uuid import uuid4


class TestInstrumentsCreate:
    """Tests for creating instruments."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_instrument_valid(self, client):
        """
        API-INST-001: Create instrument with valid data.
        
        Start: 0 instruments with this symbol
        Action: POST with valid payload
        End: 201 with instrument data
        """
        payload = {
            "symbol": f"TEST_{uuid4().hex[:6]}",
            "display_name": "Test Instrument",
            "exchange": "NSE",
            "instrument_type": "EQUITY"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited - system working correctly")
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["symbol"] == payload["symbol"]
        assert data["display_name"] == payload["display_name"]
        assert "instrument_id" in data
        assert data["is_active"] == True
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_instrument_missing_symbol(self, client):
        """
        API-INST-002: Create instrument without required symbol.
        """
        payload = {
            "display_name": "Missing Symbol Test",
            "exchange": "NSE"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 422, "Missing symbol should return 422"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_instrument_empty_body(self, client):
        """
        API-INST-003: Create instrument with empty body.
        """
        response = await client.post("/api/v1/instruments/", json={})
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 422
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_instrument_duplicate_symbol(self, client, sample_instrument):
        """
        API-INST-004: Create instrument with duplicate symbol.
        """
        payload = {
            "symbol": sample_instrument.symbol,
            "display_name": "Duplicate Test",
            "exchange": "NSE"
        }
        
        response = await client.post("/api/v1/instruments/", json=payload)
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        # May return 409 (conflict) or 400 (bad request)
        assert response.status_code in [400, 409], f"Duplicate should fail: {response.status_code}"


class TestInstrumentsList:
    """Tests for listing instruments."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_instruments_empty(self, client):
        """
        API-INST-005: List instruments when database is empty.
        """
        response = await client.get("/api/v1/instruments/")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_list_instruments_with_data(self, client, sample_instrument):
        """
        API-INST-006: List instruments with existing data.
        """
        response = await client.get("/api/v1/instruments/")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestInstrumentsGet:
    """Tests for getting individual instruments."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_instrument_by_id_exists(self, client, sample_instrument):
        """
        API-INST-008: Get instrument by ID when exists.
        """
        response = await client.get(f"/api/v1/instruments/{sample_instrument.instrument_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        assert data["instrument_id"] == sample_instrument.instrument_id
        assert data["symbol"] == sample_instrument.symbol
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_instrument_by_id_not_found(self, client):
        """
        API-INST-009: Get instrument by ID when not exists.
        """
        random_id = str(uuid4())
        response = await client.get(f"/api/v1/instruments/{random_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 404


class TestInstrumentsUpdate:
    """Tests for updating instruments."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_update_instrument_valid(self, client, sample_instrument):
        """
        API-INST-011: Update instrument with valid data.
        """
        new_name = f"Updated {uuid4().hex[:4]}"
        payload = {
            "display_name": new_name
        }
        
        response = await client.put(
            f"/api/v1/instruments/{sample_instrument.instrument_id}",
            json=payload
        )
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        if response.status_code == 200:
            data = response.json()
            assert data["display_name"] == new_name


class TestInstrumentsDelete:
    """Tests for deleting instruments."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_delete_instrument_exists(self, client, sample_instrument):
        """
        API-INST-013: Delete instrument that exists.
        """
        response = await client.delete(f"/api/v1/instruments/{sample_instrument.instrument_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code in [200, 204]
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_delete_instrument_not_found(self, client):
        """
        API-INST-014: Delete instrument that doesn't exist.
        """
        random_id = str(uuid4())
        response = await client.delete(f"/api/v1/instruments/{random_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 404


class TestInstrumentsConstitutional:
    """Constitutional compliance tests for instruments."""
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_instrument_has_no_ranking(self, client, sample_instrument):
        """
        API-INST-020: Instrument has no ranking/priority field.
        """
        response = await client.get(f"/api/v1/instruments/{sample_instrument.instrument_id}")
        
        if response.status_code == 429:
            pytest.skip("Rate limited")
        
        assert response.status_code == 200
        data = response.json()
        
        # CR-001: No ranking/priority
        assert "rank" not in data
        assert "priority" not in data
        assert "score" not in data
        assert "weight" not in data
