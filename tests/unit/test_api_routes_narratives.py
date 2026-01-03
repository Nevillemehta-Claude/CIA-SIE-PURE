"""
Tests for CIA-SIE Narratives API Routes
=======================================

Unit tests for narrative generation routes.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, UTC
from uuid import uuid4

from fastapi import HTTPException

from cia_sie.core.models import Narrative, NarrativeSection
from cia_sie.core.exceptions import AIProviderError


class TestGetExposer:
    """Tests for get_exposer dependency."""

    @pytest.mark.asyncio
    async def test_get_exposer_creates_exposer(self):
        """Test get_exposer creates proper RelationshipExposer."""
        from cia_sie.api.routes.narratives import get_exposer

        mock_session = Mock()

        with patch('cia_sie.api.routes.narratives.SiloRepository') as MockSiloRepo, \
             patch('cia_sie.api.routes.narratives.ChartRepository') as MockChartRepo, \
             patch('cia_sie.api.routes.narratives.SignalRepository') as MockSignalRepo, \
             patch('cia_sie.api.routes.narratives.RelationshipExposer') as MockExposer:

            exposer = await get_exposer(mock_session)

        MockSiloRepo.assert_called_once_with(mock_session)
        MockChartRepo.assert_called_once_with(mock_session)
        MockSignalRepo.assert_called_once_with(mock_session)
        MockExposer.assert_called_once()


class TestGetNarrativeGenerator:
    """Tests for get_narrative_generator dependency."""

    def test_get_narrative_generator_creates_generator(self):
        """Test get_narrative_generator creates NarrativeGenerator."""
        from cia_sie.api.routes.narratives import get_narrative_generator

        with patch('cia_sie.api.routes.narratives.ClaudeClient') as MockClient, \
             patch('cia_sie.api.routes.narratives.NarrativeGenerator') as MockGenerator:

            generator = get_narrative_generator()

        MockClient.assert_called_once()
        MockGenerator.assert_called_once()


class TestGenerateSiloNarrative:
    """Tests for generate_silo_narrative endpoint."""

    @pytest.fixture
    def mock_exposer(self):
        """Create mock relationship exposer."""
        exposer = Mock()
        exposer.expose_for_silo = AsyncMock()
        return exposer

    @pytest.fixture
    def mock_generator(self):
        """Create mock narrative generator."""
        generator = Mock()
        generator.generate_silo_narrative = AsyncMock()
        generator.generate_fallback_narrative = Mock()
        return generator

    @pytest.fixture
    def sample_summary(self):
        """Create sample relationship summary."""
        return {
            "silo_id": str(uuid4()),
            "silo_name": "Technical Analysis",
            "charts": [],
            "contradictions": [],
            "confirmations": [],
        }

    @pytest.fixture
    def sample_narrative(self):
        """Create sample narrative."""
        return Narrative(
            narrative_id=uuid4(),
            silo_id=uuid4(),
            sections=[
                NarrativeSection(
                    section_type="SIGNAL_SUMMARY",
                    content="The charts show mixed signals."
                )
            ],
            closing_statement="The interpretation and decision is yours.",
            generated_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_generate_silo_narrative_with_ai(
        self, mock_exposer, mock_generator, sample_summary, sample_narrative
    ):
        """Test generating narrative with AI."""
        from cia_sie.api.routes.narratives import generate_silo_narrative

        mock_exposer.expose_for_silo.return_value = sample_summary
        mock_generator.generate_silo_narrative.return_value = sample_narrative

        result = await generate_silo_narrative(
            silo_id="test_silo",
            use_ai=True,
            exposer=mock_exposer,
            generator=mock_generator,
        )

        assert result == sample_narrative
        mock_generator.generate_silo_narrative.assert_called_once_with(sample_summary)

    @pytest.mark.asyncio
    async def test_generate_silo_narrative_without_ai(
        self, mock_exposer, mock_generator, sample_summary, sample_narrative
    ):
        """Test generating narrative without AI (fallback)."""
        from cia_sie.api.routes.narratives import generate_silo_narrative

        mock_exposer.expose_for_silo.return_value = sample_summary
        mock_generator.generate_fallback_narrative.return_value = sample_narrative

        result = await generate_silo_narrative(
            silo_id="test_silo",
            use_ai=False,
            exposer=mock_exposer,
            generator=mock_generator,
        )

        assert result == sample_narrative
        mock_generator.generate_fallback_narrative.assert_called_once_with(sample_summary)

    @pytest.mark.asyncio
    async def test_generate_silo_narrative_silo_not_found(
        self, mock_exposer, mock_generator
    ):
        """Test generating narrative for non-existent silo."""
        from cia_sie.api.routes.narratives import generate_silo_narrative

        mock_exposer.expose_for_silo.side_effect = ValueError("Silo not found")

        with pytest.raises(HTTPException) as exc_info:
            await generate_silo_narrative(
                silo_id="unknown",
                use_ai=True,
                exposer=mock_exposer,
                generator=mock_generator,
            )

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_generate_silo_narrative_ai_error_fallback(
        self, mock_exposer, mock_generator, sample_summary, sample_narrative
    ):
        """Test falling back to non-AI when AI fails."""
        from cia_sie.api.routes.narratives import generate_silo_narrative

        mock_exposer.expose_for_silo.return_value = sample_summary
        mock_generator.generate_silo_narrative.side_effect = AIProviderError("API error")
        mock_generator.generate_fallback_narrative.return_value = sample_narrative

        result = await generate_silo_narrative(
            silo_id="test_silo",
            use_ai=True,
            exposer=mock_exposer,
            generator=mock_generator,
        )

        assert result == sample_narrative
        mock_generator.generate_fallback_narrative.assert_called_once()


class TestGetPlainTextNarrative:
    """Tests for get_plain_text_narrative endpoint."""

    @pytest.fixture
    def mock_exposer(self):
        """Create mock relationship exposer."""
        exposer = Mock()
        exposer.expose_for_silo = AsyncMock()
        return exposer

    @pytest.fixture
    def mock_generator(self):
        """Create mock narrative generator."""
        generator = Mock()
        generator.generate_silo_narrative = AsyncMock()
        generator.generate_fallback_narrative = Mock()
        return generator

    @pytest.fixture
    def sample_summary(self):
        """Create sample relationship summary."""
        return {
            "silo_id": str(uuid4()),
            "silo_name": "Test Silo",
            "charts": [],
            "contradictions": [],
            "confirmations": [],
        }

    @pytest.fixture
    def sample_narrative(self):
        """Create sample narrative."""
        return Narrative(
            narrative_id=uuid4(),
            silo_id=uuid4(),
            sections=[
                NarrativeSection(
                    section_type="SIGNAL_SUMMARY",
                    content="Section 1 content."
                ),
                NarrativeSection(
                    section_type="CONTRADICTION",
                    content="Section 2 content."
                ),
            ],
            closing_statement="The interpretation and decision is yours.",
            generated_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_plain_text_narrative_with_ai(
        self, mock_exposer, mock_generator, sample_summary, sample_narrative
    ):
        """Test plain text narrative with AI."""
        from cia_sie.api.routes.narratives import get_plain_text_narrative

        mock_exposer.expose_for_silo.return_value = sample_summary
        mock_generator.generate_silo_narrative.return_value = sample_narrative

        result = await get_plain_text_narrative(
            silo_id="test_silo",
            use_ai=True,
            exposer=mock_exposer,
            generator=mock_generator,
        )

        assert "Section 1 content." in result["narrative"]
        assert "Section 2 content." in result["narrative"]
        assert result["closing_statement"] == "The interpretation and decision is yours."

    @pytest.mark.asyncio
    async def test_plain_text_narrative_without_ai(
        self, mock_exposer, mock_generator, sample_summary, sample_narrative
    ):
        """Test plain text narrative without AI."""
        from cia_sie.api.routes.narratives import get_plain_text_narrative

        mock_exposer.expose_for_silo.return_value = sample_summary
        mock_generator.generate_fallback_narrative.return_value = sample_narrative

        result = await get_plain_text_narrative(
            silo_id="test_silo",
            use_ai=False,
            exposer=mock_exposer,
            generator=mock_generator,
        )

        assert "narrative" in result
        assert "closing_statement" in result

    @pytest.mark.asyncio
    async def test_plain_text_narrative_silo_not_found(
        self, mock_exposer, mock_generator
    ):
        """Test plain text for non-existent silo."""
        from cia_sie.api.routes.narratives import get_plain_text_narrative

        mock_exposer.expose_for_silo.side_effect = ValueError("Not found")

        with pytest.raises(HTTPException) as exc_info:
            await get_plain_text_narrative(
                silo_id="unknown",
                use_ai=True,
                exposer=mock_exposer,
                generator=mock_generator,
            )

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_plain_text_narrative_ai_error_fallback(
        self, mock_exposer, mock_generator, sample_summary, sample_narrative
    ):
        """Test plain text falls back when AI fails."""
        from cia_sie.api.routes.narratives import get_plain_text_narrative

        mock_exposer.expose_for_silo.return_value = sample_summary
        mock_generator.generate_silo_narrative.side_effect = AIProviderError("Error")
        mock_generator.generate_fallback_narrative.return_value = sample_narrative

        result = await get_plain_text_narrative(
            silo_id="test_silo",
            use_ai=True,
            exposer=mock_exposer,
            generator=mock_generator,
        )

        assert "note" in result
        assert "fallback" in result["note"].lower()


class TestNarrativesConstitutionalCompliance:
    """Constitutional compliance tests for narratives routes."""

    @pytest.mark.constitutional
    def test_narrative_has_closing_statement(self):
        """CRITICAL: Narratives must have closing statement."""
        assert "closing_statement" in Narrative.model_fields

    @pytest.mark.constitutional
    def test_narrative_no_recommendation_field(self):
        """CRITICAL: Narrative must not have recommendation field."""
        assert "recommendation" not in Narrative.model_fields
        assert "advice" not in Narrative.model_fields
        assert "suggested_action" not in Narrative.model_fields

    @pytest.mark.constitutional
    def test_narrative_no_score_field(self):
        """CRITICAL: Narrative must not have score field."""
        assert "score" not in Narrative.model_fields
        assert "confidence" not in Narrative.model_fields
        assert "overall_direction" not in Narrative.model_fields

    @pytest.mark.constitutional
    def test_no_recommendation_methods_in_routes(self):
        """CRITICAL: Routes module must not have recommendation methods."""
        import cia_sie.api.routes.narratives as narratives_module

        prohibited = ['recommend', 'advise', 'compute_score', 'aggregate']
        for method in prohibited:
            assert not hasattr(narratives_module, method), \
                f"CONSTITUTIONAL VIOLATION: narratives module has {method}"
