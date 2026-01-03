"""
Tests for CIA-SIE Chat API Routes
=================================

Unit tests for per-instrument chat routes.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, UTC
from uuid import uuid4

from fastapi import HTTPException
from pydantic import ValidationError

from cia_sie.api.routes.chat import (
    MANDATORY_DISCLAIMER,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    UsageInfo,
    ContextInfo,
    ConversationSummary,
)


class TestChatModels:
    """Tests for chat request/response models."""

    def test_chat_message_creation(self):
        """Test ChatMessage model creation."""
        msg = ChatMessage(
            role="user",
            content="What are the signals showing?",
            timestamp="2025-01-01T00:00:00Z",
        )
        assert msg.role == "user"
        assert "signals" in msg.content

    def test_chat_message_without_timestamp(self):
        """Test ChatMessage without timestamp."""
        msg = ChatMessage(
            role="assistant",
            content="The RSI is showing bullish momentum.",
        )
        assert msg.timestamp is None

    def test_chat_request_valid(self):
        """Test valid ChatRequest creation."""
        request = ChatRequest(
            message="Tell me about the charts",
            model="claude-3-5-haiku-20241022",
            include_context=True,
        )
        assert request.message == "Tell me about the charts"
        assert request.include_context is True

    def test_chat_request_minimum_message(self):
        """Test ChatRequest with minimum length message."""
        request = ChatRequest(message="x")  # Minimum 1 char
        assert len(request.message) == 1

    def test_chat_request_empty_message_fails(self):
        """Test ChatRequest rejects empty message."""
        with pytest.raises(ValidationError):
            ChatRequest(message="")

    def test_usage_info_creation(self):
        """Test UsageInfo model creation."""
        usage = UsageInfo(
            input_tokens=500,
            output_tokens=200,
            cost=0.005,
            model_used="claude-3-5-haiku-20241022",
        )
        assert usage.input_tokens == 500
        assert usage.cost == 0.005

    def test_context_info_creation(self):
        """Test ContextInfo model creation."""
        context = ContextInfo(
            signals_included=5,
            charts_referenced=["RSI", "MACD", "Volume"],
        )
        assert context.signals_included == 5
        assert len(context.charts_referenced) == 3

    def test_chat_response_has_disclaimer(self):
        """Test ChatResponse includes mandatory disclaimer."""
        response = ChatResponse(
            conversation_id="conv_123",
            message=ChatMessage(role="assistant", content="Test response"),
            usage=UsageInfo(
                input_tokens=100,
                output_tokens=50,
                cost=0.001,
                model_used="test-model",
            ),
        )
        assert response.disclaimer == MANDATORY_DISCLAIMER

    def test_conversation_summary_creation(self):
        """Test ConversationSummary model creation."""
        summary = ConversationSummary(
            conversation_id="conv_123",
            messages=[
                ChatMessage(role="user", content="Hello"),
                ChatMessage(role="assistant", content="Hi there"),
            ],
            created_at="2025-01-01T00:00:00Z",
            total_tokens=100,
            total_cost=0.001,
        )
        assert len(summary.messages) == 2
        assert summary.total_tokens == 100
        assert summary.total_cost == 0.001


class TestMandatoryDisclaimer:
    """Tests for mandatory disclaimer content."""

    def test_disclaimer_content(self):
        """Test disclaimer contains required elements."""
        assert "description" in MANDATORY_DISCLAIMER.lower()
        assert "yours" in MANDATORY_DISCLAIMER.lower()

    @pytest.mark.constitutional
    def test_disclaimer_no_advice(self):
        """CRITICAL: Disclaimer must not contain advisory language."""
        prohibited = ["you should", "we recommend", "it is advisable", "you must"]
        for phrase in prohibited:
            assert phrase.lower() not in MANDATORY_DISCLAIMER.lower(), \
                f"CONSTITUTIONAL VIOLATION: Disclaimer contains '{phrase}'"


class TestGetInstrumentContext:
    """Tests for get_instrument_context helper function."""

    @pytest.mark.asyncio
    async def test_get_instrument_context_basic(self):
        """Test get_instrument_context returns context tuple."""
        from cia_sie.api.routes.chat import get_instrument_context

        mock_session = Mock()

        with patch('cia_sie.api.routes.chat.RelationshipExposer') as MockExposer, \
             patch('cia_sie.api.routes.chat.SiloRepository') as MockSiloRepo:

            mock_silo_repo = Mock()
            mock_silo_repo.get_by_instrument = AsyncMock(return_value=[])
            MockSiloRepo.return_value = mock_silo_repo

            # The function returns a tuple of (context_string, chart_codes, signal_count)
            result = await get_instrument_context("inst_id", mock_session)

        assert isinstance(result, tuple)
        assert len(result) == 3


class TestBuildSystemPrompt:
    """Tests verifying chat system prompt content."""

    def test_build_system_prompt_with_context(self):
        """Test the system prompt contains context and prohibitions."""
        from cia_sie.api.routes.chat import build_system_prompt

        context = "RSI is showing BULLISH. MACD is BEARISH."
        system_prompt = build_system_prompt(include_context=True, context=context)

        # System prompt should contain constitutional constraints
        assert "descriptive" in system_prompt.lower()
        assert "NEVER" in system_prompt
        # Context should be included
        assert context in system_prompt

    def test_build_system_prompt_without_context(self):
        """Test the system prompt without context."""
        from cia_sie.api.routes.chat import build_system_prompt

        system_prompt = build_system_prompt(include_context=False, context="")

        # Should still contain constitutional constraints
        assert "descriptive" in system_prompt.lower()
        assert "NEVER" in system_prompt

    @pytest.mark.constitutional
    def test_system_prompt_prohibitions(self):
        """CRITICAL: System prompt must include constitutional prohibitions."""
        from cia_sie.api.routes.chat import build_system_prompt

        system_prompt = build_system_prompt(include_context=True, context="Test")

        # Check for prohibition phrases
        assert "recommend" in system_prompt.lower() or "NEVER" in system_prompt


class TestChatEndpoint:
    """Tests for main chat endpoint."""

    @pytest.mark.asyncio
    async def test_send_chat_message_instrument_not_found(self):
        """Test chat endpoint returns 404 for unknown instrument."""
        from cia_sie.api.routes.chat import send_chat_message

        mock_session = Mock()

        with patch('cia_sie.api.routes.chat.InstrumentRepository') as MockRepo:
            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=None)
            MockRepo.return_value = mock_repo

            request = ChatRequest(message="Hello")

            with pytest.raises(HTTPException) as exc_info:
                await send_chat_message("unknown", request, mock_session)

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_send_chat_message_budget_exhausted(self):
        """Test chat endpoint returns 503 when budget exhausted."""
        from cia_sie.api.routes.chat import send_chat_message

        mock_session = Mock()
        mock_instrument = Mock()

        with patch('cia_sie.api.routes.chat.InstrumentRepository') as MockRepo, \
             patch('cia_sie.api.routes.chat.UsageTracker') as MockTracker:

            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=mock_instrument)
            MockRepo.return_value = mock_repo

            mock_tracker = Mock()
            mock_tracker.check_budget = AsyncMock(return_value={"within_budget": False})
            MockTracker.return_value = mock_tracker

            request = ChatRequest(message="Hello")

            with pytest.raises(HTTPException) as exc_info:
                await send_chat_message("inst_id", request, mock_session)

            assert exc_info.value.status_code == 503


class TestGetChatHistory:
    """Tests for get_chat_history endpoint."""

    @pytest.mark.asyncio
    async def test_get_history_instrument_not_found(self):
        """Test get_history returns 404 for unknown instrument."""
        from cia_sie.api.routes.chat import get_chat_history

        mock_session = Mock()

        with patch('cia_sie.api.routes.chat.InstrumentRepository') as MockRepo:
            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=None)
            MockRepo.return_value = mock_repo

            with pytest.raises(HTTPException) as exc_info:
                await get_chat_history("unknown", mock_session)

            assert exc_info.value.status_code == 404


class TestChatConstitutionalCompliance:
    """Constitutional compliance tests for chat routes."""

    @pytest.mark.constitutional
    def test_chat_response_no_recommendation_field(self):
        """CRITICAL: ChatResponse must not have recommendation field."""
        assert "recommendation" not in ChatResponse.model_fields
        assert "advice" not in ChatResponse.model_fields
        assert "suggested_action" not in ChatResponse.model_fields

    @pytest.mark.constitutional
    def test_chat_response_no_score_field(self):
        """CRITICAL: ChatResponse must not have score field."""
        assert "score" not in ChatResponse.model_fields
        assert "confidence" not in ChatResponse.model_fields
        assert "probability" not in ChatResponse.model_fields

    @pytest.mark.constitutional
    def test_chat_response_requires_disclaimer(self):
        """CRITICAL: ChatResponse must include mandatory disclaimer."""
        assert "disclaimer" in ChatResponse.model_fields

    @pytest.mark.constitutional
    def test_no_scoring_methods_in_chat_module(self):
        """CRITICAL: Chat module must not have scoring methods."""
        import cia_sie.api.routes.chat as chat_module

        prohibited = [
            'recommend', 'compute_score', 'calculate_confidence',
            'aggregate_signals', 'generate_recommendation',
        ]

        for method in prohibited:
            assert not hasattr(chat_module, method), \
                f"CONSTITUTIONAL VIOLATION: chat module has {method}"

    @pytest.mark.constitutional
    def test_chat_message_no_confidence_field(self):
        """CRITICAL: ChatMessage must not have confidence field."""
        assert "confidence" not in ChatMessage.model_fields
        assert "score" not in ChatMessage.model_fields
