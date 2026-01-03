"""
CIA-SIE API Layer
=================

REST API and WebSocket endpoints using FastAPI.

GOVERNED BY: Section 11.2 (API Design)

API DESIGN STANDARDS:
- Style: RESTful with versioning
- Format: JSON
- Versioning: /api/v1/...
- Documentation: OpenAPI (auto-generated)
"""

from cia_sie.api.app import create_app
from cia_sie.api.routes import api_router

__all__ = [
    "create_app",
    "api_router",
]
