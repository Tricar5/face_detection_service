import logging
import os
import uuid
from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, File, UploadFile, status
from starlette.responses import JSONResponse

from detector.config import settings
from detector.schemas import Task, TaskResponse, TaskStatus
from detector.tasks import predict_image


__all__ = ["api_router"]

api_router = APIRouter(tags=["Face Detection"])


@api_router.post("/face/process",
                 response_model=list[TaskResponse],
                 status_code=status.HTTP_202_ACCEPTED)
async def process(files: List[UploadFile] = File(...)):
    """
    Endpoint to create task for image processing
    :param files:
    :return:
    """
    tasks = []
    try:
        for file in files:
            task_id = str(uuid.uuid4())

            ext = file.filename.split(".")[-1]
            file_name = f"{task_id}.{ext}"
            file_path = f"{settings.UPLOAD_FOLDER}/{file_name}"
            with open(file_path, "wb+") as f:
                f.write(file.file.read())

                # start task prediction
            task_id = predict_image.delay(file_path)

            resp = TaskResponse(
                    task_id=str(task_id), status=TaskStatus.PROCESSING, result=f"{settings.RESULT_FOLDER}/{file_name}"
                )

            if not task_id:
                #logging.info(ex)
                resp = TaskResponse(task_id=str(task_id), status=TaskStatus.ERROR)

            tasks.append(resp.dict())
            return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logging.info(ex)
        return JSONResponse(status_code=400, content={"message": str(ex)})


@api_router.get("/face/{task_id}",
                status_code=status.HTTP_200_OK,
                response_model=TaskResponse)
async def result(task_id: str):
    """
    Endpoint to get Task Status
    :param task_id:
    :return:
    """
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return TaskResponse(task_id= str(task_id), status=task.status)

    # Task done: return the value
    task_result = task.get()
    result = task_result.get("result")
    return TaskResponse(task_id=str(task_id), status=task_result.get("status"), result=result)


@api_router.get("/status/{task_id}",
                status_code=status.HTTP_200_OK,
                response_model=TaskResponse)
async def status(task_id: str):
    task = AsyncResult(task_id)
    return TaskResponse(task_id=str(task_id), status=task.status, result=task.result)
