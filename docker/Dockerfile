#
# Docker image for the nau-financial-manager application.
#

# Define the multi-stage arguments
# those need to be redeclared without default value after each stage (FROM).
ARG NGINX_IMAGE_NAME=nginx
ARG NGINX_IMAGE_TAG=1.20.1
ARG DOCKER_USER=nau-financial-manager
ARG STATIC_ROOT=/nau/nau-financial-manager/static

# ---- Base image ----
FROM python:3.11-slim AS core

# Create a group and user to run our app

ARG DOCKER_USER
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
  pkg-config \
  default-libmysqlclient-dev \
  mycli \
  wait-for-it \
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
RUN groupadd -r ${DOCKER_USER} && \
    useradd --no-log-init -r -g ${DOCKER_USER} ${DOCKER_USER} && \
    chown ${DOCKER_USER}:${DOCKER_USER} -R /app

# Copy only requirements, to cache them in docker layer
COPY poetry.lock pyproject.toml /app/

# Install packages via poetry:
RUN poetry install --verbose

# Gunicorn
RUN mkdir -p /usr/local/etc/gunicorn
COPY ./docker/files/usr/local/etc/gunicorn/app.py /usr/local/etc/gunicorn/app.py

# Copy the default almost empty config.yml for production
COPY ./docker/files/app/config.yml /app/config.yml
ENV FINANCIAL_MANAGER_CFG=/app/config.yml

# Copy the rest of the application files
COPY manage.py /app/
COPY nau_financial_manager /app/nau_financial_manager/
COPY wait-for-mysql.sh /app/
COPY apps /app/apps/

# ---- Static files/links collector ----
FROM core as collector

ARG STATIC_ROOT

# Install rdfind
RUN apt-get update && apt-get install -y rdfind

WORKDIR /app

# Collect static files
RUN SECRET_KEY=any python manage.py collectstatic --noinput

# Replace duplicated file by a symlink to decrease the overall size of the final image
RUN rdfind -makesymlinks true ${STATIC_ROOT}

# ---- Development image ----
FROM core as development

ARG DOCKER_USER

# Install development dependencies
# TODO

# Un-privileged user running the application
USER ${DOCKER_USER}:${DOCKER_USER}

# Run django development server
CMD python manage.py runserver 0.0.0.0:8000

# ---- Production image ----
FROM core as production

ARG DOCKER_USER

# Copy collected symlinks to static files
COPY --from=collector ${STATIC_ROOT} ${STATIC_ROOT}

# Un-privileged user running the application
USER ${DOCKER_USER}:${DOCKER_USER}

ENV GUNICORN_WORKERS=3

# The default command runs gunicorn WSGI server in the sandbox
CMD gunicorn --workers ${GUNICORN_WORKERS} -c /usr/local/etc/gunicorn/app.py nau_financial_manager.wsgi:application

# ---- Nginx ----
FROM ${NGINX_IMAGE_NAME}:${NGINX_IMAGE_TAG} as nginx

ARG STATIC_ROOT

# copy static assets directly to web server image
RUN mkdir -p ${STATIC_ROOT}
COPY --from=collector ${STATIC_ROOT} ${STATIC_ROOT}
