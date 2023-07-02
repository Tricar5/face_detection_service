import os
import sys


sys.path.insert(0, os.path.realpath(os.path.pardir))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from detector.config import settings
from detector.endpoints import api_router


isdir = os.path.isdir(settings.UPLOAD_FOLDER)
if not isdir:
    os.makedirs(settings.UPLOAD_FOLDER)

isdir = os.path.isdir(settings.STATIC_FOLDER)
if not isdir:
    os.makedirs(settings.STATIC_FOLDER)

origins = [
    "http://localhost",
    "http://localhost:8080",
]


def create_app() -> FastAPI:
    appplication = FastAPI()
    appplication.mount("/static", StaticFiles(directory=settings.STATIC_FOLDER), name="static")

    appplication.include_router(api_router, prefix="/detector")

    appplication.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return appplication


app: FastAPI = create_app()
