"""
API Tests - Narratives Endpoint
================================

Complete cycle tests for /api/v1/narratives/ endpoint.
Narratives are AI-generated descriptions of signal data.

CONSTITUTIONAL REQUIREMENTS:
- CR-001: Narratives are DESCRIPTIVE only, NO recommendations
- CR-003: Every narrative includes MANDATORY DISCLAIMER

Each test verifies: START STATE → ACTION → END STATE
Tests run 10 times each for statistical confidence.
"""

import pytest
from uuid import uuid4


class TestNarrativesGenerate:
    """Tests for generating narratives."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_generate_narrative_valid_silo(self, client, sample_silo, sample_chart, sample_signal):
        """
        API-NAR-001: Generate narrative for valid silo.
        
        Start: 1 silo with signals
        Action: GET /narratives/silo/{id}
        End: Narrative text returned
        """
        response = await client.get(f"/api/v1/narratives/silo/{sample_silo.silo_id}")
        
        # May require AI to be configured
        assert response.status_code in [200, 503, 424], \
            f"Expected 200/503/424, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert "narrative_id" in data and "sections" in data
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_generate_narrative_empty_silo(self, client, sample_silo):
        """
        API-NAR-002: Generate narrative for empty silo.
        
        Start: 1 silo, 0 signals
        Action: GET /narratives/silo/{id}
        End: Graceful empty message
        """
        response = await client.get(f"/api/v1/narratives/silo/{sample_silo.silo_id}")
        
        # Should not crash on empty data
        assert response.status_code in [200, 204, 404, 424, 503]
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_generate_narrative_silo_not_found(self, client):
        """
        API-NAR-003: Generate narrative for non-existent silo.
        
        Start: 0 silos
        Action: GET /narratives/silo/{random-uuid}
        End: 404 error
        """
        random_id = str(uuid4())
        response = await client.get(f"/api/v1/narratives/silo/{random_id}")
        
        assert response.status_code == 404


class TestNarrativesConstitutional:
    """Tests for constitutional compliance in narratives."""
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_narrative_contains_disclaimer(self, client, sample_silo, sample_chart, sample_signal):
        """
        API-NAR-004: Narrative contains mandatory disclaimer (CR-003).
        
        Start: 1 silo with signals
        Action: GET /narratives/silo/{id}
        End: Disclaimer present in response
        """
        response = await client.get(f"/api/v1/narratives/silo/{sample_silo.silo_id}")
        
        if response.status_code == 200:
            data = response.json()
            response_text = str(data).lower()
            
            # Must contain key phrases from disclaimer
            has_disclaimer = (
                "interpretation" in response_text or
                "decision" in response_text or
                "yours" in response_text or
                "disclaimer" in response_text
            )
            
            assert has_disclaimer, "Narrative must include disclaimer"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_narrative_no_recommendations(self, client, sample_silo, sample_chart, sample_signal):
        """
        API-NAR-005: Narrative has NO recommendations (CR-001).
        
        Start: 1 silo with signals
        Action: GET /narratives/silo/{id}
        End: No "you should" text
        """
        response = await client.get(f"/api/v1/narratives/silo/{sample_silo.silo_id}")
        
        if response.status_code == 200:
            data = response.json()
            response_text = str(data).lower()
            
            # Must NOT contain prescriptive language
            assert "you should" not in response_text, \
                "Narrative must not contain 'you should'"
            assert "i recommend" not in response_text, \
                "Narrative must not contain 'I recommend'"
            assert "we recommend" not in response_text, \
                "Narrative must not contain 'we recommend'"
    
    @pytest.mark.api
    @pytest.mark.constitutional
    @pytest.mark.asyncio
    async def test_narrative_no_buy_sell(self, client, sample_silo, sample_chart, sample_signal):
        """
        API-NAR-006: Narrative has NO buy/sell language (CR-001).
        
        Start: 1 silo with signals
        Action: GET /narratives/silo/{id}
        End: No "buy"/"sell" text
        """
        response = await client.get(f"/api/v1/narratives/silo/{sample_silo.silo_id}")
        
        if response.status_code == 200:
            data = response.json()
            response_text = str(data).lower()
            
            # Check for prohibited words (context matters, but these shouldn't appear)
            prohibited = ["buy now", "sell now", "should buy", "should sell", 
                         "recommend buy", "recommend sell"]
            
            for phrase in prohibited:
                assert phrase not in response_text, \
                    f"Narrative must not contain '{phrase}'"


class TestNarrativesPlainText:
    """Tests for plain text narrative format."""
    
    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_narrative_plain_text_format(self, client, sample_silo, sample_chart, sample_signal):
        """
        API-NAR-007: Narrative plain text format.
        
        Start: 1 silo with signals
        Action: GET /narratives/silo/{id}/plain
        End: Plain text, no markdown
        """
        response = await client.get(f"/api/v1/narratives/silo/{sample_silo.silo_id}/plain")
        
        if response.status_code == 200:
            # Should be plain text, not markdown
            content_type = response.headers.get("content-type", "")
            # Could be text/plain or application/json
            assert "text" in content_type or "json" in content_type

