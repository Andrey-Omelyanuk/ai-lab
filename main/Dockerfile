FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

ARG RELEASE_VERSION
ENV RELEASE_VERSION=$RELEASE_VERSION
LABEL maintainer="omelyanukandrey@gmail.com"
LABEL version="${RELEASE_VERSION}"
LABEL description="AI Lab - Backend Service"

# Install root dependencies
# RUN --mount=type=cache,target=/var/cache/apk \
#     apk update && apk upgrade && \
#     apk add --no-cache curl gcc ffmpeg

# Create user and group for the application
ARG UID=1000
ARG GID=1000
RUN addgroup -g $GID -S app \
 && adduser  -u $UID -S app -G app
USER app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Place executables in the environment at the front of the path
ENV PATH="/home/app/.venv/bin:$PATH"

# ------------------------------------------------------------------------------
FROM base AS dev
# Install the project's dependencies using the lockfile and settings
WORKDIR /home/app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --group dev --group test

WORKDIR /home/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
CMD ["granian", "--interface", "asginl", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ------------------------------------------------------------------------------
# TODO: do not tested yet
FROM base AS prod

# Install the project's dependencies using the lockfile and settings
WORKDIR /home/app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-dev

WORKDIR /home/app/src
CMD ["granian", "--interface", "asgi", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
