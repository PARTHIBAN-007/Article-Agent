from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.config import get_settings
from collections.abc import AsyncIterator

_engine =  None
_session_factory = None

settings = get_settings()

def init_engine():
    """
    Initializes the SQLAlchemy engine with the provided database URL.
    """
    db_url = settings.POSTGRES_HOST
    global _engine, _session_factory
    _engine = create_async_engine(db_url, echo=True)
    _session_factory = async_sessionmaker(bind=_engine)


async def close_engine():
    """
    Closes the SQLAlchemy engine.
    """
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Provides a new SQLAlchemy session.
    """
    if _session_factory is None:
        raise RuntimeError("Session factory is not initialized. Call init_engine first.")
    async with _session_factory() as session:
        yield session