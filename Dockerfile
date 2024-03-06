FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --deploy

COPY . .