"""
Mercury Attachments Module
==========================

File attachment handling for data analysis.

Supported formats:
- CSV files (.csv)
- Excel files (.xlsx, .xls)
- JSON files (.json)
- Text files (.txt)
- Images (.png, .jpg, .jpeg) - for chart analysis
"""

from mercury.attachments.parser import (
    FileParser,
    ParsedFile,
    parse_file,
    get_supported_formats,
)
from mercury.attachments.manager import (
    AttachmentManager,
    Attachment,
    get_attachment_manager,
)

__all__ = [
    "FileParser",
    "ParsedFile",
    "parse_file",
    "get_supported_formats",
    "AttachmentManager",
    "Attachment",
    "get_attachment_manager",
]
