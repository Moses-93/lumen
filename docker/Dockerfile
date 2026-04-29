FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --no-install-project --extra cpu --no-dev

FROM base AS production

RUN groupadd -r lumen && useradd -r -g lumen -m -s /sbin/nologin lumen

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .
RUN chown -R lumen:lumen /app

USER lumen
