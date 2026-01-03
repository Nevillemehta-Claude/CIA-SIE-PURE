"""
CIA-SIE SQLAlchemy ORM Models
=============================

Database models implementing the schema defined in Section 7.2 of the
Gold Standard Specification.

CRITICAL DESIGN CONSTRAINTS (per ADR-003):
- ChartDB has NO weight column
- SignalDB has NO confidence column
- No aggregation, scoring, or weighting columns exist

GOVERNED BY: Section 7.2 (Database Schema)
"""

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cia_sie.core.enums import BasketType
from cia_sie.dal.database import Base


def generate_uuid() -> str:
    """Generate a UUID string for primary keys."""
    return str(uuid4())


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(UTC)


class InstrumentDB(Base):
    """
    Instruments Table.

    A tradeable financial asset identified by a unique symbol.
    Per Gold Standard Specification Section 5.2.1.
    """

    __tablename__ = "instruments"

    instrument_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    symbol: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    metadata_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    # Relationships
    silos: Mapped[list["SiloDB"]] = relationship(
        "SiloDB", back_populates="instrument", cascade="all, delete-orphan"
    )
    baskets: Mapped[list["AnalyticalBasketDB"]] = relationship(
        "AnalyticalBasketDB", back_populates="instrument"
    )


class SiloDB(Base):
    """
    Silos Table.

    A logical container grouping charts for a single instrument.
    Per Gold Standard Specification Section 5.2.2.
    """

    __tablename__ = "silos"

    silo_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    instrument_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("instruments.instrument_id"), nullable=False
    )
    silo_name: Mapped[str] = mapped_column(String(100), nullable=False)
    heartbeat_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    heartbeat_frequency_min: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    current_threshold_min: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    recent_threshold_min: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    stale_threshold_min: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    instrument: Mapped["InstrumentDB"] = relationship("InstrumentDB", back_populates="silos")
    charts: Mapped[list["ChartDB"]] = relationship(
        "ChartDB", back_populates="silo", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("instrument_id", "silo_name", name="uq_silo_name_per_instrument"),
        Index("idx_silos_instrument", "instrument_id"),
    )


class ChartDB(Base):
    """
    Charts Table.

    A TradingView chart that emits signals via webhook.
    Per Gold Standard Specification Section 5.2.3.

    CRITICAL: NO WEIGHT COLUMN
    Per ADR-003: Weights enable aggregation which is PROHIBITED.
    All charts have equal standing.
    """

    __tablename__ = "charts"

    chart_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    silo_id: Mapped[str] = mapped_column(String(36), ForeignKey("silos.silo_id"), nullable=False)
    chart_code: Mapped[str] = mapped_column(String(50), nullable=False)
    chart_name: Mapped[str] = mapped_column(String(100), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(10), nullable=False)
    webhook_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # NOTE: Deliberately NO weight column - prohibited by Section 0B

    # Relationships
    silo: Mapped["SiloDB"] = relationship("SiloDB", back_populates="charts")
    signals: Mapped[list["SignalDB"]] = relationship(
        "SignalDB", back_populates="chart", cascade="all, delete-orphan"
    )
    basket_associations: Mapped[list["BasketChartDB"]] = relationship(
        "BasketChartDB", back_populates="chart", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("silo_id", "chart_code", name="uq_chart_code_per_silo"),
        Index("idx_charts_silo", "silo_id"),
        Index("idx_charts_webhook", "webhook_id"),
    )


