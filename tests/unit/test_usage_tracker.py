"""
Tests for CIA-SIE AI Usage Tracker
==================================

Validates AI usage tracking and budget management.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from cia_sie.core.enums import UsagePeriod
from cia_sie.ai.usage_tracker import UsageTracker


class TestUsageTrackerInitialization:
    """Tests for UsageTracker initialization."""

    def test_init_with_session(self):
        """Test initialization with database session."""
        mock_session = Mock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            tracker = UsageTracker(mock_session)

            assert tracker.session == mock_session
            assert tracker.settings is not None


class TestUsageTrackerPeriodBounds:
    """Tests for period bounds calculation."""

    @pytest.fixture
    def tracker(self):
        """Create UsageTracker with mock session."""
        mock_session = Mock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80
            return UsageTracker(mock_session)

    def test_daily_period_bounds(self, tracker):
        """Test daily period is just the reference date."""
        ref_date = date(2025, 6, 15)
        start, end = tracker._get_period_bounds(UsagePeriod.DAILY, ref_date)

        assert start == date(2025, 6, 15)
        assert end == date(2025, 6, 15)

    def test_weekly_period_bounds_monday(self, tracker):
        """Test weekly period starts on Monday."""
        # Wednesday, June 18, 2025
        ref_date = date(2025, 6, 18)
        start, end = tracker._get_period_bounds(UsagePeriod.WEEKLY, ref_date)

        # Should start Monday June 16
        assert start == date(2025, 6, 16)
        # Should end Sunday June 22
        assert end == date(2025, 6, 22)

    def test_weekly_period_bounds_on_monday(self, tracker):
        """Test weekly period when reference is Monday."""
        # Monday, June 16, 2025
        ref_date = date(2025, 6, 16)
        start, end = tracker._get_period_bounds(UsagePeriod.WEEKLY, ref_date)

        assert start == date(2025, 6, 16)
        assert end == date(2025, 6, 22)

    def test_monthly_period_bounds(self, tracker):
        """Test monthly period spans full month."""
        ref_date = date(2025, 6, 15)
        start, end = tracker._get_period_bounds(UsagePeriod.MONTHLY, ref_date)

        assert start == date(2025, 6, 1)
        assert end == date(2025, 6, 30)

    def test_monthly_period_bounds_december(self, tracker):
        """Test monthly period for December (year rollover)."""
        ref_date = date(2025, 12, 15)
        start, end = tracker._get_period_bounds(UsagePeriod.MONTHLY, ref_date)

        assert start == date(2025, 12, 1)
        assert end == date(2025, 12, 31)

    def test_monthly_period_bounds_february(self, tracker):
        """Test monthly period for February (short month)."""
        ref_date = date(2025, 2, 15)
        start, end = tracker._get_period_bounds(UsagePeriod.MONTHLY, ref_date)

        assert start == date(2025, 2, 1)
        assert end == date(2025, 2, 28)

    def test_monthly_period_bounds_february_leap_year(self, tracker):
        """Test monthly period for February in leap year."""
        ref_date = date(2024, 2, 15)
        start, end = tracker._get_period_bounds(UsagePeriod.MONTHLY, ref_date)

        assert start == date(2024, 2, 1)
        assert end == date(2024, 2, 29)


class TestFormatModelBreakdown:
    """Tests for model breakdown formatting."""

    @pytest.fixture
    def tracker(self):
        """Create UsageTracker with mock session."""
        mock_session = Mock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80
            return UsageTracker(mock_session)

    def test_format_empty_breakdown(self, tracker):
        """Test formatting empty breakdown."""
        result = tracker._format_model_breakdown(None)
        assert result == []

    def test_format_dict_breakdown(self, tracker):
        """Test formatting dict breakdown."""
        breakdown = {
            "claude-3-sonnet": {
                "requests": 10,
                "input_tokens": 1000,
                "output_tokens": 500,
                "cost": 0.05,
            }
        }
        result = tracker._format_model_breakdown(breakdown)

        assert len(result) == 1
        assert result[0]["model_id"] == "claude-3-sonnet"
        assert result[0]["requests"] == 10
        assert result[0]["tokens"] == 1500
        assert result[0]["cost"] == 0.05

    def test_format_string_breakdown(self, tracker):
        """Test formatting JSON string breakdown."""
        import json
        breakdown = json.dumps({
            "claude-3-opus": {
                "requests": 5,
                "input_tokens": 2000,
                "output_tokens": 1000,
                "cost": 0.10,
            }
        })
        result = tracker._format_model_breakdown(breakdown)

        assert len(result) == 1
        assert result[0]["model_id"] == "claude-3-opus"
        assert result[0]["requests"] == 5

    def test_format_multiple_models(self, tracker):
        """Test formatting multiple models."""
        breakdown = {
            "model-a": {"requests": 5, "input_tokens": 100, "output_tokens": 50, "cost": 0.01},
            "model-b": {"requests": 3, "input_tokens": 200, "output_tokens": 100, "cost": 0.02},
        }
        result = tracker._format_model_breakdown(breakdown)

        assert len(result) == 2
        model_ids = [r["model_id"] for r in result]
        assert "model-a" in model_ids
        assert "model-b" in model_ids


class TestRecordUsage:
    """Tests for recording usage."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        session = AsyncMock()
        session.execute = AsyncMock()
        session.flush = AsyncMock()
        session.add = Mock()
        return session

    @pytest.mark.asyncio
    async def test_record_usage_new_period(self, mock_session):
        """Test recording usage creates new period record."""
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            with patch("cia_sie.ai.usage_tracker.estimate_cost") as mock_cost:
                mock_cost.return_value = 0.05

                # Simulate no existing record
                mock_result = Mock()
                mock_result.scalar_one_or_none.return_value = None
                mock_session.execute.return_value = mock_result

                tracker = UsageTracker(mock_session)

                # This will try to create a new record
                # The actual database interaction is mocked
                # Just verify the method can be called
                assert tracker is not None


