import pkgutil
from collections.abc import AsyncIterator, Iterable, Iterator
from contextlib import asynccontextmanager
from importlib import import_module

from fastapi import APIRouter, FastAPI
from loguru import logger

from hello_world.core.config import settings


def _iter_modules(pkg_name: str) -> Iterator[str]:
    """Yield full module names under a package (non-packages only)."""
    pkg = import_module(pkg_name)
    pkg_path = getattr(pkg, "__path__", None)
    if pkg_path is None:
        return
    for m in pkgutil.iter_modules(pkg_path, prefix=f"{pkg_name}."):
        if not m.ispkg:
            yield m.name


def include_versioned_routers(
    app: FastAPI,
    version: str,  # e.g. "v1" or "v2"
    base_package: str | None = __package__,  # your base
    subpackage: str | None = None,  # where routers live under each version
    names: Iterable[str] | None = None,  # optionally whitelist modules: {"users","health"}
) -> None:
    """
    Import all modules under `<base_package>.<version>.<subpackage>` and include
    any `router: APIRouter` or `get_router() -> APIRouter` found.
    """
    pkg = f"{base_package}.{version}.{subpackage}" if subpackage else f"{base_package}.{version}"
    try:
        # validate the package exists
        import_module(pkg)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"Routers package not found: {pkg}. "
            f"Expected something like {pkg}/users.py with a `router` variable."
        ) from e

    target_modules = _iter_modules(pkg)
    if names:
        wanted = {f"{pkg}.{n}" for n in names}
        target_modules = (m for m in target_modules if m in wanted)

    for modname in sorted(target_modules):
        mod = import_module(modname)
        router = getattr(mod, "router", None)
        if isinstance(router, APIRouter):
            app.include_router(router, prefix=f"/{version}")
            continue
        get_router = getattr(mod, "get_router", None)
        if callable(get_router):
            r = get_router()
            if isinstance(r, APIRouter):
                app.include_router(r, prefix=f"/{version}")


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
        version=settings.api_version,  # type: ignore[unused-ignore,unknown-type]
    )
    include_versioned_routers(app, settings.api_version)  # loads all routers

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
