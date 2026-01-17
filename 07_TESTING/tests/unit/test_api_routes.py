"""
Tests for CIA-SIE API Routes
============================

Unit tests for individual API route handlers.

GOVERNED BY: Section 11 (Backend Standards)
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cia_sie.core.models import Instrument, InstrumentCreate
from cia_sie.core.exceptions import DuplicateError, InstrumentNotFoundError
from cia_sie.dal.models import InstrumentDB, SiloDB, ChartDB, AnalyticalBasketDB
from cia_sie.dal.repositories import InstrumentRepository


class TestInstrumentsRoute:
    """Tests for instruments API route handlers."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock repository."""
        repo = Mock(spec=InstrumentRepository)
        repo.get_all = AsyncMock()
        repo.get_by_id = AsyncMock()
        repo.get_by_symbol = AsyncMock()
        repo.create = AsyncMock()
        repo.update = AsyncMock()
        repo.delete = AsyncMock()
        return repo

    @pytest.fixture
    def sample_instrument_db(self):
        """Create sample InstrumentDB for testing."""
        return Mock(
            spec=InstrumentDB,
            instrument_id="12345678-1234-1234-1234-123456789012",
            symbol="NIFTY50",
            display_name="Nifty 50 Index",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            is_active=True,
            metadata_json=None,
        )

    @pytest.mark.asyncio
    async def test_list_instruments_returns_list(self, mock_repo, sample_instrument_db):
        """Test list instruments returns proper list."""
        mock_repo.get_all.return_value = [sample_instrument_db]

        from cia_sie.api.routes.instruments import list_instruments
        result = await list_instruments(active_only=True, repo=mock_repo)

        assert len(result) == 1
        mock_repo.get_all.assert_called_once_with(active_only=True)

    @pytest.mark.asyncio
    async def test_create_instrument_success(self, mock_repo, sample_instrument_db):
        """Test creating an instrument."""
        mock_repo.create.return_value = sample_instrument_db

        from cia_sie.api.routes.instruments import create_instrument
        data = InstrumentCreate(symbol="NIFTY50", display_name="Nifty 50 Index")

        result = await create_instrument(data=data, repo=mock_repo)

        assert result.symbol == "NIFTY50"
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_instrument_duplicate_raises_409(self, mock_repo):
        """Test creating duplicate instrument raises 409."""
        mock_repo.create.side_effect = DuplicateError("Already exists")

        from cia_sie.api.routes.instruments import create_instrument
        data = InstrumentCreate(symbol="EXISTS", display_name="Test")

        with pytest.raises(HTTPException) as exc_info:
            await create_instrument(data=data, repo=mock_repo)

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_get_instrument_not_found_raises_404(self, mock_repo):
        """Test getting nonexistent instrument raises 404."""
        mock_repo.get_by_id.return_value = None

        from cia_sie.api.routes.instruments import get_instrument

        with pytest.raises(HTTPException) as exc_info:
            await get_instrument(instrument_id="nonexistent", repo=mock_repo)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_instrument_not_found_raises_404(self, mock_repo):
        """Test updating nonexistent instrument raises 404."""
        mock_repo.update.side_effect = InstrumentNotFoundError("Not found")

        from cia_sie.api.routes.instruments import update_instrument

        with pytest.raises(HTTPException) as exc_info:
            await update_instrument(
                instrument_id="nonexistent",
                display_name="New Name",
                repo=mock_repo
            )

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_instrument_not_found_raises_404(self, mock_repo):
        """Test deleting nonexistent instrument raises 404."""
        mock_repo.delete.return_value = False

        from cia_sie.api.routes.instruments import delete_instrument

        with pytest.raises(HTTPException) as exc_info:
            await delete_instrument(instrument_id="nonexistent", repo=mock_repo)

        assert exc_info.value.status_code == 404


class TestWebhookRoute:
    """Tests for webhook API route handlers."""

    @pytest.fixture
    def mock_handler(self):
        """Create mock webhook handler."""
        handler = Mock()
        handler.process_webhook = AsyncMock()
        return handler

    @pytest.fixture
    def mock_request(self):
        """Create mock request."""
        request = Mock()
        request.headers = {}
        request.client = Mock(host="192.168.1.1")
        return request

    @pytest.mark.asyncio
    async def test_webhook_health_returns_status(self):
        """Test webhook health endpoint returns status."""
        from cia_sie.api.routes.webhooks import webhook_health

        result = await webhook_health()

        assert result["status"] == "healthy"
        assert "authentication_enabled" in result


