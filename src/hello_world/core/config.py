from __future__ import annotations

from pathlib import Path

from loguru import logger
from pydantic import AnyUrl, BaseModel, MySQLDsn, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PKG_ROOT = Path(__file__).resolve().parents[0]
logger.debug("Package root path: {}", PKG_ROOT)


class DB(BaseModel):
    url: PostgresDsn | MySQLDsn | AnyUrl
    pool_size: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        validate_default=False,  # until we introduce valid values
        env_prefix="HELLO_WORLD_",
        env_file=".env",  # load .env
        env_nested_delimiter="__",  # HELLO_WORLD_DB__POOL_SIZE=20
        case_sensitive=False,
        extra="ignore",
    )
    project_name: str = "Hello World"
    api_version: str = "v1"
    log_file: str | None = "hello_world.log"
    env: str = "development"
    debug: bool = False
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    secret_key: SecretStr = SecretStr("CHANGE_ME")  # default (override via env)
    db: DB = DB(url=PostgresDsn("CHANGE_ME"), pool_size=10)


settings = Settings()  # loads env + .env
