"""
CIA-SIE Freshness Calculator
============================

Calculates data freshness status based on signal age.

GOVERNED BY: Section 7.3 (Freshness Calculation)

CRITICAL: Freshness is purely DESCRIPTIVE.
It does NOT invalidate or suppress data.
All data is displayed regardless of freshness status.
"""

from datetime import datetime
from typing import Optional

from cia_sie.core.enums import FreshnessStatus
from cia_sie.core.models import Signal, Silo


class FreshnessCalculator:
    """
    Calculates freshness status for signals.

    Per Gold Standard Specification Section 7.3:
    - Freshness is purely descriptive
    - Does NOT invalidate or suppress data
    - All signals displayed regardless of freshness

    IMPORTANT: This is NOT a data validation mechanism.
    Stale data is still VALID data and must be displayed.
    """

    def calculate(
        self,
        signal_timestamp: datetime,
        current_threshold_min: int,
        recent_threshold_min: int,
        stale_threshold_min: int,
        as_of: Optional[datetime] = None,
    ) -> FreshnessStatus:
        """
        Calculate freshness status based on signal age.

        Args:
            signal_timestamp: When the signal was generated
            current_threshold_min: Minutes for CURRENT status
            recent_threshold_min: Minutes for RECENT status
            stale_threshold_min: Minutes for STALE status
            as_of: Reference time for calculation (defaults to now)

        Returns:
            FreshnessStatus enum value

        NOTE: We NEVER return UNAVAILABLE based on age.
        UNAVAILABLE is only for retrieval failures.
        """
        as_of = as_of or datetime.utcnow()
        age_minutes = (as_of - signal_timestamp).total_seconds() / 60

        if age_minutes <= current_threshold_min:
            return FreshnessStatus.CURRENT
        elif age_minutes <= recent_threshold_min:
            return FreshnessStatus.RECENT
        else:
            return FreshnessStatus.STALE

    def calculate_for_signal(
        self,
        signal: Signal,
        silo: Silo,
        as_of: Optional[datetime] = None,
    ) -> FreshnessStatus:
        """
        Calculate freshness for a signal using silo thresholds.

        Args:
            signal: The signal to evaluate
            silo: Silo containing threshold configuration
            as_of: Reference time (defaults to now)

        Returns:
            FreshnessStatus enum value
        """
        return self.calculate(
            signal_timestamp=signal.signal_timestamp,
            current_threshold_min=silo.current_threshold_min,
            recent_threshold_min=silo.recent_threshold_min,
            stale_threshold_min=silo.stale_threshold_min,
            as_of=as_of,
        )

    def calculate_age_description(
        self,
        signal_timestamp: datetime,
        as_of: Optional[datetime] = None,
    ) -> str:
        """
        Generate human-readable age description.

        Args:
            signal_timestamp: When the signal was generated
            as_of: Reference time (defaults to now)

        Returns:
            Human-readable string like "2 minutes ago"
        """
        as_of = as_of or datetime.utcnow()
        delta = as_of - signal_timestamp
        total_seconds = int(delta.total_seconds())

        if total_seconds < 60:
            return f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = total_seconds // 86400
            return f"{days} day{'s' if days != 1 else ''} ago"


# Default freshness thresholds (can be overridden per silo)
DEFAULT_FRESHNESS_THRESHOLDS = {
    "current_threshold_min": 2,
    "recent_threshold_min": 10,
    "stale_threshold_min": 30,
}
