# Define the directories where your code and tests are located
SRC_DIR = src
TEST_DIR = tests

# Define the command to run pytest
TEST_CMD = poetry run pytest $(TEST_DIR)

# Define the command to format Python code with Black
LINT_CMD = poetry run black .

# Define the command to run the Django development server
RUN_CMD = poetry run python manage.py runserver

.PHONY: test
test:
	$(TEST_CMD)

.PHONY: lint
lint:
	$(LINT_CMD)

.PHONY: run
run:
	$(RUN_CMD)
