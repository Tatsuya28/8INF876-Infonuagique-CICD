FROM python:3.13.0-slim

COPY . /app

WORKDIR /app

RUN python3 -m venv /opt/venv

RUN pip install --upgrade pip
RUN /opt/venv/bin/pip install -r requirements.txt