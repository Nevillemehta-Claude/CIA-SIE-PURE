"""
Tests for CIA-SIE Domain Models
===============================

Validates that domain models conform to Gold Standard Specification.

GOVERNED BY: Section 0A-0D of Gold Standard Specification
"""

import pytest
from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import ValidationError

from cia_sie.core.models import (
    CIASIEBaseModel,
    Instrument,
    Silo,
    Chart,
    Signal,
    AnalyticalBasket,
    Contradiction,
    Confirmation,
    ChartSignalStatus,
    RelationshipSummary,
    NarrativeSection,
    Narrative,
    InstrumentCreate,
    SiloCreate,
    ChartCreate,
    WebhookPayload,
    BasketCreate,
)
from cia_sie.core.enums import (
    SignalType,
    Direction,
    FreshnessStatus,
    BasketType,
    NarrativeSectionType,
)


# =============================================================================
# BASE MODEL TESTS
# =============================================================================

class TestCIASIEBaseModel:
    """Tests for base model configuration."""

    def test_base_model_config(self):
        """Test base model has correct configuration."""
        config = CIASIEBaseModel.model_config
        assert config.get("from_attributes") is True
        assert config.get("use_enum_values") is True
        assert config.get("validate_assignment") is True


# =============================================================================
# INSTRUMENT MODEL TESTS
# =============================================================================

class TestInstrumentModel:
    """Tests for Instrument entity."""

    def test_create_instrument(self):
        """Test basic instrument creation."""
        instrument = Instrument(
            symbol="TEST_INST",
            display_name="Test Instrument",
        )
        assert instrument.symbol == "TEST_INST"
        assert instrument.display_name == "Test Instrument"
        assert instrument.is_active is True
        assert isinstance(instrument.instrument_id, UUID)

    def test_instrument_requires_symbol(self):
        """Test that symbol is required."""
        with pytest.raises(ValidationError):
            Instrument(symbol="", display_name="Test")

    def test_instrument_requires_display_name(self):
        """Test that display_name is required."""
        with pytest.raises(ValidationError):
            Instrument(symbol="TEST", display_name="")

    def test_instrument_auto_generates_id(self):
        """Test that instrument_id is auto-generated."""
        inst1 = Instrument(symbol="A", display_name="A")
        inst2 = Instrument(symbol="B", display_name="B")
        assert inst1.instrument_id != inst2.instrument_id

    def test_instrument_default_active(self):
        """Test that new instruments are active by default."""
        instrument = Instrument(symbol="TEST", display_name="Test")
        assert instrument.is_active is True

    def test_instrument_accepts_metadata(self):
        """Test that metadata is optional."""
        instrument = Instrument(
            symbol="TEST",
            display_name="Test",
            metadata={"exchange": "NSE"}
        )
        assert instrument.metadata == {"exchange": "NSE"}

    def test_instrument_symbol_max_length(self):
        """Test symbol max length constraint."""
        with pytest.raises(ValidationError):
            Instrument(symbol="A" * 51, display_name="Test")

    def test_instrument_display_name_max_length(self):
        """Test display_name max length constraint."""
        with pytest.raises(ValidationError):
            Instrument(symbol="TEST", display_name="A" * 101)


# =============================================================================
# SILO MODEL TESTS
# =============================================================================

