"""
Tests for CIA-SIE Narrative Prompt Builder
==========================================

Validates prompt construction for AI narrative generation.

GOVERNED BY: Section 14.5 (AI Prompt Template)
"""

import pytest
from datetime import datetime, UTC
from uuid import uuid4

from cia_sie.core.enums import Direction, SignalType, FreshnessStatus
from cia_sie.core.models import (
    Signal,
    ChartSignalStatus,
    RelationshipSummary,
    Contradiction,
    Confirmation,
)
from cia_sie.ai.prompt_builder import (
    NarrativePromptBuilder,
    NARRATIVE_SYSTEM_PROMPT,
)


class TestNarrativeSystemPrompt:
    """Tests for the system prompt constant."""

    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        assert NARRATIVE_SYSTEM_PROMPT is not None
        assert len(NARRATIVE_SYSTEM_PROMPT) > 0

    def test_system_prompt_prohibits_recommendations(self):
        """Test system prompt prohibits recommendation language."""
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "you should" in prompt_lower or "never use" in prompt_lower
        assert "i recommend" in prompt_lower or "never" in prompt_lower

    def test_system_prompt_requires_descriptive_language(self):
        """Test system prompt requires descriptive output."""
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "describe" in prompt_lower
        assert "prescribe" in prompt_lower or "prescriptive" in prompt_lower

    def test_system_prompt_mentions_user_authority(self):
        """Test system prompt mentions user authority."""
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "user" in prompt_lower
        assert "decision" in prompt_lower

    def test_system_prompt_prohibits_aggregation(self):
        """Test system prompt prohibits aggregation."""
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "overall direction" in prompt_lower
        assert "never compute" in prompt_lower or "do not" in prompt_lower

    def test_system_prompt_prohibits_confidence_scores(self):
        """Test system prompt prohibits confidence scores."""
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "confidence" in prompt_lower
        assert "score" in prompt_lower or "level" in prompt_lower


