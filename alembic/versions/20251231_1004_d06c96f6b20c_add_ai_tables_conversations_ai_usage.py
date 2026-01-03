"""Add AI tables (conversations, ai_usage)

Revision ID: d06c96f6b20c
Revises: 0001
Create Date: 2025-12-31 10:04:10.946273+00:00

CIA-SIE Database Migration
==========================

Adds support for AI features:
- conversations: Per-instrument chat history with Claude
- ai_usage: Token and cost tracking by period (daily/weekly/monthly)

NOTE: Tables may already exist if init_db() was called at startup.
This migration uses IF NOT EXISTS to be idempotent.

IMPLEMENTATION NOTE: Raw SQL (op.execute) is used instead of Alembic operations
(op.create_table) because SQLite requires IF NOT EXISTS for idempotent migrations.
Alembic's op.create_table doesn't support IF NOT EXISTS natively. This approach
ensures migrations can be re-run safely without errors if tables already exist.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd06c96f6b20c'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply migration changes."""
    # Create conversations table for per-instrument chat history
    op.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id VARCHAR(36) NOT NULL PRIMARY KEY,
            instrument_id VARCHAR(36) NOT NULL REFERENCES instruments(instrument_id),
            messages JSON NOT NULL DEFAULT '[]',
            model_used VARCHAR(50) NOT NULL,
            total_tokens INTEGER NOT NULL DEFAULT 0,
            total_cost NUMERIC(10, 6) NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indexes for conversations
    op.execute("CREATE INDEX IF NOT EXISTS idx_conversations_instrument ON conversations(instrument_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_conversations_created ON conversations(created_at)")

    # Create ai_usage table for budget/usage tracking
    op.execute("""
        CREATE TABLE IF NOT EXISTS ai_usage (
            id VARCHAR(36) NOT NULL PRIMARY KEY,
            period_type VARCHAR(20) NOT NULL,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            input_tokens INTEGER NOT NULL DEFAULT 0,
            output_tokens INTEGER NOT NULL DEFAULT 0,
            total_cost NUMERIC(10, 6) NOT NULL DEFAULT 0,
            requests_count INTEGER NOT NULL DEFAULT 0,
            model_breakdown JSON NOT NULL DEFAULT '{}',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(period_type, period_start)
        )
    """)

    # Create index for ai_usage
    op.execute("CREATE INDEX IF NOT EXISTS idx_ai_usage_period ON ai_usage(period_type, period_start)")


def downgrade() -> None:
    """Revert migration changes."""
    op.drop_table('ai_usage')
    op.drop_table('conversations')
