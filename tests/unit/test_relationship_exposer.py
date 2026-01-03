"""
Tests for CIA-SIE Relationship Exposer
======================================

Validates relationship exposure and summary generation.

GOVERNED BY: Section 13.3 (Component Specifications - RelationshipExposer)
"""

import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from cia_sie.core.enums import Direction, FreshnessStatus, SignalType
from cia_sie.core.models import RelationshipSummary
from cia_sie.dal.models import SiloDB, ChartDB, SignalDB, InstrumentDB
from cia_sie.dal.repositories import SiloRepository, ChartRepository, SignalRepository
from cia_sie.exposure.relationship_exposer import RelationshipExposer, CrossSiloExposer
from cia_sie.exposure.contradiction_detector import ContradictionDetector
from cia_sie.exposure.confirmation_detector import ConfirmationDetector
from cia_sie.ingestion.freshness import FreshnessCalculator


class TestRelationshipExposer:
    """Tests for RelationshipExposer class."""

    @pytest.fixture
    def mock_silo_repo(self):
        """Create mock silo repository."""
        repo = Mock(spec=SiloRepository)
        repo.get_with_full_hierarchy = AsyncMock()
        repo.get_by_instrument = AsyncMock()
        return repo

    @pytest.fixture
    def mock_chart_repo(self):
        """Create mock chart repository."""
        repo = Mock(spec=ChartRepository)
        return repo

    @pytest.fixture
    def mock_signal_repo(self):
        """Create mock signal repository."""
        repo = Mock(spec=SignalRepository)
        repo.get_latest_by_chart = AsyncMock()
        return repo

    @pytest.fixture
    def exposer(self, mock_silo_repo, mock_chart_repo, mock_signal_repo):
        """Create exposer with mocked dependencies."""
        return RelationshipExposer(
            silo_repository=mock_silo_repo,
            chart_repository=mock_chart_repo,
            signal_repository=mock_signal_repo,
        )

    @pytest.fixture
    def sample_silo(self):
        """Create a sample silo with charts."""
        instrument = Mock(spec=InstrumentDB)
        instrument.symbol = "NIFTY50"

        chart1 = Mock(spec=ChartDB)
        chart1.chart_id = str(uuid4())
        chart1.chart_code = "RSI_14"
        chart1.chart_name = "RSI (14)"
        chart1.timeframe = "1h"
        chart1.is_active = True

        chart2 = Mock(spec=ChartDB)
        chart2.chart_id = str(uuid4())
        chart2.chart_code = "MACD"
        chart2.chart_name = "MACD"
        chart2.timeframe = "1h"
        chart2.is_active = True

        silo = Mock(spec=SiloDB)
        silo.silo_id = str(uuid4())
        silo.silo_name = "Technical"
        silo.instrument_id = str(uuid4())
        silo.current_threshold_min = 2
        silo.recent_threshold_min = 10
        silo.stale_threshold_min = 30
        silo.instrument = instrument
        silo.charts = [chart1, chart2]

        return silo

    @pytest.mark.asyncio
    async def test_expose_for_silo_returns_summary(
        self, exposer, mock_silo_repo, mock_signal_repo, sample_silo
    ):
        """Test exposing relationships returns a summary."""
        mock_silo_repo.get_with_full_hierarchy.return_value = sample_silo
        mock_signal_repo.get_latest_by_chart.return_value = None

        result = await exposer.expose_for_silo(sample_silo.silo_id)

        assert isinstance(result, RelationshipSummary)
        assert result.silo_name == "Technical"
        assert len(result.charts) == 2

    @pytest.mark.asyncio
    async def test_expose_for_silo_not_found(self, exposer, mock_silo_repo):
        """Test exposing for nonexistent silo raises error."""
        mock_silo_repo.get_with_full_hierarchy.return_value = None

        with pytest.raises(ValueError):
            await exposer.expose_for_silo("nonexistent")

    @pytest.mark.asyncio
    async def test_expose_includes_all_charts(
        self, exposer, mock_silo_repo, mock_signal_repo, sample_silo
    ):
        """
        CRITICAL: All charts must be included (none hidden).
        """
        mock_silo_repo.get_with_full_hierarchy.return_value = sample_silo
        mock_signal_repo.get_latest_by_chart.return_value = None

        result = await exposer.expose_for_silo(sample_silo.silo_id)

        # Should include all active charts
        assert len(result.charts) == len([c for c in sample_silo.charts if c.is_active])

    @pytest.mark.asyncio
    async def test_expose_skips_inactive_charts(
        self, exposer, mock_silo_repo, mock_signal_repo, sample_silo
    ):
        """Test that inactive charts are skipped."""
        # Make one chart inactive
        sample_silo.charts[0].is_active = False
        mock_silo_repo.get_with_full_hierarchy.return_value = sample_silo
        mock_signal_repo.get_latest_by_chart.return_value = None

        result = await exposer.expose_for_silo(sample_silo.silo_id)

        assert len(result.charts) == 1

    @pytest.mark.asyncio
    async def test_expose_includes_freshness(
        self, exposer, mock_silo_repo, mock_signal_repo, sample_silo
    ):
        """Test that freshness is calculated for each chart."""
        mock_silo_repo.get_with_full_hierarchy.return_value = sample_silo

        # Create a signal for the first chart
        signal = Mock(spec=SignalDB)
        signal.signal_id = str(uuid4())
        signal.chart_id = sample_silo.charts[0].chart_id
        signal.signal_timestamp = datetime.now(UTC)
        signal.received_at = datetime.now(UTC)
        signal.signal_type = "STATE_CHANGE"
        signal.direction = "BULLISH"
        signal.indicators = {}
        signal.raw_payload = {}

        mock_signal_repo.get_latest_by_chart.side_effect = [signal, None]

        result = await exposer.expose_for_silo(sample_silo.silo_id)

        # First chart should have CURRENT, second UNAVAILABLE
        assert result.charts[0].freshness == FreshnessStatus.CURRENT
        assert result.charts[1].freshness == FreshnessStatus.UNAVAILABLE

    @pytest.mark.asyncio
    async def test_expose_for_instrument(
        self, exposer, mock_silo_repo, mock_signal_repo
    ):
        """Test exposing relationships for all silos of an instrument."""
        silo1 = Mock(spec=SiloDB)
        silo1.silo_id = str(uuid4())
        silo1.silo_name = "Silo 1"
        silo1.instrument_id = str(uuid4())
        silo1.current_threshold_min = 2
        silo1.recent_threshold_min = 10
        silo1.stale_threshold_min = 30
        silo1.instrument = Mock(symbol="NIFTY50")
        silo1.charts = []

        silo2 = Mock(spec=SiloDB)
        silo2.silo_id = str(uuid4())
        silo2.silo_name = "Silo 2"
        silo2.instrument_id = silo1.instrument_id
        silo2.current_threshold_min = 2
        silo2.recent_threshold_min = 10
        silo2.stale_threshold_min = 30
        silo2.instrument = Mock(symbol="NIFTY50")
        silo2.charts = []

        mock_silo_repo.get_by_instrument.return_value = [silo1, silo2]
        mock_silo_repo.get_with_full_hierarchy.side_effect = [silo1, silo2]

        result = await exposer.expose_for_instrument(silo1.instrument_id)

        assert len(result) == 2


