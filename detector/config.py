import os
from functools import lru_cache

from pydantic import BaseSettings


__all__ = ["settings", "get_settings"]


class AppSettings(BaseSettings):
    # Base App Settings

    # Files Settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "repo/uploads")
    RESULT_FOLDER = os.getenv("RESULT_FOLDER", "repo/results")
    STATIC_FOLDER: str = os.getenv("STATIC_DIR", "static/results")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "repo/models/yolov8n-face.onnx")
    TASK_FOLDER: str = "detector.tasks.tasks"

    # Connections
    BROKER_URI: str = os.getenv("BROKER_URI", "amqp://localhost:5672")
    BACKEND_URI: str = os.getenv("BACKEND_URI", "redis://localhost:6379")


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()


settings: AppSettings = get_settings()
