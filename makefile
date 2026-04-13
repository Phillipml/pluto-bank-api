POETRY = poetry run
server:
	${POETRY} uvicorn app.main:app --reload
format:
	${POETRY} ruff format .