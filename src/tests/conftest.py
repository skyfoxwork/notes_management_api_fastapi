import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.database.session_sqlite import init_db, get_sqlite_db_contextmanager
from src.database.session_postgresql import get_db
from src.database.session_sqlite import get_sqlite_db


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_db] = get_sqlite_db
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    await init_db()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with get_sqlite_db_contextmanager() as session:
        yield session
