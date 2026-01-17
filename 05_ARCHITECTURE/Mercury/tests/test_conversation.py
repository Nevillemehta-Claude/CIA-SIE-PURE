"""
Tests for Mercury Conversation Manager
======================================

CONSTITUTIONAL: MR-004 - Conversation Continuity
Tests verify context is maintained across turns.
"""

import pytest

from mercury.chat.conversation import Conversation, Message, ConversationManager


class TestMessage:
    """Tests for Message dataclass."""
    
    def test_message_creation(self):
        """Test message creation with defaults."""
        msg = Message(role="user", content="Hello")
        
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.timestamp is not None
        assert msg.data_context is None
    
    def test_message_to_dict(self):
        """Test message serialization."""
        msg = Message(role="assistant", content="Hi there")
        d = msg.to_dict()
        
        assert d["role"] == "assistant"
        assert d["content"] == "Hi there"
        assert "timestamp" in d


class TestConversation:
    """Tests for Conversation class."""
    
    def test_conversation_creation(self):
        """Test conversation creation with defaults."""
        conv = Conversation()
        
        assert conv.id is not None
        assert conv.messages == []
        assert conv.instrument_context == []
        assert conv.is_empty
    
    def test_add_user_message(self):
        """Test adding user message."""
        conv = Conversation()
        msg = conv.add_user_message("What's gold doing?")
        
        assert len(conv.messages) == 1
        assert conv.messages[0].role == "user"
        assert msg.content == "What's gold doing?"
    
    def test_add_assistant_message(self):
        """Test adding assistant message with data context."""
        conv = Conversation()
        data = {"quotes": {"GOLDBEES": {"ltp": 58.42}}}
        msg = conv.add_assistant_message("Gold is at 58.42", data_context=data)
        
        assert len(conv.messages) == 1
        assert conv.messages[0].role == "assistant"
        assert msg.data_context == data
    
    def test_get_history(self):
        """Test getting conversation history."""
        conv = Conversation()
        conv.add_user_message("Q1")
        conv.add_assistant_message("A1")
        conv.add_user_message("Q2")
        conv.add_assistant_message("A2")
        
        # Get all
        history = conv.get_history(limit=10)
        assert len(history) == 4
        
        # Get limited
        history = conv.get_history(limit=2)
        assert len(history) == 2
        assert history[0]["content"] == "Q2"  # Most recent 2
    
    def test_instrument_context(self):
        """Test instrument context tracking."""
        conv = Conversation()
        
        conv.update_instrument_context(["GOLDBEES", "SILVERBEES"])
        assert "GOLDBEES" in conv.instrument_context
        assert "SILVERBEES" in conv.instrument_context
        
        # Duplicate should not add again
        conv.update_instrument_context(["GOLDBEES"])
        assert conv.instrument_context.count("GOLDBEES") == 1
    
    def test_get_last_instruments(self):
        """Test getting recent instruments."""
        conv = Conversation()
        conv.update_instrument_context(["A", "B", "C", "D", "E"])
        
        last_3 = conv.get_last_instruments(3)
        assert last_3 == ["C", "D", "E"]
    
    def test_clear(self):
        """Test clearing conversation."""
        conv = Conversation()
        conv.add_user_message("Test")
        conv.update_instrument_context(["GOLDBEES"])
        
        conv.clear()
        
        assert conv.is_empty
        assert conv.instrument_context == []
    
    def test_turn_count(self):
        """Test turn counting."""
        conv = Conversation()
        conv.add_user_message("Q1")
        conv.add_assistant_message("A1")
        conv.add_user_message("Q2")
        conv.add_assistant_message("A2")
        
        assert conv.turn_count == 2


class TestConversationManager:
    """Tests for ConversationManager."""
    
    def test_create_conversation(self):
        """Test creating new conversation."""
        manager = ConversationManager()
        conv = manager.create_conversation()
        
        assert conv is not None
        assert manager.get_active_conversation() == conv
    
    def test_get_active_conversation(self):
        """Test getting active conversation (creates if none)."""
        manager = ConversationManager()
        
        # Should create new
        conv1 = manager.get_active_conversation()
        assert conv1 is not None
        
        # Should return same
        conv2 = manager.get_active_conversation()
        assert conv1.id == conv2.id
    
    def test_clear_active(self):
        """Test clearing active conversation."""
        manager = ConversationManager()
        conv = manager.get_active_conversation()
        conv.add_user_message("Test")
        
        manager.clear_active()
        
        assert manager.get_active_conversation().is_empty
