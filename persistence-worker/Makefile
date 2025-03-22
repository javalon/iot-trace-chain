POETRY=POETRY
POETRY_RUN=$(POETRY) run

SOURCE_FILES=$(shell find persistence_worker -name '*.py' -not -path **/.venv/**)
SOURCE_FOLDER=persistence_worker
TEST_FOLDER=tests
DATE=$(shell date +'%Y-%m-%d %H:%M:%S')

.PHONY: all start start-local start-local-profiling tests lint format clear-cache publish-message lint-fix

start:
	$(POETRY_RUN) python $(SOURCE_FOLDER)/__main__.py

start-local:
	@echo "🚀 Starting the application in local mode..."
	$(POETRY_RUN) poe start-local

start-local-profiling:
	$(POETRY_RUN) poe start-local-profiling

publish-message:
	$(POETRY_RUN) poe publish-message

tests:
	$(POETRY_RUN) pytest

lint:
	$(POETRY_RUN) ruff check $(SOURCE_FOLDER) $(TEST_FOLDER)
	$(POETRY_RUN) ruff format $(SOURCE_FOLDER) $(TEST_FOLDER)
	
lint-fix:
	$(POETRY_RUN) ruff check $(SOURCE_FOLDER) $(TEST_FOLDER) --fix

format:
	$(POETRY_RUN) black $(SOURCE_FOLDER) $(TEST_FOLDER) --check

clear-cache:
	@echo "🧹 Clearing Python cache..."
	find . -type d -name '__pycache__' -name '.pytest_cache' -name '.ruff_cache' -exec rm -r {} + -o -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

.DEFAULT_GOAL := start-local
