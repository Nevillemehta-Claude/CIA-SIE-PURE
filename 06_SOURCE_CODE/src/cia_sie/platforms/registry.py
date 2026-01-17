"""
CIA-SIE Platform Registry
=========================

Registry for managing platform adapters.

GOVERNED BY: Section 8.1 (Integration Architecture)

This module provides:
- Registration of platform adapters
- Retrieval of adapters by name
- Listing all available platforms
"""

import logging
from typing import Optional

from cia_sie.platforms.base import PlatformAdapter

logger = logging.getLogger(__name__)


class PlatformRegistry:
    """
    Registry for platform adapters.

    Per Gold Standard Specification Section 8.1.

    Maintains a registry of available platform adapters and
    provides methods to retrieve them by name.

    Usage:
        registry = PlatformRegistry()
        registry.register(TradingViewAdapter)
        registry.register(KiteAdapter)

        adapter = registry.get("TradingView")
        adapters = registry.list_all()
    """

    _instance: Optional["PlatformRegistry"] = None

    def __new__(cls) -> "PlatformRegistry":
        """Singleton pattern for global registry access."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._adapters: dict[str, type[PlatformAdapter]] = {}
            cls._instance._instances: dict[str, PlatformAdapter] = {}
        return cls._instance

    def register(self, adapter_class: type[PlatformAdapter]) -> None:
        """
        Register a platform adapter class.

        Args:
            adapter_class: PlatformAdapter subclass to register

        Raises:
            TypeError: If adapter_class is not a PlatformAdapter subclass
        """
        if not issubclass(adapter_class, PlatformAdapter):
            raise TypeError(f"{adapter_class.__name__} must be a subclass of PlatformAdapter")

        # Create temporary instance to get platform_name
        temp_instance = adapter_class()
        name = temp_instance.platform_name

        if name in self._adapters:
            logger.warning(f"Replacing existing adapter for platform: {name}")

        self._adapters[name] = adapter_class
        logger.info(f"Registered platform adapter: {name}")

    def get(self, platform_name: str) -> Optional[PlatformAdapter]:
        """
        Get a platform adapter instance by name.

        Args:
            platform_name: Name of the platform (e.g., "TradingView", "Kite")

        Returns:
            PlatformAdapter instance, or None if not found
        """
        if platform_name not in self._adapters:
            # INLINE sanitization for CodeQL - remove newlines to prevent log injection
            safe_name = str(platform_name).replace("\n", "").replace("\r", "")[:100]
            logger.warning(f"Platform adapter not found: {safe_name}")
            return None

        # Return cached instance or create new one
        if platform_name not in self._instances:
            self._instances[platform_name] = self._adapters[platform_name]()

        return self._instances[platform_name]

    def get_class(self, platform_name: str) -> Optional[type[PlatformAdapter]]:
        """
        Get a platform adapter class by name.

        Args:
            platform_name: Name of the platform

        Returns:
            PlatformAdapter class, or None if not found
        """
        return self._adapters.get(platform_name)

    def list_all(self) -> list[dict]:
        """
        List all registered platform adapters.

        Returns:
            List of adapter info dictionaries
        """
        result = []
        for name in self._adapters:
            adapter = self.get(name)
            if adapter:
                result.append(adapter.to_dict())
        return result

    def list_names(self) -> list[str]:
        """
        List names of all registered platforms.

        Returns:
            List of platform names
        """
        return list(self._adapters.keys())

    def is_registered(self, platform_name: str) -> bool:
        """
        Check if a platform is registered.

        Args:
            platform_name: Name of the platform

        Returns:
            True if platform is registered
        """
        return platform_name in self._adapters

    def clear(self) -> None:
        """Clear all registered adapters. Primarily for testing."""
        self._adapters.clear()
        self._instances.clear()
        logger.info("Platform registry cleared")


# Global registry instance
_registry = PlatformRegistry()


def get_registry() -> PlatformRegistry:
    """Get the global platform registry instance."""
    return _registry


def register_adapter(adapter_class: type[PlatformAdapter]) -> None:
    """Convenience function to register an adapter to the global registry."""
    _registry.register(adapter_class)


def get_adapter(platform_name: str) -> Optional[PlatformAdapter]:
    """Convenience function to get an adapter from the global registry."""
    return _registry.get(platform_name)
