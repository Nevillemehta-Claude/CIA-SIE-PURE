"""
Tests for Mercury State Persistence
===================================

Tests for the persistence module that handles saving/restoring state.
"""

import asyncio
import json
import pytest
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from mercury.core.persistence import (
    StateStore,
    ConversationRecord,
    get_state_store,
)


class TestConversationRecord:
    """Tests for ConversationRecord dataclass."""
    
    def test_create_record(self):
        """Test creating a conversation record."""
        record = ConversationRecord(
            id="test-conv-1",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            messages=[
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
            metadata={"topic": "greeting"},
        )
        
        assert record.id == "test-conv-1"
        assert len(record.messages) == 2
        assert record.metadata["topic"] == "greeting"
    
    def test_to_dict(self):
        """Test serialization to dict."""
        now = datetime.now(timezone.utc)
        record = ConversationRecord(
            id="test-conv-2",
            created_at=now,
            updated_at=now,
            messages=[{"role": "user", "content": "Test"}],
        )
        
        data = record.to_dict()
        
        assert data["id"] == "test-conv-2"
        assert data["created_at"] == now.isoformat()
        assert data["updated_at"] == now.isoformat()
        assert len(data["messages"]) == 1
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        now = datetime.now(timezone.utc)
        data = {
            "id": "test-conv-3",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "messages": [{"role": "user", "content": "Hello"}],
            "metadata": {"key": "value"},
        }
        
        record = ConversationRecord.from_dict(data)
        
        assert record.id == "test-conv-3"
        assert record.messages[0]["role"] == "user"
        assert record.metadata["key"] == "value"


class TestStateStore:
    """Tests for StateStore."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir) / "test_state.db"
    
    @pytest.fixture
    def store(self, temp_db):
        """Create a StateStore with temporary database."""
        return StateStore(db_path=temp_db)
    
    @pytest.mark.asyncio
    async def test_initialize(self, store):
        """Test database initialization."""
        await store.initialize()
        
        assert store._initialized
        assert store.db_path.exists()
    
    @pytest.mark.asyncio
    async def test_save_and_load_conversation(self, store):
        """Test saving and loading a conversation."""
        await store.initialize()
        
        record = ConversationRecord(
            id="conv-save-test",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            messages=[
                {"role": "user", "content": "What's NIFTY?"},
                {"role": "assistant", "content": "NIFTY 50 is..."},
            ],
        )
        
        await store.save_conversation(record)
        loaded = await store.load_conversation("conv-save-test")
        
        assert loaded is not None
        assert loaded.id == "conv-save-test"
        assert len(loaded.messages) == 2
    
    @pytest.mark.asyncio
    async def test_list_conversations(self, store):
        """Test listing conversations."""
        await store.initialize()
        
        # Save multiple conversations
        for i in range(5):
            record = ConversationRecord(
                id=f"conv-list-{i}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc) + timedelta(seconds=i),
                messages=[],
            )
            await store.save_conversation(record)
        
        conversations = await store.list_conversations(limit=3)
        
        assert len(conversations) == 3
        # Should be ordered by updated_at DESC
        assert conversations[0].id == "conv-list-4"
    
    @pytest.mark.asyncio
    async def test_delete_conversation(self, store):
        """Test deleting a conversation."""
        await store.initialize()
        
        record = ConversationRecord(
            id="conv-delete-test",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            messages=[],
        )
        await store.save_conversation(record)
        
        deleted = await store.delete_conversation("conv-delete-test")
        assert deleted
        
        loaded = await store.load_conversation("conv-delete-test")
        assert loaded is None
    
    @pytest.mark.asyncio
    async def test_settings(self, store):
        """Test setting and getting settings."""
        await store.initialize()
        
        await store.set_setting("theme", "dark")
        await store.set_setting("user_prefs", {"lang": "en", "timezone": "IST"})
        
        theme = await store.get_setting("theme")
        prefs = await store.get_setting("user_prefs")
        missing = await store.get_setting("missing", "default")
        
        assert theme == "dark"
        assert prefs["lang"] == "en"
        assert missing == "default"
    
    @pytest.mark.asyncio
    async def test_session_storage(self, store):
        """Test session save/load."""
        await store.initialize()
        
        session_data = {
            "access_token": "test_token_123",
            "user_id": "user123",
        }
        
        await store.save_session("kite_session", session_data)
        loaded = await store.load_session("kite_session")
        
        assert loaded is not None
        assert loaded["access_token"] == "test_token_123"
    
    @pytest.mark.asyncio
    async def test_session_expiry(self, store):
        """Test that expired sessions return None."""
        await store.initialize()
        
        # Save with past expiry
        expired_at = datetime.now(timezone.utc) - timedelta(hours=1)
        await store.save_session(
            "expired_session",
            {"data": "test"},
            expires_at=expired_at,
        )
        
        loaded = await store.load_session("expired_session")
        assert loaded is None
    
    @pytest.mark.asyncio
    async def test_close(self, store):
        """Test closing the store."""
        await store.initialize()
        await store.close()
        
        assert store._conn is None


class TestIntentResolver:
    """Tests for the LLM-driven intent resolver."""
    
    @pytest.mark.asyncio
    async def test_fallback_extraction_market(self):
        """Test fallback extraction for market queries."""
        from mercury.ai.intent import IntentResolver
        
        resolver = IntentResolver()
        result = resolver._fallback_extraction("What's the market doing?")
        
        assert "NIFTY 50" in result.symbols
        assert result.confidence == 0.3  # Fallback confidence
    
    @pytest.mark.asyncio
    async def test_fallback_extraction_positions(self):
        """Test fallback extraction for position queries."""
        from mercury.ai.intent import IntentResolver
        
        resolver = IntentResolver()
        result = resolver._fallback_extraction("Show my P&L")
        
        assert "positions" in result.data_types
    
    @pytest.mark.asyncio
    async def test_fallback_extraction_holdings(self):
        """Test fallback extraction for holdings queries."""
        from mercury.ai.intent import IntentResolver
        
        resolver = IntentResolver()
        result = resolver._fallback_extraction("What's in my portfolio?")
        
        assert "holdings" in result.data_types
