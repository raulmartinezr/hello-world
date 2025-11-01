from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from hello_world.core.config import settings  # type: ignore
from loguru import logger


def build_app() -> FastAPI:
    # session_manager: Optional[DatabaseSessionManager] = None
    # if settings.PYROSCOPE_SERVER_ADDRESS:  # type:ignore
    #     check_enable_profiling()

    # Ability to provide session manager. Necessary for tests.
    # repository_factory = (
    #     RepositoriesFactory(session_manager)
    #     if session_manager
    #     else RepositoriesFactory(db_session_manager)
    # )

    # Fastapi lifespan
    # @asynccontextmanager
    # async def lifespan(app: FastAPI):  # type: ignore[unused-ignore,not-accessed]
    #     # Preparations
    #     yield app
    #     # Clean up
    #     await db_engine.dispose(close=True)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:  # type: ignore[unused-ignore,not-accessed,unused-function-argument]
        # Preparations (startup)
        # e.g., await db_engine.connect() if needed
        try:
            yield  # yield None
        finally:
            logger.info("Shutting down application...")
            # Clean up (shutdown)
            # await db_engine.dispose(close=True)

    app = FastAPI(
        title=f"{settings.project_name}: API endpoints",  # type: ignore[unused-ignore,unknown-type]
        openapi_url=f"/{settings.api_version}/openapi.json",  # type: ignore[unused-ignore,unknown-type]
        lifespan=lifespan,
    )

    # Build middlewares
    # Set all CORS enabled origins
    # app.add_middleware(
    #     OrganizationMiddleware,
    #     refresh_interval_seconds=settings.organiations_middleware_cache_refresh_period,  # type:ignore
    #     organizations_repository_factory=organizations_repository_factory,
    # )
    # app.add_middleware(DatabaseSessionMiddleware)
    # if settings.BACKEND_CORS_ORIGINS:  # type:ignore
    #     app.add_middleware(
    #         CORSMiddleware,
    #         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],  # type:ignore
    #         allow_credentials=True,
    #         allow_methods=["*"],
    #         allow_headers=["*"],
    #     )
    # # Build routers
    # users_router: APIRouter = build_users_router(users_repository_factory=users_repository_factory)  # type: ignore
    # organizations_router: APIRouter = build_organizations_router(
    #     organizations_repository_factory=organizations_repository_factory  # type: ignore
    # )

    # app.include_router(users_router, prefix="/user")
    # app.include_router(organizations_router, prefix="/organization")

    # app.include_router(users_router, prefix=f"/v1/user") # maybe better as different APIs
    return app


app: FastAPI = build_app()