class TestSiloModel:
    """Tests for Silo entity."""

    def test_create_silo(self):
        """Test basic silo creation."""
        instrument_id = uuid4()
        silo = Silo(
            instrument_id=instrument_id,
            silo_name="Technical Analysis",
        )
        assert silo.silo_name == "Technical Analysis"
        assert silo.instrument_id == instrument_id
        assert silo.is_active is True

    def test_silo_default_freshness_thresholds(self):
        """Test default freshness thresholds per SDD v4.0."""
        silo = Silo(
            instrument_id=uuid4(),
            silo_name="Test"
        )
        assert silo.current_threshold_min == 2
        assert silo.recent_threshold_min == 10
        assert silo.stale_threshold_min == 30

    def test_silo_heartbeat_defaults(self):
        """Test heartbeat is enabled by default."""
        silo = Silo(
            instrument_id=uuid4(),
            silo_name="Test"
        )
        assert silo.heartbeat_enabled is True
        assert silo.heartbeat_frequency_min == 5

    def test_silo_heartbeat_frequency_min_constraint(self):
        """Test heartbeat frequency must be >= 1."""
        with pytest.raises(ValidationError):
            Silo(
                instrument_id=uuid4(),
                silo_name="Test",
                heartbeat_frequency_min=0
            )

    def test_silo_threshold_min_constraint(self):
        """Test thresholds must be >= 1."""
        with pytest.raises(ValidationError):
            Silo(
                instrument_id=uuid4(),
                silo_name="Test",
                current_threshold_min=0
            )


# =============================================================================
# CHART MODEL TESTS
# =============================================================================

class TestChartModel:
    """Tests for Chart entity."""

    def test_create_chart(self):
        """Test basic chart creation."""
        chart = Chart(
            silo_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
            webhook_id="webhook_rsi_14",
        )
        assert chart.chart_code == "RSI_14"
        assert chart.chart_name == "RSI (14)"
        assert chart.timeframe == "1h"
        assert chart.is_active is True

    def test_chart_has_no_weight_attribute(self):
        """
        CRITICAL TEST: Charts must NOT have weight attribute.

        Per ADR-003: Weights enable aggregation which is PROHIBITED.
        """
        chart = Chart(
            silo_id=uuid4(),
            chart_code="01A",
            chart_name="Daily Momentum",
            timeframe="D",
            webhook_id="SAMPLE_01A",
        )

        # Verify no weight attribute exists
        assert not hasattr(chart, "weight")
        assert "weight" not in Chart.model_fields

    def test_chart_valid_timeframes(self):
        """Test all valid timeframes per specification."""
        valid_timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "D", "W", "M"]
        for tf in valid_timeframes:
            chart = Chart(
                silo_id=uuid4(),
                chart_code="TEST",
                chart_name="Test",
                timeframe=tf,
                webhook_id=f"webhook_{tf}",
            )
            assert chart.timeframe == tf

    def test_chart_invalid_timeframe(self):
        """Test invalid timeframe is rejected."""
        with pytest.raises(ValidationError):
            Chart(
                silo_id=uuid4(),
                chart_code="TEST",
                chart_name="Test",
                timeframe="2h",  # Invalid
                webhook_id="webhook_test",
            )

    def test_chart_webhook_id_required(self):
        """Test webhook_id is required."""
        with pytest.raises(ValidationError):
            Chart(
                silo_id=uuid4(),
                chart_code="TEST",
                chart_name="Test",
                timeframe="1h",
                webhook_id="",  # Empty
            )


# =============================================================================
# SIGNAL MODEL TESTS
# =============================================================================

class TestSignalModel:
    """Tests for Signal entity."""

    def test_create_signal(self):
        """Test basic signal creation."""
        signal = Signal(
            chart_id=uuid4(),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
        )
        assert signal.direction == Direction.BULLISH
        assert signal.signal_type == SignalType.STATE_CHANGE

    def test_signal_has_no_confidence_attribute(self):
        """
        CRITICAL TEST: Signals must NOT have confidence/strength scores.

        Per ADR-003: Scores imply system judgment which is PROHIBITED.
        """
        signal = Signal(
            chart_id=uuid4(),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
        )

        # Verify no confidence attribute exists
        assert not hasattr(signal, "confidence")
        assert not hasattr(signal, "strength")
        assert not hasattr(signal, "score")
        assert "confidence" not in Signal.model_fields
        assert "strength" not in Signal.model_fields
        assert "score" not in Signal.model_fields

    def test_signal_preserves_direction(self):
        """Test that signal direction is preserved exactly."""
        for direction in Direction:
            signal = Signal(
                chart_id=uuid4(),
                signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE,
                direction=direction,
            )
            assert signal.direction == direction

    def test_signal_all_types(self):
        """Test all signal types are valid."""
        for signal_type in SignalType:
            signal = Signal(
                chart_id=uuid4(),
                signal_timestamp=datetime.now(UTC),
                signal_type=signal_type,
                direction=Direction.NEUTRAL,
            )
            assert signal.signal_type == signal_type

    def test_signal_with_indicators(self):
        """Test signal can include indicator data."""
        indicators = {"rsi": 72.5, "macd": 0.5}
        signal = Signal(
            chart_id=uuid4(),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators=indicators,
        )
        assert signal.indicators == indicators

    def test_signal_raw_payload_preserved(self):
        """Test raw payload is preserved for audit trail."""
        raw = {"source": "TradingView", "alert_name": "RSI Cross"}
        signal = Signal(
            chart_id=uuid4(),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            raw_payload=raw,
        )
        assert signal.raw_payload == raw


