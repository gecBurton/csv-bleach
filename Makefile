build:
	poetry install
	poetry build

lint:
	poetry run ruff check .
	poetry run ruff format .
	poetry run mypy .

test:
	poetry run pytest tests --cov=csv_bleach --cov-report term-missing --cov-fail-under 100
