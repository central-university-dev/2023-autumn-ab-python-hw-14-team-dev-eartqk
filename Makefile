CODE_FOLDERS := src
TEST_FOLDERS := tests

# Poetry
all: down build up

install:
	poetry install --no-root

update:
	poetry lock
	poetry install --no-root

# Test

test:
	pytest $(TEST_FOLDER) --cov=$(CODE_FOLDERS) -p no:warnings

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

security_checks:
	poetry run bandit -r $(CODE_FOLDERS)
	poetry run flake8 $(CODE_FOLDERS)

# Docker

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

rebuild:
	docker compose up -d --build

start:
	poetry run uvicorn src.social_network.app:app --reload --port 8000

init_db:
	poetry run alembic upgrade heads

create_migration:
	poetry run alembic revision --autogenerate -m $(MIGRATION_NAME)
