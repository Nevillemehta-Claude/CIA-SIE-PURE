"""
Integration Test Configuration
==============================

Shared fixtures for integration tests.
Uses an in-memory SQLite database for test isolation.
"""

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Import Base before other modules to ensure models are registered
from cia_sie.dal.database import Base
from cia_sie.dal import models  # noqa: F401 - ensures models are registered


# Create test engine with in-memory SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for the entire test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create and dispose test engine for each test."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def setup_database(test_engine):
    """Setup and teardown test database for each test."""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(setup_database):
    """Create async test client for API testing."""
    from cia_sie.api.app import app
    from cia_sie.dal.database import get_session_dependency
    from cia_sie.core.security import webhook_rate_limiter, api_rate_limiter

    test_engine = setup_database

    test_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async def override_get_session():
        """Override database session for testing."""
        async with test_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    # Override the database dependency
    app.dependency_overrides[get_session_dependency] = override_get_session

    # Clear rate limiter state and increase limits for tests
    webhook_rate_limiter.requests.clear()
    api_rate_limiter.requests.clear()
    original_webhook_limit = webhook_rate_limiter.requests_per_minute
    original_api_limit = api_rate_limiter.requests_per_minute
    webhook_rate_limiter.requests_per_minute = 10000
    api_rate_limiter.requests_per_minute = 10000

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Restore original limits and clear overrides after test
    webhook_rate_limiter.requests_per_minute = original_webhook_limit
    api_rate_limiter.requests_per_minute = original_api_limit
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db_session(setup_database):
    """Get a database session for direct database access in tests."""
    test_engine = setup_database

    test_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with test_session_factory() as session:
        yield session
