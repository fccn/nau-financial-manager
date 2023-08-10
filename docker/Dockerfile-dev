FROM python:3.11-slim AS base_build

# Create a group and user to run our app
ARG USER=nau-financial-manager

ARG ENV
ENV ENV=${ENV} \
  # build:
  BUILD_ONLY_PACKAGES='' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin"

# System deps:
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  curl \
  git \
  build-essential \
  # Defining build-time-only dependencies:
  $BUILD_ONLY_PACKAGES \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL https://install.python-poetry.org | python - \
  && poetry --version \
  # Removing build-time-only dependencies:
  && apt-get remove -y $BUILD_ONLY_PACKAGES \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

# Setting up proper permissions:
RUN groupadd -r ${USER} && useradd --no-log-init -r -g ${USER} ${USER} \
  && chown ${USER}:${USER} -R /app

# Copy only requirements, to cache them in docker layer
COPY poetry.lock pyproject.toml /app/

# Install packages via poetry:
RUN poetry install --verbose

USER ${USER}:${USER}
