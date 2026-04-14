import sqlalchemy as sa
from app.db.database import metadata

transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column(
        "user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True
    ),
    sa.Column("value", sa.Numeric(12, 2), nullable=False),
    sa.Column("description", sa.String(255), nullable=False, server_default=""),
)
