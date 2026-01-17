"""
Tests for Mercury Graceful Shutdown
====================================

Tests for the shutdown module that handles graceful application termination.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mercury.core.shutdown import (
    GracefulShutdown,
    get_shutdown_handler,
    save_state_on_shutdown,
)


class TestGracefulShutdown:
    """Tests for GracefulShutdown handler."""
    
    @pytest.fixture
    def shutdown_handler(self):
        """Create a fresh shutdown handler."""
        return GracefulShutdown(timeout_seconds=5.0)
    
    def test_initial_state(self, shutdown_handler):
        """Test initial state of shutdown handler."""
        assert not shutdown_handler.is_shutting_down
        assert len(shutdown_handler._shutdown_handlers) == 0
    
    def test_register_handler(self, shutdown_handler):
        """Test registering shutdown handlers."""
        async def handler1():
            pass
        
        async def handler2():
            pass
        
        shutdown_handler.register_handler(handler1)
        shutdown_handler.register_handler(handler2)
        
        assert len(shutdown_handler._shutdown_handlers) == 2
    
    @pytest.mark.asyncio
    async def test_shutdown_calls_handlers(self, shutdown_handler):
        """Test that shutdown calls all registered handlers."""
        called = []
        
        async def handler1():
            called.append("handler1")
        
        async def handler2():
            called.append("handler2")
        
        shutdown_handler.register_handler(handler1)
        shutdown_handler.register_handler(handler2)
        
        with patch("mercury.core.shutdown.shutdown_state_store", new=AsyncMock()):
            await shutdown_handler.shutdown()
        
        assert "handler1" in called
        assert "handler2" in called
        assert shutdown_handler.is_shutting_down
    
    @pytest.mark.asyncio
    async def test_shutdown_only_once(self, shutdown_handler):
        """Test that shutdown only executes once."""
        call_count = 0
        
        async def handler():
            nonlocal call_count
            call_count += 1
        
        shutdown_handler.register_handler(handler)
        
        with patch("mercury.core.shutdown.shutdown_state_store", new=AsyncMock()):
            await shutdown_handler.shutdown()
            await shutdown_handler.shutdown()  # Second call should be ignored
        
        assert call_count == 1
    
    @pytest.mark.asyncio
    async def test_shutdown_handles_handler_errors(self, shutdown_handler):
        """Test that shutdown continues even if a handler fails."""
        called = []
        
        async def failing_handler():
            raise Exception("Handler failed!")
        
        async def working_handler():
            called.append("working")
        
        shutdown_handler.register_handler(failing_handler)
        shutdown_handler.register_handler(working_handler)
        
        with patch("mercury.core.shutdown.shutdown_state_store", new=AsyncMock()):
            # Should not raise
            await shutdown_handler.shutdown()
        
        # Working handler should still be called
        assert "working" in called
    
    @pytest.mark.asyncio
    async def test_wait_for_shutdown(self, shutdown_handler):
        """Test waiting for shutdown signal."""
        async def trigger_shutdown():
            await asyncio.sleep(0.1)
            with patch("mercury.core.shutdown.shutdown_state_store", new=AsyncMock()):
                await shutdown_handler.shutdown()
        
        # Start shutdown trigger
        asyncio.create_task(trigger_shutdown())
        
        # Wait for shutdown (should complete when shutdown is triggered)
        await asyncio.wait_for(
            shutdown_handler.wait_for_shutdown(),
            timeout=1.0
        )
        
        assert shutdown_handler.is_shutting_down


class TestSaveStateOnShutdown:
    """Tests for the default save_state_on_shutdown handler."""
    
    @pytest.mark.asyncio
    async def test_saves_shutdown_timestamp(self):
        """Test that shutdown saves timestamp."""
        with patch("mercury.core.shutdown.get_state_store") as mock_get_store:
            mock_store = MagicMock()
            mock_store.set_setting = AsyncMock()
            mock_get_store.return_value = mock_store
            
            await save_state_on_shutdown()
            
            mock_store.set_setting.assert_called_once()
            call_args = mock_store.set_setting.call_args
            assert call_args[0][0] == "last_shutdown"
            assert "timestamp" in call_args[0][1]
            assert call_args[0][1]["graceful"] is True


class TestGetShutdownHandler:
    """Tests for global shutdown handler access."""
    
    def test_returns_singleton(self):
        """Test that get_shutdown_handler returns same instance."""
        # Reset global state
        import mercury.core.shutdown as shutdown_module
        shutdown_module._shutdown_handler = None
        
        handler1 = get_shutdown_handler()
        handler2 = get_shutdown_handler()
        
        assert handler1 is handler2
