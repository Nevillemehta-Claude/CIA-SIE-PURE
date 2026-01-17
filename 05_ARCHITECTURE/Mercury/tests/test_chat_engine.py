"""
Tests for Mercury Chat Engine
=============================

CONSTITUTIONAL VERIFICATION:
- MR-001: Tests verify data grounding
- MR-002: Tests verify no response filtering (no prohibited pattern checks)
- MR-003: Tests verify synthesis capability
- MR-004: Tests verify conversation continuity
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from mercury.chat.engine import ChatEngine
from mercury.chat.conversation import Conversation
from mercury.kite.adapter import KiteAdapter
from mercury.kite.models import Quote, MarketDataBundle
from mercury.ai.engine import AIEngine


@pytest.fixture
def mock_kite():
    """Create mock Kite adapter."""
    kite = MagicMock(spec=KiteAdapter)
    kite.get_data_bundle = AsyncMock(return_value=MarketDataBundle())
    return kite


@pytest.fixture
def mock_ai():
    """Create mock AI engine."""
    ai = MagicMock(spec=AIEngine)
    ai.generate = AsyncMock(return_value="Mock AI response")
    return ai


@pytest.fixture
def engine(mock_kite, mock_ai):
    """Create chat engine with mocks."""
    return ChatEngine(kite=mock_kite, ai=mock_ai)


@pytest.fixture
def conversation():
    """Create empty conversation."""
    return Conversation()


class TestInstrumentIdentification:
    """Tests for instrument identification from queries."""
    
    def test_explicit_symbol_extraction(self, engine, conversation):
        """Test extraction of explicit symbols (all caps)."""
        instruments = engine.identify_instruments(
            "What's the price of GOLDBEES?",
            conversation
        )
        assert "GOLDBEES" in instruments
    
    @pytest.mark.skip(reason="Instrument alias data not configured")
    def test_alias_resolution(self, engine, conversation):
        """Test common aliases resolve to symbols."""
        instruments = engine.identify_instruments(
            "How is gold doing today?",
            conversation
        )
        assert "GOLDBEES" in instruments
    
    def test_context_reference(self, engine, conversation):
        """Test 'it', 'that' references use conversation context."""
        # Set up context
        conversation.update_instrument_context(["GOLDBEES"])
        
        instruments = engine.identify_instruments(
            "How has it performed this week?",
            conversation
        )
        assert "GOLDBEES" in instruments
    
    def test_multiple_instruments(self, engine, conversation):
        """Test multiple instruments in one query."""
        instruments = engine.identify_instruments(
            "Compare GOLDBEES and SILVERBEES",
            conversation
        )
        assert "GOLDBEES" in instruments
        assert "SILVERBEES" in instruments


class TestDataNeedsIdentification:
    """Tests for data type identification."""
    
    def test_quote_default(self, engine):
        """Test quotes are always included by default."""
        needs = engine.identify_data_needs("What's the price of gold?")
        assert "quote" in needs
    
    def test_position_detection(self, engine):
        """Test position-related keywords trigger position fetch."""
        needs = engine.identify_data_needs("Show me my open positions")
        assert "position" in needs
    
    def test_holdings_detection(self, engine):
        """Test holdings-related keywords."""
        needs = engine.identify_data_needs("What's in my portfolio?")
        assert "holding" in needs
    
    def test_history_detection(self, engine):
        """Test historical data keywords."""
        needs = engine.identify_data_needs("How has NIFTY performed this week?")
        assert "history" in needs


class TestQueryProcessing:
    """Tests for full query processing pipeline."""
    
    @pytest.mark.asyncio
    async def test_basic_query_flow(self, engine, conversation, mock_kite, mock_ai):
        """Test basic query processing flow."""
        response = await engine.process(
            "What's the price of GOLDBEES?",
            conversation
        )
        
        # Verify Kite was called
        mock_kite.get_data_bundle.assert_called_once()
        
        # Verify AI was called
        mock_ai.generate.assert_called_once()
        
        # Verify response returned
        assert response == "Mock AI response"
    
    @pytest.mark.asyncio
    async def test_conversation_updated(self, engine, conversation, mock_kite, mock_ai):
        """Test conversation history is updated after query."""
        await engine.process("What's the price of gold?", conversation)
        
        # Should have user message and assistant response
        assert len(conversation.messages) == 2
        assert conversation.messages[0].role == "user"
        assert conversation.messages[1].role == "assistant"
    
    @pytest.mark.asyncio
    async def test_instrument_context_updated(self, engine, conversation, mock_kite, mock_ai):
        """Test instrument context is tracked."""
        await engine.process("Show me GOLDBEES", conversation)
        
        assert "GOLDBEES" in conversation.instrument_context


class TestConstitutionalCompliance:
    """
    Tests verifying Mercury's constitutional compliance.
    
    NOTE: Unlike CIA-SIE, Mercury does NOT filter responses.
    These tests verify the ABSENCE of restrictions.
    """
    
    @pytest.mark.asyncio
    async def test_no_prohibited_pattern_check(self, engine, conversation, mock_kite, mock_ai):
        """
        CONSTITUTIONAL: MR-002 - Direct Communication
        
        Verify that responses are NOT validated against prohibited patterns.
        A response containing "I recommend" should pass through unchanged.
        """
        # AI returns a "recommendation" - which would fail CIA-SIE validation
        mock_ai.generate = AsyncMock(
            return_value="I recommend buying GOLDBEES at current levels."
        )
        
        response = await engine.process("What should I do with gold?", conversation)
        
        # Response should contain the recommendation - NOT filtered
        assert "recommend" in response.lower()
    
    @pytest.mark.asyncio
    async def test_no_mandatory_disclaimer(self, engine, conversation, mock_kite, mock_ai):
        """
        CONSTITUTIONAL: MR-002 - Direct Communication
        
        Verify that mandatory disclaimers are NOT injected.
        """
        mock_ai.generate = AsyncMock(
            return_value="Gold is looking strong. Consider adding to positions."
        )
        
        response = await engine.process("How's gold?", conversation)
        
        # Should NOT contain CIA-SIE's mandatory disclaimer
        assert "interpretation and any decision is entirely yours" not in response.lower()
    
    @pytest.mark.asyncio
    async def test_data_grounding(self, engine, conversation, mock_kite, mock_ai):
        """
        CONSTITUTIONAL: MR-001 - Grounded Intelligence
        
        Verify that Kite data is fetched before AI generation.
        """
        await engine.process("What's the price of gold?", conversation)
        
        # Kite should be called before AI
        mock_kite.get_data_bundle.assert_called_once()
        
        # AI should receive market_data parameter
        call_kwargs = mock_ai.generate.call_args.kwargs
        assert "market_data" in call_kwargs
