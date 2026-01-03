"""
Constitutional Compliance Tests for CIA-SIE
============================================

CRITICAL: These tests verify the system adheres to the Gold Standard
Specification Section 0B prohibitions.

The CIA-SIE system is governed by a strict constitutional framework:
- NO weights on any entity
- NO confidence scores or signal scoring
- NO aggregation of signals
- NO recommendations or prescriptive output
- NO resolving contradictions (expose only)

Failure of ANY test in this file is a CONSTITUTIONAL VIOLATION.
"""

import pytest
import inspect
from datetime import datetime, UTC
from uuid import uuid4

# Import all models and key classes
from cia_sie.core.models import (
    Instrument,
    Silo,
    Chart,
    Signal,
    ChartSignalStatus,
    RelationshipSummary,
    Contradiction,
    Confirmation,
    Narrative,
    NarrativeSection,
    AnalyticalBasket,
)
from cia_sie.core.enums import Direction, SignalType, FreshnessStatus, BasketType


# =============================================================================
# SECTION 1: NO WEIGHTS ANYWHERE
# =============================================================================

class TestNoWeightsAnywhere:
    """
    CRITICAL: No entity in the system may have a weight attribute.

    Per Gold Standard Specification Section 0B:
    "Charts MUST NOT have weights. All charts have equal standing."
    """

    def test_instrument_has_no_weight(self):
        """Instrument must have no weight attribute."""
        inst = Instrument(
            instrument_id=uuid4(),
            symbol="TEST",
            display_name="Test",
        )
        assert not hasattr(inst, 'weight'), "CONSTITUTIONAL VIOLATION: Instrument has weight"
        assert 'weight' not in inst.model_fields, "CONSTITUTIONAL VIOLATION: weight in model fields"

    def test_silo_has_no_weight(self):
        """Silo must have no weight attribute."""
        silo = Silo(
            silo_id=uuid4(),
            instrument_id=uuid4(),
            silo_name="Test",
        )
        assert not hasattr(silo, 'weight'), "CONSTITUTIONAL VIOLATION: Silo has weight"
        assert 'weight' not in silo.model_fields, "CONSTITUTIONAL VIOLATION: weight in model fields"

    def test_chart_has_no_weight(self):
        """Chart must have no weight attribute."""
        chart = Chart(
            chart_id=uuid4(),
            silo_id=uuid4(),
            chart_code="TEST",
            chart_name="Test",
            timeframe="1h",
            webhook_id="test_webhook",
        )
        assert not hasattr(chart, 'weight'), "CONSTITUTIONAL VIOLATION: Chart has weight"
        assert 'weight' not in chart.model_fields, "CONSTITUTIONAL VIOLATION: weight in model fields"
        assert not hasattr(chart, 'priority'), "CONSTITUTIONAL VIOLATION: Chart has priority"
        assert not hasattr(chart, 'importance'), "CONSTITUTIONAL VIOLATION: Chart has importance"

    def test_signal_has_no_weight(self):
        """Signal must have no weight attribute."""
        signal = Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )
        assert not hasattr(signal, 'weight'), "CONSTITUTIONAL VIOLATION: Signal has weight"
        assert 'weight' not in signal.model_fields, "CONSTITUTIONAL VIOLATION: weight in model fields"

    def test_basket_has_no_weight(self):
        """Basket must have no weight attribute (UI-only construct)."""
        basket = AnalyticalBasket(
            basket_id=uuid4(),
            basket_name="Test",
            basket_type=BasketType.CUSTOM,
        )
        assert not hasattr(basket, 'weight'), "CONSTITUTIONAL VIOLATION: Basket has weight"
        assert 'weight' not in basket.model_fields, "CONSTITUTIONAL VIOLATION: weight in model fields"


# =============================================================================
# SECTION 2: NO CONFIDENCE SCORES ANYWHERE
# =============================================================================

