from pydantic import BaseModel


class UserAuth(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
