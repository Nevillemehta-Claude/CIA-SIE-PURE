"""
Tests for CIA-SIE Claude Client
===============================

Validates Claude API client functionality.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from cia_sie.ai.claude_client import ClaudeClient
from cia_sie.core.exceptions import AIProviderError


class TestClaudeClientInitialization:
    """Tests for ClaudeClient initialization."""

    def test_init_with_explicit_api_key(self):
        """Test initialization with explicit API key."""
        client = ClaudeClient(api_key="test-api-key")
        assert client.api_key == "test-api-key"

    def test_init_with_explicit_model(self):
        """Test initialization with explicit model."""
        client = ClaudeClient(api_key="test", model="claude-3-opus")
        assert client.model == "claude-3-opus"

    def test_init_defaults_from_settings(self):
        """Test initialization uses settings defaults."""
        with patch("cia_sie.ai.claude_client.get_settings") as mock_settings:
            mock_settings.return_value.anthropic_api_key = "settings-key"
            mock_settings.return_value.anthropic_model = "settings-model"

            client = ClaudeClient()

            assert client.api_key == "settings-key"
            assert client.model == "settings-model"

    def test_init_without_api_key_logs_warning(self):
        """Test that missing API key logs a warning."""
        with patch("cia_sie.ai.claude_client.get_settings") as mock_settings:
            mock_settings.return_value.anthropic_api_key = None
            mock_settings.return_value.anthropic_model = "model"

            with patch("cia_sie.ai.claude_client.logger") as mock_logger:
                ClaudeClient()
                mock_logger.warning.assert_called()

    def test_client_not_created_until_accessed(self):
        """Test lazy initialization of underlying client."""
        client = ClaudeClient(api_key="test")
        assert client._client is None


class TestClaudeClientProperty:
    """Tests for the client property."""

    def test_client_property_creates_async_client(self):
        """Test client property creates AsyncAnthropic client."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_anthropic.return_value = Mock()

            client = ClaudeClient(api_key="test-key")
            _ = client.client

            mock_anthropic.assert_called_once_with(api_key="test-key")

    def test_client_property_returns_same_instance(self):
        """Test client property returns cached instance."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_anthropic.return_value = Mock()

            client = ClaudeClient(api_key="test-key")
            first_call = client.client
            second_call = client.client

            assert first_call is second_call
            mock_anthropic.assert_called_once()

    def test_client_property_raises_without_api_key(self):
        """Test client property raises error without API key."""
        with patch("cia_sie.ai.claude_client.get_settings") as mock_settings:
            mock_settings.return_value.anthropic_api_key = None
            mock_settings.return_value.anthropic_model = "model"

            client = ClaudeClient()

            with pytest.raises(AIProviderError) as exc_info:
                _ = client.client

            assert "API key not configured" in str(exc_info.value.message)


class TestClaudeClientGenerate:
    """Tests for the generate method."""

    @pytest.mark.asyncio
    async def test_generate_returns_text_response(self):
        """Test generate returns text from API response."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_response = Mock()
            mock_response.content = [Mock(text="Generated response")]
            mock_api.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            result = await client.generate(
                system_prompt="System prompt",
                user_prompt="User prompt",
            )

            assert result == "Generated response"

    @pytest.mark.asyncio
    async def test_generate_uses_correct_parameters(self):
        """Test generate passes correct parameters to API."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_response = Mock()
            mock_response.content = [Mock(text="Response")]
            mock_api.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            await client.generate(
                system_prompt="System prompt",
                user_prompt="User prompt",
                max_tokens=1000,
                temperature=0.5,
            )

            mock_api.messages.create.assert_called_once()
            call_kwargs = mock_api.messages.create.call_args.kwargs
            assert call_kwargs["system"] == "System prompt"
            assert call_kwargs["max_tokens"] == 1000
            assert call_kwargs["temperature"] == 0.5
            assert call_kwargs["messages"] == [{"role": "user", "content": "User prompt"}]

    @pytest.mark.asyncio
    async def test_generate_raises_on_empty_response(self):
        """Test generate raises error on empty response."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_response = Mock()
            mock_response.content = []
            mock_api.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            with pytest.raises(AIProviderError) as exc_info:
                await client.generate(
                    system_prompt="System",
                    user_prompt="User",
                )

            assert "Empty response" in str(exc_info.value.message)

    @pytest.mark.asyncio
    async def test_generate_raises_on_api_error(self):
        """Test generate raises AIProviderError on API failure."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_api.messages.create.side_effect = Exception("API failure")

            client = ClaudeClient(api_key="test-key")
            with pytest.raises(AIProviderError) as exc_info:
                await client.generate(
                    system_prompt="System",
                    user_prompt="User",
                )

            assert "Failed to generate narrative" in str(exc_info.value.message)

    @pytest.mark.asyncio
    async def test_generate_default_parameters(self):
        """Test generate uses sensible defaults."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_response = Mock()
            mock_response.content = [Mock(text="Response")]
            mock_api.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            await client.generate(
                system_prompt="System",
                user_prompt="User",
            )

            call_kwargs = mock_api.messages.create.call_args.kwargs
            assert call_kwargs["max_tokens"] == 2000
            assert call_kwargs["temperature"] == 0.3


