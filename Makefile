CODE_FOLDERS := src
TEST_FOLDERS := tests

# Poetry

install:
	poetry install --no-root

update:
	poetry lock
	poetry install --no-root

# Test

test:
	pytest $(TEST_FOLDER) --cov=$(CODE_FOLDERS)

# Lint

format:
	ruff check --fix .
	ruff format .
	black . -S

lint:
	ruff check .
	black --check .
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS)

# Docker

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

rebuild:
	docker compose up -d --build

start:
	poetry run uvicorn src.social_network.app:app --reload --port 8000
