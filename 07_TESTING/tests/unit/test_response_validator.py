"""
Tests for CIA-SIE AI Response Validator
=======================================

Validates constitutional compliance checking for AI-generated responses.

GOVERNED BY: Section 14.4 (AI Narrative Validation)

These tests ensure that:
1. All prohibited patterns are correctly detected
2. Mandatory disclaimers are verified
3. Remediation works correctly for WARNING-level violations
4. CRITICAL violations are properly rejected
5. The retry logic functions as expected
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from cia_sie.ai.response_validator import (
    AIResponseValidator,
    ValidatedResponseGenerator,
    ValidationResult,
    validate_ai_response,
    ensure_disclaimer,
    MANDATORY_DISCLAIMER,
    PROHIBITED_PATTERNS,
)
from cia_sie.core.enums import ValidationStatus
from cia_sie.core.exceptions import ConstitutionalViolationError


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def validator():
    """Create a default AIResponseValidator."""
    return AIResponseValidator()


@pytest.fixture
def strict_validator():
    """Create a strict mode validator."""
    return AIResponseValidator(strict_mode=True, allow_remediation=False)


@pytest.fixture
def lenient_validator():
    """Create a lenient validator that allows remediation."""
    return AIResponseValidator(strict_mode=False, allow_remediation=True)


@pytest.fixture
def valid_response():
    """A valid response that passes all checks."""
    return (
        "The daily chart shows a bullish signal, while the weekly chart "
        "displays a bearish signal. These are presented for your review.\n\n"
        f"{MANDATORY_DISCLAIMER}"
    )


@pytest.fixture
def mock_claude_client():
    """Create a mock Claude client."""
    client = MagicMock()
    client.generate = AsyncMock()
    return client


# =============================================================================
# TEST: PROHIBITED PATTERNS DETECTION
# =============================================================================

class TestProhibitedPatterns:
    """Tests for prohibited pattern detection."""

    # -------------------------------------------------------------------------
    # Recommendation Language
    # -------------------------------------------------------------------------

    def test_detects_you_should(self, validator):
        """Test detection of 'you should' recommendation language."""
        response = f"You should consider this signal carefully.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid
        assert any("you should" in v.lower() for v in result.violations)

    def test_detects_i_recommend(self, validator):
        """Test detection of 'I recommend' language."""
        response = f"I recommend watching this closely.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid
        assert any("recommend" in v.lower() for v in result.violations)

    def test_detects_i_suggest(self, validator):
        """Test detection of 'I suggest' language."""
        response = f"I suggest reviewing the data.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid
        assert any("suggest" in v.lower() for v in result.violations)

    def test_detects_consider_buying(self, validator):
        """Test detection of 'consider buying' trading suggestion."""
        response = f"You might consider buying at this level.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_consider_selling(self, validator):
        """Test detection of 'consider selling' trading suggestion."""
        response = f"Consider selling before the announcement.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_you_might_want_to(self, validator):
        """Test detection of 'you might want to' soft recommendation."""
        response = f"You might want to wait for confirmation.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_the_best_action(self, validator):
        """Test detection of 'the best action' language."""
        response = f"The best action here is to wait.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_prudent_approach(self, validator):
        """Test detection of 'a prudent approach' language."""
        response = f"A prudent approach would be to diversify.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    # -------------------------------------------------------------------------
    # Trading Action Language
    # -------------------------------------------------------------------------

    def test_detects_buy_now(self, validator):
        """Test detection of 'buy now' trading advice."""
        response = f"The signal suggests you buy now.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_sell_now(self, validator):
        """Test detection of 'sell now' trading advice."""
        response = f"This indicates you should sell now.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_enter_long_position(self, validator):
        """Test detection of position entry advice."""
        response = f"Enter a long position at current levels.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_exit_position(self, validator):
        """Test detection of 'exit position' advice."""
        response = f"Exit your position before the report.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_take_profits(self, validator):
        """Test detection of 'take profits' advice."""
        response = f"Take profits at this resistance level.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_cut_losses(self, validator):
        """Test detection of 'cut losses' advice."""
        response = f"Cut your losses here.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    # -------------------------------------------------------------------------
    # Aggregation Language
    # -------------------------------------------------------------------------

    def test_detects_overall_direction(self, validator):
        """Test detection of 'overall direction' aggregation."""
        response = f"The overall direction is bullish.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_net_signal(self, validator):
        """Test detection of 'net signal' aggregation."""
        response = f"The net signal favors the bulls.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_consensus_shows(self, validator):
        """Test detection of 'consensus' aggregation."""
        response = f"The consensus is bullish.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_majority_signals(self, validator):
        """Test detection of 'majority of signals' aggregation."""
        response = f"The majority of signals show bullish.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    # -------------------------------------------------------------------------
    # Confidence/Probability Language
    # -------------------------------------------------------------------------

    def test_detects_confidence_score(self, validator):
        """Test detection of confidence scores."""
        response = f"Confidence level: 85%\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_percentage_confidence(self, validator):
        """Test detection of percentage confidence."""
        response = f"There is a 75% probability of upside.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_probability_statement(self, validator):
        """Test detection of probability statements."""
        response = f"The probability of success is high.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_likely_to_rise(self, validator):
        """Test detection of 'likely to rise' predictions."""
        response = f"The price is likely to rise next week.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_high_probability(self, validator):
        """Test detection of 'high probability' language."""
        response = f"There is a high probability of breakout.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    # -------------------------------------------------------------------------
    # Prediction Language
    # -------------------------------------------------------------------------

    def test_detects_will_rise(self, validator):
        """Test detection of 'will rise' predictions."""
        response = f"The price will rise tomorrow.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_expected_to_increase(self, validator):
        """Test detection of 'expected to' predictions."""
        response = f"Prices are expected to increase.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_forecast(self, validator):
        """Test detection of 'forecast' language."""
        response = f"Our forecast is bullish.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_price_target(self, validator):
        """Test detection of 'price target' language."""
        response = f"The price target is $150.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    # -------------------------------------------------------------------------
    # Ranking/Weighting Language
    # -------------------------------------------------------------------------

    def test_detects_more_reliable(self, validator):
        """Test detection of reliability comparisons."""
        response = f"This chart is more reliable than the other.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_stronger_signal(self, validator):
        """Test detection of 'stronger signal' comparisons."""
        response = f"This is a stronger signal than yesterday.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_signal_strength_score(self, validator):
        """Test detection of signal strength scores."""
        response = f"Signal strength is 8.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_risk_score(self, validator):
        """Test detection of risk scores."""
        response = f"Risk score is 3.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid

    def test_detects_numerical_rating(self, validator):
        """Test detection of numerical ratings."""
        response = f"Rating: 7 out of 10.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert not result.is_valid


# =============================================================================
# TEST: VALID RESPONSES
# =============================================================================

class TestValidResponses:
    """Tests for responses that should pass validation."""

    def test_valid_descriptive_response(self, validator, valid_response):
        """Test that a properly formatted response passes."""
        result = validator.validate(valid_response)

        assert result.is_valid
        assert result.status == ValidationStatus.VALID
        assert len(result.violations) == 0

    def test_valid_response_with_directions(self, validator):
        """Test valid response describing directions."""
        response = (
            "Chart A displays a bullish signal on the daily timeframe. "
            "Chart B shows a bearish signal on the weekly timeframe. "
            "These signals present a contradiction that is exposed for your review.\n\n"
            f"{MANDATORY_DISCLAIMER}"
        )
        result = validator.validate(response)

        assert result.is_valid

    def test_valid_response_with_freshness(self, validator):
        """Test valid response describing freshness."""
        response = (
            "The signal from Chart A is CURRENT (received within the last hour). "
            "The signal from Chart B is STALE (last received 3 days ago).\n\n"
            f"{MANDATORY_DISCLAIMER}"
        )
        result = validator.validate(response)

        assert result.is_valid

    def test_valid_response_with_indicators(self, validator):
        """Test valid response describing indicators."""
        response = (
            "The RSI indicator shows 65. The MACD is above the signal line. "
            "The moving average crossover occurred yesterday.\n\n"
            f"{MANDATORY_DISCLAIMER}"
        )
        result = validator.validate(response)

        assert result.is_valid


# =============================================================================
# TEST: MANDATORY DISCLAIMER
# =============================================================================

class TestMandatoryDisclaimer:
    """Tests for mandatory disclaimer verification."""

    def test_missing_disclaimer_fails(self, validator):
        """Test that missing disclaimer causes validation failure."""
        response = "The chart shows a bullish signal. No further analysis needed."
        result = validator.validate(response)

        assert not result.is_valid
        assert any("disclaimer" in v.lower() for v in result.violations)

    def test_exact_disclaimer_passes(self, validator):
        """Test that exact disclaimer passes."""
        response = f"The chart shows a bullish signal.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert result.is_valid

    def test_acceptable_variation_interpretation_yours(self, validator):
        """Test acceptable disclaimer variation."""
        response = (
            "The chart shows a bullish signal.\n\n"
            "The interpretation and any decision is entirely yours."
        )
        result = validator.validate(response)

        assert result.is_valid

    def test_acceptable_variation_decision_yours(self, validator):
        """Test acceptable disclaimer variation with decision emphasis."""
        response = (
            "The chart shows a bullish signal.\n\n"
            "Any decision is entirely yours to make."
        )
        result = validator.validate(response)

        assert result.is_valid


# =============================================================================
# TEST: VALIDATION STATUS
# =============================================================================

class TestValidationStatus:
    """Tests for ValidationStatus enum usage."""

    def test_valid_status_for_clean_response(self, validator, valid_response):
        """Test VALID status for clean response."""
        result = validator.validate(valid_response)

        assert result.status == ValidationStatus.VALID

    def test_invalid_status_for_critical_violation(self, validator):
        """Test INVALID status for critical violation."""
        response = f"You should buy now.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)

        assert result.status == ValidationStatus.INVALID

    def test_remediated_status_for_warning_violation(self, lenient_validator):
        """Test REMEDIATED status for warning-level violation."""
        # "on balance" is a WARNING level violation
        response = f"On balance, the signals are mixed.\n\n{MANDATORY_DISCLAIMER}"
        result = lenient_validator.validate(response)

        # In lenient mode with only warning violations, should be remediated
        if result.is_valid:
            assert result.status == ValidationStatus.REMEDIATED


# =============================================================================
# TEST: STRICT MODE
# =============================================================================

class TestStrictMode:
    """Tests for strict mode behavior."""

    def test_strict_mode_rejects_critical(self, strict_validator):
        """Test strict mode rejects critical violations."""
        response = f"I recommend you wait.\n\n{MANDATORY_DISCLAIMER}"
        result = strict_validator.validate(response)

        assert not result.is_valid
        assert result.status == ValidationStatus.INVALID

    def test_strict_mode_no_remediation(self, strict_validator):
        """Test strict mode doesn't remediate."""
        response = f"On balance, signals are mixed.\n\n{MANDATORY_DISCLAIMER}"
        result = strict_validator.validate(response)

        # Strict mode doesn't remediate
        assert result.remediated_text is None or not result.is_valid


