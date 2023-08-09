#Variables
PYTHON_PATH_ENV_APP=$(shell which python)
SRC_DIR = src
TEST_DIR = tests
POETRY_RUN = poetry run
DOCKER_COMPOSE = docker-compose
TEST_CMD = $(POETRY_RUN) python manage.py test
LINT_CMD = $(POETRY_RUN) black .
PRE_COMMIT = $(POETRY_RUN) pre-commit run --all-files
RUN_CMD = $(DOCKER_COMPOSE) -f docker/docker-compose-dev.yml up -d
RUN_DOCKER_DEV = $(DOCKER_COMPOSE) -f docker/docker-compose-dev.yml up -d
KILL_DOCKER_DEV = $(DOCKER_COMPOSE) -f docker/docker-compose-dev.yml down

.PHONY: test  #run tests, all or specific test
test:
	@args="$(filter-out $@,$(MAKECMDGOALS))" && $(TEST_CMD) $${args:-${1}}

.PHONY: lint #use black to format code
lint:
	$(LINT_CMD)

.PHONY: pre-commit #use pre-commit to check best practices
pre-commit:
	$(PRE_COMMIT)

.PHONY: run #run django server in your host
run:
	$(RUN_CMD)

.PHONY: kill #stop django server in your host
kill:
	killall manage.py

.PHONY: run-docker #run django server in docker in dev mode
run-docker:
	$(RUN_DOCKER_DEV)

.PHONY: kill-docker #stop django server in docker in dev mode
kill-docker:
	$(KILL_DOCKER_DEV)