# =============================================================================
# CONTRADICTION MODEL TESTS
# =============================================================================

class TestContradictionModel:
    """Tests for Contradiction entity."""

    def test_create_contradiction(self):
        """Test basic contradiction creation."""
        contradiction = Contradiction(
            chart_a_id=uuid4(),
            chart_a_name="Chart A",
            chart_a_direction=Direction.BULLISH,
            chart_b_id=uuid4(),
            chart_b_name="Chart B",
            chart_b_direction=Direction.BEARISH,
        )
        assert contradiction.chart_a_direction == Direction.BULLISH
        assert contradiction.chart_b_direction == Direction.BEARISH

    def test_contradiction_exposes_both_directions(self):
        """
        CRITICAL TEST: Contradictions must expose BOTH directions.

        Per Section 0B.5 P-03: System must NOT resolve contradictions.
        """
        contradiction = Contradiction(
            chart_a_id=uuid4(),
            chart_a_name="Chart A",
            chart_a_direction=Direction.BULLISH,
            chart_b_id=uuid4(),
            chart_b_name="Chart B",
            chart_b_direction=Direction.BEARISH,
        )

        # Both directions must be preserved
        assert contradiction.chart_a_direction == Direction.BULLISH
        assert contradiction.chart_b_direction == Direction.BEARISH

        # No resolution field
        assert not hasattr(contradiction, "resolution")
        assert not hasattr(contradiction, "recommended")
        assert not hasattr(contradiction, "winner")

    def test_contradiction_no_priority_field(self):
        """
        CRITICAL: Contradictions must not have priority/weight fields.
        """
        assert "priority" not in Contradiction.model_fields
        assert "weight" not in Contradiction.model_fields
        assert "importance" not in Contradiction.model_fields


# =============================================================================
# CONFIRMATION MODEL TESTS
# =============================================================================

class TestConfirmationModel:
    """Tests for Confirmation entity."""

    def test_create_confirmation(self):
        """Test basic confirmation creation."""
        confirmation = Confirmation(
            chart_a_id=uuid4(),
            chart_a_name="Chart A",
            chart_b_id=uuid4(),
            chart_b_name="Chart B",
            aligned_direction=Direction.BULLISH,
        )
        assert confirmation.aligned_direction == Direction.BULLISH

    def test_confirmation_no_weighting(self):
        """
        CRITICAL: Confirmations must not have weighting fields.
        """
        assert "weight" not in Confirmation.model_fields
        assert "strength" not in Confirmation.model_fields
        assert "confidence" not in Confirmation.model_fields


# =============================================================================
# ANALYTICAL BASKET MODEL TESTS
# =============================================================================

