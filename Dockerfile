FROM python:3.10-slim-buster
LABEL maintainer="s.okhrym@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR app/

COPY requirements.txt .

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt && \
    apk --purge del .build-deps

COPY . .
