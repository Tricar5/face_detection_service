FROM python:3.10-slim

RUN apt-get update && apt-get install libglib2.0-0 libgl1 ffmpeg libsm6 libxext6  -y


RUN mkdir -p /app/detector
WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry install --only backend

COPY ./detector /app/detector
