import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import create_async_engine
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def db_url():
    return "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def engine(db_url):
    return create_async_engine(db_url, echo=True)


@pytest.fixture(scope="session")
async def tables(engine):
    from database.models import Base

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True)
async def db(tables, engine):
    await tables
    async with AsyncSession(engine) as session:
        yield session
