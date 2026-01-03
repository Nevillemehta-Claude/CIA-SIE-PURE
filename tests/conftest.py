"""
CIA-SIE Test Configuration
==========================

Shared fixtures and configuration for all tests.
This file is automatically loaded by pytest.

GOVERNED BY: Gold Standard Specification §12 (Quality Enforcement)
"""

import pytest
import pytest_asyncio
from datetime import datetime, UTC
from uuid import UUID, uuid4

from cia_sie.core.enums import Direction, SignalType, FreshnessStatus, BasketType
from cia_sie.core.models import (
    Instrument,
    Silo,
    Chart,
    Signal,
    ChartSignalStatus,
    AnalyticalBasket,
)


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "constitutional: marks tests that verify constitutional compliance"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


# =============================================================================
# SAMPLE DATA FIXTURES
# =============================================================================

@pytest.fixture
def sample_instrument_id() -> UUID:
    """Provide a consistent instrument ID for testing."""
    return UUID("12345678-1234-1234-1234-123456789012")


@pytest.fixture
def sample_silo_id() -> UUID:
    """Provide a consistent silo ID for testing."""
    return UUID("22345678-1234-1234-1234-123456789012")


@pytest.fixture
def sample_chart_id() -> UUID:
    """Provide a consistent chart ID for testing."""
    return UUID("32345678-1234-1234-1234-123456789012")


@pytest.fixture
def sample_instrument(sample_instrument_id) -> Instrument:
    """Create a sample instrument for testing."""
    return Instrument(
        instrument_id=sample_instrument_id,
        symbol="NIFTY50",
        display_name="Nifty 50 Index",
        is_active=True,
    )


@pytest.fixture
def sample_silo(sample_silo_id, sample_instrument_id) -> Silo:
    """Create a sample silo for testing."""
    return Silo(
        silo_id=sample_silo_id,
        instrument_id=sample_instrument_id,
        silo_name="Technical Analysis",
        heartbeat_enabled=True,
        heartbeat_frequency_min=5,
        current_threshold_min=2,
        recent_threshold_min=10,
        stale_threshold_min=30,
        is_active=True,
    )


@pytest.fixture
def sample_chart(sample_chart_id, sample_silo_id) -> Chart:
    """Create a sample chart for testing.

    NOTE: Chart has NO weight attribute - this is constitutional.
    """
    return Chart(
        chart_id=sample_chart_id,
        silo_id=sample_silo_id,
        chart_code="RSI_14",
        chart_name="RSI (14)",
        timeframe="1H",
        webhook_id="webhook_rsi_14_nifty",
        is_active=True,
    )


@pytest.fixture
def sample_signal(sample_chart_id) -> Signal:
    """Create a sample signal for testing.

    NOTE: Signal has NO confidence/score attribute - this is constitutional.
    """
    return Signal(
        signal_id=uuid4(),
        chart_id=sample_chart_id,
        received_at=datetime.now(UTC),
        signal_timestamp=datetime.now(UTC),
        signal_type=SignalType.STATE_CHANGE,
        direction=Direction.BULLISH,
        indicators={"rsi": 72.5},
        raw_payload={"source": "TradingView"},
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def make_signal(
    chart_id: UUID,
    direction: Direction,
    signal_type: SignalType = SignalType.STATE_CHANGE,
    minutes_ago: int = 0,
) -> Signal:
    """Factory function to create signals for testing.

    NOTE: Signals have NO confidence/score - this is constitutional.
    """
    from datetime import timedelta

    timestamp = datetime.now(UTC) - timedelta(minutes=minutes_ago)
    return Signal(
        signal_id=uuid4(),
        chart_id=chart_id,
        received_at=timestamp,
        signal_timestamp=timestamp,
        signal_type=signal_type,
        direction=direction,
        indicators={},
        raw_payload={},
    )


def make_chart_status(
    chart_id: str,
    chart_name: str,
    direction: Direction,
    freshness: FreshnessStatus = FreshnessStatus.CURRENT,
) -> ChartSignalStatus:
    """Factory function to create ChartSignalStatus for testing."""
    signal = Signal(
        signal_id=uuid4(),
        chart_id=UUID(chart_id),
        received_at=datetime.now(UTC),
        signal_timestamp=datetime.now(UTC),
        signal_type=SignalType.STATE_CHANGE,
        direction=direction,
        indicators={},
        raw_payload={},
    )

    return ChartSignalStatus(
        chart_id=UUID(chart_id),
        chart_code=chart_name.lower().replace(" ", "_"),
        chart_name=chart_name,
        timeframe="1H",
        latest_signal=signal,
        freshness_status=freshness,
    )


# =============================================================================
# CONSTITUTIONAL COMPLIANCE HELPERS
# =============================================================================

def assert_no_weight_attribute(obj):
    """Assert that an object has no weight attribute.

    Per Gold Standard Specification Section 0B: NO weighting allowed.
    """
    assert not hasattr(obj, 'weight'), \
        f"Constitutional violation: {type(obj).__name__} has 'weight' attribute"


def assert_no_confidence_attribute(obj):
    """Assert that an object has no confidence/score attribute.

    Per Gold Standard Specification Section 0B: NO scoring allowed.
    """
    assert not hasattr(obj, 'confidence'), \
        f"Constitutional violation: {type(obj).__name__} has 'confidence' attribute"
    assert not hasattr(obj, 'score'), \
        f"Constitutional violation: {type(obj).__name__} has 'score' attribute"


def assert_no_recommendation(text: str):
    """Assert that text contains no recommendation language.

    Per Gold Standard Specification Section 0B: NO recommendations allowed.
    """
    prohibited_phrases = [
        "you should",
        "i recommend",
        "i suggest",
        "consider buying",
        "consider selling",
        "i advise",
    ]
    text_lower = text.lower()
    for phrase in prohibited_phrases:
        assert phrase not in text_lower, \
            f"Constitutional violation: Text contains '{phrase}'"
