import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from database.models import Base, City
from database.session import create_async_engine
from main import app


@pytest_asyncio.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture(scope="session")
def db_url():
    return "sqlite+aiosqlite://"


@pytest_asyncio.fixture(scope="session")
def engine(db_url):
    return create_async_engine(db_url)


@pytest_asyncio.fixture(autouse=True)
async def db(engine: AsyncEngine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    Session = async_sessionmaker(engine)
    session = Session()
    try:
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture
async def cities(db: AsyncSession):
    res = await db.execute(
        insert(City)
        .values(
            [
                {"name": "Rio de Janeiro", "normalized_name": "Rio de Janeiro", "state_abbreviation": "RJ"},
                {"name": "São Paulo", "normalized_name": "Sao Paulo", "state_abbreviation": "SP"},
            ]
        )
        .returning(City)
    )
    return res.scalars().all()
