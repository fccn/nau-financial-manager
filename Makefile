#Variables
PYTHON_PATH_ENV_APP=$(shell which python)
SRC_DIR = src
TEST_DIR = tests
POETRY_RUN = poetry run
DOCKER_COMPOSE = docker-compose
TEST_CMD = $(POETRY_RUN) python manage.py test
LINT_CMD = $(POETRY_RUN) black .
PRE_COMMIT = $(POETRY_RUN) pre-commit run --all-files
RUN_CMD = $(POETRY_RUN) python manage.py runserver
POPULATE_DB = $(POETRY_RUN) python apps/util/populate_db.py
MAKE_MIGRATIONS = $(POETRY_RUN) python manage.py makemigrations
MIGRATE = $(POETRY_RUN) python manage.py migrate
RUN_DOCKER_DEV = $(DOCKER_COMPOSE) -f docker/docker-compose.yml up -d
KILL_DOCKER_DEV = $(DOCKER_COMPOSE) -f docker/docker-compose.yml down


ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

test:  ## run tests, all or specific test
	@args="$(filter-out $@,$(MAKECMDGOALS))" && $(TEST_CMD) $${args:-${1}}
.PHONY: test

lint: ## use black to format code
	$(LINT_CMD)
.PHONY: lint

pre-commit: ## use pre-commit to check best practices
	$(PRE_COMMIT)
.PHONY: pre-commit

run: ## run django server in your host
	$(RUN_CMD)
.PHONY: run

populatedb: ## populate the database initially with fake data
	$(POPULATE_DB)
.PHONY: populatedb

migrations: ## create migrations (app is an option parameter | make migrations {app_name})
	@args="$(filter-out $@,$(MAKECMDGOALS))" && $(MAKE_MIGRATIONS) $${args:-${1}}
.PHONY: migrations

migrate: ## apply all available migrations
	$(MIGRATE)
.PHONY: migrate

kill: ## stop django server in your host
	killall manage.py
.PHONY: kill

run-docker: ## run django server in docker in dev mode
	$(RUN_DOCKER_DEV)
	@echo "The should be running on http://localhost:8000"
.PHONY: run-docker

kill-docker: ## stop django server in docker in dev mode
	$(KILL_DOCKER_DEV)
.PHONY: kill-docker
