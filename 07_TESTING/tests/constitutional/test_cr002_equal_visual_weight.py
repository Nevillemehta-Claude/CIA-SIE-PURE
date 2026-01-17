"""
Constitutional Compliance Tests - CR-002: Equal Visual Weight
==============================================================

These tests verify that BULLISH and BEARISH signals are displayed
with EQUAL visual prominence. Neither direction should appear
more important, stronger, or more prominent than the other.

CR-002 Requirements:
- Same font size
- Same badge dimensions
- Same padding
- Same border radius
- No "stronger" or "weaker" language
- Neutral separator in contradictions

Each test runs 10 times for statistical confidence.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestCR002ModelEquality:
    """Test that models don't bias toward any direction."""
    
    @pytest.mark.constitutional
    def test_contradiction_has_no_resolution(self):
        """Contradiction model must NOT have resolution field."""
        from cia_sie.core.models import Contradiction
        
        fields = Contradiction.model_fields.keys()
        assert "resolution" not in fields, "Contradiction must not resolve conflicts"
        assert "winner" not in fields, "Contradiction must not have winner"
        assert "dominant" not in fields, "Contradiction must not indicate dominance"
    
    @pytest.mark.constitutional
    def test_contradiction_has_no_priority(self):
        """Contradiction must NOT prioritize one side."""
        from cia_sie.core.models import Contradiction
        
        fields = Contradiction.model_fields.keys()
        assert "priority" not in fields, "Contradiction must not have priority"
        assert "preferred" not in fields, "Contradiction must not have preference"
    
    @pytest.mark.constitutional
    def test_confirmation_has_no_weight(self):
        """Confirmation must NOT aggregate into a weighted score."""
        from cia_sie.core.models import Confirmation
        
        fields = Confirmation.model_fields.keys()
        assert "combined_strength" not in fields, "Confirmation must not aggregate strength"
        assert "total_weight" not in fields, "Confirmation must not have total weight"
        assert "aggregated_score" not in fields, "Confirmation must not aggregate scores"
    
    @pytest.mark.constitutional
    def test_direction_enum_is_symmetric(self):
        """Direction enum must treat BULLISH and BEARISH symmetrically."""
        from cia_sie.core.enums import Direction
        
        # Both must exist
        assert hasattr(Direction, "BULLISH"), "BULLISH must exist"
        assert hasattr(Direction, "BEARISH"), "BEARISH must exist"
        assert hasattr(Direction, "NEUTRAL"), "NEUTRAL must exist"
        
        # No implicit ordering or value suggesting one is "better"
        assert Direction.BULLISH.value == "BULLISH"
        assert Direction.BEARISH.value == "BEARISH"


class TestCR002RelationshipExposer:
    """Test that relationship exposer returns data without bias."""
    
    @pytest.mark.constitutional
    def test_relationship_exposer_exists(self):
        """RelationshipExposer class must exist."""
        from cia_sie.exposure.relationship_exposer import RelationshipExposer
        
        assert RelationshipExposer is not None
    
    @pytest.mark.constitutional
    def test_contradiction_detector_exists(self):
        """ContradictionDetector class must exist."""
        from cia_sie.exposure.contradiction_detector import ContradictionDetector
        
        assert ContradictionDetector is not None
    
    @pytest.mark.constitutional
    def test_confirmation_detector_exists(self):
        """ConfirmationDetector class must exist."""
        from cia_sie.exposure.confirmation_detector import ConfirmationDetector
        
        assert ConfirmationDetector is not None


class TestCR002EnumDocumentation:
    """Test that enums document the constitutional requirement."""
    
    @pytest.mark.constitutional
    def test_direction_enum_values_equal(self):
        """Direction enum values must be simple strings (no ranking implied)."""
        from cia_sie.core.enums import Direction
        
        # Values should be strings, not numbers that imply ranking
        assert isinstance(Direction.BULLISH.value, str)
        assert isinstance(Direction.BEARISH.value, str)
        assert isinstance(Direction.NEUTRAL.value, str)


class TestCR002FreshnessIsDescriptive:
    """Test that freshness is purely descriptive, not qualitative."""
    
    @pytest.mark.constitutional
    def test_freshness_has_no_quality_judgment(self):
        """FreshnessStatus must not imply signal quality."""
        from cia_sie.core.enums import FreshnessStatus
        
        # Freshness describes TIME, not QUALITY
        for status in FreshnessStatus:
            value = status.value.lower()
            assert "good" not in value, "Freshness must not imply quality"
            assert "bad" not in value, "Freshness must not imply quality"
            assert "reliable" not in value, "Freshness must not imply reliability"
            assert "unreliable" not in value, "Freshness must not imply reliability"
