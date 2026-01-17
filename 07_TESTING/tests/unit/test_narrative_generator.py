"""
Tests for CIA-SIE Narrative Generator
=====================================

Validates AI-powered narrative generation.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from uuid import uuid4

from cia_sie.ai.narrative_generator import (
    NarrativeGenerator,
    REQUIRED_CLOSING,
)
from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
from cia_sie.core.enums import (
    Direction,
    SignalType,
    FreshnessStatus,
    NarrativeSectionType,
    ValidationStatus,
)
from cia_sie.core.models import (
    Signal,
    ChartSignalStatus,
    RelationshipSummary,
    Contradiction,
    Confirmation,
    Narrative,
    NarrativeSection,
)


class TestNarrativeGeneratorInitialization:
    """Tests for NarrativeGenerator initialization."""

    def test_init_with_defaults(self):
        """Test initialization with defaults."""
        with patch("cia_sie.ai.narrative_generator.ClaudeClient"):
            with patch("cia_sie.ai.narrative_generator.NarrativePromptBuilder"):
                with patch("cia_sie.ai.narrative_generator.AIResponseValidator"):
                    generator = NarrativeGenerator()

                    assert generator.claude is not None
                    assert generator.prompt_builder is not None
                    assert generator.validator is not None
                    assert generator.max_retries == 3

    def test_init_with_custom_components(self):
        """Test initialization with custom components."""
        mock_client = Mock()
        mock_builder = Mock()
        mock_validator = Mock()

        generator = NarrativeGenerator(
            claude_client=mock_client,
            prompt_builder=mock_builder,
            validator=mock_validator,
            max_retries=5,
        )

        assert generator.claude is mock_client
        assert generator.prompt_builder is mock_builder
        assert generator.validator is mock_validator
        assert generator.max_retries == 5


class TestGenerateSiloNarrative:
    """Tests for silo narrative generation."""

    @pytest.fixture
    def mock_claude(self):
        """Create mock Claude client."""
        client = Mock()
        client.generate = AsyncMock()
        return client

    @pytest.fixture
    def mock_prompt_builder(self):
        """Create mock prompt builder."""
        builder = Mock()
        builder.system_prompt = "System prompt"
        builder.build_silo_narrative_prompt = Mock(return_value="User prompt")
        return builder

    @pytest.fixture
    def mock_validator(self):
        """Create mock validator."""
        validator = Mock()
        result = Mock()
        result.is_valid = True
        result.status = ValidationStatus.VALID
        result.violations = []
        result.remediated_text = None
        validator.validate = Mock(return_value=result)
        return validator

    @pytest.fixture
    def generator(self, mock_claude, mock_prompt_builder, mock_validator):
        """Create generator with mocks."""
        gen = NarrativeGenerator(
            claude_client=mock_claude,
            prompt_builder=mock_prompt_builder,
            validator=mock_validator,
        )
        gen._validated_generator = Mock()
        gen._validated_generator.generate = AsyncMock(
            return_value="Generated narrative text"
        )
        return gen

    @pytest.fixture
    def sample_summary(self):
        """Create sample relationship summary."""
        signal = Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={"rsi": 72.5},
            raw_payload={},
        )
        chart = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
            latest_signal=signal,
            freshness=FreshnessStatus.CURRENT,
        )
        return RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Technical",
            instrument_id=uuid4(),
            instrument_symbol="NIFTY50",
            charts=[chart],
            contradictions=[],
            confirmations=[],
            generated_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_returns_narrative_object(self, generator, sample_summary):
        """Test returns Narrative object."""
        result = await generator.generate_silo_narrative(sample_summary)

        assert isinstance(result, Narrative)

    @pytest.mark.asyncio
    async def test_narrative_has_sections(self, generator, sample_summary):
        """Test narrative has sections."""
        result = await generator.generate_silo_narrative(sample_summary)

        assert len(result.sections) >= 1

    @pytest.mark.asyncio
    async def test_narrative_has_closing_statement(self, generator, sample_summary):
        """Test narrative has required closing statement."""
        result = await generator.generate_silo_narrative(sample_summary)

        assert result.closing_statement == REQUIRED_CLOSING

    @pytest.mark.asyncio
    async def test_narrative_includes_silo_id(self, generator, sample_summary):
        """Test narrative includes silo ID."""
        result = await generator.generate_silo_narrative(sample_summary)

        assert result.silo_id == sample_summary.silo_id

    @pytest.mark.asyncio
    async def test_narrative_has_generated_timestamp(self, generator, sample_summary):
        """Test narrative has generation timestamp."""
        result = await generator.generate_silo_narrative(sample_summary)

        assert result.generated_at is not None

    @pytest.mark.asyncio
    async def test_builds_prompt_from_summary(self, generator, sample_summary, mock_prompt_builder):
        """Test prompt is built from summary."""
        await generator.generate_silo_narrative(sample_summary)

        mock_prompt_builder.build_silo_narrative_prompt.assert_called_once_with(
            sample_summary
        )


class TestGenerateSiloNarrativeWithContradictions:
    """Tests for narrative generation with contradictions."""

    @pytest.fixture
    def generator_with_mocks(self):
        """Create generator with mocks."""
        mock_claude = Mock()
        mock_claude.generate = AsyncMock(return_value="Narrative text")

        mock_builder = Mock()
        mock_builder.system_prompt = "System"
        mock_builder.build_silo_narrative_prompt = Mock(return_value="Prompt")

        mock_validator = Mock()
        result = Mock()
        result.is_valid = True
        result.status = ValidationStatus.VALID
        result.violations = []
        result.remediated_text = None
        mock_validator.validate = Mock(return_value=result)

        gen = NarrativeGenerator(
            claude_client=mock_claude,
            prompt_builder=mock_builder,
            validator=mock_validator,
        )
        gen._validated_generator = Mock()
        gen._validated_generator.generate = AsyncMock(return_value="Generated text")
        return gen

    @pytest.fixture
    def summary_with_contradictions(self):
        """Create summary with contradictions."""
        chart1 = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI",
            chart_name="RSI",
            timeframe="1h",
            latest_signal=Signal(
                signal_id=uuid4(),
                chart_id=uuid4(),
                received_at=datetime.now(UTC),
                signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE,
                direction=Direction.BULLISH,
                indicators={},
                raw_payload={},
            ),
            freshness=FreshnessStatus.CURRENT,
        )
        chart2 = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="MACD",
            chart_name="MACD",
            timeframe="1h",
            latest_signal=Signal(
                signal_id=uuid4(),
                chart_id=uuid4(),
                received_at=datetime.now(UTC),
                signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE,
                direction=Direction.BEARISH,
                indicators={},
                raw_payload={},
            ),
            freshness=FreshnessStatus.CURRENT,
        )
        contradiction = Contradiction(
            chart_a_id=chart1.chart_id,
            chart_a_name="RSI",
            chart_a_direction=Direction.BULLISH,
            chart_b_id=chart2.chart_id,
            chart_b_name="MACD",
            chart_b_direction=Direction.BEARISH,
            detected_at=datetime.now(UTC),
        )
        return RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Technical",
            instrument_id=uuid4(),
            instrument_symbol="NIFTY50",
            charts=[chart1, chart2],
            contradictions=[contradiction],
            confirmations=[],
            generated_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_includes_contradiction_section(
        self, generator_with_mocks, summary_with_contradictions
    ):
        """Test narrative includes contradiction section."""
        result = await generator_with_mocks.generate_silo_narrative(
            summary_with_contradictions
        )

        contradiction_sections = [
            s for s in result.sections
            if s.section_type == NarrativeSectionType.CONTRADICTION
        ]
        assert len(contradiction_sections) == 1

    @pytest.mark.asyncio
    async def test_contradiction_section_references_charts(
        self, generator_with_mocks, summary_with_contradictions
    ):
        """Test contradiction section references relevant charts."""
        result = await generator_with_mocks.generate_silo_narrative(
            summary_with_contradictions
        )

        contradiction_section = [
            s for s in result.sections
            if s.section_type == NarrativeSectionType.CONTRADICTION
        ][0]

        assert len(contradiction_section.referenced_chart_ids) > 0


class TestGenerateChartNarrative:
    """Tests for single chart narrative generation."""

    @pytest.fixture
    def generator_with_mocks(self):
        """Create generator with mocks."""
        mock_claude = Mock()
        mock_claude.generate = AsyncMock(return_value="Chart narrative")

        mock_builder = Mock()
        mock_builder.system_prompt = "System"
        mock_builder.build_chart_narrative_prompt = Mock(return_value="Prompt")

        mock_validator = Mock()
        result = Mock()
        result.is_valid = True
        result.status = ValidationStatus.VALID
        result.violations = []
        result.remediated_text = None
        mock_validator.validate = Mock(return_value=result)

        gen = NarrativeGenerator(
            claude_client=mock_claude,
            prompt_builder=mock_builder,
            validator=mock_validator,
        )
        gen._validated_generator = Mock()
        gen._validated_generator.generate = AsyncMock(return_value="Chart description")
        return gen

    @pytest.fixture
    def chart_status(self):
        """Create chart status."""
        return ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
            latest_signal=Signal(
                signal_id=uuid4(),
                chart_id=uuid4(),
                received_at=datetime.now(UTC),
                signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE,
                direction=Direction.BULLISH,
                indicators={"rsi": 72.5},
                raw_payload={},
            ),
            freshness=FreshnessStatus.CURRENT,
        )

    @pytest.mark.asyncio
    async def test_returns_narrative_object(self, generator_with_mocks, chart_status):
        """Test returns Narrative object."""
        result = await generator_with_mocks.generate_chart_narrative(
            chart_status, "NIFTY50"
        )

        assert isinstance(result, Narrative)

    @pytest.mark.asyncio
    async def test_includes_closing_statement(self, generator_with_mocks, chart_status):
        """Test includes closing statement."""
        result = await generator_with_mocks.generate_chart_narrative(
            chart_status, "NIFTY50"
        )

        assert result.closing_statement == REQUIRED_CLOSING


class TestFallbackNarrative:
    """Tests for fallback narrative generation."""

    @pytest.fixture
    def generator(self):
        """Create generator."""
        return NarrativeGenerator(
            claude_client=Mock(),
            prompt_builder=Mock(),
            validator=Mock(),
        )

    @pytest.fixture
    def sample_summary(self):
        """Create sample summary."""
        chart = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI",
            chart_name="RSI",
            timeframe="1h",
            latest_signal=Signal(
                signal_id=uuid4(),
                chart_id=uuid4(),
                received_at=datetime.now(UTC),
                signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE,
                direction=Direction.BULLISH,
                indicators={},
                raw_payload={},
            ),
            freshness=FreshnessStatus.CURRENT,
        )
        return RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Technical",
            instrument_id=uuid4(),
            instrument_symbol="NIFTY50",
            charts=[chart],
            contradictions=[],
            confirmations=[],
            generated_at=datetime.now(UTC),
        )

    def test_fallback_returns_narrative(self, generator, sample_summary):
        """Test fallback returns Narrative object."""
        result = generator.generate_fallback_narrative(sample_summary)

        assert isinstance(result, Narrative)

    def test_fallback_includes_symbol(self, generator, sample_summary):
        """Test fallback includes instrument symbol."""
        result = generator.generate_fallback_narrative(sample_summary)

        content = result.sections[0].content
        assert "NIFTY50" in content

    def test_fallback_includes_silo_name(self, generator, sample_summary):
        """Test fallback includes silo name."""
        result = generator.generate_fallback_narrative(sample_summary)

        content = result.sections[0].content
        assert "Technical" in content

    def test_fallback_includes_chart_direction(self, generator, sample_summary):
        """Test fallback includes chart direction."""
        result = generator.generate_fallback_narrative(sample_summary)

        content = result.sections[0].content
        assert "BULLISH" in content

    def test_fallback_has_closing_statement(self, generator, sample_summary):
        """Test fallback has closing statement."""
        result = generator.generate_fallback_narrative(sample_summary)

        assert result.closing_statement == REQUIRED_CLOSING


class TestNarrativeGeneratorConstitutionalCompliance:
    """
    Tests verifying NarrativeGenerator maintains constitutional compliance.

    CRITICAL: Generated narratives must be DESCRIPTIVE, never PRESCRIPTIVE.
    """

    def test_required_closing_is_mandatory_disclaimer(self):
        """Test REQUIRED_CLOSING matches MANDATORY_DISCLAIMER."""
        assert REQUIRED_CLOSING == MANDATORY_DISCLAIMER

    def test_no_aggregation_method(self):
        """
        CRITICAL: NarrativeGenerator must not aggregate.
        """
        assert not hasattr(NarrativeGenerator, "generate_aggregate_narrative")
        assert not hasattr(NarrativeGenerator, "compute_overall_direction")

    def test_no_recommendation_method(self):
        """
        CRITICAL: NarrativeGenerator must not make recommendations.
        """
        assert not hasattr(NarrativeGenerator, "generate_recommendation")
        assert not hasattr(NarrativeGenerator, "recommend_action")
        assert not hasattr(NarrativeGenerator, "suggest")

    def test_no_scoring_method(self):
        """
        CRITICAL: NarrativeGenerator must not compute scores.
        """
        assert not hasattr(NarrativeGenerator, "compute_confidence")
        assert not hasattr(NarrativeGenerator, "score_signals")
        assert not hasattr(NarrativeGenerator, "rate")

    def test_no_resolution_method(self):
        """
        CRITICAL: NarrativeGenerator must not resolve contradictions.
        """
        assert not hasattr(NarrativeGenerator, "resolve_contradictions")
        assert not hasattr(NarrativeGenerator, "pick_best_signal")

    def test_fallback_narrative_is_descriptive_only(self):
        """Test fallback narrative contains only descriptive content."""
        generator = NarrativeGenerator(
            claude_client=Mock(),
            prompt_builder=Mock(),
            validator=Mock(),
        )

        chart = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI",
            chart_name="RSI",
            timeframe="1h",
            latest_signal=Signal(
                signal_id=uuid4(),
                chart_id=uuid4(),
                received_at=datetime.now(UTC),
                signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE,
                direction=Direction.BULLISH,
                indicators={},
                raw_payload={},
            ),
            freshness=FreshnessStatus.CURRENT,
        )
        summary = RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Technical",
            instrument_id=uuid4(),
            instrument_symbol="NIFTY50",
            charts=[chart],
            contradictions=[],
            confirmations=[],
            generated_at=datetime.now(UTC),
        )

        result = generator.generate_fallback_narrative(summary)
        content = result.sections[0].content.lower()

        # Should NOT contain prescriptive language
        assert "you should" not in content
        assert "recommend" not in content
        assert "buy" not in content
        assert "sell" not in content
        assert "overall direction" not in content
        assert "confidence" not in content

    def test_format_contradiction_summary_does_not_resolve(self):
        """Test contradiction formatting does not suggest resolution."""
        generator = NarrativeGenerator(
            claude_client=Mock(),
            prompt_builder=Mock(),
            validator=Mock(),
        )

        contradictions = [
            Contradiction(
                chart_a_id=uuid4(),
                chart_a_name="RSI",
                chart_a_direction=Direction.BULLISH,
                chart_b_id=uuid4(),
                chart_b_name="MACD",
                chart_b_direction=Direction.BEARISH,
                detected_at=datetime.now(UTC),
            )
        ]

        summary = generator._format_contradiction_summary(contradictions)
        summary_lower = summary.lower()

        # Should state contradictions exist
        assert "contradiction" in summary_lower

        # Should NOT suggest resolution
        assert "correct" not in summary_lower or "does not determine" in summary_lower
        assert "better" not in summary_lower
        assert "recommend" not in summary_lower
        assert "follow" not in summary_lower or "does not" in summary_lower


class TestEnsureCompliance:
    """Tests for the _ensure_compliance method."""

    @pytest.fixture
    def generator(self):
        """Create generator with real validator."""
        from cia_sie.ai.response_validator import AIResponseValidator
        return NarrativeGenerator(
            claude_client=Mock(),
            prompt_builder=Mock(),
            validator=AIResponseValidator(),
        )

    def test_removes_prohibited_phrases(self, generator):
        """Test removes prohibited phrases (case-sensitive replacement)."""
        # Use lowercase to match the replacement logic
        narrative = "you should buy because the signal is bullish."

        result = generator._ensure_compliance(narrative)

        # The phrase should be replaced with [DESCRIPTION ONLY]
        assert "[DESCRIPTION ONLY]" in result

    def test_adds_disclaimer_if_missing(self, generator):
        """Test adds disclaimer if missing."""
        narrative = "The RSI shows BULLISH."

        result = generator._ensure_compliance(narrative)

        assert MANDATORY_DISCLAIMER in result

    def test_preserves_compliant_narrative(self, generator):
        """Test preserves compliant narrative."""
        compliant = f"The RSI shows BULLISH. {MANDATORY_DISCLAIMER}"

        result = generator._ensure_compliance(compliant)

        assert "RSI shows BULLISH" in result
        assert MANDATORY_DISCLAIMER in result