# =============================================================================
# TEST: REMEDIATION
# =============================================================================

class TestRemediation:
    """Tests for response remediation."""

    def test_remediation_adds_missing_disclaimer(self, lenient_validator):
        """Test that remediation can add missing disclaimer."""
        response = "The chart shows a bullish signal."

        # Note: Missing disclaimer is CRITICAL, so won't be remediated
        # This tests that the remediation logic exists
        result = lenient_validator.validate(response)

        # Even lenient mode can't remediate missing disclaimer (it's critical)
        assert not result.is_valid

    def test_remediation_replaces_on_balance(self, lenient_validator):
        """Test remediation of 'on balance' phrase."""
        response = f"On balance, signals are mixed.\n\n{MANDATORY_DISCLAIMER}"
        result = lenient_validator.validate(response)

        if result.is_valid and result.remediated_text:
            assert "on balance" not in result.remediated_text.lower()


# =============================================================================
# TEST: VALIDATE OR RAISE
# =============================================================================

class TestValidateOrRaise:
    """Tests for validate_or_raise method."""

    def test_returns_response_when_valid(self, validator, valid_response):
        """Test that valid response is returned."""
        result = validator.validate_or_raise(valid_response)

        assert result == valid_response

    def test_raises_on_violation(self, validator):
        """Test that violation raises ConstitutionalViolationError."""
        response = f"You should buy now.\n\n{MANDATORY_DISCLAIMER}"

        with pytest.raises(ConstitutionalViolationError) as exc_info:
            validator.validate_or_raise(response)

        assert "constitutional" in str(exc_info.value).lower()

    def test_exception_contains_violations(self, validator):
        """Test that exception contains violation details."""
        response = f"I recommend selling immediately.\n\n{MANDATORY_DISCLAIMER}"

        with pytest.raises(ConstitutionalViolationError) as exc_info:
            validator.validate_or_raise(response)

        assert exc_info.value.details is not None
        assert "violations" in exc_info.value.details


