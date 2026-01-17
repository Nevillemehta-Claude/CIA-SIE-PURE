"""
CIA-SIE Signal Normalizer
=========================

Normalizes signals from different platforms into a standard format.

GOVERNED BY: Section 8.2 (Platform Adapter Interface)

This component transforms platform-specific signals into the
NormalizedSignal format without adding any judgments or scores.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from cia_sie.core.enums import Direction, SignalType


@dataclass(frozen=True)
class NormalizedSignal:
    """
    Platform-agnostic signal format.

    Per Gold Standard Specification Section 8.2.
    This is the internal format after normalization.

    NOTE: No confidence or score fields - these are prohibited.
    """

    source_platform: str
    webhook_id: str
    timestamp: datetime
    signal_type: SignalType
    direction: Direction
    indicators: dict
    raw_payload: dict


class SignalNormalizer(ABC):
    """
    Abstract base class for platform-specific signal normalizers.

    Each platform (TradingView, Kite, etc.) implements this interface.
    The core system is platform-agnostic.
    """

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform name."""
        pass

    @abstractmethod
    def normalize(self, raw_payload: dict) -> NormalizedSignal:
        """
        Normalize a platform-specific payload to standard format.

        Args:
            raw_payload: Raw payload from the platform

        Returns:
            NormalizedSignal in standard format
        """
        pass

    @abstractmethod
    def validate(self, raw_payload: dict) -> bool:
        """
        Validate that a payload is from this platform.

        Args:
            raw_payload: Raw payload to validate

        Returns:
            True if payload is valid for this platform
        """
        pass


class TradingViewNormalizer(SignalNormalizer):
    """
    Normalizer for TradingView webhook payloads.

    Handles the various formats that TradingView alerts can use.
    """

    @property
    def platform_name(self) -> str:
        return "TradingView"

    def normalize(self, raw_payload: dict) -> NormalizedSignal:
        """
        Normalize TradingView payload.

        Expected TradingView format:
        {
            "webhook_id": "SAMPLE_01A",
            "direction": "BULLISH",
            "signal_type": "STATE_CHANGE",  # optional
            "timestamp": "2025-01-01T00:00:00Z",  # optional
            "rsi": 28.5,  # indicator values
            "macd": 0.12,
            ...
        }
        """
        # Extract webhook_id
        webhook_id = self._extract_webhook_id(raw_payload)

        # Extract direction
        direction = self._extract_direction(raw_payload)

        # Extract signal type
        signal_type = self._extract_signal_type(raw_payload)

        # Extract timestamp
        timestamp = self._extract_timestamp(raw_payload)

        # Extract indicators (everything else)
        indicators = self._extract_indicators(raw_payload)

        return NormalizedSignal(
            source_platform=self.platform_name,
            webhook_id=webhook_id,
            timestamp=timestamp,
            signal_type=signal_type,
            direction=direction,
            indicators=indicators,
            raw_payload=raw_payload,
        )

    def validate(self, raw_payload: dict) -> bool:
        """Validate TradingView payload structure."""
        # Must have webhook_id in some form
        webhook_id_fields = ["webhook_id", "chart_id", "chartId", "id"]
        has_webhook_id = any(f in raw_payload for f in webhook_id_fields)

        # Must have direction in some form
        direction_fields = ["direction", "bias", "signal", "trend"]
        has_direction = any(f in raw_payload for f in direction_fields)

        return has_webhook_id and has_direction

    def _extract_webhook_id(self, payload: dict) -> str:
        """Extract webhook_id from various possible field names."""
        for field in ["webhook_id", "chart_id", "chartId", "id"]:
            if field in payload:
                return str(payload[field])
        raise ValueError("No webhook_id found in payload")

    def _extract_direction(self, payload: dict) -> Direction:
        """Extract and validate direction."""
        for field in ["direction", "bias", "signal", "trend"]:
            if field in payload:
                value = str(payload[field]).upper()
                # Handle various synonyms
                if value in ["BULLISH", "BUY", "LONG", "UP", "POSITIVE"]:
                    return Direction.BULLISH
                elif value in ["BEARISH", "SELL", "SHORT", "DOWN", "NEGATIVE"]:
                    return Direction.BEARISH
                elif value in ["NEUTRAL", "FLAT", "NONE", "SIDEWAYS"]:
                    return Direction.NEUTRAL
        raise ValueError("No valid direction found in payload")

    def _extract_signal_type(self, payload: dict) -> SignalType:
        """Extract signal type, defaulting to STATE_CHANGE."""
        for field in ["signal_type", "type", "alertType"]:
            if field in payload:
                value = str(payload[field]).upper()
                if value in ["HEARTBEAT", "HB", "PING"]:
                    return SignalType.HEARTBEAT
                elif value in ["MANUAL", "TRIGGER", "ON_DEMAND"]:
                    return SignalType.MANUAL
                elif value in ["STATE_CHANGE", "CHANGE", "ALERT"]:
                    return SignalType.STATE_CHANGE
        return SignalType.STATE_CHANGE

    def _extract_timestamp(self, payload: dict) -> datetime:
        """Extract timestamp, defaulting to now."""
        for field in ["timestamp", "time", "alertTime", "date"]:
            if field in payload:
                value = payload[field]
                try:
                    if isinstance(value, str):
                        return datetime.fromisoformat(value.replace("Z", "+00:00"))
                    elif isinstance(value, (int, float)):
                        return datetime.utcfromtimestamp(value)
                except (ValueError, TypeError):
                    pass
        return datetime.utcnow()

    def _extract_indicators(self, payload: dict) -> dict:
        """Extract indicator values (everything not a reserved field)."""
        reserved = {
            "webhook_id",
            "chart_id",
            "chartId",
            "id",
            "direction",
            "bias",
            "signal",
            "trend",
            "signal_type",
            "type",
            "alertType",
            "timestamp",
            "time",
            "alertTime",
            "date",
        }
        return {k: v for k, v in payload.items() if k not in reserved}


class ManualTriggerNormalizer(SignalNormalizer):
    """
    Normalizer for manual trigger (MTIC) payloads.

    Handles on-demand signals triggered by user action.
    """

    @property
    def platform_name(self) -> str:
        return "ManualTrigger"

    def normalize(self, raw_payload: dict) -> NormalizedSignal:
        """Normalize manual trigger payload."""
        return NormalizedSignal(
            source_platform=self.platform_name,
            webhook_id=str(raw_payload.get("webhook_id", "")),
            timestamp=datetime.utcnow(),
            signal_type=SignalType.MANUAL,
            direction=Direction(str(raw_payload.get("direction", "NEUTRAL")).upper()),
            indicators=raw_payload.get("indicators", {}),
            raw_payload=raw_payload,
        )

    def validate(self, raw_payload: dict) -> bool:
        """Validate manual trigger payload."""
        return "webhook_id" in raw_payload
