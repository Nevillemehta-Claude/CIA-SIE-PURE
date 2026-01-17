"""
Mercury Attachment Manager
==========================

Manages file attachments for conversations.

Features:
- Upload and store attachments
- Associate attachments with conversations
- Cleanup old attachments
- Size limits and validation
"""

import asyncio
import hashlib
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

from mercury.attachments.parser import FileParser, ParsedFile, parse_file
from mercury.core.logging import get_logger

logger = get_logger("mercury.attachments.manager")


@dataclass
class Attachment:
    """An uploaded attachment."""
    id: str
    filename: str
    size_bytes: int
    mime_type: Optional[str]
    uploaded_at: datetime
    conversation_id: Optional[str] = None
    
    # Parsed content
    parsed: Optional[ParsedFile] = None
    
    # Storage path
    storage_path: Optional[Path] = None
    
    # Hash for deduplication
    content_hash: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "size_bytes": self.size_bytes,
            "mime_type": self.mime_type,
            "uploaded_at": self.uploaded_at.isoformat(),
            "conversation_id": self.conversation_id,
            "has_parsed": self.parsed is not None,
            "summary": self.parsed.summary if self.parsed else None,
        }


class AttachmentManager:
    """
    Manages file attachments for Mercury.
    
    Usage:
        manager = AttachmentManager()
        attachment = await manager.upload(file_content, filename)
        context = manager.get_context(attachment.id)
    """
    
    # Maximum attachment size (10 MB)
    MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024
    
    # Maximum attachments per conversation
    MAX_PER_CONVERSATION = 10
    
    # Attachment TTL (24 hours)
    ATTACHMENT_TTL = timedelta(hours=24)
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize attachment manager.
        
        Args:
            storage_dir: Directory for storing attachments (default: ~/.mercury/attachments)
        """
        self.storage_dir = storage_dir or (Path.home() / ".mercury" / "attachments")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self._attachments: Dict[str, Attachment] = {}
        self._by_conversation: Dict[str, List[str]] = {}
        self._parser = FileParser()
        self._lock = asyncio.Lock()
    
    async def upload(
        self,
        content: bytes,
        filename: str,
        mime_type: Optional[str] = None,
        conversation_id: Optional[str] = None,
    ) -> Attachment:
        """
        Upload and process an attachment.
        
        Args:
            content: File content bytes
            filename: Original filename
            mime_type: MIME type (optional)
            conversation_id: Associated conversation (optional)
        
        Returns:
            Attachment object with parsed content
        
        Raises:
            ValueError: If file is too large or invalid
        """
        # Validate size
        if len(content) > self.MAX_ATTACHMENT_SIZE:
            raise ValueError(
                f"File too large. Maximum size is {self.MAX_ATTACHMENT_SIZE // (1024*1024)} MB"
            )
        
        # Check conversation limits
        if conversation_id:
            async with self._lock:
                conv_attachments = self._by_conversation.get(conversation_id, [])
                if len(conv_attachments) >= self.MAX_PER_CONVERSATION:
                    raise ValueError(
                        f"Maximum {self.MAX_PER_CONVERSATION} attachments per conversation"
                    )
        
        # Generate ID and hash
        attachment_id = str(uuid.uuid4())[:12]
        content_hash = hashlib.sha256(content).hexdigest()[:16]
        
        # Parse file
        parsed = await self._parser.parse(content, filename, mime_type)
        
        # Create attachment
        attachment = Attachment(
            id=attachment_id,
            filename=filename,
            size_bytes=len(content),
            mime_type=mime_type,
            uploaded_at=datetime.now(timezone.utc),
            conversation_id=conversation_id,
            parsed=parsed,
            content_hash=content_hash,
        )
        
        # Store file (for large files or images that need persistence)
        if len(content) > 1024 * 100:  # > 100KB
            storage_path = self.storage_dir / f"{attachment_id}_{filename}"
            storage_path.write_bytes(content)
            attachment.storage_path = storage_path
        
        # Track attachment
        async with self._lock:
            self._attachments[attachment_id] = attachment
            if conversation_id:
                if conversation_id not in self._by_conversation:
                    self._by_conversation[conversation_id] = []
                self._by_conversation[conversation_id].append(attachment_id)
        
        logger.info(
            f"Attachment uploaded: {filename}",
            context={
                "id": attachment_id,
                "size": len(content),
                "type": parsed.file_type.value,
                "conversation": conversation_id,
            }
        )
        
        return attachment
    
    def get(self, attachment_id: str) -> Optional[Attachment]:
        """Get attachment by ID."""
        return self._attachments.get(attachment_id)
    
    def get_for_conversation(self, conversation_id: str) -> List[Attachment]:
        """Get all attachments for a conversation."""
        attachment_ids = self._by_conversation.get(conversation_id, [])
        return [
            self._attachments[aid]
            for aid in attachment_ids
            if aid in self._attachments
        ]
    
    def get_context(self, attachment_id: str) -> Optional[str]:
        """
        Get AI context string for an attachment.
        
        Returns formatted context that can be included in AI prompts.
        """
        attachment = self.get(attachment_id)
        if attachment and attachment.parsed:
            return attachment.parsed.to_ai_context()
        return None
    
    def get_all_context(self, conversation_id: str) -> str:
        """Get combined context for all attachments in a conversation."""
        attachments = self.get_for_conversation(conversation_id)
        if not attachments:
            return ""
        
        contexts = []
        for att in attachments:
            if att.parsed:
                contexts.append(att.parsed.to_ai_context())
        
        if contexts:
            return "\n\n---\n\n".join(contexts)
        return ""
    
    def get_image_for_vision(self, attachment_id: str) -> Optional[Dict]:
        """
        Get image data formatted for Claude vision API.
        
        Returns dict with type, media_type, and data for Claude's image format.
        """
        attachment = self.get(attachment_id)
        if not attachment or not attachment.parsed:
            return None
        
        parsed = attachment.parsed
        if parsed.image_base64 and parsed.image_mime_type:
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": parsed.image_mime_type,
                    "data": parsed.image_base64,
                }
            }
        return None
    
    async def delete(self, attachment_id: str) -> bool:
        """Delete an attachment."""
        async with self._lock:
            if attachment_id not in self._attachments:
                return False
            
            attachment = self._attachments[attachment_id]
            
            # Remove from conversation tracking
            if attachment.conversation_id:
                conv_list = self._by_conversation.get(attachment.conversation_id, [])
                if attachment_id in conv_list:
                    conv_list.remove(attachment_id)
            
            # Delete stored file
            if attachment.storage_path and attachment.storage_path.exists():
                attachment.storage_path.unlink()
            
            del self._attachments[attachment_id]
            logger.info(f"Attachment deleted: {attachment_id}")
            return True
    
    async def cleanup_expired(self) -> int:
        """
        Remove expired attachments.
        
        Returns number of attachments removed.
        """
        now = datetime.now(timezone.utc)
        expired = []
        
        async with self._lock:
            for aid, attachment in self._attachments.items():
                if now - attachment.uploaded_at > self.ATTACHMENT_TTL:
                    expired.append(aid)
        
        for aid in expired:
            await self.delete(aid)
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired attachments")
        
        return len(expired)
    
    def list_all(self) -> List[dict]:
        """List all attachments as dictionaries."""
        return [att.to_dict() for att in self._attachments.values()]


# Global attachment manager
_manager: Optional[AttachmentManager] = None


def get_attachment_manager() -> AttachmentManager:
    """Get the global attachment manager."""
    global _manager
    if _manager is None:
        _manager = AttachmentManager()
    return _manager