class TestRelationshipsRoute:
    """Tests for relationships API route handlers."""

    @pytest.fixture
    def mock_exposer(self):
        """Create mock relationship exposer."""
        exposer = Mock()
        exposer.expose_for_silo = AsyncMock()
        exposer.expose_for_instrument = AsyncMock()
        return exposer

    @pytest.mark.asyncio
    async def test_get_silo_relationships_not_found(self, mock_exposer):
        """Test getting relationships for nonexistent silo."""
        mock_exposer.expose_for_silo.side_effect = ValueError("Not found")

        from cia_sie.api.routes.relationships import get_silo_relationships

        with pytest.raises(HTTPException) as exc_info:
            await get_silo_relationships(silo_id="nonexistent", exposer=mock_exposer)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_get_instrument_relationships_empty(self, mock_exposer):
        """Test getting relationships when no silos exist."""
        mock_exposer.expose_for_instrument.return_value = []

        from cia_sie.api.routes.relationships import get_instrument_relationships

        with pytest.raises(HTTPException) as exc_info:
            await get_instrument_relationships(
                instrument_id="no-silos",
                exposer=mock_exposer
            )

        assert exc_info.value.status_code == 404


class TestBasketsRoute:
    """Tests for baskets API route handlers."""

    @pytest.fixture
    def mock_repo(self):
        """Create mock basket repository."""
        from cia_sie.dal.repositories import BasketRepository
        repo = Mock(spec=BasketRepository)
        repo.get_all = AsyncMock()
        repo.get_by_instrument = AsyncMock()
        repo.get_with_charts = AsyncMock()
        repo.create = AsyncMock()
        repo.add_chart_to_basket = AsyncMock()
        repo.remove_chart_from_basket = AsyncMock()
        repo.delete = AsyncMock()
        return repo

    @pytest.fixture
    def sample_basket_db(self):
        """Create sample AnalyticalBasketDB for testing."""
        return Mock(
            spec=AnalyticalBasketDB,
            basket_id="12345678-1234-1234-1234-123456789012",
            basket_name="My Basket",
            basket_type="CUSTOM",
            description=None,
            instrument_id=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            is_active=True,
            chart_associations=[],
        )

    @pytest.mark.asyncio
    async def test_list_baskets_returns_list(self, mock_repo, sample_basket_db):
        """Test list baskets returns proper list."""
        mock_repo.get_all.return_value = [sample_basket_db]

        from cia_sie.api.routes.baskets import list_baskets
        result = await list_baskets(
            instrument_id=None,
            active_only=True,
            repo=mock_repo
        )

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_basket_not_found_raises_404(self, mock_repo):
        """Test getting nonexistent basket raises 404."""
        mock_repo.get_with_charts.return_value = None

        from cia_sie.api.routes.baskets import get_basket

        with pytest.raises(HTTPException) as exc_info:
            await get_basket(basket_id="nonexistent", repo=mock_repo)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_add_chart_duplicate_raises_409(self, mock_repo):
        """Test adding duplicate chart raises 409."""
        mock_repo.add_chart_to_basket.return_value = False

        from cia_sie.api.routes.baskets import add_chart_to_basket

        with pytest.raises(HTTPException) as exc_info:
            await add_chart_to_basket(
                basket_id="basket-1",
                chart_id="chart-1",
                repo=mock_repo
            )

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_remove_chart_not_found_raises_404(self, mock_repo):
        """Test removing nonexistent chart raises 404."""
        mock_repo.remove_chart_from_basket.return_value = False

        from cia_sie.api.routes.baskets import remove_chart_from_basket

        with pytest.raises(HTTPException) as exc_info:
            await remove_chart_from_basket(
                basket_id="basket-1",
                chart_id="chart-1",
                repo=mock_repo
            )

        assert exc_info.value.status_code == 404


class TestAPIConstitutionalCompliance:
    """
    Tests verifying API routes maintain constitutional compliance.

    CRITICAL: These tests ensure no prohibited patterns exist in routes.
    """

    def test_no_aggregation_endpoints(self):
        """
        CRITICAL: No aggregation endpoints should exist.
        """
        from cia_sie.api.routes import api_router

        routes = [route.path for route in api_router.routes]

        prohibited_paths = [
            "aggregate",
            "combined",
            "overall",
            "net-direction",
            "weighted",
        ]

        for route in routes:
            for prohibited in prohibited_paths:
                assert prohibited not in route.lower(), \
                    f"Prohibited path '{prohibited}' found in route '{route}'"

    def test_no_recommendation_endpoints(self):
        """
        CRITICAL: No recommendation endpoints should exist.
        """
        from cia_sie.api.routes import api_router

        routes = [route.path for route in api_router.routes]

        prohibited_paths = [
            "recommend",
            "advice",
            "suggest",
            "action",
        ]

        for route in routes:
            for prohibited in prohibited_paths:
                assert prohibited not in route.lower(), \
                    f"Prohibited path '{prohibited}' found in route '{route}'"

    def test_no_score_endpoints(self):
        """
        CRITICAL: No scoring endpoints should exist.
        """
        from cia_sie.api.routes import api_router

        routes = [route.path for route in api_router.routes]

        prohibited_paths = [
            "score",
            "confidence",
            "rating",
        ]

        for route in routes:
            for prohibited in prohibited_paths:
                assert prohibited not in route.lower(), \
                    f"Prohibited path '{prohibited}' found in route '{route}'"
