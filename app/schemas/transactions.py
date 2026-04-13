from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    user_id: int
    value: int
    description: str = Field(min_length=3, max_length=255)


class TransactionsResponse(BaseModel):
    id: int
    user_id: int
    value: int
    description: str
