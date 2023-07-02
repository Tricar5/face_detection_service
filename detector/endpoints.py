import logging
import os
import uuid
from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from celery_tasks import predict_image
from detector.config import settings
from detector.schemas import Prediction


__all__ = ["api_router"]

api_router = APIRouter()


@api_router.post("/face/process")
async def process(files: List[UploadFile] = File(...)):
    tasks = []
    try:
        for file in files:
            d = {}
            try:
                name = str(uuid.uuid4()).split("-")[0]
                ext = file.filename.split(".")[-1]
                file_name = f"{settings.UPLOAD_FOLDER}/{name}.{ext}"
                with open(file_name, "wb+") as f:
                    f.write(file.file.read())
                f.close()

                # start task prediction
                task_id = predict_image.delay(os.path.join("detector", file_name))
                d["task_id"] = str(task_id)
                d["status"] = "PROCESSING"
                d["url_result"] = f"{settings.RESULT_FOLDER}/{task_id}"
            except Exception as ex:
                logging.info(ex)
                d["task_id"] = str(task_id)
                d["status"] = "ERROR"
                d["url_result"] = ""
            tasks.append(d)
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logging.info(ex)
        return JSONResponse(status_code=400, content=[])


@api_router.get("/face/{task_id}", response_model=Prediction)
async def result(task_id: str):
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return JSONResponse(status_code=202, content={"task_id": str(task_id), "status": task.status, "result": ""})

    # Task done: return the value
    task_result = task.get()
    result = task_result.get("result")
    return JSONResponse(
        status_code=200, content={"task_id": str(task_id), "status": task_result.get("status"), "result": result}
    )


@api_router.get("/status/{task_id}", response_model=Prediction)
async def status(task_id: str):
    task = AsyncResult(task_id)
    return JSONResponse(status_code=200, content={"task_id": str(task_id), "status": task.status, "result": ""})