class TestNarrativePromptBuilder:
    """Tests for NarrativePromptBuilder class."""

    @pytest.fixture
    def builder(self):
        """Create a NarrativePromptBuilder instance."""
        return NarrativePromptBuilder()

    @pytest.fixture
    def sample_signal(self):
        """Create a sample signal."""
        return Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={"rsi": 72.5, "macd": 0.5},
            raw_payload={},
        )

    @pytest.fixture
    def sample_chart_status(self, sample_signal):
        """Create a sample chart status."""
        return ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
            latest_signal=sample_signal,
            freshness=FreshnessStatus.CURRENT,
        )

    @pytest.fixture
    def sample_summary(self, sample_chart_status):
        """Create a sample relationship summary."""
        return RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Technical",
            instrument_id=uuid4(),
            instrument_symbol="NIFTY50",
            charts=[sample_chart_status],
            contradictions=[],
            confirmations=[],
            generated_at=datetime(2025, 1, 1, 12, 0, 0),
        )

    def test_builder_has_system_prompt(self, builder):
        """Test builder has system prompt attribute."""
        assert builder.system_prompt == NARRATIVE_SYSTEM_PROMPT

    def test_build_silo_narrative_prompt_includes_instrument(self, builder, sample_summary):
        """Test silo prompt includes instrument symbol."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "NIFTY50" in prompt

    def test_build_silo_narrative_prompt_includes_silo_name(self, builder, sample_summary):
        """Test silo prompt includes silo name."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "Technical" in prompt

    def test_build_silo_narrative_prompt_includes_charts(self, builder, sample_summary):
        """Test silo prompt includes chart information."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "RSI (14)" in prompt
        assert "RSI_14" in prompt
        assert "1h" in prompt

    def test_build_silo_narrative_prompt_includes_signal_direction(self, builder, sample_summary):
        """Test silo prompt includes signal direction."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "BULLISH" in prompt

    def test_build_silo_narrative_prompt_includes_indicators(self, builder, sample_summary):
        """Test silo prompt includes indicator values."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "rsi" in prompt
        assert "72.5" in prompt
        assert "macd" in prompt

    def test_build_silo_narrative_prompt_includes_freshness(self, builder, sample_summary):
        """Test silo prompt includes freshness status."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "CURRENT" in prompt

    def test_build_silo_narrative_prompt_includes_instructions(self, builder, sample_summary):
        """Test silo prompt includes instructions."""
        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "INSTRUCTIONS" in prompt
        assert "DO NOT" in prompt

    def test_build_silo_narrative_prompt_with_contradictions(self, builder, sample_summary):
        """Test silo prompt includes contradictions section."""
        sample_summary.contradictions = [
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

        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "CONTRADICTIONS DETECTED" in prompt
        assert "RSI" in prompt
        assert "MACD" in prompt
        assert "BULLISH" in prompt
        assert "BEARISH" in prompt

    def test_build_silo_narrative_prompt_with_confirmations(self, builder, sample_summary):
        """Test silo prompt includes confirmations section."""
        sample_summary.confirmations = [
            Confirmation(
                chart_a_id=uuid4(),
                chart_a_name="RSI",
                chart_b_id=uuid4(),
                chart_b_name="MACD",
                aligned_direction=Direction.BULLISH,
                detected_at=datetime.now(UTC),
            )
        ]

        prompt = builder.build_silo_narrative_prompt(sample_summary)

        assert "CONFIRMATIONS DETECTED" in prompt


class TestBuildChartNarrativePrompt:
    """Tests for chart narrative prompt building."""

    @pytest.fixture
    def builder(self):
        """Create a NarrativePromptBuilder instance."""
        return NarrativePromptBuilder()

    @pytest.fixture
    def chart_status_with_signal(self):
        """Create chart status with signal."""
        signal = Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BEARISH,
            indicators={"rsi": 25},
            raw_payload={},
        )
        return ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="4h",
            latest_signal=signal,
            freshness=FreshnessStatus.RECENT,
        )

    @pytest.fixture
    def chart_status_no_signal(self):
        """Create chart status without signal."""
        return ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="MACD",
            chart_name="MACD",
            timeframe="1d",
            latest_signal=None,
            freshness=FreshnessStatus.UNAVAILABLE,
        )

    def test_build_chart_prompt_includes_instrument(self, builder, chart_status_with_signal):
        """Test chart prompt includes instrument symbol."""
        prompt = builder.build_chart_narrative_prompt(
            chart_status_with_signal, "BANKNIFTY"
        )

        assert "BANKNIFTY" in prompt

    def test_build_chart_prompt_includes_chart_info(self, builder, chart_status_with_signal):
        """Test chart prompt includes chart information."""
        prompt = builder.build_chart_narrative_prompt(
            chart_status_with_signal, "NIFTY50"
        )

        assert "RSI (14)" in prompt
        assert "RSI_14" in prompt
        assert "4h" in prompt

    def test_build_chart_prompt_includes_signal_direction(self, builder, chart_status_with_signal):
        """Test chart prompt includes signal direction."""
        prompt = builder.build_chart_narrative_prompt(
            chart_status_with_signal, "NIFTY50"
        )

        assert "BEARISH" in prompt

    def test_build_chart_prompt_includes_indicators(self, builder, chart_status_with_signal):
        """Test chart prompt includes indicators."""
        prompt = builder.build_chart_narrative_prompt(
            chart_status_with_signal, "NIFTY50"
        )

        assert "rsi" in prompt
        assert "25" in prompt

    def test_build_chart_prompt_without_signal(self, builder, chart_status_no_signal):
        """Test chart prompt handles missing signal."""
        prompt = builder.build_chart_narrative_prompt(
            chart_status_no_signal, "NIFTY50"
        )

        assert "NO SIGNAL DATA AVAILABLE" in prompt

    def test_build_chart_prompt_includes_interpretation_reminder(self, builder, chart_status_with_signal):
        """Test chart prompt includes interpretation reminder."""
        prompt = builder.build_chart_narrative_prompt(
            chart_status_with_signal, "NIFTY50"
        )

        assert "interpretation" in prompt.lower()
        assert "decision" in prompt.lower()
        assert "yours" in prompt.lower()


