#FROM python:3.13-slim
#
## Set working directory
#WORKDIR /app
#
## Install system & build dependencies
#RUN apt-get update && apt-get install -y \
#    curl build-essential libpq-dev postgresql-client git \
#    && rm -rf /var/lib/apt/lists/*
#
## Create non-root user early
#RUN useradd -m -u 1000 appuser
#
## Install Poetry for the appuser
#USER appuser
#RUN curl -sSL https://install.python-poetry.org | python3 -
#ENV PATH="/home/appuser/.local/bin:$PATH"
#ENV POETRY_VIRTUALENVS_CREATE=false
#
## Switch back to root to copy files and install deps
#USER root
#
## Copy only dependency files first for better caching
#COPY pyproject.toml poetry.lock* ./
#
## Install Python dependencies as root, then change ownership
#RUN poetry install --no-root && \
#    chown -R appuser:appuser /app
#
## Copy the rest of the backend code
#COPY . .
#RUN chown -R appuser:appuser /app
#
## Switch to non-root user
#USER appuser
#
## Expose dev server port
#EXPOSE 8000
#
## Start Django with auto-reload
#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

ARG PYTHON_VERSION=3.14
ARG ALPINE_VERSION=3.23

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS builder

WORKDIR /build

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    curl

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main
#RUN poetry install --no-root --only main && \
#    find /usr/local -type d -name "__pycache__" -exec rm -rf {} + && \
#    rm -rf /usr/local/lib/python*/site-packages/pip

# ---------------- runtime ----------------

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS runtime

ENV PYTHONUNBUFFERED=1 \
    PATH="${PATH}:/app"

RUN apk add --no-cache libpq

COPY --from=builder /usr/local/ /usr/local/
#COPY --from=builder /usr/lib/libpq.* /usr/lib/

WORKDIR /app
COPY ./ ./

# ---------------- dev ----------------

FROM builder AS dev

RUN poetry install --no-root --with dev

WORKDIR /app
COPY pyproject.toml ./
COPY ./ ./
