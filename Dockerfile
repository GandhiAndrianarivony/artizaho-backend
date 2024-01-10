FROM python:3.11.7-slim-bullseye

ENV PIP_DISABLE_PIP_VESION CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /apps

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh

COPY . .
