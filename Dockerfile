FROM python:3.10-slim-buster
LABEL maintainer="s.okhrym@gmail.com"


ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt .

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip3 install -r requirements.txt

COPY . .
