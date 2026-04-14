from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select

import jwt
from app.core.settings import get_settings
from app.db.database import database
from app.schemas import users
from app.schemas.users import UserResponse

oauth2_scheme = OAuth2PasswordBearer("/auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponse:
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    query = select(
        users.c.id,
        users.c.name,
        users.c.email,
        users.c.amount,
    ).where(users.c.id == user_id)
    row = await database.fetch_one(query)
    if row is None:
        raise credentials_exception

    data = dict(row._mapping)
    return UserResponse(
        id=data["id"],
        name=data["name"],
        email=data["email"],
        amount=float(data["amount"]),
    )
