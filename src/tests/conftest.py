import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from sqlalchemy import text

from src.config.settings import Settings
from src.main import app
from src.database.session_sqlite import init_db, get_sqlite_db_contextmanager
from src.database.session_postgresql import get_db
from src.database.session_sqlite import get_sqlite_db
from src.security.token_manager import JWTAuthManager
from src.config.dependencies import get_settings


@pytest_asyncio.fixture(scope="session")
async def settings():
    return get_settings()


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


@pytest_asyncio.fixture(scope="function")
async def jwt_manager(settings: Settings):
    return JWTAuthManager(
        secret_key_access=settings.SECRET_KEY_ACCESS,
        secret_key_refresh=settings.SECRET_KEY_REFRESH,
        algorithm=settings.JWT_SIGNING_ALGORITHM
    )


@pytest_asyncio.fixture(autouse=True)
async def enable_foreign_keys(db_session):
    await db_session.execute(text("PRAGMA foreign_keys = ON;"))
    await db_session.commit()
