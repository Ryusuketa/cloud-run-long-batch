FROM python:3.7.12-slim-buster

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry &&\
    poetry config virtualenvs.create false &&\
    poetry config experimental.new-installer false &&\
    poetry install --no-interaction --no-ansi 
ARG GCS_BUCKET_NAME
ENV GCS_BUCKET_NAME=${GCS_BUCKET_NAME}

WORKDIR /app
COPY main.py .
COPY pipeline.py .

ENTRYPOINT uvicorn main:app --host 0.0.0.0