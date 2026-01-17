"""
CIA-SIE Webhook Handler
=======================

Receives and STORES incoming signals from TradingView and other platforms.

GOVERNED BY: Section 13.1 (Component Specifications - Webhook Handler)

DOES:
- Validate JSON structure
- Store signal in database
- Emit WebSocket event

DOES NOT:
- Aggregate signals
- Compute scores
- Make judgments
"""

import logging
from datetime import UTC, datetime
from typing import Optional
from uuid import UUID

from cia_sie.core.enums import Direction, SignalType
from cia_sie.core.exceptions import (
    ChartNotFoundError,
    InvalidWebhookPayloadError,
    WebhookNotRegisteredError,
)
from cia_sie.core.models import Signal, WebhookPayload
from cia_sie.dal.models import SignalDB
from cia_sie.dal.repositories import ChartRepository, SignalRepository

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Handles incoming webhook payloads.

    Per Gold Standard Specification Section 13.1:
    - Validates incoming payloads
    - Stores signals in the database
    - Does NOT aggregate, score, or make judgments
    """

    def __init__(
        self,
        chart_repository: ChartRepository,
        signal_repository: SignalRepository,
    ):
        self.chart_repo = chart_repository
        self.signal_repo = signal_repository

    async def process_webhook(
        self,
        payload: dict,
        received_at: Optional[datetime] = None,
    ) -> Signal:
        """
        Process an incoming webhook payload.

        Args:
            payload: Raw webhook payload from TradingView or other platform
            received_at: Timestamp when the webhook was received (defaults to now)

        Returns:
            The created Signal object

        Raises:
            InvalidWebhookPayloadError: If payload validation fails
            WebhookNotRegisteredError: If webhook_id is not found

        NOTE: This method STORES the signal. It does NOT:
        - Aggregate with other signals
        - Compute scores
        - Make any judgments
        """
        received_at = received_at or datetime.now(UTC)

        # Validate and normalize payload
        normalized = self._validate_and_normalize(payload)

        # Find the chart by webhook_id
        chart = await self.chart_repo.get_by_webhook_id(normalized.webhook_id)
        if not chart:
            raise WebhookNotRegisteredError(
                f"No chart registered with webhook_id: {normalized.webhook_id}",
                {"webhook_id": normalized.webhook_id},
            )

        if not chart.is_active:
            raise ChartNotFoundError(
                f"Chart with webhook_id '{normalized.webhook_id}' is inactive",
                {"webhook_id": normalized.webhook_id},
            )

        # Create signal record
        # Handle both enum objects and string values (Pydantic use_enum_values=True)
        signal_type_val = (
            normalized.signal_type.value
            if hasattr(normalized.signal_type, "value")
            else normalized.signal_type
        )
        direction_val = (
            normalized.direction.value
            if hasattr(normalized.direction, "value")
            else normalized.direction
        )

        signal_db = SignalDB(
            chart_id=chart.chart_id,
            received_at=received_at,
            signal_timestamp=normalized.timestamp,
            signal_type=signal_type_val,
            direction=direction_val,
            indicators=normalized.indicators,
            raw_payload=payload,  # Preserve original for audit trail
        )

        # Store in database
        await self.signal_repo.create(signal_db)

        logger.info(
            f"Signal stored: chart={chart.chart_code}, "
            f"direction={direction_val}, "
            f"type={signal_type_val}"
        )

        # Convert to domain model for return
        return Signal(
            signal_id=UUID(signal_db.signal_id),
            chart_id=UUID(signal_db.chart_id),
            received_at=signal_db.received_at,
            signal_timestamp=signal_db.signal_timestamp,
            signal_type=SignalType(signal_db.signal_type),
            direction=Direction(signal_db.direction),
            indicators=signal_db.indicators,
            raw_payload=signal_db.raw_payload,
        )

    def _validate_and_normalize(self, payload: dict) -> WebhookPayload:
        """
        Validate and normalize incoming webhook payload.

        Args:
            payload: Raw payload from webhook

        Returns:
            Normalized WebhookPayload

        Raises:
            InvalidWebhookPayloadError: If validation fails
        """
        # Required fields
        required_fields = ["webhook_id", "direction"]
        missing = [f for f in required_fields if f not in payload]
        if missing:
            raise InvalidWebhookPayloadError(
                f"Missing required fields: {', '.join(missing)}", {"missing_fields": missing}
            )

        # Parse webhook_id
        webhook_id = str(payload["webhook_id"])

        # Parse direction
        direction_str = str(payload["direction"]).upper()
        try:
            direction = Direction(direction_str)
        except ValueError:
            raise InvalidWebhookPayloadError(
                f"Invalid direction: {direction_str}. Must be BULLISH, BEARISH, or NEUTRAL",
                {"direction": direction_str},
            )

        # Parse signal_type (default to STATE_CHANGE)
        signal_type_str = str(payload.get("signal_type", "STATE_CHANGE")).upper()
        try:
            signal_type = SignalType(signal_type_str)
        except ValueError:
            raise InvalidWebhookPayloadError(
                f"Invalid signal_type: {signal_type_str}", {"signal_type": signal_type_str}
            )

        # Parse timestamp (default to now)
        timestamp = datetime.now(UTC)
        if "timestamp" in payload:
            try:
                if isinstance(payload["timestamp"], str):
                    timestamp = datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
                elif isinstance(payload["timestamp"], (int, float)):
                    timestamp = datetime.fromtimestamp(payload["timestamp"], tz=UTC)
            except (ValueError, TypeError) as e:
                logger.warning(f"Failed to parse timestamp: {e}, using current time")

        # Extract indicators (everything else except reserved fields)
        reserved_fields = {"webhook_id", "direction", "signal_type", "timestamp"}
        indicators = {k: v for k, v in payload.items() if k not in reserved_fields}

        return WebhookPayload(
            webhook_id=webhook_id,
            timestamp=timestamp,
            signal_type=signal_type,
            direction=direction,
            indicators=indicators,
        )


class TradingViewPayloadAdapter:
    """
    Adapter for TradingView-specific webhook payloads.

    Converts TradingView alert format to normalized format.
    Part of the Platform-Agnostic Integration layer (Section 8).
    """

    @staticmethod
    def adapt(tv_payload: dict) -> dict:
        """
        Adapt TradingView payload to normalized format.

        TradingView payloads may use different field names.
        This adapter normalizes them.

        Args:
            tv_payload: Raw TradingView webhook payload

        Returns:
            Normalized payload dict
        """
        normalized = {}

        # Map TradingView field names to our standard names
        field_mapping = {
            "chart_id": "webhook_id",
            "chartId": "webhook_id",
            "chart": "webhook_id",
            "id": "webhook_id",
            "bias": "direction",
            "signal": "direction",
            "trend": "direction",
            "type": "signal_type",
            "alertType": "signal_type",
            "time": "timestamp",
            "alertTime": "timestamp",
        }

        # Apply mapping
        for tv_key, std_key in field_mapping.items():
            if tv_key in tv_payload and std_key not in normalized:
                normalized[std_key] = tv_payload[tv_key]

        # Copy all other fields as-is (they become indicators)
        for key, value in tv_payload.items():
            if key not in normalized:
                normalized[key] = value

        return normalized
