from fastapi import APIRouter

from hello_world.core.config import Settings, settings


def get_router() -> APIRouter:
    """Build router for Config resource"""
    router = APIRouter(prefix="/config", tags=["config"])

    async def get_config() -> Settings:
        return settings

    router.add_api_route("/", get_config, methods=["GET"], summary="Get application configuration")
    return router