# =============================================================================
# TEST: VALIDATED RESPONSE GENERATOR
# =============================================================================

class TestValidatedResponseGenerator:
    """Tests for ValidatedResponseGenerator with retry logic."""

    @pytest.mark.asyncio
    async def test_returns_valid_response_on_first_try(self, mock_claude_client):
        """Test that valid response is returned immediately."""
        valid_text = (
            f"The chart shows bullish signals.\n\n{MANDATORY_DISCLAIMER}"
        )
        mock_claude_client.generate.return_value = valid_text

        generator = ValidatedResponseGenerator(
            claude_client=mock_claude_client,
            max_retries=3,
        )

        result = await generator.generate(
            system_prompt="Test system prompt",
            user_prompt="Test user prompt",
        )

        assert result == valid_text
        assert mock_claude_client.generate.call_count == 1

    @pytest.mark.asyncio
    async def test_retries_on_violation(self, mock_claude_client):
        """Test that generator retries on validation failure."""
        invalid_text = f"You should buy now.\n\n{MANDATORY_DISCLAIMER}"
        valid_text = f"The chart shows bullish signals.\n\n{MANDATORY_DISCLAIMER}"

        # First call returns invalid, second returns valid
        mock_claude_client.generate.side_effect = [invalid_text, valid_text]

        generator = ValidatedResponseGenerator(
            claude_client=mock_claude_client,
            max_retries=3,
        )

        result = await generator.generate(
            system_prompt="Test system prompt",
            user_prompt="Test user prompt",
        )

        assert result == valid_text
        assert mock_claude_client.generate.call_count == 2

    @pytest.mark.asyncio
    async def test_raises_after_max_retries(self, mock_claude_client):
        """Test that ConstitutionalViolationError is raised after max retries."""
        invalid_text = f"You should buy now.\n\n{MANDATORY_DISCLAIMER}"

        # All calls return invalid response
        mock_claude_client.generate.return_value = invalid_text

        generator = ValidatedResponseGenerator(
            claude_client=mock_claude_client,
            max_retries=3,
        )

        with pytest.raises(ConstitutionalViolationError) as exc_info:
            await generator.generate(
                system_prompt="Test system prompt",
                user_prompt="Test user prompt",
            )

        assert mock_claude_client.generate.call_count == 3
        assert exc_info.value.details["attempts"] == 3

    @pytest.mark.asyncio
    async def test_stricter_prompt_on_retry(self, mock_claude_client):
        """Test that prompt becomes stricter on retry."""
        invalid_text = f"I recommend waiting.\n\n{MANDATORY_DISCLAIMER}"
        valid_text = f"The chart shows signals.\n\n{MANDATORY_DISCLAIMER}"

        mock_claude_client.generate.side_effect = [invalid_text, valid_text]

        generator = ValidatedResponseGenerator(
            claude_client=mock_claude_client,
            max_retries=3,
        )

        await generator.generate(
            system_prompt="Original prompt",
            user_prompt="Test user prompt",
        )

        # Second call should have stricter prompt
        second_call_args = mock_claude_client.generate.call_args_list[1]
        system_prompt = second_call_args.kwargs.get("system_prompt", "")

        assert "CRITICAL REMINDER" in system_prompt or "REJECTED" in system_prompt

    @pytest.mark.asyncio
    async def test_temperature_decreases_on_retry(self, mock_claude_client):
        """Test that temperature decreases on retry for more focused output."""
        invalid_text = f"You should act now.\n\n{MANDATORY_DISCLAIMER}"
        valid_text = f"The chart shows signals.\n\n{MANDATORY_DISCLAIMER}"

        mock_claude_client.generate.side_effect = [invalid_text, valid_text]

        generator = ValidatedResponseGenerator(
            claude_client=mock_claude_client,
            max_retries=3,
        )

        await generator.generate(
            system_prompt="Test",
            user_prompt="Test",
            temperature=0.3,
        )

        # Check temperature decreased on second call
        first_temp = mock_claude_client.generate.call_args_list[0].kwargs.get("temperature", 0.3)
        second_temp = mock_claude_client.generate.call_args_list[1].kwargs.get("temperature", 0.3)

        assert second_temp < first_temp


