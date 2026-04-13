import sqlalchemy as sa
import databases
from app.core.settings import get_settings

database = databases.Database(get_settings().DATABASE_URL)
metadata = sa.MetaData()
engine = sa.create_engine(
    get_settings().DATABASE_URL, connect_args={"check_same_thread": False}
)