class TestAnalyticalBasketModel:
    """Tests for AnalyticalBasket entity."""

    def test_create_basket(self):
        """Test basic basket creation."""
        basket = AnalyticalBasket(
            basket_name="My Basket",
            basket_type=BasketType.CUSTOM,
        )
        assert basket.basket_name == "My Basket"
        assert basket.basket_type == BasketType.CUSTOM

    def test_basket_is_ui_only_construct(self):
        """
        CRITICAL TEST: Baskets must be UI-layer constructs only.

        Per ADR-002: Baskets must not affect processing.
        """
        basket = AnalyticalBasket(
            basket_name="My Basket",
            basket_type=BasketType.CUSTOM,
        )

        # No processing-related attributes
        assert not hasattr(basket, "aggregated_score")
        assert not hasattr(basket, "weight")
        assert not hasattr(basket, "priority")
        assert "aggregated_score" not in AnalyticalBasket.model_fields
        assert "weight" not in AnalyticalBasket.model_fields
        assert "priority" not in AnalyticalBasket.model_fields

    def test_basket_all_types(self):
        """Test all basket types are valid."""
        for basket_type in BasketType:
            basket = AnalyticalBasket(
                basket_name="Test",
                basket_type=basket_type,
            )
            assert basket.basket_type == basket_type

    def test_basket_can_hold_multiple_charts(self):
        """Test basket can contain multiple chart IDs."""
        chart_ids = [uuid4(), uuid4(), uuid4()]
        basket = AnalyticalBasket(
            basket_name="Multi-Chart",
            basket_type=BasketType.LOGICAL,
            chart_ids=chart_ids,
        )
        assert len(basket.chart_ids) == 3


# =============================================================================
# CHART SIGNAL STATUS TESTS
# =============================================================================

class TestChartSignalStatusModel:
    """Tests for ChartSignalStatus model."""

    def test_create_chart_signal_status(self):
        """Test basic chart signal status creation."""
        status = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
        )
        assert status.chart_code == "RSI_14"
        assert status.freshness == FreshnessStatus.UNAVAILABLE

    def test_chart_signal_status_with_signal(self):
        """Test chart signal status with latest signal."""
        signal = Signal(
            chart_id=uuid4(),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
        )
        status = ChartSignalStatus(
            chart_id=signal.chart_id,
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
            latest_signal=signal,
            freshness=FreshnessStatus.CURRENT,
        )
        assert status.latest_signal is not None
        assert status.freshness == FreshnessStatus.CURRENT


# =============================================================================
# RELATIONSHIP SUMMARY TESTS
# =============================================================================

class TestRelationshipSummaryModel:
    """Tests for RelationshipSummary model."""

    def test_create_relationship_summary(self):
        """Test basic relationship summary creation."""
        summary = RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Technical",
            instrument_id=uuid4(),
            instrument_symbol="NIFTY50",
        )
        assert summary.silo_name == "Technical"
        assert summary.charts == []
        assert summary.contradictions == []
        assert summary.confirmations == []

    def test_relationship_summary_no_aggregation(self):
        """
        CRITICAL: RelationshipSummary must not have aggregation fields.
        """
        assert "aggregated_direction" not in RelationshipSummary.model_fields
        assert "net_direction" not in RelationshipSummary.model_fields
        assert "overall_score" not in RelationshipSummary.model_fields
        assert "recommendation" not in RelationshipSummary.model_fields


# =============================================================================
# NARRATIVE MODEL TESTS
# =============================================================================

class TestNarrativeModel:
    """Tests for Narrative models."""

    def test_create_narrative_section(self):
        """Test basic narrative section creation."""
        section = NarrativeSection(
            section_type=NarrativeSectionType.SIGNAL_SUMMARY,
            content="RSI shows bullish momentum.",
        )
        assert section.section_type == NarrativeSectionType.SIGNAL_SUMMARY
        assert "bullish" in section.content.lower()

    def test_create_narrative(self):
        """Test basic narrative creation."""
        narrative = Narrative(
            silo_id=uuid4(),
        )
        assert narrative.sections == []
        assert "interpretation" in narrative.closing_statement.lower()

    def test_narrative_default_closing_statement(self):
        """
        CRITICAL: Narrative must have closing statement about user authority.
        """
        narrative = Narrative(silo_id=uuid4())
        assert "entirely yours" in narrative.closing_statement.lower()
        assert "interpretation" in narrative.closing_statement.lower() or \
               "decision" in narrative.closing_statement.lower()

    def test_narrative_no_recommendation_section(self):
        """
        CRITICAL: No recommendation section type in narratives.
        """
        # This is tested in enums, but double-check here
        section_types = [s.value for s in NarrativeSectionType]
        assert "RECOMMENDATION" not in section_types
        assert "ACTION" not in section_types


