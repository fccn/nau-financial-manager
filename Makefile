
PYTHON_PATH_ENV_APP=$(shell which python)

# Define the directories where your code and tests are located
SRC_DIR = src
TEST_DIR = tests

# Define the command to run pytest
TEST_CMD = pytest $(TEST_DIR)

# Define the command to format Python code with Black
LINT_CMD = black $(SRC_DIR) $(TEST_DIR)

# Define the command to run the Django development server
RUN_CMD = poetry run python manage.py runserver

.PHONY: test
test:
	$(TEST_CMD)

.PHONY: lint
lint:
	$(LINT_CMD)

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: run
run:
	$(RUN_CMD)
