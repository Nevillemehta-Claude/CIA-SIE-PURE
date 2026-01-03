"""
CIA-SIE Charts API Routes
=========================

CRUD operations for Chart entities.

NOTE: Charts have NO weight attribute (prohibited by ADR-003).
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.exceptions import DuplicateError
from cia_sie.core.models import Chart, ChartCreate
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.models import ChartDB
from cia_sie.dal.repositories import ChartRepository

router = APIRouter()


def get_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> ChartRepository:
    """
    Dependency to get repository with session.

    Args:
        session: Database session from dependency injection

    Returns:
        ChartRepository instance configured with the session
    """
    return ChartRepository(session)


@router.get("/", response_model=list[Chart])
async def list_charts(
    silo_id: Optional[str] = None,
    active_only: bool = True,
    repo: ChartRepository = Depends(get_repository),
):
    """
    List charts, optionally filtered by silo.
    """
    if silo_id:
        charts = await repo.get_by_silo(silo_id, active_only=active_only)
    else:
        charts = await repo.get_all(active_only=active_only)
    return [_db_to_model(c) for c in charts]


@router.post("/", response_model=Chart, status_code=status.HTTP_201_CREATED)
async def create_chart(
    data: ChartCreate,
    repo: ChartRepository = Depends(get_repository),
):
    """
    Create a new chart.

    NOTE: Charts have no weight attribute.
    All charts have equal standing per ADR-003.
    """
    try:
        chart_db = ChartDB(
            silo_id=str(data.silo_id),
            chart_code=data.chart_code,
            chart_name=data.chart_name,
            timeframe=data.timeframe,
            webhook_id=data.webhook_id,
        )
        created = await repo.create(chart_db)
        return _db_to_model(created)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot create chart: {e.message}. A chart with this webhook ID or code may already exist.",
        )


@router.get("/{chart_id}", response_model=Chart)
async def get_chart(
    chart_id: str,
    repo: ChartRepository = Depends(get_repository),
):
    """
    Get a specific chart by ID.
    """
    chart = await repo.get_by_id(chart_id)
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The chart with ID '{chart_id}' was not found. It may have been deleted or never existed.",
        )
    return _db_to_model(chart)


@router.get("/webhook/{webhook_id}", response_model=Chart)
async def get_chart_by_webhook(
    webhook_id: str,
    repo: ChartRepository = Depends(get_repository),
):
    """
    Get chart by webhook ID.
    """
    chart = await repo.get_by_webhook_id(webhook_id)
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No chart found with the webhook ID '{webhook_id}'. Please check the webhook ID and try again.",
        )
    return _db_to_model(chart)


@router.delete("/{chart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chart(
    chart_id: str,
    repo: ChartRepository = Depends(get_repository),
):
    """
    Soft delete a chart.
    """
    deleted = await repo.delete(chart_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot delete chart: The chart with ID '{chart_id}' was not found.",
        )


def _db_to_model(db: ChartDB) -> Chart:
    """Convert database model to domain model."""
    return Chart(
        chart_id=UUID(db.chart_id),
        silo_id=UUID(db.silo_id),
        chart_code=db.chart_code,
        chart_name=db.chart_name,
        timeframe=db.timeframe,
        webhook_id=db.webhook_id,
        created_at=db.created_at,
        updated_at=db.updated_at,
        is_active=db.is_active,
    )
