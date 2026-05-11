FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --extra cpu --no-dev

FROM base AS production

RUN groupadd -r lumen && useradd -r -g lumen -m -s /sbin/nologin lumen

WORKDIR /app
COPY --from=builder /usr/local /usr/local

COPY . .
RUN chown -R lumen:lumen /app

USER lumen
