from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config.dependencies import get_settings
from src.database.models.base import Base

settings = get_settings()

SQLITE_DATABASE_URL_MEMORY = "sqlite+aiosqlite:///:memory:"

sqlite_engine = create_async_engine(SQLITE_DATABASE_URL_MEMORY, echo=True, future=True)

AsyncSqliteSessionLocal = async_sessionmaker(
    sqlite_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True
)


async def get_sqlite_db():
    async with AsyncSqliteSessionLocal() as async_session:
        yield async_session


@asynccontextmanager
async def get_sqlite_db_contextmanager():
    async with AsyncSqliteSessionLocal() as async_session:
        yield async_session


async def init_db():
    async with sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
