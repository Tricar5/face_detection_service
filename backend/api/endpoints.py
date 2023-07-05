import logging
import os
import json
import uuid
from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, File, UploadFile, status, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse, FileResponse

from backend.deps import get_redis
from backend.config import settings
from backend.schemas import Task, TaskResponse, TaskStatus
from backend.tasks import predict_image
from backend.utils import get_all_tasks

__all__ = ["api_router"]

api_router = APIRouter(tags=["Face Detection"])


@api_router.post("/face/process",
                 response_model=list[TaskResponse],
                 status_code=status.HTTP_201_CREATED)
async def process_img(file: UploadFile = File(...)):
    """
    Endpoint to create task for image processing
    :param files:
    :return:
    """


    try:
        task_id = str(uuid.uuid4())

        ext = file.filename.split(".")[-1]
        file_name = f"{task_id}.{ext}"
        file_path = f"{settings.UPLOAD_FOLDER}/{file_name}"
        with open(file_path, "wb+") as f:
            f.write(file.file.read())

                # start task prediction
        task_id = predict_image.delay(file_path)

        resp = TaskResponse(
                id=str(task_id), status=TaskStatus.PROCESSING, result=f"{settings.RESULT_FOLDER}/{file_name}"
            )

        if not task_id:
                # logging.info(ex)
            resp = TaskResponse(id=str(task_id), status=TaskStatus.ERROR)

        return JSONResponse(status_code=201, content=resp.dict())
    except Exception as ex:
        logging.info(ex)
        return JSONResponse(status_code=400, content={"message": str(ex)})


@api_router.get("/face/{task_id}",
                status_code=status.HTTP_200_OK,
                response_model=TaskResponse)
async def get_result(task_id: str):
    """
    Endpoint to get Task Status
    :param task_id:
    :return:
    """
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return TaskResponse(id=str(task_id), status=task.status)
    # Task done: return the value
    return TaskResponse(id=str(task.id), status=task.status, result=task.result.get('result'))


@api_router.get("/face/tasks/list",
                )
async def get_task_list(start: int = 0,
                        end: int = 50,
                        r=Depends(get_redis)):
    """Endpoint to get all processed tasks"""
    tasks = get_all_tasks(r, start, end)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"data" : tasks})


@api_router.get("/face/result/{task_id}",
                )
async def get_task_data(task_id: str,
                        r=Depends(get_redis)):
    """Endpoint to get tasks result (predicted image) """
    resp = r.get("celery-task-meta-" + task_id)

    # Checking Task Existence
    if not resp:
        raise HTTPException(status_code=404, detail="Task not Found!")

    data = json.loads(resp.decode('utf-8'))

    # Checking Task Status
    if not data.get('status') == TaskStatus.SUCCESS.value:
        raise HTTPException(status_code=404, detail="Image not Found!")

    img_path = data.get('result').get('result')
    return FileResponse(img_path)
