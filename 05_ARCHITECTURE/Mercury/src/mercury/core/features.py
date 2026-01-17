"""
Mercury Feature Flags
=====================

Runtime feature toggles for safe deployments.

MISSION-CRITICAL STANDARD: Deployment Safety
- Toggle features without code changes
- Gradual rollouts
- Emergency kill switches
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from mercury.core.logging import get_logger

logger = get_logger("mercury.features")


class FeatureState(Enum):
    """State of a feature flag."""
    ENABLED = "enabled"
    DISABLED = "disabled"
    ROLLOUT = "rollout"  # Partial rollout


@dataclass
class Feature:
    """Definition of a feature flag."""
    name: str
    description: str
    state: FeatureState = FeatureState.DISABLED
    rollout_percentage: int = 0  # 0-100, used when state is ROLLOUT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    owner: str = "system"
    
    def is_enabled(self, context: Optional[dict] = None) -> bool:
        """
        Check if feature is enabled.
        
        Args:
            context: Optional context for rollout decisions
            
        Returns:
            True if feature should be enabled
        """
        if self.state == FeatureState.ENABLED:
            return True
        if self.state == FeatureState.DISABLED:
            return False
        if self.state == FeatureState.ROLLOUT:
            # Simple hash-based rollout
            if context and "user_id" in context:
                hash_val = hash(context["user_id"]) % 100
                return hash_val < self.rollout_percentage
            return False
        return False


class FeatureManager:
    """
    Manages feature flags for Mercury.
    
    Usage:
        features = FeatureManager()
        
        if features.is_enabled("new_ai_model"):
            use_new_model()
        else:
            use_old_model()
    """
    
    def __init__(self):
        self._features: dict[str, Feature] = {}
        self._load_defaults()
    
    def _load_defaults(self) -> None:
        """Load default feature flags."""
        defaults = [
            # AI Features
            Feature(
                name="ai_recommendations",
                description="Allow AI to make trade recommendations",
                state=FeatureState.ENABLED,
                owner="ai_team",
            ),
            Feature(
                name="ai_confidence_scores",
                description="Include confidence scores in AI responses",
                state=FeatureState.ENABLED,
                owner="ai_team",
            ),
            Feature(
                name="ai_streaming",
                description="Stream AI responses (when supported)",
                state=FeatureState.DISABLED,
                owner="ai_team",
            ),
            
            # Kite Features
            Feature(
                name="kite_live_quotes",
                description="Fetch live quotes from Kite API",
                state=FeatureState.ENABLED,
                owner="data_team",
            ),
            Feature(
                name="kite_historical",
                description="Fetch historical data from Kite API",
                state=FeatureState.ENABLED,
                owner="data_team",
            ),
            Feature(
                name="kite_websocket",
                description="Use WebSocket for real-time data",
                state=FeatureState.DISABLED,
                owner="data_team",
            ),
            
            # Resilience Features
            Feature(
                name="circuit_breaker_kite",
                description="Enable circuit breaker for Kite API",
                state=FeatureState.ENABLED,
                owner="platform_team",
            ),
            Feature(
                name="circuit_breaker_ai",
                description="Enable circuit breaker for AI API",
                state=FeatureState.ENABLED,
                owner="platform_team",
            ),
            Feature(
                name="graceful_degradation",
                description="Enable graceful degradation on failures",
                state=FeatureState.ENABLED,
                owner="platform_team",
            ),
            
            # Logging Features
            Feature(
                name="structured_logging",
                description="Use JSON structured logging",
                state=FeatureState.DISABLED,  # Human-readable by default
                owner="platform_team",
            ),
            Feature(
                name="verbose_logging",
                description="Enable verbose debug logging",
                state=FeatureState.DISABLED,
                owner="platform_team",
            ),
            
            # Experimental Features
            Feature(
                name="multi_instrument_analysis",
                description="Analyze multiple instruments in one query",
                state=FeatureState.DISABLED,
                owner="product_team",
            ),
            Feature(
                name="portfolio_optimization",
                description="AI-powered portfolio optimization",
                state=FeatureState.DISABLED,
                owner="product_team",
            ),
        ]
        
        for feature in defaults:
            self._features[feature.name] = feature
    
    def is_enabled(self, name: str, context: Optional[dict] = None) -> bool:
        """
        Check if a feature is enabled.
        
        Args:
            name: Feature name
            context: Optional context for rollout decisions
            
        Returns:
            True if feature is enabled
        """
        feature = self._features.get(name)
        if feature is None:
            logger.warning(f"Unknown feature flag: {name}")
            return False
        return feature.is_enabled(context)
    
    def get_feature(self, name: str) -> Optional[Feature]:
        """Get a feature by name."""
        return self._features.get(name)
    
    def set_state(self, name: str, state: FeatureState) -> bool:
        """
        Set feature state.
        
        Args:
            name: Feature name
            state: New state
            
        Returns:
            True if feature was updated
        """
        feature = self._features.get(name)
        if feature is None:
            logger.warning(f"Cannot set state for unknown feature: {name}")
            return False
        
        old_state = feature.state
        feature.state = state
        feature.updated_at = datetime.now(timezone.utc)
        
        logger.info(
            f"Feature '{name}' state changed",
            context={
                "old_state": old_state.value,
                "new_state": state.value,
            }
        )
        return True
    
    def enable(self, name: str) -> bool:
        """Enable a feature."""
        return self.set_state(name, FeatureState.ENABLED)
    
    def disable(self, name: str) -> bool:
        """Disable a feature."""
        return self.set_state(name, FeatureState.DISABLED)
    
    def set_rollout(self, name: str, percentage: int) -> bool:
        """
        Set feature to rollout with percentage.
        
        Args:
            name: Feature name
            percentage: Rollout percentage (0-100)
            
        Returns:
            True if feature was updated
        """
        feature = self._features.get(name)
        if feature is None:
            return False
        
        feature.state = FeatureState.ROLLOUT
        feature.rollout_percentage = max(0, min(100, percentage))
        feature.updated_at = datetime.now(timezone.utc)
        
        logger.info(
            f"Feature '{name}' set to rollout",
            context={"percentage": feature.rollout_percentage}
        )
        return True
    
    def list_features(self) -> list[dict]:
        """List all features and their states."""
        return [
            {
                "name": f.name,
                "description": f.description,
                "state": f.state.value,
                "rollout_percentage": f.rollout_percentage if f.state == FeatureState.ROLLOUT else None,
                "owner": f.owner,
            }
            for f in self._features.values()
        ]
    
    def register(
        self,
        name: str,
        description: str,
        state: FeatureState = FeatureState.DISABLED,
        owner: str = "system",
    ) -> Feature:
        """
        Register a new feature flag.
        
        Args:
            name: Unique feature name
            description: Human-readable description
            state: Initial state
            owner: Team/person responsible
            
        Returns:
            Created feature
        """
        feature = Feature(
            name=name,
            description=description,
            state=state,
            owner=owner,
        )
        self._features[name] = feature
        logger.info(f"Registered feature: {name}", context={"state": state.value})
        return feature


# Global feature manager instance
_feature_manager: Optional[FeatureManager] = None


def get_features() -> FeatureManager:
    """Get the global feature manager."""
    global _feature_manager
    if _feature_manager is None:
        _feature_manager = FeatureManager()
    return _feature_manager


def is_enabled(name: str, context: Optional[dict] = None) -> bool:
    """Convenience function to check if a feature is enabled."""
    return get_features().is_enabled(name, context)
