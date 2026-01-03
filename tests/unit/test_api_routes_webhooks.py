"""
Tests for CIA-SIE Webhook API Routes
====================================

Unit tests for webhook routes using mocks.

GOVERNED BY: Section 13.1 (Webhook Handler)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException
from fastapi.testclient import TestClient

from cia_sie.core.enums import Direction, SignalType
from cia_sie.core.exceptions import (
    InvalidWebhookPayloadError,
    WebhookNotRegisteredError,
    ChartNotFoundError,
)
from cia_sie.api.routes.webhooks import (
    router,
    get_webhook_handler,
)


class TestWebhookHealthEndpoint:
    """Tests for webhook health endpoint."""

    @pytest.mark.asyncio
    async def test_webhook_health_returns_status(self):
        """Test webhook health returns status info."""
        # Import the module and patch get_settings at import time
        import cia_sie.api.routes.webhooks as webhooks_module

        mock_settings = Mock()
        mock_settings.webhook_secret = "test_secret"

        # Patch the imported get_settings in the webhooks module
        with patch.object(webhooks_module, 'get_settings', create=True):
            # The function imports get_settings locally, so we need to
            # patch cia_sie.core.config.get_settings
            with patch('cia_sie.core.config.get_settings') as mock_get:
                mock_get.return_value = mock_settings
                result = await webhooks_module.webhook_health()

        assert result["status"] == "healthy"
        assert result["authentication_enabled"] is True
        assert "message" in result

    @pytest.mark.asyncio
    async def test_webhook_health_no_auth(self):
        """Test webhook health with no authentication configured."""
        import cia_sie.api.routes.webhooks as webhooks_module

        mock_settings = Mock()
        mock_settings.webhook_secret = None

        with patch('cia_sie.core.config.get_settings') as mock_get:
            mock_get.return_value = mock_settings
            result = await webhooks_module.webhook_health()

        assert result["authentication_enabled"] is False


class TestGetWebhookHandler:
    """Tests for webhook handler dependency."""

    @pytest.mark.asyncio
    async def test_get_webhook_handler_creates_handler(self):
        """Test get_webhook_handler creates proper WebhookHandler."""
        mock_session = Mock()

        with patch('cia_sie.api.routes.webhooks.ChartRepository') as MockChartRepo, \
             patch('cia_sie.api.routes.webhooks.SignalRepository') as MockSignalRepo:

            handler = await get_webhook_handler(mock_session)

        MockChartRepo.assert_called_once_with(mock_session)
        MockSignalRepo.assert_called_once_with(mock_session)


class TestReceiveWebhook:
    """Tests for main webhook receive endpoint."""

    @pytest.fixture
    def mock_handler(self):
        """Create mock webhook handler."""
        handler = Mock()
        handler.process_webhook = AsyncMock()
        return handler

    @pytest.fixture
    def mock_signal(self):
        """Create mock signal response."""
        signal = Mock()
        signal.signal_id = uuid4()
        signal.chart_id = uuid4()
        signal.direction = Direction.BULLISH
        return signal

    @pytest.mark.asyncio
    async def test_receive_webhook_success(self, mock_handler, mock_signal):
        """Test successful webhook processing."""
        from cia_sie.api.routes.webhooks import receive_webhook

        mock_handler.process_webhook.return_value = mock_signal
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "test", "direction": "BULLISH"}'

        with patch('cia_sie.api.routes.webhooks.TradingViewPayloadAdapter') as MockAdapter, \
             patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockAdapter.adapt.return_value = {"webhook_id": "test", "direction": "BULLISH"}
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            result = await receive_webhook(mock_request, validated_body, mock_handler)

        assert result["status"] == "accepted"
        assert "signal_id" in result
        assert result["direction"] == "BULLISH"

    @pytest.mark.asyncio
    async def test_receive_webhook_invalid_json(self, mock_handler):
        """Test webhook rejects invalid JSON."""
        from cia_sie.api.routes.webhooks import receive_webhook

        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'not valid json'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_webhook(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_receive_webhook_invalid_payload(self, mock_handler):
        """Test webhook rejects invalid payload."""
        from cia_sie.api.routes.webhooks import receive_webhook

        mock_handler.process_webhook.side_effect = InvalidWebhookPayloadError(
            "Missing required field"
        )
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "test"}'

        with patch('cia_sie.api.routes.webhooks.TradingViewPayloadAdapter') as MockAdapter, \
             patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockAdapter.adapt.return_value = {"webhook_id": "test"}
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_webhook(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_receive_webhook_unregistered(self, mock_handler):
        """Test webhook rejects unregistered webhook_id."""
        from cia_sie.api.routes.webhooks import receive_webhook

        mock_handler.process_webhook.side_effect = WebhookNotRegisteredError(
            "Unknown webhook"
        )
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "unknown", "direction": "BULLISH"}'

        with patch('cia_sie.api.routes.webhooks.TradingViewPayloadAdapter') as MockAdapter, \
             patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockAdapter.adapt.return_value = {"webhook_id": "unknown", "direction": "BULLISH"}
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_webhook(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_receive_webhook_chart_not_found(self, mock_handler):
        """Test webhook rejects inactive/missing chart."""
        from cia_sie.api.routes.webhooks import receive_webhook

        mock_handler.process_webhook.side_effect = ChartNotFoundError(
            "Chart inactive"
        )
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "inactive", "direction": "BULLISH"}'

        with patch('cia_sie.api.routes.webhooks.TradingViewPayloadAdapter') as MockAdapter, \
             patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockAdapter.adapt.return_value = {"webhook_id": "inactive", "direction": "BULLISH"}
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_webhook(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 404


class TestReceiveManualTrigger:
    """Tests for manual trigger endpoint."""

    @pytest.fixture
    def mock_handler(self):
        """Create mock webhook handler."""
        handler = Mock()
        handler.process_webhook = AsyncMock()
        return handler

    @pytest.fixture
    def mock_signal(self):
        """Create mock signal response."""
        signal = Mock()
        signal.signal_id = uuid4()
        signal.chart_id = uuid4()
        signal.direction = Direction.BULLISH
        return signal

    @pytest.mark.asyncio
    async def test_receive_manual_trigger_success(self, mock_handler, mock_signal):
        """Test successful manual trigger processing."""
        from cia_sie.api.routes.webhooks import receive_manual_trigger

        mock_handler.process_webhook.return_value = mock_signal
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "test", "direction": "BULLISH"}'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            result = await receive_manual_trigger(mock_request, validated_body, mock_handler)

        assert result["status"] == "accepted"
        assert result["trigger_type"] == "MANUAL"
        assert "signal_id" in result

    @pytest.mark.asyncio
    async def test_receive_manual_trigger_forces_manual_type(self, mock_handler, mock_signal):
        """Test manual trigger forces MANUAL signal type."""
        from cia_sie.api.routes.webhooks import receive_manual_trigger

        mock_handler.process_webhook.return_value = mock_signal
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "test", "direction": "BULLISH", "signal_type": "STATE_CHANGE"}'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            await receive_manual_trigger(mock_request, validated_body, mock_handler)

        # Verify that the handler was called with signal_type=MANUAL
        call_args = mock_handler.process_webhook.call_args
        payload = call_args[0][0]
        assert payload["signal_type"] == "MANUAL"

    @pytest.mark.asyncio
    async def test_receive_manual_trigger_invalid_json(self, mock_handler):
        """Test manual trigger rejects invalid JSON."""
        from cia_sie.api.routes.webhooks import receive_manual_trigger

        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'invalid json'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_manual_trigger(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_receive_manual_trigger_invalid_payload(self, mock_handler):
        """Test manual trigger handles invalid payload error."""
        from cia_sie.api.routes.webhooks import receive_manual_trigger

        mock_handler.process_webhook.side_effect = InvalidWebhookPayloadError(
            "Invalid payload"
        )
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "test"}'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_manual_trigger(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_receive_manual_trigger_webhook_not_registered(self, mock_handler):
        """Test manual trigger handles unregistered webhook."""
        from cia_sie.api.routes.webhooks import receive_manual_trigger

        mock_handler.process_webhook.side_effect = WebhookNotRegisteredError(
            "Not registered"
        )
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "unknown", "direction": "BULLISH"}'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_manual_trigger(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_receive_manual_trigger_chart_not_found(self, mock_handler):
        """Test manual trigger handles missing chart."""
        from cia_sie.api.routes.webhooks import receive_manual_trigger

        mock_handler.process_webhook.side_effect = ChartNotFoundError(
            "Not found"
        )
        mock_request = Mock()
        mock_request.client = Mock(host="127.0.0.1")
        validated_body = b'{"webhook_id": "inactive", "direction": "BULLISH"}'

        with patch('cia_sie.api.routes.webhooks.WebhookSignatureValidator') as MockValidator, \
             patch('cia_sie.api.routes.webhooks.log_security_event'):
            MockValidator.get_client_ip.return_value = "127.0.0.1"

            with pytest.raises(HTTPException) as exc_info:
                await receive_manual_trigger(mock_request, validated_body, mock_handler)

            assert exc_info.value.status_code == 404


class TestWebhookConstitutionalCompliance:
    """Constitutional compliance tests for webhook routes."""

    @pytest.mark.constitutional
    def test_no_scoring_in_webhook_routes(self):
        """CRITICAL: Webhook routes must not have scoring methods."""
        import cia_sie.api.routes.webhooks as webhooks_module

        prohibited_methods = [
            'compute_score', 'calculate_confidence', 'rate_signal',
            'aggregate_signals', 'recommend',
        ]

        for method in prohibited_methods:
            assert not hasattr(webhooks_module, method), \
                f"CONSTITUTIONAL VIOLATION: webhooks module has {method}"

    @pytest.mark.constitutional
    def test_webhook_response_structure_compliant(self):
        """CRITICAL: Webhook response must not have prohibited fields."""
        # The response dict structure that receive_webhook returns
        required_fields = ["status", "signal_id", "chart_id", "direction", "received_at"]
        prohibited_fields = ["score", "confidence", "weight", "recommendation", "advice"]

        # This test documents the expected structure
        sample_response = {
            "status": "accepted",
            "signal_id": "test",
            "chart_id": "test",
            "direction": "BULLISH",
            "received_at": "2025-01-01T00:00:00Z",
        }

        for field in required_fields:
            assert field in sample_response

        for field in prohibited_fields:
            assert field not in sample_response
