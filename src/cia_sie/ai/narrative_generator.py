"""
CIA-SIE Narrative Generator
===========================

Generates DESCRIPTIVE plain-English narratives using Claude.

GOVERNED BY: Section 14 (AI Narrative Engine)

Per Gold Standard Specification Section 14.4:
- Generated narratives are DESCRIPTIVE only
- Must include closing statement about user authority
- PROHIBITED: recommendations, direction inference, confidence scores

REQUIRED CLOSING STATEMENT:
"This is a description of what your charts are showing.
The interpretation and any decision is entirely yours."
"""

import logging
from datetime import datetime
from typing import Optional
from uuid import uuid4

from cia_sie.ai.claude_client import ClaudeClient
from cia_sie.ai.prompt_builder import NarrativePromptBuilder, _get_enum_value
from cia_sie.ai.response_validator import (
    MANDATORY_DISCLAIMER,
    AIResponseValidator,
    ValidatedResponseGenerator,
)
from cia_sie.core.enums import NarrativeSectionType, ValidationStatus
from cia_sie.core.models import (
    ChartSignalStatus,
    Narrative,
    NarrativeSection,
    RelationshipSummary,
)

logger = logging.getLogger(__name__)


# Required closing statement per Section 14.4
# Now imported from response_validator as MANDATORY_DISCLAIMER
REQUIRED_CLOSING = MANDATORY_DISCLAIMER


