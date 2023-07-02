import os

from pydantic import BaseSettings


class CelerySettings(BaseSettings):

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "repo/uploads")
    RESULT_FOLDER = os.getenv("RESULT_FOLDER", "repo/result")
    TASK_FOLDER = 'celery_tasks.tasks'
    BROKER_URI = 'amqp://rabbitmq'
    BACKEND_URI = 'redis://redis'


settings = CelerySettings()
