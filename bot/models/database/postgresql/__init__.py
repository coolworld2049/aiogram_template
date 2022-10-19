from bot.config import PG_DSN
from bot.models.database.postgresql.model import AsyncPostgresModel

asyncPostgresModel = AsyncPostgresModel(PG_DSN)
