"""
CIA-SIE FastAPI Application
===========================

Main FastAPI application factory.

GOVERNED BY: Section 11 (Backend Standards)

SECURITY FEATURES:
- CORS restriction (environment-based)
- Security headers (OWASP recommended)
- Rate limiting (per-endpoint)
- Security event logging
"""

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cia_sie.api.routes import api_router
from cia_sie.core.config import get_settings
from cia_sie.core.security import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)
from cia_sie.dal.database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting CIA-SIE application...")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Log security configuration
    settings = get_settings()
    if settings.webhook_secret:
        logger.info("Webhook authentication: ENABLED")
    else:
        logger.warning("Webhook authentication: DISABLED (set WEBHOOK_SECRET for production)")

    yield

    # Shutdown
    logger.info("Shutting down CIA-SIE application...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance
    """
    settings = get_settings()

    # Determine environment
    environment = os.getenv("ENVIRONMENT", "development").lower()
    is_production = environment == "production"

    app = FastAPI(
        title="CIA-SIE API",
        description="""
        Chart Intelligence Auditor & Signal Intelligence Engine

        A decision-support platform for trading signal analysis.

        ## Key Principles

        - **Decision-support**, NOT decision-making
        - **Expose contradictions**, NEVER resolve them
        - **Descriptive AI**, NOT prescriptive AI
        - **No aggregation**, scoring, weighting, or recommendations
        - **User retains ALL** judgment and decision authority

        ## Security

        - Webhook endpoints require HMAC-SHA256 signature validation
        - Rate limiting applied to all endpoints
        - Security headers included in all responses

        ## API Design

        This API provides access to:
        - Instrument and Silo management
        - Chart registration and signal ingestion
        - Relationship exposure (contradictions, confirmations)
        - AI-powered descriptive narratives

        All endpoints return data in a format that preserves user authority.
        No endpoint provides recommendations or resolves contradictions.
        """,
        version=settings.app_version,
        docs_url="/docs" if not is_production else None,  # Disable docs in production
        redoc_url="/redoc" if not is_production else None,
        lifespan=lifespan,
    )

    # =========================================================================
    # MIDDLEWARE STACK (order matters - first added = last executed)
    # =========================================================================

    # 1. Security Headers (outermost - runs last, adds headers to response)
    app.add_middleware(
        SecurityHeadersMiddleware,
        include_hsts=is_production,  # Only add HSTS in production (requires HTTPS)
    )

    # 2. Rate Limiting
    app.add_middleware(RateLimitMiddleware)

    # 3. CORS Configuration
    # In production: restrict to specific origins
    # In development: allow localhost origins
    if is_production:
        # Production: use explicit origins from environment
        cors_origins = settings.cors_origins_list
        logger.info(f"CORS configured for production: {cors_origins}")
    else:
        # Development: allow common development origins
        cors_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
        # Also add any configured origins
        cors_origins.extend([o for o in settings.cors_origins_list if o not in cors_origins])
        logger.info(f"CORS configured for development: {cors_origins}")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Webhook-Signature",
            "X-Webhook-Timestamp",
            "X-TradingView-Signature",
            "X-TradingView-Timestamp",
        ],
        expose_headers=[
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "Retry-After",
        ],
    )

    # =========================================================================
    # ROUTES
    # =========================================================================

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint.

        Returns basic application status and security configuration.
        """
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": environment,
            "security": {
                "webhook_auth_enabled": settings.webhook_secret is not None,
                "cors_restricted": is_production,
                "rate_limiting": "enabled",
                "security_headers": "enabled",
            },
        }

    # Security info endpoint (development only)
    if not is_production:

        @app.get("/security-info", tags=["Development"])
        async def security_info():
            """
            Security configuration info (development only).

            This endpoint is disabled in production.
            """
            return {
                "environment": environment,
                "cors_origins": cors_origins,
                "webhook_secret_configured": settings.webhook_secret is not None,
                "rate_limits": {
                    "webhook": "60 requests/minute",
                    "api": "100 requests/minute",
                },
                "security_headers": [
                    "X-Content-Type-Options",
                    "X-Frame-Options",
                    "X-XSS-Protection",
                    "Referrer-Policy",
                    "Permissions-Policy",
                ],
                "production_only_headers": [
                    "Strict-Transport-Security (HSTS)",
                ],
            }

    return app


# Create application instance
app = create_app()
