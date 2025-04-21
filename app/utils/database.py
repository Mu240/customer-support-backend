from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async SQLAlchemy engine for PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Configure session factory for async database sessions
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """
    Dependency to provide an async database session.
    Yields a session and ensures it is closed after use.
    """
    async with async_session() as session:
        yield session