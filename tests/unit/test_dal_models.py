"""
Tests for CIA-SIE Database Models
=================================

Validates SQLAlchemy ORM models for constitutional compliance.

GOVERNED BY: Section 7.2 (Database Schema) and ADR-003
"""

import pytest
from datetime import datetime, UTC
from sqlalchemy import inspect

from cia_sie.dal.models import (
    InstrumentDB,
    SiloDB,
    ChartDB,
    SignalDB,
    AnalyticalBasketDB,
    BasketChartDB,
    ConversationDB,
    AIUsageDB,
    generate_uuid,
    utc_now,
)


class TestGenerateUUID:
    """Tests for UUID generation utility."""

    def test_generates_string(self):
        """Test UUID is generated as string."""
        result = generate_uuid()
        assert isinstance(result, str)

    def test_generates_valid_uuid_format(self):
        """Test UUID has valid format."""
        result = generate_uuid()
        # UUID format: 8-4-4-4-12
        assert len(result) == 36
        assert result.count("-") == 4

    def test_generates_unique_uuids(self):
        """Test UUIDs are unique."""
        uuids = [generate_uuid() for _ in range(100)]
        assert len(set(uuids)) == 100


class TestUtcNow:
    """Tests for UTC datetime utility."""

    def test_returns_datetime(self):
        """Test returns datetime object."""
        result = utc_now()
        assert isinstance(result, datetime)

    def test_returns_timezone_aware(self):
        """Test returns timezone-aware datetime."""
        result = utc_now()
        assert result.tzinfo is not None


class TestInstrumentDBModel:
    """Tests for InstrumentDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert InstrumentDB.__tablename__ == "instruments"

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(InstrumentDB)
        columns = {c.key for c in mapper.columns}

        assert "instrument_id" in columns
        assert "symbol" in columns
        assert "display_name" in columns
        assert "created_at" in columns
        assert "updated_at" in columns
        assert "is_active" in columns

    def test_symbol_is_unique(self):
        """Test symbol column has unique constraint."""
        mapper = inspect(InstrumentDB)
        symbol_col = mapper.columns["symbol"]
        assert symbol_col.unique is True

    def test_has_silos_relationship(self):
        """Test has relationship to silos."""
        assert hasattr(InstrumentDB, "silos")


class TestSiloDBModel:
    """Tests for SiloDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert SiloDB.__tablename__ == "silos"

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(SiloDB)
        columns = {c.key for c in mapper.columns}

        assert "silo_id" in columns
        assert "instrument_id" in columns
        assert "silo_name" in columns
        assert "heartbeat_enabled" in columns
        assert "heartbeat_frequency_min" in columns
        assert "current_threshold_min" in columns
        assert "recent_threshold_min" in columns
        assert "stale_threshold_min" in columns

    def test_has_instrument_foreign_key(self):
        """Test has foreign key to instruments."""
        mapper = inspect(SiloDB)
        instrument_id_col = mapper.columns["instrument_id"]
        assert len(instrument_id_col.foreign_keys) > 0


class TestChartDBModel:
    """Tests for ChartDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert ChartDB.__tablename__ == "charts"

    def test_has_no_weight_column(self):
        """
        CRITICAL TEST: ChartDB must NOT have weight column.

        Per ADR-003: Weights enable aggregation which is PROHIBITED.
        """
        mapper = inspect(ChartDB)
        columns = {c.key for c in mapper.columns}

        assert "weight" not in columns
        assert "priority" not in columns
        assert "importance" not in columns

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(ChartDB)
        columns = {c.key for c in mapper.columns}

        assert "chart_id" in columns
        assert "silo_id" in columns
        assert "chart_code" in columns
        assert "chart_name" in columns
        assert "timeframe" in columns
        assert "webhook_id" in columns

    def test_webhook_id_is_unique(self):
        """Test webhook_id column has unique constraint."""
        mapper = inspect(ChartDB)
        webhook_col = mapper.columns["webhook_id"]
        assert webhook_col.unique is True


class TestSignalDBModel:
    """Tests for SignalDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert SignalDB.__tablename__ == "signals"

    def test_has_no_confidence_column(self):
        """
        CRITICAL TEST: SignalDB must NOT have confidence column.

        Per ADR-003: Scores imply system judgment which is PROHIBITED.
        """
        mapper = inspect(SignalDB)
        columns = {c.key for c in mapper.columns}

        assert "confidence" not in columns
        assert "strength" not in columns
        assert "score" not in columns
        assert "weight" not in columns

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(SignalDB)
        columns = {c.key for c in mapper.columns}

        assert "signal_id" in columns
        assert "chart_id" in columns
        assert "received_at" in columns
        assert "signal_timestamp" in columns
        assert "signal_type" in columns
        assert "direction" in columns
        assert "indicators" in columns
        assert "raw_payload" in columns

    def test_preserves_raw_payload(self):
        """Test raw_payload column exists for audit trail."""
        mapper = inspect(SignalDB)
        columns = {c.key for c in mapper.columns}
        assert "raw_payload" in columns