class TestNoConfidenceScores:
    """
    CRITICAL: No entity may have confidence scores.

    Per Gold Standard Specification Section 0B:
    "Signals MUST NOT have confidence levels."
    """

    def test_signal_has_no_confidence(self):
        """Signal must have no confidence attribute."""
        signal = Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )
        assert not hasattr(signal, 'confidence'), "CONSTITUTIONAL VIOLATION: Signal has confidence"
        assert not hasattr(signal, 'score'), "CONSTITUTIONAL VIOLATION: Signal has score"
        assert not hasattr(signal, 'strength'), "CONSTITUTIONAL VIOLATION: Signal has strength"
        assert 'confidence' not in signal.model_fields
        assert 'score' not in signal.model_fields
        assert 'strength' not in signal.model_fields

    def test_chart_status_has_no_confidence(self):
        """ChartSignalStatus must have no confidence attribute."""
        status = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="TEST",
            chart_name="Test",
            timeframe="1h",
            latest_signal=None,
            freshness=FreshnessStatus.CURRENT,
        )
        assert not hasattr(status, 'confidence'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(status, 'score'), "CONSTITUTIONAL VIOLATION"
        assert 'confidence' not in status.model_fields
        assert 'score' not in status.model_fields

    def test_contradiction_has_no_confidence(self):
        """Contradiction must have no confidence about which signal is correct."""
        contradiction = Contradiction(
            chart_a_id=uuid4(),
            chart_a_name="Chart A",
            chart_a_direction=Direction.BULLISH,
            chart_b_id=uuid4(),
            chart_b_name="Chart B",
            chart_b_direction=Direction.BEARISH,
            detected_at=datetime.now(UTC),
        )
        assert not hasattr(contradiction, 'confidence'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(contradiction, 'correct_signal'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(contradiction, 'preferred'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(contradiction, 'resolution'), "CONSTITUTIONAL VIOLATION"


# =============================================================================
# SECTION 3: NO AGGREGATION ANYWHERE
# =============================================================================

class TestNoAggregation:
    """
    CRITICAL: The system must NEVER aggregate signals.

    Per Gold Standard Specification Section 0B:
    "The system MUST NOT compute an 'overall direction' from multiple signals."
    """

    def test_relationship_summary_has_no_aggregation(self):
        """RelationshipSummary must not aggregate to overall direction."""
        summary = RelationshipSummary(
            silo_id=uuid4(),
            silo_name="Test",
            instrument_id=uuid4(),
            instrument_symbol="TEST",
            charts=[],
            contradictions=[],
            confirmations=[],
            generated_at=datetime.now(UTC),
        )
        assert not hasattr(summary, 'overall_direction'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(summary, 'net_signal'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(summary, 'aggregated_score'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(summary, 'summary_direction'), "CONSTITUTIONAL VIOLATION"
        assert 'overall_direction' not in summary.model_fields
        assert 'net_signal' not in summary.model_fields

    def test_no_aggregate_method_in_models(self):
        """No model should have aggregation methods."""
        models_to_check = [
            Instrument, Silo, Chart, Signal, ChartSignalStatus,
            RelationshipSummary, Narrative, AnalyticalBasket,
        ]

        prohibited_methods = [
            'aggregate', 'compute_overall', 'get_net_signal',
            'calculate_summary', 'summarize_direction',
        ]

        for model in models_to_check:
            for method_name in prohibited_methods:
                assert not hasattr(model, method_name), \
                    f"CONSTITUTIONAL VIOLATION: {model.__name__} has {method_name}"


# =============================================================================
# SECTION 4: NO RECOMMENDATIONS
# =============================================================================

class TestNoRecommendations:
    """
    CRITICAL: The system must NEVER make recommendations.

    Per Gold Standard Specification Section 0B:
    "All output is DESCRIPTIVE, never PRESCRIPTIVE."
    """

    def test_narrative_has_no_recommendation(self):
        """Narrative must not contain recommendations."""
        narrative = Narrative(
            narrative_id=uuid4(),
            silo_id=uuid4(),
            sections=[],
            closing_statement="The interpretation and decision is yours.",
            generated_at=datetime.now(UTC),
        )
        assert not hasattr(narrative, 'recommendation'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(narrative, 'advice'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(narrative, 'suggested_action'), "CONSTITUTIONAL VIOLATION"
        assert 'recommendation' not in narrative.model_fields
        assert 'advice' not in narrative.model_fields

    def test_no_recommend_methods_anywhere(self):
        """No class should have recommendation methods."""
        # Check key service classes
        from cia_sie.ai.narrative_generator import NarrativeGenerator
        from cia_sie.ai.claude_client import ClaudeClient
        from cia_sie.ai.prompt_builder import NarrativePromptBuilder

        classes_to_check = [
            NarrativeGenerator, ClaudeClient, NarrativePromptBuilder,
        ]

        prohibited_methods = [
            'recommend', 'advise', 'suggest', 'get_recommendation',
            'should_buy', 'should_sell',
        ]

        for cls in classes_to_check:
            for method_name in prohibited_methods:
                assert not hasattr(cls, method_name), \
                    f"CONSTITUTIONAL VIOLATION: {cls.__name__} has {method_name}"


# =============================================================================
# SECTION 5: CONTRADICTIONS ARE EXPOSED, NOT RESOLVED
# =============================================================================

class TestContradictionsExposed:
    """
    CRITICAL: Contradictions must be EXPOSED, never RESOLVED.

    Per Gold Standard Specification Section 0B:
    "The system MUST NOT decide which signal is 'correct'."
    """

    def test_contradiction_has_no_resolution(self):
        """Contradiction must not have resolution field."""
        contradiction = Contradiction(
            chart_a_id=uuid4(),
            chart_a_name="Chart A",
            chart_a_direction=Direction.BULLISH,
            chart_b_id=uuid4(),
            chart_b_name="Chart B",
            chart_b_direction=Direction.BEARISH,
            detected_at=datetime.now(UTC),
        )
        assert not hasattr(contradiction, 'resolution'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(contradiction, 'winner'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(contradiction, 'correct'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(contradiction, 'preferred_signal'), "CONSTITUTIONAL VIOLATION"

    def test_confirmation_has_no_extra_weight(self):
        """Confirmation must not imply confirmations are 'better'."""
        confirmation = Confirmation(
            chart_a_id=uuid4(),
            chart_a_name="Chart A",
            chart_b_id=uuid4(),
            chart_b_name="Chart B",
            aligned_direction=Direction.BULLISH,
            detected_at=datetime.now(UTC),
        )
        assert not hasattr(confirmation, 'strength'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(confirmation, 'confidence'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(confirmation, 'weight'), "CONSTITUTIONAL VIOLATION"
        assert not hasattr(confirmation, 'reliability'), "CONSTITUTIONAL VIOLATION"


# =============================================================================
# SECTION 6: BASKET PURITY (UI-ONLY)
# =============================================================================

class TestBasketPurity:
    """
    CRITICAL: Baskets are UI-layer constructs ONLY.

    Per ADR-002:
    "Baskets have ZERO impact on signal processing."
    """

    def test_basket_has_no_processing_fields(self):
        """Basket must have no fields that affect processing."""
        basket = AnalyticalBasket(
            basket_id=uuid4(),
            basket_name="Test",
            basket_type=BasketType.CUSTOM,
        )

        # These fields would imply processing impact
        prohibited_fields = [
            'weight', 'priority', 'score', 'aggregated_signal',
            'net_direction', 'confidence', 'processing_enabled',
        ]

        for field in prohibited_fields:
            assert not hasattr(basket, field), \
                f"CONSTITUTIONAL VIOLATION: Basket has {field}"
            assert field not in basket.model_fields, \
                f"CONSTITUTIONAL VIOLATION: {field} in Basket model fields"


# =============================================================================
# SECTION 7: FRESHNESS IS DESCRIPTIVE ONLY
# =============================================================================

class TestFreshnessDescriptiveOnly:
    """
    CRITICAL: Freshness is purely DESCRIPTIVE.

    Per Gold Standard Specification Section 7.3:
    "Freshness does NOT invalidate or suppress data."
    """

    def test_freshness_status_has_no_weight(self):
        """Freshness status values must not have weights."""
        for status in FreshnessStatus:
            # Freshness should be a simple string enum
            assert isinstance(status.value, str), \
                f"CONSTITUTIONAL VIOLATION: FreshnessStatus.{status.name} is not a string"

    def test_freshness_calculator_no_exclusion(self):
        """FreshnessCalculator must not exclude stale data."""
        from cia_sie.ingestion.freshness import FreshnessCalculator

        calc = FreshnessCalculator()

        # Verify no exclusion/filtering methods
        prohibited_methods = [
            'exclude', 'filter_stale', 'get_valid_only',
            'suppress', 'invalidate', 'remove_stale',
        ]

        for method in prohibited_methods:
            assert not hasattr(calc, method), \
                f"CONSTITUTIONAL VIOLATION: FreshnessCalculator has {method}"


# =============================================================================
# SECTION 8: MANDATORY CLOSING STATEMENT
# =============================================================================

class TestMandatoryClosing:
    """
    CRITICAL: All narratives must include user authority reminder.

    Per Gold Standard Specification Section 14.4:
    "Every narrative must end with: 'The interpretation and decision is yours.'"
    """

    def test_narrative_requires_closing(self):
        """Narrative must have closing_statement field."""
        assert 'closing_statement' in Narrative.model_fields, \
            "CONSTITUTIONAL VIOLATION: Narrative missing closing_statement"

    def test_response_validator_requires_disclaimer(self):
        """AIResponseValidator must check for mandatory disclaimer."""
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER

        assert MANDATORY_DISCLAIMER is not None
        assert "interpretation" in MANDATORY_DISCLAIMER.lower()
        assert "decision" in MANDATORY_DISCLAIMER.lower()
        assert "yours" in MANDATORY_DISCLAIMER.lower()


# =============================================================================
# SECTION 9: DIRECTION ENUM PURITY
# =============================================================================

class TestDirectionEnumPurity:
    """
    CRITICAL: Direction enum must be pure descriptive.

    Directions describe signal state only, never imply action.
    """

    def test_direction_values_are_descriptive(self):
        """Direction values must be descriptive, not prescriptive."""
        # Check only descriptive values exist
        valid_values = {'BULLISH', 'BEARISH', 'NEUTRAL'}
        actual_values = {d.value for d in Direction}

        assert actual_values == valid_values, \
            f"CONSTITUTIONAL VIOLATION: Direction has unexpected values: {actual_values - valid_values}"

    def test_direction_has_no_action_methods(self):
        """Direction enum must not have action-implying methods."""
        prohibited_methods = [
            'should_buy', 'should_sell', 'get_action',
            'to_trade', 'get_position',
        ]

        for method in prohibited_methods:
            assert not hasattr(Direction, method), \
                f"CONSTITUTIONAL VIOLATION: Direction has {method}"


# =============================================================================
# SECTION 10: COMPREHENSIVE MODEL FIELD AUDIT
# =============================================================================

class TestComprehensiveFieldAudit:
    """
    Audit all model fields for constitutional violations.
    """

    PROHIBITED_FIELD_NAMES = {
        'weight', 'score', 'confidence', 'priority', 'importance',
        'strength', 'reliability', 'accuracy', 'certainty',
        'recommendation', 'advice', 'suggestion', 'action',
        'overall_direction', 'net_signal', 'aggregated',
        'preferred', 'winner', 'correct', 'resolution',
    }

    def test_instrument_fields(self):
        """Audit Instrument model fields."""
        self._audit_model(Instrument)

    def test_silo_fields(self):
        """Audit Silo model fields."""
        self._audit_model(Silo)

    def test_chart_fields(self):
        """Audit Chart model fields."""
        self._audit_model(Chart)

    def test_signal_fields(self):
        """Audit Signal model fields."""
        self._audit_model(Signal)

    def test_chart_status_fields(self):
        """Audit ChartSignalStatus model fields."""
        self._audit_model(ChartSignalStatus)

    def test_relationship_summary_fields(self):
        """Audit RelationshipSummary model fields."""
        self._audit_model(RelationshipSummary)

    def test_narrative_fields(self):
        """Audit Narrative model fields."""
        self._audit_model(Narrative)

    def test_basket_fields(self):
        """Audit AnalyticalBasket model fields."""
        self._audit_model(AnalyticalBasket)

    def test_contradiction_fields(self):
        """Audit Contradiction model fields."""
        self._audit_model(Contradiction)

    def test_confirmation_fields(self):
        """Audit Confirmation model fields."""
        self._audit_model(Confirmation)

    def _audit_model(self, model_class):
        """Audit a model class for prohibited fields."""
        field_names = set(model_class.model_fields.keys())
        violations = field_names & self.PROHIBITED_FIELD_NAMES

        assert not violations, \
            f"CONSTITUTIONAL VIOLATION: {model_class.__name__} has prohibited fields: {violations}"
