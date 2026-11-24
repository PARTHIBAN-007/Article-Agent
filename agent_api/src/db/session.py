from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


from collections.abc import AsyncIterator

_engine = AsyncEngine |  None = None
_session_factory = AsyncSession | None = None

def init_engine(db_url: str):
    """
    Initializes the SQLAlchemy engine with the provided database URL.
    """
    global _engine, _session_factory
    _engine = create_async_engine(db_url, echo=True)
    _session_factory = async_sessionmaker(bind=_engine)


async def close_engine(engine):
    """
    Closes the SQLAlchemy engine.
    """
    _engine
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