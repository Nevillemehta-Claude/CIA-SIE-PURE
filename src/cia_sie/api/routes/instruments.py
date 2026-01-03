"""
CIA-SIE Instruments API Routes
==============================

CRUD operations for Instrument entities.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.exceptions import DuplicateError, InstrumentNotFoundError
from cia_sie.core.models import Instrument, InstrumentCreate
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.models import InstrumentDB
from cia_sie.dal.repositories import InstrumentRepository

router = APIRouter()


def get_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> InstrumentRepository:
    """
    Dependency to get repository with session.

    Args:
        session: Database session from dependency injection

    Returns:
        InstrumentRepository instance configured with the session
    """
    return InstrumentRepository(session)


@router.get("/", response_model=list[Instrument])
async def list_instruments(
    active_only: bool = True,
    repo: InstrumentRepository = Depends(get_repository),
):
    """
    List all instruments.

    Args:
        active_only: If True, only return active instruments
    """
    instruments = await repo.get_all(active_only=active_only)
    return [_db_to_model(i) for i in instruments]


@router.post("/", response_model=Instrument, status_code=status.HTTP_201_CREATED)
async def create_instrument(
    data: InstrumentCreate,
    repo: InstrumentRepository = Depends(get_repository),
):
    """
    Create a new instrument.

    Args:
        data: Instrument creation data
    """
    try:
        instrument_db = InstrumentDB(
            symbol=data.symbol,
            display_name=data.display_name,
            metadata_json=data.metadata,
        )
        created = await repo.create(instrument_db)
        return _db_to_model(created)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot create instrument: {e.message}. An instrument with this symbol may already exist.",
        )


@router.get("/{instrument_id}", response_model=Instrument)
async def get_instrument(
    instrument_id: str,
    repo: InstrumentRepository = Depends(get_repository),
):
    """
    Get a specific instrument by ID.
    """
    instrument = await repo.get_by_id(instrument_id)
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The instrument with ID '{instrument_id}' was not found. It may have been deleted or never existed.",
        )
    return _db_to_model(instrument)


@router.get("/symbol/{symbol}", response_model=Instrument)
async def get_instrument_by_symbol(
    symbol: str,
    repo: InstrumentRepository = Depends(get_repository),
):
    """
    Get instrument by trading symbol.
    """
    instrument = await repo.get_by_symbol(symbol)
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No instrument found with the symbol '{symbol}'. Please check the symbol and try again.",
        )
    return _db_to_model(instrument)


@router.patch("/{instrument_id}", response_model=Instrument)
async def update_instrument(
    instrument_id: str,
    display_name: Optional[str] = None,
    is_active: Optional[bool] = None,
    repo: InstrumentRepository = Depends(get_repository),
):
    """
    Update an instrument.
    """
    try:
        updated = await repo.update(
            instrument_id=instrument_id,
            display_name=display_name,
            is_active=is_active,
        )
        return _db_to_model(updated)
    except InstrumentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot update instrument: {e.message}",
        )


@router.delete("/{instrument_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instrument(
    instrument_id: str,
    repo: InstrumentRepository = Depends(get_repository),
):
    """
    Soft delete an instrument.
    """
    deleted = await repo.delete(instrument_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot delete instrument: The instrument with ID '{instrument_id}' was not found.",
        )


def _db_to_model(db: InstrumentDB) -> Instrument:
    """Convert database model to domain model."""
    return Instrument(
        instrument_id=UUID(db.instrument_id),
        symbol=db.symbol,
        display_name=db.display_name,
        created_at=db.created_at,
        updated_at=db.updated_at,
        is_active=db.is_active,
        metadata=db.metadata_json,
    )
