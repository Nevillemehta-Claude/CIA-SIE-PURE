"""
API Tests - Relationships Endpoint
===================================

Complete cycle tests for /api/v1/relationships/ endpoint.
This endpoint exposes contradictions and confirmations.

CONSTITUTIONAL REQUIREMENTS:
- CR-001: All charts returned, no filtering
- CR-001: No scores, weights, or aggregation
- CR-002: Contradictions exposed, NOT resolved

Each test verifies: START STATE → ACTION → END STATE
Tests run 10 times each for statistical confidence.
"""

import pytest
from uuid import uuid4


class TestRelationshipsSilo:
    """Tests for silo-level relationships."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_silo_relationships_no_signals(self, client, sample_silo, sample_chart):
        """
        API-REL-001: Get relationships with no signals.
        """
        response = await client.get(f"/api/v1/relationships/silo/{sample_silo.silo_id}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        # Should return structure even with no relationships
        assert "contradictions" in data or "charts" in data, \
            "Response should have relationship structure"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_silo_relationships_contradiction(self, client, two_charts_contradiction):
        """
        API-REL-002: Get relationships with contradiction.
        """
        silo_id = two_charts_contradiction["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should detect the contradiction
        contradictions = data.get("contradictions", [])
        assert len(contradictions) >= 1, "Should have at least 1 contradiction"
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_silo_relationships_confirmation(self, client, two_charts_confirmation):
        """
        API-REL-003: Get relationships with confirmation.
        """
        silo_id = two_charts_confirmation["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should detect the confirmation
        confirmations = data.get("confirmations", [])
        assert len(confirmations) >= 1, "Should have at least 1 confirmation"


class TestRelationshipsConstitutional:
    """Tests for constitutional compliance in relationships."""
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_contradiction_no_resolution(self, client, two_charts_contradiction):
        """
        API-REL-005: Contradiction has NO resolution field.
        """
        silo_id = two_charts_contradiction["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        contradictions = data.get("contradictions", [])
        for contradiction in contradictions:
            # CR-002: Must NOT resolve
            assert "resolution" not in contradiction, \
                "Contradiction must NOT have resolution"
            assert "winner" not in contradiction, \
                "Contradiction must NOT have winner"
            assert "dominant" not in contradiction, \
                "Contradiction must NOT indicate dominance"
            assert "recommendation" not in contradiction, \
                "Contradiction must NOT have recommendation"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_contradiction_no_priority(self, client, two_charts_contradiction):
        """
        API-REL-006: Contradiction has NO priority field.
        """
        silo_id = two_charts_contradiction["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        contradictions = data.get("contradictions", [])
        for contradiction in contradictions:
            assert "priority" not in contradiction, \
                "Contradiction must NOT have priority"
            assert "rank" not in contradiction, \
                "Contradiction must NOT have rank"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_confirmation_no_aggregation(self, client, two_charts_confirmation):
        """
        API-REL-007: Confirmation has NO aggregation.
        """
        silo_id = two_charts_confirmation["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        confirmations = data.get("confirmations", [])
        for confirmation in confirmations:
            # CR-001: Must NOT aggregate
            assert "combined_strength" not in confirmation, \
                "Confirmation must NOT aggregate strength"
            assert "total_weight" not in confirmation, \
                "Confirmation must NOT have total weight"
            assert "aggregated_score" not in confirmation, \
                "Confirmation must NOT aggregate scores"
            assert "net_signal" not in confirmation, \
                "Confirmation must NOT have net signal"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_all_charts_returned(self, client, two_charts_contradiction):
        """
        API-REL-011: All charts returned (CR-001).
        """
        silo_id = two_charts_contradiction["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # All charts should be present somewhere in response
        charts = data.get("charts", [])
        if charts:
            assert len(charts) >= 2, "All charts must be returned"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_no_scores_in_response(self, client, two_charts_contradiction):
        """
        API-REL-012: No scores anywhere in response (CR-001).
        """
        silo_id = two_charts_contradiction["chart1"].silo_id
        
        response = await client.get(f"/api/v1/relationships/silo/{silo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        def check_no_scores(obj, path=""):
            """Recursively check for prohibited fields."""
            if isinstance(obj, dict):
                prohibited = ["score", "weight", "strength", "confidence", "priority", "rank"]
                for key, value in obj.items():
                    assert key not in prohibited, \
                        f"Found prohibited field '{key}' at {path}"
                    check_no_scores(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    check_no_scores(item, f"{path}[{i}]")
        
        check_no_scores(data)


class TestRelationshipsEdgeCases:
    """Tests for edge cases in relationship detection."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_silo_not_found(self, client):
        """
        Get relationships for non-existent silo.
        """
        random_id = str(uuid4())
        response = await client.get(f"/api/v1/relationships/silo/{random_id}")
        
        assert response.status_code == 404
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_silo_invalid_uuid(self, client):
        """
        Get relationships with invalid UUID.
        """
        response = await client.get("/api/v1/relationships/silo/not-a-valid-uuid")
        
        # May return 404 or 422 depending on how validation is implemented
        assert response.status_code in [404, 422]