class NarrativeGenerator:
    """
    Generates descriptive narratives for signal relationships.

    Per Gold Standard Specification Section 14.4:
    - All output is DESCRIPTIVE, never PRESCRIPTIVE
    - Must include user authority reminder
    - Must NOT include recommendations, scores, rankings

    Uses AIResponseValidator for constitutional compliance checking
    with automatic retry logic on validation failures.
    """

    def __init__(
        self,
        claude_client: Optional[ClaudeClient] = None,
        prompt_builder: Optional[NarrativePromptBuilder] = None,
        validator: Optional[AIResponseValidator] = None,
        max_retries: int = 3,
    ):
        self.claude = claude_client or ClaudeClient()
        self.prompt_builder = prompt_builder or NarrativePromptBuilder()
        self.validator = validator or AIResponseValidator()
        self.max_retries = max_retries

        # Create validated generator for retry logic
        self._validated_generator = ValidatedResponseGenerator(
            claude_client=self.claude,
            validator=self.validator,
            max_retries=self.max_retries,
        )

    async def generate_silo_narrative(
        self,
        summary: RelationshipSummary,
        use_validated_generator: bool = True,
    ) -> Narrative:
        """
        Generate a narrative for a silo's relationship summary.

        Args:
            summary: RelationshipSummary containing all data
            use_validated_generator: If True, use retry logic on validation failure

        Returns:
            Narrative with sections and closing statement

        Raises:
            ConstitutionalViolationError: If all validation retries fail
        """
        # Build the prompt
        user_prompt = self.prompt_builder.build_silo_narrative_prompt(summary)

        if use_validated_generator:
            # Use validated generator with automatic retry
            try:
                cleaned_narrative = await self._validated_generator.generate(
                    system_prompt=self.prompt_builder.system_prompt,
                    user_prompt=user_prompt,
                    max_tokens=2000,
                    temperature=0.3,
                )
            except Exception as e:
                logger.error(f"Validated generation failed: {e}, using fallback")
                return self.generate_fallback_narrative(summary)
        else:
            # Legacy path: generate and post-process
            raw_narrative = await self.claude.generate(
                system_prompt=self.prompt_builder.system_prompt,
                user_prompt=user_prompt,
                max_tokens=2000,
                temperature=0.3,
            )
            # Post-process to ensure compliance
            cleaned_narrative = self._ensure_compliance(raw_narrative)

        # Build sections
        sections = [
            NarrativeSection(
                section_type=NarrativeSectionType.SIGNAL_SUMMARY,
                content=cleaned_narrative,
                referenced_chart_ids=[cs.chart_id for cs in summary.charts],
            )
        ]

        # Add contradiction section if present
        if summary.contradictions:
            sections.append(
                NarrativeSection(
                    section_type=NarrativeSectionType.CONTRADICTION,
                    content=self._format_contradiction_summary(summary.contradictions),
                    referenced_chart_ids=[c.chart_a_id for c in summary.contradictions]
                    + [c.chart_b_id for c in summary.contradictions],
                )
            )

        return Narrative(
            narrative_id=uuid4(),
            silo_id=summary.silo_id,
            sections=sections,
            closing_statement=REQUIRED_CLOSING,
            generated_at=datetime.utcnow(),
        )

    async def generate_chart_narrative(
        self,
        chart_status: ChartSignalStatus,
        instrument_symbol: str,
        use_validated_generator: bool = True,
    ) -> Narrative:
        """
        Generate a narrative for a single chart.

        Args:
            chart_status: The chart to describe
            instrument_symbol: Symbol of the instrument
            use_validated_generator: If True, use retry logic on validation failure

        Returns:
            Narrative describing the chart's signal

        Raises:
            ConstitutionalViolationError: If all validation retries fail
        """
        user_prompt = self.prompt_builder.build_chart_narrative_prompt(
            chart_status, instrument_symbol
        )

        if use_validated_generator:
            try:
                cleaned_narrative = await self._validated_generator.generate(
                    system_prompt=self.prompt_builder.system_prompt,
                    user_prompt=user_prompt,
                    max_tokens=500,
                    temperature=0.3,
                )
            except Exception as e:
                logger.error(f"Validated chart generation failed: {e}")
                # Fallback to simple description
                cleaned_narrative = self._generate_simple_chart_description(
                    chart_status, instrument_symbol
                )
        else:
            raw_narrative = await self.claude.generate(
                system_prompt=self.prompt_builder.system_prompt,
                user_prompt=user_prompt,
                max_tokens=500,
                temperature=0.3,
            )
            cleaned_narrative = self._ensure_compliance(raw_narrative)

        sections = [
            NarrativeSection(
                section_type=NarrativeSectionType.SIGNAL_SUMMARY,
                content=cleaned_narrative,
                referenced_chart_ids=[chart_status.chart_id],
            )
        ]

        return Narrative(
            narrative_id=uuid4(),
            silo_id=chart_status.chart_id,  # Using chart_id as pseudo-silo
            sections=sections,
            closing_statement=REQUIRED_CLOSING,
            generated_at=datetime.utcnow(),
        )

    def _ensure_compliance(self, narrative: str) -> str:
        """
        Post-process narrative to ensure constitutional compliance.

        Uses the AIResponseValidator for comprehensive regex-based validation.
        Falls back to simple phrase replacement if validation fails.

        Args:
            narrative: Raw narrative from Claude

        Returns:
            Cleaned narrative
        """
        # Use the validator for comprehensive check
        result = self.validator.validate(narrative)

        if result.is_valid:
            if result.status == ValidationStatus.REMEDIATED:
                logger.info("Narrative was remediated by validator")
                return result.remediated_text
            return narrative

        # Validation failed - attempt manual cleanup
        logger.warning(f"Narrative validation failed: {result.violations}")

        # Prohibited phrases to remove or flag (legacy fallback)
        prohibited_phrases = [
            "you should",
            "i recommend",
            "the best action",
            "consider buying",
            "consider selling",
            "overall direction is",
            "net signal is",
            "confidence level",
            "signal strength is",
        ]

        cleaned = narrative
        for phrase in prohibited_phrases:
            if phrase.lower() in cleaned.lower():
                logger.warning(f"Removing prohibited phrase from narrative: {phrase}")
                # Replace with neutral alternative
                cleaned = cleaned.replace(phrase, "[DESCRIPTION ONLY]")
                cleaned = cleaned.replace(phrase.title(), "[DESCRIPTION ONLY]")
                cleaned = cleaned.replace(phrase.upper(), "[DESCRIPTION ONLY]")

        # Ensure disclaimer is present
        if MANDATORY_DISCLAIMER not in cleaned:
            cleaned = cleaned.rstrip() + "\n\n" + MANDATORY_DISCLAIMER

        return cleaned

    def _generate_simple_chart_description(
        self,
        chart_status: ChartSignalStatus,
        instrument_symbol: str,
    ) -> str:
        """
        Generate a simple chart description without AI.

        Fallback when validated generation fails.
        """
        if chart_status.latest_signal:
            direction = _get_enum_value(chart_status.latest_signal.direction)
            signal_type = _get_enum_value(chart_status.latest_signal.signal_type)
            lines = [
                f"Chart {chart_status.chart_name} ({chart_status.chart_code}) "
                f"for {instrument_symbol} shows {direction}.",
                "",
                f"Timeframe: {chart_status.timeframe}",
                f"Signal type: {signal_type}",
                f"Freshness: {_get_enum_value(chart_status.freshness)}",
            ]

            if chart_status.latest_signal.indicators:
                lines.append("")
                lines.append("Indicators:")
                for key, value in chart_status.latest_signal.indicators.items():
                    lines.append(f"  - {key}: {value}")
        else:
            lines = [
                f"Chart {chart_status.chart_name} ({chart_status.chart_code}) "
                f"for {instrument_symbol} has no signal data available.",
                "",
                f"Timeframe: {chart_status.timeframe}",
                f"Freshness: {_get_enum_value(chart_status.freshness)}",
            ]

        return "\n".join(lines)

    def _format_contradiction_summary(self, contradictions: list) -> str:
        """Format contradictions into readable text."""
        if not contradictions:
            return "No contradictions detected."

        lines = ["The following contradictions have been detected:"]
        for c in contradictions:
            lines.append(
                f"- {c.chart_a_name} ({_get_enum_value(c.chart_a_direction)}) "
                f"vs {c.chart_b_name} ({_get_enum_value(c.chart_b_direction)})"
            )
        lines.append("")
        lines.append("These conflicting signals are presented for your review.")
        lines.append("The system does not determine which signal is correct.")

        return "\n".join(lines)

    def generate_fallback_narrative(
        self,
        summary: RelationshipSummary,
    ) -> Narrative:
        """
        Generate a narrative without using AI.

        Fallback when Claude is unavailable.

        Args:
            summary: RelationshipSummary to describe

        Returns:
            Basic narrative without AI enhancement
        """
        lines = [
            f"Signal summary for {summary.instrument_symbol} - {summary.silo_name}:",
            "",
        ]

        # Describe each chart
        for cs in summary.charts:
            if cs.latest_signal:
                lines.append(
                    f"- {cs.chart_name} ({cs.timeframe}): "
                    f"{_get_enum_value(cs.latest_signal.direction)} "
                    f"[{_get_enum_value(cs.freshness)}]"
                )
            else:
                lines.append(
                    f"- {cs.chart_name} ({cs.timeframe}): "
                    f"No signal available [{_get_enum_value(cs.freshness)}]"
                )

        # Note contradictions
        if summary.contradictions:
            lines.append("")
            lines.append("Contradictions detected:")
            for c in summary.contradictions:
                lines.append(
                    f"- {c.chart_a_name} ({_get_enum_value(c.chart_a_direction)}) "
                    f"vs {c.chart_b_name} ({_get_enum_value(c.chart_b_direction)})"
                )

        # Note confirmations
        if summary.confirmations:
            lines.append("")
            lines.append("Confirmations detected:")
            for c in summary.confirmations:
                lines.append(
                    f"- {c.chart_a_name} and {c.chart_b_name} "
                    f"align on {_get_enum_value(c.aligned_direction)}"
                )

        content = "\n".join(lines)

        return Narrative(
            narrative_id=uuid4(),
            silo_id=summary.silo_id,
            sections=[
                NarrativeSection(
                    section_type=NarrativeSectionType.SIGNAL_SUMMARY,
                    content=content,
                    referenced_chart_ids=[cs.chart_id for cs in summary.charts],
                )
            ],
            closing_statement=REQUIRED_CLOSING,
            generated_at=datetime.utcnow(),
        )
