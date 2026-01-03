"""
Tests for CIA-SIE Webhook Handler
=================================

Validates webhook processing and payload normalization.

GOVERNED BY: Section 13.1 (Component Specifications - Webhook Handler)
"""

import pytest
from datetime import datetime, timezone, UTC
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from cia_sie.core.enums import SignalType, Direction
from cia_sie.core.exceptions import (
    InvalidWebhookPayloadError,
    WebhookNotRegisteredError,
    ChartNotFoundError,
)
from cia_sie.dal.models import ChartDB, SignalDB
from cia_sie.dal.repositories import ChartRepository, SignalRepository
from cia_sie.ingestion.webhook_handler import WebhookHandler, TradingViewPayloadAdapter


class TestWebhookHandler:
    """Tests for WebhookHandler class."""

    @pytest.fixture
    def mock_chart_repo(self):
        """Create mock chart repository."""
        repo = Mock(spec=ChartRepository)
        repo.get_by_webhook_id = AsyncMock()
        return repo

    @pytest.fixture
    def mock_signal_repo(self):
        """Create mock signal repository."""
        repo = Mock(spec=SignalRepository)
        repo.create = AsyncMock()
        return repo

    @pytest.fixture
    def handler(self, mock_chart_repo, mock_signal_repo):
        """Create handler with mocked repositories."""
        return WebhookHandler(mock_chart_repo, mock_signal_repo)

    @pytest.fixture
    def active_chart(self):
        """Create an active chart mock."""
        chart = Mock(spec=ChartDB)
        chart.chart_id = str(uuid4())
        chart.chart_code = "RSI_14"
        chart.is_active = True
        return chart

    @pytest.mark.asyncio
    async def test_process_webhook_success(
        self, handler, mock_chart_repo, mock_signal_repo, active_chart
    ):
        """Test successful webhook processing."""
        mock_chart_repo.get_by_webhook_id.return_value = active_chart

        # Set up a side effect that populates signal_id when create is called
        # This simulates what SQLAlchemy would do when flushing
        async def mock_create(signal_db):
            if signal_db.signal_id is None:
                signal_db.signal_id = str(uuid4())
            return signal_db

        mock_signal_repo.create.side_effect = mock_create

        payload = {
            "webhook_id": "test_webhook",
            "direction": "BULLISH",
        }

        result = await handler.process_webhook(payload)

        assert result.direction == Direction.BULLISH
        mock_signal_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_webhook_missing_required_fields(self, handler):
        """Test webhook rejects missing required fields."""
        payload = {"direction": "BULLISH"}  # Missing webhook_id

        with pytest.raises(InvalidWebhookPayloadError) as exc_info:
            await handler.process_webhook(payload)

        assert "webhook_id" in str(exc_info.value.message).lower()

    @pytest.mark.asyncio
    async def test_process_webhook_invalid_direction(self, handler):
        """Test webhook rejects invalid direction."""
        payload = {
            "webhook_id": "test",
            "direction": "INVALID_DIRECTION",
        }

        with pytest.raises(InvalidWebhookPayloadError) as exc_info:
            await handler.process_webhook(payload)

        assert "direction" in str(exc_info.value.message).lower()

    @pytest.mark.asyncio
    async def test_process_webhook_unregistered(self, handler, mock_chart_repo):
        """Test webhook rejects unregistered webhook_id."""
        mock_chart_repo.get_by_webhook_id.return_value = None

        payload = {
            "webhook_id": "unknown_webhook",
            "direction": "BULLISH",
        }

        with pytest.raises(WebhookNotRegisteredError):
            await handler.process_webhook(payload)

    @pytest.mark.asyncio
    async def test_process_webhook_inactive_chart(self, handler, mock_chart_repo):
        """Test webhook rejects inactive chart."""
        inactive_chart = Mock(spec=ChartDB)
        inactive_chart.is_active = False
        mock_chart_repo.get_by_webhook_id.return_value = inactive_chart

        payload = {
            "webhook_id": "inactive_chart_webhook",
            "direction": "BULLISH",
        }

        with pytest.raises(ChartNotFoundError):
            await handler.process_webhook(payload)

    @pytest.mark.asyncio
    async def test_process_webhook_preserves_raw_payload(
        self, handler, mock_chart_repo, mock_signal_repo, active_chart
    ):
        """Test that raw payload is preserved for audit trail."""
        mock_chart_repo.get_by_webhook_id.return_value = active_chart

        # Set up a side effect that populates signal_id when create is called
        # This simulates what SQLAlchemy would do when flushing
        async def mock_create(signal_db):
            if signal_db.signal_id is None:
                signal_db.signal_id = str(uuid4())
            return signal_db

        mock_signal_repo.create.side_effect = mock_create

        payload = {
            "webhook_id": "test",
            "direction": "BEARISH",
            "rsi": 25.5,
            "custom_field": "preserved",
        }

        await handler.process_webhook(payload)

        # Verify create was called with raw_payload
        call_args = mock_signal_repo.create.call_args
        created_signal = call_args[0][0]
        assert created_signal.raw_payload == payload

    def test_validate_all_directions(self, handler):
        """Test all valid directions are accepted."""
        for direction in ["BULLISH", "BEARISH", "NEUTRAL"]:
            payload = {"webhook_id": "test", "direction": direction}
            normalized = handler._validate_and_normalize(payload)
            assert normalized.direction == Direction(direction)

    def test_validate_all_signal_types(self, handler):
        """Test all valid signal types are accepted."""
        for signal_type in ["HEARTBEAT", "STATE_CHANGE", "BAR_CLOSE", "MANUAL"]:
            payload = {
                "webhook_id": "test",
                "direction": "NEUTRAL",
                "signal_type": signal_type,
            }
            normalized = handler._validate_and_normalize(payload)
            assert normalized.signal_type == SignalType(signal_type)

    def test_validate_extracts_indicators(self, handler):
        """Test that non-reserved fields become indicators."""
        payload = {
            "webhook_id": "test",
            "direction": "BULLISH",
            "rsi": 72.5,
            "macd": 0.5,
            "custom_indicator": 100,
        }
        normalized = handler._validate_and_normalize(payload)

        assert "rsi" in normalized.indicators
        assert normalized.indicators["rsi"] == 72.5
        assert normalized.indicators["macd"] == 0.5
        assert normalized.indicators["custom_indicator"] == 100


