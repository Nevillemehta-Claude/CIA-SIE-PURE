"""
CIA-SIE Narrative Prompt Builder
================================

Builds prompts for Claude to generate DESCRIPTIVE narratives.

GOVERNED BY: Section 14.5 (AI Prompt Template)

CRITICAL: The prompts are carefully constructed to ensure
Claude generates DESCRIPTIVE output, never PRESCRIPTIVE.
"""

from enum import Enum
from typing import Union

from cia_sie.core.models import ChartSignalStatus, RelationshipSummary


def _get_enum_value(value: Union[Enum, str]) -> str:
    """
    Safely extract string value from enum or string.

    Pydantic v2 serializes enums to strings, so we need to handle both cases.

    Args:
        value: Either an Enum instance or a string

    Returns:
        String value
    """
    if isinstance(value, Enum):
        return value.value
    return str(value)


# =============================================================================
# SYSTEM PROMPT (Section 14.5)
# =============================================================================

NARRATIVE_SYSTEM_PROMPT = """You are a signal description assistant for the CIA-SIE trading analysis platform.

Your role is to DESCRIBE what trading signals are showing in plain English.

CRITICAL CONSTRAINTS - YOU MUST FOLLOW THESE:

1. DESCRIBE signals, do not PRESCRIBE actions
   - Good: "Chart 01A shows BULLISH with RSI at 28"
   - Bad: "You should buy" or "Consider entering a position"

2. EXPOSE contradictions, do not RESOLVE them
   - Good: "Charts 01A and 02 show opposing directions"
   - Bad: "The daily signal is more reliable than weekly"

3. Use plain English, avoid unexplained jargon
   - Good: "RSI at 28 indicates oversold conditions"
   - Bad: "RSI28 OB divergence confirmed"

4. Every response must end with the user authority reminder:
   "The interpretation and decision is yours."

5. NEVER use these phrases:
   - "you should"
   - "I recommend"
   - "the best action"
   - "you might want to"
   - "consider buying/selling"
   - "overall direction is"
   - "confidence level is"
   - "signal strength is"

6. NEVER compute:
   - Overall direction from multiple signals
   - Confidence scores or percentages
   - Rankings of which signals are "better"
   - Net position or summary bias

7. ALWAYS present ALL signals with equal weight
   - Do not emphasize one signal over another
   - Do not suggest one timeframe is more important

Remember: You are an information provider, not an advisor.
The user makes ALL decisions. You provide clarity, not direction."""


# =============================================================================
# PROMPT BUILDER
# =============================================================================


