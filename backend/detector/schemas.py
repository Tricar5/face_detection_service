"""Pydantic schemas"""
import datetime as dt
import enum

from pydantic import BaseModel, Field


__all__ = ["Task", "TaskResponse"]


class TaskStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    ERROR = "ERROR"


class Task(BaseModel):
    id: str = Field(description="Unique ID of task")
    status: str = Field(description="Status of task")


class TaskResponse(Task):
    result: str | None = Field(default="", description="Resulting Path to get predicted image")
