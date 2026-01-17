"""
CIA-SIE Signals API Routes
==========================

Read operations for Signal entities.

NOTE: Signals have NO confidence score (prohibited by ADR-003).
Signals are created via webhooks, not directly through this API.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.enums import Direction, SignalType
from cia_sie.core.models import Signal
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.models import SignalDB
from cia_sie.dal.repositories import SignalRepository

router = APIRouter()


def get_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> SignalRepository:
    """
    Dependency to get repository with session.

    Args:
        session: Database session from dependency injection

    Returns:
        SignalRepository instance configured with the session
    """
    return SignalRepository(session)


@router.get("/chart/{chart_id}", response_model=list[Signal])
async def list_signals_for_chart(
    chart_id: str,
    limit: int = 100,
    repo: SignalRepository = Depends(get_repository),
):
    """
    List signals for a specific chart.

    Returns signals ordered by timestamp (newest first).
    """
    signals = await repo.get_by_chart(chart_id, limit=limit)
    return [_db_to_model(s) for s in signals]


@router.get("/chart/{chart_id}/latest", response_model=Optional[Signal])
async def get_latest_signal(
    chart_id: str,
    repo: SignalRepository = Depends(get_repository),
):
    """
    Get the most recent signal for a chart.
    """
    signal = await repo.get_latest_by_chart(chart_id)
    if signal:
        return _db_to_model(signal)
    return None


@router.get("/{signal_id}", response_model=Signal)
async def get_signal(
    signal_id: str,
    repo: SignalRepository = Depends(get_repository),
):
    """
    Get a specific signal by ID.
    """
    signal = await repo.get_by_id(signal_id)
    if not signal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The signal with ID '{signal_id}' was not found. It may have been deleted or never existed.",
        )
    return _db_to_model(signal)


def _db_to_model(db: SignalDB) -> Signal:
    """Convert database model to domain model."""
    return Signal(
        signal_id=UUID(db.signal_id),
        chart_id=UUID(db.chart_id),
        received_at=db.received_at,
        signal_timestamp=db.signal_timestamp,
        signal_type=SignalType(db.signal_type),
        direction=Direction(db.direction),
        indicators=db.indicators if isinstance(db.indicators, dict) else {},
        raw_payload=db.raw_payload if isinstance(db.raw_payload, dict) else {},
    )
