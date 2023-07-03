import os
import sys


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.api import api_router as task_router
from backend.config import settings


origins = [
    "http://localhost",
    "http://localhost:8080",
]


def create_app() -> FastAPI:

    application = FastAPI(
        title=settings.API_NAME,
        version=settings.API_VERSION,
        docs_url="/docs"
    )

    # Include additional Router
    application.include_router(task_router, prefix="/api")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app: FastAPI = create_app()


#app.mount("/static", StaticFiles(directory="backend/static"), name="static")
#templates = Jinja2Templates(directory="backend/templates")


#@app.get("/")
#def home(request: Request):
#    return templates.TemplateResponse("home.html", context={"request": request})

