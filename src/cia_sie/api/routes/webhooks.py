"""
CIA-SIE Webhook API Routes
==========================

Webhook endpoints for receiving signals from TradingView and other platforms.

GOVERNED BY: Section 13.1 (Webhook Handler)

SECURITY: All webhooks require HMAC signature validation in production.

DOES:
- Validate JSON structure
- Validate webhook signature (HMAC-SHA256)
- Store signal in database
- Return success/failure status

DOES NOT:
- Aggregate signals
- Compute scores
- Make judgments
"""

import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.exceptions import (
    ChartNotFoundError,
    InvalidWebhookPayloadError,
    WebhookNotRegisteredError,
)
from cia_sie.core.security import (
    SecurityEvent,
    WebhookSignatureValidator,
    log_security_event,
    validate_webhook_request,
)
from cia_sie.dal.database import get_session_dependency
from cia_sie.dal.repositories import ChartRepository, SignalRepository
from cia_sie.ingestion.webhook_handler import TradingViewPayloadAdapter, WebhookHandler

logger = logging.getLogger(__name__)

router = APIRouter()


async def get_webhook_handler(
    session: AsyncSession = Depends(get_session_dependency),
) -> WebhookHandler:
    """
    Dependency to get webhook handler.

    Args:
        session: Database session from dependency injection

    Returns:
        WebhookHandler instance configured with repositories
    """
    return WebhookHandler(
        chart_repository=ChartRepository(session),
        signal_repository=SignalRepository(session),
    )


@router.post("/", response_model=dict)
async def receive_webhook(
    request: Request,
    validated_body: bytes = Depends(validate_webhook_request),
    handler: WebhookHandler = Depends(get_webhook_handler),
):
    """
    Receive and process a webhook from TradingView or other platforms.

    ## Authentication

    This endpoint requires HMAC-SHA256 signature validation in production.

    **Required Headers:**
    - `X-Webhook-Signature`: HMAC-SHA256 signature (sha256=...)
    - `X-Webhook-Timestamp`: Unix timestamp (optional but recommended)

    **Signature Computation:**
    ```
    signature = HMAC-SHA256(webhook_secret, timestamp + body)
    ```

    ## Behavior

    This endpoint:
    - Validates the webhook signature
    - Validates the incoming payload
    - Stores the signal in the database
    - Returns success with signal_id

    This endpoint does NOT:
    - Aggregate with other signals
    - Compute scores or recommendations
    - Make any judgments about the signal

    ## Expected Payload Format

    ```json
    {
        "webhook_id": "SAMPLE_01A",
        "direction": "BULLISH",
        "signal_type": "STATE_CHANGE",
        "timestamp": "2025-01-01T00:00:00Z",
        "rsi": 28.5,
        "macd": 0.12
    }
    ```
    """
    received_at = datetime.now(timezone.utc)
    client_ip = WebhookSignatureValidator.get_client_ip(request)

    try:
        # Parse validated JSON body
        payload = json.loads(validated_body)
    except json.JSONDecodeError as e:
        log_security_event(
            SecurityEvent.SUSPICIOUS_REQUEST,
            client_ip,
            {"reason": "Invalid JSON after signature validation", "error": str(e)},
            severity="WARNING",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The webhook payload is not valid JSON. Please check the format and try again. Error: {str(e)}",
        )

    # Log webhook received
    log_security_event(
        SecurityEvent.WEBHOOK_RECEIVED,
        client_ip,
        {"webhook_id": payload.get("webhook_id", "unknown")},
    )

    # Adapt TradingView format if needed
    adapted_payload = TradingViewPayloadAdapter.adapt(payload)

    try:
        # Process the webhook
        signal = await handler.process_webhook(adapted_payload, received_at)

        logger.info(f"Webhook processed: signal_id={signal.signal_id}")

        # Handle direction whether it's enum or string
        direction_val = (
            signal.direction.value if hasattr(signal.direction, "value") else signal.direction
        )

        return {
            "status": "accepted",
            "signal_id": str(signal.signal_id),
            "chart_id": str(signal.chart_id),
            "direction": direction_val,
            "received_at": received_at.isoformat(),
        }

    except InvalidWebhookPayloadError as e:
        logger.warning(f"Invalid webhook payload: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook validation failed: {e.message}",
        )

    except WebhookNotRegisteredError as e:
        logger.warning(f"Unregistered webhook: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The webhook ID is not registered in the system. {e.message}",
        )

    except ChartNotFoundError as e:
        logger.warning(f"Chart not found: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chart not found or inactive. {e.message}",
        )


@router.post("/manual", response_model=dict)
async def receive_manual_trigger(
    request: Request,
    validated_body: bytes = Depends(validate_webhook_request),
    handler: WebhookHandler = Depends(get_webhook_handler),
):
    """
    Receive a manual trigger signal (MTIC).

    Similar to regular webhook but explicitly marked as MANUAL type.

    ## Authentication

    Requires the same HMAC-SHA256 signature as the main webhook endpoint.
    """
    received_at = datetime.now(timezone.utc)
    client_ip = WebhookSignatureValidator.get_client_ip(request)

    try:
        payload = json.loads(validated_body)
    except json.JSONDecodeError as e:
        log_security_event(
            SecurityEvent.SUSPICIOUS_REQUEST,
            client_ip,
            {"reason": "Invalid JSON in manual trigger", "error": str(e)},
            severity="WARNING",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The request payload is not valid JSON. Please check the format and try again. Error: {str(e)}",
        )

    # Force signal_type to MANUAL
    payload["signal_type"] = "MANUAL"

    log_security_event(
        SecurityEvent.WEBHOOK_RECEIVED,
        client_ip,
        {"webhook_id": payload.get("webhook_id", "unknown"), "type": "MANUAL"},
    )

    try:
        signal = await handler.process_webhook(payload, received_at)

        return {
            "status": "accepted",
            "signal_id": str(signal.signal_id),
            "chart_id": str(signal.chart_id),
            "direction": signal.direction.value
            if hasattr(signal.direction, "value")
            else signal.direction,
            "trigger_type": "MANUAL",
            "received_at": received_at.isoformat(),
        }

    except InvalidWebhookPayloadError as e:
        logger.warning(f"Invalid manual trigger payload: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Manual trigger validation failed: {e.message}",
        )
    except WebhookNotRegisteredError as e:
        logger.warning(f"Unregistered webhook in manual trigger: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The webhook ID is not registered in the system. {e.message}",
        )
    except ChartNotFoundError as e:
        logger.warning(f"Chart not found in manual trigger: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chart not found or inactive. {e.message}",
        )


@router.get("/health", response_model=dict)
async def webhook_health():
    """
    Health check for webhook endpoint.

    Returns webhook configuration status (without exposing secrets).
    """
    from cia_sie.core.config import get_settings

    settings = get_settings()

    return {
        "status": "healthy",
        "authentication_enabled": settings.webhook_secret is not None,
        "message": "Webhook endpoint is operational",
    }
