"""
CIA-SIE Exposure Layer
======================

Detects and EXPOSES signal relationships without resolution or aggregation.

GOVERNED BY: Section 0B (Analysis Definition) and Section 13 (Component Specs)

CRITICAL CONSTRAINTS:
- Contradictions are EXPOSED, never RESOLVED
- Confirmations are EXPOSED, never WEIGHTED
- NO aggregation, scoring, or recommendations anywhere
"""

from cia_sie.exposure.confirmation_detector import ConfirmationDetector
from cia_sie.exposure.contradiction_detector import ContradictionDetector
from cia_sie.exposure.relationship_exposer import RelationshipExposer

__all__ = [
    "ContradictionDetector",
    "ConfirmationDetector",
    "RelationshipExposer",
]
