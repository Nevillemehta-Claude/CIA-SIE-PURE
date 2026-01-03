"""
CIA-SIE Silos API Routes
========================

CRUD operations for Silo entities.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.exceptions import DuplicateError
from cia_sie.core.models import Silo, SiloCreate
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.models import SiloDB
from cia_sie.dal.repositories import SiloRepository

router = APIRouter()


def get_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> SiloRepository:
    """
    Dependency to get repository with session.

    Args:
        session: Database session from dependency injection

    Returns:
        SiloRepository instance configured with the session
    """
    return SiloRepository(session)


@router.get("/", response_model=list[Silo])
async def list_silos(
    instrument_id: Optional[str] = None,
    active_only: bool = True,
    repo: SiloRepository = Depends(get_repository),
):
    """
    List silos, optionally filtered by instrument.
    """
    if instrument_id:
        silos = await repo.get_by_instrument(instrument_id, active_only=active_only)
    else:
        silos = await repo.get_all(active_only=active_only)
    return [_db_to_model(s) for s in silos]


@router.post("/", response_model=Silo, status_code=status.HTTP_201_CREATED)
async def create_silo(
    data: SiloCreate,
    repo: SiloRepository = Depends(get_repository),
):
    """
    Create a new silo.
    """
    try:
        silo_db = SiloDB(
            instrument_id=str(data.instrument_id),
            silo_name=data.silo_name,
            heartbeat_enabled=data.heartbeat_enabled,
            heartbeat_frequency_min=data.heartbeat_frequency_min,
            current_threshold_min=data.current_threshold_min,
            recent_threshold_min=data.recent_threshold_min,
            stale_threshold_min=data.stale_threshold_min,
        )
        created = await repo.create(silo_db)
        return _db_to_model(created)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot create silo: {e.message}. A silo with this name may already exist for this instrument.",
        )


@router.get("/{silo_id}", response_model=Silo)
async def get_silo(
    silo_id: str,
    repo: SiloRepository = Depends(get_repository),
):
    """
    Get a specific silo by ID.
    """
    silo = await repo.get_by_id(silo_id)
    if not silo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The silo with ID '{silo_id}' was not found. It may have been deleted or never existed.",
        )
    return _db_to_model(silo)


@router.delete("/{silo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_silo(
    silo_id: str,
    repo: SiloRepository = Depends(get_repository),
):
    """
    Soft delete a silo.
    """
    deleted = await repo.delete(silo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot delete silo: The silo with ID '{silo_id}' was not found.",
        )


def _db_to_model(db: SiloDB) -> Silo:
    """Convert database model to domain model."""
    return Silo(
        silo_id=UUID(db.silo_id),
        instrument_id=UUID(db.instrument_id),
        silo_name=db.silo_name,
        heartbeat_enabled=db.heartbeat_enabled,
        heartbeat_frequency_min=db.heartbeat_frequency_min,
        current_threshold_min=db.current_threshold_min,
        recent_threshold_min=db.recent_threshold_min,
        stale_threshold_min=db.stale_threshold_min,
        created_at=db.created_at,
        updated_at=db.updated_at,
        is_active=db.is_active,
    )