class SignalDB(Base):
    """
    Signals Table.

    A point-in-time data emission from a chart.
    Per Gold Standard Specification Section 5.2.4.

    CRITICAL: NO CONFIDENCE COLUMN
    Per ADR-003: Scores imply system judgment which is PROHIBITED.
    Raw direction and indicators preserved.
    """

    __tablename__ = "signals"

    signal_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    chart_id: Mapped[str] = mapped_column(String(36), ForeignKey("charts.chart_id"), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    signal_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    signal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    direction: Mapped[str] = mapped_column(String(20), nullable=False)
    indicators: Mapped[str] = mapped_column(JSON, nullable=False, default="{}")
    raw_payload: Mapped[str] = mapped_column(JSON, nullable=False, default="{}")

    # NOTE: Deliberately NO confidence or strength column - prohibited by Section 0B

    # Relationships
    chart: Mapped["ChartDB"] = relationship("ChartDB", back_populates="signals")

    # Constraints
    __table_args__ = (
        Index("idx_signals_chart", "chart_id"),
        Index("idx_signals_timestamp", "signal_timestamp"),
    )


class AnalyticalBasketDB(Base):
    """
    Analytical Baskets Table.

    A user-defined grouping of charts for comparison.
    Per Gold Standard Specification Section 15 and ADR-002.

    CRITICAL: Baskets are UI-layer constructs only.
    They do NOT affect processing.
    """

    __tablename__ = "analytical_baskets"

    basket_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    basket_name: Mapped[str] = mapped_column(String(100), nullable=False)
    basket_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default=BasketType.CUSTOM.value
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instrument_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("instruments.instrument_id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    instrument: Mapped[Optional["InstrumentDB"]] = relationship(
        "InstrumentDB", back_populates="baskets"
    )
    chart_associations: Mapped[list["BasketChartDB"]] = relationship(
        "BasketChartDB", back_populates="basket", cascade="all, delete-orphan"
    )


class BasketChartDB(Base):
    """
    Basket-Chart Membership Table (Many-to-Many).

    Charts can belong to multiple baskets.
    Per Gold Standard Specification Section 15.5.
    """

    __tablename__ = "basket_charts"

    basket_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("analytical_baskets.basket_id"), primary_key=True
    )
    chart_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("charts.chart_id"), primary_key=True
    )
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    basket: Mapped["AnalyticalBasketDB"] = relationship(
        "AnalyticalBasketDB", back_populates="chart_associations"
    )
    chart: Mapped["ChartDB"] = relationship("ChartDB", back_populates="basket_associations")

    # Constraints
    __table_args__ = (
        Index("idx_basket_charts_basket", "basket_id"),
        Index("idx_basket_charts_chart", "chart_id"),
    )


# =============================================================================
# AI CONVERSATION AND USAGE TRACKING
# =============================================================================


class ConversationDB(Base):
    """
    AI Conversations Table.

    Stores per-instrument conversation history with Claude.
    Per Gold Standard Specification Section 14 (AI Integration).

    CRITICAL: All AI responses are DESCRIPTIVE only.
    Conversations are stored for context, NOT for learning/training.
    """

    __tablename__ = "conversations"

    conversation_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    instrument_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("instruments.instrument_id"), nullable=False
    )
    messages: Mapped[str] = mapped_column(
        JSON, nullable=False, default="[]"
    )  # Array of {role, content, timestamp}
    model_used: Mapped[str] = mapped_column(String(50), nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now, onupdate=utc_now
    )

    # Constraints
    __table_args__ = (
        Index("idx_conversations_instrument", "instrument_id"),
        Index("idx_conversations_created", "created_at"),
    )


class AIUsageDB(Base):
    """
    AI Usage Tracking Table.

    Tracks token usage, costs, and request counts for budgeting.
    Per Gold Standard Specification Section 14 (AI Integration).
    """

    __tablename__ = "ai_usage"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    period_type: Mapped[str] = mapped_column(String(20), nullable=False)  # DAILY, WEEKLY, MONTHLY
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False, default=0)
    requests_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    model_breakdown: Mapped[str] = mapped_column(
        JSON, nullable=False, default="{}"
    )  # Per-model stats
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    # Constraints
    __table_args__ = (
        UniqueConstraint("period_type", "period_start", name="uq_usage_period"),
        Index("idx_ai_usage_period", "period_type", "period_start"),
    )
