"""
Tests for CIA-SIE Platform Registry
===================================

Unit tests for platform adapter registry.

GOVERNED BY: Section 8.1 (Integration Architecture)
"""

import pytest
from unittest.mock import Mock, patch

from cia_sie.platforms.base import PlatformAdapter, ConnectionStatus
from cia_sie.platforms.registry import (
    PlatformRegistry,
    get_registry,
    register_adapter,
    get_adapter,
)


class MockAdapter(PlatformAdapter):
    """Mock adapter for testing."""

    @property
    def platform_name(self) -> str:
        return "MockPlatform"

    @property
    def platform_display_name(self) -> str:
        return "Mock Platform"

    @property
    def supports_watchlist_import(self) -> bool:
        return True

    @property
    def supports_real_time_signals(self) -> bool:
        return True

    @property
    def requires_authentication(self) -> bool:
        return False

    async def connect(self, credentials) -> bool:
        return True

    async def disconnect(self) -> None:
        pass

    async def health_check(self) -> bool:
        return True

    async def get_watchlists(self):
        return []

    async def get_instruments(self, watchlist_id: str):
        return []


class AnotherMockAdapter(PlatformAdapter):
    """Another mock adapter for testing."""

    @property
    def platform_name(self) -> str:
        return "AnotherMock"

    @property
    def platform_display_name(self) -> str:
        return "Another Mock"

    @property
    def supports_watchlist_import(self) -> bool:
        return False

    @property
    def supports_real_time_signals(self) -> bool:
        return False

    @property
    def requires_authentication(self) -> bool:
        return True

    async def connect(self, credentials) -> bool:
        return True

    async def disconnect(self) -> None:
        pass

    async def health_check(self) -> bool:
        return True

    async def get_watchlists(self):
        raise NotImplementedError()

    async def get_instruments(self, watchlist_id: str):
        raise NotImplementedError()


class TestPlatformRegistry:
    """Tests for PlatformRegistry class."""

    @pytest.fixture
    def fresh_registry(self):
        """Create a fresh registry (bypassing singleton)."""
        # Reset singleton for clean tests
        PlatformRegistry._instance = None
        registry = PlatformRegistry()
        registry.clear()
        return registry

    def test_singleton_pattern(self, fresh_registry):
        """Test registry uses singleton pattern."""
        registry1 = PlatformRegistry()
        registry2 = PlatformRegistry()
        assert registry1 is registry2

    def test_register_adapter(self, fresh_registry):
        """Test registering an adapter."""
        fresh_registry.register(MockAdapter)
        assert fresh_registry.is_registered("MockPlatform")

    def test_register_invalid_adapter(self, fresh_registry):
        """Test registering non-adapter class raises TypeError."""

        class NotAnAdapter:
            pass

        with pytest.raises(TypeError, match="must be a subclass of PlatformAdapter"):
            fresh_registry.register(NotAnAdapter)

    def test_register_duplicate_warns(self, fresh_registry):
        """Test registering duplicate adapter logs warning."""
        fresh_registry.register(MockAdapter)

        with patch('cia_sie.platforms.registry.logger') as mock_logger:
            fresh_registry.register(MockAdapter)
            mock_logger.warning.assert_called_once()
            assert "Replacing" in mock_logger.warning.call_args[0][0]

    def test_get_adapter(self, fresh_registry):
        """Test getting registered adapter."""
        fresh_registry.register(MockAdapter)
        adapter = fresh_registry.get("MockPlatform")

        assert adapter is not None
        assert adapter.platform_name == "MockPlatform"

    def test_get_unregistered_adapter(self, fresh_registry):
        """Test getting unregistered adapter returns None."""
        result = fresh_registry.get("NonExistent")
        assert result is None

    def test_get_returns_cached_instance(self, fresh_registry):
        """Test get returns same cached instance."""
        fresh_registry.register(MockAdapter)

        adapter1 = fresh_registry.get("MockPlatform")
        adapter2 = fresh_registry.get("MockPlatform")

        assert adapter1 is adapter2

    def test_get_class(self, fresh_registry):
        """Test getting adapter class."""
        fresh_registry.register(MockAdapter)
        adapter_class = fresh_registry.get_class("MockPlatform")

        assert adapter_class is MockAdapter

    def test_get_class_unregistered(self, fresh_registry):
        """Test getting unregistered adapter class returns None."""
        result = fresh_registry.get_class("NonExistent")
        assert result is None

    def test_list_all(self, fresh_registry):
        """Test listing all registered adapters."""
        fresh_registry.register(MockAdapter)
        fresh_registry.register(AnotherMockAdapter)

        all_adapters = fresh_registry.list_all()

        assert len(all_adapters) == 2
        names = [a["platform_name"] for a in all_adapters]
        assert "MockPlatform" in names
        assert "AnotherMock" in names

    def test_list_names(self, fresh_registry):
        """Test listing all registered platform names."""
        fresh_registry.register(MockAdapter)
        fresh_registry.register(AnotherMockAdapter)

        names = fresh_registry.list_names()

        assert len(names) == 2
        assert "MockPlatform" in names
        assert "AnotherMock" in names

    def test_is_registered(self, fresh_registry):
        """Test is_registered returns correct value."""
        fresh_registry.register(MockAdapter)

        assert fresh_registry.is_registered("MockPlatform") is True
        assert fresh_registry.is_registered("NonExistent") is False

    def test_clear(self, fresh_registry):
        """Test clear removes all adapters."""
        fresh_registry.register(MockAdapter)
        fresh_registry.register(AnotherMockAdapter)

        fresh_registry.clear()

        assert len(fresh_registry.list_names()) == 0
        assert fresh_registry.get("MockPlatform") is None


