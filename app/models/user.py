import sqlalchemy as sa
from app.db.database import metadata

user = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(120), nullable=False),
    sa.Column("email", sa.String(120), nullable=False, unique=True),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("amount", sa.Integer, nullable=False, server_default="0"),
    sa.CheckConstraint("amount >= 0", name="check_users_amount_non_negative"),
)