class NarrativePromptBuilder:
    """
    Builds prompts for narrative generation.

    Per Gold Standard Specification Section 14.5:
    - Prompts are structured to ensure descriptive output
    - All relevant data is included for context
    - Explicit instructions prevent prescriptive content
    """

    def __init__(self):
        self.system_prompt = NARRATIVE_SYSTEM_PROMPT

    def build_silo_narrative_prompt(
        self,
        summary: RelationshipSummary,
    ) -> str:
        """
        Build a prompt for describing a silo's signal state.

        Args:
            summary: RelationshipSummary containing all data

        Returns:
            Formatted user prompt for Claude
        """
        lines = [
            "Please describe the following trading signals in plain English.",
            "",
            f"INSTRUMENT: {summary.instrument_symbol}",
            f"SILO: {summary.silo_name}",
            f"GENERATED AT: {summary.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "=" * 60,
            "CHARTS AND SIGNALS:",
            "=" * 60,
        ]

        # Add each chart's status
        for chart in summary.charts:
            lines.append("")
            lines.append(f"Chart: {chart.chart_name} ({chart.chart_code})")
            lines.append(f"Timeframe: {chart.timeframe}")
            lines.append(f"Freshness: {_get_enum_value(chart.freshness)}")

            if chart.latest_signal:
                signal = chart.latest_signal
                lines.append(f"Direction: {_get_enum_value(signal.direction)}")
                lines.append(f"Signal Type: {_get_enum_value(signal.signal_type)}")

                # Add indicator values if present
                if signal.indicators:
                    lines.append("Indicators:")
                    for key, value in signal.indicators.items():
                        lines.append(f"  - {key}: {value}")
            else:
                lines.append("Direction: NO SIGNAL AVAILABLE")

        # Add contradictions section
        if summary.contradictions:
            lines.append("")
            lines.append("=" * 60)
            lines.append("CONTRADICTIONS DETECTED:")
            lines.append("=" * 60)

            for c in summary.contradictions:
                lines.append(
                    f"- {c.chart_a_name} ({_get_enum_value(c.chart_a_direction)}) "
                    f"vs {c.chart_b_name} ({_get_enum_value(c.chart_b_direction)})"
                )

        # Add confirmations section
        if summary.confirmations:
            lines.append("")
            lines.append("=" * 60)
            lines.append("CONFIRMATIONS DETECTED:")
            lines.append("=" * 60)

            for c in summary.confirmations:
                lines.append(
                    f"- {c.chart_a_name} and {c.chart_b_name} "
                    f"both show {_get_enum_value(c.aligned_direction)}"
                )

        # Instructions for the narrative
        lines.append("")
        lines.append("=" * 60)
        lines.append("INSTRUCTIONS:")
        lines.append("=" * 60)
        lines.append("")
        lines.append("Generate a plain-English description that:")
        lines.append("1. Summarizes what each chart is showing")
        lines.append("2. Explicitly notes any contradictions")
        lines.append("3. Notes any confirmations (without implying they're 'better')")
        lines.append("4. Includes freshness information where relevant")
        lines.append("5. Reminds the user that interpretation is theirs")
        lines.append("")
        lines.append("DO NOT:")
        lines.append("- Recommend any action")
        lines.append("- Suggest overall direction")
        lines.append("- Rank or prioritize signals")
        lines.append("- Compute confidence or strength")

        return "\n".join(lines)

    def build_chart_narrative_prompt(
        self,
        chart_status: ChartSignalStatus,
        instrument_symbol: str,
    ) -> str:
        """
        Build a prompt for describing a single chart's signal.

        Args:
            chart_status: The chart status to describe
            instrument_symbol: Symbol of the instrument

        Returns:
            Formatted user prompt for Claude
        """
        lines = [
            "Please describe the following chart signal in plain English.",
            "",
            f"INSTRUMENT: {instrument_symbol}",
            f"CHART: {chart_status.chart_name} ({chart_status.chart_code})",
            f"TIMEFRAME: {chart_status.timeframe}",
            f"FRESHNESS: {_get_enum_value(chart_status.freshness)}",
        ]

        if chart_status.latest_signal:
            signal = chart_status.latest_signal
            lines.append(f"DIRECTION: {_get_enum_value(signal.direction)}")
            lines.append(f"SIGNAL TYPE: {_get_enum_value(signal.signal_type)}")

            if signal.indicators:
                lines.append("")
                lines.append("INDICATORS:")
                for key, value in signal.indicators.items():
                    lines.append(f"  {key}: {value}")
        else:
            lines.append("")
            lines.append("NO SIGNAL DATA AVAILABLE")

        lines.append("")
        lines.append("Provide a brief, plain-English description of what this chart is showing.")
        lines.append("End with: 'The interpretation and decision is yours.'")

        return "\n".join(lines)

    def build_contradiction_narrative_prompt(
        self,
        contradictions: list,
        instrument_symbol: str,
    ) -> str:
        """
        Build a prompt specifically for explaining contradictions.

        Args:
            contradictions: List of Contradiction objects
            instrument_symbol: Symbol of the instrument

        Returns:
            Formatted user prompt for Claude
        """
        lines = [
            "Please describe the following contradictions in plain English.",
            "",
            f"INSTRUMENT: {instrument_symbol}",
            "",
            "CONTRADICTIONS:",
        ]

        for i, c in enumerate(contradictions, 1):
            lines.append(
                f"{i}. {c.chart_a_name} shows {_get_enum_value(c.chart_a_direction)}, "
                f"while {c.chart_b_name} shows {_get_enum_value(c.chart_b_direction)}"
            )

        lines.append("")
        lines.append("Explain what these contradictions mean in plain English.")
        lines.append("DO NOT suggest which signal is 'correct' or which to follow.")
        lines.append("DO NOT recommend any action.")
        lines.append("End with: 'The interpretation and decision is yours.'")

        return "\n".join(lines)
