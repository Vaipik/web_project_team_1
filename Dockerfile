FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY /project /app/project

