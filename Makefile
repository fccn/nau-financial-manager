
PYTHON_PATH_ENV_APP=$(shell which python)

# Define the directories where your code and tests are located
SRC_DIR = src
TEST_DIR = tests
POETRY_RUN = poetry run

# Define the command to run pytest
TEST_CMD = $(POETRY_RUN) pytest $(TEST_DIR)

# Define the command to format Python code with Black
LINT_CMD = $(POETRY_RUN) black .

PRE_COMMIT = $(POETRY_RUN) pre-commit run --all-files

# Define the command to run the Django development server
RUN_CMD = $(POETRY_RUN) python manage.py runserver

.PHONY: test
test:
	$(TEST_CMD)

.PHONY: lint
lint:
	$(LINT_CMD)

.PHONY: pre-commit
pre-commit:
	$(PRE_COMMIT)

.PHONY: run
run:
	$(RUN_CMD)
