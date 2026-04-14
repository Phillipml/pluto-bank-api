from decimal import Decimal
from pydantic import BaseModel, Field

from app.schemas.users import UserResponse


class TransactionCreate(BaseModel):
    value: Decimal = Field(gt=-1, max_digits=12, decimal_places=2)
    description: str = Field(min_length=3, max_length=255)


class TransactionsResponse(BaseModel):
    id: int
    user_id: int
    value: Decimal = Field(gt=-1, max_digits=12, decimal_places=2)
    description: str
    user: UserResponse
