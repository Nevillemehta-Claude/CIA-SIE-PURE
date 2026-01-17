"""
CIA-SIE Analytical Baskets API Routes
=====================================

CRUD operations for Analytical Baskets.

GOVERNED BY: Section 15 (Analytical Baskets)

CRITICAL:
- Baskets are UI-layer constructs ONLY
- They do NOT affect processing
- Creating/modifying baskets has ZERO impact on signals
- Charts can belong to multiple baskets
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.enums import BasketType
from cia_sie.core.models import AnalyticalBasket, BasketCreate
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.models import AnalyticalBasketDB
from cia_sie.dal.repositories import BasketRepository

router = APIRouter()


def get_repository(session: AsyncSession = Depends(get_session_dependency)):
    """Dependency to get repository with session."""
    return BasketRepository(session)


@router.get("/", response_model=list[AnalyticalBasket])
async def list_baskets(
    instrument_id: Optional[str] = None,
    active_only: bool = True,
    repo: BasketRepository = Depends(get_repository),
):
    """
    List analytical baskets.

    NOTE: Baskets are organizational/display constructs.
    They have no impact on signal processing.
    """
    if instrument_id:
        baskets = await repo.get_by_instrument(instrument_id, active_only=active_only)
    else:
        baskets = await repo.get_all(active_only=active_only)
    return [_db_to_model(b) for b in baskets]


@router.post("/", response_model=AnalyticalBasket, status_code=status.HTTP_201_CREATED)
async def create_basket(
    data: BasketCreate,
    repo: BasketRepository = Depends(get_repository),
):
    """
    Create a new analytical basket.

    Baskets allow grouping charts for comparison.
    Creating a basket has NO effect on signal processing.
    """
    # Handle basket_type whether it's an enum or string
    basket_type_value = (
        data.basket_type.value if hasattr(data.basket_type, "value") else data.basket_type
    )
    basket_db = AnalyticalBasketDB(
        basket_name=data.basket_name,
        basket_type=basket_type_value,
        description=data.description,
        instrument_id=str(data.instrument_id) if data.instrument_id else None,
    )
    created = await repo.create(basket_db)

    # Add charts if provided
    for chart_id in data.chart_ids:
        await repo.add_chart_to_basket(created.basket_id, str(chart_id))

    return _db_to_model(created)


@router.get("/{basket_id}", response_model=AnalyticalBasket)
async def get_basket(
    basket_id: str,
    repo: BasketRepository = Depends(get_repository),
):
    """
    Get a specific basket by ID.
    """
    basket = await repo.get_with_charts(basket_id)
    if not basket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Basket not found: {basket_id}",
        )
    return _db_to_model_with_charts(basket)


@router.post("/{basket_id}/charts/{chart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_chart_to_basket(
    basket_id: str,
    chart_id: str,
    repo: BasketRepository = Depends(get_repository),
):
    """
    Add a chart to a basket.

    Charts can belong to multiple baskets.
    This operation has NO effect on signal processing.
    """
    added = await repo.add_chart_to_basket(basket_id, chart_id)
    if not added:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Chart already in basket",
        )


@router.delete("/{basket_id}/charts/{chart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_chart_from_basket(
    basket_id: str,
    chart_id: str,
    repo: BasketRepository = Depends(get_repository),
):
    """
    Remove a chart from a basket.

    This operation has NO effect on signal processing.
    """
    removed = await repo.remove_chart_from_basket(basket_id, chart_id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not in basket",
        )


@router.delete("/{basket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_basket(
    basket_id: str,
    repo: BasketRepository = Depends(get_repository),
):
    """
    Soft delete a basket.

    Deleting a basket does NOT delete chart data.
    """
    deleted = await repo.delete(basket_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Basket not found: {basket_id}",
        )


def _db_to_model(db: AnalyticalBasketDB) -> AnalyticalBasket:
    """Convert database model to domain model."""
    return AnalyticalBasket(
        basket_id=UUID(db.basket_id),
        basket_name=db.basket_name,
        basket_type=BasketType(db.basket_type),
        description=db.description,
        instrument_id=UUID(db.instrument_id) if db.instrument_id else None,
        chart_ids=[],  # Not loaded
        created_at=db.created_at,
        updated_at=db.updated_at,
        is_active=db.is_active,
    )


def _db_to_model_with_charts(db: AnalyticalBasketDB) -> AnalyticalBasket:
    """Convert database model to domain model with charts."""
    chart_ids = [UUID(assoc.chart_id) for assoc in db.chart_associations]
    return AnalyticalBasket(
        basket_id=UUID(db.basket_id),
        basket_name=db.basket_name,
        basket_type=BasketType(db.basket_type),
        description=db.description,
        instrument_id=UUID(db.instrument_id) if db.instrument_id else None,
        chart_ids=chart_ids,
        created_at=db.created_at,
        updated_at=db.updated_at,
        is_active=db.is_active,
    )
