from http import HTTPStatus
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "world"}


@app.post("/users/", status_code=HTTPStatus.CREATED)
def create_user():
    pass
