"""Celery Tasks module"""
import enum
import logging
from celery import Task
from celery.exceptions import MaxRetriesExceededError
from celery_tasks.app_worker import app
from celery_tasks.yolo import YoloModel

__all__ = [
    "predict_image",
]


class TaskStatus(enum.Enum):

    SUCCESS = "SUCCESS"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"


class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info('Loading Model...')
            self.model = YoloModel()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@app.task(ignore_result=False, bind=True, base=PredictTask)
def predict_image(self, data):
    try:
        data_pred = self.model.predict(data)
        return {'status': TaskStatus.SUCCESS, 'result': data_pred}
    except Exception as ex:
        try:
            self.retry(countdown=2)
        except MaxRetriesExceededError as ex:
            return {'status': TaskStatus.FAILED, 'result': 'Max retries achieved!'}