class TestRegistryConvenienceFunctions:
    """Tests for module-level convenience functions."""

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Reset registry before each test."""
        registry = get_registry()
        registry.clear()
        yield
        registry.clear()

    def test_get_registry(self):
        """Test get_registry returns global instance."""
        registry = get_registry()
        assert isinstance(registry, PlatformRegistry)

    def test_register_adapter_function(self):
        """Test register_adapter convenience function."""
        register_adapter(MockAdapter)

        registry = get_registry()
        assert registry.is_registered("MockPlatform")

    def test_get_adapter_function(self):
        """Test get_adapter convenience function."""
        register_adapter(MockAdapter)

        adapter = get_adapter("MockPlatform")
        assert adapter is not None
        assert adapter.platform_name == "MockPlatform"

    def test_get_adapter_unregistered(self):
        """Test get_adapter returns None for unregistered."""
        result = get_adapter("NonExistent")
        assert result is None


class TestRegistryLogInjectionPrevention:
    """Tests for log injection prevention."""

    @pytest.fixture
    def fresh_registry(self):
        """Create fresh registry."""
        PlatformRegistry._instance = None
        registry = PlatformRegistry()
        registry.clear()
        return registry

    def test_get_sanitizes_platform_name(self, fresh_registry):
        """Test that get method sanitizes platform name for logging."""
        # Try to inject newlines into log
        malicious_name = "Evil\nPlatform\rName"

        with patch('cia_sie.platforms.registry.logger') as mock_logger:
            fresh_registry.get(malicious_name)

            # Verify the warning was called
            mock_logger.warning.assert_called_once()
            logged_message = mock_logger.warning.call_args[0][0]

            # Verify newlines were stripped
            assert "\n" not in logged_message
            assert "\r" not in logged_message


class TestRegistryConstitutionalCompliance:
    """Constitutional compliance tests for platform registry."""

    @pytest.mark.constitutional
    def test_no_scoring_in_registry(self):
        """CRITICAL: Registry must not have scoring methods."""
        prohibited_methods = [
            'score_platform', 'rank_platforms', 'recommend_platform',
            'get_best_platform', 'prioritize',
        ]

        for method in prohibited_methods:
            assert not hasattr(PlatformRegistry, method), \
                f"CONSTITUTIONAL VIOLATION: Registry has {method}"

    @pytest.mark.constitutional
    def test_list_all_no_ranking(self):
        """CRITICAL: list_all must not rank or prioritize adapters."""
        # Reset and register
        PlatformRegistry._instance = None
        registry = PlatformRegistry()
        registry.clear()

        registry.register(MockAdapter)
        registry.register(AnotherMockAdapter)

        all_adapters = registry.list_all()

        # Verify no ranking fields
        for adapter_info in all_adapters:
            assert "rank" not in adapter_info
            assert "priority" not in adapter_info
            assert "score" not in adapter_info
            assert "recommended" not in adapter_info
