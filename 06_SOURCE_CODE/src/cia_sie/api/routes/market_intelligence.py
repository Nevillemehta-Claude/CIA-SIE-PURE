"""
CIA-SIE Market Intelligence API Routes
=======================================

API endpoints for natural language market intelligence queries.

This endpoint combines:
- Kite API market data (quotes, historical, instruments)
- CIA-SIE signal data (TradingView chart signals)
- Claude's reasoning and synthesis

All responses are DESCRIPTIVE only, per constitutional rules.

GOVERNED BY: Constitutional Rules (CR-001, CR-002, CR-003)
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from anthropic import AsyncAnthropic

from cia_sie.ai.market_intelligence_agent import AgentResponse, MarketIntelligenceAgent
from cia_sie.ai.usage_tracker import UsageTracker
from cia_sie.core.config import get_settings
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.repositories import (
    ChartRepository,
    InstrumentRepository,
    SignalRepository,
    SiloRepository,
)
from cia_sie.exposure.relationship_exposer import RelationshipExposer
from cia_sie.platforms.kite_intelligence import KiteIntelligenceEngine
from cia_sie.platforms.registry import get_adapter

router = APIRouter()


class MarketQueryRequest(BaseModel):
    """Request for market intelligence query."""
    query: str = Field(..., min_length=1, max_length=2000)
    user_context: Optional[dict] = None


class ExecutionLogResponse(BaseModel):
    """Execution log entry in response."""
    tool: str
    input_summary: str
    execution_time_ms: int
    timestamp: str


class MarketQueryResponse(BaseModel):
    """Response from market intelligence query."""
    response: str
    tools_used: list[str]
    execution_log: list[ExecutionLogResponse]
    data_sources: list[str]
    disclaimer: str
    query_time_ms: int


@router.post("/query", response_model=MarketQueryResponse)
async def query_market_intelligence(
    request: MarketQueryRequest,
    session: AsyncSession = Depends(get_session_dependency),
):
    """
    Execute a natural language market intelligence query.
    
    This endpoint combines:
    - Kite API market data (quotes, historical, instruments)
    - CIA-SIE signal data (TradingView chart signals)
    - Claude's reasoning and synthesis
    
    All responses are DESCRIPTIVE only, per constitutional rules.
    
    Example queries:
    - "What are the top 5 gainers in Nifty 50 today?"
    - "Show me unusual volume in banking stocks"
    - "Compare HDFC vs ICICI over the last month"
    - "What are my charts showing for RELIANCE?"
    """
    start_time = datetime.now()
    
    settings = get_settings()
    
    # Check budget
    tracker = UsageTracker(session)
    budget_status = await tracker.check_budget()
    if not budget_status["within_budget"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI budget exhausted. Market intelligence is temporarily disabled."
        )
    
    # Initialize components
    try:
        kite_adapter = get_adapter("Kite")
        if not kite_adapter.is_connected:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Kite connection not available. Please connect to Zerodha first."
            )
        
        kite_engine = KiteIntelligenceEngine(kite_adapter)
        
        anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        
        exposer = RelationshipExposer(
            silo_repository=SiloRepository(session),
            chart_repository=ChartRepository(session),
            signal_repository=SignalRepository(session),
        )
        
        instrument_repo = InstrumentRepository(session)
        
        agent = MarketIntelligenceAgent(
            anthropic_client=anthropic_client,
            kite_engine=kite_engine,
            relationship_exposer=exposer,
            instrument_repository=instrument_repo,
            model=settings.anthropic_model
        )
        
        result = await agent.query(
            user_message=request.query,
            user_context=request.user_context
        )
        
        # Record usage (estimate tokens)
        input_tokens = len(request.query.split()) * 4
        output_tokens = len(result.response.split()) * 4
        await tracker.record_usage(settings.anthropic_model, input_tokens, output_tokens)
        
        query_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return MarketQueryResponse(
            response=result.response,
            tools_used=result.tools_used,
            execution_log=[
                ExecutionLogResponse(
                    tool=log.tool_name,
                    input_summary=str(log.tool_input)[:200],
                    execution_time_ms=log.execution_time_ms,
                    timestamp=log.timestamp
                )
                for log in result.execution_log
            ],
            data_sources=result.data_sources,
            disclaimer=result.disclaimer,
            query_time_ms=query_time_ms
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Market intelligence query failed: {str(e)}"
        )
