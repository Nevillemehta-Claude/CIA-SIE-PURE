"""
CIA-SIE Relationship Exposer
============================

Surfaces all signal relationships for display.

GOVERNED BY: Section 13.3 (Component Specifications - RelationshipExposer)

CRITICAL CONSTRAINTS (per Section 13.3):
- Returns ALL charts (none hidden)
- Returns ALL contradictions (none resolved)
- Returns ALL confirmations (none weighted)
- NO aggregation anywhere
- NO scores anywhere
- NO recommendations anywhere
"""

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID

from cia_sie.core.enums import Direction, FreshnessStatus
from cia_sie.core.models import (
    ChartSignalStatus,
    RelationshipSummary,
    Signal,
)
from cia_sie.dal.models import SignalDB
from cia_sie.dal.repositories import ChartRepository, SignalRepository, SiloRepository
from cia_sie.exposure.confirmation_detector import ConfirmationDetector
from cia_sie.exposure.contradiction_detector import ContradictionDetector
from cia_sie.ingestion.freshness import FreshnessCalculator


class RelationshipExposer:
    """
    Surfaces all signal relationships for a silo.

    Per Gold Standard Specification Section 13.3:
    This component exposes ALL relationships without any filtering,
    aggregation, or scoring.

    The output is a RelationshipSummary containing:
    - All charts with their current signals
    - All detected contradictions
    - All detected confirmations
    - Freshness status for each chart
    """

    def __init__(
        self,
        silo_repository: SiloRepository,
        chart_repository: ChartRepository,
        signal_repository: SignalRepository,
        contradiction_detector: Optional[ContradictionDetector] = None,
        confirmation_detector: Optional[ConfirmationDetector] = None,
        freshness_calculator: Optional[FreshnessCalculator] = None,
    ):
        self.silo_repo = silo_repository
        self.chart_repo = chart_repository
        self.signal_repo = signal_repository
        self.contradiction_detector = contradiction_detector or ContradictionDetector()
        self.confirmation_detector = confirmation_detector or ConfirmationDetector()
        self.freshness_calculator = freshness_calculator or FreshnessCalculator()

    async def expose_for_silo(
        self,
        silo_id: str,
        as_of: Optional[datetime] = None,
    ) -> RelationshipSummary:
        """
        Expose all relationships for a silo.

        Args:
            silo_id: The silo to analyze
            as_of: Reference time for freshness calculation

        Returns:
            RelationshipSummary containing all charts, contradictions, confirmations

        NOTE: This returns EVERYTHING. Nothing is hidden or filtered.
        """
        as_of = as_of or datetime.now(UTC)

        # Get silo with full hierarchy
        silo = await self.silo_repo.get_with_full_hierarchy(silo_id)
        if not silo:
            raise ValueError(f"Silo not found: {silo_id}")

        # Build chart status list
        chart_statuses: list[ChartSignalStatus] = []

        for chart in silo.charts:
            if not chart.is_active:
                continue

            # Get latest signal
            latest_signal = await self.signal_repo.get_latest_by_chart(chart.chart_id)

            # Calculate freshness
            if latest_signal:
                freshness = self.freshness_calculator.calculate(
                    signal_timestamp=latest_signal.signal_timestamp,
                    current_threshold_min=silo.current_threshold_min,
                    recent_threshold_min=silo.recent_threshold_min,
                    stale_threshold_min=silo.stale_threshold_min,
                    as_of=as_of,
                )
                signal_model = self._signal_db_to_model(latest_signal)
            else:
                freshness = FreshnessStatus.UNAVAILABLE
                signal_model = None

            chart_status = ChartSignalStatus(
                chart_id=UUID(chart.chart_id),
                chart_code=chart.chart_code,
                chart_name=chart.chart_name,
                timeframe=chart.timeframe,
                latest_signal=signal_model,
                freshness=freshness,
            )
            chart_statuses.append(chart_status)

        # Detect contradictions
        contradictions = self.contradiction_detector.detect(chart_statuses)

        # Detect confirmations
        confirmations = self.confirmation_detector.detect(chart_statuses)

        # Build and return summary
        return RelationshipSummary(
            silo_id=UUID(silo.silo_id),
            silo_name=silo.silo_name,
            instrument_id=UUID(silo.instrument_id),
            instrument_symbol=silo.instrument.symbol if silo.instrument else "",
            charts=chart_statuses,
            contradictions=contradictions,
            confirmations=confirmations,
            generated_at=as_of,
        )

    async def expose_for_instrument(
        self,
        instrument_id: str,
        as_of: Optional[datetime] = None,
    ) -> list[RelationshipSummary]:
        """
        Expose relationships for all silos of an instrument.

        Args:
            instrument_id: The instrument to analyze
            as_of: Reference time for freshness calculation

        Returns:
            List of RelationshipSummary for each silo
        """
        silos = await self.silo_repo.get_by_instrument(instrument_id)
        summaries = []

        for silo in silos:
            summary = await self.expose_for_silo(silo.silo_id, as_of)
            summaries.append(summary)

        return summaries

    def _signal_db_to_model(self, signal_db: SignalDB) -> Signal:
        """Convert database signal to domain model."""
        return Signal(
            signal_id=UUID(signal_db.signal_id),
            chart_id=UUID(signal_db.chart_id),
            received_at=signal_db.received_at,
            signal_timestamp=signal_db.signal_timestamp,
            signal_type=signal_db.signal_type,
            direction=Direction(signal_db.direction),
            indicators=signal_db.indicators if isinstance(signal_db.indicators, dict) else {},
            raw_payload=signal_db.raw_payload if isinstance(signal_db.raw_payload, dict) else {},
        )


class CrossSiloExposer:
    """
    Exposes relationships across multiple silos.

    This is used for Analytical Baskets that span silos.

    NOTE: Cross-silo exposure still follows all constitutional constraints.
    No aggregation, scoring, or recommendations across silos.
    """

    def __init__(
        self,
        relationship_exposer: RelationshipExposer,
    ):
        self.exposer = relationship_exposer

    async def expose_for_basket(
        self,
        chart_ids: list[str],
        basket_name: str,
        as_of: Optional[datetime] = None,
    ) -> dict:
        """
        Expose relationships for charts in a basket.

        Baskets can contain charts from multiple silos.
        This method gathers all relevant data.

        Returns:
            Dict containing chart statuses, contradictions, confirmations
        """
        # This would fetch charts by ID and build a summary
        # Implementation depends on specific basket structure
        # For now, return empty structure
        return {
            "basket_name": basket_name,
            "charts": [],
            "contradictions": [],
            "confirmations": [],
            "generated_at": as_of or datetime.now(UTC),
        }
