build:
	poetry install
	poetry build

lint:
	poetry run ruff check tests csv_bleach
	poetry run ruff format tests csv_bleach
	poetry run mypy tests csv_bleach

test:
	poetry run pytest tests --cov=csv_bleach --cov-report term-missing --cov-fail-under 100
