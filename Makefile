#Variables
PYTHON_PATH_ENV_APP=$(shell which python)
POETRY = poetry
SRC_DIR = src
TEST_DIR = tests
POETRY_RUN = poetry run
DOCKER_TARGET ?= development
ifeq ($(DOCKER_TARGET), development)
APP_DOCKER_COMMAND='./wait-for-mysql.sh python manage.py runserver 0.0.0.0:8000'
else
APP_DOCKER_COMMAND='gunicorn --workers 3 -c /usr/local/etc/gunicorn/app.py nau_financial_manager.wsgi:application'
endif
# or use in future the 'pytest' directly
TEST_CMD = $(POETRY_RUN) python manage.py test --settings=nau_financial_manager.test
TEST_MYSQL_CMD = $(POETRY_RUN) python manage.py test --settings=nau_financial_manager.test_mysql
# TEST_CMD = $(POETRY_RUN) pytest
LINT_CMD = $(POETRY_RUN) black .
PRE_COMMIT = $(POETRY_RUN) pre-commit run --all-files
RUN_CMD = $(POETRY_RUN) python manage.py runserver
CREATE_TOKEN = $(POETRY_RUN) python manage.py drf_create_token admin
FLUSH_DB = $(POETRY_RUN) python manage.py flush
POPULATE_DB = $(POETRY_RUN) python apps/util/populate_db.py
RESET_MIGRATIONS = find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
MAKE_MIGRATIONS = $(POETRY_RUN) python manage.py makemigrations
MIGRATE = $(POETRY_RUN) python manage.py migrate
COMPOSE_FILE := docker/docker-compose-dependencies.yml
RUN_APP ?= true
ifeq ($(RUN_APP), true)
	COMPOSE_FILE := $(COMPOSE_FILE):docker/docker-compose-app.yml
endif
DOCKER_COMPOSE = APP_DOCKER_COMMAND=$(APP_DOCKER_COMMAND) DOCKER_TARGET=$(DOCKER_TARGET) COMPOSE_FILE=$(COMPOSE_FILE) docker-compose
RUN_DOCKER_DEV = $(DOCKER_COMPOSE) up -d --remove-orphans
STOP_DOCKER_DEV = $(DOCKER_COMPOSE) down
KILL_DOCKER_DEV = $(DOCKER_COMPOSE) kill
BUILD_DOCKER_DEV = $(DOCKER_COMPOSE) build
LOGS_DOCKER_DEV = $(DOCKER_COMPOSE) logs
PRUNE_DOCKER = docker system prune -af
CREATESUPERUSER = $(POETRY_RUN) python manage.py add_superuser --no-input --settings=nau_financial_manager.settings


ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

test:  ## run tests, all or a specific test, example: 'make test apps.billing.tests.test_invoice_host_service' or 'pytest apps/billing/tests/test_invoice_host_service.py -k test_get_document_transaction_not_found'
	@args="$(filter-out $@,$(MAKECMDGOALS))" && $(TEST_CMD) $${args:-${1}}
.PHONY: test

test-mysql:  ## run tests, all or a specific test, example: 'make test apps.billing.tests.test_invoice_host_service' or 'pytest apps/billing/tests/test_invoice_host_service.py -k test_get_document_transaction_not_found'
	@args="$(filter-out $@,$(MAKECMDGOALS))" && $(TEST_MYSQL_CMD) $${args:-${1}}
.PHONY: test-mysql

lint: ## use black to format code
	$(LINT_CMD)
.PHONY: lint

pre-commit: ## use pre-commit to check best practices
	$(PRE_COMMIT)
.PHONY: pre-commit

run: ## run DB's inside docker and run django server in your host
	RUN_APP=false make run-docker
	$(RUN_CMD)
.PHONY: run

run-app: ## run django server in your host
	$(RUN_DOCKER_DEV)
	$(RUN_CMD)
.PHONY: run-app

populate: ## populate the database initially with fake data
	$(POPULATE_DB)
.PHONY: populate

reset-migrations: ## reset all migrations from all apps
	$(RESET_MIGRATIONS)
.PHONY: reset-migrations

migrations: ## create migrations (app is an option parameter | make migrations {app_name})
	@args="$(filter-out $@,$(MAKECMDGOALS))" && $(MAKE_MIGRATIONS) $${args:-${1}}
.PHONY: migrations

migrate: ## apply all available migrations
	$(MIGRATE)
.PHONY: migrate

flush: ## delete all data from database
	$(FLUSH_DB) --noinput
.PHONY: flush

superuser: ## create django super user admin (username and password are option parameters | make superuser {username} {password})
	 @args="$(filter-out $@,$(MAKECMDGOALS))" && $(CREATESUPERUSER) $${args:+--username=$${args%% *} --password=$${args##* }}
.PHONY: superuser

run-docker: ## run django server in docker in dev mode
	$(BUILD_DOCKER_DEV)
	$(RUN_DOCKER_DEV)
ifeq ($(RUN_APP), true)
	@echo "The app should be running on 8000 port and you can access it from nginx on http://localhost:8081"
endif
.PHONY: run-docker

stop-docker: ## stop docker containers
	$(STOP_DOCKER_DEV)
.PHONY: stop

kill: ## stop django server in your host
	killall manage.py || echo "Couldn't find the app to kill"
.PHONY: kill

kill-docker: ## stop django server in docker in dev mode
	$(KILL_DOCKER_DEV)
.PHONY: kill-docker

stop: | stop-docker kill kill-docker ## stop everything
	@echo "Everything stopped or killed"
.PHONY: stop

hr-docker: ## remake complete docker environment (destroy dockers, prune docker, create dockers, migrate, superuser, populate)
	$(MAKE) kill-docker
	$(PRUNE_DOCKER)
	$(RUN_DOCKER_DEV)
	@echo "Waiting for MySQL server to start..."
	docker logs -f nau-database-mysql 2>&1 | grep -q "/usr/sbin/mysqld: ready for connections. Version: '8.1.0'  socket: '/var/run/mysqld/mysqld.sock'" && sleep 15 && echo "MySQL server is ready"
	$(MAKE) migrate
	$(MAKE) superuser
	$(MAKE) populate
.PHONY: hr-docker

create-token: ## create token for admin user
	$(CREATE_TOKEN)
.PHONY: create-token

install-poetry: ## Install Poetry
	@echo "Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | python -
.PHONY: install-poetry

install-packages: ## Install project dependencies
	@echo "Installing project dependencies..."
	@$(POETRY) install
.PHONY: install-packages

logs: ## display docker app logs (follow mode)
	@$(LOGS_DOCKER_DEV) -f nau-financial-app
.PHONY: logs

run-database: ## Run database in docker
	@echo "Running database..."
	@$(DOCKER_COMPOSE) -f docker/docker-compose-dependencies.yml up -d database-mysql
.PHONY: run-database
