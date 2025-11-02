import functools
from contextvars import ContextVar
from typing import Any, Awaitable, Dict, Optional

# from sqlalchemy.orm import declarative_base
from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from hello_world.core.config import settings
from hello_world.core.types import AsyncCallable

# Base = declarative_base()

db_session_context: ContextVar[str | None] = ContextVar("db_session_context", default=None)
db_engine: AsyncEngine = create_async_engine(
    url=settings.db.url.encoded_string(), pool_size=settings.db.pool_size
)


def get_db_session_context() -> str:
    session_id = db_session_context.get()
    if not session_id:
        raise ValueError("Currently no session is available")
    return session_id


def set_db_session_context(*, session_id: Optional[str]) -> None:
    db_session_context.set(session_id)


AsyncScopedSession = async_scoped_session(
    session_factory=async_sessionmaker(bind=db_engine, autoflush=False, autocommit=False),
    scopefunc=get_db_session_context,
)


def get_current_session() -> AsyncSession:
    return AsyncScopedSession()


def transactional(func: AsyncCallable) -> AsyncCallable:
    @functools.wraps(func)
    async def _wrapper(*args: str, **kwargs: int) -> Any:
        try:
            db_session = get_current_session()

            if db_session.in_transaction():
                return await func(*args, **kwargs)

            async with db_session.begin():
                # automatically committed / rolled back thanks to the context manager
                return await func(*args, **kwargs)

        except Exception as error:
            logger.info(f"request hash: {get_db_session_context()}")
            logger.exception(error)
            raise

    return _wrapper



# class DatabaseSessionManager:

#     def __init__(self, host: str):
#         self._engine: AsyncEngine | None = create_async_engine(host)
#         self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

#     async def close(self):
#         if self._engine is not None:
#             await self._engine.dispose(close=True)
#             self._engine = None
#             self._sessionmaker = None

#     @contextlib.asynccontextmanager
#     async def connect(self) -> AsyncIterator[AsyncConnection]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         async with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception:
#                 await connection.rollback()
#                 raise

#     @contextlib.asynccontextmanager
#     async def session(self) -> AsyncIterator[AsyncSession]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         session = self._sessionmaker()
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()


# db_session_manager = DatabaseSessionManager(host=DATABASE_CONFIG)


# async def get_db_session(session_manager: DatabaseSessionManager):
#     async with session_manager.session() as session:
#         yield session
#         logger.debug("DB Session yield finished")


# def db_session(func) -> Coroutine[Any, Any, None]:  # type:ignore
#     async def wrapper(*args: Any, **kwargs: Any):
#         session: AsyncSession
#         async with db_session_manager.session() as session:  # (this is now a scoped session)
#             try:
#                 func(db_session=session, *args, **kwargs)  # No need to pass session explicitly
#                 await session.commit()
#             except:
#                 await session.rollback()
#                 raise
#             finally:
#                 await session.close()  # NOTE: *remove* rather than *close* here

#     return wrapper  # type:ignore