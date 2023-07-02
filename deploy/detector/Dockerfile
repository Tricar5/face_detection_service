FROM python:3.10-bullseye

RUN mkdir -p /app/detector
WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry install --only backend

COPY ./detector /app/detector

COPY ./celery_tasks /app/celery_tasks
