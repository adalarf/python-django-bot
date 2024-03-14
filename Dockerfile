FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --deploy --no-cache-dir

COPY . .