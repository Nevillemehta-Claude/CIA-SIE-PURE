"""
Tests for CIA-SIE Signal Normalizer
===================================

Validates signal normalization from different platforms.

GOVERNED BY: Section 8.2 (Platform Adapter Interface)
"""

import pytest
from datetime import datetime

from cia_sie.core.enums import Direction, SignalType
from cia_sie.ingestion.signal_normalizer import (
    NormalizedSignal,
    SignalNormalizer,
    TradingViewNormalizer,
    ManualTriggerNormalizer,
)


class TestNormalizedSignal:
    """Tests for NormalizedSignal dataclass."""

    def test_normalized_signal_creation(self):
        """Test creating a normalized signal."""
        signal = NormalizedSignal(
            source_platform="TradingView",
            webhook_id="TEST_01",
            timestamp=datetime.utcnow(),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={"rsi": 28.5},
            raw_payload={"test": "data"},
        )
        assert signal.source_platform == "TradingView"
        assert signal.webhook_id == "TEST_01"
        assert signal.direction == Direction.BULLISH

    def test_normalized_signal_is_frozen(self):
        """Test that NormalizedSignal is immutable."""
        signal = NormalizedSignal(
            source_platform="Test",
            webhook_id="TEST",
            timestamp=datetime.utcnow(),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            signal.direction = Direction.BEARISH

    @pytest.mark.constitutional
    def test_normalized_signal_has_no_confidence(self):
        """CRITICAL: NormalizedSignal must have no confidence field."""
        signal = NormalizedSignal(
            source_platform="Test",
            webhook_id="TEST",
            timestamp=datetime.utcnow(),
            signal_type=SignalType.STATE_CHANGE,
            direction=Direction.BULLISH,
            indicators={},
            raw_payload={},
        )
        assert not hasattr(signal, 'confidence')
        assert not hasattr(signal, 'score')
        assert not hasattr(signal, 'weight')


class TestTradingViewNormalizer:
    """Tests for TradingViewNormalizer."""

    @pytest.fixture
    def normalizer(self):
        """Create TradingViewNormalizer instance."""
        return TradingViewNormalizer()

    def test_platform_name(self, normalizer):
        """Test platform name is TradingView."""
        assert normalizer.platform_name == "TradingView"

    def test_normalize_basic_payload(self, normalizer):
        """Test normalizing a basic TradingView payload."""
        payload = {
            "webhook_id": "RSI_14",
            "direction": "BULLISH",
        }
        signal = normalizer.normalize(payload)

        assert signal.webhook_id == "RSI_14"
        assert signal.direction == Direction.BULLISH
        assert signal.source_platform == "TradingView"

    def test_normalize_with_indicators(self, normalizer):
        """Test normalizing payload with indicators."""
        payload = {
            "webhook_id": "RSI_14",
            "direction": "BEARISH",
            "rsi": 75.5,
            "macd": -0.12,
        }
        signal = normalizer.normalize(payload)

        assert signal.indicators["rsi"] == 75.5
        assert signal.indicators["macd"] == -0.12
        assert "webhook_id" not in signal.indicators
        assert "direction" not in signal.indicators

    def test_normalize_direction_synonyms(self, normalizer):
        """Test normalizing various direction synonyms."""
        bullish_values = ["BULLISH", "BUY", "LONG", "UP", "POSITIVE"]
        bearish_values = ["BEARISH", "SELL", "SHORT", "DOWN", "NEGATIVE"]
        neutral_values = ["NEUTRAL", "FLAT", "NONE", "SIDEWAYS"]

        for value in bullish_values:
            payload = {"webhook_id": "TEST", "direction": value}
            signal = normalizer.normalize(payload)
            assert signal.direction == Direction.BULLISH, f"Failed for {value}"

        for value in bearish_values:
            payload = {"webhook_id": "TEST", "direction": value}
            signal = normalizer.normalize(payload)
            assert signal.direction == Direction.BEARISH, f"Failed for {value}"

        for value in neutral_values:
            payload = {"webhook_id": "TEST", "direction": value}
            signal = normalizer.normalize(payload)
            assert signal.direction == Direction.NEUTRAL, f"Failed for {value}"

    def test_normalize_webhook_id_alternatives(self, normalizer):
        """Test normalizing various webhook_id field names."""
        alternatives = [
            ("webhook_id", "ID1"),
            ("chart_id", "ID2"),
            ("chartId", "ID3"),
            ("id", "ID4"),
        ]

        for field, value in alternatives:
            payload = {field: value, "direction": "BULLISH"}
            signal = normalizer.normalize(payload)
            assert signal.webhook_id == value

    def test_normalize_signal_type_variations(self, normalizer):
        """Test normalizing various signal type values."""
        heartbeat_values = ["HEARTBEAT", "HB", "PING"]
        manual_values = ["MANUAL", "TRIGGER", "ON_DEMAND"]
        state_change_values = ["STATE_CHANGE", "CHANGE", "ALERT"]

        for value in heartbeat_values:
            payload = {"webhook_id": "TEST", "direction": "BULLISH", "signal_type": value}
            signal = normalizer.normalize(payload)
            assert signal.signal_type == SignalType.HEARTBEAT

        for value in manual_values:
            payload = {"webhook_id": "TEST", "direction": "BULLISH", "signal_type": value}
            signal = normalizer.normalize(payload)
            assert signal.signal_type == SignalType.MANUAL

        for value in state_change_values:
            payload = {"webhook_id": "TEST", "direction": "BULLISH", "signal_type": value}
            signal = normalizer.normalize(payload)
            assert signal.signal_type == SignalType.STATE_CHANGE

    def test_normalize_defaults_to_state_change(self, normalizer):
        """Test that missing signal_type defaults to STATE_CHANGE."""
        payload = {"webhook_id": "TEST", "direction": "BULLISH"}
        signal = normalizer.normalize(payload)
        assert signal.signal_type == SignalType.STATE_CHANGE

    def test_normalize_with_timestamp(self, normalizer):
        """Test normalizing with ISO timestamp."""
        payload = {
            "webhook_id": "TEST",
            "direction": "BULLISH",
            "timestamp": "2025-01-01T12:00:00Z",
        }
        signal = normalizer.normalize(payload)
        assert signal.timestamp.year == 2025
        assert signal.timestamp.month == 1
        assert signal.timestamp.day == 1

    def test_normalize_raw_payload_preserved(self, normalizer):
        """Test that raw payload is preserved."""
        payload = {
            "webhook_id": "TEST",
            "direction": "BULLISH",
            "custom_field": "custom_value",
        }
        signal = normalizer.normalize(payload)
        assert signal.raw_payload == payload

    def test_validate_valid_payload(self, normalizer):
        """Test validating a valid payload."""
        payload = {"webhook_id": "TEST", "direction": "BULLISH"}
        assert normalizer.validate(payload) is True

    def test_validate_missing_webhook_id(self, normalizer):
        """Test validating payload without webhook_id."""
        payload = {"direction": "BULLISH"}
        assert normalizer.validate(payload) is False

    def test_validate_missing_direction(self, normalizer):
        """Test validating payload without direction."""
        payload = {"webhook_id": "TEST"}
        assert normalizer.validate(payload) is False

    def test_validate_alternative_fields(self, normalizer):
        """Test validating with alternative field names."""
        payload = {"chart_id": "TEST", "bias": "BULLISH"}
        assert normalizer.validate(payload) is True

    def test_normalize_raises_on_missing_webhook_id(self, normalizer):
        """Test that normalize raises on missing webhook_id."""
        payload = {"direction": "BULLISH"}
        with pytest.raises(ValueError, match="No webhook_id found"):
            normalizer.normalize(payload)

    def test_normalize_raises_on_missing_direction(self, normalizer):
        """Test that normalize raises on missing direction."""
        payload = {"webhook_id": "TEST"}
        with pytest.raises(ValueError, match="No valid direction found"):
            normalizer.normalize(payload)


class TestManualTriggerNormalizer:
    """Tests for ManualTriggerNormalizer."""

    @pytest.fixture
    def normalizer(self):
        """Create ManualTriggerNormalizer instance."""
        return ManualTriggerNormalizer()

    def test_platform_name(self, normalizer):
        """Test platform name is ManualTrigger."""
        assert normalizer.platform_name == "ManualTrigger"

    def test_normalize_basic_payload(self, normalizer):
        """Test normalizing a basic manual trigger payload."""
        payload = {
            "webhook_id": "MANUAL_01",
            "direction": "BEARISH",
        }
        signal = normalizer.normalize(payload)

        assert signal.webhook_id == "MANUAL_01"
        assert signal.direction == Direction.BEARISH
        assert signal.signal_type == SignalType.MANUAL
        assert signal.source_platform == "ManualTrigger"

    def test_normalize_with_indicators(self, normalizer):
        """Test normalizing with provided indicators."""
        payload = {
            "webhook_id": "MANUAL_01",
            "direction": "BULLISH",
            "indicators": {"rsi": 30},
        }
        signal = normalizer.normalize(payload)

        assert signal.indicators == {"rsi": 30}

    def test_validate_valid_payload(self, normalizer):
        """Test validating a valid payload."""
        payload = {"webhook_id": "TEST"}
        assert normalizer.validate(payload) is True

    def test_validate_missing_webhook_id(self, normalizer):
        """Test validating payload without webhook_id."""
        payload = {"direction": "BULLISH"}
        assert normalizer.validate(payload) is False

    @pytest.mark.constitutional
    def test_manual_signal_has_no_score(self, normalizer):
        """CRITICAL: Manual signals must have no score."""
        payload = {"webhook_id": "TEST", "direction": "BULLISH"}
        signal = normalizer.normalize(payload)

        assert not hasattr(signal, 'confidence')
        assert not hasattr(signal, 'score')


class TestSignalNormalizerConstitutionalCompliance:
    """
    Constitutional compliance tests for signal normalizers.

    CRITICAL: Normalizers must not add any judgment or scoring.
    """

    @pytest.mark.constitutional
    def test_normalizers_dont_add_confidence(self):
        """CRITICAL: Normalizers must not add confidence fields."""
        normalizers = [TradingViewNormalizer(), ManualTriggerNormalizer()]

        for normalizer in normalizers:
            assert not hasattr(normalizer, 'compute_confidence')
            assert not hasattr(normalizer, 'score')
            assert not hasattr(normalizer, 'weight')

    @pytest.mark.constitutional
    def test_normalizer_base_class_has_no_scoring(self):
        """CRITICAL: Base class must not have scoring methods."""
        prohibited_methods = [
            'score', 'weight', 'confidence', 'rank',
            'aggregate', 'prioritize',
        ]

        for method in prohibited_methods:
            assert not hasattr(SignalNormalizer, method), \
                f"CONSTITUTIONAL VIOLATION: SignalNormalizer has {method}"
