"""
Tests for CIA-SIE Exposure Layer
================================

Validates contradiction and confirmation detection.
"""

import pytest
from datetime import datetime, UTC
from uuid import UUID, uuid4

from cia_sie.core.enums import Direction, FreshnessStatus
from cia_sie.core.models import Signal, ChartSignalStatus
from cia_sie.exposure.contradiction_detector import ContradictionDetector
from cia_sie.exposure.confirmation_detector import ConfirmationDetector


@pytest.fixture
def contradiction_detector():
    return ContradictionDetector()


@pytest.fixture
def confirmation_detector():
    return ConfirmationDetector()


def make_chart_status(
    chart_id: str,
    chart_name: str,
    direction: Direction,
) -> ChartSignalStatus:
    """Helper to create ChartSignalStatus for testing."""
    signal = Signal(
        signal_id=uuid4(),
        chart_id=UUID(chart_id),
        received_at=datetime.now(UTC),
        signal_timestamp=datetime.now(UTC),
        signal_type="STATE_CHANGE",
        direction=direction,
    )
    return ChartSignalStatus(
        chart_id=UUID(chart_id),
        chart_code="TEST",
        chart_name=chart_name,
        timeframe="D",
        latest_signal=signal,
        freshness=FreshnessStatus.CURRENT,
    )


class TestContradictionDetector:
    """Tests for ContradictionDetector."""

    def test_detects_bullish_bearish_contradiction(self, contradiction_detector):
        """Test detection of BULLISH vs BEARISH contradiction."""
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "Chart A", Direction.BULLISH),
            make_chart_status("22222222-2222-2222-2222-222222222222", "Chart B", Direction.BEARISH),
        ]

        contradictions = contradiction_detector.detect(charts)

        assert len(contradictions) == 1
        assert contradictions[0].chart_a_direction == Direction.BULLISH
        assert contradictions[0].chart_b_direction == Direction.BEARISH

    def test_neutral_does_not_contradict(self, contradiction_detector):
        """Test that NEUTRAL signals don't create contradictions."""
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "Chart A", Direction.BULLISH),
            make_chart_status("22222222-2222-2222-2222-222222222222", "Chart B", Direction.NEUTRAL),
        ]

        contradictions = contradiction_detector.detect(charts)

        assert len(contradictions) == 0

    def test_same_direction_no_contradiction(self, contradiction_detector):
        """Test that same directions don't create contradictions."""
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "Chart A", Direction.BULLISH),
            make_chart_status("22222222-2222-2222-2222-222222222222", "Chart B", Direction.BULLISH),
        ]

        contradictions = contradiction_detector.detect(charts)

        assert len(contradictions) == 0

    def test_detector_does_not_resolve(self, contradiction_detector):
        """
        CRITICAL TEST: Detector must NOT resolve contradictions.

        Per Section 0B.5 P-03: No resolution of contradictions.
        """
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "Chart A", Direction.BULLISH),
            make_chart_status("22222222-2222-2222-2222-222222222222", "Chart B", Direction.BEARISH),
        ]

        contradictions = contradiction_detector.detect(charts)

        # Contradiction should not have resolution info
        for c in contradictions:
            assert not hasattr(c, "resolution")
            assert not hasattr(c, "winner")
            assert not hasattr(c, "recommendation")


class TestConfirmationDetector:
    """Tests for ConfirmationDetector."""

    def test_detects_aligned_bullish(self, confirmation_detector):
        """Test detection of aligned BULLISH signals."""
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "Chart A", Direction.BULLISH),
            make_chart_status("22222222-2222-2222-2222-222222222222", "Chart B", Direction.BULLISH),
        ]

        confirmations = confirmation_detector.detect(charts)

        assert len(confirmations) == 1
        assert confirmations[0].aligned_direction == Direction.BULLISH

    def test_neutral_not_confirmation(self, confirmation_detector):
        """Test that NEUTRAL doesn't create confirmations."""
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "Chart A", Direction.NEUTRAL),
            make_chart_status("22222222-2222-2222-2222-222222222222", "Chart B", Direction.NEUTRAL),
        ]

        confirmations = confirmation_detector.detect(charts)

        assert len(confirmations) == 0

    def test_confirmations_not_weighted(self, confirmation_detector):
        """
        CRITICAL TEST: Confirmations must NOT be weighted.

        More confirmations does NOT mean "stronger signal".
        That would be aggregation (prohibited).
        """
        charts = [
            make_chart_status("11111111-1111-1111-1111-111111111111", "A", Direction.BULLISH),
            make_chart_status("22222222-2222-2222-2222-222222222222", "B", Direction.BULLISH),
            make_chart_status("33333333-3333-3333-3333-333333333333", "C", Direction.BULLISH),
        ]

        confirmations = confirmation_detector.detect(charts)

        # Should detect pairs but NOT aggregate them
        assert len(confirmations) == 3  # A-B, A-C, B-C

        for c in confirmations:
            assert not hasattr(c, "weight")
            assert not hasattr(c, "strength")
            assert not hasattr(c, "score")
