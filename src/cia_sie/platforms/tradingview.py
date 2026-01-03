"""
CIA-SIE TradingView Platform Adapter
====================================

Adapter for TradingView integration.

GOVERNED BY: Section 8 (Platform-Agnostic Integration)

TradingView Integration Model:
- Primary: Webhook-based signal delivery
- Signals flow from TradingView alerts to CIA-SIE via webhooks
- No public API for watchlist access
- User manually configures instruments and charts

CRITICAL NOTE:
TradingView does NOT have a public REST API. Integration is primarily
through webhooks that users configure in their TradingView alerts.

Indicator values (RSI, MACD, etc.) are included in the alert message
payload by the user's Pine Script configuration.
"""

import logging
from typing import Optional

from cia_sie.platforms.base import (
    ConnectionStatus,
    PlatformAdapter,
    PlatformCredentials,
    PlatformInstrument,
    WatchlistInfo,
)

logger = logging.getLogger(__name__)


class TradingViewAdapter(PlatformAdapter):
    """
    TradingView platform adapter.

    Per Gold Standard Specification Section 8.

    TradingView integration is WEBHOOK-BASED:
    1. User creates charts and alerts in TradingView
    2. User configures alert webhook URL pointing to CIA-SIE
    3. Alert message includes signal data (direction, indicators)
    4. CIA-SIE receives and processes signals via webhook endpoint

    This adapter provides:
    - Webhook URL templates for easy configuration
    - Alert message templates with indicator placeholders
    - Configuration guidance for users

    This adapter does NOT provide:
    - Watchlist import (no public API)
    - Real-time market data pull (webhook-push only)
    """

    def __init__(self, webhook_base_url: Optional[str] = None):
        """
        Initialize TradingView adapter.

        Args:
            webhook_base_url: Base URL for webhook endpoints
                              e.g., "https://your-domain.com/api/v1/signals/webhook"
        """
        super().__init__()
        self._webhook_base_url = webhook_base_url or "http://localhost:8000/api/v1/signals/webhook"
        # TradingView doesn't require authentication for webhook reception
        self._status = ConnectionStatus.CONNECTED

    @property
    def platform_name(self) -> str:
        return "TradingView"

    @property
    def platform_display_name(self) -> str:
        return "TradingView Charts"

    @property
    def supports_watchlist_import(self) -> bool:
        # TradingView has no public API for watchlist access
        return False

    @property
    def supports_real_time_signals(self) -> bool:
        # TradingView sends signals via webhooks
        return True

    @property
    def requires_authentication(self) -> bool:
        # No authentication needed for receiving webhooks
        return False

    async def connect(self, credentials: PlatformCredentials) -> bool:
        """
        TradingView doesn't require connection.

        Webhook reception is always available.
        """
        self._status = ConnectionStatus.CONNECTED
        logger.info("TradingView adapter connected (webhook mode)")
        return True

    async def disconnect(self) -> None:
        """Disconnect is a no-op for TradingView."""
        self._status = ConnectionStatus.DISCONNECTED
        logger.info("TradingView adapter disconnected")

    async def health_check(self) -> bool:
        """
        Health check always returns True for TradingView.

        Webhook reception doesn't require external connectivity.
        """
        return True

    async def get_watchlists(self) -> list[WatchlistInfo]:
        """
        Not supported for TradingView.

        Raises:
            NotImplementedError: TradingView has no public API for watchlists
        """
        raise NotImplementedError(
            "TradingView does not have a public API for watchlist access. "
            "Please manually configure instruments and charts."
        )

    async def get_instruments(self, watchlist_id: str) -> list[PlatformInstrument]:
        """
        Not supported for TradingView.

        Raises:
            NotImplementedError: TradingView has no public API for instruments
        """
        raise NotImplementedError(
            "TradingView does not have a public API for instrument access. "
            "Please manually configure instruments and charts."
        )

    def get_webhook_url_template(self) -> str:
        """
        Get the webhook URL for TradingView alerts.

        Returns:
            Webhook URL with {webhook_id} placeholder
        """
        return f"{self._webhook_base_url}/{{webhook_id}}"

    def get_webhook_url(self, webhook_id: str) -> str:
        """
        Get the complete webhook URL for a specific chart.

        Args:
            webhook_id: The chart's webhook identifier

        Returns:
            Complete webhook URL
        """
        return f"{self._webhook_base_url}/{webhook_id}"

    def get_alert_message_template(self) -> str:
        """
        Get the TradingView alert message template.

        This template should be used in TradingView alert configuration.
        Users can customize the indicator fields based on their chart.

        Returns:
            JSON template for alert messages with common indicators
        """
        return """{
  "webhook_id": "{{webhook_id}}",
  "direction": "{{strategy.order.action}}",
  "signal_type": "STATE_CHANGE",
  "timestamp": "{{timenow}}",
  "price": {{close}},
  "rsi": {{rsi_value}},
  "macd": {{macd_value}},
  "macd_signal": {{macd_signal}},
  "ema_9": {{ema9}},
  "ema_21": {{ema21}},
  "volume": {{volume}}
}"""

    def get_alert_message_template_simple(self) -> str:
        """
        Get a simplified alert message template.

        For users who want a minimal configuration.

        Returns:
            Simplified JSON template
        """
        return """{
  "webhook_id": "YOUR_CHART_WEBHOOK_ID",
  "direction": "BULLISH",
  "rsi": 28.5,
  "macd": 0.12
}"""

    def get_setup_instructions(self) -> str:
        """
        Get setup instructions for TradingView integration.

        Returns:
            Markdown-formatted setup instructions
        """
        return f"""
## TradingView Webhook Setup

### Step 1: Create Your Chart and Indicators
1. Open TradingView and create a new chart
2. Add your preferred indicators (RSI, MACD, EMA, etc.)
3. Configure indicator settings as needed

### Step 2: Create an Alert
1. Click the "Alerts" icon (alarm clock) in TradingView
2. Set your alert conditions
3. In "Webhook URL", enter:
   ```
   {self._webhook_base_url}/YOUR_WEBHOOK_ID
   ```
4. Replace `YOUR_WEBHOOK_ID` with your chart's webhook ID from CIA-SIE

### Step 3: Configure Alert Message
In the "Message" field, paste this JSON template:

```json
{self.get_alert_message_template()}
```

Customize the indicator fields to match your chart's Pine Script variables.

### Step 4: Indicator Values
To include indicator values in alerts, you need to:
1. Use Pine Script to compute indicators
2. Store values in plot variables
3. Reference them in the alert message using {{{{variable_name}}}}

### Example Pine Script
```pinescript
//@version=5
indicator("CIA-SIE Alert Setup")
rsi_value = ta.rsi(close, 14)
[macd_line, signal_line, _] = ta.macd(close, 12, 26, 9)

plot(rsi_value, title="RSI")
plot(macd_line, title="MACD")
```

### Webhook ID Format
Recommended format: `SYMBOL_SILOCODE_CHARTCODE`
Example: `SAMPLE_01A_RSI14`

This makes it easy to identify which chart sent each signal.
"""

    def to_dict(self) -> dict:
        """Convert adapter info to dictionary with TradingView-specific details."""
        base = super().to_dict()
        base.update(
            {
                "webhook_url_template": self.get_webhook_url_template(),
                "alert_message_template": self.get_alert_message_template_simple(),
                "integration_type": "webhook",
                "manual_setup_required": True,
            }
        )
        return base


# Register adapter on module load
def register():
    """Register TradingView adapter with the global registry."""
    from cia_sie.platforms.registry import register_adapter

    register_adapter(TradingViewAdapter)
