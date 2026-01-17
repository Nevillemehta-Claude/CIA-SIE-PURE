"""
CIA-SIE Narratives API Routes
=============================

Endpoints for AI-generated DESCRIPTIVE narratives.

GOVERNED BY: Section 14 (AI Narrative Engine)

CRITICAL:
- All narratives are DESCRIPTIVE only
- NO recommendations
- NO direction inference
- NO confidence scores
- Every narrative reminds user they retain decision authority
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.ai.claude_client import ClaudeClient
from cia_sie.ai.narrative_generator import NarrativeGenerator
from cia_sie.core.exceptions import AIProviderError
from cia_sie.core.models import Narrative
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.repositories import ChartRepository, SignalRepository, SiloRepository
from cia_sie.exposure.relationship_exposer import RelationshipExposer

logger = logging.getLogger(__name__)

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


def get_narrative_generator() -> NarrativeGenerator:
    """
    Dependency to get narrative generator.

    Returns:
        NarrativeGenerator instance configured with Claude client
    """
    return NarrativeGenerator(claude_client=ClaudeClient())


@router.get("/silo/{silo_id}", response_model=Narrative)
async def generate_silo_narrative(
    silo_id: str,
    use_ai: bool = True,
    exposer: RelationshipExposer = Depends(get_exposer),
    generator: NarrativeGenerator = Depends(get_narrative_generator),
):
    """
    Generate a DESCRIPTIVE narrative for a silo.

    The narrative describes what the signals are showing.
    It does NOT provide recommendations or resolve contradictions.

    Args:
        silo_id: The silo to describe
        use_ai: If True, use Claude for enhanced narrative. If False, use fallback.

    Returns:
        Narrative with sections and closing statement

    IMPORTANT: This endpoint generates DESCRIPTIVE content only.
    The closing statement always reminds the user that interpretation is theirs.
    """
    try:
        # Get relationship summary
        summary = await exposer.expose_for_silo(silo_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    try:
        if use_ai:
            # Generate AI-powered narrative
            narrative = await generator.generate_silo_narrative(summary)
        else:
            # Use fallback (no AI)
            narrative = generator.generate_fallback_narrative(summary)

        return narrative

    except AIProviderError as e:
        logger.warning(f"AI provider error, using fallback: {e}")
        # Fall back to non-AI narrative
        narrative = generator.generate_fallback_narrative(summary)
        return narrative


@router.get("/silo/{silo_id}/plain")
async def get_plain_text_narrative(
    silo_id: str,
    use_ai: bool = True,
    exposer: RelationshipExposer = Depends(get_exposer),
    generator: NarrativeGenerator = Depends(get_narrative_generator),
):
    """
    Get narrative as plain text (for simple display).

    Returns the narrative content as a single string.
    """
    try:
        summary = await exposer.expose_for_silo(silo_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    try:
        if use_ai:
            narrative = await generator.generate_silo_narrative(summary)
        else:
            narrative = generator.generate_fallback_narrative(summary)

        # Combine all sections into plain text
        sections_text = "\n\n".join(section.content for section in narrative.sections)

        return {
            "silo_id": str(narrative.silo_id),
            "narrative": sections_text,
            "closing_statement": narrative.closing_statement,
            "generated_at": narrative.generated_at.isoformat(),
        }

    except AIProviderError as e:
        logger.warning(f"AI provider error: {e}")
        narrative = generator.generate_fallback_narrative(summary)

        sections_text = "\n\n".join(section.content for section in narrative.sections)

        return {
            "silo_id": str(narrative.silo_id),
            "narrative": sections_text,
            "closing_statement": narrative.closing_statement,
            "generated_at": narrative.generated_at.isoformat(),
            "note": "Generated using fallback (AI unavailable)",
        }
