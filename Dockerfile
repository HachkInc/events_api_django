FROM python:3.9-alpine

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

COPY events_api_django .

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt