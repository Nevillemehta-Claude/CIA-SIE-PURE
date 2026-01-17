"""
CIA-SIE Per-Instrument Chat Routes
==================================

Endpoints for conversational AI interaction about specific instruments.

GOVERNED BY: Section 14 (AI Narrative Engine)

CRITICAL:
- All responses are DESCRIPTIVE only
- NO recommendations, predictions, or trading advice
- Every response includes mandatory disclaimer
- Response validation enforced before returning to user
"""

import logging
from datetime import UTC, datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.ai.claude_client import ClaudeClient
from cia_sie.ai.model_registry import estimate_cost, get_default_model, get_model_info
from cia_sie.ai.response_validator import ensure_disclaimer, validate_ai_response
from cia_sie.ai.usage_tracker import UsageTracker
from cia_sie.core.enums import MessageRole
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.models import ConversationDB
from cia_sie.dal.repositories import (
    ChartRepository,
    InstrumentRepository,
    SignalRepository,
    SiloRepository,
)
from cia_sie.exposure.relationship_exposer import RelationshipExposer

logger = logging.getLogger(__name__)

router = APIRouter()

# Mandatory disclaimer for all AI responses
MANDATORY_DISCLAIMER = (
    "This is a description of what your charts are showing. "
    "The interpretation and any decision is entirely yours."
)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Request to send a chat message."""

    message: str = Field(..., min_length=1, max_length=2000)
    model: Optional[str] = None
    include_context: bool = True
    conversation_id: Optional[str] = None


class UsageInfo(BaseModel):
    """Token and cost usage info."""

    input_tokens: int
    output_tokens: int
    cost: float
    model_used: str


class ContextInfo(BaseModel):
    """Context included in response."""

    signals_included: int
    charts_referenced: list[str]


class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    conversation_id: str
    message: ChatMessage
    context_used: Optional[ContextInfo] = None
    usage: UsageInfo
    disclaimer: str = MANDATORY_DISCLAIMER


class ConversationSummary(BaseModel):
    """Summary of a conversation."""

    conversation_id: str
    messages: list[ChatMessage]
    created_at: str
    total_tokens: int
    total_cost: float


class ChatHistoryResponse(BaseModel):
    """Response for chat history."""

    scrip_id: str
    conversations: list[ConversationSummary]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


async def get_instrument_context(
    instrument_id: str,
    session: AsyncSession,
) -> tuple[str, list[str], int]:
    """
    Build context about an instrument's current signals.

    Returns:
        Tuple of (context_string, chart_codes, signal_count)
    """
    exposer = RelationshipExposer(
        silo_repository=SiloRepository(session),
        chart_repository=ChartRepository(session),
        signal_repository=SignalRepository(session),
    )

    # Get all silos for this instrument
    silo_repo = SiloRepository(session)
    silos = await silo_repo.get_by_instrument(instrument_id)

    if not silos:
        return "No silos configured for this instrument.", [], 0

    context_parts = []
    chart_codes = []
    signal_count = 0

    for silo in silos:
        try:
            summary = await exposer.expose_for_silo(str(silo.silo_id))

            context_parts.append(f"Silo: {silo.silo_name}")

            for chart in summary.get("charts", []):
                chart_code = chart.get("chart_code", "Unknown")
                chart_codes.append(chart_code)

                if chart.get("latest_signal"):
                    signal = chart["latest_signal"]
                    direction = signal.get("direction", "NEUTRAL")
                    freshness = chart.get("freshness", "UNAVAILABLE")
                    context_parts.append(
                        f"  Chart {chart_code}: {direction} (Freshness: {freshness})"
                    )
                    signal_count += 1
                else:
                    context_parts.append(f"  Chart {chart_code}: No signal")

            # Include contradictions
            for c in summary.get("contradictions", []):
                context_parts.append(
                    f"  CONTRADICTION: {c['chart_a_name']} ({c['chart_a_direction']}) "
                    f"vs {c['chart_b_name']} ({c['chart_b_direction']})"
                )

        except Exception as e:
            logger.warning(f"Error getting silo context: {e}")
            continue

    context = "\n".join(context_parts) if context_parts else "No signal data available."
    return context, chart_codes, signal_count


def build_system_prompt(include_context: bool, context: str) -> str:
    """Build the system prompt for chat."""
    base_prompt = """You are a descriptive assistant for CIA-SIE (Chart Intelligence Auditor & Signal Intelligence Engine).

CRITICAL RULES - YOU MUST FOLLOW THESE:
1. You ONLY describe what the charts are showing. You NEVER make recommendations.
2. You NEVER use words like "should", "recommend", "suggest", "consider buying/selling".
3. You NEVER predict price movements or provide probability assessments.
4. You NEVER assign confidence scores or signal strength ratings.
5. You NEVER resolve contradictions - you describe both sides equally.
6. Every response MUST end with: "This is a description of what your charts are showing. The interpretation and any decision is entirely yours."

You are a DATA REPORTER, not an ADVISOR. Describe facts, not opinions."""

    if include_context and context:
        return f"""{base_prompt}

CURRENT SIGNAL CONTEXT:
{context}