class TestBuildContradictionNarrativePrompt:
    """Tests for contradiction narrative prompt building."""

    @pytest.fixture
    def builder(self):
        """Create a NarrativePromptBuilder instance."""
        return NarrativePromptBuilder()

    @pytest.fixture
    def sample_contradictions(self):
        """Create sample contradictions."""
        return [
            Contradiction(
                chart_a_id=uuid4(),
                chart_a_name="RSI",
                chart_a_direction=Direction.BULLISH,
                chart_b_id=uuid4(),
                chart_b_name="MACD",
                chart_b_direction=Direction.BEARISH,
                detected_at=datetime.now(UTC),
            ),
            Contradiction(
                chart_a_id=uuid4(),
                chart_a_name="Trend",
                chart_a_direction=Direction.BULLISH,
                chart_b_id=uuid4(),
                chart_b_name="Volume",
                chart_b_direction=Direction.BEARISH,
                detected_at=datetime.now(UTC),
            ),
        ]

    def test_build_contradiction_prompt_includes_instrument(self, builder, sample_contradictions):
        """Test contradiction prompt includes instrument."""
        prompt = builder.build_contradiction_narrative_prompt(
            sample_contradictions, "NIFTY50"
        )

        assert "NIFTY50" in prompt

    def test_build_contradiction_prompt_includes_all_contradictions(self, builder, sample_contradictions):
        """Test contradiction prompt includes all contradictions."""
        prompt = builder.build_contradiction_narrative_prompt(
            sample_contradictions, "NIFTY50"
        )

        assert "RSI" in prompt
        assert "MACD" in prompt
        assert "Trend" in prompt
        assert "Volume" in prompt

    def test_build_contradiction_prompt_includes_directions(self, builder, sample_contradictions):
        """Test contradiction prompt includes directions."""
        prompt = builder.build_contradiction_narrative_prompt(
            sample_contradictions, "NIFTY50"
        )

        assert "BULLISH" in prompt
        assert "BEARISH" in prompt

    def test_build_contradiction_prompt_prohibits_resolution(self, builder, sample_contradictions):
        """Test contradiction prompt prohibits resolution."""
        prompt = builder.build_contradiction_narrative_prompt(
            sample_contradictions, "NIFTY50"
        )

        prompt_lower = prompt.lower()
        assert "do not" in prompt_lower
        assert "correct" in prompt_lower or "follow" in prompt_lower

    def test_build_contradiction_prompt_ends_with_authority_reminder(self, builder, sample_contradictions):
        """Test contradiction prompt ends with authority reminder."""
        prompt = builder.build_contradiction_narrative_prompt(
            sample_contradictions, "NIFTY50"
        )

        prompt_lower = prompt.lower()
        assert "interpretation" in prompt_lower
        assert "decision" in prompt_lower
        assert "yours" in prompt_lower


class TestNarrativePromptBuilderConstitutionalCompliance:
    """
    Tests verifying prompt builder maintains constitutional compliance.

    CRITICAL: Prompts must ensure Claude generates DESCRIPTIVE output only.
    """

    def test_system_prompt_never_mentions_buy_sell(self):
        """
        Ensure system prompt doesn't mention buy/sell as actions.
        """
        # System prompt should only mention buy/sell as prohibited words
        lines = NARRATIVE_SYSTEM_PROMPT.split("\n")
        for line in lines:
            if "buy" in line.lower() or "sell" in line.lower():
                # If buy/sell appears, it should be in a prohibition context
                assert "never" in line.lower() or "not" in line.lower() or "consider" in line.lower()

    def test_system_prompt_emphasizes_equal_weight(self):
        """
        Ensure system prompt emphasizes equal weight for all signals.
        """
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "equal weight" in prompt_lower

    def test_system_prompt_prohibits_signal_ranking(self):
        """
        Ensure system prompt prohibits signal ranking.
        """
        prompt_lower = NARRATIVE_SYSTEM_PROMPT.lower()
        assert "rank" in prompt_lower or "better" in prompt_lower

    def test_no_aggregation_method(self):
        """
        CRITICAL: NarrativePromptBuilder must not aggregate.
        """
        assert not hasattr(NarrativePromptBuilder, "build_aggregate_prompt")
        assert not hasattr(NarrativePromptBuilder, "build_overall_direction_prompt")

    def test_no_recommendation_method(self):
        """
        CRITICAL: NarrativePromptBuilder must not generate recommendation prompts.
        """
        assert not hasattr(NarrativePromptBuilder, "build_recommendation_prompt")
        assert not hasattr(NarrativePromptBuilder, "build_advice_prompt")

    def test_no_scoring_method(self):
        """
        CRITICAL: NarrativePromptBuilder must not build scoring prompts.
        """
        assert not hasattr(NarrativePromptBuilder, "build_confidence_prompt")
        assert not hasattr(NarrativePromptBuilder, "build_score_prompt")
