from decimal import Decimal
from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    value: Decimal = Field(max_digits=12, decimal_places=2)
    description: str = Field(min_length=3, max_length=255)


class TransactionsResponse(BaseModel):
    id: int
    user_id: int
    value: Decimal = Field(max_digits=12, decimal_places=2)
    description: str
