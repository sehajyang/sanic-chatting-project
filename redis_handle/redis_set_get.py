from redis_handle import redis_pub_sub

"""
어떤건 connection 생성하고 어떤건 받아오고 (혼돈)
"""


async def set_hash_data(connection, hash_title, key, value):
    return await connection.hset(hash_title, key, value)


async def get_hash_data_len(hash_title):
    connection = await redis_pub_sub.get_redis_connection()
    return await connection.hlen(hash_title)


async def get_all_hash_title(connection, hash_title):
    return await connection.hkeys(hash_title)


async def get_hash_value_by_key(connection, hash_title, key):
    return await connection.hget(hash_title, key)


async def get_hash_all_value(hash_title):
    connection = await redis_pub_sub.get_redis_connection()
    return await connection.hgetall_asdict(hash_title)


async def get_hash_value(hash_title, key):
    connection = await redis_pub_sub.get_redis_connection()
    return await connection.hget(hash_title, key)


async def del_hash_keys(hash_title, keys):
    connection = await redis_pub_sub.get_redis_connection()
    return await connection.hdel(hash_title, keys)


async def del_hash_title(connection, hash_title):
    return await connection.delete([hash_title])
