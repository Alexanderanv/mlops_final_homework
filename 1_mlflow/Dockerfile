FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
&& rm -rf /var/lib/apt/lists/* \
&& groupadd -r app && useradd --no-log-init -r -g app app || true \
&& chown -R app /app \
&& mkdir -p /home/app && chown -R app /home/app

COPY uv.lock pyproject.toml /app

RUN python3 -m pip install -U uv==0.10.2 \
&& uv export --frozen --no-hashes --no-dev -o requirements.txt \
&& python3 -m pip install -r requirements.txt

USER app

ENTRYPOINT []
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "8080"]