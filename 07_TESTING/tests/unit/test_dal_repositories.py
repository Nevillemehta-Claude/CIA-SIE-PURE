"""
Tests for CIA-SIE Repository Pattern Implementation
====================================================

Validates repository operations and database abstractions.

GOVERNED BY: Section 9.1 (Architectural Patterns - Repository Pattern)
"""

import pytest
import pytest_asyncio
from datetime import datetime, UTC
from unittest.mock import AsyncMock, Mock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.exceptions import (
    InstrumentNotFoundError,
    DuplicateError,
)
from cia_sie.dal.repositories import (
    BaseRepository,
    InstrumentRepository,
    SiloRepository,
    ChartRepository,
    SignalRepository,
    BasketRepository,
)
from cia_sie.dal.models import (
    InstrumentDB,
    SiloDB,
    ChartDB,
    SignalDB,
    AnalyticalBasketDB,
)


class TestBaseRepository:
    """Tests for BaseRepository abstract class."""

    def test_base_repository_is_abstract(self):
        """Test that BaseRepository cannot be instantiated directly."""
        # BaseRepository is abstract so we can't directly test it
        # but we verify it defines the expected interface
        assert hasattr(BaseRepository, "get_by_id")
        assert hasattr(BaseRepository, "get_all")
        assert hasattr(BaseRepository, "create")
        assert hasattr(BaseRepository, "delete")

    def test_base_repository_requires_session(self):
        """Test that repositories require a session."""
        # All concrete repositories inherit from BaseRepository
        # and require a session parameter
        mock_session = Mock(spec=AsyncSession)
        repo = InstrumentRepository(mock_session)
        assert repo.session == mock_session


