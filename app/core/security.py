from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.settings import get_settings

pwd_context = PasswordHash.recommended()

DUMMY_PASSWORD_HASH = pwd_context.hash("password-not-used-for-real-users")


def create_access_token(*, subject: str, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}

    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
