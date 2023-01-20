build:
	poetry install
	poetry build

lint:
	poetry run isort tests bleach
	poetry run black tests bleach
	poetry run flake8 tests bleach
	poetry run mypy tests bleach

test:
	poetry run pytest tests --cov=bleach --cov-report term-missing --cov-fail-under 100
