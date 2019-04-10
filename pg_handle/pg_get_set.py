import asyncio
import asyncpg
import dotenv
import os

dotenv.load_dotenv()


async def get_pg_connection():
    return await asyncpg.connect(user=os.environ['PG_USER'], password=os.environ['PG_PASSWORD'],
                             database=os.environ['PG_DB'], host=os.environ['PG_HOST'])

