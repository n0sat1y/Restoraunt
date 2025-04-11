import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from src.core.db import Base, db
from src.main import app

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_db_engine():
    engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
    
@pytest.fixture(scope="function")
async def session(async_db_engine):
    async with async_db_engine.connect() as connection:
        trans = await connection.begin()
        
        async_session = async_sessionmaker(
            expire_on_commit=False,
            bind=connection
        )

        async with async_session() as session: 
            yield session
        await trans.rollback()

@pytest.fixture(scope="function")
async def client(session):
    async def override_get_db():
        yield session
    app.dependency_overrides[db.session] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client