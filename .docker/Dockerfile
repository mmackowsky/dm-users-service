FROM python:3.11

EXPOSE 8002

ENV PYTHONUNBUFFERED=1

WORKDIR /dm-users-service

COPY pyproject.toml poetry.lock /dm-users-service/

RUN pip3 install poetry && poetry install --no-cache

COPY . .
