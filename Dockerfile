# Base image on which to build your application. Ensure that whatever you use
# has a Python installation available.
FROM python:3.11 AS builder

# Install UV tooling. This is a multi-stage build, so the UV tooling is not
# included in the final image. Be sure you update `latest` to a stable version
# to prevent breaking changes from breaking your container builds.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

COPY . /app
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-editable

# Update runner tags with the version of Python you are using
FROM python:3.11-slim AS runner

COPY --from=builder --chown=app:app /app /app
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

ENV ENVIRONMENT=production \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    UVICORN_LOG_CONFIG=/app/src/log_config.yaml \
    UVICORN_WORKERS=1

CMD ["uvicorn", "src.app:app"]