class TestRelationshipExposerConstitutionalCompliance:
    """
    Tests verifying RelationshipExposer maintains constitutional compliance.

    CRITICAL: Per Section 13.3, these constraints are absolute.
    """

    def test_no_aggregation_method(self):
        """
        CRITICAL: RelationshipExposer must not aggregate.
        """
        assert not hasattr(RelationshipExposer, "aggregate")
        assert not hasattr(RelationshipExposer, "compute_overall")
        assert not hasattr(RelationshipExposer, "get_net_direction")

    def test_no_scoring_method(self):
        """
        CRITICAL: RelationshipExposer must not compute scores.
        """
        assert not hasattr(RelationshipExposer, "score")
        assert not hasattr(RelationshipExposer, "rate")
        assert not hasattr(RelationshipExposer, "compute_confidence")

    def test_no_recommendation_method(self):
        """
        CRITICAL: RelationshipExposer must not make recommendations.
        """
        assert not hasattr(RelationshipExposer, "recommend")
        assert not hasattr(RelationshipExposer, "advise")
        assert not hasattr(RelationshipExposer, "suggest_action")

    def test_no_filtering_method(self):
        """
        CRITICAL: RelationshipExposer must not filter/hide data.
        """
        assert not hasattr(RelationshipExposer, "filter_contradictions")
        assert not hasattr(RelationshipExposer, "hide_signals")
        assert not hasattr(RelationshipExposer, "suppress")

    def test_no_resolution_method(self):
        """
        CRITICAL: RelationshipExposer must not resolve contradictions.
        """
        assert not hasattr(RelationshipExposer, "resolve")
        assert not hasattr(RelationshipExposer, "pick_best")
        assert not hasattr(RelationshipExposer, "determine_winner")


class TestCrossSiloExposer:
    """Tests for CrossSiloExposer class."""

    def test_cross_silo_no_aggregation(self):
        """
        CRITICAL: Cross-silo exposure must not aggregate.
        """
        assert not hasattr(CrossSiloExposer, "aggregate_across_silos")
        assert not hasattr(CrossSiloExposer, "combine_silos")
        assert not hasattr(CrossSiloExposer, "compute_overall_direction")
