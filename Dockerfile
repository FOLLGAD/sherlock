FROM python:3.11-slim
MAINTAINER FOLLGAD <https://github.com/FOLLGAD>

ARG APP_HOME=/app
ENV APP_HOME ${APP_HOME}
ENV PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_HOME}

COPY requirements.txt ${APP_HOME}/
RUN python -m pip install --no-cache-dir -U pip setuptools wheel && \
    python -m pip install --no-cache-dir -r ${APP_HOME}/requirements.txt

COPY . ${APP_HOME}/

RUN chmod +x ${APP_HOME}/entrypoint.sh

ENTRYPOINT ["sh", "-c", "${APP_HOME}/entrypoint.sh"]