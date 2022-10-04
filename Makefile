test:
	isort tests csv_bleach
	black tests csv_bleach
	flake8 tests csv_bleach
	# mypy tests csv_bleach
	pytest tests --cov=csv_bleach --cov-report term-missing
