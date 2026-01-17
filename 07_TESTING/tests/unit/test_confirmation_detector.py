"""
Tests for CIA-SIE Confirmation Detector
=======================================

Validates confirmation detection and alignment exposure.

GOVERNED BY: Section 13.3 (Component Specifications - ConfirmationDetector)
"""

import pytest
from datetime import datetime, UTC
from uuid import uuid4

from cia_sie.core.enums import Direction, SignalType, FreshnessStatus
from cia_sie.core.models import Signal, ChartSignalStatus, Confirmation
from cia_sie.exposure.confirmation_detector import ConfirmationDetector


class TestConfirmationDetector:
    """Tests for ConfirmationDetector class."""

    @pytest.fixture
    def detector(self):
        """Create a ConfirmationDetector instance."""
        return ConfirmationDetector()

    @pytest.fixture
    def bullish_signal(self):
        """Create a bullish signal."""
        return Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )

    @pytest.fixture
    def bearish_signal(self):
        """Create a bearish signal."""
        return Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BEARISH,
            indicators={},
            raw_payload={},
        )

    @pytest.fixture
    def neutral_signal(self):
        """Create a neutral signal."""
        return Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=datetime.now(UTC),
            signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.NEUTRAL,
            indicators={},
            raw_payload={},
        )

    def make_chart_status(
        self, chart_name: str, signal: Signal
    ) -> ChartSignalStatus:
        """Helper to create ChartSignalStatus."""
        return ChartSignalStatus(
            chart_id=uuid4(),
            chart_code=chart_name.lower().replace(" ", "_"),
            chart_name=chart_name,
            timeframe="1h",
            latest_signal=signal,
            freshness=FreshnessStatus.CURRENT,
        )

    def test_detects_bullish_confirmation(
        self, detector, bullish_signal
    ):
        """Test detecting BULLISH confirmation."""
        # Create two separate bullish signals
        bullish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bullish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI", bullish1),
            self.make_chart_status("MACD", bullish2),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 1
        assert confirmations[0].aligned_direction == Direction.BULLISH

    def test_detects_bearish_confirmation(self, detector):
        """Test detecting BEARISH confirmation."""
        bearish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BEARISH,
            indicators={}, raw_payload={},
        )
        bearish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BEARISH,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI", bearish1),
            self.make_chart_status("MACD", bearish2),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 1
        assert confirmations[0].aligned_direction == Direction.BEARISH

    def test_no_confirmation_opposite_directions(
        self, detector, bullish_signal, bearish_signal
    ):
        """Test no confirmation when signals have opposite directions."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
            self.make_chart_status("MACD", bearish_signal),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 0

    def test_neutral_does_not_create_confirmation(
        self, detector, bullish_signal, neutral_signal
    ):
        """Test that NEUTRAL signals don't create confirmations."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
            self.make_chart_status("MACD", neutral_signal),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 0

    def test_two_neutral_no_confirmation(self, detector):
        """Test that two NEUTRAL signals don't create a confirmation."""
        neutral1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.NEUTRAL,
            indicators={}, raw_payload={},
        )
        neutral2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.NEUTRAL,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI", neutral1),
            self.make_chart_status("MACD", neutral2),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 0

    def test_multiple_confirmations(self, detector):
        """Test detecting multiple confirmations."""
        # Create 3 bullish signals
        signals = []
        for i in range(3):
            s = Signal(
                signal_id=uuid4(), chart_id=uuid4(),
                received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
                indicators={}, raw_payload={},
            )
            signals.append(s)

        chart_statuses = [
            self.make_chart_status(f"Chart_{i}", signals[i])
            for i in range(3)
        ]

        confirmations = detector.detect(chart_statuses)

        # 3 choose 2 = 3 confirmations
        assert len(confirmations) == 3

    def test_mixed_directions_correct_count(self, detector):
        """Test correct confirmation count with mixed directions."""
        # 2 bullish + 2 bearish
        bullish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bullish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bearish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BEARISH,
            indicators={}, raw_payload={},
        )
        bearish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BEARISH,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("Bullish_1", bullish1),
            self.make_chart_status("Bullish_2", bullish2),
            self.make_chart_status("Bearish_1", bearish1),
            self.make_chart_status("Bearish_2", bearish2),
        ]

        confirmations = detector.detect(chart_statuses)

        # 2 bullish pairs + 2 bearish pairs = 2 total confirmations
        # Actually: 2 choose 2 bullish = 1 + 2 choose 2 bearish = 1 = 2
        assert len(confirmations) == 2

    def test_empty_chart_list(self, detector):
        """Test with empty chart list."""
        confirmations = detector.detect([])
        assert len(confirmations) == 0

    def test_single_chart_no_confirmation(self, detector, bullish_signal):
        """Test single chart cannot have confirmations."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 0

    def test_charts_without_signals_ignored(self, detector):
        """Test charts without signals are ignored."""
        chart_status = ChartSignalStatus(
            chart_id=uuid4(),
            chart_code="empty",
            chart_name="Empty Chart",
            timeframe="1h",
            latest_signal=None,  # No signal
            freshness=FreshnessStatus.UNAVAILABLE,
        )

        confirmations = detector.detect([chart_status])

        assert len(confirmations) == 0

    def test_count_confirmations(self, detector):
        """Test counting confirmations without full objects."""
        bullish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bullish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI", bullish1),
            self.make_chart_status("MACD", bullish2),
        ]

        count = detector.count_confirmations(chart_statuses)

        assert count == 1

    def test_is_confirmation_method(self, detector):
        """Test _is_confirmation helper method."""
        # Same direction (non-NEUTRAL) is confirmation
        assert detector._is_confirmation(Direction.BULLISH, Direction.BULLISH)
        assert detector._is_confirmation(Direction.BEARISH, Direction.BEARISH)

        # Different directions are not confirmations
        assert not detector._is_confirmation(Direction.BULLISH, Direction.BEARISH)
        assert not detector._is_confirmation(Direction.BEARISH, Direction.BULLISH)

        # NEUTRAL is never confirmation (even with itself)
        assert not detector._is_confirmation(Direction.NEUTRAL, Direction.NEUTRAL)
        assert not detector._is_confirmation(Direction.NEUTRAL, Direction.BULLISH)
        assert not detector._is_confirmation(Direction.BULLISH, Direction.NEUTRAL)

    def test_group_by_direction(self, detector):
        """Test grouping charts by direction."""
        bullish = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bearish = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BEARISH,
            indicators={}, raw_payload={},
        )
        neutral = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.NEUTRAL,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI", bullish),
            self.make_chart_status("MACD", bearish),
            self.make_chart_status("Trend", neutral),
        ]

        groups = detector.group_by_direction(chart_statuses)

        assert len(groups[Direction.BULLISH]) == 1
        assert len(groups[Direction.BEARISH]) == 1
        assert len(groups[Direction.NEUTRAL]) == 1

    def test_detect_from_signals(self, detector):
        """Test detection using the alternate detect_from_signals method."""
        bullish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bullish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )

        signals = [
            (uuid4(), "RSI", bullish1),
            (uuid4(), "MACD", bullish2),
        ]

        confirmations = detector.detect_from_signals(signals)

        assert len(confirmations) == 1
        assert confirmations[0].aligned_direction == Direction.BULLISH

    def test_confirmation_includes_chart_names(self, detector):
        """Test that confirmation objects include chart names."""
        bullish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bullish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI (14)", bullish1),
            self.make_chart_status("MACD Signal", bullish2),
        ]

        confirmations = detector.detect(chart_statuses)

        assert len(confirmations) == 1
        assert confirmations[0].chart_a_name == "RSI (14)"
        assert confirmations[0].chart_b_name == "MACD Signal"

    def test_confirmation_has_detected_at_timestamp(self, detector):
        """Test that confirmations have detection timestamp."""
        bullish1 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )
        bullish2 = Signal(
            signal_id=uuid4(), chart_id=uuid4(),
            received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
            signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
            indicators={}, raw_payload={},
        )

        chart_statuses = [
            self.make_chart_status("RSI", bullish1),
            self.make_chart_status("MACD", bullish2),
        ]

        confirmations = detector.detect(chart_statuses)

        assert confirmations[0].detected_at is not None
        assert isinstance(confirmations[0].detected_at, datetime)


class TestConfirmationDetectorConstitutionalCompliance:
    """
    Tests verifying ConfirmationDetector maintains constitutional compliance.

    CRITICAL: Per Gold Standard Specification, these constraints are absolute.
    """

    def test_no_weight_method(self):
        """
        CRITICAL: ConfirmationDetector must not weight confirmations.
        """
        assert not hasattr(ConfirmationDetector, "weight")
        assert not hasattr(ConfirmationDetector, "weight_confirmation")
        assert not hasattr(ConfirmationDetector, "compute_weight")

    def test_no_score_method(self):
        """
        CRITICAL: ConfirmationDetector must not score confidence.
        """
        assert not hasattr(ConfirmationDetector, "score")
        assert not hasattr(ConfirmationDetector, "compute_confidence")
        assert not hasattr(ConfirmationDetector, "rate_strength")

    def test_no_aggregation_method(self):
        """
        CRITICAL: ConfirmationDetector must not aggregate.
        """
        assert not hasattr(ConfirmationDetector, "aggregate")
        assert not hasattr(ConfirmationDetector, "compute_overall")
        assert not hasattr(ConfirmationDetector, "get_net_direction")

    def test_no_ranking_method(self):
        """
        CRITICAL: ConfirmationDetector must not rank or prioritize.
        """
        assert not hasattr(ConfirmationDetector, "rank")
        assert not hasattr(ConfirmationDetector, "prioritize")
        assert not hasattr(ConfirmationDetector, "sort_by_strength")

    def test_no_suggestion_method(self):
        """
        CRITICAL: ConfirmationDetector must not suggest confirmations are "better".
        """
        assert not hasattr(ConfirmationDetector, "suggest")
        assert not hasattr(ConfirmationDetector, "recommend")
        assert not hasattr(ConfirmationDetector, "advise")

    def test_returns_all_confirmations(self):
        """
        CRITICAL: All confirmations must be returned (none hidden).
        """
        detector = ConfirmationDetector()

        # Create maximum confirmations scenario
        signals = []
        for i in range(4):
            bullish = Signal(
                signal_id=uuid4(), chart_id=uuid4(),
                received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
                indicators={}, raw_payload={},
            )
            signals.append((uuid4(), f"Bullish_{i}", bullish))

        confirmations = detector.detect_from_signals(signals)

        # 4 choose 2 = 6 confirmations
        assert len(confirmations) == 6


class TestConfirmationModel:
    """Tests for the Confirmation model used by the detector."""

    def test_confirmation_has_no_weight_field(self):
        """Test Confirmation model has no weight field."""
        assert "weight" not in Confirmation.model_fields
        assert "strength" not in Confirmation.model_fields

    def test_confirmation_has_no_confidence_field(self):
        """Test Confirmation model has no confidence field."""
        assert "confidence" not in Confirmation.model_fields
        assert "score" not in Confirmation.model_fields

    def test_confirmation_has_no_priority_field(self):
        """Test Confirmation model has no priority field."""
        assert "priority" not in Confirmation.model_fields
        assert "rank" not in Confirmation.model_fields
