import os
from functools import lru_cache

from pydantic import BaseSettings


__all__ = ["settings", "get_settings"]


class ApiSettings(BaseSettings):
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "repo/uploads")
    RESULT_FOLDER = os.getenv("RESULT_FOLDER", "repo/results")
    STATIC_FOLDER = os.getenv("STATIC_DIR", "static/results")


@lru_cache(maxsize=1)
def get_settings() -> ApiSettings:
    return ApiSettings()


settings: ApiSettings = get_settings()
