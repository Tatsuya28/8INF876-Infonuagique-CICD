FROM python:3.13-slim

# Mettre à jour les paquets et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends\
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD [ "/app/entrypoint.sh" ]