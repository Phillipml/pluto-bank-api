from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.controllers import health, user
from app.db.database import database, metadata, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(user.router)
