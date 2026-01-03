"""
CIA-SIE AI Usage Tracker
========================

Tracks AI usage, costs, and budget management.

GOVERNED BY: Section 14 (AI Narrative Engine)
"""

import logging
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.ai.model_registry import estimate_cost
from cia_sie.core.config import get_settings
from cia_sie.core.enums import UsagePeriod
from cia_sie.dal.models import AIUsageDB

logger = logging.getLogger(__name__)


class UsageTracker:
    """
    Tracks AI usage and manages budgets.

    Features:
    - Track token usage per request
    - Calculate costs
    - Monitor budget limits
    - Alert at thresholds
    """

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session
        self.settings = get_settings()

    async def record_usage(
        self,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
    ) -> dict:
        """
        Record AI usage for a request.

        Args:
            model_id: Model used
            input_tokens: Input tokens consumed
            output_tokens: Output tokens generated

        Returns:
            Usage record with cost info
        """
        cost = estimate_cost(model_id, input_tokens, output_tokens)
        today = date.today()

        # Get or create monthly usage record
        monthly_usage = await self._get_or_create_period_usage(UsagePeriod.MONTHLY, today)

        # Update totals
        monthly_usage.input_tokens += input_tokens
        monthly_usage.output_tokens += output_tokens
        monthly_usage.total_cost = Decimal(str(float(monthly_usage.total_cost) + cost))
        monthly_usage.requests_count += 1

        # Update model breakdown
        breakdown = monthly_usage.model_breakdown or {}
        if isinstance(breakdown, str):
            import json

            breakdown = json.loads(breakdown) if breakdown else {}

        if model_id not in breakdown:
            breakdown[model_id] = {
                "requests": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cost": 0,
            }

        breakdown[model_id]["requests"] += 1
        breakdown[model_id]["input_tokens"] += input_tokens
        breakdown[model_id]["output_tokens"] += output_tokens
        breakdown[model_id]["cost"] += cost

        monthly_usage.model_breakdown = breakdown

        await self.session.flush()

        return {
            "model_id": model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "period_total_cost": float(monthly_usage.total_cost),
        }

    async def get_usage(
        self,
        period: UsagePeriod = UsagePeriod.MONTHLY,
    ) -> dict:
        """
        Get usage statistics for a period.

        Args:
            period: Time period (DAILY, WEEKLY, MONTHLY)

        Returns:
            Usage statistics
        """
        today = date.today()
        usage = await self._get_or_create_period_usage(period, today)

        budget_limit = self.settings.ai_budget_limit
        used = float(usage.total_cost)
        remaining = max(0, budget_limit - used)
        percentage_used = (used / budget_limit * 100) if budget_limit > 0 else 0

        return {
            "period": period.value.lower(),
            "period_start": usage.period_start.isoformat(),
            "period_end": usage.period_end.isoformat(),
            "tokens_used": {
                "input": usage.input_tokens,
                "output": usage.output_tokens,
                "total": usage.input_tokens + usage.output_tokens,
            },
            "cost": {
                "amount": round(used, 4),
                "currency": "USD",
            },
            "budget": {
                "limit": budget_limit,
                "used": round(used, 4),
                "remaining": round(remaining, 4),
                "percentage_used": round(percentage_used, 1),
            },
            "requests_count": usage.requests_count,
            "average_tokens_per_request": (
                (usage.input_tokens + usage.output_tokens) // usage.requests_count
                if usage.requests_count > 0
                else 0
            ),
            "model_breakdown": self._format_model_breakdown(usage.model_breakdown),
        }

    async def check_budget(self) -> dict:
        """
        Check budget status.

        Returns:
            Budget status with alerts
        """
        usage = await self.get_usage(UsagePeriod.MONTHLY)
        percentage_used = usage["budget"]["percentage_used"]
        alert_threshold = self.settings.ai_budget_alert_threshold

        status = {
            "within_budget": percentage_used < 100,
            "percentage_used": percentage_used,
            "remaining": usage["budget"]["remaining"],
            "alert_level": None,
            "message": None,
        }

        if percentage_used >= 100:
            status["alert_level"] = "blocked"
            status["message"] = "Monthly AI budget exhausted. AI features disabled."
        elif percentage_used >= 90:
            status["alert_level"] = "critical"
            status["message"] = f"Budget critical: {percentage_used:.0f}% used."
        elif percentage_used >= alert_threshold:
            status["alert_level"] = "warning"
            status["message"] = f"Budget warning: {percentage_used:.0f}% used."

        return status

    async def _get_or_create_period_usage(
        self,
        period: UsagePeriod,
        reference_date: date,
    ) -> AIUsageDB:
        """Get or create usage record for a period."""
        period_start, period_end = self._get_period_bounds(period, reference_date)

        # Try to find existing record
        stmt = select(AIUsageDB).where(
            and_(
                AIUsageDB.period_type == period.value,
                AIUsageDB.period_start == period_start,
            )
        )
        result = await self.session.execute(stmt)
        usage = result.scalar_one_or_none()

        if not usage:
            # Create new record
            usage = AIUsageDB(
                period_type=period.value,
                period_start=period_start,
                period_end=period_end,
                input_tokens=0,
                output_tokens=0,
                total_cost=Decimal("0"),
                requests_count=0,
                model_breakdown={},
            )
            self.session.add(usage)
            await self.session.flush()

        return usage

    def _get_period_bounds(
        self,
        period: UsagePeriod,
        reference_date: date,
    ) -> tuple[date, date]:
        """Get start and end dates for a period."""
        if period == UsagePeriod.DAILY:
            return reference_date, reference_date

        elif period == UsagePeriod.WEEKLY:
            # Start on Monday
            start = reference_date - timedelta(days=reference_date.weekday())
            end = start + timedelta(days=6)
            return start, end

        else:  # MONTHLY
            start = reference_date.replace(day=1)
            # Last day of month
            if reference_date.month == 12:
                end = reference_date.replace(year=reference_date.year + 1, month=1, day=1)
            else:
                end = reference_date.replace(month=reference_date.month + 1, day=1)
            end = end - timedelta(days=1)
            return start, end

    def _format_model_breakdown(self, breakdown: Optional[dict | str]) -> list[dict]:
        """Format model breakdown for API response."""
        if not breakdown:
            return []

        if isinstance(breakdown, str):
            import json

            breakdown = json.loads(breakdown) if breakdown else {}

        return [
            {
                "model_id": model_id,
                "requests": stats.get("requests", 0),
                "tokens": stats.get("input_tokens", 0) + stats.get("output_tokens", 0),
                "cost": round(stats.get("cost", 0), 4),
            }
            for model_id, stats in breakdown.items()
        ]
