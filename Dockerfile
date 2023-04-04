FROM python:3.11
MAINTAINER FOLLGAD <https://github.com/FOLLGAD>

WORKDIR /app/source

COPY requirements.txt /app/
RUN pip install --progress-bar=off --no-cache-dir -U pip setuptools wheel && pip install --progress-bar=off --no-cache-dir -r /app/requirements.txt

COPY . /app/source/
RUN chmod +x /app/source/entrypoint.sh

ENV PYTHONIOENCODING=utf-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PYTHONUNBUFFERED=1

CMD ["/app/source/entrypoint.sh"]