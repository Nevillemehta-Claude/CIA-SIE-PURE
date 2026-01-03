"""
CIA-SIE Domain Models
=====================

Defines all domain entities as Pydantic models.
These models represent the core business objects of the platform.

GOVERNED BY: Section 0A-0D of Gold Standard Specification

CRITICAL DESIGN CONSTRAINTS:
- Chart has NO weight attribute (ADR-003)
- Signal has NO confidence score (ADR-003)
- No aggregation, scoring, or weighting anywhere
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from cia_sie.core.enums import (
    BasketType,
    Direction,
    FreshnessStatus,
    NarrativeSectionType,
    SignalType,
)

# =============================================================================
# BASE CONFIGURATION
# =============================================================================


class CIASIEBaseModel(BaseModel):
    """Base model with common configuration for all CIA-SIE models."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_assignment=True,
    )


# =============================================================================
# DOMAIN ENTITIES (Section 5.2)
# =============================================================================


class Instrument(CIASIEBaseModel):
    """
    A tradeable financial asset identified by a unique symbol.

    Per Gold Standard Specification Section 5.2.1:
    - Lifecycle: Created by user -> Active -> Archived (soft delete)
    - Relationships: Has many Silos

    Invariants:
    - symbol must be unique across all instruments
    - display_name must be non-empty
    """

    instrument_id: UUID = Field(default_factory=uuid4)
    symbol: str = Field(..., min_length=1, max_length=50)
    display_name: str = Field(..., min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    metadata: Optional[dict] = Field(default=None)


class Silo(CIASIEBaseModel):
    """
    A logical container grouping charts for a single instrument.

    Per Gold Standard Specification Section 5.2.2:
    - Lifecycle: Created by user -> Configured -> Active -> Archived
    - Relationships: Belongs to one Instrument, Has many Charts

    Invariants:
    - current_threshold_min < recent_threshold_min < stale_threshold_min
    - heartbeat_frequency_min >= 1
    - silo_name unique within instrument
    """

    silo_id: UUID = Field(default_factory=uuid4)
    instrument_id: UUID
    silo_name: str = Field(..., min_length=1, max_length=100)
    heartbeat_enabled: bool = Field(default=True)
    heartbeat_frequency_min: int = Field(default=5, ge=1)
    current_threshold_min: int = Field(default=2, ge=1)
    recent_threshold_min: int = Field(default=10, ge=1)
    stale_threshold_min: int = Field(default=30, ge=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class Chart(CIASIEBaseModel):
    """
    A TradingView chart that emits signals via webhook.

    Per Gold Standard Specification Section 5.2.3:
    - Lifecycle: Registered -> Active -> Disabled -> Archived
    - Relationships: Belongs to one Silo, Produces many Signals

    CRITICAL: NO WEIGHT ATTRIBUTE
    Per ADR-003: Weights enable aggregation which is PROHIBITED.
    All charts have equal standing. User determines importance through interpretation.

    Invariants:
    - chart_code unique within silo
    - webhook_id globally unique
    - timeframe must be valid (1m, 5m, 15m, 1h, 4h, D, W, M)
    """

    chart_id: UUID = Field(default_factory=uuid4)
    silo_id: UUID
    chart_code: str = Field(..., min_length=1, max_length=50)
    chart_name: str = Field(..., min_length=1, max_length=100)
    timeframe: str = Field(..., pattern=r"^(1m|5m|15m|30m|1h|4h|D|W|M)$")
    webhook_id: str = Field(..., min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # NOTE: Deliberately NO weight field - prohibited by Section 0B


class Signal(CIASIEBaseModel):
    """
    A point-in-time data emission from a chart.

    Per Gold Standard Specification Section 5.2.4:
    - Lifecycle: Received -> Stored -> Available for display -> Archived
    - Relationships: Belongs to one Chart

    CRITICAL: NO CONFIDENCE/STRENGTH SCORES
    Per ADR-003: Scores imply system judgment which is PROHIBITED.
    Raw direction and indicators preserved. User interprets significance.

    Invariants:
    - direction must be one of: BULLISH, BEARISH, NEUTRAL
    - indicators must conform to IndicatorReading schema
    - raw_payload preserved for audit trail
    """

    signal_id: UUID = Field(default_factory=uuid4)
    chart_id: UUID
    received_at: datetime = Field(default_factory=datetime.utcnow)
    signal_timestamp: datetime
    signal_type: SignalType
    direction: Direction
    indicators: dict = Field(default_factory=dict)
    raw_payload: dict = Field(default_factory=dict)

    # NOTE: Deliberately NO confidence or strength field - prohibited by Section 0B


class AnalyticalBasket(CIASIEBaseModel):
    """
    A user-defined grouping of charts for comparison.

    Per Gold Standard Specification Section 15 and ADR-002:
    - Lives in UI layer, NOT in core engine
    - Does NOT affect processing
    - Enables multiple views of same data
    - Charts can belong to multiple baskets

    CRITICAL: Baskets are organizational/display constructs ONLY.
    They have ZERO impact on signal processing.
    """

    basket_id: UUID = Field(default_factory=uuid4)
    basket_name: str = Field(..., min_length=1, max_length=100)
    basket_type: BasketType
    description: Optional[str] = Field(default=None, max_length=500)
    instrument_id: Optional[UUID] = Field(default=None)  # NULL for cross-instrument
    chart_ids: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


# =============================================================================
# RELATIONSHIP MODELS (Section 13.2, 13.3)
# =============================================================================


class Contradiction(CIASIEBaseModel):
    """
    Represents a detected contradiction between two charts.

    Per Gold Standard Specification Section 13.2:
    The Contradiction Detector identifies when chart signals conflict.
    It does NOT resolve contradictions - only EXPOSES them.

    PROHIBITED ACTIONS:
    - Resolving which signal is "correct"
    - Suggesting which to prioritize
    - Hiding any contradiction
    """

    chart_a_id: UUID
    chart_a_name: str
    chart_a_direction: Direction
    chart_b_id: UUID
    chart_b_name: str
    chart_b_direction: Direction
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class Confirmation(CIASIEBaseModel):
    """
    Represents detected alignment between two charts.

    Per Gold Standard Specification Section 13.3:
    The Confirmation Detector identifies when chart signals align.
    It does NOT weight or prioritize confirmations.
    """

    chart_a_id: UUID
    chart_a_name: str
    chart_b_id: UUID
    chart_b_name: str
    aligned_direction: Direction
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class ChartSignalStatus(CIASIEBaseModel):
    """
    Current status of a chart including its latest signal and freshness.

    Per Gold Standard Specification Section 13.3 (RelationshipSummary).
    """

    chart_id: UUID
    chart_code: str
    chart_name: str
    timeframe: str
    latest_signal: Optional[Signal] = None
    freshness: FreshnessStatus = FreshnessStatus.UNAVAILABLE


class RelationshipSummary(CIASIEBaseModel):
    """
    Complete relationship summary for a silo.

    Per Gold Standard Specification Section 13.3:
    - Returns ALL charts (none hidden)
    - Returns ALL contradictions (none resolved)
    - Returns ALL confirmations (none weighted)
    - NO aggregation anywhere
    - NO scores anywhere
    - NO recommendations anywhere
    """

    silo_id: UUID
    silo_name: str
    instrument_id: UUID
    instrument_symbol: str
    charts: list[ChartSignalStatus] = Field(default_factory=list)
    contradictions: list[Contradiction] = Field(default_factory=list)
    confirmations: list[Confirmation] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# NARRATIVE MODELS (Section 14)
# =============================================================================


class NarrativeSection(CIASIEBaseModel):
    """
    A section of the AI-generated narrative.

    Per Gold Standard Specification Section 14.4:
    All sections are DESCRIPTIVE, never PRESCRIPTIVE.
    """

    section_type: NarrativeSectionType
    content: str
    referenced_chart_ids: list[UUID] = Field(default_factory=list)


class Narrative(CIASIEBaseModel):
    """
    Complete AI-generated narrative for a relationship summary.

    Per Gold Standard Specification Section 14.4:
    - Generated narratives are DESCRIPTIVE only
    - Must include closing statement about user authority
    - PROHIBITED: recommendations, direction inference, confidence scores

    REQUIRED CLOSING STATEMENT:
    "This is a description of what your charts are showing.
    The interpretation and any decision is entirely yours."
    """

    narrative_id: UUID = Field(default_factory=uuid4)
    silo_id: UUID
    sections: list[NarrativeSection] = Field(default_factory=list)
    closing_statement: str = Field(
        default="This is a description of what your charts are showing. "
        "The interpretation and any decision is entirely yours."
    )
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# API REQUEST/RESPONSE MODELS
# =============================================================================


class InstrumentCreate(CIASIEBaseModel):
    """Request model for creating an instrument."""

    symbol: str = Field(..., min_length=1, max_length=50)
    display_name: str = Field(..., min_length=1, max_length=100)
    metadata: Optional[dict] = None


class SiloCreate(CIASIEBaseModel):
    """Request model for creating a silo."""

    instrument_id: UUID
    silo_name: str = Field(..., min_length=1, max_length=100)
    heartbeat_enabled: bool = True
    heartbeat_frequency_min: int = Field(default=5, ge=1)
    current_threshold_min: int = Field(default=2, ge=1)
    recent_threshold_min: int = Field(default=10, ge=1)
    stale_threshold_min: int = Field(default=30, ge=1)


class ChartCreate(CIASIEBaseModel):
    """Request model for creating a chart."""

    silo_id: UUID
    chart_code: str = Field(..., min_length=1, max_length=50)
    chart_name: str = Field(..., min_length=1, max_length=100)
    timeframe: str = Field(..., pattern=r"^(1m|5m|15m|30m|1h|4h|D|W|M)$")
    webhook_id: str = Field(..., min_length=1, max_length=100)


class WebhookPayload(CIASIEBaseModel):
    """
    Incoming webhook payload from TradingView or other platforms.

    This is the normalized format expected by the webhook handler.
    Platform-specific adapters convert to this format.
    """

    webhook_id: str
    timestamp: datetime
    signal_type: SignalType
    direction: Direction
    indicators: dict = Field(default_factory=dict)


class BasketCreate(CIASIEBaseModel):
    """Request model for creating an analytical basket."""

    basket_name: str = Field(..., min_length=1, max_length=100)
    basket_type: BasketType = BasketType.CUSTOM
    description: Optional[str] = None
    instrument_id: Optional[UUID] = None
    chart_ids: list[UUID] = Field(default_factory=list)
