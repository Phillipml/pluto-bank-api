from http import HTTPStatus
from warnings import deprecated
from fastapi import APIRouter
from app.db.database import database
from app.schemas.users import UserCreate, UserResponse
from app.models.user import users
from pwdlib import PasswordHash


router = APIRouter(prefix="/users")
pwd_context = PasswordHash.recommended()


@router.get("/", response_model=list[UserResponse])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@router.post("/create", status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(user: UserCreate):
    password_hash = pwd_context.hash(user.password)
    query = (
        users.insert()
        .values(name=user.name, email=user.email, password=password_hash)
        .returning(users.c.id, users.c.name, users.c.email, users.c.amount)
    )
    row = await database.fetch_one(query)
    return dict(row._mapping)
