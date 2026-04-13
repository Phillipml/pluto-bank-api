from contextlib import asynccontextmanager
from http import HTTPStatus
from fastapi import FastAPI

from app.controllers import health
from app.db import database
from app.schemas.users import UserCreate, UserResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    database.metadata.create_all(database.engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserCreate):
    return user


app.include_router(health.router)