class TestInstrumentRepository:
    """Tests for InstrumentRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return InstrumentRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_id_returns_instrument(self, repo, mock_session):
        """Test getting instrument by ID."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_id("test-id")

        assert result == mock_instrument
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_returns_none_when_not_found(self, repo, mock_session):
        """Test getting nonexistent instrument."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_symbol(self, repo, mock_session):
        """Test getting instrument by symbol."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_symbol("NIFTY50")

        assert result == mock_instrument

    @pytest.mark.asyncio
    async def test_get_all_active_only_by_default(self, repo, mock_session):
        """Test get_all filters active by default."""
        mock_instruments = [Mock(spec=InstrumentDB), Mock(spec=InstrumentDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_instruments
        mock_session.execute.return_value = mock_result

        result = await repo.get_all()

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_create_checks_for_duplicates(self, repo, mock_session):
        """Test create rejects duplicate symbols."""
        existing = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing
        mock_session.execute.return_value = mock_result

        new_instrument = Mock(spec=InstrumentDB)
        new_instrument.symbol = "EXISTING"

        with pytest.raises(DuplicateError):
            await repo.create(new_instrument)

    @pytest.mark.asyncio
    async def test_create_adds_new_instrument(self, repo, mock_session):
        """Test successful instrument creation."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        new_instrument = Mock(spec=InstrumentDB)
        new_instrument.symbol = "NEW"

        result = await repo.create(new_instrument)

        mock_session.add.assert_called_once_with(new_instrument)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_raises_when_not_found(self, repo, mock_session):
        """Test update raises error for nonexistent instrument."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with pytest.raises(InstrumentNotFoundError):
            await repo.update("nonexistent", display_name="New Name")

    @pytest.mark.asyncio
    async def test_delete_soft_deletes(self, repo, mock_session):
        """Test delete performs soft delete."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_instrument.is_active = True
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.delete("test-id")

        assert result is True
        assert mock_instrument.is_active is False


class TestSiloRepository:
    """Tests for SiloRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return SiloRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_id(self, repo, mock_session):
        """Test getting silo by ID."""
        mock_silo = Mock(spec=SiloDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_silo
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_id("test-id")

        assert result == mock_silo

    @pytest.mark.asyncio
    async def test_get_by_instrument(self, repo, mock_session):
        """Test getting silos by instrument."""
        mock_silos = [Mock(spec=SiloDB), Mock(spec=SiloDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_silos
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_instrument("instrument-id")

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_create_checks_for_duplicate_name(self, repo, mock_session):
        """Test create rejects duplicate silo names within instrument."""
        existing = Mock(spec=SiloDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing
        mock_session.execute.return_value = mock_result

        new_silo = Mock(spec=SiloDB)
        new_silo.instrument_id = "inst-1"
        new_silo.silo_name = "EXISTING"

        with pytest.raises(DuplicateError):
            await repo.create(new_silo)


class TestChartRepository:
    """Tests for ChartRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return ChartRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_webhook_id(self, repo, mock_session):
        """Test getting chart by webhook ID."""
        mock_chart = Mock(spec=ChartDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_chart
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_webhook_id("webhook-123")

        assert result == mock_chart

    @pytest.mark.asyncio
    async def test_get_by_silo(self, repo, mock_session):
        """Test getting charts by silo."""
        mock_charts = [Mock(spec=ChartDB), Mock(spec=ChartDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_charts
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_silo("silo-id")

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_create_checks_for_duplicate_webhook(self, repo, mock_session):
        """Test create rejects duplicate webhook IDs."""
        existing = Mock(spec=ChartDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing
        mock_session.execute.return_value = mock_result

        new_chart = Mock(spec=ChartDB)
        new_chart.webhook_id = "EXISTING"

        with pytest.raises(DuplicateError):
            await repo.create(new_chart)


class TestSignalRepository:
    """Tests for SignalRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return SignalRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_chart(self, repo, mock_session):
        """Test getting signals by chart."""
        mock_signals = [Mock(spec=SignalDB), Mock(spec=SignalDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_signals
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_chart("chart-id")

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_latest_by_chart(self, repo, mock_session):
        """Test getting latest signal for chart."""
        mock_signal = Mock(spec=SignalDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_signal
        mock_session.execute.return_value = mock_result

        result = await repo.get_latest_by_chart("chart-id")

        assert result == mock_signal

    @pytest.mark.asyncio
    async def test_get_latest_by_charts_empty_list(self, repo, mock_session):
        """Test getting latest signals with empty chart list."""
        result = await repo.get_latest_by_charts([])

        assert result == {}

    @pytest.mark.asyncio
    async def test_create_adds_signal(self, repo, mock_session):
        """Test signal creation."""
        new_signal = Mock(spec=SignalDB)

        await repo.create(new_signal)

        mock_session.add.assert_called_once_with(new_signal)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_is_hard_delete(self, repo, mock_session):
        """Test signal deletion is hard delete."""
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result

        result = await repo.delete("signal-id")

        # Signals are hard deleted (immutable)
        assert result is True


class TestBasketRepository:
    """Tests for BasketRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return BasketRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_id(self, repo, mock_session):
        """Test getting basket by ID."""
        mock_basket = Mock(spec=AnalyticalBasketDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_basket
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_id("basket-id")

        assert result == mock_basket

    @pytest.mark.asyncio
    async def test_get_by_instrument(self, repo, mock_session):
        """Test getting baskets by instrument."""
        mock_baskets = [Mock(spec=AnalyticalBasketDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_baskets
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_instrument("instrument-id")

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_add_chart_to_basket_skips_duplicate(self, repo, mock_session):
        """Test adding chart to basket skips if already exists."""
        existing = Mock()
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing
        mock_session.execute.return_value = mock_result

        result = await repo.add_chart_to_basket("basket-id", "chart-id")

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_soft_deletes(self, repo, mock_session):
        """Test basket deletion is soft delete."""
        mock_basket = Mock(spec=AnalyticalBasketDB)
        mock_basket.is_active = True
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_basket
        mock_session.execute.return_value = mock_result

        result = await repo.delete("basket-id")

        assert result is True
        assert mock_basket.is_active is False


class TestInstrumentRepositoryExtended:
    """Extended tests for InstrumentRepository to improve coverage."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return InstrumentRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_with_silos(self, repo, mock_session):
        """Test getting instrument with eagerly loaded silos."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.get_with_silos("inst-id")

        assert result == mock_instrument
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_updates_display_name(self, repo, mock_session):
        """Test update modifies display_name."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.update("inst-id", display_name="New Name")

        assert mock_instrument.display_name == "New Name"

    @pytest.mark.asyncio
    async def test_update_updates_metadata(self, repo, mock_session):
        """Test update modifies metadata_json."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.update("inst-id", metadata_json={"key": "value"})

        assert mock_instrument.metadata_json == {"key": "value"}

    @pytest.mark.asyncio
    async def test_update_updates_is_active(self, repo, mock_session):
        """Test update modifies is_active."""
        mock_instrument = Mock(spec=InstrumentDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_instrument
        mock_session.execute.return_value = mock_result

        result = await repo.update("inst-id", is_active=True)

        assert mock_instrument.is_active is True

    @pytest.mark.asyncio
    async def test_get_all_includes_inactive(self, repo, mock_session):
        """Test get_all with active_only=False includes inactive."""
        mock_instruments = [Mock(spec=InstrumentDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_instruments
        mock_session.execute.return_value = mock_result

        result = await repo.get_all(active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_not_found(self, repo, mock_session):
        """Test delete returns False when instrument not found."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repo.delete("nonexistent")

        assert result is False


class TestSiloRepositoryExtended:
    """Extended tests for SiloRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return SiloRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_all(self, repo, mock_session):
        """Test getting all silos."""
        mock_silos = [Mock(spec=SiloDB), Mock(spec=SiloDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_silos
        mock_session.execute.return_value = mock_result

        result = await repo.get_all()

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_all_inactive(self, repo, mock_session):
        """Test get_all with active_only=False."""
        mock_silos = [Mock(spec=SiloDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_silos
        mock_session.execute.return_value = mock_result

        result = await repo.get_all(active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_with_charts(self, repo, mock_session):
        """Test getting silo with eagerly loaded charts."""
        mock_silo = Mock(spec=SiloDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_silo
        mock_session.execute.return_value = mock_result

        result = await repo.get_with_charts("silo-id")

        assert result == mock_silo

    @pytest.mark.asyncio
    async def test_get_with_full_hierarchy(self, repo, mock_session):
        """Test getting silo with instrument and charts."""
        mock_silo = Mock(spec=SiloDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_silo
        mock_session.execute.return_value = mock_result

        result = await repo.get_with_full_hierarchy("silo-id")

        assert result == mock_silo

    @pytest.mark.asyncio
    async def test_get_by_instrument_inactive(self, repo, mock_session):
        """Test get_by_instrument with active_only=False."""
        mock_silos = [Mock(spec=SiloDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_silos
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_instrument("inst-id", active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_create_success(self, repo, mock_session):
        """Test successful silo creation."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        new_silo = Mock(spec=SiloDB)
        new_silo.instrument_id = "inst-1"
        new_silo.silo_name = "NEW"

        result = await repo.create(new_silo)

        mock_session.add.assert_called_once_with(new_silo)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_success(self, repo, mock_session):
        """Test successful silo deletion."""
        mock_silo = Mock(spec=SiloDB)
        mock_silo.is_active = True
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_silo
        mock_session.execute.return_value = mock_result

        result = await repo.delete("silo-id")

        assert result is True
        assert mock_silo.is_active is False

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, mock_session):
        """Test delete returns False when not found."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repo.delete("nonexistent")

        assert result is False


class TestChartRepositoryExtended:
    """Extended tests for ChartRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return ChartRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_id(self, repo, mock_session):
        """Test getting chart by ID."""
        mock_chart = Mock(spec=ChartDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_chart
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_id("chart-id")

        assert result == mock_chart

    @pytest.mark.asyncio
    async def test_get_all(self, repo, mock_session):
        """Test getting all charts."""
        mock_charts = [Mock(spec=ChartDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_charts
        mock_session.execute.return_value = mock_result

        result = await repo.get_all()

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_all_inactive(self, repo, mock_session):
        """Test get_all with active_only=False."""
        mock_charts = [Mock(spec=ChartDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_charts
        mock_session.execute.return_value = mock_result

        result = await repo.get_all(active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_by_silo_inactive(self, repo, mock_session):
        """Test get_by_silo with active_only=False."""
        mock_charts = [Mock(spec=ChartDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_charts
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_silo("silo-id", active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_with_latest_signal(self, repo, mock_session):
        """Test getting chart with its latest signal."""
        mock_chart = Mock(spec=ChartDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_chart
        mock_session.execute.return_value = mock_result

        result = await repo.get_with_latest_signal("chart-id")

        assert result == mock_chart

    @pytest.mark.asyncio
    async def test_create_success(self, repo, mock_session):
        """Test successful chart creation."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        new_chart = Mock(spec=ChartDB)
        new_chart.webhook_id = "NEW"

        result = await repo.create(new_chart)

        mock_session.add.assert_called_once_with(new_chart)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_success(self, repo, mock_session):
        """Test successful chart deletion."""
        mock_chart = Mock(spec=ChartDB)
        mock_chart.is_active = True
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_chart
        mock_session.execute.return_value = mock_result

        result = await repo.delete("chart-id")

        assert result is True
        assert mock_chart.is_active is False

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, mock_session):
        """Test delete returns False when not found."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repo.delete("nonexistent")

        assert result is False


class TestSignalRepositoryExtended:
    """Extended tests for SignalRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return SignalRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_by_id(self, repo, mock_session):
        """Test getting signal by ID."""
        mock_signal = Mock(spec=SignalDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_signal
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_id("signal-id")

        assert result == mock_signal

    @pytest.mark.asyncio
    async def test_get_all(self, repo, mock_session):
        """Test getting all signals."""
        mock_signals = [Mock(spec=SignalDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_signals
        mock_session.execute.return_value = mock_result

        result = await repo.get_all()

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_latest_by_charts_with_charts(self, repo, mock_session):
        """Test getting latest signals for multiple charts."""
        mock_signal = Mock(spec=SignalDB)
        mock_signal.chart_id = "chart-1"
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_signal]
        mock_session.execute.return_value = mock_result

        result = await repo.get_latest_by_charts(["chart-1", "chart-2"])

        assert "chart-1" in result
        assert result["chart-1"] == mock_signal

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, mock_session):
        """Test delete returns False when signal not found."""
        mock_result = Mock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result

        result = await repo.delete("nonexistent")

        assert result is False


class TestBasketRepositoryExtended:
    """Extended tests for BasketRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = Mock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def repo(self, mock_session):
        """Create repository with mock session."""
        return BasketRepository(mock_session)

    @pytest.mark.asyncio
    async def test_get_all(self, repo, mock_session):
        """Test getting all baskets."""
        mock_baskets = [Mock(spec=AnalyticalBasketDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_baskets
        mock_session.execute.return_value = mock_result

        result = await repo.get_all()

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_all_inactive(self, repo, mock_session):
        """Test get_all with active_only=False."""
        mock_baskets = [Mock(spec=AnalyticalBasketDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_baskets
        mock_session.execute.return_value = mock_result

        result = await repo.get_all(active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_with_charts(self, repo, mock_session):
        """Test getting basket with charts."""
        mock_basket = Mock(spec=AnalyticalBasketDB)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_basket
        mock_session.execute.return_value = mock_result

        result = await repo.get_with_charts("basket-id")

        assert result == mock_basket

    @pytest.mark.asyncio
    async def test_get_by_instrument_inactive(self, repo, mock_session):
        """Test get_by_instrument with active_only=False."""
        mock_baskets = [Mock(spec=AnalyticalBasketDB)]
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_baskets
        mock_session.execute.return_value = mock_result

        result = await repo.get_by_instrument("inst-id", active_only=False)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_create(self, repo, mock_session):
        """Test basket creation."""
        new_basket = Mock(spec=AnalyticalBasketDB)

        result = await repo.create(new_basket)

        mock_session.add.assert_called_once_with(new_basket)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_chart_to_basket_success(self, repo, mock_session):
        """Test successfully adding chart to basket."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None  # No existing association
        mock_session.execute.return_value = mock_result

        result = await repo.add_chart_to_basket("basket-id", "chart-id")

        assert result is True
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_remove_chart_from_basket_success(self, repo, mock_session):
        """Test removing chart from basket."""
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result

        result = await repo.remove_chart_from_basket("basket-id", "chart-id")

        assert result is True

    @pytest.mark.asyncio
    async def test_remove_chart_from_basket_not_found(self, repo, mock_session):
        """Test removing non-existent chart from basket."""
        mock_result = Mock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result

        result = await repo.remove_chart_from_basket("basket-id", "chart-id")

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, mock_session):
        """Test delete returns False when basket not found."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repo.delete("nonexistent")

        assert result is False


class TestRepositoryConstitutionalCompliance:
    """
    Tests verifying repositories don't expose prohibited operations.

    CRITICAL: Per Section 0B, certain operations are PROHIBITED.
    """

    def test_no_aggregation_methods(self):
        """
        CRITICAL: Repositories must not have aggregation methods.
        """
        prohibited_methods = [
            "compute_aggregate",
            "get_weighted_average",
            "calculate_score",
            "get_overall_direction",
        ]

        repositories = [
            InstrumentRepository,
            SiloRepository,
            ChartRepository,
            SignalRepository,
            BasketRepository,
        ]

        for repo_class in repositories:
            for method in prohibited_methods:
                assert not hasattr(repo_class, method), \
                    f"{repo_class.__name__} has prohibited '{method}' method"

    def test_no_recommendation_methods(self):
        """
        CRITICAL: Repositories must not have recommendation methods.
        """
        prohibited_methods = [
            "get_recommendation",
            "suggest_action",
            "compute_advice",
        ]

        repositories = [
            InstrumentRepository,
            SiloRepository,
            ChartRepository,
            SignalRepository,
            BasketRepository,
        ]

        for repo_class in repositories:
            for method in prohibited_methods:
                assert not hasattr(repo_class, method), \
                    f"{repo_class.__name__} has prohibited '{method}' method"
