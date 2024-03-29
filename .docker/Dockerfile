FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip3 install poetry && poetry install --no-cache

COPY . .
