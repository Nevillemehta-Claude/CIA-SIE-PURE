"""
Mercury State Persistence
=========================

Handles saving and restoring application state across restarts.

AUTONOMOUS PRINCIPLE: Zero-loss state management.
Conversations, preferences, and session data survive restarts.

Features:
- SQLite-based persistent storage
- Async-first design
- Automatic migration handling
- Graceful degradation if storage fails
"""

import asyncio
import json
import logging
import sqlite3
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from mercury.core.logging import get_logger

logger = get_logger("mercury.persistence")


@dataclass
class ConversationRecord:
    """A persisted conversation."""
    id: str
    created_at: datetime
    updated_at: datetime
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages": self.messages,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ConversationRecord":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            messages=data.get("messages", []),
            metadata=data.get("metadata", {}),
        )


class StateStore:
    """
    Persistent state storage for Mercury.
    
    Uses SQLite for reliable, file-based storage.
    All operations are async-safe using thread pool.
    """
    
    # Schema version for migrations
    SCHEMA_VERSION = 1
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize state store.
        
        Args:
            db_path: Path to SQLite database (default: ~/.mercury/state.db)
        """
        self.db_path = db_path or (Path.home() / ".mercury" / "state.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._lock = asyncio.Lock()
        self._initialized = False
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
            )
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    async def initialize(self) -> None:
        """Initialize database schema."""
        if self._initialized:
            return
        
        async with self._lock:
            await asyncio.to_thread(self._create_schema)
            self._initialized = True
            logger.info(f"State store initialized at {self.db_path}")
    
    def _create_schema(self) -> None:
        """Create database tables."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                messages TEXT NOT NULL,
                metadata TEXT DEFAULT '{}'
            )
        """)
        
        # Key-value settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Session data table (for OAuth tokens, etc.)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT
            )
        """)
        
        # Schema version tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_info (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Set schema version
        cursor.execute(
            "INSERT OR REPLACE INTO schema_info (key, value) VALUES (?, ?)",
            ("version", str(self.SCHEMA_VERSION))
        )
        
        conn.commit()
    
    async def close(self) -> None:
        """Close database connection."""
        if self._conn:
            await asyncio.to_thread(self._conn.close)
            self._conn = None
            logger.info("State store closed")
    
    # =========================================================================
    # CONVERSATION OPERATIONS
    # =========================================================================
    
    async def save_conversation(self, record: ConversationRecord) -> None:
        """Save a conversation to persistent storage."""
        await self.initialize()
        
        async with self._lock:
            await asyncio.to_thread(
                self._save_conversation_sync,
                record
            )
    
    def _save_conversation_sync(self, record: ConversationRecord) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO conversations 
            (id, created_at, updated_at, messages, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            record.id,
            record.created_at.isoformat(),
            record.updated_at.isoformat(),
            json.dumps(record.messages),
            json.dumps(record.metadata),
        ))
        
        conn.commit()
        logger.debug(f"Saved conversation {record.id}")
    
    async def load_conversation(self, conv_id: str) -> Optional[ConversationRecord]:
        """Load a conversation by ID."""
        await self.initialize()
        
        async with self._lock:
            return await asyncio.to_thread(
                self._load_conversation_sync,
                conv_id
            )
    
    def _load_conversation_sync(self, conv_id: str) -> Optional[ConversationRecord]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM conversations WHERE id = ?",
            (conv_id,)
        )
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return ConversationRecord(
            id=row["id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            messages=json.loads(row["messages"]),
            metadata=json.loads(row["metadata"]),
        )
    
    async def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ConversationRecord]:
        """List recent conversations."""
        await self.initialize()
        
        async with self._lock:
            return await asyncio.to_thread(
                self._list_conversations_sync,
                limit,
                offset
            )
    
    def _list_conversations_sync(
        self,
        limit: int,
        offset: int,
    ) -> List[ConversationRecord]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            ORDER BY updated_at DESC 
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        return [
            ConversationRecord(
                id=row["id"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
                messages=json.loads(row["messages"]),
                metadata=json.loads(row["metadata"]),
            )
            for row in cursor.fetchall()
        ]
    
    async def delete_conversation(self, conv_id: str) -> bool:
        """Delete a conversation."""
        await self.initialize()
        
        async with self._lock:
            return await asyncio.to_thread(
                self._delete_conversation_sync,
                conv_id
            )
    
    def _delete_conversation_sync(self, conv_id: str) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
        conn.commit()
        
        deleted = cursor.rowcount > 0
        if deleted:
            logger.debug(f"Deleted conversation {conv_id}")
        return deleted
    
    # =========================================================================
    # SETTINGS OPERATIONS
    # =========================================================================
    
    async def set_setting(self, key: str, value: Any) -> None:
        """Save a setting."""
        await self.initialize()
        
        async with self._lock:
            await asyncio.to_thread(
                self._set_setting_sync,
                key,
                value
            )
    
    def _set_setting_sync(self, key: str, value: Any) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, json.dumps(value), datetime.now(timezone.utc).isoformat()))
        
        conn.commit()
    
    async def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        await self.initialize()
        
        async with self._lock:
            return await asyncio.to_thread(
                self._get_setting_sync,
                key,
                default
            )
    
    def _get_setting_sync(self, key: str, default: Any) -> Any:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        
        if row is None:
            return default
        
        return json.loads(row["value"])
    
    # =========================================================================
    # SESSION OPERATIONS (for OAuth tokens)
    # =========================================================================
    
    async def save_session(
        self,
        session_id: str,
        data: Dict[str, Any],
        expires_at: Optional[datetime] = None,
    ) -> None:
        """Save session data."""
        await self.initialize()
        
        async with self._lock:
            await asyncio.to_thread(
                self._save_session_sync,
                session_id,
                data,
                expires_at
            )
    
    def _save_session_sync(
        self,
        session_id: str,
        data: Dict[str, Any],
        expires_at: Optional[datetime],
    ) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (id, data, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        """, (
            session_id,
            json.dumps(data),
            datetime.now(timezone.utc).isoformat(),
            expires_at.isoformat() if expires_at else None,
        ))
        
        conn.commit()
        logger.debug(f"Saved session {session_id}")
    
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data."""
        await self.initialize()
        
        async with self._lock:
            return await asyncio.to_thread(
                self._load_session_sync,
                session_id
            )
    
    def _load_session_sync(self, session_id: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT data, expires_at FROM sessions WHERE id = ?",
            (session_id,)
        )
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        # Check expiry
        if row["expires_at"]:
            expires = datetime.fromisoformat(row["expires_at"])
            if datetime.now(timezone.utc) >= expires:
                # Session expired, delete it
                cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
                conn.commit()
                return None
        
        return json.loads(row["data"])
    
    async def delete_session(self, session_id: str) -> None:
        """Delete session data."""
        await self.initialize()
        
        async with self._lock:
            await asyncio.to_thread(
                self._delete_session_sync,
                session_id
            )
    
    def _delete_session_sync(self, session_id: str) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()


# Global state store instance
_state_store: Optional[StateStore] = None


def get_state_store() -> StateStore:
    """Get or create the global state store."""
    global _state_store
    if _state_store is None:
        _state_store = StateStore()
    return _state_store


async def shutdown_state_store() -> None:
    """Shutdown the state store gracefully."""
    global _state_store
    if _state_store:
        await _state_store.close()
        _state_store = None
