"""Celery configuration"""

import os

from celery import Celery

from detector.config import settings


__all__ = [
    "app",
]

app = Celery("tasks", broker=settings.BROKER_URI, backend=settings.BACKEND_URI, include=settings.TASK_FOLDER)