class TestTradingViewPayloadAdapter:
    """Tests for TradingView-specific payload adaptation."""

    def test_adapt_standard_format(self):
        """Test adapting standard TradingView format."""
        tv_payload = {
            "webhook_id": "my_chart",
            "direction": "BULLISH",
            "rsi": 72.5,
        }

        result = TradingViewPayloadAdapter.adapt(tv_payload)

        assert result["webhook_id"] == "my_chart"
        assert result["direction"] == "BULLISH"

    def test_adapt_chart_id_to_webhook_id(self):
        """Test mapping chart_id to webhook_id."""
        tv_payload = {
            "chart_id": "my_chart",  # TradingView uses chart_id
            "direction": "BEARISH",
        }

        result = TradingViewPayloadAdapter.adapt(tv_payload)

        assert result["webhook_id"] == "my_chart"

    def test_adapt_bias_to_direction(self):
        """Test mapping bias to direction."""
        tv_payload = {
            "webhook_id": "chart1",
            "bias": "BULLISH",  # TradingView may use 'bias'
        }

        result = TradingViewPayloadAdapter.adapt(tv_payload)

        assert result["direction"] == "BULLISH"

    def test_adapt_preserves_extra_fields(self):
        """Test that extra fields are preserved as indicators."""
        tv_payload = {
            "webhook_id": "chart1",
            "direction": "NEUTRAL",
            "rsi": 50,
            "volume": 1000000,
            "custom": "value",
        }

        result = TradingViewPayloadAdapter.adapt(tv_payload)

        assert result["rsi"] == 50
        assert result["volume"] == 1000000
        assert result["custom"] == "value"


class TestWebhookHandlerConstitutionalCompliance:
    """
    Tests verifying WebhookHandler maintains constitutional compliance.

    CRITICAL: Per Section 0B, these behaviors are PROHIBITED.
    """

    def test_no_aggregation_method(self):
        """
        CRITICAL: WebhookHandler must not aggregate signals.
        """
        assert not hasattr(WebhookHandler, "aggregate_signals")
        assert not hasattr(WebhookHandler, "compute_aggregate")
        assert not hasattr(WebhookHandler, "get_combined_direction")

    def test_no_scoring_method(self):
        """
        CRITICAL: WebhookHandler must not compute scores.
        """
        assert not hasattr(WebhookHandler, "compute_score")
        assert not hasattr(WebhookHandler, "calculate_confidence")
        assert not hasattr(WebhookHandler, "rate_signal")

    def test_no_recommendation_method(self):
        """
        CRITICAL: WebhookHandler must not make recommendations.
        """
        assert not hasattr(WebhookHandler, "recommend_action")
        assert not hasattr(WebhookHandler, "suggest")
        assert not hasattr(WebhookHandler, "advise")
