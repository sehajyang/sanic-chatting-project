import asyncio
import asyncpg
import dotenv
import os

dotenv.load_dotenv()


async def get_pg_connection():
    return await asyncpg.connect(user=os.environ['PG_USER'], password=os.environ['PG_PASSWORD'],
                                 database=os.environ['PG_DB'], host=os.environ['PG_HOST'])


async def get_user_password_by_id(id):
    conn = await get_pg_connection()
    row = await conn.fetchrow(
        'SELECT password FROM users WHERE user_id = $1', id
    )
    return row['password']


# TODO: 파라미터 이렇게 넘기지 말 것
async def set_user_data(user_id, name, password):
    conn = await get_pg_connection()
    row = await conn.execute('''
            INSERT INTO users(user_id, password, name) VALUES($1, $2, $3)
            ''', user_id, password, name)
    return row

