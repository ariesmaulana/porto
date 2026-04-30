# =============================================
# Stage 1: Builder - install deps & collect static
# =============================================
FROM python:3.13-slim AS builder

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv venv /app/.venv
ENV VIRTUAL_ENV=/app/.venv PATH="/app/.venv/bin:$PATH"
RUN uv sync --frozen --no-dev

# Copy project source
COPY . .

# Collect static files
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV DEBUG=False
RUN python manage.py collectstatic --noinput


# =============================================
# Stage 2: Runtime - minimal production image
# =============================================
FROM python:3.13-slim AS runtime

# Add non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Install runtime system dependencies (libpq for psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy project source from builder
COPY --from=builder /app /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=core.settings

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Run with Granian ASGI server
CMD ["granian", "--host", "0.0.0.0", "--port", "8000", "core.asgi:application"]
