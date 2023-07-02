"""Celery configuration"""

import os
from celery import Celery
from celery_tasks.config import settings
__all__ = [
    "app"
]

app = Celery(
    'celery_tasks',
    broker=settings.BROKER_URI,
    backend=settings.BACKEND_URI,
    include=settings.TASK_FOLDER
)
