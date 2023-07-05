"""Celery Tasks module"""
import logging

import cv2
from celery import Task
from celery.exceptions import MaxRetriesExceededError

from detector.config import settings
from detector.schemas import TaskStatus
from detector.tasks.app_worker import app
from detector.tasks.yolo import YoloModel


__all__ = [
    "predict_image",
]


class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            logging.info("Loading Model...")
            self.model = YoloModel(settings.MODEL_PATH)
            logging.info("Model loaded")
        return self.run(*args, **kwargs)


@app.task(ignore_result=False, bind=True, base=PredictTask)
def predict_image(self, img_path):
    try:
        # Read Image
        srcimg = cv2.imread(img_path)

        # Detect Objects
        boxes, scores, classids, kpts = self.model.detect(srcimg)

        # Draw detections
        dstimg = self.model.draw_detections(srcimg, boxes, scores, kpts)

        # Saving Image
        res_path = f"{settings.RESULT_FOLDER}/{img_path.split('/')[-1]}"
        cv2.imwrite(res_path, dstimg)

        # data_pred = self.model.predict(data, settings.RESULT_FOLDER)
        return {"result": res_path, "original": img_path, "bboxes": list(boxes[0])}
    except Exception as ex:
        try:
            self.retry(countdown=2)
        except MaxRetriesExceededError as ex:
            return {"status": TaskStatus.FAILED, "result": "Max retries achieved!"}
