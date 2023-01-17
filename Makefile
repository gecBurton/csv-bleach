build:
	poetry install
	poetry build

lint:
	poetry run isort tests csv_bleach
	poetry run black tests csv_bleach
	poetry run flake8 tests csv_bleach

test:
	poetry run pytest tests --cov=csv_bleach --cov-report term-missing --cov-fail-under 100