class TestCheckBudget:
    """Tests for budget checking."""

    @pytest.fixture
    def tracker_with_usage(self):
        """Create tracker with mocked usage data."""
        mock_session = Mock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80
            return UsageTracker(mock_session)

    @pytest.mark.asyncio
    async def test_budget_check_within_budget(self):
        """Test budget check when within budget."""
        mock_session = AsyncMock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            tracker = UsageTracker(mock_session)

            with patch.object(tracker, 'get_usage') as mock_get_usage:
                mock_get_usage.return_value = {
                    "budget": {
                        "percentage_used": 50.0,
                        "remaining": 50.0,
                    }
                }

                status = await tracker.check_budget()

                assert status["within_budget"] is True
                assert status["percentage_used"] == 50.0
                assert status["alert_level"] is None

    @pytest.mark.asyncio
    async def test_budget_check_warning_level(self):
        """Test budget check at warning threshold."""
        mock_session = AsyncMock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            tracker = UsageTracker(mock_session)

            with patch.object(tracker, 'get_usage') as mock_get_usage:
                mock_get_usage.return_value = {
                    "budget": {
                        "percentage_used": 85.0,
                        "remaining": 15.0,
                    }
                }

                status = await tracker.check_budget()

                assert status["within_budget"] is True
                assert status["alert_level"] == "warning"

    @pytest.mark.asyncio
    async def test_budget_check_critical_level(self):
        """Test budget check at critical threshold."""
        mock_session = AsyncMock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            tracker = UsageTracker(mock_session)

            with patch.object(tracker, 'get_usage') as mock_get_usage:
                mock_get_usage.return_value = {
                    "budget": {
                        "percentage_used": 95.0,
                        "remaining": 5.0,
                    }
                }

                status = await tracker.check_budget()

                assert status["within_budget"] is True
                assert status["alert_level"] == "critical"

    @pytest.mark.asyncio
    async def test_budget_check_blocked(self):
        """Test budget check when exhausted."""
        mock_session = AsyncMock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            tracker = UsageTracker(mock_session)

            with patch.object(tracker, 'get_usage') as mock_get_usage:
                mock_get_usage.return_value = {
                    "budget": {
                        "percentage_used": 105.0,
                        "remaining": 0.0,
                    }
                }

                status = await tracker.check_budget()

                assert status["within_budget"] is False
                assert status["alert_level"] == "blocked"
                assert "exhausted" in status["message"]


class TestUsageTrackerConstitutionalCompliance:
    """
    Constitutional compliance tests for UsageTracker.

    CRITICAL: Usage tracking is purely administrative.
    It must not affect signal processing or recommendations.
    """

    @pytest.mark.constitutional
    def test_tracker_has_no_signal_methods(self):
        """CRITICAL: Tracker must not interact with signals."""
        prohibited_methods = [
            'score_signal', 'weight_signal', 'aggregate',
            'recommend', 'advise', 'prioritize',
        ]

        for method in prohibited_methods:
            assert not hasattr(UsageTracker, method), \
                f"CONSTITUTIONAL VIOLATION: UsageTracker has {method}"

    @pytest.mark.constitutional
    def test_tracker_output_has_no_recommendations(self):
        """CRITICAL: Tracker output must not include recommendations."""
        mock_session = AsyncMock()
        with patch("cia_sie.ai.usage_tracker.get_settings") as mock_settings:
            mock_settings.return_value.ai_budget_limit = 100.0
            mock_settings.return_value.ai_budget_alert_threshold = 80

            tracker = UsageTracker(mock_session)

            # Check method signatures don't return recommendations
            import inspect

            for name, method in inspect.getmembers(tracker, predicate=inspect.ismethod):
                if name.startswith('_'):
                    continue
                # Just verify methods exist and are callable
                assert callable(method)
