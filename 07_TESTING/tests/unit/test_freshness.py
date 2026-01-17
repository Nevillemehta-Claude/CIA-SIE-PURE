"""
Tests for CIA-SIE Freshness Calculator
======================================

Validates freshness calculation and status determination.

GOVERNED BY: Section 7.3 (Freshness Calculation)
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

from cia_sie.core.enums import FreshnessStatus, SignalType, Direction
from cia_sie.core.models import Signal, Silo
from cia_sie.ingestion.freshness import (
    FreshnessCalculator,
    DEFAULT_FRESHNESS_THRESHOLDS,
)


class TestFreshnessCalculator:
    """Tests for FreshnessCalculator class."""

    @pytest.fixture
    def calculator(self):
        """Create a FreshnessCalculator instance."""
        return FreshnessCalculator()

    @pytest.fixture
    def reference_time(self):
        """Create a fixed reference time for testing."""
        return datetime(2025, 1, 1, 12, 0, 0)

    @pytest.fixture
    def sample_silo(self):
        """Create a sample silo with thresholds."""
        return Silo(
            silo_id=uuid4(),
            instrument_id=uuid4(),
            silo_name="Technical",
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
        )

    @pytest.fixture
    def sample_signal(self, reference_time):
        """Create a sample signal."""
        return Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=reference_time,
            signal_timestamp=reference_time,
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )

    def test_current_status_within_threshold(self, calculator, reference_time):
        """Test CURRENT status when signal is within current threshold."""
        signal_time = reference_time - timedelta(minutes=1)

        status = calculator.calculate(
            signal_timestamp=signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.CURRENT

    def test_current_status_at_exact_threshold(self, calculator, reference_time):
        """Test CURRENT status at exact threshold boundary."""
        signal_time = reference_time - timedelta(minutes=2)

        status = calculator.calculate(
            signal_timestamp=signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.CURRENT

    def test_recent_status_after_current_threshold(self, calculator, reference_time):
        """Test RECENT status when past current but within recent threshold."""
        signal_time = reference_time - timedelta(minutes=5)

        status = calculator.calculate(
            signal_timestamp=signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.RECENT

    def test_recent_status_at_exact_threshold(self, calculator, reference_time):
        """Test RECENT status at exact recent threshold boundary."""
        signal_time = reference_time - timedelta(minutes=10)

        status = calculator.calculate(
            signal_timestamp=signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.RECENT

    def test_stale_status_after_recent_threshold(self, calculator, reference_time):
        """Test STALE status when past recent threshold."""
        signal_time = reference_time - timedelta(minutes=15)

        status = calculator.calculate(
            signal_timestamp=signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.STALE

    def test_stale_status_very_old(self, calculator, reference_time):
        """Test STALE status for very old signals."""
        signal_time = reference_time - timedelta(hours=24)

        status = calculator.calculate(
            signal_timestamp=signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.STALE

    def test_calculate_for_signal_with_silo(
        self, calculator, sample_signal, sample_silo, reference_time
    ):
        """Test calculating freshness using signal and silo objects."""
        # Signal is at reference_time, check at reference_time (0 minutes old)
        status = calculator.calculate_for_signal(
            signal=sample_signal,
            silo=sample_silo,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.CURRENT

    def test_calculate_for_signal_stale(
        self, calculator, sample_silo, reference_time
    ):
        """Test calculating STALE freshness for old signal."""
        old_signal = Signal(
            signal_id=uuid4(),
            chart_id=uuid4(),
            received_at=reference_time - timedelta(hours=1),
            signal_timestamp=reference_time - timedelta(hours=1),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )

        status = calculator.calculate_for_signal(
            signal=old_signal,
            silo=sample_silo,
            as_of=reference_time,
        )

        assert status == FreshnessStatus.STALE

    def test_uses_current_time_when_as_of_not_provided(self, calculator):
        """Test that current time is used when as_of is not provided."""
        recent_signal_time = datetime.utcnow() - timedelta(seconds=30)

        status = calculator.calculate(
            signal_timestamp=recent_signal_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
            # as_of not provided - should use current time
        )

        assert status == FreshnessStatus.CURRENT


class TestFreshnessCalculatorAgeDescription:
    """Tests for age description generation."""

    @pytest.fixture
    def calculator(self):
        """Create a FreshnessCalculator instance."""
        return FreshnessCalculator()

    @pytest.fixture
    def reference_time(self):
        """Create a fixed reference time for testing."""
        return datetime(2025, 1, 1, 12, 0, 0)

    def test_seconds_ago_description(self, calculator, reference_time):
        """Test age description for seconds."""
        signal_time = reference_time - timedelta(seconds=30)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "30 seconds ago"

    def test_one_minute_ago_singular(self, calculator, reference_time):
        """Test singular minute description."""
        signal_time = reference_time - timedelta(minutes=1)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "1 minute ago"

    def test_multiple_minutes_ago_plural(self, calculator, reference_time):
        """Test plural minutes description."""
        signal_time = reference_time - timedelta(minutes=5)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "5 minutes ago"

    def test_one_hour_ago_singular(self, calculator, reference_time):
        """Test singular hour description."""
        signal_time = reference_time - timedelta(hours=1)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "1 hour ago"

    def test_multiple_hours_ago_plural(self, calculator, reference_time):
        """Test plural hours description."""
        signal_time = reference_time - timedelta(hours=5)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "5 hours ago"

    def test_one_day_ago_singular(self, calculator, reference_time):
        """Test singular day description."""
        signal_time = reference_time - timedelta(days=1)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "1 day ago"

    def test_multiple_days_ago_plural(self, calculator, reference_time):
        """Test plural days description."""
        signal_time = reference_time - timedelta(days=5)

        description = calculator.calculate_age_description(
            signal_timestamp=signal_time,
            as_of=reference_time,
        )

        assert description == "5 days ago"

    def test_zero_seconds_ago(self, calculator, reference_time):
        """Test zero seconds description."""
        description = calculator.calculate_age_description(
            signal_timestamp=reference_time,
            as_of=reference_time,
        )

        assert description == "0 seconds ago"


class TestDefaultFreshnessThresholds:
    """Tests for default freshness thresholds."""

    def test_default_thresholds_exist(self):
        """Test that default thresholds are defined."""
        assert "current_threshold_min" in DEFAULT_FRESHNESS_THRESHOLDS
        assert "recent_threshold_min" in DEFAULT_FRESHNESS_THRESHOLDS
        assert "stale_threshold_min" in DEFAULT_FRESHNESS_THRESHOLDS

    def test_default_current_threshold(self):
        """Test default current threshold value."""
        assert DEFAULT_FRESHNESS_THRESHOLDS["current_threshold_min"] == 2

    def test_default_recent_threshold(self):
        """Test default recent threshold value."""
        assert DEFAULT_FRESHNESS_THRESHOLDS["recent_threshold_min"] == 10

    def test_default_stale_threshold(self):
        """Test default stale threshold value."""
        assert DEFAULT_FRESHNESS_THRESHOLDS["stale_threshold_min"] == 30

    def test_thresholds_are_ordered(self):
        """Test that thresholds are properly ordered."""
        current = DEFAULT_FRESHNESS_THRESHOLDS["current_threshold_min"]
        recent = DEFAULT_FRESHNESS_THRESHOLDS["recent_threshold_min"]
        stale = DEFAULT_FRESHNESS_THRESHOLDS["stale_threshold_min"]

        assert current < recent < stale


class TestFreshnessCalculatorConstitutionalCompliance:
    """
    Tests verifying FreshnessCalculator maintains constitutional compliance.

    CRITICAL: Per Section 7.3, freshness is purely DESCRIPTIVE.
    It does NOT invalidate or suppress data.
    """

    def test_no_invalidation_method(self):
        """
        CRITICAL: FreshnessCalculator must not invalidate data.
        """
        assert not hasattr(FreshnessCalculator, "invalidate")
        assert not hasattr(FreshnessCalculator, "mark_invalid")
        assert not hasattr(FreshnessCalculator, "discard")

    def test_no_suppression_method(self):
        """
        CRITICAL: FreshnessCalculator must not suppress data.
        """
        assert not hasattr(FreshnessCalculator, "suppress")
        assert not hasattr(FreshnessCalculator, "hide")
        assert not hasattr(FreshnessCalculator, "filter_out")

    def test_no_exclusion_method(self):
        """
        CRITICAL: FreshnessCalculator must not exclude stale data.
        """
        assert not hasattr(FreshnessCalculator, "exclude")
        assert not hasattr(FreshnessCalculator, "remove_stale")
        assert not hasattr(FreshnessCalculator, "get_valid_only")

    def test_no_weight_method(self):
        """
        CRITICAL: FreshnessCalculator must not weight by freshness.
        """
        assert not hasattr(FreshnessCalculator, "weight")
        assert not hasattr(FreshnessCalculator, "weight_by_freshness")
        assert not hasattr(FreshnessCalculator, "compute_freshness_weight")

    def test_no_score_method(self):
        """
        CRITICAL: FreshnessCalculator must not score freshness.
        """
        assert not hasattr(FreshnessCalculator, "score")
        assert not hasattr(FreshnessCalculator, "freshness_score")
        assert not hasattr(FreshnessCalculator, "compute_confidence")

    def test_stale_data_still_returned(self):
        """
        CRITICAL: Stale data must be classified but NOT excluded.
        """
        calculator = FreshnessCalculator()
        very_old_time = datetime.utcnow() - timedelta(days=365)

        status = calculator.calculate(
            signal_timestamp=very_old_time,
            current_threshold_min=2,
            recent_threshold_min=10,
            stale_threshold_min=30,
        )

        # Even 1 year old data should return STALE, not raise an error
        # and definitely not return UNAVAILABLE
        assert status == FreshnessStatus.STALE

    def test_unavailable_never_returned_for_old_data(self):
        """
        CRITICAL: UNAVAILABLE is only for retrieval failures, not age.
        """
        calculator = FreshnessCalculator()

        # Test various ages - none should return UNAVAILABLE
        ages = [
            timedelta(seconds=1),
            timedelta(minutes=5),
            timedelta(hours=2),
            timedelta(days=7),
            timedelta(days=365),
        ]

        for age in ages:
            signal_time = datetime.utcnow() - age
            status = calculator.calculate(
                signal_timestamp=signal_time,
                current_threshold_min=2,
                recent_threshold_min=10,
                stale_threshold_min=30,
            )
            assert status != FreshnessStatus.UNAVAILABLE, \
                f"UNAVAILABLE should never be returned for age {age}"


class TestFreshnessStatusValues:
    """Tests for FreshnessStatus enum values."""

    def test_all_status_values_exist(self):
        """Test that all required status values exist."""
        assert hasattr(FreshnessStatus, "CURRENT")
        assert hasattr(FreshnessStatus, "RECENT")
        assert hasattr(FreshnessStatus, "STALE")
        assert hasattr(FreshnessStatus, "UNAVAILABLE")

    def test_status_values_are_strings(self):
        """Test that status values are string-based."""
        assert FreshnessStatus.CURRENT.value == "CURRENT"
        assert FreshnessStatus.RECENT.value == "RECENT"
        assert FreshnessStatus.STALE.value == "STALE"
        assert FreshnessStatus.UNAVAILABLE.value == "UNAVAILABLE"

    def test_status_has_no_numeric_ordering(self):
        """
        CRITICAL: Status should not have numeric values that imply quality.
        """
        # Ensure values are strings, not numbers that could be compared
        for status in FreshnessStatus:
            assert isinstance(status.value, str), \
                f"Status {status.name} should have string value, not numeric"
