FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
 PYTHONDONTWRITEBYTECODE=1 \
 PIP_NO_CACHE_DIR=on \
 PIP_DISABLE_PIP_VERSION_CHECK=on \
 PIP_DEFAULT_TIMEOUT=120 \
 LC_ALL=C.UTF-8 \
 LANG=C.UTF-8

WORKDIR /app

USER root

RUN groupadd -r app && useradd --no-log-init -r -g app app || true \
&& chown -R app /app \
&& mkdir -p /home/app && chown -R app /home/app

# install packages
RUN apt-get update --yes \
&& apt-get install -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" --yes --no-install-recommends \
 curl build-essential sqlite3 \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# install nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
&& apt-get update --yes \
&& apt-get install -y nodejs \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# install configurable-http-proxy
RUN npm install -g configurable-http-proxy

COPY uv.lock pyproject.toml /app/

RUN python3 -m pip install -U uv==0.10.2 \
&& uv export --frozen --no-hashes --no-dev -o requirements.txt \
&& python3 -m pip install -r requirements.txt

USER app

ENTRYPOINT []
CMD ["jupyterhub", "--config", "/usr/local/etc/jupyterhub_config.py", "--upgrade-db"]