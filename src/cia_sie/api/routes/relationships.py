"""
CIA-SIE Relationships API Routes
================================

Endpoints for exposing signal relationships.

GOVERNED BY: Section 13.3 (Relationship Exposer)

CRITICAL:
- Returns ALL charts (none hidden)
- Returns ALL contradictions (none resolved)
- Returns ALL confirmations (none weighted)
- NO aggregation anywhere
- NO scores anywhere
- NO recommendations anywhere
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.models import RelationshipSummary
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.repositories import ChartRepository, SignalRepository, SiloRepository
from cia_sie.exposure.relationship_exposer import RelationshipExposer

router = APIRouter()


async def get_exposer(
    session: AsyncSession = Depends(get_session_dependency),
) -> RelationshipExposer:
    """
    Dependency to get relationship exposer.

    Args:
        session: Database session from dependency injection

    Returns:
        RelationshipExposer instance configured with repositories
    """
    return RelationshipExposer(
        silo_repository=SiloRepository(session),
        chart_repository=ChartRepository(session),
        signal_repository=SignalRepository(session),
    )


@router.get("/silo/{silo_id}", response_model=RelationshipSummary)
async def get_silo_relationships(
    silo_id: str,
    exposer: RelationshipExposer = Depends(get_exposer),
):
    """
    Get complete relationship summary for a silo.

    Returns:
    - All charts with their current signals
    - All detected contradictions (EXPOSED, not resolved)
    - All detected confirmations (not weighted)
    - Freshness status for each chart

    This endpoint does NOT:
    - Hide any signals or charts
    - Resolve or prioritize contradictions
    - Weight or rank confirmations
    - Aggregate to a single score
    - Provide recommendations
    """
    try:
        summary = await exposer.expose_for_silo(silo_id)
        return summary
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/instrument/{instrument_id}", response_model=list[RelationshipSummary])
async def get_instrument_relationships(
    instrument_id: str,
    exposer: RelationshipExposer = Depends(get_exposer),
):
    """
    Get relationship summaries for all silos of an instrument.

    Returns a list of RelationshipSummary, one per silo.
    """
    summaries = await exposer.expose_for_instrument(instrument_id)
    if not summaries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No silos found for the instrument with ID '{instrument_id}'. Please check the instrument ID and try again.",
        )
    return summaries


@router.get("/contradictions/silo/{silo_id}")
async def get_silo_contradictions(
    silo_id: str,
    exposer: RelationshipExposer = Depends(get_exposer),
):
    """
    Get only the contradictions for a silo.

    Convenience endpoint for quickly checking conflicts.

    NOTE: These contradictions are presented for user review.
    The system does NOT suggest which signal is correct.
    """
    try:
        summary = await exposer.expose_for_silo(silo_id)
        return {
            "silo_id": str(summary.silo_id),
            "silo_name": summary.silo_name,
            "contradiction_count": len(summary.contradictions),
            "contradictions": [
                {
                    "chart_a": {
                        "id": str(c.chart_a_id),
                        "name": c.chart_a_name,
                        "direction": c.chart_a_direction.value
                        if hasattr(c.chart_a_direction, "value")
                        else c.chart_a_direction,
                    },
                    "chart_b": {
                        "id": str(c.chart_b_id),
                        "name": c.chart_b_name,
                        "direction": c.chart_b_direction.value
                        if hasattr(c.chart_b_direction, "value")
                        else c.chart_b_direction,
                    },
                    "detected_at": c.detected_at.isoformat(),
                }
                for c in summary.contradictions
            ],
            "note": "These conflicting signals are presented for your review. "
            "The system does not determine which signal is correct.",
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
