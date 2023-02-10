check-format:
	poetry run black --check .

format-fix:
	poetry run black .

db-create-revision:
	poetry run alembic revision --autogenerate -m "$(title)"

db-create-migration:
	poetry run alembic --name alembic upgrade head

test:
	poetry run pytest ./tests

lint:
	poetry run mypy --config-file mypy.ini .