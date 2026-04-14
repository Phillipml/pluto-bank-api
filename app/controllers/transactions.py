from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select, update

from app.core.deps import get_current_user
from app.db.database import database
from app.models.transaction import transactions
from app.models.user import users
from app.schemas.transactions import TransactionRequest, TransactionsResponse
from app.schemas.users import UserResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_transaction(
    body: TransactionRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> dict:
    uid = current_user.id
    value = body.value
    description = body.description or ""

    async with database.transaction():
        upd = (
            update(users)
            .where(users.c.id == uid)
            .where((users.c.amount + value) >= 0)
            .values(amount=users.c.amount + value)
            .returning(
                users.c.id,
                users.c.name,
                users.c.email,
                users.c.amount,
            )
        )
        user_row = await database.fetch_one(upd)
        if user_row is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saldo insuficiente",
            )

        ins = (
            insert(transactions)
            .values(user_id=uid, value=value, description=description)
            .returning(
                transactions.c.id,
                transactions.c.user_id,
                transactions.c.value,
                transactions.c.description,
                transactions.c.created_at,
            )
        )
        tx_row = await database.fetch_one(ins)

    tx = dict(tx_row._mapping)
    u = dict(user_row._mapping)

    return {
        "transaction": TransactionsResponse(
            id=tx["id"],
            user_id=tx["user_id"],
            value=tx["value"],
            description=tx["description"],
            created_at=tx["created_at"],
        ),
        "user": UserResponse(
            id=u["id"],
            name=u["name"],
            email=u["email"],
            amount=float(u["amount"]),
        ),
    }
