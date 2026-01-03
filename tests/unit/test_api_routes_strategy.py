"""
Tests for CIA-SIE Strategy Evaluation Routes
=============================================

Unit tests for strategy evaluation routes using mocks.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from uuid import uuid4

from fastapi import HTTPException

from cia_sie.api.routes.strategy import (
    STRATEGY_DISCLAIMER,
    StrategyEvaluationRequest,
    StrategyAnalysis,
    UsageInfo,
    StrategyEvaluationResponse,
    get_signal_context,
    build_strategy_prompt,
)


class TestStrategyModels:
    """Tests for strategy request/response models."""

    def test_strategy_evaluation_request_valid(self):
        """Test valid strategy evaluation request."""
        request = StrategyEvaluationRequest(
            scrip_id="test_instrument",
            strategy_description="I am considering entering a long position on this stock",
        )
        assert request.scrip_id == "test_instrument"
        assert len(request.strategy_description) >= 10

    def test_strategy_evaluation_request_too_short(self):
        """Test strategy description minimum length."""
        with pytest.raises(ValueError):
            StrategyEvaluationRequest(
                scrip_id="test",
                strategy_description="short",  # Less than 10 chars
            )

    def test_strategy_analysis_model(self):
        """Test StrategyAnalysis model creation."""
        analysis = StrategyAnalysis(
            alignment_with_signals="The RSI shows bullish momentum",
            contradictions_noted=["MACD contradicts RSI"],
            confirmations_noted=["RSI and Stochastic both bullish"],
            freshness_concerns=["Volume data is stale"],
        )
        assert "bullish" in analysis.alignment_with_signals
        assert len(analysis.contradictions_noted) == 1
        assert len(analysis.confirmations_noted) == 1
        assert len(analysis.freshness_concerns) == 1

    def test_usage_info_model(self):
        """Test UsageInfo model creation."""
        usage = UsageInfo(
            input_tokens=500,
            output_tokens=200,
            cost=0.005,
            model_used="claude-3-5-haiku-20241022",
        )
        assert usage.input_tokens == 500
        assert usage.output_tokens == 200
        assert usage.cost == 0.005

    def test_strategy_evaluation_response(self):
        """Test StrategyEvaluationResponse model creation."""
        response = StrategyEvaluationResponse(
            analysis=StrategyAnalysis(
                alignment_with_signals="Analysis text",
                contradictions_noted=[],
                confirmations_noted=[],
                freshness_concerns=[],
            ),
            usage=UsageInfo(
                input_tokens=100,
                output_tokens=50,
                cost=0.001,
                model_used="test-model",
            ),
        )
        assert response.disclaimer == STRATEGY_DISCLAIMER
        assert "decision is entirely yours" in response.disclaimer


class TestStrategyDisclaimer:
    """Tests for mandatory strategy disclaimer."""

    def test_disclaimer_content(self):
        """Test disclaimer contains required elements."""
        assert "NOT a recommendation" in STRATEGY_DISCLAIMER
        assert "decision is entirely yours" in STRATEGY_DISCLAIMER

    @pytest.mark.constitutional
    def test_disclaimer_no_advice(self):
        """CRITICAL: Disclaimer must not contain advisory language."""
        prohibited_phrases = [
            "you should",
            "we recommend",
            "it is advisable",
            "best to",
        ]
        for phrase in prohibited_phrases:
            assert phrase.lower() not in STRATEGY_DISCLAIMER.lower(), \
                f"CONSTITUTIONAL VIOLATION: Disclaimer contains '{phrase}'"


class TestBuildStrategyPrompt:
    """Tests for strategy prompt building."""

    def test_build_strategy_prompt_basic(self):
        """Test building prompts with basic context."""
        strategy = "I am considering entering a long position"
        context = {
            "signals": [
                {"chart": "RSI", "direction": "BULLISH", "freshness": "CURRENT"},
                {"chart": "MACD", "direction": "BEARISH", "freshness": "CURRENT"},
            ],
            "contradictions": ["RSI contradicts MACD"],
            "confirmations": [],
            "freshness_issues": [],
        }

        system_prompt, user_prompt = build_strategy_prompt(strategy, context)

        # System prompt checks
        assert "DESCRIPTIVE" in system_prompt
        assert "NEVER recommend" in system_prompt
        assert "probability of success" in system_prompt.lower()

        # User prompt checks
        assert strategy in user_prompt
        assert "BULLISH signals: 1" in user_prompt
        assert "BEARISH signals: 1" in user_prompt
        assert "RSI contradicts MACD" in user_prompt

    def test_build_strategy_prompt_with_no_signals(self):
        """Test building prompts with no signals."""
        strategy = "I am thinking about selling"
        context = {
            "signals": [],
            "contradictions": [],
            "confirmations": [],
            "freshness_issues": [],
        }

        system_prompt, user_prompt = build_strategy_prompt(strategy, context)

        assert "BULLISH signals: 0" in user_prompt
        assert "BEARISH signals: 0" in user_prompt
        assert "None detected" in user_prompt

    def test_build_strategy_prompt_counts_directions(self):
        """Test prompt correctly counts signal directions."""
        strategy = "Long position consideration"
        context = {
            "signals": [
                {"chart": "RSI", "direction": "BULLISH", "freshness": "CURRENT"},
                {"chart": "MACD", "direction": "BULLISH", "freshness": "CURRENT"},
                {"chart": "Volume", "direction": "NEUTRAL", "freshness": "CURRENT"},
                {"chart": "Stoch", "direction": None, "freshness": "UNAVAILABLE"},
            ],
            "contradictions": [],
            "confirmations": [],
            "freshness_issues": [],
        }

        _, user_prompt = build_strategy_prompt(strategy, context)

        assert "BULLISH signals: 2" in user_prompt
        assert "BEARISH signals: 0" in user_prompt
        assert "NEUTRAL signals: 1" in user_prompt
        assert "No signal: 1" in user_prompt

    @pytest.mark.constitutional
    def test_system_prompt_prohibitions(self):
        """CRITICAL: System prompt must contain constitutional prohibitions."""
        _, user_prompt = build_strategy_prompt("test", {"signals": [], "contradictions": [], "confirmations": [], "freshness_issues": []})
        system_prompt = build_strategy_prompt("test", {"signals": [], "contradictions": [], "confirmations": [], "freshness_issues": []})[0]

        required_prohibitions = [
            "NEVER recommend",
            "NEVER provide probability of success",
            "NEVER assign risk scores",
            "NEVER use words like \"should\"",
        ]

        for prohibition in required_prohibitions:
            assert prohibition in system_prompt, \
                f"CONSTITUTIONAL: Missing prohibition '{prohibition}' in system prompt"


class TestGetSignalContext:
    """Tests for get_signal_context function."""

    @pytest.mark.asyncio
    async def test_get_signal_context_empty(self):
        """Test get_signal_context with no silos."""
        mock_session = Mock()

        with patch('cia_sie.api.routes.strategy.RelationshipExposer'), \
             patch('cia_sie.api.routes.strategy.SiloRepository') as MockSiloRepo:

            mock_repo = Mock()
            mock_repo.get_by_instrument = AsyncMock(return_value=[])
            MockSiloRepo.return_value = mock_repo

            context = await get_signal_context("test_id", mock_session)

        assert context["signals"] == []
        assert context["contradictions"] == []
        assert context["confirmations"] == []
        assert context["freshness_issues"] == []

    @pytest.mark.asyncio
    async def test_get_signal_context_with_silos(self):
        """Test get_signal_context with silos and signals."""
        mock_session = Mock()
        mock_silo = Mock()
        mock_silo.silo_id = uuid4()

        with patch('cia_sie.api.routes.strategy.RelationshipExposer') as MockExposer, \
             patch('cia_sie.api.routes.strategy.SiloRepository') as MockSiloRepo:

            # Mock silo repository
            mock_silo_repo = Mock()
            mock_silo_repo.get_by_instrument = AsyncMock(return_value=[mock_silo])
            MockSiloRepo.return_value = mock_silo_repo

            # Mock relationship exposer
            mock_exposer_instance = Mock()
            mock_exposer_instance.expose_for_silo = AsyncMock(return_value={
                "charts": [
                    {
                        "chart_name": "RSI",
                        "freshness": "CURRENT",
                        "latest_signal": {"direction": "BULLISH"},
                    },
                    {
                        "chart_name": "MACD",
                        "freshness": "STALE",
                        "latest_signal": {"direction": "BEARISH"},
                    },
                ],
                "contradictions": [
                    {
                        "chart_a_name": "RSI",
                        "chart_a_direction": "BULLISH",
                        "chart_b_name": "MACD",
                        "chart_b_direction": "BEARISH",
                    }
                ],
                "confirmations": [],
            })
            MockExposer.return_value = mock_exposer_instance

            context = await get_signal_context("test_id", mock_session)

        assert len(context["signals"]) == 2
        assert len(context["contradictions"]) == 1
        assert len(context["freshness_issues"]) == 1  # MACD is STALE

    @pytest.mark.asyncio
    async def test_get_signal_context_handles_exceptions(self):
        """Test get_signal_context handles exceptions gracefully."""
        mock_session = Mock()
        mock_silo = Mock()
        mock_silo.silo_id = uuid4()

        with patch('cia_sie.api.routes.strategy.RelationshipExposer') as MockExposer, \
             patch('cia_sie.api.routes.strategy.SiloRepository') as MockSiloRepo:

            mock_silo_repo = Mock()
            mock_silo_repo.get_by_instrument = AsyncMock(return_value=[mock_silo])
            MockSiloRepo.return_value = mock_silo_repo

            # Mock exposer to raise exception
            mock_exposer_instance = Mock()
            mock_exposer_instance.expose_for_silo = AsyncMock(side_effect=Exception("Test error"))
            MockExposer.return_value = mock_exposer_instance

            # Should not raise, should return empty context
            context = await get_signal_context("test_id", mock_session)

        assert context["signals"] == []


class TestEvaluateStrategyAlignment:
    """Tests for main strategy evaluation endpoint."""

    @pytest.mark.asyncio
    async def test_evaluate_strategy_instrument_not_found(self):
        """Test evaluate_strategy returns 404 for unknown instrument."""
        from cia_sie.api.routes.strategy import evaluate_strategy_alignment

        mock_session = Mock()

        with patch('cia_sie.api.routes.strategy.InstrumentRepository') as MockInstrumentRepo:
            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=None)
            MockInstrumentRepo.return_value = mock_repo

            request = StrategyEvaluationRequest(
                scrip_id="unknown",
                strategy_description="I am considering a long position",
            )

            with pytest.raises(HTTPException) as exc_info:
                await evaluate_strategy_alignment(request, mock_session)

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_evaluate_strategy_budget_exhausted(self):
        """Test evaluate_strategy returns 503 when budget exhausted."""
        from cia_sie.api.routes.strategy import evaluate_strategy_alignment

        mock_session = Mock()
        mock_instrument = Mock()

        with patch('cia_sie.api.routes.strategy.InstrumentRepository') as MockInstrumentRepo, \
             patch('cia_sie.api.routes.strategy.UsageTracker') as MockTracker:

            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=mock_instrument)
            MockInstrumentRepo.return_value = mock_repo

            mock_tracker = Mock()
            mock_tracker.check_budget = AsyncMock(return_value={"within_budget": False})
            MockTracker.return_value = mock_tracker

            request = StrategyEvaluationRequest(
                scrip_id="test",
                strategy_description="I am considering a long position",
            )

            with pytest.raises(HTTPException) as exc_info:
                await evaluate_strategy_alignment(request, mock_session)

            assert exc_info.value.status_code == 503

    @pytest.mark.asyncio
    async def test_evaluate_strategy_unknown_model(self):
        """Test evaluate_strategy rejects unknown model."""
        from cia_sie.api.routes.strategy import evaluate_strategy_alignment

        mock_session = Mock()
        mock_instrument = Mock()

        with patch('cia_sie.api.routes.strategy.InstrumentRepository') as MockInstrumentRepo, \
             patch('cia_sie.api.routes.strategy.UsageTracker') as MockTracker, \
             patch('cia_sie.api.routes.strategy.get_model_info') as mock_get_model:

            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=mock_instrument)
            MockInstrumentRepo.return_value = mock_repo

            mock_tracker = Mock()
            mock_tracker.check_budget = AsyncMock(return_value={"within_budget": True})
            MockTracker.return_value = mock_tracker

            mock_get_model.return_value = None  # Unknown model

            request = StrategyEvaluationRequest(
                scrip_id="test",
                strategy_description="I am considering a long position",
                model="unknown-model",
            )

            with pytest.raises(HTTPException) as exc_info:
                await evaluate_strategy_alignment(request, mock_session)

            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_evaluate_strategy_ai_error(self):
        """Test evaluate_strategy handles AI generation errors."""
        from cia_sie.api.routes.strategy import evaluate_strategy_alignment

        mock_session = Mock()
        mock_instrument = Mock()
        mock_model = Mock()
        mock_model.id = "test-model"

        with patch('cia_sie.api.routes.strategy.InstrumentRepository') as MockInstrumentRepo, \
             patch('cia_sie.api.routes.strategy.UsageTracker') as MockTracker, \
             patch('cia_sie.api.routes.strategy.get_default_model') as mock_default_model, \
             patch('cia_sie.api.routes.strategy.get_signal_context') as mock_context, \
             patch('cia_sie.api.routes.strategy.ClaudeClient') as MockClient:

            mock_repo = Mock()
            mock_repo.get_by_id = AsyncMock(return_value=mock_instrument)
            MockInstrumentRepo.return_value = mock_repo

            mock_tracker = Mock()
            mock_tracker.check_budget = AsyncMock(return_value={"within_budget": True})
            MockTracker.return_value = mock_tracker

            mock_default_model.return_value = mock_model

            mock_context.return_value = {
                "signals": [],
                "contradictions": [],
                "confirmations": [],
                "freshness_issues": [],
            }

            mock_client_instance = Mock()
            mock_client_instance.generate = AsyncMock(side_effect=Exception("AI error"))
            MockClient.return_value = mock_client_instance

            request = StrategyEvaluationRequest(
                scrip_id="test",
                strategy_description="I am considering a long position",
            )

            with pytest.raises(HTTPException) as exc_info:
                await evaluate_strategy_alignment(request, mock_session)

            assert exc_info.value.status_code == 503


class TestStrategyConstitutionalCompliance:
    """Constitutional compliance tests for strategy routes."""

    @pytest.mark.constitutional
    def test_no_recommendation_in_response_model(self):
        """CRITICAL: Response model must not have recommendation field."""
        assert "recommendation" not in StrategyAnalysis.model_fields
        assert "advice" not in StrategyAnalysis.model_fields
        assert "suggested_action" not in StrategyAnalysis.model_fields

    @pytest.mark.constitutional
    def test_no_probability_in_response_model(self):
        """CRITICAL: Response model must not have probability field."""
        assert "probability" not in StrategyAnalysis.model_fields
        assert "likelihood" not in StrategyAnalysis.model_fields
        assert "success_rate" not in StrategyAnalysis.model_fields

    @pytest.mark.constitutional
    def test_no_risk_score_in_response_model(self):
        """CRITICAL: Response model must not have risk score field."""
        assert "risk_score" not in StrategyAnalysis.model_fields
        assert "risk_level" not in StrategyAnalysis.model_fields
        assert "risk" not in StrategyAnalysis.model_fields

    @pytest.mark.constitutional
    def test_response_requires_disclaimer(self):
        """CRITICAL: Response must include mandatory disclaimer."""
        assert "disclaimer" in StrategyEvaluationResponse.model_fields

    @pytest.mark.constitutional
    def test_no_scoring_methods_in_module(self):
        """CRITICAL: Strategy module must not have scoring methods."""
        import cia_sie.api.routes.strategy as strategy_module

        prohibited = ['compute_score', 'calculate_risk', 'recommend', 'advise']
        for method in prohibited:
            assert not hasattr(strategy_module, method), \
                f"CONSTITUTIONAL VIOLATION: strategy module has {method}"
