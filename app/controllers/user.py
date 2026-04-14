from datetime import timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.core.deps import get_current_user
from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    pwd_context,
)
from app.core.settings import get_settings
from app.db.database import database
from app.models.user import users
from app.schemas.auth import Token
from app.schemas.users import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users() -> list[UserResponse]:
    query = users.select()
    rows = await database.fetch_all(query)
    return [
        UserResponse(
            id=r["id"],
            name=r["name"],
            email=r["email"],
            amount=float(r["amount"]),
        )
        for r in rows
    ]


@router.post("/create", status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    password_hash = pwd_context.hash(user.password)
    query = (
        users.insert()
        .values(name=user.name, email=user.email, password=password_hash)
        .returning(users.c.id, users.c.name, users.c.email, users.c.amount)
    )
    row = await database.fetch_one(query)
    data = dict(row._mapping)
    return UserResponse(
        id=data["id"],
        name=data["name"],
        email=data["email"],
        amount=float(data["amount"]),
    )


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    query = select(users.c.id, users.c.password).where(
        users.c.email == form_data.username
    )
    row = await database.fetch_one(query)

    if row is None:
        pwd_context.verify(form_data.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not pwd_context.verify(form_data.password, row["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(row["id"]),
        expires_delta=expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    return current_user
