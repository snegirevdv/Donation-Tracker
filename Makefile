make install:
	pip install poetry
	poetry install

lint:
	poetry run ruff check .

debug:
	poetry run uvicorn app.main:app --reload

run:
	poetry run uvicorn app.main:app
