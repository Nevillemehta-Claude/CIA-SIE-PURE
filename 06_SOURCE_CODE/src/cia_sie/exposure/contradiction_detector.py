"""
CIA-SIE Contradiction Detector
==============================

Identifies when chart signals conflict for EXPOSURE, not resolution.

GOVERNED BY: Section 13.2 (Component Specifications - ContradictionDetector)

DOES:
- Identify BULLISH vs BEARISH conflicts
- Return list of all contradictions found

DOES NOT:
- Resolve contradictions
- Suggest which is "right"
- Weight or prioritize signals
- Hide any contradiction
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from cia_sie.core.enums import Direction
from cia_sie.core.models import (
    ChartSignalStatus,
    Contradiction,
    Signal,
)


class ContradictionDetector:
    """
    Detects contradictions between chart signals.

    Per Gold Standard Specification Section 13.2:
    The detector identifies when chart signals conflict.
    It does NOT resolve contradictions - only EXPOSES them.

    PROHIBITED ACTIONS (per Section 0B.5 P-03):
    - Resolving which signal is "correct"
    - Suggesting which to prioritize
    - Hiding any contradiction
    """

    def detect(
        self,
        chart_statuses: Sequence[ChartSignalStatus],
    ) -> list[Contradiction]:
        """
        Detect all contradictions among chart signals.

        A contradiction exists when one chart shows BULLISH and another
        shows BEARISH for the same instrument/silo context.

        Args:
            chart_statuses: List of charts with their latest signals

        Returns:
            List of all detected contradictions

        NOTE: This method detects but does NOT resolve.
        ALL contradictions are returned - none are hidden.
        """
        contradictions: list[Contradiction] = []
        detected_at = datetime.now(UTC)

        # Get charts with non-neutral signals
        charts_with_signals = [
            cs
            for cs in chart_statuses
            if cs.latest_signal is not None and cs.latest_signal.direction != Direction.NEUTRAL
        ]

        # Compare all pairs
        for i, chart_a in enumerate(charts_with_signals):
            for chart_b in charts_with_signals[i + 1 :]:
                assert chart_a.latest_signal is not None
                assert chart_b.latest_signal is not None

                if self._is_contradiction(
                    chart_a.latest_signal.direction,
                    chart_b.latest_signal.direction,
                ):
                    contradiction = Contradiction(
                        chart_a_id=chart_a.chart_id,
                        chart_a_name=chart_a.chart_name,
                        chart_a_direction=chart_a.latest_signal.direction,
                        chart_b_id=chart_b.chart_id,
                        chart_b_name=chart_b.chart_name,
                        chart_b_direction=chart_b.latest_signal.direction,
                        detected_at=detected_at,
                    )
                    contradictions.append(contradiction)

        return contradictions

    def detect_from_signals(
        self,
        signals: list[tuple[UUID, str, Signal]],
    ) -> list[Contradiction]:
        """
        Detect contradictions from a list of (chart_id, chart_name, signal) tuples.

        Args:
            signals: List of tuples containing chart info and signal

        Returns:
            List of all detected contradictions
        """
        contradictions: list[Contradiction] = []
        detected_at = datetime.now(UTC)

        # Filter to non-neutral signals
        non_neutral = [
            (chart_id, chart_name, signal)
            for chart_id, chart_name, signal in signals
            if signal.direction != Direction.NEUTRAL
        ]

        # Compare all pairs
        for i, (chart_a_id, chart_a_name, signal_a) in enumerate(non_neutral):
            for chart_b_id, chart_b_name, signal_b in non_neutral[i + 1 :]:
                if self._is_contradiction(signal_a.direction, signal_b.direction):
                    contradiction = Contradiction(
                        chart_a_id=chart_a_id,
                        chart_a_name=chart_a_name,
                        chart_a_direction=signal_a.direction,
                        chart_b_id=chart_b_id,
                        chart_b_name=chart_b_name,
                        chart_b_direction=signal_b.direction,
                        detected_at=detected_at,
                    )
                    contradictions.append(contradiction)

        return contradictions

    def _is_contradiction(
        self,
        direction_a: Direction,
        direction_b: Direction,
    ) -> bool:
        """
        Determine if two directions constitute a contradiction.

        A contradiction exists when:
        - One is BULLISH and the other is BEARISH
        - (or vice versa)

        NEUTRAL does not create contradictions.
        """
        return (direction_a == Direction.BULLISH and direction_b == Direction.BEARISH) or (
            direction_a == Direction.BEARISH and direction_b == Direction.BULLISH
        )

    def count_contradictions(
        self,
        chart_statuses: Sequence[ChartSignalStatus],
    ) -> int:
        """
        Count total contradictions without building full objects.

        Useful for summary displays.
        """
        return len(self.detect(chart_statuses))
