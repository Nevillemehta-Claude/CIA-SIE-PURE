"""
Mercury Conversation Manager
============================

Manages conversation state and history.

CONSTITUTIONAL: MR-004 - Conversation Continuity
This module maintains context across conversation turns.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4


def _utc_now() -> datetime:
    """Return current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


@dataclass
class Message:
    """Single conversation message."""
    
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=_utc_now)
    data_context: Optional[dict] = None  # Market data used for this message
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API calls."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class Conversation:
    """
    Conversation session with history.
    
    CONSTITUTIONAL: MR-004 - Maintains context across turns.
    """
    
    id: str = field(default_factory=lambda: str(uuid4()))
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=_utc_now)
    instrument_context: list[str] = field(default_factory=list)
    
    def add_user_message(self, content: str) -> Message:
        """Add a user message to the conversation."""
        msg = Message(role="user", content=content)
        self.messages.append(msg)
        return msg
    
    def add_assistant_message(
        self,
        content: str,
        data_context: Optional[dict] = None,
    ) -> Message:
        """Add an assistant message to the conversation."""
        msg = Message(
            role="assistant",
            content=content,
            data_context=data_context,
        )
        self.messages.append(msg)
        return msg
    
    def get_history(self, limit: int = 10) -> list[dict]:
        """
        Get recent conversation history.
        
        Args:
            limit: Maximum messages to return
            
        Returns:
            List of message dicts for API consumption
        """
        recent = self.messages[-limit:] if limit else self.messages
        return [msg.to_dict() for msg in recent]
    
    def update_instrument_context(self, instruments: list[str]) -> None:
        """Update the instruments mentioned in conversation."""
        for inst in instruments:
            if inst not in self.instrument_context:
                self.instrument_context.append(inst)
    
    def get_last_instruments(self, n: int = 5) -> list[str]:
        """Get the most recently mentioned instruments."""
        return self.instrument_context[-n:]
    
    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []
        self.instrument_context = []
    
    @property
    def turn_count(self) -> int:
        """Number of conversation turns (user messages)."""
        return len([m for m in self.messages if m.role == "user"])
    
    @property
    def is_empty(self) -> bool:
        """Check if conversation has no messages."""
        return len(self.messages) == 0


class ConversationManager:
    """
    Manages multiple conversation sessions.
    
    For Mercury v1, we only track a single conversation,
    but this structure allows for future expansion.
    """
    
    def __init__(self):
        self._conversations: dict[str, Conversation] = {}
        self._active_id: Optional[str] = None
    
    def create_conversation(self) -> Conversation:
        """Create a new conversation."""
        conv = Conversation()
        self._conversations[conv.id] = conv
        self._active_id = conv.id
        return conv
    
    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        """Get conversation by ID."""
        return self._conversations.get(conv_id)
    
    def get_active_conversation(self) -> Conversation:
        """Get the active conversation, creating if needed."""
        if self._active_id and self._active_id in self._conversations:
            return self._conversations[self._active_id]
        return self.create_conversation()
    
    def clear_active(self) -> None:
        """Clear the active conversation."""
        conv = self.get_active_conversation()
        conv.clear()
