"""
CIA-SIE Application Entry Point
===============================

Main entry point for running the CIA-SIE application.
"""

import logging
import sys

import uvicorn

from cia_sie.core.config import get_settings


def setup_logging() -> None:
    """Configure application logging."""
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Add file handler if configured
    if settings.log_file:
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(file_handler)


def main() -> None:
    """
    Main entry point.

    Starts the FastAPI application with uvicorn.
    """
    setup_logging()
    settings = get_settings()

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")

    uvicorn.run(
        "cia_sie.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