class TestAnalyticalBasketDBModel:
    """Tests for AnalyticalBasketDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert AnalyticalBasketDB.__tablename__ == "analytical_baskets"

    def test_has_no_processing_columns(self):
        """
        CRITICAL TEST: Baskets must not have processing columns.

        Per ADR-002: Baskets are UI-layer constructs only.
        """
        mapper = inspect(AnalyticalBasketDB)
        columns = {c.key for c in mapper.columns}

        assert "aggregated_score" not in columns
        assert "weight" not in columns
        assert "priority" not in columns
        assert "overall_direction" not in columns

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(AnalyticalBasketDB)
        columns = {c.key for c in mapper.columns}

        assert "basket_id" in columns
        assert "basket_name" in columns
        assert "basket_type" in columns
        assert "description" in columns
        assert "instrument_id" in columns


class TestBasketChartDBModel:
    """Tests for BasketChartDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert BasketChartDB.__tablename__ == "basket_charts"

    def test_is_many_to_many(self):
        """Test it's a proper many-to-many join table."""
        mapper = inspect(BasketChartDB)
        columns = {c.key for c in mapper.columns}

        assert "basket_id" in columns
        assert "chart_id" in columns
        assert "added_at" in columns

    def test_has_relationships(self):
        """Test has relationships to both basket and chart."""
        assert hasattr(BasketChartDB, "basket")
        assert hasattr(BasketChartDB, "chart")


class TestConversationDBModel:
    """Tests for ConversationDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert ConversationDB.__tablename__ == "conversations"

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(ConversationDB)
        columns = {c.key for c in mapper.columns}

        assert "conversation_id" in columns
        assert "instrument_id" in columns
        assert "messages" in columns
        assert "model_used" in columns
        assert "total_tokens" in columns
        assert "total_cost" in columns


class TestAIUsageDBModel:
    """Tests for AIUsageDB SQLAlchemy model."""

    def test_table_name(self):
        """Test correct table name."""
        assert AIUsageDB.__tablename__ == "ai_usage"

    def test_has_required_columns(self):
        """Test all required columns exist."""
        mapper = inspect(AIUsageDB)
        columns = {c.key for c in mapper.columns}

        assert "id" in columns
        assert "period_type" in columns
        assert "period_start" in columns
        assert "period_end" in columns
        assert "input_tokens" in columns
        assert "output_tokens" in columns
        assert "total_cost" in columns
        assert "requests_count" in columns


class TestConstitutionalCompliance:
    """
    Comprehensive constitutional compliance tests for database models.

    CRITICAL: These tests verify the core prohibitions from Section 0B.
    """

    def test_no_weight_columns_anywhere(self):
        """
        CRITICAL: No weight columns in any table.

        Per Section 0B: Weights enable aggregation which is PROHIBITED.
        """
        models = [InstrumentDB, SiloDB, ChartDB, SignalDB, AnalyticalBasketDB]

        for model in models:
            mapper = inspect(model)
            columns = {c.key for c in mapper.columns}
            assert "weight" not in columns, \
                f"{model.__name__} has prohibited 'weight' column"

    def test_no_confidence_columns_anywhere(self):
        """
        CRITICAL: No confidence/score columns in any table.

        Per Section 0B: Scoring is PROHIBITED.
        """
        models = [InstrumentDB, SiloDB, ChartDB, SignalDB, AnalyticalBasketDB]

        for model in models:
            mapper = inspect(model)
            columns = {c.key for c in mapper.columns}
            assert "confidence" not in columns, \
                f"{model.__name__} has prohibited 'confidence' column"
            assert "score" not in columns, \
                f"{model.__name__} has prohibited 'score' column"
            assert "strength" not in columns, \
                f"{model.__name__} has prohibited 'strength' column"

    def test_no_aggregation_columns_anywhere(self):
        """
        CRITICAL: No aggregation-related columns in any table.

        Per Section 0B: Aggregation is PROHIBITED.
        """
        prohibited_columns = [
            "aggregated_direction",
            "overall_direction",
            "net_direction",
            "combined_score",
            "aggregate_score",
        ]

        models = [InstrumentDB, SiloDB, ChartDB, SignalDB, AnalyticalBasketDB]

        for model in models:
            mapper = inspect(model)
            columns = {c.key for c in mapper.columns}
            for prohibited in prohibited_columns:
                assert prohibited not in columns, \
                    f"{model.__name__} has prohibited '{prohibited}' column"

    def test_no_recommendation_columns_anywhere(self):
        """
        CRITICAL: No recommendation columns in any table.

        Per Section 0B.5 P-04: Recommendations are PROHIBITED.
        """
        models = [InstrumentDB, SiloDB, ChartDB, SignalDB, AnalyticalBasketDB]

        for model in models:
            mapper = inspect(model)
            columns = {c.key for c in mapper.columns}
            assert "recommendation" not in columns, \
                f"{model.__name__} has prohibited 'recommendation' column"
            assert "advice" not in columns, \
                f"{model.__name__} has prohibited 'advice' column"
            assert "action" not in columns, \
                f"{model.__name__} has prohibited 'action' column"
