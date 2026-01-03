"""Initial CIA-SIE database schema

Revision ID: 0001
Revises: None
Create Date: 2025-12-30

CIA-SIE Database Migration
==========================

Initial schema migration establishing the core database structure
per Gold Standard Specification Section 7.2.

IMPORTANT: Per Gold Standard Specification Section 0B (Constitutional Prohibitions):
- NO columns for weights, scores, or confidence may be added
- NO aggregation or recommendation columns permitted
- All charts and signals must remain equal standing

Tables Created:
- instruments: Tradeable financial assets
- silos: Logical containers for charts
- charts: TradingView chart configurations
- signals: Point-in-time signal emissions
- analytical_baskets: User-defined chart groupings (UI-only)
- basket_charts: Many-to-many basket membership
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply migration changes - create all tables."""

    # Create instruments table
    op.create_table(
        'instruments',
        sa.Column('instrument_id', sa.String(36), primary_key=True),
        sa.Column('symbol', sa.String(50), unique=True, nullable=False),
        sa.Column('display_name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('metadata_json', sa.JSON, nullable=True),
    )

    # Create silos table
    op.create_table(
        'silos',
        sa.Column('silo_id', sa.String(36), primary_key=True),
        sa.Column('instrument_id', sa.String(36), sa.ForeignKey('instruments.instrument_id'), nullable=False),
        sa.Column('silo_name', sa.String(100), nullable=False),
        sa.Column('heartbeat_enabled', sa.Boolean, nullable=False, default=True),
        sa.Column('heartbeat_frequency_min', sa.Integer, nullable=False, default=5),
        sa.Column('current_threshold_min', sa.Integer, nullable=False, default=2),
        sa.Column('recent_threshold_min', sa.Integer, nullable=False, default=10),
        sa.Column('stale_threshold_min', sa.Integer, nullable=False, default=30),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.UniqueConstraint('instrument_id', 'silo_name', name='uq_silo_name_per_instrument'),
    )
    op.create_index('idx_silos_instrument', 'silos', ['instrument_id'])

    # Create charts table (NO WEIGHT COLUMN - PROHIBITED)
    op.create_table(
        'charts',
        sa.Column('chart_id', sa.String(36), primary_key=True),
        sa.Column('silo_id', sa.String(36), sa.ForeignKey('silos.silo_id'), nullable=False),
        sa.Column('chart_code', sa.String(50), nullable=False),
        sa.Column('chart_name', sa.String(100), nullable=False),
        sa.Column('timeframe', sa.String(10), nullable=False),
        sa.Column('webhook_id', sa.String(100), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        # NOTE: NO weight column - prohibited by Section 0B
        sa.UniqueConstraint('silo_id', 'chart_code', name='uq_chart_code_per_silo'),
    )
    op.create_index('idx_charts_silo', 'charts', ['silo_id'])
    op.create_index('idx_charts_webhook', 'charts', ['webhook_id'])

    # Create signals table (NO CONFIDENCE COLUMN - PROHIBITED)
    op.create_table(
        'signals',
        sa.Column('signal_id', sa.String(36), primary_key=True),
        sa.Column('chart_id', sa.String(36), sa.ForeignKey('charts.chart_id'), nullable=False),
        sa.Column('received_at', sa.DateTime, nullable=False),
        sa.Column('signal_timestamp', sa.DateTime, nullable=False),
        sa.Column('signal_type', sa.String(20), nullable=False),
        sa.Column('direction', sa.String(20), nullable=False),
        sa.Column('indicators', sa.JSON, nullable=False),
        sa.Column('raw_payload', sa.JSON, nullable=False),
        # NOTE: NO confidence column - prohibited by Section 0B
    )
    op.create_index('idx_signals_chart', 'signals', ['chart_id'])
    op.create_index('idx_signals_timestamp', 'signals', ['signal_timestamp'])

    # Create analytical_baskets table (UI-only construct)
    op.create_table(
        'analytical_baskets',
        sa.Column('basket_id', sa.String(36), primary_key=True),
        sa.Column('basket_name', sa.String(100), nullable=False),
        sa.Column('basket_type', sa.String(20), nullable=False, default='CUSTOM'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('instrument_id', sa.String(36), sa.ForeignKey('instruments.instrument_id'), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
    )

    # Create basket_charts table (many-to-many)
    op.create_table(
        'basket_charts',
        sa.Column('basket_id', sa.String(36), sa.ForeignKey('analytical_baskets.basket_id'), primary_key=True),
        sa.Column('chart_id', sa.String(36), sa.ForeignKey('charts.chart_id'), primary_key=True),
        sa.Column('added_at', sa.DateTime, nullable=False),
    )
    op.create_index('idx_basket_charts_basket', 'basket_charts', ['basket_id'])
    op.create_index('idx_basket_charts_chart', 'basket_charts', ['chart_id'])


def downgrade() -> None:
    """Revert migration changes - drop all tables."""
    op.drop_table('basket_charts')
    op.drop_table('analytical_baskets')
    op.drop_table('signals')
    op.drop_table('charts')
    op.drop_table('silos')
    op.drop_table('instruments')
