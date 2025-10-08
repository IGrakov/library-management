FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system & build dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev postgresql-client git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user early
RUN useradd -m -u 1000 appuser

# Install Poetry for the appuser
USER appuser
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/appuser/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

# Switch back to root to copy files and install deps
USER root

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies as root, then change ownership
RUN poetry install --no-root && \
    chown -R appuser:appuser /app

# Copy the rest of the backend code
COPY . .
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose dev server port
EXPOSE 8000

# Start Django with auto-reload
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]