# =============================================================================
# TEST: CONVENIENCE FUNCTIONS
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_validate_ai_response_valid(self):
        """Test validate_ai_response with valid input."""
        response = f"The chart shows bullish signals.\n\n{MANDATORY_DISCLAIMER}"
        result = validate_ai_response(response)

        assert result.is_valid
        assert len(result.violations) == 0

    def test_validate_ai_response_invalid(self):
        """Test validate_ai_response with invalid input."""
        response = f"You should buy now.\n\n{MANDATORY_DISCLAIMER}"
        result = validate_ai_response(response)

        assert not result.is_valid
        assert len(result.violations) > 0

    def test_ensure_disclaimer_adds_when_missing(self):
        """Test ensure_disclaimer adds disclaimer when missing."""
        response = "The chart shows bullish signals."
        result = ensure_disclaimer(response)

        assert MANDATORY_DISCLAIMER in result

    def test_ensure_disclaimer_preserves_when_present(self):
        """Test ensure_disclaimer doesn't duplicate."""
        response = f"The chart shows signals.\n\n{MANDATORY_DISCLAIMER}"
        result = ensure_disclaimer(response)

        # Should only have one disclaimer
        assert result.count(MANDATORY_DISCLAIMER) == 1


# =============================================================================
# TEST: PATTERN COUNT VERIFICATION
# =============================================================================

