"""
Mercury Main Entry Point
========================

Launch Mercury - the LLM as Financial Market Cognitive Interface.

DIRECTIVE: Full operational readiness with API authentication on launch.
STANDARD: Zero-Defect execution.

Usage:
    # Terminal mode (REPL)
    python -m mercury.main
    
    # Web mode (FastAPI + Browser UI)
    python -m mercury.main --web
    
    # Check system status only
    python -m mercury.main --check
"""

import argparse
import asyncio
import sys
import uvicorn

from mercury.core.logging import setup_logging, get_logger
from mercury.core.startup import (
    initialize_system,
    perform_launch_readiness_check,
    print_launch_status,
    LaunchReadiness,
    ServiceStatus,
)

logger = get_logger("mercury.main")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Mercury - LLM as Financial Market Cognitive Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m mercury.main          # Start terminal REPL
  python -m mercury.main --web    # Start web interface
  python -m mercury.main --check  # Check system status
  python -m mercury.main --port 8080 --web  # Web on custom port
        """
    )
    
    parser.add_argument(
        "--web",
        action="store_true",
        help="Start web interface (default: terminal REPL)"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check system status and exit"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8888,
        help="Port for web interface (default: 8888)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for web interface (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't open browser automatically"
    )
    
    return parser.parse_args()


async def run_check() -> int:
    """
    Run system check and exit.
    
    Returns:
        Exit code (0 if ready, 1 if not)
    """
    print("\n" + "=" * 70)
    print("  MERCURY SYSTEM CHECK")
    print("=" * 70)
    
    readiness = await perform_launch_readiness_check()
    print_launch_status(readiness)
    
    return 0 if readiness.ready else 1


async def run_web(host: str, port: int, open_browser: bool) -> None:
    """
    Run Mercury web interface.
    
    DIRECTIVE: UI/UX execution to the highest design standards.
    """
    # Perform initialization
    readiness = await initialize_system()
    
    if not readiness.ready:
        print("\n⚠️  System starting in degraded mode.")
        print("    Some features may be limited.\n")
    
    # Open browser
    if open_browser:
        import webbrowser
        webbrowser.open(f"http://{host}:{port}")
    
    print(f"\n🌐 Mercury Web Interface: http://{host}:{port}")
    print("   Press Ctrl+C to stop\n")
    
    # Run uvicorn
    config = uvicorn.Config(
        "mercury.api.app:app",
        host=host,
        port=port,
        log_level="info",
        reload=False,
    )
    server = uvicorn.Server(config)
    await server.serve()


def run_repl() -> None:
    """
    Run Mercury terminal REPL.
    """
    from mercury.interface.repl import run_mercury
    run_mercury()


def main() -> int:
    """
    Main entry point with startup validation.
    
    Returns:
        Exit code
    """
    args = parse_args()
    
    # Setup logging
    setup_logging(level="INFO", json_format=False)
    
    try:
        if args.check:
            # Check mode
            return asyncio.run(run_check())
        
        elif args.web:
            # Web mode
            asyncio.run(run_web(
                host=args.host,
                port=args.port,
                open_browser=not args.no_browser,
            ))
            return 0
        
        else:
            # Terminal REPL mode
            run_repl()
            return 0
    
    except KeyboardInterrupt:
        print("\n\nShutdown requested. Goodbye!")
        return 0
    
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
