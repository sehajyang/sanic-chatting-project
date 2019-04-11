import asyncio
import asyncpg
import dotenv
import os

dotenv.load_dotenv()


async def get_pg_connection():
    return await asyncpg.connect(user=os.environ['PG_USER'], password=os.environ['PG_PASSWORD'],
                                 database=os.environ['PG_DB'], host=os.environ['PG_HOST'])


async def get_user_password_by_id(id):
    return await get_pg_connection().fetch(
        'SELECT * FROM users WHERE id = $id', id
        )


# TODO: 파라미터 이렇게 넘기지 말 것
async def set_user_data(id, name ,password):
    return await get_pg_connection().execute('''
        INSERT INTO users VALUES ($id), ($password), ($name)
        ''', id, password, name)
