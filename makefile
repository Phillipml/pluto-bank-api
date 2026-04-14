POETRY = poetry run

server:
	${POETRY} uvicorn app.main:app --reload

format:
	${POETRY} ruff format .

get_secret_key:
	openssl rand -hex 32

migrations:
	${POETRY} alembic revision --autogenerate -m "transactions decimal and created_at"
	${POETRY} alembic upgrade head

migrate-and-run: migrations
	$(MAKE) server