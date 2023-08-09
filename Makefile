
PYTHON_PATH_ENV_APP=$(shell which python)

# Define the directories where your code and tests are located
SRC_DIR = src
TEST_DIR = tests
POETRY_RUN = poetry run
DOCKER_COMPOSE = docker-compose

# Define the command to run pytest
TEST_CMD = $(POETRY_RUN) python manage.py test

# Define the command to format Python code with Black
LINT_CMD = $(POETRY_RUN) black .

PRE_COMMIT = $(POETRY_RUN) pre-commit run --all-files

# Define the command to run the Django development server
RUN_CMD = $(DOCKER_COMPOSE) -f docker/docker-compose-dev.yml up -d

RUN_DOCKER_DEV = $(DOCKER_COMPOSE) -f docker/docker-compose-dev.yml up -d

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

.PHONY: stop #stop django server in your host
stop:
	killall manage.py

.PHONY: run-docker-dev #run django server in docker in dev mode
run-docker-dev:
	$(RUN_DOCKER_DEV)
