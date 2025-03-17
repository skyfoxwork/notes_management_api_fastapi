from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config.dependencies import get_settings


settings = get_settings()

POSTGRESQL_DATABASE_URL = (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
                           f"{settings.POSTGRES_HOST}:{settings.POSTGRES_DB_PORT}/{settings.POSTGRES_DB}")

postgresql_engine = create_async_engine(POSTGRESQL_DATABASE_URL, echo=True, future=True)

AsyncPostgresqlSessionLocal = async_sessionmaker(
    postgresql_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True
)


async def get_db():
    async with AsyncPostgresqlSessionLocal() as async_session:
        yield async_session
