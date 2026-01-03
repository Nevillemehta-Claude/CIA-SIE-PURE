"""
CIA-SIE Platform Adapters
=========================

Platform-agnostic integration layer for connecting to trading platforms.

GOVERNED BY: Section 8 (Platform-Agnostic Integration)

This module provides:
- Abstract base class for platform adapters
- Concrete adapters for TradingView, Kite, etc.
- Platform registry for adapter management
- Watchlist import functionality
"""

from cia_sie.platforms.base import (
    ConnectionStatus,
    PlatformAdapter,
    PlatformCredentials,
    PlatformInstrument,
    WatchlistInfo,
)
from cia_sie.platforms.registry import PlatformRegistry

__all__ = [
    "PlatformAdapter",
    "PlatformCredentials",
    "WatchlistInfo",
    "PlatformInstrument",
    "ConnectionStatus",
    "PlatformRegistry",
]