# =============================================================================
# API REQUEST/RESPONSE MODEL TESTS
# =============================================================================

class TestInstrumentCreateModel:
    """Tests for InstrumentCreate model."""

    def test_create_instrument_request(self):
        """Test instrument create request validation."""
        req = InstrumentCreate(
            symbol="NIFTY50",
            display_name="Nifty 50 Index",
        )
        assert req.symbol == "NIFTY50"

    def test_instrument_create_requires_symbol(self):
        """Test symbol is required."""
        with pytest.raises(ValidationError):
            InstrumentCreate(symbol="", display_name="Test")


class TestSiloCreateModel:
    """Tests for SiloCreate model."""

    def test_create_silo_request(self):
        """Test silo create request validation."""
        req = SiloCreate(
            instrument_id=uuid4(),
            silo_name="Technical Analysis",
        )
        assert req.silo_name == "Technical Analysis"
        assert req.heartbeat_enabled is True


class TestChartCreateModel:
    """Tests for ChartCreate model."""

    def test_create_chart_request(self):
        """Test chart create request validation."""
        req = ChartCreate(
            silo_id=uuid4(),
            chart_code="RSI_14",
            chart_name="RSI (14)",
            timeframe="1h",
            webhook_id="webhook_rsi_14",
        )
        assert req.timeframe == "1h"

    def test_chart_create_no_weight(self):
        """
        CRITICAL: ChartCreate must not have weight field.
        """
        assert "weight" not in ChartCreate.model_fields


class TestWebhookPayloadModel:
    """Tests for WebhookPayload model."""

    def test_create_webhook_payload(self):
        """Test webhook payload validation."""
        payload = WebhookPayload(
            webhook_id="webhook_rsi_14",
            timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
        )
        assert payload.direction == Direction.BULLISH

    def test_webhook_payload_with_indicators(self):
        """Test webhook payload accepts indicators."""
        payload = WebhookPayload(
            webhook_id="webhook_rsi_14",
            timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BEARISH,
            indicators={"rsi": 25.5},
        )
        assert payload.indicators["rsi"] == 25.5


class TestBasketCreateModel:
    """Tests for BasketCreate model."""

    def test_create_basket_request(self):
        """Test basket create request validation."""
        req = BasketCreate(
            basket_name="My Basket",
            basket_type=BasketType.CUSTOM,
        )
        assert req.basket_name == "My Basket"

    def test_basket_create_no_processing_fields(self):
        """
        CRITICAL: BasketCreate must not have processing fields.
        """
        assert "weight" not in BasketCreate.model_fields
        assert "priority" not in BasketCreate.model_fields
        assert "aggregated_score" not in BasketCreate.model_fields


# =============================================================================
# FRESHNESS STATUS TESTS
# =============================================================================

class TestFreshnessStatus:
    """Tests for FreshnessStatus enum usage in models."""

    def test_all_freshness_values_exist(self):
        """Test all required freshness values per SDD v4.0."""
        assert FreshnessStatus.CURRENT
        assert FreshnessStatus.RECENT
        assert FreshnessStatus.STALE
        assert FreshnessStatus.UNAVAILABLE

    def test_freshness_is_descriptive_only(self):
        """
        CRITICAL: Freshness must not invalidate data.
        """
        freshness_names = [f.name for f in FreshnessStatus]
        assert "INVALID" not in freshness_names
        assert "REJECTED" not in freshness_names
        assert "EXPIRED" not in freshness_names
