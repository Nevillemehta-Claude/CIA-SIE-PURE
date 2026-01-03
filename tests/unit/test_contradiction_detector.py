"""
Tests for CIA-SIE Contradiction Detector
========================================

Validates contradiction detection and exposure.

GOVERNED BY: Section 13.2 (Component Specifications - ContradictionDetector)
"""

import pytest
from datetime import datetime, UTC
from uuid import uuid4

from cia_sie.core.enums import Direction, SignalType, FreshnessStatus
from cia_sie.core.models import Signal, ChartSignalStatus, Contradiction
from cia_sie.exposure.contradiction_detector import ContradictionDetector


class TestContradictionDetector:
    """Tests for ContradictionDetector class."""

    @pytest.fixture
    def detector(self):
        """Create a ContradictionDetector instance."""
        return ContradictionDetector()

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

    def test_detects_bullish_vs_bearish_contradiction(
        self, detector, bullish_signal, bearish_signal
    ):
        """Test detecting BULLISH vs BEARISH contradiction."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
            self.make_chart_status("MACD", bearish_signal),
        ]

        contradictions = detector.detect(chart_statuses)

        assert len(contradictions) == 1
        assert contradictions[0].chart_a_direction == Direction.BULLISH
        assert contradictions[0].chart_b_direction == Direction.BEARISH

    def test_no_contradiction_same_direction(
        self, detector, bullish_signal
    ):
        """Test no contradiction when all signals same direction."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
            self.make_chart_status("MACD", bullish_signal),
        ]

        contradictions = detector.detect(chart_statuses)

        assert len(contradictions) == 0

    def test_neutral_does_not_create_contradiction(
        self, detector, bullish_signal, neutral_signal
    ):
        """Test that NEUTRAL signals don't create contradictions."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
            self.make_chart_status("MACD", neutral_signal),
        ]

        contradictions = detector.detect(chart_statuses)

        assert len(contradictions) == 0

    def test_multiple_contradictions(
        self, detector, bullish_signal, bearish_signal
    ):
        """Test detecting multiple contradictions."""
        # Create signals with unique IDs
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

        chart_statuses = [
            self.make_chart_status("RSI", bullish1),
            self.make_chart_status("MACD", bullish2),
            self.make_chart_status("Trend", bearish1),
        ]

        contradictions = detector.detect(chart_statuses)

        # 2 bullish vs 1 bearish = 2 contradictions
        assert len(contradictions) == 2

    def test_empty_chart_list(self, detector):
        """Test with empty chart list."""
        contradictions = detector.detect([])
        assert len(contradictions) == 0

    def test_single_chart_no_contradiction(self, detector, bullish_signal):
        """Test single chart cannot have contradictions."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
        ]

        contradictions = detector.detect(chart_statuses)

        assert len(contradictions) == 0

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

        contradictions = detector.detect([chart_status])

        assert len(contradictions) == 0

    def test_count_contradictions(self, detector, bullish_signal, bearish_signal):
        """Test counting contradictions without full objects."""
        chart_statuses = [
            self.make_chart_status("RSI", bullish_signal),
            self.make_chart_status("MACD", bearish_signal),
        ]

        count = detector.count_contradictions(chart_statuses)

        assert count == 1

    def test_is_contradiction_method(self, detector):
        """Test _is_contradiction helper method."""
        # BULLISH vs BEARISH is contradiction
        assert detector._is_contradiction(Direction.BULLISH, Direction.BEARISH)
        assert detector._is_contradiction(Direction.BEARISH, Direction.BULLISH)

        # Same direction is not
        assert not detector._is_contradiction(Direction.BULLISH, Direction.BULLISH)
        assert not detector._is_contradiction(Direction.BEARISH, Direction.BEARISH)

        # NEUTRAL is never contradiction
        assert not detector._is_contradiction(Direction.NEUTRAL, Direction.BULLISH)
        assert not detector._is_contradiction(Direction.NEUTRAL, Direction.BEARISH)
        assert not detector._is_contradiction(Direction.BULLISH, Direction.NEUTRAL)


class TestContradictionDetectorConstitutionalCompliance:
    """
    Tests verifying ContradictionDetector maintains constitutional compliance.

    CRITICAL: Per Section 0B.5 P-03, contradiction resolution is PROHIBITED.
    """

    def test_no_resolution_method(self):
        """
        CRITICAL: ContradictionDetector must not resolve contradictions.
        """
        assert not hasattr(ContradictionDetector, "resolve")
        assert not hasattr(ContradictionDetector, "resolve_contradiction")
        assert not hasattr(ContradictionDetector, "pick_winner")

    def test_no_prioritization_method(self):
        """
        CRITICAL: ContradictionDetector must not prioritize signals.
        """
        assert not hasattr(ContradictionDetector, "prioritize")
        assert not hasattr(ContradictionDetector, "rank")
        assert not hasattr(ContradictionDetector, "weight")

    def test_no_hiding_method(self):
        """
        CRITICAL: ContradictionDetector must not hide contradictions.
        """
        assert not hasattr(ContradictionDetector, "filter_out")
        assert not hasattr(ContradictionDetector, "hide")
        assert not hasattr(ContradictionDetector, "suppress")

    def test_returns_all_contradictions(self):
        """
        CRITICAL: All contradictions must be returned (none hidden).
        """
        detector = ContradictionDetector()

        # Create maximum contradictions scenario
        signals = []
        for i in range(3):
            bullish = Signal(
                signal_id=uuid4(), chart_id=uuid4(),
                received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE, direction=Direction.BULLISH,
                indicators={}, raw_payload={},
            )
            signals.append((uuid4(), f"Bullish_{i}", bullish))

        for i in range(2):
            bearish = Signal(
                signal_id=uuid4(), chart_id=uuid4(),
                received_at=datetime.now(UTC), signal_timestamp=datetime.now(UTC),
                signal_type=SignalType.STATE_CHANGE, direction=Direction.BEARISH,
                indicators={}, raw_payload={},
            )
            signals.append((uuid4(), f"Bearish_{i}", bearish))

        contradictions = detector.detect_from_signals(signals)

        # 3 bullish x 2 bearish = 6 contradictions
        assert len(contradictions) == 6
