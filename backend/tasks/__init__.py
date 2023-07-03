"""Header for Celery Tasks"""

from backend.tasks.tasks import predict_image


__all__ = ["predict_image"]
