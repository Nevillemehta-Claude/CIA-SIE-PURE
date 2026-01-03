"""
Tests for CIA-SIE Core Enumerations
===================================

Validates all enums conform to Gold Standard Specification.

GOVERNED BY: Section 0B (Analysis Definition)
"""

import pytest
from cia_sie.core.enums import (
    SignalType,
    Direction,
    FreshnessStatus,
    BasketType,
    NarrativeSectionType,
    ValidationStatus,
    AIModelTier,
    UsagePeriod,
    MessageRole,
)


class TestSignalType:
    """Tests for SignalType enum."""

    def test_all_signal_types_exist(self):
        """Per Section 5.3: All signal types must be defined."""
        assert SignalType.HEARTBEAT == "HEARTBEAT"
        assert SignalType.STATE_CHANGE == "STATE_CHANGE"
        assert SignalType.BAR_CLOSE == "BAR_CLOSE"
        assert SignalType.MANUAL == "MANUAL"

    def test_signal_type_count(self):
        """Verify exactly 4 signal types."""
        assert len(SignalType) == 4

    def test_signal_type_is_string_enum(self):
        """Signal types should be string values."""
        for signal_type in SignalType:
            assert isinstance(signal_type.value, str)


class TestDirection:
    """Tests for Direction enum."""

    def test_all_directions_exist(self):
        """Per Section 5.3: All directions must be defined."""
        assert Direction.BULLISH == "BULLISH"
        assert Direction.BEARISH == "BEARISH"
        assert Direction.NEUTRAL == "NEUTRAL"

    def test_direction_count(self):
        """Verify exactly 3 directions."""
        assert len(Direction) == 3

    def test_direction_is_string_enum(self):
        """Directions should be string values."""
        for direction in Direction:
            assert isinstance(direction.value, str)

    def test_no_aggregated_direction(self):
        """
        CRITICAL: No 'OVERALL' or 'COMBINED' direction.

        Per Section 0B: System shall NOT compute aggregate direction.
        """
        direction_names = [d.name for d in Direction]
        assert "OVERALL" not in direction_names
        assert "COMBINED" not in direction_names
        assert "AGGREGATE" not in direction_names
        assert "NET" not in direction_names


class TestFreshnessStatus:
    """Tests for FreshnessStatus enum."""

    def test_all_freshness_values_exist(self):
        """Per SDD v4.0: All freshness states must be defined."""
        assert FreshnessStatus.CURRENT == "CURRENT"
        assert FreshnessStatus.RECENT == "RECENT"
        assert FreshnessStatus.STALE == "STALE"
        assert FreshnessStatus.UNAVAILABLE == "UNAVAILABLE"

    def test_freshness_count(self):
        """Verify exactly 4 freshness states."""
        assert len(FreshnessStatus) == 4

    def test_freshness_is_descriptive_only(self):
        """
        CRITICAL: Freshness is descriptive, not prescriptive.

        Per Section 0C: Freshness does NOT invalidate data.
        No 'INVALID' or 'REJECTED' status exists.
        """
        freshness_names = [f.name for f in FreshnessStatus]
        assert "INVALID" not in freshness_names
        assert "REJECTED" not in freshness_names
        assert "EXPIRED" not in freshness_names


class TestBasketType:
    """Tests for BasketType enum."""

    def test_all_basket_types_exist(self):
        """Per Section 5.3: All basket types must be defined."""
        assert BasketType.LOGICAL == "LOGICAL"
        assert BasketType.HIERARCHICAL == "HIERARCHICAL"
        assert BasketType.CONTEXTUAL == "CONTEXTUAL"
        assert BasketType.CUSTOM == "CUSTOM"

    def test_basket_type_count(self):
        """Verify exactly 4 basket types."""
        assert len(BasketType) == 4


class TestNarrativeSectionType:
    """Tests for NarrativeSectionType enum."""

    def test_all_section_types_exist(self):
        """Per Section 14.2: All narrative section types must be defined."""
        assert NarrativeSectionType.SIGNAL_SUMMARY == "SIGNAL_SUMMARY"
        assert NarrativeSectionType.CONTRADICTION == "CONTRADICTION"
        assert NarrativeSectionType.CONFIRMATION == "CONFIRMATION"
        assert NarrativeSectionType.FRESHNESS == "FRESHNESS"

    def test_no_recommendation_section_type(self):
        """
        CRITICAL: No recommendation section type.

        Per Section 14.4: All narratives are DESCRIPTIVE only.
        """
        section_names = [s.name for s in NarrativeSectionType]
        assert "RECOMMENDATION" not in section_names
        assert "ACTION" not in section_names
        assert "ADVICE" not in section_names


class TestValidationStatus:
    """Tests for ValidationStatus enum."""

    def test_all_validation_statuses_exist(self):
        """All validation statuses must be defined."""
        assert ValidationStatus.VALID == "VALID"
        assert ValidationStatus.INVALID == "INVALID"
        assert ValidationStatus.REMEDIATED == "REMEDIATED"

    def test_validation_status_count(self):
        """Verify exactly 3 validation statuses."""
        assert len(ValidationStatus) == 3


class TestAIModelTier:
    """Tests for AIModelTier enum."""

    def test_all_model_tiers_exist(self):
        """All Claude model tiers must be defined."""
        assert AIModelTier.HAIKU == "HAIKU"
        assert AIModelTier.SONNET == "SONNET"
        assert AIModelTier.OPUS == "OPUS"

    def test_model_tier_count(self):
        """Verify exactly 3 model tiers."""
        assert len(AIModelTier) == 3


class TestUsagePeriod:
    """Tests for UsagePeriod enum."""

    def test_all_usage_periods_exist(self):
        """All usage periods must be defined."""
        assert UsagePeriod.DAILY == "DAILY"
        assert UsagePeriod.WEEKLY == "WEEKLY"
        assert UsagePeriod.MONTHLY == "MONTHLY"


class TestMessageRole:
    """Tests for MessageRole enum."""

    def test_all_message_roles_exist(self):
        """All message roles must be defined."""
        assert MessageRole.USER == "user"
        assert MessageRole.ASSISTANT == "assistant"

    def test_message_role_values_match_api(self):
        """Message roles should match Claude API conventions."""
        assert MessageRole.USER.value == "user"
        assert MessageRole.ASSISTANT.value == "assistant"
