"""Header for Celery Tasks"""

from detector.tasks.tasks import predict_image


__all__ = ["predict_image"]
