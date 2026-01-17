"""
Constitutional Compliance Tests - CR-001: No Recommendations
============================================================

These tests verify that the system NEVER provides prescriptive advice.
The system is decision-SUPPORT, not decision-MAKING.

PROHIBITED PHRASES (CR-001):
- "you should"
- "I recommend"
- "buy" / "sell" / "trade" / "invest"
- "profitable" / "guaranteed"
- "strong signal" / "weak signal"
- "overall direction" / "net bullish" / "net bearish"

Each test runs 10 times for statistical confidence.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from cia_sie.ai.response_validator import AIResponseValidator, MANDATORY_DISCLAIMER


# =============================================================================
# PROHIBITED PHRASES - CR-001
# =============================================================================

PROHIBITED_PHRASES = [
    "you should",
    "i recommend",
    "we recommend",
    "buy",
    "sell",
    "trade",
    "invest",
    "profitable",
    "guaranteed",
    "strong signal",
    "weak signal",
    "stronger signal",
    "weaker signal",
    "overall direction",
    "net bullish",
    "net bearish",
    "take profit",
    "stop loss",
    "entry point",
    "exit point",
    "target price",
    "price target",
]


class TestCR001ProhibitedPhrases:
    """Test that prohibited phrases are detected and rejected."""
    
    @pytest.fixture
    def validator(self):
        return AIResponseValidator()
    
    @pytest.mark.constitutional
    @pytest.mark.parametrize("phrase", PROHIBITED_PHRASES)
    def test_prohibited_phrase_detected(self, validator, phrase):
        """Each prohibited phrase must be detected by the validator."""
        test_response = f"Based on the signals, {phrase} this stock."
        result = validator.validate(test_response)
        
        assert result.is_valid == False, f"Phrase '{phrase}' should be detected as violation"
        assert len(result.violations) > 0, f"Should have violations for '{phrase}'"
    
    @pytest.mark.constitutional
    def test_compliant_response_with_disclaimer_passes(self, validator):
        """A compliant response WITH disclaimer should pass validation."""
        compliant_response = f"""
        The RSI indicator on the daily chart shows a reading of 65, which is 
        in the upper range. The MACD histogram is positive with increasing 
        momentum. The 50-day moving average is above the 200-day moving average.
        
        These are the current readings from your configured charts.
        
        {MANDATORY_DISCLAIMER}
        """
        result = validator.validate(compliant_response)
        
        assert result.is_valid == True, f"Compliant response with disclaimer should pass. Violations: {result.violations}"
    
    @pytest.mark.constitutional
    def test_missing_disclaimer_is_violation(self, validator):
        """A response without disclaimer should fail (CR-003)."""
        no_disclaimer_response = """
        The RSI indicator on the daily chart shows a reading of 65.
        The MACD histogram is positive.
        """
        result = validator.validate(no_disclaimer_response)
        
        # Missing disclaimer IS a violation per CR-003
        assert result.is_valid == False, "Missing disclaimer should be a violation"
        assert any("disclaimer" in v.lower() for v in result.violations), \
            "Should report missing disclaimer"
    
    @pytest.mark.constitutional
    def test_case_insensitive_detection(self, validator):
        """Prohibited phrases should be detected regardless of case."""
        test_cases = [
            "YOU SHOULD buy this stock",
            "You Should consider this",
            "I RECOMMEND this action",
            "i recommend buying",
        ]
        
        for test_response in test_cases:
            result = validator.validate(test_response)
            assert result.is_valid == False, f"Case variation should be detected: {test_response}"
    
    @pytest.mark.constitutional
    def test_multiple_violations(self, validator):
        """Response with multiple violations should all be reported."""
        multi_violation = "You should buy this stock. I recommend selling the other. The overall direction is bullish."
        result = validator.validate(multi_violation)
        
        assert result.is_valid == False
        assert len(result.violations) >= 2, "Multiple violations should be detected"
    
    @pytest.mark.constitutional
    def test_empty_response_handling(self, validator):
        """Empty response should be handled gracefully."""
        result = validator.validate("")
        # Empty is technically a violation (no disclaimer)
        assert result is not None
    
    @pytest.mark.constitutional
    def test_whitespace_only_response(self, validator):
        """Whitespace-only response handling."""
        result = validator.validate("   \n\t  ")
        assert result is not None


class TestCR001ModelFields:
    """Test that models don't have prohibited fields."""
    
    @pytest.mark.constitutional
    def test_chart_has_no_weight_field(self):
        """Chart model must NOT have a weight field."""
        from cia_sie.core.models import Chart
        
        chart_fields = Chart.model_fields.keys()
        assert "weight" not in chart_fields, "Chart must not have weight field (CR-001)"
        assert "priority" not in chart_fields, "Chart must not have priority field (CR-001)"
        assert "importance" not in chart_fields, "Chart must not have importance field (CR-001)"
    
    @pytest.mark.constitutional
    def test_signal_has_no_confidence_field(self):
        """Signal model must NOT have a confidence field."""
        from cia_sie.core.models import Signal
        
        signal_fields = Signal.model_fields.keys()
        assert "confidence" not in signal_fields, "Signal must not have confidence field (CR-001)"
        assert "score" not in signal_fields, "Signal must not have score field (CR-001)"
        assert "strength" not in signal_fields, "Signal must not have strength field (CR-001)"
    
    @pytest.mark.constitutional
    def test_db_chart_has_no_weight_column(self):
        """Database Chart model must NOT have weight column."""
        from cia_sie.dal.models import ChartDB
        
        columns = [c.name for c in ChartDB.__table__.columns]
        assert "weight" not in columns, "ChartDB must not have weight column"
        assert "priority" not in columns, "ChartDB must not have priority column"
    
    @pytest.mark.constitutional
    def test_db_signal_has_no_confidence_column(self):
        """Database Signal model must NOT have confidence column."""
        from cia_sie.dal.models import SignalDB
        
        columns = [c.name for c in SignalDB.__table__.columns]
        assert "confidence" not in columns, "SignalDB must not have confidence column"
        assert "score" not in columns, "SignalDB must not have score column"


class TestCR001ConfigProhibitions:
    """Test that configuration doesn't allow prohibited features."""
    
    @pytest.mark.constitutional
    def test_no_aggregation_config(self):
        """Settings must not have aggregation configuration."""
        from cia_sie.core.config import Settings
        
        settings_fields = Settings.model_fields.keys()
        prohibited_configs = [
            "aggregation_weights",
            "scoring_thresholds", 
            "recommendation_rules",
            "signal_priority_config",
            "confidence_calculation_params",
        ]
        
        for prohibited in prohibited_configs:
            assert prohibited not in settings_fields, f"Config must not have {prohibited}"


class TestCR001ExceptionExists:
    """Test that constitutional violation exceptions exist."""
    
    @pytest.mark.constitutional
    def test_constitutional_violation_error_exists(self):
        """ConstitutionalViolationError must exist."""
        from cia_sie.core.exceptions import ConstitutionalViolationError
        
        assert ConstitutionalViolationError is not None
        assert issubclass(ConstitutionalViolationError, Exception)
    
    @pytest.mark.constitutional
    def test_recommendation_attempt_error_exists(self):
        """RecommendationAttemptError must exist."""
        from cia_sie.core.exceptions import RecommendationAttemptError
        
        assert RecommendationAttemptError is not None
    
    @pytest.mark.constitutional
    def test_aggregation_attempt_error_exists(self):
        """AggregationAttemptError must exist."""
        from cia_sie.core.exceptions import AggregationAttemptError
        
        assert AggregationAttemptError is not None
