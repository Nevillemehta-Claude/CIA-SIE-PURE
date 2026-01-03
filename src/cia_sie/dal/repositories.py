"""
CIA-SIE Repository Pattern Implementation
==========================================

Implements the Repository Pattern for data access abstraction.
All database operations go through these repositories.

GOVERNED BY: Section 9.1 (Architectural Patterns - Repository Pattern)
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from typing import Generic, Optional, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from cia_sie.core.exceptions import (
    DuplicateError,
    InstrumentNotFoundError,
)
from cia_sie.dal.models import (
    AnalyticalBasketDB,
    BasketChartDB,
    ChartDB,
    InstrumentDB,
    SignalDB,
    SiloDB,
)

# =============================================================================
# GENERIC REPOSITORY BASE
# =============================================================================

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository with common operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def get_all(self, active_only: bool = True) -> Sequence[T]:
        """Get all entities."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete an entity."""
        pass


# =============================================================================
# INSTRUMENT REPOSITORY
# =============================================================================


class InstrumentRepository(BaseRepository[InstrumentDB]):
    """Repository for Instrument entities."""

    async def get_by_id(self, instrument_id: str) -> Optional[InstrumentDB]:
        """Get instrument by ID."""
        result = await self.session.execute(
            select(InstrumentDB).where(InstrumentDB.instrument_id == instrument_id)
        )
        return result.scalar_one_or_none()

    async def get_by_symbol(self, symbol: str) -> Optional[InstrumentDB]:
        """Get instrument by symbol."""
        result = await self.session.execute(
            select(InstrumentDB).where(InstrumentDB.symbol == symbol)
        )
        return result.scalar_one_or_none()

    async def get_all(self, active_only: bool = True) -> Sequence[InstrumentDB]:
        """Get all instruments."""
        query = select(InstrumentDB)
        if active_only:
            query = query.where(InstrumentDB.is_active)
        query = query.order_by(InstrumentDB.display_name)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_silos(self, instrument_id: str) -> Optional[InstrumentDB]:
        """Get instrument with eagerly loaded silos."""
        result = await self.session.execute(
            select(InstrumentDB)
            .options(selectinload(InstrumentDB.silos))
            .where(InstrumentDB.instrument_id == instrument_id)
        )
        return result.scalar_one_or_none()

    async def create(self, instrument: InstrumentDB) -> InstrumentDB:
        """Create a new instrument."""
        existing = await self.get_by_symbol(instrument.symbol)
        if existing:
            raise DuplicateError(
                f"Instrument with symbol '{instrument.symbol}' already exists",
                {"symbol": instrument.symbol},
            )
        self.session.add(instrument)
        await self.session.flush()
        return instrument

    async def update(
        self,
        instrument_id: str,
        display_name: Optional[str] = None,
        metadata_json: Optional[dict] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[InstrumentDB]:
        """Update an instrument."""
        instrument = await self.get_by_id(instrument_id)
        if not instrument:
            raise InstrumentNotFoundError(f"Instrument with ID '{instrument_id}' not found")

        if display_name is not None:
            instrument.display_name = display_name
        if metadata_json is not None:
            instrument.metadata_json = metadata_json
        if is_active is not None:
            instrument.is_active = is_active

        instrument.updated_at = datetime.utcnow()
        await self.session.flush()
        return instrument

    async def delete(self, instrument_id: str) -> bool:
        """Soft delete an instrument."""
        instrument = await self.get_by_id(instrument_id)
        if not instrument:
            return False
        instrument.is_active = False
        instrument.updated_at = datetime.utcnow()
        await self.session.flush()
        return True


# =============================================================================
# SILO REPOSITORY
# =============================================================================


class SiloRepository(BaseRepository[SiloDB]):
    """Repository for Silo entities."""

    async def get_by_id(self, silo_id: str) -> Optional[SiloDB]:
        """Get silo by ID."""
        result = await self.session.execute(select(SiloDB).where(SiloDB.silo_id == silo_id))
        return result.scalar_one_or_none()

    async def get_all(self, active_only: bool = True) -> Sequence[SiloDB]:
        """Get all silos."""
        query = select(SiloDB)
        if active_only:
            query = query.where(SiloDB.is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_instrument(
        self, instrument_id: str, active_only: bool = True
    ) -> Sequence[SiloDB]:
        """Get all silos for an instrument."""
        query = select(SiloDB).where(SiloDB.instrument_id == instrument_id)
        if active_only:
            query = query.where(SiloDB.is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_charts(self, silo_id: str) -> Optional[SiloDB]:
        """Get silo with eagerly loaded charts."""
        result = await self.session.execute(
            select(SiloDB).options(selectinload(SiloDB.charts)).where(SiloDB.silo_id == silo_id)
        )
        return result.scalar_one_or_none()

    async def get_with_full_hierarchy(self, silo_id: str) -> Optional[SiloDB]:
        """Get silo with instrument and charts."""
        result = await self.session.execute(
            select(SiloDB)
            .options(
                selectinload(SiloDB.instrument),
                selectinload(SiloDB.charts).selectinload(ChartDB.signals),
            )
            .where(SiloDB.silo_id == silo_id)
        )
        return result.scalar_one_or_none()

    async def create(self, silo: SiloDB) -> SiloDB:
        """Create a new silo."""
        # Check for duplicate name within instrument
        result = await self.session.execute(
            select(SiloDB).where(
                SiloDB.instrument_id == silo.instrument_id, SiloDB.silo_name == silo.silo_name
            )
        )
        if result.scalar_one_or_none():
            raise DuplicateError(
                f"Silo with name '{silo.silo_name}' already exists for this instrument",
                {"silo_name": silo.silo_name},
            )
        self.session.add(silo)
        await self.session.flush()
        return silo

    async def delete(self, silo_id: str) -> bool:
        """Soft delete a silo."""
        silo = await self.get_by_id(silo_id)
        if not silo:
            return False
        silo.is_active = False
        silo.updated_at = datetime.utcnow()
        await self.session.flush()
        return True


# =============================================================================
# CHART REPOSITORY
# =============================================================================


class ChartRepository(BaseRepository[ChartDB]):
    """Repository for Chart entities."""

    async def get_by_id(self, chart_id: str) -> Optional[ChartDB]:
        """Get chart by ID."""
        result = await self.session.execute(select(ChartDB).where(ChartDB.chart_id == chart_id))
        return result.scalar_one_or_none()

    async def get_by_webhook_id(self, webhook_id: str) -> Optional[ChartDB]:
        """Get chart by webhook ID."""
        result = await self.session.execute(select(ChartDB).where(ChartDB.webhook_id == webhook_id))
        return result.scalar_one_or_none()

    async def get_all(self, active_only: bool = True) -> Sequence[ChartDB]:
        """Get all charts."""
        query = select(ChartDB)
        if active_only:
            query = query.where(ChartDB.is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_silo(self, silo_id: str, active_only: bool = True) -> Sequence[ChartDB]:
        """Get all charts for a silo."""
        query = select(ChartDB).where(ChartDB.silo_id == silo_id)
        if active_only:
            query = query.where(ChartDB.is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_latest_signal(self, chart_id: str) -> Optional[ChartDB]:
        """Get chart with its latest signal."""
        result = await self.session.execute(
            select(ChartDB)
            .options(selectinload(ChartDB.signals))
            .where(ChartDB.chart_id == chart_id)
        )
        return result.scalar_one_or_none()

    async def create(self, chart: ChartDB) -> ChartDB:
        """Create a new chart."""
        # Check for duplicate webhook_id
        existing = await self.get_by_webhook_id(chart.webhook_id)
        if existing:
            raise DuplicateError(
                f"Chart with webhook_id '{chart.webhook_id}' already exists",
                {"webhook_id": chart.webhook_id},
            )
        self.session.add(chart)
        await self.session.flush()
        return chart

    async def delete(self, chart_id: str) -> bool:
        """Soft delete a chart."""
        chart = await self.get_by_id(chart_id)
        if not chart:
            return False
        chart.is_active = False
        chart.updated_at = datetime.utcnow()
        await self.session.flush()
        return True


# =============================================================================
# SIGNAL REPOSITORY
# =============================================================================


class SignalRepository(BaseRepository[SignalDB]):
    """Repository for Signal entities."""

    async def get_by_id(self, signal_id: str) -> Optional[SignalDB]:
        """Get signal by ID."""
        result = await self.session.execute(select(SignalDB).where(SignalDB.signal_id == signal_id))
        return result.scalar_one_or_none()

    async def get_all(self, active_only: bool = True) -> Sequence[SignalDB]:
        """Get all signals (recent only by default)."""
        query = select(SignalDB).order_by(SignalDB.signal_timestamp.desc()).limit(1000)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_chart(self, chart_id: str, limit: int = 100) -> Sequence[SignalDB]:
        """Get signals for a chart, ordered by timestamp descending."""
        result = await self.session.execute(
            select(SignalDB)
            .where(SignalDB.chart_id == chart_id)
            .order_by(SignalDB.signal_timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_latest_by_chart(self, chart_id: str) -> Optional[SignalDB]:
        """Get the most recent signal for a chart."""
        result = await self.session.execute(
            select(SignalDB)
            .where(SignalDB.chart_id == chart_id)
            .order_by(SignalDB.signal_timestamp.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_latest_by_charts(self, chart_ids: list[str]) -> dict[str, SignalDB]:
        """
        Get latest signal for multiple charts.

        This method efficiently retrieves the most recent signal for each chart
        in the provided list. Charts without signals are excluded from the result.

        Args:
            chart_ids: List of chart IDs to query

        Returns:
            Dictionary mapping chart_id to its latest SignalDB, if available
        """
        if not chart_ids:
            return {}

        # Optimize: Use a single query with subquery for better performance
        from sqlalchemy import func

        subquery = (
            select(SignalDB.chart_id, func.max(SignalDB.signal_timestamp).label("max_timestamp"))
            .where(SignalDB.chart_id.in_(chart_ids))
            .group_by(SignalDB.chart_id)
            .subquery()
        )

        result_query = select(SignalDB).join(
            subquery,
            (SignalDB.chart_id == subquery.c.chart_id)
            & (SignalDB.signal_timestamp == subquery.c.max_timestamp),
        )

        query_result = await self.session.execute(result_query)
        signals = query_result.scalars().all()

        return {signal.chart_id: signal for signal in signals}

    async def create(self, signal: SignalDB) -> SignalDB:
        """Create a new signal."""
        self.session.add(signal)
        await self.session.flush()
        return signal

    async def delete(self, signal_id: str) -> bool:
        """Hard delete a signal (signals are immutable)."""
        result = await self.session.execute(delete(SignalDB).where(SignalDB.signal_id == signal_id))
        return result.rowcount > 0


# =============================================================================
# ANALYTICAL BASKET REPOSITORY
# =============================================================================


class BasketRepository(BaseRepository[AnalyticalBasketDB]):
    """Repository for AnalyticalBasket entities."""

    async def get_by_id(self, basket_id: str) -> Optional[AnalyticalBasketDB]:
        """Get basket by ID."""
        result = await self.session.execute(
            select(AnalyticalBasketDB).where(AnalyticalBasketDB.basket_id == basket_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, active_only: bool = True) -> Sequence[AnalyticalBasketDB]:
        """Get all baskets."""
        query = select(AnalyticalBasketDB)
        if active_only:
            query = query.where(AnalyticalBasketDB.is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_charts(self, basket_id: str) -> Optional[AnalyticalBasketDB]:
        """Get basket with its charts."""
        result = await self.session.execute(
            select(AnalyticalBasketDB)
            .options(
                selectinload(AnalyticalBasketDB.chart_associations).selectinload(
                    BasketChartDB.chart
                )
            )
            .where(AnalyticalBasketDB.basket_id == basket_id)
        )
        return result.scalar_one_or_none()

    async def get_by_instrument(
        self, instrument_id: str, active_only: bool = True
    ) -> Sequence[AnalyticalBasketDB]:
        """Get all baskets for an instrument."""
        query = select(AnalyticalBasketDB).where(AnalyticalBasketDB.instrument_id == instrument_id)
        if active_only:
            query = query.where(AnalyticalBasketDB.is_active)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, basket: AnalyticalBasketDB) -> AnalyticalBasketDB:
        """Create a new basket."""
        self.session.add(basket)
        await self.session.flush()
        return basket

    async def add_chart_to_basket(self, basket_id: str, chart_id: str) -> bool:
        """Add a chart to a basket."""
        # Check if already exists
        result = await self.session.execute(
            select(BasketChartDB).where(
                BasketChartDB.basket_id == basket_id, BasketChartDB.chart_id == chart_id
            )
        )
        if result.scalar_one_or_none():
            return False  # Already exists

        association = BasketChartDB(basket_id=basket_id, chart_id=chart_id)
        self.session.add(association)
        await self.session.flush()
        return True

    async def remove_chart_from_basket(self, basket_id: str, chart_id: str) -> bool:
        """Remove a chart from a basket."""
        result = await self.session.execute(
            delete(BasketChartDB).where(
                BasketChartDB.basket_id == basket_id, BasketChartDB.chart_id == chart_id
            )
        )
        return result.rowcount > 0

    async def delete(self, basket_id: str) -> bool:
        """Soft delete a basket."""
        basket = await self.get_by_id(basket_id)
        if not basket:
            return False
        basket.is_active = False
        basket.updated_at = datetime.utcnow()
        await self.session.flush()
        return True
