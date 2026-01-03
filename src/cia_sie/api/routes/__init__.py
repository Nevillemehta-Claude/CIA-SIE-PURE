"""
CIA-SIE API Routes
==================

All API route definitions organized by resource.
"""

from fastapi import APIRouter

from cia_sie.api.routes.ai import router as ai_router
from cia_sie.api.routes.baskets import router as baskets_router
from cia_sie.api.routes.charts import router as charts_router
from cia_sie.api.routes.chat import router as chat_router
from cia_sie.api.routes.instruments import router as instruments_router
from cia_sie.api.routes.narratives import router as narratives_router
from cia_sie.api.routes.platforms import router as platforms_router
from cia_sie.api.routes.relationships import router as relationships_router
from cia_sie.api.routes.signals import router as signals_router
from cia_sie.api.routes.silos import router as silos_router
from cia_sie.api.routes.strategy import router as strategy_router
from cia_sie.api.routes.webhooks import router as webhooks_router

# Main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(instruments_router, prefix="/instruments", tags=["Instruments"])
api_router.include_router(silos_router, prefix="/silos", tags=["Silos"])
api_router.include_router(charts_router, prefix="/charts", tags=["Charts"])
api_router.include_router(signals_router, prefix="/signals", tags=["Signals"])
api_router.include_router(webhooks_router, prefix="/webhook", tags=["Webhooks"])
api_router.include_router(relationships_router, prefix="/relationships", tags=["Relationships"])
api_router.include_router(narratives_router, prefix="/narratives", tags=["Narratives"])
api_router.include_router(baskets_router, prefix="/baskets", tags=["Analytical Baskets"])
api_router.include_router(platforms_router, prefix="/platforms", tags=["Platform Integration"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI Management"])
api_router.include_router(chat_router, prefix="/chat", tags=["AI Chat"])
api_router.include_router(strategy_router, prefix="/strategy", tags=["Strategy Analysis"])
