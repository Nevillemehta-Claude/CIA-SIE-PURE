"""
CIA-SIE Core Module
===================

Contains domain models, enums, and core business logic.
All components here are governed by Section 0A-0D of the Gold Standard Specification.
"""

from cia_sie.core.enums import (
    BasketType,
    Direction,
    FreshnessStatus,
    SignalType,
)
from cia_sie.core.models import (
    AnalyticalBasket,
    Chart,
    ChartSignalStatus,
    Confirmation,
    Contradiction,
    Instrument,
    Narrative,
    NarrativeSection,
    RelationshipSummary,
    Signal,
    Silo,
)

__all__ = [
    # Enums
    "SignalType",
    "Direction",
    "FreshnessStatus",
    "BasketType",
    # Domain Models
    "Instrument",
    "Silo",
    "Chart",
    "Signal",
    "AnalyticalBasket",
    # Relationship Models
    "Contradiction",
    "Confirmation",
    "RelationshipSummary",
    "ChartSignalStatus",
    # Narrative Models
    "Narrative",
    "NarrativeSection",
]
