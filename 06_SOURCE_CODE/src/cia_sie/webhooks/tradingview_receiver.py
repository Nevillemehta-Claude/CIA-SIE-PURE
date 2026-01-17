"""
TradingView Webhook Receiver for CIA-SIE

This module handles incoming webhook alerts from TradingView Pine Scripts
and routes them to the appropriate data handlers (Excel, Database, etc.)

Version: 2.0.0
Chart Support:
  - GOLD_01A (GOLDBEES Daily PRIMARY_SIGNAL)
  - GOLD_01A (GOLDBEES Daily MOMENTUM_HEALTH)
  - GOLD_02 (GOLDBEES Weekly HTF_STRUCTURE)
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, Field, validator

# Configure logging
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS FOR WEBHOOK PAYLOADS
# ═══════════════════════════════════════════════════════════════════════════════

class PriceData(BaseModel):
    """OHLC price data"""
    open: float
    high: float
    low: float
    close: float


class EMAData(BaseModel):
    """Exponential Moving Average data"""
    ema20: float
    ema50: float
    ema200: float


class Week52Data(BaseModel):
    """52-week high/low data"""
    high: float
    low: float


class SignalData(BaseModel):
    """Primary signal data"""
    direction: str = Field(..., pattern="^(BULLISH|BEARISH|NEUTRAL)$")
    direction_score: int = Field(..., ge=-4, le=4)
    macro_state: str = Field(..., pattern="^(PASS|FAIL|UNCLEAR)$")
    trend: str = Field(..., pattern="^(UPTREND|DOWNTREND|RANGE)$")
    ema_stack: str = Field(..., pattern="^(BULLISH_STACK|BEARISH_STACK|MIXED)$")
    strength: str = Field(..., pattern="^(STRONG|MODERATE|WEAK)$")
    strength_score: int = Field(..., ge=0, le=5)


class RiskData(BaseModel):
    """Risk management data"""
    invalidation: float
    risk_pct: float


class ExternalData(BaseModel):
    """External market data (DXY, VIX)"""
    dxy_close: float = 0.0
    vix_close: float = 0.0


class StateChangeData(BaseModel):
    """State change tracking"""
    changed: bool
    changes: str = ""


class MomentumData(BaseModel):
    """Momentum health data"""
    health: str = Field(..., pattern="^(HEALTHY|WARNING|EXHAUSTED)$")
    health_score: int = Field(..., ge=0, le=100)
    health_changed: bool = False


class RSIData(BaseModel):
    """RSI indicator data"""
    value: float
    ma: float
    zone: str = Field(..., pattern="^(EXTREME_OB|OVERBOUGHT|NEUTRAL|OVERSOLD|EXTREME_OS)$")


class MACDData(BaseModel):
    """MACD indicator data"""
    line: float
    signal: float
    histogram: float
    status: str = Field(..., pattern="^(BULLISH|BEARISH)$")
    cross: str = "NONE"


class DivergenceData(BaseModel):
    """Divergence detection data"""
    status: str = Field(..., pattern="^(BEARISH|BULLISH|NONE)$")
    bearish_active: bool = False
    bullish_active: bool = False


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WEBHOOK PAYLOAD MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class PrimarySignalPayload(BaseModel):
    """
    Full payload from PRIMARY_SIGNAL indicator
    """
    chart_id: str
    chart_role: str = "PRIMARY_SIGNAL"
    instrument: str
    timeframe: str
    schema_version: str = "2.0.0"
    timestamp: int
    bar_time: str
    price: PriceData
    ema: EMAData
    week52: Week52Data
    signals: SignalData
    risk: RiskData
    external: ExternalData
    state_change: StateChangeData
    alert_type: str

    @validator('chart_id')
    def validate_chart_id(cls, v):
        if not v.startswith('GOLD_'):
            logger.warning(f"Non-standard chart_id received: {v}")
        return v


class MomentumHealthPayload(BaseModel):
    """
    Full payload from MOMENTUM_HEALTH indicator
    """
    chart_id: str
    chart_role: str = "MOMENTUM_HEALTH"
    instrument: str
    timeframe: str
    schema_version: str = "2.0.0"
    timestamp: int
    bar_time: str
    close: float
    momentum: MomentumData
    rsi: RSIData
    macd: MACDData
    divergence: DivergenceData
    alert_type: str


class SimpleEventPayload(BaseModel):
    """
    Simplified event payload for specific alerts
    """
    chart_id: str
    event: str
    close: Optional[float] = None
    health: Optional[str] = None
    health_score: Optional[int] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    cross_type: Optional[str] = None
    divergence_type: Optional[str] = None
    reason: Optional[str] = None
    timestamp: Optional[int] = None


class HTFStructurePayload(BaseModel):
    """
    Full payload from HTF_STRUCTURE indicator (Chart 02 - Weekly)
    """
    chart_id: str
    timestamp: str  # Unix timestamp as string
    close: float
    htf_bias: str = Field(..., pattern="^(STRONGLY_BULLISH|BULLISH|NEUTRAL|BEARISH|STRONGLY_BEARISH)$")
    htf_trend: str = Field(..., pattern="^(BULLISH|BEARISH|MIXED)$")
    sma_alignment: str = Field(..., pattern="^(BULLISH_STACK|BEARISH_STACK|MIXED)$")
    swing_structure: str = Field(..., pattern="^(HH_HL|LH_LL|EXPANSION|CONTRACTION)$")
    range_position: str = Field(..., pattern="^(UPPER|MIDDLE|LOWER)$")
    htf_score: int = Field(..., ge=-5, le=5)
    position_pct: float = Field(..., ge=0, le=100)
    sma50: float
    sma100: float
    sma200: float
    ema20: float
    high_52w: float
    low_52w: float
    state_changed: bool

    @validator('chart_id')
    def validate_chart_id(cls, v):
        if not v.startswith('GOLD_02'):
            logger.warning(f"HTF_STRUCTURE payload with non-standard chart_id: {v}")
        return v


# ═══════════════════════════════════════════════════════════════════════════════
# WEBHOOK ROUTER
# ═══════════════════════════════════════════════════════════════════════════════

router = APIRouter(prefix="/webhook", tags=["TradingView Webhooks"])


class WebhookResponse(BaseModel):
    """Standard webhook response"""
    success: bool
    message: str
    chart_id: Optional[str] = None
    event_type: Optional[str] = None
    processed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# In-memory storage for recent alerts (for debugging/monitoring)
recent_alerts: list = []
MAX_RECENT_ALERTS = 100


def store_alert(payload: Dict[str, Any], alert_type: str) -> None:
    """Store alert in memory for debugging"""
    global recent_alerts
    recent_alerts.insert(0, {
        "received_at": datetime.utcnow().isoformat(),
        "alert_type": alert_type,
        "payload": payload
    })
    if len(recent_alerts) > MAX_RECENT_ALERTS:
        recent_alerts = recent_alerts[:MAX_RECENT_ALERTS]


async def write_to_excel(payload: Dict[str, Any], chart_id: str) -> None:
    """
    Background task to write payload data to Excel
    This will be implemented with openpyxl or xlsxwriter
    """
    # TODO: Implement Excel writing logic
    logger.info(f"Writing to Excel for chart: {chart_id}")
    
    # Excel file path pattern: INSTRUMENT_CHARTID.xlsx
    # Each row = one data point with timestamp
    pass


async def write_to_database(payload: Dict[str, Any], chart_id: str) -> None:
    """
    Background task to write payload data to SQLite database
    """
    # TODO: Implement database writing logic
    logger.info(f"Writing to database for chart: {chart_id}")
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# WEBHOOK ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/tradingview", response_model=WebhookResponse)
async def receive_tradingview_alert(
    request: Request,
    background_tasks: BackgroundTasks
) -> WebhookResponse:
    """
    Main endpoint for all TradingView webhook alerts.
    
    Accepts JSON payloads from Pine Script alerts and routes them
    based on chart_id and alert_type.
    
    Example curl test:
    ```
    curl -X POST http://localhost:8000/webhook/tradingview \
      -H "Content-Type: application/json" \
      -d '{"chart_id":"GOLD_01A","event":"TEST","close":116.76}'
    ```
    """
    try:
        # Parse raw body
        body = await request.body()
        body_text = body.decode('utf-8')
        
        # Handle empty body
        if not body_text.strip():
            raise HTTPException(status_code=400, detail="Empty request body")
        
        # Parse JSON
        try:
            payload = json.loads(body_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}, body: {body_text[:200]}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
        
        # Extract chart_id for routing
        chart_id = payload.get("chart_id", "UNKNOWN")
        alert_type = payload.get("alert_type", payload.get("event", "UNKNOWN"))
        
        logger.info(f"Received alert: chart={chart_id}, type={alert_type}")
        
        # Store for debugging
        store_alert(payload, alert_type)
        
        # Route based on alert type
        if alert_type == "STATE_CHANGE":
            # Full PRIMARY_SIGNAL state change
            try:
                validated = PrimarySignalPayload(**payload)
                background_tasks.add_task(write_to_excel, payload, chart_id)
                background_tasks.add_task(write_to_database, payload, chart_id)
            except Exception as e:
                logger.warning(f"Payload validation warning: {e}")
                # Still process even if validation fails
        
        elif alert_type == "MOMENTUM_UPDATE":
            # Full MOMENTUM_HEALTH update
            try:
                validated = MomentumHealthPayload(**payload)
                background_tasks.add_task(write_to_excel, payload, chart_id)
            except Exception as e:
                logger.warning(f"Payload validation warning: {e}")
        
        elif alert_type in ["BAR_CLOSE", "HEALTH_CHANGE", "MACD_BULL_CROSS", 
                           "MACD_BEAR_CROSS", "BEARISH_DIVERGENCE", "BULLISH_DIVERGENCE"]:
            # Simplified event payloads
            background_tasks.add_task(write_to_excel, payload, chart_id)
        
        elif chart_id.startswith("GOLD_02") or "HTF_STRUCTURE" in chart_id:
            # HTF_STRUCTURE payload (Weekly Chart 02)
            try:
                validated = HTFStructurePayload(**payload)
                logger.info(f"HTF_STRUCTURE validated: bias={validated.htf_bias}, score={validated.htf_score}")
                background_tasks.add_task(write_to_excel, payload, chart_id)
                background_tasks.add_task(write_to_database, payload, chart_id)
            except Exception as e:
                logger.warning(f"HTF_STRUCTURE validation warning: {e}")
                # Still process even if validation fails
                background_tasks.add_task(write_to_excel, payload, chart_id)
        
        else:
            # Unknown alert type - still accept and log
            logger.warning(f"Unknown alert_type: {alert_type}")
        
        return WebhookResponse(
            success=True,
            message=f"Alert processed: {alert_type}",
            chart_id=chart_id,
            event_type=alert_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tradingview/{chart_id}", response_model=WebhookResponse)
async def receive_chart_specific_alert(
    chart_id: str,
    request: Request,
    background_tasks: BackgroundTasks
) -> WebhookResponse:
    """
    Chart-specific endpoint for cleaner routing.
    
    Example: POST /webhook/tradingview/GOLD_01A
    """
    try:
        body = await request.body()
        body_text = body.decode('utf-8')
        
        if not body_text.strip():
            raise HTTPException(status_code=400, detail="Empty request body")
        
        payload = json.loads(body_text)
        
        # Inject chart_id from URL if not in payload
        if "chart_id" not in payload:
            payload["chart_id"] = chart_id
        
        alert_type = payload.get("alert_type", payload.get("event", "UNKNOWN"))
        
        logger.info(f"Chart-specific alert: chart={chart_id}, type={alert_type}")
        store_alert(payload, alert_type)
        
        background_tasks.add_task(write_to_excel, payload, chart_id)
        background_tasks.add_task(write_to_database, payload, chart_id)
        
        return WebhookResponse(
            success=True,
            message=f"Chart {chart_id} alert processed",
            chart_id=chart_id,
            event_type=alert_type
        )
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        logger.exception(f"Error processing chart-specific webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent", response_model=Dict[str, Any])
async def get_recent_alerts(limit: int = 10) -> Dict[str, Any]:
    """
    Get recent alerts for debugging/monitoring.
    
    Example: GET /webhook/recent?limit=5
    """
    return {
        "count": len(recent_alerts[:limit]),
        "alerts": recent_alerts[:limit]
    }


@router.get("/health")
async def webhook_health() -> Dict[str, Any]:
    """
    Health check for webhook receiver.
    """
    return {
        "status": "healthy",
        "service": "tradingview_webhook_receiver",
        "version": "2.0.0",
        "supported_charts": [
            "GOLD_01A_DAILY_PRIMARY_SIGNAL",
            "GOLD_01A_MOMENTUM",
            "GOLD_02_WEEKLY_HTF_STRUCTURE"
        ],
        "total_alerts_received": len(recent_alerts),
        "last_alert_at": recent_alerts[0]["received_at"] if recent_alerts else None
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EXCEL WRITER UTILITY
# ═══════════════════════════════════════════════════════════════════════════════

class ExcelDataWriter:
    """
    Handles writing TradingView data to Excel files.
    One file per instrument, one sheet per chart/timeframe.
    """
    
    def __init__(self, output_dir: str = "data/tradingview"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_filepath(self, instrument: str) -> Path:
        """Get Excel file path for instrument"""
        return self.output_dir / f"{instrument}_charts.xlsx"
    
    def append_primary_signal(self, payload: Dict[str, Any]) -> None:
        """Append PRIMARY_SIGNAL data to Excel"""
        # Implementation with openpyxl
        # Will create sheet "PRIMARY_SIGNAL_D" for daily timeframe
        pass
    
    def append_momentum_health(self, payload: Dict[str, Any]) -> None:
        """Append MOMENTUM_HEALTH data to Excel"""
        # Implementation with openpyxl
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def init_webhook_receiver():
    """Initialize webhook receiver module"""
    logger.info("TradingView Webhook Receiver initialized")
    logger.info(f"Endpoints: /webhook/tradingview, /webhook/tradingview/{{chart_id}}")
    return router