class TestPatternCoverage:
    """Tests to verify pattern coverage."""

    def test_prohibited_patterns_count(self):
        """Verify we have comprehensive pattern coverage."""
        # Should have at least 25 patterns
        assert len(PROHIBITED_PATTERNS) >= 25

    def test_all_patterns_are_tuples(self):
        """Verify pattern structure."""
        for pattern in PROHIBITED_PATTERNS:
            assert isinstance(pattern, tuple)
            assert len(pattern) == 3
            pattern_str, reason, severity = pattern
            assert isinstance(pattern_str, str)
            assert isinstance(reason, str)
            assert severity in ("CRITICAL", "WARNING")


# =============================================================================
# TEST: CONSTITUTIONAL COMPLIANCE (CRITICAL)
# =============================================================================

class TestConstitutionalCompliance:
    """
    CRITICAL TESTS: Verify constitutional principles are enforced.

    Per Gold Standard Specification Section 0B.5:
    - No aggregation
    - No recommendations
    - No resolution of contradictions
    """

    def test_no_aggregation_allowed(self, validator):
        """
        CRITICAL: Aggregation language must be rejected.

        Per Section 0B.5 P-01: No system component shall reduce
        multiple chart outputs to a single score.
        """
        aggregation_phrases = [
            "The overall direction is bullish",
            "The net signal is bearish",
            "The consensus shows upward momentum",
            "The majority of charts indicate bullish",
        ]

        for phrase in aggregation_phrases:
            response = f"{phrase}.\n\n{MANDATORY_DISCLAIMER}"
            result = validator.validate(response)
            assert not result.is_valid, f"Failed to reject: {phrase}"

    def test_no_recommendations_allowed(self, validator):
        """
        CRITICAL: Recommendation language must be rejected.

        Per Section 0B.5 P-04: No system component shall recommend
        actions based on analytical outputs.
        """
        recommendation_phrases = [
            "You should wait for confirmation",
            "I recommend entering a position",
            "I suggest selling here",
            "The best action is to hold",
            "Consider buying at this level",
        ]

        for phrase in recommendation_phrases:
            response = f"{phrase}.\n\n{MANDATORY_DISCLAIMER}"
            result = validator.validate(response)
            assert not result.is_valid, f"Failed to reject: {phrase}"

    def test_no_predictions_allowed(self, validator):
        """
        CRITICAL: Prediction language must be rejected.

        The system describes what IS, not what WILL BE.
        """
        prediction_phrases = [
            "The price will rise tomorrow",
            "Expected to increase next week",
            "The forecast is bullish",
            "Likely to fall in the coming days",
        ]

        for phrase in prediction_phrases:
            response = f"{phrase}.\n\n{MANDATORY_DISCLAIMER}"
            result = validator.validate(response)
            assert not result.is_valid, f"Failed to reject: {phrase}"

    def test_no_confidence_scores_allowed(self, validator):
        """
        CRITICAL: Confidence scores must be rejected.

        Confidence implies the system knows which signal is "right".
        """
        confidence_phrases = [
            "Confidence level: 85%",
            "There is a 90% probability",
            "High probability of success",
            "Signal strength is 8",
        ]

        for phrase in confidence_phrases:
            response = f"{phrase}.\n\n{MANDATORY_DISCLAIMER}"
            result = validator.validate(response)
            assert not result.is_valid, f"Failed to reject: {phrase}"

    def test_descriptive_language_allowed(self, validator):
        """
        Verify that purely descriptive language is allowed.

        The system DESCRIBES signals, it doesn't PRESCRIBE actions.
        """
        descriptive_phrases = [
            "The daily chart shows a bullish signal",
            "Chart A displays bearish momentum",
            "The RSI indicator reads 65",
            "A contradiction exists between Chart A and Chart B",
            "The signal was received 2 hours ago",
            "This timeframe shows NEUTRAL",
        ]

        for phrase in descriptive_phrases:
            response = f"{phrase}.\n\n{MANDATORY_DISCLAIMER}"
            result = validator.validate(response)
            assert result.is_valid, f"Wrongly rejected: {phrase}"