Use this context to answer questions about current signals. Always describe the data factually without recommendations."""

    return base_prompt


# =============================================================================
# ROUTES
# =============================================================================


@router.post("/{scrip_id}", response_model=ChatResponse)
async def send_chat_message(
    scrip_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session_dependency),
):
    """
    Send a chat message about a specific instrument.

    The AI will describe current signals and answer questions
    in a DESCRIPTIVE manner only. No recommendations.

    Args:
        scrip_id: Instrument ID
        request: Chat message and options

    Returns:
        AI response with usage info and mandatory disclaimer
    """
    # Verify instrument exists
    instrument_repo = InstrumentRepository(session)
    instrument = await instrument_repo.get_by_id(scrip_id)
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instrument not found: {scrip_id}",
        )

    # Check budget
    tracker = UsageTracker(session)
    budget_status = await tracker.check_budget()
    if not budget_status["within_budget"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI budget exhausted. AI features are temporarily disabled.",
        )

    # Select model
    model_id = request.model
    if not model_id:
        model_info = get_default_model()
        model_id = model_info.id
    else:
        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown model: {model_id}",
            )

    # Build context if requested
    context = ""
    chart_codes = []
    signal_count = 0
    if request.include_context:
        context, chart_codes, signal_count = await get_instrument_context(scrip_id, session)

    # Build prompts
    system_prompt = build_system_prompt(request.include_context, context)

    # Get or create conversation
    conversation_id = request.conversation_id or str(uuid4())
    conversation = await _get_or_create_conversation(session, conversation_id, scrip_id, model_id)

    # Generate response
    client = ClaudeClient(model=model_id)
    try:
        response_text = await client.generate(
            system_prompt=system_prompt,
            user_prompt=request.message,
            max_tokens=1500,
            temperature=0.3,
        )
    except Exception as e:
        logger.error(f"AI generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable.",
        )

    # Validate response
    validation = validate_ai_response(response_text)
    if not validation.is_valid:
        logger.warning(f"AI response validation failed: {validation.violations}")
        # Remediate by ensuring disclaimer
        response_text = ensure_disclaimer(response_text)

    # Estimate tokens (rough approximation)
    input_tokens = len(system_prompt.split()) + len(request.message.split())
    output_tokens = len(response_text.split())

    # Calculate cost
    cost = estimate_cost(model_id, input_tokens * 4, output_tokens * 4)  # ~4 chars/token

    # Record usage
    await tracker.record_usage(model_id, input_tokens * 4, output_tokens * 4)

    # Update conversation
    now = datetime.now(UTC)
    messages = conversation.messages if isinstance(conversation.messages, list) else []

    messages.append(
        {
            "role": MessageRole.USER.value,
            "content": request.message,
            "timestamp": now.isoformat(),
        }
    )
    messages.append(
        {
            "role": MessageRole.ASSISTANT.value,
            "content": response_text,
            "timestamp": now.isoformat(),
        }
    )

    conversation.messages = messages
    conversation.total_tokens += (input_tokens + output_tokens) * 4
    conversation.total_cost = float(conversation.total_cost) + cost

    await session.flush()

    return ChatResponse(
        conversation_id=conversation_id,
        message=ChatMessage(
            role=MessageRole.ASSISTANT.value,
            content=response_text,
            timestamp=now.isoformat(),
        ),
        context_used=ContextInfo(
            signals_included=signal_count,
            charts_referenced=chart_codes,
        )
        if request.include_context
        else None,
        usage=UsageInfo(
            input_tokens=input_tokens * 4,
            output_tokens=output_tokens * 4,
            cost=cost,
            model_used=model_id,
        ),
        disclaimer=MANDATORY_DISCLAIMER,
    )


@router.get("/{scrip_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    scrip_id: str,
    limit: int = 50,
    session: AsyncSession = Depends(get_session_dependency),
):
    """
    Get conversation history for an instrument.

    Args:
        scrip_id: Instrument ID
        limit: Maximum conversations to return

    Returns:
        List of conversations with messages
    """
    # Verify instrument exists
    instrument_repo = InstrumentRepository(session)
    instrument = await instrument_repo.get_by_id(scrip_id)
    if not instrument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instrument not found: {scrip_id}",
        )

    # Get conversations
    stmt = (
        select(ConversationDB)
        .where(ConversationDB.instrument_id == scrip_id)
        .order_by(ConversationDB.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    conversations = result.scalars().all()

    return ChatHistoryResponse(
        scrip_id=scrip_id,
        conversations=[
            ConversationSummary(
                conversation_id=c.conversation_id,
                messages=[
                    ChatMessage(
                        role=m.get("role", "user"),
                        content=m.get("content", ""),
                        timestamp=m.get("timestamp"),
                    )
                    for m in (c.messages if isinstance(c.messages, list) else [])
                ],
                created_at=c.created_at.isoformat() if c.created_at else "",
                total_tokens=c.total_tokens or 0,
                total_cost=float(c.total_cost) if c.total_cost else 0,
            )
            for c in conversations
        ],
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


async def _get_or_create_conversation(
    session: AsyncSession,
    conversation_id: str,
    instrument_id: str,
    model_id: str,
) -> ConversationDB:
    """Get or create a conversation record."""
    stmt = select(ConversationDB).where(ConversationDB.conversation_id == conversation_id)
    result = await session.execute(stmt)
    conversation = result.scalar_one_or_none()

    if not conversation:
        conversation = ConversationDB(
            conversation_id=conversation_id,
            instrument_id=instrument_id,
            messages=[],
            model_used=model_id,
            total_tokens=0,
            total_cost=0,
        )
        session.add(conversation)
        await session.flush()

    return conversation
