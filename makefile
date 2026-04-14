POETRY = poetry run

server:
	${POETRY} uvicorn app.main:app --reload

format:
	${POETRY} ruff format .

get_secret_key:
	openssl rand -hex 32