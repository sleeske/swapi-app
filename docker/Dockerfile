# Dockerfile could be rewritten to use multi-stage build

FROM python:3.8.5-slim-buster as build

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libxml2 \
    apt-utils\
    build-essential \
    libpq5 \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements/ /requirements

RUN pip install -U pip \
    && pip install -r /requirements/local.txt

WORKDIR /project/src
COPY ./src /project/src


