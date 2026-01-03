"""
CIA-SIE Confirmation Detector
=============================

Identifies when chart signals align.

GOVERNED BY: Section 13.3 (Component Specifications)

DOES:
- Identify when charts show aligned directions
- Return list of all confirmations found

DOES NOT:
- Weight confirmations
- Score confidence
- Aggregate into a single view
- Suggest confirmations are "better" than contradictions
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from cia_sie.core.enums import Direction
from cia_sie.core.models import (
    ChartSignalStatus,
    Confirmation,
    Signal,
)


class ConfirmationDetector:
    """
    Detects confirmations (aligned signals) between charts.

    Per Gold Standard Specification:
    The detector identifies when chart signals align.
    It does NOT weight or prioritize confirmations.

    CRITICAL: Confirmations are informational only.
    More confirmations does NOT mean "stronger signal".
    That would be aggregation (prohibited).
    """

    def detect(
        self,
        chart_statuses: Sequence[ChartSignalStatus],
    ) -> list[Confirmation]:
        """
        Detect all confirmations among chart signals.

        A confirmation exists when two charts show the same
        directional bias (both BULLISH or both BEARISH).

        Args:
            chart_statuses: List of charts with their latest signals

        Returns:
            List of all detected confirmations

        NOTE: This is purely informational.
        We do NOT imply that confirmations make a signal "stronger".
        """
        confirmations: list[Confirmation] = []
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

                if self._is_confirmation(
                    chart_a.latest_signal.direction,
                    chart_b.latest_signal.direction,
                ):
                    confirmation = Confirmation(
                        chart_a_id=chart_a.chart_id,
                        chart_a_name=chart_a.chart_name,
                        chart_b_id=chart_b.chart_id,
                        chart_b_name=chart_b.chart_name,
                        aligned_direction=chart_a.latest_signal.direction,
                        detected_at=detected_at,
                    )
                    confirmations.append(confirmation)

        return confirmations

    def detect_from_signals(
        self,
        signals: list[tuple[UUID, str, Signal]],
    ) -> list[Confirmation]:
        """
        Detect confirmations from a list of (chart_id, chart_name, signal) tuples.

        Args:
            signals: List of tuples containing chart info and signal

        Returns:
            List of all detected confirmations
        """
        confirmations: list[Confirmation] = []
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
                if self._is_confirmation(signal_a.direction, signal_b.direction):
                    confirmation = Confirmation(
                        chart_a_id=chart_a_id,
                        chart_a_name=chart_a_name,
                        chart_b_id=chart_b_id,
                        chart_b_name=chart_b_name,
                        aligned_direction=signal_a.direction,
                        detected_at=detected_at,
                    )
                    confirmations.append(confirmation)

        return confirmations

    def _is_confirmation(
        self,
        direction_a: Direction,
        direction_b: Direction,
    ) -> bool:
        """
        Determine if two directions constitute a confirmation.

        A confirmation exists when both directions are the same
        non-NEUTRAL value.
        """
        return direction_a == direction_b and direction_a != Direction.NEUTRAL

    def count_confirmations(
        self,
        chart_statuses: Sequence[ChartSignalStatus],
    ) -> int:
        """
        Count total confirmations without building full objects.

        Useful for summary displays.
        """
        return len(self.detect(chart_statuses))

    def group_by_direction(
        self,
        chart_statuses: Sequence[ChartSignalStatus],
    ) -> dict[Direction, list[ChartSignalStatus]]:
        """
        Group charts by their signal direction.

        This is for display purposes only - NOT for aggregation.

        Returns:
            Dict mapping Direction to list of charts with that direction
        """
        groups: dict[Direction, list[ChartSignalStatus]] = {
            Direction.BULLISH: [],
            Direction.BEARISH: [],
            Direction.NEUTRAL: [],
        }

        for cs in chart_statuses:
            if cs.latest_signal:
                groups[cs.latest_signal.direction].append(cs)

        return groups
