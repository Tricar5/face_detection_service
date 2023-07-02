"""Header for Celery Tasks"""

from celery_tasks.tasks import predict_image

__all__ = [
    "predict_image"
]
