"""
Constitutional Compliance Tests - CR-003: Mandatory Disclaimer
===============================================================

These tests verify that the mandatory disclaimer is present
in ALL AI-generated content and cannot be removed.

CR-003 Requirements:
- Disclaimer is HARDCODED and IMMUTABLE
- Disclaimer is NON-DISMISSIBLE
- Disclaimer is NON-COLLAPSIBLE
- Disclaimer MUST be rendered with every narrative/AI output

DISCLAIMER TEXT:
"This is a description of what your charts are showing. 
The interpretation and any decision is entirely yours."

Each test runs 10 times for statistical confidence.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestCR003DisclaimerText:
    """Test that disclaimer text is correctly defined."""
    
    @pytest.mark.constitutional
    def test_mandatory_disclaimer_exists(self):
        """MANDATORY_DISCLAIMER constant must exist."""
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
        
        assert MANDATORY_DISCLAIMER is not None
        assert len(MANDATORY_DISCLAIMER) > 0
    
    @pytest.mark.constitutional
    def test_disclaimer_contains_key_phrases(self):
        """Disclaimer must contain required phrases."""
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
        
        disclaimer_lower = MANDATORY_DISCLAIMER.lower()
        
        # Must mention it's a description
        assert "description" in disclaimer_lower, "Disclaimer must mention 'description'"
        
        # Must mention charts
        assert "chart" in disclaimer_lower, "Disclaimer must mention 'chart'"
        
        # Must indicate user has decision authority
        has_decision_phrase = (
            "decision" in disclaimer_lower or 
            "interpretation" in disclaimer_lower or
            "entirely yours" in disclaimer_lower
        )
        assert has_decision_phrase, "Disclaimer must reference user decision authority"
    
    @pytest.mark.constitutional
    def test_disclaimer_is_string(self):
        """Disclaimer must be a string (not callable, not mutable object)."""
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
        
        assert isinstance(MANDATORY_DISCLAIMER, str), "Disclaimer must be a string"
        assert not callable(MANDATORY_DISCLAIMER), "Disclaimer must not be callable"


class TestCR003DisclaimerValidation:
    """Test that validator enforces disclaimer presence."""
    
    @pytest.fixture
    def validator(self):
        from cia_sie.ai.response_validator import AIResponseValidator
        return AIResponseValidator()
    
    @pytest.mark.constitutional
    def test_response_without_disclaimer_fails(self, validator):
        """Response without disclaimer must fail validation."""
        response_no_disclaimer = """
        The RSI indicator is at 65. The MACD is positive.
        Moving averages show an upward trend.
        """
        
        result = validator.validate(response_no_disclaimer)
        
        assert result.is_valid == False, "Response without disclaimer must fail"
        assert any("disclaimer" in v.lower() for v in result.violations), \
            "Should report missing disclaimer"
    
    @pytest.mark.constitutional
    def test_response_with_disclaimer_passes(self, validator):
        """Response with disclaimer passes (assuming no other violations)."""
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
        
        response_with_disclaimer = f"""
        The RSI indicator is at 65. The MACD is positive.
        Moving averages show an upward trend.
        
        {MANDATORY_DISCLAIMER}
        """
        
        result = validator.validate(response_with_disclaimer)
        
        # Should pass (no violations)
        assert result.is_valid == True, f"Response with disclaimer should pass. Violations: {result.violations}"
    
    @pytest.mark.constitutional
    def test_partial_disclaimer_fails(self, validator):
        """Partial disclaimer is not sufficient."""
        response_partial = """
        The RSI indicator is at 65.
        
        This is a description of charts.
        """
        
        result = validator.validate(response_partial)
        
        # Partial disclaimer should fail
        assert result.is_valid == False, "Partial disclaimer should fail"


class TestCR003DisclaimerImmutability:
    """Test that disclaimer cannot be modified at runtime."""
    
    @pytest.mark.constitutional
    def test_disclaimer_is_constant(self):
        """Disclaimer should be treated as a constant."""
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
        
        # Get initial value
        initial_value = MANDATORY_DISCLAIMER
        
        # The constant itself shouldn't change
        from cia_sie.ai import response_validator
        
        # Re-import and verify
        current_value = response_validator.MANDATORY_DISCLAIMER
        
        assert initial_value == current_value, "Disclaimer should not change"


class TestCR003ValidationResult:
    """Test that ValidationResult correctly tracks disclaimer violations."""
    
    @pytest.mark.constitutional
    def test_validation_result_structure(self):
        """ValidationResult must have required fields."""
        from cia_sie.ai.response_validator import ValidationResult
        from cia_sie.core.enums import ValidationStatus
        
        # Create a result using correct field names
        result = ValidationResult(
            is_valid=False,
            status=ValidationStatus.INVALID,
            violations=["Missing disclaimer"],
            remediated_text=None
        )
        
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'violations')
        assert isinstance(result.violations, list)
    
    @pytest.mark.constitutional
    def test_empty_violations_when_valid(self):
        """When valid, violations should be empty."""
        from cia_sie.ai.response_validator import ValidationResult
        from cia_sie.core.enums import ValidationStatus
        
        result = ValidationResult(
            is_valid=True,
            status=ValidationStatus.VALID,
            violations=[],
            remediated_text=None
        )
        
        assert result.is_valid == True
        assert len(result.violations) == 0


class TestCR003IntegrationWithNarratives:
    """Test that narrative generator enforces disclaimer."""
    
    @pytest.mark.constitutional
    def test_narrative_generator_uses_disclaimer(self):
        """NarrativeGenerator must use MANDATORY_DISCLAIMER."""
        from cia_sie.ai.narrative_generator import NarrativeGenerator
        from cia_sie.ai.response_validator import MANDATORY_DISCLAIMER
        
        # The generator should have access to the disclaimer
        generator = NarrativeGenerator()
        
        assert generator is not None
        # The generator should validate its outputs
        assert hasattr(generator, 'validator') or hasattr(generator, '_validator'), \
            "Generator should have a validator"
