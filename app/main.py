from http import HTTPStatus
from fastapi import FastAPI

from app.controllers import health
from app.schemas.users import UserCreate, UserResponse

app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "world"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserCreate):
    return user


app.include_router(health.router)
