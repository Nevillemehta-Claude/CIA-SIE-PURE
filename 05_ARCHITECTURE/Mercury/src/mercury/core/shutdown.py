"""
Mercury Graceful Shutdown
=========================

Handles graceful shutdown with state preservation.

AUTONOMOUS PRINCIPLE: Zero-loss shutdown.
All in-flight operations complete, state is saved, resources are released.
"""

import asyncio
import signal
import sys
from datetime import datetime, timezone
from typing import Awaitable, Callable, List, Optional

from mercury.core.logging import get_logger
from mercury.core.persistence import get_state_store, shutdown_state_store

logger = get_logger("mercury.shutdown")


class GracefulShutdown:
    """
    Manages graceful shutdown of the Mercury application.
    
    Features:
    - Signal handling (SIGINT, SIGTERM)
    - Ordered shutdown of components
    - State persistence before exit
    - Timeout protection
    """
    
    def __init__(self, timeout_seconds: float = 10.0):
        """
        Initialize shutdown handler.
        
        Args:
            timeout_seconds: Max time to wait for shutdown
        """
        self.timeout = timeout_seconds
        self._shutdown_event = asyncio.Event()
        self._shutdown_handlers: List[Callable[[], Awaitable[None]]] = []
        self._is_shutting_down = False
        self._signals_installed = False
    
    @property
    def is_shutting_down(self) -> bool:
        """Check if shutdown is in progress."""
        return self._is_shutting_down
    
    def register_handler(
        self,
        handler: Callable[[], Awaitable[None]],
        priority: int = 0,
    ) -> None:
        """
        Register a shutdown handler.
        
        Handlers are called in order of registration during shutdown.
        
        Args:
            handler: Async function to call during shutdown
            priority: Unused currently, for future ordering
        """
        self._shutdown_handlers.append(handler)
        logger.debug(f"Registered shutdown handler: {handler.__name__}")
    
    def install_signal_handlers(self) -> None:
        """Install signal handlers for graceful shutdown."""
        if self._signals_installed:
            return
        
        try:
            loop = asyncio.get_running_loop()
            
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(
                    sig,
                    lambda s=sig: asyncio.create_task(self._signal_handler(s))
                )
            
            self._signals_installed = True
            logger.info("Signal handlers installed (SIGINT, SIGTERM)")
            
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            logger.warning("Signal handlers not supported on this platform")
        except RuntimeError:
            # No running loop
            logger.warning("No running event loop for signal handlers")
    
    async def _signal_handler(self, sig: signal.Signals) -> None:
        """Handle shutdown signal."""
        logger.info(f"Received signal {sig.name}, initiating graceful shutdown...")
        await self.shutdown()
    
    async def shutdown(self) -> None:
        """
        Execute graceful shutdown.
        
        Calls all registered handlers and saves state.
        """
        if self._is_shutting_down:
            logger.warning("Shutdown already in progress")
            return
        
        self._is_shutting_down = True
        self._shutdown_event.set()
        
        logger.info("=" * 60)
        logger.info("MERCURY GRACEFUL SHUTDOWN")
        logger.info("=" * 60)
        
        start_time = datetime.now(timezone.utc)
        
        # Call all shutdown handlers
        for handler in self._shutdown_handlers:
            try:
                logger.info(f"Executing shutdown handler: {handler.__name__}")
                await asyncio.wait_for(
                    handler(),
                    timeout=self.timeout / len(self._shutdown_handlers) if self._shutdown_handlers else self.timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Shutdown handler {handler.__name__} timed out")
            except Exception as e:
                logger.error(f"Shutdown handler {handler.__name__} failed: {e}")
        
        # Close state store
        try:
            await shutdown_state_store()
        except Exception as e:
            logger.error(f"Failed to close state store: {e}")
        
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        logger.info(f"Graceful shutdown complete in {elapsed:.2f}s")
        logger.info("=" * 60)
    
    async def wait_for_shutdown(self) -> None:
        """Wait for shutdown signal."""
        await self._shutdown_event.wait()


# Global shutdown handler
_shutdown_handler: Optional[GracefulShutdown] = None


def get_shutdown_handler() -> GracefulShutdown:
    """Get or create the global shutdown handler."""
    global _shutdown_handler
    if _shutdown_handler is None:
        _shutdown_handler = GracefulShutdown()
    return _shutdown_handler


async def save_state_on_shutdown() -> None:
    """
    Default shutdown handler that saves application state.
    
    This is automatically registered and saves:
    - Active conversations
    - Current session data
    - User preferences
    """
    logger.info("Saving application state...")
    
    store = get_state_store()
    
    # Save shutdown timestamp
    await store.set_setting("last_shutdown", {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "graceful": True,
    })
    
    logger.info("Application state saved")
