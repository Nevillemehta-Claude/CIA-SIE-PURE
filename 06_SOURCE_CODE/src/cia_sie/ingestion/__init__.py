"""
CIA-SIE Ingestion Layer
=======================

Handles signal ingestion from external platforms.
Implements platform-agnostic integration per Section 8.

CRITICAL: This layer STORES signals - it does NOT process, aggregate, or score them.
"""

from cia_sie.ingestion.freshness import FreshnessCalculator
from cia_sie.ingestion.signal_normalizer import SignalNormalizer
from cia_sie.ingestion.webhook_handler import WebhookHandler

__all__ = [
    "WebhookHandler",
    "SignalNormalizer",
    "FreshnessCalculator",
]
