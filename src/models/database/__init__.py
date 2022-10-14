from config import PG_DSN
from models.database.model import AsyncPostgresModel

asyncPostgresModel = AsyncPostgresModel(PG_DSN)