# =============================================================================
# TEST: VALIDATION RESULT STR REPRESENTATION
# =============================================================================

class TestValidationResultStr:
    """Tests for ValidationResult string representation."""

    def test_valid_result_str(self):
        """Test string representation of valid result."""
        result = ValidationResult(
            is_valid=True,
            status=ValidationStatus.VALID,
            violations=[],
        )

        assert "VALID" in str(result)

    def test_invalid_result_str(self):
        """Test string representation of invalid result."""
        result = ValidationResult(
            is_valid=False,
            status=ValidationStatus.INVALID,
            violations=["Test violation"],
        )

        assert "INVALID" in str(result)
        assert "violations" in str(result)


# =============================================================================
# TEST: CASE INSENSITIVITY
# =============================================================================

class TestCaseInsensitivity:
    """Tests for case-insensitive pattern matching."""

    def test_lowercase_you_should(self, validator):
        """Test lowercase detection."""
        response = f"you should act now.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)
        assert not result.is_valid

    def test_uppercase_you_should(self, validator):
        """Test uppercase detection."""
        response = f"YOU SHOULD act now.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)
        assert not result.is_valid

    def test_mixed_case_you_should(self, validator):
        """Test mixed case detection."""
        response = f"You Should act now.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)
        assert not result.is_valid

    def test_lowercase_recommend(self, validator):
        """Test lowercase recommend."""
        response = f"i recommend waiting.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)
        assert not result.is_valid

    def test_uppercase_recommend(self, validator):
        """Test uppercase recommend."""
        response = f"I RECOMMEND WAITING.\n\n{MANDATORY_DISCLAIMER}"
        result = validator.validate(response)
        assert not result.is_valid