class TestClaudeClientHealthCheck:
    """Tests for the health_check method."""

    @pytest.mark.asyncio
    async def test_health_check_returns_true_on_success(self):
        """Test health check returns True on successful API call."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_response = Mock()
            mock_response.content = [Mock(text="OK")]
            mock_api.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            result = await client.health_check()

            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_returns_false_on_failure(self):
        """Test health check returns False on API failure."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_api.messages.create.side_effect = Exception("API unavailable")

            client = ClaudeClient(api_key="test-key")
            result = await client.health_check()

            assert result is False

    @pytest.mark.asyncio
    async def test_health_check_uses_minimal_tokens(self):
        """Test health check uses minimal token count."""
        with patch("cia_sie.ai.claude_client.AsyncAnthropic") as mock_anthropic:
            mock_api = Mock()
            mock_api.messages = Mock()
            mock_api.messages.create = AsyncMock()
            mock_anthropic.return_value = mock_api

            mock_response = Mock()
            mock_response.content = [Mock(text="OK")]
            mock_api.messages.create.return_value = mock_response

            client = ClaudeClient(api_key="test-key")
            await client.health_check()

            call_kwargs = mock_api.messages.create.call_args.kwargs
            assert call_kwargs["max_tokens"] == 10


class TestClaudeClientConstitutionalCompliance:
    """
    Tests verifying ClaudeClient maintains constitutional compliance.

    CRITICAL: The client must not perform aggregation, scoring, or recommendations.
    """

    def test_no_aggregation_method(self):
        """
        CRITICAL: ClaudeClient must not aggregate signals.
        """
        assert not hasattr(ClaudeClient, "aggregate_signals")
        assert not hasattr(ClaudeClient, "compute_overall_direction")
        assert not hasattr(ClaudeClient, "get_net_signal")

    def test_no_recommendation_method(self):
        """
        CRITICAL: ClaudeClient must not make recommendations.
        """
        assert not hasattr(ClaudeClient, "recommend")
        assert not hasattr(ClaudeClient, "advise")
        assert not hasattr(ClaudeClient, "suggest_action")

    def test_no_scoring_method(self):
        """
        CRITICAL: ClaudeClient must not compute scores.
        """
        assert not hasattr(ClaudeClient, "compute_confidence")
        assert not hasattr(ClaudeClient, "score_signal")
        assert not hasattr(ClaudeClient, "rate")

    def test_no_prediction_method(self):
        """
        CRITICAL: ClaudeClient must not make predictions.
        """
        assert not hasattr(ClaudeClient, "predict")
        assert not hasattr(ClaudeClient, "forecast")
        assert not hasattr(ClaudeClient, "project")

    def test_generate_is_only_text_generation(self):
        """
        Verify generate is for descriptive text only.
        """
        import inspect
        sig = inspect.signature(ClaudeClient.generate)

        # Parameters should be for text generation, not analysis
        params = list(sig.parameters.keys())
        assert "system_prompt" in params
        assert "user_prompt" in params
        assert "max_tokens" in params
        assert "temperature" in params

        # Should NOT have parameters implying analysis
        prohibited_params = ["signals", "aggregate", "confidence", "recommendation"]
        for p in prohibited_params:
            assert p not in params
