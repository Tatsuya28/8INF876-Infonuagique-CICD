FROM python:3.13.0-slim

COPY . /app

WORKDIR /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmode +x /entrypoint.sh

CMD [ "/app/entrypoint.sh" ]